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


# ── coverage_status ────────────────────────────────────────────────────────────

def test_coverage_status_missing():
    assert vec.coverage_status(0) == "Missing"

def test_coverage_status_partial():
    assert vec.coverage_status(1) == "Partial"

def test_coverage_status_strong_two():
    assert vec.coverage_status(2) == "Strong"

def test_coverage_status_strong_many():
    assert vec.coverage_status(5) == "Strong"
