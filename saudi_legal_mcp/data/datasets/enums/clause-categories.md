# Enum: clause_category

**عمود:** `clause_category`
**Column:** `clause_category`

هذا الملف هو المرجع الرسمي للقيم المقبولة في عمود `clause_category` بالـ dataset.
This file is the authoritative reference for accepted values in the `clause_category` column.

**المُتحقَّق بواسطة / Validated by:** `scripts/validate_dataset.py`

---

## القيم المقبولة / Accepted Values

| القيمة | التصنيف بالعربي | الأنظمة ذات الصلة الشائعة |
|--------|----------------|--------------------------|
| `Jurisdiction & Dispute Resolution` | الاختصاص القضائي وفض النزاعات | نظام التحكيم م/34، نظام المحاكم التجارية م/93 |
| `Liability` | المسؤولية والتعويض | نظام المعاملات المدنية م/191 |
| `Data Protection & Privacy` | حماية البيانات والخصوصية | PDPL م/19 |
| `Intellectual Property` | الملكية الفكرية | نظام حماية الملكية الفكرية م/41 |
| `Termination` | إنهاء العقد | نظام المعاملات المدنية م/191، نظام العمل م/51 |
| `Confidentiality` | السرية | نظام المعاملات المدنية م/191، PDPL م/19 |
| `Payment Terms` | شروط الدفع ومواعيده | نظام المعاملات المدنية م/191 |
| `Governing Law` | القانون الحاكم | نظام المعاملات المدنية م/191 |
| `Force Majeure` | القوة القاهرة | نظام المعاملات المدنية م/191 |
| `Warranties` | الضمانات والكفالات | نظام المعاملات المدنية م/191 |
| `Indemnification` | التعويض والإبراء | نظام المعاملات المدنية م/191 |
| `Employment & Labor` | العمل والموارد البشرية | نظام العمل م/51 |
| `Saudization` | السعودة ونطاقات | نظام العمل م/51، لوائح نطاقات |
| `Corporate Governance` | حوكمة الشركات | نظام الشركات م/132 |

## ملاحظات التصنيف / Classification Notes

- **`Jurisdiction & Dispute Resolution`** يشمل: التحكيم، الوساطة، الاختصاص القضائي، اختيار محكمة
- **`Governing Law`** هو القانون الحاكم للعقد — يختلف عن **`Jurisdiction`** الذي هو مكان التقاضي
- **`Confidentiality`** للبنود العامة — **`Data Protection & Privacy`** للبنود المتعلقة بـ PDPL تحديدًا
- **`Termination`** يشمل: الإنهاء بعذر، التعسفي، بالإشعار، الفوري، وشروط الإنهاء المتبادل
- القيم حساسة لحالة الأحرف والمسافات — انسخ القيمة من الجدول أعلاه بالضبط
- Values are case- and space-sensitive — copy the value from the table above exactly
