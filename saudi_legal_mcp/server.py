"""
server.py — Saudi Legal AI MCP Server (v0.4)
Pure retrieval server for OpenClaw. No external API calls. No LLM keys needed.
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from saudi_legal_mcp.tools.skills import read_skill, VALID_DOMAINS
from saudi_legal_mcp.tools.sources import read_source, VALID_REGULATIONS
from saudi_legal_mcp.tools.search import find_risks
from saudi_legal_mcp.tools.reasoning import find_legal_provision, build_legal_brief
from saudi_legal_mcp.tools.manifests import read_manifest
from saudi_legal_mcp.tools.policy import enforce_evidence
from saudi_legal_mcp.tools.schemas import SourceStatusResponse, ReportIssueResponse
from saudi_legal_mcp.tools import get_repo_path

# ── Configuration ────────────────────────────────────────────────────────────────────────────────
# Uses get_repo_path() from tools/__init__.py:
# Priority 1: REPO_PATH env var (local dev / custom data override)
# Priority 2: importlib.resources — works after pip install (no env var needed)
REPO_PATH = get_repo_path()

# Docker/env-var support for report_source_issue (v0.4 will add volumes)
ISSUE_REPORTS_DIR = Path(os.environ.get("ISSUE_REPORTS_DIR", str(REPO_PATH / "issues")))
ENABLE_LOCAL_REPORTS = os.environ.get("ENABLE_LOCAL_REPORTS", "false").lower() == "true"

# Freshness warning threshold (days before review_due_at triggers a warning)
REVIEW_DUE_WARNING_DAYS = 30

# Valid issue types for report_source_issue
_VALID_ISSUE_TYPES = frozenset({
    "outdated", "missing_article", "incorrect_citation", "broken_url",
})

# ── MCP server ────────────────────────────────────────────────────────────────
mcp = FastMCP(
    "Saudi Legal AI Framework",
    instructions=(
        "Saudi legal knowledge retrieval server for OpenClaw. "
        "All tools return structured JSON from official Saudi sources. "
        "The OpenClaw agent performs legal analysis using its active model — "
        "this server never calls an external LLM and requires no API keys. "
        "POLICY: no legal claim is returned without a source citation. "
        "When evidence is insufficient, tools return insufficient_evidence:true. "
        "Always pair retrieval with the mandatory disclaimer: "
        "'هذه معلومات قانونية عامة وليست استشارة قانونية.'"
    ),
)


# ── Tool 1: get_legal_skill ───────────────────────────────────────────────────

@mcp.tool()
def get_legal_skill(
    domain: str,
    section: str = None,
    include_content: bool = False,
) -> dict:
    """Returns the Saudi legal skill/guide for a legal domain.

    The skill tells the agent HOW to reason about that domain under Saudi law:
    scope, key rules, red flags, recommended structure. Content is factual
    reference only — never legal advice. Note: Skills are reasoning guides,
    not legal texts, so they intentionally do not require manifests or 
    verification_status.

    Args:
        domain:          One of: arbitration, commercial-dispute, compliance-check,
                         contract-review, intellectual-property-law, labor-law-analysis,
                         legal-drafting, real-estate-contracts, sports-dispute
        section:         Optional section heading to extract (e.g. "المخاطر الشائعة").
                         Returns only that section, not the full file.
        include_content: If True, returns full skill text (capped at 6000 chars).
                         Default False returns metadata only (saves context).
    """
    return read_skill(domain, section=section, include_content=include_content)


# ── Tool 2: get_regulation_source ────────────────────────────────────────────

@mcp.tool()
def get_regulation_source(
    regulation: str,
    section: str = None,
    include_content: bool = False,
) -> dict:
    """Returns reference information about an official Saudi regulation.

    Returns decree numbers, key articles, competent authority, and deadlines.
    Factual reference only — not the full legal text.

    Args:
        regulation:      One of: arbitration-law, bankruptcy-law,
                         civil-transactions-law, commercial-courts, companies-law,
                         competition-law, e-commerce-law, evidence-law, fifa-rstp,
                         intellectual-property-law, labor-law, legal-profession-law,
                         open-data-judicial-sources, pdpl, real-estate-arbitration-reac,
                         regulation-index, saudi-laws, sports-law-saff,
                         whistleblower-protection, zatca-e-invoicing
        section:         Optional section heading to extract (e.g. "المادة 74").
        include_content: If True, returns full text (capped at 6000 chars).
                         Default False returns metadata only.
    """
    return read_source(regulation, section=section, include_content=include_content)


# ── Tool 3: get_legal_context ─────────────────────────────────────────────────

@mcp.tool()
def get_legal_context(contract_type: str) -> dict:
    """One-call retrieval of everything needed to analyze a contract type.

    Returns: matching skill (reasoning guide) + relevant regulation summary
    + known risk patterns. Each source is capped at 6000 chars to avoid
    context bloat (~12K chars total before risks — see implementation notes).

    Args:
        contract_type: One of: Employment Contract, Lease Agreement,
                       Construction Contract, Supply Agreement, NDA,
                       SaaS Agreement, Cloud Storage Agreement,
                       Professional Services Agreement,
                       Commercial Agency Agreement, Shareholder Agreement,
                       Franchise Agreement
    """
    skill_map = {
        "Employment Contract": "labor-law-analysis",
        "Lease Agreement": "real-estate-contracts",
        "Construction Contract": "commercial-dispute",
        "Supply Agreement": "commercial-dispute",
        "NDA": "compliance-check",
        "SaaS Agreement": "compliance-check",
        "Cloud Storage Agreement": "compliance-check",
        "Professional Services Agreement": "contract-review",
        "Commercial Agency Agreement": "commercial-dispute",
        "Shareholder Agreement": "contract-review",
        "Franchise Agreement": "commercial-dispute",
    }
    source_map = {
        "labor-law-analysis": "labor-law",
        "real-estate-contracts": "real-estate-arbitration-reac",
        "commercial-dispute": "commercial-courts",
        "compliance-check": "pdpl",
        "contract-review": "civil-transactions-law",
    }

    skill_domain = skill_map.get(contract_type)
    if skill_domain is None:
        return {
            "error": f"Unknown contract_type '{contract_type}'.",
            "valid_types": sorted(skill_map),
        }

    skill = read_skill(skill_domain, include_content=False, max_chars=6000)
    source = read_source(source_map[skill_domain], include_content=False, max_chars=6000)
    risks = find_risks(contract_type=contract_type)  # returns dict directly (v0.3)

    return {
        "contract_type": contract_type,
        "skill": skill,
        "regulation": source,
        "risks": risks,
        "context_note": (
            "Skill and regulation each capped at 6000 chars. "
            "Use include_content=True on individual tools for full text."
        ),
        "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
    }


# ── Tool 4: search_contract_risks ────────────────────────────────────────────

@mcp.tool()
def search_contract_risks(
    contract_type: str = None,
    risk_level: str = None,
    category: str = None,
) -> dict:
    """Returns structured risk data from the Saudi contract risk dataset.

    Read-only tabular data describing known legal risk patterns in Saudi
    contracts. Each record contains: risk_level, category, clause_text,
    risk_reason, saudi_legal_note, recommended_revision, related_regulation,
    requires_escalation. Evidence is required for each flag (policy enforced).

    Args:
        contract_type: Optional filter. One of: Employment Contract, Lease Agreement,
                       NDA, SaaS Agreement, Construction Contract, Supply Agreement,
                       Professional Services Agreement, Commercial Agency Agreement,
                       Shareholder Agreement, Franchise Agreement, Cloud Storage Agreement
        risk_level:    Optional filter. One of: critical, high, medium, low
        category:      Optional filter. One of: Employment & Labor, Saudization,
                       Termination, Liability, Data Protection & Privacy,
                       Jurisdiction & Dispute Resolution, Governing Law,
                       Payment Terms, Confidentiality, Intellectual Property,
                       Force Majeure, Warranties, Indemnification, Corporate Governance
    """
    data = find_risks(contract_type, risk_level, category)  # returns dict directly (v0.3)

    # Policy enforcement: each risk must have related_regulation as evidence
    enforced_risks = []
    for risk in data.get("risks", []):
        regulation = risk.get("related_regulation", "")
        evidence = [{"source_id": regulation, "excerpt": risk.get("saudi_legal_note", "")}] if regulation else []
        policy_result = enforce_evidence(None, evidence)
        risk["_policy"] = policy_result
        enforced_risks.append(risk)

    data["risks"] = enforced_risks
    return data


# ── Tool 5: list_legal_domains ────────────────────────────────────────────────

@mcp.tool()
def list_legal_domains() -> dict:
    """Lists all available legal skill domains and regulation sources."""
    return {
        "skills": sorted(VALID_DOMAINS),
        "regulations": sorted(VALID_REGULATIONS),
        "skill_count": len(VALID_DOMAINS),
        "regulation_count": len(VALID_REGULATIONS),
        "verified_count": 0,  # updated as human verification progresses
        "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
    }


# ── Tool 6: get_source_status ─────────────────────────────────────────────────

@mcp.tool()
def get_source_status(source_id: str) -> dict:
    """Returns manifest metadata for a source: publisher, verification status,
    last verified date, and any freshness warnings.

    Args:
        source_id: A key from VALID_REGULATIONS (e.g. "labor-law", "pdpl").
    """
    if source_id not in VALID_REGULATIONS:
        return {
            "error": f"Unknown source_id '{source_id}'.",
            "valid_options": sorted(VALID_REGULATIONS),
        }

    manifest = read_manifest(source_id)
    if manifest is None:
        return SourceStatusResponse(
            source_id=source_id,
            verification_status="unverified",
            warning="Manifest not yet generated. Run scripts/generate_manifests.py.",
        ).to_dict()

    verification_status = manifest.get("verification_status", "unverified")
    review_due_at_str = manifest.get("review_due_at")

    # Build warning
    warning_parts = []

    if verification_status == "field_tested":
        warning_parts.append(
            f"المصدر '{source_id}' مُجرَّب ميدانياً ونجح تقنياً (field_tested)، لكنه لم يُراجع من محامٍ. "
            "استخدمه بحذر وبلا إجابة جازمة."
        )
    elif verification_status != "verified":
        warning_parts.append(
            f"المصدر '{source_id}' غير مُتحقَّق منه بعد (verification_status={verification_status}). "
            "لا تستخدمه في إجابة جازمة."
        )

    # Only check freshness if review_due_at is explicitly set (not None)
    # Never raise exception on None — all current sources have review_due_at=null
    if review_due_at_str is not None:
        try:
            review_due = datetime.fromisoformat(review_due_at_str.replace("Z", "+00:00"))
            days_until_due = (review_due - datetime.now(timezone.utc)).days
            if days_until_due <= REVIEW_DUE_WARNING_DAYS:
                warning_parts.append(
                    f"موعد المراجعة ({review_due_at_str}) "
                    f"يقترب خلال {max(days_until_due, 0)} يوماً."
                )
        except (ValueError, TypeError):
            warning_parts.append(f"قيمة review_due_at غير صالحة: {review_due_at_str!r}")

    return SourceStatusResponse(
        source_id=source_id,
        verification_status=verification_status,
        warning=" | ".join(warning_parts) if warning_parts else None,
    ).to_dict()


# ── Tool 7: report_source_issue ───────────────────────────────────────────────

@mcp.tool()
def report_source_issue(
    source_id: str,
    issue_type: str,
    notes: str,
) -> dict:
    """Creates a local JSON report about a missing, outdated, or inaccurate source.

    Does NOT modify any source file automatically. Requires ENABLE_LOCAL_REPORTS=true
    environment variable to write anything — disabled by default.

    Args:
        source_id:  A key from VALID_REGULATIONS.
        issue_type: One of: outdated, missing_article, incorrect_citation, broken_url
        notes:      Description of the issue. Include the specific article or URL if known.
    """
    # ── Validation always runs first, regardless of ENABLE_LOCAL_REPORTS ─────
    if source_id not in VALID_REGULATIONS:
        raise ValueError(
            f"unknown source_id '{source_id}'. "
            f"Valid IDs: {sorted(VALID_REGULATIONS)}"
        )
    if issue_type not in _VALID_ISSUE_TYPES:
        raise ValueError(
            f"invalid issue_type '{issue_type}'. "
            f"Must be one of: {sorted(_VALID_ISSUE_TYPES)}"
        )
    if not notes or not notes.strip():
        raise ValueError("notes must not be empty.")

    # ── Only after validation: check if writing is enabled ───────────────────
    if not ENABLE_LOCAL_REPORTS:
        return ReportIssueResponse(
            report_id="N/A",
            written=False,
            path=None,
        ).to_dict()

    # Write the report
    report_id = str(uuid.uuid4())[:8]
    report = {
        "report_id": report_id,
        "source_id": source_id,
        "issue_type": issue_type,
        "notes": notes.strip(),
        "reported_at": datetime.now(timezone.utc).isoformat(),
    }

    ISSUE_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = ISSUE_REPORTS_DIR / f"{report_id}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    return ReportIssueResponse(
        report_id=report_id,
        written=True,
        path=str(report_path),
    ).to_dict()


# ── Tool 8: find_legal_provision (v0.4.6 — was dead code, now registered) ─────

@mcp.tool()
def search_legal_provision(
    query: str,
    source_id: str,
    max_sections: int = 3,
    max_chars_per_section: int = 1500,
) -> dict:
    """Searches a regulation source file for sections matching the query.

    Keyword-based section retrieval with Arabic definite-article (ال) aliasing.
    Returns up to max_sections best-matching sections with match confidence.

    The response includes:
      - matched_sections: list of {heading, body, match_score, match_confidence}
      - insufficient_evidence: true when no substantive section matched
      - placeholder_warning: set when sections contain [يحتاج تحقق] markers
      - placeholder_dominated: true when ALL sections contain such markers

    Args:
        query:      Search query (Arabic or English).
        source_id:  A key from VALID_REGULATIONS (e.g. "labor-law", "pdpl").
        max_sections: Maximum sections to return (default 3).
        max_chars_per_section: Cap on returned section body length (default 1500).
    """
    return find_legal_provision(
        query=query,
        source_id=source_id,
        max_sections=max_sections,
        max_chars_per_section=max_chars_per_section,
    )


# ── Tool 9: build_legal_brief (v0.4.6 — was dead code, now registered) ────────

@mcp.tool()
def get_legal_brief(
    scenario: str,
    domain: str,
    contract_type: str = None,
    source_id: str = None,
) -> dict:
    """Assembles a structured legal brief from skill + provisions + risks.

    Orchestrator tool: retrieves the domain skill, searches the regulation
    source for matching provisions, and pulls known contract risks — then
    assembles them into a single capped brief (max 4000 chars).

    Evidence policy:
      - insufficient_evidence: true when no usable evidence is found
      - placeholder_dominated: when ALL retrieved sections are placeholder
        text, the brief is withheld (insufficient_evidence: true)
      - placeholder_warning: attached when partial placeholder text exists

    Args:
        scenario:      Free-text legal scenario (Arabic or English).
        domain:        A key from VALID_DOMAINS (e.g. "labor-law-analysis").
        contract_type: Optional contract type for risk lookup (e.g. "SaaS Agreement").
        source_id:     Optional regulation key from VALID_REGULATIONS.
    """
    return build_legal_brief(
        scenario=scenario,
        domain=domain,
        contract_type=contract_type,
        source_id=source_id,
    )


# ── Entrypoint ────────────────────────────────────────────────────────────────────────────────

def main() -> None:
    """Entry point for the `saudi-legal-mcp` console script (pyproject.toml)."""
    mcp.run()


if __name__ == "__main__":
    main()
