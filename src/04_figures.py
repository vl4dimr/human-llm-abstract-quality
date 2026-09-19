"""Fase 4 - Figuras del articulo (PDF vectorial + PNG 300 dpi, escala de grises, serif).

Figura 1: forest plot de delta-kappa por variable, linea vertical en 0 (requiere tabla 3).
Figura 2: matrices de confusion del mejor modelo frente al consenso humano.
Figura 3: kappa (y AC1) por variable ordenados por desequilibrio de prevalencia.

Las figuras no llevan titulo: el pie va en el manuscrito. Cada figura que no pueda
generarse por falta de datos se omite con un aviso, nunca se rellena.

Uso:  python src/04_figures.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib import metrics as M  # noqa: E402
from lib.figstyle import GRID, INK, INK_2, apply_style, save, series_style  # noqa: E402
from lib.io_raw import load_config, variable_specs  # noqa: E402
from lib.logging_utils import get_logger  # noqa: E402

cfg = load_config()
SPECS = variable_specs(cfg)
VARS = list(SPECS)
LAB = cfg["scheme"].get("labels_en", {})
DISP = cfg.get("display_names", {})
TABLES = ROOT / cfg["paths"]["tables"]
FIGS = ROOT / cfg["paths"]["figures"]
INTERIM = ROOT / cfg["paths"]["interim"]
PROCESSED = ROOT / cfg["paths"]["processed"]
log = get_logger("04_figures", ROOT / cfg["paths"]["logs"])
apply_style()


def label(v: str) -> str:
    return LAB.get(v, v)


def display(annotator: str) -> str:
    m, _, r = annotator.partition("#")
    base = DISP.get(m, m)
    return f"{base} ({r})" if r else base


def load_long() -> pd.DataFrame:
    p = TABLES / "table2_agreement_long.csv"
    if not p.exists():
        raise SystemExit("falta outputs/tables/table2_agreement_long.csv: ejecuta antes src/03_agreement.py")
    return pd.read_csv(p)


# --------------------------------------------------------------------------- #
# Figura 1 - forest plot de delta-kappa
# --------------------------------------------------------------------------- #
def fig1_forest() -> None:
    p = TABLES / "table3_delta_kappa.csv"
    if not p.exists():
        log.warning("Figura 1 omitida: no existe table3_delta_kappa.csv (falta A2 independiente).")
        return
    t3 = pd.read_csv(p)
    anchor = cfg["contrast"]["reference_human"]
    t3 = t3[t3["anchor"] == anchor].copy()
    t3["model"] = t3["llm"].str.split("#").str[0]
    t3["run"] = t3["llm"].str.split("#").str[1].fillna("")
    models = list(dict.fromkeys(t3["model"]))
    runs = [r for r in dict.fromkeys(t3["run"]) if r]      # "" = anotador sin corridas
    series = runs or [""]
    n_m = len(models)
    fig, axes = plt.subplots(1, n_m, figsize=(2.9 * n_m + 1.4, 4.6), sharey=True, sharex=True)
    axes = np.atleast_1d(axes)
    y = np.arange(len(VARS))[::-1]
    off = np.linspace(0.24, -0.24, len(series)) if len(series) > 1 else [0.0]
    # Escala comun: el asterisco se coloca junto al extremo del IC, en coordenadas de datos.
    lo_all, hi_all = t3["delta_lo"].min(), t3["delta_hi"].max()
    pad = 0.10 * (hi_all - lo_all)
    for ax, m in zip(axes, models):
        ax.axvline(0, color=INK, linewidth=0.8, zorder=1)
        ax.grid(axis="x", color=GRID, linewidth=0.5)
        ax.set_axisbelow(True)
        # Un anotador sin corridas (p. ej. el LLM previo) se dibuja como serie unica.
        m_runs = [r for r in series if ((t3["model"] == m) & (t3["run"] == r)).any()] or [""]
        for j, r in enumerate(m_runs):
            mask = (t3["model"] == m) & (t3["run"] == r) if r else (t3["model"] == m)
            sub = t3[mask].set_index("variable").reindex(VARS)
            if sub["delta"].isna().all():
                continue
            st = series_style(j)
            yy = y + (off[j] if len(m_runs) > 1 else 0.0)
            line_c = st["color"] if st["color"] != "#ffffff" else INK_2
            ax.hlines(yy, sub["delta_lo"], sub["delta_hi"], color=line_c, linewidth=1.0, zorder=2)
            ax.plot(sub["delta"], yy, linestyle="none", zorder=3, **st)
            # IC inestable (muchos remuestreos degenerados): se marca con extremos abiertos
            unstable = (sub["degenerate_frac"].fillna(0) > 0.10).to_numpy()
            if unstable.any():
                ax.plot(sub["delta"].to_numpy()[unstable], yy[unstable], linestyle="none",
                        marker="x", color=INK, markersize=6, markeredgewidth=1.0, zorder=4)
            sig = sub["significant_bh"].fillna(False).astype(bool).to_numpy()
            for yi, xi in zip(yy[sig], sub["delta_hi"].to_numpy()[sig]):
                if np.isnan(xi):
                    continue
                ax.text(xi + 0.02 * (hi_all - lo_all), yi, "*", ha="left", va="center",
                        fontsize=10, color=INK)
        ax.set_xlabel(f"Δκ = κ({DISP.get(anchor, anchor)}, LLM) − κ(A1, A2)")
        ax.text(0.5, 1.02, display(m), transform=ax.transAxes, ha="center", va="bottom", fontsize=9)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels([label(v) for v in VARS])
    axes[0].set_xlim(lo_all - pad, hi_all + pad)
    if len(series) > 1:
        handles = [Line2D([], [], linestyle="none", **series_style(j)) for j in range(len(series))]
        labels = [f"run {r}" for r in series]
        handles.append(Line2D([], [], linestyle="none", marker="x", color=INK, markersize=6))
        labels.append("unstable CI (>10 % degenerate resamples)")
        fig.legend(handles, labels, loc="lower center", ncol=len(labels),
                   bbox_to_anchor=(0.5, -0.06), frameon=False)
    pdf, png = save(fig, FIGS, "fig1_forest_delta_kappa")
    log.info("Figura 1 -> %s", pdf.name)


# --------------------------------------------------------------------------- #
# Figura 2 - matrices de confusion del mejor modelo vs consenso humano
# --------------------------------------------------------------------------- #
def human_consensus(wide_by_var: dict[str, pd.DataFrame], a2_ok: bool) -> dict[str, pd.Series]:
    """Consenso = etiqueta en la que A1 y A2 coinciden; sin A2 independiente, solo A1 (aviso)."""
    out = {}
    for v, w in wide_by_var.items():
        if a2_ok and "A2" in w.columns:
            agree = w["A1"].notna() & (w["A1"] == w["A2"])
            out[v] = w.loc[agree, "A1"]
        else:
            out[v] = w["A1"].dropna()
    return out


def fig2_confusion() -> None:
    long = load_long()
    ann = pd.read_csv(INTERIM / "annotations.csv")
    llm_p = PROCESSED / "llm_annotations.csv"
    if not llm_p.exists():
        log.warning("Figura 2 omitida: no hay anotaciones LLM.")
        return
    llm = pd.read_csv(llm_p)
    a2_ok = bool(cfg["annotators"]["A2"].get("independent", False))
    sub = set(pd.read_csv(PROCESSED / "subset.csv")["doc_id"])
    data = pd.concat([ann, llm]); data = data[data["doc_id"].isin(sub)]
    # mejor modelo: mayor kappa medio frente a A1 en la corrida r1
    cand = long[(long["a"] == "A1") & long["b"].str.contains("#r1", regex=False)]
    if cand.empty:
        log.warning("Figura 2 omitida: sin pares A1 vs modelo#r1.")
        return
    best = cand.groupby("b")["kappa"].mean().idxmax()
    log.info("Figura 2: mejor modelo por kappa medio vs A1 = %s", best)
    W = {v: data[data["category"] == v].pivot_table(index="doc_id", columns="annotator", values="label", aggfunc="first")
         for v in VARS}
    cons = human_consensus(W, a2_ok)
    fig, axes = plt.subplots(3, 4, figsize=(7.4, 6.6), gridspec_kw={"wspace": 0.45, "hspace": 0.55})
    cmap = plt.get_cmap("Greys")
    for k, (ax, v) in enumerate(zip(axes.ravel(), VARS)):
        row, colk = divmod(k, 4)
        lv = [float(x) for x in SPECS[v]["levels"]]
        h = cons[v]
        m = W[v][best] if best in W[v].columns else pd.Series(dtype=float)
        idx = h.index.intersection(m.dropna().index)
        if len(idx) == 0:
            ax.axis("off"); continue
        cm = M.confusion_matrix(h.loc[idx].to_numpy(float), m.loc[idx].to_numpy(float), lv)
        rowsum = cm.sum(axis=1, keepdims=True)
        prop = np.divide(cm, rowsum, out=np.zeros_like(cm), where=rowsum > 0)
        ax.imshow(prop, cmap=cmap, vmin=0, vmax=1, aspect="equal")
        q = len(lv)
        for i in range(q):
            for j in range(q):
                if rowsum[i, 0] == 0 and cm[i, j] == 0:
                    continue
                ax.text(j, i, f"{int(cm[i, j])}", ha="center", va="center", fontsize=7,
                        color="white" if prop[i, j] > 0.55 else INK)
        ax.set_xticks(range(q)); ax.set_xticklabels([str(int(x)) for x in lv])
        ax.set_yticks(range(q)); ax.set_yticklabels([str(int(x)) for x in lv])
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
        # titulo de panel en dos lineas (nombre / n) para que no choque con el vecino
        ax.text(0.5, 1.04, f"{label(v).replace(' (1–5)', '')}\nn = {len(idx)}", transform=ax.transAxes,
                ha="center", va="bottom", fontsize=7.5, linespacing=1.1)
        # rotulos compartidos: eje x solo en la ultima fila, eje y solo en la primera columna
        if row == 2:
            ax.set_xlabel(display(best), fontsize=7, color=INK_2)
        if colk == 0:
            ax.set_ylabel("Human" + ("" if a2_ok else " (A1)"), fontsize=7, color=INK_2)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
    cbar = fig.colorbar(sm, ax=axes.ravel().tolist(), fraction=0.025, pad=0.02)
    cbar.set_label("Row proportion (share of human label)", fontsize=8)
    cbar.outline.set_linewidth(0.5)
    pdf, png = save(fig, FIGS, "fig2_confusion_best_vs_human")
    log.info("Figura 2 -> %s (%s)", pdf.name, "consenso A1=A2" if a2_ok else "solo A1: A2 no independiente")


# --------------------------------------------------------------------------- #
# Figura 3 - kappa y AC1 por variable, ordenados por desequilibrio de prevalencia
# --------------------------------------------------------------------------- #
def majority_share() -> pd.Series:
    """Proporcion de la categoria mayoritaria en A1 (binarias y ordinales por igual)."""
    ann = pd.read_csv(INTERIM / "annotations.csv")
    sub = set(pd.read_csv(PROCESSED / "subset.csv")["doc_id"])
    a1 = ann[(ann["annotator"] == "A1") & ann["doc_id"].isin(sub)]
    return a1.groupby("category")["label"].agg(lambda s: s.value_counts(normalize=True).max()).reindex(VARS)


def fig3_kappa_by_prevalence() -> None:
    long = load_long()
    share = majority_share()
    pairs = []
    if ((long["a"] == "A1") & (long["b"] == "A2")).any():
        pairs.append(("A1", "A2"))
    for b in sorted(long.loc[(long["a"] == "A1") & long["b"].str.contains("#r1", regex=False), "b"].unique()):
        pairs.append(("A1", b))
    if ((long["a"] == "A1") & (long["b"] == "LLM_prior")).any():
        pairs.append(("A1", "LLM_prior"))
    if not pairs:
        log.warning("Figura 3 omitida: sin pares con A1.")
        return
    # Eje x categorico ordenado por desequilibrio (proporcion de la etiqueta mayoritaria):
    # evita colisiones de etiquetas donde dos variables tienen casi la misma prevalencia.
    order = share.sort_values().index.tolist()
    xpos = np.arange(len(order))
    # desplazamiento horizontal pequeno por serie para que los IC no se superpongan
    offs = np.linspace(-0.25, 0.25, len(pairs)) if len(pairs) > 1 else [0.0]
    fig, (ax_k, ax_a) = plt.subplots(2, 1, figsize=(7.2, 5.6), sharex=True)
    for ax, col, lo, hi, yl in ((ax_k, "kappa", "kappa_lo", "kappa_hi", "Cohen's κ"),
                                (ax_a, "gwet_ac", "ac_lo", "ac_hi", "Gwet's AC1 / AC2")):
        ax.axhline(0, color=INK, linewidth=0.6, zorder=1)
        ax.grid(axis="y", color=GRID, linewidth=0.5); ax.set_axisbelow(True)
        for i, (a, b) in enumerate(pairs):
            sub = long[(long["a"] == a) & (long["b"] == b)].set_index("variable").reindex(order)
            st = series_style(i)
            x = xpos + offs[i]
            ax.vlines(x, sub[lo], sub[hi], color=st["color"] if st["color"] != "#ffffff" else INK_2,
                      linewidth=0.7, zorder=2)
            ax.plot(x, sub[col], linestyle="none", zorder=3, **st)
        ax.set_ylabel(yl)
        ax.set_ylim(-1.0, 1.05)
        ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax_a.set_xticks(xpos)
    ax_a.set_xticklabels([f"{label(v).replace(' (1–5)', '')}\n{share[v]:.2f}" for v in order],
                         rotation=45, ha="right", rotation_mode="anchor", fontsize=7)
    ax_a.set_xlabel("Variable, ordered by share of the majority label in A1 (value under each name)")
    handles = [Line2D([], [], linestyle="none", **series_style(i)) for i in range(len(pairs))]
    ax_k.legend(handles, [f"{display(a)} vs {display(b)}" for a, b in pairs], loc="lower left", ncol=1)
    pdf, png = save(fig, FIGS, "fig3_kappa_by_prevalence")
    log.info("Figura 3 -> %s", pdf.name)


if __name__ == "__main__":
    fig1_forest()
    fig2_confusion()
    fig3_kappa_by_prevalence()
    log.info("figuras en %s", FIGS)
