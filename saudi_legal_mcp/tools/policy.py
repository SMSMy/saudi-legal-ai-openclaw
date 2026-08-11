"""
policy.py — Legal response policy enforcement for Saudi Legal AI MCP Server.

Provides enforce_evidence() — a shared utility that ALL tools must use
when returning any legal claim. This is a programmatic constraint, not
a natural-language instruction.

Usage:
    from tools.policy import enforce_evidence

    result = enforce_evidence(
        claim="يحق للموظف...",
        evidence=[{"source_id": "labor-law", "excerpt": "المادة 74: ..."}],
    )

v0.3 requirement: any new tool (find_legal_provision, build_legal_brief, etc.)
MUST call enforce_evidence() before returning a legal claim.
This is a PR acceptance criterion — see CONTRIBUTING.md.
"""
from __future__ import annotations

_DISCLAIMER = "هذه معلومات قانونية عامة وليست استشارة قانونية."

from saudi_legal_mcp.tools.manifests import get_verification_status

def enforce_evidence(
    claim: str | None,
    evidence: list[dict],
    *,
    disclaimer: str = _DISCLAIMER,
) -> dict:
    """Enforce the evidence requirement for any legal claim.

    Rules (from final-plan.md §5):
    - If evidence is empty → return insufficient_evidence: true, NO claim.
    - If evidence is present → return claim + evidence + evidence_status.
    - claim=None with evidence → evidence_status="supported" (informational result).

    Args:
        claim:      The legal statement being made. May be None for info-only results.
        evidence:   List of dicts, each with at minimum: source_id, excerpt.
                    Each entry should also include: section (optional), authority (optional).
        disclaimer: Legal disclaimer appended to all responses.

    Returns:
        dict with either:
          {"insufficient_evidence": True, "disclaimer": ...}
        or:
          {"claim": ..., "evidence": [...], "evidence_status": "supported", "disclaimer": ...}
    """
    if not evidence:
        return {
            "insufficient_evidence": True,
            "disclaimer": disclaimer,
        }

    # Inject review_level for each evidence item
    enriched_evidence = []
    for item in evidence:
        source_id = item.get("source_id")
        review_level = "unverified"
        if source_id:
            status = get_verification_status(source_id)
            review_level = "human_reviewed" if status == "verified" else status
        
        enriched_item = dict(item)
        enriched_item["review_level"] = review_level
        enriched_evidence.append(enriched_item)

    return {
        "claim": claim,
        "evidence": enriched_evidence,
        "evidence_status": "supported",
        "disclaimer": disclaimer,
    }
