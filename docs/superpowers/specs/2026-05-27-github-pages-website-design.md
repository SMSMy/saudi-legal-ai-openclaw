# GitHub Pages Website — Design Spec

**Date:** 2026-05-27
**Scope:** Phase 1 — static website only. No judicial template JSON system, no calculators, no dataset expansion, no AI integrations.
**Deliverable:** Production-ready `docs/` HTML/CSS/JS website, GitHub Pages compatible, Arabic-first.

---

## Canonical Directory Rule

`docs/` is the **only production directory** for the website. Every HTML, CSS, JS, and asset file that ships to GitHub Pages lives under `docs/`. Nothing else.

`.superpowers/brainstorm/` contains mockups and design experiments created during brainstorming. It is **never deployed**, never referenced from production HTML, and should be added to `.gitignore`. The final implementation does not use, reference, or depend on any file under `.superpowers/`.

Existing markdown files in `docs/` (architectural docs, cross-reference map, usage guides) remain untouched. They are developer-facing internal documentation and are not part of the public website navigation.

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
- No hamburger menu in Phase 1. On narrow viewports (≤600px) the nav links wrap or collapse to a single visible item — see §12 for mobile behavior.
- No dropdown menus.

### Active state

Set via a `data-page` attribute on `<body>`. Each nav link has a matching `data-nav` attribute. CSS selector: `body[data-page="sources"] [data-nav="sources"]`.

### Footer links

GitHub (opens in new tab), CONTRIBUTING.md, LICENSE — all open in new tab as absolute GitHub URLs.

---

## 4. Arabic-First UX Rules

### Direction and language

1. **`<html lang="ar" dir="rtl">`** on every page.
2. **RTL layout everywhere.** No LTR islands except English sub-labels, which use `dir="ltr"` inline and `font-family: 'Segoe UI', sans-serif` at 11px.
3. **CSS reset sets `text-align: right`** on `body`. No LTR overrides unless explicitly required for a code snippet or URL.
4. **Navigation order (RTL):** Brand on the far right, links progressing left, GitHub CTA on the far left.

### RTL spacing rules

5. **Logical CSS properties.** Use `padding-inline-start` / `padding-inline-end` and `margin-inline-*` in preference to explicit `left`/`right` padding — this makes RTL/LTR switching safe.
6. **Disclaimer accent border** on `border-inline-start: 4px solid var(--amber)` — maps to the right edge in RTL (reading entry side).
7. **Card icon** sits at `inline-end` (left visually in RTL) of the card header. Arrow sits at `inline-start` (right visually in RTL).
8. **Flex row direction.** All `display: flex` rows that depend on order use `flex-direction: row` — no `row-reverse` tricks. RTL flipping is handled by `dir="rtl"` on the HTML element.
9. **Search input** uses `direction: rtl; text-align: right`. The search icon is positioned at `left: 16px` (the visually trailing side in RTL).

### Typography rules

10. **Card titles in Arabic first.** English subtitle is a `<span>` with `dir="ltr"` below the Arabic title, at `font-size: 11px`, `color: var(--text-muted)`.
11. **Card tag chips** (e.g. "12 مصدراً رسمياً") are in Arabic. No English-only chips.
12. **Tajawal font** is loaded via Google Fonts on every page. The system-font fallback stack handles the unlikely case Google Fonts is unreachable, but Tajawal is required for correct Arabic spacing.
13. **No mixed-direction paragraphs.** If a paragraph contains both Arabic and English sentences, they are split into separate `<p>` elements, each with appropriate `dir` attribute.
14. **Numerals.** Use Arabic-Indic numerals (٠١٢٣) only where the content itself is Arabic-language prose. Use Western numerals (0123) for counts in card chips and in English-language inline labels.

---

## 5. Search Behavior (Intentionally Limited)

Phase 1 search is **deliberately simple**. Its purpose is discoverability, not full-text retrieval. It does not search document bodies, datasets, or examples. It does not require a backend, build step, or index generation script.

**Implementation:** Single `search.js` file. Hardcoded in-memory array. No external dependency.

**Scope (explicit ceiling — do not expand in Phase 1):**
- 7 skills — `name_ar`, `name_en`, `keywords[]`
- ~12 official sources — `name_ar`, `name_en`, `authority`, `url`
- 3 prompt templates — `name_ar`, `name_en`, `keywords[]`

**What is NOT searched in Phase 1:** dataset files, example files, source regulation text, judicial templates, full skill body text. These are future phases.

**Index format (hardcoded in `search.js`):**
```js
const SEARCH_INDEX = [
  { type: 'skill',   title_ar: '...', title_en: '...', keywords: ['...'], url: 'skills.html#slug' },
  { type: 'source',  title_ar: '...', title_en: '...', keywords: ['...'], url: 'https://...' },
  { type: 'prompt',  title_ar: '...', title_en: '...', keywords: ['...'], url: 'templates.html' },
];
```

**Behavior:**
- Trigger: `input` event (live, no submit required)
- Minimum query: 2 characters — below this, dropdown is hidden
- Match: case-insensitive substring on `title_ar`, `title_en`, and each keyword
- Results: max 6 items, inline dropdown, type badge + Arabic title + muted English label
- No result: "لا توجد نتائج مطابقة" + link to sources page and skills page
- Dismiss: click outside dropdown, or press Escape

**Not in scope:** fuzzy matching, ranked results, query highlighting, search history, autocomplete suggestions.

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

## 10. GitHub Pages Deployment

### Step-by-step setup (one-time)

1. Go to **Settings → Pages** in the GitHub repository.
2. Under "Build and deployment", set Source to **"Deploy from a branch"**.
3. Set Branch to **`main`**, folder to **`/docs`**.
4. Click **Save**. GitHub will publish within 1–2 minutes.
5. The site URL will be `https://samix2026.github.io/saudi-legal-ai-framework/`.

### Required file: `docs/.nojekyll`

Create an empty file at `docs/.nojekyll`. This tells GitHub Pages not to run Jekyll, which would otherwise ignore files starting with `_` and may interfere with directory structure. No content needed — the file's presence is the signal.

### Asset path rule

All paths in HTML and CSS must be **relative**, not absolute:
- `href="styles.css"` ✓ — works on GitHub Pages subpath and locally
- `href="/docs/styles.css"` ✗ — breaks locally
- `href="https://..."` ✓ — allowed only for external resources (Google Fonts, GitHub links)

### Artifact isolation

`.superpowers/brainstorm/` must be listed in `.gitignore`. It contains only mockup HTML used during the design phase. It is never served by GitHub Pages and must not be referenced from any production file.

If `.superpowers/` is already tracked, add it to `.gitignore` and remove it from git tracking with `git rm -r --cached .superpowers/`.

### Local preview

Open `docs/index.html` directly in a browser — no local server required. Relative paths mean the full site works without any dev server. For accurate GitHub Pages subpath testing, use `python3 -m http.server` from the repo root and navigate to `http://localhost:8000/docs/`.

---

## 11. Mobile Behavior

Phase 1 is mobile-aware but not mobile-first in design priority. It must be usable on phones without horizontal scrolling or broken layouts. No JavaScript is used for responsive behavior — CSS only.

### Breakpoints

| Breakpoint | Width | Changes |
|---|---|---|
| Desktop | > 768px | Default layout as specified in §2 |
| Tablet | 601–768px | Card grid collapses to 1-column. Hero padding reduces to 40px top. |
| Mobile | ≤ 600px | Nav links hidden except brand and GitHub CTA. Hero title reduces to 22px. Search bar full-width. Cards single column. |

### Mobile nav rule

At ≤600px: show only the brand monogram + name and the GitHub CTA button. All four nav links are hidden with `display: none`. This is intentional — a hamburger menu is a Phase 2 addition. Users on mobile can reach all pages via the homepage navigation cards.

### Mobile typography adjustments

| Element | Desktop | Mobile (≤600px) |
|---|---|---|
| Hero title | 30px | 22px |
| Hero subtitle | 15px | 14px |
| Section heading | 20px | 17px |
| Body/description | 13–14px | 13px (unchanged) |

### Mobile touch targets

- All navigation links and card links: minimum 44px tap height
- Search input: minimum 48px height on mobile
- Card padding on mobile: 16px (reduced from 22px desktop)

### No horizontal scroll

The `max-width: 780px` centered container must not cause horizontal overflow on any viewport. Use `width: 100%; max-width: 780px` with `padding: 0 20px` on mobile (reduced from `0 40px` desktop).

---

## 12. README Update

Add a "Website" section to `README.md` above the existing structure section:

```markdown
## 🌐 Website

The framework is available as a browsable website:
**[saudi-legal-ai-framework.github.io](https://samix2026.github.io/saudi-legal-ai-framework)**

The site is built with plain HTML/CSS/JS and served via GitHub Pages from the `docs/` directory.
```

---

## Non-Goals (Phase 1)

This is a **static knowledge platform**, not an application. The following are explicitly out of scope and must not appear in the implementation:

**Infrastructure:**
- No build step, bundler, or framework (no React, Vue, Webpack, Vite, etc.)
- No server-side rendering or static site generator (no Jekyll, Hugo, Next.js)
- No package.json, node_modules, or npm scripts
- No cookies, local storage, or session state
- No external API calls at runtime
- No analytics or tracking scripts
- No PWA / service worker

**Features:**
- No authentication or user accounts
- No form submissions or user-generated content
- No dark mode (Phase 2)
- No language toggle / English version (Phase 2)
- No hamburger nav menu (Phase 2)
- No pagination (card counts are small enough to show all items)
- No infinite scroll or lazy loading

**Content:**
- No judicial template JSON system (Phase 2)
- No legal calculators (Phase 2)
- No dataset browser (Phase 2)
- No full skill body text rendered in the browser (link to GitHub source file instead)
- No AI integrations (Phase 3+)

If any feature not listed in §2–§12 seems like a good addition during implementation, it should be documented in a follow-up issue rather than added to this PR.
