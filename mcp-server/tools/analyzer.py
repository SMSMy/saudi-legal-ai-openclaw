import json
import os
import re
from typing import Optional

import anthropic

from tools.skills import read_skill
from tools.sources import read_source
from tools.search import find_risks

_CONTRACT_TO_SKILL: dict = {
    "Employment Contract": "labor-law-analysis",
    "Lease Agreement": "real-estate-contracts",
    "Construction Contract": "commercial-dispute",
    "Supply Agreement": "commercial-dispute",
    "NDA": "compliance-check",
    "SaaS Agreement": "compliance-check",
    "Cloud Storage Agreement": "compliance-check",
    "Professional Services Agreement": "contract-review",
    "Commercial Agency Agreement": "commercial-dispute",
    "Shareholder Agreement": "contract-review",
    "Franchise Agreement": "commercial-dispute",
}

_SKILL_TO_SOURCE: dict = {
    "labor-law-analysis": "labor-law",
    "real-estate-contracts": "real-estate-arbitration-reac",
    "commercial-dispute": "commercial-courts",
    "compliance-check": "pdpl",
    "contract-review": "civil-transactions-law",
}

_SYSTEM_PROMPT = (
    "You are a Saudi legal analysis assistant. "
    "Analyze the provided contract clause against Saudi law and return ONLY a JSON object with no additional text. "
    "Do not include markdown code fences, explanations, or any text outside the JSON object."
)

_JSON_SCHEMA = """{
  "risk_level": "critical|high|medium|low|none",
  "issues": [
    {
      "description": "string",
      "legal_reference": "string (نظام + article number)",
      "severity": "critical|high|medium|low"
    }
  ],
  "recommendation": "string",
  "requires_lawyer": true,
  "saudi_law_notes": "string"
}"""


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        text = "\n".join(lines[1:end])
    return text.strip()


def analyze_clause(
    clause_text: str,
    contract_type: str,
    language: str = "ar",
) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return json.dumps(
            {"error": "ANTHROPIC_API_KEY environment variable not set"},
            ensure_ascii=False,
        )

    skill_domain = _CONTRACT_TO_SKILL.get(contract_type)
    if skill_domain is None:
        return json.dumps(
            {
                "error": f"Unknown contract_type '{contract_type}'",
                "valid_types": sorted(_CONTRACT_TO_SKILL),
            },
            ensure_ascii=False,
        )

    skill_content = read_skill(skill_domain)

    source_reg = _SKILL_TO_SOURCE.get(skill_domain)
    source_content = read_source(source_reg) if source_reg else ""
    if source_content.startswith("Unknown") or source_content.startswith("Source file"):
        source_content = ""

    risk_data = find_risks(contract_type=contract_type)

    lang_line = "Respond in Arabic." if language == "ar" else "Respond in English."

    user_prompt = (
        "## Saudi Legal Framework Reference\n\n"
        f"### Skill: {skill_domain}\n{skill_content}\n\n"
        f"### Legal Source\n{source_content or '(no additional source available)'}\n\n"
        f"### Known Risk Patterns for {contract_type}\n{risk_data}\n\n"
        "---\n\n"
        f"## Clause to Analyze\n{clause_text}\n\n"
        "---\n\n"
        f"{lang_line}\n"
        f"Return ONLY this JSON structure (no markdown, no extra text):\n{_JSON_SCHEMA}"
    )

    client = anthropic.Anthropic(api_key=api_key)
    raw = ""
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        raw = message.content[0].text
        cleaned = _strip_fences(raw)
        json.loads(cleaned)
        return cleaned
    except anthropic.APIError as exc:
        return json.dumps({"error": f"API error: {exc}"}, ensure_ascii=False)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            candidate = match.group(0)
            try:
                json.loads(candidate)
                return candidate
            except json.JSONDecodeError:
                pass

        return json.dumps(
            {"error": "Model returned non-JSON response", "raw": raw[:500]},
            ensure_ascii=False,
        )
