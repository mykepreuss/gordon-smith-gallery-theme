# Content held in the current theme, and where it goes

The new theme (P-13) doesn't carry over the current theme's templates, so everything the current theme holds in its template and section settings has to move, or be dropped on purpose, before release. Page bodies, products, collections and files live in Shopify admin and are not affected.

Source: the baseline theme's templates and section groups (commit 27ef593), read 2026-09-25. Destinations marked **new** are the additions to the content model approved on 2026-09-25 (P-16; `design-system/proposals/content-model.md` parts 4 to 6).

**Build status (branch `build-new-theme`):** every theme-side home below exists in the new theme. Content already moved into it as defaults: the land acknowledgement (theme setting), the newsletter heading and sentence (from the Contact template), the product archive note and framing text, and the cart's sales policy (its privacy link made relative). Content that lives in fields and entries moved on 2026-09-25, with Michael's go-ahead, in four steps: exhibitions, programme pages, Shop, then everything else (`proposals/store-writes/README.md`). **Every row below now has its content in the new theme or the store.** Page text that changes at release (On Now, Upcoming, Upcoming Events, Donate, Gordon and Marion) is staged until then (DS-39, `proposals/store-changes.md` §8).

## What the inventory shows

- **Content leaks through the default page template.** About's hero image, its three organisation columns and a land acknowledgement sit in the default template, so every page without its own template shows them too: FAQ, Upcoming Events, Engage and the privacy opt-out page (checked on the live FAQ page).
- **Three templates no page uses:** `page.about` (still holding the theme's sample text, "Introduce your brand's story."), `page.about-us-template` and `page.engage` (the Engage page uses the default template).
- **Hand-picked lists go stale.** The home page features the 2026 Spring Portfolio while the announcement bar says Fall 2026 is out. Upcoming and Past Exhibitions are typed card by card into templates.
- **Empty or broken placeholders:** Speaker Series shows five "Past Speaker Series" year headings (2022 to 2026) with nothing inside; the Foundation's "2025 A Year In Review" button links to a Shopify admin address, which visitors can't open; Public Programs' "Music At The Smith" card has no link.
- **Two kinds of content have no home in the approved model:** card grids (image, title, text, link) on 5 pages, and dated event listings on 4 programme pages. The rule that per-page content never lives in template settings (DESIGN.md §7.3) means they need fields: parts 4 and 5 of the content model.

## Site-wide

| Current place | Content | New home |
| --- | --- | --- |
| Header: announcement bar | Two messages with links ("Fall 2026 Limited Editions Now Available", "Exhibition Opening: September 25th, 6 to 8 PM") | Dropped (DS-27, superseding DS-26). The home page carries the same news: exhibitions on now and upcoming from entries, and the newest portfolio |
| Header: menu | `new-website-menu-1` | The approved menu map (`proposals/store-changes.md` §1) |
| Footer | Land acknowledgement (full wording) | Footer theme setting, once. The shorter copies on exhibition and programme pages are dropped |
| Default page template | About's hero, three organisation columns, land acknowledgement | About only: hero image field, card group **new**. Nothing on other pages |

## Home

| Content | New home |
| --- | --- |
| Rotating banner, 4 images, autoplay | The hero leads with the exhibition on now (DS-30). When nothing is on, it shows one image from the home template's settings: the banner's first image (`ON9DA8_1.jpg`) is set. No autoplay carousel |
| The whole On Now page embedded | Exhibitions on now and upcoming, from exhibition entries |
| "Shop Limited Editions", 2026 Spring Portfolio, "View Shop" | Shop feature: the newest portfolio automatically, linking to the Shop landing |
| Two frame blocks | Dropped (the product page offers the frame) |

## Exhibitions

| Template | Content | New home |
| --- | --- | --- |
| Six `page.exhibition-*` | Banner image and credit, 1 to 9 installation images and credit, land acknowledgement | Exhibition entries (P-10, P-11): key image and caption, installation views and credit |
| `page.current-on-now-exhibition`, `page.upcoming-exhibitions` | *Collect, Assemble, Gather*; three upcoming cards (image, dates, title) | Exhibition entries; the lists build themselves |
| `page.past-exhibitions` | 12 cards (image, dates, title, link); 6 link to pages, 6 older ones (2020 to 2023) don't | 12 exhibition entries. The 6 older ones hold title, dates and image, and their cards don't link (DS-25, follows from P-13) |
| `page.exhibitions-overview` | Rotating banner (4 images) and credit | Hero image and caption fields |

## Programme and information pages

| Template (page) | Content | New home |
| --- | --- | --- |
| `page.artists-for-kids` | Banner and credit; 6 cards linking to the Artists for Kids site; "Artists For Kids Website" button | Hero image, caption **new**; card group **new**; call to action **new** |
| `page.public-programs` | Rotating banner (5); 4 cards to programme pages | Hero image; card group **new** (with the missing Music at the Smith link) |
| `page.explore-create` | Rotating banner (5) and credit; "Upcoming Calendar", 4 dated drop-ins | Hero image, caption; event entries **new** |
| `page.music-at-the-smith` | Rotating banner (5); "Upcoming Concerts": La Modestine, November 7, 2026, image, "Tickets Coming Soon" | Hero image; event entry **new** with a ticket link |
| `page.speaker-series` | Rotating banner (3); upcoming talk (Omer Arbel, November 26, 2026, portrait, two paragraphs); empty "Past Speaker Series" | Hero image; event entry **new**; past speakers in the page body if the gallery supplies them, otherwise dropped |
| `page.art-in-good-company` | Banner; upcoming session (October 8, 2026, 2:30 to 4 PM, image) | Hero image; event entry **new** |
| `page.the-smith-foundation` | Rotating banner (5); 5 cards (programs, donations, gala, scholarships, endowment); "2025 A Year In Review" button; Board of Directors, 14 people with photo, name, role | Hero image; two card groups **new** (programmes, board); call to action **new**, pointing at the public file address |
| `page.donate` | Banner; "Ways To Give", 4 cards (online form, email, mail, phone); tax receipt note | Hero image; card group **new**; the note in the page body |
| `page.permanent-collection` | Heading, "Explore over 1,000 + Works...", "BROWSE" to the external catalogue; banner | Hero image; intro field; call to action **new** |
| `page.volunteer` | Rotating banner (3); "VOLUNTEER FORM" button to a PDF | Hero image; call to action **new** |
| `page.gordon-and-marion` | Banner; Vimeo video "Gordon Smith's Magic" with a cover image | Hero image; the video embedded in the page body |
| `page.plan-your-visit`, `page.about-us` | Banner (and the page's own body) | Hero image field |
| `page.contact` | "Contact Us"; contact form; newsletter ("Join Our Newsletter" and a sentence) | Contact template; the newsletter band is site-wide (DS-09) and reuses this wording until the gallery supplies final copy |
| `page.engage` (unused) | 3 columns | Nothing today; a card group if the gallery wants it |
| `page.shop` (Shop and Our Story) | Rotating banner; the Our Story page embedded; photo credit | Shop landing: one introduction and the portfolio navigation (DS-14, SHOP-01, SHOP-02); Our Story keeps its own page |

## Shop

| Template | Content | New home |
| --- | --- | --- |
| Three collection templates | Collection banner; "Photo(graphy) by Rachel Topham"; hand-picked portfolio lists | One collection template: collection image and description, photo credit field **new** |
| Four product templates | Vendor line; "The first edition is archived in the ... Permanent Collection"; "AVAILABLE FOR PURCHASE SEPT 25 AT NOON (PT)"; Disclosures; "Add a Frame" with framing text and the linked frame (`custom.featured_frame`); "You may also like" | One product template: label from product fields; the archive note and framing text as theme settings (the same on every product); availability from `custom.coming_soon` plus an availability note field **new**; disclosures, linked frame and related products kept |
| Cart | Policy text ("All sales are final..."); two "Complete your artwork" frame blocks | Policy text as a cart setting; the frame blocks dropped (they never worked: `baseline/theme-check.txt`) |

Standard templates (404, search, blog, article, password, gift card, customer accounts) hold no gallery content; the new theme's own versions replace them.
