"""Fase 2 - Anotacion con LLMs.

- El prompt contiene el manual de codificacion LITERAL (data/raw/scheme/...).
- Blindaje: este script no abre ningun archivo de anotaciones humanas. Solo lee
  data/interim/documents.csv (titulo + texto) y data/processed/subset.csv (ids).
- Salida JSON con esquema estricto; hasta `max_parse_retries` reintentos por fallo
  de parseo, cada fallo queda registrado.
- N corridas por modelo (config llm.runs), cada llamada cacheada por hash en disco.
- Barra de progreso con coste acumulado y tiempo restante.

Uso:
  python src/02_annotate_llm.py --dry-run                 # sin llamadas: prompts, tamanos, coste estimado
  python src/02_annotate_llm.py --ollama mistral:latest --limit 2 --runs r1   # prueba de humo local
  python src/02_annotate_llm.py                           # todos los modelos de config.yaml
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib.io_raw import load_config, variable_specs  # noqa: E402
from lib.llm.cache import CallCache, call_key  # noqa: E402
from lib.llm.prompt import (build_schema, build_system, build_user, load_protocol,  # noqa: E402
                            prompt_fingerprint, validate_output)
from lib.llm.providers import make_provider  # noqa: E402
from lib.logging_utils import get_logger  # noqa: E402

cfg = load_config()


def load_dotenv(path: Path) -> None:
    """Carga KEY=VALUE de .env (ignorado por git) sin pisar variables ya definidas."""
    import os
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_dotenv(ROOT / ".env")
SPECS = variable_specs(cfg)
VARS = list(SPECS)
RAW = ROOT / cfg["paths"]["raw"]
INTERIM = ROOT / cfg["paths"]["interim"]
PROCESSED = ROOT / cfg["paths"]["processed"]
LOGS = ROOT / cfg["paths"]["logs"]
L = cfg["llm"]
log = get_logger("02_annotate_llm", LOGS)


# --------------------------------------------------------------------------- #
def load_documents(which: str) -> pd.DataFrame:
    docs = pd.read_csv(INTERIM / "documents.csv", encoding="utf-8")
    if which == "subset":
        sub_path = PROCESSED / "subset.csv"
        if not sub_path.exists():
            raise SystemExit("falta data/processed/subset.csv: ejecuta antes src/00b_select_subset.py")
        ids = pd.read_csv(sub_path)["doc_id"]
        docs = docs[docs["doc_id"].isin(ids)]
    docs = docs[["doc_id", "title", "text"]].dropna(subset=["text"]).sort_values("doc_id")
    if docs.empty:
        raise SystemExit("no hay documentos con texto")
    return docs.reset_index(drop=True)


def price_of(model_name: str, usage: dict) -> float:
    p = (L.get("pricing_usd_per_mtok") or {}).get(model_name)
    if not p:
        return 0.0
    cost = 0.0
    cost += (usage.get("input_tokens") or 0) * p.get("input", 0) / 1e6
    cost += (usage.get("output_tokens") or 0) * p.get("output", 0) / 1e6
    cost += (usage.get("cache_read_tokens") or 0) * (p.get("cache_read", 0) - p.get("input", 0)) / 1e6
    cost += (usage.get("cache_write_tokens") or 0) * (p.get("cache_write", 0) - p.get("input", 0)) / 1e6
    return max(cost, 0.0)


def retry_delay(exc: Exception, n: int) -> tuple[float, bool]:
    """Espera antes de reintentar un error de proveedor. Devuelve (segundos, fatal).

    Respeta la cabecera `retry-after` si existe (cuotas por minuto/dia de las capas
    gratuitas). Si supera `max_retry_wait_s` se declara fatal: mejor parar y reanudar
    desde el cache que quemar reintentos en todos los documentos.
    """
    cap = float(L.get("max_retry_wait_s", 900))
    ra = None
    resp = getattr(exc, "response", None)
    headers = getattr(resp, "headers", None)
    if headers is not None:
        raw = headers.get("retry-after") or headers.get("Retry-After")
        try:
            ra = float(raw) if raw is not None else None
        except ValueError:
            ra = None
    if ra is not None:
        return (ra + 1.0, False) if ra <= cap else (ra, True)
    return (min(5.0 * 2 ** n, 120.0), False)


def try_parse(text: str, schema: dict) -> tuple[dict | None, list[str]]:
    """Parsea y valida. Tolera un bloque ```json ... ``` alrededor."""
    t = text.strip()
    if t.startswith("```"):
        t = t.strip("`")
        if t.lower().startswith("json"):
            t = t[4:]
    try:
        obj = json.loads(t)
    except json.JSONDecodeError as e:
        return None, [f"JSON invalido: {e}"]
    errs = validate_output(obj, schema)
    return (obj if not errs else None), errs


# --------------------------------------------------------------------------- #
def run_model(mspec: dict, docs: pd.DataFrame, system: str, schema: dict, runs: list[dict],
              fingerprint: str, dry_run: bool) -> dict:
    name = mspec["name"]
    cache = CallCache(ROOT / L["cache_dir"], name)
    stats = {"model": name, "calls_made": 0, "cache_hits": 0, "parse_failures": 0,
             "hard_failures": 0, "cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0}
    provider = None
    if not dry_run:
        provider = make_provider(mspec)
        desc = provider.describe()
        desc.update({"name": name, "prompt_fingerprint": fingerprint,
                     "started_utc": datetime.now(timezone.utc).isoformat(), "runs": runs})
        (LOGS / f"llm_model_{name}_{datetime.now():%Y%m%dT%H%M%S}.json").write_text(
            json.dumps(desc, ensure_ascii=False, indent=2), encoding="utf-8")
        log.info("modelo %s: %s", name, json.dumps(desc, ensure_ascii=False)[:400])
    min_interval = float(mspec.get("min_interval_s", 0))

    todo = [(r, d) for r in runs for d in docs.itertuples(index=False)]
    bar = tqdm(todo, desc=name, unit="call", dynamic_ncols=True)
    last_call = 0.0
    for run, d in bar:
        user = build_user(d.title, d.text)
        key = call_key(mspec["provider"], mspec["model"], system, user, schema,
                       run["name"], run["temperature"], int(run["seed"]))
        rec = cache.get(key)
        if rec and rec.get("parse_ok"):
            stats["cache_hits"] += 1
            continue
        if dry_run:
            continue

        parsed, errs, attempts, result = None, [], 0, None
        net_errors, fatal = 0, False
        # Dos contadores: `attempts` = respuestas recibidas que no parsean (max_parse_retries);
        # `net_errors` = errores de red/cuota del proveedor (max_provider_retries).
        while parsed is None and attempts < int(L["max_parse_retries"]) \
                and net_errors < int(L.get("max_provider_retries", 5)):
            wait = min_interval - (time.time() - last_call)
            if wait > 0:
                time.sleep(wait)
            try:
                temp = None if run["temperature"] is None else float(run["temperature"])
                result = provider.complete(system, user, schema, temp,
                                           int(run["seed"]) + attempts,
                                           int(mspec.get("max_output_tokens", L["max_output_tokens"])))
            except Exception as e:  # noqa: BLE001
                net_errors += 1
                last_call = time.time()
                delay, fatal = retry_delay(e, net_errors)
                log.error("%s %s %s: error de proveedor (%d): %s", name, run["name"], d.doc_id, net_errors, e)
                if fatal:
                    break
                log.info("reintento en %.0f s", delay)
                time.sleep(delay)
                continue
            attempts += 1
            last_call = time.time()
            stats["calls_made"] += 1
            stats["input_tokens"] += result.usage.get("input_tokens") or 0
            stats["output_tokens"] += result.usage.get("output_tokens") or 0
            stats["cost_usd"] += price_of(name, result.usage)
            parsed, errs = try_parse(result.text, schema)
            if parsed is None:
                stats["parse_failures"] += 1
                log.warning("%s %s %s intento %d: fallo de parseo: %s | texto: %s",
                            name, run["name"], d.doc_id, attempts, errs, result.text[:200].replace("\n", " "))
                cache.put(f"{key}_fail{attempts}", {
                    "doc_id": d.doc_id, "run": run["name"], "attempt": attempts, "parse_ok": False,
                    "errors": errs, "text": result.text, "usage": result.usage, "raw": result.raw})
        if fatal:
            stats["hard_failures"] += 1
            log.error("%s: cuota agotada (retry-after supera %s s). Se detiene este modelo; "
                      "relanzar mas tarde reanuda desde el cache.", name, L.get("max_retry_wait_s", 900))
            break
        if parsed is None:
            stats["hard_failures"] += 1
            log.error("%s %s %s: SIN RESULTADO tras %d respuestas / %d errores", name, run["name"],
                      d.doc_id, attempts, net_errors)
            continue
        cache.put(key, {
            "doc_id": d.doc_id, "model_name": name, "provider": mspec["provider"], "model": mspec["model"],
            "model_reported": result.model_reported, "run": run["name"],
            "temperature": run["temperature"], "seed": run["seed"], "attempts": attempts,
            "parse_ok": True, "output": parsed, "text": result.text, "usage": result.usage,
            "latency_s": result.latency_s, "prompt_fingerprint": fingerprint,
            "called_at_utc": datetime.now(timezone.utc).isoformat(), "raw": result.raw,
        })
        bar.set_postfix(cost=f"${stats['cost_usd']:.3f}", fails=stats["hard_failures"], refresh=False)
    bar.close()
    return stats


def collect(model_names: list[str], docs: pd.DataFrame, runs: list[dict]) -> None:
    """Reune el cache en formato largo canonico + observaciones + registro de llamadas."""
    ids = set(docs["doc_id"])
    long_rows, note_rows, call_rows = [], [], []
    for name in model_names:
        cdir = ROOT / L["cache_dir"] / name
        if not cdir.exists():
            continue
        for p in cdir.glob("*.json"):
            if "_fail" in p.name:
                continue
            rec = json.loads(p.read_text(encoding="utf-8"))
            if not rec.get("parse_ok") or rec["doc_id"] not in ids:
                continue
            ann = f"{name}#{rec['run']}"
            out = rec["output"]
            for v in VARS:
                if out.get(v) is not None:
                    long_rows.append({"doc_id": rec["doc_id"], "annotator": ann, "category": v, "label": int(out[v])})
            if out.get("observaciones"):
                note_rows.append({"doc_id": rec["doc_id"], "annotator": ann, "notes": out["observaciones"]})
            call_rows.append({"doc_id": rec["doc_id"], "annotator": ann, "model": rec["model"],
                              "model_reported": rec.get("model_reported"), "attempts": rec["attempts"],
                              "input_tokens": rec["usage"].get("input_tokens"),
                              "output_tokens": rec["usage"].get("output_tokens"),
                              "latency_s": round(rec.get("latency_s", 0), 2),
                              "called_at_utc": rec.get("called_at_utc"),
                              "prompt_fingerprint": rec.get("prompt_fingerprint")})
    PROCESSED.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(long_rows).sort_values(["annotator", "doc_id", "category"]).to_csv(
        PROCESSED / "llm_annotations.csv", index=False, encoding="utf-8")
    pd.DataFrame(note_rows).to_csv(PROCESSED / "llm_notes.csv", index=False, encoding="utf-8")
    pd.DataFrame(call_rows).to_csv(PROCESSED / "llm_calls.csv", index=False, encoding="utf-8")
    if long_rows:
        cov = pd.DataFrame(long_rows).groupby("annotator")["doc_id"].nunique()
        log.info("cobertura por anotador LLM:\n%s", cov.to_string())
    log.info("escrito %s (%d filas), llm_notes.csv, llm_calls.csv", PROCESSED / "llm_annotations.csv", len(long_rows))


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="no llama a ningun proveedor")
    ap.add_argument("--limit", type=int, default=None, help="solo los N primeros documentos")
    ap.add_argument("--runs", default=None, help="corridas a ejecutar, p.ej. r1 o r1,r2")
    ap.add_argument("--models", default=None, help="nombres de modelos del config, separados por coma")
    ap.add_argument("--ollama", default=None, help="atajo: modelo local de Ollama (p.ej. mistral:latest)")
    ap.add_argument("--docs", default="subset", choices=["subset", "all"])
    ap.add_argument("--collect-only", action="store_true",
                    help="solo reune el cache existente en data/processed/ (sin llamadas)")
    args = ap.parse_args()
    if args.collect_only:
        docs = load_documents(args.docs)
        collect(sorted(m["name"] for m in (L.get("models") or [])), docs, list(L["runs"]))
        return 0

    docs = load_documents(args.docs)
    if args.limit:
        docs = docs.head(args.limit)
    protocol = load_protocol(RAW / L["prompt"]["protocol_file"], L["prompt"].get("strip_sections"))
    system = build_system(protocol)
    schema = build_schema(SPECS, bool(L.get("include_notes", True)))
    fp = prompt_fingerprint(system, schema)

    # Registro literal del prompt usado (parte del metodo).
    pdir = ROOT / "outputs" / "prompts"
    pdir.mkdir(parents=True, exist_ok=True)
    (pdir / f"system_prompt_{fp}.txt").write_text(system, encoding="utf-8")
    (pdir / f"output_schema_{fp}.json").write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")
    d0 = docs.iloc[0]
    (pdir / "example_user_prompt.txt").write_text(build_user(d0.title, d0.text), encoding="utf-8")
    log.info("prompt fingerprint %s | system %d chars (~%d tokens) | docs %d",
             fp, len(system), len(system) // 4, len(docs))

    runs = list(L["runs"])
    if args.runs:
        want = set(args.runs.split(","))
        runs = [r for r in runs if r["name"] in want]
    if args.ollama:
        models = [{"name": "smoke_" + args.ollama.replace(":", "_").replace("/", "_"),
                   "provider": "ollama", "model": args.ollama, "options": {"num_ctx": 20000}}]
    else:
        models = list(L.get("models") or [])
        if args.models:
            want = set(args.models.split(","))
            models = [m for m in models if m["name"] in want]
    if not models:
        log.error("no hay modelos definidos (config llm.models vacio). Nada que ejecutar.")
        if not args.dry_run:
            return 1

    n_calls = len(models) * len(runs) * len(docs)
    est_in = (len(system) + 600) // 4
    log.info("%d modelos x %d corridas x %d docs = %d llamadas; ~%d tokens de entrada por llamada (estimacion chars/4)",
             len(models), len(runs), len(docs), n_calls, est_in)
    for m in models:
        p = (L.get("pricing_usd_per_mtok") or {}).get(m["name"])
        if p:
            # sin cache de prefijo (peor caso) y con cache (mejor caso, 90 % de lectura)
            worst = n_calls / len(models) * (est_in * p["input"] + 800 * p["output"]) / 1e6
            best = n_calls / len(models) * (est_in * p.get("cache_read", p["input"]) + 800 * p["output"]) / 1e6
            log.info("coste estimado %s: %.2f–%.2f USD", m["name"], best, worst)
        else:
            log.info("coste estimado %s: 0 USD (local o sin tarifa en config)", m["name"])
    if args.dry_run:
        log.info("dry-run: no se ha llamado a ningun proveedor. Prompts en %s", pdir)
        return 0

    all_stats = []
    for m in models:
        t0 = time.time()
        st = run_model(m, docs, system, schema, runs, fp, dry_run=False)
        st["elapsed_s"] = round(time.time() - t0, 1)
        all_stats.append(st)
        log.info("resumen %s: %s", m["name"], json.dumps(st))
    # Se reunen TODOS los modelos del config (no solo los de esta invocacion) para que dos
    # procesos en paralelo (p.ej. Groq y Ollama) no se sobrescriban el CSV final.
    collect(sorted({m["name"] for m in (L.get("models") or [])} | {m["name"] for m in models}), docs, runs)
    hard = sum(s["hard_failures"] for s in all_stats)
    if hard:
        log.error("%d llamadas sin resultado valido. Revisa el log.", hard)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
