"""Construccion del prompt y del esquema JSON de salida.

Blindaje: este modulo NO importa ni lee ninguna anotacion humana. Solo recibe el
manual de codificacion (literal) y el titulo + texto del resumen.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

# Envoltorio minimo. No define ni reformula ninguna categoria: todo eso esta en el manual.
SYSTEM_WRAPPER = (
    "Eres un anotador. Aplica el siguiente protocolo de anotación, tal como está escrito, "
    "al resumen de tesis que se te entregue. Devuelve únicamente un objeto JSON con los "
    "campos del protocolo.\n\n<protocolo>\n{protocol}\n</protocolo>"
)

USER_TEMPLATE = (
    "Título: {title}\n\nResumen:\n{text}\n\n"
    "Anota este resumen según el protocolo. Responde solo con el JSON."
)


def load_protocol(path: Path, strip_sections: list[str] | None = None) -> str:
    """Devuelve el manual literal, opcionalmente sin las secciones indicadas por prefijo."""
    text = Path(path).read_text(encoding="utf-8")
    if not strip_sections:
        return text
    parts = re.split(r"(?m)^(?=## )", text)
    kept = [p for p in parts if not any(p.startswith(pref) for pref in strip_sections)]
    return "".join(kept)


def build_system(protocol_text: str) -> str:
    return SYSTEM_WRAPPER.format(protocol=protocol_text)


def build_user(title: str, text: str) -> str:
    return USER_TEMPLATE.format(title=(title or "").strip(), text=(text or "").strip())


def build_schema(variable_specs: dict[str, dict], include_notes: bool = True) -> dict:
    """Esquema JSON estricto: un campo por variable del manual, mismos nombres.

    Todas las variables admiten null (el manual manda dejar campos vacios en dos
    situaciones: D4 cuando no_evaluable = 1, y todo cuando el texto no es un
    resumen). `no_evaluable` es obligatorio y no nulo.
    """
    props: dict[str, dict] = {}
    for name, spec in variable_specs.items():
        levels = list(spec["levels"])
        if name == "no_evaluable":
            props[name] = {"type": "integer", "enum": levels}
        else:
            props[name] = {"type": ["integer", "null"], "enum": levels + [None]}
    if include_notes:
        # Al final del objeto para que se genere DESPUES de las etiquetas.
        props["observaciones"] = {"type": "string"}
    return {
        "type": "object",
        "properties": props,
        "required": list(props.keys()),
        "additionalProperties": False,
    }


def validate_output(obj: object, schema: dict) -> list[str]:
    """Validacion manual contra el esquema (sin dependencias). Devuelve lista de errores."""
    errs: list[str] = []
    if not isinstance(obj, dict):
        return [f"no es un objeto JSON: {type(obj).__name__}"]
    props = schema["properties"]
    for k in schema["required"]:
        if k not in obj:
            errs.append(f"falta '{k}'")
    for k, v in obj.items():
        if k not in props:
            errs.append(f"campo inesperado '{k}'")
            continue
        spec = props[k]
        if "enum" in spec:
            # bool es subclase de int en Python: se rechaza explicitamente
            if isinstance(v, bool) or v not in spec["enum"]:
                errs.append(f"'{k}'={v!r} fuera de {spec['enum']}")
        elif spec.get("type") == "string" and not isinstance(v, str):
            errs.append(f"'{k}' debe ser texto")
    return errs


def prompt_fingerprint(system: str, schema: dict) -> str:
    """Hash corto del prompt fijo, para registrar en el metodo que prompt se uso."""
    import json
    h = hashlib.sha256()
    h.update(system.encode("utf-8"))
    h.update(json.dumps(schema, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    return h.hexdigest()[:16]
