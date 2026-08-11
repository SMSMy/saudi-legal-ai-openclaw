# Enum: industry

**عمود:** `industry`
**Column:** `industry`

هذا الملف هو المرجع الرسمي للقيم المقبولة في عمود `industry` بالـ dataset.
This file is the authoritative reference for accepted values in the `industry` column.

**المُتحقَّق بواسطة / Validated by:** `scripts/validate_dataset.py`

---

## القيم المقبولة / Accepted Values

| القيمة | القطاع بالعربي | Arabic Sector | أمثلة على العقود |
|--------|--------------|---------------|-----------------|
| `Technology` | تقنية المعلومات | Technology & IT | SaaS، تطوير برمجيات، استضافة سحابية |
| `Professional Services` | الخدمات المهنية | Professional Services | استشارات، محاسبة، هندسة، قانون |
| `Construction` | الإنشاءات | Construction | مقاولات، تصميم، إشراف على مشاريع |
| `Healthcare` | الرعاية الصحية | Healthcare | مستشفيات، مختبرات، تجهيزات طبية |
| `Real Estate` | العقارات | Real Estate | إيجار، بيع، تطوير عقاري |
| `Finance` | المالية والمصرفية | Finance & Banking | تمويل، استثمار، تأمين، بنوك |
| `Retail` | التجزئة | Retail | توريد، امتياز تجاري، توزيع |
| `Logistics` | اللوجستيات | Logistics & Supply Chain | شحن، مستودعات، سلسلة توريد |
| `Energy` | الطاقة | Energy & Oil & Gas | نفط، غاز، طاقة متجددة |
| `Education` | التعليم | Education | مدارس، جامعات، تدريب مهني |
| `Government` | الجهات الحكومية | Government | عقود حكومية، مناقصات، BOT |
| `General` | عام | General / Cross-Sector | لا ينتمي لقطاع محدد أو متعدد القطاعات |

## قواعد الاختيار / Selection Rules

- استخدم القطاع الأكثر تحديدًا — `Technology` أولى من `General` لعقد SaaS
- Use the most specific sector — prefer `Technology` over `General` for a SaaS contract
- إذا كان العقد يمتد لأكثر من قطاع، اختر القطاع المسيطر أو استخدم `General`
- If the contract spans multiple sectors, choose the dominant one or use `General`
- القيم حساسة لحالة الأحرف — `Technology` لا `technology` ولا `TECHNOLOGY`
- Values are case-sensitive — `Technology` not `technology` or `TECHNOLOGY`
