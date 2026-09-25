# Proposed store-level changes

Changes to Shopify Admin resources that the theme work needs. None of these is made until the gallery approves the structure (approval package) and, for live resources, until release approval. Menus, pages, fields and products are shared by every theme, so a preview theme does not isolate them (`AGENTS.md`). Baseline state: `baseline/store-manifest.md`.

## 1. Main menu map (NAV-01 to NAV-04, EXH-01, EXH-02, SHOP-02)

Model (DS-11): a section with pages under it is one button; its main page is the first link inside, with its own label. A section without pages is a plain link. Labels below are proposals; the gallery sets the final wording (EXH-04). Order: Exhibitions first (P-09), then the rest in the live menu's order.

| Section | Type | Items, in order (destination) | Change from today |
| --- | --- | --- | --- |
| Exhibitions | Section | On now (`/pages/on-now`), Upcoming (`/pages/upcoming-exhibitions`), Past exhibitions (`/pages/past-exhibitions`) | Moves to the first place in the menu (P-09). Adds Upcoming (missing today). The Exhibitions overview page (`/pages/exhibitions-1`) leaves the menu and stays reachable from On now |
| About | Section | About the gallery (`/pages/about` or `/pages/about-us`, one page, Q: which), Plan your visit (`/pages/plan-your-visit`), Permanent collection (`/pages/permanent-collection`), Volunteer (`/pages/volunteer`) | The About page becomes reachable (today the parent label only opens the dropdown). Contact moves to the always-visible utility row and footer. About and About Us: gallery decides whether they are one page |
| Artists for Kids | Link | `/pages/artists-for-kids` | None, unless the external-site links move into the menu (Q5); then it becomes a section with "About Artists for Kids" first and the external links after it, each with the external cue |
| Programs | Section | Public programs (`/pages/public-programs-1`), Speaker series, Music at the Smith, Explore + Create, Art in Good Company | "Public Programs" no longer repeats the section, because the section itself is not a link |
| Smith Foundation | Section | About the Foundation (`/pages/the-smith-foundation`), Gordon and Marion (`/pages/gordon-and-marion`), Donate (`/pages/donate`) | Renames the first item so it doesn't repeat the section |
| Shop | Section | Limited editions (`/pages/shop`), 2026 Fall Portfolio, 2026 Spring Portfolio, 2025 Fall Portfolio, 2025 Spring Portfolio, 2024 Fall Portfolio, Our story (`/pages/our-story`), Artists (`/pages/artists`) | Leads to the Shop landing page instead of Shopify's `/collections` list. 2025 Fall Portfolio uses the relative `/collections/2025-fall-portfolio` instead of the absolute myshopify URL |

Each section's own link in the Shopify menu editor points at its first item, so `snippets/gs-nav.liquid` raises no editor warning.

**How it is applied:** during review, as a separate new menu referenced only by the review theme (so the live header doesn't change). At release, either switch the live header to the reviewed menu or edit `new-website-menu-1` to match, recorded in the release change set.

## 2. Utility and footer menus (ACCESS-02, ACCESS-03)

| Menu | Items | Note |
| --- | --- | --- |
| New `utility` menu | Contact (`/pages/contact`), Newsletter (link to the newsletter band), Search (`/search`) | The theme adds Cart. Shown in the header row on desktop and in the Menu drawer |
| Footer | Explore links (Exhibitions, Limited editions, Artists for Kids), Frequently asked questions (`/pages/frequently-asked-questions`, relative instead of the absolute URL), Do not sell or share my personal information | Social links come from theme settings with visible names (gallery supplies URLs) |

## 3. Template assignments (REUSE-01, DS-14)

Moving pages from their one-off templates to the closed set in `design-system/DESIGN.md` §7.4 is a store-level release action (the Admin assignment list reads the live theme). Until then, new templates are previewed on the review theme with `?view=`. Full mapping: DESIGN.md §7.4.

## 4. Field definitions (content model)

`design-system/proposals/content-model.md`, approved 2026-09-25 (DS-14 to DS-16):

1. Page fields (`custom.*`): hero image, hero is artwork, eyebrow, intro, programme, gallery images.
2. Exhibition entries (metaobject `exhibition`, web pages at `/pages/exhibitions/<entry>`), with the fields revised from the review of content in use: dates and dates note, curator credit, artists and collection artists, venue, opening reception, events, key image and caption, summary, body, installation photos, credits, funder logos, programme.
3. Product label fields (artist, title, year, medium, edition, dimensions, coming soon) and plain-text product titles.

Creating definitions is additive and doesn't change what visitors see, but it is still a store-level change: create them when implementation starts, with Michael's go-ahead, and record each in the pull request. Exhibition entries are created as drafts.

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
4. Clear the copy of *Collect, Assemble, Gather* from the On Now and Upcoming page bodies; it lives in its entry.

Rollback: republish the baseline theme, unhide the six pages, delete the six redirects. Entry handles are proposals until the entries exist.

## 6. Not proposed

- No other redirects, no product or collection changes beyond part 4, no app installs, no checkout changes.
- Mailchimp: no change until the audit is complete (`baseline/mailchimp-audit.md`).
