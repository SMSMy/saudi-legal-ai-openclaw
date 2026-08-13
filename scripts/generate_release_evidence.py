"""
generate_release_evidence.py — Legal Release Gate evidence bundle (v0.4.12).

Produces releases/<version>-evidence.json — the public 'source of truth'
for a release.  EVERY number is pulled from an actual run:

  - release:          parsed from pyproject.toml
  - git_commit:       git rev-parse HEAD (subprocess)
  - generated_at:     wall-clock ISO timestamp
  - sources_by_verification_status: counted from committed manifests
  - skills:           fixed not_applicable policy string
  - tests:            pytest -q output parsed (real run)
  - evaluation:       eval_runner.run_eval() executed in-process
  - policy_gates:     match_confidence_threshold imported from the live
                      constant; placeholder_dominated_abstention and
                      evidence policy VERIFIED BY BEHAVIOR (a real gate
                      must demonstrably fire), not by assumption

Usage:
  python scripts/generate_release_evidence.py [--out releases/<version>-evidence.json]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

RELEASES_DIR = REPO_ROOT / "releases"

_SKILLS_POLICY = (
    "not_applicable (reasoning guides — see legal_response_policy.md)"
)


def _read_release_version() -> str:
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return data["project"]["version"]


def _read_git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout.strip()


def _count_sources_by_status() -> dict[str, int]:
    from saudi_legal_mcp.tools.sources import VALID_REGULATIONS

    counts: dict[str, int] = {}
    manifests_dir = REPO_ROOT / "saudi_legal_mcp" / "data" / "sources" / "manifests"
    for manifest_path in sorted(manifests_dir.glob("*.json")):
        if manifest_path.stem not in VALID_REGULATIONS:
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        status = manifest.get("verification_status", "unverified")
        counts[status] = counts.get(status, 0) + 1
    for status in ("field_tested", "verified", "unverified", "review_due", "outdated", "disputed"):
        counts.setdefault(status, 0)
    return counts


def _run_pytest() -> dict[str, int]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=short"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = result.stdout + "\n" + result.stderr
    passed = 0
    failed = 0
    m = re.search(r"(\d+) passed", output)
    if m:
        passed = int(m.group(1))
    m = re.search(r"(\d+) failed", output)
    if m:
        failed = int(m.group(1))
    return {"passed": passed, "failed": failed}


def _run_evaluation() -> dict:
    from evals.metrics.eval_runner import run_eval

    result = run_eval()
    return {
        "corpus_questions": result["total_questions"],
        "citation_precision": result["citation_precision_avg"],
        "source_recall": result["source_recall_avg"],
        "abstention_accuracy": result["abstention_accuracy"],
        "response_time_ms_avg": result["response_time_ms_avg"],
    }


def _verify_placeholder_gate_fires() -> bool:
    """BEHAVIORAL proof: the all-placeholder bankruptcy scenario must
    return insufficient_evidence=True.  'true' in the evidence file
    means the gate demonstrably fired during generation, not that we
    assume the code exists."""
    from saudi_legal_mcp.tools.reasoning import build_legal_brief

    result = build_legal_brief(
        scenario="كم مهلة اعتراض الدائنين وفق اللائحة التنفيذية لنظام الإفلاس",
        domain="commercial-dispute",
        source_id="bankruptcy-law",
    )
    return result.get("insufficient_evidence") is True


def _verify_evidence_policy_enforced() -> bool:
    """BEHAVIORAL proof: enforce_evidence with zero evidence must yield
    insufficient_evidence=True."""
    from saudi_legal_mcp.tools.policy import enforce_evidence

    result = enforce_evidence("ادعاء تجريبي", [])
    return result.get("insufficient_evidence") is True


def _read_confidence_threshold() -> float:
    from saudi_legal_mcp.tools.search import MATCH_CONFIDENCE_THRESHOLD

    return float(MATCH_CONFIDENCE_THRESHOLD)


def build_evidence() -> dict:
    return {
        "release": _read_release_version(),
        "git_commit": _read_git_commit(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources_by_verification_status": _count_sources_by_status(),
        "skills_verification_status": _SKILLS_POLICY,
        "tests": _run_pytest(),
        "evaluation": _run_evaluation(),
        "policy_gates": {
            "match_confidence_threshold": _read_confidence_threshold(),
            "placeholder_dominated_abstention": _verify_placeholder_gate_fires(),
            "all_claims_require_evidence_or_insufficient_evidence": _verify_evidence_policy_enforced(),
        },
    }


def main() -> int:
    evidence = build_evidence()
    RELEASES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RELEASES_DIR / f"{evidence['release']}-evidence.json"
    out_path.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[generate_release_evidence] Written: {out_path}")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
