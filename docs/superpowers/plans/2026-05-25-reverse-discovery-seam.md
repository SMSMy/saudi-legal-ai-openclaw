# Reverse-Discovery Seam Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a validated reverse-discovery seam so every `sources/` file cited by a skill links back to the skills that use it, enforced by CI.

**Architecture:** A new CI script (`validate_cross_refs.py`) parses each skill's regulations section using alias-based heading detection, then checks that every cited source file has a `## See also` section listing the citing skills. `docs/cross-reference-map.md` gains a Section 1b reverse-index table as the authoritative CI source of truth.

**Tech Stack:** Python 3.11 stdlib only (pathlib, re, sys, argparse) · pytest · GitHub Actions

---

## Pre-work: citation ground truth

Before Task 3, the validator output (Task 2 step 5) reveals the actual citations. The table below is the verified ground truth from auditing all seven skills directly — use it to write the "See also" sections in Tasks 3–7.

| Source file | Cited by skill | Description from §11 |
|---|---|---|
| `sources/civil-transactions-law.md` | `skills/labor-law-analysis.md` | مبادئ العقود التكميلية |
| `sources/civil-transactions-law.md` | `skills/commercial-dispute.md` | العقود والالتزامات — أساس المطالبات |
| `sources/civil-transactions-law.md` | `skills/compliance-check.md` | التزامات تعاقدية تنظيمية |
| `sources/civil-transactions-law.md` | `skills/legal-drafting.md` | الإطار العام للعقود والالتزامات |
| `sources/civil-transactions-law.md` | `skills/arbitration.md` | مبادئ العقود والالتزامات في النزاعات |
| `sources/civil-transactions-law.md` | `skills/real-estate-contracts.md` | مبادئ العقود والالتزامات العامة |
| `sources/labor-law.md` | `skills/labor-law-analysis.md` | الإطار الحاكم الأساسي |
| `sources/labor-law.md` | `skills/compliance-check.md` | السعودة، WPS، GOSI |
| `sources/labor-law.md` | `skills/legal-drafting.md` | عقود العمل — أحكام آمرة |
| `sources/companies-law.md` | `skills/commercial-dispute.md` | نزاعات المساهمين والشركاء |
| `sources/companies-law.md` | `skills/compliance-check.md` | هيكل الملكية ومتطلبات الإفصاح |
| `sources/companies-law.md` | `skills/legal-drafting.md` | وثائق الشركات والمساهمين |
| `sources/companies-law.md` | `skills/real-estate-contracts.md` | عقارات الشركات والتصرف فيها |
| `sources/pdpl.md` | `skills/labor-law-analysis.md` | بنود السرية في عقود العمل |
| `sources/pdpl.md` | `skills/compliance-check.md` | PDPL — نقل البيانات والخصوصية |
| `sources/pdpl.md` | `skills/legal-drafting.md` | بنود السرية ومعالجة البيانات |
| `sources/commercial-courts.md` | `skills/commercial-dispute.md` | الإطار الإجرائي الأساسي |
| `sources/commercial-courts.md` | `skills/compliance-check.md` | فض النزاعات التنظيمية |
| `sources/commercial-courts.md` | `skills/arbitration.md` | الرقابة القضائية على التحكيم وتنفيذ الاحكام |

**Not cited (no See also needed):** `sources/saudi-laws.md` — no skill's §11 references it by path.

**Excluded from validation:** `sources/regulation-index.md` — cited only as a citation-format reference (`EXCLUDED_SOURCES` constant in the script), not as a substantive legal source.

**Note on `skills/contract-review.md`:** Its §11 does not use backtick-quoted `sources/` paths — it lists regulation names only. The validator will not detect any citations from it. This is a documentation gap to address in a follow-on task (not in scope here).

---

## File map

| Action | File | Responsibility |
|---|---|---|
| Create | `scripts/validate_cross_refs.py` | Parse skills + sources, run 4 checks, exit 1 on errors |
| Create | `tests/test_validate_cross_refs.py` | Unit + integration tests for all parsing functions and checks |
| Modify | `sources/civil-transactions-law.md` | Add `## See also` (6 skills) |
| Modify | `sources/labor-law.md` | Add `## See also` (3 skills) |
| Modify | `sources/companies-law.md` | Add `## See also` (4 skills) |
| Modify | `sources/pdpl.md` | Add `## See also` (3 skills) |
| Modify | `sources/commercial-courts.md` | Add `## See also` (3 skills) |
| Modify | `docs/cross-reference-map.md` | Add Section 1b reverse-index table + two maintenance rules |
| Modify | `.github/workflows/validate-datasets.yml` | Add `validate_cross_refs.py` step after pytest |

---

## Task 1: Write the failing tests

**Files:**
- Create: `tests/test_validate_cross_refs.py`

- [ ] **Step 1: Create the test file**

```python
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
    # regulation-index.md is in EXCLUDED_SOURCES — should not appear
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

def _write_skill(path: Path, name: str, sources: list[str]) -> None:
    rows = "\n".join(f"| reg | ref | desc | `{s}` |" for s in sources)
    path.write_text(
        f"## Introduction\nIntro.\n\n"
        f"## 11. Relevant Regulations / الأنظمة ذات الصلة\n"
        f"{rows}\n"
        f"راجع `sources/regulation-index.md` للصيغ الرسمية.\n\n"
        f"## 12. Next\nOther.\n",
        encoding="utf-8",
    )

def _write_source_with_see_also(path: Path, skills: list[str]) -> None:
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
    # See also exists but is missing compliance-check.md
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

    # skill does NOT cite sources/labor-law.md
    _write_skill(skills_dir / "legal-drafting.md", "legal-drafting", ["sources/pdpl.md"])
    (sources_dir / "pdpl.md").write_text("## Overview\n", encoding="utf-8")
    # but labor-law.md See also lists legal-drafting.md — phantom
    _write_source_with_see_also(sources_dir / "labor-law.md", ["legal-drafting.md"])

    errors, _ = vcr.run_checks(skills_dir, sources_dir, cross_ref)
    assert any("phantom" in e.lower() or "does not cite" in e for e in errors)


def test_run_checks_check4_map_missing_row_is_warning(tmp_path):
    skills_dir = tmp_path / "skills"
    sources_dir = tmp_path / "sources"
    skills_dir.mkdir()
    sources_dir.mkdir()
    cross_ref = tmp_path / "cross-reference-map.md"
    cross_ref.write_text("# Map\nNo rows yet.\n", encoding="utf-8")  # empty map

    _write_skill(skills_dir / "labor-law-analysis.md", "labor-law-analysis", ["sources/labor-law.md"])
    _write_source_with_see_also(sources_dir / "labor-law.md", ["labor-law-analysis.md"])

    errors, warnings = vcr.run_checks(skills_dir, sources_dir, cross_ref)
    assert errors == []
    assert any("cross-reference-map" in w for w in warnings)
```

- [ ] **Step 2: Run tests — confirm all fail with ImportError**

```bash
cd /Users/samialmohaimeed/saudi-legal-ai-framework
pytest tests/test_validate_cross_refs.py -v 2>&1 | head -20
```

Expected output: `ModuleNotFoundError: No module named 'validate_cross_refs'`

---

## Task 2: Implement `validate_cross_refs.py`

**Files:**
- Create: `scripts/validate_cross_refs.py`

- [ ] **Step 1: Create the script**

```python
#!/usr/bin/env python3
"""
validate_cross_refs.py
Saudi Legal AI Framework — reverse-discovery seam validator

Checks that every sources/ file cited in a skill's regulations section
has a matching ## See also section listing that skill.

Usage:
    python scripts/validate_cross_refs.py          # validate
    python scripts/validate_cross_refs.py --fix    # auto-fix (not yet implemented)

Exit codes: 0 = pass, 1 = errors found
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
SOURCES_DIR = REPO_ROOT / "sources"
CROSS_REF_MAP = REPO_ROOT / "docs" / "cross-reference-map.md"

# Heading aliases for the regulations section — add future aliases here.
# Matching is case-insensitive and strips leading #, digits, §, and whitespace.
REGULATIONS_HEADING_ALIASES = [
    "relevant regulations",
    "الأنظمة المرتبطة",
    "الأنظمة ذات الصلة",
]

# Heading aliases for the See also section.
SEE_ALSO_HEADING_ALIASES = [
    "see also",
    "انظر أيضًا",
]

# Sources excluded from validation — meta-documents that are not substantive
# legal sources (cited only as format/citation references).
EXCLUDED_SOURCES = {
    "sources/regulation-index.md",
}


def _normalize_heading(line: str) -> str:
    """Strip leading #, section numbers (11., §11), and lowercase."""
    text = re.sub(r"^#+\s*", "", line)
    text = re.sub(r"^\d+\.\s*", "", text)
    text = re.sub(r"§\d+\s*", "", text)
    return text.strip().lower()


def _is_regulations_heading(line: str) -> bool:
    normalized = _normalize_heading(line)
    return any(alias in normalized for alias in REGULATIONS_HEADING_ALIASES)


def _is_see_also_heading(line: str) -> bool:
    normalized = _normalize_heading(line)
    return any(alias in normalized for alias in SEE_ALSO_HEADING_ALIASES)


def _heading_level(line: str) -> int:
    m = re.match(r"^(#+)", line)
    return len(m.group(1)) if m else 0


def _extract_section(lines: list[str], heading_predicate) -> str:
    """Return the text body of the first section matching heading_predicate."""
    in_section = False
    section_level = 0
    body: list[str] = []
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


def _extract_source_paths(text: str) -> set[str]:
    """Return all sources/*.md paths mentioned in text, excluding EXCLUDED_SOURCES."""
    found = set(re.findall(r"sources/[\w-]+\.md", text))
    return found - EXCLUDED_SOURCES


def _extract_skill_paths(text: str) -> set[str]:
    """Return all skills/*.md paths mentioned in text."""
    return set(re.findall(r"skills/[\w-]+\.md", text))


def parse_skill(path: Path) -> set[str]:
    """Return sources/*.md paths cited in this skill's regulations section."""
    lines = path.read_text(encoding="utf-8").splitlines()
    section_text = _extract_section(lines, _is_regulations_heading)
    return _extract_source_paths(section_text)


def parse_source(path: Path) -> tuple[bool, set[str]]:
    """Return (has_see_also, set of skills/*.md paths listed in See also)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    section_text = _extract_section(lines, _is_see_also_heading)
    has_see_also = bool(section_text.strip())
    return has_see_also, _extract_skill_paths(section_text)


def run_checks(
    skills_dir: Path = SKILLS_DIR,
    sources_dir: Path = SOURCES_DIR,
    cross_ref_map: Path = CROSS_REF_MAP,
) -> tuple[list[str], list[str]]:
    """
    Run all four checks. Returns (errors, warnings).
    errors  → Check 1 / 2 / 3 (CI-blocking)
    warnings → Check 4 (documentation drift, non-blocking)
    """
    errors: list[str] = []
    warnings: list[str] = []

    # Build (source_path → set of citing skill_paths) from all skills
    skill_citations: dict[str, set[str]] = {}
    for skill_file in sorted(skills_dir.glob("*.md")):
        cited = parse_skill(skill_file)
        skill_path = f"skills/{skill_file.name}"
        for source_path in cited:
            skill_citations.setdefault(source_path, set()).add(skill_path)

    # Parse each cited source's See also
    source_see_also: dict[str, set[str]] = {}
    for source_path_str, citing_skills in skill_citations.items():
        source_file = sources_dir / Path(source_path_str).name
        if not source_file.exists():
            errors.append(
                f"ERROR: {source_path_str} is referenced in skills but file not found."
            )
            continue

        has_see_also, listed_skills = parse_source(source_file)
        source_see_also[source_path_str] = listed_skills

        # Check 1: cited source has no See also section
        if not has_see_also:
            for skill in sorted(citing_skills):
                errors.append(
                    f"ERROR: {source_path_str} is cited by {skill} "
                    f"(regulations section) but has no '## See also' section."
                )
            continue

        # Check 2: See also is missing a citing skill
        for skill in sorted(citing_skills):
            if skill not in listed_skills:
                errors.append(
                    f"ERROR: {source_path_str} 'See also' is missing {skill} "
                    f"(cited in its regulations section)."
                )

    # Check 3: phantom references (See also lists a skill that doesn't cite it)
    for source_path_str, listed_skills in source_see_also.items():
        citing_skills = skill_citations.get(source_path_str, set())
        for skill in sorted(listed_skills):
            if skill not in citing_skills:
                errors.append(
                    f"ERROR: {source_path_str} 'See also' lists {skill} "
                    f"but {skill} regulations section does not cite {source_path_str}."
                )

    # Check 4: cross-reference-map.md Section 1b sync (warn only)
    map_text = cross_ref_map.read_text(encoding="utf-8") if cross_ref_map.exists() else ""
    for source_path_str, citing_skills in skill_citations.items():
        for skill in sorted(citing_skills):
            if source_path_str not in map_text or skill not in map_text:
                warnings.append(
                    f"WARNING: cross-reference-map.md Section 1b may be missing row: "
                    f"{source_path_str} → {skill}"
                )

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate reverse-discovery seam in sources/ and skills/."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix missing See also sections (not yet implemented).",
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
        print("✓ All cross-reference checks passed.")
    elif not errors:
        print("✓ No errors. See warnings above.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run tests — confirm they pass**

```bash
pytest tests/test_validate_cross_refs.py -v
```

Expected: all tests PASS.

- [ ] **Step 3: Run validator to see current errors (audit)**

```bash
python scripts/validate_cross_refs.py
```

Expected output (before any See also sections exist):

```
WARNING: cross-reference-map.md Section 1b may be missing row: ...
ERROR: sources/civil-transactions-law.md is cited by skills/arbitration.md ... but has no '## See also' section.
ERROR: sources/civil-transactions-law.md is cited by skills/commercial-dispute.md ... but has no '## See also' section.
... (19 errors total, one per pair in the pre-work table)
```

Exit code: 1

- [ ] **Step 4: Commit**

```bash
git add scripts/validate_cross_refs.py tests/test_validate_cross_refs.py
git commit -m "feat: add validate_cross_refs.py with full test suite"
```

---

## Task 3: Add `## See also` to `sources/civil-transactions-law.md`

**Files:**
- Modify: `sources/civil-transactions-law.md`

- [ ] **Step 1: Append the See also section**

Add this block at the very end of `sources/civil-transactions-law.md` (after the last `<!-- TODO -->` comment):

```markdown

---

## See also / انظر أيضًا

المهارات التي تستند إلى هذا المصدر / Skills that cite this source:

| Skill | Section | طبيعة الاستخدام |
|-------|---------|----------------|
| [skills/labor-law-analysis.md](../skills/labor-law-analysis.md) | §11 الأنظمة ذات الصلة | مبادئ العقود التكميلية |
| [skills/commercial-dispute.md](../skills/commercial-dispute.md) | §11 الأنظمة ذات الصلة | العقود والالتزامات — أساس المطالبات |
| [skills/compliance-check.md](../skills/compliance-check.md) | §11 الأنظمة ذات الصلة | التزامات تعاقدية تنظيمية |
| [skills/legal-drafting.md](../skills/legal-drafting.md) | §11 الأنظمة ذات الصلة | الإطار العام للعقود والالتزامات |
| [skills/arbitration.md](../skills/arbitration.md) | §11 الأنظمة ذات الصلة | مبادئ العقود والالتزامات في النزاعات |
| [skills/real-estate-contracts.md](../skills/real-estate-contracts.md) | §11 الأنظمة ذات الصلة | مبادئ العقود والالتزامات العامة |

> للاطلاع على الفهرس الكامل: [`docs/cross-reference-map.md`](../docs/cross-reference-map.md)
```

- [ ] **Step 2: Run validator — civil-transactions errors should clear**

```bash
python scripts/validate_cross_refs.py 2>&1 | grep "civil-transactions"
```

Expected: no output (no errors for this file).

- [ ] **Step 3: Commit**

```bash
git add sources/civil-transactions-law.md
git commit -m "docs: add See also section to civil-transactions-law.md"
```

---

## Task 4: Add `## See also` to `sources/labor-law.md`

**Files:**
- Modify: `sources/labor-law.md`

- [ ] **Step 1: Append the See also section**

Add at the very end of `sources/labor-law.md`:

```markdown

---

## See also / انظر أيضًا

المهارات التي تستند إلى هذا المصدر / Skills that cite this source:

| Skill | Section | طبيعة الاستخدام |
|-------|---------|----------------|
| [skills/labor-law-analysis.md](../skills/labor-law-analysis.md) | §11 الأنظمة ذات الصلة | الإطار الحاكم الأساسي |
| [skills/compliance-check.md](../skills/compliance-check.md) | §11 الأنظمة ذات الصلة | السعودة، WPS، GOSI |
| [skills/legal-drafting.md](../skills/legal-drafting.md) | §11 الأنظمة ذات الصلة | عقود العمل — أحكام آمرة |

> للاطلاع على الفهرس الكامل: [`docs/cross-reference-map.md`](../docs/cross-reference-map.md)
```

- [ ] **Step 2: Run validator — labor-law errors should clear**

```bash
python scripts/validate_cross_refs.py 2>&1 | grep "labor-law"
```

Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add sources/labor-law.md
git commit -m "docs: add See also section to labor-law.md"
```

---

## Task 5: Add `## See also` to `sources/companies-law.md`

**Files:**
- Modify: `sources/companies-law.md`

- [ ] **Step 1: Append the See also section**

Add at the very end of `sources/companies-law.md`:

```markdown

---

## See also / انظر أيضًا

المهارات التي تستند إلى هذا المصدر / Skills that cite this source:

| Skill | Section | طبيعة الاستخدام |
|-------|---------|----------------|
| [skills/commercial-dispute.md](../skills/commercial-dispute.md) | §11 الأنظمة ذات الصلة | نزاعات المساهمين والشركاء |
| [skills/compliance-check.md](../skills/compliance-check.md) | §11 الأنظمة ذات الصلة | هيكل الملكية ومتطلبات الإفصاح |
| [skills/legal-drafting.md](../skills/legal-drafting.md) | §11 الأنظمة ذات الصلة | وثائق الشركات والمساهمين |
| [skills/real-estate-contracts.md](../skills/real-estate-contracts.md) | §11 الأنظمة ذات الصلة | عقارات الشركات والتصرف فيها |

> للاطلاع على الفهرس الكامل: [`docs/cross-reference-map.md`](../docs/cross-reference-map.md)
```

- [ ] **Step 2: Run validator — companies-law errors should clear**

```bash
python scripts/validate_cross_refs.py 2>&1 | grep "companies-law"
```

Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add sources/companies-law.md
git commit -m "docs: add See also section to companies-law.md"
```

---

## Task 6: Add `## See also` to `sources/pdpl.md`

**Files:**
- Modify: `sources/pdpl.md`

- [ ] **Step 1: Append the See also section**

Add at the very end of `sources/pdpl.md`:

```markdown

---

## See also / انظر أيضًا

المهارات التي تستند إلى هذا المصدر / Skills that cite this source:

| Skill | Section | طبيعة الاستخدام |
|-------|---------|----------------|
| [skills/labor-law-analysis.md](../skills/labor-law-analysis.md) | §11 الأنظمة ذات الصلة | بنود السرية في عقود العمل |
| [skills/compliance-check.md](../skills/compliance-check.md) | §11 الأنظمة ذات الصلة | PDPL — نقل البيانات والخصوصية |
| [skills/legal-drafting.md](../skills/legal-drafting.md) | §11 الأنظمة ذات الصلة | بنود السرية ومعالجة البيانات |

> للاطلاع على الفهرس الكامل: [`docs/cross-reference-map.md`](../docs/cross-reference-map.md)
```

- [ ] **Step 2: Run validator — pdpl errors should clear**

```bash
python scripts/validate_cross_refs.py 2>&1 | grep "pdpl"
```

Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add sources/pdpl.md
git commit -m "docs: add See also section to pdpl.md"
```

---

## Task 7: Add `## See also` to `sources/commercial-courts.md`

**Files:**
- Modify: `sources/commercial-courts.md`

- [ ] **Step 1: Append the See also section**

Add at the very end of `sources/commercial-courts.md`:

```markdown

---

## See also / انظر أيضًا

المهارات التي تستند إلى هذا المصدر / Skills that cite this source:

| Skill | Section | طبيعة الاستخدام |
|-------|---------|----------------|
| [skills/commercial-dispute.md](../skills/commercial-dispute.md) | §11 الأنظمة ذات الصلة | الإطار الإجرائي الأساسي |
| [skills/compliance-check.md](../skills/compliance-check.md) | §11 الأنظمة ذات الصلة | فض النزاعات التنظيمية |
| [skills/arbitration.md](../skills/arbitration.md) | §11 الأنظمة ذات الصلة | الرقابة القضائية على التحكيم وتنفيذ الاحكام |

> للاطلاع على الفهرس الكامل: [`docs/cross-reference-map.md`](../docs/cross-reference-map.md)
```

- [ ] **Step 2: Run validator — should show only Check 4 warnings now**

```bash
python scripts/validate_cross_refs.py
```

Expected: zero ERRORs, only WARNING lines about cross-reference-map.md Section 1b. Exit code: 0.

- [ ] **Step 3: Commit**

```bash
git add sources/commercial-courts.md
git commit -m "docs: add See also section to commercial-courts.md"
```

---

## Task 8: Add Section 1b to `docs/cross-reference-map.md`

**Files:**
- Modify: `docs/cross-reference-map.md`

- [ ] **Step 1: Insert Section 1b after Section 1**

In `docs/cross-reference-map.md`, find the line:

```
---

## 2. Skills ← → Prompts / المهارات ← → قوالب المطالبات
```

Insert this block immediately before it:

```markdown
---

## 1b. Sources → Skills — Reverse Index / المصادر → المهارات (فهرس عكسي)

> هذا الجدول مصدر الحقيقة للـ CI — يُشغِّل `scripts/validate_cross_refs.py` في كل push.
> أي تغيير في §11 لأي skill يستلزم تحديث هذا الجدول.
> This table is the CI source of truth. Any change to a skill's §11 requires updating it.

| Source File | Cited by Skill | Section | طبيعة الاستخدام |
|---|---|---|---|
| `sources/civil-transactions-law.md` | `skills/labor-law-analysis.md` | §11 | مبادئ العقود التكميلية |
| `sources/civil-transactions-law.md` | `skills/commercial-dispute.md` | §11 | العقود والالتزامات — أساس المطالبات |
| `sources/civil-transactions-law.md` | `skills/compliance-check.md` | §11 | التزامات تعاقدية تنظيمية |
| `sources/civil-transactions-law.md` | `skills/legal-drafting.md` | §11 | الإطار العام للعقود والالتزامات |
| `sources/civil-transactions-law.md` | `skills/arbitration.md` | §11 | مبادئ العقود والالتزامات في النزاعات |
| `sources/civil-transactions-law.md` | `skills/real-estate-contracts.md` | §11 | مبادئ العقود والالتزامات العامة |
| `sources/labor-law.md` | `skills/labor-law-analysis.md` | §11 | الإطار الحاكم الأساسي |
| `sources/labor-law.md` | `skills/compliance-check.md` | §11 | السعودة، WPS، GOSI |
| `sources/labor-law.md` | `skills/legal-drafting.md` | §11 | عقود العمل — أحكام آمرة |
| `sources/companies-law.md` | `skills/commercial-dispute.md` | §11 | نزاعات المساهمين والشركاء |
| `sources/companies-law.md` | `skills/compliance-check.md` | §11 | هيكل الملكية ومتطلبات الإفصاح |
| `sources/companies-law.md` | `skills/legal-drafting.md` | §11 | وثائق الشركات والمساهمين |
| `sources/companies-law.md` | `skills/real-estate-contracts.md` | §11 | عقارات الشركات والتصرف فيها |
| `sources/pdpl.md` | `skills/labor-law-analysis.md` | §11 | بنود السرية في عقود العمل |
| `sources/pdpl.md` | `skills/compliance-check.md` | §11 | PDPL — نقل البيانات والخصوصية |
| `sources/pdpl.md` | `skills/legal-drafting.md` | §11 | بنود السرية ومعالجة البيانات |
| `sources/commercial-courts.md` | `skills/commercial-dispute.md` | §11 | الإطار الإجرائي الأساسي |
| `sources/commercial-courts.md` | `skills/compliance-check.md` | §11 | فض النزاعات التنظيمية |
| `sources/commercial-courts.md` | `skills/arbitration.md` | §11 | الرقابة القضائية على التحكيم وتنفيذ الاحكام |

```

- [ ] **Step 2: Add "When editing a skill's §11" maintenance rule**

In the maintenance rules section (after "When Adding a New Source"), add:

```markdown
### عند تعديل §11 في Skill / When Editing a Skill's §11

```
✅ حدّث Section 1b في:           docs/cross-reference-map.md
✅ حدّث "See also" في:           كل sources/ file أُضيف أو حُذف من §11
✅ شغّل محليًا:                  python scripts/validate_cross_refs.py
✅ تأكد من خروج 0 قبل الـ commit
```
```

- [ ] **Step 3: Update the last-updated timestamp** (bottom of the file)

Change:
```
*آخر تحديث / Last updated: 2026-05-17 — يعكس حالة المشروع في v0.3 ...*
```
To:
```
*آخر تحديث / Last updated: 2026-05-25 — إضافة Section 1b (reverse index) + validate_cross_refs.py*
```

- [ ] **Step 4: Run validator — confirm zero errors and zero warnings**

```bash
python scripts/validate_cross_refs.py
```

Expected:
```
✓ All cross-reference checks passed.
```

Exit code: 0.

- [ ] **Step 5: Commit**

```bash
git add docs/cross-reference-map.md
git commit -m "docs: add Section 1b reverse index to cross-reference-map.md"
```

---

## Task 9: Wire into CI

**Files:**
- Modify: `.github/workflows/validate-datasets.yml`

- [ ] **Step 1: Add the validation step**

In `.github/workflows/validate-datasets.yml`, after the `Run tests` step (pytest), add:

```yaml
      - name: Validate cross-references
        run: python scripts/validate_cross_refs.py
```

The full jobs section should read:

```yaml
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6

      - name: Set up Python 3.11
        uses: actions/setup-python@v6
        with:
          python-version: "3.11"

      - name: Install dev dependencies
        run: pip install -r requirements-dev.txt

      - name: Run tests
        run: pytest

      - name: Validate cross-references
        run: python scripts/validate_cross_refs.py

      - name: Validate main dataset
        run: python3 scripts/validate_dataset.py
      # ... rest unchanged
```

- [ ] **Step 2: Run the full local test suite to confirm nothing breaks**

```bash
pytest && python scripts/validate_cross_refs.py
```

Expected: pytest passes, validator exits 0 with `✓ All cross-reference checks passed.`

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/validate-datasets.yml
git commit -m "ci: add validate_cross_refs.py step to validation workflow"
```

---

## Self-review notes

- `contract-review.md §11` uses regulation names only (no `sources/` paths) — the validator will not detect its citations. This is a documentation gap flagged in the pre-work section; resolving it requires adding backtick-quoted source paths to that skill's §11 (out of scope here).
- `sources/saudi-laws.md` has no citations from any skill's §11 by path — no See also needed, confirmed by validator output in Task 2 step 3.
- `sources/regulation-index.md` is excluded via `EXCLUDED_SOURCES` — it appears as a citation format reference in every skill's regulations section but is not a substantive legal source.
- Check 4 warnings (map sync) are non-blocking — they clear only in Task 8 when Section 1b is added.
