# citation-index.md
# فهرس الاستشهادات الفقهية القضائية — Fiqh Citation Index

**الغرض:** يحتوي هذا الجدول على المراجع الفقهية التي استشهد بها قضاة سعوديون صراحةً في تسبيب أحكام موثَّقة. كل سجل مرتبط بـ `case_id` المصدر في `datasets/judicial-reasoning/cases/`.

**تحذير:** كل إحالة لرقم صفحة أو طبعة مُستمَدة من OCR تحمل `verification_status: draft` ولا تُعتمد للاستشهاد قبل التحقق البشري من المصدر المطبوع.

---

## مخطط الجدول / Table Schema

| الحقل | الوصف |
|-------|--------|
| `reference_id` | معرّف فريد: `FQR-{سنة}-{NNN}` |
| `book_title_ar` | اسم الكتاب بالعربية |
| `book_title_en` | اسم الكتاب بالإنجليزية |
| `author` | اسم المؤلف |
| `madhhab` | المذهب الفقهي |
| `citation_as_seen_in_judgment` | النص الحرفي للإحالة كما ظهر في الحكم (من OCR) |
| `related_case_id` | معرّف ملف الاستخراج المصدر |
| `related_pdf` | ملف PDF المصدر |
| `page_in_pdf` | صفحة PDF التي ظهرت فيها الإحالة |
| `topic` | الموضوع الفقهي المستشهَد به |
| `verification_status` | حالة التحقق من رقم الصفحة والطبعة |
| `notes` | ملاحظات التحقق والغموض |

---

## السجلات / Records

### FQR-1435-001

| الحقل | القيمة |
|-------|--------|
| `reference_id` | FQR-1435-001 |
| `book_title_ar` | كشاف القناع عن متن الإقناع |
| `book_title_en` | Kashshaf al-Qina' (Uncovering the Veil from the Text of al-Iqna') |
| `author` | منصور بن يونس البهوتي (Mansur ibn Yunus al-Buhuti, d. 1051H) |
| `madhhab` | حنبلي (Hanbali) |
| `citation_as_seen_in_judgment` | "كشاف القناع (البهوتي، 1/474): العيب نقص عين المبيع" [OCR_UNCERTAIN — رقم المجلد والصفحة قد يكون محرَّفاً] |
| `related_case_id` | JD-1435-002 |
| `related_pdf` | sources/judicial-decisions/1435/1.pdf |
| `page_in_pdf` | 247–254 |
| `topic` | تعريف العيب الموجِب لخيار العيب في عقد البيع — خيار العيب |
| `verification_status` | draft |
| `notes` | TO VERIFY — رقم الصفحة (1/474) مُستخرَج من OCR. الطبعة المرجَّحة هي طبعة دار الكتب العلمية أو دار عالم الكتب — يحتاج مقارنة بالمطبوع. الإحالة ذُكرت في حكم الدرجة الأولى لا في صك محكمة الاستئناف. |

---

### FQR-1435-002

| الحقل | القيمة |
|-------|--------|
| `reference_id` | FQR-1435-002 |
| `book_title_ar` | الروض المربع شرح زاد المستقنع |
| `book_title_en` | al-Rawd al-Murbi' (The Flowering Garden — Commentary on Zad al-Mustaqni') |
| `author` | منصور بن يونس البهوتي (Mansur ibn Yunus al-Buhuti, d. 1051H) |
| `madhhab` | حنبلي (Hanbali) |
| `citation_as_seen_in_judgment` | "الروض المربع (مؤسسة الرسالة، ط.3 1437هـ، ص275): أو ظهر أن المشتري معسر فللبائع الفسخ لتعذر الثمن عليه كما لو كان المشتري مفلساً" [OCR_UNCERTAIN] |
| `related_case_id` | JD-1435-005 |
| `related_pdf` | sources/judicial-decisions/1435/1.pdf |
| `page_in_pdf` | 296–301 |
| `topic` | إعسار المشتري وحق البائع في فسخ عقد البيع — انفساخ العقد |
| `verification_status` | draft |
| `notes` | TO VERIFY — الإحالة تُحدد الطبعة (مؤسسة الرسالة، ط.3، 1437هـ) والصفحة (275) — لكن كليهما مُستخرَج من OCR وعُرضة للتشويه. التحقق يستلزم مقارنة النص المُستشهَد به مع نص هذه الطبعة تحديداً. |

---

## إحصائيات الفهرس / Index Statistics

| المذهب | عدد الإحالات |
|--------|-------------|
| حنبلي | 2 |
| **الإجمالي** | **2** |

| حالة التحقق | عدد السجلات |
|------------|------------|
| draft | 2 |
| community-reviewed | 0 |
| verified | 0 |

---

## كيفية الإضافة / How to Add

لإضافة سجل جديد:
1. تحقق أن المرجع ظهر صراحةً في حكم قضائي موثَّق داخل `datasets/judicial-reasoning/cases/`
2. انسخ قالب السجل أعلاه واملأه
3. ابدأ الـ `reference_id` بـ `FQR-{سنة هجرية}-{رقم تسلسلي}`
4. استخدم `verification_status: draft` لأي رقم صفحة مُستمَد من OCR
5. حدّث إحصائيات الجدول أعلاه
