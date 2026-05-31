import csv
import json
from pathlib import Path
from typing import Optional
from tools import get_repo_path

_DATASET = "datasets/saudi-contract-risk-dataset.csv"

_KEEP_FIELDS = (
    "contract_type",
    "clause_category",
    "clause_text",
    "risk_level",
    "risk_reason",
    "saudi_legal_note",
    "recommended_revision",
    "related_regulation",
)

_ESCALATION_LEVELS = {"critical", "high"}


def find_risks(
    contract_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    category: Optional[str] = None,
) -> str:
    csv_path: Path = get_repo_path() / _DATASET
    if not csv_path.exists():
        return json.dumps(
            {
                "query": {
                    "contract_type": contract_type,
                    "risk_level": risk_level,
                    "category": category,
                },
                "total_found": 0,
                "risks": [],
                "data_source": "saudi-contract-risk-dataset.csv",
                "disclaimer": "For preliminary research only. Not legal advice.",
                "error": f"Dataset not found: {csv_path}",
            },
            ensure_ascii=False,
            indent=2,
        )

    risks = []
    with open(csv_path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if contract_type and row.get("contract_type") != contract_type:
                continue
            if risk_level and row.get("risk_level") != risk_level:
                continue
            if category and row.get("clause_category") != category:
                continue
            level = row.get("risk_level", "")
            risks.append(
                {
                    "risk_level": level,
                    "category": row.get("clause_category", ""),
                    "clause_text": row.get("clause_text", ""),
                    "risk_reason": row.get("risk_reason", ""),
                    "saudi_legal_note": row.get("saudi_legal_note", ""),
                    "recommended_revision": row.get("recommended_revision", ""),
                    "related_regulation": row.get("related_regulation", ""),
                    "requires_escalation": level in _ESCALATION_LEVELS,
                }
            )

    return json.dumps(
        {
            "query": {
                "contract_type": contract_type,
                "risk_level": risk_level,
                "category": category,
            },
            "total_found": len(risks),
            "risks": risks,
            "data_source": "saudi-contract-risk-dataset.csv",
            "disclaimer": "For preliminary research only. Not legal advice.",
        },
        ensure_ascii=False,
        indent=2,
    )
