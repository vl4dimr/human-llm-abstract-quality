"""Fase 5 - Analisis cualitativo del error.

Extrae los casos donde el LLM discrepa del humano PERO los dos humanos coincidian
(fallos genuinos del modelo), los etiqueta con una taxonomia preliminar de modos de
fallo basada en reglas verificables, y deja 3-5 ejemplos citables por tipo.

Modo estricto (annotators.A2.independent = true): humano = consenso A1 = A2.
Modo provisional (--provisional): humano = A1 solo. Los archivos llevan el sufijo
PROVISIONAL y no deben usarse en el articulo: sin A2 no se distingue el fallo del
modelo del desacuerdo legitimo entre humanos.

Salida: outputs/tables/disagreements_for_review[_PROVISIONAL_A1only].csv,
        outputs/tables/error_taxonomy_counts[...].csv, outputs/error_analysis_report[...].md

Uso:  python src/05_error_analysis.py [--provisional]
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib.io_raw import load_config, read_annotation_workbook, variable_specs  # noqa: E402
from lib.logging_utils import get_logger  # noqa: E402
from lib.tables import write_table  # noqa: E402

cfg = load_config()
SPECS = variable_specs(cfg)
VARS = list(SPECS)
LAB = cfg["scheme"].get("labels_en", {})
RAW = ROOT / cfg["paths"]["raw"]
INTERIM = ROOT / cfg["paths"]["interim"]
PROCESSED = ROOT / cfg["paths"]["processed"]
TABLES = ROOT / cfg["paths"]["tables"]
log = get_logger("05_error_analysis", ROOT / cfg["paths"]["logs"])

# Palabras clave superficiales por componente. Sirven para detectar el modo de fallo
# "sobre-etiquetado por palabra clave": el LLM marca 1 donde el humano marco 0 y el
# texto contiene una senal lexica del componente sin cumplir su funcion.
KEYWORDS = {
    "D1_imryd_objetivo": ["objetivo", "proposito", "finalidad", "busca ", "pretende"],
    "D1_imryd_metodologia": ["metodo", "metodolog", "diseno", "muestra", "encuesta", "cuestionario",
                             "entrevista", "experimental", "descriptiv", "correlacional", "cualitativ", "cuantitativ"],
    "D1_imryd_resultados": ["resultado", "se encontro", "se hallo", "%", "p<", "p <", "significativ"],
    "D1_imryd_conclusiones": ["se concluye", "conclusion", "se recomienda", "concluyo"],
    "D3_contextualizacion": ["problema", "importancia", "contexto", "actualidad", "situacion"],
    "D3_metodo_detallado": ["muestra", "diseno", "instrumento", "prueba", "cuestionario", "n="],
    "D3_resultados_concretos": ["%", "p<", "p <", "r=", "media", "promedio", "categor"],
    "D3_conclusion_responde": ["se concluye", "conclusion", "por lo tanto"],
}
COMPONENTS = ["D1_imryd_objetivo", "D1_imryd_metodologia", "D1_imryd_resultados", "D1_imryd_conclusiones"]
D3_OF_D1 = {"D3_metodo_detallado": "D1_imryd_metodologia",
            "D3_resultados_concretos": "D1_imryd_resultados",
            "D3_conclusion_responde": "D1_imryd_conclusiones"}


def norm(s: str) -> str:
    return unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()


def classify(v: str, human: float, llm: float, llm_row: pd.Series, text: str, n_words: int,
             runs_agree: bool) -> str:
    """Taxonomia preliminar, por reglas verificables. Se refina a mano en la revision."""
    t = norm(text)
    if v == "no_evaluable":
        return "assessability_mismatch"
    if SPECS[v]["type"] == "ordinal":
        d = llm - human
        sev = "severe" if abs(d) >= 2 else "mild"
        return f"ordinal_shift_{'up' if d > 0 else 'down'}_{sev}"
    # binarias
    if v in D3_OF_D1 and llm == 1 and llm_row.get(D3_OF_D1[v], 1) == 0:
        return "protocol_rule_violation_D3_without_D1"
    if v == "D1_orden_logico" and llm == 1 and sum(llm_row.get(c, 0) or 0 for c in COMPONENTS) <= 1:
        return "protocol_rule_violation_order_with_le1_component"
    if llm == 1 and human == 0:
        if any(k in t for k in KEYWORDS.get(v, [])):
            return "over_labeling_keyword_present"
        return "over_labeling_no_keyword"
    if llm == 0 and human == 1:
        if n_words >= 400:
            return "under_labeling_long_abstract"
        return "under_labeling"
    return "other"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provisional", action="store_true", help="humano = A1 solo (sin A2 independiente)")
    ap.add_argument("--run", default="r1", help="corrida del LLM que define la etiqueta (por defecto r1)")
    args = ap.parse_args()

    a2_ok = bool(cfg["annotators"]["A2"].get("independent", False))
    if not a2_ok and not args.provisional:
        log.error("A2 no es independiente. Sin consenso humano no hay 'fallos genuinos'. "
                  "Usa --provisional para una revision preliminar solo con A1.")
        return 1
    provisional = not a2_ok
    suffix = "_PROVISIONAL_A1only" if provisional else ""

    ann = pd.read_csv(INTERIM / "annotations.csv")
    docs = pd.read_csv(INTERIM / "documents.csv").set_index("doc_id")
    sub = set(pd.read_csv(PROCESSED / "subset.csv")["doc_id"])
    llm = pd.read_csv(PROCESSED / "llm_annotations.csv")
    notes_p = PROCESSED / "llm_notes.csv"
    llm_notes = pd.read_csv(notes_p) if notes_p.exists() else pd.DataFrame(columns=["doc_id", "annotator", "notes"])
    llm_notes = llm_notes.set_index(["annotator", "doc_id"])["notes"] if len(llm_notes) else pd.Series(dtype=str)
    # observaciones humanas, desde los cuadernillos crudos (esto NO es el paso ciego)
    h_notes = {}
    for h in (["A1", "A2"] if a2_ok else ["A1"]):
        wb = read_annotation_workbook(RAW / cfg["annotators"][h]["file"], cfg).set_index("doc_id")
        h_notes[h] = wb["notes"]

    H = {}
    for v in VARS:
        w = ann[(ann["category"] == v) & ann["doc_id"].isin(sub)].pivot_table(
            index="doc_id", columns="annotator", values="label", aggfunc="first")
        if a2_ok:
            ok = w["A1"].notna() & (w["A1"] == w["A2"])
            H[v] = w.loc[ok, "A1"]
        else:
            H[v] = w["A1"].dropna()
    Lw = {v: llm[llm["category"] == v].pivot_table(index="doc_id", columns="annotator", values="label", aggfunc="first")
          for v in VARS}
    models = sorted({a.split("#")[0] for a in llm["annotator"].unique()})

    rows = []
    for m in models:
        main_a = f"{m}#{args.run}"
        run_cols = [f"{m}#{r['name']}" for r in cfg["llm"]["runs"]]
        for v in VARS:
            if main_a not in Lw[v].columns:
                continue
            hv, lv = H[v], Lw[v][main_a].dropna()
            idx = hv.index.intersection(lv.index)
            for d in idx:
                if hv[d] == lv[d]:
                    continue
                runs_vals = {c.split("#")[1]: Lw[v][c].get(d) for c in run_cols if c in Lw[v].columns}
                present = [x for x in runs_vals.values() if pd.notna(x)]
                runs_agree = len(set(present)) == 1 if present else True
                llm_row = pd.Series({vv: Lw[vv][main_a].get(d) for vv in VARS if main_a in Lw[vv].columns})
                text = docs.loc[d, "text"] if d in docs.index else ""
                n_words = int(docs.loc[d, "n_words_text"]) if d in docs.index else 0
                ftype = classify(v, hv[d], lv[d], llm_row, text, n_words, runs_agree)
                rows.append({
                    "model": m, "doc_id": d, "variable": v, "variable_en": LAB.get(v, v),
                    "human_label": int(hv[d]), "llm_label": int(lv[d]),
                    "llm_runs": " ".join(f"{k}={'' if pd.isna(x) else int(x)}" for k, x in runs_vals.items()),
                    "llm_runs_agree": runs_agree,
                    "failure_type": ftype,
                    "n_words": n_words,
                    "llm_notes": llm_notes.get((main_a, d), "") if len(llm_notes) else "",
                    "human_notes_A1": h_notes["A1"].get(d, ""),
                    "human_notes_A2": h_notes["A2"].get(d, "") if a2_ok else "",
                    "title": docs.loc[d, "title"] if d in docs.index else "",
                    "text_excerpt": str(text)[:400],
                    "reviewer_verdict": "",      # a rellenar a mano
                    "reviewer_notes": "",
                })
    out = pd.DataFrame(rows)
    if out.empty:
        log.warning("sin discrepancias (¿faltan anotaciones LLM?)")
        return 0
    out = out.sort_values(["model", "variable", "failure_type", "doc_id"])
    out_path = TABLES / f"disagreements_for_review{suffix}.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    log.info("%d casos -> %s", len(out), out_path)

    counts = out.pivot_table(index=["model", "variable"], columns="failure_type", values="doc_id",
                             aggfunc="count", fill_value=0).reset_index()
    write_table(counts, TABLES, f"error_taxonomy_counts{suffix}",
                caption="Preliminary failure-mode taxonomy: number of LLM–human disagreements by model, "
                        "variable and rule-based type." + (" PROVISIONAL (A1 only)." if provisional else ""),
                label="tab:error-taxonomy")

    # informe con ejemplos citables
    R = [f"# Error analysis{' (PROVISIONAL: human = A1 only)' if provisional else ''}\n",
         f"Generated {datetime.now().isoformat(timespec='seconds')}. LLM label = run {args.run}; "
         f"`llm_runs_agree` marks whether all runs gave the same label.\n"]
    if provisional:
        R.append("> **Not for the paper.** Without an independent A2 these are LLM–A1 disagreements, not "
                 "genuine model failures. Re-run without --provisional once A2 exists.\n")
    R.append("## Counts by model and failure type\n")
    R.append(out.groupby(["model", "failure_type"]).size().rename("n").reset_index()
             .pivot(index="failure_type", columns="model", values="n").fillna(0).astype(int).to_markdown())
    R.append("\n## Examples per failure type (up to 5, prefer cases where all runs agree)\n")
    for ft, g in out.groupby("failure_type"):
        R.append(f"### {ft} (n = {len(g)})\n")
        g = g.sort_values(["llm_runs_agree", "n_words"], ascending=[False, True])
        for _, r in g.head(5).iterrows():
            quote = re.sub(r"\s+", " ", str(r["text_excerpt"]))[:220]
            R.append(f"- **{r['doc_id']}** · {r['model']} · {r['variable_en']}: human = {r['human_label']}, "
                     f"LLM = {r['llm_label']} ({r['llm_runs']}; agree = {r['llm_runs_agree']}; {r['n_words']} words)")
            R.append(f"  - Text: «{quote}…»")
            if str(r["llm_notes"]).strip():
                R.append(f"  - LLM note: {str(r['llm_notes'])[:220]}")
            if str(r["human_notes_A1"]).strip():
                R.append(f"  - A1 note: {str(r['human_notes_A1'])[:220]}")
        R.append("")
    rep = ROOT / "outputs" / f"error_analysis_report{suffix}.md"
    rep.write_text("\n".join(R) + "\n", encoding="utf-8")
    log.info("informe -> %s", rep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
