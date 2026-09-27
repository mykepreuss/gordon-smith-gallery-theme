# Gordon Smith Gallery website

A new Shopify theme for gordonsmithgallery.com (store `ed35ee-ea.myshopify.com`), built as if from scratch on Shopify's Skeleton theme (P-13, P-14 in `DECISIONS.md`). Rules for store targets, Git, Shopify CLI and writing: @AGENTS.md

## Where things are

- Plan: `IMPLEMENTATION_PLAN.md`. Status and what's blocked: `PROJECT.md`. Decisions: `DECISIONS.md`. Requirements (29, with source wording): `REQUIREMENTS.md`.
- Design specification: `design-system/DESIGN.md` (§9 maps it onto the theme). Tokens are the only source of values (`design-system/tokens.css`); components in `components.css`; scripts in `js/`; checks in `design-system/scripts/`.
- The theme: `theme/`. Its `gs-` snippets, sections, templates and wording (`locales/en.default.json`) are edited there. `assets/gs-tokens.css`, `gs-components.css`, `gs-nav.js`, `gs-forms.js` and `snippets/gs-logo-*.liquid` are copies: edit the design-system file, then run `python3 design-system/scripts/sync_theme.py theme/`.
- Content model (page fields, exhibitions, product labels, card groups, events): `design-system/proposals/content-model.md`.
- What the current theme holds and where it goes: `proposals/content-migration.md`. Store changes for review and release: `proposals/store-changes.md`.
- The live theme (Colorblock, ID `183162372393`) is in `baseline/theme/` as a reference for content and placement only. Don't copy its code or settings, and never write to it.

## Current phase: iterating (release on hold)

The theme is built, all content is migrated, every design decision is decided (DS-01 to DS-66), and the review theme (`184767250729`) follows `main`. Michael has put release on hold: we keep improving the site until he decides to go ahead.

- Work the loop in the plan's "How we iterate": branch from `main`, work against the development theme, design system first, record decisions as Proposed for Michael, open a pull request. After Michael merges, update the review theme from `main`, checking its editor JSON first.
- Open work: the plan's "Iteration backlog". The "Release backlog" (release scripts, verification, staff and newsletter tests, the release gate) waits until Michael says to release.
- Nothing the live site shows changes before release. Store writes are limited to the kinds under "Store writes before release", need Michael's go-ahead and a before-snapshot, and are logged in `proposals/store-writes/README.md`. A page's own text is staged in `custom.release_body` (DS-39).
- Another session may be working in this repo at the same time: pull `main` before starting, and merge `main` into your branch if it moved.

## Commands

- Preview while building: `shopify theme dev --store ed35ee-ea.myshopify.com --path theme` (a hidden development theme; last used: 184755814697).
- Review theme: `shopify theme push --store ed35ee-ea.myshopify.com --path theme --theme 184767250729 --strict`, only from `main` or a reviewed branch, after bringing any theme editor changes into Git (`AGENTS.md`). Preview: https://ed35ee-ea.myshopify.com?preview_theme_id=184767250729. Every page shows its release layout at its own address: the exhibition lists follow Theme settings (DS-48), and the programme pages are recognised by their old template names until release (`snippets/gs-is-programme-page.liquid`, L-08). `?view=` still previews any template.
- Checks: `shopify theme check --path theme`, `python3 design-system/scripts/lint_theme.py theme/ --strict`, `python3 design-system/scripts/tests/test_lint_theme.py`, `python3 design-system/scripts/check_contrast.py`, `python3 design-system/scripts/sync_theme.py theme/ --check`.
- Rendered fonts: `python3 design-system/scripts/audit_fonts.py <url> ...` against the theme's preview link (`?preview_theme_id=<id>`); the `theme dev` address never goes network-idle.
- Shopify docs, API schemas and Liquid validation: Shopify's Dev MCP server (`claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest`).

## Working here vs in Cowork

- On Michael's Mac, use git normally: `origin` is SSH and his key works. The Cowork VM notes in `AGENTS.md` (external git directory, deploy key) apply only in Cowork.
- The gallery approval doc and the Shopify Admin connector live in the Cowork project. Store writes (field definitions, entries, redirects) need Michael's approval whichever tool makes them.
