# المنظومة القانونية السعودية للذكاء الاصطناعي 🇸🇦
# Saudi Legal AI Framework — OpenClaw Edition

[![Version](https://img.shields.io/badge/version-0.2-orange.svg)](https://github.com/SMSMy/saudi-legal-ai-framework)
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
git clone https://github.com/SMSMy/saudi-legal-ai-framework.git
cd saudi-legal-ai-framework
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# 2. Register in OpenClaw
openclaw mcp set saudi-legal \
  '{"command":"'$(pwd)'/.venv/bin/python","args":["'$(pwd)'/mcp-server/server.py"],"env":{"REPO_PATH":"'$(pwd)'"},"cwd":"'$(pwd)'"}'

# 3. Reload
openclaw mcp reload
```

**Done!** 5 legal tools ready — no API key configuration needed. 🔓

---

## 🛠️ الأدوات | Tools

| الأداة | الوظيفة |
|--------|---------|
| `get_legal_skill` | المهارة/الدليل القانوني لمجال محدد |
| `get_regulation_source` | ملخص النظام السعودي الرسمي |
| `get_legal_context` | السياق الكامل لتحليل عقد (مهارة + نظام + مخاطر) |
| `search_contract_risks` | بحث في قاعدة بيانات المخاطر العقدية |
| `list_legal_domains` | تصفح كل المجالات والمصادر المتاحة |

---

## 📚 المحتوى | Content

| المجلد | المحتوى |
|--------|---------|
| `skills/` | 9 مهارات قانونية: عقود، نزاعات تجارية، عمل، امتثال، تحكيم، صياغة، عقار، ملكية فكرية، منازعات رياضية |
| `sources/` | 20 ملخص نظام سعودي: العمل، الشركات، المعاملات المدنية، المحاكم التجارية، PDPL، التجارة الإلكترونية... |
| `datasets/` | بيانات المخاطر العقدية + أدلة قضائية + إجراءات امتثال |
| `examples/` | 14 مثال تطبيقي موثق عبر المجالات القانونية |
| `prompts/` | قوالب مطالبات جاهزة (تحليل مخاطر، مراجعة عقود، صياغة إشعارات) |

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
