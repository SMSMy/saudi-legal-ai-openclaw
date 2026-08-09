# Saudi Contract Risk Dataset
# مجموعة بيانات مخاطر العقود السعودية

---

## ⚠️ تحذير صارم / Critical Warning

> **بالعربية:** يُحظر تمامًا إضافة بيانات عقود حقيقية أو بيانات عملاء أو معلومات شخصية أو أسماء شركات حقيقية دون إخفاء كامل وموثَّق. أي مساهمة تحتوي بيانات حقيقية غير مُخفاة ستُرفض فورًا وتُحذف من السجل.
>
> **In English:** Adding real contract data, client information, personal data, or actual company names without complete and documented anonymization is strictly prohibited. Any contribution containing non-anonymized real data will be rejected immediately and purged from history.

---

## الهدف / Purpose

هذا المجلد يحتوي على مجموعة بيانات منظَّمة لأنماط المخاطر القانونية الشائعة في العقود السعودية. الهدف هو بناء مرجع مفتوح المصدر يساعد الذكاء الاصطناعي والباحثين والمختصين القانونيين على فهم أنماط المخاطر في السياق القانوني السعودي.

This directory contains a structured dataset of common legal risk patterns in Saudi contracts. The goal is to build an open-source reference that helps AI systems, researchers, and legal professionals understand risk patterns in the Saudi legal context.

**ما هذا الـ dataset؟ / What is this dataset?**
- مجموعة أمثلة افتراضية ومُجرَّدة لبنود عقدية إشكالية
- كل مثال مُصنَّف بمستوى خطر ومُرتبط بنظام سعودي محدد
- مخصص للبحث والتدريب والتوثيق — لا للاستشارة القانونية المباشرة

- A collection of hypothetical and abstracted examples of problematic contractual clauses
- Each example is classified by risk level and linked to a specific Saudi regulation
- Intended for research, training, and documentation — not for direct legal advice

---

## كيفية المساهمة / How to Contribute

### للمحامين والمختصين القانونيين / For Legal Professionals

إذا كنت محاميًا أو مستشارًا قانونيًا سعوديًا:

1. **أضف أنماطًا من تجربتك** — ليس عقودًا حقيقية، بل أنماط بنود إشكالية تتكرر
2. **تحقق من الدقة القانونية** — راجع `saudi_legal_note` و `related_regulation` في كل صف
3. **صحّح المعلومات غير الدقيقة** — افتح Issue لأي خطأ قانوني وأشر للمصدر الرسمي
4. **أضف قطاعات جديدة** — العقارات، الصحة، التقنية، المقاولات، الامتياز التجاري

If you are a Saudi attorney or legal advisor:

1. **Add patterns from your experience** — not real contracts, but recurring problematic clause patterns
2. **Verify legal accuracy** — review `saudi_legal_note` and `related_regulation` in each row
3. **Correct inaccuracies** — open an Issue for any legal error and cite the official source
4. **Add new sectors** — real estate, healthcare, technology, construction, franchise

### للمطورين / For Developers

1. **تشغيل السكربت قبل المساهمة** — `python scripts/validate_dataset.py`
2. **اتباع مخطط البيانات** — راجع `datasets/schema.md` لفهم كل عمود
3. **اتباع معايير الخطورة** — راجع `datasets/risk-taxonomy.md` و `datasets/severity-standards.md`
4. **اختبار CSV** — تأكد أن الملف يُقرأ بـ pandas بدون أخطاء

1. **Run the script before contributing** — `python scripts/validate_dataset.py`
2. **Follow the data schema** — see `datasets/schema.md` for each column
3. **Follow severity standards** — see `datasets/risk-taxonomy.md` and `datasets/severity-standards.md`
4. **Test the CSV** — ensure the file is readable by pandas without errors

---

## ما المسموح إضافته / What Is Allowed

| مسموح | Allowed |
|-------|---------|
| ✅ أنماط بنود عقدية افتراضية مُجرَّدة | Hypothetical abstracted clause patterns |
| ✅ بنود مستخلصة من عقود موحَّدة معروفة ومُعدَّلة | Clauses derived from known standard contracts and modified |
| ✅ أمثلة من قضايا منشورة أو مبادئ قضائية معروفة | Examples from published cases or known judicial principles |
| ✅ تصنيفات مخاطر مبنية على أنظمة سعودية رسمية | Risk classifications based on official Saudi regulations |
| ✅ ملاحظات قانونية مُحالة لمصادر رسمية | Legal notes citing official sources |
| ✅ بيانات خيالية مُوضَّح صراحةً أنها `hypothetical` | Fictional data explicitly marked as `hypothetical` |

## ما الممنوع إضافته / What Is Prohibited

| ممنوع | Prohibited |
|-------|-----------|
| ❌ عقود حقيقية بأي شكل حتى لو جزئية | Real contracts in any form even partially |
| ❌ أسماء شركات أو أفراد حقيقيين | Real company or individual names |
| ❌ أرقام عقود أو سجلات تجارية حقيقية | Real contract numbers or commercial registration numbers |
| ❌ بيانات مالية حقيقية لأطراف بعينها | Real financial data of specific parties |
| ❌ معلومات قضايا منظورة أو عقود متنازع عليها | Information about pending cases or disputed contracts |
| ❌ أي بيانات شخصية حتى مُجزَّأة | Any personal data even if fragmented |
| ❌ محتوى مُولَّد بالذكاء الاصطناعي دون مراجعة قانونية بشرية | AI-generated content without human legal review |

---

## إجراء المراجعة / Review Process

كل مساهمة في هذا الـ dataset تمر بـ:

1. **فحص آلي** — سكربت `validate_dataset.py` يتحقق من صحة التنسيق
2. **مراجعة المحتوى** — التحقق من غياب البيانات الحقيقية وصحة المراجع القانونية
3. **قبول المساهمة** — Pull Request يُقبل بعد اجتياز الخطوتين السابقتين

Every contribution to this dataset goes through:

1. **Automated check** — `validate_dataset.py` verifies format validity
2. **Content review** — verifying absence of real data and accuracy of legal references
3. **Contribution acceptance** — Pull Request accepted after passing both steps

---

## إخلاء المسؤولية / Disclaimer

> هذا الـ dataset للأغراض البحثية والتعليمية فقط. لا يُعدّ محتواه استشارةً قانونية. المراجع القانونية الواردة هي للإرشاد — الرجوع دائمًا للمصدر الرسمي: هيئة الخبراء بمجلس الوزراء (boe.gov.sa) والجريدة الرسمية (uqn.gov.sa).
>
> This dataset is for research and educational purposes only. Its content does not constitute legal advice. Legal references are for guidance — always refer to official sources: Bureau of Experts (boe.gov.sa) and Official Gazette (uqn.gov.sa).
