# Store resource manifest (baseline)

Read-only Admin API snapshot taken 2026-09-25 at about 19:10 UTC through the Shopify connector. Nothing was changed. Theme-preview work does not sandbox any of these resources: menus, pages, collections, products, Files and definitions are shared by every theme (IMPLEMENTATION_PLAN.md, "Keep four change surfaces distinct").

## Store

| Field | Value |
| --- | --- |
| Name | Artists for Kids & The Gordon Smith Gallery |
| Shopify domain | `ed35ee-ea.myshopify.com` |
| Primary domain | `gordonsmithgallery.com` |
| Currency | CAD |
| Timezone | America/Los_Angeles (Liquid `'now'` follows this; see DESIGN.md §9.6 item 6) |

## Themes

| ID | Name | Role | Created | Updated |
| --- | --- | --- | --- | --- |
| 183162372393 | Colorblock: NEW WEBSITE | **MAIN (live)** | 2026-07-20 | 2026-09-25 19:02:55 UTC |
| 182990274857 | July 7 - OLD Updated copy of Dawn | Unpublished | 2026-07-07 | 2026-07-23 |
| 182550266153 | Updated copy of Dawn | Unpublished | 2026-06-04 | 2026-07-23 |
| 181481079081 | Copy of Dawn | Unpublished | 2026-03-17 | 2026-09-14 |
| 171508039977 | Studio | Unpublished | 2024-10-01 | 2026-09-14 |
| 171407442217 | Old- 06-04-26 Dawn | Unpublished | 2024-09-27 | 2026-09-14 |

The live theme reports Colorblock 15.5.0 (theme store ID 1499) in the storefront's `Shopify.theme` object. Its updated time matches, to the second, the last save of the product "Arnold Shives, Seven Sisters Range" (19:02:55 UTC), so it may reflect staff product edits rather than a theme-code change. The drift check before release compares files, not this timestamp.

## Menus

`new-website-menu-1` ("NEW WEBSITE MENU") is the live header menu. Parent items with children render as dropdown buttons, so the parent's own link is unreachable (see `screenshots/capture-log.json`, `navigation.desktop_items`).

| Parent (link) | Children |
| --- | --- |
| About (`/pages/about`, unreachable) | About Us, Contact, Volunteer, Permanent Collection, Plan Your Visit |
| Exhibitions (`/pages/exhibitions-1`, unreachable) | On Now, Past Exhibitions. **Upcoming Exhibitions is missing** |
| Artists For Kids (`/pages/artists-for-kids`) | none |
| Programs (`/pages/public-programs-1`, unreachable) | **Public Programs (repeats the parent's page)**, Speaker Series, Music At The Smith, Explore + Create, Art In Good Company |
| Smith Foundation (`/pages/the-smith-foundation`, unreachable) | **Smith Foundation (repeats the parent)**, Gordon and Marion, Donate |
| Shop (`/collections`, unreachable) | Our Story, 2026 Fall Portfolio, 2026 Spring Portfolio, **2025 Fall Portfolio (absolute `https://ed35ee-ea.myshopify.com/...` URL)**, 2025 Spring Portfolio, 2024 Fall Portfolio, Artists |

Other menus: `main-menu` (default; HOME, SHOP, ABOUT with Plan Your Visit and Contact, Portfolios, Artists; not used by the live header), `footer` (Search, Do not sell or share my personal information, Frequently Asked Questions as an absolute URL), `footer-menu-copy` (Frequently Asked Questions), `customer-account-main-menu` (Orders, Profile).

## Pages (35: 32 published, 3 unpublished)

| Title | Handle | Template suffix | Published | Updated |
| --- | --- | --- | --- | --- |
| Contact | contact | contact | yes | 2026-07-28 |
| Artists | artists | artists | yes | 2026-09-10 |
| About | about | (default) | yes | 2026-06-05 |
| Do not sell or share my personal information | data-sale-opt-out | (default) | yes | 2024-10-28 |
| 2025 Spring Portfolio | 2025-spring-portfolio | page | **no** | 2025-03-12 |
| Frequently Asked Questions | frequently-asked-questions | page | yes | 2026-06-03 |
| Public Programs | public-programs | page | **no** | 2026-07-20 |
| Upcoming Events | upcoming-events | page | yes | 2026-09-17 |
| Plan Your Visit | plan-your-visit | plan-your-visit | yes | 2026-09-22 |
| About Us | about-us | about-us | yes | 2026-09-10 |
| Gordon and Marion | gordon-and-marion | gordon-and-marion | yes | 2026-09-20 |
| Our Story | our-story | shop | yes | 2026-09-24 |
| The Smith Foundation | the-smith-foundation | the-smith-foundation | yes | 2026-08-13 |
| Engage | engage | page | yes | 2026-07-24 |
| Public Programs | public-programs-1 | public-programs | yes | 2026-08-14 |
| Speaker Series | speaker-series | speaker-series | yes | 2026-08-14 |
| Music At The Smith | music-at-the-smith | music-at-the-smith | yes | 2026-08-14 |
| Explore + Create | explore-create | explore-create | yes | 2026-08-14 |
| Art In Good Company | art-in-good-company | art-in-good-company | yes | 2026-09-20 |
| Permanent Collection | permanent-collection | permanent-collection | yes | 2026-08-13 |
| Artists For Kids | artists-for-kids | artists-for-kids | yes | 2026-09-20 |
| Exhibitions | exhibitions-1 | exhibitions-overview | yes | 2026-08-14 |
| Shop | shop | shop | yes | 2026-07-28 |
| Upcoming Exhibitions | upcoming-exhibitions | upcoming-exhibitions | yes | 2026-09-21 |
| Past Exhibitions | past-exhibitions | past-exhibitions | yes | 2026-07-30 |
| On Now | on-now | current-on-now-exhibition | yes | 2026-09-21 |
| Exhibition: One Hundred Artists Deep | exhibition-one-hundred-artists-deep | exhibition-ohad-2026 | yes | 2026-07-30 |
| Exhibition: From The Ground | exhibition-from-the-ground | exhibition-ftg | yes | 2026-07-30 |
| Exhibition: Stitched: Merging Photography and Textile Practices | exhibition-stitched-merging-photography-and-textile-practices | exhibition-stitched | yes | 2026-07-30 |
| Exhibition: Playhouse | exhibition-playhouse | exhibition-playhouse | yes | 2026-07-30 |
| Exhibition: Prevailing Landscapes | exhibition-prevailing-landscapes | exhibition-prevailing | yes | 2026-07-30 |
| Exhibition: The Art of Conversation | exhibition-the-art-of-conversation | exhibition-taoc | yes | 2026-07-31 |
| Donate | donate | donate | yes | 2026-09-20 |
| Volunteer | volunteer | volunteer | yes | 2026-08-05 |
| Exhibition Tours | exhibition-tours | page | **no** | 2026-08-13 |

Content notes from the page bodies read so far: the On Now and Upcoming Exhibitions pages both currently describe *Collect, Assemble, Gather* (September 25, 2026 to February 20, 2027); page bodies carry pasted Word markup with inline fonts (e.g. Poppins, 13.5pt), which TYPE-03 must neutralise.

## Collections (7)

| Title | Handle | Template suffix | Products |
| --- | --- | --- | --- |
| 2026 Fall Portfolio | 2026-fall-portfolio | alt-collection-temp | 5 |
| 2026 Spring Portfolio | 2026-spring-portfolio | collection-template | 3 |
| 2025 Fall Portfolio | 2025-fall-portfolio | collection-template | 3 |
| 2025 Spring Portfolio | 2025-spring-portfolio | collection-template | 5 |
| 2024 Fall Portfolio | 2024-fall-portfolio | collection-template | 5 |
| All Limited Editions | all-prints | all-products-template | 21 |
| Framing | framing | collection-template | 17 |

## Products (38: 21 limited-edition prints, 17 frames)

- Prints: 21 active. Titles carry Unicode mathematical italic letters for the artwork title (for example "Gordon Smith, 𝘗𝘦𝘯𝘥𝘦𝘳 𝘏𝘢𝘳𝘣𝘰𝘶𝘳, 2006"), which breaks search and screen readers (DS-16, proposal part 3). One print (Jack Shadbolt, *Toward a White Garden*) has no product type.
- Frames: 16 active, 1 draft (Michael Snow FRAME).
- Product template suffixes in use: default, `no-frame-product` (prints by Elizabeth McIntosh and Amelia Butcher, and four frames).
- Staff were editing products during this snapshot (Arnold Shives prints and frame saved 18:02 to 19:02 UTC).

## Definitions

- Page metafield definitions: none.
- Metaobject definitions: only Shopify's standard product-taxonomy types (paper finish, frame style, print edition type, and similar). No exhibition definition exists yet (proposal part 2).
