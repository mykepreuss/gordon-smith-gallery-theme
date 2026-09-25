# Gordon Smith Gallery website: project status

Plan: `IMPLEMENTATION_PLAN.md`. Requirements: `REQUIREMENTS.md`. Decisions: `DECISIONS.md`. Rules: `AGENTS.md`. Baseline evidence: `BASELINE.md`.

## Milestones

| # | Milestone (plan step) | Status | Evidence |
| --- | --- | --- | --- |
| 0 | Design specification (`design-system/`, v0.4) | Done, pending gallery approval of the structural parts | `design-system/DESIGN.md`, `design-system/preview.html` |
| 1 | Source of truth: Git repo, untouched live-theme baseline, records | In progress | `BASELINE.md` |
| 1a | Baseline evidence: screenshots, store manifest, Mailchimp audit, Theme Check and linter baselines | In progress (Theme Check and linter wait on the theme pull) | `baseline/` |
| 1b | Gallery approval package: menu map, page hierarchy, editor model, access placement, store-level field proposal, inputs list | Drafted, to be sent by Michael | `proposals/`, shared doc |
| 2 | Implementation on a feature branch, after structural approval | Not started (gated on 1b) | |
| 3 | Pull request with code, register, proposed store changes, Theme Check | Not started | |
| 4 | Unpublished review theme (duplicate of baseline), CLI pushes to its ID only | Not started | |
| 5 | Verification: 1440 / 768 / 390, touch, keyboard, staff editing on two pages of one template, newsletter test | Not started | |
| 6 | Release approval, publish, apply approved store changes, post-release check | Not started | |

## Requirement status

29 requirements, all **Not started** (read-only discovery and design work are not completion evidence). See `REQUIREMENTS.md`.

## Waiting on

| Item | From | Blocks |
| --- | --- | --- |
| Approval of the menu map, page hierarchy, editor model and access placement | Gallery | Milestone 2 |
| Approval of the content model (page fields, exhibition entries, product label fields) | Gallery | REUSE-01, DS-14 to DS-16 |
| Menu labels, signup wording and destination, consent wording, contact emails, phone, hours, social URLs | Gallery | NAV-02, ACCESS-01 to ACCESS-04 |
| Mailchimp for Shopify app settings (customer sync, audience, consent) | Gallery or Michael | ACCESS-01 |
| Artists for Kids external site address and links (Q5) | Gallery | NAV-04 |
| Whether current exhibition page URLs must stay unchanged (Q7) | Gallery | EXH-02, content model part 2 |

## Limitation log (REUSE-04)

| # | Limitation | Evidence | Recommended path |
| --- | --- | --- | --- |
| L-01 | A JSON template's section settings are shared by every page on it, so per-page heroes and intros led to one template per page (32 published pages on 28 page templates, 25 of them serving one page) | `baseline/store-manifest.md` | Page fields read through dynamic sources; closed template set (DS-14) |
| L-02 | Mailchimp's storefront script is injected through a ScriptTag, which Shopify stops injecting on 2027-03-01 | `baseline/mailchimp-audit.md` | Native newsletter form plus app customer sync, or an app embed |
| L-03 | Product titles carry Unicode italic letters for artwork titles, which the site font can't render as intended and search can't match | `baseline/store-manifest.md` | Plain-text titles plus label fields (DS-16) |
| L-04 | Focal-point support depends on how each image is rendered; the current banner ignores it | Plan discovery | `image_tag` through `gs-media`; verify in the review theme (IMG-03) |
