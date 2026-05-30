import json
import os
from typing import Optional

import anthropic

from tools.sources import read_source, VALID_REGULATIONS

_SYSTEM_PROMPT = (
    "You are a Saudi legal expert assistant. "
    "Extract key facts from the provided Saudi regulation document and return ONLY a JSON object. "
    "Do not include markdown code fences, explanations, or any text outside the JSON object."
)

_JSON_SCHEMA = """{
  "regulation_name": "string",
  "decree_number": "string",
  "key_articles": [
    {
      "article": "string",
      "topic": "string",
      "summary": "string"
    }
  ],
  "competent_authority": "string",
  "important_deadlines": ["string"],
  "common_violations": ["string"],
  "official_source": "string"
}"""


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        text = "\n".join(lines[1:end])
    return text.strip()


def summarize_regulation(regulation: str, topic: Optional[str] = None) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return json.dumps(
            {"error": "ANTHROPIC_API_KEY environment variable not set"},
            ensure_ascii=False,
        )

    source_content = read_source(regulation)
    if source_content.startswith("Unknown") or source_content.startswith("Source file"):
        return json.dumps(
            {
                "error": source_content,
                "valid_regulations": sorted(VALID_REGULATIONS),
            },
            ensure_ascii=False,
        )

    topic_line = (
        f'Focus only on articles and provisions related to "{topic}". '
        if topic
        else ""
    )

    user_prompt = (
        "## Saudi Regulation Document\n\n"
        f"{source_content}\n\n"
        "---\n\n"
        f"{topic_line}"
        f"Return ONLY this JSON structure (no markdown, no extra text):\n{_JSON_SCHEMA}"
    )

    client = anthropic.Anthropic(api_key=api_key)
    raw = ""
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=800,
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
        return json.dumps(
            {"error": "Model returned non-JSON response", "raw": raw[:500]},
            ensure_ascii=False,
        )
