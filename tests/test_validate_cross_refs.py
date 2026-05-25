# tests/test_validate_cross_refs.py
"""
Tests for scripts/validate_cross_refs.py
Saudi Legal AI Framework — reverse-discovery seam validator
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import validate_cross_refs as vcr


# ── Heading detection ──────────────────────────────────────────────────────────

def test_normalize_heading_strips_hashes():
    assert vcr._normalize_heading("## Introduction") == "introduction"

def test_normalize_heading_strips_section_number():
    assert vcr._normalize_heading("## 11. Relevant Regulations / الأنظمة ذات الصلة") == "relevant regulations / الأنظمة ذات الصلة"

def test_normalize_heading_strips_section_number_with_symbol():
    assert vcr._normalize_heading("## §11 Relevant Regulations") == "relevant regulations"

def test_is_regulations_heading_english():
    assert vcr._is_regulations_heading("## 11. Relevant Regulations / الأنظمة ذات الصلة")

def test_is_regulations_heading_arabic():
    assert vcr._is_regulations_heading("## الأنظمة المرتبطة")

def test_is_regulations_heading_unrelated():
    assert not vcr._is_regulations_heading("## Introduction")

def test_is_regulations_heading_case_insensitive():
    assert vcr._is_regulations_heading("## RELEVANT REGULATIONS")

def test_is_see_also_heading():
    assert vcr._is_see_also_heading("## See also / انظر أيضًا")

def test_is_see_also_heading_plain():
    assert vcr._is_see_also_heading("## See also")

def test_is_see_also_heading_unrelated():
    assert not vcr._is_see_also_heading("## Overview")

def test_is_regulations_heading_arabic_alt():
    assert vcr._is_regulations_heading("## الأنظمة ذات الصلة")

def test_is_see_also_heading_arabic_only():
    assert vcr._is_see_also_heading("## انظر أيضًا")


# ── Path extraction ────────────────────────────────────────────────────────────

def test_extract_source_paths_backtick():
    text = "See `sources/labor-law.md` for details"
    assert vcr._extract_source_paths(text) == {"sources/labor-law.md"}

def test_extract_source_paths_bare():
    text = "See sources/pdpl.md in this project"
    assert vcr._extract_source_paths(text) == {"sources/pdpl.md"}

def test_extract_source_paths_multiple():
    text = "`sources/labor-law.md` and `sources/pdpl.md`"
    assert vcr._extract_source_paths(text) == {"sources/labor-law.md", "sources/pdpl.md"}

def test_extract_source_paths_deduplicates():
    text = "`sources/labor-law.md` appears twice `sources/labor-law.md`"
    assert vcr._extract_source_paths(text) == {"sources/labor-law.md"}

def test_extract_source_paths_excludes_regulation_index():
    text = "راجع `sources/regulation-index.md` للصيغ الرسمية"
    assert "sources/regulation-index.md" not in vcr._extract_source_paths(text)

def test_extract_skill_paths_backtick():
    text = "Implemented in `skills/contract-review.md`"
    assert vcr._extract_skill_paths(text) == {"skills/contract-review.md"}

def test_extract_skill_paths_markdown_link():
    text = "- [skills/contract-review.md](../skills/contract-review.md) — §11"
    assert vcr._extract_skill_paths(text) == {"skills/contract-review.md"}


# ── Section extraction ─────────────────────────────────────────────────────────

def test_extract_section_returns_body(tmp_path):
    skill = tmp_path / "skill.md"
    skill.write_text(
        "## Introduction\nSome text.\n\n"
        "## 11. Relevant Regulations / الأنظمة ذات الصلة\n"
        "`sources/labor-law.md`\n\n"
        "## 12. Next Section\nOther content.\n",
        encoding="utf-8",
    )
    body = vcr._extract_section(skill.read_text(encoding="utf-8").splitlines(), vcr._is_regulations_heading)
    assert "sources/labor-law.md" in body
    assert "Next Section" not in body

def test_extract_section_not_found_returns_empty(tmp_path):
    skill = tmp_path / "skill.md"
    skill.write_text("## Introduction\nSome text.\n", encoding="utf-8")
    body = vcr._extract_section(skill.read_text(encoding="utf-8").splitlines(), vcr._is_regulations_heading)
    assert body == ""


# ── parse_skill ────────────────────────────────────────────────────────────────

def test_parse_skill_finds_sources_in_regulations_section(tmp_path):
    skill = tmp_path / "labor-law-analysis.md"
    skill.write_text(
        "## Introduction\nSome intro.\n\n"
        "## 11. Relevant Regulations / الأنظمة ذات الصلة\n"
        "| نظام العمل | م/51 | الإطار | `sources/labor-law.md` |\n"
        "| PDPL | م/19 | السرية | `sources/pdpl.md` |\n"
        "راجع `sources/regulation-index.md` للصيغ الرسمية.\n\n"
        "## 12. Next\nOther.\n",
        encoding="utf-8",
    )
    result = vcr.parse_skill(skill)
    assert result == {"sources/labor-law.md", "sources/pdpl.md"}
    assert "sources/regulation-index.md" not in result

def test_parse_skill_ignores_sources_outside_regulations(tmp_path):
    skill = tmp_path / "skill.md"
    skill.write_text(
        "## Introduction\nSee `sources/other.md` here.\n\n"
        "## 11. Relevant Regulations / الأنظمة ذات الصلة\n"
        "`sources/labor-law.md`\n\n"
        "## 12. Next\n",
        encoding="utf-8",
    )
    assert vcr.parse_skill(skill) == {"sources/labor-law.md"}

def test_parse_skill_arabic_heading(tmp_path):
    skill = tmp_path / "skill.md"
    skill.write_text(
        "## الأنظمة المرتبطة\n`sources/civil-transactions-law.md`\n\n## Next\n",
        encoding="utf-8",
    )
    assert vcr.parse_skill(skill) == {"sources/civil-transactions-law.md"}

def test_parse_skill_no_regulations_section_returns_empty(tmp_path):
    skill = tmp_path / "skill.md"
    skill.write_text("## Introduction\nNo regulations here.\n", encoding="utf-8")
    assert vcr.parse_skill(skill) == set()


# ── parse_source ───────────────────────────────────────────────────────────────

def test_parse_source_no_see_also(tmp_path):
    source = tmp_path / "labor-law.md"
    source.write_text("## Overview\nSome content.\n", encoding="utf-8")
    has_see_also, skills = vcr.parse_source(source)
    assert not has_see_also
    assert skills == set()

def test_parse_source_with_see_also_backtick(tmp_path):
    source = tmp_path / "labor-law.md"
    source.write_text(
        "## Overview\nContent.\n\n"
        "## See also / انظر أيضًا\n"
        "- `skills/labor-law-analysis.md` — §11\n"
        "- `skills/compliance-check.md` — §11\n",
        encoding="utf-8",
    )
    has_see_also, skills = vcr.parse_source(source)
    assert has_see_also
    assert skills == {"skills/labor-law-analysis.md", "skills/compliance-check.md"}

def test_parse_source_with_see_also_markdown_link(tmp_path):
    source = tmp_path / "labor-law.md"
    source.write_text(
        "## See also / انظر أيضًا\n"
        "| [skills/contract-review.md](../skills/contract-review.md) | §11 |\n",
        encoding="utf-8",
    )
    has_see_also, skills = vcr.parse_source(source)
    assert has_see_also
    assert "skills/contract-review.md" in skills


# ── run_checks integration ─────────────────────────────────────────────────────

def _write_skill(path: Path, name: str, sources: list) -> None:
    rows = "\n".join(f"| reg | ref | desc | `{s}` |" for s in sources)
    path.write_text(
        f"## Introduction\nIntro.\n\n"
        f"## 11. Relevant Regulations / الأنظمة ذات الصلة\n"
        f"{rows}\n"
        f"راجع `sources/regulation-index.md` للصيغ الرسمية.\n\n"
        f"## 12. Next\nOther.\n",
        encoding="utf-8",
    )

def _write_source_with_see_also(path: Path, skills: list) -> None:
    rows = "\n".join(
        f"| [skills/{s}](../skills/{s}) | §11 | desc |"
        for s in skills
    )
    path.write_text(
        f"## Overview\nContent.\n\n---\n\n"
        f"## See also / انظر أيضًا\n\n"
        f"| Skill | Section | طبيعة الاستخدام |\n"
        f"|-------|---------|----------------|\n"
        f"{rows}\n",
        encoding="utf-8",
    )

def _write_source_no_see_also(path: Path) -> None:
    path.write_text("## Overview\nContent.\n", encoding="utf-8")


def test_run_checks_passes_when_all_correct(tmp_path):
    skills_dir = tmp_path / "skills"
    sources_dir = tmp_path / "sources"
    skills_dir.mkdir()
    sources_dir.mkdir()
    cross_ref = tmp_path / "cross-reference-map.md"

    _write_skill(skills_dir / "labor-law-analysis.md", "labor-law-analysis", ["sources/labor-law.md"])
    _write_source_with_see_also(sources_dir / "labor-law.md", ["labor-law-analysis.md"])
    cross_ref.write_text(
        "## 1b.\n`sources/labor-law.md` | `skills/labor-law-analysis.md`\n",
        encoding="utf-8",
    )

    errors, warnings = vcr.run_checks(skills_dir, sources_dir, cross_ref)
    assert errors == []
    assert warnings == []


def test_run_checks_check1_missing_see_also(tmp_path):
    skills_dir = tmp_path / "skills"
    sources_dir = tmp_path / "sources"
    skills_dir.mkdir()
    sources_dir.mkdir()
    cross_ref = tmp_path / "cross-reference-map.md"
    cross_ref.write_text("", encoding="utf-8")

    _write_skill(skills_dir / "labor-law-analysis.md", "labor-law-analysis", ["sources/labor-law.md"])
    _write_source_no_see_also(sources_dir / "labor-law.md")

    errors, _ = vcr.run_checks(skills_dir, sources_dir, cross_ref)
    assert any("no '## See also'" in e for e in errors)


def test_run_checks_check2_missing_reverse_link(tmp_path):
    skills_dir = tmp_path / "skills"
    sources_dir = tmp_path / "sources"
    skills_dir.mkdir()
    sources_dir.mkdir()
    cross_ref = tmp_path / "cross-reference-map.md"
    cross_ref.write_text("", encoding="utf-8")

    _write_skill(skills_dir / "compliance-check.md", "compliance-check", ["sources/labor-law.md"])
    _write_source_with_see_also(sources_dir / "labor-law.md", ["labor-law-analysis.md"])

    errors, _ = vcr.run_checks(skills_dir, sources_dir, cross_ref)
    assert any("missing skills/compliance-check.md" in e for e in errors)


def test_run_checks_check3_phantom_reference(tmp_path):
    skills_dir = tmp_path / "skills"
    sources_dir = tmp_path / "sources"
    skills_dir.mkdir()
    sources_dir.mkdir()
    cross_ref = tmp_path / "cross-reference-map.md"
    cross_ref.write_text("", encoding="utf-8")

    _write_skill(skills_dir / "legal-drafting.md", "legal-drafting", ["sources/pdpl.md"])
    (sources_dir / "pdpl.md").write_text("## Overview\n", encoding="utf-8")
    _write_source_with_see_also(sources_dir / "labor-law.md", ["legal-drafting.md"])

    errors, _ = vcr.run_checks(skills_dir, sources_dir, cross_ref)
    assert any("phantom" in e.lower() or "does not cite" in e for e in errors)


def test_run_checks_check4_map_missing_row_is_warning(tmp_path):
    skills_dir = tmp_path / "skills"
    sources_dir = tmp_path / "sources"
    skills_dir.mkdir()
    sources_dir.mkdir()
    cross_ref = tmp_path / "cross-reference-map.md"
    cross_ref.write_text("# Map\nNo rows yet.\n", encoding="utf-8")

    _write_skill(skills_dir / "labor-law-analysis.md", "labor-law-analysis", ["sources/labor-law.md"])
    _write_source_with_see_also(sources_dir / "labor-law.md", ["labor-law-analysis.md"])

    errors, warnings = vcr.run_checks(skills_dir, sources_dir, cross_ref)
    assert errors == []
    assert any("cross-reference-map" in w for w in warnings)
