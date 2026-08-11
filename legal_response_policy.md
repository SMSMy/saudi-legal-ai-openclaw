# سياسة الاستجابة القانونية — Legal Response Policy

> هذه الوثيقة تُطبَّق **برمجياً** في `mcp-server/tools/policy.py` — ليست توجيهاً نصياً للنموذج فقط.

## القواعد الأساسية

### 1. لا ادعاء قانوني بدون دليل
كل نتيجة تحتوي على ادعاء قانوني **يجب** أن تُرفق بـ `evidence[]` من مصدر داخل المستودع.
- إذا لم يوجد دليل: `insufficient_evidence: true` — لا ادعاء إطلاقاً.
- يُطبَّق هذا عبر `enforce_evidence()` في `policy.py`.

### 2. التمييز الصريح بين أنواع المعلومات

| النوع | المعنى | الإجراء |
|---|---|---|
| **نص نظامي** | مقتطف حرفي من مصدر رسمي | يُقدَّم مع citation واضح |
| **تفسير مبسّط** | شرح بلغة عادية | يُعلَّم صراحةً كـ "تفسير" |
| **معلومة تحتاج محامياً** | حالة فردية معقدة | يُوجَّه المستخدم لمختص |

### 3. الامتناع عند عدم كفاية الدليل
- إذا كان المصدر `verification_status: unverified` → تحذير صريح في الاستجابة.
- إذا كان المصدر `verification_status: outdated` → لا يُستخدم في إجابة جازمة.

### 4. الصيغة الموحدة الإلزامية

> **"هذه معلومات قانونية عامة وليست استشارة قانونية."**

تُدرج هذه الجملة في كل مخرج من مخرجات الأدوات دون استثناء.

### 5. نقطة المراجعة البشرية
المهام التالية تستلزم مراجعة محامٍ مرخّص قبل الاعتماد على النتيجة:
- قرارات تمس مالاً أو مواعيد قانونية
- وثائق رسمية أو عقود ذات قيمة عالية
- نزاعات تجارية أو عمالية جارية
- أي حالة يُعيد فيها النموذج `requires_escalation: true`

---

## تطبيق برمجي — `policy.py`

```python
from tools.policy import enforce_evidence

# صحيح — مع دليل
result = enforce_evidence(
    claim="يحق للموظف...",
    evidence=[{"source_id": "labor-law", "excerpt": "المادة 74: ..."}],
)

# صحيح — بلا دليل
result = enforce_evidence(claim="...", evidence=[])
# → {"insufficient_evidence": True, "disclaimer": "..."}
```

## شرط قبول الـ PRs لأدوات v0.3

أي أداة جديدة (`find_legal_provision`, `build_legal_brief`, إلخ) **يجب** أن تستدعي `enforce_evidence()` قبل إعادة أي ادعاء قانوني.
هذا شرط مدرج في PR template ولن يُقبل أي PR يخالفه.

---

## عقد معماري — `find_legal_provision` (v0.3)

`find_legal_provision` هي **طبقة معلومات خام** لا طبقة قرار:

- تُعيد **كل الأقسام** التي `score > 0`، مرتبةً تنازلياً.
- كل قسم يحمل `match_confidence` كمعلومة فقط — **لا قطع داخلي بأي عتبة**.
- `build_legal_brief` تطبق `MATCH_CONFIDENCE_THRESHOLD = 0.7` كبوابة `enforce_evidence` على نتائج `find_risks` المرنة.

### القاعدة الملزمة لكل أداة تستدعي `find_legal_provision` مباشرة:

> **أي أداة تستدعي `find_legal_provision()` مباشرة (لا عبر `build_legal_brief`)،
> يجب أن تفلتر `matched_sections` بـ `match_confidence >= MATCH_CONFIDENCE_THRESHOLD`
> قبل عرض النتائج كدليل مدعوم للمستخدم.**

عدم الالتزام بهذه القاعدة يُفضي إلى تسريب أقسام ذات ثقة منخفضة كسلطة قانونية — وهو بالضبط النمط الذي تمنعه `enforce_evidence`.

---

## 6. أنواع الأدلة وتصنيف الثقة (`review_level`)

يُطبق `enforce_evidence` تصنيفاً مستقلاً (`review_level`) على كل عنصر دليل يتم إرفاقه بالاستجابة. لا يجب الخلط بين `review_level` وبين `verification_status` الخاص بالمصدر أو المهارة نفسها.

تنقسم الأدلة إلى نوعين رئيسيين:
1. **نصوص تشريعية (Legislative Texts):**
   - تُجلب من المصادر (Sources) وتخضع لسلم الثقة البشري/الميداني (`verified`, `field_tested`, `unverified`).
   - `review_level` يُصبح مساوياً للحالة الفعلية (مع تحويل `verified` إلى `human_reviewed`).
2. **أدلة استدلال أو مهارات (Reasoning Guides/Skills):**
   - لا تُمثل نصوصاً قابلة للمصادقة وتُستثنى كلياً من سلم التوثيق.
   - حالة המهارة (`verification_status`) تكون دائماً `"not_applicable"`.
   - `review_level` في الدليل يُصبح دائماً `"reasoning_guide"`.

> **تنبيه:** إذا فُقد معرّف المصدر (`source_id` / `domain`)، يُعطى الدليل مستوى التقييم `"unknown"`.
