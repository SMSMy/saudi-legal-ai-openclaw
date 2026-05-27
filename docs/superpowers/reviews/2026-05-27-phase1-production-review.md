# Phase 1 Production Review
**Date:** 2026-05-27  
**Files reviewed:** `docs/index.html`, `docs/styles.css`, `docs/search.js`

---

## Critical

Issues that affect accessibility, legal readability, or are outright incorrect.

### C1 — RTL search icon placement
**File:** `styles.css:189`, `styles.css:167`

The search icon sits at physical `left: 16px`. In an RTL document, Arabic text starts at the **right** edge and flows left. The icon is therefore on the opposite side from where text begins — a mismatch between text direction and icon position.

The input padding also compensates on the wrong side:
```css
/* current */
padding: 13px 20px 13px 52px;   /* 52px on physical left for icon */
left: 16px;

/* correct for RTL */
padding: 13px 52px 13px 20px;   /* 52px on physical right (inline-start) for icon */
inset-inline-start: 16px;       /* logical property — maps to right in RTL */
```

### C2 — No `<main>` landmark
**File:** `index.html`

The page has no `<main>` element. Screen reader users cannot jump to main content. Keyboard users must tab through all 5 topbar links on every page load before reaching the search field.

Add `<main>` wrapping hero through disclaimer:
```html
<main id="main-content">
  <section class="hero">…</section>
  …
  <section class="disclaimer-section">…</section>
</main>
```

And a skip link as the very first element in `<body>`:
```html
<a href="#main-content" class="skip-link">تخطّ إلى المحتوى الرئيسي</a>
```
With CSS to visually hide it until focused.

### C3 — No `:focus-visible` styles
**File:** `styles.css`

Zero explicit focus styles anywhere. All interactive elements — nav links, cards, search input, search results — rely entirely on browser defaults, which are inconsistent across browsers and invisible in some.

Minimum required:
```css
:focus-visible {
  outline: 2px solid var(--teal);
  outline-offset: 2px;
}
a:focus-visible, button:focus-visible {
  border-radius: 3px;
}
```

### C4 — `--text-muted` fails WCAG AA contrast
**File:** `styles.css:13`

`--text-muted: #7a7a78` on white (`#ffffff`) produces a contrast ratio of approximately **3.85:1**. WCAG AA requires 4.5:1 for body text below 18px (or below 14px bold). This fails for:
- `.hero-subtitle` (15px, weight 400)
- `.card-desc` (13px, weight 400)
- `.search-hint` (11px)
- `.card-title-en` (11px)

Minimum passing value at this hue: `#767472` → `#696766` (4.5:1). A value of `#696766` resolves this.

### C5 — Footer text is near-invisible
**File:** `styles.css:441`, `styles.css:451`

`rgba(255,255,255,.4)` on `--navy: #1a2e3b` background: effective contrast ≈ **2.1:1**. Both `.footer-text` and `.footer-links a` fail AA at 12px. The footer contains real navigation (GitHub, Contributing, License) — these are not merely decorative.

`rgba(255,255,255,.6)` reaches approximately 3.5:1 (passes AA Large). `rgba(255,255,255,.75)` reaches approximately 4.5:1 (passes AA).

---

## Recommended

Correctness and quality issues that don't break the page but should be fixed before the site is considered production-grade.

### R1 — Dead CSS variables
**File:** `styles.css:8–9`

`--cream-dark: #eceae3` and `--text-mid: #3a3a3a` are defined in `:root` but referenced nowhere in the stylesheet. Remove both.

### R2 — Unused Tajawal weight 300 in font import
**File:** `styles.css:1`

```css
/* current — downloads weight 300 unnecessarily */
family=Tajawal:wght@300;400;500;700

/* fix */
family=Tajawal:wght@400;500;700
```

Weight 300 appears in no rule in the stylesheet. This adds ~6–10KB to the font payload on first load.

### R3 — `@import` blocks font load
**File:** `styles.css:1`, `index.html`

`@import` in CSS means: parse CSS → discover `@import` → fetch font sheet → continue rendering. It introduces a serial fetch that `<link>` in `<head>` avoids.

Move to `index.html` (and all future pages):
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap"
      rel="stylesheet" />
```
Remove the `@import` line from `styles.css`.

### R4 — Card titles are `<div>`, not headings
**File:** `index.html:69,85,101,119`

`<div class="card-title">` contains the primary label for each card section. Screen readers cannot navigate by heading to "المصادر الرسمية" or "المهارات القانونية". Change to `<h2>` with a visual-only style override if needed — the font size and weight don't need to change.

```html
<!-- current -->
<div class="card-title">المصادر الرسمية</div>

<!-- fix -->
<h2 class="card-title">المصادر الرسمية</h2>
```

### R5 — `<div role="separator">` should be `<hr>`
**File:** `index.html:57`

`<hr>` is the native thematic break / separator element. Style it to match:
```css
hr.section-divider {
  border: none;
  border-bottom: 1px solid var(--border-light);
  /* ... rest of existing .section-divider rules */
}
```

### R6 — Search has no keyboard result navigation
**File:** `search.js:178`

Pressing `↑` / `↓` after typing does not move focus into the dropdown. Keyboard-only users cannot select a result without a mouse. This blocks a common interaction pattern.

Minimum implementation: on `ArrowDown` key from the input, move focus to the first `.search-result` element; on `ArrowUp` from first result, return focus to input.

### R7 — `.nav-cta` uses `!important` twice
**File:** `styles.css:108–115`

The `!important` escalation exists because `.topbar-nav a` (specificity 0,1,1) overrides `.nav-cta` (specificity 0,1,0). Fix with a more specific selector instead:

```css
/* current */
.nav-cta { color: var(--teal) !important; font-size: 12px !important; }
.nav-cta:hover { background: …!important; color: …!important; }

/* fix */
.topbar-nav .nav-cta { color: var(--teal); font-size: 12px; }
.topbar-nav .nav-cta:hover { background: rgba(46,139,122,.12); }
```

### R8 — No `prefers-reduced-motion` guard
**File:** `styles.css:312`

`.nav-card` uses `transform: translateY(-1px)` and `box-shadow` transitions. Users who have set "reduce motion" in OS accessibility preferences should not see animation:

```css
@media (prefers-reduced-motion: reduce) {
  .nav-card { transition: none; }
}
```

### R9 — Card and icon background colors are hardcoded inline
**File:** `index.html:65,81,97,115`

Four card icons and four card tags use `style="background:#eef3f7; color:#1a2e3b;"` etc. These hardcoded hex values are not connected to the CSS variable system. If the color palette changes, these won't update.

Move these to classes in the stylesheet:
```css
.card-icon-sources  { background: #eef3f7; }
.card-icon-skills   { background: #eef7f4; }
.card-icon-templates { background: #f7f3ee; }
.card-icon-datasets { background: #f0eef7; }
```

---

## Optional Polish

Minor quality improvements that are not blocking.

### P1 — Arabic-irrelevant typography properties
**File:** `styles.css:131–132,146,77`

`text-transform: uppercase`, `letter-spacing: .12em`, and `letter-spacing: -.01em` have no effect on Arabic glyphs (Arabic has no uppercase; letter-spacing disrupts Arabic ligatures). These properties only affect fallback Latin text. They won't cause visible problems but add noise:

```css
/* .hero-eyebrow — remove these two lines */
text-transform: uppercase;
letter-spacing: .12em;

/* .hero-title — remove */
letter-spacing: -.01em;

/* .brand-name — remove */
letter-spacing: .01em;
```

### P2 — Emoji `color` property has no effect
**File:** `styles.css:192`

`.search-icon { color: #9a9890; }` — emoji (🔍) ignores CSS `color`. The `font-size` and `pointer-events` on the same rule are correct and needed. The `color` line is inert; remove it.

### P3 — `cursor: pointer` redundant on `<a>` elements
**File:** `styles.css:229`

`.search-result { cursor: pointer; }` — `<a>` elements already have `cursor: pointer` by default. Remove.

### P4 — `font-size: 16px` on `html, body` is browser default
**File:** `styles.css:34`

Redundant declaration. Harmless but adds noise.

### P5 — Add `rel="noreferrer"` to external links
**File:** `index.html` (multiple)

All `target="_blank"` links already have `rel="noopener"`. Adding `noreferrer` also suppresses the `Referer` header, which is a small privacy improvement. Use `rel="noopener noreferrer"` consistently.

### P6 — Card arrow directional ambiguity in RTL
**File:** `index.html:66,82,98`

The three internal-navigation cards use `←` (left arrow). In RTL context where reading direction is right-to-left, a left-pointing arrow can mean either "forward" (in reading direction) or "back" (LTR navigation convention). The datasets external card correctly uses `↗`. Consider `→` for the internal cards or document the convention. This is a content/UX judgment call, not a technical defect.

### P7 — `<meta name="theme-color">` missing
**File:** `index.html`

```html
<meta name="theme-color" content="#1a2e3b" />
```

Sets browser chrome color on mobile. One line, matches the topbar.

### P8 — Hardcoded counts in card tags will drift
**File:** `index.html:75,91`

`"8 مصادر رسمية"` and `"7 مهارات"` are accurate now but are presentation-layer strings that have no connection to the actual source/skill file counts. As the repo grows, these will quietly become wrong. Either update them in Phase 2 or change the tag text to something timeless ("مصادر رسمية" without the number).

---

## Summary Table

| ID | Category | Area | Effort |
|----|----------|------|--------|
| C1 | Critical | RTL / Search | Small |
| C2 | Critical | Accessibility / HTML | Small |
| C3 | Critical | Accessibility / CSS | Small |
| C4 | Critical | Accessibility / Contrast | Small |
| C5 | Critical | Accessibility / Contrast | Small |
| R1 | Recommended | Dead CSS | Trivial |
| R2 | Recommended | Performance | Trivial |
| R3 | Recommended | Performance | Small |
| R4 | Recommended | Semantics / A11y | Small |
| R5 | Recommended | Semantics | Trivial |
| R6 | Recommended | Search UX / A11y | Medium |
| R7 | Recommended | CSS quality | Trivial |
| R8 | Recommended | Accessibility | Trivial |
| R9 | Recommended | Maintainability | Small |
| P1 | Optional | Typography | Trivial |
| P2 | Optional | Dead CSS | Trivial |
| P3 | Optional | Dead CSS | Trivial |
| P4 | Optional | Dead CSS | Trivial |
| P5 | Optional | Security/Privacy | Trivial |
| P6 | Optional | RTL UX | Small |
| P7 | Optional | Mobile | Trivial |
| P8 | Optional | Content drift | Small |
