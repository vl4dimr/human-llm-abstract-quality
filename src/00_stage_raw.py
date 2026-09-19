"""Copia los archivos fuente originales a data/raw/ y registra su procedencia.

Los originales estan dispersos por el disco del investigador. Este script los
copia (nunca los mueve ni los modifica) y escribe un manifiesto con SHA-256 para
que cualquier persona pueda verificar que analiza exactamente los mismos bytes.

Uso:  python src/00_stage_raw.py [--force]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib.logging_utils import get_logger  # noqa: E402

RAW = ROOT / "data" / "raw"

# (destino_en_data_raw, ruta_origen_absoluta, nota de procedencia)
SOURCES: list[tuple[str, str, str]] = [
    ("annotations/Anotacion_principal_A1.xlsx",
     r"C:/Users/LENOVO/Downloads/vlad/DATOS/Anotacion_principal_A1 (1).xlsx",
     "A1, fase principal. Copia mas reciente (mtime 2026-08-11 22:27)."),
    ("annotations/Anotacion_principal_A1_REV.xlsx",
     r"C:/Users/LENOVO/Downloads/vlad/Anotacion_principal_A1 -REV.xlsx",
     "A1, fase principal, version '-REV' (mtime 2026-08-11 22:09)."),
    ("annotations/Anotacion_principal_A1_v0.xlsx",
     r"C:/Users/LENOVO/Downloads/vlad/Anotacion_principal_A1.xlsx",
     "A1, fase principal, version mas antigua y parcial (mtime 2026-08-11 21:52)."),
    ("annotations/Anotacion_principal_A2.xlsx",
     r"C:/Users/LENOVO/Downloads/vlad/DATOS/Anotacion_principal_A2.xlsx",
     "A2 ORIGINAL: copia exacta de A1, NO independiente. Se conserva solo como "
     "evidencia de la auditoria; no entra en el analisis."),
    ("annotations/Anotacion_principal_A2_independiente.xlsx",
     r"C:/Users/LENOVO/Documents/paers/Anotacion_subset160_A2.xlsx",
     "A2 REAL: 160 documentos del subconjunto, anotados a ciegas sobre el cuadernillo "
     "generado el 2026-09-17; entregado el 2026-09-18. Validado por 00c_receive_a2.py: "
     "147/1920 celdas distintas de A1, 0 observaciones identicas."),
    ("annotations/Anotacion_calibracion_A2_independiente.xlsx",
     r"C:/Users/LENOVO/Documents/paers/Anotacion_calibracion_A2.xlsx",
     "A2 REAL, fase de calibracion (30 documentos). Excluida del analisis principal."),
    ("annotations/Anotacion_calibracion_A1.xlsx",
     r"C:/Users/LENOVO/Downloads/vlad/DATOS/Anotacion_calibracion_A1.xlsx",
     "A1, fase de calibracion (30 resumenes)."),
    ("annotations/Anotacion_calibracion_A2.xlsx",
     r"C:/Users/LENOVO/Downloads/vlad/DATOS/Anotacion_calibracion_A2.xlsx",
     "A2, fase de calibracion (30 resumenes)."),
    ("annotations/Anotacion_principal_A3_template.csv",
     r"C:/Users/LENOVO/Documents/analisis/tesis_doctoral/ground_truth/anotacion_principal_A3.csv",
     "A3, plantilla de la fase principal."),
    ("llm_prior/Anotacion_IA_Claude.xlsx",
     r"C:/Users/LENOVO/Downloads/vlad/DATOS/Anotacion_IA_Claude-c.xlsx",
     "Anotacion LLM previa, hecha via claude.ai. NO es la corrida de la fase 2."),
    ("scheme/PROTOCOLO_ANOTACION.md",
     r"C:/Users/LENOVO/Documents/analisis/tesis_doctoral/ground_truth/PROTOCOLO_ANOTACION.md",
     "Manual de codificacion. Fuente literal del prompt de la fase 2."),
    ("corpus/clave_maestra.csv",
     r"C:/Users/LENOVO/Documents/analisis/tesis_doctoral/ground_truth/clave_maestra.csv",
     "Clave id_anotacion -> tesis real. CONTIENE IDENTIFICADORES: excluir del deposito."),
    ("corpus/cuadernillo_principal.txt",
     r"C:/Users/LENOVO/Documents/analisis/tesis_doctoral/ground_truth/cuadernillo_principal.txt",
     "Cuadernillo entregado a los anotadores (fase principal)."),
    ("corpus/CORPUS.md",
     r"C:/Users/LENOVO/Documents/analisis/tesis_doctoral/CORPUS.md",
     "Descripcion del corpus del que se muestrearon los 330 resumenes."),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="sobrescribe los archivos ya presentes en data/raw")
    args = ap.parse_args()

    log = get_logger("00_stage_raw", ROOT / "outputs" / "logs")
    manifest = []
    missing = []

    for dest_rel, src_str, note in SOURCES:
        src = Path(src_str)
        dest = RAW / dest_rel
        if not src.exists():
            # Regla dura: si falta algo, fallamos ruidosamente. No se inventa nada.
            missing.append(src_str)
            log.error("FALTA el origen: %s", src_str)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and not args.force:
            log.info("ya presente, no se toca: %s", dest_rel)
        else:
            if dest.exists():
                os.chmod(dest, stat.S_IWRITE | stat.S_IREAD)
            shutil.copy2(src, dest)
            # Marcar solo lectura: data/raw es intocable.
            os.chmod(dest, stat.S_IREAD)
            log.info("copiado: %s  <-  %s", dest_rel, src_str)
        manifest.append({
            "path": dest_rel,
            "source": src_str,
            "note": note,
            "bytes": dest.stat().st_size,
            "sha256": sha256(dest),
            "source_mtime_utc": datetime.fromtimestamp(
                src.stat().st_mtime, tz=timezone.utc).isoformat(),
        })

    if missing:
        log.error("Faltan %d archivos de origen. Abortando sin escribir manifiesto.", len(missing))
        return 1

    out = RAW / "PROVENANCE.json"
    if out.exists():
        os.chmod(out, stat.S_IWRITE | stat.S_IREAD)
    payload = {
        "staged_at_utc": datetime.now(timezone.utc).isoformat(),
        "staged_by": "src/00_stage_raw.py",
        "files": manifest,
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    os.chmod(out, stat.S_IREAD)
    log.info("manifiesto escrito: %s (%d archivos)", out.relative_to(ROOT), len(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
