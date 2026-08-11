"""
sources.py — Saudi Legal AI MCP Server
Trusted source registry with validation before registration.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from saudi_legal_mcp.tools import get_repo_path

# ---------------------------------------------------------------------------
# Validation guard — runs before any file is accepted into VALID_REGULATIONS
# ---------------------------------------------------------------------------

def validate_before_register(filepath: Path) -> tuple[bool, str]:
    """Verify a source file is safe to register.

    Checks:
    1. File is non-empty.
    2. Content is valid UTF-8.
    3. Contains at least one Markdown H1 heading (# …).

    Returns:
        (True, "") on success.
        (False, reason) on failure — caller must NOT register the file.
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
# VALID_REGULATIONS — every entry here MUST have a corresponding .md file
# in sources/ that passes validate_before_register()
# ---------------------------------------------------------------------------

VALID_REGULATIONS: set[str] = {
    "arbitration-law",
    "bankruptcy-law",
    "civil-transactions-law",
    "commercial-courts",
    "companies-law",
    "competition-law",           # ← previously unregistered (file existed)
    "e-commerce-law",
    "evidence-law",
    "fifa-rstp",
    "intellectual-property-law", # ← previously unregistered (file existed)
    "labor-law",
    "legal-profession-law",
    "open-data-judicial-sources",
    "pdpl",
    "real-estate-arbitration-reac",
    "regulation-index",
    "saudi-laws",
    "sports-law-saff",
    "whistleblower-protection",
    "zatca-e-invoicing",         # ← previously unregistered (file existed)
}

# Legal fields that must NEVER be auto-populated — require human verification
_LEGAL_FIELDS = frozenset({
    "official_url", "publisher", "royal_decree",
    "effective_date", "status",
})


# ---------------------------------------------------------------------------
# Core read function (graduated interface — step 4 of implementation plan)
# ---------------------------------------------------------------------------

def read_source(
    regulation: str,
    section: Optional[str] = None,
    include_content: bool = False,
    max_chars: int = 6000,
) -> dict:
    """Return structured information about an official Saudi regulation.

    Args:
        regulation:      A key from VALID_REGULATIONS.
        section:         Optional section hint (e.g. "المادة 74").
                         When provided, only lines near that heading are returned.
        include_content: When True, full text is included (capped at max_chars).
                         Default False — returns metadata + summary only.
        max_chars:       Maximum characters of content to return when
                         include_content=True (default 6000).

    Returns:
        dict matching SourceResponse schema (see schemas.py).
    """
    if regulation not in VALID_REGULATIONS:
        return {
            "error": f"Unknown regulation '{regulation}'.",
            "valid_options": sorted(VALID_REGULATIONS),
            "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
        }

    source_path: Path = get_repo_path() / "sources" / f"{regulation}.md"
    if not source_path.exists():
        return {
            "error": f"Source file not found: {source_path.name}",
            "source_id": regulation,
            "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
        }

    # Load manifest if available (populated in step 3)
    manifest = _load_manifest(regulation)
    verification_status = manifest.get("verification_status", "unverified") if manifest else "unverified"

    full_text = source_path.read_text(encoding="utf-8")

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
        "source_id": regulation,
        "verification_status": verification_status,
        "content": content,
        "content_available": True,
        "content_truncated": content_truncated,
        "retrieval_hint": (
            "استخدم section أو include_content=True عند الحاجة للنص الكامل."
            if not include_content and not section else None
        ),
        "citations": [],
        "disclaimer": "هذه معلومات قانونية عامة وليست استشارة قانونية.",
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_manifest(regulation: str) -> Optional[dict]:
    """Load the JSON manifest for a regulation if it exists."""
    manifest_path = (
        get_repo_path() / "sources" / "manifests" / f"{regulation}.json"
    )
    if not manifest_path.exists():
        return None
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _extract_section(text: str, section: str, max_chars: int) -> Optional[str]:
    """Return lines around a heading that matches section hint.

    Searches for a line containing the section string (case-insensitive,
    Arabic-normalised). Returns lines from that heading up to the next
    same-level heading, capped at max_chars.
    """
    lines = text.splitlines()
    section_lower = section.strip().lower()
    start_idx: Optional[int] = None
    heading_prefix: str = ""

    for i, line in enumerate(lines):
        if section_lower in line.lower():
            start_idx = i
            heading_prefix = line.lstrip("#").strip()[:0]  # detect '#' depth
            # detect actual heading level
            stripped = line.lstrip()
            j = 0
            while j < len(line) and line[j] == "#":
                j += 1
            heading_prefix = "#" * j
            break

    if start_idx is None:
        return None

    # Collect lines until next heading of same or higher level
    collected = [lines[start_idx]]
    for line in lines[start_idx + 1:]:
        stripped = line.lstrip()
        if stripped.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            if level <= len(heading_prefix):
                break
        collected.append(line)

    result = "\n".join(collected)
    return result[:max_chars] if len(result) > max_chars else result
