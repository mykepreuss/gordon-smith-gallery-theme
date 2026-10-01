# Working rules for this repository

For any person or agent (Claude, Codex, or other) working in this repo. These rules add to, and never override, the owner's own instructions. `IMPLEMENTATION_PLAN.md` is the owner's plan: follow it, and change it only when the owner asks.

## Store target

| | |
| --- | --- |
| Store | `ed35ee-ea.myshopify.com` (public domain `gordonsmithgallery.com`) |
| Live theme | `184824725801` "Gordon Smith Gallery", role MAIN since the fourth release, 2026-10-01 at 20:15 UTC (1:15 PM Pacific), from `main` at 220213c. It was the review theme until then, named "Review theme (do not publish)", so older records call it that. **Write to it only as "Small fixes on the live theme" below says.** |
| Rollback theme | `184824398121` "Gordon Smith Gallery (rollback, third release)", role UNPUBLISHED. The live theme from the third release until the fourth, from `main` at 1168190 with the settings of 2026-10-01 (P-66), and the review theme before that. Kept unchanged to roll back the fourth release. **Never write to it.** |
| Earlier rollback themes | `184823611689` "Gordon Smith Gallery (rollback, second release)", the live theme from the second release until the third, from `main` at 8bcfaa7; and `184767250729` "Gordon Smith Gallery (rollback, 2026-09-29)", the live theme from the first release until the second, from `main` at dee1885. Both role UNPUBLISHED, kept unchanged. **Never write to them.** |
| Old theme | `183162372393` "Colorblock: NEW WEBSITE", role UNPUBLISHED since the release. Kept unchanged for rollback. **Never write to it, never delete it.** |
| Review theme | `184856445225` "Review theme (do not publish)", role UNPUBLISHED. Created 2026-10-01 from `main` at 220213c, at the fourth release. It follows `main`: after a merge, push `main` to it (editor JSON checked first) and record the commit in `PROJECT.md`. Push only to this ID |
| How a change goes live | At a release Michael approves: a release publishes the review theme; the theme it replaces is kept for rollback, and a new review theme is made from `main` and written here. Between releases, a small fix to the live theme's settings or page layouts can go live on its own, with Michael's go-ahead (below). Code goes live only at a release |

Before any write to Shopify, recheck: store domain, live theme ID and role, the review theme's ID and `UNPUBLISHED` role, and the CLI account.

## Change surfaces (keep them separate)

1. **Git** owns theme source (`theme/`), the design system (`design-system/`) and project records. The site gets a new theme (P-13): once the build branch lands, `theme/` holds the new theme and `baseline/theme/` the untouched Colorblock theme, kept for reference and drift checks. Don't copy code or settings from the baseline; move content as `proposals/content-migration.md` sets out.
2. **The unpublished review theme** owns preview-only code and settings.
3. **Shopify Admin resources** (menus, pages, page fields, metaobjects, products, collections, Files, redirects) are shared by every theme. A preview theme does not sandbox them. Propose changes to them as files in Git (`proposals/`), and apply them only at an approved preview or release gate.
4. **Installed apps** (Mailchimp) have their own settings and per-theme embeds.

## Shopify CLI

- Theme reads: `shopify theme pull --store ed35ee-ea.myshopify.com --theme <id> --path <folder>`. Never pull into `theme/`, which holds the new theme; pull the live theme into a separate folder for drift checks.
- Preview while building: `shopify theme dev --store ed35ee-ea.myshopify.com --path theme`. It uploads to a hidden development theme, never the live one; allowed during the build. Never pass it the live theme's ID.
- Before a push to the review theme, pull its `config/settings_data.json` and `templates/*.json` into a scratch folder and compare them with Git. Changes made in its theme editor (staff testing) come into Git first, so a push never overwrites them.
- The review theme is shared: every session pushes to the same one, and none sees another's push until it lands. Before a push to it, read the open pull requests (`gh pr list --state open`) and `PROJECT.md`, milestone 4. If either says the review theme is ahead of `main`, stop. Push only once that pull request has merged, or when Michael says to.
- A branch that goes to the review theme merges `main` in first, so the push takes nothing off the theme. Its pull request says so under a "Review theme" heading, with the commit, and `PROJECT.md` records it. After any push, read the theme back (a page, or the pushed files) to see that it held.
- Theme writes: `shopify theme push --theme <verified unpublished id> --strict`. `--allow-live` only for a small fix on the live theme, below. Never `theme push --publish`, never `theme publish` without explicit release approval.

### Small fixes on the live theme

The site is live, so a small fix need not wait for a release. An agent may write to the live theme only when all of these hold:

1. **Michael has said yes to this change,** in the session. A yes to one change isn't a yes to the next.
2. **Only the files the theme editor changes:** `config/settings_data.json`, `templates/*.json`, `templates/metaobject/*.json` and `sections/*.json`. No Liquid, CSS, JavaScript, `locales/` or assets: code goes live only at a release, through the review theme.
3. **The live theme's own file, not Git's.** Pull that file from the live theme into a scratch folder and keep the copy. Compare it with `main`: anything else that differs is an editor change, which stays and comes into Git. Change only what was agreed, and check the difference is only that.
4. **One file at a time:** `shopify theme push --store ed35ee-ea.myshopify.com --theme <live id> --path <scratch folder> --only <file> --allow-live`. Never a whole-theme push to the live theme.
5. **Read it back:** pull the file again, and read the page it changes on gordonsmithgallery.com.
6. **Log it** in `proposals/store-writes/README.md`, with why, the before copy and the undo (push the before copy the same way, or undo it in the editor).
7. **The same change in Git,** through a pull request, and on the review theme once it merges, so the live theme, the review theme and `main` stay alike.

The rollback and old themes are never written to.
- Theme Check: `shopify theme check --path theme` without auto-correct. The new theme has no errors; explain any warning in the pull request. `baseline/theme-check.json` records the old theme for comparison only.
- Admin writes through the Shopify connector or Admin only for approved store-resource changes, with a before-snapshot in `baseline/` or the PR.

## Git

- `main` holds the reviewed state. Work on feature branches and open a pull request; do not push work directly to `main` after the baseline commits.
- The first theme commit is the untouched live theme. Never amend or rewrite it.
- No credentials, tokens, `.env` files or Shopify CLI config in Git.
- Each requirement's row in `REQUIREMENTS.md` changes in the same commit as the work.
- **Remote:** `origin` is `git@github.com:mykepreuss/gordon-smith-gallery-theme.git` (SSH). Michael pushes from his Mac with his own SSH key.
- **Agents in the Cowork VM** push with the repo's deploy key "Claude agent (Cowork VM)", which can write to this repo only. The key lives in `.git/agent/`, so it is never committed. Copy `deploy_key` to a private path in the VM, `chmod 600` it, and run git with `GIT_SSH_COMMAND="ssh -i <that copy> -o IdentitiesOnly=yes -o UserKnownHostsFile=<folder>/.git/agent/known_hosts"`. That `known_hosts` entry was checked against GitHub's published Ed25519 fingerprint. Push branches only, never `main`: the key technically can, so this rule is what stops it. Deploy keys can't open pull requests, so write the title and description to `.git/pr/<branch>.title` and `.git/pr/<branch>.md` (use `_` for `/` in the branch name) and give Michael the filled-in link that `DRY_RUN=1 scripts/push-pr.sh` prints. To revoke: delete the key under the repo's Settings, Deploy keys, and remove `.git/agent/`.
- **Other sandboxed agents** without the key commit on a branch and write the same two files; Michael runs `scripts/push-pr.sh`, which pushes over his SSH key and opens the filled-in form. A GitHub token is used only with Michael's approval for that session, is never written to the repo or its config, and is signed out afterwards.
- **Cowork VM only:** deleting files in the connected folder is blocked, so git can't clean up its own lock files there. Never run git directly on the folder's `.git` from the VM. Instead: check `.git` has no `*.lock` files, make a fresh copy of it outside the folder at the start of each piece of work (never reuse an older copy: Michael may have committed, pushed or pulled on his Mac since), run git with `GIT_DIR` pointing at the copy and `GIT_WORK_TREE` at the folder, then copy it back (objects without overwriting, other files by rename) only after checking that `HEAD`, the refs and `config` in `.git` haven't changed since the copy.

## Design system

- `design-system/DESIGN.md` is the design specification. Tokens in `design-system/tokens.css` are the only source of values; `gs-` code uses semantic tokens only.
- Before a pull request run: `python3 design-system/scripts/check_contrast.py`, `python3 design-system/scripts/lint_theme.py theme/`, `python3 design-system/scripts/tests/test_lint_theme.py` and `python3 design-system/scripts/sync_theme.py theme/ --check`. The new theme passes the linter with no errors; `baseline/lint-theme.txt` records the old theme.
- The brand guide (`reference/GordonSmith-BrandGuide_sm.pdf`) is the source of truth for brand essence.

## Gallery-facing work

Final labels and editorial copy come from the gallery (EXH-04, ACCESS-04). Do not rewrite existing copy. Anything structural goes through the approval package before code.

## Writing

Plain language, short sentences, sentence case. No em dashes or en dashes.
