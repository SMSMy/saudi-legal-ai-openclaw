"""
eval_runner.py — Baseline evaluation for Saudi Legal AI retrieval tools.

Measures:
  - citation_precision:  fraction of returned results matching expected source
  - source_recall:       fraction of expected sources actually retrieved
  - abstention_accuracy: fraction of should_abstain questions correctly declined
  - response_time_ms:    tool response time in milliseconds

Usage:
  python evals/metrics/eval_runner.py
  python evals/metrics/eval_runner.py > evals/metrics/results/baseline.json
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Path setup ───────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent.parent
MCP_SERVER = REPO_ROOT / "mcp-server"

for p in [str(REPO_ROOT), str(MCP_SERVER)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import os
os.environ.setdefault("REPO_PATH", str(REPO_ROOT / "saudi_legal_mcp" / "data"))
from saudi_legal_mcp.tools.sources import read_source, VALID_REGULATIONS
from saudi_legal_mcp.tools.skills import read_skill
from saudi_legal_mcp.tools.search import find_risks
from saudi_legal_mcp.tools.reasoning import find_legal_provision  # v0.3: replaces read_source in eval

# ── Corpus loading ────────────────────────────────────────────────────────────
CORPUS_DIR = REPO_ROOT / "evals" / "corpus"


def load_corpus() -> list[dict]:
    questions = []
    for corpus_file in sorted(CORPUS_DIR.glob("*.json")):
        with corpus_file.open(encoding="utf-8-sig") as f:
            batch = json.load(f)
        for q in batch:
            q["_corpus_file"] = corpus_file.name
        questions.extend(batch)
    return questions


# ── Evaluation helpers ────────────────────────────────────────────────────────

def _run_source_retrieval(question: dict) -> tuple[dict, float]:
    """Run find_legal_provision for questions with expected_source_id.

    v0.3 change: replaced read_source(max_chars=3000) with find_legal_provision
    which reads the full file and returns the best-matching sections.
    This fixes the recall issue where answers in the latter part of a file
    were never found due to the 3000-char hard cap in the old eval logic.
    """
    source_id = question.get("expected_source_id")
    if not source_id or source_id not in VALID_REGULATIONS:
        return {}, 0.0
    section_hint = question.get("expected_section_hint") or ""
    query = section_hint if section_hint else question.get("question", "")
    t0 = time.perf_counter()
    result = find_legal_provision(query=query, source_id=source_id)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    return result, elapsed_ms


def _run_risk_retrieval(question: dict) -> tuple[dict, float]:
    """Run find_risks for contract-risk questions."""
    contract_type = question.get("expected_contract_type")
    if not contract_type:
        return {}, 0.0
    t0 = time.perf_counter()
    result = find_risks(contract_type=contract_type)  # returns dict directly (v0.3)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    return result, elapsed_ms


def eval_question(question: dict) -> dict:
    """Evaluate a single corpus question. Returns result record."""
    qid = question["id"]
    should_abstain = question.get("should_abstain", False)
    expected_source = question.get("expected_source_id")
    expected_contract = question.get("expected_contract_type")
    expected_contains = question.get("expected_answer_contains", [])
    expected_risk_levels = set(question.get("expected_risk_levels", []))
    expected_categories = set(question.get("expected_categories", []))

    metrics: dict[str, Any] = {
        "id": qid,
        "corpus_file": question.get("_corpus_file"),
        "difficulty": question.get("difficulty"),
        "should_abstain": should_abstain,
        "citation_precision": None,
        "source_recall": None,
        "abstention_correct": None,
        "response_time_ms": None,
        "notes": [],
    }

    # ── Source retrieval questions ────────────────────────────────────────────
    if expected_source and expected_source in VALID_REGULATIONS:
        result, ms = _run_source_retrieval(question)
        metrics["response_time_ms"] = round(ms, 2)

        if result.get("error") or result.get("insufficient_evidence"):
            metrics["citation_precision"] = 0.0
            metrics["source_recall"] = 0.0
            if result.get("insufficient_evidence"):
                metrics["notes"].append("find_legal_provision: insufficient_evidence")
            else:
                metrics["notes"].append(f"find_legal_provision returned error: {result.get('error')}")
        else:
            # Precision: did we get sections from the right source?
            metrics["citation_precision"] = 1.0 if result.get("source_id") == expected_source else 0.0
            # Recall: does any matched section body contain expected terms?
            if expected_contains:
                all_content = " ".join(
                    s.get("body", "") for s in result.get("matched_sections", [])
                )
                hits = sum(1 for term in expected_contains if term in all_content)
                metrics["source_recall"] = round(hits / len(expected_contains), 2)
            else:
                metrics["source_recall"] = 1.0  # no specific terms required

        # Abstention not applicable for source retrieval
        metrics["abstention_correct"] = None

    # ── Contract risk questions ───────────────────────────────────────────────
    elif expected_contract:
        result, ms = _run_risk_retrieval(question)
        metrics["response_time_ms"] = round(ms, 2)
        risks = result.get("risks", [])

        if should_abstain:
            # Abstention: correct if zero risks returned or insufficient_evidence
            returned_critical = any(r["risk_level"] in {"critical", "high"} for r in risks)
            metrics["abstention_correct"] = not returned_critical
            metrics["citation_precision"] = None
            metrics["source_recall"] = None
        else:
            # Precision: fraction of returned risks matching expected risk levels
            if risks and expected_risk_levels:
                matching = [r for r in risks if r["risk_level"] in expected_risk_levels]
                metrics["citation_precision"] = round(len(matching) / len(risks), 2) if risks else 0.0
            else:
                metrics["citation_precision"] = 1.0 if not expected_risk_levels else 0.0

            # Recall: did we get at least one risk per expected category?
            if expected_categories:
                returned_cats = {r.get("category", "") for r in risks}
                hits = expected_categories & returned_cats
                metrics["source_recall"] = round(len(hits) / len(expected_categories), 2)
            else:
                metrics["source_recall"] = 1.0

    # ── Abstention-only questions (no expected source) ────────────────────────
    elif should_abstain:
        metrics["abstention_correct"] = True  # no retrieval — correct by definition
        metrics["citation_precision"] = None
        metrics["source_recall"] = None
        metrics["response_time_ms"] = 0.0

    return metrics


# ── Main runner ───────────────────────────────────────────────────────────────

def run_eval() -> dict:
    """Run the full evaluation and return a results dict."""
    questions = load_corpus()
    results = [eval_question(q) for q in questions]

    # Aggregate
    precision_vals = [r["citation_precision"] for r in results if r["citation_precision"] is not None]
    recall_vals = [r["source_recall"] for r in results if r["source_recall"] is not None]
    abstention_vals = [r["abstention_correct"] for r in results if r["abstention_correct"] is not None]
    time_vals = [r["response_time_ms"] for r in results if r["response_time_ms"] is not None and r["response_time_ms"] > 0]

    def avg(vals: list) -> float | None:
        return round(sum(vals) / len(vals), 4) if vals else None

    summary = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "total_questions": len(questions),
        "citation_precision_avg": avg(precision_vals),
        "source_recall_avg": avg(recall_vals),
        "abstention_accuracy": avg([1.0 if v else 0.0 for v in abstention_vals]),
        "response_time_ms_avg": avg(time_vals),
        "by_question": results,
    }
    return summary


if __name__ == "__main__":
    output = run_eval()
    # Print JSON to stdout (can be redirected to baseline.json)
    print(json.dumps(output, ensure_ascii=False, indent=2))

    # Print human-readable summary to stderr
    print("\n── Evaluation Summary ──────────────────────", file=sys.stderr)
    print(f"  Questions:          {output['total_questions']}", file=sys.stderr)
    print(f"  Citation Precision: {output['citation_precision_avg']}", file=sys.stderr)
    print(f"  Source Recall:      {output['source_recall_avg']}", file=sys.stderr)
    print(f"  Abstention Acc:     {output['abstention_accuracy']}", file=sys.stderr)
    print(f"  Avg Response (ms):  {output['response_time_ms_avg']}", file=sys.stderr)
