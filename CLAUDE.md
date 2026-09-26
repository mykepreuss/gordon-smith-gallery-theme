# Gordon Smith Gallery website

A new Shopify theme for gordonsmithgallery.com (store `ed35ee-ea.myshopify.com`), built as if from scratch on Shopify's Skeleton theme (P-13, P-14 in `DECISIONS.md`). Rules for store targets, Git, Shopify CLI and writing: @AGENTS.md

## Where things are

- Plan: `IMPLEMENTATION_PLAN.md`. Status and what's blocked: `PROJECT.md`. Decisions: `DECISIONS.md`. Requirements (29, with source wording): `REQUIREMENTS.md`.
- Design specification: `design-system/DESIGN.md` (§9 maps it onto the theme). Tokens are the only source of values (`design-system/tokens.css`); components in `components.css`; scripts in `js/`; checks in `design-system/scripts/`.
- The theme: `theme/`. Its `gs-` snippets, sections, templates and wording (`locales/en.default.json`) are edited there. `assets/gs-tokens.css`, `gs-components.css`, `gs-nav.js`, `gs-forms.js` and `snippets/gs-logo-*.liquid` are copies: edit the design-system file, then run `python3 design-system/scripts/sync_theme.py theme/`.
- Content model (page fields, exhibitions, product labels, card groups, events): `design-system/proposals/content-model.md`.
- What the current theme holds and where it goes: `proposals/content-migration.md`. Store changes for review and release: `proposals/store-changes.md`.
- The live theme (Colorblock, ID `183162372393`) is in `baseline/theme/` as a reference for content and placement only. Don't copy its code or settings, and never write to it.

## Next body of work (plan step 5, then release)

The theme is built, all content is migrated, every design decision is decided, and the review theme exists (`184767250729`, from `main` at 594eb01). The to-do list is the plan's "Remaining work before release". In order:

1. The two release scripts, each with a dry run: template reassignment and staged page text (`proposals/store-changes.md` §3, §8). The frames step (§9) goes in with them.
2. Verification (plan step 5), on the review theme: the still-to-verify list in DESIGN.md §9.6, the date-driven checks, the font audit, the newsletter test and the staff editing test.
3. The release gate (plan, "Release gate and rollback").

Store writes (definitions, entries, field values, menus) need Michael's go-ahead and a before-snapshot, and are logged in `proposals/store-writes/README.md`. Page text that changes at release is staged in `custom.release_body` (DS-39), never written to the live page.

## Commands

- Preview while building: `shopify theme dev --store ed35ee-ea.myshopify.com --path theme` (a hidden development theme; last used: 184755814697).
- Review theme: `shopify theme push --store ed35ee-ea.myshopify.com --path theme --theme 184767250729 --strict`, only from `main` or a reviewed branch, after bringing any theme editor changes into Git (`AGENTS.md`). Preview: https://ed35ee-ea.myshopify.com?preview_theme_id=184767250729. Preview a page on its new template with `?view=`, e.g. `/pages/on-now?view=exhibitions`, until templates are reassigned at release.
- Checks: `shopify theme check --path theme`, `python3 design-system/scripts/lint_theme.py theme/ --strict`, `python3 design-system/scripts/tests/test_lint_theme.py`, `python3 design-system/scripts/check_contrast.py`, `python3 design-system/scripts/sync_theme.py theme/ --check`.
- Rendered fonts: `python3 design-system/scripts/audit_fonts.py <url> ...` against the theme's preview link (`?preview_theme_id=<id>`); the `theme dev` address never goes network-idle.
- Shopify docs, API schemas and Liquid validation: Shopify's Dev MCP server (`claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest`).

## Working here vs in Cowork

- On Michael's Mac, use git normally: `origin` is SSH and his key works. The Cowork VM notes in `AGENTS.md` (external git directory, deploy key) apply only in Cowork.
- The gallery approval doc and the Shopify Admin connector live in the Cowork project. Store writes (field definitions, entries, redirects) need Michael's approval whichever tool makes them.
