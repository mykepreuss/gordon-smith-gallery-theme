# Gordon Smith Gallery website: project status

Plan: `IMPLEMENTATION_PLAN.md`. Requirements: `REQUIREMENTS.md`. Decisions: `DECISIONS.md`. Rules: `AGENTS.md`. Baseline evidence: `BASELINE.md`.

**Current phase (from 2026-09-26): iterating on the site in the review theme. Release is on hold until Michael decides to go ahead.** How changes flow: the plan, "How we iterate". Open work: the plan's "Iteration backlog" and "Release backlog".

## Milestones

| # | Milestone (plan step) | Status | Evidence |
| --- | --- | --- | --- |
| 0 | Design specification (`design-system/`, v0.5) | Done; structural parts approved 2026-09-25 (P-15); §9 rewritten for the new theme | `design-system/DESIGN.md`, `design-system/preview.html` |
| 1 | Source of truth: Git repo, untouched live-theme baseline, records | Done 2026-09-25 | `BASELINE.md`, first theme commit |
| 1a | Baseline evidence: screenshots, store manifest, Mailchimp audit, Theme Check and linter baselines | Done 2026-09-25, except Mailchimp app settings (need access) | `baseline/` |
| 1b | Gallery approval package: menu map, page hierarchy, editor model, access placement, store-level field proposal, inputs list | Approved 2026-09-25: content model parts 1 to 3, menu map and labels, page types, editing model, contact and newsletter placement. Content model parts 4 to 6 approved the same day (P-16) | `proposals/`, shared doc, `DECISIONS.md` P-10 to P-16 |
| 1c | Content inventory of the current theme, for the new build | Done 2026-09-25 | `proposals/content-migration.md` |
| 2 | Build the new theme on a feature branch (P-13), from Shopify's Skeleton theme (P-14) | Template set built on `build-new-theme`, 2026-09-25, then design passes with real content for Home, Exhibitions, the programme pages and Shop. All content migrated 2026-09-25: every page, exhibition, card and menu is in the store or the theme, with the page text that changes at release staged (DS-39). Checked in development theme 184755814697. Design pass on every remaining page and the review fixes done 2026-09-26. Every design decision decided 2026-09-26 (DS-01 to DS-50) | `theme/`, DESIGN.md §9.6, `proposals/store-writes/` |
| 3 | Pull request with code, register, proposed store changes, Theme Check | Done: [PR #4](https://github.com/mykepreuss/gordon-smith-gallery-theme/pull/4) merged 2026-09-25; [PR #5](https://github.com/mykepreuss/gordon-smith-gallery-theme/pull/5) and [PR #6](https://github.com/mykepreuss/gordon-smith-gallery-theme/pull/6) merged 2026-09-26. Further changes in smaller pull requests (plan step 3) | Theme Check 0 offences; lint 0 errors, 0 warnings |
| 4 | Unpublished review theme (the new theme uploaded unpublished), CLI pushes to its ID only | Done 2026-09-26: `184767250729` "New theme for review (do not publish)", role unpublished. Last pushed from d0d50d0; matches `main` at 1ad4dba (no theme files changed since). Editor JSON checked before each push: no staff changes so far | Preview https://ed35ee-ea.myshopify.com?preview_theme_id=184767250729; editor https://ed35ee-ea.myshopify.com/admin/themes/184767250729/editor |
| 4a | Iterate on the site in the review theme (current phase) | In progress from 2026-09-26: branch, pull request, `main`, then the review theme (plan, "How we iterate") | Plan, "Iteration backlog" |
| 5 | Verification: 1440 / 768 / 390, touch, keyboard, staff editing on two pages of one template, newsletter test | Agent checks done 2026-09-26 (`verification/2026-09-26.md`): pages, widths, keyboard, no-JavaScript menu, links, fonts, contact form address. Waiting: focal points (Michael), the date checks, the staff and newsletter tests | Plan, "Release backlog" |
| 6 | Release approval, publish, apply approved store changes, post-release check | On hold until Michael decides to release | Plan, "Release gate and rollback" |

## Requirement status

29 requirements: 26 **In progress** (built in the new theme, not yet verified in a review theme with staff) and 3 **Blocked** on gallery input (ACCESS-01, ACCESS-03, ACCESS-04). Nothing is Done: Done needs storefront and staff-editing evidence. See `REQUIREMENTS.md`.

## Waiting on

All the gallery's questions, in one list to send: `proposals/gallery-questions.md`.

| Item | From | Blocks |
| --- | --- | --- |
| Signup wording, consent wording, the site email, social URLs; confirming the hours and phone taken from the current site | Gallery | ACCESS-01 to ACCESS-04 |
| Mailchimp for Shopify app settings (customer sync, audience, consent) | Gallery or Michael | ACCESS-01 |
| Room names for the exhibition venue field, the label for the second artist group, *Stitched* start date (content model "Still open") | Gallery | Exhibition entries (defaults apply until answered) |
| Land acknowledgement font (Q11): accept Arial for the characters Mulish lacks, or load a font for BC Indigenous languages | Gallery | L-06 |
| Checks from the migration and page pass: the Donate "Online Form" card (the form is off), Carl Heywood in *Collect, Assemble, Gather*, a broken *Stitched* credit link, About and About Us as two pages, three artist names that may be misspelled (`proposals/store-writes/README.md`) | Gallery | Nothing; the review shows today's content |

## Limitation log (REUSE-04)

| # | Limitation | Evidence | Recommended path |
| --- | --- | --- | --- |
| L-01 | A JSON template's section settings are shared by every page on it, so per-page heroes and intros led to one template per page (32 published pages on 28 page templates, 25 of them serving one page) | `baseline/store-manifest.md` | Page fields read through dynamic sources; closed template set (DS-14) |
| L-02 | Mailchimp's storefront script is injected through a ScriptTag, which Shopify stops injecting on 2027-03-01 | `baseline/mailchimp-audit.md` | Native newsletter form plus app customer sync (chosen, P-18); the ScriptTag isn't used |
| L-03 | Product titles carry Unicode italic letters for artwork titles, which the site font can't render as intended and search can't match | `baseline/store-manifest.md` | Plain-text titles plus label fields (DS-16). Label fields filled 2026-09-25, so the new theme no longer shows the styled letters; the titles themselves change at release |
| L-04 | Focal-point support depends on how each image is rendered; the current banner ignores it | Plan discovery | `image_tag` through `gs-media`; verify in the review theme (IMG-03) |
| L-05 | Blocks generated in the theme editor sit outside the theme's system: the rotating banner (used in 10 templates) has 85 staff settings, and both cart frame blocks use a filter Theme Check doesn't recognise | `baseline/theme-check.txt` | Replace the banner with the `gs` hero (IMG-04); report the frame blocks to the gallery (outside scope) |
| L-06 | Mulish has no glyphs for some characters in the land acknowledgement's Squamish, Tsleil-Waututh and Musqueam place names (ʔ, ɬ, θ, some combining marks); 12 characters render in Arial | `audit_fonts.py` on development theme 184755814697 | Gallery decides (Q11): accept, or load a font made for BC Indigenous languages for that text |
| L-07 | Liquid loops read at most 50 entries without pagination, so the exhibition and event lists read the first 50 active entries of each type | `snippets/gs-exhibition-index.liquid`, `gs-event-index.liquid` | Fine for today (15 exhibitions); paginate the Past list if the archive passes 50 |
| L-08 | Pages keep their old template names until release, and the new theme doesn't have most of them, so they fall back to the default page template in preview. Every page still shows correctly: the exhibition lists come from Theme settings (DS-48), and Our Story, whose `shop` name picks up the Shop template, reads as a plain page there (DS-49) | Development and review theme checks, 2026-09-26 | Reassign templates by script after publishing, so the admin shows the right template names; the script is written and dry-run before release (`proposals/store-changes.md` §3) |
