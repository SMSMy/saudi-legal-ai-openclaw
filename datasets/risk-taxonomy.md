# Risk Taxonomy / تصنيف مستويات المخاطر

**يُستخدم هذا الملف لتوحيد تصنيف عمود `risk_level` في الـ dataset.**
**This file standardizes the classification of the `risk_level` column in the dataset.**

---

## نظرة عامة / Overview

```
critical  →  يوقف الإجراء / Stop proceeding
high      →  تصعيد عاجل / Urgent escalation
medium    →  تعديل قبل التوقيع / Amend before signing
low       →  ملاحظة تحسينية / Improvement note
```

---

## critical — حرج

### التعريف / Definition

بند يُنشئ خطرًا قانونيًا جسيمًا يجعل المضي في التوقيع دون معالجة أمرًا غير مقبول — سواء لتعارضه مع نظام آمر، أو لتهديده الوجود القانوني للعقد، أو لتعرضه مصالح جوهرية لخطر فادح.

A clause that creates a serious legal risk making it unacceptable to proceed to signing without resolution — whether due to conflict with a mandatory regulation, threatening the legal existence of the contract, or exposing core interests to severe risk.

### متى نستخدمه / When to Use

- البند يتعارض صراحةً مع نص نظامي آمر لا يجوز الاتفاق على مخالفته
- البند يُسقط حقًا نظاميًا لا يجوز التنازل عنه (إجازة سنوية، مكافأة نهاية خدمة، حقوق PDPL)
- البند ينطوي على ربا صريح في عقد تمويل
- البند يُفقد العقد ركنًا أساسيًا (غياب الثمن، الغرر الجسيم في موضوع العقد)
- البند يُلزم بفعل مخالف للشريعة أو النظام العام السعودي

- The clause explicitly conflicts with a mandatory regulation that cannot be contracted around
- The clause waives a non-waivable statutory right (annual leave, EOSB, PDPL rights)
- The clause involves explicit usury (riba) in a finance contract
- The clause eliminates an essential contract element (absent price, extreme gharar in subject matter)
- The clause requires an act contrary to Sharia or Saudi public order

### أمثلة قانونية سعودية / Saudi Legal Examples

| المثال | السبب |
|--------|-------|
| شرط إسقاط مكافأة نهاية الخدمة في عقد عمل | المادة 84 من نظام العمل — حق آمر لا يُسقط |
| نقل بيانات شخصية للخارج بلا أساس قانوني | PDPL المادتان 29-30 — مخالفة صريحة |
| فائدة ثابتة على قرض نقدي في عقد غير مالي | تعارض مع أحكام الشريعة الإسلامية |
| إسناد اختصاص قضائي أجنبي في نزاع عمالي | المحاكم العمالية السعودية ذات اختصاص آمر |
| عقد بلا تحديد للثمن أو ضابط لحسابه | يفتقد ركن المحل — قد يُفضي للبطلان |

---

## high — مرتفع

### التعريف / Definition

بند يُنشئ مخاطر قانونية أو تجارية جسيمة لا تجعل العقد باطلًا بالضرورة لكنها تعرّض الطرف لخسائر أو نزاعات محتملة كبيرة إذا لم تُعالَج قبل التوقيع.

A clause that creates significant legal or commercial risks that do not necessarily void the contract but expose the party to potential major losses or disputes if not addressed before signing.

### متى نستخدمه / When to Use

- بند جزاء تعسفي مبالغ فيه قابل للتخفيف القضائي لكنه يُنشئ ضغطًا قانونيًا غير متوازن
- حد مسؤولية يتضارب تضاربًا صارخًا مع قيمة العقد
- حق إنهاء أحادي مفرط الاتساع لأحد الأطراف
- بند تعديل أحادي للشروط الجوهرية
- شرط اختصاص قضائي أجنبي في عقد لا يحتمله عمليًا

- An excessive penalty clause subject to judicial reduction but creating disproportionate legal pressure
- A liability cap starkly disproportionate to the contract value
- An excessively broad unilateral termination right for one party
- A clause allowing unilateral amendment of material terms
- A foreign jurisdiction clause in a contract that practically cannot sustain it

### أمثلة قانونية سعودية / Saudi Legal Examples

| المثال | السبب |
|--------|-------|
| حد مسؤولية بـ USD 500 في عقد بمليون ريال | تفاوت جسيم يُشبه الإعفاء الكامل |
| إنهاء الخدمة بـ 7 أيام فقط لعقد ثلاث سنوات | إنهاء تعسفي محتمل — م/80 نظام العمل |
| غرامة إنهاء = كامل القيمة المتبقية | قد يُخفَّف قضائيًا لكنه يُكبّل الطرف |
| شرط تحكيم في لندن لعقد لوجستيات سعودي | عسير التطبيق وعالي التكلفة على العميل |
| ملكية المخرجات تؤول للمزود لا للممول | يُفقد العميل ما دفع ثمنه |

---

## medium — متوسط

### التعريف / Definition

بند يحتوي غموضًا أو ثغرة أو تفاوتًا في الحقوق يستوجب معالجة قبل التوقيع لكنه لا يُنشئ خطرًا جسيمًا فوريًا.

A clause containing ambiguity, a gap, or a rights imbalance that requires addressing before signing but does not create an immediate serious risk.

### متى نستخدمه / When to Use

- تعريفات ناقصة أو تحتمل أكثر من تفسير
- حالات لم يُعالجها العقد (صمت تعاقدي)
- بنود القوة القاهرة الفضفاضة أو الضيقة بشكل غير معتاد
- آلية دفع غامضة (بدون تواريخ، عملة، أو مرجع)
- غياب آلية لتعديل الأسعار في العقود الطويلة

- Incomplete definitions or definitions open to multiple interpretations
- Situations the contract does not address (contractual silence)
- Unusually broad or narrow force majeure clauses
- Vague payment mechanism (no dates, currency, or reference)
- Absence of a price adjustment mechanism in long-term contracts

### أمثلة قانونية سعودية / Saudi Legal Examples

| المثال | السبب |
|--------|-------|
| "في أقرب وقت ممكن" بدلًا من مدة محددة | غموض يُفضي لنزاع حول التأخر |
| بند قوة قاهرة يشمل "تصرفات الحكومة" | قد يُستخدم للتهرب من الالتزامات |
| غياب آلية مراجعة أسعار في عقد 5 سنوات | التضخم قد يُربك التوازن التعاقدي |
| عدم تحديد العملة في عقد بين طرفين مختلفَي الجنسية | نزاع محتمل عند تذبذب أسعار الصرف |
| بند سرية بلا تعريف للمعلومات السرية | نطاق غير محدد = حماية فعلية أقل |

---

## low — منخفض

### التعريف / Definition

ملاحظة تحسينية أو ثغرة شكلية لا تُنشئ خطرًا قانونيًا جسيمًا — يُنصح بمعالجتها لكنها لا تحول دون التوقيع.

An improvement note or formal gap that does not create a serious legal risk — addressing it is recommended but it does not prevent signing.

### متى نستخدمه / When to Use

- غياب بند الإشعارات أو طريقة التبليغ
- التواريخ بالميلادي فقط دون الهجري
- غياب ختم الشركة أو بيانات السجل التجاري على الصفحة الأولى
- عدم تحديد اللغة المعتمدة عند وجود نسختين
- غياب بيانات الاتصال للمستشار القانوني

- Absence of a notices clause or notification method
- Dates in Gregorian calendar only without Hijri equivalent
- Absence of company seal or commercial registration details on the first page
- Failure to specify the governing language when two versions exist
- Absence of legal counsel contact details

### أمثلة قانونية سعودية / Saudi Legal Examples

| المثال | السبب |
|--------|-------|
| التواريخ ميلادية فقط | المحاكم والجهات السعودية تعتمد الهجري |
| غياب بند الإشعارات | يُعقّد إثبات التبليغ عند النزاع |
| عدم ذكر رقم السجل التجاري | قد يُبطئ إجراءات التوثيق |
| غياب تحديد اللغة المعتمدة | لبس محتمل عند نسختين لغويتين |
| بيانات اتصال ناقصة | تعقيد في إجراءات التبليغ الرسمي |

---

## جدول مقارنة سريعة / Quick Comparison Table

| المعيار | critical 🔴 | high 🟠 | medium 🟡 | low 🟢 |
|---------|------------|--------|----------|-------|
| **يوقف التوقيع؟** | نعم — فورًا | نعم — حتى المعالجة | يُنصح | لا |
| **يستوجب محاميًا؟** | نعم — حتمًا | نعم — بشدة | يُنصح | اختياري |
| **`requires_escalation`** | `yes` دائمًا | `yes` في الغالب | `no` في الغالب | `no` |
| **مصدر الخطر** | نص نظامي | توازن تجاري | غموض | شكل |
| **الأثر المحتمل** | بطلان / مساءلة | خسارة كبيرة | نزاع | إجراءات أبطأ |
