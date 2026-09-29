# Gordon Smith Gallery website

A new Shopify theme for gordonsmithgallery.com (store `ed35ee-ea.myshopify.com`), built as if from scratch on Shopify's Skeleton theme (P-13, P-14 in `DECISIONS.md`). Rules for store targets, Git, Shopify CLI and writing: @AGENTS.md

## Where things are

- Plan: `IMPLEMENTATION_PLAN.md`. Status and what's blocked: `PROJECT.md`. Decisions: `DECISIONS.md`. Requirements (29, with source wording): `REQUIREMENTS.md`.
- Design specification: `design-system/DESIGN.md` (§9 maps it onto the theme). Tokens are the only source of values (`design-system/tokens.css`); components in `components.css`; scripts in `js/`; checks in `design-system/scripts/`.
- The theme: `theme/`. Its `gs-` snippets, sections, templates and wording (`locales/en.default.json`) are edited there. `assets/gs-tokens.css`, `gs-components.css`, `gs-nav.js`, `gs-forms.js` and `snippets/gs-logo-*.liquid` are copies: edit the design-system file, then run `python3 design-system/scripts/sync_theme.py theme/`.
- Content model (page fields, exhibitions, product labels, card groups, events): `design-system/proposals/content-model.md`.
- For search and answer engines: the review and what is built, `proposals/aeo-geo-review.md`; the content side (the four entities, the 32 questions, how to measure), `aeo/`.
- The links between pages (the rules, what each kind of page links to, the check): `proposals/internal-linking-review.md`; names in texts, `proposals/linked-names.md`.
- What the current theme holds and where it goes: `proposals/content-migration.md`. Store changes for review and release: `proposals/store-changes.md`.
- The old Foundation site's addresses (smithfoundation.co) and the redirect file for its server, to upload now the site is live: `proposals/foundation-redirects/`.
- The old theme (Colorblock, ID `183162372393`, live until the release) is in `baseline/theme/` as a reference for content and placement only. Don't copy its code or settings, and never write to it: the store keeps it unchanged for rollback.

## Current phase: released on 2026-09-29

The new theme is live: `184767250729` "Gordon Smith Gallery", from `main` at dee1885, published with Michael's approval. The review theme is `184823611689`, made from `main` the same day, and follows `main`. What was done, checked and found: `verification/2026-09-29-release-gate.md` and `proposals/store-writes/README.md`, "2026-09-29: the release". Design decisions are decided as they are made: `DECISIONS.md` marks each one Decided or Proposed, and nothing Proposed ships.

- **Everything in the store is live now.** A page, a menu, an entry, a field, a product: a visitor sees a change the moment it is written. Every store write needs Michael's go-ahead, a before-snapshot and an undo step, and is logged in `proposals/store-writes/README.md`.
- **Never push to `184767250729`.** It was the review theme until the release, and records from before it give a push command for it. The review theme now is `184823611689`. A merged change is on the live site only after a release Michael approves (`AGENTS.md`).
- Still open after release: `verification/2026-09-29-release-gate.md`, "Still open after release".

- Work the loop in the plan's "How we iterate": branch from `main`, work against the development theme, design system first, record decisions as Proposed for Michael, open a pull request. After Michael merges, update the review theme from `main`, checking its editor JSON first. Staff may edit the live theme in its editor: before a release, bring those changes into Git too.
- Open work: the plan's "Iteration backlog", and what is left of its "Release backlog" (the staff and newsletter tests, the gallery's approvals). The plan still reads as before the release; Michael says when it changes.
- `custom.release_body` is gone: a page's text is the page's own text again (DS-39), and a page's template alone decides its layout (L-08). `custom.release_description` stays until the descriptions move to the search engine listings (`store-changes.md` §8d).
- Another session may be working in this repo at the same time: pull `main` before starting, and merge `main` into your branch if it moved.

## Commands

- Preview while building: `shopify theme dev --store ed35ee-ea.myshopify.com --path theme` (a hidden development theme; last used: 184806277417).
- Review theme: `shopify theme push --store ed35ee-ea.myshopify.com --path theme --theme 184823611689 --strict`, only from `main` or a reviewed branch, after bringing any theme editor changes into Git (`AGENTS.md`). Preview: https://ed35ee-ea.myshopify.com?preview_theme_id=184823611689. `?view=` still previews any template on a page.
- Checks: `shopify theme check --path theme`, `python3 design-system/scripts/lint_theme.py theme/ --strict`, `python3 design-system/scripts/tests/test_lint_theme.py`, `python3 design-system/scripts/check_contrast.py`, `python3 design-system/scripts/sync_theme.py theme/ --check`.
- Structured data, titles and descriptions as a page sends them: `python3 design-system/scripts/check_structured_data.py <url> ...` against a preview link or the `theme dev` address; its tests, `python3 design-system/scripts/tests/test_check_structured_data.py`.
- The questions the site must answer: `python3 design-system/scripts/check_answers.py <address>` (the `theme dev` address or a preview address, no path; `--theme <id>` with the store's address reads an unpublished theme); its tests, `python3 design-system/scripts/tests/test_check_answers.py`. The questions are in `design-system/scripts/answers.json`.
- The links between pages: `python3 design-system/scripts/check_links.py <address>` (the `theme dev` address, the live site's, or the store's with `--theme <id>`); it reads every page, about three minutes. Run it on the live site after any change to a page's template: it is the check that caught the release's one fault. Its limits are in `design-system/scripts/links.json`; its tests, `python3 design-system/scripts/tests/test_check_links.py`.
- Rendered fonts: `python3 design-system/scripts/audit_fonts.py <url> ...` against the theme's preview link (`?preview_theme_id=<id>`); the `theme dev` address never goes network-idle.
- Shopify docs, API schemas and Liquid validation: Shopify's Dev MCP server (`claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest`).

## Working here vs in Cowork

- On Michael's Mac, use git normally: `origin` is SSH and his key works. The Cowork VM notes in `AGENTS.md` (external git directory, deploy key) apply only in Cowork.
- The gallery approval doc and the Shopify Admin connector live in the Cowork project. Store writes (field definitions, entries, redirects) need Michael's approval whichever tool makes them.
