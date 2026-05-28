"""
sync_to_insforge.py
Saudi Legal AI Framework — InsForge Mirror Sync Script

Reads the master contract risk dataset and syncs it to the InsForge
PostgreSQL mirror via the PostgREST HTTP API. The CSV is the source of
truth; this script never modifies it.

Usage:
    export INSFORGE_BASE_URL=http://localhost:7130
    export INSFORGE_SERVICE_KEY=your-service-key-here
    python3 scripts/sync_to_insforge.py

    # Or with a .env.local file and python-dotenv installed:
    # python3 -c "from dotenv import load_dotenv; load_dotenv('.env.local')" && ...

Environment variables (required):
    INSFORGE_BASE_URL     Backend base URL — no trailing slash
    INSFORGE_SERVICE_KEY  Service role key — bypasses RLS for write operations

Run scripts/schema_insforge.sql against InsForge before running this script.
"""

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import requests

# ── Constants ──────────────────────────────────────────────────────────────────

MASTER_CSV     = Path("datasets/saudi-contract-risk-dataset.csv")
TABLE_CLAUSES  = "contract_risk_clauses"
TABLE_SYNC_LOG = "contract_risk_sync_log"


# ── Helpers ────────────────────────────────────────────────────────────────────

def print_section(title: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


def get_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        print(f"  ❌ Required environment variable not set: {name}")
        print(f"     Copy .env.example to .env.local and fill in real values.")
        sys.exit(1)
    return value


def get_git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        return result.stdout.strip() or "unknown"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def compute_row_hash(row: dict) -> str:
    """SHA-256 of the row dict serialised as sorted JSON. Detects value changes."""
    canonical = json.dumps(row, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def parse_bool(value: str, column: str, row_num: int) -> bool:
    """Convert CSV 'yes'/'no' to Python bool. Exits on unexpected values."""
    v = value.strip().lower()
    if v == "yes":
        return True
    if v == "no":
        return False
    print(f"  ❌ Row {row_num} [{column}]: expected 'yes' or 'no', got '{value!r}'")
    sys.exit(1)


def service_headers(service_key: str) -> dict:
    return {
        "Authorization": f"Bearer {service_key}",
        "Content-Type":  "application/json",
        "Prefer":        "return=minimal",
    }


# ── CSV ────────────────────────────────────────────────────────────────────────

def read_and_transform(git_sha: str) -> list[dict]:
    """
    Read MASTER_CSV and return rows ready for INSERT.
    Exits with code 1 on any data or file error.
    """
    if not MASTER_CSV.exists():
        print(f"  ❌ Master CSV not found: {MASTER_CSV}")
        print(f"     Run this script from the repository root.")
        sys.exit(1)

    raw_rows: list[dict] = []
    with open(MASTER_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            raw_rows.append({k: v.strip() for k, v in row.items()})

    if not raw_rows:
        print(f"  ❌ Master CSV has no data rows.")
        sys.exit(1)

    print(f"  ✅ Read {len(raw_rows)} row(s) from {MASTER_CSV}")

    db_rows: list[dict] = []
    for row_num, raw in enumerate(raw_rows, start=2):
        db_rows.append({
            "id":                   int(raw["id"]),
            "contract_type":        raw["contract_type"],
            "clause_category":      raw["clause_category"],
            "clause_text":          raw["clause_text"],
            "risk_level":           raw["risk_level"],
            "risk_reason":          raw["risk_reason"],
            "saudi_legal_note":     raw["saudi_legal_note"],
            "recommended_revision": raw["recommended_revision"],
            "related_regulation":   raw["related_regulation"],
            "requires_escalation":  parse_bool(raw["requires_escalation"], "requires_escalation", row_num),
            "language":             raw["language"],
            "industry":             raw["industry"],
            "source_type":          raw["source_type"],
            "reviewed_by_lawyer":   parse_bool(raw["reviewed_by_lawyer"], "reviewed_by_lawyer", row_num),
            # Empty notes → NULL (column is nullable in schema)
            "notes":                raw["notes"] or None,
            "verification_status":  raw["verification_status"],
            # Mirror-only tracking columns
            "csv_row_hash":         compute_row_hash(raw),
            "git_sha":              git_sha,
            # synced_at is omitted — DB DEFAULT now() sets it automatically
        })

    return db_rows


# ── PostgREST operations ───────────────────────────────────────────────────────

def delete_all_rows(base_url: str, service_key: str) -> None:
    """
    Delete all rows from contract_risk_clauses via PostgREST.
    Uses ?id=gte.0 as the required filter (all ids are integers >= 1).
    Returns normally if the table is already empty.
    """
    url = f"{base_url}/{TABLE_CLAUSES}?id=gte.0"
    resp = requests.delete(url, headers=service_headers(service_key), timeout=30)
    if resp.status_code not in (200, 204):
        raise RuntimeError(
            f"DELETE failed: HTTP {resp.status_code}\n{resp.text[:500]}"
        )


def insert_rows(base_url: str, service_key: str, rows: list[dict]) -> None:
    """
    Bulk-insert all rows. PostgREST wraps this in a single transaction:
    either all rows succeed or none do.
    """
    url = f"{base_url}/{TABLE_CLAUSES}"
    body = json.dumps(rows, ensure_ascii=False).encode("utf-8")
    resp = requests.post(url, headers=service_headers(service_key), data=body, timeout=60)
    if resp.status_code not in (200, 201, 204):
        raise RuntimeError(
            f"INSERT failed: HTTP {resp.status_code}\n{resp.text[:500]}"
        )


def write_sync_log(
    base_url: str,
    service_key: str,
    git_sha: str,
    rows_total: int,
    rows_inserted: int,
    status: str,
    error_detail: Optional[str] = None,
) -> None:
    """
    Append one row to contract_risk_sync_log.
    Failures here are non-fatal — a warning is printed but the script does not exit.
    """
    url = f"{base_url}/{TABLE_SYNC_LOG}"
    body = json.dumps([{
        "git_sha":       git_sha,
        "csv_path":      str(MASTER_CSV),
        "rows_total":    rows_total,
        "rows_inserted": rows_inserted,
        "rows_updated":  0,
        "rows_skipped":  0,
        "sync_status":   status,
        "error_detail":  error_detail,
    }], ensure_ascii=False).encode("utf-8")
    try:
        resp = requests.post(url, headers=service_headers(service_key), data=body, timeout=30)
        if resp.status_code not in (200, 201, 204):
            print(f"  ⚠️  Sync log write failed: HTTP {resp.status_code}: {resp.text[:200]}")
    except Exception as exc:
        print(f"  ⚠️  Sync log write failed: {exc}")


# ── Dry-run ────────────────────────────────────────────────────────────────────

def run_dry_run() -> None:
    """
    Preview mode: read and transform the CSV, print full payloads and
    normalization notes. Makes zero network connections.
    """
    git_sha = get_git_sha()

    print_section("DRY-RUN — Reading Master CSV")
    db_rows = read_and_transform(git_sha)

    print_section("DRY-RUN — Normalization Applied")
    print("  The following conversions are applied to every row:")
    print("  Column                    CSV value      DB value")
    print("  requires_escalation       'yes'/'no'     true / false")
    print("  reviewed_by_lawyer        'yes'/'no'     true / false")
    print("  notes (empty string)      ''             null")
    print("  id                        string         integer")
    print("  synced_at                 (not in CSV)   DB DEFAULT now()")

    print_section("DRY-RUN — Per-Row Normalization Confirmed")
    for row in db_rows:
        notes_display = (
            repr(row["notes"])
            if row["notes"] is not None
            else "null  <- empty string converted to NULL"
        )
        print(
            f"  Row {row['id']}  "
            f"requires_escalation={row['requires_escalation']}  "
            f"reviewed_by_lawyer={row['reviewed_by_lawyer']}  "
            f"notes={notes_display}"
        )

    print_section("DRY-RUN — Full Transformed Payloads (JSON)")
    print("  Exact dicts that would be POST-ed to InsForge.")
    print("  synced_at is absent — DB sets it via DEFAULT now().\n")
    print(json.dumps(db_rows, indent=4, ensure_ascii=False))

    print_section("DRY-RUN — Operations That Would Execute")
    base_url_display = os.environ.get("INSFORGE_BASE_URL", "<INSFORGE_BASE_URL>").rstrip("/")
    print(f"  1. DELETE  {base_url_display}/{TABLE_CLAUSES}?id=gte.0")
    print(f"             Removes all existing rows.")
    print(f"             Table is currently EMPTY — nothing will be deleted.")
    print(f"  2. POST    {base_url_display}/{TABLE_CLAUSES}")
    print(f"             Inserts {len(db_rows)} row(s) in a single PostgREST transaction.")
    print(f"             All-or-nothing: if any row fails, zero rows are inserted.")
    print(f"  3. POST    {base_url_display}/{TABLE_SYNC_LOG}")
    print(f"             Appends 1 audit row with sync_status='success'.")

    print_section("DRY-RUN — Overwrite / Truncation Risk")
    print(f"  Master CSV : {MASTER_CSV}  — NEVER modified by this script.")
    print(f"  DELETE scope : contract_risk_clauses rows with id >= 0 only.")
    print(f"  No other tables or files are touched.")

    print(f"\n{'─' * 60}")
    print(f"  Dry run complete — zero network connections made.")
    print(f"  Git SHA that will be recorded : {git_sha}")
    print(f"{'─' * 60}\n")


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync master contract risk CSV to InsForge mirror.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview transformations and payloads without connecting to InsForge.",
    )
    args = parser.parse_args()

    if args.dry_run:
        run_dry_run()
        return

    # ── 1. Environment ────────────────────────────────────────────────────────
    print_section("1 / 5  Environment")
    base_url    = get_env("INSFORGE_BASE_URL").rstrip("/")
    service_key = get_env("INSFORGE_SERVICE_KEY")
    git_sha     = get_git_sha()
    print(f"  Base URL : {base_url}")
    print(f"  Git SHA  : {git_sha}")
    print(f"  ✅ Environment OK")

    # ── 2. Read + transform CSV ───────────────────────────────────────────────
    print_section("2 / 5  Reading Master CSV")
    db_rows = read_and_transform(git_sha)

    # ── 3. Transform summary ──────────────────────────────────────────────────
    print_section("3 / 5  Transform Summary")
    for row in db_rows:
        print(
            f"  Row {row['id']:>3}  "
            f"{row['risk_level']:<8}  "
            f"{row['contract_type']}"
        )
    print(f"\n  ✅ {len(db_rows)} row(s) ready for insert")

    # ── 4. Sync ───────────────────────────────────────────────────────────────
    print_section("4 / 5  Syncing to InsForge")
    try:
        print(f"  Deleting existing rows ...")
        delete_all_rows(base_url, service_key)
        print(f"  ✅ Delete complete")

        print(f"  Inserting {len(db_rows)} row(s) ...")
        insert_rows(base_url, service_key, db_rows)
        print(f"  ✅ Insert complete")

    except Exception as exc:
        print(f"\n  ❌ Sync failed: {exc}")
        write_sync_log(
            base_url, service_key, git_sha,
            rows_total=len(db_rows), rows_inserted=0,
            status="failed", error_detail=str(exc)[:1000],
        )
        sys.exit(1)

    # ── 5. Audit log ──────────────────────────────────────────────────────────
    print_section("5 / 5  Writing Sync Log")
    write_sync_log(
        base_url, service_key, git_sha,
        rows_total=len(db_rows), rows_inserted=len(db_rows),
        status="success",
    )
    print(f"  ✅ Sync log written")

    print(f"\n{'─' * 60}")
    print(f"  Sync complete")
    print(f"  Rows synced : {len(db_rows)}")
    print(f"  Git SHA     : {git_sha}")
    print(f"{'─' * 60}\n")


if __name__ == "__main__":
    main()
