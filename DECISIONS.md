# Decisions

Approved and proposed decisions for the Gordon Smith Gallery site. Full reasoning for the design decisions (DS-) is in `design-system/DESIGN.md` §12; this file is the index and the approval record. Add a row when something is decided; never rewrite an old row, supersede it.

**Status values:** Decided (who, date), Proposed (needs gallery approval through the approval package), Superseded (by which row).

## Project and process

| ID | Decision | Status | Where |
| --- | --- | --- | --- |
| P-01 | The developer notes are the authoritative requirements; the brand guide and logo guide constrain visual work; the brand guide is the source of truth for brand essence | Decided by Michael, 2026-09-25 | `IMPLEMENTATION_PLAN.md`, `DESIGN.md` §12 |
| P-02 | GitHub-first: theme source, register, proposed store changes, decisions and test evidence are reviewed in a private pull request before any release. Private repo `mykepreuss/gordon-smith-gallery-theme` | Decided by Michael, 2026-09-25 | `IMPLEMENTATION_PLAN.md` step 1, `AGENTS.md` |
| P-03 | Nothing on the live store changes until explicit release approval. Read-only discovery only; preview work goes to one designated unpublished theme | Decided (plan) | `IMPLEMENTATION_PLAN.md`, `AGENTS.md` |
| P-04 | Scope excludes platform replacement, a full rewrite, archive rebuild, rebranding, general copy rewriting, paid apps, checkout changes and new shop functionality | Decided (plan); "a full rewrite" superseded by P-13, the rest stands | `IMPLEMENTATION_PLAN.md` "Inputs, exclusions, and known limits" |
| P-05 | Exhibitions leads to On Now (first link in the Exhibitions dropdown); Upcoming and Past sit beside it; the Exhibitions overview page moves to a secondary pathway | Decided by Michael | `IMPLEMENTATION_PLAN.md` "Approved direction" |
| P-06 | Shop leads to the Limited Editions landing page (not Shopify's `/collections` list), with one introduction and one portfolio navigation | Decided by Michael | `IMPLEMENTATION_PLAN.md` "Approved direction" |
| P-07 | Newsletter band above the footer, Contact in the header utility row and footer, social links in the footer | Decided by Michael; gallery supplies values | `IMPLEMENTATION_PLAN.md`, `DESIGN.md` §6.1, §6.9, §6.10 |
| P-08 | Do not build a signup on storefront ScriptTags | Decided (plan) | `baseline/mailchimp-audit.md` |
| P-09 | Exhibitions is the first item in the main menu, ahead of About | Decided by Michael, 2026-09-25 (comment on the approval doc); gallery approves labels | `proposals/store-changes.md` §1 |
| P-10 | Exhibition pages move to Exhibition entries at `/pages/exhibitions/<entry>`. The six old exhibition page addresses redirect to them; the old pages are hidden first, because redirects only work from addresses that no longer load | Approved 2026-09-25 (content model answer 2: "URLs can change, redirects would be a good idea") | `design-system/proposals/content-model.md` part 2, `proposals/store-changes.md` §5 |
| P-11 | Exhibition entries include opening reception, curator and venue, plus the fields added after the review of content in use (dates note, collection artists, events, credits, funder logos, key image caption) | Reception, curator, venue: approved 2026-09-25 (answer 3). Fields from the review: approved with P-16, which replaces the `events` field with event entries | `design-system/proposals/content-model.md` part 2 |
| P-12 | The gallery's admin account creates exhibition entries and fills page fields day to day | Approved 2026-09-25 (answer 4) | `design-system/proposals/content-model.md` part 2 |
| P-13 | Build a new theme for the same store, as if starting from scratch today, instead of modifying the current theme. The developer notes, the approved decisions and `design-system/` drive it; the current theme is a reference for content and placement only. Still Shopify, same store, same products and pages | **Decided by Michael, 2026-09-25** | `IMPLEMENTATION_PLAN.md`, `proposals/content-migration.md` |
| P-14 | The new theme starts from Shopify's Skeleton theme (MIT licence, released May 2025, what `shopify theme init` starts from), not Horizon or the current Colorblock theme. Reason: it's minimal and has no staff design controls to strip out, so the design system supplies the rest; Horizon would mean removing more than keeping | **Decided by Michael, 2026-09-25** | [Skeleton theme](https://github.com/Shopify/skeleton-theme), [changelog](https://shopify.dev/changelog/skeleton-theme-is-now-available) |
| P-15 | The menu map and labels (approval doc section 1), page types (section 2) and contact and newsletter placement (section 4) | **Approved 2026-09-25** | Approval doc, `proposals/store-changes.md` |
| P-16 | Content model parts 4 to 6: card groups, events (replacing the exhibition `events` field from P-11), hero caption, call to action, collection photo credit, product availability note | **Approved by Michael, 2026-09-25**; found by the content inventory | `design-system/proposals/content-model.md` parts 4 to 6 |

## Design system (`design-system/DESIGN.md` §12)

| ID | Decision (short) | Status |
| --- | --- | --- |
| DS-01 | Where the guides disagree, the supplied logo files set the colour values | Proposed; designer to confirm (Q4) |
| DS-02 | Mulish is the web font; Soleil only if the gallery holds an Adobe licence | Proposed (plan already chose Mulish) |
| DS-03 | One rounded corner, bottom-right, site-wide | Proposed |
| DS-04 | Programme theming via `data-gs-brand`; Foundation and Artists for Kids text colours fall back to ink | Proposed |
| DS-05 | Artworks never cropped, rounded, shifted or overlaid | Proposed |
| DS-06 | Inline links keep a designed underline with a tint hover fill | Proposed |
| DS-07 | Header logo: Gallery simple stacked colour box, flush top-left, 64 / 96 px | Proposed; judge in a header mockup (TYPE-04) |
| DS-08 | Hero text in a title box in the programme colour, never on the image | Proposed |
| DS-09 | Newsletter band on tint above an ink footer, on every template | Proposed |
| DS-10 | Headings in capitals; artwork titles italic sentence case | Proposed |
| DS-11 | A section with pages is one button that opens its dropdown; its main page is the first link inside. Replaces the linked-label-plus-caret model | **Decided by Michael, 2026-09-25**; gallery approves labels |
| DS-12 | Photo hero overlaps the image by a fixed amount; artwork hero never overlaps | Proposed |
| DS-13 | Sibling navigation (switcher) on exhibition list and portfolio pages | Proposed |
| DS-14 | Closed set of templates with per-page content in page fields | **Approved 2026-09-25** (content model answers recorded by Michael) |
| DS-15 | Exhibitions as structured entries with status from dates | **Approved 2026-09-25** (content model answers recorded by Michael) |
| DS-16 | Artwork label data in product fields; plain-text product titles | **Approved 2026-09-25** (content model answers recorded by Michael) |
| DS-17 | Capitals stay for headings, subheadings and labels (brand guide pp.11, 15) | **Decided by Michael, 2026-09-25** |
| DS-18 | Eyebrows only when they carry information; status as chip plus dates line | **Decided by Michael, 2026-09-25** |
| DS-19 | Header and dropdowns are native `<details>` and work without JavaScript | **Decided by Michael, 2026-09-25** |
| DS-20 | Standalone links underlined; arrow only on "more of the same list" links | **Decided by Michael, 2026-09-25** |
| DS-21 | Box colour only for the brand's boxes; tints and rules for everything else (brand guide p.11) | **Decided by Michael, 2026-09-25** |
| DS-22 | System error colour `#a3261b` (`#f28b82` on ink) | **Decided by Michael, 2026-09-25** |
| DS-23 | Header not sticky | **Decided by Michael, 2026-09-25** |
| DS-24 | Past Exhibitions lists past entries automatically above the existing archive | **Decided by Michael, 2026-09-25**; amended by DS-25 |
| DS-25 | Past Exhibitions lists all 12 past exhibitions from entries. The six older ones (2020 to 2023) hold title, dates and image and don't link. Reason: the hand-built archive sections don't carry over to the new theme (P-13) | **Decided by Michael, 2026-09-25**; follows from P-13 |
| DS-26 | Up to two short announcements with links in the header, set in theme settings (kept from the current announcement bar) | Decided by Michael, 2026-09-25; **superseded by DS-27** |
| DS-27 | No announcement bar in the header (supersedes DS-26). The home page carries the same news from entries and the newest portfolio | **Decided by Michael, 2026-09-25** ("we do not want that anymore") |
| DS-28 | Page fields and entries are read directly in Liquid, not connected through dynamic sources in the editor | Proposed (build) |
| DS-29 | Header utility links are built in (Contact from the contact-page theme setting, Newsletter, Search, Cart), so no utility menu is created | Proposed (build) |

"Decided by Michael" rows are structural or design-system choices; the gallery still approves labels, copy and anything in the approval package.

## Open questions for the gallery

Q1 to Q10 in `design-system/DESIGN.md` §12 (Q7 and Q9 answered 2026-09-25), the "Still open" list in `design-system/proposals/content-model.md`, plus the inputs listed in the approval package: menu labels, signup wording and destination, consent wording, contact email addresses and phone, hours, social URLs, and any replacement images or captions.
