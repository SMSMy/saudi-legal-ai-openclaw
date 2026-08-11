# فهرس المجموعة القضائية
# Judicial Corpus Index

**المجلد / Directory:** `datasets/judicial-index/`
**المرحلة في سير العمل / Workflow stage:** الفهرسة — قبل الاستخراج
**Workflow stage:** Indexing — before extraction

---

## ⚠️ ملاحظة / Note

> هذا المجلد يحتوي فهرس محتوى الـ PDFs **فقط** — لا reasoning ولا استخلاص قضائي.
> الاستخراج يتم لاحقاً في `datasets/judicial-reasoning/` بعد اكتمال الفهرس ومراجعته.
>
> This directory contains PDF content **indexing only** — no reasoning or judicial extraction.
> Extraction happens later in `datasets/judicial-reasoning/` after the index is complete and reviewed.

---

## 1. لماذا نعمل Indexing قبل Extraction / Why Index Before Extraction

الفهرسة أولاً تحل ثلاث مشكلات تظهر عند البدء بالاستخراج مباشرة:

Indexing first solves three problems that arise when starting extraction immediately:

### المشكلة الأولى: لا تعرف ماذا عندك
14 ملف PDF يمثّل مئات الصفحات من الأحكام. بدون فهرس لا تعرف أي أقسام موجودة، ولا أيها ذو أولوية، ولا كيف توزع العمل.

14 PDF files representing hundreds of pages of rulings. Without an index you don't know which sections exist, which are priority, or how to distribute the work.

### المشكلة الثانية: التكرار
بدون فهرس مركزي قد يستخرج مساهمان من نفس القسم دون علم كل منهما بالآخر.

Without a central index, two contributors may extract from the same section without knowing about each other.

### المشكلة الثالثة: ضياع السياق
حكم مُجرَّد عن سياقه في مجلّد الأحكام أصعب تحققاً. الفهرس يحفظ الرابط بين الاستخراج ومصدره.

A ruling isolated from its context in the decisions volume is harder to verify. The index preserves the link between the extraction and its source.

### سير العمل الصحيح / Correct Workflow

```
PDF files في sources/judicial-decisions/
        │
        ▼ (الفهرسة — هذا المجلد)
datasets/judicial-index/judicial-corpus-index.csv
        │
        ▼ (اختيار الأقسام بناءً على extraction_priority)
        │
        ▼ (الاستخراج)
datasets/judicial-reasoning/{ملفات الاستخراج}
        │
        ▼ (التحقق)
skills/ و datasets/ الرئيسية
```

---

## 2. كيف نقرأ الفهرس من PDF / How to Read the Index from a PDF

الـ PDFs في هذا المشروع مُحوَّلة بالمسح الضوئي (scanned) — لا يمكن استخراج نصها آلياً. الفهرسة تتم يدوياً:

The PDFs in this project are scanned — text cannot be extracted automatically. Indexing is done manually:

### الخطوات / Steps

**الخطوة 1:** افتح الـ PDF في قارئ PDF يدعم الأرقام.

**الخطوة 2:** ابحث عن صفحة الفهرس (عادةً في بداية الملف). في مجلدات الأحكام القضائية السعودية يظهر الفهرس بعنوان "فهرس الموضوعات" أو "المحتويات".

**الخطوة 3:** لكل موضوع في الفهرس، سجّل:
- اسم الموضوع كما هو (لا تُترجم)
- رقم الصفحة المذكور في الفهرس → `start_page`
- رقم بداية الموضوع التالي ناقص واحد → `end_page`

**الخطوة 4:** أضف صفاً في `judicial-corpus-index.csv` بالقيم الصحيحة وغيّر `start_page` و`end_page` من `0` إلى الأرقام الفعلية، وأزل `TO VERIFY` من `notes` إذا تحققت.

**ملاحظة بشأن الأرقام الحالية:** الصفوف الحالية تحتوي `start_page = 0` و`end_page = 0` لأن الـ PDF مقروء بالمسح الضوئي ولم تُستخلَص أرقام الصفحات بعد. يجب تحديثها يدوياً من فهرس الـ PDF.

---

## 3. كيف نضيف نطاق صفحات جديد / How to Add a New Page Range

لإضافة موضوع جديد من نفس الـ PDF أو من PDF مختلف:

To add a new topic from the same PDF or a different one:

```
1. احدد رقم index_id التالي للملف:
   IDX-{volume_year}-{volume_number بخانتين}-{رقم تسلسلي بثلاث خانات}
   مثال: IDX-1435-01-006 للموضوع السادس من 1.pdf

2. اقرأ start_page و end_page من فهرس الـ PDF يدوياً

3. حدّد main_domain و subcategory من عنوان الموضوع

4. حدّد extraction_priority بناءً على الجدول أدناه

5. اترك verification_status = draft

6. أضف TO VERIFY في notes لأي حقل غير مؤكد
```

---

## 4. كيف نختار extraction_priority / How to Choose extraction_priority

الأولوية تعكس مدى صلة الموضوع بالعقود التجارية والعمالية التي يُركّز عليها المشروع:

Priority reflects how relevant the topic is to the commercial and labor contracts the project focuses on:

| الأولوية | متى تُستخدم | أمثلة |
|---------|------------|-------|
| `high` | صلة مباشرة بأنواع عقود في datasets/ | إعسار، ضمان، وكالة تجارية، عقد عمل |
| `medium` | صلة غير مباشرة أو تحتاج مراجعة أولى | عقار، إخلاء، حيازة، هبة |
| `low` | صلة محدودة بالسياق التجاري للمشروع | وصية، نسب، ميراث |
| `skip` | خارج نطاق المشروع بالكامل | جنائي، أحوال شخصية، تعزير |

**قاعدة عملية:** إذا كان الموضوع يظهر في أي من أنواع العقود في `datasets/enums/contract-types.md` — فهو `high`. إذا كان يرتبط بحقوق مدنية قد تظهر في عقود — فهو `medium`. إذا كان أحوالاً شخصية أو جنائياً — فهو `skip`.

---

## 5. هذا الملف لا يحتوي Reasoning بعد / This Index Contains No Reasoning Yet

الفرق الجوهري بين هذا المجلد و`datasets/judicial-reasoning/`:

| هذا المجلد | datasets/judicial-reasoning/ |
|-----------|------------------------------|
| فهرس المحتوى — ماذا يوجد في الـ PDFs | استخراج الـ reasoning — ماذا قالت المحاكم |
| لا يتضمن حكمًا ولا استدلالاً | يتضمن `judicial_reasoning` و`legal_principle` |
| المدخل هو فهرس الـ PDF | المدخل هو نص الحكم نفسه |
| يُنجَز قبل الاستخراج | يُنجَز بعد الفهرسة واختيار الأقسام |

**لا تضع أي reasoning أو legal_principle في هذا المجلد.**

---

## الملفات في هذا المجلد / Files in This Directory

| الملف | الوصف |
|-------|-------|
| [`schema.md`](schema.md) | تعريف الحقول الـ 13 |
| [`judicial-corpus-index.csv`](judicial-corpus-index.csv) | بيانات الفهرس الفعلية |

---

## الملفات المرتبطة / Related Files

| الملف | العلاقة |
|-------|---------|
| [`sources/judicial-decisions/README.md`](../../sources/judicial-decisions/README.md) | سياق ملفات PDF المصدر |
| [`datasets/judicial-reasoning/schema.md`](../judicial-reasoning/schema.md) | مخطط الاستخراج اللاحق |
| [`datasets/judicial-reasoning/extraction-guidelines.md`](../judicial-reasoning/extraction-guidelines.md) | دليل الاستخراج بعد الفهرسة |
