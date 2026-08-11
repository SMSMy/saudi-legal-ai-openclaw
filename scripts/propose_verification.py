"""
propose_verification.py — Helper script for contributors to propose a source verification.

Usage:
  python scripts/propose_verification.py <source_id>
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MANIFESTS_DIR = REPO_ROOT / "sources" / "manifests"

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/propose_verification.py <source_id>")
        sys.exit(1)
        
    source_id = sys.argv[1]
    manifest_path = MANIFESTS_DIR / f"{source_id}.json"
    
    if not manifest_path.exists():
        print(f"Error: Manifest for {source_id} not found at {manifest_path}")
        sys.exit(1)
        
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error reading manifest: {e}")
        sys.exit(1)
        
    print(f"Proposing verification for: {source_id}")
    official_url = input("Enter official URL (e.g. boe.gov.sa/...): ").strip()
    publisher = input("Enter publisher (e.g. هيئة الخبراء بمجلس الوزراء): ").strip()
    
    if not official_url or not publisher:
        print("URL and publisher are required.")
        sys.exit(1)
        
    manifest["official_url"] = official_url
    manifest["publisher"] = publisher
    manifest["verification_status"] = "review_due"
    manifest["metadata_status"] = "proposed"
    manifest["verified_by"] = "proposed_by_contributor"
    
    # Set a review due date 30 days from now to force a quick first review
    review_due = datetime.now(timezone.utc).date()
    manifest["review_due_at"] = f"{review_due.year}-{review_due.month:02d}-{review_due.day:02d}T00:00:00Z"
    
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print("\nManifest updated successfully!")
    print(f"Next steps:")
    print(f"1. git add {manifest_path.relative_to(REPO_ROOT)}")
    print(f"2. git commit -m 'Propose verification for {source_id}'")
    print(f"3. Create a Pull Request (the CODEOWNER will be automatically requested for review).")

if __name__ == "__main__":
    main()
