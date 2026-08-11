"""
search.py -- Saudi Legal AI MCP Server
Contract risk search with Case-insensitive and partial category matching.

v0.3 changes:
  - find_risks() now returns dict (not JSON string) -- aligned with v0.2 contract
  - Category matching is case-insensitive (exact) by default
  - Partial/fuzzy category matching supported via category_fuzzy=True flag,
    in which case match_confidence is set in the response (never silent)
"""
import csv
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from saudi_legal_mcp.tools import get_repo_path
from saudi_legal_mcp.tools.schemas import RiskResponse

_DATASET = "datasets/saudi-contract-risk-dataset.csv"
_ESCALATION_LEVELS = {"critical", "high"}

# Minimum confidence for fuzzy category match to be included in results.
# Below this threshold the row is excluded even in fuzzy mode, preventing
# low-signal noise from polluting the output.
MATCH_CONFIDENCE_THRESHOLD = 0.7


def _category_exact_match(row_cat: str, query_cat: str) -> bool:
    """Case-insensitive exact match."""
    return row_cat.strip().lower() == query_cat.strip().lower()


def _category_fuzzy_score(row_cat: str, query_cat: str) -> float:
    """Simple word-overlap confidence: fraction of query words found in row_cat.

    Returns a float in [0.0, 1.0].  A score of 1.0 is equivalent to exact match.
    This is intentionally lightweight (no external deps) and conservative.
    """
    q_words = set(query_cat.lower().split())
    r_words = set(row_cat.lower().split())
    if not q_words:
        return 0.0
    overlap = q_words & r_words
    return round(len(overlap) / len(q_words), 2)


def find_risks(
    contract_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    category: Optional[str] = None,
    category_fuzzy: bool = False,
) -> dict:
    """Return contract risks from the dataset as a structured dict.

    Args:
        contract_type:   Filter by contract type (exact, case-sensitive).
        risk_level:      Filter by risk level (exact, case-insensitive).
        category:        Filter by clause category.
                         Exact case-insensitive match by default.
                         If category_fuzzy=True, partial word-overlap match is used
                         and match_confidence is set on the response.
        category_fuzzy:  Enable fuzzy category matching.
                         When True, match_confidence is set and rows below
                         MATCH_CONFIDENCE_THRESHOLD are excluded.
                         When False (default), match_confidence=None (exact match).

    Returns:
        dict matching RiskResponse schema.
    """
    csv_path: Path = get_repo_path() / _DATASET
    if not csv_path.exists():
        return asdict(RiskResponse(
            query={
                "contract_type": contract_type,
                "risk_level": risk_level,
                "category": category,
            },
            total_found=0,
            risks=[],
            data_source=_DATASET,
            match_confidence=None,
        )) | {"error": f"Dataset not found: {csv_path}"}

    risks: list[dict] = []
    # When fuzzy matching, track lowest confidence encountered among included rows
    min_confidence: float = 1.0
    any_fuzzy_applied = False
    excluded_count: int = 0  # rows that matched but fell below threshold

    with open(csv_path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            # -- contract_type: exact (CSV values are canonical)
            if contract_type and row.get("contract_type") != contract_type:
                continue

            # -- risk_level: case-insensitive exact
            if risk_level:
                if row.get("risk_level", "").lower() != risk_level.lower():
                    continue

            # -- category matching
            row_cat = row.get("clause_category", "")
            if category:
                if category_fuzzy:
                    any_fuzzy_applied = True
                    score = _category_fuzzy_score(row_cat, category)
                    if score < MATCH_CONFIDENCE_THRESHOLD:
                        excluded_count += 1  # count, not silently ignore
                        continue
                    min_confidence = min(min_confidence, score)
                else:
                    if not _category_exact_match(row_cat, category):
                        continue

            level = row.get("risk_level", "")
            risks.append({
                "risk_level": level,
                "category": row_cat,
                "clause_text": row.get("clause_text", ""),
                "risk_reason": row.get("risk_reason", ""),
                "saudi_legal_note": row.get("saudi_legal_note", ""),
                "recommended_revision": row.get("recommended_revision", ""),
                "related_regulation": row.get("related_regulation", ""),
                "requires_escalation": level in _ESCALATION_LEVELS,
            })

    # Only set match_confidence when fuzzy was actually applied and returned results
    effective_confidence: Optional[float] = None
    if any_fuzzy_applied and risks:
        effective_confidence = min_confidence

    return asdict(RiskResponse(
        query={
            "contract_type": contract_type,
            "risk_level": risk_level,
            "category": category,
        },
        total_found=len(risks),
        risks=risks,
        data_source=_DATASET,
        match_confidence=effective_confidence,
        excluded_low_confidence_count=excluded_count,
    ))
