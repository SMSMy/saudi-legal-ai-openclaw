# GitHub Pages — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a production-ready Arabic-first static website in `docs/` served via GitHub Pages, consisting of `index.html`, `styles.css`, `search.js`, and `.nojekyll`.

**Architecture:** Four files only. All CSS in one shared stylesheet. All search logic in one JS file with a hardcoded in-memory index. No build step, no framework, no dependencies beyond the Google Fonts CDN. Relative paths throughout so the site works locally and on GitHub Pages. No `innerHTML` with dynamic content — all DOM manipulation uses safe `textContent` and `createElement`.

**Tech Stack:** HTML5, CSS custom properties, Vanilla JS (ES6). Tajawal font via Google Fonts. RTL layout via `<html dir="rtl">`.

**Spec:** `docs/superpowers/specs/2026-05-27-github-pages-website-design.md`

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `docs/.nojekyll` | Disables Jekyll processing on GitHub Pages |
| Create | `docs/styles.css` | Shared RTL stylesheet, all CSS variables, all components |
| Create | `docs/index.html` | Homepage: topbar, hero, search, 4 nav cards, disclaimer, footer |
| Create | `docs/search.js` | Hardcoded search index + safe DOM dropdown logic |
| Modify | `README.md` | Add GitHub Pages URL under new "Website" section |

**Not created in this plan:** `sources.html`, `skills.html`, `templates.html`, `assets/` — Phase 2.

---

## Task 1: Scaffold — `.nojekyll` and `.gitignore` check

**Files:**
- Create: `docs/.nojekyll`
- Verify: `.gitignore` already contains `.superpowers/`

- [ ] **Step 1: Create `.nojekyll`**

Create an empty file. No content needed — its presence is the signal to GitHub Pages.

```bash
touch docs/.nojekyll
```

- [ ] **Step 2: Verify `.gitignore` has `.superpowers/`**

```bash
grep ".superpowers" .gitignore
```

Expected output: `.superpowers/`

If missing, add it manually to `.gitignore`.

- [ ] **Step 3: Commit**

```bash
git add docs/.nojekyll
git commit -m "chore: add docs/.nojekyll to disable Jekyll on GitHub Pages"
```

---

## Task 2: `styles.css` — Full shared stylesheet

**Files:**
- Create: `docs/styles.css`

- [ ] **Step 1: Create `docs/styles.css`**

```css
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap');

/* ── CSS Custom Properties ──────────────────────────────── */
:root {
  --navy:          #1a2e3b;
  --navy-mid:      #2c4a5a;
  --cream:         #f7f5f0;
  --cream-dark:    #eceae3;
  --border:        #dddad3;
  --border-light:  #ebe9e2;
  --text:          #1a1a1a;
  --text-mid:      #3a3a3a;
  --text-muted:    #7a7a78;
  --teal:          #2e8b7a;
  --amber:         #b5651d;
  --amber-bg:      #fdf6ec;
  --amber-border:  #ddb88a;
  --white:         #ffffff;
  --max-width:     780px;
  --page-padding:  40px;
}

/* ── Reset + RTL defaults ───────────────────────────────── */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  font-family: 'Tajawal', 'Segoe UI', Tahoma, Arial, sans-serif;
  background: var(--cream);
  color: var(--text);
  font-size: 16px;
  line-height: 1.7;
  text-align: right;
}

a { color: inherit; text-decoration: none; }

/* ── Topbar ─────────────────────────────────────────────── */
.topbar {
  background: var(--navy);
  padding: 0 var(--page-padding);
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  border-bottom: 1px solid rgba(255, 255, 255, .06);
}

.topbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
}

.brand-dot {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: var(--teal);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.brand-name {
  font-size: 14px;
  font-weight: 500;
  color: rgba(255, 255, 255, .92);
  letter-spacing: .01em;
}

.topbar-nav {
  display: flex;
  gap: 6px;
  align-items: center;
}

.topbar-nav a {
  color: rgba(255, 255, 255, .65);
  font-size: 13px;
  padding: 5px 12px;
  border-radius: 5px;
  transition: color .15s, background .15s;
}

.topbar-nav a:hover {
  color: #fff;
  background: rgba(255, 255, 255, .08);
}

/* Active nav state — controlled by data-page on <body> and data-nav on <a> */
body[data-page="home"]      [data-nav="home"],
body[data-page="sources"]   [data-nav="sources"],
body[data-page="skills"]    [data-nav="skills"],
body[data-page="templates"] [data-nav="templates"] {
  color: rgba(255, 255, 255, .92);
}

.nav-cta {
  color: var(--teal) !important;
  border: 1px solid rgba(46, 139, 122, .4);
  font-size: 12px !important;
}

.nav-cta:hover {
  background: rgba(46, 139, 122, .12) !important;
  color: var(--teal) !important;
}

/* ── Hero ───────────────────────────────────────────────── */
.hero {
  padding: 64px var(--page-padding) 52px;
  max-width: var(--max-width);
  margin: 0 auto;
  text-align: center;
}

.hero-eyebrow {
  display: inline-block;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--teal);
  border: 1px solid rgba(46, 139, 122, .3);
  padding: 3px 12px;
  border-radius: 20px;
  margin-bottom: 22px;
  background: rgba(46, 139, 122, .04);
}

.hero-title {
  font-size: 30px;
  font-weight: 700;
  color: var(--navy);
  line-height: 1.35;
  margin-bottom: 14px;
  letter-spacing: -.01em;
}

.hero-subtitle {
  font-size: 15px;
  color: var(--text-muted);
  font-weight: 400;
  max-width: 560px;
  margin: 0 auto 32px;
  line-height: 1.75;
}

/* ── Search ─────────────────────────────────────────────── */
.search-wrap {
  max-width: 520px;
  margin: 0 auto 12px;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 13px 20px 13px 52px;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  background: var(--white);
  font-family: inherit;
  font-size: 14px;
  color: var(--text);
  outline: none;
  transition: border-color .2s, box-shadow .2s;
  direction: rtl;
  text-align: right;
}

.search-input:focus {
  border-color: var(--navy-mid);
  box-shadow: 0 0 0 3px rgba(44, 74, 90, .08);
}

.search-input::placeholder { color: #b0ada6; }

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #9a9890;
  font-size: 16px;
  pointer-events: none;
  line-height: 1;
}

.search-hint {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 7px;
  text-align: center;
  margin-bottom: 36px;
}

/* Search dropdown */
.search-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  right: 0;
  left: 0;
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(26, 46, 59, .10);
  z-index: 100;
  overflow: hidden;
  display: none;
}

.search-dropdown.visible { display: block; }

.search-result {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background .1s;
  border-bottom: 1px solid var(--border-light);
  text-align: right;
}

.search-result:last-child { border-bottom: none; }
.search-result:hover { background: var(--cream); }

.result-type {
  font-size: 9px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 20px;
  letter-spacing: .06em;
  white-space: nowrap;
  flex-shrink: 0;
}

.result-type-skill   { background: #eef7f4; color: var(--teal); }
.result-type-source  { background: #eef3f7; color: var(--navy); }
.result-type-prompt  { background: #fdf6ec; color: var(--amber); }

.result-text { flex: 1; min-width: 0; }

.result-title-ar {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

.result-title-en {
  font-size: 11px;
  color: var(--text-muted);
  font-family: 'Segoe UI', sans-serif;
  direction: ltr;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.search-no-result {
  padding: 14px 16px;
  font-size: 13px;
  color: var(--text-muted);
  text-align: center;
}

.search-no-result a { color: var(--teal); text-decoration: underline; }

/* ── Section divider ────────────────────────────────────── */
.section-divider {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 var(--page-padding);
  border-bottom: 1px solid var(--border-light);
}

/* ── Nav cards ──────────────────────────────────────────── */
.cards-section {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 40px var(--page-padding) 48px;
}

.cards-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.nav-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 22px 22px 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: border-color .2s, box-shadow .2s, transform .15s;
}

.nav-card:hover {
  border-color: var(--navy-mid);
  box-shadow: 0 4px 16px rgba(26, 46, 59, .08);
  transform: translateY(-1px);
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}

.card-icon {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  flex-shrink: 0;
}

.card-arrow {
  font-size: 16px;
  color: var(--border);
  margin-top: 2px;
  transition: color .15s;
  font-family: 'Segoe UI', sans-serif;
}

.nav-card:hover .card-arrow { color: var(--navy-mid); }

.card-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--navy);
  margin-bottom: 3px;
}

.card-title-en {
  font-size: 11px;
  font-weight: 400;
  color: var(--text-muted);
  display: block;
  margin-bottom: 6px;
  font-family: 'Segoe UI', sans-serif;
  direction: ltr;
  text-align: left;
}

.card-desc {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.6;
}

.card-tag {
  display: inline-block;
  margin-top: 6px;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 20px;
  letter-spacing: .04em;
}

/* ── Disclaimer ─────────────────────────────────────────── */
.disclaimer-section {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 var(--page-padding) 56px;
}

.disclaimer-box {
  background: var(--amber-bg);
  border: 1px solid var(--amber-border);
  border-inline-start: 4px solid var(--amber);
  border-radius: 8px;
  padding: 18px 22px;
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.disc-icon {
  font-size: 18px;
  flex-shrink: 0;
  margin-top: 1px;
  line-height: 1;
}

.disc-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--amber);
  margin-bottom: 6px;
}

.disc-body-ar {
  font-size: 12px;
  color: #6b4c2a;
  line-height: 1.7;
  margin-bottom: 6px;
}

.disc-body-en {
  font-size: 12px;
  color: #6b4c2a;
  line-height: 1.7;
  direction: ltr;
  text-align: left;
}

/* ── Footer ─────────────────────────────────────────────── */
.footer {
  background: var(--navy);
  padding: 24px var(--page-padding);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-text {
  font-size: 12px;
  color: rgba(255, 255, 255, .4);
}

.footer-links {
  display: flex;
  gap: 18px;
}

.footer-links a {
  font-size: 12px;
  color: rgba(255, 255, 255, .4);
  transition: color .15s;
}

.footer-links a:hover { color: rgba(255, 255, 255, .7); }

/* ── Mobile ─────────────────────────────────────────────── */
@media (max-width: 768px) {
  .cards-grid { grid-template-columns: 1fr; }
  .hero { padding: 40px var(--page-padding) 36px; }
}

@media (max-width: 600px) {
  :root { --page-padding: 20px; }

  /* Hide all nav links except the GitHub CTA on mobile */
  .topbar-nav a:not(.nav-cta) { display: none; }

  .hero-title    { font-size: 22px; }
  .hero-subtitle { font-size: 14px; }
  .cards-section { padding-top: 28px; }
  .nav-card      { padding: 16px; }
  .card-title    { font-size: 14px; }

  .disclaimer-box { flex-direction: column; gap: 8px; }

  .footer        { flex-direction: column; gap: 12px; text-align: center; }
  .footer-links  { justify-content: center; }
}
```

- [ ] **Step 2: Verify the file exists**

```bash
wc -l docs/styles.css
```

Expected: 280+ lines.

- [ ] **Step 3: Commit**

```bash
git add docs/styles.css
git commit -m "feat: add shared RTL stylesheet for GitHub Pages website"
```

---

## Task 3: `index.html` — Homepage

**Files:**
- Create: `docs/index.html`

- [ ] **Step 1: Create `docs/index.html`**

```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="إطار الذكاء الاصطناعي للبيئة القانونية السعودية — مرجع منظَّم للمصادر القانونية الرسمية ومهارات التحليل القانوني." />
  <title>إطار الذكاء الاصطناعي القانوني السعودي</title>
  <link rel="stylesheet" href="styles.css" />
  <script src="search.js" defer></script>
</head>
<body data-page="home">

  <!-- ── Topbar ── -->
  <header class="topbar">
    <div class="topbar-brand">
      <div class="brand-dot" aria-hidden="true">ق</div>
      <span class="brand-name">إطار الذكاء الاصطناعي القانوني السعودي</span>
    </div>
    <nav class="topbar-nav" aria-label="التنقل الرئيسي">
      <a href="index.html"     data-nav="home">الرئيسية</a>
      <a href="sources.html"   data-nav="sources">المصادر الرسمية</a>
      <a href="skills.html"    data-nav="skills">المهارات القانونية</a>
      <a href="templates.html" data-nav="templates">الصياغة القضائية</a>
      <a href="https://github.com/Samix2026/saudi-legal-ai-framework"
         target="_blank" rel="noopener" class="nav-cta">GitHub ↗</a>
    </nav>
  </header>

  <!-- ── Hero ── -->
  <section class="hero">
    <span class="hero-eyebrow">منصة معرفية مفتوحة المصدر</span>
    <h1 class="hero-title">إطار الذكاء الاصطناعي للبيئة القانونية السعودية</h1>
    <p class="hero-subtitle">
      مرجع منظَّم للمصادر القانونية الرسمية، ومهارات التحليل القانوني بالذكاء الاصطناعي،
      والقوالب القضائية — مُخصَّص للمملكة العربية السعودية.
    </p>

    <!-- Search -->
    <div class="search-wrap" id="search-wrap">
      <input
        class="search-input"
        id="search-input"
        type="search"
        placeholder="ابحث في المصادر والمهارات والقوالب…"
        autocomplete="off"
        aria-label="بحث في المنصة"
        aria-expanded="false"
        aria-controls="search-dropdown"
      />
      <span class="search-icon" aria-hidden="true">🔍</span>
      <div class="search-dropdown" id="search-dropdown" role="listbox"
           aria-label="نتائج البحث"></div>
    </div>
    <p class="search-hint">مثال: نظام العمل · شرط جزائي · محكمة تجارية · عقد إيجار</p>
  </section>

  <div class="section-divider" role="separator"></div>

  <!-- ── Navigation cards ── -->
  <section class="cards-section" aria-label="أقسام المنصة">
    <div class="cards-grid">

      <a class="nav-card" href="sources.html">
        <div class="card-header">
          <div class="card-icon" style="background:#eef3f7;" aria-hidden="true">📚</div>
          <span class="card-arrow" aria-hidden="true">←</span>
        </div>
        <div class="card-body">
          <div class="card-title">المصادر الرسمية</div>
          <span class="card-title-en" dir="ltr">Official Legal Sources</span>
          <p class="card-desc">
            بوابة هيئة الخبراء، أم القرى، ناجز، وزارة العدل، الموارد البشرية،
            ومنصات الأنظمة الرسمية الأخرى.
          </p>
          <span class="card-tag" style="background:#eef3f7; color:#1a2e3b;">8 مصادر رسمية</span>
        </div>
      </a>

      <a class="nav-card" href="skills.html">
        <div class="card-header">
          <div class="card-icon" style="background:#eef7f4;" aria-hidden="true">⚖️</div>
          <span class="card-arrow" aria-hidden="true">←</span>
        </div>
        <div class="card-body">
          <div class="card-title">المهارات القانونية بالذكاء الاصطناعي</div>
          <span class="card-title-en" dir="ltr">Legal AI Skills</span>
          <p class="card-desc">
            مهارات تحليلية موجَّهة: مراجعة العقود، النزاعات التجارية،
            نظام العمل، الامتثال، التحكيم، والتعاملات العقارية.
          </p>
          <span class="card-tag" style="background:#eef7f4; color:#2e8b7a;">7 مهارات</span>
        </div>
      </a>

      <a class="nav-card" href="templates.html">
        <div class="card-header">
          <div class="card-icon" style="background:#f7f3ee;" aria-hidden="true">📝</div>
          <span class="card-arrow" aria-hidden="true">←</span>
        </div>
        <div class="card-body">
          <div class="card-title">القوالب الإرشادية والصياغة القضائية</div>
          <span class="card-title-en" dir="ltr">Prompt Templates</span>
          <p class="card-desc">
            نماذج موجَّهة جاهزة الاستخدام لكلود وجيمني وتشات جي بي تي،
            تغطي مراجعة العقود والمذكرات القانونية.
          </p>
          <span class="card-tag" style="background:#fdf6ec; color:#b5651d;">قريباً</span>
        </div>
      </a>

      <a class="nav-card"
         href="https://github.com/Samix2026/saudi-legal-ai-framework/tree/main/datasets"
         target="_blank" rel="noopener">
        <div class="card-header">
          <div class="card-icon" style="background:#f0eef7;" aria-hidden="true">🗂️</div>
          <span class="card-arrow" aria-hidden="true">↗</span>
        </div>
        <div class="card-body">
          <div class="card-title">مجموعات البيانات القانونية</div>
          <span class="card-title-en" dir="ltr">Legal Datasets</span>
          <p class="card-desc">
            بيانات منظَّمة: مخاطر العقود، الأنظمة المقارنة،
            التحليل القضائي، ومعجم المصطلحات القانونية السعودية.
          </p>
          <span class="card-tag" style="background:#f0eef7; color:#5b4e8a;">GitHub ↗</span>
        </div>
      </a>

    </div>
  </section>

  <!-- ── Disclaimer ── -->
  <section class="disclaimer-section" aria-label="تحذير قانوني">
    <div class="disclaimer-box" role="note">
      <span class="disc-icon" aria-hidden="true">⚠️</span>
      <div>
        <div class="disc-title">تحذير قانوني مهم</div>
        <p class="disc-body-ar">
          هذا تحليل أولي بمساعدة الذكاء الاصطناعي ولا يُعدّ استشارة قانونية.
          يجب مراجعة مختص قانوني مرخّص في المملكة العربية السعودية قبل اتخاذ أي إجراء.
          الأنظمة واللوائح عرضةٌ للتغيير — تحقق دائماً من المصادر الرسمية المعتمدة.
        </p>
        <p class="disc-body-en" dir="ltr">
          <strong>Warning:</strong> This is a preliminary AI-assisted analysis and does not
          constitute legal advice. A licensed legal professional in the Kingdom of Saudi Arabia
          must be consulted before taking any action.
        </p>
      </div>
    </div>
  </section>

  <!-- ── Footer ── -->
  <footer class="footer">
    <span class="footer-text">إطار الذكاء الاصطناعي القانوني السعودي — مفتوح المصدر</span>
    <nav class="footer-links" aria-label="روابط ثانوية">
      <a href="https://github.com/Samix2026/saudi-legal-ai-framework"
         target="_blank" rel="noopener">GitHub</a>
      <a href="https://github.com/Samix2026/saudi-legal-ai-framework/blob/main/CONTRIBUTING.md"
         target="_blank" rel="noopener">المساهمة</a>
      <a href="https://github.com/Samix2026/saudi-legal-ai-framework/blob/main/LICENSE"
         target="_blank" rel="noopener">الترخيص</a>
    </nav>
  </footer>

</body>
</html>
```

- [ ] **Step 2: Open locally and verify**

```bash
open docs/index.html
```

On Linux: `xdg-open docs/index.html`

Check:
- Arabic title renders in Tajawal font
- Layout is RTL (nav on left, brand on right)
- 4 nav cards in a 2×2 grid
- Disclaimer amber block visible above footer
- No horizontal scrollbar at default viewport

- [ ] **Step 3: Commit**

```bash
git add docs/index.html
git commit -m "feat: add docs/index.html — Arabic-first GitHub Pages homepage"
```

---

## Task 4: `search.js` — Client-side search with safe DOM API

**Files:**
- Create: `docs/search.js`

All DOM manipulation uses `createElement` and `textContent` — no `innerHTML` with dynamic content.

- [ ] **Step 1: Create `docs/search.js`**

```js
'use strict';

// ── Search index (hardcoded — Phase 1 scope: skills, sources, prompts only) ──
const SEARCH_INDEX = [
  // Skills
  { type: 'skill',  title_ar: 'مراجعة العقود',              title_en: 'Contract Review',
    keywords: ['عقد','بنود','مراجعة','مخاطر','شرط جزائي','فسخ','contract','clause','review'],
    url: 'skills.html#contract-review' },
  { type: 'skill',  title_ar: 'النزاعات التجارية',          title_en: 'Commercial Dispute',
    keywords: ['نزاع','تجاري','محكمة تجارية','مطالبة','دعوى','commercial','dispute','court'],
    url: 'skills.html#commercial-dispute' },
  { type: 'skill',  title_ar: 'نظام التحكيم',               title_en: 'Arbitration',
    keywords: ['تحكيم','شرط تحكيم','محكم','arbitration','award'],
    url: 'skills.html#arbitration' },
  { type: 'skill',  title_ar: 'فحص الامتثال',               title_en: 'Compliance Check',
    keywords: ['امتثال','نطاقات','سعودة','PDPL','WPS','GOSI','compliance','nitaqat'],
    url: 'skills.html#compliance-check' },
  { type: 'skill',  title_ar: 'تحليل نظام العمل',           title_en: 'Labor Law Analysis',
    keywords: ['نظام العمل','عمالة','عقد عمل','مكافأة نهاية الخدمة','labor','employment'],
    url: 'skills.html#labor-law-analysis' },
  { type: 'skill',  title_ar: 'الصياغة القانونية',          title_en: 'Legal Drafting',
    keywords: ['صياغة','مذكرة','عريضة','إشعار','drafting','notice','memo'],
    url: 'skills.html#legal-drafting' },
  { type: 'skill',  title_ar: 'عقود العقارات والإيجار',     title_en: 'Real Estate Contracts',
    keywords: ['عقار','إيجار','ايجار','REGA','real estate','lease'],
    url: 'skills.html#real-estate-contracts' },

  // Official sources
  { type: 'source', title_ar: 'هيئة الخبراء بمجلس الوزراء', title_en: 'Bureau of Experts (boe.gov.sa)',
    keywords: ['هيئة الخبراء','نص نظام','boe','bureau of experts'],
    url: 'https://www.boe.gov.sa' },
  { type: 'source', title_ar: 'الجريدة الرسمية — أم القرى', title_en: 'Official Gazette (uqn.gov.sa)',
    keywords: ['أم القرى','جريدة رسمية','مرسوم ملكي','official gazette','uqn'],
    url: 'https://www.uqn.gov.sa' },
  { type: 'source', title_ar: 'ناجز — وزارة العدل',          title_en: 'Najiz — Ministry of Justice',
    keywords: ['ناجز','وزارة العدل','قضاء','تنفيذ','najiz','justice'],
    url: 'https://www.najiz.sa' },
  { type: 'source', title_ar: 'وزارة الموارد البشرية',       title_en: 'Ministry of Human Resources (hrsd.gov.sa)',
    keywords: ['موارد بشرية','وزارة العمل','hrsd','human resources'],
    url: 'https://www.hrsd.gov.sa' },
  { type: 'source', title_ar: 'منصة قيوة',                  title_en: 'Qiwa Platform',
    keywords: ['قيوة','عقود عمل','رخص العمل','qiwa','work permit'],
    url: 'https://www.qiwa.sa' },
  { type: 'source', title_ar: 'منصة استطلاع',               title_en: 'Istitlaa — Public Consultation',
    keywords: ['استطلاع','مشاورة عامة','مسودة أنظمة','istitlaa','consultation'],
    url: 'https://www.istitlaa.gov.sa' },
  { type: 'source', title_ar: 'هيئة حماية البيانات الشخصية', title_en: 'Personal Data Protection Authority',
    keywords: ['PDPL','حماية البيانات','خصوصية','pdpa','data protection'],
    url: 'https://www.pdpa.gov.sa' },
  { type: 'source', title_ar: 'الهيئة العامة للعقار',        title_en: 'Real Estate General Authority (rega.gov.sa)',
    keywords: ['عقار','REGA','تسجيل عقاري','real estate authority'],
    url: 'https://www.rega.gov.sa' },

  // Prompts
  { type: 'prompt', title_ar: 'قالب مراجعة عقد',             title_en: 'Contract Review Prompt',
    keywords: ['مراجعة عقد','تحليل عقد','contract review','prompt'],
    url: 'templates.html' },
  { type: 'prompt', title_ar: 'قالب صياغة إشعار قانوني',    title_en: 'Draft Legal Notice Prompt',
    keywords: ['إشعار','إنذار','مطالبة','legal notice','draft'],
    url: 'templates.html' },
  { type: 'prompt', title_ar: 'قالب تحليل المخاطر القانونية', title_en: 'Legal Risk Analysis Prompt',
    keywords: ['مخاطر','تحليل قانوني','تقييم مخاطر','risk analysis'],
    url: 'templates.html' },
];

const TYPE_LABELS = {
  skill:  { ar: 'مهارة', cls: 'result-type-skill'  },
  source: { ar: 'مصدر',  cls: 'result-type-source' },
  prompt: { ar: 'قالب',  cls: 'result-type-prompt' },
};

// ── DOM wiring (runs after defer) ──
const searchInput    = document.getElementById('search-input');
const searchDropdown = document.getElementById('search-dropdown');

if (searchInput && searchDropdown) {
  searchInput.addEventListener('input', onInput);
  searchInput.addEventListener('keydown', onKeydown);
  document.addEventListener('click', onClickOutside);
}

function onInput() {
  const query = searchInput.value.trim();
  if (query.length < 2) { hideDropdown(); return; }
  renderDropdown(runSearch(query));
}

function runSearch(query) {
  const q = query.toLowerCase();
  return SEARCH_INDEX.filter(item =>
    item.title_ar.toLowerCase().includes(q) ||
    item.title_en.toLowerCase().includes(q) ||
    item.keywords.some(k => k.toLowerCase().includes(q))
  ).slice(0, 6);
}

// ── Safe DOM rendering (no innerHTML with dynamic content) ──
function renderDropdown(results) {
  // Clear previous results safely
  while (searchDropdown.firstChild) {
    searchDropdown.removeChild(searchDropdown.firstChild);
  }

  if (results.length === 0) {
    const msg = document.createElement('div');
    msg.className = 'search-no-result';

    const text = document.createTextNode('لا توجد نتائج مطابقة — تصفّح ');
    const sourcesLink = document.createElement('a');
    sourcesLink.href = 'sources.html';
    sourcesLink.textContent = 'المصادر';
    const orText = document.createTextNode(' أو ');
    const skillsLink = document.createElement('a');
    skillsLink.href = 'skills.html';
    skillsLink.textContent = 'المهارات';
    const endText = document.createTextNode(' مباشرةً.');

    msg.appendChild(text);
    msg.appendChild(sourcesLink);
    msg.appendChild(orText);
    msg.appendChild(skillsLink);
    msg.appendChild(endText);
    searchDropdown.appendChild(msg);
    showDropdown();
    return;
  }

  results.forEach(item => {
    const type = TYPE_LABELS[item.type] || { ar: item.type, cls: '' };
    const isExternal = item.url.startsWith('http');

    const link = document.createElement('a');
    link.className = 'search-result';
    link.href = item.url;
    if (isExternal) { link.target = '_blank'; link.rel = 'noopener'; }
    link.setAttribute('role', 'option');

    const badge = document.createElement('span');
    badge.className = 'result-type ' + type.cls;
    badge.textContent = type.ar;

    const textWrap = document.createElement('span');
    textWrap.className = 'result-text';

    const titleAr = document.createElement('span');
    titleAr.className = 'result-title-ar';
    titleAr.textContent = item.title_ar;

    const titleEn = document.createElement('span');
    titleEn.className = 'result-title-en';
    titleEn.setAttribute('dir', 'ltr');
    titleEn.textContent = item.title_en;

    textWrap.appendChild(titleAr);
    textWrap.appendChild(titleEn);
    link.appendChild(badge);
    link.appendChild(textWrap);
    searchDropdown.appendChild(link);
  });

  showDropdown();
}

function showDropdown() {
  searchDropdown.classList.add('visible');
  searchInput.setAttribute('aria-expanded', 'true');
}

function hideDropdown() {
  searchDropdown.classList.remove('visible');
  searchInput.setAttribute('aria-expanded', 'false');
}

function onClickOutside(e) {
  if (!e.target.closest('#search-wrap')) { hideDropdown(); }
}

function onKeydown(e) {
  if (e.key === 'Escape') { hideDropdown(); searchInput.blur(); }
}
```

- [ ] **Step 2: Verify search in browser**

Open `docs/index.html`. In the search box:

| Query | Expected result |
|-------|----------------|
| `نظام العمل` | Labor Law skill + HRSD source appear |
| `contract` | Contract Review skill + Contract Review prompt appear |
| `boe` | Bureau of Experts source appears |
| `zzz` | "لا توجد نتائج مطابقة" message with links to sources/skills |
| Escape key | Dropdown closes |
| Click outside | Dropdown closes |
| 1 character | No dropdown shown |

- [ ] **Step 3: Commit**

```bash
git add docs/search.js
git commit -m "feat: add client-side search index and safe DOM dropdown for GitHub Pages"
```

---

## Task 5: README update

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read the current README opening**

```bash
head -40 README.md
```

Find the first `##` section heading (e.g. `## Repository Structure` or `## Overview`).

- [ ] **Step 2: Insert the Website section above that first `##` heading**

Add this block immediately before the first `##` section:

```markdown
## 🌐 Website

The framework is available as a browsable website built with plain HTML/CSS/JS,
served via GitHub Pages from the `docs/` directory:

**https://samix2026.github.io/saudi-legal-ai-framework/**

Features: Arabic-first interface · official sources directory · legal AI skills browser · client-side search
```

- [ ] **Step 3: Verify**

```bash
grep -n "Website\|github.io" README.md | head -5
```

Expected: the Website section and the GitHub Pages URL appear.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add GitHub Pages website link to README"
```

---

## Task 6: Validation and local preview

No new files. Verification only.

- [ ] **Step 1: Local preview via HTTP server**

```bash
python3 -m http.server 8080 --directory .
```

Open `http://localhost:8080/docs/` in browser (tests the exact GitHub Pages subpath).

- [ ] **Step 2: Full validation checklist**

Work through every item:

- [ ] `docs/.nojekyll` exists (`ls -la docs/.nojekyll`)
- [ ] `docs/styles.css` loads — no CSS errors in browser console
- [ ] `docs/index.html` opens — no 404s in Network tab
- [ ] Arabic title renders in Tajawal font (DevTools → Elements → Computed → font-family)
- [ ] Layout is RTL: brand on right side, nav links on left side
- [ ] Disclaimer amber accent bar on the right edge of the box (border-inline-start maps to right in RTL)
- [ ] Search "عقد" → Contract Review skill appears
- [ ] Search "boe" → Bureau of Experts source appears
- [ ] Search "zzz" → "لا توجد نتائج مطابقة" message
- [ ] Escape key closes dropdown
- [ ] Click outside search area closes dropdown
- [ ] Mobile 375px (DevTools device toolbar): single column, nav links hidden, no horizontal scroll
- [ ] Datasets card opens GitHub `datasets/` tree in new tab
- [ ] GitHub CTA opens repo in new tab
- [ ] Footer links open GitHub in new tab
- [ ] `.superpowers/` in `.gitignore`: `grep superpowers .gitignore`
- [ ] No `.superpowers/` files tracked: `git ls-files .superpowers/` → empty
- [ ] README contains GitHub Pages URL: `grep github.io README.md`

- [ ] **Step 3: Fix any issues found, then commit**

```bash
git add -p
git commit -m "fix: address validation issues from local preview pass"
```

Skip if no issues found.

---

## Commit Strategy Summary

| # | Message | Files |
|---|---------|-------|
| 1 | `chore: add docs/.nojekyll to disable Jekyll on GitHub Pages` | `docs/.nojekyll` |
| 2 | `feat: add shared RTL stylesheet for GitHub Pages website` | `docs/styles.css` |
| 3 | `feat: add docs/index.html — Arabic-first GitHub Pages homepage` | `docs/index.html` |
| 4 | `feat: add client-side search index and safe DOM dropdown for GitHub Pages` | `docs/search.js` |
| 5 | `docs: add GitHub Pages website link to README` | `README.md` |
| 6 | `fix: address validation issues from local preview pass` | (only if needed) |

---

## Validation Checklist (pre-PR)

- [ ] `docs/.nojekyll` exists and is empty
- [ ] `docs/styles.css` — no console CSS errors
- [ ] `docs/index.html` — no 404s, no console JS errors
- [ ] Arabic text renders in Tajawal font
- [ ] RTL layout correct: brand right, nav left, amber bar on right edge
- [ ] Search works for Arabic query ("عقد"), English query ("contract"), source domain ("boe")
- [ ] No-result message appears with links for unknown query
- [ ] Escape and click-outside dismiss dropdown
- [ ] Mobile 375px: single column, no horizontal scroll, nav links hidden
- [ ] Disclaimer bilingual text present (Arabic + English paragraphs)
- [ ] All 4 nav cards link to correct targets
- [ ] Footer GitHub links open in new tab
- [ ] `.superpowers/` in `.gitignore`, not tracked in git
- [ ] README contains GitHub Pages URL
- [ ] No files from `.superpowers/brainstorm/` referenced by any `docs/` file
