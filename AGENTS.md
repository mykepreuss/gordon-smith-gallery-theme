# Working rules for this repository

For any person or agent (Claude, Codex, or other) working in this repo. These rules add to, and never override, the owner's own instructions. `IMPLEMENTATION_PLAN.md` is the owner's plan: follow it, and change it only when the owner asks.

## Store target

| | |
| --- | --- |
| Store | `ed35ee-ea.myshopify.com` (public domain `gordonsmithgallery.com`) |
| Live theme | `183162372393` "Colorblock: NEW WEBSITE", role MAIN. **Never write to it.** |
| Review theme | Not created yet. When it is, record its ID here and in `PROJECT.md`, and push only to that ID |

Before any write to Shopify, recheck: store domain, live theme ID and role, the review theme's ID and `UNPUBLISHED` role, and the CLI account.

## Change surfaces (keep them separate)

1. **Git** owns theme source (`theme/`), the design system (`design-system/`) and project records.
2. **The unpublished review theme** owns preview-only code and settings.
3. **Shopify Admin resources** (menus, pages, page fields, metaobjects, products, collections, Files, redirects) are shared by every theme. A preview theme does not sandbox them. Propose changes to them as files in Git (`proposals/`), and apply them only at an approved preview or release gate.
4. **Installed apps** (Mailchimp) have their own settings and per-theme embeds.

## Shopify CLI

- Theme reads: `shopify theme pull --store ed35ee-ea.myshopify.com --theme <id> --path theme`.
- Theme writes: only `shopify theme push --theme <verified unpublished id> --strict`. Never use `--allow-live`, never `theme push --publish`, never `theme publish` without explicit release approval.
- Theme Check: `shopify theme check --path theme` without auto-correct. Compare against `baseline/theme-check.json`; no new unexplained findings.
- Admin writes through the Shopify connector or Admin only for approved store-resource changes, with a before-snapshot in `baseline/` or the PR.

## Git

- `main` holds the reviewed state. Work on feature branches and open a pull request; do not push work directly to `main` after the baseline commits.
- The first theme commit is the untouched live theme. Never amend or rewrite it.
- No credentials, tokens, `.env` files or Shopify CLI config in Git.
- Each requirement's row in `REQUIREMENTS.md` changes in the same commit as the work.
- **Remote:** `origin` is `git@github.com:mykepreuss/gordon-smith-gallery-theme.git` (SSH). Michael pushes from his Mac with his own SSH key.
- **Agents in a sandbox** (the Cowork VM, a cloud session) don't have that key. Commit on a branch and write the pull request title and description to `.git/pr/<branch>.title` and `.git/pr/<branch>.md` (use `_` for `/` in the branch name). Michael then runs `scripts/push-pr.sh`, which pushes the branch and opens GitHub's pull request form filled in. A GitHub token is used only with Michael's approval for that session, is never written to the repo or its config, and is signed out afterwards.
- **Cowork VM only:** deleting files in the connected folder is blocked, so git can't clean up its own lock files there. Never run git directly on the folder's `.git` from the VM. Instead: check `.git` has no `*.lock` files, copy it to a git directory outside the folder, run git with `GIT_DIR` pointing there and `GIT_WORK_TREE` at the folder, then copy it back (objects without overwriting, other files by rename) after checking the folder's branch hasn't moved since the copy.

## Design system

- `design-system/DESIGN.md` is the design specification. Tokens in `design-system/tokens.css` are the only source of values; `gs-` code uses semantic tokens only.
- Before a pull request run: `python3 design-system/scripts/check_contrast.py`, `python3 design-system/scripts/lint_theme.py theme/`, and `python3 design-system/scripts/tests/test_lint_theme.py`. Compare the linter against `baseline/lint-theme.txt`.
- The brand guide (`reference/GordonSmith-BrandGuide_sm.pdf`) is the source of truth for brand essence.

## Gallery-facing work

Final labels and editorial copy come from the gallery (EXH-04, ACCESS-04). Do not rewrite existing copy. Anything structural goes through the approval package before code.

## Writing

Plain language, short sentences, sentence case. No em dashes or en dashes.
