"""Cache en disco de cada llamada, indexada por hash del (modelo, prompt, doc, corrida).

Reejecutar el script no vuelve a llamar a la API para nada que ya este aqui.
Los fallos de parseo tambien se guardan (con `parse_ok: false`) para que queden
registrados, pero no bloquean un reintento.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def call_key(provider: str, model: str, system: str, user: str, schema: dict,
             run_name: str, temperature: float, seed: int) -> str:
    h = hashlib.sha256()
    for part in (provider, model, system, user, json.dumps(schema, sort_keys=True, ensure_ascii=False),
                 run_name, repr(temperature), str(seed)):
        h.update(part.encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()


class CallCache:
    def __init__(self, root: Path, model_name: str):
        self.dir = Path(root) / model_name
        self.dir.mkdir(parents=True, exist_ok=True)

    def path(self, key: str) -> Path:
        return self.dir / f"{key}.json"

    def get(self, key: str) -> dict | None:
        p = self.path(key)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

    def put(self, key: str, record: dict) -> None:
        record = {**record, "cached_at_utc": datetime.now(timezone.utc).isoformat()}
        tmp = self.path(key).with_suffix(".tmp")
        tmp.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
        tmp.replace(self.path(key))
