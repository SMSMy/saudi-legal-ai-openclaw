"""
audit_substring_vs_wordboundary.py — DIAGNOSTIC ONLY (no production change).

Discovery (b) from 2026-08-14: `_score_section` matches query terms as
SUBSTRINGS (`variant in haystack`), not whole words.  Any short Arabic
term that appears inside a longer word is a false match.

This script measures the REAL damage: for every source-retrieval question
in the eval corpus, it runs find_legal_provision twice — once with the
current substring scoring, once with strict word-boundary scoring — and
reports how many questions flip classification (success <-> fail).

It does NOT modify production code.  It monkeypatches the module global
`_score_section` for the second pass, then restores it.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO = Path("/mnt/c/Code-backup/saudi-legal-ai-openclaw-main")
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "evals" / "metrics"))
os.environ.setdefault("REPO_PATH", str(REPO / "saudi_legal_mcp" / "data"))

import saudi_legal_mcp.tools.reasoning as R  # noqa: E402
from saudi_legal_mcp.tools.reasoning import (  # noqa: E402
    _normalize_arabic,
    _score_section,
    _synonym_variants,
)
import eval_runner as ER  # noqa: E402

# Word chars for boundary: Latin letters + Arabic script letters
_WORD_CHAR = r"A-Za-z\u0600-\u06ff"


def _contains_word(haystack: str, word: str) -> bool:
    """True if `word` appears as a WHOLE word (not inside a longer word)."""
    if not word:
        return False
    pat = re.compile(
        r"(?<![" + _WORD_CHAR + r"])" + re.escape(word) + r"(?![" + _WORD_CHAR + r"])"
    )
    return pat.search(haystack) is not None


def _score_section_wordboundary(section: dict, query_terms: list[str]) -> int:
    """Mirror of _score_section, but word-boundary instead of substring."""
    hay = _normalize_arabic((section["heading"] + " " + section["body"]).lower())
    score = 0
    for term in query_terms:
        t = _normalize_arabic(term.lower())
        matched = False
        for variant in _synonym_variants(t):
            if _contains_word(hay, variant):
                matched = True
                break
            if len(variant) > 2 and variant[:2] == "ال" and _contains_word(hay, variant[2:]):
                matched = True
                break
            if len(variant) >= 2 and _contains_word(hay, "ال" + variant):
                matched = True
                break
        if matched:
            score += 1
    return score


def classify(r: dict) -> str:
    """Success/fail for a source-retrieval question, mirroring eval semantics."""
    if r.get("citation_precision") is None and r.get("source_recall") is None:
        return "n/a"
    if (r.get("source_recall") or 0.0) > 0:
        return "OK"
    return "FAIL"


def main() -> None:
    # Pass 1: current substring scoring
    R._score_section = _score_section
    sub = ER.run_eval()

    # Pass 2: word-boundary scoring
    R._score_section = _score_section_wordboundary
    wb = ER.run_eval()

    # Restore production state
    R._score_section = _score_section

    sub_by = {r["id"]: r for r in sub["by_question"]}
    wb_by = {r["id"]: r for r in wb["by_question"]}

    flips = []
    recall_changes = []
    for qid in sub_by:
        a, b = sub_by[qid], wb_by[qid]
        ca, cb = classify(a), classify(b)
        if ca == "n/a" or cb == "n/a":
            continue
        ra = a.get("source_recall") or 0.0
        rb = b.get("source_recall") or 0.0
        if ca != cb:
            flips.append((qid, ca, cb, ra, rb, a.get("corpus_file")))
        elif ra != rb:
            recall_changes.append((qid, ra, rb, a.get("corpus_file")))

    n_src = sum(
        1
        for r in sub["by_question"]
        if classify(r) != "n/a"
    )

    print("=" * 70)
    print("AUDIT: substring vs word-boundary matching (diagnostic)")
    print("=" * 70)
    print(f"total_questions            : {sub['total_questions']}")
    print(f"source-retrieval questions : {n_src}")
    print()
    print("aggregate (substring):")
    print(f"  precision = {sub['citation_precision_avg']}")
    print(f"  recall    = {sub['source_recall_avg']}")
    print("aggregate (word-boundary):")
    print(f"  precision = {wb['citation_precision_avg']}")
    print(f"  recall    = {wb['source_recall_avg']}")
    print()
    print(f"classification flips (OK<->FAIL) : {len(flips)}")
    for qid, ca, cb, ra, rb, cf in sorted(flips):
        print(f"  {qid:20s} {ca:4s} -> {cb:4s}   recall {ra:.2f} -> {rb:.2f}   [{cf}]")
    print()
    print(f"recall changed (no flip)         : {len(recall_changes)}")
    for qid, ra, rb, cf in sorted(recall_changes):
        print(f"  {qid:20s} recall {ra:.2f} -> {rb:.2f}   [{cf}]")
    print()
    # Direction of flips
    ok_to_fail = sum(1 for _, ca, cb, *_ in flips if ca == "OK" and cb == "FAIL")
    fail_to_ok = sum(1 for _, ca, cb, *_ in flips if ca == "FAIL" and cb == "OK")
    print(f"OK->FAIL flips : {ok_to_fail}")
    print(f"FAIL->OK flips : {fail_to_ok}")
    print("=" * 70)


if __name__ == "__main__":
    main()
