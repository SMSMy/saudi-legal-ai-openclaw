"""
test_server.py — MCP tool registration regression tests.

Lesson (2026-08-12): build_legal_brief and find_legal_provision were
fully implemented in tools/reasoning.py since v0.3 but NEVER registered
as MCP tools — real OpenClaw agents had only 7 tools for the entire
project lifetime.  These tests lock the registration so dead-code
regression is impossible to miss again.
"""
import asyncio

import pytest

EXPECTED_TOOL_NAMES = {
    "get_legal_skill",
    "get_regulation_source",
    "get_legal_context",
    "search_contract_risks",
    "list_legal_domains",
    "get_source_status",
    "report_source_issue",
    "search_legal_provision",   # v0.4.6 — was dead code
    "get_legal_brief",          # v0.4.6 — was dead code
}


@pytest.fixture(scope="module")
def registered_tools() -> list[str]:
    from saudi_legal_mcp.server import mcp
    tools = asyncio.run(mcp.list_tools())
    return [t.name for t in tools]


def test_nine_tools_registered(registered_tools):
    names = set(registered_tools)
    missing = EXPECTED_TOOL_NAMES - names
    assert not missing, (
        f"Registered tools missing: {sorted(missing)}. "
        "Dead-code regression: tools exist in tools/*.py but are not "
        "exposed via @mcp.tool() in server.py."
    )
    assert len(names) == len(EXPECTED_TOOL_NAMES), (
        f"Unexpected extra tools: {sorted(names - EXPECTED_TOOL_NAMES)}"
    )


def test_search_legal_provision_confidence_gate():
    """v0.4.7: weak sections (conf < 0.7) must be excluded, not warned."""
    from saudi_legal_mcp.server import search_legal_provision

    result = search_legal_provision(
        query="المهل الزمنية اعتراض الدائنين",
        source_id="bankruptcy-law",
    )
    if result.get("insufficient_evidence"):
        return  # acceptable outcome — gate may refuse everything

    for s in result.get("matched_sections", []):
        assert s["match_confidence"] >= 0.7, (
            f"Section below threshold leaked through the gate: "
            f"conf={s['match_confidence']}, heading={s['heading']}"
        )
    assert "excluded_low_confidence_count" in result
