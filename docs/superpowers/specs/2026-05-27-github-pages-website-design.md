# GitHub Pages Website — Design Spec

**Date:** 2026-05-27
**Scope:** Phase 1 — static website only. No judicial template JSON system, no calculators, no dataset expansion, no AI integrations.
**Deliverable:** Production-ready `docs/` HTML/CSS/JS website, GitHub Pages compatible, Arabic-first.

---

## 1. Visual Direction

### Color Palette

| Token | Value | Usage |
|---|---|---|
| `--navy` | `#1a2e3b` | Primary: header background, headings, card icons |
| `--navy-mid` | `#2c4a5a` | Secondary: hover states, card icon backgrounds |
| `--cream` | `#f7f5f0` | Page background |
| `--cream-dark` | `#eceae3` | Subtle section dividers, hover backgrounds |
| `--border` | `#dddad3` | Card borders, input borders |
| `--border-light` | `#ebe9e2` | Section separators |
| `--text` | `#1a1a1a` | Primary body text |
| `--text-mid` | `#3a3a3a` | Secondary body text |
| `--text-muted` | `#7a7a78` | Subtitles, descriptions, hints |
| `--teal` | `#2e8b7a` | Active nav item, card tags, interactive accents |
| `--amber` | `#b5651d` | Disclaimer accent, warning elements |
| `--amber-bg` | `#fdf6ec` | Disclaimer section background |
| `--amber-border` | `#ddb88a` | Disclaimer border |
| `--white` | `#ffffff` | Card backgrounds, input fields |

No gradients. No shadows heavier than `0 4px 16px rgba(26,46,59,.08)`. No decorative images.

### Typography

**Primary font:** `'Tajawal'` (Google Fonts) — Arabic-optimized, clean, institutional feel.
**Fallback stack:** `'Segoe UI', Tahoma, Arial, sans-serif`
**Load strategy:** Single `@import` in `styles.css` for Tajawal weights 300, 400, 500, 700.

| Element | Size | Weight | Color |
|---|---|---|---|
| Page title (hero) | 30px | 700 | `--navy` |
| Section heading | 20px | 700 | `--navy` |
| Card title (Arabic) | 15px | 700 | `--navy` |
| Card subtitle (English) | 11px | 400 | `--text-muted` |
| Body / description | 13–14px | 400 | `--text-muted` |
| Eyebrow label | 11px | 500 | `--teal` |
| Search hint | 11px | 400 | `--text-muted` |
| Disclaimer title | 13px | 700 | `--amber` |
| Disclaimer body | 12px | 400 | `#6b4c2a` |
| Footer | 12px | 400 | `rgba(255,255,255,.4)` |
| Nav links | 13px | 400–500 | `rgba(255,255,255,.65)` → `.92` |

**Line height:** 1.7 for body paragraphs. 1.35 for headings.
**Letter spacing:** `-0.01em` on large headings. `0.12em` on eyebrow labels.

### Spacing System

Base unit: 8px. All padding and gap values are multiples of 8.

- Header height: 56px
- Hero padding: 64px top, 52px bottom
- Section padding: 40px horizontal, consistent across all sections
- Card padding: 22px top/sides, 18px bottom
- Card gap: 14px
- Max content width: 780px (centered)

### Borders and Radius

- Cards: `border-radius: 10px`, `border: 1px solid var(--border)`
- Inputs: `border-radius: 8px`
- Brand icon: `border-radius: 6px`
- Tags/pills: `border-radius: 20px`
- Disclaimer: `border-radius: 8px`, right border `4px solid var(--amber)` (RTL emphasis side)

---

## 2. Page Structure

### 2.1 index.html — Home

Sections in order (top to bottom):

1. **Top bar** — fixed height 56px, dark navy, brand monogram + name, nav links, GitHub link
2. **Hero** — eyebrow label, large title (Arabic), subtitle (Arabic), search bar + hint text
3. **Section divider** — 1px `--border-light` line, full-width up to max-width
4. **Navigation cards** — 2×2 grid, 4 cards (sources, skills, templates, datasets)
5. **Disclaimer section** — amber-accented box, bilingual (Arabic + English)
6. **Footer** — dark navy, repo name left, links (GitHub, Contributing, License) right

### 2.2 sources.html — Official Sources

Sections in order:

1. **Top bar** (same as all pages)
2. **Page header** — title "المصادر الرسمية / Official Legal Sources", 1-line description
3. **Category sections** — one `<section>` per authority group:
   - نظام التشريعات: هيئة الخبراء (boe.gov.sa) · أم القرى (uqn.gov.sa)
   - القضاء والتنفيذ: ناجز (najiz.sa) · وزارة العدل (moj.gov.sa)
   - العمل والتوظيف: وزارة الموارد البشرية (hrsd.gov.sa) · قيوة (qiwa.sa)
   - التشاور والتشريع: منصة استطلاع (istitlaa.gov.sa)
   - حماية البيانات: هيئة حماية البيانات الشخصية (pdpa.gov.sa)
4. **Source cards** — each card: Arabic name, English name, authority type badge, 1-line description, official URL (external link, opens in new tab)
5. **Disclaimer section** (same amber block as homepage)
6. **Footer** (same)

### 2.3 skills.html — Legal AI Skills

Sections in order:

1. **Top bar**
2. **Page header** — title, 1-line description of what "skills" are in this context
3. **Skills grid** — 7 skill cards in a 2-column grid (or 3 on wide screens):
   - contract-review, commercial-dispute, arbitration, compliance-check, labor-law-analysis, legal-drafting, real-estate-contracts
4. **Each skill card** — Arabic name, English name, use-case tags (2–3), short description, "اقرأ المزيد" link to the raw GitHub skill file
5. **Relationship graph note** — a small informational box: "هذه المهارات مترابطة في شبكة علائقية موجَّهة مكوَّنة من 14 حافة" (forward-reference to future visualization)
6. **Disclaimer section**
7. **Footer**

### 2.4 templates.html — Judicial Drafting (Placeholder)

Sections in order:

1. **Top bar**
2. **Page header** — title "الصياغة القضائية / Judicial Drafting"
3. **Coming-soon block** — clear visual placeholder explaining what will be here:
   - Structured judicial templates in JSON format
   - Court session templates, settlement notices, procedural templates
   - All clearly labeled as community-generated, unverified
4. **Disclaimer section**
5. **Footer**

---

## 3. Navigation Model

### Top bar (persistent across all pages)

```
[ق brand] [إطار الذكاء الاصطناعي القانوني السعودي]   [الرئيسية] [المصادر الرسمية] [المهارات القانونية] [الصياغة القضائية] [GitHub ↗]
```

- Direction: RTL. Brand on the right, nav links and GitHub CTA on the left.
- Active page link: full white (`rgba(255,255,255,.92)`).
- Inactive links: `rgba(255,255,255,.65)`.
- GitHub link: teal-bordered pill button.
- No hamburger menu in Phase 1 (desktop-first, mobile wrapping acceptable).
- No dropdown menus.

### Active state

Set via a `data-page` attribute on `<body>`. Each nav link has a matching `data-nav` attribute. CSS selector: `body[data-page="sources"] [data-nav="sources"]`.

### Footer links

GitHub (opens in new tab), CONTRIBUTING.md, LICENSE — all open in new tab as absolute GitHub URLs.

---

## 4. Arabic-First UX Rules

1. **`<html lang="ar" dir="rtl">`** on every page.
2. **RTL layout everywhere.** No LTR islands except English sub-labels (which use `font-family: 'Segoe UI', sans-serif` and `font-size: 11px`).
3. **Text alignment: `text-align: right`** by default via CSS reset.
4. **Disclaimer border emphasis on the right** (not left) to match RTL reading direction.
5. **Search input: `direction: rtl; text-align: right`**. Placeholder in Arabic.
6. **Navigation order:** Arabic links precede the English GitHub CTA.
7. **Card titles in Arabic first**, English subtitle in smaller muted text below.
8. **Card tag chips** (e.g. "12 مصدراً رسمياً", "7 مهارات") in Arabic.
9. **Tajawal font** loaded from Google Fonts for every page. No system-font-only fallback for Arabic.
10. **No mixed-direction paragraphs.** Arabic text and English text are in separate `<span>` or `<p>` elements.

---

## 5. Search Behavior

**Phase 1 implementation:** Client-side, single-file `search.js`. No server, no API.

**What it searches:** A static in-memory index built from:
- 7 skills (name_ar, name_en, keywords)
- 12+ sources (name_ar, name_en, authority, url)
- 3 prompts (name_ar, name_en, keywords)

**Index format:**
```js
const SEARCH_INDEX = [
  { type: 'skill', title_ar: '...', title_en: '...', keywords: ['...'], url: 'skills.html#slug' },
  { type: 'source', title_ar: '...', title_en: '...', keywords: ['...'], url: 'https://...' },
  ...
];
```

**Search trigger:** `input` event on the search box (no form submit required).

**Minimum query length:** 2 characters.

**Match strategy:** Case-insensitive substring match against `title_ar`, `title_en`, and `keywords[]`. No fuzzy matching in Phase 1.

**Result display:** Inline dropdown below the search box, max 6 results, showing type badge + Arabic title + English subtitle. Each result is a clickable link.

**No results state:** "لا توجد نتائج مطابقة" with a suggestion to check the sources or skills pages directly.

**Dropdown dismiss:** Click outside or press Escape.

---

## 6. Disclaimer Placement

The disclaimer block appears **on every page**, positioned between the main content and the footer. It is never inside a card, never in the nav, never collapsed behind a toggle.

**Visual spec:**
- Background: `var(--amber-bg)` (`#fdf6ec`)
- Border: `1px solid var(--amber-border)` + `4px solid var(--amber)` on the right (RTL)
- Border radius: 8px
- Icon: ⚠️ emoji, 18px, top-aligned
- Title: "تحذير قانوني مهم" in `--amber`, 13px, bold
- Arabic body paragraph
- English body paragraph

**Required Arabic text (verbatim from CLAUDE.md):**
> هذا تحليل أولي بمساعدة الذكاء الاصطناعي ولا يُعدّ استشارة قانونية. يجب مراجعة مختص قانوني مرخّص في المملكة العربية السعودية قبل اتخاذ أي إجراء.

**Required English text (verbatim from CLAUDE.md):**
> This is a preliminary AI-assisted analysis and does not constitute legal advice. A licensed legal professional in the Kingdom of Saudi Arabia must be consulted before taking any action.

Supplementary text (website-specific): "الأنظمة واللوائح عرضةٌ للتغيير — تحقق دائماً من المصادر الرسمية المعتمدة."

---

## 7. Content Hierarchy

### Homepage

```
Eyebrow label (smallest, teal, uppercase)
  └─ Hero title (largest, navy, 30px bold)
       └─ Hero subtitle (muted, 15px)
            └─ Search bar (prominent, white card)
                 └─ Search hint (smallest, muted)
─────────────────────────────────────────
Nav cards (2×2, equal visual weight)
  Each card:
    Icon (top right, soft colored background)
    Arrow (top left, fades in on hover)
    Arabic title (bold, navy)
    English subtitle (small, muted)
    Description (muted paragraph)
    Tag chip (bottom, colored pill)
─────────────────────────────────────────
Disclaimer (amber, always present)
─────────────────────────────────────────
Footer (dark, secondary links)
```

### Inner pages (sources, skills)

```
Top bar
─────────────────────────────────────────
Page header (title + 1-line description)
─────────────────────────────────────────
Content grid (cards or category sections)
─────────────────────────────────────────
Disclaimer
─────────────────────────────────────────
Footer
```

---

## 8. Files to Create Under docs/

```
docs/
├── index.html              ← Homepage (hero, search, 4 nav cards, disclaimer, footer)
├── sources.html            ← Official sources, categorized cards
├── skills.html             ← 7 AI skill cards with descriptions and tags
├── templates.html          ← Judicial drafting placeholder page
├── styles.css              ← Shared stylesheet (RTL reset, variables, all components)
├── search.js               ← Client-side search index and dropdown logic
└── assets/
    └── cover.png           ← Symlink or copy of existing assets/cover.png (for og:image)
```

Existing files in `docs/` (markdown architectural docs) remain untouched. GitHub Pages serves them as raw text, which is acceptable for developer-facing content.

### Each HTML file must include

- `<html lang="ar" dir="rtl">`
- `<meta charset="UTF-8">`
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- `<meta name="description" content="...">` (Arabic)
- `<link rel="stylesheet" href="styles.css">` (relative path)
- `<script src="search.js" defer></script>` (on index, sources, skills pages)
- `<body data-page="...">` for active nav state

### styles.css structure

```
1. @import Tajawal from Google Fonts
2. CSS custom properties (:root)
3. Reset + RTL defaults
4. Topbar component
5. Hero component
6. Search component + dropdown
7. Cards grid + nav-card
8. Section divider
9. Disclaimer box
10. Footer
11. Page-specific overrides (sources, skills, templates)
12. Responsive breakpoints (≤768px)
```

---

## 9. Placeholder Content (Later Phases)

The following are **explicitly out of scope for Phase 1** and must appear only as placeholder blocks:

| Feature | Placeholder treatment |
|---|---|
| Judicial template JSON system | `templates.html` shows a "coming soon" block with description of what's planned |
| Legal calculators (Diyat, inheritance, fees) | Not referenced in Phase 1 |
| Dataset browser | The "مجموعات البيانات" nav card links to the raw GitHub `datasets/` folder on GitHub.com (external link, new tab) |
| Full-text dataset search | Phase 1 search covers only skills, sources, prompts |
| Skill relationship graph visualization | A note on `skills.html` references the 14-edge graph but no visual renderer |
| MCP / AI assistant integration | Not referenced |
| Arabic/English language toggle | Not in Phase 1; full Arabic only |
| Dark mode | Not in Phase 1 |

**Placeholder block visual spec:** A `--cream-dark` background box with a teal left border (RTL: right border), icon, Arabic title, brief description of what's planned, and "قريباً / Coming Soon" badge.

---

## 10. GitHub Pages Configuration

- **Source:** `docs/` folder on `main` branch (configured in repo Settings → Pages).
- **No Jekyll.** Add an empty `.nojekyll` file at `docs/.nojekyll` to prevent Jekyll processing.
- **All asset paths are relative** (e.g. `href="styles.css"` not `href="/docs/styles.css"`) so the site works both on `github.io/repo/` paths and locally by opening `index.html` directly.
- The `.superpowers/brainstorm/` directory is for mockups only. Nothing inside it is part of the production website.

---

## 11. README Update

Add a "Website" section to `README.md` above the existing structure section:

```markdown
## 🌐 Website

The framework is available as a browsable website:
**[saudi-legal-ai-framework.github.io](https://samix2026.github.io/saudi-legal-ai-framework)**

The site is built with plain HTML/CSS/JS and served via GitHub Pages from the `docs/` directory.
```

---

## Non-Goals (Phase 1)

- No build step, bundler, or framework
- No server-side rendering
- No authentication
- No form submissions
- No external APIs
- No cookies or local storage
- No analytics
- No PWA / service worker
- No i18n toggle (English version is a later phase)
