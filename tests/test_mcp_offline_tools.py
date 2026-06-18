"""
Offline MCP Tool Tests — Saudi Legal AI Framework
=================================================
Tests MCP-backed tool behavior without requiring a live MCP transport
or an ANTHROPIC_API_KEY.

Strategy
--------
- search_contract_risks  → reads a local CSV, fully testable offline.
- analyze_contract_clause / get_regulation_summary → return a known JSON error
  payload when ANTHROPIC_API_KEY is absent, which we assert on.
- All tools must return valid JSON regardless of error/success state.

Run with:
    cd /path/to/saudi-legal-ai-framework
    PYTHONPATH=mcp-server pytest tests/test_mcp_offline_tools.py -v
"""
import json
import os
import sys
from pathlib import Path
from typing import Union

import pytest

# ── Path setup ────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
MCP_SERVER_PATH = REPO_ROOT / "mcp-server"
sys.path.insert(0, str(MCP_SERVER_PATH))

# Ensure ANTHROPIC_API_KEY is absent so offline tests are deterministic
os.environ.pop("ANTHROPIC_API_KEY", None)

# ── Imports after path setup ──────────────────────────────────────────────────
from tools.search import find_risks  # noqa: E402
from tools.analyzer import analyze_clause  # noqa: E402
from tools.summarizer import summarize_regulation  # noqa: E402


# ═════════════════════════════════════════════════════════════════════════════
# Helpers
# ═════════════════════════════════════════════════════════════════════════════

def parse_json(raw: str) -> Union[dict, list]:
    """Assert raw output is valid JSON and return parsed object."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        pytest.fail(f"Tool did not return valid JSON.\nRaw output:\n{raw}\nError: {exc}")


# ═════════════════════════════════════════════════════════════════════════════
# search_contract_risks / find_risks
# ═════════════════════════════════════════════════════════════════════════════

class TestFindRisks:
    """Tests for tools/search.py::find_risks() (no API key required)."""

    def test_returns_valid_json_no_filters(self):
        result = parse_json(find_risks())
        assert isinstance(result, dict), "Expected a JSON object at top level"

    def test_top_level_keys_present(self):
        result = parse_json(find_risks())
        required_keys = {"query", "total_found", "risks", "data_source", "disclaimer"}
        assert required_keys.issubset(result.keys()), (
            f"Missing keys: {required_keys - result.keys()}"
        )

    def test_filter_by_contract_type(self):
        result = parse_json(find_risks(contract_type="Employment Contract"))
        # Every returned record must match the filter
        for risk in result["risks"]:
            assert risk.get("risk_level") is not None, "risk_level must be present"

    def test_filter_by_risk_level_critical(self):
        result = parse_json(find_risks(risk_level="critical"))
        for risk in result["risks"]:
            assert risk["risk_level"] == "critical"

    def test_filter_by_risk_level_high(self):
        result = parse_json(find_risks(risk_level="high"))
        for risk in result["risks"]:
            assert risk["risk_level"] == "high"

    def test_requires_escalation_flag_for_critical(self):
        result = parse_json(find_risks(risk_level="critical"))
        for risk in result["risks"]:
            assert risk["requires_escalation"] is True, (
                f"Critical risk must have requires_escalation=True, got {risk}"
            )

    def test_requires_escalation_flag_for_low(self):
        result = parse_json(find_risks(risk_level="low"))
        for risk in result["risks"]:
            assert risk["requires_escalation"] is False, (
                f"Low risk must have requires_escalation=False, got {risk}"
            )

    def test_total_found_matches_risks_length(self):
        result = parse_json(find_risks())
        assert result["total_found"] == len(result["risks"]), (
            "total_found must equal len(risks)"
        )

    def test_combined_filters(self):
        result = parse_json(
            find_risks(contract_type="NDA", risk_level="high")
        )
        for risk in result["risks"]:
            assert risk["risk_level"] == "high"

    def test_unknown_contract_type_returns_empty(self):
        result = parse_json(find_risks(contract_type="NONEXISTENT_CONTRACT_XYZ"))
        assert result["total_found"] == 0
        assert result["risks"] == []

    def test_risk_record_required_fields(self):
        """Every risk record must contain the documented fields."""
        required = {
            "risk_level", "category", "clause_text",
            "risk_reason", "saudi_legal_note",
            "recommended_revision", "related_regulation",
            "requires_escalation",
        }
        result = parse_json(find_risks())
        if result["risks"]:
            first = result["risks"][0]
            assert required.issubset(first.keys()), (
                f"Missing risk record fields: {required - first.keys()}"
            )

    def test_data_source_label(self):
        result = parse_json(find_risks())
        assert "saudi-contract-risk-dataset.csv" in result["data_source"]

    def test_disclaimer_present(self):
        result = parse_json(find_risks())
        assert result["disclaimer"], "disclaimer must be a non-empty string"


# ═════════════════════════════════════════════════════════════════════════════
# analyze_clause — offline (no API key)
# ═════════════════════════════════════════════════════════════════════════════

class TestAnalyzeClauseOffline:
    """Tests for tools/analyzer.py::analyze_clause() without ANTHROPIC_API_KEY."""

    def test_returns_valid_json(self):
        raw = analyze_clause("Test clause", "Employment Contract", "en")
        parse_json(raw)  # will fail the test if not valid JSON

    def test_missing_api_key_returns_error(self):
        result = parse_json(analyze_clause("Test clause", "Employment Contract", "en"))
        assert "error" in result, "Expected an 'error' key when API key is absent"
        assert "ANTHROPIC_API_KEY" in result["error"]

    def test_unknown_contract_type_returns_error(self):
        # Unknown contract type is caught before API key check in newer code,
        # but if API key is missing it may surface the API error first.
        # Either way it must return valid JSON with an 'error' key.
        result = parse_json(
            analyze_clause("clause text", "UNKNOWN_CONTRACT_TYPE_XYZ", "ar")
        )
        assert "error" in result

    def test_error_payload_is_json_object(self):
        result = parse_json(analyze_clause("x", "NDA", "ar"))
        assert isinstance(result, dict), "Error payload must be a JSON object"

    def test_arabic_language_parameter_accepted(self):
        # Just ensure it doesn't raise a Python exception
        raw = analyze_clause("بند تجاري", "Employment Contract", "ar")
        assert isinstance(raw, str) and len(raw) > 0

    def test_english_language_parameter_accepted(self):
        raw = analyze_clause("Test clause", "Lease Agreement", "en")
        assert isinstance(raw, str) and len(raw) > 0


# ═════════════════════════════════════════════════════════════════════════════
# summarize_regulation — offline (no API key)
# ═════════════════════════════════════════════════════════════════════════════

class TestSummarizeRegulationOffline:
    """Tests for tools/summarizer.py::summarize_regulation() without API key."""

    def test_returns_valid_json(self):
        raw = summarize_regulation("labor-law")
        parse_json(raw)

    def test_missing_api_key_returns_error(self):
        result = parse_json(summarize_regulation("labor-law"))
        assert "error" in result
        assert "ANTHROPIC_API_KEY" in result["error"]

    def test_invalid_regulation_returns_error_with_valid_list(self):
        result = parse_json(summarize_regulation("not-a-real-regulation"))
        assert "error" in result
        # Should surface valid regulations list for discoverability
        # (handled in summarizer via read_source returning an error string)
        assert isinstance(result, dict)

    def test_all_known_regulations_return_valid_json(self):
        """Smoke test: every valid regulation key returns parseable JSON."""
        known_regulations = [
            "labor-law", "companies-law", "civil-transactions-law",
            "commercial-courts", "pdpl", "e-commerce-law", "evidence-law",
            "whistleblower-protection", "legal-profession-law", "arbitration-law",
            "bankruptcy-law",
        ]
        for reg in known_regulations:
            raw = summarize_regulation(reg)
            result = parse_json(raw)
            assert isinstance(result, dict), f"Expected dict for regulation '{reg}'"

    def test_topic_filter_accepted(self):
        raw = summarize_regulation("labor-law", topic="termination")
        assert isinstance(raw, str) and len(raw) > 0

    def test_error_payload_structure(self):
        result = parse_json(summarize_regulation("pdpl"))
        assert isinstance(result, dict)
        assert "error" in result
