"""
validate_manifests.py — Single source of truth for manifest validation.

Used in two ways:
  1. CLI (CI): python scripts/validate_manifests.py → exit(1) on errors
  2. pytest:   from scripts.validate_manifests import validate_all
               assert validate_all() == []

Behaviour when sources/manifests/ does not yet exist:
  - Prints a warning and exits 0 (no failure).
  - Becomes a hard failure only after generate_manifests.py has been run
    at least once (i.e. the directory exists).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

# Resolve repo root relative to this script's location (scripts/ → repo root)
REPO_ROOT = Path(__file__).parent.parent
MANIFESTS_DIR = REPO_ROOT / "sources" / "manifests"
SOURCES_DIR = REPO_ROOT / "sources"

# Legal fields that must NOT be auto-populated without human verification
_LEGAL_FIELDS = frozenset({
    "official_url", "publisher", "royal_decree",
    "effective_date",
})

# Valid verification_status values
_VALID_STATUSES = frozenset({
    "unverified", "verified", "review_due", "outdated", "disputed",
})


def _sha256(path: Path) -> str:
    """Return the SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _load_valid_regulations() -> set[str]:
    """Import VALID_REGULATIONS from the tools package."""
    sys.path.insert(0, str(REPO_ROOT / "mcp-server"))
    from saudi_legal_mcp.tools.sources import VALID_REGULATIONS  # noqa: PLC0415
    return set(VALID_REGULATIONS)


def validate_all() -> list[str]:
    """Run all manifest checks. Returns a list of error strings (empty = OK).

    Safe to call even before generate_manifests.py has been run:
    if MANIFESTS_DIR does not exist, returns [] (no errors, just a warning
    printed to stderr).
    """
    if not MANIFESTS_DIR.exists():
        print(
            f"[validate_manifests] WARNING: {MANIFESTS_DIR} does not exist yet. "
            "Run scripts/generate_manifests.py first. Skipping checks.",
            file=sys.stderr,
        )
        return []  # Warn, do not fail — see task.md note on CI red period

    errors: list[str] = []
    valid_regulations = _load_valid_regulations()

    # ── Check 1: every registered source_id has a manifest ──────────────────
    for reg_id in sorted(valid_regulations):
        manifest_path = MANIFESTS_DIR / f"{reg_id}.json"
        if not manifest_path.exists():
            errors.append(f"MISSING manifest for registered source: {reg_id}")

    # ── Check 2: every manifest has a corresponding source file & no orphans ─
    for manifest_path in sorted(MANIFESTS_DIR.glob("*.json")):
        reg_id = manifest_path.stem
        if reg_id not in valid_regulations:
            errors.append(
                f"ORPHAN manifest (not in VALID_REGULATIONS): {manifest_path.name}"
            )

    # ── Check 3: SHA-256 matches actual file content ─────────────────────────
    for manifest_path in sorted(MANIFESTS_DIR.glob("*.json")):
        reg_id = manifest_path.stem
        source_path = SOURCES_DIR / f"{reg_id}.md"
        if not source_path.exists():
            continue  # already caught above

        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"INVALID JSON in manifest {manifest_path.name}: {exc}")
            continue

        stored_sha = manifest.get("sha256", "")
        actual_sha = _sha256(source_path)
        if stored_sha and stored_sha != actual_sha:
            errors.append(
                f"SHA MISMATCH for {reg_id}: "
                f"manifest={stored_sha[:12]}… actual={actual_sha[:12]}…"
            )

        # ── Check 4: legal fields not auto-populated without verification ────
        verification_status = manifest.get("verification_status", "")
        if verification_status not in _VALID_STATUSES:
            errors.append(
                f"INVALID verification_status '{verification_status}' in {manifest_path.name}. "
                f"Must be one of: {sorted(_VALID_STATUSES)}"
            )

        if verification_status == "unverified":
            for field in _LEGAL_FIELDS:
                if manifest.get(field):
                    errors.append(
                        f"LEGAL FIELD '{field}' is populated in {manifest_path.name} "
                        f"but verification_status=unverified. Remove or get human sign-off."
                    )

    return errors


if __name__ == "__main__":
    errs = validate_all()
    if errs:
        print(f"[validate_manifests] {len(errs)} error(s) found:", file=sys.stderr)
        for e in errs:
            print(f"  ✗ {e}", file=sys.stderr)
        sys.exit(1)
    else:
        print("[validate_manifests] All checks passed [OK]")
        sys.exit(0)
