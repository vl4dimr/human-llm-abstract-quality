"""Estimadores de concordancia entre dos anotadores, con bootstrap a nivel de documento.

Todas las funciones devuelven NaN (nunca 0) cuando el estimador es indefinido, y
exponen esa condicion para que las tablas la marquen en vez de esconderla.

Convenciones:
  - `x`, `y` son vectores alineados de etiquetas de dos anotadores sobre los
    MISMOS documentos, ya filtrados de faltantes.
  - `levels` es la lista completa de niveles del esquema, no solo los observados.
    Esto importa: p_e y AC1 dependen del numero de categorias q.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Sequence

import numpy as np

__all__ = [
    "confusion_matrix", "agreement_weights", "observed_agreement",
    "cohen_kappa", "gwet_ac1", "pabak", "krippendorff_alpha",
    "BootstrapResult", "bootstrap_ci", "paired_bootstrap_delta",
    "benjamini_hochberg",
]


# --------------------------------------------------------------------------- #
# Utilidades basicas
# --------------------------------------------------------------------------- #
def _encode(values: Sequence, levels: Sequence) -> np.ndarray:
    """Mapea etiquetas a indices 0..q-1. Falla ruidosamente ante valores ajenos."""
    lookup = {v: i for i, v in enumerate(levels)}
    out = np.empty(len(values), dtype=np.int64)
    for k, v in enumerate(values):
        try:
            out[k] = lookup[v]
        except KeyError:
            raise ValueError(
                f"valor fuera del esquema: {v!r}; esperado uno de {list(levels)}"
            ) from None
    return out


def confusion_matrix(x: Sequence, y: Sequence, levels: Sequence) -> np.ndarray:
    """Matriz de contingencia q x q (filas = x, columnas = y) en el orden de `levels`."""
    if len(x) != len(y):
        raise ValueError("x e y deben tener la misma longitud")
    q = len(levels)
    if len(x) == 0:
        return np.zeros((q, q), dtype=float)
    ix = _encode(x, levels)
    iy = _encode(y, levels)
    return np.bincount(ix * q + iy, minlength=q * q).reshape(q, q).astype(float)


def agreement_weights(levels: Sequence, scheme: str = "unweighted") -> np.ndarray:
    """Pesos de ACUERDO w_ij en [0, 1]: 1 en la diagonal, menos fuera.

    unweighted -> identidad (variables binarias o nominales)
    quadratic  -> 1 - (i-j)^2 / (q-1)^2   (ordinales)
    linear     -> 1 - |i-j| / (q-1)
    """
    q = len(levels)
    i = np.arange(q)[:, None]
    j = np.arange(q)[None, :]
    if scheme == "unweighted":
        return (i == j).astype(float)
    if q < 2:
        raise ValueError("se necesitan al menos 2 niveles para pesos ponderados")
    if scheme == "quadratic":
        return 1.0 - ((i - j) ** 2) / ((q - 1) ** 2)
    if scheme == "linear":
        return 1.0 - np.abs(i - j) / (q - 1)
    raise ValueError(f"esquema de pesos desconocido: {scheme}")


def observed_agreement(x, y, levels, weights: str = "unweighted") -> float:
    """Acuerdo bruto (ponderado si se pide)."""
    m = confusion_matrix(x, y, levels)
    n = m.sum()
    if n == 0:
        return float("nan")
    w = agreement_weights(levels, weights)
    return float((w * m).sum() / n)


# --------------------------------------------------------------------------- #
# Estimadores
# --------------------------------------------------------------------------- #
def cohen_kappa(x, y, levels, weights: str = "unweighted") -> float:
    """Kappa de Cohen, ponderado o no.

    Indefinido (NaN) cuando el acuerdo esperado vale 1, es decir cuando los dos
    anotadores usan un unico nivel identico: no hay margen de mejora sobre el azar.
    """
    m = confusion_matrix(x, y, levels)
    n = m.sum()
    if n == 0:
        return float("nan")
    p = m / n
    w = agreement_weights(levels, weights)
    row = p.sum(axis=1)
    col = p.sum(axis=0)
    p_o = float((w * p).sum())
    p_e = float((w * np.outer(row, col)).sum())
    if np.isclose(p_e, 1.0):
        return float("nan")
    return (p_o - p_e) / (1.0 - p_e)


def gwet_ac1(x, y, levels, weights: str = "unweighted") -> float:
    """AC1 de Gwet (AC2 si se pasan pesos).

    Sustituye el acuerdo esperado de Cohen, que se dispara con prevalencias
    extremas, por uno basado en la probabilidad de que una asignacion sea
    aleatoria. Es el complemento obligatorio frente a la paradoja del kappa.

    p_e = (T_w / (q(q-1))) * sum_k pi_k (1 - pi_k),  pi_k = (n_k1 + n_k2) / 2n
    """
    m = confusion_matrix(x, y, levels)
    n = m.sum()
    q = len(levels)
    if n == 0 or q < 2:
        return float("nan")
    p = m / n
    w = agreement_weights(levels, weights)
    pi = (p.sum(axis=1) + p.sum(axis=0)) / 2.0
    t_w = float(w.sum())
    p_o = float((w * p).sum())
    p_e = (t_w / (q * (q - 1))) * float((pi * (1.0 - pi)).sum())
    if np.isclose(p_e, 1.0):
        return float("nan")
    return (p_o - p_e) / (1.0 - p_e)


def pabak(x, y, levels) -> float:
    """PABAK: kappa ajustado por prevalencia y sesgo (Byrt, Bishop y Carlin, 1993).

    PABAK = (q * p_o - 1) / (q - 1). Con q = 2 se reduce a 2 * p_o - 1.
    Depende solo del acuerdo bruto: por eso acompana al kappa, no lo sustituye.
    """
    q = len(levels)
    if q < 2:
        return float("nan")
    p_o = observed_agreement(x, y, levels, "unweighted")
    if np.isnan(p_o):
        return float("nan")
    return (q * p_o - 1.0) / (q - 1.0)


def _delta2(levels: Sequence, n_c: np.ndarray, metric: str) -> np.ndarray:
    """Matriz de distancias al cuadrado de Krippendorff."""
    q = len(levels)
    if metric == "nominal":
        return 1.0 - np.eye(q)
    if metric == "ordinal":
        d = np.zeros((q, q), dtype=float)
        for a in range(q):
            for b in range(q):
                lo, hi = (a, b) if a <= b else (b, a)
                s = n_c[lo:hi + 1].sum() - (n_c[a] + n_c[b]) / 2.0
                d[a, b] = s ** 2
        return d
    if metric == "interval":
        v = np.asarray(levels, dtype=float)
        return (v[:, None] - v[None, :]) ** 2
    raise ValueError(f"metrica desconocida: {metric}")


def krippendorff_alpha(data: np.ndarray, levels: Sequence, metric: str = "nominal") -> float:
    """Alpha de Krippendorff a partir de la matriz de fiabilidad.

    `data`: array (n_anotadores, n_unidades) con np.nan en lo no anotado.
    Admite datos faltantes y cualquier numero de anotadores.
    Referencia: Krippendorff (2011), "Computing Krippendorff's Alpha-Reliability".
    """
    data = np.asarray(data, dtype=float)
    lookup = {float(v): i for i, v in enumerate(levels)}
    q = len(levels)

    coincidence = np.zeros((q, q), dtype=float)
    for u in range(data.shape[1]):
        vals = data[:, u]
        vals = vals[~np.isnan(vals)]
        m_u = len(vals)
        if m_u < 2:
            continue  # una unidad con una sola valoracion no informa de fiabilidad
        counts = np.zeros(q)
        for v in vals:
            if float(v) not in lookup:
                raise ValueError(f"valor fuera del esquema: {v!r}")
            counts[lookup[float(v)]] += 1
        outer = np.outer(counts, counts)
        np.fill_diagonal(outer, counts * (counts - 1))
        coincidence += outer / (m_u - 1)

    n_c = coincidence.sum(axis=1)
    n = n_c.sum()
    if n < 2:
        return float("nan")

    d2 = _delta2(levels, n_c, metric)
    d_o = float((coincidence * d2).sum()) / n
    d_e = float((np.outer(n_c, n_c) * d2).sum()) / (n * (n - 1))
    if np.isclose(d_e, 0.0):
        return float("nan")
    return 1.0 - d_o / d_e


# --------------------------------------------------------------------------- #
# Bootstrap a nivel de documento
# --------------------------------------------------------------------------- #
@dataclass
class BootstrapResult:
    estimate: float
    ci_low: float
    ci_high: float
    n_resamples: int
    n_degenerate: int
    n_units: int
    replicates: np.ndarray = field(repr=False, default=None)

    @property
    def degenerate_fraction(self) -> float:
        return self.n_degenerate / self.n_resamples if self.n_resamples else float("nan")

    @property
    def excludes_zero(self) -> bool:
        if np.isnan(self.ci_low) or np.isnan(self.ci_high):
            return False
        return (self.ci_low > 0) or (self.ci_high < 0)


def _percentile_ci(reps: np.ndarray, alpha: float) -> tuple[float, float]:
    ok = reps[~np.isnan(reps)]
    if len(ok) < 2:
        return float("nan"), float("nan")
    return (float(np.percentile(ok, 100 * alpha / 2)),
            float(np.percentile(ok, 100 * (1 - alpha / 2))))


def bootstrap_ci(units: Sequence, stat_fn: Callable[[np.ndarray], float],
                 n_resamples: int = 2000, alpha: float = 0.05,
                 seed: int = 42) -> BootstrapResult:
    """IC por bootstrap no parametrico remuestreando DOCUMENTOS con reemplazo.

    `units` son identificadores (o posiciones) de documento. `stat_fn` recibe un
    array de unidades, con repeticiones, y devuelve el estadistico. Remuestrear
    documentos y no anotaciones sueltas respeta la dependencia entre las 12
    variables de un mismo resumen.
    """
    units = np.asarray(units)
    rng = np.random.default_rng(seed)
    est = stat_fn(units)
    reps = np.empty(n_resamples, dtype=float)
    for b in range(n_resamples):
        draw = rng.choice(units, size=len(units), replace=True)
        try:
            reps[b] = stat_fn(draw)
        except Exception:
            reps[b] = np.nan
    lo, hi = _percentile_ci(reps, alpha)
    return BootstrapResult(estimate=est, ci_low=lo, ci_high=hi,
                           n_resamples=n_resamples,
                           n_degenerate=int(np.isnan(reps).sum()),
                           n_units=len(units), replicates=reps)


def paired_bootstrap_delta(units: Sequence,
                           stat_a: Callable[[np.ndarray], float],
                           stat_b: Callable[[np.ndarray], float],
                           n_resamples: int = 2000, alpha: float = 0.05,
                           seed: int = 42) -> BootstrapResult:
    """IC pareado de la diferencia stat_a - stat_b.

    Clave del contraste central: en cada remuestreo se usan LOS MISMOS documentos
    para los dos terminos, de modo que el IC recoge la correlacion entre ambos y
    no la suma de sus varianzas.
    """
    return bootstrap_ci(units, lambda d: stat_a(d) - stat_b(d),
                        n_resamples=n_resamples, alpha=alpha, seed=seed)


def benjamini_hochberg(pvals: Sequence[float], alpha: float = 0.05):
    """Correccion de Benjamini-Hochberg. Devuelve (rechazos, p_ajustados).

    Los NaN se ignoran en la familia y se devuelven como NaN.
    """
    p = np.asarray(pvals, dtype=float)
    ok = ~np.isnan(p)
    adj = np.full(p.shape, np.nan)
    rej = np.zeros(p.shape, dtype=bool)
    if ok.sum() == 0:
        return rej, adj
    sub = p[ok]
    m = len(sub)
    order = np.argsort(sub)
    ranked = sub[order]
    adj_sorted = np.minimum.accumulate((ranked * m / np.arange(1, m + 1))[::-1])[::-1]
    adj_sorted = np.clip(adj_sorted, 0, 1)
    out = np.empty(m)
    out[order] = adj_sorted
    adj[ok] = out
    rej[ok] = out <= alpha
    return rej, adj
