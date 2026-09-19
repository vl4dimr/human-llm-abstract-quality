"""Estilo comun de las figuras del articulo.

Escala de grises legible en impresion, tipografia serif, sin titulos dentro de la
figura (van en el pie), marcas finas y rejilla recesiva. La identidad de cada serie
va por FORMA de marcador ademas del tono de gris: en escala de grises el color solo
no basta.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

INK = "#000000"
INK_2 = "#444444"
GRID = "#d9d9d9"        # hairline, un paso fuera del blanco
SURFACE = "#ffffff"

# Tonos de gris y marcadores para hasta 6 series, en orden fijo (nunca ciclico).
SERIES = [
    {"color": "#000000", "marker": "o"},   # 1: negro, circulo
    {"color": "#555555", "marker": "s"},   # 2: gris oscuro, cuadrado
    {"color": "#8c8c8c", "marker": "^"},   # 3: gris medio, triangulo
    {"color": "#bdbdbd", "marker": "D"},   # 4: gris claro, rombo
    {"color": "#ffffff", "marker": "o"},   # 5: hueco, circulo
    {"color": "#ffffff", "marker": "s"},   # 6: hueco, cuadrado
]

RC = {
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],   # DejaVu viene con matplotlib: portable
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.edgecolor": INK_2,
    "axes.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "grid.color": GRID,
    "grid.linewidth": 0.5,
    "grid.linestyle": "-",
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "lines.linewidth": 1.2,
    "lines.markersize": 5,
    "legend.frameon": False,
    "figure.dpi": 100,
    "savefig.dpi": 300,
    "pdf.fonttype": 42,      # fuentes incrustadas como TrueType (editable en la imprenta)
    "ps.fonttype": 42,
    "text.color": INK,
    "axes.labelcolor": INK,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
}


def apply_style() -> None:
    plt.rcParams.update(RC)


def series_style(i: int) -> dict:
    """Estilo de la serie i (0-based): color de relleno, marcador; borde siempre tinta."""
    s = SERIES[i % len(SERIES)]
    return {"color": s["color"], "marker": s["marker"], "markeredgecolor": INK,
            "markeredgewidth": 0.6, "markerfacecolor": s["color"]}


def save(fig, out_dir: Path, name: str) -> tuple[Path, Path]:
    """PDF vectorial + PNG 300 dpi con el mismo nombre base."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = out_dir / f"{name}.pdf"
    png = out_dir / f"{name}.png"
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(png, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return pdf, png
