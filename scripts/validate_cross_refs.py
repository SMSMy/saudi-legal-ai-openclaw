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


def _extract_source_paths(text: str) -> set:
    """Return all sources/*.md paths mentioned in text, excluding EXCLUDED_SOURCES."""
    found = set(re.findall(r"sources/[\w-]+\.md", text))
    return found - EXCLUDED_SOURCES


def _extract_skill_paths(text: str) -> set:
    """Return all skills/*.md paths mentioned in text."""
    return set(re.findall(r"skills/[\w-]+\.md", text))


def parse_skill(path: Path) -> set:
    """Return sources/*.md paths cited in this skill's regulations section."""
    lines = path.read_text(encoding="utf-8").splitlines()
    section_text = _extract_section(lines, _is_regulations_heading)
    return _extract_source_paths(section_text)


def parse_source(path: Path) -> tuple:
    """Return (has_see_also, set of skills/*.md paths listed in See also)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    section_text = _extract_section(lines, _is_see_also_heading)
    has_see_also = bool(section_text.strip())
    return has_see_also, _extract_skill_paths(section_text)


def run_checks(
    skills_dir: Path = SKILLS_DIR,
    sources_dir: Path = SOURCES_DIR,
    cross_ref_map: Path = CROSS_REF_MAP,
) -> tuple:
    """
    Run all four checks. Returns (errors, warnings).
    errors   → Check 1 / 2 / 3 (CI-blocking)
    warnings → Check 4 (documentation drift, non-blocking)
    """
    errors: list = []
    warnings: list = []

    # Build (source_path → set of citing skill_paths) from all skills
    skill_citations: dict = {}
    for skill_file in sorted(skills_dir.glob("*.md")):
        cited = parse_skill(skill_file)
        skill_path = f"skills/{skill_file.name}"
        for source_path in cited:
            skill_citations.setdefault(source_path, set()).add(skill_path)

    # Parse each cited source's See also
    source_see_also: dict = {}
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

    # Check 3: phantom references (See also lists a skill that doesn't cite it).
    # Scan ALL source files so we catch phantom entries in sources never cited by any skill.
    all_source_see_also: dict = {}
    for source_file in sorted(sources_dir.glob("*.md")):
        source_path_str = f"sources/{source_file.name}"
        if source_path_str in EXCLUDED_SOURCES:
            continue
        _has, listed = parse_source(source_file)
        if listed:
            all_source_see_also[source_path_str] = listed

    for source_path_str, listed_skills in all_source_see_also.items():
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
