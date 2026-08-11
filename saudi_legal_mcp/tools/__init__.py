"""
saudi_legal_mcp/tools/__init__.py
Shared utilities: repo path resolution + whitelist-validated path helpers.

Path traversal guard:
  All file access MUST go through resolve_source_path() or resolve_skill_path().
  These functions validate the ID against the whitelist BEFORE building any path,
  so no raw user input can escape the sources/ or skills/ directories.

get_repo_path() resolution order (v0.4):
  1. REPO_PATH env var — override for local dev or custom data bundles.
  2. importlib.resources.files("saudi_legal_mcp") / "data" — works after
     pip install regardless of install location (editable or wheel in site-packages).
     This is the path that matters for end users: no env var needed post-install.
"""
import os
from importlib.resources import files
from pathlib import Path


def get_repo_path() -> Path:
    """Resolve the data root.

    Priority 1: REPO_PATH env var (override for local dev or custom data).
    Priority 2: importlib.resources — works after pip install regardless of
                install location (editable or wheel in site-packages).
    """
    env_path = os.environ.get("REPO_PATH")
    if env_path:
        return Path(env_path)
    # importlib.resources.files() returns a Traversable — cast to Path via str
    return Path(str(files("saudi_legal_mcp") / "data"))


# ── Lazy imports to avoid circular dependencies ───────────────────────────────
# VALID_REGULATIONS and VALID_DOMAINS are defined in sources.py / skills.py.
# We import them here only when needed, not at module load time.

def resolve_source_path(source_id: str) -> Path:
    """Return the validated Path for a source .md file.

    Raises ValueError for any source_id not in VALID_REGULATIONS,
    preventing path traversal via crafted input.
    """
    from saudi_legal_mcp.tools.sources import VALID_REGULATIONS  # noqa: PLC0415
    if source_id not in VALID_REGULATIONS:
        raise ValueError(
            f"unknown source_id '{source_id}'. "
            f"Valid IDs: {sorted(VALID_REGULATIONS)}"
        )
    return get_repo_path() / "sources" / f"{source_id}.md"


def resolve_skill_path(domain: str) -> Path:
    """Return the validated Path for a skill .md file.

    Raises ValueError for any domain not in VALID_DOMAINS,
    preventing path traversal via crafted input.
    """
    from saudi_legal_mcp.tools.skills import VALID_DOMAINS  # noqa: PLC0415
    if domain not in VALID_DOMAINS:
        raise ValueError(
            f"unknown domain '{domain}'. "
            f"Valid domains: {sorted(VALID_DOMAINS)}"
        )
    return get_repo_path() / "skills" / f"{domain}.md"
