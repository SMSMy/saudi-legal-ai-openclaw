"""
skills.py — Saudi Legal AI MCP Server
Trusted skill registry with validation and graduated retrieval interface.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from saudi_legal_mcp.tools import get_repo_path


# ---------------------------------------------------------------------------
# Validation guard (shared logic with sources.py)
# ---------------------------------------------------------------------------

def validate_before_register(filepath: Path) -> tuple[bool, str]:
    """Verify a skill file is safe to register.

    Checks:
    1. File is non-empty.
    2. Content is valid UTF-8.
    3. Contains at least one Markdown H1 heading (# …).

    Returns:
        (True, "") on success.
        (False, reason) on failure.
    """
    try:
        text = filepath.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return False, f"encoding error: {exc}"
    except OSError as exc:
        return False, f"cannot read file: {exc}"

    if not text.strip():
        return False, "file is empty"

    has_h1 = any(
        line.startswith("# ") or line == "#"
        for line in text.splitlines()
    )
    if not has_h1:
        return False, "no Markdown H1 heading found"

    return True, ""


# ---------------------------------------------------------------------------
# VALID_DOMAINS — every entry MUST have a corresponding .md file in skills/
# that passes validate_before_register()
# ---------------------------------------------------------------------------

VALID_DOMAINS: set[str] = {
    "arbitration",
    "commercial-dispute",
    "compliance-check",
    "contract-review",
    "intellectual-property-law",
    "labor-law-analysis",
    "legal-drafting",
    "real-estate-contracts",
    "sports-dispute",            # ← previously unregistered (file existed)
}


# ---------------------------------------------------------------------------
# Core read function (graduated interface — mirrors sources.py)
# ---------------------------------------------------------------------------

def read_skill(
    domain: str,
    section: Optional[str] = None,
    include_content: bool = False,
    max_chars: int = 6000,
) -> dict:
    """Return structured information about a Saudi legal skill/guide.

    Args:
        domain:          A key from VALID_DOMAINS.
        section:         Optional section hint (e.g. "المخاطر الشائعة").
                         When provided, only lines near that heading are returned.
        include_content: When True, full skill text is included (capped at max_chars).
                         Default False — returns metadata only.
        max_chars:       Maximum characters of content to return when
                         include_content=True (default 6000).

    Returns:
        dict matching SkillResponse schema (see schemas.py).
    """
    if domain not in VALID_DOMAINS:
        return {
            "error": f"Unknown domain '{domain}'.",
            "valid_options": sorted(VALID_DOMAINS),
            "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
        }

    skill_path: Path = get_repo_path() / "skills" / f"{domain}.md"
    if not skill_path.exists():
        return {
            "error": f"Skill file not found: {skill_path.name}",
            "domain": domain,
            "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
        }

    full_text = skill_path.read_text(encoding="utf-8")

    content: Optional[str] = None
    content_truncated = False

    if section:
        content = _extract_section(full_text, section, max_chars)
        content_truncated = content is not None and len(content) >= max_chars
    elif include_content:
        if len(full_text) > max_chars:
            content = full_text[:max_chars]
            content_truncated = True
        else:
            content = full_text

    return {
        "domain": domain,
        "verification_status": "unverified",  # skills not yet in manifest cycle
        "content": content,
        "content_available": True,
        "content_truncated": content_truncated,
        "retrieval_hint": (
            "استخدم section أو include_content=True عند الحاجة للنص الكامل."
            if not include_content and not section else None
        ),
        "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
    }


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _extract_section(text: str, section: str, max_chars: int) -> Optional[str]:
    """Return lines around a heading that matches section hint."""
    lines = text.splitlines()
    section_lower = section.strip().lower()
    start_idx: Optional[int] = None
    heading_prefix: str = ""

    for i, line in enumerate(lines):
        if section_lower in line.lower():
            start_idx = i
            j = 0
            while j < len(line) and line[j] == "#":
                j += 1
            heading_prefix = "#" * j
            break

    if start_idx is None:
        return None

    collected = [lines[start_idx]]
    for line in lines[start_idx + 1:]:
        if line.lstrip().startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            if level <= len(heading_prefix):
                break
        collected.append(line)

    result = "\n".join(collected)
    return result[:max_chars] if len(result) > max_chars else result
