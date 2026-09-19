"""Lectura de los archivos crudos SIN asumir su estructura mas alla de config.yaml.

Cada lector valida lo que espera encontrar y falla con un mensaje explicito si
no lo encuentra. Nunca rellena ni imputa.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_config(path: Path | None = None) -> dict:
    path = path or ROOT / "config.yaml"
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def variable_specs(cfg: dict) -> dict[str, dict]:
    """Devuelve {nombre_canonico: {excel, type, levels, dimension}}."""
    return cfg["scheme"]["variables"]


def read_annotation_workbook(path: Path, cfg: dict) -> pd.DataFrame:
    """Lee un cuadernillo .xlsx o una plantilla .csv y devuelve columnas canonicas.

    Columnas de salida: doc_id, <12 variables canonicas>, title, text, notes.
    Los valores se dejan tal cual (float con NaN): la validacion del dominio es
    tarea de la auditoria, que debe REPORTAR los valores ajenos, no ocultarlos.
    """
    path = Path(path)
    sch = cfg["scheme"]
    specs = variable_specs(cfg)

    if path.suffix.lower() in {".xlsx", ".xlsm"}:
        xl = pd.ExcelFile(path)
        if sch["sheet"] not in xl.sheet_names:
            raise ValueError(f"{path.name}: falta la hoja '{sch['sheet']}'. Hojas: {xl.sheet_names}")
        df = xl.parse(sch["sheet"])
        colmap = {sch["id_column"]: "doc_id"}
        for canon, spec in specs.items():
            colmap[spec["excel"]] = canon
        optional = {sch["title_column"]: "title", sch["text_column"]: "text",
                    sch["notes_column"]: "notes"}
    elif path.suffix.lower() == ".csv":
        # Las plantillas CSV usan ya los nombres canonicos del protocolo.
        df = pd.read_csv(path, encoding="utf-8-sig")
        colmap = {"id_anotacion": "doc_id"}
        for canon in specs:
            colmap[canon] = canon
        optional = {"observaciones": "notes"}
    else:
        raise ValueError(f"formato no soportado: {path}")

    missing = [c for c in colmap if c not in df.columns]
    if missing:
        raise ValueError(f"{path.name}: faltan columnas {missing}. Presentes: {list(df.columns)}")

    out = df.rename(columns=colmap)
    for src, dst in optional.items():
        if src in out.columns:
            out = out.rename(columns={src: dst})
    # Las plantillas CSV no traen titulo ni texto: se dejan vacios, no se inventan.
    for dst in ("title", "text", "notes"):
        if dst not in out.columns:
            out[dst] = pd.NA
    keep = ["doc_id", *specs.keys(), "title", "text", "notes"]
    out = out[keep].copy()
    out["doc_id"] = out["doc_id"].astype(str).str.strip()
    return out


def read_master_key(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    required = {"id_anotacion", "fase", "tipo", "institucion_cod", "anio",
                "estrato", "resumen_palabras"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"clave maestra: faltan columnas {sorted(missing)}")
    return df.rename(columns={"id_anotacion": "doc_id"})


def to_long(df: pd.DataFrame, annotator: str, cfg: dict) -> pd.DataFrame:
    """Formato largo canonico: doc_id, annotator, category, label.

    Solo se emiten celdas NO vacias: una fila ausente significa 'no anotado',
    nunca se escribe un valor de relleno.
    """
    specs = variable_specs(cfg)
    long = df.melt(id_vars=["doc_id"], value_vars=list(specs.keys()),
                   var_name="category", value_name="label")
    long = long.dropna(subset=["label"]).copy()
    long["annotator"] = annotator
    long["label"] = long["label"].astype(float)
    # Etiquetas enteras: 0/1 o 1..5. Un 2.5 seria un valor fuera del esquema y
    # se conserva tal cual para que la auditoria lo detecte.
    is_int = (long["label"] % 1 == 0)
    long.loc[is_int, "label"] = long.loc[is_int, "label"].astype(int)
    return long[["doc_id", "annotator", "category", "label"]].sort_values(
        ["doc_id", "annotator", "category"]).reset_index(drop=True)
