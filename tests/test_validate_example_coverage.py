# tests/test_validate_example_coverage.py
"""
Tests for scripts/validate_example_coverage.py
Saudi Legal AI Framework — skill→example coverage validator
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import validate_example_coverage as vec


# ── Helpers ────────────────────────────────────────────────────────────────────

def _write_skill_with_examples(path: Path, example_refs: list) -> None:
    items = "\n".join(
        f"* [{ref}](../{ref}) — description"
        for ref in example_refs
    )
    path.write_text(
        f"## Introduction\nIntro.\n\n"
        f"## 11. Relevant Regulations\n\n"
        f"## Related examples / أمثلة مرتبطة\n\n"
        f"{items}\n",
        encoding="utf-8",
    )


def _write_skill_no_section(path: Path) -> None:
    path.write_text(
        "## Introduction\nIntro.\n\n## 11. Relevant Regulations\n",
        encoding="utf-8",
    )


def _write_skill_malformed_item(path: Path) -> None:
    path.write_text(
        "## Related examples / أمثلة مرتبطة\n\n"
        "* some description without a link\n",
        encoding="utf-8",
    )


def _write_example(path: Path) -> None:
    path.write_text("# Example\nContent.\n", encoding="utf-8")


# ── Heading detection ──────────────────────────────────────────────────────────

def test_normalize_heading_strips_hashes():
    assert vec._normalize_heading("## Related examples") == "related examples"

def test_normalize_heading_arabic():
    assert vec._normalize_heading("## أمثلة مرتبطة") == "أمثلة مرتبطة"

def test_normalize_heading_strips_section_number():
    assert vec._normalize_heading("## 15. Related examples") == "related examples"

def test_is_related_examples_heading_bilingual():
    assert vec._is_related_examples_heading("## Related examples / أمثلة مرتبطة")

def test_is_related_examples_heading_arabic_only():
    assert vec._is_related_examples_heading("## أمثلة مرتبطة")

def test_is_related_examples_heading_case_insensitive():
    assert vec._is_related_examples_heading("## RELATED EXAMPLES")

def test_is_related_examples_heading_with_section_number():
    assert vec._is_related_examples_heading("## 15. Related examples")

def test_is_related_examples_heading_unrelated():
    assert not vec._is_related_examples_heading("## Introduction")

def test_is_related_examples_heading_unrelated_arabic():
    assert not vec._is_related_examples_heading("## الأنظمة ذات الصلة")


# ── Path extraction ────────────────────────────────────────────────────────────

def test_extract_example_paths_relative():
    text = "* [examples/foo.md](../examples/foo.md) — description"
    assert vec._extract_example_paths(text) == ["examples/foo.md"]

def test_extract_example_paths_without_dotdot():
    text = "* [foo](examples/foo.md) — description"
    assert vec._extract_example_paths(text) == ["examples/foo.md"]

def test_extract_example_paths_multiple():
    text = (
        "* [a](../examples/a.md) — desc\n"
        "* [b](../examples/b.md) — desc\n"
    )
    result = vec._extract_example_paths(text)
    assert "examples/a.md" in result
    assert "examples/b.md" in result
    assert len(result) == 2

def test_extract_example_paths_ignores_non_examples():
    text = "* [skills/foo.md](../skills/foo.md) — not an example"
    assert vec._extract_example_paths(text) == []

def test_extract_example_paths_empty_section():
    assert vec._extract_example_paths("") == []


# ── Malformed item detection ───────────────────────────────────────────────────

def test_find_malformed_items_clean():
    text = "* [examples/foo.md](../examples/foo.md) — description"
    assert vec._find_malformed_items(text) == []

def test_find_malformed_items_no_link():
    text = "* some description without a link"
    result = vec._find_malformed_items(text)
    assert len(result) == 1
    assert "some description without a link" in result[0]

def test_find_malformed_items_dash_prefix():
    text = "- some item without a link"
    assert len(vec._find_malformed_items(text)) == 1

def test_find_malformed_items_blank_lines_ok():
    text = "\n\n* [examples/foo.md](../examples/foo.md) — ok\n\n"
    assert vec._find_malformed_items(text) == []

def test_find_malformed_items_non_list_lines_ok():
    text = "Some intro text\n* [examples/foo.md](../examples/foo.md) — ok"
    assert vec._find_malformed_items(text) == []

def test_find_malformed_items_link_to_wrong_dir():
    text = "* [sources/foo.md](../sources/foo.md) — wrong dir"
    assert len(vec._find_malformed_items(text)) == 1


# ── parse_skill ────────────────────────────────────────────────────────────────

def test_parse_skill_with_valid_section(tmp_path):
    skill = tmp_path / "labor-law-analysis.md"
    _write_skill_with_examples(skill, ["examples/labor-dispute.md"])
    has_section, paths, malformed = vec.parse_skill(skill)
    assert has_section
    assert "examples/labor-dispute.md" in paths
    assert malformed == []

def test_parse_skill_no_section(tmp_path):
    skill = tmp_path / "skill.md"
    _write_skill_no_section(skill)
    has_section, paths, malformed = vec.parse_skill(skill)
    assert not has_section
    assert paths == []
    assert malformed == []

def test_parse_skill_malformed_item(tmp_path):
    skill = tmp_path / "skill.md"
    _write_skill_malformed_item(skill)
    has_section, paths, malformed = vec.parse_skill(skill)
    assert has_section
    assert paths == []
    assert len(malformed) == 1

def test_parse_skill_arabic_heading(tmp_path):
    skill = tmp_path / "skill.md"
    skill.write_text(
        "## أمثلة مرتبطة\n\n"
        "* [examples/foo.md](../examples/foo.md) — description\n",
        encoding="utf-8",
    )
    has_section, paths, _ = vec.parse_skill(skill)
    assert has_section
    assert "examples/foo.md" in paths

def test_parse_skill_empty_section(tmp_path):
    skill = tmp_path / "skill.md"
    skill.write_text(
        "## Related examples / أمثلة مرتبطة\n\n## Next Section\n",
        encoding="utf-8",
    )
    has_section, paths, malformed = vec.parse_skill(skill)
    assert has_section
    assert paths == []
    assert malformed == []

def test_parse_skill_section_not_bleed_into_next(tmp_path):
    skill = tmp_path / "skill.md"
    skill.write_text(
        "## Related examples / أمثلة مرتبطة\n\n"
        "* [examples/foo.md](../examples/foo.md) — ok\n\n"
        "## Next Section\n"
        "* [examples/bar.md](../examples/bar.md) — should not appear\n",
        encoding="utf-8",
    )
    _, paths, _ = vec.parse_skill(skill)
    assert "examples/foo.md" in paths
    assert "examples/bar.md" not in paths

def test_parse_skill_deduplicates_paths(tmp_path):
    skill = tmp_path / "skill.md"
    skill.write_text(
        "## Related examples / أمثلة مرتبطة\n\n"
        "* [examples/foo.md](../examples/foo.md) — ok\n"
        "* [examples/foo.md](../examples/foo.md) — duplicate\n",
        encoding="utf-8",
    )
    _, paths, _ = vec.parse_skill(skill)
    assert len(paths) == 1


# ── coverage_status ────────────────────────────────────────────────────────────

def test_coverage_status_missing():
    assert vec.coverage_status(0) == "Missing"

def test_coverage_status_partial():
    assert vec.coverage_status(1) == "Partial"

def test_coverage_status_strong_two():
    assert vec.coverage_status(2) == "Strong"

def test_coverage_status_strong_many():
    assert vec.coverage_status(5) == "Strong"


# ── run_checks integration ─────────────────────────────────────────────────────

def _make_dirs(tmp_path):
    skills_dir = tmp_path / "skills"
    examples_dir = tmp_path / "examples"
    skills_dir.mkdir()
    examples_dir.mkdir()
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    return skills_dir, examples_dir, docs_dir


def test_run_checks_passes_all_valid(tmp_path):
    skills_dir, examples_dir, docs_dir = _make_dirs(tmp_path)
    cross_ref = docs_dir / "cross-reference-map.md"
    cross_ref.write_text(
        "## Skill → Example Coverage\n"
        "| `skills/labor-law-analysis.md` | 1 | ... | Partial |\n",
        encoding="utf-8",
    )
    _write_example(examples_dir / "labor-dispute.md")
    _write_skill_with_examples(
        skills_dir / "labor-law-analysis.md",
        ["examples/labor-dispute.md"],
    )
    errors, warnings = vec.run_checks(skills_dir, examples_dir, cross_ref)
    assert errors == []
    assert warnings == []


def test_run_checks_check1_malformed_item_is_error(tmp_path):
    skills_dir, examples_dir, docs_dir = _make_dirs(tmp_path)
    cross_ref = docs_dir / "cross-reference-map.md"
    cross_ref.write_text("", encoding="utf-8")
    _write_skill_malformed_item(skills_dir / "skill.md")
    errors, _ = vec.run_checks(skills_dir, examples_dir, cross_ref)
    assert any("malformed" in e for e in errors)


def test_run_checks_check2_broken_path_is_error(tmp_path):
    skills_dir, examples_dir, docs_dir = _make_dirs(tmp_path)
    cross_ref = docs_dir / "cross-reference-map.md"
    cross_ref.write_text("", encoding="utf-8")
    _write_skill_with_examples(
        skills_dir / "skill.md",
        ["examples/does-not-exist.md"],
    )
    errors, _ = vec.run_checks(skills_dir, examples_dir, cross_ref)
    assert any("not found" in e for e in errors)


def test_run_checks_check3_no_section_is_warning(tmp_path):
    skills_dir, examples_dir, docs_dir = _make_dirs(tmp_path)
    cross_ref = docs_dir / "cross-reference-map.md"
    cross_ref.write_text("", encoding="utf-8")
    _write_skill_no_section(skills_dir / "skill.md")
    errors, warnings = vec.run_checks(skills_dir, examples_dir, cross_ref)
    assert errors == []
    assert any("no '## Related examples'" in w for w in warnings)


def test_run_checks_check4_zero_examples_is_warning(tmp_path):
    skills_dir, examples_dir, docs_dir = _make_dirs(tmp_path)
    cross_ref = docs_dir / "cross-reference-map.md"
    cross_ref.write_text("", encoding="utf-8")
    (skills_dir / "skill.md").write_text(
        "## Related examples / أمثلة مرتبطة\n\n## Next\n",
        encoding="utf-8",
    )
    errors, warnings = vec.run_checks(skills_dir, examples_dir, cross_ref)
    assert errors == []
    assert any("0 valid examples" in w for w in warnings)


def test_run_checks_check5_map_missing_row_is_warning(tmp_path):
    skills_dir, examples_dir, docs_dir = _make_dirs(tmp_path)
    cross_ref = docs_dir / "cross-reference-map.md"
    cross_ref.write_text(
        "## Skill → Example Coverage\n| some-other-skill | ...\n",
        encoding="utf-8",
    )
    _write_example(examples_dir / "example.md")
    _write_skill_with_examples(skills_dir / "skill.md", ["examples/example.md"])
    errors, warnings = vec.run_checks(skills_dir, examples_dir, cross_ref)
    assert errors == []
    assert any("cross-reference-map" in w for w in warnings)


def test_run_checks_missing_skills_dir_is_error(tmp_path):
    errors, _ = vec.run_checks(
        tmp_path / "nonexistent-skills",
        tmp_path / "examples",
        tmp_path / "map.md",
    )
    assert any("not found" in e for e in errors)


def test_run_checks_broken_path_does_not_suppress_warning_for_other_skills(tmp_path):
    """Check 2 error in skill-a does not suppress Check 3 warning for skill-b."""
    skills_dir, examples_dir, docs_dir = _make_dirs(tmp_path)
    cross_ref = docs_dir / "cross-reference-map.md"
    cross_ref.write_text("", encoding="utf-8")
    _write_skill_with_examples(skills_dir / "skill-a.md", ["examples/missing.md"])
    _write_skill_no_section(skills_dir / "skill-b.md")
    errors, warnings = vec.run_checks(skills_dir, examples_dir, cross_ref)
    assert any("missing.md" in e for e in errors)
    assert any("skill-b.md" in w for w in warnings)
