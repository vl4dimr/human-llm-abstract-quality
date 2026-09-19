"""Logging comun: consola + archivo con timestamp en outputs/logs/."""
from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

_FMT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"


def get_logger(name: str, log_dir: Path) -> logging.Logger:
    """Devuelve un logger que escribe a consola y a outputs/logs/<name>_<ts>.log."""
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    path = log_dir / f"{name}_{stamp}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    fh = logging.FileHandler(path, encoding="utf-8")
    fh.setFormatter(logging.Formatter(_FMT))
    logger.addHandler(fh)

    # La consola de Windows suele ser cp1252; forzamos UTF-8 para los acentos.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter(_FMT))
    logger.addHandler(sh)

    logger.info("log -> %s", path)
    return logger
