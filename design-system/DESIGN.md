# Gordon Smith Gallery website design system

Version 0.6.20 (draft), 2026-09-26. Built from `reference/GordonSmith-BrandGuide_sm.pdf` (17 pp.), `reference/GS-Logo-Guide.pdf` (3 pp.), the supplied logo files in `reference/GS Logos New/`, the requirements in `IMPLEMENTATION_PLAN.md` and the developer notes, and a read-only snapshot of the live store's pages, menus, collections and products (Admin API, 2026-09-25). Page numbers below (p.N) refer to the brand guide unless marked "logo guide".

Nothing here changes the live store. Every design decision is decided as of 2026-09-27 (DS-01 to DS-63); a new one starts as **Proposed** and needs Michael's approval before release (P-17); items marked **Input needed** are blocked on the gallery.

## 0. How to use this

| File | Role |
| --- | --- |
| `DESIGN.md` | Rules, rationale, component and template specs, decisions. Read before any UI work. |
| `tokens.css` | Source of truth for every value. Ships to the theme as `assets/gs-tokens.css` (`scripts/sync_theme.py`). |
| `components.css` | The components in §6. Ships as `assets/gs-components.css` (`scripts/sync_theme.py`). |
| `js/gs-nav.js`, `js/gs-forms.js` | Header navigation extras (§6.1) and form states (§6.12). Everything works without them. Ship as `assets/gs-nav.js`, `assets/gs-forms.js`. |
| `../theme/snippets/gs-*.liquid` | The snippets that enforce rules in code (§9.5). They moved into the theme when it was built; the theme is their source. |
| `templates.rules.json` | The page-template rules in §7, machine-readable. |
| `proposals/content-model.md` | Store-level proposal for page fields, exhibition entries and artwork label fields. Needs gallery approval. |
| `preview.html` | Living style guide with real titles, dates, curators, portfolios and prices from the live store (images are placeholders). Open it in a browser (it loads Mulish from Google Fonts for the preview only); update it when a component changes. |
| `logos/*.svg`, `logos/logos.json` | Web-ready logo set and its manifest (sizes, use, source file). |
| `scripts/check_contrast.py` | Checks every allowed colour pairing against WCAG 2.2 AA. |
| `scripts/lint_theme.py` | Checks a theme folder against §7 and §9: approved templates only, composition, locked settings, raw values, required snippet parameters. Tests in `scripts/tests/`. |
| `scripts/audit_fonts.py` | Reports which fonts actually render the text on live or preview pages, and flags fallbacks. |
| `scripts/build_logo_snippets.py` | Generates the inline-SVG logo snippets from `logos/`. |
| `scripts/sync_theme.py` | Copies tokens, components, scripts and logo snippets into `theme/`; `--check` reports copies that differ. |
| `fonts/Mulish-OFL.txt` | The licence for the Mulish files bundled in the theme. |

Working rules:

1. Components use semantic tokens (`--gs-color-*`, `--gs-text-*`, `--gs-space-*`, `--gs-shape-*`) only. No raw hex, px font sizes or ad hoc radii in theme code.
2. A new value goes into `tokens.css` first, with a comment saying where it came from, then into a component.
3. One template per kind of page. A page's own content lives in its fields and body, never in template section settings (§7.3).
4. Staff choose content, not design (§9.4). If a section needs a new visual option, add it here as a decision before building it.
5. When a brand source is ambiguous, follow the supplied logo files, record the call in §11, and ask the gallery.
6. Before a pull request: run the contrast check, the theme linter and its tests, and `sync_theme.py --check`; before release, run the font audit on the review theme (§10).

## 1. Principles

1. **The art leads.** The interface is paper, ink and one brand colour per view. Artworks are never cropped, corner-rounded, overlaid with text or zoomed on hover.
2. **The brand is a coloured box, black capitals and one rounded corner.** The box colour is for the brand's boxes only: logo, hero title box, primary button. Rules and tints do everything else, as the guide assigns them (p.11).
3. **Structure before styling.** Consistency comes from a small, closed set of page templates fed by structured content. Styling alone can't hold a site together if every page is its own template.
4. **Staff pick content; components pick design.** Ratios, image treatment, type, spacing and colour come from the component. Staff pick at most a programme and a surface from short named lists.
5. **Enforced, not just documented.** Where a rule can be checked or applied in code (menu duplicates, external links, fonts, template composition, locked settings), it is.
6. **Accessible by construction.** Every pairing the system allows passes WCAG 2.2 AA, checked by script. Keyboard, focus, touch, forced colours, reduced motion and working without JavaScript are part of each component spec.
7. **One system, three programmes.** Gallery, Smith Foundation and Artists for Kids pages share layouts and components; only the accent tokens change (§3.3).

## 2. Brand foundations

### 2.1 Organisations and hierarchy

- Gordon Smith Gallery of Canadian Art is the umbrella identity over Artists for Kids and The Smith Foundation (p.2). The website defaults to the Gallery brand.
- Logos are normally used together in clusters, with hierarchy set by the content (pp.3 to 4). Special use: one logo alone when others would confuse the audience, e.g. children-only programming (Artists for Kids) or adult/professional art (Gallery) (p.5).
- Public copy never says "AFK"; write "Artists for Kids" (p.2). Filenames and code may abbreviate internally, but alt text, labels and URLs visible to visitors may not.
- Messaging must make the audience clear: children only, children's work versus professional artists' work, adult audience first (p.2).

### 2.2 Palette

Each organisation has two primary and two secondary colours (pp.10 to 13). Web values are sRGB hex.

| Org | Token | Hex | PMS | Guide use | Web use |
| --- | --- | --- | --- | --- | --- |
| Gallery | `--gs-gsg-text` | `#5b757a` | 548 | Text-only logo | Eyebrows, link underlines, current-item bars, accent headings (on paper) |
| Gallery | `--gs-gsg-box` | `#89a6ab` | 5425 | Logo box | Hero title box, primary button (the brand's boxes only) |
| Gallery | `--gs-gsg-rule` | `#cdd7db` | 5455 | Rules, graphic boxes | Dividers, dropdown edge, quote rule, text selection, link hover on tint bands |
| Gallery | `--gs-gsg-tint` | `#e4eaec` | 538 | Background tints, boxes | Tinted bands (newsletter), chips, link hover fill, media placeholders |
| Foundation | `--gs-gsf-text` | `#b8bc49` | 397 | Text-only logo | Decorative only (2.03:1 on white) |
| Foundation | `--gs-gsf-box` | `#cfd65e` | 382 | Logo box | Title box and primary button on Foundation pages |
| Foundation | `--gs-gsf-rule` | `#ede658` | 395 | Rules, graphic boxes | Rules on Foundation pages (as Gallery rule) |
| Foundation | `--gs-gsf-tint` | `#ebede3` | 538 | Background tints, boxes | Tints on Foundation pages (as Gallery tint) |
| Artists for Kids | `--gs-afk-swoosh` | `#f4853d` | 151 | Swoosh | Decorative only (2.54:1 on white) |
| Artists for Kids | `--gs-afk-box` | `#fcb547` | 1365 | Logo box | Title box and primary button on Artists for Kids pages |
| Artists for Kids | `--gs-afk-rule` | `#ffdd62` | 107 | Rules, graphic boxes | Rules on Artists for Kids pages (as Gallery rule) |
| Artists for Kids | `--gs-afk-tint` | `#f6efe3` | 7499 | Background tints, boxes | Tints on Artists for Kids pages (as Gallery tint) |

System neutrals (the guide defines none): `--gs-ink #231f20` (the guide's text black), `--gs-ink-soft #625c5e` (secondary text), `--gs-ink-faint #bfb9ba` (secondary text on ink), `--gs-paper #ffffff`, `--gs-mat #f2f5f6` (artwork mat, a 50% mix of the Gallery tint with white). Logo artwork uses pure `#000000` and stays that way.

System error colour (the guide defines none, DS-22): `--gs-error #a3261b` for error text and invalid-field borders on paper and tints, `--gs-error-light #f28b82` for the same on ink. Never a fill, so it can't compete with the brand's boxes.

Two box colours differ from the brand guide on purpose; see §11.

### 2.3 Typography source

- Brand font: Soleil (TypeTogether), used for everything; headlines and subheadings ExtraBold all caps, deck paragraphs Bold, body Regular, captions Light (pp.14 to 15).
- Online alternative: Mulish, with Mulish Black replacing Soleil ExtraBold for headlines and Mulish Regular for body (p.16). Arial is the system fallback (p.16).
- Web decision: Mulish (DS-02). Soleil is available through Adobe Fonts web projects ([Adobe Fonts: Soleil](https://fonts.adobe.com/fonts/soleil)), so it is an upgrade path only if the gallery holds an Adobe licence.

### 2.4 Graphic device

Round a single corner on a box or image, 30 to 40 pt depending on box size (p.17). The logo boxes follow the same idea: the Gallery box rounds bottom-right, Foundation top-right, Artists for Kids bottom-left, at roughly 20 to 35% of the box's short side (measured from the logo artwork).

## 3. Colour system

### 3.1 Roles

Components only use these. Defaults are the Gallery programme on paper.

| Token | Default | Purpose |
| --- | --- | --- |
| `--gs-color-bg` / `--gs-color-fg` | paper / ink | Surface and body text |
| `--gs-color-fg-muted` | ink-soft | Meta text, dates, captions that need to recede |
| `--gs-color-box` | programme box colour | The brand box. Never remapped by surfaces |
| `--gs-color-accent` / `--gs-color-accent-fg` | box / ink | Primary button fill (turns ink on accent surfaces) |
| `--gs-color-accent-text` | Gallery teal | Eyebrows and accent headings. Falls back to ink where colour would fail contrast |
| `--gs-color-tint` / `--gs-color-rule` | programme tint / rule | Tinted bands, chips / dividers, dropdown edge, quote rule, selection |
| `--gs-color-hover-fill` / `--gs-color-hover-fill-fg` | tint / ink | Inline-link hover and press fill: tint on paper, rule on tint, paper on accent, box on ink |
| `--gs-color-link-line` | Gallery teal | Link underlines, current-item bars in the nav and switcher; always ≥ 3:1 on its background |
| `--gs-color-error` | error | Error text and invalid-field borders (light error on ink, ink on accent surfaces) |
| `--gs-color-control-border` | ink-soft | Inputs, secondary buttons |
| `--gs-color-focus` | ink | Focus outline |
| `--gs-color-mat` | mat | Background behind artworks in tiles |

### 3.2 Surfaces

A section's background is one of four surfaces. Each class remaps the roles so everything inside stays legible.

| Surface | Class | Background | Typical use |
| --- | --- | --- | --- |
| Paper | `.gs-surface-paper` | white | Default for all content |
| Tint | `.gs-surface-tint` | programme tint | Newsletter band, alternating feature band. Never two in a row. Primary buttons inside turn ink (DS-31) |
| Accent | `.gs-surface-accent` | programme box colour | Hero title box, one feature panel. Primary buttons inside turn ink |
| Ink | `.gs-surface-ink` | `#231f20` | Footer, rare dark band. Brand box colours become text and underline colours here |

No other backgrounds. No gradients, no photos behind body text, no rule or swoosh colours as backgrounds.

### 3.3 Programme theming

Set `data-gs-brand` once on `<body>` (from the page's `programme` field, §7.3) or on a section: `gallery` (default), `foundation`, `artists-for-kids`. It swaps the box, tint, rule and accent-text tokens. Foundation and Artists for Kids have no colour that passes text contrast on white, so their eyebrows and link underlines use ink, and their colour lives in the title box, primary buttons, tinted bands and rules.

Use a programme scope when the page belongs to that programme (Artists for Kids and Smith Foundation sections of the site). Exhibitions, Shop, About and Visit stay Gallery.

### 3.4 Contrast rules

`python3 design-system/scripts/check_contrast.py` checks 85 required pairings (every programme on every surface, including link hover fills, strong chips and error text) and exits non-zero if any fail. Current result: 85/85 pass. Lowest passing values:

| Pairing | Ratio | Rule |
| --- | --- | --- |
| Gallery teal on paper | 4.92 | OK for any text size |
| Gallery teal on Gallery tint | 4.05 | Large text (h3 and up) and underlines only |
| Ink on Gallery box | 6.29 | Buttons, title box, link hover on ink |
| Error on Gallery tint | 6.06 | Error text on tinted bands |
| Ink-soft on Gallery tint | 5.38 | Muted text on tint |

Forbidden, with the reason:

| Pairing | Ratio |
| --- | --- |
| Gallery box `#89a6ab` as text on white, or white text on it | 2.59 |
| Foundation green `#b8bc49` as text on white | 2.03 |
| Artists for Kids orange `#f4853d` as text on white, or white text on it | 2.54 |
| Gallery teal `#5b757a` as text on ink | 3.31 |
| Error `#a3261b` as text on the Gallery box (accent surfaces use ink for errors) | 2.84 |
| Error `#a3261b` as text on ink (ink surfaces use `#f28b82`) | 2.21 |

The brand guide sets coloured headlines and orange deck text (p.15). That works in print but fails on screen, so on the web those colours move to fills and text stays ink.

## 4. Typography

### 4.1 Loading (DS-02)

- Family stack: `"Mulish", Arial, "Helvetica Neue", Helvetica, sans-serif`. Arial is the brand-sanctioned fallback.
- Weights needed: 300, 400, 700, 800, 900, plus 400 italic for artwork titles.
- Bundled with the theme, not a font picker, because fonts aren't a staff choice: the Mulish variable woff2 files (weights 200 to 1000, latin and latin-ext subsets, normal and italic; SIL OFL 1.1, `fonts/Mulish-OFL.txt`) in `theme/assets/`, loaded by `snippets/gs-fonts.liquid` with `font-display: swap`; the roman latin file is preloaded. No text may fall back to Assistant, the old theme's font.
- Coverage: Mulish has no glyphs for some characters in the Squamish, Tsleil-Waututh and Musqueam names in the land acknowledgement (ʔ, ɬ, θ and some combining marks), so those render in Arial (L-06, Q11).

### 4.2 Scale

Sizes are fluid between 390 px and 1440 px viewports (`clamp()`), so there are no per-breakpoint font overrides.

| Role | Token | Size (px) | Weight | Case | Leading | Tracking | Use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Display | `--gs-text-display` | 44 to 96 | 900 | Caps | 0.98 | 0 | Home hero only |
| H1 | `--gs-text-h1` | 36 to 64 | 900 | Caps | 1.06 | 0 | Page title, hero title (both fit their box, §4.3) |
| H2 | `--gs-text-h2` | 28 to 44 | 900 | Caps | 1.06 | 0 | Section titles |
| H3 | `--gs-text-h3` | 22 to 28 | 900 | Caps | 1.06 | 0 | Card titles, sub-sections |
| H4 / subheading | `--gs-text-h4` | 17 to 19 | 900 | Caps | 1.2 | 0.03em | Minor headings in text, compact card titles |
| Deck | `--gs-text-deck` | 19 to 24 | 700 | Sentence | 1.38 | 0 | Intro paragraph, max 42ch |
| Body | `--gs-text-body` | 16 to 18 | 400 | Sentence | 1.6 | 0 | Running text, max 68ch |
| Small / meta | `--gs-text-small` | 15 | 400 | Sentence | 1.5 | 0 | Dates, artist lists, prices |
| Caption | `--gs-text-caption` | 14 to 15 | 300 | Sentence | 1.45 | 0 | Image captions, credits |
| Label | `--gs-text-label` | 13 to 14 | 800 (buttons 900) | Caps | 1.2 | 0.08em | Eyebrows, buttons, chips, standalone links, utility links |
| Nav | `--gs-text-nav` | 15 | 800 | Caps | 1.2 | 0.05em | Main navigation, switchers |

### 4.3 Rules

- Headings are Mulish Black in capitals (p.15). Use real heading elements in order; style follows the element or a `gs-` class, never a size choice by staff.
- Capitals stay for labels too (DS-17). The brand guide sets headlines and subheadings in caps (p.15) and labels its own pages in small tracked caps (p.11: "USE FOR BACKGROUND LOGO BOX", "PRIMARY"), so caps labels are the brand's voice here, not a template habit. What changes is how many there are: a label only appears when it carries information (DS-18).
- Titles fit their box. Hero and page-header titles size to the width of their box, so the longest word always fits on a 320 px phone and at 200% zoom: `snippets/gs-fit.liquid` passes the title's longest word length as `--gs-fit-chars`, and the CSS divides the box width by it (0.74 em per capital, the widest average in Mulish Black), capped at the H1 or display size. Short titles still reach full size. As a last resort a word breaks instead of overflowing.
- The home hero's own heading (shown when no exhibition is on) keeps its words together in two balanced lines: "Gordon Smith Gallery" reads GORDON SMITH / GALLERY at every width, sized to the longer line (`snippets/gs-fit-lines.liquid`, DS-33). A heading whose longer line would pass 14 letters wraps normally instead, so it never shrinks below about H1 size on desktop.
- Exception: artwork titles are italic, sentence case, regular weight (museum-label convention), e.g. artist name in bold, then *Title*, year. The italics come from markup (`<cite>`), never from Unicode "italic" letters typed into titles (§7.1, proposal part 3).
- Deck paragraphs are Bold; emphasis in body is Bold, not colour or underline.
- Captions are Light but stay full ink colour; Light plus grey reads too faint.
- Kerning stays at the browser default (`font-kerning: normal`), as the plan requires. Tracking on small capitals (labels, nav, subheadings) is a system choice; the guide specifies none.
- No body text in capitals, no justified text, no text over images.
- Fallback guards: form controls inherit the site font, pasted inline fonts and colours in rich text are neutralised, and third-party embeds sit in `.gs-embed`, which forces the site font (§6.9, §6.11).

## 5. Space, layout, shape, motion

### 5.1 Spacing

4 px base: `--gs-space-1` to `--gs-space-10` = 4, 8, 12, 16, 24, 32, 48, 64, 96, 128. Fluid layout spacing:

| Token | Range | Use |
| --- | --- | --- |
| `--gs-gutter` | 16 to 48 | Page side padding and grid column gap |
| `--gs-section-space` | 48 to 112 | Vertical padding of every section |
| `--gs-stack-lg` | 32 to 64 | Section heading block to its content |
| `--gs-hero-overlap` | 48 to 96 | How far the hero title box overlaps the image |

Rhythm inside components: eyebrow to heading 12, heading to deck 16, text to actions 24 to 32. Two paper sections in a row share one gap: paper sections are spaced with margins, which collapse, even across Shopify's section wrappers; bands (tint, ink, accent) pad inside their colour. A page header or switcher (`.gs-lead-in`) sets its own gap to what follows.

### 5.2 Layout and breakpoints

- Containers: wide 1440 (heroes, image grids), content 1200 (cards, header, footer), prose 720.
- Breakpoints: 750 (md), 990 (lg), 1200 (xl), in `components.css` (the new theme has no others). The header is the one exception to the defaults: the logo reaches desktop size at 990, but the inline navigation needs room for six or seven section labels, so it starts at 1200 and the Menu drawer is used below that.
- Grids: cards 1 / 2 / 3 columns at base / 750 / 990. Artwork tiles and portfolio cards 2 / 3 / 4 at base / 750 / 1200. Installation views 1 / 2 / 3 at base / 750 / 1200.
- Media ratios (components choose; staff never do): hero 4:5 / 4:3 / 21:9, card 4:3, installation view 3:2, artwork tile 1:1, portrait 4:5.

### 5.3 Shape (DS-03)

- One rounded corner, **bottom-right, everywhere in the UI**, matching the Gallery logo box. Programme logos keep their own corners because they are artwork.
- Sizes by element: `--gs-shape-sm` 12 px (buttons, inputs, chips), `--gs-shape-md` 24 px (cards, images in text, dropdowns), `--gs-shape-lg` 24 to 48 px (hero media, title box, bands).
- Never on artwork. In artwork tiles and the artwork hero the corner belongs to the mat; the artwork sits inside it untouched.
- No fully rounded pills, no four-corner radii, no borders plus radius on photos. The one exception is a hairline inside a photo's edge at 10% ink (10% paper on ink), which keeps a photo with a white wall or sky from melting into the paper; it isn't seen as a frame (`--gs-color-media-edge`, DS-55).

### 5.4 Motion and depth

- Durations 120 / 200 / 320 ms with `cubic-bezier(0.2, 0, 0, 1)`, and 160 ms with a strong ease-out, `cubic-bezier(0.23, 1, 0.32, 1)`, for a button press (DS-55). All set to 0 under `prefers-reduced-motion`.
- Motion only answers a person's action, and stays out of the art's way:
  - 120 ms: link hover fill fades in (a colour fade, not a sweep), the "more" arrow nudges and its underline darkens together, button colours invert.
  - 120 ms: a dropdown or the Menu drawer fades in and drops 4 px when opened. Closing is instant.
  - 200 ms: the section chevron turns.
  - 160 ms: a pressed button shrinks to 97%, so it gives a little under the finger or the click, and springs back on release (`--gs-duration-press`, `--gs-ease-press`, DS-55). Only with `prefers-reduced-motion: no-preference`.
  - Nothing moves on its own: no parallax, no image zoom, no scroll-triggered reveals, no loading spinners (a submitting button says "Signing up" instead).
- Hover effects apply only with a mouse or trackpad (`@media (hover: hover) and (pointer: fine)`), so a tap never leaves a link filled or a button inverted. `:active` gives touch the same feedback while the finger is down.
- Flat: the only shadow is under dropdown panels and the Menu drawer.
- Slideshows do not autoplay. If the gallery insists on autoplay, it needs a visible pause control plus previous/next buttons (plan requirement).

## 6. Components

Each spec lists anatomy, tokens, states and staff controls. Class names are from `components.css`; `preview.html` shows each one.

### 6.1 Header and navigation (NAV-01 to 04, TYPE-04, ACCESS-02)

- **Logo (DS-07, DS-47):** the page's programme decides the logo: Artists for Kids pages carry `artists-for-kids-full-colour-box`, Smith Foundation pages `foundation-simple-colour-box` (72 px tall on phones, its minimum), every other page `gallery-simple-stacked-colour-box`. Each hangs flush from the top-left corner of the page, rounded corner facing into the page, 64 px tall on mobile and 96 px from 990 px. It is the brand's primary lockup and the mark on the brand guide cover, and the solid box carries more presence than type alone. Judge it against the current header (logo width setting 250 px) in a mockup before approving. Rendered inline through `snippets/gs-logo.liquid`; the link's accessible name is "Gordon Smith Gallery, home".
- **Markup:** `snippets/gs-header.liquid`. The main menu renders twice, once in the Menu drawer and once in the desktop bar; CSS shows one, so assistive tech only ever finds one "Main" navigation. In each, the order in the markup matches the order on screen, so focus order follows what people see.
- **Main nav model (DS-11):** every top-level item is one of two things, never both.
  - **A section with pages under it** is a `<details>` whose `<summary>` is the section's button (label plus chevron). Clicking, tapping, Enter or Space opens its dropdown; the button never navigates. The section's main page is the first link inside the dropdown, with its own label (for example On now, Public programs, About the Foundation, Limited editions).
  - **A section with no pages under it** is a plain link.
  - Caps, 800 weight, 15 px. Current section: 3 px underline in `--gs-color-link-line` on its button or link, ", current section" for screen readers, and `aria-current="page"` on the current link inside the dropdown.
- **Works without JavaScript (DS-19):** the drawer and every dropdown are native `<details>`, so every link is reachable even if the script fails or loads late. Dropdowns in one menu share a `name`, so opening one closes the others without script. `js/gs-nav.js` adds only what `<details>` can't: Escape closes the open dropdown and returns focus to its button (pressed again, it closes the drawer and returns focus to Menu); a click outside the header closes everything; on the desktop bar, focus leaving a dropdown closes it; choosing a link closes the drawer; crossing 1200 px closes everything; and one-open for older browsers without `<details name>`.
- **Behaviour:** no hover opening, so nothing opens or closes by accident and mouse, touch and keyboard behave identically. One dropdown open at a time, in the bar and in the drawer. Normal list and link semantics, no ARIA menu roles (the W3C disclosure navigation pattern). Tested in a browser with and without JavaScript: mouse, keyboard, touch, drawer and overflow at 320 to 1440 px and at 200% zoom.
- **Dropdown panel:** paper, 4 px top edge in the rule colour, `--gs-shape-md`, one soft shadow. Items are body size, regular weight, 40 px tall (44 px on touch screens). Opens with a 120 ms fade and 4 px drop. The last two sections' dropdowns open leftwards so they never run off the right edge.
- **Desktop (1200 px and up):** utility links sit in a small row above the main nav, so the nav keeps one line.
- **Below 1200 px:** a Menu button (label plus icon, 44 px tall) opens a drawer that lies over the page under the header and scrolls inside itself if it is taller than the screen. Each section button becomes a full-width row with the chevron on the right and opens its pages in place; the current section starts open, so people see where they are. Every row and link is 44 px tall. Utility links follow the nav.
- **Not sticky (DS-23):** the header scrolls away with the page on every screen size. A fixed header would permanently cover part of a phone screen the art needs; the Menu button is one scroll up.
- **Utility links** (label style): Contact, Search, Cart. Contact is always visible (desktop utility row, mobile drawer, footer). No Newsletter link (DS-56): the sign-up band is at the foot of every page.
- **Enforced in `snippets/gs-nav.liquid` and `gs-url.liquid`:**
  - Items with children render as section buttons, items without as links; staff can't produce the old mixed behaviour.
  - If a parent's link points to a page that isn't in its dropdown, the theme editor shows a warning, because that page would no longer be reachable from the menu. The simple rule for staff: point each parent at its first dropdown item.
  - A dropdown item labelled exactly like its section gets a warning to give it its own label.
  - Store URLs typed as absolute links are made relative (the live menu sends 2025 Fall Portfolio to the myshopify domain).
  - Any other absolute URL gets the external cue: a north-east arrow and visually hidden "(external site)", same tab by default. This covers the Artists for Kids site automatically, with no class for staff to remember.
  - A plain link with no destination ("#") gets a warning. Only two levels render.
- **What this means for the live menu** (store-level change; the gallery approves labels through the menu map):
  - Exhibitions: On now first, then Upcoming (currently missing) and Past. Keep the Exhibitions overview page as a secondary link (for example from On now), not in the dropdown.
  - Programs: Public programs first; it's no longer a duplicate, because the section itself isn't a link.
  - Smith Foundation: rename the first item from "Smith Foundation" to its own label, such as "About the Foundation".
  - About: decide whether About and About Us are one page; that page goes first.
  - Shop: Limited editions (the Shop landing page) first, instead of Shopify's /collections list; then portfolios and Artists (Our Story left the Shop, P-25). Fix the absolute 2025 Fall Portfolio link.
  - Artists for Kids: stays a plain link unless the external-site links move into the menu; then it becomes a section with "About Artists for Kids" first.

### 6.2 Links and calls to action (TYPE-05)

| Element | Class | Rest | Hover (mouse) and press (touch) | Focus | Notes |
| --- | --- | --- | --- | --- | --- |
| Inline link | `.gs-link`, any `a` in `.gs-prose` | Ink text, 2 px underline in link-line colour, 0.22em offset | The surface's hover fill fades in behind the words (120 ms); underline takes the text colour | 3 px outline, 3 px offset | Keeps the underline (DS-06). Fill is a tint, never the box colour (DS-21) |
| Standalone link | `.gs-cta-link` | Caps label, underlined in link-line colour | Underline darkens to the text colour | Outline | "About the exhibition", "Plan your visit". No arrow (DS-20) |
| "More" link | `.gs-cta-link.gs-cta-link--more` | As above, plus an arrow | Arrow nudges right as the underline darkens, same timing | Outline | Only for links to more of the same list: "All past exhibitions" |
| Primary button | `.gs-button` | Box colour, ink caps 900, 48 px tall, bottom-right corner. Ink with paper text on accent and tint surfaces, where the box colour would disappear into the background (DS-31) | Inverts to the surface's text colour with background-coloured text; on accent and tint, paper with ink text. Pressed, it shrinks to 97% (§5.4, DS-55) | Outline | One per view where possible. The brand's box in small |
| Secondary button | `.gs-button--secondary` | Transparent, 2 px ink border | Fills ink | Outline | Beside a primary, or on busy pages |
| Disabled | `button[disabled]`, `[aria-disabled="true"]` | 45% opacity, not-allowed cursor | None | Outline (`aria-disabled` stays focusable) | A link is never disabled: remove it. Say why nearby ("Sold out") |
| Submitting | `.gs-button[aria-busy="true"]` | Colours unchanged; label says what's happening ("Signing up"); progress cursor | None | Outline | The form ignores repeat submits while busy |

A link to a PDF says "(PDF)" after its label, so nobody opens a large file by surprise (`gs-link`). A way to get in touch or to give is something to act on, not only to read: an email address or phone number that a page offers as the way to act gets a link (`mailto:`, `tel:`) with a verb for its label ("Email us", "Call us"), and the page's last section is how to act (DS-58, DS-60). Hover styles apply only with a mouse or trackpad; on touch, `:active` shows the same change while pressed and nothing sticks after the tap (§5.4). On touch screens standalone links, footer, utility and dropdown links grow to 44 px targets. Visited links look the same as unvisited. One size of button only. Button labels are 1 to 3 words, verb first; the words for an action stay the same through the flow ("Sign up", "Signing up", "You're signed up").

### 6.3 Hero (IMG-01, IMG-02, IMG-04, SHOP-04, DS-08, DS-12)

Two variants, chosen by what the image is, never by taste. With page fields (§7.3) the choice comes from `hero_is_artwork`.

- **Photo hero** (`.gs-hero`): installation views, events, people. Media ratio 4:5 below 750, 4:3 to 989, 21:9 from 990, capped at 80% of viewport height, `--gs-shape-lg`, cropped around the editor's focal point. The title box (`.gs-hero__box.gs-surface-accent`: status chip and dates on their own line for an exhibition, or an optional eyebrow such as a programme name; H1, or display on Home; optional deck; up to two actions) sits under the image and overlaps it by exactly `--gs-hero-overlap` (48 to 96 px), inset from the left on wide screens. The covered area is therefore a known strip along the bottom-left edge: keep faces and key details out of it when setting the focal point. The title sizes to the box (§4.3), so a long word like CONVERSATION fits on a phone. Without an image the box stands alone and doesn't overlap anything.
- **Artwork hero** (`.gs-hero--artwork`): the image is an artwork. The work shows whole on the mat, never cropped, rounded or overlapped; the title box sits beside it from 990 px (7:5 columns) and below it on smaller screens. The mat takes the work's own shape, kept between 4:5 and 4:3 (`--gs-art-ratio`, set from the image), so a wide print doesn't float in a square of empty mat. Below 990 px the caption sits straight under the work it names, before the title box (DS-55).
- **Home leads with the exhibition on now (DS-30):** the home hero shows the most recently opened exhibition that's on, from its entry: key image, status chip and dates, title at H1 size, and "About the exhibition". The section's own image and heading show only when nothing is on. So the home page follows the programme without anyone updating it, and the art leads. The page's H1 stays the gallery's name, visually hidden while an exhibition leads. When the exhibition has installation views, the first one leads as a photo hero, the art in the room, with the installation credit as its caption; until there are some, the key image (DS-54).
- Title box width: `min(40rem, 58%)` from 990 px, `min(48rem, 60%)` from 1200 px, so a four-word title breaks into two lines. Its left edge lines up with the content column (1200 wide) and never sits closer than 48 px to the image's edge.
- Same position and treatment on every page type that has a hero (Home, exhibition, programme, Shop landing). A page without a strong image uses the page header (§6.6) instead of a weak hero.
- Staff controls: image (with focal point), whether it is an artwork, heading, deck, up to two buttons, and an eyebrow on non-exhibition pages. Exhibition status and dates come from the exhibition's data, not typed text. No colour, alignment, height or overlay options.
- The hero image loads first: `gs-media` with `preset: 'hero'` loads it eagerly with high fetch priority.
- Alt text comes from the image's own, set in Files. Without one the image is decorative (`alt=""`), never the page or exhibition title again: the title comes right after it, so a screen reader would hear the same words twice and learn nothing about the picture (DS-58).
- Slideshow variant: same frame; no autoplay by default; visible previous/next and pause if any movement.

### 6.4 Media (IMG-02, IMG-03, DS-05)

Two modes, chosen by the component. Sections render images only through `snippets/gs-media.liquid`, with a `preset` for where the image sits (`hero`, `card`, `tile`, `gallery`, `full`) that sets the `sizes` attribute and loading, so phones don't download desktop widths. The theme linter rejects a `gs-media` call without a preset or explicit `sizes`. A blank image renders nothing, so no empty tinted box is left in a card or gallery; the theme editor shows a warning where it's missing.

| Mode | Class | For | Behaviour |
| --- | --- | --- | --- |
| Photo | `.gs-media--photo` | Installation views, events, people, programme photos | Fills a fixed ratio with `object-fit: cover`, honours the editor's focal point. A hairline inside the edge (`--gs-color-media-edge`, §5.3) keeps a light photo's edge on paper (DS-55) |
| Artwork | `.gs-media--artwork` | Any image that is an artwork (products, artwork features, artwork hero) | Whole image, `object-fit: contain`, 8% inset on the mat colour; never cropped, rounded or overlaid. Position is pinned to the centre so a focal point set for another use of the same file can't shift it |

- Focal points: `image_tag` writes the editor's focal point as inline `object-position` ([Shopify: image_tag](https://shopify.dev/docs/api/liquid/filters/image_tag)); the CSS fallback is `--gs-focal`. Verify in the review theme before closing IMG-03.
- Ratios come from the component (§5.2). Use a separate mobile image only when one focal point cannot serve both crops.
- Alt text is required; artwork alt follows "Artist, Title, year" plus a short visual description where useful.

### 6.5 Cards

- **Exhibition / programme card** (`.gs-card`): photo media 4:3 with `--gs-shape-md`; status chip only where a list mixes statuses (Home), not on a list that is all one status; H3 title in caps; dates, then curators or artists, each on its own line in muted small. On a grid card the curator credit stops at two lines, so cards in a row stay even; wide cards and the exhibition page show it whole. The title link is stretched over the whole card; the card shows the focus ring where the browser supports `:has()`, otherwise the link keeps its own. Hover (mouse) and press (touch) underline the title; images do not zoom.
- **Card groups** (`.gs-grid--cards`): one, two, then three across. A group of four or eight (`.gs-grid--fours`) goes two, then four, across instead, so no card sits alone on a row (DS-44). Any other count that would leave a short last row gives the spare room to its first cards (DS-52): at three across, five (or eleven) cards start with two wider ones (`.gs-grid--lead`); at two across, an odd count starts with one wide card, its image beside its text (`.gs-grid--odd`). Card text wraps with `text-wrap: pretty`, so no single word sits alone on its last line. Each group can be linked to by its handle (`/pages/donate#donate-ways-to-give`), so a page's call to action can jump to it (DS-53). A first group without a heading continues the text before it ("Current volunteer roles include the following:"), so it follows that text at `--gs-space-7` instead of a section's space; a group with a heading starts a new part of the page at the usual space (`.gs-section--continues`, DS-58).
- **Logo card** (`.gs-card--logo`, DS-50): a card about one of the three organisations, chosen by the card's Logo field. The organisation's full logo (§8.2) is the card's heading, and the title is there for screen readers only, so the name isn't said twice on screen. The card takes the organisation's rule and link colours (`data-gs-brand`, §3.3). A group whose cards all have logos (`.gs-grid--logos`) is one organisation per row: the logo beside its text from 750 px, above it on phones, each row under a rule in the organisation's colour. Logos are 112 px tall (the Foundation's wider lockup 88 px), 144 and 104 px from 990 px; the gap to the text is at least the logo's clear space (§8.3). Staff don't choose it; the Logo field does.
- **Compact card** (`.gs-card--compact`): same anatomy with an H4-size title; used for portfolio navigation and "More exhibitions" rows.
- **Artwork tile** (`.gs-artwork-tile`): in grids of two, then three across, never four, so each work shows large (DS-46); artwork media 1:1 on the mat; artist (bold), *title* (italic) and year, medium and edition (muted small), price (bold small). No badges over the image; sold-out or edition status goes in the text.
- **Status chip** (`.gs-chip`): On now, Upcoming, Past, Sold out. Tint background; the single most important state (On now) is `.gs-chip--strong`, a solid chip in the surface's text colour (ink on paper, paper on ink). Text always states the status; colour is never the only signal. Exhibition status is computed from dates, never typed (`snippets/gs-exhibition-status.liquid`).
- **Status and dates** (`.gs-status`): the chip, then the dates on their own line in bold small (`.gs-status__dates`), written out by `snippets/gs-date-range.liquid`: "September 25, 2026 to February 20, 2027"; "April 12 to June 22, 2024" when both dates share a year; "From September 25, 2026" without an end date. Never a joined string such as "On now · Until February" (DS-18).

### 6.6 Page and section headers

- Page header (`.gs-page-head`): H1 (max 20ch, sized to the box, §4.3), optional deck. Used on pages without a hero.
- Section header (`.gs-section-head`): H2, optional "more" link aligned right on wide screens ("All past exhibitions").
- Eyebrows (DS-18): only when the label tells the reader something the heading doesn't: the programme or organisation a page belongs to ("Artists for Kids"), a season. Never a generic section name ("Explore", "Featured") and never a status or date, which use `.gs-status`. Most headings have none.

### 6.7 Sibling navigation (EXH-02, SHOP-02, DS-13)

`.gs-switcher` moves sideways between pages of the same kind without the main menu. Real links with `aria-current="page"`, not ARIA tabs, because each item is its own page.

- Exhibitions: On now / Upcoming / Past, with counts from the exhibition data. Placed directly under the page header on the three exhibition list pages, including Past Exhibitions. No other page shows it; there is no overview page (P-20).
- Portfolios: one link per portfolio plus All editions, under the collection header on every portfolio page.
- Label style, 44 px targets, 4 px underline in the link-line colour on the current item (3:1 or more on every surface; the box colour isn't). Items wrap onto a second row on narrow screens, so every portfolio stays visible; nothing scrolls sideways out of view.
- Counts show only when they're above zero. A list with nothing in it shows the empty state (§6.12), not a heading over nothing.

### 6.8 Image gallery

`.gs-gallery` is a list of figures with captions always visible. No lightbox in v1 (Q8).

- Installation views (`.gs-gallery--installation`): photo mode 3:2, `--gs-shape-md`, caption in caption style ("Installation view, Exhibition, year. Photo: Name").
- Works (`.gs-gallery--works`): two, then three across, never more (DS-46); artwork mode on the mat with a museum label (`.gs-label-block`: artist bold, *title* italic and year, medium and credit light). Phase 2: needs artwork data (proposal part 2).

### 6.9 Newsletter band (ACCESS-01)

A reusable section placed above the footer on every template: tint surface, H3, one sentence, email field plus primary button, consent text in caption style. Wording, destination and consent copy come from the gallery (Input needed). Mailchimp integration method per the plan's audit; if an embedded form is used, wrap it in `.gs-embed` so it takes the site font and field style.

States (§6.12): a missing or malformed address shows "Enter an email address like name@example.com." under the row, linked to the field; while sending, the button reads "Signing up"; when done, "You're signed up for the newsletter." replaces the error in a `role="status"` line. Final wording follows the gallery's copy.

### 6.10 Footer (ACCESS-02, ACCESS-03)

Ink surface, in three rows (DS-57):

1. **Who and where:** the three white logos, the Gallery first (interim until the cluster artwork arrives, Q1), then the land acknowledgement, which names the organisations. Side by side from 990 px, in two equal columns; stacked below that. The logos are set at one letter size, the Foundation's at its 72 px minimum (`--gs-footer-logo-x`, 23 px lowercase letters), so the Gallery is 121 px tall and Artists for Kids 112 px; and on one baseline, so "Gallery", "Kids" and "Foundation" sit on the same line, the Gallery's y and the Artists for Kids brush hanging below it. Each logo's letter height and reach below its last line are measured from its file (logo metrics in `components.css`). The row fits beside the acknowledgement from about 1250 px; narrower, the Foundation takes a second row (DS-59).
2. **Columns**, each headed by a label-style heading: Visit (2121 Lonsdale Avenue, North Vancouver, V7M 2K6; hours), Contact (email, phone, contact form), Explore (key links), Follow (social links with visible names, not icons alone). Four across from 1200 px, two across below that; on phones Visit takes the first row alone. The positions are fixed, so Follow fills the fourth column when the gallery adds its social links and nothing else moves. The two rows share one column gap, so from 990 px a column starts where the acknowledgement does.
3. **Legal line** in muted caption: the copyright on its own line, the policy and legal links together under it, so no link is left alone on a line.

The rows are grouped by space, not rules. Links underline in the box colour on hover and press; 44 px targets on touch screens.

### 6.11 Rich text

`.gs-prose` wraps staff-entered text: 68ch measure, 1em paragraph spacing, headings inside use the scale above, blockquote with a 4 px rule in the rule colour and deck styling, images in text get `--gs-shape-md`. A YouTube or Vimeo video embedded in the text fills its column at its own shape: the embed code's width and height set it (`--gs-video-ratio`, written by `snippets/gs-page-text.liquid`; `--gs-ratio-video`, 16:9, when the code gives none), so a square or portrait video isn't boxed with bars down its sides (DS-53). The tint shows while the player loads. As a figure with a caption it sits beside its text like a picture. Staff formatting is limited to headings, bold, italic, lists, links, quotes and embedded video. A picture with a caption is a `<figure>` with a `<figcaption>` in the caption style; a photo gets the rounded corner, and an artwork (`<figure class="gs-figure--artwork">`) sits whole on the mat, which takes the corner (DS-05), as with the Artists for Kids page's Bill Reid print. A quote with who said it is a figure too (`<figure class="gs-quote">`: the words in a `<blockquote>`, the name in the `<figcaption>`), so it sits beside the text it belongs to as a pull quote from 990 px, with the blockquote's rule in the page's rule colour (DS-53). A list whose items each open with a bold phrase (a line break after it) can be a list of points, `<ul class="gs-points">`: no bullets, each point under a 2 px rule in the page's rule colour, like a text card, its phrase as a small heading (H4 style, caps), so a list of long points reads as separate things. A list of example amounts, `<ul class="gs-amounts">` with each amount in bold ("<strong>$150</strong> can help bring a classroom…"), is a row of tint tiles from 750 px, each amount at H2 size and its text in the small size. Both keep the staff's own markup; only the class is added (DS-60, Donate).

**Text with pictures** (`.gs-text-media`, DS-51): when page text has figures, it is split at its H2 headings, and each part's figures sit beside its paragraphs from 990 px (text in 7 columns, pictures in 5), aligned to the part's first line. On smaller screens they follow the part's text. So a picture sits next to what it belongs to instead of breaking the reading column, and the empty side of a wide screen is used. Staff don't choose it; a figure in the text does. In the headed sections a programme page shows after its programmes, each H2 is a section heading (`.gs-section-head`, H2 size) above its text and pictures, level with the programmes' heading, and the sections are spaced as page sections. Inline fonts, sizes and colours pasted from Word or email are neutralised.

Headings in page text sit one step below the page's section headings: `h2` at the H3 size, `h3` and `h4` at the H4 size (DS-40). They organise a page's reading; they don't open a new part of the page. A list of twelve or more items (the Artists page's names) flows into two columns, three from 990 px, without bullets (DS-45). A heading at the very start of the text that only repeats the page title isn't shown (DS-41).

Until release, the page text can come from a staged field instead of the live page text (DS-39). `snippets/gs-page-text.liquid` resolves both, for the page text section and the Contact page.

### 6.12 States: empty, error, submitting, done

Every list, form and image has a defined state for when things aren't there or go wrong. `preview.html` shows each one.

| State | Pattern | Default wording (the gallery can change it) |
| --- | --- | --- |
| No exhibitions on now | `.gs-empty`: bold deck-size sentence, then a standalone link | "No exhibitions are on right now." / "See what's coming up" |
| No upcoming exhibitions | `.gs-empty` | "No upcoming exhibitions are announced yet." / "See what's on now" |
| Empty portfolio | `.gs-empty` | "This portfolio has no works available right now." / "See all limited editions" |
| Gallery with no images | Section not rendered at all | |
| Missing image | Nothing rendered; theme-editor warning only | |
| Zero count in a switcher | Count hidden | |
| Field error | Field border thickens in `--gs-color-error` (`aria-invalid="true"`); `.gs-field__error` under the field or form row, linked with `aria-describedby`, with an icon; focus moves to the field | Says what to do: "Enter an email address like name@example.com." |
| Submitting | Button keeps its colours, `aria-busy="true"`, label in the present tense | "Signing up" |
| Done | `.gs-form-status` with a check icon, `role="status"` | "You're signed up for the newsletter." |
| Unavailable | `button[disabled]` with the reason as text beside it | "Add to cart" disabled, "Sold out" |

Errors state what happened and how to fix it, without apology. Empty states always point somewhere useful. Colour is never the only signal: the icon and the words carry the error, including in forced-colours mode, where every icon is repainted in the system text colour.

### 6.13 Components added in the build (0.5)

Specified here because the build needed them; each follows the rules above and is in `components.css`.

| Component | Class | Use |
| --- | --- | --- |
| Feature panel | `.gs-feature` | One box, text beside an image, on the Home and Shop landing pages. The box takes the surface (tint, accent once per page, or ink) inside a paper section, so it reads as the brand's box. A programme setting gives it that programme's colours (Artists for Kids, the Foundation), and a second, plain link can sit beside its button (DS-54). On a tint or ink box the programme's logo leads the text, 72 px tall (`--gs-feature-logo-h`): the colour box logo on tint, the white one on ink; not on the programme's own box colour (accent), where a boxed logo mustn't sit (§8.3). From 990 px a page's second panel with an image puts it on the right, so image-led rows alternate (DS-55). Renders nothing when empty |
| Details list | `.gs-details` | Facts: label over value, each under a rule, in one to three columns; long lists of names run in columns across the full width. `.gs-details--stack` keeps one column from 990 px, for a side column |
| Wide card | `.gs-card--wide` | On now and Upcoming (DS-34): image (7 columns) beside dates, H2 title, curator, the start of the summary and an "About the exhibition" cue. The whole card is one link; the cue is decoration, not a second link. Stacks below 750 px |
| About the exhibition | `.gs-about` | The exhibition page's text (DS-35): summary as deck, text and credits in 7 columns, the facts in 4 beside them from 990 px. Below that the facts come straight after the summary. Credits sit under a rule with a label heading |
| Events | `.gs-events`, `.gs-event` | Title, time (`gs-time-range`: "Thursday, October 8, 2026, 2:30 to 4 PM"), place, a sentence, tickets. With an image, the image sits beside the text from 750 px. On a programme page, an event titled like the page (a run of drop-ins) leads with its date and time instead (DS-36) |
| People grid | `.gs-grid--people` | A card group whose images are all portraits (a board): 4:5 frames, compact titles, two, three and four across (DS-37). The images decide, not a setting |
| Text card | `.gs-card--text` | A card without an image: starts under a rule. From card entries (content model part 4) |
| Artwork detail | `.gs-artwork`, `.gs-artwork-label` | The product page: every image whole on the mat; beside it only what it takes to decide and buy: the museum label (artist bold, *title* in a `<cite>`, year), medium, edition, size, price, one action, the archive note and the framing panel. "About the work" (the description, then disclosures) follows at reading width under both columns (DS-38). In tiles the medium stops at two lines |
| Panel | `.gs-panel` | A small box on tint inside a paper section: the framing offer, contact details |
| Disclosure | `.gs-disclosure` | A `<details>` for product disclosures, with the chevron |
| Select | `.gs-select`, `.gs-select-wrap` | A native select styled as an input, chevron from the icon set |
| Cart | `.gs-cart__*` | One row per work (thumbnail on the mat, label, price, quantity, remove), then policy and summary |
| Pagination, results | `.gs-pagination`, `.gs-results` | Real links, `aria-current` on the current page; search results for pages and articles |
| Skip link | `.gs-skip-link` | The first stop for keyboard users; hidden until focused |
| What's on | `sections/gs-whats-on`, `.gs-rail` | Home (DS-54): the next exhibitions and events in one row, soonest first, from their entries. Events show once, at their next date, as event cards (`snippets/gs-event-card`: the event's image, else its programme page's hero, else its exhibition's key image; the programme or exhibition under the date, so every title in a row starts at the same height, DS-55). On phones the row scrolls sideways, bleeding to the edges with the next card peeking in, snapping card by card, with no script |
| Open today | `.gs-open`, `snippets/gs-open-today`, `js/gs-open.js` | "Open now until 4 PM", "Open today, 12 to 4 PM", "Closed today. Open Thursday, 12 to 4 PM", worked out in the gallery's time zone from the opening days and times in Theme settings. Without the script, the week's hours ("Open Thursday to Saturday, 12 to 4 PM"). Holidays aren't known: Plan your visit carries them |
| New limited editions | `sections/gs-portfolio-row` | Home (DS-54): three works from the newest portfolio as artwork tiles, with links to the portfolio and to all editions. Scrolls sideways on phones |
| Visit | `.gs-visit` | Home (DS-32): heading and a link to Plan your visit beside the address and hours, which reuse the details list. From theme settings, so they're typed once for the footer, contact page and home. With an image (`.gs-visit--media`, DS-54) the building's photo sits beside them and the heading gets today's opening line; the heading and details sit together, centred on the photo, with the details two across (`.gs-visit__body`, DS-55) |
| Visit details | `snippets/gs-visit-info`, `.gs-visit-info` | Plan your visit (DS-61): the brand's box on the tint, first thing after the hero. Today's opening line leads it at H2 size in sentence case (`.gs-open--lead`: "Open now until 4 PM", "Closed today. Open Thursday, 12 to 4 PM"), since the gallery opens three afternoons a week and that is what most visitors check. Under it, the details list: Address with "Get directions" (Google Maps, the address as destination), Gallery hours, Admission, Artists for Kids office hours, all from Theme settings, so they are typed once. Four across from 1200 px (the address column a little wider, labels on one row by subgrid, so the values line up), two across from 750 px, stacked on phones. Rendered by the page text section, before the text, on the page chosen as Plan your visit page in Theme settings; staff don't add it |
| Artists A to Z | `sections/gs-artist-index`, `.gs-index`, `.gs-letters` | The Artists page (DS-62): every artist entry, sorted by its sort name (surname first) under a letter in the accent text colour at display size (the page's one large gesture), with life dates and the number of works; names in columns (three from 990 px, two on phones, as DS-45), each opening the artist's page on the site, never another site. Letter links jump down the list; on phones they are one row that scrolls sideways. With the script, a field above filters the names as you type, accents ignored, and says how many match |
| Work tile | `snippets/gs-work-tile` (`.gs-artwork-tile`) | A work in the collection (DS-62): the edition's tile without a price, so a work looks the same in the Shop and the collection. On the artist's own page it leaves the artist's name off |
| Work page | `sections/gs-work-detail` (`.gs-artwork`, `.gs-details--stack`) | The product page's layout (DS-38) without price or cart: every image whole on the mat; the museum label with the artists linking to their pages; the facts one to a row under rules (medium, dimensions, edition, credit, accession number, shown in, browse); the edition in the Shop in a tint panel when this is the collection's copy of one. With no image, the label takes the width (`.gs-artwork--text`) |
| Artist and grouping header | `sections/gs-entry-head`, `.gs-entry-head`, `.gs-crumb` | A link back (Artists, or the Permanent Collection) above the name; the artist's other names, then nationality and dates, the biography and the portrait. No website (DS-63). A grouping gets its introduction |
| Documents | `sections/gs-artist-documents`, `.gs-doc-tile` | After an artist's works (DS-63): Document entries as tiles like the works, each cover whole on the mat and its title under it; the tile opens the file, "(PDF)" where it is one. No link while the file is missing (a PDF over 20 MB); the mat with "PDF" when there's no cover |
| Search the collection | `sections/gs-collection-search`, `.gs-finder`, `js/gs-collection.js` | The Permanent Collection page (DS-62): the counts from the entries, then a field that finds works by artist, title, year, medium, category or theme, 48 tiles at a time. Shopify's search doesn't look in entries, so the script reads `sections/gs-collection-data` (250 works a request) the first time it's needed. The site's search page shows the first six matches and links here with `?q=`. Without the script the field isn't shown; the browse and artist pages reach every work |
| Ways into the collection | `sections/gs-collection-ways`, `.gs-ways`, `.gs-browse` | The groupings as compact cards with their first work on the mat (two across on phones), then every category and theme as a list of links with its count, and a link to Artists A to Z. From the grouping entries, so a new one shows without editing the page |
| Featured works | `sections/gs-collection-featured` | Six works from the grouping `featured`, which staff change in the admin |
| Text with pictures | `.gs-text-media` | Page text with figures, split at its H2 headings; each part's pictures beside its paragraphs from 990 px, after them below (DS-51, §6.11) |

## 7. Page templates (REUSE-01 to 04, SHOP-01 to 03, EXH-01 to 03)

### 7.1 Why this layer exists

The live store (read-only snapshot, 2026-09-25): **32 published pages use 28 page templates, and 25 of those templates serve exactly one page.** Every exhibition has its own template, as do On Now, Upcoming, Past, the Exhibitions overview and each programme page; Our Story uses the Shop template. Portfolios use three collection templates, and products use templates per state.

The cause is a Shopify behaviour, not carelessness: a template's sections are shared by every page assigned to it, so the only way to give one page its own hero image or intro inside a section is to copy the template. Each copy then gets designed separately and drifts. Styling rules alone can't fix that; the fix is a closed set of templates fed by per-page fields.

### 7.2 Composition rules (all templates)

Canonical, machine-readable version: `templates.rules.json`. Checked by `scripts/lint_theme.py`.

1. The set of templates is closed (§7.4). A new template needs a decision in §12 first.
2. A page starts with a hero or a page header (collections with the collection header, products with the artwork detail). Exactly one H1.
3. At most one hero, one page header and one switcher per page.
4. At most eight sections. At most one listing on the Shop landing, exhibition lists and portfolio pages; nothing may repeat a list already on the page.
5. Surfaces: paper by default; never two tinted, ink or accent sections in a row.
6. No disabled sections left in templates: delete them.
7. No `custom-liquid` or app sections inside page templates without a logged decision.

### 7.3 Where content lives

- **Page body:** running text, in the normal page editor, styled by `.gs-prose`.
- **Page fields** (proposal parts 1, 4 and 6): hero image, whether it is an artwork, eyebrow, intro, programme, gallery images, card groups, hero caption, call to action. Template sections read them directly in Liquid, so one template serves many pages and nothing has to be connected in the editor (DS-28).
- **Exhibition entries** (proposal part 2): all exhibition data, with status computed from dates.
- **Product fields** (proposal part 3): artist, title, year, medium, edition for the museum label.
- **Never in template section settings:** anything that differs from page to page. Section settings hold only choices that are the same for every page on that template.

Until templates are reassigned at release, a page whose old template the new theme lacks falls back to `page`. The exhibition lists show on `page` anyway (DS-48), and so does the programme pages' layout: `page` carries the same two text parts as `page.programme`, and `snippets/gs-is-programme-page.liquid` recognises the seven programme pages by their old template names until release (DS-51). `?view=` still previews any template (for example `/pages/artists-for-kids?view=programme`).

### 7.4 Template set and mapping

| Template | Used by (current template in brackets) |
| --- | --- |
| `page` | About (default; hidden at release, its history joins Artists for Kids, P-24), About Us (`about-us`), Our Story (`shop`; hidden at release, P-25), Plan Your Visit, Donate, Gordon and Marion, Engage (`page`), FAQ (`page`), Upcoming Events (`page`), On Now (`current-on-now-exhibition`), Upcoming Exhibitions (`upcoming-exhibitions`), Past Exhibitions (`past-exhibitions`), privacy opt-out (default) |
| `page.programme` | Artists for Kids, The Smith Foundation, Public Programs, Speaker Series, Music at the Smith, Explore + Create, Art in Good Company (each currently its own template). Volunteer (`volunteer`) too: its roles are its cards (DS-58) |
| `page.permanent-collection` | Permanent Collection (`permanent-collection`, the same name, so nothing is reassigned; DS-62) |
| `page.artists` | Artists (`artists`, the same name; DS-62) |
| `metaobject/artist`, `metaobject/artwork`, `metaobject/collection_group` | Every artist, work and grouping in the Permanent Collection (DS-62) |
| `metaobject/exhibition` | Every exhibition (six current templates `exhibition-ftg`, `-ohad-2026`, `-playhouse`, `-prevailing`, `-stitched`, `-taoc`, plus the exhibitions now written into On Now and Upcoming) |
| `page.shop` | Shop / Limited Editions landing (`shop`) |
| `page.contact` | Contact (`contact`) |
| `collection` | Every portfolio and All Limited Editions (`collection-template`, `alt-collection-temp`, `all-products-template`) |
| `product` | Every limited edition (`not-available-yet-product`, `no-frame-product`, default); availability and framing come from product data |
| `index` | Home |

From 28 page templates to six (DS-48, DS-62), plus one exhibition template and three for the collection; from three collection templates to one; from three product templates to one. Three unpublished pages (2025 Spring Portfolio, Exhibition Tours and an older Public Programs) aren't mapped; the gallery can decide whether to keep them.

### 7.5 Template specs

Sections in order; brackets mean optional. All templates also get the global header, newsletter band and footer.

- **index (Home, DS-54):** hero, led by the exhibition on now, by an installation view when it has one (DS-30) · What's on: the next exhibitions and events in one row, soonest first, each event once at its next date, with today's opening line and links to all exhibitions and all events · feature panel for Artists for Kids (its colours and logo, tint) · New limited editions: three works from the newest portfolio as artwork tiles · feature panel for the Foundation's support (its colours, accent, image on the right) · Visit with the building's photo, today's opening line, address and hours · newsletter band. Two of the three allowed listings; the rows scroll sideways on phones (`.gs-rail`). The two feature panels are apart, and the accent one sits away from the tint newsletter band, so two tints never touch. It follows the reference galleries (MoMA, Vancouver Art Gallery, Gagosian, David Zwirner): art in the room first, then what's on today, then one image-led idea per row, with a way in for each audience.
- **page:** hero or page header · [switcher and exhibition list: the On now, Upcoming and Past pages only] · [visit details: the Plan your visit page only, DS-61] · rich text (page body) · [card groups] · [the text's headed sections: programme pages only, until their templates are reassigned] · [upcoming events] · [image gallery]. Most pages need only the first two; the others show only when the page has them. On the Upcoming Events page (theme setting) the events list shows every upcoming event, and its heading is for screen readers only, since the page title says the same.
- **page.programme:** for the programme pages, and for Volunteer, whose roles are laid out the same way (DS-58). Hero or page header (programme colours from the `programme` field; the programme's logo above the title when there's no hero image; the call to action field as the button) · the page text's opening, up to its first H2 · [card groups, e.g. Programs] · [the text's headed sections, e.g. History, each under a section heading] · [upcoming events for this page] · [image gallery]. The programmes come straight after the opening, since they are what most visitors come for; background with headings follows them (DS-51). A page whose text has no H2 shows all of it before the programmes, as before. The Artists for Kids page carries the external-site links as normal links; the cue is automatic.
- **The exhibition lists (on `page`, DS-48):** on the pages chosen as On now, Upcoming and Past in Theme settings, the page template shows the switcher (On now / Upcoming / Past) and the exhibition list after the page header. On now and Upcoming show wide cards of their status, soonest first (DS-34), with the empty state when there are none; Past shows every past exhibition from entries, newest first (DS-24, DS-25), with no hand-built archive section. Any page text follows the list. The lists don't depend on the page's template assignment, so they work before templates are reassigned and can't be lost to a wrong template choice.
- **metaobject/exhibition:** hero (key image, artwork or photo variant; status chip and dates, or the dates note, from the entry; key image caption) · about the exhibition (summary as deck, text, credits and funder logos, beside the facts: opening reception until it has ended, upcoming events that reference the exhibition, curator credit, venue, artists and collection artists; empty fields show nothing; DS-35) · [installation views gallery] · [works from the collection: the entry's Works from the collection as artwork tiles, all on one page, DS-63] · [more exhibitions: compact cards].
- **page.permanent-collection (DS-62):** hero (the Browse button opens the search) · the gallery's introduction (page text) · search the collection · ways into the collection · featured works. Nothing here links to the old catalogue.
- **page.artists (DS-62):** hero or page header · the page text (the two paragraphs) · Artists A to Z.
- **metaobject/artist (DS-62, DS-63):** header (name, other names, nationality and dates, biography, portrait) · works in the collection, 24 to a page · [documents: tiles with their covers] · [editions in the Shop: the editions whose Artist pages field names the artist] · [exhibitions at the gallery, newest first]. Each part shows only when the artist has some. No link to the artist's website.
- **metaobject/artwork (DS-62):** the work (images, label, facts, the edition in the Shop, about the work) · [more by the artist: one row of three and a link to their page].
- **metaobject/collection_group (DS-62):** header (name, introduction) · its works, 24 to a page, with the count as the heading.
- **page.shop:** hero or page header · [rich text: one short introduction] · portfolio navigation (compact cards, artwork mode, one per portfolio) · [feature panel: e.g. framing]. No other listings (SHOP-01, SHOP-02). The portfolio navigation and the feature panel show only on the Shop landing page chosen in Theme settings, so another page on this template reads as a plain page (DS-49).
- **page.contact:** page header · contact details beside the form. The details are the page's own text when it has some, in the tint panel, so the gallery's words (both email addresses, office hours) show once; otherwise the address, hours, email and phone from Theme settings (DS-42).
- **collection:** collection header (title, season, short intro) · switcher (portfolios) · artwork grid (tiles) · [rich text]. Keeps the cleaner layout the notes praise (SHOP-03).
- **product:** artwork detail (artwork-mode media, museum label from product fields, price, edition, add to cart, framing option from `custom.featured_frame`) · [rich text: about the work] · [related works, one row of three].

## 8. Logos

### 8.1 Files

`logos/` holds 29 SVGs converted from the supplied vector print PDFs, plus `logos/derived/` (2 files) and `logos/logos.json` (size, aspect ratio, placement, minimum size, brand use, and original source file for each). Naming: `{org}-{lockup}-{variant}.svg`.

- Orgs: `gallery`, `foundation`, `artists-for-kids`.
- Lockups: Gallery `simple-stacked`, `simple-horizontal`, `full-stacked`, `full-horizontal` (full adds "of Canadian Art"); Foundation `simple`, `full` (full adds "for Young Artists"); Artists for Kids `full` (single lockup).
- Variants: `colour-box`, `bw-box`, `black`, `white`, and `colour` (Artists for Kids unboxed, black type with orange swoosh).

Conversion notes: fills were remapped from the PDFs' CMYK builds to the official web sRGB values (§11), unboxed variants were cropped to the artwork's bounds so they align with type and grid edges, and each file carries `role="img"` and an `aria-label`. The originals in `reference/` are untouched. The nine logos the website uses are generated into theme snippets by `scripts/build_logo_snippets.py` and rendered with `{% render 'gs-logo', name: ... %}`. The snippets leave out the files' embedded content credentials (a C2PA manifest of about 7.7 KB each), which would otherwise be inlined on every page; the files keep them.

### 8.2 Which logo where

| Placement | File |
| --- | --- |
| Header, Gallery pages (all but the two below) | `gallery-simple-stacked-colour-box` |
| Header, Artists for Kids pages (DS-47) | `artists-for-kids-full-colour-box` |
| Header, Smith Foundation pages: the Foundation, Gordon and Marion, Donate (DS-47) | `foundation-simple-colour-box` |
| Condensed or very tight header (if ever needed) | `gallery-simple-horizontal-colour-box` |
| Footer (ink) | `gallery-simple-stacked-white`, `artists-for-kids-full-white`, `foundation-simple-white` |
| About page, official content | `gallery-full-stacked-colour-box` at 112 px tall or more |
| A logo card: each organisation beside its own text, as on About Us (DS-50) | `gallery-full-stacked-colour-box`, `artists-for-kids-full-colour-box`, `foundation-full-colour-box`: the full lockups, since the text names each organisation in full |

The horizontal Gallery lockups are "limited use when this shape is more appealing in a design" (p.7); the simplified lockups are the primary use (pp.6, 8).

### 8.3 Rules

- Minimum display heights (system rule, since the guides set none; keeps the smallest lettering at about 7 px cap height): Gallery simple stacked 48, simple horizontal 32, full stacked 112, full horizontal 64; Foundation simple 72, full 88; Artists for Kids 48. Below these, use a simpler lockup.
- Logos side by side are matched by their letters, not their boxes: the same lowercase height and the same last baseline, from each file's measured metrics (DS-59). Equal box heights make the two-line Foundation lockup's letters half as big again as the three-line stacks'.
- Clear space (system rule): at least 25% of the logo's height on all sides, except the header logo, which is deliberately flush to the page corner.
- Do not recolour, stretch, rotate, add effects, crop, or put a boxed logo on its own box colour. White versions only on ink or dark photography.
- Derived teal versions (`logos/derived/`) follow the "text only logo" colour on pp.6 and 11 but were not supplied; use only after the gallery approves (Q3).
- Clusters: the "GS logo clusters document" referenced on pp.3 to 5 is not in the folder. Do not hand-assemble clusters for production until it arrives (Q1).

## 9. Shopify implementation map

The site gets a new theme (P-13), built on Shopify's Skeleton theme (P-14) in `theme/`. Skeleton supplied the file layout, the meta tags and the gift card page; everything else is `gs-` code. The untouched Colorblock theme is kept in `baseline/theme/` for reference and drift checks only. Rewritten for the build on 2026-09-25 (0.5).

### 9.1 Files

| Theme file | Source | Role |
| --- | --- | --- |
| `assets/gs-tokens.css`, `assets/gs-components.css` | `tokens.css`, `components.css` | Copies. Edit the design-system file, then run `scripts/sync_theme.py theme/`; `--check` fails if a copy differs |
| `assets/gs-nav.js`, `assets/gs-forms.js` | `js/` | Copies, loaded with `defer`. Header extras (§6.1) and form states (§6.12). Everything works without them |
| `assets/mulish-*.woff2` | Google Fonts, SIL OFL 1.1 (`fonts/Mulish-OFL.txt`) | Mulish variable font, latin and latin-ext, normal and italic (DS-02) |
| `snippets/gs-logo-*.liquid` | `logos/` via `scripts/build_logo_snippets.py` (run by `sync_theme.py`) | Generated inline SVG logos; never edited by hand |
| `snippets/gs-*.liquid` | The theme itself | Everything that enforces a rule in code (§9.5). LiquidDoc headers, so Theme Check verifies each `render` call's parameters |
| `sections/gs-*.liquid` | The theme itself | One section per component; no `{% stylesheet %}` blocks, all styling is in `gs-components.css` |
| `locales/en.default.json` | The theme itself | Every word visitors see that isn't content: labels, states, empty and error messages (§6.12). Staff can change them in the admin (Online Store, Themes, Edit default theme content) without code |
| `layout/theme.liquid` | The theme itself | Loads the font, tokens, components and scripts; sets `data-gs-brand` (§9.3); skip link; header group, main, footer group |

### 9.2 Settings

There is no bridge to translate: the theme has no colour schemes, font pickers, radius, width or spacing settings. Its settings hold facts, not design:

- **Theme settings:** Gallery details (address, hours, admission and the Artists for Kids office hours (DS-61), the opening days and times for the "open today" line, email, phone, contact page, land acknowledgement), Social links, Exhibitions and events (the On now, Upcoming, Past, Exhibitions overview and Upcoming events pages; the label for artists from the collection), Permanent Collection (the Permanent Collection and Artists pages, DS-62), Shop (Shop landing page, the portfolio list newest first, All limited editions).
- **Section settings** only where a template serves one page (Home hero and feature, Shop landing feature) or where the value is the same everywhere (the product archive note and framing text, the cart's sales policy, the newsletter band's heading, text and consent wording).
- **Everything that differs by page** comes from the page's fields and entries (§7.3), read directly in Liquid (`page.metafields.custom.*`, `metaobject.*`, `shop.metaobjects.*`) rather than connected through dynamic sources in the editor. Nothing has to be connected per template, and a template can't be left connected to the wrong field (DS-28).

### 9.3 Programme and surface

- **Programme:** `layout/theme.liquid` reads the page's `programme` field (or the exhibition entry's) through `snippets/gs-programme.liquid` and sets `data-gs-brand` on `<body>`: `gallery`, `foundation` or `artists-for-kids`. Staff pick the programme in the page's field, never a colour.
- **Surface:** sections are paper. The newsletter band is tint and the footer ink, fixed. The feature panels (`gs-feature`, `gs-shop-feature`) offer one select, Tint, Brand colour (once per page) or Ink, which colours the box inside a paper section (§6.13). The hero title box is always accent.
- **Spacing:** paper sections are spaced by margins, which collapse, so two paper sections share one gap even across Shopify's section wrappers and sections that render nothing; bands pad inside their colour (§5.1).

### 9.4 What staff control

Staff edit words, images (with focal point and alt text), links, page fields, entries, the programme, the feature panel's surface, and which pages and portfolios the theme settings point to. They do not get colour pickers, colour-scheme pickers, font or size settings, alignment toggles, ratio pickers, overlay opacity, or padding and spacing sliders (`lockedSettings` in `templates.rules.json`; the linter finds none in the theme). Any new option is a design decision logged in §12 first.

| Where staff work | What they do |
| --- | --- |
| Online Store, Pages | Write the body; fill the page fields (hero image, is artwork, eyebrow, intro, programme, gallery images, card groups, hero caption, call to action); choose the template once |
| Content, Metaobjects | Add exhibitions, events, cards and card groups. Exhibition lists, Home, the switcher counts and "More exhibitions" update from the dates |
| Content, Metaobjects (the collection) | Add artists, works and groupings (DS-62). A new artist shows on the Artists page by itself; a new work also goes in its artist's Works list, and in any grouping it belongs to, so it shows there. Featured works is the grouping `featured`. An edition's Artist pages field puts it on the artist's page |
| Products, Collections | Fill the artwork label fields, Coming soon and Availability note, the linked frame, the collection's Photo credit |
| Online Store, Themes, Customize | Theme settings (§9.2); Home hero and features; the Shop landing feature; the main menu |
| Online Store, Navigation | The main menu (DS-11 model) and the footer's Explore and Legal menus. Contact, Search and Cart are built in (DS-29, DS-56) |

### 9.5 Enforced in code

| Rule | Where |
| --- | --- |
| Sections with pages are buttons, sections without are links; a parent's page must be in its dropdown; no repeated labels; store URLs relative; external links get the cue | `snippets/gs-nav.liquid`, `gs-url.liquid`, `gs-link.liquid` |
| Header and navigation work without JavaScript; one dropdown open at a time; drawer below 1200 px | `snippets/gs-header.liquid`, `gs-nav.liquid` (native `<details>`) |
| Escape, outside click, focus leaving | `js/gs-nav.js` (tested in the development theme: Escape closes and returns focus) |
| Contact always in the header and footer | `snippets/gs-header.liquid`, `sections/gs-footer.liquid` (from the contact page theme setting) |
| Images only through photo or artwork mode; artworks never shifted by a focal point; no empty box when an image is missing | `snippets/gs-media.liquid`, `components.css` |
| Every image call says where it sits, so the right width downloads | `scripts/lint_theme.py` (`renderRules` in `templates.rules.json`) |
| Hero and page titles fit their box on any screen | `snippets/gs-fit.liquid`, `components.css` |
| No sticky hover on touch; icons survive forced colours | `components.css` (hover media query, forced-colours block) |
| Exhibition status from dates; one date format; one time format | `snippets/gs-exhibition-status.liquid`, `gs-date-range.liquid`, `gs-time-range.liquid` |
| Exhibition lists pick and order themselves; a past exhibition with no summary or text has a card that doesn't link (DS-25) | `snippets/gs-exhibition-index.liquid`, `gs-exhibition-card.liquid` |
| Events drop off once over; each page lists its own, the Upcoming events page lists all | `snippets/gs-event-index.liquid`, `sections/gs-events.liquid` |
| Card layout from content: image card or text card; a labelled link shows as a link, an unlabelled one makes the whole card a link | `snippets/gs-card.liquid` |
| Museum label from product fields, falling back to the product title | `snippets/gs-artwork-label.liquid`, `gs-artwork-tile.liquid` |
| Price, sold out and not yet on sale from product data, one template for every product | `snippets/gs-price.liquid`, `sections/gs-artwork-detail.liquid` |
| Site font on form controls, pasted text and embeds | `components.css` base guards, `.gs-prose`, `.gs-embed` |
| Mulish from bundled files, no fallback to Assistant | `snippets/gs-fonts.liquid` |
| Visitor-facing wording in one place, editable by staff | `locales/en.default.json` (Theme Check flags a missing key) |
| Closed template set, composition, no disabled leftovers | `scripts/lint_theme.py` + `templates.rules.json` |
| No design controls in section schemas | `scripts/lint_theme.py` |
| No raw colours or px font sizes in `gs-` code | `scripts/lint_theme.py` |
| Theme copies match the design system | `scripts/sync_theme.py --check` |
| Text actually renders in Mulish; no Unicode styled letters | `scripts/audit_fonts.py` |
| Colour pairings pass WCAG AA | `scripts/check_contrast.py` |

### 9.6 Verified, and still to verify

Verified in development theme `184755814697` (created by `shopify theme dev`, hidden, never the live theme) on 2026-09-25:

1. Every template renders on the store's real pages, collections and products with no Liquid errors or missing wording (home, about, on now, upcoming, past, programme pages, contact, shop, `/collections`, two portfolios, a product, cart, search, 404, blog).
2. Text renders in the bundled Mulish (`audit_fonts.py` on home, on now, a portfolio and contact). Two fallbacks, both expected: the Unicode italic letters in product titles (L-03, fixed by the label fields) and 12 characters in the land acknowledgement's Indigenous place names, which Mulish doesn't have (L-06).
3. Header: bar at 1440 and drawer at 652, dropdowns open on click, Escape closes and returns focus, the current section opens in the drawer, Contact shows in the utility row.
4. With the first exhibition and event entries (`proposals/store-writes/`): exhibition pages, On now, Upcoming, Past and Home render from entries; status follows the dates; a past entry with no text has a card that doesn't link.
5. Date and time fields show in the store's timezone: the reception entered as 18:00 Pacific reads "Friday, September 25, 2026, 6 to 8 PM".
6. Under the live theme, an entry's address returns 404, so nothing is visible to the public before release.

Since then every page has had a design pass with its real content, on the development theme and the review theme `184767250729` (2026-09-26). Still to verify, on the review theme, as part of the release backlog (plan):

1. That `image_tag` writes the editor's focal point from a file field's image as `object-position`, and the artwork-mode override holds (IMG-03).
2. The timezone Liquid uses for `'now'` on a changeover day (date and time fields are verified, item 5 above).
3. ~~Exhibition entry pages: the link-preview image.~~ Verified 2026-09-26: every page has one (`verification/2026-09-26.md`).
4. The newsletter form with an approved test address: customer created with the `newsletter` tag and email consent, and Mailchimp receiving it (ACCESS-01).
5. The contact form's delivery address: the store's contact email, `artistsforkids@sd44.ca` (Settings, Store details), checked 2026-09-26; a test message waits for the gallery.
6. Staff editing: two pages on one template with different fields, content stays separate (REUSE-03).

## 10. Quality checks

| Check | Command | When |
| --- | --- | --- |
| Colour contrast | `python3 design-system/scripts/check_contrast.py` | After any palette change |
| Theme structure | `python3 design-system/scripts/lint_theme.py theme/` (`--strict` once legacy warnings are cleared) | Every pull request |
| Linter tests | `python3 design-system/scripts/tests/test_lint_theme.py` (7 tests) | When the linter or rules change |
| Rendered fonts | `python3 design-system/scripts/audit_fonts.py <preview URLs>` (needs Playwright) | Before release, on the review theme's representative pages |
| Manual | Keyboard through the header on desktop and mobile, with JavaScript off once; a real phone for tap feedback; Windows High Contrast once; hero crops at 1440 / 768 / 390 and the longest real title at 320; staff edit of two pages on one template | Before release (plan verification rules) |

## 11. Source discrepancies and resolutions

| # | Issue | Evidence | Resolution |
| --- | --- | --- | --- |
| 1 | Gallery box colour | Brand guide p.11: `#9eb0b9` (its RGB row, 159/177/122, matches neither). Logo guide and every supplied colour-box logo: `#89a6ab`. Both say PMS 5425 | Use `#89a6ab`: UI that sits beside the logo must match it (DS-01) |
| 2 | Foundation box colour | Brand guide p.12: `#dad758`, PMS 388. Logo guide and supplied PNGs: `#cfd65e`, PMS 382. The full colour-box PDF renders a third value | Use `#cfd65e` (DS-01) |
| 3 | Gallery rule colour RGB | p.11 RGB row reads 206/177/185; hex `#cdd7db` matches the swatch | Use the hex |
| 4 | Small hex/RGB mismatches | `#e4eaec`, `#dad758`, `#ede658`, `#ffdd62`, `#f6efe3` each differ from their RGB row by 1 | Use the hex values; the difference is invisible |
| 5 | Alternative font | p.16 body text names Poppins; the specimen beside it shows Mulish; the plan already chose Mulish | Mulish (DS-02) |
| 6 | Text-only logo colour | pp.6, 11 show the Gallery text-only logo in teal; supplied files only have black and white | Derived teal SVGs, pending approval (Q3) |
| 7 | Logo file packaging | Foundation files in "3 GSF - Logos" are named `GSG-*`; the Artists for Kids "Full Colour" web PNG/JPG is identical to the boxed one (the unboxed colour version exists only in the print PDF); AFK black print files are named `.eps.eps` / `.eps.pdf`; Gallery simple horizontal white files lack "-White" | Clean names in `logos/`; unboxed colour version built from the print PDF |
| 8 | Old artwork | "TEMP USE GSF LOGOS" are low-resolution raster files in an older green (`#b0bc36`) | Do not use |
| 9 | Logo colours in PDFs | Print PDFs are CMYK builds that render differently from the web values | SVG fills remapped to the web values |

## 12. Decisions and open questions

| ID | Decision | Status |
| --- | --- | --- |
| DS-01 | Where the guides disagree, the supplied logo files set the colour values | Decided by Michael, 2026-09-26 |
| DS-02 | Mulish is the web font; Soleil via Adobe Fonts only if the gallery holds a licence | Decided by Michael, 2026-09-26 |
| DS-03 | One rounded corner, bottom-right, site-wide; sizes sm/md/lg | Decided by Michael, 2026-09-26 |
| DS-04 | Programme theming via `data-gs-brand`; Foundation and Artists for Kids text colours fall back to ink | Decided by Michael, 2026-09-26 |
| DS-05 | Artwork images are never cropped, rounded, shifted or overlaid; photo mode for everything else | Decided by Michael, 2026-09-26 |
| DS-06 | Inline links keep an underline, styled in brand colour with a tint hover fill (DS-21); "beyond default underlining" is met by design, not by removing the cue | Decided by Michael, 2026-09-26 |
| DS-07 | Header logo: Gallery simple stacked colour box, flush top-left, 64 / 96 px | Decided by Michael, 2026-09-26; amended by DS-47 |
| DS-08 | Hero text lives in a title box in the programme colour, never on the image | Decided by Michael, 2026-09-26 |
| DS-09 | Newsletter band on tint above an ink footer, on every template | Decided by Michael, 2026-09-26 |
| DS-10 | Headings in capitals per brand; artwork titles italic sentence case | Decided by Michael, 2026-09-26 |
| DS-11 | A section with pages under it is one button that opens its dropdown and never navigates; the section's main page is the first item inside. Sections without pages are plain links. Click or keyboard only, never hover; one open at a time. Reason: one target and one behaviour on mouse, touch and keyboard (NAV-01, NAV-03). Cost: a section's main page is two clicks from the menu, and its dropdown label must not read as a repeat of the section. Replaces the linked-label-plus-separate-caret model recorded in `IMPLEMENTATION_PLAN.md`, which that file still describes. Revisit only if testing shows people can't find section main pages, and fix that with clearer labels first | Decided by Michael, 2026-09-25; gallery approves labels |
| DS-12 | Photo hero overlaps the image by a fixed amount only; artwork hero never overlaps | Decided by Michael, 2026-09-26 |
| DS-13 | Sibling navigation (switcher) on exhibition list pages and portfolio pages | Decided by Michael, 2026-09-26 |
| DS-14 | Closed set of templates (§7.4) with per-page content in page fields | Approved 2026-09-25 (content model answers recorded by Michael) |
| DS-15 | Exhibitions as structured entries with status computed from dates. Addresses change to `/pages/exhibitions/<entry>`; old addresses redirect | Approved 2026-09-25 (content model answers recorded by Michael) |
| DS-16 | Artwork label data in product fields; plain-text product titles | Approved 2026-09-25 (content model answers recorded by Michael) |
| DS-24 | Past Exhibitions lists past entries automatically, newest first, above the existing archive; the six migrated exhibitions leave the hand-built archive at release. Reason: otherwise a closing exhibition has to be added by hand, which undoes DS-15 | Decided by Michael, 2026-09-25; amended by DS-25 |
| DS-25 | Past Exhibitions lists all 12 past exhibitions from entries; the six older ones (2020 to 2023) hold title, dates and image and don't link. Reason: the hand-built archive sections don't carry over to the new theme (P-13 in `DECISIONS.md`) | Decided by Michael, 2026-09-25 |
| DS-26 | Up to two short announcements with links in the header, set in theme settings, kept from the current announcement bar. One line, text only, no autoplay | Decided by Michael, 2026-09-25; superseded by DS-27 |
| DS-17 | Capitals stay for headings, subheadings and labels. The brand guide sets headlines and subheadings in caps (p.15) and labels its own pages in small tracked caps (p.11). The frontend-design review guidance treats caps labels as a template habit; the brand guide wins, and DS-18 limits how many labels there are | Decided by Michael, 2026-09-25 (brand guide governs) |
| DS-18 | Eyebrows only when they carry information (programme or organisation, season), never as generic section names. Status and dates are a chip plus a dates line, never a joined "A · B" string | Decided by Michael, 2026-09-25 |
| DS-19 | The header and every dropdown are native `<details>`, so navigation works without JavaScript; the script adds Escape, outside click and focus-leaving only. Same model as DS-11 | Decided by Michael, 2026-09-25 (review fix) |
| DS-20 | Standalone links are underlined caps labels without an arrow; the arrow is kept for "more of the same list" links only | Decided by Michael, 2026-09-25 |
| DS-21 | The box colour is for the brand's boxes only: logo, hero title box, primary button (brand guide p.11: "use for background logo box"; p.17: rounded-corner boxes). Link hover fills use the tint, and selection, the dropdown edge and the quote rule use the rule colour, as the guide assigns them. The On now chip is solid ink instead of box colour | Decided by Michael, 2026-09-25 (brand guide governs) |
| DS-22 | A system error colour, `#a3261b` (light `#f28b82` on ink), for error text and invalid-field borders only. The brand guide defines none | Decided by Michael, 2026-09-25 |
| DS-23 | The header is not sticky on any screen size, so nothing permanently covers the art on a phone | Decided by Michael, 2026-09-25 |
| DS-27 | No announcement bar in the header. Supersedes DS-26. The news it carried (a new portfolio, an exhibition opening) is on the home page, which builds its exhibition list from entries and features the newest portfolio automatically | Decided by Michael, 2026-09-25 ("we do not want that anymore") |
| DS-28 | Page fields and entries are read directly in Liquid (`page.metafields.custom.*`, `metaobject.*`), not connected to section settings through dynamic sources. Reason: nothing to connect per template in the editor, nothing that can be connected to the wrong field, and the sections can decide from the content (hero or page header, image card or text card) | Decided by Michael, 2026-09-25 |
| DS-30 | The home hero leads with the exhibition on now, from its entry, and shows the section's own image and heading only when nothing is on. Reason: the home page's lead stays current without anyone editing it (the old home featured a portfolio that had been replaced), and the art leads (principle 1). The home exhibition list leaves out the exhibition in the hero | Decided by Michael, 2026-09-25 |
| DS-31 | On tint surfaces the primary button is ink with paper text. Reason: the Gallery box colour on its own tint is 1.9:1 and reads as disabled (seen on the newsletter band) | Decided by Michael, 2026-09-25 |
| DS-32 | The home page gets a Visit block: address and hours from theme settings, and a link to Plan your visit. Reason: where and when to visit is the first thing a gallery visitor needs, and the old home page didn't say | Decided by Michael, 2026-09-25 |
| DS-33 | The home hero's own heading breaks into two balanced lines, sized to the longer line: GORDON SMITH / GALLERY | Decided by Michael, 2026-09-25 |
| DS-34 | On now and Upcoming show each exhibition as a wide card, image beside dates, title, curator and the start of the summary. Reason: there are rarely more than two, and a single small card in a three-column grid undersold what's on. Past stays a grid of cards | Decided by Michael, 2026-09-25 |
| DS-35 | The exhibition page puts the summary first, then the text and credits beside a column of facts (reception, events, curator, artists); on a phone the facts follow the summary. Replaces separate details and credits sections. Reason: a list of 19 artists before the description buried what the exhibition is about, and the text column left half the page empty | Decided by Michael, 2026-09-25 |
| DS-36 | On a programme page, an event titled the same as the page leads with its date and time instead of its title. Reason: four Explore + Create drop-ins read as the same heading four times | Decided by Michael, 2026-09-25 |
| DS-37 | A card group whose images are all portraits shows as a people grid: 4:5 frames, compact titles, up to four across. Reason: 14 board headshots cropped to wide 4:3 cards in three large columns made a very long page. Staff don't choose it; the images do | Decided by Michael, 2026-09-25 |
| DS-38 | The product page keeps only the label, price, action, archive note and framing offer beside the work; the description follows as "About the work" at reading width. Reason: the description in the narrow column ran the page to twice the image's height with empty space beside it | Decided by Michael, 2026-09-25 |
| DS-29 | The header's utility links are built in: Contact (the contact page in theme settings), Newsletter, Search and Cart, as approved (P-07, P-15). Reason: Contact can't be dropped by a menu edit, and no utility menu has to be created in the store | Decided by Michael, 2026-09-25 |
| DS-39 | Page text that changes at release is staged in a temporary page field (`custom.release_body`) that the new theme shows instead of the live text; a release script moves it into the page and deletes the field, stopping if the live text changed meanwhile. Reason: the review has to show the site as it will launch, and page text is live, so it can't change before release. Used for On Now, Upcoming and Upcoming Events (cleared) and for Donate and Gordon and Marion (content added from their old templates). The fallback leaves the theme after release | Decided by Michael, 2026-09-25 |
| DS-40 | Headings in page text sit one step below section headings: `h2` at the H3 size, `h3` and `h4` at the H4 size. Reason: on Plan Your Visit, the FAQ and Donate, headings in the page text were as large as the page's own section headings (Ways To Give, Upcoming events), so eight short facts read as eight sections | Decided by Michael, 2026-09-26 |
| DS-41 | A heading at the very start of the page text that only repeats the page title isn't shown. Reason: the FAQ opens with "Frequently Asked Questions" under its own title; the page header already says it. Nothing is deleted from the page | Decided by Michael, 2026-09-26 |
| DS-42 | The Contact page shows its own text beside the form, in the tint panel, in place of the theme's contact details; a page without text still gets the details from Theme settings. Reason: the page text repeated the address and phone below the form, and holds what the settings don't (both email addresses, office hours) | Decided by Michael, 2026-09-26 |
| DS-43 | The Exhibitions overview page carries the On now / Upcoming / Past switcher under its hero. Reason: the overview had no way into the three lists except the menu (EXH-02); with the switcher it's the way in | Decided by Michael, 2026-09-26; superseded by P-20 (no overview page) |
| DS-44 | A card group of four or eight goes two, then four, across instead of three. Reason: four cards in three columns left one alone (Donate's Ways To Give, Public Programs) | Decided by Michael, 2026-09-26 |
| DS-45 | A list of twelve or more items in page text flows into two columns, three from 990 px, without bullets. The Artists page's names become one list in its staged text (DS-39): same names, order and links. Reason: 59 names in one centred column made a very long page | Decided by Michael, 2026-09-26 |
| DS-46 | Artwork grids (portfolio pages, the Shop's portfolio navigation, search results, related works, galleries of works) show at most three across, and related works one row of three. Reason: at four across each print was too small to see; asked for with the approval of DS-05 | Decided by Michael, 2026-09-26 |
| DS-47 | The header logo follows the page's programme field (the same value that sets the programme colours, DS-04): `artists-for-kids-full-colour-box` on Artists for Kids pages, `foundation-simple-colour-box` on Smith Foundation pages (the Foundation, Gordon and Marion, Donate), `gallery-simple-stacked-colour-box` everywhere else, including the Shop, portfolios, products, Our Story and Artists (Michael, 2026-09-26). It always links home, and its accessible name says whose logo it is. The Foundation logo is 72 px tall on phones, its minimum (§8.3); a page header no longer repeats a programme logo. Reason: asked for with the approval of DS-07, so each organisation's pages carry its own mark | Decided by Michael, 2026-09-26 |
| DS-48 | On Now, Upcoming and Past use the standard page template: it carries the switcher and the exhibition list, which show only on the pages chosen as On now, Upcoming and Past in Theme settings, as the events list does on the Upcoming events page. The `page.exhibitions` and `page.past-exhibitions` templates are removed. Reason: the lists no longer depend on each page's template assignment. They show in the review before templates are reassigned, release has three fewer pages to reassign, and a wrong template choice can't empty On Now | Decided by Michael, 2026-09-26 |
| DS-49 | On the Shop template, the portfolio navigation and the feature panel show only on the Shop landing page chosen in Theme settings; any other page on that template shows its page header and text. Reason: Our Story still has the old template name `shop` until release, so it showed as the Shop landing page. Same principle as DS-48: special content follows Theme settings, not template assignment | Decided by Michael, 2026-09-26 |
| DS-61 | Plan your visit pass. The page opens with its visit details: today's opening line, large, then the address with "Get directions", gallery hours, admission and the Artists for Kids office hours, from Theme settings (admission and office hours are new settings, holding the page's own words). The page text keeps the rest: "Getting Here" beside a photo of the entrance, with Public Transport and Parking as its points, then Accessibility. Reason: eight headings in one narrow column, the right half empty, the facts visitors need (open today? where? what does it cost?) no more prominent than parking, the address and hours typed a second time, and no way to get directions (Michael, 2026-09-26: "Let's improve /pages/plan-your-visit using all our design skills - it looks really bad") | Decided by Michael, 2026-09-26 |
| DS-60 | Donate pass, as on Volunteer (DS-58): the page's ways to act can be acted on. "How to give" (was "Ways To Give", which read like the text's "Ways to Support" just above it) holds Email, Mail and Phone; Email and Phone get "Email us" and "Call us" links. Online Form leaves the group until there is a form, since it points to one "above" that isn't on the page. The hero button says what it does, "Make a gift", and still jumps to those cards. A photo of a class visit sits beside "Ways to Support", whose $150 example is exactly that (Michael, 2026-09-26: "The improvements we made to /pages/volunteer we need to look at /pages/donate and also improve"); and, after Michael's review ("we can improve the presentation of the The impact of your gift and Ways to Support text sections"), its two lists become lists of points and its three example amounts a row of amount tiles (`gs-points`, `gs-amounts`, §6.11) | Decided by Michael, 2026-09-26 |
| DS-63 | Artist and exhibition pages (after Michael's review of DS-62). An artist's documents show under "Documents", after the works, as tiles like the works (`sections/gs-artist-documents`): each cover whole on the mat, its title under it, as the catalogue showed them. Each is a Document entry (title, cover, file); the tile opens its PDF, and says "(PDF)". A document whose PDF is over 20 MB shows its cover without a link until a smaller copy is uploaded; one without a cover gets the mat with "PDF". The covers are decorative (empty alt), since the title is right under them. The artist's website isn't shown: the page is about their work here. An exhibition's page lists its works from the collection after the installation views (the exhibition entry's Works from the collection field, `gs-work-grid`), all on one page. Reason: Michael, 2026-09-27: "We can also remove the Website labels and links - we do not need those"; then, on the first version's text links, "I didn't want them as a text list, I wanted the images displayed like the art works as the original catalogue site had them"; and he asked for the exhibition pages' works | Decided by Michael, 2026-09-27 |
| DS-62 | The collection's five templates join the closed set (§7.4): `page.permanent-collection` (the front door: hero, the gallery's introduction, collection search, ways in, featured works, the count), `page.artists` (the page's text, then an A to Z index of every artist entry with life dates and counts, three columns from 990 px as DS-45, letter links across the top), `metaobject/artist` (name and dates, works as artwork tiles 24 to a page, editions in the Shop, exhibitions, documents, the artist's website with the external cue), `metaobject/artwork` (the product page's artwork layout without price or cart: every image whole on the mat, the museum label, more by the artist) and `metaobject/collection_group` (a grouping's introduction and works). Names on the Artists page link to the artists' pages on the site, never out. Reason: the Permanent Collection lives on an external catalogue, and the Artists page sends visitors to 59 outside sites instead of to the artists' work (Michael, 2026-09-26: "/pages/artists should not link out to the artist's website, it should link to their associated page like [the catalogue's artists page]. Moma does this as well"). Plan: `proposals/permanent-collection.md` | Decided by Michael, 2026-09-26 ("Sounds good, let's start there") |
| DS-59 | The footer's three logos share one letter size and one baseline instead of box heights (the Gallery 96 px, the others 72): the Foundation's letters at its 72 px minimum set the size, so the Gallery is 121 px tall and Artists for Kids 112 px, and each logo hangs by its own descent so the last lines align. Reason: at equal heights the Foundation's letters were half as big again as the Gallery's and Artists for Kids' smallest, and the Gallery's y and the brush mark lifted their words off the line (Michael, 2026-09-26: "The logos in the footer do not look optically aligned nor the same size") | Decided by Michael, 2026-09-26 |
| DS-58 | Volunteer pass. Its two roles become cards between the opening sentence and the rest, which goes under a "Join the team" heading beside a photo of an event from the page's old banner and ends with how to apply (the form and a contact link), so the page no longer ends without a way to act. The hero button says what it does: "Download the form". Volunteer takes the programme template's layout for this (bridged until release). Two rules for every page: a hero image without its own alt text is decorative rather than repeating the title, and a card group without a heading follows the text it continues at a group's space. Reason: the page was one column of text with its only action at the top and never said what to do with the form (Michael, 2026-09-26: "Is /pages/volunteer as good as it can be?") | Decided by Michael, 2026-09-26 |
| DS-57 | The footer in three rows: the logos beside the land acknowledgement that names the organisations, then the Visit, Contact, Explore and Follow columns in fixed places lined up with it (four across from 1200 px, two below, Visit alone on phones), then the copyright on its own line over the legal links. Reason: the acknowledgement sat between the columns and the legal line at the same weight as the links; the columns spread to the page's edge whatever their number, so Follow would have moved everything when it arrives; the last legal link sat alone on a line; and the phone footer was longer than it needed to be | Decided by Michael, 2026-09-26 |
| DS-56 | The header's utility links are Contact, Search and Cart. Newsletter goes: the sign-up band is at the foot of every page, so the link only jumped down to it. Changes the header part of DS-29 and the approved newsletter placement (P-07, P-15); the band itself stays on every page (DS-09, ACCESS-01) | Decided by Michael, 2026-09-26 |
| DS-55 | Home page design pass with the design skills, inside this system. Feature panels for a programme lead with its logo on tint or ink, and a page's second image panel puts its image on the right. Event cards name their programme or exhibition under the date, so titles line up. Visit's heading and details sit together, centred on the photo. The artwork hero's mat takes the work's shape (4:5 to 4:3) and its caption sits under the work on phones and tablets. Photos get a hairline inside their edge (an exception to §5.3's no-borders rule, which Michael kept), and buttons shrink to 97% while pressed (160 ms, a new motion in §5.4). The Artists for Kids panel's heading and button say who it's for and where it goes: "For kids, families and schools", "See Artists for Kids programs" | Decided by Michael, 2026-09-26, with the photo edge and button press kept |
| DS-54 | A new home page after reviewing MoMA, the Vancouver Art Gallery, Gagosian and David Zwirner: What's on (exhibitions and events together, sideways on phones), an "open today" line from structured opening days and times, an Artists for Kids panel, the newest portfolio's works as tiles, a Foundation support panel, and Visit with the building's photo. The hero leads with an installation view when the exhibition has one. Feature panels take a programme's colours from a programme setting and can carry a second link | Decided by Michael, 2026-09-26 |
| DS-53 | A quote in page text with who said it is a pull-quote figure beside its text; card groups can be linked to by their handle, so a call to action can jump to them. Donate: "The impact of your gift" is a heading, Asha's words a pull quote beside what a gift does, and the hero button "Ways to give" jumps to the Ways To Give cards. Gordon and Marion: the biography is paragraphs, and their photo, with a description, sits beside it, with the video under it at its own square shape, captioned with its heading. Embedded videos keep the shape their embed code gives | Decided by Michael, 2026-09-26 |
| DS-52 | A card group whose count would leave a short last row gives the spare room to its first cards: five cards go two wider, then three; an odd count at two across starts with one wide card, image beside text. First used on The Smith Foundation's five ways to take part, which left an empty slot. Its text leaves out the full-name line that repeated the next sentence's opening, and the four programmes it names link to their pages. The five get a "Get involved" heading | Decided by Michael, 2026-09-26 |
| DS-51 | Programme pages put their programmes straight after the opening text: the page text up to its first H2 comes before the card groups, the headed sections after them. Page text with figures sets each picture beside its paragraphs from 990 px (`.gs-text-media`), and an artwork figure sits on the mat. The headed sections after the programmes are parts of the page: their H2 is a section heading, level with the programmes' heading. First used on Artists for Kids, whose six programmes had been below its history and two large pictures | Decided by Michael, 2026-09-26 |
| DS-50 | Cards get a Logo field (Gallery, Smith Foundation, Artists for Kids). A card with a logo shows that organisation's full logo as its heading, in its colours; a group of them is one organisation per row, the logo beside its text (§6.5). About Us uses it: its three descriptions move from the page text into a card group, each beside its own logo, and the combined logo image above them goes at release. Each row links on: Plan your visit, More about Artists for Kids, More about the Foundation. Reason: Michael asked for the correct logo with each description and the two better integrated (2026-09-26) | Decided by Michael, 2026-09-26 |

| ID | Question or input | Needed for |
| --- | --- | --- |
| Q1 | The "GS logo clusters document" referenced on pp.3 to 5 | Footer and partner logo areas |
| Q2 | Does the gallery (or school district) hold Adobe Creative Cloud, making Soleil available on the web? | DS-02 |
| Q3 | May we use the teal text-only Gallery logo (derived from pp.6, 11)? | Optional header/footer variants |
| Q4 | Designer confirmation of the colour conflicts in §11 rows 1 and 2 | DS-01 |
| Q5 | Artists for Kids external site address and which links go there. Answered 2026-09-25 by the approved menu map: Artists for Kids stays one menu link; its programme links to https://artistsforkids.sd44.ca/ stay on the Artists for Kids page as cards | NAV-04 |
| Q6 | Accept the system rules for logo minimum size and clear space (the guides set none)? | §8.3 |
| Q7 | Must the current exhibition page URLs stay unchanged? Answered 2026-09-25: no, redirect them | Proposal part 2 (entries chosen) |
| Q8 | Is an enlarge/lightbox view wanted for gallery images? | §6.8 |
| Q9 | Approval of the three parts of `proposals/content-model.md`. Answered 2026-09-25: all approved | DS-14 to DS-16 |
| Q10 | Room names for the exhibition `venue` field, the label for the second artist group, and the start date of *Stitched* | `proposals/content-model.md` "Still open" |
| Q11 | The land acknowledgement's place names use characters Mulish doesn't have (ʔ, ɬ, θ, some combining marks), so those letters render in Arial. Accept that, or load a font made for BC Indigenous languages for that text (for example BC Sans, SIL OFL)? | L-06, §4.1 |

## 13. Changelog

- 0.6.20 (2026-09-27): DS-63 corrected by Michael: an artist's documents are tiles with their covers, like the works, from Document entries (`gs-artist-documents`, `.gs-doc-tile`), not a list of links.
- 0.6.19 (2026-09-27): DS-63, from Michael's review: artists' documents after the works (`gs-artist-documents`), no website link on artist pages, exhibition pages list their works from the collection (`gs-work-grid` on `metaobject/exhibition`).
- 0.6.18 (2026-09-27): the Permanent Collection (DS-62, approved by Michael): five templates (`page.permanent-collection`, `page.artists`, `metaobject/artist`, `metaobject/artwork`, `metaobject/collection_group`), Artists A to Z, the work tile and page, the artist and grouping header, the collection search (`js/gs-collection.js`, also on the site's search page), ways in and featured works (§6.13, §7.4, §7.5); the product label's artist links to their page; the nav marks Collection current on entry pages; Theme settings gain a Permanent Collection group.
- 0.6.17 (2026-09-26): Plan your visit pass (DS-61, approved by Michael): visit details (`snippets/gs-visit-info`, `.gs-visit-info`, `.gs-open--lead`), rendered by `gs-page-body` on the Plan your visit page; Gallery details gain Admission and Artists for Kids office hours.
- 0.6.16 (2026-09-26): Donate pass (DS-60, approved by Michael): card links, card group, staged text, button label; lists of points and amounts in page text (`.gs-prose .gs-points`, `.gs-amounts`, §6.11); §6.2 says an email address or phone number offered as the way to act is a link with a verb.
- 0.6.15 (2026-09-26): footer logos at one letter size on one baseline (DS-59, approved by Michael): logo metrics (`--gs-logo-x`, `--gs-logo-descent`) for the three white logos, `--gs-footer-logo-x` in place of `--gs-footer-logo-h` and `--gs-footer-logo-h-lead`.
- 0.6.14 (2026-09-26): Volunteer pass (DS-58, approved by Michael). Volunteer's roles are cards and its page ends with how to apply; it takes the programme layout (`gs-is-programme-page` knows its old template name until release). Hero images without alt text of their own are decorative (`gs-page-hero`, `gs-exhibition-hero`, `gs-hero`). A card group without a heading follows the text it continues at a group's space (`.gs-section--continues`).
- 0.6.13 (2026-09-26): no Newsletter link in the header (DS-56, Michael); the footer in three rows (DS-57, approved by Michael): logos beside the land acknowledgement (`.gs-footer__top`), columns in fixed places lined up with it, the copyright on its own line.
- 0.6.12 (2026-09-26): home page design pass (DS-55, approved by Michael, keeping the photo edge and button press). Feature panels lead with the programme's logo (`.gs-feature__logo`, `--gs-feature-logo-h`) and alternate their image side; event cards put the programme or exhibition under the date; Visit's text is centred on its photo (`.gs-visit__body`); the artwork hero's mat follows the work's ratio (`--gs-art-ratio`) and its caption sits under the work below 990 px; a hairline inside photos (`--gs-color-media-edge`); buttons shrink while pressed (`--gs-duration-press`, `--gs-ease-press`).
- 0.6.11 (2026-09-26): new home page (DS-54, approved by Michael). New: What's on (`gs-whats-on`, `gs-event-card`), sideways rows on phones (`.gs-rail`, `--gs-rail-item`), the open today line (`gs-open-today`, `gs-open-times`, `js/gs-open.js`; opening days and times in Theme settings), New limited editions (`gs-portfolio-row`). Changed: the hero prefers an installation view; Visit takes a photo; feature panels take a programme and a second link. The Shop feature box leaves the home page.
- 0.6.10 (2026-09-26): Donate and Gordon and Marion pass (DS-53, approved by Michael). Quote figures (`.gs-quote`) as pull quotes; card groups carry their handle as an anchor, with scroll margin; embedded videos keep their own shape (`--gs-video-ratio`) and show the tint while loading.
- 0.6.9 (2026-09-26): The Smith Foundation pass (DS-52, approved by Michael; its five ways to take part under "Get involved"). Card groups that would leave a short last row give the spare room to their first cards (`.gs-grid--lead`, `.gs-grid--odd`); card text wraps with `text-wrap: pretty`.
- 0.6.8 (2026-09-26): programme pages show their release layout at their own address before release. The default page template carries the same two text parts as the programme template; on any other page the first part is all of the text and the second is empty (`snippets/gs-is-programme-page.liquid`, L-08). Delete its list of old template names after release.
- 0.6.7 (2026-09-26): Artists for Kids design pass (DS-51, approved by Michael). The programme template shows the page text's opening before the programmes and its headed sections after them (`gs-page-body` Part setting, `gs-page-text` part); text with figures sets each picture beside its paragraphs (`snippets/gs-text-media.liquid`, `.gs-text-media`); an artwork figure sits on the mat. The headed sections after the programmes take section headings (`gs-text-media` heads). Artists for Kids gains Our Story's sentence on art specialists and fuller print caption, word for word, and a Programs heading over its programmes.
- 0.6.6 (2026-09-26): logo cards (DS-50, approved by Michael): a card with a logo shows it as its heading, and a group of them sets each organisation beside its text. About Us uses them. About's history joins the Artists for Kids page (P-24), so About loses the organisation rows it shared with About Us. Pictures in page text can be figures with captions; an artwork keeps square corners (§6.11). At release `/pages/about` forwards to About Us; Our Story leaves the Shop (P-25). `foundation-full-colour-box` joins the website's logos (§8.1, §8.2); logo card tokens `--gs-org-logo-*`.
- 0.6.5 (2026-09-26): a funder logo without alt text is marked decorative (the credits name the funder). Verification record: `verification/2026-09-26.md`.
- 0.6.4 (2026-09-26): the Shop template's portfolio navigation and feature panel follow the Shop landing setting (DS-49), so Our Story reads as a plain page before its template is reassigned.
- 0.6.3 (2026-09-26): the exhibition lists move into the standard page template, driven by Theme settings (DS-48); `page.exhibitions` and `page.past-exhibitions` removed.
- 0.6.2 (2026-09-26): no Exhibitions overview page (P-20): the lists no longer link to it, the switcher leaves the page template, and its theme setting goes.
- 0.6.1 (2026-09-26): review fixes. Buttons from a section's link setting get the external and PDF cues (feature panel, home hero); card groups without a heading keep heading levels in order; artist names in the facts column no longer break across lines; logo snippets leave out the files' embedded content credentials (§8.1); the product page names its variant select after the product's option.
- 0.6 (2026-09-26): every design decision is decided (DS-40 to DS-45 approved by Michael). The review theme exists: 184767250729.
- 0.5.9 (2026-09-26): Michael approves DS-01 and DS-07. The header logo follows the page's programme (DS-47); page headers no longer repeat a programme logo.
- 0.5.8 (2026-09-26): Michael approves DS-02 to DS-06, DS-08 to DS-10, DS-12 and DS-13. Artwork grids stay at three across (DS-46).
- 0.5.7 (2026-09-26): remaining pages pass. Smaller headings in page text (DS-40), no heading that repeats the title (DS-41), Contact's own text beside the form (DS-42), the switcher on the Exhibitions overview (DS-43), groups of four go two then four across (DS-44), long lists in columns (DS-45). Fixes: the Upcoming Events page no longer shows its title twice; long curator credits stop at two lines on grid cards; `.gs-panel` includes its padding in its width; empty sections no longer break the space after a page header.
- 0.5.6 (2026-09-25): all content migrated for review (`proposals/store-writes/`). Page text that changes at release is staged (DS-39). Videos embedded in page text fill the column at 16:9 (`--gs-ratio-video`, §6.11).
- 0.5.5 (2026-09-25): the build decisions DS-28 to DS-38 are approved by Michael, who approves design decisions for the gallery (P-17). No design change.
- 0.5.4 (2026-09-25): Shop pass, with real product labels and collection credits (`proposals/store-writes/`). Product page split into the buying column and "About the work" (DS-38); tile mediums clamp at two lines; portfolio description sits under the hero. The font audit no longer finds Unicode italics on Shop pages.
- 0.5.3 (2026-09-25): programme pages pass, with real page fields, cards and events (`proposals/store-writes/`). Events titled like their page lead with the date (DS-36); portrait card groups become a people grid (DS-37); links to PDFs say so. Fixed: the Upcoming Events page listed nothing, because the event index's `page` parameter was shadowed by the current page inside the snippet (now `for_page`).
- 0.5.2 (2026-09-25): exhibitions pass, reviewed with real entries (`proposals/store-writes/`). Wide cards on On now and Upcoming (DS-34); exhibition page with the facts beside the text (DS-35, `.gs-about`); installation views aligned to the content column; timezone and live-theme checks in §9.6 answered.
- 0.5.1 (2026-09-25): home page pass. The hero leads with the exhibition on now (DS-30) and its title box widens and lines up with the content column; primary buttons turn ink on tint (DS-31, contrast check now 85 pairings); Visit block on Home (DS-32, §6.13); Home order revised (§7.5). The home heading breaks as GORDON SMITH / GALLERY (DS-33, §4.3).
- 0.5 (2026-09-25): the new theme is built (P-13, P-14). §9 rewritten for it. New components in §6.13; section spacing by collapsing margins (§5.1); page and programme templates gain card groups and events (P-16); Past Exhibitions from entries only (DS-25). DS-27 (no announcement bar, supersedes DS-26) decided; DS-28 (fields read in Liquid) and DS-29 (built-in utility links) proposed; Q11 added. The gs- snippets moved into `theme/snippets/`; `scripts/sync_theme.py` added; Mulish bundled.
- 0.4.2 (2026-09-25): the site gets a new theme built from Shopify's Skeleton theme (P-13, P-14), so §9 is marked for rewrite; DS-25 (all past exhibitions as entries) and DS-26 (header announcements) decided; Past Exhibitions is a normal template in the rules; Q5 answered by the approved menu map.
- 0.4.1 (2026-09-25): content model approved (DS-14 to DS-16); exhibition fields revised from a review of the content in use (`proposals/content-model.md` part 2); exhibition template spec lists the new details; option B fallback template removed; customer account templates added to the template rules as system templates; DS-24 decided: Past Exhibitions lists past entries automatically above the archive.

- 0.4 (2026-09-25): skill-review fixes, with the brand guide as the source of truth for brand essence (DS-17 to DS-23). Hero and page titles fit their box down to 320 px; navigation and Menu drawer rebuilt on `<details>` so they work without JavaScript, with a new `gs-header` snippet and slimmer script; dropdowns near the right edge open leftwards; forced-colours support for icons, panels and the switcher; hover only with a mouse, `:active` for touch, 44 px touch targets; switcher wraps and marks the current item in the link-line colour; box colour reserved for the brand's boxes (tint link fills, rule-colour selection, dropdown edge and quote rule, ink On now chip); standalone links underlined, arrow only on "more" links; status chip plus dates instead of eyebrow strings; empty, error, submitting, done and disabled states with default wording and a system error colour; `gs-media` presets with a linter rule, and no empty box for a missing image; motion reduced to 120 ms fades plus the chevron, with a 120 ms dropdown reveal; header stays static; preview rebuilt with real store content; contrast check now 79 pairings.

- 0.3 (2026-09-25): navigation model changed (DS-11): sections with pages are single buttons with the main page first in the dropdown; inline nav from 1200 px with utility links in a row above; snippet checks updated; live-menu changes listed in §6.1.
- 0.2 (2026-09-25): page templates layer (§7) grounded in a read-only store snapshot; sibling navigation, image gallery, artwork hero and compact card; fixed-overlap photo hero; click-only navigation behaviour with tested JS; enforcement in code (draft Liquid snippets, theme linter with tests, font audit, logo snippet builder); fallback-font guards; content-model proposal.
- 0.1 (2026-09-25): first draft from brand guide, logo guide and logo files. Tokens, reference components, logo set, contrast check, preview page.
