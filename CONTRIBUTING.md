# دليل المساهمة / Contributing Guide

**Saudi Legal AI Framework** — إطار مفتوح المصدر لتكييف الذكاء الاصطناعي مع البيئة القانونية السعودية

---

> **⚠️ تحذير قانوني / Legal Warning**
>
> **بالعربية:** هذا المشروع أداة بحثية وتوثيقية فقط. لا يُعدّ أي محتوى فيه استشارةً قانونية. يحظر تمامًا إضافة بيانات حقيقية غير مُخفاة، أو نسب آراء قانونية غير مُؤكَّدة كحقائق، أو نسخ نصوص أنظمة من مصادر غير رسمية دون توضيح.
>
> **In English:** This project is a research and documentation tool only. No content in it constitutes legal advice. Adding non-anonymized real data, presenting unverified legal opinions as facts, or copying regulatory text from unofficial sources without attribution is strictly prohibited.

---

## جدول المحتويات / Table of Contents

- [هدف المشروع](#هدف-المشروع--project-goal)
- [أنواع المساهمات المقبولة](#أنواع-المساهمات-المقبولة--accepted-contribution-types)
- [Good First Issues](#good-first-issues)
- [كيفية تقديم Pull Request](#كيفية-تقديم-pull-request--how-to-submit-a-pr)
- [Good First Contributions](#good-first-contributions)
- [الفرق بين Source و Extraction](#الفرق-بين-source-و-extraction--source-vs-extraction)
- [Contribution Workflow](#contribution-workflow)
- [كيفية فتح Issue](#كيفية-فتح-issue--how-to-open-an-issue)
- [كيفية فتح Pull Request](#كيفية-فتح-pull-request--how-to-open-a-pull-request)
- [Before Opening a Pull Request](#before-opening-a-pull-request)
- [قواعد إضافة Datasets](#قواعد-إضافة-datasets--dataset-contribution-rules)
- [قواعد Anonymization](#قواعد-anonymization--anonymization-rules)
- [معايير الاستشهاد](#معايير-الاستشهاد--citation-standards)
- [قواعد التحقق](#قواعد-التحقق--verification-rules)
- [قواعد الـ Enums](#قواعد-الـ-enums--enum-rules)
- [اقتراح Skills أو Sources جديدة](#اقتراح-skills-أو-sources-جديدة--proposing-new-skills-or-sources)
- [متى يُستخدم TO VERIFY](#متى-يُستخدم-to-verify--when-to-use-to-verify)
- [ممنوعات المشروع](#ممنوعات-المشروع--project-prohibitions)

---

## هدف المشروع / Project Goal

**بالعربية:**
يهدف هذا الإطار إلى بناء مرجع مفتوح المصدر يُعلّم مساعدات الذكاء الاصطناعي كيف تُفكّر في المسائل القانونية السعودية — لا أن تُصدر أحكامًا قانونية نهائية. المساهمة الجيدة هي التي تُضيف وضوحًا أو دقةً أو مثالًا تطبيقيًا يخدم المختصين والباحثين والمطورين في السياق القانوني السعودي.

**In English:**
This framework aims to build an open-source reference that teaches AI assistants *how to reason* about Saudi legal matters — not to issue final legal rulings. A good contribution adds clarity, accuracy, or a practical example that serves legal professionals, researchers, and developers operating within the Saudi legal context.

---

## أنواع المساهمات المقبولة / Accepted Contribution Types

| النوع | الوصف | الأولوية |
|-------|-------|----------|
| 🔴 **تصحيح قانوني** | تصحيح معلومة نظامية غير دقيقة مع إرفاق المرجع الرسمي | عالية جدًا |
| 🔴 **تحديث تشريعي** | تحديث ملفات `sources/` عند صدور تعديل على نظام | عالية جدًا |
| 🟠 **إضافة dataset** | إضافة بنود عقدية افتراضية أو مُجرَّدة ممنهجة | عالية |
| 🟠 **skill جديدة** | توثيق مجال قانوني سعودي لم يُغطَّ بعد | عالية |
| 🟡 **مثال تطبيقي** | إضافة سيناريو افتراضي موثَّق في `examples/` | متوسطة |
| 🟡 **source جديد** | توثيق نظام سعودي لم يُشمَل في `sources/` | متوسطة |
| 🟢 **تحسين لغوي** | تحسين الصياغة العربية أو الإنجليزية دون تغيير المعنى | منخفضة |
| 🟢 **تحسين تنسيق** | توحيد التنسيق وتصحيح روابط | منخفضة |

---

## Good First Issues

هذه المهام الخمس مُعلَّمة `good-first-issue` على GitHub — مناسبة لمن يبدأ مساهمته الأولى في المشروع:

These five tasks are labeled `good-first-issue` on GitHub — ideal for a first contribution:

### 1. أضف مثالاً لعقد إيجار تجاري / Add a Commercial Lease Example

أضف ملف مثال في `examples/` يُغطي سيناريو عقد إيجار تجاري (عقد إيجار محل، مكتب، أو مستودع) وفق قواعد الإخفاء الكاملة. استخدم `examples/employment-contract-review.md` كنموذج للهيكل.

Add an example file in `examples/` covering a commercial lease scenario (retail shop, office, or warehouse) following full anonymization rules. Use `examples/employment-contract-review.md` as a structural template.

### 2. صحّح خطأ تنسيقي في sources/ / Fix a Formatting Issue in sources/

ابحث عن أي خطأ إملائي أو تنسيقي في أي ملف داخل `sources/` وأصلحه. أمثلة: رابط مكسور، جدول غير منتظم، رقم مادة مكتوب بصيغتين مختلفتين.

Find any typo or formatting inconsistency in any file under `sources/` and fix it. Examples: broken link, misaligned table, article number written in two different formats.

### 3. ترجم قسمًا إلى العربية أو الإنجليزية / Translate a Section

اختر قسمًا موجودًا مكتوبًا بلغة واحدة فقط وأضف ترجمته. تأكد من الحفاظ على المعنى القانوني الدقيق.

Find an existing section written in only one language and add its translation. Ensure the precise legal meaning is preserved.

### 4. أضف رابط مصدر رسمي مفقود / Add a Missing Official Source URL

ابحث في `sources/regulation-index.md` أو أي ملف `sources/*.md` عن نظام يفتقر لرابط رسمي من `boe.gov.sa` أو `uqn.gov.sa` وأضف الرابط الصحيح.

Search `sources/regulation-index.md` or any `sources/*.md` file for a regulation missing an official link from `boe.gov.sa` or `uqn.gov.sa` and add the correct URL.

### 5. راجع ملف skill وافتح Issue / Review a Skill File and Open an Issue

اختر أي ملف من `skills/` واقرأه بعناية. إذا وجدت معلومة نظامية غير دقيقة أو افتراضًا قانونيًا غير موثَّق، افتح Issue يصف المشكلة والتصحيح المقترح مع مصدره الرسمي.

Choose any file from `skills/` and read it carefully. If you find an inaccurate regulatory claim or an unverified legal assumption, open an Issue describing the problem, the suggested correction, and its official source.

---

## كيفية تقديم Pull Request / How to Submit a PR

```
1. Fork + Branch    غصّن المشروع وأنشئ فرعًا وصفيًا
                    Fork and create a descriptive branch
                    مثال: add-commercial-lease-example / fix-pdpl-link

2. Edit + Validate  أجرِ التعديل وشغّل التحقق إن عدّلت CSV
                    Make your change and run validation if editing CSV:
                    python3 scripts/validate_dataset.py --file <file.csv>

3. Open PR          افتح PR مع وصف يُجيب على: ماذا؟ لماذا؟ المصدر القانوني؟
                    Open a PR answering: what? why? legal source?

4. Review           المراجعة تشمل دقة المحتوى + غياب البيانات الحقيقية + صحة التنسيق
                    Review covers content accuracy + no real data + format validity
```

للتفاصيل الكاملة: [كيفية فتح Pull Request](#كيفية-فتح-pull-request--how-to-open-a-pull-request) و[Before Opening a Pull Request](#before-opening-a-pull-request)

For full details: [How to Open a Pull Request](#كيفية-فتح-pull-request--how-to-open-a-pull-request) and [Before Opening a Pull Request](#before-opening-a-pull-request)

---

## Good First Contributions

إذا كنت جديدًا على المشروع، ابدأ بإحدى هذه المهام:

If you are new to the project, start with one of these tasks:

### 1. تحسين الاستشهادات / Improve Citations
ابحث عن أي استشهاد بنظام لا يتطابق مع صيغة الاستشهاد في [`sources/regulation-index.md`](sources/regulation-index.md) وصحّحه.

Search for any regulation citation that does not match the format in [`sources/regulation-index.md`](sources/regulation-index.md) and fix it.

### 2. إضافة بنود مُجرَّدة / Add Anonymized Clauses
أضف صفوفًا جديدة لـ [`datasets/saudi-contract-risk-dataset.csv`](datasets/saudi-contract-risk-dataset.csv) تُغطي قطاعات أو أنواع بنود لم تُغطَّ بعد — بعد قراءة [قواعد الـ Dataset](#قواعد-إضافة-datasets--dataset-contribution-rules).

Add new rows to the dataset covering sectors or clause types not yet represented — after reading the [Dataset Rules](#قواعد-إضافة-datasets--dataset-contribution-rules).

### 3. توحيد المصطلحات / Unify Terminology
تحقق من ملفات `skills/` و`prompts/` وتأكد أن المصطلحات القانونية المتكررة تُستخدم بنفس الصياغة في جميع الملفات.

Check `skills/` and `prompts/` files and verify that recurring legal terms are used with consistent wording across all files.

### 4. تحسين ملفات Dataset / Improve Dataset Files
راجع [`datasets/examples/`](datasets/examples/) وأضف أمثلة لقطاعات مفقودة (عقارات، صحة، تمويل، تعليم).

Review [`datasets/examples/`](datasets/examples/) and add examples for missing sectors (real estate, healthcare, finance, education).

### 5. مراجعة Article Mappings / Review Article Mappings
تحقق من أن المواد النظامية المذكورة في `related_regulation` بالـ dataset تُشير إلى المواد الصحيحة. إذا وجدت خطأ، افتح Issue.

Verify that the regulatory articles cited in the dataset's `related_regulation` column point to the correct articles. If you find an error, open an Issue.

---

## الفرق بين Source و Extraction / Source vs Extraction

هذا التمييز ضروري لأن المساهمين يخلطون أحيانًا بين الطبقتين.

This distinction is critical because contributors sometimes confuse the two layers.

| الطبقة | المجلد | المحتوى | من يُضيف |
|--------|--------|---------|---------|
| **Source** | `sources/` | ملخصات مرجعية للأنظمة — ما يقوله النظام | أي مساهم مع مصدر رسمي |
| **Judicial Corpus** | `sources/judicial-decisions/` | ملفات PDF مسحوبة ضوئيًا — النص الخام | ملفات إضافية بإذن المشروع |
| **Corpus Index** | `datasets/judicial-index/` | فهرس أقسام الـ PDF — ما الذي يوجد أين | أي مساهم يستطيع قراءة فهرس PDF |
| **Extraction** | `datasets/judicial-reasoning/` | ما قالته المحاكم — استخلاص منظَّم من الأحكام | مساهمون مؤهلون قانونيًا فقط |

### القاعدة الأساسية / The Core Rule

```
sources/        ←  ما يقوله النظام (تشريع)
judicial-index/ ←  ما يوجد في الـ PDF (فهرسة)
judicial-reasoning/ ←  ما قالته المحكمة (استخراج)
```

**المصادر التشريعية لا تحلّ محل الأحكام القضائية، والعكس صحيح.**

Legislative sources do not replace judicial decisions, and vice versa.

### قبل المساهمة في Extraction / Before Contributing an Extraction

1. تأكد أن القسم المعني مُسجَّل في [`datasets/judicial-index/judicial-corpus-index.csv`](datasets/judicial-index/judicial-corpus-index.csv) أولًا
2. اقرأ [`datasets/judicial-reasoning/extraction-guidelines.md`](datasets/judicial-reasoning/extraction-guidelines.md) كاملًا
3. أخفِ جميع البيانات الشخصية قبل الإرسال
4. أضف `verification_status = draft` على كل صف

---

### 🆕 جديد على GitHub؟ ابدأ من هنا

إذا كنت محاميا او مستشارا قانونيا ولا تعرف GitHub، لا تقلق.
اعددنا دليلا عربيا شاملا يشرح كل شيء خطوة بخطوة:

👉 [دليل GitHub للمبتدئين بالعربي](https://samix2026.github.io/github-beginner-guide-ar/)

بعد قراءة الدليل، عد هنا وابدأ مساهمتك.

---

## Contribution Workflow

```
1. Fork          غصّن المشروع على حسابك
   │             Fork the repository to your account
   │
2. Branch        أنشئ فرعًا باسم وصفي
   │             Create a descriptive branch name
   │             مثال: add-real-estate-dataset / fix-labor-law-citation
   │
3. Edit          أجرِ التعديلات مع الالتزام بالمعايير أدناه
   │             Make changes following the standards below
   │
4. Validate      شغّل سكربت التحقق إذا عدّلت ملفات CSV
   │             Run the validation script if you edited CSV files:
   │             python3 scripts/validate_dataset.py --file <your-file.csv>
   │
5. PR            افتح Pull Request مع وصف واضح
   │             Open a Pull Request with a clear description
   │             - ماذا أضفت أو عدّلت / What you added or changed
   │             - لماذا / Why
   │             - المصدر القانوني إن وُجد / Legal source if applicable
   │
6. Review        المراجعة تشمل: صحة التنسيق + سلامة المحتوى + غياب البيانات الحقيقية
                 Review covers: format validity + content safety + absence of real data
```

> ⚠️ **قاعدة تشغيلية دائمة / Operational rule (v0.4.9):**
> بعد أي تعديل على كود `saudi_legal_mcp/`، **أعد تشغيل عملية OpenClaw بالكامل**
> (لا تكتفِ بـ`openclaw mcp reload`) قبل الاختبار. لوحظ مراراً أن العملية
> الحيّة تحتفظ بنسخة قديمة من الكود (runtime قديم) — الاختبار اللاحق قد
> يعكس نسخة سابقة بصمت ويضيّع جولات تصحيح كاملة. إن ظهرت نتيجة لا تطابق
> الكود المثبَّت، اشتبه في هذه المشكلة أولاً قبل أي شيء آخر.
>
> After any change to `saudi_legal_mcp/`, **fully restart the OpenClaw
> process** (not just `openclaw mcp reload`) before testing. Stale-runtime
> behaviour has been observed repeatedly — the live process silently keeps
> the old code and your test may validate a ghost version.

**تسمية الفروع / Branch Naming:**

| النوع | الصيغة | مثال ||-------|--------|-------|
| إضافة محتوى | `add-<description>` | `add-healthcare-examples` |
| تصحيح | `fix-<description>` | `fix-pdpl-article-reference` |
| تحديث | `update-<description>` | `update-labor-law-amendments` |
| تحسين | `improve-<description>` | `improve-nda-skill` |

---

## كيفية فتح Issue / How to Open an Issue

**متى تفتح Issue؟ / When to open an Issue:**
- وجدت معلومة قانونية غير دقيقة / You found an inaccurate legal fact
- تريد اقتراح skill أو source أو dataset جديد / You want to propose new content
- وجدت تعارضًا بين ملفين / You found a conflict between two files
- صدر تعديل على نظام مُشمول في المشروع / A covered regulation has been amended

**ما يجب أن يحتوي عليه الـ Issue:**

```markdown
## الموضوع / Subject
[وصف موجز للمشكلة أو الاقتراح]

## الملف المعني / Affected File
[مسار الملف — مثال: sources/labor-law.md]

## المشكلة أو الاقتراح / Problem or Proposal
[شرح تفصيلي]

## المصدر القانوني (للتصحيحات) / Legal Source (for corrections)
[رابط أو مرجع من boe.gov.sa أو uqn.gov.sa]
```

---

## كيفية فتح Pull Request / How to Open a Pull Request

يجب أن يتضمن كل PR وصفًا يُجيب على:

Every PR must include a description answering:

1. **ماذا؟ / What?** — ما الذي أضفته أو عدّلته بالتحديد
2. **لماذا؟ / Why?** — ما المشكلة التي يحلّها هذا التغيير
3. **المصدر / Source** — المرجع القانوني الرسمي إذا كان التغيير يتعلق بمعلومة نظامية
4. **التحقق / Validation** — نتيجة `validate_dataset.py` إذا عدّلت ملفات CSV

**عنوان الـ PR / PR Title Format:**
```
[type]: short description in English
```
أمثلة: `fix: correct PDPL Art. 29 reference` | `add: healthcare dataset examples` | `update: labor law probation period`

---

## Before Opening a Pull Request

تأكد من المربعات التالية قبل الإرسال:

Verify the following before submitting:

### عام / General
- [ ] الفرع مبني على آخر نسخة من `main`
- [ ] Branch is based on the latest `main`
- [ ] عنوان الـ PR واضح ويتبع الصيغة المطلوبة
- [ ] PR title is clear and follows the required format
- [ ] الوصف يُجيب على: ماذا، لماذا، المصدر
- [ ] Description answers: what, why, source

### المحتوى القانوني / Legal Content
- [ ] كل معلومة نظامية مرتبطة بمصدر رسمي (boe.gov.sa أو uqn.gov.sa)
- [ ] Every regulatory fact is linked to an official source
- [ ] الاستشهادات تتطابق مع صيغ [`sources/regulation-index.md`](sources/regulation-index.md)
- [ ] Citations match the formats in `sources/regulation-index.md`
- [ ] المعلومات غير المؤكدة تحمل علامة `TO VERIFY`
- [ ] Unverified information is marked `TO VERIFY`

### Dataset (إذا عدّلت CSV) / Dataset (if you edited CSV)
- [ ] شغّلت `python3 scripts/validate_dataset.py --file <your-file.csv>` وأجاز
- [ ] Ran `python3 scripts/validate_dataset.py --file <your-file.csv>` and it passed
- [ ] القيم في `contract_type`، `clause_category`، `industry` من الـ enums المعتمدة
- [ ] Values in `contract_type`, `clause_category`, `industry` are from the approved enums
- [ ] كل صف يحتوي على `verification_status` — القيمة الافتراضية `draft`
- [ ] Every row has a `verification_status` value — default is `draft`
- [ ] لا توجد بيانات حقيقية (أسماء شركات، أفراد، أرقام عقود)
- [ ] No real data (company names, individuals, contract numbers)
- [ ] كل صف `clause_text` افتراضي أو مُجرَّد تمامًا
- [ ] Every `clause_text` is hypothetical or fully abstracted

### السلامة / Safety
- [ ] لا يحتوي الـ PR على استشارة قانونية مباشرة أو قاطعة
- [ ] PR contains no direct or definitive legal advice
- [ ] لا يحتوي على بيانات شخصية أو بيانات عملاء
- [ ] Contains no personal data or client information
- [ ] لا يُقدّم رأيًا قانونيًا بصياغة جازمة دون مصدر
- [ ] Does not present a legal opinion as definitive fact without a source

---

## قواعد إضافة Datasets / Dataset Contribution Rules

### الملف الرئيسي / Main File
[`datasets/saudi-contract-risk-dataset.csv`](datasets/saudi-contract-risk-dataset.csv)

### الملفات المرجعية / Reference Files
- المخطط: [`datasets/schema.md`](datasets/schema.md)
- مستويات الخطر: [`datasets/risk-taxonomy.md`](datasets/risk-taxonomy.md)
- معايير التصعيد: [`datasets/severity-standards.md`](datasets/severity-standards.md)
- الـ Enums: [`datasets/enums/`](datasets/enums/)

### قواعد الـ Naming / Naming Conventions

**ملفات CSV الجديدة في `datasets/examples/`:**
- اسم وصفي بأحرف صغيرة مفصولة بشرطة: `real-estate-contracts.csv`
- لا مسافات، لا أحرف عربية في اسم الملف
- Lowercase, hyphen-separated: `real-estate-contracts.csv`

**عمود `id`:**
- رقم صحيح موجب متسلسل داخل كل ملف يبدأ من `1`
- لا يُشترط التسلسل العالمي عبر الملفات المختلفة
- Positive integer, sequential within each file starting from `1`

### كيفية تشغيل Validation / Running Validation

```bash
# التحقق من الملف الرئيسي / Validate the main file
python3 scripts/validate_dataset.py

# التحقق من ملف محدد / Validate a specific file
python3 scripts/validate_dataset.py --file datasets/examples/your-file.csv

# التحقق من جميع ملفات الأمثلة / Validate all example files
for f in datasets/examples/*.csv; do
    echo "=== $f ===" && python3 scripts/validate_dataset.py --file "$f"
done
```

**يجب أن يُجيز السكربت قبل فتح الـ PR. Exit code `1` = فشل.**
**The script must pass before opening a PR. Exit code `1` = failure.**

---

## قواعد Anonymization / Anonymization Rules

كل بند مُدخَل يجب أن يمر باختبار الإخفاء الكامل:

Every entered clause must pass the full anonymization test:

### ✅ مسموح / Allowed

| النوع | المتطلب |
|-------|---------|
| **افتراضي (`hypothetical`)** | نص مُنشأ خصيصًا كمثال — لا يستند لعقد حقيقي |
| **مُجرَّد (`abstracted`)** | نمط من عقد حقيقي مع إزالة كاملة لأي بيانات تعريفية |
| **قضية منشورة (`published_case`)** | مستند لحكم أو قضية منشورة رسميًا — مع ذكر المصدر في `notes` |
| **نموذج قياسي (`standard_form`)** | مستخلص من نموذج عقد معروف ومعدَّل — مع ذكر المصدر في `notes` |

### ❌ ممنوع / Prohibited

- أي نص يحتوي على اسم شركة حقيقية، حتى لو كانت شركة عامة
- أي اسم شخص طبيعي، بما في ذلك الأسماء المستعارة المرتبطة بشخص حقيقي
- أرقام عقود، أرقام فواتير، أرقام سجل تجاري حقيقية
- مبالغ مالية حقيقية مرتبطة بعقد بعينه
- بيانات موظفين أو عملاء حتى لو كانت منقوصة

- Any text containing a real company name, even a public company
- Any real or pseudonymous name tied to a real individual
- Real contract numbers, invoice numbers, or commercial registration numbers
- Real financial amounts tied to a specific contract
- Employee or client data even if partial

### اختبار الإخفاء / The Anonymization Test

اسأل نفسك: هل يمكن لشخص يعرف الطرف الأصلي أن يُعرّف هوية العقد أو الأطراف من هذا النص؟
إذا كانت الإجابة "ربما"، لا تُدرج البند.

Ask yourself: could someone who knows the original party identify the contract or parties from this text?
If the answer is "possibly", do not include the clause.

---

## معايير الاستشهاد / Citation Standards

**المرجع الرسمي الوحيد:** [`sources/regulation-index.md`](sources/regulation-index.md)

**الصيغة القياسية للاستشهاد بنظام كامل:**
```
Saudi Labor Law (Royal Decree M/51 1426H)
```

**الصيغة مع مادة محددة:**
```
Saudi Labor Law (Royal Decree M/51 1426H) Art. 84
```

**الصيغة مع مواد متعددة:**
```
PDPL (Royal Decree M/19 1443H) Arts. 29-30
```

**قواعد الاستشهاد:**
- لا تستشهد بنص من موقع غير رسمي (ويكيبيديا، مدونات، إلخ)
- إذا لم تجد النظام في `regulation-index.md`، افتح Issue لإضافته أولًا
- نصوص المواد القانونية الكاملة لا تُنسَخ — أشر إليها بالمادة والمصدر فقط

- Do not cite text from unofficial sources (Wikipedia, blogs, etc.)
- If the regulation is not in `regulation-index.md`, open an Issue to add it first
- Full regulatory article text is never copied — reference the article and source only

**المصادر الرسمية المقبولة:**
- [boe.gov.sa](https://boe.gov.sa) — هيئة الخبراء بمجلس الوزراء
- [uqn.gov.sa](https://uqn.gov.sa) — الجريدة الرسمية (أم القرى)
- [sdaia.gov.sa](https://sdaia.gov.sa) — سدايا (لـ PDPL)
- [hrsd.gov.sa](https://hrsd.gov.sa) — وزارة الموارد البشرية (لنظام العمل)

---

## قواعد التحقق / Verification Rules

### مستويات الثقة / Confidence Levels

| الحالة | الصياغة المطلوبة |
|--------|-----------------|
| معلومة مؤكدة من مصدر رسمي | اذكرها مباشرةً مع الاستشهاد |
| معلومة محتملة غير مؤكدة | أضف `<!-- TO VERIFY -->` وصِغها بـ "قد يكون / may be" |
| تفسير قضائي غير موثَّق | لا تُدرجه إلا مع تحفّظ واضح وعلامة `TO VERIFY` |
| رأي قانوني شخصي | لا يُدرج أبدًا كحقيقة |

### الصياغة التحليلية / Analytical Language

استخدم دائمًا صياغةً تُشير لطبيعة التحليل الأولية:

Always use language that reflects the preliminary nature of the analysis:

```
✅ "قد يتعارض هذا البند مع..."   / "This clause may conflict with..."
✅ "يُحتمل أن تعتبره المحاكم..."  / "Courts may consider this..."
✅ "وفق المادة X، يُشترط..."      / "Per Article X, it is required..."

❌ "هذا البند باطل"              / "This clause is void"
❌ "ستحكم المحكمة بـ..."         / "The court will rule..."
❌ "القانون يُلزم بـ..."          / "The law requires..." (بدون استشهاد)
```

---

## قواعد الـ Enums / Enum Rules

الـ enums محددة في [`datasets/enums/`](datasets/enums/) ومُطبَّقة في [`scripts/validate_dataset.py`](scripts/validate_dataset.py).

Enums are defined in [`datasets/enums/`](datasets/enums/) and enforced by [`scripts/validate_dataset.py`](scripts/validate_dataset.py).

| العمود | ملف الـ Enum | عدد القيم |
|--------|------------|-----------|
| `risk_level` | [`enums/risk-levels.md`](datasets/enums/risk-levels.md) | 4 |
| `contract_type` | [`enums/contract-types.md`](datasets/enums/contract-types.md) | 11 |
| `clause_category` | [`enums/clause-categories.md`](datasets/enums/clause-categories.md) | 14 |
| `industry` | [`enums/industries.md`](datasets/enums/industries.md) | 12 |

### إضافة قيمة enum جديدة / Adding a New Enum Value

1. افتح **Issue** أولًا لمناقشة القيمة الجديدة قبل تنفيذها
2. بعد الموافقة: عدّل ملف الـ enum في `datasets/enums/`
3. عدّل `scripts/validate_dataset.py` لإضافة القيمة للمجموعة المقابلة
4. ابحث عن أي صفوف موجودة قد تستفيد من التصنيف الجديد وعدّلها
5. شغّل السكربت على جميع الـ CSVs وتأكد من عدم ظهور أخطاء جديدة

1. Open an **Issue** first to discuss the new value before implementing
2. After approval: edit the enum file in `datasets/enums/`
3. Edit `scripts/validate_dataset.py` to add the value to the corresponding set
4. Search existing rows that might benefit from the new classification
5. Run the script on all CSVs and confirm no new errors appear

---

## اقتراح Skills أو Sources جديدة / Proposing New Skills or Sources

### Skill جديدة / New Skill

`skills/` تحتوي على توجيهات لكيفية تفكير الذكاء الاصطناعي في مجال قانوني محدد.

`skills/` contains guidance on how AI should reason in a specific legal domain.

**لاقتراح skill جديدة:**
1. افتح Issue بعنوان: `[skill] اسم المجال القانوني`
2. حدد: ما المجال؟ ما الفجوة التي تسدّها؟ ما الأنظمة ذات الصلة؟
3. بعد الموافقة، أنشئ `skills/<domain-name>.md` باتباع هيكل `skills/contract-review.md`

**هيكل الـ Skill الموحَّد:**
```
## 1. Scope
## 2. Supported [Contract/Case] Types
## 3. Analysis Workflow
## 4. Red Flags Checklist
## 5. [Domain-specific section]
## 6. Saudi-Specific Considerations
## 7. Output Format  ← يشير إلى skills/contract-review.md §8 أو يُعرّف هيكله الخاص
## 8. Escalation Rules
## 9. Limitations
## 10. Relevant Regulations
```

### Source جديد / New Source

`sources/` تحتوي على ملخصات مرجعية للأنظمة السعودية — ليست نصوصًا رسمية كاملة.

`sources/` contains reference summaries of Saudi regulations — not full official texts.

**لاقتراح source جديد:**
1. افتح Issue بعنوان: `[source] اسم النظام`
2. أرفق رابط النظام من boe.gov.sa أو uqn.gov.sa
3. بعد الموافقة، أنشئ `sources/<regulation-name>.md` باتباع هيكل `sources/labor-law.md`
4. أضف النظام لـ [`sources/regulation-index.md`](sources/regulation-index.md)

---

## متى يُستخدم TO VERIFY / When to Use TO VERIFY

ضع `<!-- TO VERIFY -->` مباشرةً بعد أي جملة أو معلومة:

Place `<!-- TO VERIFY -->` immediately after any sentence or information that:

| الحالة | مثال |
|--------|-------|
| لم تتحقق منها من مصدر رسمي | "تشترط اللائحة التنفيذية 90 يومًا <!-- TO VERIFY -->" |
| تخص تفسيرًا قضائيًا غير موثَّق | "تميل المحاكم عادةً إلى... <!-- TO VERIFY -->" |
| قد تكون تغيّرت بعد تعديل تشريعي | "الحد الأقصى للغرامة 5 ملايين ريال <!-- TO VERIFY: check latest PDPL amendment -->" |
| اجتهاد شخصي يحتاج مراجعة متخصص | أي رأي قانوني لم يُدعَم بمصدر |

**قاعدة ذهبية:** الشك يذهب لـ `TO VERIFY`، ليس للحذف.
**Golden rule:** When in doubt, use `TO VERIFY`, not deletion.

---

## ممنوعات المشروع / Project Prohibitions

### ❌ بيانات العملاء / Client Data

يُحظر بشكل مطلق إدخال أي بيانات مرتبطة بعلاقة مهنية حقيقية بين محامٍ وموكّل، أو بين شركة وعميل — حتى لو كانت منقوصة أو مجزأة.

Absolutely prohibited: any data linked to a real attorney-client or company-client relationship — even if partial or fragmented.

### ❌ الاستشارات القانونية / Legal Advice

يُحظر تقديم أي مخرج بصياغة جازمة تُوهم المستخدم بأنه يتلقى استشارة قانونية ملزمة. كل مخرج يجب أن يتضمن تحذيرًا بأنه تحليل أولي.

Prohibited: presenting any output in definitive language that leads a user to believe they are receiving binding legal advice. Every output must include a disclaimer that it is preliminary analysis.

### ❌ المعلومات غير المؤكدة كحقائق / Unverified Information as Facts

يُحظر تقديم رأي قانوني أو تفسير قضائي بصياغة جازمة دون استشهاد بمصدر رسمي. كل ادعاء قانوني يحتاج مصدرًا أو علامة `TO VERIFY`.

Prohibited: presenting a legal opinion or judicial interpretation as definitive fact without citing an official source. Every legal claim needs a source or a `TO VERIFY` marker.

### ❌ نسخ النصوص من مصادر غير رسمية / Copying Text from Unofficial Sources

يُحظر نسخ نصوص أنظمة من ويكيبيديا، مدونات، مواقع مكاتب محاماة، أو أي مصدر غير رسمي وتقديمها كنص نظامي رسمي. المصادر المقبولة فقط: boe.gov.sa وuqn.gov.sa والمنصات الحكومية الرسمية.

Prohibited: copying regulatory text from Wikipedia, blogs, law firm websites, or any unofficial source and presenting it as official regulatory text. Only accepted sources: boe.gov.sa, uqn.gov.sa, and official government platforms.

### ❌ المحتوى المُولَّد بالذكاء الاصطناعي بلا مراجعة / AI-Generated Content Without Review

يُحظر إضافة محتوى مُولَّد بالكامل بالذكاء الاصطناعي دون مراجعة بشرية واعية. المساهم مسؤول شخصيًا عن دقة ما يُرسله.

Prohibited: adding content generated entirely by AI without conscious human review. The contributor is personally responsible for the accuracy of what they submit.

### ❌ رفع Extracted Reasoning بدون Anonymization / Uploading Extracted Reasoning Without Anonymization

يُحظر رفع أي استخراج من حكم قضائي يحتوي على اسم طرف حقيقي، رقم ملف رسمي، أو بيانات تعريفية يمكن من خلالها تحديد هوية الأطراف. كل استخراج يجب أن يستبدل الأسماء بعلامات مُجرَّدة مثل `[صاحب العمل]` و`[العامل]`.

اقرأ [`datasets/judicial-reasoning/extraction-guidelines.md`](datasets/judicial-reasoning/extraction-guidelines.md) قبل أي استخراج.

Prohibited: uploading any extraction from a judicial decision that contains real party names, official case numbers, or identifying data. Every extraction must replace names with abstract markers such as `[صاحب العمل]` and `[العامل]`. Read the extraction guidelines before submitting.

### ❌ استخراج حكم غير قابل للقراءة / Extracting from an Unreadable Decision

يُحظر محاولة استخراج reasoning من صفحة PDF غير واضحة القراءة، أو من نص مُشوَّه، أو من حكم لا يمكن التحقق من سياقه. في هذه الحالة: أضف ملاحظة في سجل الفهرس وتوقف.

Prohibited: attempting to extract reasoning from a PDF page that is unclear, corrupted, or whose context cannot be verified. In that case: add a note in the index record and stop.

### ❌ إضافة صف Extraction بدون verification_status / Adding an Extraction Row Without verification_status

كل صف في `datasets/judicial-reasoning/` يجب أن يحتوي على `verification_status = draft` كحد أدنى. لا تُرسل صفًا فارغ الحقل.

Every row in `datasets/judicial-reasoning/` must include `verification_status = draft` at minimum. Do not submit a row with an empty status field.

---

## دورة التحقق القانوني (Legal Verification Lifecycle)

أي تعديل على المعلومات القانونية في مجلدي `sources/` و `skills/` يخضع لعملية تدقيق صارمة لضمان موثوقية الأداة:

### 1. مسؤوليات الملاك (CODEOWNERS)
حُدد الحساب `@SMSMy` كمراجع افتراضي لكل ملفات المحتوى. أي طلب سحب (PR) يعدل ملفاً قانونياً سيطلب تلقائياً مراجعته.
مهمته التحقق من **المصدر (Provenance)**:
- هل الرابط الرسمي المرفق يعمل ويشير إلى موقع حكومي (مثل `boe.gov.sa` أو `uqn.gov.sa`)؟
- هل الـ SHA256 في الـ `manifest` متطابق؟

### 2. مسؤوليات المراجع القانوني (Legal Reviewer)
للمصادر عالية الأثر (مثل نظام العمل، العقود، المحاكم التجارية، PDPL)، نطلب أن يتم التدقيق النهائي من قبل محامٍ أو مستشار قانوني ممارس في المملكة.
- **إذا لم يتوفر مراجع**: ستبقى حالة الملف `unverified` في الـ `manifest`. هذا إجراء مقصود لحماية المستخدم.

### 3. اقتراح تدقيق (Proposing Verification)
كمساهم، يمكنك اقتراح تدقيق مصدر باستخدام السكربت المخصص:
```bash
python scripts/propose_verification.py <source_id>
```
سيطالبك السكربت بإدخال الرابط الرسمي وجهة الإصدار، وسيحدّث ملف الـ manifest تلقائياً لتفتحه في PR. الأداة `validate_manifests.py` ستتأكد ألا تمرر حقولاً قانونية ما لم تعلن صراحة نيتك لطلب المراجعة.

---

## التواصل / Contact

- **Issues:** استخدم GitHub Issues لأي سؤال أو اقتراح
- **Pull Requests:** التواصل يتم عبر تعليقات الـ PR مباشرةً
- **الأخطاء القانونية الحرجة:** افتح Issue بعنوان يبدأ بـ `[CRITICAL]`

- **Issues:** Use GitHub Issues for any question or suggestion
- **Pull Requests:** Communication happens directly through PR comments
- **Critical legal errors:** Open an Issue with a title starting with `[CRITICAL]`

---

**شكرًا لمساهمتك في بناء إطار قانوني عربي مفتوح المصدر ودقيق.**
**Thank you for contributing to building an accurate, open-source Arabic legal framework.**
