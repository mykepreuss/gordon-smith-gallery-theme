# Proposed store-level changes

Changes to Shopify Admin resources that the theme work needs. None of these is made until the gallery approves the structure (approval package) and, for live resources, until release approval. Menus, pages, fields and products are shared by every theme, so a preview theme does not isolate them (`AGENTS.md`). Baseline state: `baseline/store-manifest.md`.

## 1. Main menu map (NAV-01 to NAV-04, EXH-01, EXH-02, SHOP-02)

Model (DS-11): a section with pages under it is one button; its main page is the first link inside, with its own label. A section without pages is a plain link. Labels below are proposals; the gallery sets the final wording (EXH-04). Order: Exhibitions first (P-09), then the rest in the live menu's order.

| Section | Type | Items, in order (destination) | Change from today |
| --- | --- | --- | --- |
| Exhibitions | Section | On now (`/pages/on-now`), Upcoming (`/pages/upcoming-exhibitions`), Past exhibitions (`/pages/past-exhibitions`) | Moves to the first place in the menu (P-09). Adds Upcoming (missing today). The Exhibitions overview page (`/pages/exhibitions-1`) is removed (P-20): hidden at release, its address redirecting to On now (§5) |
| About | Section | About the gallery (`/pages/about-us`; `/pages/about` is hidden at release and forwards to Artists for Kids, P-24), Plan your visit (`/pages/plan-your-visit`), Permanent collection (`/pages/permanent-collection`), Volunteer (`/pages/volunteer`) | The About page becomes reachable (today the parent label only opens the dropdown). Contact moves to the always-visible utility row and footer. About Us is the page about the three organisations. About's history joins the Artists for Kids page, and About is hidden at release (Michael, 2026-09-26, P-24) |
| Artists for Kids | Link | `/pages/artists-for-kids` | None. Approved 2026-09-25 as one link (P-15); the programme links to the Artists for Kids site stay on its page |
| Programs | Section | Public programs (`/pages/public-programs-1`), Speaker series, Music at the Smith, Explore + Create, Art in Good Company | "Public Programs" no longer repeats the section, because the section itself is not a link |
| Smith Foundation | Section | About the Foundation (`/pages/the-smith-foundation`), Gordon and Marion (`/pages/gordon-and-marion`), Donate (`/pages/donate`) | Renames the first item so it doesn't repeat the section |
| Shop | Section | Limited editions (`/pages/shop`), 2026 Fall Portfolio, 2026 Spring Portfolio, 2025 Fall Portfolio, 2025 Spring Portfolio, 2024 Fall Portfolio, Artists (`/pages/artists`) | Leads to the Shop landing page instead of Shopify's `/collections` list. 2025 Fall Portfolio uses the relative `/collections/2025-fall-portfolio` instead of the absolute myshopify URL |

Each section's own link in the Shopify menu editor points at its first item, so `snippets/gs-nav.liquid` raises no editor warning.

**How it is applied:** during review, as a separate new menu referenced only by the review theme (so the live header doesn't change). At release, either switch the live header to the reviewed menu or edit `new-website-menu-1` to match, recorded in the release change set.

**Created 2026-09-25** as `new-theme-main` ("Main menu (new theme)"), with Michael's go-ahead, and set in the new theme's header (`sections/header-group.json`). Our story removed from its Shop section 2026-09-26 (P-25). Publishing the new theme switches the header to it; `new-website-menu-1` is then unused and stays for rollback.

## 2. Utility and footer menus (ACCESS-02, ACCESS-03)

| Menu | Items | Note |
| --- | --- | --- |
| ~~New `utility` menu~~ | Not needed: the theme builds the utility links in (DS-29): Contact from the contact-page theme setting, Search, Cart (Newsletter removed, DS-56) | One store change fewer. Contact can't be dropped by a menu edit |
| Footer | Explore links (Exhibitions, Limited editions, Artists for Kids), Frequently asked questions (`/pages/frequently-asked-questions`, relative instead of the absolute URL), Do not sell or share my personal information | Social links come from theme settings with visible names (gallery supplies URLs). The footer section takes two menus: Explore, and an optional Legal menu for the small last-line links; store policies are added automatically. Created 2026-09-25 as `new-theme-explore` (Exhibitions, Limited editions, Artists for Kids, Frequently asked questions) and `new-theme-legal` (Do not sell or share my personal information), set in the new theme's footer. The live `footer` menu is untouched |

## 3. Template assignments (REUSE-01, DS-14)

Script: `proposals/store-writes/release.py templates` (dry run 2026-09-26: `store-writes/dry-runs/2026-09-26/templates.md`).

Moving pages from their one-off templates to the closed set in `design-system/DESIGN.md` §7.4 (On Now, Upcoming and Past go to the standard page template, DS-48) is a store-level release action (the Admin assignment list reads the live theme). Until then, the review theme shows every page with its release layout at its own address (DS-48, DS-49, and for the programme pages and Volunteer `snippets/gs-is-programme-page.liquid`); `?view=` still previews any template. After the script has run, delete that snippet's list of old template names in a follow-up pull request. Full mapping: DESIGN.md §7.4. With the new theme (P-13) none of today's page templates exist after publishing, so every page's assignment is set at release by a script run straight after publishing, with a snapshot of today's assignments for rollback.

Until the script runs, pages whose old template the new theme lacks fall back to the default page template, which shows them correctly (the exhibition lists from Theme settings, DS-48), and Our Story (old template `shop`) shows as a plain page on the Shop template (DS-49). So the script puts the right template names on the pages for staff rather than fixing what visitors see. It is written and dry-run before release (plan, "Release gate and rollback"): it snapshots every page's template, maps each page to its new one, and prints the changes for Michael to check. At release it runs straight after publishing, and every page is opened to check it. Not written yet.

## 4. Field definitions (content model)

`design-system/proposals/content-model.md`, approved 2026-09-25 (DS-14 to DS-16):

1. Page fields (`custom.*`): hero image, hero is artwork, eyebrow, intro, programme, gallery images.
2. Exhibition entries (metaobject `exhibition`, web pages at `/pages/exhibitions/<entry>`), with the fields revised from the review of content in use: dates and dates note, curator credit, artists and collection artists, venue, opening reception, events, key image and caption, summary, body, installation photos, credits, funder logos, programme.
3. Product label fields (artist, title, year, medium, edition, dimensions, coming soon) and plain-text product titles.
4. Approved 2026-09-25 (P-16): card groups, events, page hero caption and call to action, collection photo credit, product availability note (content model parts 4 to 6).

Creating definitions is additive and doesn't change what visitors see, but it is still a store-level change: create them when implementation starts, with Michael's go-ahead, and record each in the pull request.

**Done 2026-09-25, with Michael's go-ahead:** the `exhibition` and `event` definitions, four exhibition entries and one event, active so they render in the development theme. Their addresses return 404 under the live theme. Log, IDs and undo steps: `proposals/store-writes/README.md`. The other 11 exhibitions followed (below).

**Also done 2026-09-25, with Michael's go-ahead:** the page field, `card` and `card_group` definitions; the cards, card groups and events of the seven programme pages; and their field values. The other pages' fields followed (below).

**Also done 2026-09-25, with Michael's go-ahead:** the product label and availability fields, the collection photo credit field, label values on the 21 limited editions, credits on the five portfolios, and the Shop page's hero. Product titles are unchanged; plain-text titles (DS-16) wait for release (§3 of the content model, migration).

**Also done 2026-09-25, with Michael's go-ahead ("migrate all content"):** the other 11 exhibitions, the About and Donate card groups, the remaining pages' fields, the staged page text (§8) and the three review menus (§1, §2). Every item in `proposals/content-migration.md` now has its content in the store or the theme. Log: `proposals/store-writes/README.md`.

## 5. Addresses at release (P-10, P-20, P-24, P-25)

Script: `release.py addresses` (dry run: `dry-runs/2026-09-26/addresses.md`).

Redirects only work from addresses that no longer load a page, so the order matters. At release, after the theme is published and the exhibition entries are active:

1. Hide (don't delete) the six exhibition pages, the Exhibitions overview (`exhibitions-1`, P-20), About (P-24) and Our Story (P-25), keeping them for rollback.
2. Create nine URL redirects:

| From | To |
| --- | --- |
| `/pages/exhibition-one-hundred-artists-deep` | `/pages/exhibitions/one-hundred-artists-deep` |
| `/pages/exhibition-from-the-ground` | `/pages/exhibitions/from-the-ground` |
| `/pages/exhibition-stitched-merging-photography-and-textile-practices` | `/pages/exhibitions/stitched` |
| `/pages/exhibition-playhouse` | `/pages/exhibitions/playhouse` |
| `/pages/exhibition-prevailing-landscapes` | `/pages/exhibitions/prevailing-landscapes` |
| `/pages/exhibition-the-art-of-conversation` | `/pages/exhibitions/the-art-of-conversation` |
| `/pages/exhibitions-1` | `/pages/on-now` |
| `/pages/about` | `/pages/about-us` |
| `/pages/our-story` | `/pages/artists-for-kids` |

3. Open each old address and check it lands on its entry.
4. Move the staged page text into its pages (§8). This clears the exhibition text repeated in the On Now, Upcoming and Upcoming Events page bodies; it lives in the entries now.

The Exhibitions overview stays live until release: Michael chose not to hide it early, 2026-09-26. No short forwarding addresses such as `/exhibitions` or `/exhibitions/on-now` (Shopify serves pages only at `/pages/`; Michael, 2026-09-26: keep the addresses as they are).

Rollback: republish the baseline theme, unhide the nine pages, delete the nine redirects, restore the page bodies from `proposals/store-writes/snapshots/pages-2026-09-25.json`. Entry handles are proposals until the entries exist.

The entries are already active (created 2026-09-25); their pages return 404 only because the live theme has no exhibition template. Publishing the new theme makes every active entry public, so each one is checked before release.

## 6. Theme settings for the review theme

Values the theme's settings need (Online Store, Themes, Customize, Theme settings). These are theme data, not store resources: they live in the review theme's `config/settings_data.json` and change nothing else. The build sets the ones already known.

| Setting | Value | Status |
| --- | --- | --- |
| Address | 2121 Lonsdale Avenue, North Vancouver, BC V7M 2K6 | Set (DESIGN.md §6.10) |
| Land acknowledgement | The current footer's wording | Set (moved from the current theme) |
| Contact page, On now, Upcoming, Past, Upcoming events and Shop landing pages | `contact`, `on-now`, `upcoming-exhibitions`, `past-exhibitions`, `upcoming-events`, `shop` | Set |
| Portfolios, newest first; All limited editions | The five portfolios, 2026 Fall first; `all-prints` | Set |
| Hours, phone | Thursday to Saturday, 12:00 PM - 4:00 PM (Plan Your Visit); (604) 903-3798 (Contact page) | Set 2026-09-25 from the current site; gallery to confirm |
| Email | One address, for the footer and Contact | Blank until the gallery chooses (Michael, 2026-09-25) |
| Social links, newsletter consent wording | From the gallery (ACCESS-04) | Waiting |
| Main menu; footer Explore and Legal menus | `new-theme-main`; `new-theme-explore`, `new-theme-legal` (§1, §2) | Set |

## 7. Product titles and descriptions at release (DS-16)

Script: `release.py products` (dry run for the gallery: `dry-runs/2026-09-26/products.md`; the 21 titles and descriptions before any change: `snapshots/prints-descriptions-2026-09-26.json`).

The 21 limited editions' titles carry Unicode italic letters (L-03). At release, each title becomes the same words in plain text (`proposals/store-writes/shop.py`, `plain()`). The new theme shows the label fields, so this changes the admin, order emails, search and the browser tab. The live theme shows the titles, which is why this waits for release.

Rollback: restore each title from `proposals/store-writes/snapshots/prints-2026-09-25.json`.

**Descriptions (found 2026-09-26).** Each of the 21 descriptions opens with its label typed out: artist, title and year, "Limited Edition" (or "Art Edition"), on some an "Availability" line, then "PRINT DETAILS" with edition, sizes, paper, technique, date and signature. The new theme shows the label beside the work and the description under About the work, so a product page says most of it twice. The live theme has no label fields and shows these details only through the description, which is why they stay until release.

Proposed for release, in the same script as the titles, after a dry run the gallery approves:

1. Remove the lines that repeat a label field: artist, title and year, "Limited Edition", edition, sizes, technique, date. Remove the second repeat of the details in Samuel Roy-Bois's and Sara Khan's descriptions too (P-21, decided).
2. Keep paper and signature, which have no field, as one short line. Keep everything else in the description as written, including Russna Kaur's opening quote.
3. Remove the "Availability" lines ("Low Stock", "SOLD OUT"): typed stock status goes out of date, and the theme already says Sold out from inventory (P-22, decided).

The dry run prints each description before and after; nothing changes until the gallery approves. Before the change, snapshot the 21 descriptions in full (`snapshots/prints-2026-09-25.json` holds the titles and parsed details, not the descriptions). Rollback: restore each description from that snapshot.

## 8. Staged page text at release (DS-39)

Script: `release.py staged` (dry run 2026-09-26: all nine pages still match the snapshot).

Page text is live, so the text that changes at release is staged in a temporary page field, `custom.release_body`, which the new theme shows instead of the page's text (`sections/gs-page-body.liquid`). Created 2026-09-25 with Michael's go-ahead (`proposals/store-writes/README.md`).

| Page | Staged text |
| --- | --- |
| On Now, Upcoming Exhibitions, Upcoming Events | None: each repeats *Collect, Assemble, Gather*, which lives in its entry |
| Donate | Its text, then the tax receipt note from the old template. "Ways to Support" is a heading and "Every contribution makes a difference:" the paragraph after it (page pass, 2026-09-26). "The impact of your gift" is a heading too, and Asha's words a quote with her name under it; spacing typed as line breaks goes, and the Explore + Create link stays in the same tab (DS-53) |
| Gordon and Marion | Its text, then the video from the old template. The biography's paragraphs, split by line breaks, become paragraphs, and the photo becomes a figure with a description. The video, which is square, joins the photo beside the biography, captioned with its heading, without Vimeo's title overlay (DS-53) |
| Artists | Its two paragraphs, then its 59 artist links as one list, same order and addresses (page pass, 2026-09-26, DS-45) |
| About Us | None: its three descriptions live in its card group, each beside its organisation's logo, and the combined logo image above them goes (DS-50, 2026-09-26) |
| The Smith Foundation | Its two paragraphs, word for word, without the line above them that repeated the first sentence's opening (the Foundation's full name). Explore + Create, Art In Good Company, Speaker Series and Music at The Smith link to their pages; the Gordon and Marion link stays on the site instead of opening a new tab (DS-52) |
| Artists for Kids | Its own two paragraphs and the Paradise Valley photo, then About's four paragraphs under a "History" heading (P-24), with Our Story's sentence on art specialists and its fuller caption for the Bill Reid print (P-25). Our Story's sentence on the ceremonial drum was added, then dropped because it repeated the sentences around it. Words unchanged; both pictures become figures with their own captions; "contemporary limited editions" links to the Shop; pasted formatting stays behind |

At release, a script (to write before release, with a dry run) does, for each page:

1. Checks the page's live text still matches `proposals/store-writes/snapshots/pages-2026-09-25.json`. If not, it stops: the staged text is rebuilt from the new live text and checked again.
2. Replaces the page's text with the staged text (an HTML comment alone means no text).
3. Clears the staged value.

Then it deletes the `release_body` definition. The theme's fallback in `gs-page-body.liquid` is removed in a later pull request.

Rollback: restore each page's text from the snapshot.

## 9. Frame products at release (P-19)

Script: `release.py frames` (dry run: `dry-runs/2026-09-26/frames.md`).

Each print's frame is its own product (product type Frame, collection `framing`), so search results fill with frames. At release, after publishing, the 16 active frames become **Unlisted**: still buyable, still offered on each print's page through `custom.featured_frame` (a metafield reference, which Liquid still returns), but out of search, collections and recommendations. The draft Michael Snow frame stays a draft. Snapshot: `proposals/store-writes/snapshots/frames-2026-09-26.json`.

This waits for release because the old theme's add-a-frame popup looks frames up by their collection. Smoke test after: a search for "smith" shows no frames, and a print's "Add a frame" still adds its frame to the cart.

Rollback: set the 16 back to Active from the snapshot.

## 10. Not proposed

- No other redirects, no product or collection changes beyond part 4, no app installs, no checkout changes.
- Mailchimp: no change until the audit is complete (`baseline/mailchimp-audit.md`).
