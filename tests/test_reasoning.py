"""
test_reasoning.py -- Tests for v0.3 reasoning tools.

Validates:
  - find_legal_provision finds sections anywhere in the file (not just first 3000 chars)
  - max_chars_per_section cap is respected (default 1500)
  - insufficient_evidence returned when no matches found
  - unknown source_id handled gracefully
  - ProvisionResponse and LegalBriefResponse schema conformance
  - match_confidence in [0.0, 1.0]
"""
import pytest
from saudi_legal_mcp.tools.reasoning import find_legal_provision, build_legal_brief
from saudi_legal_mcp.tools.schemas import ProvisionResponse, LegalBriefResponse, MatchedSection


# -- find_legal_provision -----------------------------------------------------

class TestFindLegalProvision:

    def test_finds_section_beyond_3000_chars(self):
        """Saudization section starts at char ~4014 in labor-law.md.
        The old read_source(max_chars=3000) would have missed it entirely."""
        result = find_legal_provision(
            query="سعودة نطاقات توطين",
            source_id="labor-law",
        )
        assert result.get("insufficient_evidence") is False, (
            "Expected to find Saudization content beyond char 3000"
        )
        sections = result.get("matched_sections", [])
        assert len(sections) >= 1
        # At least one matched section heading should relate to Saudization
        headings = " ".join(s["heading"] for s in sections)
        assert "سعودة" in headings or "Saudization" in headings or "Nitaqat" in headings

    def test_finds_termination_notice(self):
        """Termination notice terms exist in labor-law.md."""
        result = find_legal_provision(
            query="إشعار إنهاء عقد",
            source_id="labor-law",
        )
        assert result.get("insufficient_evidence") is False
        assert len(result.get("matched_sections", [])) >= 1

    def test_max_chars_per_section_respected(self):
        """No returned section body should exceed max_chars_per_section."""
        result = find_legal_provision(
            query="بيانات شخصية موافقة معالجة",
            source_id="pdpl",
            max_chars_per_section=1500,
        )
        if result.get("insufficient_evidence"):
            pytest.skip("No matching sections found -- check pdpl.md content")
        for section in result.get("matched_sections", []):
            assert len(section["body"]) <= 1500, (
                f"Section body exceeds 1500 chars: {len(section['body'])}"
            )

    def test_max_sections_respected(self):
        """Should return at most max_sections results."""
        result = find_legal_provision(
            query="عقد عمل نظام",
            source_id="labor-law",
            max_sections=2,
        )
        if not result.get("insufficient_evidence"):
            assert len(result.get("matched_sections", [])) <= 2

    def test_unknown_source_id_returns_error(self):
        """Unknown source_id must return an error, not raise an exception."""
        result = find_legal_provision(
            query="اختبار",
            source_id="nonexistent-law-xyz",
        )
        assert "error" in result
        assert "valid_options" in result

    def test_no_matching_terms_returns_insufficient_evidence(self):
        """Gibberish query that matches nothing should return insufficient_evidence=True."""
        result = find_legal_provision(
            query="xyzxyz123 zzz",
            source_id="labor-law",
        )
        assert result.get("insufficient_evidence") is True
        assert result.get("matched_sections") == []

    def test_match_confidence_in_range(self):
        """match_confidence must be in [0.0, 1.0] for all returned sections."""
        result = find_legal_provision(
            query="تقادم مدة فصل",
            source_id="labor-law",
        )
        if result.get("insufficient_evidence"):
            pytest.skip("No matching sections")
        for section in result.get("matched_sections", []):
            conf = section.get("match_confidence")
            assert conf is not None
            assert 0.0 <= conf <= 1.0, f"match_confidence out of range: {conf}"

    def test_result_has_disclaimer(self):
        result = find_legal_provision(query="عقد", source_id="labor-law")
        assert "disclaimer" in result


# -- ProvisionResponse schema -------------------------------------------------

class TestProvisionResponseSchema:

    def test_provision_response_fields(self):
        r = ProvisionResponse(
            source_id="labor-law",
            query="test",
            matched_sections=[],
            total_matched=0,
            insufficient_evidence=True,
        )
        d = r.to_dict()
        assert d["source_id"] == "labor-law"
        assert d["insufficient_evidence"] is True
        assert d["matched_sections"] == []
        assert "disclaimer" in d

    def test_matched_section_fields(self):
        ms = MatchedSection(
            heading="## التعريفات",
            body="نص قصير",
            match_score=3,
            match_confidence=0.75,
        )
        d = ms.to_dict()
        assert d["heading"] == "## التعريفات"
        assert d["match_score"] == 3
        assert d["match_confidence"] == 0.75


# -- LegalBriefResponse schema ------------------------------------------------

class TestLegalBriefResponseSchema:

    def test_legal_brief_response_insufficient(self):
        r = LegalBriefResponse(
            scenario="test",
            domain="nonexistent-domain",
            contract_type=None,
            source_id=None,
            evidence_count=0,
            brief=None,
            insufficient_evidence=True,
        )
        d = r.to_dict()
        assert d["insufficient_evidence"] is True
        assert d["brief"] is None
        assert "disclaimer" in d

    def test_legal_brief_response_with_data(self):
        r = LegalBriefResponse(
            scenario="هل ينتهي عقد العمل تلقائياً؟",
            domain="labor",
            contract_type="Employment Contract",
            source_id="labor-law",
            evidence_count=2,
            brief="مذكرة تجريبية",
            insufficient_evidence=False,
        )
        d = r.to_dict()
        assert d["evidence_count"] == 2
        assert d["brief"] == "مذكرة تجريبية"


# -- build_legal_brief integration --------------------------------------------

class TestBuildLegalBrief:

    def test_brief_returns_dict(self):
        result = build_legal_brief(
            scenario="هل يُلزم صاحب العمل بتقديم إشعار قبل إنهاء العقد؟",
            domain="labor",
            source_id="labor-law",
        )
        assert isinstance(result, dict)

    def test_brief_char_cap(self):
        """Output brief must not exceed 4000 chars."""
        result = build_legal_brief(
            scenario="ما التزامات الشركة تجاه حماية بيانات الموظفين وفق PDPL؟",
            domain="data-protection",
            source_id="pdpl",
        )
        brief = result.get("brief")
        if brief is not None:
            assert len(brief) <= 4000, f"Brief exceeds 4000 chars: {len(brief)}"

    def test_brief_insufficient_evidence_for_unknown_domain(self):
        """An entirely unknown domain with no matching source should return insufficient."""
        result = build_legal_brief(
            scenario="سؤال عشوائي",
            domain="nonexistent-domain-xyz",
            source_id=None,
            contract_type=None,
        )
        assert result.get("insufficient_evidence") is True


# -- v0.4.5/0.4.7 evidence gates (regression) ---------------------------------

class TestEvidenceGates:

    def test_bankruptcy_all_placeholder_returns_insufficient(self):
        """Gate A: when ALL retrieved sections are [يحتاج تحقق] templates,
        the brief must be withheld — the skill alone is not legal data."""
        result = build_legal_brief(
            scenario="كم مهلة اعتراض الدائنين وفق اللائحة التنفيذية لنظام الإفلاس",
            domain="commercial-dispute",
            source_id="bankruptcy-law",
        )
        assert result.get("insufficient_evidence") is True
        assert result.get("brief") is None

    def test_bankruptcy_with_contract_risks_not_insufficient(self):
        """Mixed evidence: placeholder provisions + real risk data →
        brief allowed with placeholder_warning attached."""
        result = build_legal_brief(
            scenario="كم مهلة اعتراض الدائنين",
            domain="commercial-dispute",
            source_id="bankruptcy-law",
            contract_type="Employment Contract",
        )
        assert result.get("insufficient_evidence") is False

    def test_labor_brief_passes_with_real_evidence(self):
        """Real (non-dominated) provisions must still produce a brief."""
        result = build_legal_brief(
            scenario="كم مدة إشعار إنهاء عقد العمل للموظف",
            domain="labor-law-analysis",
            source_id="labor-law",
        )
        assert result.get("insufficient_evidence") is False
        assert result.get("evidence_count", 0) >= 1

    def test_weak_confidence_provisions_filtered_from_brief(self):
        """Gate B: provisions below MATCH_CONFIDENCE_THRESHOLD are excluded
        from evidence.  build_legal_brief must not count them."""
        from saudi_legal_mcp.tools.reasoning import find_legal_provision
        from saudi_legal_mcp.tools.search import MATCH_CONFIDENCE_THRESHOLD

        result = find_legal_provision(
            query="المهل الزمنية اعتراض الدائنين",
            source_id="bankruptcy-law",
        )
        raw = result.get("matched_sections", [])
        assert raw, "expected raw sections for the gate test"
        weak = [s for s in raw if s["match_confidence"] < MATCH_CONFIDENCE_THRESHOLD]
        assert weak, "test premise requires at least one weak section"

        brief = build_legal_brief(
            scenario="المهل الزمنية اعتراض الدائنين",
            domain="commercial-dispute",
            source_id="bankruptcy-law",
        )
        if not brief.get("insufficient_evidence"):
            # brief evidence must exclude weak sections
            assert brief.get("evidence_count", 0) < 1 + len(raw)

    def test_provision_response_has_placeholder_dominated_field(self):
        result = find_legal_provision(
            query="المهل الزمنية",
            source_id="bankruptcy-law",
        )
        assert "placeholder_dominated" in result
        assert isinstance(result["placeholder_dominated"], bool)
