# YC Intelligence — Full Frontend Redesign Spec

**Date:** 2026-05-31
**Status:** Approved

---

## Concept: The Specimen Vault

YC startups treated as natural history specimens — each catalogued, pinned, and studied. The site is the field guide to the YC ecosystem. Every design decision evokes a research archive or natural history museum: aged gold borders, specimen boxes, catalogue numbering, botanical structure.

This is an explicit break from the "AI data platform" reflex (neural gradients, pill navs, three-equal-card grids, Inter font, centered hero).

---

## Visual Identity

### Palette

| Token | Value | Role |
|---|---|---|
| `--bg-void` | `#070e09` | Page background |
| `--bg-deep` | `#0f1a12` | Alternate section background |
| `--bg-card` | `#142018` | Specimen card backgrounds |
| `--bg-lift` | `#1a2e1d` | Hover state, elevated surfaces |
| `--gold` | `#b78c4e` | Primary accent, borders, labels |
| `--gold-bright` | `#d4a847` | Hover accent |
| `--gold-dim` | `rgba(183,140,78,0.35)` | Subtle borders, dividers |
| `--green` | `#4a7c59` | Live indicators, progress bars |
| `--parchment` | `#e8e0d0` | Primary text |
| `--parchment-dim` | `rgba(232,224,208,0.55)` | Body text, descriptions |
| `--parchment-ghost` | `rgba(232,224,208,0.18)` | Ultra-muted labels |
| `--border` | `rgba(183,140,78,0.18)` | All structural borders |
| `--border-green` | `rgba(74,124,89,0.2)` | Internal row dividers |

Zero blue. Zero purple. Zero AI gradients.

### Typography

| Role | Font | Notes |
|---|---|---|
| Display / Headings | Cormorant Garamond | Italic for drama, 500-600 weight for impact |
| Body text | Libre Baskerville | Readable serif, 14-15px body |
| Data / labels / code | JetBrains Mono | All-caps uppercase labels at 9-10px |

No Inter. No Plus Jakarta Sans as primary display font.

### Motion System

- All transitions use `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out expo)
- GSAP ScrollTrigger for scrubbed animations
- Framer Motion for React component entrances
- Staggered mask reveals on section headings
- No `ease-in-out` defaults

---

## Navigation

**Style:** Horizontal rule top bar — NOT a floating pill, NOT centered.

- Fixed position, `backdrop-filter: blur(20px)`, gold-tinted border-bottom
- Brand: `YC Intel` in Cormorant Garamond italic, gold accent on "Intel"
- Links: JetBrains Mono, 9-10px, uppercase, letter-spaced — rule-divided columns
- CTA: Solid gold background, void text, no border-radius (square)
- Mobile: Hamburger expands to full-screen overlay with large italic links

---

## Page Sections (7 total)

### Section 1 — Hero

**Layout:** Asymmetric 2-column — headline left, specimen panel right. NOT centered.

- Left: catalogue-ID badge, large italic display headline, horizontal rule, body copy, two CTAs (primary + ghost)
- Right: Double-bezel specimen box showing live top-company data with progress bars
- Background: Fine gold grid lines (opacity 2.5%), two radial green/gold glows

**Headline:** "Every YC startup, *catalogued.* Open. Free. Complete."

### Section 2 — Specimen Stats

**Layout:** Full-bleed 4-column rule-divided row (no outer container padding cut).

- Each cell: mono label, large Cormorant number, italic sub-label
- Corner catalogue index numbers (01-04) in ghost opacity
- Gold top/bottom border rules, no card backgrounds

Stats: 5,247 companies | $4.2B capital | 12,400 open roles | 847 founders

### Section 3 — The Collection

**Layout:** Asymmetric mosaic grid — 2fr + 1fr + 1fr columns, 2 rows. Zero equal-width grids.

- 2fr card spans 2 rows (featured specimen)
- Each card: catalogue ID, serif company name, italic tagline, funding label, tag pills
- Corner "pin" dot (active = green, default = gold dim)
- Hover lifts background to `--bg-lift`
- "Browse Archive" CTA in header half

### Section 4 — Intelligence Modules

**Layout:** 2-column — sticky lede left (280px), scrollable list right.

- NOT cards. Numbered list rows with bottom rule dividers.
- Hover reveals right-arrow, shifts row background to green-dim
- Six modules: 01 Directory, 02 Funding, 03 Hiring, 04 Founders, 05 LLM, 06 Pipeline

### Section 5 — The Methodology (Pipeline)

**Layout:** 2-column — text/code block left, numbered steps right.

- Left: section label, display heading, body copy, code block (dark card with mono text, gold comments)
- Right: vertical stepper with square step circles (not round), vertical line connector, mono step label + serif description

### Section 6 — Open Source CTA

**Layout:** 2-column — headline/copy/CTAs left, tech stack aside right.

- Left: italic display headline "The archive is open. Fork it.", body copy, two CTAs
- Right: double-bezel aside with tech stack list (dot + name + detail, mono)
- No centered layout

### Section 7 — Footer

Minimal catalogue-style: brand | copy | links in mono uppercase, all in one row.

---

## Component Patterns

### Double-Bezel Box

All major containers use this pattern:
```
outer border: 1px solid var(--border)
inner shadow border: pseudo-element offset 6px right+down, rgba(gold, 0.07)
```

### Specimen Card

```
background: var(--bg-card)
border: part of mosaic gap (background: var(--border))
catalogue ID: mono 9px gold uppercase
company name: Cormorant 20-28px
tagline: Libre Baskerville italic 12px dim
funding: mono 12px gold
tags: mono 9px, green-dim background
pin dot: absolute top-right
```

### Stat Cell

```
border-right: 1px var(--border)
mono label: 9px gold uppercase
number: Cormorant 2.4-3.5rem
italic sub: 12px dim
ghost index: absolute top-right mono 9px
```

---

## Hard Constraints (non-negotiable)

- Zero em-dashes in all copy
- Zero Inter as primary font
- Zero centered hero
- Zero three-equal-card grids
- Zero AI purple/blue gradients
- No rounded "pill" navigation
- No `ease-in-out` defaults on motion

---

## Implementation Plan

Following user-specified skill sequence:
1. `impeccable init` — scaffold PRODUCT.md and DESIGN.md
2. `imagegen-frontend-web` — generate one horizontal reference image per section (7 total)
3. `image-to-code` — analyze ALL images, extract typography/spacing/palette, implement faithfully
4. `design-taste-frontend` — DESIGN_VARIANCE: 9, MOTION_INTENSITY: 8, VISUAL_DENSITY: 3; pre-flight checklist as final gate
5. `high-end-visual-design` — Creative Variance Engine, Vibe Archetype, Layout Archetype; double-bezel all containers
6. `typography` — type system and font pairing
7. `gsap-framer-scroll-animation` — sticky stacks, horizontal pans, scrubbed animations
8. `impeccable animate -> delight -> overdrive`
