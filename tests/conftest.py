"""
conftest.py — Shared pytest fixtures for Saudi Legal AI test suite.
"""
import sys
import os
import pytest
from pathlib import Path

# Repo root (for scripts.* imports like validate_manifests)
REPO_ROOT = Path(__file__).parent.parent

for p in [str(REPO_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Point REPO_PATH to the data directory inside the package.
# This mirrors what get_repo_path() returns via importlib.resources post pip-install.
# Using an explicit path here lets tests run without pip install -e . installed,
# while still exercising the same data layout as production.
DATA_DIR = REPO_ROOT / "saudi_legal_mcp" / "data"
os.environ.setdefault("REPO_PATH", str(DATA_DIR))


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def data_dir() -> Path:
    return DATA_DIR
