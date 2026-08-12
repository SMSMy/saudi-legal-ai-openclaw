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


def _strip_placeholders(text: str) -> str:
    """Remove [يحتاج تحقق ...] placeholder markers from text.

    v0.4.5: these markers indicate missing/not-yet-verified information.
    Sections whose query match depends entirely on placeholder text are
    not real evidence and should be excluded from retrieval results.
    """
    return re.sub(r"\[يحتاج تحقق[^\]]*\]", "", text)


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
    """Return hit count of query_terms found in section heading + body.

    v0.4.3: Arabic definite-article (ال) aliasing (v0.3 decision implemented).
    A query token "مدعي" matches section text "المدعي" and vice versa.
    Only Arabic-script tokens receive alias expansion to avoid false matches
    on Latin text.  Query term count is unchanged — this is scoring-side
    expansion, not query-side inflation.
    """
    haystack = (section["heading"] + " " + section["body"]).lower()
    score = 0
    for term in query_terms:
        t = term.lower()
        if t in haystack:
            score += 1
        elif _is_arabic(term):
            # Try ال-stripped variant (المدعي → مدعي)
            if len(term) > 2 and term[:2] == "ال" and term[2:] in haystack:
                score += 1
            # Try ال-prepended variant (مدعي → المدعي)
            elif len(term) >= 2 and ("ال" + term).lower() in haystack:
                score += 1
    return score


def _is_arabic(s: str) -> bool:
    """True if string consists entirely of Arabic-script characters."""
    return bool(re.fullmatch(r"[\u0600-\u06ff]+", s))


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

    # v0.4.5 — exclude sections whose score comes entirely from
    # [يحتاج تحقق] placeholder markers.
    substantive_hits: list[tuple[dict, int]] = []
    for section, score in hits:
        stripped = _strip_placeholders(section["body"])
        stripped_score = _score_section(
            {"heading": section["heading"], "body": stripped},
            query_terms,
        )
        if stripped_score == 0:
            continue  # all query matches were inside [يحتاج تحقق] blocks
        substantive_hits.append((section, score))

    if not substantive_hits:
        return {
            "source_id": source_id,
            "query": query,
            "matched_sections": [],
            "total_matched": 0,
            "insufficient_evidence": True,
            "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
        }

    top = substantive_hits[:max_sections]
    matched: list[dict] = []

    # Check placeholder signals on the sections actually returned
    any_placeholder = False
    all_placeholder = len(top) > 0
    for section, score in top:
        has_marker = "يحتاج تحقق" in section["body"]
        if has_marker:
            any_placeholder = True
        else:
            all_placeholder = False
        body = section["body"][:max_chars_per_section]
        confidence = round(score / max(len(query_terms), 1), 2)
        matched.append(asdict(MatchedSection(
            heading=section["heading"],
            body=body,
            match_score=score,
            match_confidence=confidence,
        )))

    placeholder_warning: Optional[str] = None
    if all_placeholder:
        placeholder_warning = (
            "جميع الأقسام المسترجعة تحتوي على علامات [يحتاج تحقق] "
            "تشير إلى معلومات غير مكتملة أو لم تُراجع بعد. "
            "هذه الأدلة غير كافية للإجابة."
        )
    elif any_placeholder:
        placeholder_warning = (
            "بعض الأقسام المسترجعة تحتوي على علامات [يحتاج تحقق] "
            "تشير إلى معلومات غير مكتملة أو لم تُراجع بعد."
        )

    return asdict(ProvisionResponse(
        source_id=source_id,
        query=query,
        matched_sections=matched,
        total_matched=len(hits),
        insufficient_evidence=False,
        placeholder_warning=placeholder_warning,
        placeholder_dominated=all_placeholder,
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

    # include_content=True required — default graduated interface returns
    # metadata only, which would leave the skill section empty (v0.4.6 fix)
    skill_result = read_skill(domain, include_content=True)
    skill_summary: str = ""
    if isinstance(skill_result, dict) and not skill_result.get("error"):
        skill_summary = (skill_result.get("content") or "")[:800]
        if skill_summary:
            evidence_parts.append(f"[skill:{domain}]")

    provisions: list[dict] = []
    prov_placeholder_warning: Optional[str] = None
    prov_placeholder_dominated: bool = False
    if source_id:
        prov_result = find_legal_provision(scenario, source_id)
        if not prov_result.get("insufficient_evidence"):
            provisions = prov_result.get("matched_sections", [])
            prov_placeholder_warning = prov_result.get("placeholder_warning")
            prov_placeholder_dominated = prov_result.get("placeholder_dominated", False)
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

    # v0.4.5 gate: if ALL data evidence is dominated by placeholders
    # (every retrieved section contains [يحتاج تحقق] markers), treat as
    # insufficient even if a skill is present.  The skill provides
    # conceptual guidance, not specific legal data.
    has_data = bool(provisions) or bool(risks)
    data_all_placeholder = (
        bool(provisions)
        and prov_placeholder_dominated
        and not bool(risks)
    )
    if has_data and data_all_placeholder:
        return {
            "scenario": scenario,
            "domain": domain,
            "contract_type": contract_type,
            "source_id": source_id,
            "insufficient_evidence": True,
            "brief": None,
            "placeholder_warning": prov_placeholder_warning,
            "disclaimer": (
                "جميع النصوص النظامية المسترجعة تحتوي على علامات [يحتاج تحقق] "
                "تشير إلى معلومات غير مكتملة. لا يمكن إصدار مذكرة قانونية بهذا "
                "الدليل. يرجى الاستعانة بمحامٍ مرخّص."
            ),
        }

    sections_text = ""
    for p in provisions:
        # strip markdown # prefix — heading already includes it, wrapping in
        # ** would render "**## 8. ...**" instead of a clean heading (v0.4.6)
        clean_heading = p.get('heading', '').lstrip('#').strip()
        sections_text += f"\n**{clean_heading}**\n{p.get('body','')[:400]}\n"

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

    response = asdict(LegalBriefResponse(
        scenario=scenario,
        domain=domain,
        contract_type=contract_type,
        source_id=source_id,
        evidence_count=len(evidence_parts),
        brief=brief,
        insufficient_evidence=False,
    ))
    if prov_placeholder_warning:
        response["placeholder_warning"] = prov_placeholder_warning
    return response
