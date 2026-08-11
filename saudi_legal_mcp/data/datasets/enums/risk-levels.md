# Enum: risk_level

**عمود:** `risk_level`
**Column:** `risk_level`

هذا الملف هو المرجع الرسمي للقيم المقبولة في عمود `risk_level` بالـ dataset.
This file is the authoritative reference for accepted values in the `risk_level` column.

**المصدر التفصيلي / Full definitions:** `datasets/risk-taxonomy.md`
**المُتحقَّق بواسطة / Validated by:** `scripts/validate_dataset.py`

---

## القيم المقبولة / Accepted Values

| القيمة | المعنى العربي | English Meaning | يوقف التوقيع؟ |
|--------|--------------|-----------------|--------------|
| `critical` | حرج | Stop proceeding immediately | نعم — فورًا |
| `high` | مرتفع | Urgent escalation required | نعم — حتى المعالجة |
| `medium` | متوسط | Amend before signing | يُنصح |
| `low` | منخفض | Improvement note | لا |

## قواعد التنسيق / Format Rules

- القيم بأحرف إنجليزية صغيرة فقط — `critical` لا `Critical` ولا `CRITICAL`
- Values must be lowercase English only — `critical` not `Critical` or `CRITICAL`
- لا يُسمح بالفراغ — الحقل إلزامي
- Empty values are not allowed — field is required
