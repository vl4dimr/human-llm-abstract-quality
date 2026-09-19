"""Pruebas del prompt de la fase 2: esquema, validacion y blindaje frente a etiquetas humanas."""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lib.io_raw import load_config, variable_specs  # noqa: E402
from lib.llm.prompt import build_schema, build_system, build_user, load_protocol, validate_output  # noqa: E402

cfg = load_config()
SPECS = variable_specs(cfg)


def test_schema_has_one_field_per_variable_plus_notes():
    s = build_schema(SPECS, include_notes=True)
    assert set(s["properties"]) == set(SPECS) | {"observaciones"}
    assert s["additionalProperties"] is False
    assert list(s["properties"])[-1] == "observaciones"


def test_validate_accepts_protocol_conformant_output():
    s = build_schema(SPECS)
    good = {v: (1 if SPECS[v]["type"] == "binary" else 3) for v in SPECS}
    good["no_evaluable"] = 0
    good["observaciones"] = "ok"
    assert validate_output(good, s) == []
    good["D4_consistencia"] = None  # permitido por §9.3
    assert validate_output(good, s) == []


def test_validate_rejects_out_of_scheme_values():
    s = build_schema(SPECS)
    bad = {v: 0 for v in SPECS}
    bad["observaciones"] = ""
    bad["D2_coherencia"] = 7
    bad["D1_imryd_objetivo"] = True   # bool no es un nivel valido
    errs = validate_output(bad, s)
    assert any("D2_coherencia" in e for e in errs)
    assert any("D1_imryd_objetivo" in e for e in errs)


def test_strip_sections_removes_only_requested():
    p = ROOT / "data" / "raw" / "scheme" / "PROTOCOLO_ANOTACION.md"
    full = load_protocol(p)
    stripped = load_protocol(p, ["## 12."])
    assert "## 12. Ejemplos completos resueltos" in full
    assert "## 12. Ejemplos completos resueltos" not in stripped
    assert "## 6. Dimensión 1" in stripped


def test_prompts_contain_no_human_annotations():
    """Blindaje: ninguna observacion ni etiqueta humana aparece en ningun prompt."""
    p = ROOT / "data" / "raw" / "scheme" / "PROTOCOLO_ANOTACION.md"
    system = build_system(load_protocol(p))
    docs = pd.read_csv(ROOT / "data" / "interim" / "documents.csv")
    ann = pd.read_csv(ROOT / "data" / "interim" / "annotations.csv")
    human_notes = pd.read_excel(ROOT / "data" / "raw" / "annotations" / "Anotacion_principal_A1.xlsx",
                                sheet_name="Anotación")["Observaciones"].dropna().astype(str)
    frags = [n[:40] for n in human_notes if len(n) >= 40]
    for d in docs.head(40).itertuples():
        user = build_user(d.title, d.text)
        for f in frags:
            assert f not in user and f not in system, f"fragmento de observacion humana en el prompt: {f!r}"
        # ningun par 'variable: valor' de ese documento
        for r in ann[(ann.doc_id == d.doc_id) & (ann.annotator == "A1")].itertuples():
            assert f"{r.category}: {r.label}" not in user
    assert "annotations" not in json.dumps(build_schema(SPECS))
