"""
test_sources.py — Verify every registered source_id has a readable .md file
that passes validate_before_register().
"""
import pytest
from pathlib import Path
from saudi_legal_mcp.tools.sources import VALID_REGULATIONS, validate_before_register


def test_all_registered_sources_have_files(data_dir: Path):
    """Every entry in VALID_REGULATIONS must have a corresponding .md file."""
    missing = []
    for reg_id in sorted(VALID_REGULATIONS):
        path = data_dir / "sources" / f"{reg_id}.md"
        if not path.exists():
            missing.append(reg_id)
    assert not missing, (
        f"Registered source_ids with no .md file: {missing}\n"
        "Either remove from VALID_REGULATIONS or add the missing file."
    )


def test_no_unregistered_source_files(data_dir: Path):
    """Every .md file in sources/ (direct children) must be registered."""
    source_dir = data_dir / "sources"
    unregistered = []
    for md_file in source_dir.glob("*.md"):
        reg_id = md_file.stem
        if reg_id not in VALID_REGULATIONS:
            unregistered.append(reg_id)
    assert not unregistered, (
        f"Source files with no registration in VALID_REGULATIONS: {unregistered}\n"
        "Either register them or remove the files."
    )


def test_all_source_files_pass_validation(data_dir: Path):
    """Every registered source file must pass validate_before_register()."""
    failures = []
    for reg_id in sorted(VALID_REGULATIONS):
        path = data_dir / "sources" / f"{reg_id}.md"
        if not path.exists():
            continue  # covered by test_all_registered_sources_have_files
        ok, reason = validate_before_register(path)
        if not ok:
            failures.append(f"{reg_id}: {reason}")
    assert not failures, (
        "Source files that failed validation:\n" + "\n".join(failures)
    )


def test_skills_registration(data_dir: Path):
    """Every entry in VALID_DOMAINS must have a corresponding .md file."""
    from saudi_legal_mcp.tools.skills import VALID_DOMAINS, validate_before_register as skill_validate
    missing = []
    for domain in sorted(VALID_DOMAINS):
        path = data_dir / "skills" / f"{domain}.md"
        if not path.exists():
            missing.append(domain)
    assert not missing, f"Registered domains with no .md file: {missing}"


def test_no_unregistered_skill_files(data_dir: Path):
    """Every .md file in skills/ must be registered in VALID_DOMAINS."""
    from saudi_legal_mcp.tools.skills import VALID_DOMAINS
    skills_dir = data_dir / "skills"
    unregistered = []
    for md_file in skills_dir.glob("*.md"):
        domain = md_file.stem
        if domain not in VALID_DOMAINS:
            unregistered.append(domain)
    assert not unregistered, (
        f"Skill files with no registration in VALID_DOMAINS: {unregistered}"
    )


def test_every_registered_source_has_eval_questions():
    """Coverage guard (2026-08-13 lesson): every registered regulation
    must be exercised by at least one eval question.  A source added to
    VALID_REGULATIONS without eval coverage is untested by definition —
    exactly the gap that stayed open for 6 sources until it was audited."""
    import json
    repo_root = Path(__file__).parent.parent
    corpus_dir = repo_root / "evals" / "corpus"

    covered = set()
    for corpus_file in corpus_dir.glob("*.json"):
        with corpus_file.open(encoding="utf-8-sig") as f:
            for q in json.load(f):
                if q.get("expected_source_id"):
                    covered.add(q["expected_source_id"])

    missing = VALID_REGULATIONS - covered
    assert not missing, (
        f"Registered sources without any eval question: {sorted(missing)}\n"
        "Add questions under evals/corpus/ or remove the registration."
    )
