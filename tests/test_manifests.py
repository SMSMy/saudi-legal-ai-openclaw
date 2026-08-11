"""
test_manifests.py — Manifest completeness tests.

Imports validate_all() from scripts/validate_manifests.py — single source of
logic. No duplicate validation code here.

NOTE: These tests will PASS (with warning) before generate_manifests.py has
been run (manifests/ dir does not exist yet). They become meaningful only
after step 3 of the implementation plan is complete.
"""
import sys
from pathlib import Path

# Ensure scripts/ is importable
REPO_ROOT = Path(__file__).parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.validate_manifests import validate_all  # noqa: E402


def test_manifests_complete():
    """All manifest checks must pass with zero errors."""
    errors = validate_all()
    assert errors == [], (
        f"Manifest validation failed with {len(errors)} error(s):\n"
        + "\n".join(f"  • {e}" for e in errors)
    )
