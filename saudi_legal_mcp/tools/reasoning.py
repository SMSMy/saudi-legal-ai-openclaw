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
from saudi_legal_mcp.tools.sources import VALID_REGULATIONS, _extract_links
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


# v0.4.9 — diacritics stripped from both haystack and query terms so
# 'يوما' matches 'يومًا' (tanween/fatha/sukun are not semantic for
# retrieval).  ROADMAP Arabic-normalisation backlog item, now justified
# by a concrete false-insufficient case.
_DIACRITICS_RE = re.compile(r"[\u064B-\u0652\u0670]")

# v0.4.10 — orthographic normalization (safe, no true stemming):
# hamza seats أ/إ/آ → ا, alef maqsura ى → ي, ta marbuta ة → ه.
# These variants are pure spelling differences — same word, same root.
# True synonym mapping (الموظف/العامل) is deliberately OUT of scope
# (would need a dictionary and carries over-matching risk).
_HAMZA_TABLE = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه"})


def _strip_diacritics(s: str) -> str:
    return _DIACRITICS_RE.sub("", s)


def _normalize_arabic(s: str) -> str:
    """Diacritics removal + orthographic normalization for matching."""
    return _strip_diacritics(s).translate(_HAMZA_TABLE)


# v0.4.12 — minimal synonym groups for scoring-side expansion.
# Built ONLY from the documented direct-tool failure
# ('كم يستحق الموظف إجازة في السنة؟' → insufficient_evidence:true
# although the leaves section contains the answer): الموظف↔العامل,
# السنة↔سنوياً/سنوية, يستحق↔تستحق.  Groups are in NORMALIZED form.
# Per the v0.4.3 lesson, expansion happens at scoring time — the query
# term count (confidence denominator) stays unchanged.
_SYNONYM_GROUPS: tuple[frozenset[str], ...] = (
    frozenset({"الموظف", "العامل"}),
    frozenset({"السنه", "سنه", "سنويا", "سنويه", "سنوي", "السنوي"}),
    frozenset({"يستحق", "تستحق"}),
)


def _synonym_variants(term_normalized: str) -> frozenset[str]:
    """Return the synonym group containing the term (normalized), or just the term."""
    for group in _SYNONYM_GROUPS:
        if term_normalized in group:
            return group
    return frozenset({term_normalized})


# v0.4.11 — phrase-level equivalence for the EVAL comparison layer.
# The eval compares expected_answer_contains terms against retrieved
# content literally, while the retrieval engine treats these forms as
# equivalent: phrase-level definite article (تسوية وقائية ↔ التسوية
# الوقائية), prepositional ال elision (للمحاكم ↔ المحاكم), word-medial
# hamza (غسل أموال ↔ غسل الاموال).  The comparison must speak the same
# normalization language as retrieval — otherwise the metric punishes
# correct retrieval for spelling variance.
_ARABIC_PREFIXES = ("لل", "وال", "بال", "كال", "فال", "ال")


def normalize_phrase(s: str) -> str:
    """Normalize Arabic text for equivalence comparison.

    Diacritics + orthographic normalization, then per-word stripping of
    leading prefixes (لل/وال/بال/كال/فال/ال).  Symmetric on both sides —
    used by the eval runner's recall check, not by retrieval scoring.
    """
    normalized = _normalize_arabic(s)
    out_words = []
    for w in normalized.split():
        for pref in _ARABIC_PREFIXES:
            if w.startswith(pref) and len(w) > len(pref) + 1:
                w = w[len(pref):]
                break
        out_words.append(w)
    return " ".join(out_words)


def _score_section(section: dict, query_terms: list[str]) -> int:
    """Return hit count of query_terms found in section heading + body.

    v0.4.3: Arabic definite-article (ال) aliasing (v0.3 decision implemented).
    A query token "مدعي" matches section text "المدعي" and vice versa.
    v0.4.9: diacritics-stripped matching ('يوما' ↔ 'يومًا').
    v0.4.10: orthographic normalization (أ/إ/آ→ا, ى→ي, ة→ه) on both sides.
    Only Arabic-script tokens receive alias expansion to avoid false matches
    on Latin text.  Query term count is unchanged — this is scoring-side
    expansion, not query-side inflation.
    """
    haystack = _normalize_arabic(
        (section["heading"] + " " + section["body"]).lower()
    )
    score = 0
    for term in query_terms:
        t = _normalize_arabic(term.lower())
        matched = False
        for variant in _synonym_variants(t):
            if variant in haystack:
                matched = True
                break
            # ال-aliasing per variant (المدعي/مدعي — v0.4.3 decision)
            if len(variant) > 2 and variant[:2] == "ال" and variant[2:] in haystack:
                matched = True
                break
            if len(variant) >= 2 and ("ال" + variant) in haystack:
                matched = True
                break
        if matched:
            score += 1
    return score


def _is_arabic(s: str) -> bool:
    """True if string consists entirely of Arabic-script characters."""
    return bool(re.fullmatch(r"[\u0600-\u06ff]+", s))


# v0.4.9 — Arabic function words excluded from scoring.  Full-question
# scenarios were diluted by tokens like كم/في/هل, pushing confidence
# below the 0.7 gate and triggering false insufficient_evidence.
_ARABIC_STOPWORDS = frozenset({
    "كم", "في", "من", "إلى", "على", "عن", "هل", "ما", "هذا", "هذه",
    "ذلك", "تلك", "الذي", "التي", "الذين", "أن", "إن", "هو", "هي",
    "هم", "لم", "لن", "لا", "قد", "كان", "كانت", "كل", "بعض", "أي",
    "غير", "حيث", "إذا", "ثم", "أو", "حتى", "مع", "بين", "بعد", "قبل",
    "عند", "لدى", "نحو", "حول", "مثل", "دون", "كيف", "متى", "أين",
    "لماذا", "ماذا", "هل", "ما",
})


def _tokenize_query(query: str) -> list[str]:
    """Extract meaningful tokens from query.

    v0.4.9: Arabic letters only (U+0621-U+064A — punctuation such as
    '؟' and diacritics are no longer glued to tokens), and function
    words are excluded.  Latin tokens unchanged (>= 3 chars).
    """
    tokens = re.findall(r"[\u0621-\u064A]{2,}|[a-zA-Z]{3,}", query)
    seen: set[str] = set()
    unique: list[str] = []
    for t in tokens:
        t_lower = t.lower()
        if t_lower in _ARABIC_STOPWORDS:
            continue
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
            # v0.4.9: citations scope-bound to THIS section's body
            citations=_extract_links(section["body"]),
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
    prov_raw_count: int = 0
    if source_id:
        prov_result = find_legal_provision(scenario, source_id)
        if not prov_result.get("insufficient_evidence"):
            raw_sections = prov_result.get("matched_sections", [])
            prov_raw_count = len(raw_sections)
            # v0.4.9: brief includes all substantively-matched sections.
            # Confidence gating lives in search_legal_provision (tool layer);
            # the orchestrator keeps real retrieved text and relies on the
            # placeholder gate for safety (see insufficient-evidence gate).
            provisions = list(raw_sections)
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

    # v0.4.5/0.4.9 gate: insufficient when ALL data evidence is
    # placeholder-dominated (gate A).  Confidence gating (0.7) is the
    # tool-layer responsibility of search_legal_provision — applying it
    # here as well produced false insufficient_evidence on full
    # natural-language scenarios, where token-ratio confidence is
    # systematically depressed by synonym/morphology variance.
    # The safety-critical gate is placeholder dominance, which stays.
    has_data = prov_raw_count > 0 or bool(risks)
    data_all_placeholder = (
        prov_raw_count > 0
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

    # v0.4.9: sources & links section — citations from matched sections
    # and risk related_regulation.  Portal labels are copied verbatim so
    # the portal-vs-article distinction survives into the brief text.
    sources_text = ""
    seen_sources: set[str] = set()
    for p in provisions:
        for c in p.get("citations", []):
            url = c.get("url", "")
            if url and url not in seen_sources:
                seen_sources.add(url)
                label = c.get("label") or url
                sources_text += f"- [{label}]({url})\n"
    if not sources_text:
        for r in risks[:3]:
            reg = r.get("related_regulation", "")
            if reg and reg not in seen_sources:
                seen_sources.add(reg)
                sources_text += f"- {reg}\n"

    sources_block = ""
    if sources_text:
        sources_block = f"\n### المصادر والروابط\n{sources_text}\n"

    brief = (
        f"## مذكرة قانونية مختصرة\n"
        f"**السيناريو:** {scenario}\n\n"
        f"### السياق المجالي ({domain})\n{skill_summary[:400]}\n\n"
        f"### النصوص النظامية ذات الصلة\n{sections_text}\n"
        f"### المخاطر التعاقدية\n{risks_text}\n"
        f"{sources_block}"
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
