"""
Validates that all JSON files in the evals/cases directory conform to the evals/schema.json,
plus custom business logic checks.
"""
import json
import re
import sys
import datetime
from pathlib import Path

def validate_case(case, idx, case_file_name, registry):
    """Validates a single case dict and returns a list of error strings."""
    errors = []

    # 1. Scoring sum = 1.0
    scoring = case.get("scoring", {})
    total_weight = sum([
        scoring.get("legal_accuracy_weight", 0),
        scoring.get("source_accuracy_weight", 0),
        scoring.get("safety_and_limits_weight", 0)
    ])
    if round(total_weight, 5) != 1.0:
        errors.append(f"sum of scoring weights is {total_weight}, must be 1.0")

    # 2. effective_date ISO format
    effective_date = case.get("effective_date")
    if effective_date:
        try:
            datetime.datetime.strptime(effective_date, "%Y-%m-%d")
        except ValueError:
            errors.append(f"effective_date '{effective_date}' is not ISO YYYY-MM-DD")

    # 3. verified_at ISO format
    verified_at = case.get("verified_at")
    if verified_at:
        try:
            datetime.datetime.strptime(verified_at, "%Y-%m-%d")
        except ValueError:
            errors.append(f"verified_at '{verified_at}' is not ISO YYYY-MM-DD")

    # 4. source_id does not contain _mXX
    source_id = case.get("source_id", "")
    if re.search(r'_m\d+$', source_id):
        errors.append(f"source_id '{source_id}' must not contain decree numbers like _mXX")

    # 5. source_id exists in registry
    if source_id and source_id not in registry:
        errors.append(f"source_id '{source_id}' not found in source-registry.json")

    # 6. URL and Version match registry
    if source_id in registry:
        expected_url = registry[source_id].get("url")
        expected_version = registry[source_id].get("date")
        actual_url = case.get("source_url")
        actual_version = case.get("source_version")

        if actual_url and actual_url != expected_url:
            errors.append(f"source_url '{actual_url}' does not match registry URL '{expected_url}'")

        if actual_version and actual_version != expected_version:
            errors.append(f"source_version '{actual_version}' does not match registry date '{expected_version}'")

    # 7. status is valid
    if case.get("status") not in ["draft", "verified", "deprecated"]:
        errors.append("status must be draft, verified, or deprecated")

    return [f"❌ {case_file_name}[{idx}] failed: {e}" for e in errors]

def main():
    base_dir = Path(__file__).parent
    schema_path = base_dir / "schema.json"
    registry_path = base_dir / "source-registry.json"
    cases_dir = base_dir / "cases"

    try:
        import jsonschema
    except ImportError:
        print("jsonschema not installed. Skip validation or run: pip install jsonschema")
        sys.exit(1)

    if not schema_path.exists():
        print(f"Error: Schema not found at {schema_path}")
        sys.exit(1)

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    total_errors = 0
    for case_file in cases_dir.glob("*.json"):
        with open(case_file, "r", encoding="utf-8") as f:
            try:
                cases = json.load(f)
                jsonschema.validate(instance=cases, schema=schema)

                file_errors = 0
                for idx, case in enumerate(cases):
                    errs = validate_case(case, idx, case_file.name, registry)
                    for e in errs:
                        print(e)
                        file_errors += 1
                        total_errors += 1

                if file_errors == 0:
                    print(f"✅ {case_file.name} is valid.")
            except jsonschema.exceptions.ValidationError as e:
                print(f"❌ {case_file.name} failed schema validation:\n  {e.message}")
                total_errors += 1
            except json.JSONDecodeError as e:
                print(f"❌ {case_file.name} is not valid JSON:\n  {e}")
                total_errors += 1

    if total_errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
