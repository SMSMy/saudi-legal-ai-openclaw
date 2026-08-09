# مخطط فهرس المجموعة القضائية
# Judicial Corpus Index Schema

**المجلد / Directory:** `datasets/judicial-index/`
**الغرض / Purpose:** فهرسة محتوى ملفات PDF القضائية قبل أي استخراج للـ reasoning
**Purpose:** Index the content of judicial PDF files before any reasoning extraction
**عدد الحقول / Field count:** 13

---

## ⚠️ ملاحظة / Note

> هذا المخطط للفهرسة **فقط** — لا يحتوي على reasoning أو استخلاص قضائي.
> الاستخراج يتم لاحقاً في `datasets/judicial-reasoning/` بعد اكتمال الفهرس.
>
> This schema is for **indexing only** — it contains no reasoning or judicial extraction.
> Extraction happens later in `datasets/judicial-reasoning/` after the index is complete.

---

## الحقول / Fields

---

### 1. `index_id`
**النوع / Type:** نص — معرّف فريد (String — unique identifier)
**الوصف / Description:**
معرّف فريد للصف في الفهرس — لا علاقة له بأي رقم رسمي.
Unique identifier for the index row — unrelated to any official number.

**الصيغة / Format:** `IDX-{سنة هجرية}-{رقم PDF}-{رقم تسلسلي}` — مثال: `IDX-1435-01-001`

| صحيح ✅ | خطأ ❌ |
|--------|-------|
| `IDX-1435-01-001` | `1435/1/هبة` |
| `IDX-1435-03-012` | رقم الملف القضائي |

---

### 2. `source_pdf`
**النوع / Type:** نص (String)
**الوصف / Description:**
المسار النسبي لملف PDF المصدر من جذر المشروع.
Relative path to the source PDF from the project root.

**الصيغة / Format:** `sources/judicial-decisions/{سنة}/{رقم}.pdf`
**مثال / Example:** `sources/judicial-decisions/1435/1.pdf`

---

### 3. `volume_year`
**النوع / Type:** عدد صحيح — سنة هجرية (Integer — Hijri year)
**الوصف / Description:**
السنة الهجرية التي تغطيها هذه المجلدة — مستخلَصة من اسم المجلد.
The Hijri year covered by this volume — derived from the directory name.

**مثال / Example:** `1435`

---

### 4. `volume_number`
**النوع / Type:** عدد صحيح (Integer)
**الوصف / Description:**
رقم ملف PDF داخل مجلد السنة — يُقابل اسم الملف الرقمي.
The PDF file number within the year directory — corresponds to the numeric filename.

**مثال / Example:** `1` للملف `1.pdf`

---

### 5. `main_domain`
**النوع / Type:** نص محدود القيم (Enum)
**الوصف / Description:**
المجال القانوني الرئيسي للقسم المُفهرَس.
The primary legal domain of the indexed section.

| القيمة | المعنى |
|--------|-------|
| `civil` | مدني — أحوال شخصية، عقود، حيازة |
| `commercial` | تجاري — شركات، عقود تجارية، إفلاس |
| `labor` | عمالي — نزاعات العمل والأجور |
| `administrative` | إداري — نزاعات مع جهات حكومية |
| `criminal` | جنائي — خارج نطاق المشروع عادةً |
| `mixed` | يشمل أكثر من مجال |
| `unknown` | غير محدد — يحتاج قراءة يدوية |

---

### 6. `subcategory`
**النوع / Type:** نص (String)
**الوصف / Description:**
العنوان الفرعي كما يظهر في فهرس PDF — النص الحرفي من الفهرس.
The subcategory title as it appears in the PDF index — verbatim text from the index.

**أمثلة / Examples:** `هبة وعطية` · `إعسار` · `عقار` · `إخلاء عقار` · `استرداد حيازة`

**ملاحظة / Note:** لا تُترجم ولا تُعدِّل — اكتب النص كما هو في الفهرس.
Do not translate or modify — write the text exactly as it appears in the index.

---

### 7. `start_page`
**النوع / Type:** عدد صحيح (Integer)
**الوصف / Description:**
رقم أول صفحة من هذا القسم في الـ PDF — كما يظهر في فهرس PDF.
First page number of this section in the PDF — as shown in the PDF index.

**ملاحظة / Note:** يُستخلَص من فهرس الـ PDF يدوياً. ضع `0` إذا لم تتأكد وأضف `TO VERIFY` في `notes`.

---

### 8. `end_page`
**النوع / Type:** عدد صحيح (Integer)
**الوصف / Description:**
رقم آخر صفحة من هذا القسم — بداية القسم التالي ناقص واحد.
Last page number of this section — start of the next section minus one.

**ملاحظة / Note:** يُستخلَص من فهرس الـ PDF يدوياً. ضع `0` إذا لم تتأكد وأضف `TO VERIFY` في `notes`.

---

### 9. `estimated_case_count`
**النوع / Type:** عدد صحيح (Integer)
**الوصف / Description:**
تقدير عدد الأحكام في هذا القسم — مبني على عدد الصفحات أو عد يدوي تقريبي.
Estimated number of rulings in this section — based on page count or approximate manual count.

**ملاحظة / Note:** تقدير — ليس عدًّا دقيقاً. ضع `0` إذا لم تتمكن من التقدير.

---

### 10. `court_type`
**النوع / Type:** نص محدود القيم (Enum)
**الوصف / Description:**
نوع المحكمة المُصدِرة للأحكام في هذا القسم.
Type of court that issued the rulings in this section.

**القيم / Values:** نفس قيم `court_type` في `datasets/judicial-reasoning/schema.md`
`commercial` · `labor` · `administrative` · `civil` · `appellate` · `supreme` · `unknown`

---

### 11. `extraction_priority`
**النوع / Type:** نص محدود القيم (Enum)
**الوصف / Description:**
الأولوية المُقترَحة لاستخراج الـ reasoning من هذا القسم.
Suggested priority for extracting reasoning from this section.

| القيمة | المعنى |
|--------|-------|
| `high` | ذو صلة مباشرة بأنواع عقود مُغطّاة في المشروع |
| `medium` | ذو صلة غير مباشرة أو يحتاج مراجعة أولى |
| `low` | خارج النطاق الحالي للمشروع أو صعب الاستخراج |
| `skip` | لا استخراج — جنائي أو أحوال شخصية خارج النطاق |

---

### 12. `verification_status`
**النوع / Type:** نص محدود القيم (Enum)
**الوصف / Description:**
حالة التحقق من بيانات هذا الصف في الفهرس — نفس قيم الـ dataset الرئيسي.
Verification status of this index row's data — same values as the main dataset.

**القيم / Values:** `draft` · `pending-review` · `community-reviewed` · `reviewed` · `verified` · `deprecated` · `superseded`
**الافتراضي / Default:** `draft`
**المسار الأساسي / Primary path:** `draft` → `community-reviewed` → `verified`

---

### 13. `notes`
**النوع / Type:** نص (String) — اختياري
**الوصف / Description:**
ملاحظات تتعلق بهذا القسم: صعوبة القراءة، تداخل مع قسم آخر، أرقام صفحات تحتاج تحقق.
Notes about this section: readability issues, overlap with another section, page numbers needing verification.

**استخدام TO VERIFY:** `TO VERIFY — [وصف موجز للجزء غير المؤكد]`

---

## الترتيب الموحَّد للحقول / Standard Field Order

```
index_id, source_pdf, volume_year, volume_number, main_domain, subcategory,
start_page, end_page, estimated_case_count, court_type, extraction_priority,
verification_status, notes
```

---

## الملفات المرتبطة / Related Files

| الملف | العلاقة |
|-------|---------|
| [`README.md`](README.md) | دليل استخدام الفهرس |
| [`judicial-corpus-index.csv`](judicial-corpus-index.csv) | بيانات الفهرس الفعلية |
| [`datasets/judicial-reasoning/schema.md`](../judicial-reasoning/schema.md) | مخطط الاستخراج اللاحق |
| [`sources/judicial-decisions/README.md`](../../sources/judicial-decisions/README.md) | سياق مجموعة الأحكام |
