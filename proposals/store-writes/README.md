# Store writes log

Every write to the store's Admin resources, with what it was for and how to undo it. Theme files aren't here: they're in Git and pushed only to the review theme (`AGENTS.md`).

Before any write: recheck the store domain, the live theme ID and role, and take a before-snapshot.

## 2026-09-25: exhibition and event definitions, first entries

**Why:** to review the exhibition pages with real content in the development theme. Michael's go-ahead, 2026-09-25 ("Create entries"). Definitions are content model parts 2 and 5 (approved, P-10 to P-12, P-16).

**Checked first:** store `ed35ee-ea.myshopify.com` (Artists for Kids & The Gordon Smith Gallery), timezone America/Los_Angeles; live theme `183162372393` "Colorblock: NEW WEBSITE", role MAIN (`shopify theme list`). Before-snapshot: the store had 20 metaobject definitions, all Shopify's standard product-taxonomy types (`shopify--*`), and no `exhibition` or `event` type.

**Made through the Shopify connector (Admin GraphQL):**

| What | ID | Source |
| --- | --- | --- |
| Definition `exhibition` (22 fields, publishable, renderable, web pages at `/pages/exhibitions/<handle>`, storefront read) | `gid://shopify/MetaobjectDefinition/23753359657` | `definitions.py exhibition` |
| Definition `event` (9 fields, publishable, storefront read; `exhibition` field limited to the definition above) | `gid://shopify/MetaobjectDefinition/23753392425` | `definitions.py event` |
| Exhibition `collect-assemble-gather`, active. From the On Now page: dates, curator credit, 19 artists, opening reception, key image (artwork) and caption, summary, text, credits, Canada Council logo | `gid://shopify/Metaobject/608352043305` | `entries.py exhibitions` |
| Exhibition `one-hundred-artists-deep`, active. From its page and template: dates, curator, 8 artists and 3 founding artists, key image and credit, summary, text, 9 installation views and credit | `gid://shopify/Metaobject/608352076073` | same |
| Exhibition `against-the-latitude-of-progress`, active. From the Upcoming card: title, dates, image (artwork). No text yet, so its card doesn't link | `gid://shopify/Metaobject/608352108841` | same |
| Exhibition `play`, active. From the Past archive (2020 to 2021): title, dates, image (DS-25) | `gid://shopify/Metaobject/608352141609` | same |
| Event `curatorial-tour-collect-assemble-gather`, active. From the On Now page: October 26, 2026, 3:30 to 4:30 PM, linked to Collect, Assemble, Gather | `gid://shopify/Metaobject/608352272681` | `entries.py event` |

Text is the gallery's, moved without rewriting. Pasted formatting (inline Poppins, Word markup) stayed behind. Two small format changes to fit the fields: the curator credit and reception note lost their trailing punctuation and pipes ("Welcome Ceremony | 7 PM" became "Welcome ceremony at 7 PM", the content model's example). Approved by Michael, 2026-09-25 (P-17).

**Effect on the live site:** none seen. The entries' addresses return 404 on gordonsmithgallery.com, because the live theme has no exhibition template; nothing on the live theme reads these entries. Checked 2026-09-25 (`/pages/exhibitions/collect-assemble-gather`, `/pages/exhibitions/play`).

**Undo:** delete the five entries (Content, Metaobjects), then the `event` definition, then the `exhibition` definition. Nothing else refers to them.

**Still to create** (content model part 2, migration step 1): the other 11 exhibitions, the other events, and the page, card, product and collection fields (parts 1, 3, 4, 6).

## 2026-09-25: programme pages (page fields, cards, events)

**Why:** to review the seven programme pages with their real content. Michael's go-ahead, 2026-09-25 ("All seven pages"). Definitions are content model parts 1, 4 and 6 (approved, DS-14, P-16).

**Checked first:** same store and live theme as above. Before-snapshot: none of the seven pages had any `custom` fields; no `card` or `card_group` definitions existed; no page field definitions existed.

**Made through the Shopify connector** (payloads from `programmes.py`; created IDs in `created/`):

| What | IDs |
| --- | --- |
| Definition `card` (image, title, text, link; storefront read) | `gid://shopify/MetaobjectDefinition/23754375465` |
| Definition `card_group` (heading, cards; storefront read) | `gid://shopify/MetaobjectDefinition/23754408233` |
| 9 page field definitions, namespace `custom`, pinned on the page editor: `hero_image`, `hero_is_artwork`, `hero_caption`, `eyebrow`, `intro`, `cta`, `programme`, `card_groups`, `gallery_images` | `gid://shopify/MetafieldDefinition/272783147305` to `…409449` |
| 29 cards: Artists for Kids' 6 programmes (linking to artistsforkids.sd44.ca), Public Programs' 4, the Foundation's 5 ways to take part, and its 14-person board | `created/cards.json` |
| 4 card groups: `afk-programmes`, `public-programs`, `foundation-take-part`, `foundation-board` (heading "Board of Directors") | `created/card-groups.json` |
| 7 events, active: Explore + Create on September 26 and October 3, 10 and 17, 2026; Art In Good Company on October 8; La Modestine (Music at the Smith) on November 7; Omer Arbel (Speaker Series) on November 26. Each linked to its programme page | `gid://shopify/Metaobject/608367575337` to `…771945` |
| 16 field values on the seven live pages: hero images (each page's first banner image), hero captions (Artists for Kids, Explore + Create), programme (Artists for Kids, Smith Foundation), calls to action (Artists For Kids Website; 2025 A Year In Review), card groups | Pages `artists-for-kids`, `public-programs-1`, `the-smith-foundation`, `speaker-series`, `music-at-the-smith`, `explore-create`, `art-in-good-company` |

Text is the gallery's, moved without rewriting. Choices made while moving it, approved by Michael on 2026-09-25 (P-17). Omer Arbel's biography is still open for the gallery:

- The Foundation's "More" links become links on the card titles; a link reading only "More" doesn't say where it goes. The three "More" links that pointed nowhere (gala, scholarships, endowment) are left out.
- Public Programs' cards had no images; each now shows its programme page's hero image. Music at the Smith's card gets the link it was missing.
- The 2025 A Year In Review button pointed at a Shopify admin address visitors can't open; it now opens the PDF at `/cdn/shop/files/SMITH_ANNUAL_REPORT_2025.pdf`, and the theme marks it "(PDF)".
- Speaker Series: the talk's three paragraphs go in the event summary, with "Doors 6 PM, talk begins 6:30 PM." first. Omer Arbel's separate biography paragraph isn't moved yet; the gallery can add it to the page text or the summary. The empty "Past Speaker Series" year headings are dropped.
- Art In Good Company's "Description of Activity Coming soon" placeholder isn't moved; the event has no summary until there is one.
- Explore + Create's shorter land acknowledgement is dropped: the footer carries the full one on every page.

**Effect on the live site:** none. The live theme reads none of these fields or entry types (checked in `baseline/theme/`), and the pages still load normally.

**Undo:** clear the 16 page field values; delete the 7 events, 4 card groups and 29 cards; then delete the 9 page field definitions and the `card_group` and `card` definitions.

## 2026-09-25: Shop (product labels, collection credits, Shop page)

**Why:** to review the Shop with real museum labels. Michael's go-ahead, 2026-09-25 ("Yes, all of it"). Definitions are content model parts 3 and 6 (approved, DS-16, P-16).

**Checked first:** same store and live theme. Before-snapshot: the 21 limited editions' titles, collections, existing custom fields (only `featured_frame`) and the facts in their descriptions are in `snapshots/prints-2026-09-25.json`; no collection or the Shop page had custom fields; no product label or collection credit definitions existed.

**Made through the Shopify connector** (payloads from `shop.py`):

| What | IDs |
| --- | --- |
| 8 product field definitions, pinned: `artist`, `artwork_title`, `year`, `medium`, `edition`, `dimensions`, `coming_soon`, `availability_note` | `gid://shopify/MetafieldDefinition/272792060201` to `…289577` |
| Collection field definition `photo_credit`, pinned | `gid://shopify/MetafieldDefinition/272792322345` |
| 125 label values on the 21 limited editions (`python3 shop.py review` prints them as a table) | Products listed in the snapshot |
| Photo credits on the five portfolios ("Photography by Rachel Topham" on 2026 Fall, "Photo by Rachel Topham" on the other four, as their old templates said) | Collections `2026-fall-portfolio`, `2026-spring-portfolio`, `2025-fall-portfolio`, `2025-spring-portfolio`, `2024-fall-portfolio` |
| Shop landing page: hero image (`GSG_2026_Fall_Edition_1.jpg`, the old banner's first slide) and caption "Photography by Rachel Topham" | Page `shop` |

Label values come only from each print's own title and description: artist, title and year from the title (Unicode styled letters made plain); medium from "Technique:"; edition from "Edition:" ("Edition: 50" became "Edition of 50"); dimensions from "Dimensions:", "Size:" or "Image size:" (the last keeps its label). Approved by Michael, 2026-09-25 (P-17). Still open for the gallery: a medium for *Good Luck (wheelbarrow)*, and trimming the descriptions. Notes:

- Samuel Roy-Bois, *Good Luck (wheelbarrow)*: the description has no Technique line, so the label has no medium.
- Russna Kaur, *What remains after bloom*: the Technique line is a paragraph about the process; it's the medium as written. Tiles show two lines of it.
- Product titles are unchanged. They still carry Unicode italic letters in the admin, order emails and the browser tab; the theme shows the labels instead. Plain-text titles (DS-16) are a live change, made at release.
- The descriptions still open with the name, title and a "Print details" list that now repeat the label. The gallery can trim them; paper and signature details have no field and stay in the description.

**Effect on the live site:** none. The live theme reads only `custom.featured_frame` among product fields (checked in `baseline/theme/`).

**Undo:** clear the 132 values, then delete the 9 definitions.

## 2026-09-25: the rest of the content (exhibitions, pages, staged text, review menus)

**Why:** to review and improve every page with its real content before release. Michael's go-ahead, 2026-09-25 ("migrate all content into our new theme so we can review and improve comprehensively"). He chose to stage the page text that changes at release (DS-39) and to leave the site email blank until the gallery chooses one.

**Checked first:** store `ed35ee-ea.myshopify.com`; live theme `183162372393` "Colorblock: NEW WEBSITE", role live (`shopify theme list`); development theme 184755814697 present. Before-snapshots: every page's text, template and fields in `snapshots/pages-2026-09-25.json`; the entries, menus and page field definitions that existed in `snapshots/entries-2026-09-25-before-migration.json`. The live theme reads no page fields (`baseline/theme/`).

**Made through the Shopify connector** (payloads from `migration.py`; created IDs in `created/migration-*.json`):

| What | IDs |
| --- | --- |
| Page field definition `release_body` ("Text at release (temporary)"), not pinned | `gid://shopify/MetafieldDefinition/272804249897` |
| 11 exhibitions, active. Five past shows from their pages: *From the Ground*, *Stitched*, *Playhouse*, *Prevailing Landscapes*, *The Art of Conversation*. Five older shows from the Past cards (title, dates, image; DS-25): *Endless Summer*, *Paths*, *We Can Only Hint at This with Words*, *Beyond the Horizon*, *Unfixed*. The Upcoming page's third card: *Fall 2027 Exhibition* | `created/migration-exhibitions.json` |
| 7 cards: About's three organisation columns (from the old default template) and Donate's four "Ways To Give" | `created/migration-cards.json` |
| 2 card groups: `about-organisations`, `donate-ways-to-give` | `created/migration-card-groups.json` |
| 14 field values on 8 pages: hero images (each page's old banner or first slide) on About, About Us, Exhibitions, Donate, Permanent Collection, Volunteer, Gordon and Marion and Plan Your Visit; the Exhibitions hero caption; card groups on About and Donate; Permanent Collection's intro and call to action (Browse, the collection catalogue); Volunteer's call to action (Volunteer Form, the PDF) | Pages as listed |
| Staged text (`release_body`) on 5 pages. On Now, Upcoming Exhibitions and Upcoming Events: cleared, since each repeats *Collect, Assemble, Gather*. Donate: its text plus the tax receipt note from the old template. Gordon and Marion: its text plus the Vimeo video from the old template ("Video: Gordon Smith's Magic") | Pages `on-now`, `upcoming-exhibitions`, `upcoming-events`, `donate`, `gordon-and-marion` |
| 3 menus, referenced only by the new theme: `new-theme-main` (the approved menu map, `store-changes.md` §1), `new-theme-explore` and `new-theme-legal` (the footer, §2) | `created/migration-menus.json` |

Read back after writing: every entry, card and page field matches `migration.py` exactly.

Text is the gallery's, moved without rewriting; exhibition text is read from the page snapshot, so nothing was retyped. Choices made while moving it, for Michael to check:

- **Exhibition summaries:** each page's first paragraph. *Stitched*'s first paragraph is six sentences, so its first two are the summary and the rest opens the text, in the same reading order.
- **Curators and artists:** lines as written. *From the Ground* had no artist list, so its artists and collection artists are read from its text, which keeps them too. Lists ending "X and Y" became two names, except "Hannah Jickling and Reed H. Reed", who work as a pair.
- **Repeated images left out:** *From the Ground*'s and *Stitched*'s galleries each repeated the key image, and *Prevailing Landscapes*' one gallery image was the key image. *The Art of Conversation*: the page's banner is the key image, and the Past card's image is its one installation view.
- **Older shows:** titles in title case, from the cards' capitals. *Paths* and *Unfixed* show artworks, so their images are marked as artworks (shown whole).
- **Fall 2027 Exhibition:** title as on the card, "Coming soon, September 2027" as the dates note, September 1, 2027 as the expected start (the field needs a date). No text, so its card doesn't link.
- **About's organisation cards:** text cards titled with each organisation's name. The columns' only titles were logos, which the footer carries. The dead "Exhibitions" and "The Foundation" labels now link to the Exhibitions and Smith Foundation pages.
- **Labels in capitals** (BROWSE, VOLUNTEER FORM) are stored as Browse and Volunteer Form; buttons set their own case.
- **Permanent Collection's long heading** ("Artists For Kids & The Gordon Smith Gallery Permanent Collection") is dropped: the page title and the first sentence of its text say the same.
- **Hours and phone** in theme settings come from Plan Your Visit's gallery hours and the Contact page (Git, not a store write).

For the gallery:

- The Donate card "Online Form" refers to a form "above", but the donation form is switched off on the live page too.
- Upcoming Events' copy of *Collect, Assemble, Gather* lists Carl Heywood among the artists; On Now's newer copy, which the entry follows, doesn't.
- *Stitched*'s credits link the Smith Foundation to `smithfoundation.co/…/smithfoundation.ca`, which doesn't open.
- About and About Us are still two pages. The menu links About Us, as today; About keeps its text and gains the organisation cards.

**Effect on the live site:** none. The live theme reads no page fields and has no exhibition template (the new entries' addresses return 404), and the three menus aren't used by it.

**Undo:** delete the 3 menus; clear the 19 page field values; delete the 2 card groups, 7 cards and 11 exhibitions; delete the `release_body` definition.

**At release:** a script moves each staged text into its page, stopping if the live text no longer matches `snapshots/pages-2026-09-25.json`, then deletes the values and the definition (`store-changes.md` §8).

## 2026-09-26: page pass (staged text on Donate and Artists)

**Why:** fixes from the review of the remaining pages. Michael's go-ahead, 2026-09-26 ("Fix what the review found" and "Design passes on the pages not yet reviewed").

**Checked first:** the live text of Donate and Artists still matches `snapshots/pages-2026-09-25.json` (Donate's later update time is the field write of 2026-09-25; Artists hasn't changed since 2026-09-25 19:40 UTC).

**Made through the Shopify connector** (payload from `migration.py page-pass`):

| What | Page |
| --- | --- |
| Donate's staged text rewritten: "Ways to Support" becomes a heading and "Every contribution makes a difference:" the paragraph after it. The two phrases sat in one heading, split by line breaks, so they read as two headings. Words unchanged; the tax receipt note stays at the end | `donate` |
| Artists' staged text added: its two paragraphs, then its 59 artist links as one list, in the same order with the same addresses. Today they're loose links and line breaks centred in two blocks; as a list they flow into columns (DS-45) | `artists` |

**For the gallery:** three names on the Artists page may be misspelled: "Atilla Lukacs" (his site is attilarichardlukacs.com), "Jean McEwan" (the link is to Jean McEwen) and "Graham Gillmore" (Permanent Collection's text says Graham Gilmore). Moved as written.

**Effect on the live site:** none; the live theme doesn't read the staged field.

**Undo:** set Donate's staged text back to the 2026-09-25 value (`migration.py` before this pass: text plus the tax receipt note), and clear Artists' staged text.

## 2026-09-26: programme on Donate and Gordon and Marion

**Why:** the header logo follows the page's programme (DS-47). Michael asked for the Foundation logo on the Foundation's pages: Donate and Gordon and Marion sit under Smith Foundation in the menu, beside the Foundation page, which already had it.

**Made through the Shopify connector:** the `programme` field set to "Smith Foundation" on pages `donate` and `gordon-and-marion`. Their title boxes take the Foundation's colour too (DS-04).

**Effect on the live site:** none; the live theme reads no page fields.

**Undo:** clear the two values.

## 2026-09-26: Donate's Email card, typo

**Why:** the card read "email us as at". Michael asked for it fixed, 2026-09-26. The rest of the words are the gallery's, unchanged.

**Checked first:** store `ed35ee-ea.myshopify.com`, live theme `183162372393` "Colorblock: NEW WEBSITE", role MAIN (Admin API). Before-snapshot: `snapshots/card-donate-email-2026-09-26-before.json`.

**Made through the Shopify connector:** card `donate-email` (`gid://shopify/Metaobject/608389398825`), field `text`: "...email us as at admin@smithfoundation.ca" became "...email us at admin@smithfoundation.ca". Nothing else on the entry changed. `migration.py` has the corrected text, so a re-run can't bring the typo back.

**Effect on the live site:** none; the live theme reads no card entries. The live Donate page shows the same words from the live theme's own template, which keeps the typo until release: the live theme isn't written to (AGENTS.md).

**Undo:** set the field back to the value in the snapshot.

## 2026-09-26: About's Gallery card links to On Now

**Why:** there is no Exhibitions overview page any more (P-20, Michael, 2026-09-26). The card `about-gordon-smith-gallery` linked its "Exhibitions" label to it.

**Made through the Shopify connector:** the card's link now goes to `/pages/on-now`, label unchanged (`migration.py` updated to match).

**Effect on the live site:** none; the live theme doesn't read cards. The overview page's own field values (hero image, caption) stay on the page, which is hidden at release.

**Undo:** set the link back to `https://gordonsmithgallery.com/pages/exhibitions-1`.

## 2026-09-26: two fixes from verification

**Why:** the verification and release-preparation pass (Michael, 2026-09-26: "do the hero crop and all other backlog items we can").

**Checked first:** store `ed35ee-ea.myshopify.com`; live theme `183162372393` unchanged.

| What | Before | After |
| --- | --- | --- |
| Alt text on the Canada Council logo file (`gid://shopify/MediaImage/45716498317609`, `CAC-lockup-EN-RGB-Black.png`), the funder logo on *Collect, Assemble, Gather* | empty | "Canada Council for the Arts" |
| Medium on *Good Luck (wheelbarrow)* by Samuel Roy-Bois (`gid://shopify/Product/9501294690601`, `custom.medium`) | not set: the description has no Technique line | "archival pigment print", from the description's own second list of details ("archival pigment print on Legacy Baryta paper") |

**Effect on the live site:** none. The live theme shows this logo inside the On Now page's own text, with its own `alt`, and doesn't read label fields.

**Undo:** set the alt text back to empty; delete the medium value.

## 2026-09-26: About Us, each organisation beside its logo (DS-50)

**Why:** Michael, 2026-09-26: "Improve the design of this page: /pages/about-us. We should use the correct logo for each text description and integrate the logo and text better." Today the page shows one combined logo image, then three descriptions under capitalised headings, so no logo sits with its own text.

**Checked first:** store `ed35ee-ea.myshopify.com`; live theme `183162372393` "Colorblock: NEW WEBSITE", role MAIN; review theme `184767250729`, role UNPUBLISHED (Admin API). About Us's text matched `snapshots/pages-2026-09-25.json`. Before-snapshot: `snapshots/about-us-2026-09-26-before.json` (the card definition's four fields and 30 cards; About Us's only field, its hero image).

**Made through the Shopify connector** (payloads from `about_us.py`; created IDs in `created/about-us-*.json`):

| What | ID |
| --- | --- |
| Card definition: new field `logo` ("Logo"; Gallery, Smith Foundation or Artists for Kids) | `gid://shopify/MetaobjectDefinition/23754375465` |
| Card `about-us-gallery`: "The Gordon Smith Gallery of Canadian Art", logo Gallery, link "Plan your visit" | `gid://shopify/Metaobject/608631816489` |
| Card `about-us-artists-for-kids`: "Artists for Kids", logo Artists for Kids, link "More about Artists for Kids" | `gid://shopify/Metaobject/608631882025` |
| Card `about-us-foundation`: "The Gordon and Marion Smith Foundation for Young Artists", logo Smith Foundation, link "More about the Foundation" | `gid://shopify/Metaobject/608631947561` |
| Card group `about-us-organisations` (no heading), the three cards in the page's order | `gid://shopify/Metaobject/608631980329` |
| About Us: `card_groups` set to that group; staged text (`release_body`) set to none | Page `about-us` |

The descriptions are the gallery's, read from the snapshot, word for word. The card titles are the page's headings in normal capitals; the logos show them on screen and the titles are read by screen readers. The three links are new, pointing to the pages the header already has. At release the page's own text goes: its three descriptions now live in the cards, and the combined logo image above them would repeat the logos.

**Effect on the live site:** none. The live theme reads no card entries or page fields, and the live About Us page still shows its own text and image (checked 2026-09-26). The review theme shows the cards once `main` has the logo cards; until then it shows them as plain text cards.

**Undo:** clear About Us's `card_groups` and `release_body`; delete the card group and the three cards; delete the `logo` field from the card definition.

## 2026-09-26: About's organisation cards get their logos (DS-50)

**Why:** Michael, 2026-09-26: "DS-50 approved, apply logos to the About page too."

**Checked first:** same store and live theme as the entry above. Before-snapshot: `snapshots/about-cards-2026-09-26-before.json` (the three cards had no logo; their other fields are unchanged and listed in `migration.py`).

**Made through the Shopify connector** (payload from `about_us.py about-logos`; `migration.py` has the same values, so a re-run matches):

| Card | ID | Logo |
| --- | --- | --- |
| `about-artists-for-kids` | `gid://shopify/Metaobject/608389267753` | Artists for Kids |
| `about-gordon-smith-gallery` | `gid://shopify/Metaobject/608389300521` | Gallery |
| `about-smith-foundation` | `gid://shopify/Metaobject/608389333289` | Smith Foundation |

The words, titles, links and order are unchanged: Artists for Kids first, as on the old page, whose text is Artists for Kids' history.

**Effect on the live site:** none; the live theme reads no card entries, and the live About page still loads normally (checked 2026-09-26).

**Undo:** clear the Logo field on the three cards.
