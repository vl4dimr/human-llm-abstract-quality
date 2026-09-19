"""Adaptadores de proveedor. Todos exponen la misma llamada:

    complete(system, user, schema, temperature, seed, max_tokens) -> ProviderResult

Cada adaptador solo se importa/instancia si se usa, para no exigir todos los SDK.
Las claves se leen SIEMPRE de variables de entorno, nunca del config ni del codigo.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field


@dataclass
class ProviderResult:
    text: str                      # cuerpo devuelto (deberia ser JSON)
    model_reported: str            # version/digest que el proveedor dice haber usado
    usage: dict = field(default_factory=dict)   # input_tokens, output_tokens, cache_read_tokens...
    latency_s: float = 0.0
    raw: dict = field(default_factory=dict)     # respuesta completa serializable, para el cache
    supports_temperature: bool = True
    supports_seed: bool = True


class Provider:
    name = "base"

    def __init__(self, spec: dict):
        self.spec = spec
        self.model = spec["model"]

    def complete(self, system: str, user: str, schema: dict, temperature: float,
                 seed: int, max_tokens: int) -> ProviderResult:
        raise NotImplementedError

    def describe(self) -> dict:
        """Metadatos fijos del modelo para el registro del metodo."""
        return {"provider": self.name, "model": self.model}


# --------------------------------------------------------------------------- #
class OllamaProvider(Provider):
    """API nativa de Ollama (/api/chat). Local, sin clave.

    Se usa la API nativa y no la compatible con OpenAI porque solo la nativa permite
    fijar `num_ctx`: con el valor por defecto (4096) el manual se truncaria en silencio.
    """
    name = "ollama"

    def __init__(self, spec: dict):
        super().__init__(spec)
        self.base_url = spec.get("base_url", "http://localhost:11434").rstrip("/")
        self.options = dict(spec.get("options", {}))
        self.keep_alive = spec.get("keep_alive", "30m")

    def _post(self, path: str, payload: dict, timeout: int = 600) -> dict:
        req = urllib.request.Request(
            self.base_url + path, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))

    def describe(self) -> dict:
        d = super().describe()
        try:
            info = self._post("/api/show", {"model": self.model}, timeout=30)
            d["digest"] = (info.get("details") or {}).get("digest") or info.get("digest")
            d["details"] = info.get("details")
            mi = info.get("model_info") or {}
            ctx = [v for k, v in mi.items() if k.endswith(".context_length")]
            d["context_length"] = ctx[0] if ctx else None
        except Exception as e:  # noqa: BLE001
            d["error"] = f"no se pudo consultar /api/show: {e}"
        return d

    def complete(self, system, user, schema, temperature, seed, max_tokens) -> ProviderResult:
        options = {**self.options, "seed": seed, "num_predict": max_tokens}
        if temperature is not None:          # None = temperature por defecto del modelo
            options["temperature"] = temperature
        payload = {
            "model": self.model, "stream": False, "format": schema,
            "keep_alive": self.keep_alive, "options": options,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
        }
        if "think" in self.spec:             # modelos con modo de razonamiento (qwen3, deepseek-r1)
            payload["think"] = bool(self.spec["think"])
        t0 = time.time()
        try:
            resp = self._post("/api/chat", payload)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            raise RuntimeError(f"ollama HTTP {e.code}: {body[:400]}") from None
        lat = time.time() - t0
        n_in = resp.get("prompt_eval_count")
        # Ollama trunca el prompt EN SILENCIO si no cabe en num_ctx: el modelo veria
        # un manual cortado y la anotacion seria invalida sin que nada lo indicase.
        # Se exige margen para el prompt y la respuesta completa.
        num_ctx = self.options.get("num_ctx")
        if num_ctx and n_in and n_in + max_tokens > num_ctx:
            raise RuntimeError(
                f"prompt de {n_in} tokens + {max_tokens} de salida no caben en num_ctx={num_ctx}: "
                f"Ollama habria truncado el manual. Sube num_ctx o baja max_output_tokens.")
        usage = {"input_tokens": n_in,
                 "output_tokens": resp.get("eval_count"),
                 "total_duration_s": (resp.get("total_duration") or 0) / 1e9}
        return ProviderResult(text=resp["message"]["content"], model_reported=resp.get("model", self.model),
                              usage=usage, latency_s=lat, raw=resp)


# --------------------------------------------------------------------------- #
class OpenAICompatibleProvider(Provider):
    """Cualquier endpoint compatible con la API de chat de OpenAI.

    Cubre OpenAI, Groq, Together, OpenRouter, Mistral, DeepSeek, Cerebras, etc.
    `json_mode`: 'schema' (response_format json_schema estricto) u 'object'
    (solo JSON valido; para endpoints que no soportan json_schema).
    """
    name = "openai_compatible"

    def __init__(self, spec: dict):
        super().__init__(spec)
        from openai import OpenAI  # import perezoso
        key_env = spec.get("api_key_env", "OPENAI_API_KEY")
        key = os.environ.get(key_env)
        if not key:
            raise RuntimeError(f"variable de entorno {key_env} no definida")
        self.client = OpenAI(api_key=key, base_url=spec.get("base_url"))
        self.json_mode = spec.get("json_mode", "schema")
        self.extra = dict(spec.get("extra", {}))

    def complete(self, system, user, schema, temperature, seed, max_tokens) -> ProviderResult:
        if self.json_mode == "schema":
            rf = {"type": "json_schema",
                  "json_schema": {"name": "anotacion", "schema": schema, "strict": True}}
        else:
            rf = {"type": "json_object"}
        kw = {}
        if temperature is not None:
            kw["temperature"] = temperature
        t0 = time.time()
        resp = self.client.chat.completions.create(
            model=self.model, seed=seed, max_tokens=max_tokens, response_format=rf, **kw,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            **self.extra,
        )
        lat = time.time() - t0
        u = resp.usage
        usage = {"input_tokens": getattr(u, "prompt_tokens", None),
                 "output_tokens": getattr(u, "completion_tokens", None)}
        cached = getattr(getattr(u, "prompt_tokens_details", None), "cached_tokens", None)
        if cached is not None:
            usage["cache_read_tokens"] = cached
        return ProviderResult(text=resp.choices[0].message.content or "",
                              model_reported=resp.model, usage=usage, latency_s=lat,
                              raw=json.loads(resp.model_dump_json()))


# --------------------------------------------------------------------------- #
class GoogleProvider(Provider):
    """Gemini via google-genai. NO VERIFICADO aun con una clave real."""
    name = "google"

    def __init__(self, spec: dict):
        super().__init__(spec)
        from google import genai  # import perezoso
        key_env = spec.get("api_key_env", "GOOGLE_API_KEY")
        key = os.environ.get(key_env)
        if not key:
            raise RuntimeError(f"variable de entorno {key_env} no definida")
        self.client = genai.Client(api_key=key)

    def complete(self, system, user, schema, temperature, seed, max_tokens) -> ProviderResult:
        from google.genai import types
        cfg = types.GenerateContentConfig(
            system_instruction=system, seed=seed,
            **({"temperature": temperature} if temperature is not None else {}),
            max_output_tokens=max_tokens, response_mime_type="application/json",
            response_json_schema=schema,
        )
        t0 = time.time()
        resp = self.client.models.generate_content(model=self.model, contents=user, config=cfg)
        lat = time.time() - t0
        um = getattr(resp, "usage_metadata", None)
        usage = {"input_tokens": getattr(um, "prompt_token_count", None),
                 "output_tokens": getattr(um, "candidates_token_count", None),
                 "cache_read_tokens": getattr(um, "cached_content_token_count", None)}
        return ProviderResult(text=resp.text or "", model_reported=getattr(resp, "model_version", self.model),
                              usage=usage, latency_s=lat, raw=resp.model_dump(mode="json"))


# --------------------------------------------------------------------------- #
class AnthropicProvider(Provider):
    """Claude via SDK oficial, salida estructurada con output_config.format.

    Limitaciones documentadas (Claude Opus 5 / Sonnet 5): `temperature` devuelve 400 y no
    existe `seed`; el razonamiento adaptativo va activado por defecto. Las corridas
    solo difieren por el muestreo interno del modelo. El manual se cachea (prefijo).
    """
    name = "anthropic"

    def __init__(self, spec: dict):
        super().__init__(spec)
        import anthropic  # import perezoso
        self.client = anthropic.Anthropic()  # credenciales desde el entorno

    def complete(self, system, user, schema, temperature, seed, max_tokens) -> ProviderResult:
        t0 = time.time()
        resp = self.client.messages.create(
            model=self.model, max_tokens=max_tokens,
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
            messages=[{"role": "user", "content": user}],
            output_config={"format": {"type": "json_schema", "schema": schema}},
        )
        lat = time.time() - t0
        if resp.stop_reason == "refusal":
            raise RuntimeError(f"anthropic refusal: {getattr(resp, 'stop_details', None)}")
        text = next((b.text for b in resp.content if b.type == "text"), "")
        u = resp.usage
        usage = {"input_tokens": u.input_tokens, "output_tokens": u.output_tokens,
                 "cache_read_tokens": getattr(u, "cache_read_input_tokens", 0) or 0,
                 "cache_write_tokens": getattr(u, "cache_creation_input_tokens", 0) or 0}
        return ProviderResult(text=text, model_reported=resp.model, usage=usage, latency_s=lat,
                              raw=json.loads(resp.model_dump_json()),
                              supports_temperature=False, supports_seed=False)


PROVIDERS = {
    "ollama": OllamaProvider,
    "openai_compatible": OpenAICompatibleProvider,
    "google": GoogleProvider,
    "anthropic": AnthropicProvider,
}


def make_provider(spec: dict) -> Provider:
    kind = spec.get("provider")
    if kind not in PROVIDERS:
        raise ValueError(f"proveedor desconocido: {kind!r}; validos: {sorted(PROVIDERS)}")
    if not spec.get("model"):
        raise ValueError(f"modelo '{spec.get('name')}' ({kind}): falta el ID exacto del modelo")
    return PROVIDERS[kind](spec)
