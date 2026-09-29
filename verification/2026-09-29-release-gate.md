# Release gate, 2026-09-29

Michael, 2026-09-29: "We're ready to put the new theme live". This is the package the plan asks for before release approval ("Release gate and rollback"). Everything here was read only: nothing was written to the store or to any theme.

**Approved:** Michael, 2026-09-29, after reading this package: "Everything is approved", "Supporters confirmed, keep in", "All good, release as is" (the consent wording), "Proceed with your recommendation" (the writes from files), "Everything can be put live now". What was done is under "The release" at the end.

**The candidate moved before the approval.** #119 and #122 merged after the first checks, and the review theme was pushed with #122 (the Home row of works from the collection, DS-188, decided). The checks below were run again on that candidate, and the table shows the second run.

## What is being released

| | |
| --- | --- |
| Store | `ed35ee-ea.myshopify.com`, "Artists for Kids & The Gordon Smith Gallery", gordonsmithgallery.com (connector and CLI agree) |
| Live theme | `183162372393` "Colorblock: NEW WEBSITE", role live. Kept for rollback |
| Candidate | `184767250729` "New theme for review (do not publish)", role unpublished |
| Git commit | `main` at dee1885 (after #122). The theme's files last changed at db338ed (#122). First checked at 5d498ae |
| Theme checksum | Git tree of `theme/`: `e8426474494513f298191e7f4e23ca8449d1ca66`, 185 files |
| CLI | Shopify CLI 4.8.2 |
| Open pull requests | #121, this package. It changes no theme file |

## Checks

| Check | Result | Notes |
| --- | --- | --- |
| Live theme against the baseline | PASS | Downloaded whole to a scratch folder: it matches `baseline/theme/` file for file. No one has changed the live theme since 2026-09-25 |
| Review theme against `main` | PASS | Downloaded whole: 180 files. 22 JSON files differ only by the empty settings Shopify adds; `config/settings_data.json` is identical. No theme editor changes. Four Git and tooling files are in Git only. Home shows the collection row, no Liquid errors |
| Theme Check | PASS | 166 files, no offences |
| Design system linter, strict | PASS | 0 errors, 0 warnings; its 16 tests pass |
| Contrast | PASS | 85 of 85 pairings |
| Theme copies match the design system | PASS | `sync_theme.py --check` |
| Tests of the three page checks | PASS | Structured data, answers, links |
| Links between pages, review theme | PASS | 1,627 addresses read, 0 errors, 14 notes. Ten notes are the pages hidden at release |
| Questions the site must answer, review theme | PASS | 27 answered, 5 known gaps for the gallery, 0 errors |
| Structured data, review theme | PASS | 17 pages on the first candidate, 0 errors, 15 warnings (events without a description or an end time). Home, On now, Permanent Collection and Donate again on the second: 0 errors |
| Fonts, review theme | PASS | 4 pages. Only the land acknowledgement's 12 characters fall back to Arial (L-06, accepted, P-58) |
| Events drop off after they end | PASS | The Explore + Create session of September 26 is on Past events only. Current shows October 3 and 5, Upcoming starts October 8 |
| Exhibition status at midnight Pacific | NOT RUN | No start or end date falls before February 20, 2027. Needs a test entry, with Michael's go-ahead |
| Every exhibition entry ready to be seen | PASS | 32 entries, all active. 30 have pages with text, read by the links check. *Fall 2027 Exhibition* and *Against the Latitude of "Progress"* have no text: their addresses answer 200, ask not to be listed, and nothing links to them |
| App embeds | PASS | Neither theme has any, so publishing turns none off |
| Staff editing test | NOT RUN | Gallery staff, in the review theme's editor |
| Newsletter test | NOT RUN | Needs an approved test address and Mailchimp access |
| Hero focal points | NOT CHECKED | Seven points for Michael to set in Content, Files (`proposals/hero-focal-points.md`). The API can't read or set them |

## The store today, read 2026-09-29

Exports and dry runs: `proposals/store-writes/dry-runs/2026-09-29/`.

- **58 pages.** Read twice through the connector, saved without retyping, and compared with the storefront's own copy of each published page: all agree.
- **Page text:** the 32 published pages in `snapshots/pages-2026-09-25.json` match it character for character. The 23 pages made before release are still empty. So no one has edited a page's text since the staged text was written.
- **The 21 prints:** every description matches `snapshots/prints-descriptions-2026-09-26.json`. Every title is in plain letters (P-61).
- **Frames:** 16 active and one draft, as in `snapshots/frames-2026-09-26.json`.
- **Menus:** `new-theme-main-2`, `new-theme-explore-2`, `new-theme-legal` and `new-theme-programmes` exist and hold what `store-changes.md` §1 and §2 say. The live header's `new-website-menu-1` is unchanged.
- **Redirects:** three exist. None is from an address the release redirects. One, `/pages/who-we-are`, goes to `/pages/our-story`, which the release hides and sends on (below).
- **Event pages:** off (`renderable` and `onlineStore` both off), as left on 2026-09-29.
- **Descriptions for search engines:** staged on 40 pages; no page has one in its search engine listing yet.

## The change set, in order

| # | Step | What changes | Ready? |
| --- | --- | --- | --- |
| 0a | Theme settings still to fill | Newsletter consent wording is empty, so the band shows none. Hours, phone, email and social links are set, from the current sites; the gallery hasn't confirmed them | Michael, 2026-09-29: release as it is |
| 0b | Mailchimp | The app's permission update, and its app embed for site tracking after 2027-03-01 (`baseline/mailchimp-audit.md`) | Michael decides. Neither blocks publishing |
| 0c | Supporters (§8c) | Confirmed (Michael, 2026-09-29): it stays in the menu and the Foundation page's cards, goes live with the rest, and Donate's "donor page" links to it (P-43) | Ready |
| 0d | Event pages (§8e) | Web pages on for the Event definition, then three event pages read with both checks on the review theme | Ready. Tested once on 2026-09-29 |
| 1 | Publish | `shopify theme publish --theme 184767250729` | Ready |
| 2 | Templates (§3) | 38 pages take their new template name. 7 are already right, 13 are left alone (10 hidden at release, 3 unpublished). The package first said 40: the script wrongly moved Permanent Collection and Artists off their own templates ("The release", below) | Ready. `templates.md` |
| 3 | Addresses (§5) | 10 pages hidden, then 10 redirects. Proposed today: the older `/pages/who-we-are` redirect goes straight to `/pages/artists-for-kids` | Ready. `addresses.md` |
| 4 | Staged text (§8) | 32 pages take their staged text; 4 of them are cleared. Then the staged values and the `release_body` definition are deleted | Ready: all pages match. `staged.md` |
| 5 | New pages shown (§8b, §8c) | 23 pages lose `seo.hidden` | Ready. `unhide.md` |
| 6 | Print descriptions (§7) | The clean-up on the 21 prints | Waits for the gallery's approval of `products.md`. Can follow later: the new theme shows the label and the description as they are |
| 7 | Frames (§9) | 16 active frames become Unlisted | Ready. `frames.md` |
| 8 | Descriptions to the search listings (§8d) | 40 pages | Waits for the gallery's approval of the words. Can follow later: the new theme reads the staged descriptions |

The release script's order is publish, templates, addresses, staged, unhide, products, frames. Steps 0c and 0d come before publishing because the new theme shows them the moment it is live.

**Outside the store, the same day:** the Artists for Kids team cuts artistsforkids.sd44.ca back to registration (P-30). The redirect file goes on smithfoundation.co's server and GoDaddy's forwarding goes off (#119, P-63).

## Since the first dry runs (2026-09-26)

- Pages: 35 then, 58 now (18 Artists for Kids, 3 Foundation, Past events and Current events).
- Template names: 20 pages changed then, 38 now.
- Staged text: 9 pages then, 32 now. Contact and Frequently Asked Questions have staged text too.
- Product titles: done ahead of release (P-61), so step 6 changes descriptions only.

## How the writes are made

Steps 2 to 5 and 7 make 163 changes, 32 of them whole page texts. Two ways:

1. **Shopify CLI, from files** (`shopify store execute --variable-file`). Each value goes to the store exactly as the script printed it. The CLI's store access covers entries and files today; a page read was refused ("ACCESS_DENIED"). Michael would add pages, redirects, products and definitions with `shopify store auth`.
2. **The connector**, as every write so far. Each page's text is passed by hand, then read back from the storefront and compared with the export, so a slip is caught and fixed.

Michael chose the first. `proposals/store-writes/release_run.py` makes the calls: it lists them without `--go`, and with it makes them one at a time, stops at the first error and keeps the store's answers in `created/release-2026-09-29/`.

## Decisions

None is Proposed for anything built. DS-70a is Proposed and not built, so nothing of it ships.

## Requirements

29 requirements. 26 are In progress: built, checked by the agent, not yet through the staff editing test. 3 are Blocked on gallery input (ACCESS-01, ACCESS-03, ACCESS-04). None is Done, since Done needs the staff test (`REQUIREMENTS.md`).

## Rollback

1. Republish `183162372393`: `shopify theme publish --theme 183162372393`. It is unchanged and matches the baseline.
2. Templates: set each page back to the "Now" column of `dry-runs/2026-09-29/templates.md`.
3. Addresses: delete the 10 redirects, publish the 10 pages, set `/pages/who-we-are` back to `/pages/our-story`.
4. Page text: restore each page from `dry-runs/2026-09-29/pages-now.json`, which holds today's text and the staged text. Make the `release_body` definition again if the staged values are wanted back.
5. New pages: set `seo.hidden` to 1 on the 23.
6. Frames: set the 16 back to Active.
7. Event pages: turn `renderable` and `onlineStore` off.
8. Descriptions: restore from `snapshots/prints-descriptions-2026-09-26.json`.

Republishing the old theme alone does not undo steps 2 to 8.

## After release

- Open every page, then run `check_links.py`, `check_answers.py` and `check_structured_data.py` on gordonsmithgallery.com.
- A search for "smith" shows no frames; a print's Framed choice adds its frame to the cart. No order is placed.
- Each of the 11 old addresses lands on its new page.
- Record the final theme ID, commit and results here and in `PROJECT.md`.
- Follow-up pull request: remove the pre-release bridges (`gs-page-text`'s fallback, the old names in `gs-is-programme-page` and `gs-is-story-page`), empty the unlinked list in `links.json`.

## The release, 2026-09-29

Done between 23:07 and 23:17 UTC (4:07 to 4:17 PM Pacific). The full log, with each call and the store's answer: `proposals/store-writes/README.md`, "2026-09-29: the release", and `proposals/store-writes/created/release-2026-09-29/`.

| | |
| --- | --- |
| Live theme | `184767250729` "New theme for review (do not publish)", role live, published 23:08:52 UTC |
| Old theme | `183162372393` "Colorblock: NEW WEBSITE", role unpublished, unchanged, kept for rollback |
| Git commit | `main` at dee1885; theme tree `e8426474494513f298191e7f4e23ca8449d1ca66` |

| Step | Result |
| --- | --- |
| Event pages on, read on the candidate before publishing | PASS: structured data on 8 pages, 0 errors; answers, 27 answered, 0 errors |
| Publish | PASS: Home, On now, Donate, an exhibition and a portfolio answer 200 in the new theme, no Liquid errors |
| Templates | FIXED: 38 pages right. Permanent Collection and Artists were moved off their own templates by a fault in the script, for about eight minutes, then set back |
| Addresses | PASS: 10 pages hidden; each of the 11 old addresses answers 301 to its new page |
| Staged text | PASS: 32 pages. 25 hold their text character for character; 7 hold the same tags, attributes and words with Shopify's own line breaks and characters. Every run of each page's text is on its live page |
| New pages shown | PASS: 23 pages no longer ask not to be listed, and are in the sitemap |
| Frames | PASS: 16 Unlisted, out of the collections' lists. A print's Framed choice adds its frame under the print in the cart ($1,600 in all); the cart was emptied and no order placed. A search for "smith" still listed 15 frames for the first minutes, while Shopify's search index caught up; read again at 23:30 UTC, it lists none |
| Answers on the live site | PASS: 27 answered, 5 known gaps, 0 errors |
| Structured data on the live site | PASS: 20 pages, 0 errors |
| Links on the live site | PASS after the fix: 1,636 pages read, 0 errors, 4 notes, no page more than three clicks from home. The nine event pages are read now. The first run, before the fix: 982 errors, which is how the template fault was found |

**What the release taught.** The dry run showed `permanent-collection` and `artists` going to the standard template, in plain sight, and the row was read as right. A dry run is only as good as the check of each row against the specification. `release.py` now holds the two names, and the links check on the live site is the check that caught it.

## Still open after release

- The print descriptions (§7) and the descriptions in the search engine listings (§8d): the gallery's approval.
- The newsletter consent wording, the staff editing test, the newsletter test, the exhibition date check, the seven hero focal points.
- A review theme. The old one is the live theme now, so there is none. Until Michael approves a new unpublished theme, no theme is pushed to (`AGENTS.md`).
- The live theme's name still says "for review (do not publish)". Renaming it is a theme write, for Michael to approve.
- Outside the store: the Artists for Kids site cut back to registration (P-30); the redirect file on smithfoundation.co's server and GoDaddy's forwarding off (P-63).
- The follow-up pull request: the pre-release bridges out of the theme, and the unlinked list in `links.json` emptied.
