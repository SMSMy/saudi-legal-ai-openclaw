# Reverse-Discovery Seam — Design Spec

**Date:** 2026-05-25
**Status:** Awaiting implementation
**Scope:** sources→skills only (Phase 1 of bidirectional cascade)

---

## Problem

The framework's cascade is unidirectional: prompts → skills → sources. A user or AI starting from a `sources/` file has no path to the skills that implement it or the examples that demonstrate it. Coverage gaps are invisible without manual grep. The existing `docs/cross-reference-map.md` captures the forward direction (skills→sources in §1) but has no reverse.

---

## Decisions

| Question | Decision |
|---|---|
| Where does the reverse seam live? | Both: `cross-reference-map.md` as authoritative index + "See also" in each `sources/` file |
| Scope | sources→skills only (this spec); skills→examples and skills→prompts in follow-on |
| Maintenance | Script-enforced CI validation |
| "See also" format | Skill name + link + which section of that skill cites this source |

---

## Invariant

> **If a `sources/` file is cited in any `skills/*.md` §11 (Relevant Regulations), it must have a `## See also / انظر أيضًا` section.**

Missing section = CI failure. This is checked before link correctness.

---

## Change 1 — `docs/cross-reference-map.md`

Add **Section 1b** immediately after the existing Section 1 (Skills ↔ Sources):

```markdown
## 1b. Sources → Skills — Reverse Index / المصادر → المهارات (فهرس عكسي)

> هذا الجدول مصدر الحقيقة للـ CI. أي تغيير في §11 لأي skill يستلزم تحديثه.
> This table is the CI source of truth. Any change to a skill's §11 requires updating it.

| Source File | Cited by Skill | Section | طبيعة الاستخدام |
|---|---|---|---|
| `sources/civil-transactions-law.md` | `skills/contract-review.md` | §11 | المصدر الرئيسي للعقود المدنية |
| `sources/civil-transactions-law.md` | `skills/legal-drafting.md` | §11 | مرجع مبادئ الصياغة |
| `sources/labor-law.md` | `skills/contract-review.md` | §11 | نطاق العقود الوظيفية |
| `sources/labor-law.md` | `skills/labor-law-analysis.md` | §11 | النظام الأساسي للمهارة |
| `sources/labor-law.md` | `skills/compliance-check.md` | §11 | نطاقات / Saudization |
| `sources/companies-law.md` | `skills/contract-review.md` | §11 | الشركات كطرف متعاقد |
| `sources/companies-law.md` | `skills/compliance-check.md` | §11 | متطلبات الحوكمة |
| `sources/pdpl.md` | `skills/contract-review.md` | §11 | بنود البيانات الشخصية |
| `sources/pdpl.md` | `skills/compliance-check.md` | §11 | النظام الأساسي للامتثال |
| `sources/commercial-courts.md` | `skills/contract-review.md` | §11 | اختصاص المحكمة |
| `sources/commercial-courts.md` | `skills/commercial-dispute.md` | §11 | النظام الأساسي للمهارة |
| `sources/saudi-laws.md` | `skills/commercial-dispute.md` | §11 | مرجع عام للنزاعات |
| `sources/saudi-laws.md` | `skills/legal-drafting.md` | §11 | مرجع عام للصياغة |
```

> **Note:** These rows are illustrative based on current cross-reference-map.md §1 data. The implementation step must audit each `skills/*.md` §11 directly to confirm and complete the table before adding it.

Also update the **maintenance rule** for "When Adding a New Source" to include:

```
✅ أضف "See also" في ملف الـ source الجديد إذا أشار إليه أي skill في §11
```

And add a new maintenance rule **"When Editing a Skill's §11"**:

```
✅ حدّث Section 1b في cross-reference-map.md
✅ حدّث "See also" في كل sources/ file أُضيف أو حُذف من §11
✅ شغّل: python scripts/validate_cross_refs.py
```

---

## Change 2 — `## See also` in each `sources/` file

Add this section at the **end** of each source file that is cited by at least one skill. Five files need it today:

- `sources/civil-transactions-law.md`
- `sources/labor-law.md`
- `sources/companies-law.md`
- `sources/pdpl.md`
- `sources/commercial-courts.md`
- `sources/saudi-laws.md`

**Section format** (bilingual, consistent across all files):

```markdown
---

## See also / انظر أيضًا

المهارات التي تستند إلى هذا المصدر / Skills that cite this source:

| Skill | Section | طبيعة الاستخدام |
|-------|---------|----------------|
| [skills/contract-review.md](../skills/contract-review.md) | §11 الأنظمة المرتبطة | المصدر الرئيسي للعقود المدنية |
| [skills/legal-drafting.md](../skills/legal-drafting.md) | §11 الأنظمة المرتبطة | مرجع مبادئ الصياغة |

> للاطلاع على الفهرس الكامل: [`docs/cross-reference-map.md` — Section 1b](../docs/cross-reference-map.md)
```

Rules:
- The section is added **only** if the source is cited by at least one skill's §11.
- The link text for each row uses the relative path from `sources/` to `skills/` (`../skills/`).
- The footer link always points to `cross-reference-map.md` Section 1b.

---

## Change 3 — `scripts/validate_cross_refs.py`

New script. Runs standalone; no new dependencies beyond the Python stdlib already used by `validate_dataset.py`.

### What it parses

**From each `skills/*.md`:**
Extract the §11 section (heading contains "Relevant Regulations" or "الأنظمة المرتبطة"). Within that section, collect every `sources/` path mentioned (via regex on backtick-quoted paths or markdown links).

**From each `sources/*.md`:**
Detect whether a `## See also` section exists. If it does, extract every `skills/` path listed in it.

### Checks (in order)

**Check 1 — Missing "See also" (invariant)**
For every `(source_file, skill_file)` pair found in skills §11: if `source_file` has no `## See also` section → **FAIL**.

```
ERROR: sources/labor-law.md is cited by skills/labor-law-analysis.md §11
       but has no "## See also" section.
```

**Check 2 — Missing reverse link**
For every `(source_file, skill_file)` pair found in skills §11: if `source_file`'s "See also" does not list `skill_file` → **FAIL**.

```
ERROR: sources/labor-law.md "See also" is missing skills/compliance-check.md
       (cited in skills/compliance-check.md §11).
```

**Check 3 — Phantom reference**
For every `skill_file` listed in a `source_file`'s "See also": if that skill's §11 does not cite the source → **FAIL**.

```
ERROR: sources/labor-law.md "See also" lists skills/legal-drafting.md
       but skills/legal-drafting.md §11 does not cite sources/labor-law.md.
```

**Check 4 — Cross-reference-map.md sync**
For every `(source_file, skill_file)` pair confirmed by checks 1–3: if Section 1b of `cross-reference-map.md` does not contain a row for that pair → **WARN** (not FAIL — the map is documentation, not enforcement).

```
WARNING: cross-reference-map.md Section 1b is missing row:
         sources/pdpl.md → skills/compliance-check.md
```

### Exit codes

- `0` — all checks pass
- `1` — any FAIL (Check 1, 2, or 3)
- Warnings (Check 4) print but do not affect exit code

### Integration

Add to `.github/workflows/validate-datasets.yml` as a second step in the existing validation job, after `validate_dataset.py`:

```yaml
- name: Validate cross-references
  run: python scripts/validate_cross_refs.py
```

---

## Files changed

| File | Change |
|---|---|
| `docs/cross-reference-map.md` | Add Section 1b reverse index table + two maintenance rules |
| `sources/civil-transactions-law.md` | Add `## See also` |
| `sources/labor-law.md` | Add `## See also` |
| `sources/companies-law.md` | Add `## See also` |
| `sources/pdpl.md` | Add `## See also` |
| `sources/commercial-courts.md` | Add `## See also` |
| `sources/saudi-laws.md` | Add `## See also` |
| `scripts/validate_cross_refs.py` | New file |
| `.github/workflows/validate-datasets.yml` | Add validation step |

---

## Out of scope (follow-on)

- skills→examples reverse links (Candidate 3 in architecture report)
- skills→prompts seam declaration (Candidate 2)
- skills cross-reference seams (Candidate 4)
- Completing `real-estate-contracts.md §11` (Candidate 5 — its incomplete §11 will produce Check 4 warnings but not block CI, since Check 4 is WARN not FAIL)
