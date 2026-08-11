"""
test_schema.py — Verify all 6 v0.2 dataclass schemas with runtime validation.
"""
import pytest
from saudi_legal_mcp.tools.schemas import (
    SourceResponse,
    SkillResponse,
    RiskResponse,
    ManifestResponse,
    SourceStatusResponse,
    ReportIssueResponse,
)


# ── SourceResponse ─────────────────────────────────────────────────────────────

def test_source_response_valid():
    r = SourceResponse(
        source_id="labor-law",
        verification_status="unverified",
        content=None,
        content_available=True,
        content_truncated=False,
    )
    d = r.to_dict()
    assert d["source_id"] == "labor-law"
    assert d["verification_status"] == "unverified"
    assert d["disclaimer"] == "هذه معلومات قانونية عامة وليست استشارة قانونية."


def test_source_response_invalid_status():
    with pytest.raises(ValueError, match="invalid verification_status"):
        SourceResponse(
            source_id="labor-law",
            verification_status="unknown_status",
            content=None,
            content_available=True,
            content_truncated=False,
        )


def test_source_response_all_valid_statuses():
    for status in ("unverified", "verified", "review_due", "outdated", "disputed"):
        r = SourceResponse(
            source_id="pdpl",
            verification_status=status,
            content=None,
            content_available=True,
            content_truncated=False,
        )
        assert r.verification_status == status


# ── SkillResponse ──────────────────────────────────────────────────────────────

def test_skill_response_valid():
    r = SkillResponse(
        domain="labor-law-analysis",
        verification_status="unverified",
        content=None,
        content_available=True,
        content_truncated=False,
    )
    d = r.to_dict()
    assert d["domain"] == "labor-law-analysis"


def test_skill_response_invalid_status():
    with pytest.raises(ValueError):
        SkillResponse(
            domain="labor-law-analysis",
            verification_status="invalid",
            content=None,
            content_available=True,
            content_truncated=False,
        )


# ── RiskResponse ───────────────────────────────────────────────────────────────

def test_risk_response_valid():
    r = RiskResponse(
        query={"contract_type": "NDA"},
        total_found=2,
        risks=[{"risk_level": "high"}],
        data_source="saudi-contract-risk-dataset.csv",
    )
    d = r.to_dict()
    assert d["total_found"] == 2
    assert "disclaimer" in d


# ── ManifestResponse ───────────────────────────────────────────────────────────

def test_manifest_response_valid():
    r = ManifestResponse(
        source_id="labor-law",
        verification_status="unverified",
        metadata_status="needs_review",
        sha256="abc123",
        generated_at="2026-08-10T00:00:00+00:00",
        review_due_at=None,
        verified_by=None,
        verified_at=None,
    )
    d = r.to_dict()
    assert d["review_due_at"] is None


def test_manifest_response_invalid_status():
    with pytest.raises(ValueError):
        ManifestResponse(
            source_id="pdpl",
            verification_status="bad_value",
            metadata_status="needs_review",
            sha256=None,
            generated_at=None,
            review_due_at=None,
            verified_by=None,
            verified_at=None,
        )


# ── SourceStatusResponse ───────────────────────────────────────────────────────

def test_source_status_no_warning():
    r = SourceStatusResponse(
        source_id="labor-law",
        verification_status="verified",
        warning=None,
    )
    d = r.to_dict()
    assert d["warning"] is None


def test_source_status_with_warning():
    r = SourceStatusResponse(
        source_id="pdpl",
        verification_status="unverified",
        warning="المصدر غير مُتحقَّق منه بعد.",
    )
    assert r.warning is not None


# ── ReportIssueResponse ────────────────────────────────────────────────────────

def test_report_issue_not_written():
    r = ReportIssueResponse(report_id="N/A", written=False, path=None)
    d = r.to_dict()
    assert d["written"] is False
    assert d["path"] is None


def test_report_issue_written():
    r = ReportIssueResponse(
        report_id="abc12345",
        written=True,
        path="/data/issues/abc12345.json",
    )
    assert r.written is True


# ── Policy enforcement ─────────────────────────────────────────────────────────

def test_enforce_evidence_with_evidence():
    from saudi_legal_mcp.tools.policy import enforce_evidence
    result = enforce_evidence(
        "يحق للموظف كذا",
        [{"source_id": "labor-law", "excerpt": "المادة 74"}],
    )
    assert result["evidence_status"] == "supported"
    assert "claim" in result


def test_enforce_evidence_no_evidence():
    from saudi_legal_mcp.tools.policy import enforce_evidence
    result = enforce_evidence("ادعاء بلا دليل", [])
    assert result["insufficient_evidence"] is True
    assert "claim" not in result
