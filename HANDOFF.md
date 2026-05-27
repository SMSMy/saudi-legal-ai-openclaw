# Handoff — Saudi Legal AI Framework

**Date:** 2026-05-25  
**Branch:** `main` (PR #27 merged)  
**Status:** All CI checks green — 79 tests pass, validator clean

---

## What Was Shipped Today

### Reverse-Discovery Seam (PR #27 — merged)

The framework's documentation cascade was unidirectional: skills cited sources, but there was no way to navigate the reverse direction (source → which skills use it). A reader starting from `sources/labor-law.md` had no path to `skills/labor-law-analysis.md`. Coverage gaps were invisible without manual grep.

**What was built:**

| Deliverable | File | Description |
|---|---|---|
| CI validator | `scripts/validate_cross_refs.py` | Enforces bidirectional traceability in every push |
| Tests | `tests/test_validate_cross_refs.py` | 79 tests (TDD: tests written first) |
| Reverse links | `sources/civil-transactions-law.md` | `## See also` section appended |
| Reverse links | `sources/labor-law.md` | `## See also` section appended |
| Reverse links | `sources/companies-law.md` | `## See also` section appended |
| Reverse links | `sources/pdpl.md` | `## See also` section appended |
| Reverse links | `sources/commercial-courts.md` | `## See also` section appended |
| Reverse index | `docs/cross-reference-map.md` | Section 1b (19-row table) + new maintenance rule |
| CI step | `.github/workflows/validate-datasets.yml` | `python3 scripts/validate_cross_refs.py` added |
| Design spec | `docs/superpowers/specs/2026-05-25-reverse-discovery-seam-design.md` | Full design decisions |
| Plan | `docs/superpowers/plans/2026-05-25-reverse-discovery-seam.md` | 9-task incremental plan |

---

## How the Validator Works

`scripts/validate_cross_refs.py` runs four checks on every CI push:

| Check | Behavior | On failure |
|---|---|---|
| **Check 1** | Source cited by a skill has no `## See also` section | FAIL (CI blocks) |
| **Check 2** | Source's `## See also` is missing a skill that cites it | FAIL (CI blocks) |
| **Check 3** | Source's `## See also` lists a skill that doesn't cite it (phantom) | FAIL (CI blocks) |
| **Check 4** | `cross-reference-map.md` Section 1b is missing a confirmed pair | WARN only |

**Key design decisions:**
- Heading detection is alias-based (`REGULATIONS_HEADING_ALIASES`), not hardcoded to `§11`. Adding a new alias is a one-line change.
- `sources/regulation-index.md` is in `EXCLUDED_SOURCES` — it's a meta-document cited only for citation format, not a substantive legal source.
- Check 3 scans ALL `sources/*.md` (not just those cited by skills), catching phantoms in uncited sources.
- `--fix` flag is reserved for a future auto-repair mode; currently prints a not-implemented message and exits 0.

**Run locally:**
```bash
python3 scripts/validate_cross_refs.py    # validate
pytest tests/test_validate_cross_refs.py  # run tests only
```

---

## Current Repository Map

```
skills/           7 files — reasoning guides per legal domain
  arbitration.md
  commercial-dispute.md
  compliance-check.md
  contract-review.md
  labor-law-analysis.md
  legal-drafting.md
  real-estate-contracts.md

sources/          substantive legal reference files
  civil-transactions-law.md   ← has See also (6 skills)
  labor-law.md                ← has See also (3 skills)
  companies-law.md            ← has See also (4 skills)
  pdpl.md                     ← has See also (3 skills)
  commercial-courts.md        ← has See also (3 skills)
  saudi-laws.md               ← no See also (no skill cites it by path yet)
  regulation-index.md         ← excluded from validation (meta-document)
  e-commerce-law.md           ← no skills cite it yet
  evidence-law.md             ← no skills cite it yet
  legal-profession-law.md     ← no skills cite it yet
  open-data-judicial-sources.md
  whistleblower-protection.md
  fiqh-judicial-references/
  judicial-decisions/

prompts/          3 prompt templates
  review-contract.md
  risk-analysis.md
  draft-notice.md

examples/         13 worked examples

scripts/
  validate_cross_refs.py   ← new
  validate_dataset.py
  build_dataset.py
  ocr_pdf_pages.py

tests/
  test_validate_cross_refs.py   ← new (79 tests)
  test_validate_dataset.py
  test_build_dataset.py
```

---

## Known Gaps (Not Blocking)

These were identified during implementation and are follow-on work:

### 1. `skills/contract-review.md §11` — validator cannot see its citations
**Problem:** The regulations section uses regulation names in prose (e.g., "نظام المعاملات المدنية") rather than backtick-quoted `sources/` paths. The validator's regex `sources/[\w-]+\.md` finds no matches, so `contract-review.md` appears to cite nothing.  
**Impact:** Check 1 and Check 2 won't fire for this skill. No CI failure, but the reverse seam is incomplete for `contract-review.md`.  
**Fix:** Add backtick-quoted paths like `` `sources/civil-transactions-law.md` `` to `skills/contract-review.md §11`. After the fix, the 5 source files it cites will automatically require `contract-review.md` in their `## See also` sections, and CI will enforce it.

### 2. `skills/real-estate-contracts.md §11` — incomplete section
**Problem:** The §11 section contains "TO VERIFY" placeholders and is not fully populated.  
**Impact:** Check 4 warnings will appear (non-blocking). No FAIL.  
**Fix:** Audit and complete the §11 section when the real-estate domain is prioritized.

### 3. `sources/saudi-laws.md` — no `## See also` yet
**Problem:** No skill currently cites `sources/saudi-laws.md` by a `sources/` path in its regulations section.  
**Impact:** No validator failures. But the architectural report noted `saudi-laws.md` is a general-purpose reference that may gain citing skills.  
**Fix:** No action needed now. If a skill adds `sources/saudi-laws.md` to its §11, CI will require the See also section.

---

## Next Architectural Candidates

From the architecture review report (run earlier today). In priority order:

### Candidate 2 — Standardize prompt→skill seam declaration
**Problem:** `prompts/draft-notice.md` and `prompts/risk-analysis.md` don't declare which skill they implement. A reader can't navigate prompt → skill.  
**Effort:** Low. Add a `## Implements / يُطبِّق` frontmatter or header section to each prompt file, then update Section 2 in `cross-reference-map.md`.  
**Validator:** Could extend `validate_cross_refs.py` or add a separate `validate_prompts.py`.

### Candidate 3 — Skill-to-example coverage index
**Problem:** `docs/cross-reference-map.md` Section 3 shows `skills/commercial-dispute.md`, `skills/compliance-check.md`, and `skills/legal-drafting.md` all have no worked examples. Gaps are visible in the map but not enforced.  
**Effort:** Medium. Add a completeness check (warn if a skill has no example).

### Candidate 4 — Connect related skills at explicit seams
**Problem:** `skills/arbitration.md` and `skills/commercial-dispute.md` overlap but have no explicit cross-link. Same for `skills/compliance-check.md` ↔ `skills/labor-law-analysis.md`.  
**Effort:** Low documentation change. Add a `## Related skills / مهارات ذات صلة` section to affected skills.

### Candidate 5 — Repair `real-estate-contracts.md §11`
**Problem:** Incomplete "TO VERIFY" entries in the regulations section.  
**Effort:** Domain research required. Blocked until real-estate domain is prioritized.

---

## Maintenance Rules (for whoever touches skills or sources next)

**When adding a new `sources/` file:**
1. If any existing skill's §11 cites it → add `## See also / انظر أيضًا` to the new source file
2. Add a row to Section 1b in `docs/cross-reference-map.md`
3. Run: `python3 scripts/validate_cross_refs.py`

**When editing a skill's §11 (adding or removing a source citation):**
1. Update Section 1b in `docs/cross-reference-map.md`
2. Update `## See also` in every `sources/` file added or removed from §11
3. Run: `python3 scripts/validate_cross_refs.py`
4. CI will catch any remaining inconsistencies on push

**Citation format in §11** (required for the validator to detect citations):
```markdown
`sources/labor-law.md`, `sources/pdpl.md`
```
or as a markdown link:
```markdown
[نظام العمل](../sources/labor-law.md)
```
Prose-only mentions (e.g., "نظام المعاملات المدنية") are **not** detected by the validator.

---

## CI Workflow

`.github/workflows/validate-datasets.yml` steps (in order):

1. `pytest` — 79 unit tests
2. `python3 scripts/validate_cross_refs.py` — reverse-seam validation ← new
3. `python3 scripts/validate_dataset.py` — main dataset
4. Validate each `datasets/examples/*.csv`
5. `python3 scripts/build_dataset.py`
6. Validate generated dataset

All steps passed on PR #27. CI runs on every push and PR.

---

## Contacts / References

- **Repo:** https://github.com/Samix2026/saudi-legal-ai-framework
- **PR #27 (merged):** https://github.com/Samix2026/saudi-legal-ai-framework/pull/27
- **Design spec:** `docs/superpowers/specs/2026-05-25-reverse-discovery-seam-design.md`
- **Implementation plan:** `docs/superpowers/plans/2026-05-25-reverse-discovery-seam.md`
- **Cross-reference map:** `docs/cross-reference-map.md`
