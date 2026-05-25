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
CROSS_REF_MAP = REPO_ROOT / "docs" / "cross-reference-map.md"  # used in run_checks

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
    return list(dict.fromkeys(paths))


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
