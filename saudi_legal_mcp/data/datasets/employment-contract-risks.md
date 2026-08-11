# مجموعة بيانات: أنماط مخاطر عقود العمل السعودية
# Dataset: Saudi Employment Contract Risk Patterns

**الغرض:** توثيق الأنماط الشائعة لبنود العقود العمالية عالية الخطورة في السياق السعودي — سياق تدريبي للذكاء الاصطناعي ومرجع للمراجعة القانونية
**Purpose:** Document common high-risk employment clause patterns in the Saudi context — AI training context and legal review reference

**المصدر التشريعي الرئيسي:** نظام العمل الصادر بالمرسوم الملكي م/51 لعام 1426هـ وتعديلاته
**Primary Legislative Source:** Saudi Labor Law (Royal Decree M/51 1426H) and amendments

**الملفات ذات الصلة:**
- `skills/labor-law-analysis.md` — الاستدلال القانوني
- `sources/labor-law.md` — المرجع التشريعي
- `datasets/judicial-decisions/labor/` — الأحكام القضائية المرتبطة
- `datasets/risk-taxonomy.md` — معايير تصنيف المخاطر
- `datasets/severity-standards.md` — معايير الخطورة والتصعيد

---

## تحذير / Warning

> هذا ملف بيانات تعليمي. الأنماط الموثقة هنا للاسترشاد لا للحكم القانوني القاطع. يجب مراجعة أي عقد مع محامٍ مرخص في المملكة العربية السعودية قبل التوقيع أو اتخاذ إجراء.
>
> This is an educational dataset file. Documented patterns are for reference only and do not constitute definitive legal rulings. Any contract must be reviewed with a licensed attorney in the Kingdom of Saudi Arabia before signing or taking action.

---

## 1. الديباجة / Preamble

نظام العمل السعودي (م/51 لعام 1426هـ) يحتوي على أحكام آمرة لا يجوز الاتفاق على مخالفتها — أي بند تعاقدي يخالفها يقع باطلاً ويُطبَّق النظام بدلاً منه. هذا الملف يُوثِّق الأنماط الاكثر تكراراً في عقود العمل التي تنطوي على مخاطر نظامية، مع مثال للصياغة الإشكالية وتوصية عملية لكل نمط.

Saudi Labor Law (Royal Decree M/51 1426H) contains mandatory provisions that cannot be contracted around — any contractual clause that conflicts with them is void and the statutory rule applies instead. This file documents the most recurring patterns in employment contracts that carry regulatory risk, with a problematic clause example and practical recommendation for each pattern.

**اساس تصنيف الخطر:** وفق `datasets/risk-taxonomy.md` — critical / high / medium / low

---

## 2. أنماط المخاطر: عقود محددة المدة
## Section 2: Fixed-Term Contract Risk Patterns

---

### النمط 1 — غياب تحديد مدة العقد بوضوح
### Pattern 1 — Missing Clear Contract Duration

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | high |
| **التصعيد** | لا — ما لم تكن للعقد قيمة كبيرة |
| **المادة النظامية** | المواد 51-65 من نظام العمل [يحتاج تحقق من رقم المادة المحدد] |

**الوصف:**
عقد العمل الذي لا يُحدد صراحةً ما إذا كان محدد المدة أم غير محدد يُعامَل قضائياً على انه عقد غير محدد المدة في الغالب — مع ما يترتب على ذلك من حقوق الإشعار المسبق والتعويض عن الإنهاء.

A contract that does not clearly specify whether it is fixed-term or open-term is typically treated by courts as open-term — with the attendant notice and wrongful dismissal rights.

**البند الإشكالي النموذجي:**
> "يُعيَّن الموظف لأداء مهام المنصب المذكور أعلاه ويبدأ عمله اعتباراً من تاريخ التوقيع."

**المخاطرة القانونية:**
صاحب العمل يعتقد ان العقد محدد المدة لمشروع بعينه، لكن المحكمة العمالية قد تعتبره مفتوح المدة وتُلزم بدفع مكافأة نهاية الخدمة الكاملة وبدل إشعار عند الإنهاء.

The employer believes the contract is fixed-term for a specific project; the Labor Court may treat it as open-term and require full EOSB and notice pay upon termination.

**التوصية:**
يجب أن يتضمن العقد صراحةً: (أ) "عقد محدد المدة" مع تاريخ انتهاء، أو (ب) "عقد غير محدد المدة" مع شروط الإنهاء. صياغة الغرض التشغيلي وحده لا يُحدد النوع.

---

### النمط 2 — تجديد العقد المحدد المدة أكثر من مرتين
### Pattern 2 — Fixed-Term Contract Renewed More Than Twice

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | critical |
| **التصعيد** | نعم — تحول تلقائي للعقد غير محدد المدة |
| **المادة النظامية** | المادة 55 من نظام العمل |

**الوصف:**
العقد المحدد المدة الذي يُجدَّد أكثر من مرتين، أو الذي يتجاوز مجموع مدده أربع سنوات، يُعدّ عقداً غير محدد المدة تلقائياً بقوة النظام.

A fixed-term contract renewed more than twice, or whose aggregate duration exceeds four years, becomes an open-term contract automatically by operation of law.

**البند الإشكالي النموذجي:**
> "يُمدَّد هذا العقد لسنة إضافية بقبول ضمني ما لم يُخطر أحد الطرفين الآخر بالرغبة في إنهائه قبل 30 يوماً."

**المخاطرة القانونية:**
بعد التجديد الثالث يصبح العقد مفتوح المدة — الإنهاء اللاحق يُوجب بدل إشعار (60 يوماً) ومكافأة نهاية الخدمة الكاملة، وقد يُعدّ فصلاً تعسفياً.

After the third renewal the contract becomes open-term — subsequent termination requires 60-day notice pay and full EOSB, and may be treated as wrongful dismissal.

**التوصية:**
تتبع عدد مرات التجديد في سجل الموارد البشرية. عند الاقتراب من الحد يجب اتخاذ قرار واعٍ: إما التحول الرسمي لعقد مفتوح، أو الإنهاء قبل التجديد الثالث مع توثيق السبب.

---

### النمط 3 — فترة التجربة تتجاوز 90 يوماً أو تتكرر
### Pattern 3 — Probation Period Exceeding 90 Days or Repeated

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | high |
| **التصعيد** | لا |
| **المادة النظامية** | المواد 51-65 من نظام العمل [يحتاج تحقق من رقم المادة المحدد لفترة التجربة] |

**الوصف:**
فترة التجربة لا تتجاوز 90 يوماً، وتُمدَّد باتفاق كتابي حتى 180 يوماً كحد أقصى. لا يجوز تكرارها مع نفس العامل على العمل ذاته.

Probation cannot exceed 90 days, and may be extended by written agreement to a maximum of 180 days. It cannot be repeated for the same worker in the same role.

**البند الإشكالي النموذجي:**
> "تمتد فترة التجربة ستة أشهر قابلة للتمديد ثلاثة أشهر إضافية بقرار الإدارة."

**المخاطرة القانونية:**
البند يُحاول فرض فترة تجربة تتجاوز 180 يوماً — هذا الجزء الزائد باطل. إذا أنهى صاحب العمل العقد خلال المدة الممتدة بحجة "فترة التجربة" قد لا تعتبر المحكمة الإنهاء قانونياً.

The clause attempts a probation exceeding 180 days — the excess is void. If the employer terminates during the extended period citing "probation," the court may not recognise the termination as lawful.

**التوصية:**
تحديد فترة التجربة بـ 90 يوماً صراحةً. إذا لزم التمديد، يُوثَّق بملحق كتابي موقع ولا يتجاوز إجمالي المدتين 180 يوماً.

---

### النمط 4 — غياب بند الوصف الوظيفي
### Pattern 4 — Missing Job Description Clause

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | medium |
| **التصعيد** | لا |
| **المادة النظامية** | المواد 51-65 من نظام العمل — البيانات الإلزامية في العقد [يحتاج تحقق] |

**الوصف:**
نظام العمل يُوجب تحديد طبيعة العمل في العقد. غياب الوصف الوظيفي يُعرِّض صاحب العمل لصعوبة في إثبات مخالفة العامل لمهامه، ويُعرِّض العامل لتكليفات خارج نطاق اتفاقه.

The Labor Law requires specifying the nature of work in the contract. A missing job description makes it harder for the employer to prove job-duty violations and exposes the employee to assignments outside their agreed scope.

**البند الإشكالي النموذجي:**
> "يقوم الموظف بأداء المهام التي تُكلَّف بها من قِبَل الإدارة."

**المخاطرة القانونية:**
في نزاعات الفصل المرتبطة بالأداء أو بإساءة استخدام السلطة، غياب الوصف الوظيفي يُضعف حجة صاحب العمل ويُقوِّي ادعاء العامل بالتعديل الأحادي لمهامه.

In disputes involving performance-based termination or abuse of authority, missing job description weakens the employer's position and strengthens the employee's claim of unilateral duty modification.

**التوصية:**
إضافة ملحق بالوصف الوظيفي مُوقَّع من الطرفين، مع الإشارة الى إمكانية مراجعته بالاتفاق. يجب أن يُحدد المسمى الوظيفي والمهام الجوهرية والخط الإداري.

---

### النمط 5 — الراتب الأساسي والمكونات الإلزامية
### Pattern 5 — Basic Salary and Mandatory Components

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | high |
| **التصعيد** | نعم — إذا كانت الفجوة كبيرة أو الأثر على EOSB جوهرياً |
| **المادة النظامية** | المواد 88-108 من نظام العمل — باب الأجور [يحتاج تحقق من رقم المادة المحدد] |

**الوصف:**
العقود التي تُضمِّن الراتب بدلات متنوعة دون تحديد "الأجر الأساسي" بوضوح تُعرِّض صاحب العمل لنزاع في احتساب مكافأة نهاية الخدمة — فالاجتهاد القضائي السائد يحتسبها على الأجر الأساسي.

Contracts bundling the salary into multiple allowances without clearly defining the "base salary" expose the employer to disputes over EOSB calculation — prevailing judicial practice computes it on base salary.

**البند الإشكالي النموذجي:**
> "يتقاضى الموظف إجمالي 12,000 ريال شاملاً جميع البدلات والمزايا."

**المخاطرة القانونية:**
العامل يطالب عند الإنهاء باحتساب EOSB على الإجمالي (12,000). صاحب العمل يدّعي أن الأساسي 5,000 فقط. غياب التفصيل يُضعف حجة صاحب العمل في المحكمة العمالية.

Upon termination the employee claims EOSB on the total (12,000). The employer claims base is only 5,000. Absence of breakdown weakens the employer's position before the Labor Court.

**التوصية:**
يجب تفصيل مكونات الراتب: الأجر الأساسي + بدل السكن + بدل النقل + أي بدلات أخرى — كل منها برقم مستقل. هذا يحمي كلا الطرفين ويُقلل من النزاع.

---

## 3. أنماط المخاطر: إنهاء العقد
## Section 3: Contract Termination Risk Patterns

---

### النمط 6 — إنهاء العقد بدون إشعار مسبق
### Pattern 6 — Termination Without Prior Notice

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | critical |
| **التصعيد** | نعم |
| **المادة النظامية** | المادة 75 من نظام العمل [يحتاج تحقق من رقم المادة المحدد] / المواد 74-87 |

**الوصف:**
إنهاء عقد غير محدد المدة لعامل يتقاضى أجراً شهرياً يستلزم إشعاراً مسبقاً مكتوباً لا يقل عن 60 يوماً. الإنهاء الفوري دون إشعار — حتى لو كان بعذر مشروع — يُوجب دفع بدل الإشعار.

Terminating an open-term contract for a monthly-paid worker requires at least 60 days' written advance notice. Immediate termination without notice — even for valid cause — triggers a notice-pay obligation.

**البند الإشكالي النموذجي:**
> "يحق لصاحب العمل إنهاء هذا العقد في أي وقت بإشعار مدته 7 أيام."

**المخاطرة القانونية:**
البند يُحدد إشعاراً أقل من الحد الأدنى النظامي — لا يُلزم العامل ولا المحكمة العمالية. الإنهاء بناءً عليه يُوجب بدل الفترة المتبقية من الإشعار الواجب (60 يوماً) ويُعرِّض للدعوى العمالية.

The clause sets a notice period below the statutory minimum — it does not bind the employee or the Labor Court. Termination based on it triggers pay for the remaining notice period (60 days) and exposes the employer to a labor claim.

**التوصية:**
تحديد مدة الإشعار بـ 60 يوماً على الأقل للعمال بأجر شهري. يجوز الاتفاق على مدة أطول — لا يجوز الاتفاق على مدة أقصر.

---

### النمط 7 — صياغة مبررات الفصل بشكل مبهم
### Pattern 7 — Vague Termination Justification Language

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | high |
| **التصعيد** | لا |
| **المادة النظامية** | المادة 80 من نظام العمل |

**الوصف:**
المادة 80 تُحدد 12 حالة يجوز فيها إنهاء العقد دون مكافأة أو تعويض. صياغة مبررات الفصل بشكل عام ("عدم الكفاءة"، "لاعتبارات تنظيمية") دون ربطها بالحالات المحددة تُضعف الموقف القانوني لصاحب العمل.

Article 80 specifies 12 situations where termination without gratuity or compensation is permitted. Framing termination justifications generally ("inefficiency," "organisational considerations") without linking them to the specified cases weakens the employer's legal position.

**البند الإشكالي النموذجي:**
> "يُنهى عقد الموظف في حالة عدم الوفاء بمعايير الأداء أو لأسباب تنظيمية تقديرية."

**المخاطرة القانونية:**
المحكمة العمالية قد تعتبر هذا الفصل تعسفياً ما لم يُثبت صاحب العمل انطباق إحدى حالات المادة 80 بأدلة موثقة. الفصل التعسفي يُوجب تعويضاً لا يقل عن 15 يوماً عن كل سنة خدمة.

The Labor Court may treat this as wrongful dismissal unless the employer proves one of Article 80's cases applies with documented evidence. Wrongful dismissal triggers compensation of at least 15 days' pay per year of service.

**التوصية:**
توثيق مسار التأديب كاملاً (إنذارات مكتوبة، جلسات استماع، مدد منح الفرصة للتحسين) قبل الفصل. ربط قرار الإنهاء بصياغة تتطابق مع إحدى حالات المادة 80.

---

### النمط 8 — غياب إجراءات التأديب قبل الفصل
### Pattern 8 — Missing Disciplinary Procedure Before Termination

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | high |
| **التصعيد** | نعم — في حالات الفصل الجماعي أو الكبير |
| **المادة النظامية** | المادة 80 من نظام العمل |

**الوصف:**
نظام العمل ينطوي على مبدأ ضمني بمنح العامل فرصة للإيضاح والتحسين قبل الفصل في معظم حالات المادة 80. غياب إجراءات التأديب يُعرِّض صاحب العمل لادعاء الفصل التعسفي حتى لو كان السبب مشروعاً من حيث المضمون.

The Labor Law contains an implied principle of allowing the employee an opportunity for clarification and improvement before termination in most Article 80 cases. Missing disciplinary procedures exposes the employer to a wrongful dismissal claim even if the substantive ground is valid.

**البند الإشكالي النموذجي:**
> (لا يتضمن العقد أو اللوائح الداخلية أي نص على إجراءات التأديب قبل الفصل)

**المخاطرة القانونية:**
الفصل المباشر — حتى لسبب موضوعي مشروع — دون سابقة إنذار مكتوب أو جلسة استماع يُعرِّض صاحب العمل لدعوى تعسف تعتمد على غياب الإجراء لا على الموضوع.

Direct termination — even for substantively valid grounds — without prior written warning or hearing exposes the employer to a wrongful dismissal claim based on procedural absence rather than substantive grounds.

**التوصية:**
إدراج نظام تأديبي في لوائح العمل الداخلية: إنذار شفوي، إنذار مكتوب أول، إنذار مكتوب ثانٍ، ثم إنهاء — مع منح مدة معقولة للتحسين بين كل مرحلة. توثيق كل خطوة في ملف الموظف.

---

### النمط 9 — عدم صرف مكافأة نهاية الخدمة وفق النظام
### Pattern 9 — EOSB Not Calculated or Paid as Required

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | critical |
| **التصعيد** | نعم |
| **المادة النظامية** | المادة 84 من نظام العمل |

**الوصف:**
مكافأة نهاية الخدمة حق نظامي آمر لا يُسقط بالاتفاق. تُحتسب على الأجر الأساسي: نصف شهر عن كل سنة من السنوات الخمس الأولى، وشهر كامل عن كل سنة بعد ذلك.

EOSB is a mandatory statutory right that cannot be waived by agreement. It is calculated on base salary: half a month per year for the first five years, and a full month per year thereafter.

**البند الإشكالي النموذجي:**
> "تُحتسب مكافأة نهاية الخدمة على إجمالي مدة العقد المحدد فقط ولا تسري في حالة الاستقالة."

**المخاطرة القانونية:**
إسقاط حق EOSB في حالة الاستقالة باطل إذا تجاوزت مدة الخدمة سنتين. كما أن احتساب EOSB على غير الأجر الأساسي مخالف للنظام. الدعوى العمالية بالمطالبة بالفروقات شائعة جداً.

Waiving EOSB on resignation is void if service exceeds two years. Computing EOSB on total compensation rather than base salary violates the law. Labor claims for the difference are extremely common.

**التوصية:**
احتساب EOSB وفق المادة 84 بدقة. تفصيل الأجر الأساسي عن البدلات في العقد. توثيق احتساب EOSB عند كل إنهاء في كشف تفصيلي موقَّع.

---

### النمط 10 — اشتراطات تُسقط حقوق العامل النظامية
### Pattern 10 — Clauses That Waive Statutory Worker Rights

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | critical |
| **التصعيد** | نعم |
| **المادة النظامية** | المبدأ العام لنظام العمل م/51 — الأحكام الآمرة غير قابلة للتنازل |

**الوصف:**
أي بند يُوجب على العامل التنازل عن حق نظامي آمر — الإجازة السنوية، EOSB، أجر الإضافي، حماية الأجر — باطل بطلاناً مطلقاً بقوة النظام حتى لو وقَّع العامل بإرادته.

Any clause obliging the employee to waive a mandatory statutory right — annual leave, EOSB, overtime pay, wage protection — is absolutely void by operation of law even if the employee signed voluntarily.

**البند الإشكالي النموذجي:**
> "يوافق الموظف على التنازل عن أي مطالبة مستقبلية تتعلق بمكافأة نهاية الخدمة أو الإجازات غير المستخدمة مقابل الراتب المتفق عليه."

**المخاطرة القانونية:**
البند باطل كلياً. العامل يستطيع المطالبة بجميع الحقوق النظامية أمام المحكمة العمالية متجاهلاً هذا البند. وقوع الاستقطاعات بموجبه يُنشئ مطالبة بالاسترداد.

The clause is wholly void. The worker may claim all statutory rights before the Labor Court ignoring this clause entirely. Any deductions made under it create a recovery claim.

**التوصية:**
مراجعة جميع بنود التنازل أو الإسقاط في العقد وحذفها. لا يجوز بأي وسيلة تعاقدية التقليل من الحقوق النظامية الآمرة — يجوز فقط الزيادة عليها.

---

## 4. أنماط المخاطر: بنود ما بعد الخدمة
## Section 4: Post-Service Clause Risk Patterns

---

### النمط 11 — بند عدم المنافسة: شروط الصحة والبطلان
### Pattern 11 — Non-Compete Clause: Validity Conditions and Voidness

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | high |
| **التصعيد** | نعم — تستلزم تقييماً متخصصاً |
| **المادة النظامية** | المادة 83 من نظام العمل [يحتاج تحقق من رقم المادة المحدد] |

**الوصف:**
بند عدم المنافسة في عقود العمل السعودية مقيَّد بضوابط صارمة: يجب أن يكون محدداً زمنياً وجغرافياً ومهنياً، وأن يكون ضرورياً لحماية مصلحة مشروعة، وألا يُلقي على العامل عبئاً يتجاوز ما هو ضروري.

Non-compete clauses in Saudi employment contracts are subject to strict conditions: they must be limited in time, geography, and professional scope; necessary to protect a legitimate interest; and must not impose a burden exceeding what is necessary.

**البند الإشكالي النموذجي:**
> "يلتزم الموظف بعدم العمل في أي نشاط مشابه في أي مكان لمدة خمس سنوات بعد إنهاء العقد."

**المخاطرة القانونية:**
البند على هذه الصياغة مرشح للبطلان: مدة 5 سنوات وغياب التحديد الجغرافي والمهني يجعله مبالغاً في تقييد العامل. المحكمة العمالية قد تُبطله كلياً أو تُعدِّله.

This clause is prone to voidness: 5-year duration and lack of geographic and professional specificity make it excessively restrictive. The Labor Court may void it entirely or modify it.

**التوصية:**
يُحدَّد بند عدم المنافسة بـ: (1) مدة معقولة لا تتجاوز سنة أو سنتين في الغالب، (2) نطاق جغرافي محدد، (3) مجال مهني محدد يرتبط فعلاً بالعمل المُؤدَّى، (4) مقابل مادي إن أمكن.

---

### النمط 12 — بند السرية: ما يجوز وما لا يجوز
### Pattern 12 — Confidentiality Clause: Permissible and Impermissible Scope

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | medium |
| **التصعيد** | لا |
| **المادة النظامية** | لا توجد مادة محددة في نظام العمل — يُحكمه المبادئ العامة + PDPL |

**الوصف:**
بند السرية المشروع يحمي المعلومات التجارية الحقيقية للمنشأة. البند المفرط الذي يمتد ليشمل ما اكتسبه العامل من مهارات ومعرفة عامة يتجاوز نطاقه المشروع ويُعرِّض صاحب العمل للطعن فيه.

A lawful confidentiality clause protects genuine business information. A clause extending to skills and general knowledge the employee acquired exceeds its legitimate scope and exposes the employer to challenge.

**البند الإشكالي النموذجي:**
> "يلتزم الموظف بعدم الإفصاح عن أي معلومات اطلع عليها خلال فترة عمله بما في ذلك أساليب العمل والتقنيات المهنية المكتسبة."

**المخاطرة القانونية:**
تضمين "الأساليب المهنية والمهارات المكتسبة" في بند السرية يُقيِّد حق العامل في استخدام خبرته في عمل مستقبلي — وهذا تقييد يتجاوز حماية المعلومات الى تقييد حرية العمل.

Including "professional methods and acquired skills" in the confidentiality clause restricts the employee's right to use their expertise in future employment — extending beyond information protection into restriction of work freedom.

**التوصية:**
تحديد المعلومات المشمولة بالسرية بشكل محدد: قوائم العملاء، البيانات المالية السرية، الأسرار التجارية، المعلومات التقنية الخاصة. استثناء صريح للمهارات والمعرفة العامة المكتسبة.

---

### النمط 13 — اشتراطات متعلقة بحرية العمل (العمالة الوافدة)
### Pattern 13 — Work Freedom Restrictions (Expatriate Workers)

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | critical |
| **التصعيد** | نعم |
| **المادة النظامية** | تعديلات نظام العمل المتعلقة بنظام حماية الأجور + تعميمات وزارة الموارد البشرية |

**الوصف:**
منذ إصلاحات سوق العمل السعودي 2021م أصبح بمقدور كثير من العمال الوافدين التنقل بين أصحاب العمل أو مغادرة البلاد دون الحاجة لموافقة صاحب العمل في حالات محددة. البنود التعاقدية التي تشترط إذن صاحب العمل في كل حالة قد تكون مخالفة للإصلاحات الجديدة.

Since the 2021 Saudi labor market reforms, many expatriate workers can transfer between employers or exit the country without employer consent in specified circumstances. Contractual clauses conditioning every such move on employer approval may conflict with the new reforms.

**البند الإشكالي النموذجي:**
> "لا يحق للموظف مغادرة المملكة أو الانتقال لصاحب عمل آخر إلا بموافقة كتابية مسبقة من الشركة تحت أي ظرف."

**المخاطرة القانونية:**
البند قد يُعدّ مخالفاً لإصلاحات سوق العمل — يُعرِّض صاحب العمل للمسؤولية ويُسهم في نزاعات تشغيلية إذا أفضى تطبيقه الى تقييد حقوق نظامية. كما يُلقي بظلال الممارسة غير المشروعة على المنشأة.

The clause may conflict with labor market reforms — exposing the employer to liability and operational disputes if its enforcement restricts statutory rights. It also creates reputational and compliance risk for the organisation.

**التوصية:**
مراجعة البنود المتعلقة بنقل الكفالة وإذن المغادرة في ضوء إصلاحات 2021م والتعميمات الوزارية الحديثة. الاستعانة بمستشار قانوني متخصص في نظام سوق العمل المُحدَّث.

---

## 5. أنماط المخاطر: العمالة الوافدة
## Section 5: Expatriate Worker Risk Patterns

---

### النمط 14 — تغيير مسمى الوظيفة عن تأشيرة الإقامة
### Pattern 14 — Job Title Differs from Residence Permit Visa

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | critical |
| **التصعيد** | نعم |
| **المادة النظامية** | أنظمة الإقامة ووزارة الداخلية — يُجاوز نطاق نظام العمل وحده |

**الوصف:**
تكليف العامل الوافد بمهام تختلف جوهرياً عن مسمى وظيفته في تأشيرة الإقامة يُعدّ مخالفة لأنظمة الإقامة ومخالفة لاشتراطات السعودة — ويُعرِّض صاحب العمل لغرامات ويُعرِّض العامل لمشكلات إقامة.

Assigning an expatriate worker tasks materially different from their residence permit job title constitutes a violation of residency regulations and Saudization requirements — exposing the employer to fines and the worker to residency complications.

**البند الإشكالي النموذجي:**
> "يشغل الموظف منصب 'مستشار' ويُكلَّف بأداء مهام المبيعات والتشغيل اليومي حسب احتياجات الشركة."

**المخاطرة القانونية:**
مخالفة أنظمة الإقامة + مخالفة اشتراطات نطاقات (Nitaqat) + تعرض المنشأة لمراجعة وزارية. في الحالات الجسيمة تُلغى تصاريح الاستقدام وتُشدَّد الرقابة على المنشأة.

Violation of residency regulations + Nitaqat requirements + exposure to ministerial audit. In serious cases, recruitment permits are cancelled and the organisation faces heightened regulatory scrutiny.

**التوصية:**
التطابق الدقيق بين المسمى الوظيفي في العقد والمسمى في تصريح الإقامة والتأشيرة. أي تغيير في المهام يستلزم تحديث إجراءات الإقامة أولاً.

---

### النمط 15 — الاستقطاع مقابل تكاليف الاستقدام (محظور)
### Pattern 15 — Deductions for Recruitment Costs (Prohibited)

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | critical |
| **التصعيد** | نعم |
| **المادة النظامية** | محظور بموجب أنظمة العمل والتعميمات الوزارية — أحكام مكافحة العمل القسري [يحتاج تحقق] |

**الوصف:**
استقطاع أي مبالغ من راتب العامل الوافد مقابل تكاليف استقدامه (رسوم التأشيرة، تذاكر السفر، رسوم الوسيط) محظور نظاماً. تكاليف الاستقدام تقع على عاتق صاحب العمل حصراً.

Deducting any amounts from an expatriate worker's salary for recruitment costs (visa fees, travel tickets, agent fees) is prohibited by law. Recruitment costs fall exclusively on the employer.

**البند الإشكالي النموذجي:**
> "يُستقطع من راتب الموظف 500 ريال شهرياً لمدة 12 شهراً مقابل تكاليف الاستقدام والتأشيرة."

**المخاطرة القانونية:**
مخالفة صريحة للأنظمة. يُعرِّض المنشأة لغرامات مالية ولإدراجها في قوائم المخالفين. يُمثِّل ممارسة تمسّ بسمعة المنشأة دولياً في إطار معايير مكافحة العمل القسري.

Explicit regulatory violation. Exposes the organisation to fines and inclusion in violators lists. Represents a practice that damages the organisation's reputation internationally under forced labour prevention standards.

**التوصية:**
حذف أي بند يتضمن استقطاعاً مقابل الاستقدام. جميع تكاليف الاستقدام والتأشيرة والسفر تتحملها المنشأة. التأكد من عدم تضمين هذا البند في أي اتفاق جانبي أو ملحق.

---

### النمط 16 — غياب بدلات السكن أو النقل عند الاشتراط
### Pattern 16 — Missing Housing or Transport Allowances When Contractually Required

| الحقل | القيمة |
|-------|-------|
| **مستوى الخطر** | medium |
| **التصعيد** | لا |
| **المادة النظامية** | المواد 88-108 من نظام العمل + تعميمات وزارة الموارد البشرية [يحتاج تحقق من النص المحدد] |

**الوصف:**
إذا نصَّ العقد على بدل سكن أو نقل، أو كانت لوائح المنشأة توجبهما، فإن عدم صرفهما أو تضمينهما في الراتب دون تفصيل يُنشئ التزاماً مدنياً قابلاً للمطالبة.

If the contract specifies housing or transport allowances, or the employer's internal regulations mandate them, failure to pay or itemise them in the salary creates an enforceable civil obligation.

**البند الإشكالي النموذجي:**
> "يتضمن الراتب الإجمالي جميع بدلات السكن والنقل والانتقال دون تحديد."

**المخاطرة القانونية:**
العامل يطالب عند الإنهاء بإثبات أن البدلات مُدرجة فعلاً ومحتسبة في EOSB. غياب التفصيل يُنشئ نزاعاً حول الأساس الفعلي للراتب وتركيبته.

Upon termination the employee may demand proof that allowances were included and factored into EOSB. Lack of itemisation creates a dispute over the actual salary base and its composition.

**التوصية:**
تفصيل بدل السكن وبدل النقل كل منهما برقم مستقل في العقد. إذا كانا مُدرجَين في الراتب الأساسي يجب توثيق ذلك صراحةً مع الأرقام.

---

## 6. جدول ملخص المخاطر
## Section 6: Risk Summary Table

| رقم | النمط | مستوى الخطر | المادة النظامية | الجهة المختصة |
|-----|-------|------------|----------------|--------------|
| 1 | غياب تحديد مدة العقد | 🟡 high | م/51 مواد 51-65 | المحكمة العمالية |
| 2 | تجديد العقد أكثر من مرتين | 🔴 critical | المادة 55 | المحكمة العمالية |
| 3 | فترة تجربة تتجاوز 90 يوماً أو تتكرر | 🟡 high | م/51 مواد 51-65 | المحكمة العمالية |
| 4 | غياب الوصف الوظيفي | 🟢 medium | م/51 مواد 51-65 | المحكمة العمالية |
| 5 | غموض الراتب الأساسي | 🟡 high | م/51 مواد 88-108 | المحكمة العمالية |
| 6 | إنهاء بلا إشعار مسبق | 🔴 critical | المادة 75 [يحتاج تحقق] | المحكمة العمالية |
| 7 | مبررات فصل مبهمة | 🟡 high | المادة 80 | المحكمة العمالية |
| 8 | غياب إجراءات التأديب | 🟡 high | المادة 80 | المحكمة العمالية |
| 9 | إشكاليات EOSB | 🔴 critical | المادة 84 | المحكمة العمالية |
| 10 | بنود تُسقط حقوقاً نظامية | 🔴 critical | المبادئ الآمرة في م/51 | المحكمة العمالية |
| 11 | بند عدم المنافسة مفرط | 🟡 high | المادة 83 [يحتاج تحقق] | المحكمة العمالية |
| 12 | بند سرية مفرط النطاق | 🟢 medium | مبادئ عامة + PDPL | المحكمة العمالية |
| 13 | تقييد حرية العمل (وافدون) | 🔴 critical | إصلاحات سوق العمل 2021م | المحكمة العمالية + وزارة الداخلية |
| 14 | تغيير مسمى الوظيفة عن التأشيرة | 🔴 critical | أنظمة الإقامة | وزارة الداخلية + وزارة الموارد البشرية |
| 15 | استقطاع تكاليف الاستقدام | 🔴 critical | تعميمات وزارية | وزارة الموارد البشرية + غرامات |
| 16 | غياب بدلات السكن/النقل | 🟢 medium | م/51 مواد 88-108 | المحكمة العمالية |

**تلخيص:** 7 أنماط بمستوى critical — 6 أنماط بمستوى high — 3 أنماط بمستوى medium

---

## 7. الربط بالقرارات القضائية
## Section 7: Link to Judicial Decisions

### العلاقة بملف datasets/judicial-decisions/labor/

كل نمط من الأنماط الـ 16 الموثقة يمكن أن يتوفر له سند قضائي من المحاكم العمالية السعودية. مجلد `datasets/judicial-decisions/labor/` مُعدٌّ لاستقبال هذه الأحكام بمجرد توفرها من البوابة القانونية لوزارة العدل.

Each of the 16 documented patterns can have judicial support from Saudi Labor Courts. The `datasets/judicial-decisions/labor/` directory is ready to receive such decisions as they become available from the MOJ Legal Portal.

### دعوة المجتمع للمساهمة / Community Contribution Invitation

إذا وجدت حكماً قضائياً عمالياً صادراً عن المحاكم السعودية يتعلق بأحد الأنماط أعلاه:

1. افتح Issue بعنوان: `"حكم قضائي عمالي: [رقم النمط] — [موضوع الحكم]"`
2. أضف رابط الحكم من `laws.moj.gov.sa`
3. اذكر رقم النمط المرتبط ورقم القضية والمبدأ القانوني

If you find a Saudi Labor Court decision relating to any of the above patterns:

1. Open an Issue titled: `"حكم قضائي عمالي: [Pattern Number] — [decision topic]"`
2. Add the decision link from `laws.moj.gov.sa`
3. Specify the related pattern number, case number, and legal principle

### صيغة الإضافة المقترحة / Suggested Addition Format

```markdown
## [رقم القضية] — [المحكمة] — [تاريخ الحكم هجري/ميلادي]

**النمط المرتبط:** النمط [رقم] — [اسم النمط]
**المبدأ القانوني:** [وصف المبدأ الذي رسّخه الحكم]
**المصدر:** laws.moj.gov.sa — [رابط الحكم]
**حالة التحقق:** draft
```

---

## 8. المصادر الرسمية
## Section 8: Official Sources

- **نظام العمل السعودي (النص الرسمي):** [boe.gov.sa](https://boe.gov.sa)
- **وزارة الموارد البشرية والتنمية الاجتماعية:** [hrsd.gov.sa](https://www.hrsd.gov.sa)
- **البوابة القانونية — وزارة العدل (الأحكام القضائية):** [laws.moj.gov.sa](https://laws.moj.gov.sa/ar)
- **منصة قوى:** [qiwa.com.sa](https://www.qiwa.com.sa)
- **الجريدة الرسمية (أم القرى):** [uqn.gov.sa](https://uqn.gov.sa)

---

## ملاحظات التحقق / Verification Notes

| المسألة | الحالة |
|---------|--------|
| أرقام المواد المحددة لأحكام العقد (51-65) | to_verify — مستمدة من ملخص تعليمي |
| رقم مادة الإشعار المسبق (المادة 75) | to_verify — يحتاج تأكيد من النص الرسمي |
| رقم مادة عدم المنافسة (المادة 83) | to_verify — يحتاج تأكيد من النص الرسمي |
| حظر استقطاع الاستقدام — الأساس التشريعي المحدد | to_verify — التعميمات الوزارية تحتاج تحديد الرقم والتاريخ |
| تفاصيل إصلاحات سوق العمل 2021م | to_verify — يحتاج مراجعة قرارات الإصلاح من hrsd.gov.sa |

<!-- TODO: يحتاج تحقق — أرقام المواد المحددة من النص الرسمي لنظام العمل م/51 لعام 1426هـ عبر boe.gov.sa -->
<!-- TODO: يحتاج تحقق — إحالة كل نمط بحكم قضائي من laws.moj.gov.sa عند توفره -->
