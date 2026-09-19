"""Fase 3 - Estadistica de concordancia.

Para cada par de anotadores y cada variable:
  kappa de Cohen (ponderado cuadratico en ordinales), AC1/AC2 de Gwet, PABAK,
  alpha de Krippendorff, acuerdo bruto y matriz de confusion, con IC 95 % por
  bootstrap no parametrico a nivel de documento.

Contraste central: delta_kappa = kappa(ancla, LLM) - kappa(A1, A2), por variable,
con IC bootstrap PAREADO (mismos documentos en ambos terminos), p bootstrap
bilateral y correccion de Benjamini-Hochberg. Solo se calcula si A2 es
independiente (config annotators.A2.independent); si no, se deja NaN y se avisa.

Autoconsistencia: kappa entre corridas del mismo modelo (techo de rendimiento).

Uso:  python src/03_agreement.py [--n-boot 2000] [--quick]
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib import metrics as M  # noqa: E402
from lib.io_raw import load_config, variable_specs  # noqa: E402
from lib.logging_utils import get_logger  # noqa: E402
from lib.tables import write_table  # noqa: E402

cfg = load_config()
SPECS = variable_specs(cfg)
VARS = list(SPECS)
SEED = int(cfg["seed"])
INTERIM = ROOT / cfg["paths"]["interim"]
PROCESSED = ROOT / cfg["paths"]["processed"]
TABLES = ROOT / cfg["paths"]["tables"]
AG = cfg["agreement"]
CT = cfg["contrast"]
log = get_logger("03_agreement", ROOT / cfg["paths"]["logs"])
REPORT: list[str] = []


def say(line: str = "") -> None:
    REPORT.append(line)
    if line.strip():
        log.info(line)


def md(df: pd.DataFrame, floatfmt: str = ".3f") -> str:
    return df.to_markdown(index=False, floatfmt=floatfmt)


def display(annotator: str) -> str:
    """Nombre legible para el articulo (config display_names)."""
    m, _, r = annotator.partition("#")
    base = cfg.get("display_names", {}).get(m, m)
    return f"{base} ({r})" if r else base


# --------------------------------------------------------------------------- #
# Carga y registro de anotadores
# --------------------------------------------------------------------------- #
def load_all() -> tuple[pd.DataFrame, list[str], dict]:
    ann = pd.read_csv(INTERIM / "annotations.csv", encoding="utf-8")
    llm_path = PROCESSED / "llm_annotations.csv"
    llm = pd.read_csv(llm_path, encoding="utf-8") if llm_path.exists() else pd.DataFrame(columns=ann.columns)
    sub = pd.read_csv(PROCESSED / "subset.csv")["doc_id"]
    universe = sorted(set(sub) & set(ann.loc[ann["annotator"] == "A1", "doc_id"]))
    if not universe:
        raise SystemExit("universo vacio: no hay documentos del subconjunto anotados por A1")

    a2_ok = bool(cfg["annotators"]["A2"].get("independent", False))
    humans = ["A1"] + (["A2"] if a2_ok else [])
    if not a2_ok:
        ann = ann[ann["annotator"] != "A2"]
    if not CT.get("include_llm_prior", True):
        ann = ann[ann["annotator"] != "LLM_prior"]

    data = pd.concat([ann, llm], ignore_index=True)
    data = data[data["doc_id"].isin(universe)]

    # registro: modelo -> corridas
    models: dict[str, list[str]] = {}
    for a in sorted(llm["annotator"].unique()):
        m, _, r = a.partition("#")
        models.setdefault(m, []).append(a)
    reg = {"humans": humans, "a2_independent": a2_ok, "models": models,
           "prior": ["LLM_prior"] if "LLM_prior" in set(data["annotator"]) else []}
    return data, universe, reg


def wide_tables(data: pd.DataFrame, universe: list[str]) -> dict[str, pd.DataFrame]:
    out = {}
    for v in VARS:
        w = (data[data["category"] == v]
             .pivot_table(index="doc_id", columns="annotator", values="label", aggfunc="first")
             .reindex(universe))
        out[v] = w.astype(float)
    return out


# --------------------------------------------------------------------------- #
# Estadisticos sobre indices de documento (para el bootstrap)
# --------------------------------------------------------------------------- #
def make_stat(arr_a: np.ndarray, arr_b: np.ndarray, levels: list[float], weights: str, kind: str):
    """Devuelve f(idx) que calcula el estadistico sobre los documentos idx (con repeticion)."""
    def f(idx: np.ndarray) -> float:
        x, y = arr_a[idx], arr_b[idx]
        ok = ~np.isnan(x) & ~np.isnan(y)
        if ok.sum() == 0:
            return float("nan")
        if kind == "kappa":
            return M.cohen_kappa(x[ok], y[ok], levels, weights)
        if kind == "ac":
            return M.gwet_ac1(x[ok], y[ok], levels, weights)
        raise ValueError(kind)
    return f


def boot_p_two_sided(reps: np.ndarray) -> float:
    ok = reps[~np.isnan(reps)]
    if len(ok) < 10:
        return float("nan")
    return float(min(1.0, 2 * min((ok <= 0).mean(), (ok >= 0).mean())))


def fmt_ci(est: float, lo: float, hi: float) -> str:
    if np.isnan(est):
        return "n/d"
    return f"{est:.2f} [{lo:.2f}, {hi:.2f}]"


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=int(AG["bootstrap"]["n_resamples"]))
    ap.add_argument("--quick", action="store_true", help="200 remuestreos, para pruebas")
    args = ap.parse_args()
    NB = 200 if args.quick else args.n_boot

    data, universe, reg = load_all()
    W = wide_tables(data, universe)
    n_docs = len(universe)
    pos = np.arange(n_docs)
    say("# Informe de concordancia (Fase 3)\n")
    say(f"Generado: {datetime.now().isoformat(timespec='seconds')} · universo: {n_docs} documentos · "
        f"bootstrap: {NB} remuestreos a nivel de documento, IC percentil 95 %, semilla {SEED}\n")
    say(f"Anotadores humanos: {reg['humans']} (A2 independiente: **{reg['a2_independent']}**). "
        f"Modelos: {json.dumps(reg['models'])}. Exploratorio: {reg['prior']}.\n")
    if not reg["a2_independent"]:
        say("> **A2 no es una anotacion independiente** (copia de A1, ver auditoria). No se calcula "
            "la linea base kappa(A1,A2) ni el contraste delta-kappa. Todo lo demas si.\n")

    llm_annotators = [a for runs in reg["models"].values() for a in runs] + reg["prior"]
    cov = {a: int(W[VARS[0]][a].notna().sum()) if a in W[VARS[0]] else 0 for a in llm_annotators}
    say("Cobertura (docs con etiqueta en D1_imryd_objetivo): " + ", ".join(f"{a}={n}" for a, n in cov.items()) + "\n")

    # ------------------------------------------------------------------ pares
    pairs: list[tuple[str, str, str]] = []  # (a, b, tipo)
    if reg["a2_independent"]:
        pairs.append(("A1", "A2", "human-human"))
    for h in reg["humans"]:
        for a in llm_annotators:
            pairs.append((h, a, "human-llm"))
    for m, runs in reg["models"].items():
        for a, b in itertools.combinations(runs, 2):
            pairs.append((a, b, "self-consistency"))
    cross = [f"{m}#{r}" for m in reg["models"] for r in AG.get("cross_model_runs", ["r1"])
             if f"{m}#{r}" in {a for runs in reg["models"].values() for a in runs}] + reg["prior"]
    for a, b in itertools.combinations(cross, 2):
        pairs.append((a, b, "llm-llm"))
    pairs = [p for p in pairs if p[0] in W[VARS[0]].columns and p[1] in W[VARS[0]].columns]
    say(f"## 1. Todos contra todos: {len(pairs)} pares x {len(VARS)} variables\n")

    conf_dir = TABLES / "confusion"
    conf_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for a, b, kind in pairs:
        for v in VARS:
            spec = SPECS[v]
            lv = [float(x) for x in spec["levels"]]
            wts = AG["weights_by_type"][spec["type"]]
            km = AG["krippendorff_metric_by_type"][spec["type"]]
            xa, xb = W[v][a].to_numpy(), W[v][b].to_numpy()
            ok = ~np.isnan(xa) & ~np.isnan(xb)
            n = int(ok.sum())
            row = {"pair": f"{a} vs {b}", "a": a, "b": b, "type": kind, "variable": v, "n": n}
            if n == 0:
                rows.append(row)
                continue
            bk = M.bootstrap_ci(pos, make_stat(xa, xb, lv, wts, "kappa"), n_resamples=NB, seed=SEED)
            ba = M.bootstrap_ci(pos, make_stat(xa, xb, lv, wts, "ac"), n_resamples=NB, seed=SEED)
            cm = M.confusion_matrix(xa[ok], xb[ok], lv)
            pd.DataFrame(cm, index=[f"{a}={int(l)}" for l in lv], columns=[f"{b}={int(l)}" for l in lv]) \
                .to_csv(conf_dir / f"{a}__{b}__{v}.csv".replace("#", "-"), encoding="utf-8")
            row.update({
                "p_obs": M.observed_agreement(xa[ok], xb[ok], lv, "unweighted"),
                "p_obs_w": M.observed_agreement(xa[ok], xb[ok], lv, wts),
                "kappa": bk.estimate, "kappa_lo": bk.ci_low, "kappa_hi": bk.ci_high,
                "kappa_degenerate_frac": bk.degenerate_fraction,
                "gwet_ac": ba.estimate, "ac_lo": ba.ci_low, "ac_hi": ba.ci_high,
                "pabak": M.pabak(xa[ok], xb[ok], lv),
                "kripp_alpha": M.krippendorff_alpha(np.vstack([xa[ok], xb[ok]]), lv, km),
                "weights": wts,
            })
            rows.append(row)
        log.info("par %s vs %s listo", a, b)
    t2 = pd.DataFrame(rows)
    write_table(t2, TABLES, "table2_agreement_long",
                caption="Pairwise agreement for every annotator pair and variable (Cohen's kappa with "
                        "document-level bootstrap 95% CI, Gwet's AC1/AC2, PABAK, Krippendorff's alpha).",
                label="tab:agreement-long")
    t2["kappa_ci"] = [fmt_ci(r["kappa"], r["kappa_lo"], r["kappa_hi"])
                      if not pd.isna(r.get("kappa", np.nan)) else "n/d"
                      for r in t2.to_dict("records")]
    mat = t2.pivot(index=["type", "pair"], columns="variable", values="kappa_ci").reindex(columns=VARS).reset_index()
    write_table(mat, TABLES, "table2_kappa_matrix",
                caption="All-vs-all agreement matrix: Cohen's kappa [95% bootstrap CI] per variable.",
                label="tab:agreement-matrix")
    say(md(mat))
    say()

    # ------------------------------------------------------ autoconsistencia
    say("## 2. Autoconsistencia intra-modelo (techo de rendimiento)\n")
    sc = t2[t2["type"] == "self-consistency"].copy()
    if len(sc):
        temps = {r["name"]: r["temperature"] for r in cfg["llm"]["runs"]}
        sc["model"] = sc["a"].str.split("#").str[0]
        sc["run_pair"] = sc["a"].str.split("#").str[1] + "-" + sc["b"].str.split("#").str[1]
        # Las corridas no son intercambiables: r1 va a temperature 0 y r2/r3 a la del
        # modelo. Promediar los tres pares mezclaria dos condiciones distintas, asi que
        # se reporta par a par y se marca cual es "determinista vs muestreada".
        sc["condition"] = [
            "sampled-sampled" if temps.get(a) is None and temps.get(b) is None
            else ("deterministic-sampled" if (temps.get(a) is None) != (temps.get(b) is None)
                  else "deterministic-deterministic")
            for a, b in zip(sc["a"].str.split("#").str[1], sc["b"].str.split("#").str[1])]
        keep = ["model", "run_pair", "condition", "variable", "n", "p_obs", "kappa",
                "kappa_lo", "kappa_hi", "gwet_ac", "kripp_alpha"]
        write_table(sc[keep], TABLES, "table_selfconsistency",
                    caption="Intra-model self-consistency: Cohen's kappa between each pair of runs of the "
                            "same model, per variable. Run r1 uses temperature 0; r2 and r3 use the "
                            "model's default temperature, so run pairs are reported separately.",
                    label="tab:selfconsistency")
        for m, g in sc.groupby("model"):
            say(f"**{display(m)}** — κ entre corridas, por par:\n")
            piv = g.pivot(index="variable", columns="run_pair", values="kappa").reindex(VARS)
            cond = g.drop_duplicates("run_pair").set_index("run_pair")["condition"]
            piv.columns = [f"{c} ({cond[c].replace('-', '/')})" for c in piv.columns]
            say(md(piv.reset_index()))
            say()
        say("> Un modelo cuya autoconsistencia en una variable es baja no puede concordar con nadie en "
            "esa variable: ese kappa es el techo del kappa humano-LLM. El par de corridas muestreadas "
            "(r2-r3) es el que mide la inestabilidad propia del modelo; los pares con r1 mezclan "
            "decodificacion determinista y muestreada.\n")
    else:
        say("Sin corridas multiples todavia.\n")

    # ------------------------------------------------------------ delta-kappa
    say("## 3. Contraste central: delta-kappa = kappa(ancla, LLM) - kappa(A1, A2)\n")
    drows = []
    if not reg["a2_independent"]:
        say("> **No calculable**: falta la anotacion independiente de A2. Cuando exista, poner "
            "`annotators.A2.independent: true` y relanzar.\n")
    else:
        anchors = [CT["reference_human"]] + [a for a in CT.get("also_anchor_on", []) if a in reg["humans"]]
        for anchor in anchors:
            other = "A2" if anchor == "A1" else "A1"
            for llm_a in llm_annotators:
                for v in VARS:
                    spec = SPECS[v]
                    lv = [float(x) for x in spec["levels"]]
                    wts = AG["weights_by_type"][spec["type"]]
                    xa, xl = W[v][anchor].to_numpy(), W[v][llm_a].to_numpy()
                    x1, x2 = W[v]["A1"].to_numpy(), W[v]["A2"].to_numpy()
                    r = M.paired_bootstrap_delta(pos, make_stat(xa, xl, lv, wts, "kappa"),
                                                 make_stat(x1, x2, lv, wts, "kappa"), n_resamples=NB, seed=SEED)
                    drows.append({
                        "anchor": anchor, "llm": llm_a, "variable": v,
                        "n_llm": int((~np.isnan(xa) & ~np.isnan(xl)).sum()),
                        "n_hh": int((~np.isnan(x1) & ~np.isnan(x2)).sum()),
                        "kappa_anchor_llm": make_stat(xa, xl, lv, wts, "kappa")(pos),
                        "kappa_hh": make_stat(x1, x2, lv, wts, "kappa")(pos),
                        "delta": r.estimate, "delta_lo": r.ci_low, "delta_hi": r.ci_high,
                        "degenerate_frac": r.degenerate_fraction,
                        "p_boot": boot_p_two_sided(r.replicates),
                        "excludes_zero": r.excludes_zero,
                    })
                log.info("delta-kappa %s vs %s listo", anchor, llm_a)
        t3 = pd.DataFrame(drows)
        fam = CT["multiple_comparisons"]["family"]
        alpha = float(CT["multiple_comparisons"]["alpha"])
        t3["p_adj_bh"] = np.nan
        groups = [t3.index] if fam == "all" else [g.index for _, g in t3.groupby(["anchor", "llm"])]
        for gi in groups:
            _, adj = M.benjamini_hochberg(t3.loc[gi, "p_boot"].to_numpy(), alpha)
            t3.loc[gi, "p_adj_bh"] = adj
        t3["significant_bh"] = t3["p_adj_bh"] <= alpha
        t3["verdict"] = np.where(t3["delta"].isna(), "n/d",
                         np.where(~t3["excludes_zero"], "indistinguible (IC incluye 0)",
                         np.where(t3["delta"] < 0, "LLM peor que humano", "LLM mejor que humano")))
        write_table(t3, TABLES, "table3_delta_kappa",
                    caption="Delta-kappa = kappa(anchor, LLM) - kappa(A1, A2) per variable, with paired "
                            "document-level bootstrap 95% CI, two-sided bootstrap p and BH-adjusted p.",
                    label="tab:delta-kappa")
        show = t3[t3["anchor"] == CT["reference_human"]][["llm", "variable", "delta", "delta_lo", "delta_hi",
                                                          "p_boot", "p_adj_bh", "verdict"]]
        say(md(show))
        say()
        # anclas discrepantes
        if len(anchors) > 1:
            piv = t3.pivot_table(index=["llm", "variable"], columns="anchor", values="excludes_zero", aggfunc="first")
            disc = piv[piv.nunique(axis=1) > 1]
            say(f"Filas donde las anclas A1 y A2 no coinciden en la conclusion: **{len(disc)}**.\n")

    # -------------------------------------------------- Krippendorff multi
    say("## 4. Alpha de Krippendorff multi-anotador por variable\n")
    krows = []
    for v in VARS:
        spec = SPECS[v]
        lv = [float(x) for x in spec["levels"]]
        km = AG["krippendorff_metric_by_type"][spec["type"]]
        row = {"variable": v, "metric": km}
        if reg["a2_independent"]:
            row["alpha_A1_A2"] = M.krippendorff_alpha(W[v][["A1", "A2"]].to_numpy().T, lv, km)
        for m, runs in reg["models"].items():
            cols = [c for c in runs if c in W[v].columns]
            if len(cols) >= 2:
                row[f"alpha_runs_{m}"] = M.krippendorff_alpha(W[v][cols].to_numpy().T, lv, km)
        cols = [c for c in W[v].columns if c != "A2" or reg["a2_independent"]]
        row["alpha_all"] = M.krippendorff_alpha(W[v][cols].to_numpy().T, lv, km)
        krows.append(row)
    tk = pd.DataFrame(krows)
    write_table(tk, TABLES, "table_krippendorff",
                caption="Krippendorff's alpha per variable: human pair, runs within each model, and all annotators.",
                label="tab:krippendorff")
    say(md(tk))
    say()

    out = ROOT / "outputs" / "agreement_report.md"
    out.write_text("\n".join(REPORT) + "\n", encoding="utf-8")
    log.info("informe: %s", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
