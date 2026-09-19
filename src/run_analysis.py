"""Ejecuta el analisis completo de una vez: fases 2(recoleccion)-3-4-5-6.

Se detiene en el primer fallo y dice en que fase. Antes de empezar comprueba que
todas las corridas de LLM esten completas, porque ejecutar la fase 3 con datos
parciales produce cifras que parecen definitivas y no lo son.

Uso:
  python src/run_analysis.py              # exige cobertura completa
  python src/run_analysis.py --partial    # permite corridas incompletas (marca el informe)
  python src/run_analysis.py --quick      # 200 remuestreos en vez de 2000 (solo pruebas)
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib.io_raw import load_config  # noqa: E402

cfg = load_config()
PROCESSED = ROOT / cfg["paths"]["processed"]


def run(step: str, args: list[str]) -> None:
    print(f"\n{'=' * 72}\n{step}\n{'=' * 72}", flush=True)
    t0 = time.time()
    r = subprocess.run([sys.executable, *args], cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(f"\nFALLO en {step} (codigo {r.returncode}). Nada mas se ejecuta.")
    print(f"-> {step} OK en {time.time() - t0:.0f} s", flush=True)


def check_coverage(allow_partial: bool) -> None:
    n_docs = len(pd.read_csv(PROCESSED / "subset.csv"))
    runs = [r["name"] for r in cfg["llm"]["runs"]]
    expected = {f"{m['name']}#{r}" for m in (cfg["llm"].get("models") or []) for r in runs}
    p = PROCESSED / "llm_annotations.csv"
    have = pd.read_csv(p) if p.exists() else pd.DataFrame(columns=["annotator", "doc_id"])
    cov = have.groupby("annotator")["doc_id"].nunique() if len(have) else pd.Series(dtype=int)
    print(f"\nCobertura esperada: {len(expected)} anotadores LLM x {n_docs} documentos")
    incomplete = []
    for a in sorted(expected):
        n = int(cov.get(a, 0))
        mark = "ok" if n == n_docs else f"INCOMPLETO ({n_docs - n} faltan)"
        print(f"  {a:22s} {n:3d}/{n_docs}  {mark}")
        if n != n_docs:
            incomplete.append(a)
    if incomplete and not allow_partial:
        raise SystemExit(
            f"\n{len(incomplete)} corridas incompletas. La fase 3 produciria cifras parciales "
            f"con aspecto de definitivas.\nEspera a que terminen, o usa --partial si lo quieres igualmente.")
    if incomplete:
        print(f"\nAVISO: {len(incomplete)} corridas incompletas; los resultados son provisionales.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partial", action="store_true")
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()

    t0 = time.time()
    run("Fase 2 - recoleccion del cache", ["src/02_annotate_llm.py", "--collect-only"])
    check_coverage(args.partial)
    run("Fase 3 - concordancia", ["src/03_agreement.py"] + (["--quick"] if args.quick else []))
    run("Fase 4 - figuras", ["src/04_figures.py"])
    run("Fase 5 - analisis del error",
        ["src/05_error_analysis.py"] + ([] if cfg["annotators"]["A2"].get("independent") else ["--provisional"]))
    run("Fase 6 - empaquetado", ["src/06_package_release.py"])
    print(f"\n{'=' * 72}\nTODO OK en {(time.time() - t0) / 60:.1f} min")
    print("  outputs/agreement_report.md      concordancia y contraste")
    print("  outputs/error_analysis_report.md modos de fallo")
    print("  outputs/tables/                  CSV + LaTeX")
    print("  outputs/figures/                 PDF + PNG 300 dpi")
    print("  outputs/dataset_release/         paquete para Zenodo")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
