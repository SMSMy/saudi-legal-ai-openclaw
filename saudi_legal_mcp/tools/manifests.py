"""
manifests.py — Read source manifests for the Saudi Legal AI MCP server.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from saudi_legal_mcp.tools import get_repo_path


def read_manifest(source_id: str) -> Optional[dict]:
    """Load the JSON manifest for a regulation source.

    Returns the manifest dict if found, or None if not yet generated.
    Callers should handle None gracefully (manifests may not exist yet).
    """
    manifest_path = (
        get_repo_path() / "sources" / "manifests" / f"{source_id}.json"
    )
    if not manifest_path.exists():
        return None
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def get_verification_status(source_id: str) -> str:
    """Return the verification_status for a source, defaulting to 'unverified'."""
    manifest = read_manifest(source_id)
    if manifest is None:
        return "unverified"
    return manifest.get("verification_status", "unverified")
