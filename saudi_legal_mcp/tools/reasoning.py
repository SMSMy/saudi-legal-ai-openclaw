"""
reasoning.py - Saudi Legal AI v0.3
Semantic section retrieval and legal brief orchestration.

Tools:
  - find_legal_provision: Keyword-based section retrieval from a regulation file.
  - build_legal_brief: Orchestrator that assembles skill + provisions + risks into a brief.
"""
from __future__ import annotations

import re
from dataclasses import asdict
from typing import Optional

from saudi_legal_mcp.tools import get_repo_path
from saudi_legal_mcp.tools.sources import VALID_REGULATIONS
from saudi_legal_mcp.tools.schemas import ProvisionResponse, MatchedSection, LegalBriefResponse
from saudi_legal_mcp.tools.skills import read_skill
from saudi_legal_mcp.tools.search import find_risks, MATCH_CONFIDENCE_THRESHOLD

# Constants
_MAX_CHARS_PER_SECTION = 1500
_MAX_SECTIONS_RETURNED = 3
_BRIEF_MAX_CHARS = 4000


def _split_into_sections(text: str) -> list[dict]:
    """Split markdown text into sections by heading level (## or ###)."""
    lines = text.splitlines()
    sections: list[dict] = []
    current_heading = "(preamble)"
    current_level = 0
    current_body: list[str] = []

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("#"):
            if current_body or current_heading != "(preamble)":
                sections.append({
                    "heading": current_heading,
                    "body": "\n".join(current_body).strip(),
                    "level": current_level,
                })
            j = 0
            while j < len(line) and line[j] == "#":
                j += 1
            current_level = j
            current_heading = line.strip()
            current_body = []
        else:
            current_body.append(line)

    if current_body or current_heading != "(preamble)":
        sections.append({
            "heading": current_heading,
            "body": "\n".join(current_body).strip(),
            "level": current_level,
        })

    return sections


def _score_section(section: dict, query_terms: list[str]) -> int:
    """Return hit count of query_terms found in section heading + body (case-insensitive)."""
    haystack = (section["heading"] + " " + section["body"]).lower()
    return sum(1 for term in query_terms if term.lower() in haystack)


def _tokenize_query(query: str) -> list[str]:
    """Extract meaningful tokens from query (Arabic words >= 2 chars or Latin >= 3 chars)."""
    tokens = re.findall(r"[\u0600-\u06ff]{2,}|[a-zA-Z]{3,}", query)
    seen: set[str] = set()
    unique: list[str] = []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique


def find_legal_provision(
    query: str,
    source_id: str,
    max_sections: int = _MAX_SECTIONS_RETURNED,
    max_chars_per_section: int = _MAX_CHARS_PER_SECTION,
) -> dict:
    """Search a regulation file for sections matching the query.

    Uses keyword scoring across all Markdown headings/bodies.
    Returns up to max_sections best-matching sections, each capped
    at max_chars_per_section characters.

    Returns insufficient_evidence=True if no matches found.

    *** ARCHITECTURAL CONTRACT (v0.3) ***
    This function is a RAW INFORMATION LAYER — it applies NO confidence threshold.
    Every section with score > 0 is returned, each carrying its own match_confidence.
    THE CALLER is solely responsible for applying MATCH_CONFIDENCE_THRESHOLD before
    presenting results as supported evidence to the user.
    build_legal_brief() does this correctly via its enforce_evidence gate.
    Any future tool that calls find_legal_provision() directly (not via build_legal_brief)
    MUST apply the threshold before treating matched_sections as confirmed evidence.
    Failure to do so will silently surface low-confidence sections as legal authority.
    """
    if source_id not in VALID_REGULATIONS:
        return {
            "error": f"Unknown source_id '{source_id}'.",
            "valid_options": sorted(VALID_REGULATIONS),
            "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
        }

    source_path = get_repo_path() / "sources" / f"{source_id}.md"
    if not source_path.exists():
        return {
            "error": f"Source file not found: {source_path.name}",
            "source_id": source_id,
            "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
        }

    full_text = source_path.read_text(encoding="utf-8")
    sections = _split_into_sections(full_text)

    query_terms = _tokenize_query(query)
    if not query_terms:
        return {
            "source_id": source_id,
            "query": query,
            "matched_sections": [],
            "total_matched": 0,
            "insufficient_evidence": True,
            "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
        }

    scored = sorted(
        [(s, _score_section(s, query_terms)) for s in sections],
        key=lambda x: x[1],
        reverse=True,
    )
    hits = [(s, score) for s, score in scored if score > 0]

    if not hits:
        return {
            "source_id": source_id,
            "query": query,
            "matched_sections": [],
            "total_matched": 0,
            "insufficient_evidence": True,
            "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
        }

    top = hits[:max_sections]
    matched: list[dict] = []
    for section, score in top:
        body = section["body"][:max_chars_per_section]
        confidence = round(score / max(len(query_terms), 1), 2)
        matched.append(asdict(MatchedSection(
            heading=section["heading"],
            body=body,
            match_score=score,
            match_confidence=confidence,
        )))

    return asdict(ProvisionResponse(
        source_id=source_id,
        query=query,
        matched_sections=matched,
        total_matched=len(hits),
        insufficient_evidence=False,
    ))


def build_legal_brief(
    scenario: str,
    domain: str,
    contract_type: Optional[str] = None,
    source_id: Optional[str] = None,
) -> dict:
    """Orchestrate a brief legal analysis from skill + provisions + risks.

    enforce_evidence is applied: if no evidence found across all sources,
    returns insufficient_evidence=True with no brief.
    """
    import json
    evidence_parts: list[str] = []

    skill_result = read_skill(domain)
    skill_summary: str = ""
    if isinstance(skill_result, dict) and not skill_result.get("error"):
        skill_summary = (skill_result.get("content") or "")[:800]
        if skill_summary:
            evidence_parts.append(f"[skill:{domain}]")

    provisions: list[dict] = []
    if source_id:
        prov_result = find_legal_provision(scenario, source_id)
        if not prov_result.get("insufficient_evidence"):
            provisions = prov_result.get("matched_sections", [])
            for p in provisions:
                evidence_parts.append(f"[provision:{source_id}:{p.get('heading','')}]")

    risks: list[dict] = []
    if contract_type:
        risk_result = find_risks(contract_type=contract_type)  # returns dict directly
        raw_risks = risk_result.get("risks", [])
        resp_confidence = risk_result.get("match_confidence")  # None = exact match (always trusted)
        # Gate: if fuzzy matching was used and confidence is below threshold, treat as no evidence
        confidence_ok = (
            resp_confidence is None  # exact match — always trusted
            or resp_confidence >= MATCH_CONFIDENCE_THRESHOLD
        )
        if confidence_ok:
            for r in raw_risks[:3]:
                reg = r.get("related_regulation", "")
                if reg:
                    evidence_parts.append(f"[risk:{contract_type}]")
            risks = raw_risks[:3]

    if not evidence_parts:
        return {
            "scenario": scenario,
            "domain": domain,
            "insufficient_evidence": True,
            "brief": None,
            "disclaimer": "لا يوجد دليل كافٍ لإصدار مذكرة قانونية. يرجى الاستعانة بمحامٍ مرخّص.",
        }

    sections_text = ""
    for p in provisions:
        sections_text += f"\n**{p.get('heading','')}**\n{p.get('body','')[:400]}\n"

    risks_text = ""
    for r in risks:
        risks_text += f"- [{r.get('risk_level','').upper()}] {r.get('risk_reason','')[:200]}\n"

    brief = (
        f"## مذكرة قانونية مختصرة\n"
        f"**السيناريو:** {scenario}\n\n"
        f"### السياق المجالي ({domain})\n{skill_summary[:400]}\n\n"
        f"### النصوص النظامية ذات الصلة\n{sections_text}\n"
        f"### المخاطر التعاقدية\n{risks_text}\n"
        f"\n*الأدلة المستخدمة: {len(evidence_parts)} مصدر(اً)*"
    )[:_BRIEF_MAX_CHARS]

    return asdict(LegalBriefResponse(
        scenario=scenario,
        domain=domain,
        contract_type=contract_type,
        source_id=source_id,
        evidence_count=len(evidence_parts),
        brief=brief,
        insufficient_evidence=False,
    ))
