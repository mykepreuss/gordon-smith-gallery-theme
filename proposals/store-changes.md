# Proposed store-level changes

Changes to Shopify Admin resources that the theme work needs. None of these is made until the gallery approves the structure (approval package) and, for live resources, until release approval. Menus, pages, fields and products are shared by every theme, so a preview theme does not isolate them (`AGENTS.md`). Baseline state: `baseline/store-manifest.md`.

## 1. Main menu map (NAV-01 to NAV-04, EXH-01, EXH-02, SHOP-02)

By what visitors come to do, not by which organisation runs a page (P-50 to P-57, decided by Michael 2026-09-28: "Proceed with implementing this new navigation and IA"; the review is `proposals/navigation-review.md`). Model (DS-11): a section with pages under it is one button; its main page is one of its links, with its own label. A section without pages is a plain link. A dropdown item with items of its own is a group (DS-133). Labels are proposals; the gallery sets the final wording (EXH-04). Exhibitions stays first (P-09).

| Item | Type | Holds, in order (destination) | Change from the menu before (P-29, P-33) |
| --- | --- | --- | --- |
| Exhibitions | Link | On now (`/pages/on-now`) | Was a section of three. Upcoming and Past are reached from the switcher on the three lists (P-51) |
| Collection | Section | The collection (`/pages/permanent-collection`), Artists (`/pages/artists`) | None (P-26) |
| Programs | Section with groups | Upcoming events (`/pages/upcoming-events`). **Public programs** (`/pages/public-programs-1`): Speaker series, Music at the Smith, Explore + Create, Art in Good Company. **Artists for Kids** (`/pages/artists-for-kids`): Classes and camps, Schools and teachers. **Scholarships and awards** (no page, "#"): Smith Foundation scholarships (`/pages/smith-foundation-scholarships`), Artists for Kids awards (`/pages/awards-and-scholarships`) | Artists for Kids leaves the bar and becomes a group here, its title linking to its page; the two organisations' scholarships sit together (P-52) |
| Support | Section | Give to the Smith Foundation (`/pages/donate`), Give to Artists for Kids (`/pages/support-artists-for-kids`), Brilliance Gala (`/pages/brilliance-gala`), Volunteer (`/pages/volunteer`), Supporters (`/pages/smith-foundation-supporters`) | New. Takes the Smith Foundation section's place; Volunteer leaves About, and Support Artists for Kids leaves Artists for Kids (P-53) |
| About | Section | About the gallery (`/pages/about-us`), Plan your visit (`/pages/plan-your-visit`), Gordon and Marion Smith (`/pages/gordon-and-marion`), The Smith Foundation (`/pages/the-smith-foundation`) | Gains Gordon and Marion, with "Smith" in its label, and the Foundation's page. Visit stays here; the header shows today's opening line (P-54, DS-132) |
| Shop | Link | The Shop page (`/pages/shop`) | Was a section with the five portfolios, which the Shop page and the portfolio switcher list (P-55) |

Each section's own link in the Shopify menu editor points at one of its links (Programs at Public programs' title, Support at Donate), so `snippets/gs-nav.liquid` raises no editor warning.

**The Programs switcher (DS-143), proposed 2026-09-28, not made yet.** Three changes, each needing Michael's go-ahead and a before-snapshot:

- A new menu, `new-theme-programmes` ("Programs filter (new theme)"): Speaker series, Music at the Smith, Explore + Create, Art in Good Company, each linking to its page. Theme settings, Exhibitions and events, Programs filter menu names it (`config/settings_data.json`). Until it exists the row holds only the pages with an upcoming event, so nothing breaks without it.
- A new page, Past events (`/pages/past-events`), with no text, for DS-147. Theme settings, Exhibitions and events, Past events page names it. Unlike a menu, the live theme shows a new page at its address, as a title with nothing under it; nothing links to it there. Hidden from search engines until release, as the Artists for Kids pages are (P-35). Until it exists the row has no Past events link.
- The Programs section's own link in `new-theme-main-2`, and the Programs link in the footer's `new-theme-explore-2`, point at Upcoming events (`/pages/upcoming-events`) in place of Public programs. Public programs keeps its link as its group's title.

**The three Foundation pages from `proposals/smith-foundation-site.md`** joined this menu when they were made, 2026-09-28, where the table says, with `menuUpdate` keeping the other items' IDs (P-52, P-53). If the gallery hasn't confirmed the Supporters list by release (P-43, `gallery-questions.md` 8.1), Supporters leaves the menu that day (§8c).

**How it is applied:** during review, as a menu referenced only by the new theme, so the live header doesn't change. At release, publishing the new theme switches the header to it; `new-website-menu-1` is then unused and stays for rollback.

**Created 2026-09-28** as `new-theme-main-2` ("Main menu (new theme, 2026-09-28)", `gid://shopify/Menu/305944068393`), with Michael's go-ahead, and set in the new theme's header (`sections/header-group.json`). The earlier review menu, `new-theme-main` (created 2026-09-25; Our story out 2026-09-26, P-25; Collection 2026-09-27, P-26; order P-29; Artists for Kids section P-33; Upcoming events 2026-09-27), is unchanged. The review theme reads it until this work merges and the review theme is pushed from `main`; it can be deleted after release.

## 2. Utility and footer menus (ACCESS-02, ACCESS-03)

| Menu | Items | Note |
| --- | --- | --- |
| ~~New `utility` menu~~ | Not needed: the theme builds the utility links in (DS-29): Contact from the contact-page theme setting, Search, Cart (Newsletter removed, DS-56) | One store change fewer. Contact can't be dropped by a menu edit |
| Footer | Explore (`new-theme-explore-2`, P-56): Exhibitions, Collection, Programs, Artists for Kids, Support, About, Shop, Frequently asked questions; Legal (`new-theme-legal`): Do not sell or share my personal information | Social links come from theme settings with visible names (gallery supplies URLs). The footer section takes two menus: Explore, and an optional Legal menu for the small last-line links; store policies are added automatically. Explore names every section's main page, so the whole site is one click from the foot of every page. Created 2026-09-28 (`gid://shopify/Menu/305944330537`) and set in the new theme's footer; the earlier `new-theme-explore` (Exhibitions, Limited editions, Artists for Kids, Frequently asked questions, created 2026-09-25) is unchanged until this merges. The live `footer` menu is untouched |

## 3. Template assignments (REUSE-01, DS-14)

Script: `proposals/store-writes/release.py templates` (dry run 2026-09-26: `store-writes/dry-runs/2026-09-26/templates.md`).

Moving pages from their one-off templates to the closed set in `design-system/DESIGN.md` §7.4 (On Now, Upcoming and Past go to the standard page template, DS-48) is a store-level release action (the Admin assignment list reads the live theme). Until then, the review theme shows every page with its release layout at its own address (DS-48, DS-49, and for the programme pages and Volunteer `snippets/gs-is-programme-page.liquid`); `?view=` still previews any template. After the script has run, delete that snippet's list of old template names in a follow-up pull request. The 18 Artists for Kids pages made 2026-09-27 (P-35) carry the live theme's On Now template name (`current-on-now-exhibition`) so the live site shows only their titles; the script gives 13 of them the programme template, and the four residency pages and Support Artists for Kids the standard one (`release.py`, `AFK_PROGRAMME`, `AFK_STANDARD`). Full mapping: DESIGN.md §7.4. With the new theme (P-13) none of today's page templates exist after publishing, so every page's assignment is set at release by a script run straight after publishing, with a snapshot of today's assignments for rollback.

Until the script runs, pages whose old template the new theme lacks fall back to the default page template, which shows them correctly (the exhibition lists from Theme settings, DS-48), and Our Story (old template `shop`) shows as a plain page on the Shop template (DS-49). So the script puts the right template names on the pages for staff rather than fixing what visitors see. It is written and dry-run before release (plan, "Release gate and rollback"): it snapshots every page's template, maps each page to its new one, and prints the changes for Michael to check. At release it runs straight after publishing, and every page is opened to check it. Not written yet.

## 4. Field definitions (content model)

`design-system/proposals/content-model.md`, approved 2026-09-25 (DS-14 to DS-16):

1. Page fields (`custom.*`): hero image, hero is artwork, eyebrow, intro, programme, gallery images.
2. Exhibition entries (metaobject `exhibition`, web pages at `/pages/exhibitions/<entry>`), with the fields revised from the review of content in use: dates and dates note, curator credit, artists and collection artists, venue, opening reception, events, key image and caption, summary, body, installation photos, credits, funder logos, programme.
3. Product label fields (artist, title, year, medium, edition, dimensions, coming soon) and plain-text product titles.
4. Approved 2026-09-25 (P-16): card groups, events, page hero caption and call to action, collection photo credit, product availability note (content model parts 4 to 6).
5. The Permanent Collection (P-27, DS-62): artist, artwork and collection grouping entries (web pages at `/pages/artists/`, `/pages/collection/` and `/pages/browse/`), and the editions' Artist pages field (`custom.artist_entries`). Fields: `proposals/store-writes/collection/definitions.py`.

Creating definitions is additive and doesn't change what visitors see, but it is still a store-level change: create them when implementation starts, with Michael's go-ahead, and record each in the pull request.

**Done 2026-09-25, with Michael's go-ahead:** the `exhibition` and `event` definitions, four exhibition entries and one event, active so they render in the development theme. Their addresses return 404 under the live theme. Log, IDs and undo steps: `proposals/store-writes/README.md`. The other 11 exhibitions followed (below).

**Also done 2026-09-25, with Michael's go-ahead:** the page field, `card` and `card_group` definitions; the cards, card groups and events of the seven programme pages; and their field values. The other pages' fields followed (below).

**Also done 2026-09-25, with Michael's go-ahead:** the product label and availability fields, the collection photo credit field, label values on the 21 limited editions, credits on the five portfolios, and the Shop page's hero. Product titles are unchanged; plain-text titles (DS-16) wait for release (§3 of the content model, migration).

**Also done 2026-09-25, with Michael's go-ahead ("migrate all content"):** the other 11 exhibitions, the About and Donate card groups, the remaining pages' fields, the staged page text (§8) and the three review menus (§1, §2). Every item in `proposals/content-migration.md` now has its content in the store or the theme. Log: `proposals/store-writes/README.md`.

**Also done 2026-09-26 and 27, with Michael's go-ahead ("please proceed with delivering the plan", "all the artists and everything"):** the collection's three definitions and the product field, 171 artists, 1,168 works, 1,417 images, 180 documents and 26 groupings, all active; the Artists page's staged text without its links out; the Permanent Collection page's Browse button to its own search; the Collection section in the review menu (§1). The entries go live with the site. Then, after Michael's review (2026-09-27, P-28, DS-63): the 6 works on loan, the exhibition entry's Works from the collection field (filled for three exhibitions), and the documents as Document entries with their covers. Log: `proposals/store-writes/README.md`.

**Also done 2026-09-27, with Michael's go-ahead ("all recommendations are approved ... let's get started on implementation"):** the Artists for Kids site's content (P-30 to P-40): the `lesson` definition and the event's `keep_off_home` field (content model part 8), 92 files, 27 lessons, 46 cards, 15 card groups and two extended ones, 6 events and the curatorial tour's programme page, 18 pages published with their title only and hidden from search engines (P-35), their fields and staged text, the Artists for Kids page's new card groups, button and history, and the review menu's Artists for Kids section. Log: `proposals/store-writes/README.md`.

**Also done 2026-09-28, with Michael's go-ahead ("Proceed with implementing this new navigation and IA"):** the artist entry's About page field (`about_page`, a page reference, P-57), set on Gordon Smith's entry to Gordon and Marion; the eyebrow "The Smith Foundation" on Donate and Gordon and Marion, which links back to the Foundation's page (DS-80); and Gordon and Marion's button, "See Gordon Smith's works". Log: `proposals/store-writes/README.md`.

**Also done 2026-09-28, with Michael's go-ahead ("Yes to everything except integrating the older Year in Review content", then "Proceed with implementation"):** the Smith Foundation's old website (P-41 to P-49, DS-138; `proposals/smith-foundation-site.md`): the exhibition field Videos and publications (`media`, a list of links), 60 files, 17 older exhibitions (2013 to 2019) and nine existing ones filled in, the Foundation page's scholarship and gala cards linked and a Supporters card added, three pages published with their title only and hidden from search engines (P-35), their fields and staged text, staged additions on Speaker Series, Music at the Smith, Gordon and Marion and Awards and scholarships, and the three pages in the new theme's menu. Log: `proposals/store-writes/README.md`.

## 5. Addresses at release (P-10, P-20, P-24, P-25, DS-129)

Script: `release.py addresses` (dry run: `dry-runs/2026-09-26/addresses.md`).

Redirects only work from addresses that no longer load a page, so the order matters. At release, after the theme is published and the exhibition entries are active:

1. Hide (don't delete) the six exhibition pages, the Exhibitions overview (`exhibitions-1`, P-20), About (P-24), Our Story (P-25) and Engage (DS-129), keeping them for rollback.
2. Create ten URL redirects:

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
| `/pages/engage` | `/pages/public-programs-1` |

3. Open each old address and check it lands on its entry.
4. Move the staged page text into its pages (§8). This clears the exhibition text repeated in the On Now, Upcoming and Upcoming Events page bodies; it lives in the entries now.

The Exhibitions overview stays live until release: Michael chose not to hide it early, 2026-09-26. No short forwarding addresses such as `/exhibitions` or `/exhibitions/on-now` (Shopify serves pages only at `/pages/`; Michael, 2026-09-26: keep the addresses as they are).

Rollback: republish the baseline theme, unhide the ten pages, delete the ten redirects, restore the page bodies from `proposals/store-writes/snapshots/pages-2026-09-25.json`. Entry handles are proposals until the entries exist.

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
| Main menu; footer Explore and Legal menus | `new-theme-main-2`; `new-theme-explore-2`, `new-theme-legal` (§1, §2) | Set 2026-09-28 in Git (`sections/header-group.json`, `footer-group.json`); the review theme follows when it is pushed from `main` |

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
| Artists for Kids | Its own two paragraphs and the Paradise Valley photo, then About's four paragraphs under a "History" heading (P-24), with Our Story's sentence on art specialists and its fuller caption for the Bill Reid print (P-25). Our Story's sentence on the ceremonial drum was added, then dropped because it repeated the sentences around it. Words unchanged; both pictures become figures with their own captions; "contemporary limited editions" links to the Shop; pasted formatting stays behind. 2026-09-27 (P-30): two paragraphs from the Artists for Kids site's Who We Are join the History, then "Meet the Artists for Kids Team" (the team photo and four names) and the 2024-2025 annual report (PDF) |
| The 18 Artists for Kids pages (P-35) | All their text: the pages were made with none, so the live site shows only their titles until release (`proposals/store-writes/artists-for-kids/content.py`) |
| Speaker Series, Music at the Smith | Their text, then "Past talks" and "Past concerts" from the Smith Foundation's old site, and on Music at the Smith the Steinway (P-44; `proposals/store-writes/foundation/content.py`) |
| Gordon and Marion, Awards and scholarships | Their staged text above, then the obituary line and a second video (Gordon and Marion), and a line linking the Foundation's scholarships (Awards and scholarships) |
| Scholarships, Brilliance Gala, Supporters (P-35, P-42) | All their text, from the Smith Foundation's old site. Supporters only if the gallery has confirmed its list (§8c) |

At release, a script (to write before release, with a dry run) does, for each page:

1. Checks the page's live text still matches `proposals/store-writes/snapshots/pages-2026-09-25.json`. If not, it stops: the staged text is rebuilt from the new live text and checked again.
2. Replaces the page's text with the staged text (an HTML comment alone means no text).
3. Clears the staged value.

Then it deletes the `release_body` definition. The theme's fallback in `gs-page-body.liquid` is removed in a later pull request.

Rollback: restore each page's text from the snapshot.

## 8b. The Artists for Kids pages at release (P-35)

Script: `release.py unhide`, after `staged`.

The 18 pages are published but carry `seo.hidden` (noindex, out of the sitemap and the store's search), so the live site's search engines and search never find a page that shows only a title. At release, after their text moves in (§8) and their template changes (§3), the script deletes `seo.hidden` from each.

The team cuts the old site (artistsforkids.sd44.ca) back to registration the same day (P-30): After School Art, the camps and their forms, with links here. The list of old and new addresses is in `proposals/artists-for-kids-integration.md`, "Where each page goes".

Rollback: set `seo.hidden` back to 1 on each page, or hide the pages. The lessons, cards and events can stay: the old theme reads none of them.

## 8c. The Smith Foundation's pages at release (P-35, P-42, P-43)

Scripts: `release.py templates` (the standard page template), `staged`, `unhide`: the three pages are in `FOUNDATION_NEW`.

The same as the Artists for Kids pages (§8b): published with a title only and `seo.hidden` until release; at release their template changes, their text moves in and `seo.hidden` goes.

**Supporters waits for the gallery** (P-43, `gallery-questions.md` 8.1). It is in `HOLD_AT_RELEASE`, so `staged` and `unhide` skip it. If the gallery hasn't confirmed the list by release, the same day: take Supporters out of the new theme's menu (`menuUpdate`, the other items keep their IDs), take `foundation-supporters` out of the card group `foundation-take-part`, and hide the page. When the gallery confirms: take it out of `HOLD_AT_RELEASE`, run the three steps for it, put it back in the menu and the group, and link Donate's "donor page" to it (the one change to Donate's staged text still to make).

Rollback: set `seo.hidden` back to 1 on each page, or hide the pages. The exhibitions and cards can stay: the old theme reads none of them.

## 9. Frame products at release (P-19)

Script: `release.py frames` (dry run: `dry-runs/2026-09-26/frames.md`).

Each print's frame is its own product (product type Frame, collection `framing`), so search results fill with frames. At release, after publishing, the 16 active frames become **Unlisted**: still buyable, still offered on each print's page through `custom.featured_frame` (a metafield reference, which Liquid still returns) as the Framing choice that nests the frame under the print (DS-137), but out of search, collections and recommendations. The new theme already treats a frame as sold only with its print: a frame's own page points to its print and isn't listed by search engines. The draft Michael Snow frame stays a draft. Snapshot: `proposals/store-writes/snapshots/frames-2026-09-26.json`.

This waits for release because the old theme's add-a-frame popup looks frames up by their collection. Smoke test after: a search for "smith" shows no frames, and a print's Framed choice still adds its frame, nested under the print in the cart and at checkout.

Rollback: set the 16 back to Active from the snapshot.

## 9b. Page fields from the whole-site design review (DS-122, DS-129)

Decided by Michael on 2026-09-28; each waits for his go-ahead to write, with a before-snapshot, and is logged in `proposals/store-writes/README.md`. The theme is ready for both.

- **Permanent Collection's Browse button (DS-122):** the page's call to action (`custom.cta`, `gid://shopify/Metafield/190392604131625`) changes from `https://gordonsmithgallery.com/pages/permanent-collection#collection-search` to `https://gordonsmithgallery.com/pages/permanent-collection#collection-browse`, so "Browse" lands on "Browse the collection" (the theme gives that section the ID and makes the address relative). The label stays. Rollback: set the old address back.
- **Learning kits order (DS-129):** each kit, then its lesson plans, then its video. `load.py cards` creates the four one-kit groups and the two one-video groups ("Clay Lesson Video", "Trace Monotype Lesson Video"; headings for the gallery to confirm), then the Learning kits page's Card groups field takes the new order: only that row of `content.py page-fields` (the page `learning-kits`), since the rest are unchanged. No card changes. The old "afk-kits" and "afk-kit-videos" groups leave the page and stay in the store. Rollback: set the field back from the snapshot.

## 10. Not proposed

- No other redirects, no product or collection changes beyond part 4, no app installs, no checkout changes.
- Mailchimp: no change until the audit is complete (`baseline/mailchimp-audit.md`).
