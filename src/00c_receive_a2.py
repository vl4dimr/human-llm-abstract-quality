"""Fase 1c - Recepcion y validacion del cuadernillo devuelto por A2.

Comprueba, ANTES de dejar entrar el archivo en el analisis:
  1. Estructura: hoja, columnas, ids y textos identicos a los que se enviaron.
  2. Completitud: casillas rellenadas, filas sin anotar.
  3. Dominio: ningun valor fuera del esquema.
  4. Reglas del protocolo (§9.3, §6.5, §8.4).
  5. INDEPENDENCIA: que no sea una copia de A1 (celdas identicas y observaciones
     literalmente iguales). Este es el fallo que ya ocurrio una vez en este estudio.

No modifica nada por su cuenta. Si todo pasa, indica el unico cambio que hay que
hacer en config.yaml para que el analisis use a A2.

Uso:
  python src/00c_receive_a2.py <archivo_devuelto.xlsx> [--install]
  --install copia el archivo a data/raw/annotations/ (solo si no hay errores duros)
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import stat
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib.io_raw import load_config, read_annotation_workbook, variable_specs  # noqa: E402
from lib.logging_utils import get_logger  # noqa: E402

cfg = load_config()
SPECS = variable_specs(cfg)
VARS = list(SPECS)
RAW = ROOT / cfg["paths"]["raw"]
log = get_logger("00c_receive_a2", ROOT / cfg["paths"]["logs"])

COMPONENTS = ["D1_imryd_objetivo", "D1_imryd_metodologia", "D1_imryd_resultados", "D1_imryd_conclusiones"]
D3_OF_D1 = {"D3_metodo_detallado": "D1_imryd_metodologia",
            "D3_resultados_concretos": "D1_imryd_resultados",
            "D3_conclusion_responde": "D1_imryd_conclusiones"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("returned", help="archivo .xlsx devuelto por A2")
    ap.add_argument("--sent", default="outputs/for_annotation/Anotacion_subset160_A2_CIEGO.xlsx",
                    help="cuadernillo ciego que se envio")
    ap.add_argument("--install", action="store_true", help="copiar a data/raw/annotations/ si no hay errores duros")
    args = ap.parse_args()

    ret_path = Path(args.returned)
    sent_path = ROOT / args.sent
    if not ret_path.exists():
        log.error("no existe: %s", ret_path)
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    try:
        ret = read_annotation_workbook(ret_path, cfg)
    except Exception as e:  # noqa: BLE001
        log.error("no se puede leer el cuadernillo: %s", e)
        return 1
    sent = read_annotation_workbook(sent_path, cfg)

    print("\n" + "=" * 72)
    print(f"VALIDACION DE {ret_path.name}")
    print("=" * 72)

    # ---------------------------------------------------------------- 1. estructura
    if set(ret["doc_id"]) != set(sent["doc_id"]):
        falta = sorted(set(sent["doc_id"]) - set(ret["doc_id"]))
        sobra = sorted(set(ret["doc_id"]) - set(sent["doc_id"]))
        errors.append(f"los ids no coinciden con el cuadernillo enviado (faltan {len(falta)}, sobran {len(sobra)})")
    if ret["doc_id"].duplicated().any():
        errors.append(f"{int(ret['doc_id'].duplicated().sum())} ids duplicados")
    common = ret.set_index("doc_id").index.intersection(sent.set_index("doc_id").index)
    r_i, s_i = ret.set_index("doc_id").loc[common], sent.set_index("doc_id").loc[common]
    txt_diff = int((r_i["text"].fillna("").astype(str).str.strip()
                    != s_i["text"].fillna("").astype(str).str.strip()).sum())
    if txt_diff:
        errors.append(f"{txt_diff} resumenes tienen un texto distinto del que se envio")
    print(f"\n1. Estructura: {len(ret)} filas · ids coinciden: {set(ret['doc_id']) == set(sent['doc_id'])} · "
          f"textos alterados: {txt_diff}")

    # -------------------------------------------------------------- 2. completitud
    annotated = r_i[VARS].notna().any(axis=1)
    n_ann = int(annotated.sum())
    filled = {v: int(r_i[v].notna().sum()) for v in VARS}
    ne1 = (r_i["no_evaluable"] == 1)
    others = [v for v in VARS if v != "no_evaluable"]
    # §10: "si no es un resumen en absoluto, deja todos los demas campos vacios".
    # Esas filas no son incompletas: son la aplicacion de la regla.
    not_abstract = ne1 & r_i[others].isna().all(axis=1)
    # §9.3: D4 vacia cuando no_evaluable = 1.
    d4_expected = len(common) - int(ne1.sum())
    print(f"2. Completitud: {n_ann}/{len(common)} filas anotadas "
          f"({100 * n_ann / max(len(common), 1):.0f} %) · "
          f"{int(not_abstract.sum())} marcadas 'no es un resumen' (§10, en blanco a proposito)")
    for v in VARS:
        if v == "D4_consistencia":
            exp = d4_expected
        elif v == "no_evaluable":
            exp = len(common)
        else:
            exp = len(common) - int(not_abstract.sum())
        mark = "ok" if filled[v] >= exp else f"FALTAN {exp - filled[v]}"
        print(f"     {SPECS[v]['excel']:22s} {filled[v]:4d}/{exp:<4d} {mark}")
    if n_ann < len(common):
        errors.append(f"{len(common) - n_ann} filas sin anotar (no se imputa nada: hay que completarlas)")
    obs = int(r_i["notes"].notna().sum())
    print(f"     Observaciones rellenadas: {obs}/{len(common)}")
    if obs < 0.2 * len(common):
        warnings.append(f"pocas observaciones ({obs}); el protocolo (§10) pide usarlas con generosidad")

    # ------------------------------------------------------------------ 3. dominio
    bad = []
    for v in VARS:
        allowed = {float(x) for x in SPECS[v]["levels"]}
        m = r_i[v].notna() & ~r_i[v].isin(allowed)
        for d in r_i.index[m]:
            bad.append((d, v, r_i.loc[d, v]))
    print(f"3. Valores fuera del esquema: {len(bad)}")
    for d, v, x in bad[:10]:
        print(f"     {d} {v} = {x!r}")
    if bad:
        errors.append(f"{len(bad)} valores fuera del esquema")

    # ------------------------------------------------------------------ 4. reglas
    v_d3 = sum(int(((r_i[d1] == 0) & (r_i[d3] == 1)).sum()) for d3, d1 in D3_OF_D1.items())
    s = r_i[COMPONENTS].sum(axis=1)
    v_ord = int(((s <= 1) & (r_i["D1_orden_logico"] == 1)).sum())
    v_d4 = int((ne1 & r_i["D4_consistencia"].notna()).sum())
    print(f"4. Reglas del protocolo: D3=1 con D1=0 (§8.4): {v_d3} · "
          f"orden=1 con ≤1 componente (§6.5): {v_ord} · no_evaluable=1 con D4 relleno (§9.3): {v_d4}")
    for n, txt in ((v_d3, "§8.4"), (v_ord, "§6.5"), (v_d4, "§9.3")):
        if n:
            warnings.append(f"{n} filas incumplen {txt} (desvio del anotador; se reporta, no se corrige)")

    # ------------------------------------------------------------- 5. independencia
    print("\n5. INDEPENDENCIA frente a A1")
    a1 = read_annotation_workbook(RAW / cfg["annotators"]["A1"]["file"], cfg).set_index("doc_id")
    idx = common.intersection(a1.index[a1[VARS].notna().any(axis=1)])
    if len(idx) == 0:
        warnings.append("sin solape con A1: no se puede comprobar la independencia")
    else:
        X, Y = r_i.loc[idx, VARS], a1.loc[idx, VARS]
        neq = (X != Y) & ~(X.isna() & Y.isna())
        n_cells, n_diff = int(neq.size), int(neq.values.sum())
        na = r_i.loc[idx, "notes"].fillna("").astype(str).str.strip()
        nb = a1.loc[idx, "notes"].fillna("").astype(str).str.strip()
        both = (na != "") & (nb != "")
        ident = int(((na == nb) & both).sum())
        agree = 100 * (1 - n_diff / n_cells) if n_cells else 0
        print(f"     documentos comparados: {len(idx)}")
        print(f"     celdas distintas: {n_diff}/{n_cells}  (acuerdo bruto {agree:.1f} %)")
        print(f"     observaciones literalmente identicas: {ident}/{int(both.sum())}")
        if n_diff == 0:
            errors.append("COPIA EXACTA DE A1: 0 celdas distintas. No es una anotacion independiente.")
        elif ident > 0:
            errors.append(f"{ident} observaciones son texto identico al de A1: el archivo se derivo del de A1")
        elif agree > 97:
            warnings.append(f"acuerdo bruto {agree:.1f} %: inverosimilmente alto para dos lecturas "
                            f"independientes de este protocolo; conviene confirmar el procedimiento")
        else:
            print("     -> compatible con una anotacion independiente")

    # ------------------------------------------------------------------ veredicto
    print("\n" + "=" * 72)
    if errors:
        print("RESULTADO: NO ACEPTABLE")
        for e in errors:
            print(f"  [ERROR]   {e}")
    else:
        print("RESULTADO: ACEPTABLE")
    for w in warnings:
        print(f"  [aviso]   {w}")
    print("=" * 72)

    if errors:
        log.error("validacion fallida: %d errores", len(errors))
        return 2

    dest = RAW / cfg["annotators"]["A2"]["file"]
    if "copia" in dest.name.lower() or dest.name == "Anotacion_principal_A2.xlsx":
        log.warning("config apunta todavia al A2 antiguo (%s); revisa annotators.A2.file", dest.name)
    if args.install:
        if dest.exists():
            os.chmod(dest, stat.S_IWRITE | stat.S_IREAD)
            bak = dest.with_suffix(".xlsx.copia_de_A1_sustituida")
            shutil.move(dest, bak)
            print(f"\nEl A2 anterior (copia de A1) se guardo como {bak.name}")
        shutil.copy2(ret_path, dest)
        os.chmod(dest, stat.S_IREAD)
        h = hashlib.sha256(dest.read_bytes()).hexdigest()[:16]
        print(f"Instalado en {dest.relative_to(ROOT)} (sha256 {h}…)")
        print("\nAhora, en config.yaml:  annotators.A2.independent: true")
        print("Y despues:")
        print("  python src/00_stage_raw.py --force")
        print("  python src/01_audit.py")
        print("  python src/03_agreement.py")
        print("  python src/04_figures.py")
        print("  python src/05_error_analysis.py")
    else:
        print(f"\nPara instalarlo:  python src/00c_receive_a2.py \"{ret_path}\" --install")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
