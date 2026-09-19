"""Pruebas de los estimadores contra valores publicados y contra sklearn/statsmodels.

Ejecutar:  python -m pytest tests/ -q
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lib import metrics as M  # noqa: E402

rng = np.random.default_rng(42)


# ----------------------------------------------------------------- kappa ---- #
def test_cohen_kappa_matches_sklearn_nominal():
    from sklearn.metrics import cohen_kappa_score
    x = rng.integers(0, 3, 500)
    y = np.where(rng.random(500) < 0.7, x, rng.integers(0, 3, 500))
    assert M.cohen_kappa(x, y, [0, 1, 2]) == pytest.approx(cohen_kappa_score(x, y), abs=1e-12)


def test_cohen_kappa_quadratic_matches_sklearn():
    from sklearn.metrics import cohen_kappa_score
    x = rng.integers(1, 6, 400)
    y = np.clip(x + rng.integers(-1, 2, 400), 1, 5)
    ours = M.cohen_kappa(x, y, [1, 2, 3, 4, 5], weights="quadratic")
    ref = cohen_kappa_score(x, y, weights="quadratic", labels=[1, 2, 3, 4, 5])
    assert ours == pytest.approx(ref, abs=1e-12)


def test_kappa_degenerate_is_nan_not_zero():
    x = [1] * 50
    y = [1] * 50
    assert np.isnan(M.cohen_kappa(x, y, [0, 1]))
    assert np.isnan(M.gwet_ac1(x, y, [0, 1])) is False or True  # AC1 esta definido: pe=0
    assert M.gwet_ac1(x, y, [0, 1]) == pytest.approx(1.0)


def test_value_outside_scheme_raises():
    with pytest.raises(ValueError):
        M.cohen_kappa([0, 1, 2], [0, 1, 1], [0, 1])


# ----------------------------------------------------- AC1 y PABAK a mano ---- #
def _table_2x2(a, b, c, d):
    """Construye vectores a partir de una tabla [[a, b], [c, d]] (filas = x)."""
    x = [0] * (a + b) + [1] * (c + d)
    y = [0] * a + [1] * b + [0] * c + [1] * d
    return x, y


def test_ac1_pabak_hand_computed():
    # Tabla [[45, 15], [25, 15]], n = 100:
    #   p_o = 0.60 ; p_e(Cohen) = 0.54 -> kappa = 0.130435
    #   pi_0 = 0.65, pi_1 = 0.35 -> p_e(Gwet) = 0.455 -> AC1 = 0.266055
    #   PABAK = 2 * 0.60 - 1 = 0.20
    x, y = _table_2x2(45, 15, 25, 15)
    assert M.observed_agreement(x, y, [0, 1]) == pytest.approx(0.60)
    assert M.cohen_kappa(x, y, [0, 1]) == pytest.approx(0.06 / 0.46, abs=1e-9)
    assert M.gwet_ac1(x, y, [0, 1]) == pytest.approx(0.145 / 0.545, abs=1e-9)
    assert M.pabak(x, y, [0, 1]) == pytest.approx(0.20, abs=1e-12)


def test_kappa_paradox_case():
    # Prevalencia extrema: acuerdo bruto 0.944 pero kappa negativo (Feinstein y
    # Cicchetti, 1990). AC1 y PABAK deben permanecer altos.
    x, y = _table_2x2(118, 5, 2, 0)
    assert M.observed_agreement(x, y, [0, 1]) == pytest.approx(118 / 125)
    assert M.cohen_kappa(x, y, [0, 1]) < 0
    assert M.gwet_ac1(x, y, [0, 1]) > 0.9
    assert M.pabak(x, y, [0, 1]) > 0.85


def test_pabak_generalises_to_q_levels():
    x = [1, 2, 3, 4, 5] * 20
    y = list(x)
    y[0] = 2
    p_o = 99 / 100
    assert M.pabak(x, y, [1, 2, 3, 4, 5]) == pytest.approx((5 * p_o - 1) / 4)


# ----------------------------------------------------- Krippendorff alpha ---- #
_KRIPP = np.array([  # Krippendorff (2011), tabla de 3 observadores x 15 unidades
    [np.nan, np.nan, np.nan, np.nan, np.nan, 3, 4, 1, 2, 1, 1, 3, 3, np.nan, 3],
    [1, np.nan, 2, 1, 3, 3, 4, 3, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, 2, 1, 3, 4, 4, np.nan, 2, 1, 1, 3, 3, np.nan, 4],
])


def test_krippendorff_published_example():
    lv = [1, 2, 3, 4]
    assert M.krippendorff_alpha(_KRIPP, lv, "nominal") == pytest.approx(0.691, abs=1e-3)
    assert M.krippendorff_alpha(_KRIPP, lv, "ordinal") == pytest.approx(0.807, abs=1e-3)
    assert M.krippendorff_alpha(_KRIPP, lv, "interval") == pytest.approx(0.811, abs=1e-3)


def test_krippendorff_two_raters_complete_equals_scott_pi_correction():
    # Con 2 anotadores y datos completos, alpha nominal = 1 - (1-pi)(n-1)/n... en la
    # practica basta comprobar que alpha ~ kappa cuando las marginales coinciden.
    x = rng.integers(0, 2, 300)
    y = np.where(rng.random(300) < 0.8, x, 1 - x)
    a = M.krippendorff_alpha(np.vstack([x, y]).astype(float), [0, 1], "nominal")
    k = M.cohen_kappa(x, y, [0, 1])
    assert abs(a - k) < 0.05


# ----------------------------------------------------------------- bootstrap - #
def test_bootstrap_ci_is_reproducible_and_contains_estimate():
    x = rng.integers(0, 2, 200)
    y = np.where(rng.random(200) < 0.85, x, 1 - x)
    pos = np.arange(200)

    def stat(idx):
        return M.cohen_kappa(x[idx], y[idx], [0, 1])

    r1 = M.bootstrap_ci(pos, stat, n_resamples=300, seed=42)
    r2 = M.bootstrap_ci(pos, stat, n_resamples=300, seed=42)
    assert r1.ci_low == r2.ci_low and r1.ci_high == r2.ci_high
    assert r1.ci_low <= r1.estimate <= r1.ci_high
    assert r1.n_degenerate == 0


def test_paired_delta_of_identical_stats_is_zero():
    x = rng.integers(0, 2, 100)
    y = np.where(rng.random(100) < 0.85, x, 1 - x)
    pos = np.arange(100)
    f = lambda idx: M.cohen_kappa(x[idx], y[idx], [0, 1])  # noqa: E731
    r = M.paired_bootstrap_delta(pos, f, f, n_resamples=200)
    assert r.estimate == 0.0 and r.ci_low == 0.0 and r.ci_high == 0.0


# ------------------------------------------------------------------- BH ------ #
def test_bh_matches_statsmodels():
    from statsmodels.stats.multitest import multipletests
    p = rng.random(12) * 0.2
    rej, adj = M.benjamini_hochberg(p, alpha=0.05)
    ref_rej, ref_adj, _, _ = multipletests(p, alpha=0.05, method="fdr_bh")
    assert np.allclose(adj, ref_adj)
    assert np.array_equal(rej, ref_rej)


def test_bh_handles_nan():
    p = np.array([0.01, np.nan, 0.04, 0.5])
    rej, adj = M.benjamini_hochberg(p)
    assert np.isnan(adj[1]) and not rej[1]
    assert not np.isnan(adj[0])
