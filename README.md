# المنظومة القانونية السعودية للذكاء الاصطناعي 🇸🇦
# Saudi Legal AI Framework — OpenClaw Edition

[![Version](https://img.shields.io/badge/version-0.4-blue.svg)](https://github.com/SMSMy/saudi-legal-ai-openclaw)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-ready-green.svg)](https://openclaw.ai)

> ⚠️ للبحث الأولي فقط — ليس استشارة قانونية. يجب مراجعة مختص قانوني مرخص في المملكة العربية السعودية.
> For preliminary research only — not legal advice. Must be reviewed by a licensed Saudi legal professional.

---

## 🦞 مبني لـ OpenClaw | Built for OpenClaw

هذه النسخة **مُكيّفة خصيصاً لـ [OpenClaw](https://openclaw.ai)** — مساعد ذكي متعدد القنوات والنماذج.

> This edition is **specifically adapted for OpenClaw** — a multi-channel, multi-model AI assistant.

**الفرق عن النسخة الأصلية:**
- ✅ سيرفر **استرجاع خالص** — لا يحتاج أي مفتاح API (المساعد هو اللي يحلل بالنموذج النشط)
- ✅ تكامل كامل مع OpenClaw — أي نموذج (DeepSeek, GLM, Mimo, ...) يشتغل مباشرة
- ✅ لا Docker، لا Anthropic، لا مفاتيح خارجية

**What's different from the original:**
- ✅ Pure **retrieval server** — no API keys needed (the agent analyzes with its active model)
- ✅ Full OpenClaw integration — any model works out of the box
- ✅ No Docker, no Anthropic, no external keys

---

## 📦 تركيب سريع | Quick Install

```bash
# 1. Clone + venv
git clone https://github.com/SMSMy/saudi-legal-ai-openclaw.git
cd saudi-legal-ai-openclaw
python3 -m venv .venv
.venv/bin/pip install -e .

# 2. Register in OpenClaw
openclaw mcp set saudi-legal \
  '{"command":"'$(pwd)'/.venv/bin/saudi-legal-mcp","args":[]}'

# 3. Reload
openclaw mcp reload
```

**Done!** Legal tools ready — standard Python package, no env-var hacks needed. 🔓

> **تلميح:** الحزمة تثبّت `mcp<2.0.0` تلقائياً (مُقيَّدة في pyproject.toml).
> لو ظهر خطأ `ModuleNotFoundError: No module named 'mcp.server.fastmcp'`
> فبيئتك فيها mcp 2.0.0 — أزله ثم أعد التثبيت: `pip uninstall mcp && pip install -e .`

---

## 🛠️ الأدوات | Tools

| الأداة | الوصف |
|--------|---------|
| `get_legal_skill` | استرجاع/تحميل المهارات القانونية المجالية بالكامل (أو metadata / section فقط) |
| `get_regulation_source` | قراءة المصادر النظامية المحددة (metadata افتراضياً؛ include_content لقراءة النص) |
| `get_legal_context` | تجميع سياق قانوني موحّد (مهارة + مصدر + حالة في استدعاء واحد) |
| `search_contract_risks` | بحث في مخاطر العقود مع policy enforcement (evidence إلزامي) |
| `list_legal_domains` | قائمة كل المجالات والمصادر المتاحة مع حالة التحقق |
| `get_source_status` | حالة المصدر: verification_status، freshness، تحذير منتهي الصلاحية |
| `report_source_issue` | تسجيل مشكلة في مصدر (يتطلب ENABLE_LOCAL_REPORTS=true) |
| `search_legal_provision` | بحث نصي في نصوص الأنظمة (أل التعريف aliasing). **بوابة ثقة 0.7**: الأقسام الأضعف تُستبعد برمجياً، لا تُعرض بتحذير |
| `get_legal_brief` | مذكرة موحّدة من مهارة + نصوص + مخاطر. **بوابات إلزامية**: `insufficient_evidence` عند نقص الدليل أو هيمنة `[يحتاج تحقق]` |

**سياسة الأدلة (evidence policy):** لا ادعاء بلا citation داخل المستودع. أي نتيجة يجب أن تحمل `evidence[]` أو `insufficient_evidence: true`. عند اقتطاع المحتوى الطويل يُعاد `sections_index` (فهرس العناوين) ليكتشف الوكيل الأقسام البعيدة بدل تخمينها.

---

## 📚 المحتوى | Content

| المجلد | المحتوى |
|--------|---------|
| `skills/` | 9 مهارات قانونية: العقود، نظام العمل، حماية البيانات، النزاعات، الشركات، العقارات، التجارة الإلكترونية، الرياضة، ZATCA |
| `sources/` | 20 مصدر نظامي (source_documents_count=20، reference_collections_count=2، verified_sources_count=0) |
| `sources/manifests/` | 20 manifest JSON لكل مصدر (sha256، verification_status، مواعيد المراجعة الدورية) |
| `datasets/` | مجموعة مخاطر تعاقدية + جدول مصادر + تعريفات المجال |
| `examples/` | 14 مثال تفاعلي مع كل الأدوات |
| `prompts/` | نصوص التوجيه (الإجابة الآمنة، الصياغة المقيدة، الكشف عن المخاطر) |
| `scripts/` | generate_manifests.py، validate_manifests.py، propose_verification.py |
| `tests/` | 65 اختباراً آلياً (بدون API خارجي) — تشمل حراسة تسجيل الأدوات وبوابات الثقة |
| `evals/` | corpus 65 سؤالاً + eval_runner.py + baseline_v04_7_fullcover.json (recall=86.2%، precision=97.2%) |
| `memory/` | دروس الجلسات الحرجة — ما تعلمه المشروع من اكتشافات الاستخدام الفعلي |

---

## 🔒 الأمان | Security

- ✅ **بدون أي مفتاح API** — السيرفر لا يتصل بأي خدمة خارجية
- ✅ **بيانات محلية** — كل الملفات نصية مقروءة محلياً
- ✅ **مصادر رسمية** — الأنظمة منشورة على boe.gov.sa و uqn.gov.sa
- ⚠️ **ليس استشارة قانونية** — للمراجعة الأولية فقط

---

## 🤝 المساهمة | Contributing

المنظومة القانونية السعودية مشروع مفتوح المصدر. رحب بمساهماتك: إضافة أنظمة جديدة، تحسين المهارات، بيانات مخاطر، أمثلة تطبيقية.

راجع [CONTRIBUTING.md](CONTRIBUTING.md) للتفاصيل.

This is an open-source project. Contributions welcome: new regulations, improved skills, risk data, worked examples.

---

## 📄 الرخص | License

MIT License — للاستخدام الحر مع نسب المصدر والاحتفاظ بإخلاء المسؤولية القانوني.

MIT License — free to use with attribution and retention of legal disclaimer.

---

## 🔗 الشكر | Credits

- النسخة الأصلية: [Samix2026/saudi-legal-ai-framework](https://github.com/Samix2026/saudi-legal-ai-framework)
- هذا الـ fork: مُكيّف خصيصاً لـ OpenClaw بواسطة [SMSMy](https://github.com/SMSMy)
