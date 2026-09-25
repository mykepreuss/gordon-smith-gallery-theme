# Proposed store-level changes

Changes to Shopify Admin resources that the theme work needs. None of these is made until the gallery approves the structure (approval package) and, for live resources, until release approval. Menus, pages, fields and products are shared by every theme, so a preview theme does not isolate them (`AGENTS.md`). Baseline state: `baseline/store-manifest.md`.

## 1. Main menu map (NAV-01 to NAV-04, EXH-01, EXH-02, SHOP-02)

Model (DS-11): a section with pages under it is one button; its main page is the first link inside, with its own label. A section without pages is a plain link. Labels below are proposals; the gallery sets the final wording (EXH-04). Order: Exhibitions first (P-09), then the rest in the live menu's order.

| Section | Type | Items, in order (destination) | Change from today |
| --- | --- | --- | --- |
| Exhibitions | Section | On now (`/pages/on-now`), Upcoming (`/pages/upcoming-exhibitions`), Past exhibitions (`/pages/past-exhibitions`) | Moves to the first place in the menu (P-09). Adds Upcoming (missing today). The Exhibitions overview page (`/pages/exhibitions-1`) leaves the menu and stays reachable from On now |
| About | Section | About the gallery (`/pages/about` or `/pages/about-us`, one page, Q: which), Plan your visit (`/pages/plan-your-visit`), Permanent collection (`/pages/permanent-collection`), Volunteer (`/pages/volunteer`) | The About page becomes reachable (today the parent label only opens the dropdown). Contact moves to the always-visible utility row and footer. About and About Us: gallery decides whether they are one page |
| Artists for Kids | Link | `/pages/artists-for-kids` | None. Approved 2026-09-25 as one link (P-15); the programme links to the Artists for Kids site stay on its page |
| Programs | Section | Public programs (`/pages/public-programs-1`), Speaker series, Music at the Smith, Explore + Create, Art in Good Company | "Public Programs" no longer repeats the section, because the section itself is not a link |
| Smith Foundation | Section | About the Foundation (`/pages/the-smith-foundation`), Gordon and Marion (`/pages/gordon-and-marion`), Donate (`/pages/donate`) | Renames the first item so it doesn't repeat the section |
| Shop | Section | Limited editions (`/pages/shop`), 2026 Fall Portfolio, 2026 Spring Portfolio, 2025 Fall Portfolio, 2025 Spring Portfolio, 2024 Fall Portfolio, Our story (`/pages/our-story`), Artists (`/pages/artists`) | Leads to the Shop landing page instead of Shopify's `/collections` list. 2025 Fall Portfolio uses the relative `/collections/2025-fall-portfolio` instead of the absolute myshopify URL |

Each section's own link in the Shopify menu editor points at its first item, so `snippets/gs-nav.liquid` raises no editor warning.

**How it is applied:** during review, as a separate new menu referenced only by the review theme (so the live header doesn't change). At release, either switch the live header to the reviewed menu or edit `new-website-menu-1` to match, recorded in the release change set.

## 2. Utility and footer menus (ACCESS-02, ACCESS-03)

| Menu | Items | Note |
| --- | --- | --- |
| ~~New `utility` menu~~ | Not needed: the theme builds the utility links in (DS-29): Contact from the contact-page theme setting, Newsletter (the band's anchor), Search, Cart | One store change fewer. Contact can't be dropped by a menu edit |
| Footer | Explore links (Exhibitions, Limited editions, Artists for Kids), Frequently asked questions (`/pages/frequently-asked-questions`, relative instead of the absolute URL), Do not sell or share my personal information | Social links come from theme settings with visible names (gallery supplies URLs). The footer section takes two menus: Explore, and an optional Legal menu for the small last-line links; store policies are added automatically. Until the footer menu is edited, the theme uses the existing `footer` menu as Explore, and its absolute FAQ link is made relative by the theme |

## 3. Template assignments (REUSE-01, DS-14)

Moving pages from their one-off templates to the closed set in `design-system/DESIGN.md` §7.4 is a store-level release action (the Admin assignment list reads the live theme). Until then, new templates are previewed on the review theme with `?view=`. Full mapping: DESIGN.md §7.4. With the new theme (P-13) none of today's page templates exist after publishing, so every page's assignment is set at release by a script run straight after publishing, with a snapshot of today's assignments for rollback.

Until the script runs, pages whose old template the new theme lacks fall back to the default page template, and Our Story (old template `shop`) renders as the Shop landing page (L-08). So the script is written and dry-run before release (plan, "Release gate and rollback"): it snapshots every page's template, maps each page to its new one, and prints the changes for Michael to check. At release it runs straight after publishing, and every page is opened to check it. Not written yet.

## 4. Field definitions (content model)

`design-system/proposals/content-model.md`, approved 2026-09-25 (DS-14 to DS-16):

1. Page fields (`custom.*`): hero image, hero is artwork, eyebrow, intro, programme, gallery images.
2. Exhibition entries (metaobject `exhibition`, web pages at `/pages/exhibitions/<entry>`), with the fields revised from the review of content in use: dates and dates note, curator credit, artists and collection artists, venue, opening reception, events, key image and caption, summary, body, installation photos, credits, funder logos, programme.
3. Product label fields (artist, title, year, medium, edition, dimensions, coming soon) and plain-text product titles.
4. Approved 2026-09-25 (P-16): card groups, events, page hero caption and call to action, collection photo credit, product availability note (content model parts 4 to 6).

Creating definitions is additive and doesn't change what visitors see, but it is still a store-level change: create them when implementation starts, with Michael's go-ahead, and record each in the pull request.

**Done 2026-09-25, with Michael's go-ahead:** the `exhibition` and `event` definitions, four exhibition entries and one event, active so they render in the development theme. Their addresses return 404 under the live theme. Log, IDs and undo steps: `proposals/store-writes/README.md`. Still to create: the other 11 exhibitions and the page, card, product and collection fields.

**Also done 2026-09-25, with Michael's go-ahead:** the page field, `card` and `card_group` definitions; the cards, card groups and events of the seven programme pages; and their field values. Still to create: fields on the other pages (About, Donate, Contact and the rest).

**Also done 2026-09-25, with Michael's go-ahead:** the product label and availability fields, the collection photo credit field, label values on the 21 limited editions, credits on the five portfolios, and the Shop page's hero. Product titles are unchanged; plain-text titles (DS-16) wait for release (§3 of the content model, migration).

## 5. Exhibition addresses at release (P-10)

Redirects only work from addresses that no longer load a page, so the order matters. At release, after the theme is published and the exhibition entries are active:

1. Hide (don't delete) the six exhibition pages, keeping them for rollback.
2. Create six URL redirects:

| From | To |
| --- | --- |
| `/pages/exhibition-one-hundred-artists-deep` | `/pages/exhibitions/one-hundred-artists-deep` |
| `/pages/exhibition-from-the-ground` | `/pages/exhibitions/from-the-ground` |
| `/pages/exhibition-stitched-merging-photography-and-textile-practices` | `/pages/exhibitions/stitched` |
| `/pages/exhibition-playhouse` | `/pages/exhibitions/playhouse` |
| `/pages/exhibition-prevailing-landscapes` | `/pages/exhibitions/prevailing-landscapes` |
| `/pages/exhibition-the-art-of-conversation` | `/pages/exhibitions/the-art-of-conversation` |

3. Open each old address and check it lands on its entry.
4. Clear the exhibition text repeated in the On Now, Upcoming and Upcoming Events page bodies; it lives in the entries now. Snapshot each body first, for rollback.

Rollback: republish the baseline theme, unhide the six pages, delete the six redirects, restore the three page bodies from their snapshots. Entry handles are proposals until the entries exist.

The entries are already active (created 2026-09-25); their pages return 404 only because the live theme has no exhibition template. Publishing the new theme makes every active entry public, so each one is checked before release.

## 6. Theme settings for the review theme

Values the theme's settings need (Online Store, Themes, Customize, Theme settings). These are theme data, not store resources: they live in the review theme's `config/settings_data.json` and change nothing else. The build sets the ones already known.

| Setting | Value | Status |
| --- | --- | --- |
| Address | 2121 Lonsdale Avenue, North Vancouver, BC V7M 2K6 | Set (DESIGN.md §6.10) |
| Land acknowledgement | The current footer's wording | Set (moved from the current theme) |
| Contact page, On now, Upcoming, Past, Exhibitions overview, Upcoming events and Shop landing pages | `contact`, `on-now`, `upcoming-exhibitions`, `past-exhibitions`, `exhibitions-1`, `upcoming-events`, `shop` | Set |
| Portfolios, newest first; All limited editions | The five portfolios, 2026 Fall first; `all-prints` | Set |
| Hours, email, phone, social links, newsletter consent wording | From the gallery (ACCESS-04) | Waiting |
| Main menu | `new-website-menu-1` until the review menu exists (§1) | Temporary |

## 7. Product titles at release (DS-16)

The 21 limited editions' titles carry Unicode italic letters (L-03). At release, each title becomes the same words in plain text (`proposals/store-writes/shop.py`, `plain()`). The new theme shows the label fields, so this changes the admin, order emails, search and the browser tab. The live theme shows the titles, which is why this waits for release.

Rollback: restore each title from `proposals/store-writes/snapshots/prints-2026-09-25.json`.

## 8. Not proposed

- No other redirects, no product or collection changes beyond part 4, no app installs, no checkout changes.
- Mailchimp: no change until the audit is complete (`baseline/mailchimp-audit.md`).
