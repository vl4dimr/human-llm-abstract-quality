"""Fase 1 - Auditoria de datos.

1. Carga los archivos crudos y reporta: resumenes, anotaciones por anotador,
   cobertura, valores fuera del esquema, duplicados, textos vacios o truncados.
2. Normaliza al formato largo canonico data/interim/annotations.csv.
3. Calcula la prevalencia de cada variable por anotador.
4. Recalcula desde cero el acuerdo humano-humano (A1 vs A2) con kappa, AC1,
   PABAK y alpha de Krippendorff, con IC bootstrap a nivel de documento.
5. Comprueba explicitamente si dos cuadernillos son copias uno del otro.

Escribe outputs/audit_report.md y las tablas en outputs/tables/.
No modifica nada en data/raw/. No imputa nada.

Uso:  python src/01_audit.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib import metrics as M  # noqa: E402
from lib.io_raw import (load_config, read_annotation_workbook, read_master_key,  # noqa: E402
                        to_long, variable_specs)
from lib.logging_utils import get_logger  # noqa: E402
from lib.tables import write_table  # noqa: E402

cfg = load_config()
SEED = int(cfg["seed"])
RAW = ROOT / cfg["paths"]["raw"]
INTERIM = ROOT / cfg["paths"]["interim"]
TABLES = ROOT / cfg["paths"]["tables"]
LOGS = ROOT / cfg["paths"]["logs"]
SPECS = variable_specs(cfg)
VARS = list(SPECS.keys())

log = get_logger("01_audit", LOGS)
REPORT: list[str] = []  # lineas del informe markdown


def say(line: str = "") -> None:
    """Escribe una linea al informe y al log a la vez."""
    REPORT.append(line)
    if line.strip():
        log.info(line)


def md_table(df: pd.DataFrame, floatfmt: str = ".3f") -> str:
    return df.to_markdown(index=False, floatfmt=floatfmt)


# --------------------------------------------------------------------------- #
# 0. Comprobaciones previas
# --------------------------------------------------------------------------- #
say(f"# Informe de auditoria de datos (Fase 1)\n")
say(f"Generado: {datetime.now().isoformat(timespec='seconds')}  ·  semilla: {SEED}\n")

prov_path = RAW / "PROVENANCE.json"
if not prov_path.exists():
    log.error("No existe %s. Ejecuta antes: python src/00_stage_raw.py", prov_path)
    raise SystemExit(1)
prov = json.loads(prov_path.read_text(encoding="utf-8"))
say("## 0. Procedencia de los archivos crudos\n")
say(f"{len(prov['files'])} archivos copiados el {prov['staged_at_utc']} (SHA-256 en `data/raw/PROVENANCE.json`).\n")
say(md_table(pd.DataFrame(prov["files"])[["path", "bytes", "sha256"]].assign(
    sha256=lambda d: d["sha256"].str[:12] + "…")))
say()

# --------------------------------------------------------------------------- #
# 1. Corpus: clave maestra
# --------------------------------------------------------------------------- #
say("## 1. Corpus muestreado (clave maestra)\n")
key = read_master_key(RAW / cfg["corpus"]["master_key"])
say(f"Filas en la clave maestra: **{len(key)}**. IDs unicos: {key['doc_id'].is_unique}.\n")
say("Por fase:\n")
say(md_table(key.groupby("fase").size().rename("n").reset_index()))
say()
analysis_phase = cfg["corpus"]["analysis_phase"]
key_main = key[key["fase"] == analysis_phase].copy()
say(f"Fase de analisis: `{analysis_phase}` -> **{len(key_main)} documentos**. "
    f"Fases excluidas: {cfg['corpus']['exclude_phases']}.\n")

say("Composicion de la fase de analisis (tipo de tesis):\n")
comp_tipo = key_main.groupby("tipo").size().rename("n").reset_index()
comp_tipo["pct"] = 100 * comp_tipo["n"] / len(key_main)
say(md_table(comp_tipo, ".1f"))
say()
say("Por institucion:\n")
say(md_table(key_main.groupby("institucion_cod").size().rename("n").reset_index()))
say()
say("Por estrato disciplinar (OCDE/FORD):\n")
say(md_table(key_main.groupby("estrato").size().rename("n").reset_index().sort_values("n", ascending=False)))
say()
say(f"Anios: {int(key_main['anio'].min())}–{int(key_main['anio'].max())}. "
    f"Palabras por resumen (segun clave): media {key_main['resumen_palabras'].mean():.0f}, "
    f"mediana {key_main['resumen_palabras'].median():.0f}, "
    f"min {key_main['resumen_palabras'].min()}, max {key_main['resumen_palabras'].max()}.\n")

n_doc = int((key_main["tipo"] == "doctoralThesis").sum())
say(f"> **Aviso:** solo {n_doc} de {len(key_main)} documentos de la fase principal son tesis "
    f"doctorales ({100*n_doc/len(key_main):.1f} %). El corpus es mayoritariamente de tesis de "
    f"pregrado (bachelorThesis). La descripcion del estudio como «resumenes de tesis doctorales» "
    f"no coincide con los datos.\n")

# --------------------------------------------------------------------------- #
# 2. Cuadernillos de anotacion
# --------------------------------------------------------------------------- #
say("## 2. Cuadernillos de anotacion\n")

workbooks: dict[str, Path] = {}
for name, spec in cfg["annotators"].items():
    workbooks[name] = RAW / spec["file"]
# Versiones alternativas de A1 (se auditan siempre, use la que use el config)
alt_a1 = {p.stem.replace("Anotacion_principal_", ""): p
          for p in (RAW / "annotations").glob("Anotacion_principal_A1*.xlsx")}
for k, p in alt_a1.items():
    if p != workbooks["A1"]:
        workbooks[f"A1[{k}]"] = p
# El A2 original (copia exacta de A1) se mantiene en la auditoria como evidencia
# documental, aunque ya no sea el A2 del analisis.
legacy_a2 = RAW / "annotations" / "Anotacion_principal_A2.xlsx"
if legacy_a2.exists() and legacy_a2 != workbooks.get("A2"):
    workbooks["A2[original_copia]"] = legacy_a2
workbooks["LLM_prior"] = RAW / cfg["llm_prior"]["file"]

frames: dict[str, pd.DataFrame] = {}
wb_rows = []
value_issues = []
raw_llm: pd.DataFrame | None = None
LLM_OFFSET = int(cfg["llm_prior"].get("row_offset", 0))
for name, path in workbooks.items():
    df = read_annotation_workbook(path, cfg)
    if name == "LLM_prior":
        raw_llm = df.copy()
        if LLM_OFFSET != 0:
            # Realineacion: valor[k] := valor_crudo[k + offset]. Se mueven las 12
            # variables y las observaciones; texto y titulo NO (estan alineados).
            df = df.sort_values("doc_id").reset_index(drop=True)
            df[VARS + ["notes"]] = df[VARS + ["notes"]].shift(-LLM_OFFSET)
            log.warning("LLM_prior realineado con row_offset=%d (config.yaml)", LLM_OFFSET)
    frames[name] = df
    annotated = df[VARS].notna().any(axis=1)
    n_ann = int(annotated.sum())
    dup = int(df["doc_id"].duplicated().sum())
    not_in_key = sorted(set(df["doc_id"]) - set(key["doc_id"]))
    # valores fuera del esquema
    for v in VARS:
        allowed = set(float(x) for x in SPECS[v]["levels"])
        bad = df.loc[df[v].notna() & ~df[v].isin(allowed), ["doc_id", v]]
        for _, r in bad.iterrows():
            value_issues.append({"workbook": name, "doc_id": r["doc_id"], "variable": v, "value": r[v]})
    # rango de ids anotados
    nums = sorted(int(re.sub(r"\D", "", d)) for d in df.loc[annotated, "doc_id"])
    contiguous = bool(nums) and nums == list(range(nums[0], nums[0] + len(nums)))
    wb_rows.append({
        "workbook": name, "file": path.name, "rows": len(df), "annotated_rows": n_ann,
        "coverage_pct": round(100 * n_ann / len(df), 1) if len(df) else np.nan,
        "annotated_range": f"{nums[0]}–{nums[-1]}" if nums else "—",
        "contiguous": contiguous, "duplicate_ids": dup, "ids_not_in_key": len(not_in_key),
        "D4_filled": int(df["D4_consistencia"].notna().sum()),
        "notes_filled": int(df["notes"].notna().sum()),
    })
    log.info("%s: %d filas, %d anotadas", name, len(df), n_ann)

wb_table = pd.DataFrame(wb_rows)
say(md_table(wb_table))
say()
say(f"Valores fuera del esquema: **{len(value_issues)}**.")
if value_issues:
    say(md_table(pd.DataFrame(value_issues)))
say()

expected_empty = [n for n, s in cfg["annotators"].items() if s.get("expected_empty")]
for n in expected_empty:
    n_ann = int(wb_table.loc[wb_table["workbook"] == n, "annotated_rows"].iloc[0])
    say(f"> {n}: plantilla declarada como vacia en config; anotadas = {n_ann}. "
        + ("Confirmado: **A3 no anoto nada**." if n_ann == 0 else "**Contradice el config.**") + "\n")

# --------------------------------------------------------------------------- #
# 3. Textos: vacios, truncados, identicos entre cuadernillos
# --------------------------------------------------------------------------- #
say("## 3. Textos de los resumenes\n")
ref = frames["A1"]
txt = ref[["doc_id", "text"]].copy()
txt["n_chars"] = txt["text"].fillna("").astype(str).str.len()
txt["n_words"] = txt["text"].fillna("").astype(str).str.split().str.len()
txt["ends_punct"] = txt["text"].fillna("").astype(str).str.strip().str[-1:].isin(list(".!?)»\"”"))
empty = txt[txt["n_chars"] == 0]
short = txt[(txt["n_chars"] > 0) & (txt["n_chars"] < cfg["audit"]["text_min_chars"])]
nopunct = txt[(txt["n_chars"] > 0) & ~txt["ends_punct"]]
say(f"Textos vacios: **{len(empty)}**. Textos < {cfg['audit']['text_min_chars']} caracteres: **{len(short)}**. "
    f"Textos que no terminan en puntuacion (posible truncado): **{len(nopunct)}**.\n")
if len(nopunct):
    say("IDs sin puntuacion final: " + ", ".join(nopunct["doc_id"].tolist()) + "\n")

# palabras del texto vs palabras declaradas en la clave
chk = txt.merge(key[["doc_id", "resumen_palabras"]], on="doc_id", how="left")
chk["ratio"] = chk["n_words"] / chk["resumen_palabras"]
tol = cfg["audit"]["words_tolerance"]
off = chk[(chk["ratio"] < 1 - tol) | (chk["ratio"] > 1 + tol)]
say(f"Documentos cuyo texto difiere >{int(tol*100)} % en palabras de lo declarado en la clave: **{len(off)}**.\n")
if len(off):
    say(md_table(off[["doc_id", "n_words", "resumen_palabras", "ratio"]].head(20), ".2f"))

# Todos los anotadores vieron el mismo texto?
say("¿Los cuadernillos contienen el mismo texto por id?\n")
same_rows = []
for name, df in frames.items():
    if name == "A1" or df["text"].isna().all():
        continue
    m = ref[["doc_id", "text"]].merge(df[["doc_id", "text"]], on="doc_id", suffixes=("_a1", "_x"))
    diff = int((m["text_a1"].fillna("") != m["text_x"].fillna("")).sum())
    same_rows.append({"workbook": name, "ids_common": len(m), "texts_differ": diff})
say(md_table(pd.DataFrame(same_rows)))
say()

# --------------------------------------------------------------------------- #
# 4. Cobertura cruzada y documentos con un solo anotador
# --------------------------------------------------------------------------- #
say("## 4. Cobertura cruzada (fase principal)\n")
ann_ids = {n: set(df.loc[df[VARS].notna().any(axis=1), "doc_id"]) for n, df in frames.items()}
humans = [n for n, spec in cfg["annotators"].items()
          if spec["kind"] == "human" and not spec.get("expected_empty")]
both = set.intersection(*(ann_ids[h] for h in humans))
any_h = set.union(*(ann_ids[h] for h in humans))
say(f"Anotadores humanos activos: {humans}. Documentos con TODOS ellos: **{len(both)}**; "
    f"con al menos uno: {len(any_h)}; con uno solo: **{len(any_h - both)}**; "
    f"sin ningun humano: **{len(set(key_main['doc_id']) - any_h)}** de {len(key_main)}.\n")
say(f"LLM_prior anotado: {len(ann_ids['LLM_prior'])} docs; solapa con los dos humanos en "
    f"**{len(ann_ids['LLM_prior'] & both)}** docs.\n")

# --------------------------------------------------------------------------- #
# 5. ¿Son copias? Diferencia celda a celda entre cuadernillos
# --------------------------------------------------------------------------- #
say("## 5. Independencia entre cuadernillos (diferencia celda a celda)\n")
say("Para cada par se comparan las 12 variables en los documentos anotados por ambos, "
    "y ademas el texto libre de `observaciones`. Dos anotadores independientes no pueden "
    "producir observaciones libres identicas.\n")
pair_rows = []
names = list(frames.keys())
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = names[i], names[j]
        ids = sorted(ann_ids[a] & ann_ids[b])
        if not ids:
            continue
        X = frames[a].set_index("doc_id").loc[ids]
        Y = frames[b].set_index("doc_id").loc[ids]
        neq = (X[VARS] != Y[VARS]) & ~(X[VARS].isna() & Y[VARS].isna())
        n_cells = int(neq.size)
        n_diff = int(neq.values.sum())
        by_var = {v: int(neq[v].sum()) for v in VARS if neq[v].sum()}
        na = X["notes"].fillna("").astype(str).str.strip()
        nb = Y["notes"].fillna("").astype(str).str.strip()
        both_nonempty = (na != "") & (nb != "")
        notes_identical = int(((na == nb) & both_nonempty).sum())
        pair_rows.append({
            "pair": f"{a} vs {b}", "same_source": a.split("[")[0] == b.split("[")[0],
            "docs_common": len(ids), "cells": n_cells,
            "cells_differ": n_diff, "pct_differ": round(100 * n_diff / n_cells, 2),
            "notes_both": int(both_nonempty.sum()), "notes_identical": notes_identical,
            "differing_vars": ", ".join(f"{k}:{v}" for k, v in by_var.items()) or "—",
        })
pairs = pd.DataFrame(pair_rows)
say(md_table(pairs.drop(columns=["same_source"]), ".2f"))
say()

copies = pairs[(pairs["cells_differ"] == 0) & (pairs["notes_identical"] >= 0.9 * pairs["notes_both"])
               & (pairs["notes_both"] > 0) & ~pairs["same_source"]]
if len(copies):
    say("> **HALLAZGO CRITICO.** Los siguientes pares son copias exactas (0 celdas distintas y "
        "observaciones libres identicas):\n")
    for _, r in copies.iterrows():
        say(f"> - **{r['pair']}** — {r['docs_common']} documentos, {r['notes_identical']}/{r['notes_both']} "
            f"observaciones identicas.")
    say(">")
    say("> Un acuerdo humano-humano calculado sobre un par asi vale 1.0 por construccion y no "
        "mide nada. **No existe en estos datos una segunda anotacion humana independiente.**\n")

# calibracion tambien
cal = {}
for k in ("A1", "A2"):
    rel = cfg["annotators"].get(k, {}).get("calibration_file")
    if rel and (RAW / rel).exists():
        cal[k] = read_annotation_workbook(RAW / rel, cfg).set_index("doc_id")
if len(cal) == 2:
    ids = sorted(set(cal["A1"].index[cal["A1"][VARS].notna().any(axis=1)]) &
                 set(cal["A2"].index[cal["A2"][VARS].notna().any(axis=1)]))
    X, Y = cal["A1"].loc[ids, VARS], cal["A2"].loc[ids, VARS]
    neq = (X != Y) & ~(X.isna() & Y.isna())
    na = cal["A1"].loc[ids, "notes"].fillna("").astype(str)
    nb = cal["A2"].loc[ids, "notes"].fillna("").astype(str)
    say(f"Fase de calibracion (A1 vs A2): {len(ids)} docs, **{int(neq.values.sum())}** celdas distintas de "
        f"{neq.size}, observaciones identicas {int((na == nb).sum())}/{len(ids)}.\n")

say("Relacion entre las versiones de A1: `A1_v0` (120 docs) ⊂ `A1_REV` (160 docs) celda por celda; "
    "`A1` (la mas reciente) difiere de `A1_REV` solo en `D4_consistencia`. Ver seccion 10.\n")

# --------------------------------------------------------------------------- #
# 5b. Alineacion de filas del cuadernillo LLM_prior
# --------------------------------------------------------------------------- #
say("### 5b. Alineacion de filas: LLM_prior vs A1\n")
say("Se compara A1[k] con LLM_crudo[k + s] para s en −3..+3. Si el maximo no esta en s = 0, "
    "los valores del cuadernillo LLM estan corridos respecto a sus textos. Se usa el archivo "
    f"**crudo** (sin aplicar `row_offset`, que ahora vale {LLM_OFFSET}).\n")
order_ids = sorted(frames["A1"]["doc_id"])
A_mat = frames["A1"].set_index("doc_id").loc[order_ids, VARS].to_numpy(float)
L_mat = raw_llm.set_index("doc_id").loc[order_ids, VARS].to_numpy(float)
n_all = len(order_ids)
scan_rows = []
for s in range(-3, 4):
    ks = range(max(0, -s), min(n_all, n_all - s))
    row = {"shift": s}
    kv = []
    for j, v in enumerate(VARS):
        lv = [float(x) for x in SPECS[v]["levels"]]
        w = cfg["agreement"]["weights_by_type"][SPECS[v]["type"]]
        x = np.array([A_mat[k, j] for k in ks])
        y = np.array([L_mat[k + s, j] for k in ks])
        ok = ~np.isnan(x) & ~np.isnan(y)
        kap = M.cohen_kappa(x[ok], y[ok], lv, w) if ok.sum() else np.nan
        row[v.replace("_imryd", "")[:14]] = kap
        kv.append(kap)
    row["mean_kappa"] = float(np.nanmean(kv))
    scan_rows.append(row)
scan = pd.DataFrame(scan_rows)
say(md_table(scan))
say()
best = int(scan.loc[scan["mean_kappa"].idxmax(), "shift"])
best_k = float(scan["mean_kappa"].max())
zero_k = float(scan.loc[scan["shift"] == 0, "mean_kappa"].iloc[0])

# Evidencia independiente: citas literales de las observaciones contra el texto
import unicodedata  # noqa: E402


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


def _quote_hits(df: pd.DataFrame, offset: int) -> tuple[int, int]:
    """Cuantas citas entre comillas simples (≥4 palabras) de la observacion de la fila k
    aparecen literalmente en el texto del documento k + offset."""
    d = df.set_index("doc_id")
    n_q = n_hit = 0
    for i in d.index:
        num = int(re.sub(r"\D", "", i))
        tgt = f"GT-{num + offset:03d}"
        if tgt not in d.index or pd.isna(d.loc[i, "notes"]):
            continue
        for q in re.findall(r"'([^']{15,})'", str(d.loc[i, "notes"])):
            if len(q.split()) < 4:
                continue
            n_q += 1
            if _norm(q) in _norm(d.loc[tgt, "text"]):
                n_hit += 1
    return n_hit, n_q


say("Evidencia independiente: citas literales de las `observaciones` de la fila k buscadas en el "
    "texto del documento k + offset (un anotador alineado cita el texto de su propia fila):\n")
qrows = []
for lab, df in (("A1", frames["A1"]), ("LLM_prior (crudo)", raw_llm)):
    for off in (-1, 0, 1):
        h, q = _quote_hits(df, off)
        qrows.append({"workbook": lab, "offset": off, "quotes": q, "found_in_text": h})
say(md_table(pd.DataFrame(qrows)))
say()
if best != 0 and best_k - zero_k > 0.3:
    say(f"> **HALLAZGO.** El acuerdo A1–LLM_prior es maximo con desplazamiento **s = {best}** "
        f"(κ medio {best_k:.3f}) y practicamente nulo con s = 0 (κ medio {zero_k:.3f}). Las citas "
        f"de A1 caen en su propia fila y las del LLM en la fila k+1: **el cuadernillo del LLM tiene sus "
        f"valores y observaciones corridos una fila respecto a los textos** (la fila GT-k contiene el "
        f"juicio del documento GT-(k{'+' if best < 0 else '-'}{abs(best)})). Es un error de manipulacion "
        f"del archivo previo, no un desacuerdo real. Para corregirlo: `llm_prior.row_offset: {best}` en "
        f"config.yaml y volver a ejecutar. No se ha tocado `data/raw/`.\n")
elif LLM_OFFSET != 0:
    say(f"> `row_offset = {LLM_OFFSET}` aplicado desde config.yaml. El barrido sobre el archivo crudo "
        f"sigue mostrando el maximo en s = {best}.\n")

# --------------------------------------------------------------------------- #
# 6. Reglas internas del protocolo
# --------------------------------------------------------------------------- #
say("## 6. Consistencia con las reglas del protocolo\n")
rule_rows = []
d3_d1 = [("D3_metodo_detallado", "D1_imryd_metodologia"),
         ("D3_resultados_concretos", "D1_imryd_resultados"),
         ("D3_conclusion_responde", "D1_imryd_conclusiones")]
comp = ["D1_imryd_objetivo", "D1_imryd_metodologia", "D1_imryd_resultados", "D1_imryd_conclusiones"]
for name, df in frames.items():
    d = df[df[VARS].notna().any(axis=1)]
    if d.empty:
        continue
    v_d3 = sum(int(((d[d1] == 0) & (d[d3] == 1)).sum()) for d3, d1 in d3_d1)
    s = d[comp].sum(axis=1)
    v_ord = int(((s <= 1) & (d["D1_orden_logico"] == 1)).sum())
    d4_nan = d["D4_consistencia"].isna()
    ne1 = d["no_evaluable"] == 1
    rule_rows.append({
        "workbook": name,
        "D3=1 con D1=0 (§8.4)": v_d3,
        "orden=1 con ≤1 componente (§6.5)": v_ord,
        "D4 vacio": int(d4_nan.sum()),
        "D4 vacio y no_evaluable=1": int((d4_nan & ne1).sum()),
        "no_evaluable=1 con D4 relleno (§9.3)": int((ne1 & ~d4_nan).sum()),
        "no_evaluable=1 con D4 vacio pero otras rellenas": int((ne1 & d4_nan & d[comp].notna().any(axis=1)).sum()),
    })
say(md_table(pd.DataFrame(rule_rows)))
say()
say("> Nota: §8.4 hace que D3 dependa deterministicamente de D1 (si D1=0 entonces D3=0). "
    "El acuerdo en D3 hereda parte del acuerdo en D1; las 12 variables no son 12 pruebas independientes.\n")
say("> Nota: la regla §6.5 (orden = 0 con ≤ 1 componentes) se incumple en 8 documentos por los "
    "humanos y en 0 por el LLM. Es un desvio del anotador respecto al manual, no un error de datos; "
    "se deja tal cual.\n")

# --------------------------------------------------------------------------- #
# 7. Normalizacion a formato largo
# --------------------------------------------------------------------------- #
say("## 7. Normalizacion\n")
INTERIM.mkdir(parents=True, exist_ok=True)
main_ids = set(key_main["doc_id"])
long_parts = []
for name in [*humans, "LLM_prior"]:
    df = frames[name]
    df = df[df["doc_id"].isin(main_ids)]
    long_parts.append(to_long(df, name, cfg))
long = pd.concat(long_parts, ignore_index=True)
long_path = INTERIM / "annotations.csv"
long.to_csv(long_path, index=False, encoding="utf-8")

docs = key_main[["doc_id", "fase", "tipo", "institucion_cod", "anio", "estrato", "resumen_palabras"]].merge(
    frames["A1"][["doc_id", "title", "text"]], on="doc_id", how="left")
docs["n_words_text"] = docs["text"].fillna("").astype(str).str.split().str.len()
docs_path = INTERIM / "documents.csv"
docs.to_csv(docs_path, index=False, encoding="utf-8")
say(f"- `{long_path.relative_to(ROOT)}`: {len(long)} filas (doc_id, annotator, category, label). "
    f"Solo celdas no vacias; una fila ausente = no anotado.")
say(f"- `{docs_path.relative_to(ROOT)}`: {len(docs)} documentos con texto y metadatos. "
    f"**Contiene titulos: no es la version de deposito.**\n")
say(md_table(long.groupby("annotator").agg(rows=("label", "size"), docs=("doc_id", "nunique")).reset_index()))
say()

# --------------------------------------------------------------------------- #
# 8. Prevalencia por variable
# --------------------------------------------------------------------------- #
say("## 8. Prevalencia por variable y anotador (fase principal, docs anotados)\n")
prev_rows = []
for v in VARS:
    spec = SPECS[v]
    row = {"variable": v, "type": spec["type"], "dimension": spec["dimension"]}
    for name in [*humans, "LLM_prior"]:
        s = long[(long["annotator"] == name) & (long["category"] == v)]["label"]
        if spec["type"] == "binary":
            row[f"{name}_n"] = len(s)
            row[f"{name}_p1"] = float(s.mean()) if len(s) else np.nan
        else:
            row[f"{name}_n"] = len(s)
            row[f"{name}_mean"] = float(s.mean()) if len(s) else np.nan
            row[f"{name}_dist"] = " ".join(f"{int(k)}:{int(c)}" for k, c in s.value_counts().sort_index().items())
    prev_rows.append(row)
prev = pd.DataFrame(prev_rows)
write_table(prev, TABLES, "table1_prevalence",
            caption="Corpus descriptives and per-variable prevalence by annotator (audit).",
            label="tab:prevalence")
say(md_table(prev.drop(columns=[c for c in prev.columns if c.endswith("_dist")])))
say()
say("Distribucion de las ordinales:\n")
say(md_table(prev[prev["type"] == "ordinal"][["variable"] + [c for c in prev.columns if c.endswith("_dist")]]))
say()
say("> Variables con prevalencia extrema (p1 > 0.95 o < 0.05) en humanos: "
    + ", ".join(f"`{r['variable']}` ({r['A1_p1']:.3f})" for _, r in prev.iterrows()
                if r["type"] == "binary" and (r["A1_p1"] > 0.95 or r["A1_p1"] < 0.05))
    + ". Ahi kappa colapsa por construccion: AC1 y PABAK son imprescindibles.\n")
say("> `D1_imryd_objetivo`: el LLM_prior asigna 1 a **todos** los documentos (varianza cero). "
    "Cualquier kappa contra el es degenerado o inestable.\n")

# --------------------------------------------------------------------------- #
# 9. Acuerdo por pares, recalculado desde cero
# --------------------------------------------------------------------------- #
say("## 9. Acuerdo entre anotadores, recalculado desde cero\n")
NB = int(cfg["agreement"]["bootstrap"]["n_resamples"])
say(f"Bootstrap: {NB} remuestreos a nivel de documento, IC percentil 95 %, semilla {SEED}. "
    f"Exclusion por pares de los faltantes (D4 vacio cuando no_evaluable = 1 es estructural, §9.3).\n")

wide = long.pivot_table(index=["doc_id", "category"], columns="annotator", values="label", aggfunc="first")


def agreement_table(a: str, b: str) -> pd.DataFrame:
    rows = []
    for v in VARS:
        spec = SPECS[v]
        lv = [float(x) for x in spec["levels"]]
        w = cfg["agreement"]["weights_by_type"][spec["type"]]
        km = cfg["agreement"]["krippendorff_metric_by_type"][spec["type"]]
        sub = wide.xs(v, level="category")[[a, b]].dropna()
        x = sub[a].to_numpy(float)
        y = sub[b].to_numpy(float)
        n = len(sub)
        if n == 0:
            rows.append({"variable": v, "n": 0})
            continue
        pos = np.arange(n)
        f_k = lambda idx, x=x, y=y, lv=lv, w=w: M.cohen_kappa(x[idx], y[idx], lv, w)  # noqa: E731
        f_a = lambda idx, x=x, y=y, lv=lv, w=w: M.gwet_ac1(x[idx], y[idx], lv, w)  # noqa: E731
        bk = M.bootstrap_ci(pos, f_k, n_resamples=NB, seed=SEED)
        ba = M.bootstrap_ci(pos, f_a, n_resamples=NB, seed=SEED)
        alpha = M.krippendorff_alpha(np.vstack([x, y]), lv, km)
        rows.append({
            "variable": v, "type": spec["type"], "weights": w, "n": n,
            "p_obs": M.observed_agreement(x, y, lv, w),
            "kappa": bk.estimate, "kappa_lo": bk.ci_low, "kappa_hi": bk.ci_high,
            "kappa_degenerate_frac": bk.degenerate_fraction,
            "gwet_ac": ba.estimate, "ac_lo": ba.ci_low, "ac_hi": ba.ci_high,
            "pabak": M.pabak(x, y, lv),
            "kripp_alpha": alpha, "kripp_metric": km,
        })
    return pd.DataFrame(rows)


# 9a. Humano-humano
hh = agreement_table("A1", "A2")
write_table(hh, TABLES, "audit_agreement_A1_A2", caption="Human–human agreement A1 vs A2 (audit, recomputed).",
            label="tab:audit-hh")
say("### 9a. A1 vs A2 (humano-humano)\n")
say(md_table(hh[["variable", "type", "n", "p_obs", "kappa", "kappa_lo", "kappa_hi", "gwet_ac", "pabak", "kripp_alpha"]]))
say()
prev_rep = cfg["audit"].get("previously_reported_agreement")
if prev_rep is None:
    say("> No se ha proporcionado el valor de acuerdo humano-humano reportado previamente "
        "(`audit.previously_reported_agreement` en config.yaml). Indicalo para contrastarlo.\n")
else:
    say(f"> Valor previamente reportado: {prev_rep}. Recalculado arriba.\n")
if (hh["p_obs"].dropna() == 1.0).all():
    say("> **Acuerdo bruto = 1.000 en las 12 variables.** Coherente con el hallazgo de la seccion 5: "
        "A2 es una copia de A1. Este kappa no puede usarse como linea base humana.\n")

# 9b. Humano vs LLM previo (contexto, NO es la fase 2)
hl = agreement_table("A1", "LLM_prior")
write_table(hl, TABLES, "audit_agreement_A1_LLMprior",
            caption="A1 vs prior LLM annotation (claude.ai chat, 2026-08-12). Descriptive only; not a Phase-2 run.",
            label="tab:audit-hl")
say(f"### 9b. A1 vs LLM_prior (solo contexto; row_offset = {LLM_OFFSET})\n")
say("La anotacion LLM previa se hizo por chat (claude.ai), sin temperature fija, sin semilla ni "
    "repeticiones y con el protocolo v2.0. **No es admisible como corrida de la fase 2**; se muestra "
    "solo para ver que aspecto tiene un acuerdo no trivial en este esquema. "
    + ("**Calculado sobre el archivo crudo, sin realinear: ver 5b antes de interpretar.**"
       if LLM_OFFSET == 0 else f"Calculado tras realinear con offset {LLM_OFFSET}.") + "\n")
say(md_table(hl[["variable", "type", "n", "p_obs", "kappa", "kappa_lo", "kappa_hi", "kappa_degenerate_frac",
                 "gwet_ac", "ac_lo", "ac_hi", "pabak", "kripp_alpha"]]))
say()
unstable = hl[hl["kappa_degenerate_frac"] > cfg["agreement"]["bootstrap"]["max_degenerate_fraction"]]
if len(unstable):
    say("> IC de kappa inestable (fraccion de remuestreos degenerados > "
        f"{cfg['agreement']['bootstrap']['max_degenerate_fraction']}): "
        + ", ".join(f"`{r['variable']}` ({r['kappa_degenerate_frac']:.2f})" for _, r in unstable.iterrows()) + ".\n")

# Matrices de confusion A1 vs LLM_prior (las de A1 vs A2 son diagonales)
say("Matrices de confusion A1 (filas) vs LLM_prior (columnas):\n")
cm_rows = []
for v in VARS:
    lv = [float(x) for x in SPECS[v]["levels"]]
    sub = wide.xs(v, level="category")[["A1", "LLM_prior"]].dropna()
    m = M.confusion_matrix(sub["A1"].to_numpy(float), sub["LLM_prior"].to_numpy(float), lv)
    cm_rows.append({"variable": v, "matrix": " | ".join(" ".join(str(int(c)) for c in row) for row in m)})
say(md_table(pd.DataFrame(cm_rows)))
say()

# --------------------------------------------------------------------------- #
# 10. Resumen de bloqueos
# --------------------------------------------------------------------------- #
say("## 10. Estado y bloqueos\n")
blocks, resolved = [], []

# El A2 que usa el analisis, es independiente de A1?
active = pairs[pairs["pair"] == "A1 vs A2"]
if len(active):
    r = active.iloc[0]
    if r["cells_differ"] == 0 or r["notes_identical"] > 0:
        blocks.append(f"**El A2 activo no es independiente**: {int(r['cells_differ'])} celdas distintas y "
                      f"{int(r['notes_identical'])} observaciones identicas a las de A1.")
    else:
        resolved.append(f"**Segunda anotacion humana independiente disponible.** A1 y A2 difieren en "
                        f"{int(r['cells_differ'])}/{int(r['cells'])} celdas (acuerdo bruto "
                        f"{100 - r['pct_differ']:.1f} %) y ninguna observacion libre coincide. "
                        f"La linea base kappa(A1-A2) y el contraste delta-kappa ya son calculables.")
else:
    blocks.append("**Falta el par A1-A2.**")

legacy = pairs[pairs["pair"] == "A1 vs A2[original_copia]"]
if len(legacy) and legacy.iloc[0]["cells_differ"] == 0:
    resolved.append(f"El A2 **original** era copia exacta de A1 (0 celdas distintas, "
                    f"{int(legacy.iloc[0]['notes_identical'])}/160 observaciones identicas). Se conserva en "
                    f"`data/raw/` solo como evidencia de esta auditoria; `config.yaml` ya no lo usa.")

n_cov = len(both)
if n_cov < len(key_main):
    blocks.append(f"**Cobertura:** {n_cov} de {len(key_main)} documentos de la fase principal tienen "
                  f"anotacion humana doble ({100*n_cov/len(key_main):.0f} %). Los {len(key_main)-n_cov} "
                  f"restantes quedan fuera del analisis; no se imputa nada.")
blocks.append(f"**Corpus:** {n_doc} tesis doctorales de {len(key_main)}; el resto son de pregrado y maestria. "
              f"Hay que corregir la descripcion del estudio o restringir la muestra.")
blocks.append(f"**Tres versiones de A1** que difieren en 22 celdas de `D4_consistencia` (la '-REV' es "
              f"sistematicamente un punto mas baja). En uso: `{cfg['annotators']['A1']['file']}`.")
if best != 0 and best_k - zero_k > 0.3 and LLM_OFFSET == 0:
    blocks.append(f"**Cuadernillo LLM_prior desalineado una fila** (seccion 5b). Fijar "
                  f"`llm_prior.row_offset: {best}`.")
_models = cfg.get("llm", {}).get("models") or []
_sin_id = [m.get("name") for m in _models if not m.get("model")]
if not _models:
    blocks.append("**Modelos de la fase 2 sin definir** (`llm.models` vacio en config.yaml).")
elif _sin_id:
    blocks.append(f"**Modelos sin ID exacto**: {_sin_id}.")
else:
    resolved.append(f"**Modelos de la fase 2 definidos**: {[m['name'] for m in _models]}, "
                    f"{len(cfg['llm']['runs'])} corridas cada uno.")

if resolved:
    say("### Resuelto\n")
    for b in resolved:
        say(f"- {b}")
    say()
say("### Pendiente\n")
for b in blocks:
    say(f"- {b}")
say()

report_path = ROOT / "outputs" / "audit_report.md"
report_path.write_text("\n".join(REPORT) + "\n", encoding="utf-8")
log.info("informe escrito: %s", report_path)
print(f"\n=== informe: {report_path} ===")
