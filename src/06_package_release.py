"""Fase 6 - Empaquetado del dataset para deposito en Zenodo.

Produce outputs/dataset_release/ con:
  - annotations.csv        anotaciones humanas y de LLM en formato largo
  - documents.csv          metadatos por documento (sin titulo ni texto por defecto)
  - annotator_notes.csv    observaciones libres, tras el escaneo de identificadores
  - codebook/              el manual de codificacion literal
  - data_dictionary.csv    una fila por campo de cada tabla
  - README.md              licencia CC-BY-4.0, cita sugerida, metodo y limitaciones
  - CHECKSUMS.sha256

Dos comprobaciones que bloquean el empaquetado si fallan:
  1. Escaneo de identificadores personales (correos, DNI, codigos de estudiante,
     telefonos) en TODOS los campos de texto que se publican.
  2. Ningun campo con el titulo de la tesis ni el texto del resumen, salvo que se
     active explicitamente `release.include_text`.

Nada se redacta automaticamente: si aparece algo, se reporta y se aborta para que
lo revise una persona.

Uso:  python src/06_package_release.py [--force]
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import stat
import sys
import unicodedata
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib.io_raw import load_config, read_annotation_workbook, read_master_key, variable_specs  # noqa: E402
from lib.logging_utils import get_logger  # noqa: E402

cfg = load_config()
SPECS = variable_specs(cfg)
VARS = list(SPECS)
LAB = cfg["scheme"].get("labels_en", {})
RAW = ROOT / cfg["paths"]["raw"]
INTERIM = ROOT / cfg["paths"]["interim"]
PROCESSED = ROOT / cfg["paths"]["processed"]
REL = ROOT / "outputs" / "dataset_release"
R = cfg.get("release", {})
log = get_logger("06_package_release", ROOT / cfg["paths"]["logs"])

# Patrones de identificadores personales. Se aplican a todo texto publicado.
PII = {
    "correo": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "dni_peruano": re.compile(r"\b\d{8}\b"),
    "codigo_estudiante": re.compile(r"\b(?:cod(?:igo)?|matricula|c\.?u\.?)\s*[:.\-]?\s*\d{6,}\b", re.I),
    "telefono": re.compile(r"\b(?:\+?51\s?)?9\d{8}\b"),
    "orcid": re.compile(r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dX]\b"),
    "url_repositorio": re.compile(r"https?://\S*(?:handle|repositorio)\S*", re.I),
}


def norm(s: str) -> str:
    return unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()


def scan_pii(df: pd.DataFrame, table: str) -> pd.DataFrame:
    """Busca identificadores en cada celda de texto. Devuelve los hallazgos."""
    hits = []
    for col in df.columns:
        if df[col].dtype != object:
            continue
        for idx, val in df[col].dropna().items():
            t = norm(val)
            for kind, rx in PII.items():
                for m in rx.findall(t):
                    hits.append({"table": table, "column": col, "row": idx,
                                 "kind": kind, "match": str(m)[:80],
                                 "context": t[max(0, t.find(str(m)) - 40):t.find(str(m)) + 60]})
    return pd.DataFrame(hits)


def data_dictionary() -> pd.DataFrame:
    rows = [
        ("annotations.csv", "doc_id", "string", "Anonymous document identifier (GT-nnn)."),
        ("annotations.csv", "annotator", "string",
         "A1, A2 (human annotators) or <model>#<run> for LLM runs."),
        ("annotations.csv", "category", "string", "Variable of the coding scheme (see codebook)."),
        ("annotations.csv", "label", "integer",
         "Assigned value. 0/1 for binary variables, 1-5 for ordinal ones. "
         "An absent row means 'not annotated'; nothing is imputed."),
        ("documents.csv", "doc_id", "string", "Anonymous document identifier."),
        ("documents.csv", "phase", "string", "calibration or principal."),
        ("documents.csv", "stratum", "string", "OECD/FORD discipline area used for stratified sampling."),
        ("documents.csv", "thesis_type", "string", "bachelorThesis, masterThesis, doctoralThesis, Thesis."),
        ("documents.csv", "institution", "string", "Repository code (UNAP, UPEU, UPSC, UANCV)."),
        ("documents.csv", "year", "integer", "Year of deposit (2016-2026)."),
        ("documents.csv", "abstract_words", "integer", "Length of the abstract in words."),
        ("documents.csv", "handle", "string",
         "Persistent public URL of the thesis record in its institutional repository. "
         "Present only if release.include_handle is true; it is the pointer that makes "
         "the abstract text retrievable without redistributing it."),
        ("annotator_notes.csv", "doc_id", "string", "Anonymous document identifier."),
        ("annotator_notes.csv", "annotator", "string", "A1, A2 or <model>#<run>."),
        ("annotator_notes.csv", "notes", "string",
         "Free-text justification written while annotating. Screened for personal identifiers."),
    ]
    extra = [("annotations.csv", f"category = {v}", SPECS[v]["type"],
              f"{LAB.get(v, v)}; levels {SPECS[v]['levels']}; dimension {SPECS[v]['dimension']}.")
             for v in VARS]
    return pd.DataFrame(rows + extra, columns=["file", "field", "type", "description"])


def readme(n_docs: int, n_ann: int, annotators: list[str], models: list[dict]) -> str:
    today = date.today().isoformat()
    cite = R.get("citation", "<AUTHORS> (<YEAR>). <TITLE> [Data set]. Zenodo. https://doi.org/<DOI>")
    model_rows = "\n".join(
        f"| {m['name']} | `{m['model']}` | {m['provider']} | {R.get('llm_call_dates', 'see logs')} |"
        for m in models) or "| — | — | — | — |"
    return f"""# Human–LLM agreement on the structural quality of thesis abstracts — annotation dataset

Released {today}. Version {R.get('version', '1.0.0')}.

## What this is

Independent annotations of {n_docs} Spanish-language thesis abstracts by two human
annotators and by several open-weight language models, using a single coding
protocol with 12 variables (10 binary, 2 ordinal 1–5) over four dimensions:
IMRaD adherence, organisational coherence, component completeness and
methodological consistency.

The dataset supports the question the study asks: *is the disagreement between a
language model and a human annotator distinguishable from the disagreement that
already exists between two human annotators, and in which variables does that
equivalence break?*

## Files

| File | Rows | Description |
|---|---|---|
| `annotations.csv` | {n_ann} | Long format: one row per (document, annotator, variable). |
| `documents.csv` | {n_docs} | Document-level metadata. |
| `annotator_notes.csv` | — | Free-text justifications written during annotation. |
| `codebook/PROTOCOLO_ANOTACION.md` | — | The coding manual, verbatim, in Spanish. |
| `data_dictionary.csv` | — | One row per field. |
| `CHECKSUMS.sha256` | — | Integrity of every file above. |

## What is NOT included, and why

**Abstract texts and thesis titles are not redistributed.** They were harvested via
OAI-PMH from four public institutional repositories in Puno, Peru, and their
copyright belongs to the respective authors and institutions; this dataset does not
hold the rights to relicense them. `documents.csv` carries the persistent `handle`
of each record, so anyone can retrieve the exact text from the source repository
and reproduce the analysis.

Annotators are identified only as A1 and A2. Free-text notes were screened for
e-mail addresses, national identity numbers, student codes, phone numbers and
ORCIDs; the scan is reported in the study repository.

## Coding scheme

See `codebook/`. In brief, for each abstract:

| Variable | Type | Levels |
|---|---|---|
{chr(10).join(f"| `{v}` | {SPECS[v]['type']} | {SPECS[v]['levels']} |" for v in VARS)}

Two rules of the protocol create structural blanks that are **not** missing data:
§9.3 leaves `D4_consistencia` empty when `no_evaluable = 1`, and §10 leaves every
field empty when the text is not an abstract at all.

## Annotators and models

Human annotators: {', '.join(annotators)}. Both applied the same protocol
independently; the second annotator worked from a blinded workbook containing no
labels or notes from the first.

| Name | Exact model id | Provider | Call dates |
|---|---|---|---|
{model_rows}

The exact model version and the date of the calls are part of the method: models
change over time and results are not reproducible without them.

## Licence

Annotations, notes, metadata and the coding protocol: **CC BY 4.0**
(https://creativecommons.org/licenses/by/4.0/). Attribution as below. The abstract
texts are not part of this release and remain under their original terms.

## Suggested citation

> {cite}

## Reproducing the analysis

The full pipeline — audit, LLM annotation, agreement statistics, figures and error
analysis — is in the study repository, with pinned dependency versions and a fixed
random seed (42). Bootstrap confidence intervals resample **documents**, not
individual annotations.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="empaquetar aunque el escaneo encuentre algo")
    args = ap.parse_args()

    # ------------------------------------------------------------------ cargar
    ann = pd.read_csv(INTERIM / "annotations.csv")
    llm_p = PROCESSED / "llm_annotations.csv"
    if llm_p.exists():
        ann = pd.concat([ann, pd.read_csv(llm_p)], ignore_index=True)
    sub = set(pd.read_csv(PROCESSED / "subset.csv")["doc_id"])
    ann = ann[ann["doc_id"].isin(sub)].sort_values(["doc_id", "annotator", "category"])

    key = read_master_key(RAW / cfg["corpus"]["master_key"])
    docs = key[key["doc_id"].isin(sub)].copy()
    docs = docs.rename(columns={"fase": "phase", "estrato": "stratum", "tipo": "thesis_type",
                                "institucion_cod": "institution", "anio": "year",
                                "resumen_palabras": "abstract_words"})
    cols = ["doc_id", "phase", "stratum", "thesis_type", "institution", "year", "abstract_words"]
    if R.get("include_handle", True):
        cols.append("handle")
    docs = docs[cols]
    if R.get("include_text", False):
        txt = pd.read_csv(INTERIM / "documents.csv")[["doc_id", "title", "text"]]
        docs = docs.merge(txt, on="doc_id", how="left")
        log.warning("release.include_text = true: se publican titulo y texto. "
                    "Comprueba que tienes derecho a redistribuirlos.")

    # observaciones: humanas (de los cuadernillos) + de los LLM
    notes = []
    for a in ("A1", "A2"):
        wb = read_annotation_workbook(RAW / cfg["annotators"][a]["file"], cfg)
        wb = wb[wb["doc_id"].isin(sub) & wb["notes"].notna()]
        notes.append(pd.DataFrame({"doc_id": wb["doc_id"], "annotator": a, "notes": wb["notes"]}))
    ln = PROCESSED / "llm_notes.csv"
    if ln.exists():
        n = pd.read_csv(ln)
        notes.append(n[n["doc_id"].isin(sub)][["doc_id", "annotator", "notes"]])
    notes = pd.concat(notes, ignore_index=True).sort_values(["doc_id", "annotator"])

    # ------------------------------------------------- comprobaciones que bloquean
    problems: list[str] = []
    scans = pd.concat([scan_pii(docs, "documents.csv"), scan_pii(notes, "annotator_notes.csv")],
                      ignore_index=True)
    # El handle es un identificador publico y persistente, no personal: se admite
    # en documents.csv si se ha pedido, pero nunca dentro de una observacion.
    allowed = (scans["kind"] == "url_repositorio") & (scans["table"] == "documents.csv") \
        & bool(R.get("include_handle", True))
    scans = scans[~allowed]
    if len(scans):
        problems.append(f"{len(scans)} posibles identificadores personales en los campos publicados")

    if not R.get("include_text", False):
        for df, name in ((docs, "documents.csv"), (notes, "annotator_notes.csv")):
            for c in ("title", "text", "titulo", "resumen"):
                if c in df.columns:
                    problems.append(f"{name} contiene la columna '{c}' y release.include_text es false")

    print("\n" + "=" * 72)
    print("COMPROBACIONES PREVIAS AL DEPOSITO")
    print("=" * 72)
    print(f"documentos: {len(docs)} · anotaciones: {len(ann)} · observaciones: {len(notes)}")
    print(f"anotadores: {sorted(ann['annotator'].unique())}")
    print(f"escaneo de identificadores: {len(scans)} hallazgos")
    if len(scans):
        print(scans.head(20).to_string(index=False))
        (ROOT / "outputs" / "pii_scan.csv").write_text(scans.to_csv(index=False), encoding="utf-8")
        print(f"\ninforme completo -> outputs/pii_scan.csv")
    if problems and not args.force:
        print("\nNO SE EMPAQUETA:")
        for p in problems:
            print(f"  [ERROR] {p}")
        print("\nRevisa los hallazgos. Si son falsos positivos, vuelve a lanzar con --force.")
        print("=" * 72)
        return 2
    for p in problems:
        log.warning("ignorado por --force: %s", p)

    # --------------------------------------------------------------- empaquetar
    if REL.exists():
        # Los archivos copiados de data/raw/ heredan el atributo de solo lectura y
        # rmtree no puede borrarlos en Windows: se quita a todo el arbol primero.
        for q in REL.rglob("*"):
            try:
                os.chmod(q, stat.S_IWRITE | stat.S_IREAD)
            except OSError:
                pass
        shutil.rmtree(REL)
    (REL / "codebook").mkdir(parents=True)
    ann.to_csv(REL / "annotations.csv", index=False, encoding="utf-8")
    docs.to_csv(REL / "documents.csv", index=False, encoding="utf-8")
    notes.to_csv(REL / "annotator_notes.csv", index=False, encoding="utf-8")
    data_dictionary().to_csv(REL / "data_dictionary.csv", index=False, encoding="utf-8")
    cb = REL / "codebook" / "PROTOCOLO_ANOTACION.md"
    shutil.copy2(RAW / cfg["llm"]["prompt"]["protocol_file"], cb)
    os.chmod(cb, stat.S_IWRITE | stat.S_IREAD)   # el original es de solo lectura; la copia no

    humans = [a for a in ("A1", "A2") if a in set(ann["annotator"])]
    models = [m for m in (cfg["llm"].get("models") or [])
              if any(str(a).startswith(m["name"]) for a in ann["annotator"].unique())]
    (REL / "README.md").write_text(readme(len(docs), len(ann), humans, models), encoding="utf-8")

    lines = []
    for p in sorted(REL.rglob("*")):
        if p.is_file() and p.name != "CHECKSUMS.sha256":
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            lines.append(f"{h}  {p.relative_to(REL).as_posix()}")
    (REL / "CHECKSUMS.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\nEMPAQUETADO OK ->", REL.relative_to(ROOT))
    for p in sorted(REL.rglob("*")):
        if p.is_file():
            print(f"  {p.relative_to(REL).as_posix():40s} {p.stat().st_size:>9,} B")
    print("=" * 72)
    log.info("dataset_release listo (%d archivos)", len(lines) + 1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
