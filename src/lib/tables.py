"""Exportacion de tablas a CSV y LaTeX con el mismo nombre base."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_table(df: pd.DataFrame, out_dir: Path, name: str, caption: str = "",
                label: str = "", float_fmt: str = "%.3f", index: bool = False) -> tuple[Path, Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"{name}.csv"
    tex_path = out_dir / f"{name}.tex"
    df.to_csv(csv_path, index=index, encoding="utf-8", float_format=float_fmt)
    tex = df.to_latex(index=index, float_format=lambda v: float_fmt % v,
                      na_rep="--", escape=True,
                      caption=caption or None, label=label or None,
                      longtable=False)
    tex_path.write_text(tex, encoding="utf-8")
    return csv_path, tex_path
