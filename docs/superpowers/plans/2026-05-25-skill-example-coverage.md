# Skill → Example Coverage System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bidirectional skill → example coverage system so contributors and AI agents can instantly discover which skills have worked examples, which have none, and which examples demonstrate each skill.

**Architecture:** A new validator (`scripts/validate_example_coverage.py`) parses `## Related examples` sections in every `skills/*.md` file using alias-based heading detection, verifies referenced example files exist, and produces coverage counts. A new table in `docs/cross-reference-map.md` gives the human-readable overview. CI blocks on broken paths and malformed sections; missing coverage is a non-blocking warning.

**Tech Stack:** Python 3.11, pytest, pathlib, re (stdlib only — no new dependencies)

---

## Architecture: Invariants

Before touching code, lock in these rules. Violation = test failure or CI error.

1. **Forward link:** Every `skills/*.md` MUST eventually have a `## Related examples` section (enforced as warning today, error in future).
2. **Path integrity:** Every `examples/` path listed in a `## Related examples` section MUST exist on disk. This is CI-blocking from day one.
3. **Format integrity:** Every bullet item in a `## Related examples` section MUST contain a markdown link whose href resolves to `examples/*.md`. A bullet with no link is CI-blocking.
4. **Section heading aliases:** Detection is alias-based, case-insensitive, strips `#`, digits, and `§` — never hardcoded to a section number.
5. **Coverage table:** `docs/cross-reference-map.md §Skill → Example Coverage` is the authoritative human-readable index but is NOT CI source-of-truth. Divergence → warning only.

## Architecture: Coverage Heuristics

- `count == 0` → **Missing** (WARNING — non-blocking)
- `count == 1` → **Partial** (OK)
- `count >= 2` → **Strong** (OK)

## Architecture: Failure/Warning Rules

| Check | Condition | Severity |
|---|---|---|
| 1 | Bullet item in Related examples has no `[text](examples/…)` link | **ERROR** — CI-blocking |
| 2 | Referenced example path does not exist on disk | **ERROR** — CI-blocking |
| 3 | Skill has no `## Related examples` heading | **WARNING** — non-blocking |
| 4 | Skill has 0 valid examples listed | **WARNING** — non-blocking |
| 5 | Coverage table in cross-reference-map.md missing a row | **WARNING** — non-blocking |

## File Map

| Action | File | Responsibility |
|---|---|---|
| **Create** | `scripts/validate_example_coverage.py` | Core validator: heading detection, link extraction, malformation checks, `run_checks`, `main` |
| **Create** | `tests/test_validate_example_coverage.py` | Unit + integration tests for the validator |
| **Modify** | `skills/arbitration.md` | Append `## Related examples` section |
| **Modify** | `skills/commercial-dispute.md` | Append `## Related examples` section |
| **Modify** | `skills/compliance-check.md` | Append `## Related examples` section |
| **Modify** | `skills/contract-review.md` | Append `## Related examples` section |
| **Modify** | `skills/labor-law-analysis.md` | Append `## Related examples` section |
| **Modify** | `skills/legal-drafting.md` | Append `## Related examples` section |
| **Modify** | `skills/real-estate-contracts.md` | Append `## Related examples` section |
| **Modify** | `docs/cross-reference-map.md` | Add `## Skill → Example Coverage` section; fix stale §3 entries |
| **Modify** | `.github/workflows/validate-datasets.yml` | Add `validate_example_coverage.py` step after `validate_cross_refs.py` |

## Confirmed Skill → Example Mappings

Derived by grepping `skills/` references inside each `examples/*.md` file and cross-checking `docs/cross-reference-map.md §3`:

| Skill | Examples | Coverage |
|---|---|---|
| `skills/arbitration.md` | `examples/arbitration-example.md` | Partial |
| `skills/commercial-dispute.md` | `examples/commercial-dispute-example.md` | Partial |
| `skills/compliance-check.md` | `examples/compliance-example.md` · `examples/pdpl-data-breach-example.md` | Strong |
| `skills/contract-review.md` | `examples/contract-review-example.md` · `examples/employment-contract-review.md` · `examples/nda-review.md` · `examples/saudi-contract-review-demo.md` | Strong |
| `skills/labor-law-analysis.md` | `examples/employment-contract-review.md` · `examples/labor-dispute-job-change-example.md` · `examples/labor-law-example.md` | Strong |
| `skills/legal-drafting.md` | `examples/legal-drafting-example.md` | Partial |
| `skills/real-estate-contracts.md` | `examples/commercial-lease-exit-example.md` · `examples/real-estate-example.md` | Strong |

---

## Task 1: Core Functions + Unit Tests (TDD — write tests first)

**Files:**
- Create: `scripts/validate_example_coverage.py`
- Create: `tests/test_validate_example_coverage.py`

- [ ] **Step 1.1: Write the failing unit tests**

Create `tests/test_validate_example_coverage.py` with this exact content:

```python
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
```

- [ ] **Step 1.2: Run tests to confirm they fail**

```bash
pytest tests/test_validate_example_coverage.py -v
```

Expected: `ImportError: No module named 'validate_example_coverage'` (all tests fail to import)

- [ ] **Step 1.3: Create the script with all core functions**

Create `scripts/validate_example_coverage.py` with this content (stop before `run_checks` and `main` — those come in Task 2):

```python
#!/usr/bin/env python3
"""
validate_example_coverage.py
Saudi Legal AI Framework — skill → example coverage validator

Checks that every skills/*.md file has a ## Related examples section and that
all referenced example files exist on disk.

Usage:
    python scripts/validate_example_coverage.py          # validate
    python scripts/validate_example_coverage.py --fix    # auto-fix (not yet implemented)

Exit codes: 0 = pass, 1 = errors found
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
EXAMPLES_DIR = REPO_ROOT / "examples"
CROSS_REF_MAP = REPO_ROOT / "docs" / "cross-reference-map.md"

# Heading aliases — add future multilingual aliases here.
# Matching is case-insensitive and strips leading #, digits, §, and whitespace.
RELATED_EXAMPLES_HEADING_ALIASES = [
    "related examples",
    "أمثلة مرتبطة",
]

COVERAGE_STRONG = 2
COVERAGE_PARTIAL = 1


def _normalize_heading(line: str) -> str:
    """Strip leading #, section numbers (11., §11), and lowercase."""
    text = re.sub(r"^#+\s*", "", line)
    text = re.sub(r"^\d+\.\s*", "", text)
    text = re.sub(r"§\d+\s*", "", text)
    return text.strip().lower()


def _is_related_examples_heading(line: str) -> bool:
    normalized = _normalize_heading(line)
    return any(alias in normalized for alias in RELATED_EXAMPLES_HEADING_ALIASES)


def _heading_level(line: str) -> int:
    m = re.match(r"^(#+)", line)
    return len(m.group(1)) if m else 0


def _extract_section(lines: list, heading_predicate) -> str:
    """Return the text body of the first section matching heading_predicate."""
    in_section = False
    section_level = 0
    body: list = []
    for line in lines:
        if not in_section:
            if line.startswith("#") and heading_predicate(line):
                in_section = True
                section_level = _heading_level(line)
        else:
            lvl = _heading_level(line)
            if line.startswith("#") and lvl <= section_level:
                break
            body.append(line)
    return "\n".join(body)


def _has_section_heading(lines: list, heading_predicate) -> bool:
    """Return True if any line is a heading matching heading_predicate."""
    return any(
        line.startswith("#") and heading_predicate(line)
        for line in lines
    )


def _extract_example_paths(section_text: str) -> list:
    """
    Return list of example path strings (relative to repo root, e.g. 'examples/foo.md')
    from markdown links in the section. Accepts both '../examples/foo.md' and
    'examples/foo.md' forms.
    """
    paths = []
    for m in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", section_text):
        raw_path = m.group(2)
        normalized = re.sub(r"^\.\./", "", raw_path)
        if normalized.startswith("examples/"):
            paths.append(normalized)
    return paths


def _find_malformed_items(section_text: str) -> list:
    """
    Return list of bullet items (lines starting with * or -) that contain no
    markdown link whose path resolves to examples/. These are structurally
    malformed entries that should be fixed.
    """
    malformed = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith(("*", "-")):
            continue
        has_example_link = bool(
            re.search(r"\[([^\]]*)\]\(\.\./examples/[\w.-]+\)", stripped)
            or re.search(r"\[([^\]]*)\]\(examples/[\w.-]+\)", stripped)
        )
        if not has_example_link:
            malformed.append(stripped)
    return malformed


def parse_skill(path: Path) -> tuple:
    """
    Parse a skill file for its Related examples section.

    Returns (has_section, example_paths, malformed_items):
    - has_section: True if a ## Related examples heading was found
    - example_paths: list of normalized paths like 'examples/foo.md'
    - malformed_items: bullet items without a valid examples/ link
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    has_section = _has_section_heading(lines, _is_related_examples_heading)
    if not has_section:
        return False, [], []
    section_text = _extract_section(lines, _is_related_examples_heading)
    return True, _extract_example_paths(section_text), _find_malformed_items(section_text)


def coverage_status(count: int) -> str:
    """Return 'Strong', 'Partial', or 'Missing' based on example count."""
    if count >= COVERAGE_STRONG:
        return "Strong"
    if count == COVERAGE_PARTIAL:
        return "Partial"
    return "Missing"
```

- [ ] **Step 1.4: Run unit tests — expect them to pass**

```bash
pytest tests/test_validate_example_coverage.py -v -k "not run_checks"
```

Expected: all unit tests PASS (the `run_checks` integration tests will fail — that's fine, they're excluded)

- [ ] **Step 1.5: Commit**

```bash
git add scripts/validate_example_coverage.py tests/test_validate_example_coverage.py
git commit -m "feat: add validate_example_coverage.py core functions and unit tests"
```

---

## Task 2: `run_checks`, `main`, and Integration Tests

**Files:**
- Modify: `scripts/validate_example_coverage.py` (append `run_checks` and `main`)
- Modify: `tests/test_validate_example_coverage.py` (append integration tests — already written in Task 1)

- [ ] **Step 2.1: Run the integration tests to confirm they fail**

```bash
pytest tests/test_validate_example_coverage.py -v -k "run_checks"
```

Expected: `AttributeError: module 'validate_example_coverage' has no attribute 'run_checks'`

- [ ] **Step 2.2: Append `run_checks` and `main` to the script**

Append this to the end of `scripts/validate_example_coverage.py`:

```python

def run_checks(
    skills_dir: Path = SKILLS_DIR,
    examples_dir: Path = EXAMPLES_DIR,
    cross_ref_map: Path = CROSS_REF_MAP,
) -> tuple:
    """
    Run all checks. Returns (errors, warnings).
    errors   → CI-blocking (broken paths, malformed sections)
    warnings → non-blocking (missing sections, zero coverage, map drift)

    Check 1: Malformed bullet item in Related examples section
    Check 2: Referenced example file does not exist on disk
    Check 3: Skill has no ## Related examples section
    Check 4: Skill has 0 valid examples listed
    Check 5: cross-reference-map.md coverage table missing a row for this skill
    """
    errors: list = []
    warnings: list = []

    for d in (skills_dir, examples_dir):
        if not d.exists():
            errors.append(f"ERROR: required directory not found: {d}")
    if errors:
        return errors, warnings

    map_text = cross_ref_map.read_text(encoding="utf-8") if cross_ref_map.exists() else ""

    for skill_file in sorted(skills_dir.glob("*.md")):
        skill_path = f"skills/{skill_file.name}"
        has_section, example_paths, malformed = parse_skill(skill_file)

        # Check 3: No section at all
        if not has_section:
            warnings.append(
                f"WARNING: {skill_path} has no '## Related examples' section."
            )
            continue

        # Check 1: Malformed items
        for item in malformed:
            errors.append(
                f"ERROR: {skill_path} 'Related examples': malformed list item: {item!r}"
            )

        # Check 2: Broken paths
        for ex_path in example_paths:
            if not (examples_dir.parent / ex_path).exists():
                errors.append(
                    f"ERROR: {skill_path} references {ex_path} but file not found."
                )

        # Check 4: Zero coverage (section present but lists nothing valid)
        valid_paths = [p for p in example_paths if (examples_dir.parent / p).exists()]
        if len(valid_paths) == 0:
            warnings.append(
                f"WARNING: {skill_path} 'Related examples' lists 0 valid examples."
            )

        # Check 5: Map drift
        row_present = (skill_path in map_text) and ("Example Coverage" in map_text)
        if not row_present:
            warnings.append(
                f"WARNING: cross-reference-map.md 'Skill → Example Coverage' "
                f"may be missing row for {skill_path}."
            )

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate skill→example coverage in skills/."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix missing Related examples sections (not yet implemented).",
    )
    args = parser.parse_args()

    if args.fix:
        print("--fix mode is not yet implemented.")
        sys.exit(0)

    errors, warnings = run_checks()

    for w in warnings:
        print(w)
    for e in errors:
        print(e)

    if not errors and not warnings:
        print("✓ All example coverage checks passed.")
    elif not errors:
        print("✓ No errors. See warnings above.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2.3: Append the integration tests to the test file**

Append this block to the end of `tests/test_validate_example_coverage.py`:

```python

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


def test_run_checks_broken_path_does_not_produce_warning_for_missing_section(tmp_path):
    """Check 2 error does not suppress Check 3 warning for other skills."""
    skills_dir, examples_dir, docs_dir = _make_dirs(tmp_path)
    cross_ref = docs_dir / "cross-reference-map.md"
    cross_ref.write_text("", encoding="utf-8")
    # skill-a has bad path → error
    _write_skill_with_examples(skills_dir / "skill-a.md", ["examples/missing.md"])
    # skill-b has no section → warning
    _write_skill_no_section(skills_dir / "skill-b.md")
    errors, warnings = vec.run_checks(skills_dir, examples_dir, cross_ref)
    assert any("missing.md" in e for e in errors)
    assert any("skill-b.md" in w for w in warnings)
```

- [ ] **Step 2.4: Run all tests**

```bash
pytest tests/test_validate_example_coverage.py -v
```

Expected: all tests PASS

- [ ] **Step 2.5: Run the script manually against the real repo (expect warnings — no errors)**

```bash
python3 scripts/validate_example_coverage.py
```

Expected output (warnings only, no errors, exit code 0):
```
WARNING: skills/arbitration.md has no '## Related examples' section.
WARNING: skills/commercial-dispute.md has no '## Related examples' section.
WARNING: skills/compliance-check.md has no '## Related examples' section.
WARNING: skills/contract-review.md has no '## Related examples' section.
WARNING: skills/labor-law-analysis.md has no '## Related examples' section.
WARNING: skills/legal-drafting.md has no '## Related examples' section.
WARNING: skills/real-estate-contracts.md has no '## Related examples' section.
✓ No errors. See warnings above.
```

Exit code: `0` (warnings are non-blocking; confirm with `echo $?`)

- [ ] **Step 2.6: Commit**

```bash
git add scripts/validate_example_coverage.py tests/test_validate_example_coverage.py
git commit -m "feat: add run_checks and integration tests for validate_example_coverage"
```

---

## Task 3: Add `## Related examples` Sections to All 7 Skill Files

**Files:** Modify all 7 files under `skills/` — append a new section at the end of each.

The canonical format (per spec) is:
```
* [examples/filename.md](../examples/filename.md) — one-line scenario description
```

- [ ] **Step 3.1: Append to `skills/arbitration.md`**

Append this exact block at the very end of the file (after the last line of §14):

```markdown

---

## Related examples / أمثلة مرتبطة

* [examples/arbitration-example.md](../examples/arbitration-example.md) — cross-border supply dispute: enforcing a DIAC arbitration clause under Saudi law
```

- [ ] **Step 3.2: Append to `skills/commercial-dispute.md`**

```markdown

---

## Related examples / أمثلة مرتبطة

* [examples/commercial-dispute-example.md](../examples/commercial-dispute-example.md) — commercial dispute analysis under Saudi commercial courts framework
```

- [ ] **Step 3.3: Append to `skills/compliance-check.md`**

```markdown

---

## Related examples / أمثلة مرتبطة

* [examples/compliance-example.md](../examples/compliance-example.md) — SaaS startup compliance assessment (PDPL, Nitaqat, WPS)
* [examples/pdpl-data-breach-example.md](../examples/pdpl-data-breach-example.md) — medical data breach: PDPL notification obligations and response workflow
```

- [ ] **Step 3.4: Append to `skills/contract-review.md`**

```markdown

---

## Related examples / أمثلة مرتبطة

* [examples/contract-review-example.md](../examples/contract-review-example.md) — professional services contract review: foreign governing law clause, interest, IP transfer
* [examples/employment-contract-review.md](../examples/employment-contract-review.md) — employment contract review: Saudi national, full §8 output demonstration
* [examples/nda-review.md](../examples/nda-review.md) — NDA review: confidentiality scope, PDPL alignment, enforceability
* [examples/saudi-contract-review-demo.md](../examples/saudi-contract-review-demo.md) — full 9-section contract review workflow demo (authoritative §8 reference)
```

- [ ] **Step 3.5: Append to `skills/labor-law-analysis.md`**

```markdown

---

## Related examples / أمثلة مرتبطة

* [examples/employment-contract-review.md](../examples/employment-contract-review.md) — employment contract review: mandatory elements check under Saudi Labour Law
* [examples/labor-dispute-job-change-example.md](../examples/labor-dispute-job-change-example.md) — unilateral job title and salary change without employee consent
* [examples/labor-law-example.md](../examples/labor-law-example.md) — EOSB calculation and wrongful termination analysis (7-year employee)
```

- [ ] **Step 3.6: Append to `skills/legal-drafting.md`**

```markdown

---

## Related examples / أمثلة مرتبطة

* [examples/legal-drafting-example.md](../examples/legal-drafting-example.md) — software services contract drafting: milestone-linked payments, IP, PDPL clauses
```

- [ ] **Step 3.7: Append to `skills/real-estate-contracts.md`**

```markdown

---

## Related examples / أمثلة مرتبطة

* [examples/commercial-lease-exit-example.md](../examples/commercial-lease-exit-example.md) — early exit from commercial lease: penalty clause enforceability
* [examples/real-estate-example.md](../examples/real-estate-example.md) — residential lease renewal dispute: Ejar platform registration and rent increase limits
```

- [ ] **Step 3.8: Run the validator — expect warnings only for map drift (no missing-section warnings)**

```bash
python3 scripts/validate_example_coverage.py
```

Expected output (all 7 skills covered, warnings only about missing map rows):
```
WARNING: cross-reference-map.md 'Skill → Example Coverage' may be missing row for skills/arbitration.md.
WARNING: cross-reference-map.md 'Skill → Example Coverage' may be missing row for skills/commercial-dispute.md.
... (one per skill)
✓ No errors. See warnings above.
```

Exit code: `0`

- [ ] **Step 3.9: Commit**

```bash
git add skills/arbitration.md skills/commercial-dispute.md skills/compliance-check.md \
        skills/contract-review.md skills/labor-law-analysis.md \
        skills/legal-drafting.md skills/real-estate-contracts.md
git commit -m "docs: add Related examples sections to all 7 skill files"
```

---

## Task 4: Update `docs/cross-reference-map.md`

**Files:** Modify `docs/cross-reference-map.md`

Two changes:
1. Fix stale §3 (Skills ← → Examples) — it shows `compliance-check.md`, `legal-drafting.md`, and `commercial-dispute.md` as having no examples, which is now wrong.
2. Add new `## Skill → Example Coverage` section between §3 and §4.

- [ ] **Step 4.1: Replace the stale §3 table**

Find this block in `docs/cross-reference-map.md`:

```markdown
## 3. Skills ← → Examples / المهارات ← → الأمثلة التطبيقية

| Skill | Related Examples | ملاحظة |
|---|---|---|
| `skills/contract-review.md` | `examples/employment-contract-review.md` · `examples/nda-review.md` · `examples/saudi-contract-review-demo.md` | الـ demo هو التطبيق الكامل لـ §8 |
| `skills/labor-law-analysis.md` | `examples/employment-contract-review.md` | المثال يُطبِّق تحليل نظام العمل |
| `skills/commercial-dispute.md` | — | لا يوجد مثال تطبيقي بعد |
| `skills/compliance-check.md` | — | لا يوجد مثال تطبيقي بعد |
| `skills/legal-drafting.md` | — | لا يوجد مثال تطبيقي بعد |
```

Replace with:

```markdown
## 3. Skills ← → Examples / المهارات ← → الأمثلة التطبيقية

| Skill | Related Examples | ملاحظة |
|---|---|---|
| `skills/arbitration.md` | `examples/arbitration-example.md` | نزاع توريد عابر للحدود |
| `skills/commercial-dispute.md` | `examples/commercial-dispute-example.md` | تحليل نزاع تجاري |
| `skills/compliance-check.md` | `examples/compliance-example.md` · `examples/pdpl-data-breach-example.md` | فحص امتثال SaaS + اختراق بيانات طبية |
| `skills/contract-review.md` | `examples/contract-review-example.md` · `examples/employment-contract-review.md` · `examples/nda-review.md` · `examples/saudi-contract-review-demo.md` | الـ demo هو التطبيق الكامل لـ §8 |
| `skills/labor-law-analysis.md` | `examples/employment-contract-review.md` · `examples/labor-dispute-job-change-example.md` · `examples/labor-law-example.md` | يتضمن حساب EOSB ونزاع تغيير المسمى |
| `skills/legal-drafting.md` | `examples/legal-drafting-example.md` | صياغة عقد خدمات برمجيات |
| `skills/real-estate-contracts.md` | `examples/commercial-lease-exit-example.md` · `examples/real-estate-example.md` | إيجار تجاري + سكني |
```

- [ ] **Step 4.2: Insert the new `## Skill → Example Coverage` section**

After the `---` separator that follows §3, insert this new section (before the current `## 4. Sources ← → Regulations` heading):

```markdown
## Skill → Example Coverage

> هذا الجدول مُولَّد من `## Related examples` في كل ملف `skills/*.md`.
> يُشغَّل `scripts/validate_example_coverage.py` في كل push للتحقق منه.
> This table is derived from `## Related examples` in each `skills/*.md` file.
> `scripts/validate_example_coverage.py` runs on every push to verify it.

| Skill | Example Count | Example Files | Coverage Status |
|---|---|---|---|
| `skills/arbitration.md` | 1 | `examples/arbitration-example.md` | Partial |
| `skills/commercial-dispute.md` | 1 | `examples/commercial-dispute-example.md` | Partial |
| `skills/compliance-check.md` | 2 | `examples/compliance-example.md` · `examples/pdpl-data-breach-example.md` | Strong |
| `skills/contract-review.md` | 4 | `examples/contract-review-example.md` · `examples/employment-contract-review.md` · `examples/nda-review.md` · `examples/saudi-contract-review-demo.md` | Strong |
| `skills/labor-law-analysis.md` | 3 | `examples/employment-contract-review.md` · `examples/labor-dispute-job-change-example.md` · `examples/labor-law-example.md` | Strong |
| `skills/legal-drafting.md` | 1 | `examples/legal-drafting-example.md` | Partial |
| `skills/real-estate-contracts.md` | 2 | `examples/commercial-lease-exit-example.md` · `examples/real-estate-example.md` | Strong |

**Coverage rules:** 0 examples → Missing | 1 example → Partial | 2+ examples → Strong

---

```

Also update the "Last updated" line at the bottom of the file:
```
*آخر تحديث / Last updated: 2026-05-25 — إضافة § Skill → Example Coverage + تحديث §3 + validate_example_coverage.py*
```

- [ ] **Step 4.3: Run the full validator — expect zero errors and zero warnings**

```bash
python3 scripts/validate_example_coverage.py
```

Expected:
```
✓ All example coverage checks passed.
```

Exit code: `0` (confirm with `echo $?`)

- [ ] **Step 4.4: Run the cross-refs validator — confirm it still passes**

```bash
python3 scripts/validate_cross_refs.py
```

Expected: `✓ All cross-reference checks passed.` or `✓ No errors.`

- [ ] **Step 4.5: Run the full test suite**

```bash
pytest
```

Expected: all tests PASS

- [ ] **Step 4.6: Commit**

```bash
git add docs/cross-reference-map.md
git commit -m "docs: add Skill → Example Coverage section and fix stale §3 in cross-reference-map"
```

---

## Task 5: Wire Validator into CI

**Files:** Modify `.github/workflows/validate-datasets.yml`

- [ ] **Step 5.1: Add the new CI step**

In `.github/workflows/validate-datasets.yml`, find:

```yaml
      - name: Validate cross-references
        run: python3 scripts/validate_cross_refs.py
```

Replace with:

```yaml
      - name: Validate cross-references
        run: python3 scripts/validate_cross_refs.py

      - name: Validate example coverage
        run: python3 scripts/validate_example_coverage.py
```

- [ ] **Step 5.2: Run pytest to confirm the full suite still passes**

```bash
pytest
```

Expected: all tests PASS

- [ ] **Step 5.3: Dry-run both validators**

```bash
python3 scripts/validate_cross_refs.py && python3 scripts/validate_example_coverage.py
```

Expected: both print `✓ ...` and exit 0.

- [ ] **Step 5.4: Commit**

```bash
git add .github/workflows/validate-datasets.yml
git commit -m "ci: add validate_example_coverage.py step after validate_cross_refs.py"
```

---

## Self-Review Checklist

**Spec coverage:**
- [x] §1 — `## Related examples` section added to every skill file (Task 3)
- [x] §2 — `## Skill → Example Coverage` table added to cross-reference-map.md (Task 4)
- [x] §3 — `scripts/validate_example_coverage.py` with all 5 checks (Task 2)
- [x] §4 — `tests/test_validate_example_coverage.py` with unit + integration tests (Tasks 1–2)
- [x] §5 — CI wiring after `validate_cross_refs.py` (Task 5)
- [x] Architecture requirements — alias-based heading detection, same coding style as validate_cross_refs.py, `--fix` stub, future multilingual alias support, no hardcoded section numbers

**Placeholder scan:** No TBD, TODO, or "similar to" references found.

**Type consistency:**
- `parse_skill(path)` → `(bool, list[str], list[str])` — used consistently in Tasks 1 and 2
- `run_checks(skills_dir, examples_dir, cross_ref_map)` → `(list[str], list[str])` — matches test expectations
- `coverage_status(count: int)` → `str` — used only in documentation, not checked by validator (table is maintained manually)

**Rollout sequence:** validator-first → docs-last → CI-last. At no point does CI block on a condition that doesn't yet pass.
