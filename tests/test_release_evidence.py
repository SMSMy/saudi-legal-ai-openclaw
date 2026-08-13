"""
test_release_evidence.py — evidence-bundle generator invariants (v0.4.12).

The release evidence file is the public source of truth — every number
must come from an actual run.  These tests lock the generator's pure
components so a future edit cannot silently hard-code a fake value.
"""
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def test_sources_count_actual():
    import scripts.generate_release_evidence as gre
    counts = gre._count_sources_by_status()
    assert sum(counts.values()) == 20
    assert counts["field_tested"] == 20
    assert counts["verified"] == 0


def test_git_commit_matches_actual_head():
    import scripts.generate_release_evidence as gre
    actual = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert gre._read_git_commit() == actual


def test_placeholder_gate_fires_behaviorally():
    import scripts.generate_release_evidence as gre
    assert gre._verify_placeholder_gate_fires() is True


def test_evidence_policy_fires_behaviorally():
    import scripts.generate_release_evidence as gre
    assert gre._verify_evidence_policy_enforced() is True


def test_confidence_threshold_imported_from_live_constant():
    import scripts.generate_release_evidence as gre
    from saudi_legal_mcp.tools.search import MATCH_CONFIDENCE_THRESHOLD
    assert gre._read_confidence_threshold() == float(MATCH_CONFIDENCE_THRESHOLD)


def test_release_version_parsed_from_pyproject():
    import scripts.generate_release_evidence as gre
    import tomllib
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert gre._read_release_version() == data["project"]["version"]
