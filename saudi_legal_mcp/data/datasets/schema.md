# Dataset Schema / مخطط البيانات

**الملف:** `saudi-contract-risk-dataset.csv`
**عدد الأعمدة:** 16
**الترميز:** UTF-8
**الفاصل:** فاصلة `,`

---

## الأعمدة / Columns

---

### 1. `id`
**النوع:** عدد صحيح (Integer)
**الوصف:** معرّف فريد لكل صف — يزداد بالتسلسل.
**Unique sequential identifier for each row.**

| صحيح ✅ | خطأ ❌ |
|--------|-------|
| `1` | `row_1` |
| `42` | `` (فارغ) |

---

### 2. `contract_type`
**النوع:** نص محدود القيم (Enum)
**الوصف:** نوع العقد الذي يحتوي هذا البند.
**Type of contract containing this clause.**

**القيم المقبولة والمرجع الرسمي / Accepted values & authoritative reference:** [`datasets/enums/contract-types.md`](enums/contract-types.md)

| صحيح ✅ | خطأ ❌ |
|--------|-------|
| `SaaS Agreement` | `SaaS` |
| `Employment Contract` | `عقد` (مبهم جداً) |
| `Cloud Storage Agreement` | `` (فارغ) |

**قيم شائعة / Common values:**
`Employment Contract` | `SaaS Agreement` | `Professional Services Agreement` | `Construction Contract` | `Supply Agreement` | `NDA` | `Shareholder Agreement` | `Franchise Agreement` | `Commercial Agency Agreement` | `Lease Agreement` | `Cloud Storage Agreement`

---

### 3. `clause_category`
**النوع:** نص محدود القيم (Enum)
**الوصف:** تصنيف موضوع البند القانوني.
**Legal topic category of the clause.**

**القيم المقبولة والمرجع الرسمي / Accepted values & authoritative reference:** [`datasets/enums/clause-categories.md`](enums/clause-categories.md)

| صحيح ✅ | خطأ ❌ |
|--------|-------|
| `Jurisdiction & Dispute Resolution` | `Legal Stuff` |
| `Data Protection & Privacy` | `PDPL` (استخدم الاسم الكامل) |
| `Liability` | `` (فارغ) |

**تصنيفات موحَّدة / Standardized categories:**
`Jurisdiction & Dispute Resolution` | `Liability` | `Data Protection & Privacy` | `Intellectual Property` | `Termination` | `Confidentiality` | `Payment Terms` | `Governing Law` | `Force Majeure` | `Warranties` | `Indemnification` | `Employment & Labor` | `Saudization` | `Corporate Governance`

---

### 4. `clause_text`
**النوع:** نص طويل (Long String) — يُحاط بعلامات اقتباس دائمًا
**الوصف:** النص الحرفي (أو المُجرَّد) للبند محل المراجعة. يجب أن يكون افتراضيًا أو مُجرَّدًا — لا نصًا من عقد حقيقي.
**Verbatim or abstracted text of the clause under review. Must be hypothetical or abstracted — not from a real contract.**

| صحيح ✅ | خطأ ❌ |
|--------|-------|
| `"Any disputes shall be submitted to the courts of England."` | نص من عقد حقيقي |
| نص افتراضي واضح | نص يتضمن اسم شركة حقيقية |

**ملاحظة تنسيق:** يجب دائمًا إحاطة هذا الحقل بـ `"..."` لأنه يحتوي فواصل.
**Format note:** Always wrap in `"..."` as it contains commas.

---

### 5. `risk_level`
**النوع:** نص محدود القيم (Enum)
**الوصف:** مستوى خطورة البند.
**Risk level of the clause.**

**القيم المقبولة والمرجع الرسمي / Accepted values & authoritative reference:** [`datasets/enums/risk-levels.md`](enums/risk-levels.md)
**التعريفات التفصيلية / Full definitions:** [`datasets/risk-taxonomy.md`](risk-taxonomy.md)

| القيمة | المعنى |
|--------|-------|
| `critical` | يستوجب إيقاف الإجراء فورًا |
| `high` | يستوجب مراجعة قانونية متخصصة |
| `medium` | يستوجب تعديلًا قبل التوقيع |
| `low` | ملاحظة تحسينية غير عاجلة |

**خطأ شائع:** استخدام `Critical` بحرف كبير أو `HIGH` — القيم بأحرف صغيرة فقط.
**Common error:** Using `Critical` or `HIGH` — values must be lowercase only.

---

### 6. `risk_reason`
**النوع:** نص (String)
**الوصف:** شرح موجز بالإنجليزية لسبب تصنيف هذا البند كخطر.
**Brief English explanation of why this clause is classified as a risk.**

- يجب ألا يحتوي فواصل دون إحاطة بـ `"..."`
- لا يُكرر نص البند — يشرح الإشكالية
- جملة أو جملتان كحد أقصى

- Must not contain unquoted commas
- Does not repeat the clause text — explains the problem
- One or two sentences maximum

---

### 7. `saudi_legal_note`
**النوع:** نص (String) — بالعربية غالبًا
**الوصف:** الملاحظة القانونية في السياق السعودي — الحكم النظامي أو الشرعي المنطبق.
**Legal note in the Saudi context — the applicable regulatory or Sharia ruling.**

- يُكتب بالعربية كلغة أساسية (يمكن الإنجليزية إذا كان الجمهور المستهدف إنجليزيًا)
- يُشير للنظام أو المادة دون نسخ النص الرسمي كاملًا
- يُحاط بـ `"..."` دائمًا لاحتوائه نصًا طويلًا

- Written in Arabic as primary language (English allowed if target audience is English)
- References the regulation or article without copying the full official text
- Always wrapped in `"..."` as it contains long text

---

### 8. `recommended_revision`
**النوع:** نص (String)
**الوصف:** اقتراح عملي لإعادة صياغة البند أو تعديله.
**Practical suggestion for revising or amending the clause.**

- يكون محددًا وقابلًا للتطبيق
- لا يُفسَّر كاستشارة قانونية نهائية
- يُحاط بـ `"..."` دائمًا

- Should be specific and actionable
- Not to be interpreted as final legal advice
- Always wrapped in `"..."`

---

### 9. `related_regulation`
**النوع:** نص (String)
**الوصف:** النظام أو الأنظمة السعودية ذات الصلة بالبند.
**Saudi regulation(s) relevant to this clause.**

**الصيغة الموحَّدة / Standard format:**
`[اسم النظام] ([رقم المرسوم الملكي] [السنة الهجرية])`

| صحيح ✅ | خطأ ❌ |
|--------|-------|
| `Saudi Labor Law (Royal Decree M/51 1426H)` | `Labor Law` (غير محدد) |
| `PDPL (Royal Decree M/19 1443H) Arts. 29-30` | `Saudi law` (مبهم) |

لفصل أكثر من نظام: استخدم ` | `

---

### 10. `requires_escalation`
**النوع:** Boolean نصي (yes / no)
**الوصف:** هل يستوجب هذا البند تصعيدًا فوريًا لمحامٍ مختص؟
**Does this clause require immediate escalation to a specialist attorney?**

| القيمة | المعنى |
|--------|-------|
| `yes` | يجب إيقاف الإجراء ومراجعة محامٍ قبل المضي |
| `no` | يمكن معالجته بتعديل داخلي دون تصعيد فوري |

**راجع `severity-standards.md` لمعايير التصعيد التفصيلية.**

---

### 11. `language`
**النوع:** رمز اللغة (Language code)
**الوصف:** لغة `clause_text` المدخَل.
**Language of the entered `clause_text`.**

| القيمة | المعنى |
|--------|-------|
| `en` | إنجليزية |
| `ar` | عربية |
| `bilingual` | البند موجود بالنسختين |

---

### 12. `industry`
**النوع:** نص محدود القيم (Enum)
**الوصف:** القطاع الاقتصادي الذي ينتمي إليه العقد.
**Economic sector the contract belongs to.**

**القيم المقبولة والمرجع الرسمي / Accepted values & authoritative reference:** [`datasets/enums/industries.md`](enums/industries.md)

**قيم موحَّدة / Standardized values:**
`Technology` | `Professional Services` | `Construction` | `Healthcare` | `Real Estate` | `Finance` | `Retail` | `Logistics` | `Energy` | `Education` | `Government` | `General`

---

### 13. `source_type`
**النوع:** نص محدود القيم (Enum)
**الوصف:** مصدر البند المُدخَل.
**Source of the entered clause.**

| القيمة | المعنى |
|--------|-------|
| `hypothetical` | افتراضي مُنشأ لأغراض التوضيح |
| `abstracted` | مستخلص من نمط حقيقي مع إخفاء كامل |
| `published_case` | مستند لقضية أو حكم منشور |
| `standard_form` | مستخلص من عقد نموذجي معروف ومُعدَّل |

---

### 14. `reviewed_by_lawyer`
**النوع:** Boolean نصي (yes / no)
**الوصف:** هل راجع محامٍ مرخَّص في المملكة هذا الصف وأقرَّ دقته؟
**Has a licensed Saudi attorney reviewed this row and confirmed its accuracy?**

| القيمة | المعنى |
|--------|-------|
| `yes` | مراجَع ومُعتمَد من محامٍ مرخَّص |
| `no` | لم يُراجَع بعد — يُعامَل كمسودة |

---

### 15. `notes`
**النوع:** نص (String) — اختياري
**الوصف:** أي ملاحظات إضافية للمساهم أو المراجع.
**Any additional notes from the contributor or reviewer.**

- سياق إضافي غير ملائم لبقية الأعمدة
- ملاحظة عن شيوع هذا النمط في قطاع معين
- عند الحالة `superseded` يجب ذكر ID البديل: `superseded by row <ID>`

---

### 16. `verification_status`
**النوع:** نص محدود القيم (Enum)
**الوصف:** مرحلة دورة حياة التحقق القانوني لهذا الصف.
**Legal verification lifecycle stage of this row.**

**القيم المقبولة والمرجع الرسمي / Accepted values & authoritative reference:** [`datasets/enums/verification-status.md`](enums/verification-status.md)

**التوثيق الكامل / Full documentation:** [`docs/legal-verification-lifecycle.md`](../docs/legal-verification-lifecycle.md)

| القيمة | المعنى | يُسمح في production |
|--------|-------|---------------------|
| `draft` | مسودة أولية — لم تُراجَع | ❌ |
| `pending-review` | قيد المراجعة القانونية | ❌ |
| `community-reviewed` | مراجَع مجتمعيًا (باحث / ممارس / مساهم) ★ | ⚠️ بتحفظ مع إفصاح |
| `reviewed` | مراجَع من مختص (غير محامٍ) | ⚠️ بتحفظ |
| `verified` | مُتحقَّق من محامٍ مرخَّص | ✅ |
| `deprecated` | متقادم — تغير التشريع | ❌ |
| `superseded` | مستبدَل بصف أحدث | ❌ |

★ المسار الأساسي: `draft` → `community-reviewed` → `verified`

**الحالة الافتراضية / Default:** `draft` — استخدم هذه القيمة دائمًا عند إضافة صفوف جديدة.

**Default:** `draft` — always use this value when adding new rows.

**قاعدة الاتساق / Consistency rule:**
إذا كانت `verification_status = verified` فيجب أن تكون `reviewed_by_lawyer = yes`.
If `verification_status = verified`, then `reviewed_by_lawyer` must be `yes`.

---

## ملاحظات التنسيق العامة / General Formatting Notes

```
- الترميز: UTF-8 — ضروري للنصوص العربية
- الفاصل: فاصلة , فقط
- الأعمدة التي تحتوي فواصل أو نصًا طويلًا: تُحاط بـ "..."
- الأعمدة الفارغة: تُترك فارغة بين فاصلتين (,,) لا تُملأ بـ N/A أو -
- لا سطور فارغة بين الصفوف
- لا مسافات زائدة قبل أو بعد الفاصلة
```

```
- Encoding: UTF-8 — required for Arabic text
- Delimiter: comma , only
- Columns containing commas or long text: wrap in "..."
- Empty columns: leave empty between commas (,,) — do not fill with N/A or -
- No blank lines between rows
- No extra spaces before or after the comma
```
