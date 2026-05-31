# Design

## Theme

Dark. Void black foundation with forest green depth and aged gold as the single accent. The palette evokes a natural history archive — deep, serious, textured — not a SaaS dashboard.

**Mode:** Dark only (no light mode). The physical scene: an analyst studying specimens at 11pm, single desk lamp, focused and precise.

## Colors

All values in OKLCH.

```css
/* Backgrounds */
--bg-void:   oklch(8% 0.018 145);    /* #070e09 — page bg */
--bg-deep:   oklch(12% 0.022 145);   /* #0f1a12 — alternate sections */
--bg-card:   oklch(14% 0.025 145);   /* #142018 — specimen cards */
--bg-lift:   oklch(18% 0.030 145);   /* #1a2e1d — hover, elevated */

/* Accent */
--gold:        oklch(62% 0.085 68);  /* #b78c4e — primary accent */
--gold-bright: oklch(70% 0.095 68);  /* #d4a847 — hover accent */
--gold-dim:    oklch(62% 0.085 68 / 35%); /* borders, dividers */

/* Green */
--green:     oklch(48% 0.080 155);   /* #4a7c59 — live indicators, progress */
--green-dim: oklch(48% 0.080 155 / 20%); /* row backgrounds, hover fills */

/* Text */
--parchment:       oklch(89% 0.012 68);        /* #e8e0d0 — primary text */
--parchment-dim:   oklch(89% 0.012 68 / 55%);  /* body text */
--parchment-ghost: oklch(89% 0.012 68 / 18%);  /* ultra-muted labels */

/* Borders */
--border:       oklch(62% 0.085 68 / 18%);  /* gold-tinted structural borders */
--border-green: oklch(48% 0.080 155 / 20%); /* green row dividers */
```

**Color strategy:** Committed — aged gold carries 30-40% of all visible surface area (borders, labels, highlights, CTA background). Forest green is secondary (live states, progress bars). Void black is the canvas.

## Typography

```css
--font-display: 'Cormorant Garamond', Georgia, serif;
--font-body:    'Libre Baskerville', Georgia, serif;
--font-mono:    'JetBrains Mono', 'Fira Code', monospace;
```

Google Fonts import:
```
Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600
Libre+Baskerville:ital,wght@0,400;0,700;1,400
JetBrains+Mono:wght@400;500
```

### Type Scale

| Role | Font | Size | Weight | Notes |
|---|---|---|---|---|
| Hero display | Cormorant Garamond | clamp(3.5rem, 6vw, 6rem) | 500 | Italic for key phrase |
| Section heading | Cormorant Garamond | clamp(2.4rem, 4vw, 3.5rem) | 500 | Letter-spacing -0.02em |
| Sub-heading | Cormorant Garamond | clamp(2rem, 3.5vw, 2.8rem) | 500 | |
| Body | Libre Baskerville | 14-15px | 400 | Line-height 1.75, max 65ch |
| UI label | JetBrains Mono | 9-10px | 400-500 | Uppercase, 0.12-0.16em tracking |
| Data value | Cormorant Garamond | varies | 600 | Stats, large numbers |
| Code | JetBrains Mono | 12px | 400 | Line-height 1.8 |

**Rules:** text-wrap: balance on h1-h3. No all-caps body copy. Italic Cormorant is the signature move — use it deliberately on key phrases.

## Spacing

Base unit: 4px. Scale: 4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 112, 120px.

Section vertical padding: 112px default. Stats section: no padding (full-bleed). Hero: 100px top, 80px bottom.

Container: max-width 1240px, 40px horizontal padding. Full-bleed sections span 100% width with inner content at max-width.

## Layout

- **No three-equal-column grids.** Asymmetric always.
- Hero: `grid-template-columns: 1fr 520px`
- Stats: full-bleed 4-column `repeat(4, 1fr)`
- Collection: `2fr 1fr 1fr` mosaic, 2-row grid
- Features: `280px 1fr` (lede + stacked list)
- Pipeline: `1fr 480px`
- CTA: `1fr 320px`
- Mosaic gap technique: `gap: 2px; background: var(--border)` (border via background, not individual borders)

## Components

### Navigation (top bar)
Fixed, horizontal-rule style. Not a pill. Not centered.
- Height: 52px
- Background: `var(--bg-void)` at 88% opacity, `backdrop-filter: blur(20px)`
- Border-bottom: `1px solid var(--border)`
- Brand: Cormorant Garamond italic 19px, gold accent on "Intel"
- Links: JetBrains Mono 10px uppercase, 0.1em tracking, rule-divided
- CTA: solid gold background, void text, no border-radius (square)

### Specimen Box (Double-Bezel)
Key signature container — main cards, CTA aside.
```
border: 1px solid var(--border)
background: var(--bg-card)
padding: 28px
position: relative

::before (pseudo-element):
  position: absolute
  top: 6px; left: 6px; right: -6px; bottom: -6px
  border: 1px solid rgba(gold, 0.07)
```

### Buttons

**Primary:** Solid gold, void text, 0 border-radius (square). Font: JetBrains Mono 10px uppercase 0.12em tracking. Padding: 12px 24px. Hover: gold-bright, translateY(-1px).

**Ghost:** 1px border (--border), parchment-dim text. Same font. Hover: gold-dim border, parchment text.

**CTA arrow:** inline `→` character or `ArrowRight` icon, not inside a circle.

### Stat Cell
- Border-right: `1px solid var(--border)` (grid dividers)
- Ghost index: absolute top-right, JetBrains Mono 9px, parchment-ghost
- Number: Cormorant Garamond with `<sup>` for unit symbol in gold

### Specimen Card
- Part of mosaic (background gap technique)
- Catalogue ID: mono 9px gold uppercase
- Company name: Cormorant 20-28px 500
- Tagline: Libre Baskerville italic 12px dim
- Funding: mono 12px gold
- Tags: mono 9px, green-dim bg, border-green border
- Pin dot: 8px circle, absolute top-right (active = green, default = gold-dim)

### Feature Row
- No cards. Stacked list with bottom rule dividers.
- `grid-template-columns: 40px 1fr auto`
- Hover: background shifts to green-dim (negative margin trick for full-width)
- Arrow: right-aligned, opacity 0 by default, opacity 1 on hover

## Motion

All transitions: `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out expo). No `ease-in-out`.

- **Scroll reveals:** Framer Motion + IntersectionObserver. Staggered per-section. Default: `y: 24px → 0, opacity: 0 → 1, duration: 0.7s`.
- **Hero entrance:** Staggered fade-up sequence (badge → headline → rule → body → CTAs → specimen box), 80ms per step.
- **GSAP ScrollTrigger:** Sticky section stacks, scrubbed parallax on bg grid lines, horizontal pan on stats row.
- **Hover micro-interactions:** Feature row background (200ms), button lift translateY(-1px) (200ms), specimen card background lift (150ms).
- **Live dot pulse:** scale 1→0.7→1, opacity 1→0.4→1, 2s ease-in-out infinite.

`@media (prefers-reduced-motion: reduce)`: crossfade only (opacity transition, no transforms), no scroll-driven scrubbing.

## Absolute Bans (from spec)

- Zero em-dashes in copy
- Zero Inter as primary font
- Zero centered hero
- Zero three-equal-column grids
- Zero AI purple/blue gradients
- No pill/floating navigation
- No `ease-in-out` defaults
- No side-stripe accent borders
- No gradient text
- No glassmorphism decorative blur
