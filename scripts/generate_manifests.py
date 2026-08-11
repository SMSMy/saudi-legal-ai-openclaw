"""
generate_manifests.py — Build initial JSON manifests for all sources in sources/.

Generates ONLY fields that can be determined locally and deterministically:
  - id, path, sha256, generated_at, metadata_status, verification_status

NEVER auto-populates legal fields that require human verification:
  official_url, publisher, royal_decree, effective_date, status

Run once to bootstrap sources/manifests/, then update manually via PR.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from saudi_legal_mcp.tools import get_repo_path

DATA_DIR = get_repo_path()
SOURCES_DIR = DATA_DIR / "sources"
MANIFESTS_DIR = SOURCES_DIR / "manifests"

# Fields that must NEVER be auto-populated
_BLOCKED_AUTO_FIELDS = (
    "official_url", "publisher", "royal_decree",
    "effective_date", "status",
)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _load_valid_regulations() -> set[str]:
    from saudi_legal_mcp.tools.sources import VALID_REGULATIONS  # noqa: PLC0415
    return set(VALID_REGULATIONS)


def generate_manifest(source_path: Path, *, overwrite: bool = False) -> dict:
    """Build a manifest dict for a single source file.

    Args:
        source_path: Path to the .md file.
        overwrite:   If False (default), preserves existing manifest if found.
                     If True, regenerates from scratch (loses manual edits).

    Returns the manifest dict written to disk.
    """
    reg_id = source_path.stem
    manifest_path = MANIFESTS_DIR / f"{reg_id}.json"

    # Preserve existing manual edits unless overwrite=True
    existing: dict = {}
    if manifest_path.exists() and not overwrite:
        try:
            existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing = {}

    now = datetime.now(timezone.utc).isoformat()

    manifest = {
        # ── Auto-populated (local, deterministic) ────────────────────────────
        "id": reg_id,
        "path": f"sources/{source_path.name}",
        "sha256": _sha256(source_path),
        "generated_at": now,
        # ── Status fields — start as needs_review / unverified ───────────────
        "metadata_status": existing.get("metadata_status", "needs_review"),
        "verification_status": existing.get("verification_status", "unverified"),
        # ── Human-filled fields — preserved if already set ───────────────────
        "verified_by": existing.get("verified_by", None),
        "verified_at": existing.get("verified_at", None),
        "verification_scope": existing.get("verification_scope", []),
        "review_due_at": existing.get("review_due_at", None),
        "review_notes": existing.get("review_notes", None),
        "approval_commit": existing.get("approval_commit", None),
        # ── Legal fields — intentionally absent until human review ───────────
        # official_url, publisher, royal_decree, effective_date, status
        # DO NOT add these here. See final-plan.md §2.2.
    }

    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return manifest


def run(overwrite: bool = False) -> int:
    """Generate manifests for all registered source files.

    Returns the count of manifests written.
    """
    valid_regulations = _load_valid_regulations()
    count = 0
    skipped = []
    errors = []

    for reg_id in sorted(valid_regulations):
        source_path = SOURCES_DIR / f"{reg_id}.md"
        if not source_path.exists():
            skipped.append(reg_id)
            continue
        try:
            generate_manifest(source_path, overwrite=overwrite)
            count += 1
            print(f"  [ok] {reg_id}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{reg_id}: {exc}")
            print(f"  [ERR] {reg_id}: {exc}", file=sys.stderr)

    print(f"\n[generate_manifests] Written: {count}, Skipped: {len(skipped)}, Errors: {len(errors)}")
    if skipped:
        print(f"  Skipped (no .md file): {skipped}", file=sys.stderr)
    return count


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate source manifests.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Regenerate manifests from scratch (loses manual edits to human fields).",
    )
    args = parser.parse_args()

    print(f"[generate_manifests] Writing to {MANIFESTS_DIR}")
    run(overwrite=args.overwrite)
