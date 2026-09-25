# Gordon Smith Gallery website

A new Shopify theme for gordonsmithgallery.com (store `ed35ee-ea.myshopify.com`), built as if from scratch on Shopify's Skeleton theme (P-13, P-14 in `DECISIONS.md`). Rules for store targets, Git, Shopify CLI and writing: @AGENTS.md

## Where things are

- Plan: `IMPLEMENTATION_PLAN.md`. Status and what's blocked: `PROJECT.md`. Decisions: `DECISIONS.md`. Requirements (29, with source wording): `REQUIREMENTS.md`.
- Design specification: `design-system/DESIGN.md` (§9 maps it onto the theme). Tokens are the only source of values (`design-system/tokens.css`); components in `components.css`; scripts in `js/`; checks in `design-system/scripts/`.
- The theme: `theme/`. Its `gs-` snippets, sections, templates and wording (`locales/en.default.json`) are edited there. `assets/gs-tokens.css`, `gs-components.css`, `gs-nav.js`, `gs-forms.js` and `snippets/gs-logo-*.liquid` are copies: edit the design-system file, then run `python3 design-system/scripts/sync_theme.py theme/`.
- Content model (page fields, exhibitions, product labels, card groups, events): `design-system/proposals/content-model.md`.
- What the current theme holds and where it goes: `proposals/content-migration.md`. Store changes for review and release: `proposals/store-changes.md`.
- The live theme (Colorblock, ID `183162372393`) is in `baseline/theme/` as a reference for content and placement only. Don't copy its code or settings, and never write to it.

## Next body of work (plan steps 3 to 5)

The template set is built on `build-new-theme` (DESIGN.md §9.6 lists what was checked and what's left). Next:

1. Pull request for the build (plan step 3).
2. With Michael's go-ahead: create the field and entry definitions (content model parts 1 to 6) and draft entries, and a review-only copy of the main menu (`proposals/store-changes.md` §1, §4). Additive and invisible under the live theme, but still store writes: log each in the PR.
3. Review theme (plan step 4): `shopify theme push --unpublished`, record its ID and role here and in `AGENTS.md`, then push only to that ID with `--strict`.
4. Verification (plan step 5): the still-to-verify list in DESIGN.md §9.6, the font audit, and the staff editing test.

## Commands

- Preview while building: `shopify theme dev --store ed35ee-ea.myshopify.com --path theme` (a hidden development theme; last used: 184755814697). Preview a page on its new template with `?view=`, e.g. `/pages/on-now?view=exhibitions`, until templates are reassigned at release.
- Checks: `shopify theme check --path theme`, `python3 design-system/scripts/lint_theme.py theme/ --strict`, `python3 design-system/scripts/tests/test_lint_theme.py`, `python3 design-system/scripts/check_contrast.py`, `python3 design-system/scripts/sync_theme.py theme/ --check`.
- Rendered fonts: `python3 design-system/scripts/audit_fonts.py <url> ...` against the theme's preview link (`?preview_theme_id=<id>`); the `theme dev` address never goes network-idle.
- Shopify docs, API schemas and Liquid validation: Shopify's Dev MCP server (`claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest`).

## Working here vs in Cowork

- On Michael's Mac, use git normally: `origin` is SSH and his key works. The Cowork VM notes in `AGENTS.md` (external git directory, deploy key) apply only in Cowork.
- The gallery approval doc and the Shopify Admin connector live in the Cowork project. Store writes (field definitions, entries, redirects) need Michael's approval whichever tool makes them.
