# Enum: contract_type

**عمود:** `contract_type`
**Column:** `contract_type`

هذا الملف هو المرجع الرسمي للقيم المقبولة في عمود `contract_type` بالـ dataset.
This file is the authoritative reference for accepted values in the `contract_type` column.

**المُتحقَّق بواسطة / Validated by:** `scripts/validate_dataset.py`

---

## القيم المقبولة / Accepted Values

| القيمة | نوع العقد بالعربي | الأنظمة السعودية الرئيسية ذات الصلة |
|--------|-----------------|--------------------------------------|
| `Employment Contract` | عقد العمل | نظام العمل م/51 1426هـ |
| `SaaS Agreement` | اتفاقية SaaS | نظام المعاملات المدنية م/191، PDPL م/19 |
| `Professional Services Agreement` | اتفاقية خدمات مهنية | نظام المعاملات المدنية م/191 |
| `Construction Contract` | عقد المقاولة والإنشاء | نظام المعاملات المدنية م/191 |
| `Supply Agreement` | عقد التوريد والمشتريات | نظام المعاملات المدنية م/191 |
| `NDA` | اتفاقية عدم الإفصاح | نظام المعاملات المدنية م/191، PDPL م/19 |
| `Shareholder Agreement` | اتفاقية المساهمين | نظام الشركات م/132 1443هـ |
| `Franchise Agreement` | عقد الامتياز التجاري | نظام المعاملات المدنية م/191، نظام الوكالة التجارية |
| `Commercial Agency Agreement` | عقد الوكالة التجارية | نظام الوكالة التجارية م/11 1382هـ وتعديلاته |
| `Lease Agreement` | عقد الإيجار | نظام المعاملات المدنية م/191، نظام إيجار |
| `Cloud Storage Agreement` | اتفاقية التخزين السحابي | نظام المعاملات المدنية م/191، PDPL م/19 |

## قواعد الاختيار / Selection Rules

- استخدم القيمة الأقرب لنوع العقد الفعلي — لا تستخدم `Professional Services Agreement` لعقد SaaS
- Use the value closest to the actual contract type — do not use `Professional Services Agreement` for a SaaS contract
- **`Cloud Storage Agreement`** مخصص لعقود التخزين السحابي المستقلة — عقود SaaS المتكاملة تستخدم `SaaS Agreement`
- **`NDA`** يشمل اتفاقيات السرية المستقلة — بنود السرية ضمن عقد أكبر تُصنَّف بنوع العقد الأكبر
- القيم حساسة لحالة الأحرف — `Employment Contract` لا `employment contract`
- Values are case-sensitive — `Employment Contract` not `employment contract`

## إضافة نوع عقد جديد / Adding a New Contract Type

لإضافة نوع عقد غير موجود:
1. افتح Issue مع وصف النوع ومثال عليه
2. بعد الموافقة أضفه لهذا الملف وعدّل `scripts/validate_dataset.py`

To add a contract type not listed here:
1. Open an Issue describing the type with an example
2. After approval add it here and update `scripts/validate_dataset.py`
