# Gordon Smith Gallery website

A new Shopify theme for gordonsmithgallery.com (store `ed35ee-ea.myshopify.com`), built as if from scratch on Shopify's Skeleton theme (P-13, P-14 in `DECISIONS.md`). Rules for store targets, Git, Shopify CLI and writing: @AGENTS.md

## Where things are

- Plan: `IMPLEMENTATION_PLAN.md`. Status and what's blocked: `PROJECT.md`. Decisions: `DECISIONS.md`. Requirements (29, with source wording): `REQUIREMENTS.md`.
- Design specification: `design-system/DESIGN.md`. Tokens are the only source of values (`design-system/tokens.css`); components in `components.css`; draft `gs-` snippets in `design-system/liquid/`; checks in `design-system/scripts/`.
- Content model (page fields, exhibitions, product labels, card groups, events): `design-system/proposals/content-model.md`.
- What the current theme holds and where it goes: `proposals/content-migration.md`. Store changes for release: `proposals/store-changes.md`.
- The live theme (Colorblock, ID `183162372393`) is a reference for content and placement only. Don't copy its code or settings, and never write to it.

## Next body of work (plan step 2)

On a branch from `main`:

1. Move the untouched baseline from `theme/` to `baseline/theme/` with `git mv`, then start `theme/` from Shopify's Skeleton theme (`shopify theme init`, without its `.git`).
2. Rewrite `design-system/DESIGN.md` §9 for the new theme. Bring in the tokens, components and `gs-` snippets, and bundle Mulish (OFL) as theme assets.
3. Build the approved template set (DESIGN.md §7.4, §7.5): header and navigation (DS-11, DS-19, menu order P-09), footer, newsletter band, announcements (DS-26), exhibitions from entries (DS-15, DS-24, DS-25), page fields, card groups and events (content model parts 1, 4, 5), and the shop templates.
4. Theme Check and the design-system linter with no errors, then open a pull request. The review theme (plan step 4) and any store writes wait for Michael's go-ahead.

## Commands

- Preview while building: `shopify theme dev --store ed35ee-ea.myshopify.com --path theme`.
- Checks: `shopify theme check --path theme`, `python3 design-system/scripts/lint_theme.py theme/`, `python3 design-system/scripts/tests/test_lint_theme.py`, `python3 design-system/scripts/check_contrast.py`.
- Shopify docs, API schemas and Liquid validation: Shopify's Dev MCP server (`claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest`).

## Working here vs in Cowork

- On Michael's Mac, use git normally: `origin` is SSH and his key works. The Cowork VM notes in `AGENTS.md` (external git directory, deploy key) apply only in Cowork.
- The gallery approval doc and the Shopify Admin connector live in the Cowork project. Store writes (field definitions, entries, redirects) need Michael's approval whichever tool makes them.
