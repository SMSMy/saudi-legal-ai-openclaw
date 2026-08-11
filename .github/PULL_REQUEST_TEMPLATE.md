## وصف التغيير / Change Description

<!-- اشرح ماذا يغيّر هذا الـ PR وما سببه -->

## نوع التغيير / Change Type

- [ ] إضافة مصدر قانوني جديد (New legal source)
- [ ] تحديث مصدر موجود (Update existing source)
- [ ] إصلاح خطأ في محتوى قانوني (Fix legal content error)
- [ ] تغيير في الكود / البنية (Code / structure change)
- [ ] تحديث توثيق (Documentation update)

---

## قائمة التحقق الإلزامية / Required Checklist

### ⚠️ إذا كان PR يعدّل سلوك أداة استرجاع أو بحث (`search.py`، `reasoning.py`، `sources.py`، `eval_runner.py`):

هذا البند **إلزامي** ضمن نفس الـ commit — لا كـ PR منفصل لاحق.

- [ ] **إعادة تشغيل التقييم**: `python evals/metrics/eval_runner.py > evals/metrics/results/baseline_vXX.json`
- [ ] **تحديث `.gitignore`**: إضافة استثناء `!evals/metrics/results/baseline_vXX.json` للملف الجديد
- [ ] **مزامنة التوثيق**: أي ملف (`README.md`، `legal_response_policy.md`، docstring) يصف سلوك الأداة القديم يجب تحديثه

> **السبب**: تكرر عبر v0.2 وv0.3 أن الكود يُصحَّح لكن eval_runner أو الـ baseline يبقى يعكس النسخة القديمة لجولة كاملة.
> الأرقام التي لا تعكس الكود الفعلي ليست قياساً — هي ضوضاء.

---

### إذا كان PR يغيّر محتوى قانونياً في `sources/` أو `skills/`:

- [ ] **diff للمصدر**: ما الذي تغيّر بالضبط في الملف؟
- [ ] **تحديث manifest**: هل حُدِّث `sources/manifests/<id>.json` مع SHA256 الجديد؟
- [ ] **سبب التعديل + الرابط الرسمي**: ما مصدر المعلومة الجديدة؟ (رابط boe.gov.sa / uqn.gov.sa أو ما يعادله)
- [ ] **نتيجة tests**: هل جميع الاختبارات تعمل؟ (`pytest tests/ -q`)
- [ ] **نتيجة validate_manifests**: (`python scripts/validate_manifests.py`)

### للمصادر عالية الأثر (عمل / PDPL / عقود / إفلاس / شركات / إجراءات قضائية):

- [ ] **reviewer sign-off**: تأكيد من مراجع قانوني سعودي إن توفر
  - المراجع: <!-- أضف اسم المراجع أو "غير متاح" -->
  - إذا لم يتوفر مراجع: `verification_status` يبقى `unverified` في الـ manifest

---

## معلومات إضافية / Additional Notes

<!-- أي سياق إضافي يساعد المراجع -->

---

> ⚠️ **تذكير**: لا ادعاء قانوني بدون citation من مصدر داخل المستودع.
> هذه معلومات قانونية عامة وليست استشارة قانونية.
