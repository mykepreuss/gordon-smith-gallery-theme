# Gordon Smith Gallery website: project status

Plan: `IMPLEMENTATION_PLAN.md`. Requirements: `REQUIREMENTS.md`. Decisions: `DECISIONS.md`. Rules: `AGENTS.md`. Baseline evidence: `BASELINE.md`.

## Milestones

| # | Milestone (plan step) | Status | Evidence |
| --- | --- | --- | --- |
| 0 | Design specification (`design-system/`, v0.4.1) | Done, pending gallery approval of the structural parts | `design-system/DESIGN.md`, `design-system/preview.html` |
| 1 | Source of truth: Git repo, untouched live-theme baseline, records | Done 2026-09-25 | `BASELINE.md`, first theme commit |
| 1a | Baseline evidence: screenshots, store manifest, Mailchimp audit, Theme Check and linter baselines | Done 2026-09-25, except Mailchimp app settings (need access) | `baseline/` |
| 1b | Gallery approval package: menu map, page hierarchy, editor model, access placement, store-level field proposal, inputs list | Content model approved 2026-09-25 (all three parts); menu map, page types, editing model and contact placement still to approve | `proposals/`, shared doc, `DECISIONS.md` P-10 to P-12 |
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
| Menu labels, signup wording and destination, consent wording, contact emails, phone, hours, social URLs | Gallery | NAV-02, ACCESS-01 to ACCESS-04 |
| Mailchimp for Shopify app settings (customer sync, audience, consent) | Gallery or Michael | ACCESS-01 |
| Artists for Kids external site address and links (Q5) | Gallery | NAV-04 |
| Room names for the exhibition venue field, the label for the second artist group, *Stitched* start date (content model "Still open") | Gallery | Exhibition entries (defaults apply until answered) |
| DS-24: automatic list of past entries on Past Exhibitions | Michael | Past Exhibitions template |

## Limitation log (REUSE-04)

| # | Limitation | Evidence | Recommended path |
| --- | --- | --- | --- |
| L-01 | A JSON template's section settings are shared by every page on it, so per-page heroes and intros led to one template per page (32 published pages on 28 page templates, 25 of them serving one page) | `baseline/store-manifest.md` | Page fields read through dynamic sources; closed template set (DS-14) |
| L-02 | Mailchimp's storefront script is injected through a ScriptTag, which Shopify stops injecting on 2027-03-01 | `baseline/mailchimp-audit.md` | Native newsletter form plus app customer sync, or an app embed |
| L-03 | Product titles carry Unicode italic letters for artwork titles, which the site font can't render as intended and search can't match | `baseline/store-manifest.md` | Plain-text titles plus label fields (DS-16) |
| L-04 | Focal-point support depends on how each image is rendered; the current banner ignores it | Plan discovery | `image_tag` through `gs-media`; verify in the review theme (IMG-03) |
| L-05 | Blocks generated in the theme editor sit outside the theme's system: the rotating banner (used in 10 templates) has 85 staff settings, and both cart frame blocks use a filter Theme Check doesn't recognise | `baseline/theme-check.txt` | Replace the banner with the `gs` hero (IMG-04); report the frame blocks to the gallery (outside scope) |
