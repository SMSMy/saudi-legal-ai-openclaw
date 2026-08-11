# Severity Standards / معايير الخطورة الموحَّدة

**هذا الملف يُحدد كيف نُقيّم الخطورة ومتى نُصعّد للمختص القانوني.**
**This file defines how we assess severity and when to escalate to a legal specialist.**

---

## الفرق بين `risk_level` و `requires_escalation`
## Difference Between `risk_level` and `requires_escalation`

كثيرًا ما يُخلَط بين المفهومين. هما متصلان لكن ليسا متطابقين:

The two concepts are often confused. They are related but not identical:

| | `risk_level` | `requires_escalation` |
|--|-------------|----------------------|
| **ما يقيس** | خطورة البند في حد ذاته | الحاجة لتدخل محامٍ مختص **فورًا** |
| **What it measures** | Severity of the clause itself | Need for immediate specialist attorney intervention |
| **من يحدده** | المحلِّل أو الذكاء الاصطناعي | قواعد موضوعية محددة في هذا الملف |
| **Who sets it** | Analyst or AI | Objective rules defined in this file |
| **نطاق القيم** | critical / high / medium / low | yes / no فقط |
| **Value range** | critical / high / medium / low | yes / no only |

### المبدأ الجوهري / Core Principle

> ليس كل بند `critical` يستوجب `requires_escalation = yes` بالضرورة في كل سياق — وليس كل بند `requires_escalation = yes` بالضرورة `critical`. لكن في الغالب يرتبطان.

> Not every `critical` clause necessarily requires `requires_escalation = yes` in every context — and not every `requires_escalation = yes` is necessarily `critical`. But they are usually correlated.

**مثال على الفرق:**
- بند إجازة سنوية 15 يومًا في عقد عمل: `risk_level = critical` (مخالف للنظام) لكن `requires_escalation = no` إذا كان التعديل بسيطًا ومعروفًا
- عقد استحواذ يتضمن شرطًا غامضًا حول نقل الموظفين: `risk_level = medium` لكن `requires_escalation = yes` لأن التبعات على مئات الموظفين كبيرة

---

## معايير تحديد `requires_escalation`
## Criteria for Setting `requires_escalation`

### يجب أن يكون `yes` إذا / Must be `yes` if:

**1. قيمة العقد أو التبعات كبيرة**
- قيمة العقد تتجاوز 500,000 ريال سعودي، أو
- قرار يُؤثر على أكثر من 50 موظفًا، أو
- تبعات ضريبية أو تنظيمية تتجاوز 100,000 ريال

- Contract value exceeds SAR 500,000, or
- Decision affects more than 50 employees, or
- Tax or regulatory consequences exceed SAR 100,000

**2. مسائل تنازع القوانين**
- طرف أجنبي مع بنود اختصاص قضائي خارج المملكة
- عقد يختار قانونًا أجنبيًا لمسائل لها أنظمة آمرة سعودية

- Foreign party with jurisdiction clauses outside the Kingdom
- Contract choosing foreign law for matters with Saudi mandatory regulations

**3. مخاطر PDPL جسيمة**
- نقل بيانات شخصية خارج المملكة بلا أساس قانوني
- معالجة بيانات حساسة (صحة، بيومترية، معتقدات)
- غياب آلية الإبلاغ عن الاختراقات

- Cross-border transfer of personal data without legal basis
- Processing sensitive data (health, biometric, beliefs)
- Absence of breach notification mechanism

**4. مسائل شرعية**
- أي شبهة ربا في عقود التمويل والمضاربة
- غرر مفضٍ لجهالة جسيمة في موضوع العقد أو ثمنه

- Any suspicion of usury in finance or partnership contracts
- Gharar leading to major uncertainty in the contract subject or price

**5. الإخلال الفعلي أو النزاع القائم**
- وجود خلاف قائم بين الأطراف حول تفسير البند
- إشعار رسمي بالإخلال سبق توجيهه لأي طرف

- An existing dispute between parties over the clause's interpretation
- A formal breach notice previously issued to any party

**6. ملكية فكرية أو أسرار تجارية جوهرية**
- العقد يتضمن نقل براءات اختراع أو أسرار تجارية حيوية
- بنود ملكية تطال مخرجات استراتيجية للشركة

- Contract involving transfer of patents or vital trade secrets
- Ownership clauses affecting the company's strategic outputs

---

### يكون `no` إذا / Should be `no` if:

- البند مشكلته شكلية أو تنسيقية (مستوى `low`)
- البند يحتاج تعديلًا بسيطًا معروفًا وموثَّقًا في هذا الإطار
- القيمة المالية للعقد منخفضة ولا توجد تبعات تنظيمية
- البند `medium` وتبعاته محدودة نطاقًا
- الطرفان محترفان في هذا النوع من العقود وعلى دراية بالمخاطر

- The clause's issue is formal or formatting-related (level `low`)
- The clause needs a simple, well-documented amendment covered in this framework
- The contract's financial value is low with no regulatory consequences
- The clause is `medium` with limited scope implications
- Both parties are experienced with this contract type and aware of the risks

---

## متى نُصعّد لمحامٍ متخصص / When to Escalate to a Specialist Attorney

التصعيد لا يعني محاميًا عامًا — بل متخصصًا في المجال. الجدول التالي يُوجّه التصعيد:

Escalation means a specialist in the relevant field — not just any attorney:

| نوع الإشكالية | التخصص المطلوب |
|--------------|---------------|
| عقود عمل — فصل، مكافأة، نزاع | محامٍ متخصص في نظام العمل |
| PDPL — نقل بيانات، اختراق | مستشار حماية بيانات / محامٍ تقنية |
| عقود تمويل — ربا، مضاربة | مستشار قانوني متخصص في التمويل الإسلامي |
| تحكيم — شرط تحكيم، تنفيذ حكم | محكّم أو محامٍ متخصص في التحكيم |
| استحواذ وشركات | محامٍ متخصص في قانون الشركات |
| عقارات وإنشاءات | محامٍ متخصص في العقود العقارية |
| ملكية فكرية | محامٍ متخصص في الملكية الفكرية (SAIP) |
| نزاعات تجارية | محامٍ متخصص في التقاضي التجاري |

---

## أمثلة عملية مقارنة / Practical Comparative Examples

### المثال 1 — عقد عمل / Employment Contract

| البند | risk_level | requires_escalation | السبب |
|-------|-----------|---------------------|-------|
| إجازة سنوية 15 يومًا (بدلًا من 21) | critical | no | التعديل بسيط ومعروف — يُصحَّح بتعديل البند |
| فصل بلا سبب مشروع وبلا مكافأة | critical | yes | نزاع عمالي محتمل — يستلزم محاميًا عماليًا |
| فترة تجربة 9 أشهر | high | no | يكفي تعديل المدة للحد النظامي (180 يومًا) |
| غياب بند الإشعارات | low | no | شكلي — لا يؤثر على الحقوق الجوهرية |

### المثال 2 — عقد SaaS / SaaS Agreement

| البند | risk_level | requires_escalation | السبب |
|-------|-----------|---------------------|-------|
| تخزين بيانات خارج المملكة بلا أساس PDPL | critical | yes | مخاطر PDPL جسيمة تستلزم مختص بيانات |
| حد مسؤولية USD 500 لعقد 2M ريال | critical | yes | قيمة مرتفعة + شرط تعسفي واضح |
| حق تعليق الخدمة بلا إشعار | high | no | يكفي التفاوض على مهلة 10 أيام |
| غياب SLA | medium | no | يُضاف ملحق مستوى الخدمة كوثيقة منفصلة |

### المثال 3 — اتفاقية مساهمين / Shareholder Agreement

| البند | risk_level | requires_escalation | السبب |
|-------|-----------|---------------------|-------|
| غياب آلية تقييم الحصص عند الخروج | high | yes | قيمة الحصص كبيرة وتستلزم متخصصًا في قانون الشركات |
| حق الفيتو المطلق لشريك أقلية | high | yes | يُعطّل اتخاذ القرار ويستلزم هيكلة قانونية دقيقة |
| بند عدم منافسة لمدة 10 سنوات | medium | no | المدة مفرطة لكن قابلة للتعديل التفاوضي |
| غياب تعريف "منافس مباشر" | low | no | توضيح تعريفي كافٍ |

---

## خلاصة / Summary

```
risk_level = critical  →  requires_escalation = yes  (في الغالب)
risk_level = high      →  requires_escalation = yes  (إذا كانت القيمة أو التبعات كبيرة)
risk_level = medium    →  requires_escalation = no   (في الغالب)
risk_level = low       →  requires_escalation = no   (دائمًا تقريبًا)
```

**القاعدة الذهبية:** عند الشك، اجعلها `yes`. التصعيد لمختص أفضل من معالجة خاطئة.
**Golden rule:** When in doubt, set `yes`. Escalating to a specialist is better than handling it incorrectly.
