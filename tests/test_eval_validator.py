import pytest
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from evals.validate_cases import validate_case
import jsonschema
import json

@pytest.fixture
def registry():
    return {
        "test_law": {
            "name": "Test Law",
            "decree": "m/1",
            "date": "1440/01/01هـ",
            "url": "https://example.com/law"
        }
    }

@pytest.fixture
def schema():
    schema_path = REPO_ROOT / "evals" / "schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_base_case():
    return {
        "id": "TEST-001",
        "domain": "test",
        "status": "draft",
        "scenario": "test scenario",
        "reference_answer": "test answer",
        "source_id": "test_law",
        "source_url": "https://example.com/law",
        "source_locator": "Article 1",
        "source_version": "1440/01/01هـ",
        "verified_at": "2024-06-19",
        "must_include": ["test"],
        "must_not_claim": ["wrong"],
        "critical_errors": ["critical"],
        "scoring": {
            "legal_accuracy_weight": 0.6,
            "source_accuracy_weight": 0.25,
            "safety_and_limits_weight": 0.15
        }
    }

def test_valid_case(registry, schema):
    case = get_base_case()
    jsonschema.validate(instance=[case], schema=schema)
    errors = validate_case(case, 0, "test.json", registry)
    assert len(errors) == 0

def test_invalid_scoring_sum(registry):
    case = get_base_case()
    case["scoring"]["legal_accuracy_weight"] = 0.5
    errors = validate_case(case, 0, "test.json", registry)
    assert any("sum of scoring weights" in e for e in errors)

def test_missing_source_id_in_registry(registry):
    case = get_base_case()
    case["source_id"] = "unknown_law"
    errors = validate_case(case, 0, "test.json", registry)
    assert any("not found in source-registry" in e for e in errors)

def test_source_id_contains_mXX(registry):
    case = get_base_case()
    case["source_id"] = "test_law_m12"
    registry["test_law_m12"] = registry["test_law"]
    errors = validate_case(case, 0, "test.json", registry)
    assert any("must not contain decree numbers like _mXX" in e for e in errors)

def test_invalid_verified_at(registry):
    case = get_base_case()
    # Hijri slash format is genuinely non-ISO (strptime "%Y-%m-%d" rejects it)
    case["verified_at"] = "1445/02/02هـ"
    errors = validate_case(case, 0, "test.json", registry)
    assert any("not ISO YYYY-MM-DD" in e for e in errors)

def test_invalid_effective_date(registry):
    case = get_base_case()
    # Hijri slash format is genuinely non-ISO (strptime "%Y-%m-%d" rejects it)
    case["effective_date"] = "1445/02/02هـ"
    errors = validate_case(case, 0, "test.json", registry)
    assert any("not ISO YYYY-MM-DD" in e for e in errors)

def test_source_url_mismatch(registry):
    case = get_base_case()
    case["source_url"] = "https://example.com/wrong"
    errors = validate_case(case, 0, "test.json", registry)
    assert any("does not match registry URL" in e for e in errors)

def test_source_version_mismatch(registry):
    case = get_base_case()
    case["source_version"] = "1499/12/30هـ"
    errors = validate_case(case, 0, "test.json", registry)
    assert any("does not match registry date" in e for e in errors)

def test_missing_required_field(schema):
    case = get_base_case()
    del case["scenario"]
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(instance=[case], schema=schema)

def test_additional_property(schema):
    case = get_base_case()
    case["extra"] = "value"
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(instance=[case], schema=schema)
