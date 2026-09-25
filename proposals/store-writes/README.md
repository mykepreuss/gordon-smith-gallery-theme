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
