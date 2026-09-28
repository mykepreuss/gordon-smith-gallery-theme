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

## 2026-09-26: About becomes About Artists for Kids (P-23)

**Why:** Michael, 2026-09-26: "/about-us and /about look very similar, why is this? I think /about should be /about-artists-for-kids and be focused on that part of the organization." They looked alike because both had the building photo as their hero and the same three organisation rows at the end; only About's text, Artists for Kids' history, was its own.

**Checked first:** store `ed35ee-ea.myshopify.com`; live theme `183162372393` "Colorblock: NEW WEBSITE", role MAIN. About's text matched `snapshots/pages-2026-09-25.json`. Before-snapshot: `snapshots/about-2026-09-26-before.json` (its hero image and card group; the print's empty alt text).

**Made through the Shopify connector** (payload from `about_us.py about-afk`; `about-afk-review` prints the text):

| What | Before | After |
| --- | --- | --- |
| About's `programme` | not set | Artists for Kids: its logo in the header, its colours (DS-04, DS-47) |
| About's `hero_image` | the building photo, as on About Us | the Bill Reid print from its text (`Reid_REID002_Xhuwaji_HaidaGrizzly.jpg`, `gid://shopify/MediaImage/40274179096873`, 3589 × 3629) |
| About's `hero_is_artwork` | not set | true: shown whole, never cropped |
| About's `hero_caption` | not set | "Bill Reid, (Canadian, 1920 – 1998) XHUWAJI/Haida Grizzly Bear", the page's own caption |
| About's `card_groups` | the three organisation cards | removed: they're on About Us. The cards and their group stay in the store, unused |
| About's staged text (`release_body`) | not set | its four paragraphs, word for word, without the print and caption the hero now carries |
| The print's alt text | empty | "Bill Reid, Xhuwaji / Haida Grizzly Bear, 1990" (artwork alt: artist, title, year) |

**At release** (`release.py addresses`): title "About Artists for Kids" and address `/pages/about-artists-for-kids`, with Shopify forwarding `/pages/about`. Until then the review theme still says "About" at `/pages/about`.

**Effect on the live site:** none. The live theme reads no page fields, and shows the print only inside page text, with its own empty `alt`. The live About page still shows its text and print (checked 2026-09-26).

**Undo:** set `hero_image` back to `gid://shopify/MediaImage/45637943591209` and `card_groups` back to `["gid://shopify/Metaobject/608389529897"]`; clear `programme`, `hero_is_artwork`, `hero_caption` and `release_body`; set the print's alt text back to empty.

## 2026-09-26: About merges into Artists for Kids (P-24, supersedes P-23)

**Why:** Michael, 2026-09-26: "Should /pages/artists-for-kids and /pages/about be merged? I prefer /pages/artists-for-kids." Two pages about the same organisation; the Artists for Kids page is the one in the menu, with the programmes and the website link.

**Checked first:** same store and live theme. The Artists for Kids page's text matched `snapshots/pages-2026-09-25.json` and it had no staged text. Before-snapshot: `snapshots/afk-merge-2026-09-26-before.json` (About's staged text from the entry above).

**Made through the Shopify connector** (payload from `about_us.py afk-merge`; `afk-merge-review` prints the text):

| What | Before | After |
| --- | --- | --- |
| Artists for Kids' staged text (`release_body`) | not set | its own two paragraphs and Paradise Valley photo, then About's four paragraphs under "History", with the Bill Reid print after the paragraph that names it. Words unchanged; both pictures are figures with their own captions |
| About's staged text | its four paragraphs (P-23) | removed: About is hidden at release |

About keeps the fields from the entry above (Artists for Kids programme, the print as its hero, no organisation rows) until release, when it is hidden and `/pages/about` forwards to `/pages/artists-for-kids` (`release.py addresses`). The print's alt text stays: the figure uses the same words.

**Effect on the live site:** none; the live theme doesn't read the staged field. The live Artists for Kids page shows its own text, without the print (checked 2026-09-26).

**For the gallery:** the Paradise Valley photo's description says 1994, its caption 1996 (`proposals/gallery-questions.md` §2).

**Undo:** clear Artists for Kids' staged text; set About's back from the snapshot.

## 2026-09-26: Our Story leaves the Shop; About forwards to About Us (P-25, P-24)

**Why:** Michael, 2026-09-26: "I think /pages/about should redirect to /about-us and remove Our Story under Shop." Our Story retold the Artists for Kids history that is now on the Artists for Kids page (P-24), with the same print and two of that page's paragraphs.

**Checked first:** the review menu `new-theme-main` is used only by the new theme (`theme/sections/header-group.json`); the live header uses `new-website-menu-1` (`baseline/theme/sections/header-group.json`). No page text links to `/pages/our-story`. Before-snapshot: `snapshots/menu-new-theme-main-2026-09-26-before.json` (the whole menu, with item IDs).

**Made through the Shopify connector:** `new-theme-main` (`gid://shopify/Menu/305860739369`) without "Our story" (item `gid://shopify/MenuItem/767490195753`) in its Shop section. The other 28 items keep their IDs, titles and order.

**At release** (`release.py addresses`, not before, because the live site shows them): Our Story and About are hidden; `/pages/our-story` forwards to `/pages/artists-for-kids`, where its history now is, and `/pages/about` to `/pages/about-us` (Michael's choice, replacing the forward to Artists for Kids). Shopify serves pages only under `/pages/`, so the target is `/pages/about-us`.

**Effect on the live site:** none. The live menu is untouched, and Our Story and About still load.

**Undo:** set the menu back from the snapshot (put "Our story" back between "2024 Fall Portfolio" and "Artists").

## 2026-09-26: Our Story's details join the Artists for Kids history (P-25)

**Why:** Michael, 2026-09-26: "Add that content you identified word for word." The three things from Our Story that the Artists for Kids page didn't have.

**Before-snapshot:** `snapshots/afk-our-story-2026-09-26-before.json` (the staged text from the entry before last).

**Made through the Shopify connector** (`about_us.py afk-merge`, now reading Our Story from `snapshots/pages-2026-09-25.json`): the Artists for Kids page's staged text, with, word for word:

- after "Artists for Kids was founded in 1989…": "Through art specialists, Artists for Kids provides enriching art-making experiences for thousands of students each year across Canada, as well as professional development opportunities for educators."
- after the paragraph on the first print: "This print by Bill Reid, based on a ceremonial drum, marked the beginning of an extraordinary partnership with now more than 100 Canadian artists - from Kenojuak Ashevak to Ian Wallace - that has produced one of the most significant limited edition collections in the country."
- the print's caption: "Bill Reid, (Canadian, 1920 – 1998) *XHUWAJI/Haida Grizzly Bear*, (1990) Serigraph, 22 in x 22 in." (the italics end before the comma now).

Also "contemporary limited editions" links to the Shop (`/pages/shop`), which Our Story sat under. Two phrases now come twice in a row; the words are the gallery's, so that's a question for them (`proposals/gallery-questions.md` 6.8).

**Effect on the live site:** none; the live theme doesn't read the staged field.

**Undo:** set the staged text back from the snapshot.

## 2026-09-26: Artists for Kids, a Programs heading and one repeat dropped (DS-51)

**Why:** Michael, 2026-09-26: "DS-51 approved, drop the repeated sentences and add a Programs heading."

**Before-snapshot:** `snapshots/afk-repeats-2026-09-26-before.json` (the group had no heading; the staged text from the entry above).

**Made through the Shopify connector** (`about_us.py afk-programs-heading` and `afk-merge`):

| What | Before | After |
| --- | --- | --- |
| Card group `afk-programmes` (`gid://shopify/Metaobject/608367378729`), `heading` | not set | "Programs": its card titles become H3s under it |
| Artists for Kids' staged text | with Our Story's sentence "This print by Bill Reid, based on a ceremonial drum, …" | without it: it repeated "marked the beginning of an extraordinary partnership" and "one of the most significant limited edition collections" from the paragraphs on either side. The ceremonial drum and the more than 100 artists go with it; `proposals/gallery-questions.md` 6.8 asks the gallery whether to mention them in its own words |

**Effect on the live site:** none; the live theme reads no card groups or staged text.

**Undo:** clear the group's heading; set the staged text back from the snapshot.

## 2026-09-26: The Smith Foundation's staged text (DS-52)

**Why:** Michael, 2026-09-26: "improve the design of the page while still adhering to the brand guidelines and design system."

**Checked first:** store `ed35ee-ea.myshopify.com`; live theme `183162372393` unchanged. The page's text matched `snapshots/pages-2026-09-25.json`, and it had no staged text (`snapshots/foundation-2026-09-26-before.json`).

**Made through the Shopify connector** (payload from `foundation.py staged`; `foundation.py review` prints the text): the page's staged text (`release_body`, `gid://shopify/Page/155705409833`).

- Its two paragraphs, word for word, without pasted styling.
- The line above them, "The Gordon and Marion Smith Foundation for Young Artists", in the Foundation's colour at 20 pt, is left out. The next sentence opens with the same words, and the header already carries the Foundation's logo.
- Explore + Create, Art In Good Company, Speaker Series and Music at The Smith link to their pages.
- "Gordon A. Smith and his late wife, Marion." still links to Gordon and Marion, now without opening a new tab.

**Effect on the live site:** none; the live theme doesn't read the staged field.

**Undo:** clear the page's staged text.

## 2026-09-26: "Get involved" over the Foundation's five ways to take part (DS-52)

**Why:** Michael, 2026-09-26: "DS-52 approved, add a Get involved heading."

**Before-snapshot:** `snapshots/foundation-take-part-2026-09-26-before.json` (no heading).

**Made through the Shopify connector** (`foundation.py heading`): card group `foundation-take-part` (`gid://shopify/Metaobject/608367444265`), `heading` set to "Get involved". Its card titles become H3s under it.

**Effect on the live site:** none; the live theme reads no card groups.

**Undo:** clear the group's heading.

## 2026-09-26: Donate and Gordon and Marion pass (DS-53)

**Why:** Michael, 2026-09-26: "using our design skills let's improve these pages."

**Checked first:** store `ed35ee-ea.myshopify.com`; live theme `183162372393` unchanged. Both pages' staged text matched what `migration.py` builds, and Donate had no call to action (`snapshots/donate-gm-2026-09-26-before.json`).

**Made through the Shopify connector** (payloads from `donate_gm.py`; `donate_gm.py review` prints both texts; each step checks the words are unchanged):

| Page | Field | Change |
| --- | --- | --- |
| Gordon and Marion | staged text | The biography, one paragraph split by line breaks, becomes paragraphs. The photo becomes a figure with the description "Gordon and Marion Smith looking at a print together" (it had none), so it sits beside the biography |
| Donate | staged text | "The impact of your gift" becomes a heading. Asha's words become a quote with her name under it, beside the list of what a gift does. Spacing typed as line breaks goes; the Explore + Create link stays in the same tab; a space inside a link moves out |
| Donate | `cta` | "Ways to give", to `/pages/donate#donate-ways-to-give`: the hero's button jumps to the Ways To Give cards |

**Effect on the live site:** none; the live theme reads neither field.

**Undo:** set both staged texts back to `migration.py`'s (`donate_body()`, and Gordon and Marion's text plus the video); clear Donate's `cta`.

## 2026-09-26: Gordon and Marion's video at its own shape (DS-53)

**Why:** Michael, 2026-09-26: "Let's improve this video embed, it looks bad." Vimeo gives the video as square (240 × 240 in its oEmbed data, 200 × 200 thumbnail), and the page boxed it at 16:9, so it played with bars down both sides under a heading pressed against it.

**Before-snapshot:** `snapshots/gm-video-2026-09-26-before.json`.

**Made through the Shopify connector** (`donate_gm.py gm-staged`): Gordon and Marion's staged text. The video is now a figure under the photo, beside the biography:
- It has width and height 640, which the theme turns into its shape.
- Its caption is its old heading, "Video: Gordon Smith's Magic", with the words unchanged.
- The player asks Vimeo for no title, byline or portrait overlay (`title=0&byline=0&portrait=0`), which would repeat the caption, and for the ink colour (`color=231f20`) instead of Vimeo's blue.

**Effect on the live site:** none; the live theme doesn't read the staged field.

**Undo:** set the staged text back from the snapshot.

## 2026-09-26: Volunteer pass (DS-58)

**Why:** the review of the Volunteer page found its two roles buried in paragraphs, its only action at the top, and no word on what to do with the form. Michael's go-ahead, 2026-09-26 ("Proceed").

**Checked first:** store `ed35ee-ea.myshopify.com` (Admin API `shop`), live theme `183162372393` "Colorblock: NEW WEBSITE", role MAIN. Before-snapshot: `snapshots/volunteer-2026-09-26-before.json` (the page's text, template, fields; no volunteer cards existed). The page's text still matches `snapshots/pages-2026-09-25.json`.

**Made through the Shopify connector** (payloads from `volunteer.py`; IDs in `created/volunteer-*.json`):

| What | ID |
| --- | --- |
| Card `volunteer-gallery-attendant`: title "Gallery Attendant", the role's sentence from the page | `gid://shopify/Metaobject/608724943145` |
| Card `volunteer-event-assistant`: title "Event Assistant", the role's sentence from the page | `gid://shopify/Metaobject/608724975913` |
| Card group `volunteer-roles`, no heading, the two cards | `gid://shopify/Metaobject/608725008681` |
| Page `volunteer` field `card_groups`: the group | `gid://shopify/Metafield/190408730411305` |
| Page `volunteer` staged text (`release_body`): the opening sentence; "Join the team" (new heading) with the photo `khimhipol221129_0389.jpg` from the page's old banner, alt "Guests are served drinks at a gallery event"; the two closing paragraphs; a new last line, "To apply, fill in the volunteer form (PDF). Questions? Contact us." | `gid://shopify/Metafield/190408730444073` |
| Page `volunteer` field `cta`: label "Volunteer Form" became "Download the form"; the address is unchanged | `gid://shopify/Metafield/190392604197161` |

`volunteer.py` checks that every word of the page's text is still there, in order. The only change to the gallery's words: each role's sentence starts the card, so its first letter is a capital ("greet" became "Greet", "support" became "Support"). The heading and last line are new, for the gallery to check (`gallery-questions.md` §3).

**Not written:** alt text on the hero photo. The live theme's slideshow reads each image's alt text from Files, so it would change the live page. The new theme treats a hero image without alt text as decorative instead (DS-58); descriptions can be added at release.

**Effect on the live site:** none. The live theme reads no page fields or cards, and its Volunteer page still shows its own text and "VOLUNTEER FORM" button.

**Undo:** set `cta` back to the snapshot's value; clear `card_groups` and `release_body` on the page; delete the card group, then the two cards.

## 2026-09-26: Donate pass (DS-60)

**Why:** the improvements made to Volunteer (DS-58), applied to Donate. Michael, 2026-09-26: "The improvements we made to /pages/volunteer we need to look at /pages/donate and also improve".

**Checked first:** store `ed35ee-ea.myshopify.com`, live theme `183162372393` role MAIN. Before-snapshot: `snapshots/donate-2026-09-26-before.json` (page fields, the four cards, the card group). The staged text in the store equals `donate_gm.py donate-staged` (DS-53), checked character for character.

**Made through the Shopify connector** (payloads from `donate.py`):

| What | ID | Before | After |
| --- | --- | --- | --- |
| Card `donate-email`, field `link` | `gid://shopify/Metaobject/608389398825` | empty | "Email us", `mailto:admin@smithfoundation.ca` |
| Card `donate-phone`, field `link` | `gid://shopify/Metaobject/608389464361` | empty | "Call us", `tel:+16049988563` |
| Card group `donate-ways-to-give`, heading and cards | `gid://shopify/Metaobject/608389562665` | "Ways To Give"; Online Form, Email, Mail, Phone | "How to give"; Email, Mail, Phone |
| Page `donate`, staged text (`release_body`) | `gid://shopify/Metafield/190392604393769` | DS-53's | The same, with `galleryschool-13.jpg` (a class visit) as a figure under "Ways to Support", alt "Students sit on the gallery floor with a guide during a class visit". Words unchanged (`donate.py` checks) |
| Page `donate`, call to action (`cta`) | `gid://shopify/Metafield/190406558417193` | "Ways to give" | "Make a gift", same address (`#donate-ways-to-give`) |

The cards' text is unchanged; the email address and number stay in it as the gallery wrote them. The Online Form card entry is unchanged and kept, out of the group, until there is a form (`gallery-questions.md` 7.3).

**Effect on the live site:** none. The live theme reads no page fields, cards or card groups; its Donate page still shows its own template.

**Undo:** set the group's heading and cards back to the snapshot's; clear the two card links; set the staged text back to `donate_gm.py donate-staged` and the call to action to the snapshot's value.

**Then, same day:** Michael, "we can improve the presentation of the The impact of your gift and Ways to Support text sections". Donate's staged text written again (`donate.py points`): the two lists get `class="gs-points"`, the example amounts' list `class="gs-amounts"`, and each amount ($75, $150, $500) is in bold. Words unchanged (`donate.py` checks). Undo: `donate.py staged` for the version before, or `donate_gm.py donate-staged` for the one before that.

## 2026-09-26: Plan your visit pass (DS-61)

**Why:** Michael, 2026-09-26: "Let's improve /pages/plan-your-visit using all our design skills - it looks really bad".

**Checked first:** store `ed35ee-ea.myshopify.com`, live theme `183162372393` role MAIN. Before-snapshot: `snapshots/plan-your-visit-2026-09-26-before.json`. The page's text still matches `snapshots/pages-2026-09-25.json`; it had no staged text.

**Made through the Shopify connector** (payload from `visit.py`):

| What | ID | Value |
| --- | --- | --- |
| Page `plan-your-visit`, staged text (`release_body`), new | `gid://shopify/Metafield/190408864235817` | "Getting Here" with `gordonsmithgallery-exterior-image.jpg` beside it (alt "The entrance at 2121 Lonsdale Avenue, with the gallery's sign above the doors"), Public Transport and Parking as points (`gs-points`), then Accessibility |

The first four sections (Address, Gallery Hours, Artists For Kids Office Hours, Admission) aren't in the staged text: the theme shows them from Theme settings, in the visit details at the top of the page (`snippets/gs-visit-info`). Address and hours were already there; admission and office hours are new settings (Git, `theme/config/settings_data.json`), holding the page's own words. `visit.py` checks each is in Theme settings word for word, and that the rest of the text is unchanged. The headings lose the bold and line break pasted into them.

**Effect on the live site:** none. The live theme reads neither the staged field nor the new settings.

**Undo:** clear the page's `release_body`; the page then shows its own text again, with the visit details above it.

## 2026-09-26 and 27: the Permanent Collection moves in (P-26, P-27, DS-62)

**Why:** Michael, 2026-09-26: "/pages/artists should not link out to the artist's website, it should link to their associated page", then "I agree with all of this implementation plan, please proceed with delivering the plan", "I think we can do all the artists and everything" and "We gave all the image rights". Plan: `proposals/permanent-collection.md`.

**Checked first:** store `ed35ee-ea.myshopify.com`; live theme `183162372393` role MAIN, review theme `184767250729` UNPUBLISHED (`shopify theme list`). Before-snapshots: `snapshots/collection-2026-09-27-before.json` (the Artists page's staged text, the Permanent Collection page's call to action, no collection entries or definitions) and `snapshots/menu-new-theme-main-2026-09-27-before.json`.

**How:** definitions, page and product fields and the review menu through the Shopify connector. Entries and Files through the Shopify CLI's store commands (`shopify store execute`), which Michael authorised for this import on 2026-09-27 with the scopes `read_metaobjects, write_metaobjects, read_files, write_files`: the connector can't upload files. Scripts in `collection/`, in order: `inventory.py`, `clean.py`, `definitions.py`, `images.py convert, upload, docs`, `import.py artists, works, link, groups, products`. Created IDs are in `created/collection-*.json`.

| What | IDs | Notes |
| --- | --- | --- |
| Definitions `artist` (12 fields, web pages at `/pages/artists/<handle>`), `artwork` (14 fields, `/pages/collection/<handle>`), `collection_group` (4 fields, `/pages/browse/<handle>`); all publishable, storefront read | `created/collection-definitions.json` | `definitions.py`. The artist's Works field was added after `artwork` existed, since the two refer to each other |
| Product field `custom.artist_entries` (Artist pages), pinned | `gid://shopify/MetafieldDefinition/272985850153` | |
| 1,417 images, JPEG 3,000 px on the long side, sRGB, quality 85, from the catalogue's masters (34 GB of TIFF and JPEG, downloaded one at a time and deleted after converting); alt text "Artist, Title, year" and the catalogue's visual description | `created/collection-files.json` (keyed by the catalogue's media ID) | 1.88 GB in all. 55 alt texts corrected the next hour (`images.py alts`) after the clean-up collapsed stray spaces and took cataloguer notes off. None failed processing |
| 180 documents for 51 artists (73 PDFs, 107 photographs and scans), 20 MB and under, named in their alt text ("Press", "Exhibitions, Photos") | `created/collection-files.json` (`doc-<media ID>`) | 39 PDFs over 20 MB aren't uploaded (Shopify's limit); listed in `collection/sheets/problems.csv` |
| 171 artist entries, active: name, sort name, full and other names, life dates, website (from today's Artists page), exhibitions, works, documents | `created/collection-artists.json` | 20 of them first through the connector, then all 171 through the CLI (the same entries, by handle) |
| 1,168 artwork entries, active, handle = accession number | `created/collection-works.json` | The 6 works on loan aren't imported. 16 link to their edition in the Shop |
| 26 collection groupings, active: 8 categories, 13 themes, 4 groupings (Indigenous artists, Artists for Kids Published Editions with the catalogue's history paragraph, Teaching Collection, the Portfolio Collective's 2021 series), and Featured works (6 works) | `created/collection-groups.json` | |
| 21 editions' Artist pages field | Products in `snapshots/prints-2026-09-25.json` | Kwikwi's names both artists |
| Page `artists`, staged text (`release_body`) | `gid://shopify/Metafield/190402028667177` | The two paragraphs only; the list of 59 links out gives way to the A to Z index (DS-62). Words unchanged |
| Page `permanent-collection`, call to action (`cta`) | `gid://shopify/Metafield/190392604131625` | "Browse" now opens the page's own search (`https://gordonsmithgallery.com/pages/permanent-collection#collection-search`; the theme makes it relative) instead of the catalogue. Link fields refuse a relative address |
| Review menu `new-theme-main` | `gid://shopify/Menu/305860739369` | A Collection section, second: The collection, Artists. Permanent collection leaves About and Artists leaves Shop (P-26) |

The cleaned data follows the gallery-questions defaults (§5) where the gallery hasn't answered: names as the site or catalogue has them, dates left off where they disagree or don't fit the works, the collection credit alone, no donors named, catalogue notes after "*" left off. The review sheets are in `collection/sheets/`.

**Effect on the live site:** none. The live theme has no templates for the three entry types, so `/pages/collection/<handle>` and `/pages/browse/<handle>` return 404 there (checked 2026-09-27). `/pages/artists/<anything>` shows the live Artists page, as it did before any entry existed (checked with a made-up handle): Shopify serves the page at any address under it, and none of an entry's content appears. The live theme reads neither page field, the product field nor the review menu (`baseline/theme/`).

**Undo:** clear the product field on the 21 editions; set the two page fields back from the snapshot; set the review menu back from its snapshot; delete the entries (Content, Metaobjects: groupings, then artworks, then artists) and the definitions; delete the uploaded files (`created/collection-files.json`). The catalogue is untouched throughout.

## 2026-09-27: the collection after Michael's review (P-28, DS-63)

**Why:** Michael, 2026-09-27: "display the items we have as text links in Documents below the artist's works. We can also remove the Website labels and links"; "Import The 6 works on loan"; "Exhibition pages: they don't list their works from the collection yet; that needs a new field on the exhibition entry." "Please do this."

**Checked first:** same store and themes as the entry above. Before: the exhibition and artist definitions as in `collection/definitions.py` at the previous commit; the entries as that import left them (`created/collection-*.json`).

| What | Through | Notes |
| --- | --- | --- |
| Exhibition definition: new field `collection_works` (Works from the collection, a list of artwork entries) | Connector | `definitions.py exhibition_works`. The live theme doesn't render exhibitions |
| Artist definition: Website renamed "Website (not shown)", Documents' description | Connector | `definitions.py artist_notes`. The values stay |
| The 6 works in "Things On Loan to AFK", with their 3 images; "On Loan" taken off two accession numbers (BOBA005, SMIT038) | CLI | `import.py works`. Credit lines as the catalogue records them (gallery question 5.13) |
| Every artist's Works and Documents lists | CLI | `import.py link`, now always sending both lists so an emptied one clears. Documents: one link per document, its PDF (or its photographs when it has no PDF); 79 in all. The cover images that went up with the first import aren't linked any more and can be deleted from Files |
| Documents' names (alt text): the catalogue item's title without the artist's name, numbered where one artist has two with the same name | CLI | `images.py docalts` |
| The groupings again, with the loans in their categories and themes | CLI | `import.py groups` |
| Works from the collection on *From the Ground* (26), *Playhouse* (25) and *The Art of Conversation* (18), from the works' sets and the catalogue's "Works in …" pages | CLI | `import.py exhibitions` |
| All works again after the edition rule accepted "AP, 11/14" (483 titles tidied), and their images' alt text | CLI | `import.py works`, `images.py alts` |

**Effect on the live site:** none. The live theme renders none of these entries or fields.

**Undo:** clear the three exhibitions' Works from the collection and delete that field; set the artist fields' names back; delete the 6 loan works and their images; run `import.py link` from the previous commit's `clean.py` for the old document lists.

## 2026-09-27: documents as tiles with their covers (DS-63, corrected)

**Why:** Michael, 2026-09-27, on the text links: "I don't see that updated Documents section on /pages/artists/gordon-smith and I didn't want them as a text list, I wanted the images displayed like the art works as the original catalogue site had them".

**Checked first:** same store and themes. Before: each artist's Documents field was a list of files (the entry above); those values are rebuilt by `import.py link` from `clean.py` at the previous commit.

| What | Through | IDs and notes |
| --- | --- | --- |
| 4 files the first upload missed (David Blackwood's three covers and one PDF: his documents found their owner after a clean-up fix) | CLI | `images.py docs`; `created/collection-files.json` |
| Definition `document` (title, cover, file; publishable, storefront read; no pages of its own) | Connector | `gid://shopify/MetaobjectDefinition/23783571753`; `definitions.py document` |
| 113 Document entries, active: one per catalogue document, its cover image and its file (the PDF, or the photograph itself). 34 have no file yet: their PDF is over 20 MB | CLI | `created/collection-documents.json`; `import.py documents` |
| Artist field `documents`: emptied on every artist (`import.py clear-documents`), the empty field deleted, and created again as a list of Document entries | CLI, then connector | The field changes type, which Shopify can't do in place. `definitions.py artist_documents` |
| Every artist's Documents list: their Document entries | CLI | `import.py link` |
| The documents' alt text: covers empty (the title is right under them), files their titles | CLI | `images.py docalts` |

**Effect on the live site:** none. The live theme renders none of these.

**Undo:** delete the Document entries and the `document` definition; recreate the artist's `documents` field as a list of files and run `import.py link` from the previous commit.

## 2026-09-27: the review menu's order (P-29)

**Why:** Michael, 2026-09-27: "the main navigation should be: Exhibitions, Collection, Programs, About, Artists for Kids, Smith Foundation, Shop".

**Checked first:** same store and themes. Before-snapshot: `snapshots/menu-new-theme-main-2026-09-27-before-order.json` (Exhibitions, Collection, About, Artists for Kids, Programs, Smith Foundation, Shop).

**Made through the Shopify connector:** `menuUpdate` on the review menu `new-theme-main` (`gid://shopify/Menu/305860739369`): the same items with the same IDs, in the new order. Nothing inside a section changed.

**Effect on the live site:** none. The live header uses `new-website-menu-1`, which is untouched.

**Undo:** `menuUpdate` with the snapshot's order.

## 2026-09-27: smaller copies of the 39 documents over 20 MB (DS-63)

**Why:** Michael, 2026-09-27: "Can you create the optimized versions of all the Documents too large for the site". Asked whether to upload and link them too: "Upload and link".

**Checked first:** store `ed35ee-ea.myshopify.com` (a shop query through the CLI); the live theme 183162372393 (live) and the review theme 184767250729 (unpublished), neither touched by these writes. Before-snapshot: `snapshots/collection-documents-2026-09-27-before.json` (113 Document entries, 34 without a file, and every artist's Documents list). The regenerated data was compared with what was imported: only the 34 entries' file, 5 new entries and 4 artists' Documents lists differ.

| What | Through | IDs and notes |
| --- | --- | --- |
| 39 PDFs: smaller copies of the catalogue's originals (1.9 GB to 378 MB, each under 19 MB; 34 at 200 dpi, 3 at 150, one each at 130 and 120), named in their alt text | CLI | `images.py shrink`, then `images.py docs`. How each was made: `collection/shrunk-documents.json`; file IDs: `created/collection-files.json` |
| 34 Document entries: their file | CLI | `import.py documents` (upserts all 118; the other 79 are unchanged) |
| 5 new Document entries, active, with a file and no cover: Robert Bateman's Biography and Press, Books, Exhibitions; Nuveeya Ipellie's Document; Melia Padluq's Works; Kabubuwa Tunnillie's Works | CLI | `created/collection-documents.json` |
| 4 artists' Documents lists: those new entries | CLI | `import.py link` (rewrites every artist's lists from the data; the other 167 are unchanged, checked against the snapshot) |
| The new files' alt text: their titles | CLI | `images.py docalts` |

**Checked after:** 118 Document entries, none without a file; no title or cover changed; only those 4 artists' lists differ from the snapshot. On the development theme, Gordon Smith's, Jack Shadbolt's and Robert Bateman's documents open their PDFs, and the largest (18.2 MB) is served as a PDF.

**Effect on the live site:** none. The live theme renders none of these.

**Undo:** empty the 34 entries' file field, delete the 5 new entries, run `import.py link` from the previous commit, and delete the 39 files (their IDs are in `created/collection-files.json`, under the media IDs in `shrunk-documents.json`).

## 2026-09-27: Artists for Kids moves onto the site (P-30 to P-40)

**Why:** Michael, 2026-09-27: the Artists for Kids site (artistsforkids.sd44.ca) becomes part of gordonsmithgallery.com, all but registration; "Decisions for Michael: all recommendations are approved ... let's get started on implementation". Plan: `proposals/artists-for-kids-integration.md`.

**Checked first:** store `ed35ee-ea.myshopify.com` (Artists for Kids & The Gordon Smith Gallery, through the connector and the CLI); the live theme 183162372393 "Colorblock: NEW WEBSITE" (live) and the review theme 184767250729 (unpublished), neither touched. Before-snapshot: `snapshots/afk-2026-09-27-before.json` (the programme, Public programs and Donate cards, every card group, the curatorial tour event, and the Artists for Kids page's card groups, button and full staged text). No page, entry or file with these handles existed.

**Read-only first:** the old site in full (`artists-for-kids/inventory.py`, 48 pages); each video's owner, upload date and thumbnail from YouTube (`lessons.py youtube`: all 27 belong to the gallery's channel, "Artists for Kids & The Gordon Smith Gallery"); the collection's artwork titles, to match the works each lesson names.

| What | Through | IDs and notes |
| --- | --- | --- |
| Definition `lesson` (9 fields, publishable, pages at `/pages/lessons/<handle>`, storefront read; content model part 8) | Connector | `gid://shopify/MetaobjectDefinition/23785144617`. The CLI's app may not create store-owned types |
| Event field `keep_off_home` (P-37) | Connector | on `gid://shopify/MetaobjectDefinition/23753392425` |
| 44 pictures and 27 lesson covers, each with alt text; 21 PDFs (5 of them smaller copies under 19 MB, `artists-for-kids/shrunk-pdfs.json`, P-40) | CLI | `created/afk-files.json`. The first upload enlarged the smaller pictures to 3,000 px; each was replaced in place with a copy at its own size (`files.py replace`, fileUpdate, same IDs) |
| Test page `after-school-art`, published, title only, `seo.hidden` = 1 | Connector | `gid://shopify/Page/165837373737`. Made with the programme template name first: the live theme fell back to its default page template, which carries About's content, so the address showed About's text under "After School Art". Changed to the live theme's On Now template name (`current-on-now-exhibition`), which shows the title only; checked on gordonsmithgallery.com (title only, `noindex,nofollow`, not in the sitemap or search) |
| 17 more pages, the same way | Connector | `created/afk-pages.json` |
| 46 cards (40 new; the 6 programme cards' links and nothing else changed, to the site's pages; the 8 residency cards renamed after the first look) | CLI | `created/afk-cards.json` |
| 15 card groups, and one card added to `public-programs` and to `donate-ways-to-give` | CLI | `created/afk-card-groups.json`, `afk-card-groups-extended.json` |
| 27 lessons, active: title, video, posted (the YouTube upload date), cover, the old page's four parts, and the works they name from the collection (22 lessons) | CLI | `created/afk-lessons.json` |
| 6 events, active, Keep off the home page: the educators' workshops with a date; the curatorial tour (existing) gains Professional development as its page | CLI | `created/afk-events.json` |
| Page fields on the 18 pages: programme, hero image and caption, eyebrow, button, card groups, staged text (`custom.release_body`) | Connector | 56 values in three `metafieldsSet` calls; two staged texts set again after the first look ("(PDF)" on PDF links) |
| The Artists for Kids page: card groups (was `afk-programmes`), button (the 2026-2027 program guide, was the Artists For Kids Website), staged text (two history paragraphs, the team, the annual report) | Connector | Its previous values are in the before-snapshot |
| The review menu `new-theme-main`: Artists for Kids becomes a section of five items (P-33) | Connector | `created/afk-menu-input.json`; the other items keep their IDs |

Text is the old site's, moved as written; what changed and why is in `artists-for-kids/content.py`'s docstring. Kept, for the gallery: `proposals/gallery-questions.md` §6.

**Checked after:** on the development theme at 1440, 768 and 390: every new page, a lesson, the home page (no workshops in What's on; the tour named by its exhibition), Donate and Public programs; no sideways scrolling, one H1 each, the Artists for Kids colours and logo, no empty links. On gordonsmithgallery.com: the new pages show their title only, with `noindex,nofollow`, and aren't in the sitemap; `/pages/lessons/paper-fruit` is 404; the Artists for Kids page is unchanged.

**Effect on the live site:** 18 new addresses that show a page title and nothing else, hidden from search engines, the sitemap and the store's search, linked from nowhere on the live site (P-35). Nothing else the live theme renders changed.

**Undo:** hide or delete the 18 pages; set the Artists for Kids page's card groups, button and staged text back from the snapshot; restore the six programme cards' links and the two extended groups' card lists from the snapshot; delete the 40 new cards, 15 groups, 27 lessons and 6 events, and clear the tour's programme page; `menuUpdate` the review menu with Artists for Kids as a plain link; delete the files in `created/afk-files.json`; delete the `keep_off_home` field and the `lesson` definition.

## 2026-09-27: Artists for Kids after the design review (DS-73 to DS-83)

**Why:** Michael, 2026-09-27: "Spawn an agent per new page to review the design ... to ensure each page is as great as it can be while sticking to our design system." The review's content changes (`artists-for-kids/content.py` docstring, "After the design review"); the theme changes and Proposed rules are in `design-system/DESIGN.md` 0.6.28.

**Checked first:** store `ed35ee-ea.myshopify.com`; the live theme 183162372393 and the review theme 184767250729, neither touched. Before-snapshot: everything this round writes was made earlier the same day, from `content.py` and `files.py` at commit `aea9961`, whose values are the before-state; the Artists for Kids page's own previous values are in `snapshots/afk-2026-09-27-before.json`. No file, card or group the live theme shows was changed.

| What | Through | IDs and notes |
| --- | --- | --- |
| 10 pictures replaced in place (the program guide's and Mini Monster's covers rendered from their PDFs, the Paradise Valley collage without its white border, the black bars cut from seven lesson covers); the 27 lesson covers' alt text cleared, since each cover's title follows it | CLI (`files.py revise`) | Same IDs, `created/afk-files.json` |
| 6 new cards (Explore + Create Saturdays for families; Awards and scholarships and Support Artists for Kids as text cards; the three ways to give) and text on the community programme cards; 4 new groups (`afk-more-classes-and-camps`, `afk-awards-and-support`, `afk-air-sara-jeanne-bourget-guides`, `afk-how-to-give`); `afk-also-for-families` holds the new Explore + Create card | CLI (`load.py cards`) | `created/afk-cards.json`, `afk-card-groups.json`; 52 cards and 19 groups upserted by handle, the two extended groups unchanged |
| The 6 educators' workshops: typographic quotes in two titles, "**" markers dropped | CLI (`load.py events`) | `created/afk-events.json` |
| Page fields on the 18 pages and the Artists for Kids page: intros (Studio Art Academy, Paradise Valley, Awards), buttons ("Register for classes", "Register for camps", "Register for camp"), card groups (Day camps, Sara-Jeanne Bourget, Support, Artists for Kids), staged text (phone links, lists, standalone links, figures moved, the team's names as the photo's caption) | Connector | 62 values in three `metafieldsSet` calls |

Support Artists for Kids now goes to the standard page template at release (`release.py`, `AFK_STANDARD`), so its ways to give follow all its text, as on Donate.

**Checked after:** the 20 pages on the development theme at 1440, 768 and 390; Paradise Valley, the home page, Donate, The Smith Foundation, Plan your visit, Volunteer, Gordon and Marion and an exhibition page at the same widths.

**Effect on the live site:** none. The 18 pages still show their title only; the Artists for Kids page's staged text and fields aren't read by the live theme.

**Undo:** rebuild the earlier copies from the old site with `files.py prepare` and put them back with `files.py replace` (same IDs), and set the covers' alt text from `cover_alt` at `aea9961`; delete the 6 new cards and 4 new groups; run `load.py cards`, `load.py events` and the page-field batches from `content.py` at `aea9961`.

## 2026-09-27: whole-site design review (proposals/site-design-review.md)

**Why:** Michael, 2026-09-27: "Do the same using all of our design skills ... on every page of our new version of the site ... we want the design to be as good and consistent as possible". The review's content changes of our own words and markup only; the gallery's words are unchanged, and changes that need the gallery's words or would show on the live site wait (the review record lists them).

**Checked first:** store `ed35ee-ea.myshopify.com`; the live theme 183162372393 and the review theme 184767250729, neither touched. Before-snapshot: `snapshots/site-review-2026-09-27-before.json` (the three giving cards, Stitched's credits, the review menu, the two buttons; staged texts as the generators' output at the commits it names; FAQ and Contact had none).

| What | Through | IDs and notes |
| --- | --- | --- |
| Staged text: Donate's camp links go to the camps' pages here; FAQ and Contact get staged text (line-break paragraphs made paragraphs; Contact's phone and emails as links); Awards' three requirement links are standalone links (DS-82); Support's NVSD point is two paragraphs | Connector | `site_review.py pages`, `artists-for-kids/content.py` page-fields; one `metafieldsSet` of 7 values with the two buttons below |
| Buttons: Support Artists for Kids "Make a gift", to its How to give cards (as Donate); the Artists for Kids page "Download the guide" (was "2026-2027 Program Guide") | Connector | Same call |
| The three giving cards: "Online" (Through CanadaHelps. / Give online), "School Cash Online" (With an NVSD School Cash Online account. / Give with School Cash), "Phone" ((604) 903-3798 / Call us), as Donate's | Connector | `metaobjectUpdate` on 609010778409, 609010811177, 609010843945; `content.py` updated to match |
| Stitched's credits: Artists For Kids and the Foundation link to their pages here; the Foundation's link was broken | Connector | `metaobjectUpdate` on 608388448553 (`site_review.py stitched`) |
| The review menu `new-theme-main`: "Upcoming events" under Programs, after Public programs (label for the gallery to confirm) | Connector | `menuUpdate` (`site_review.py menu`); the other items keep their IDs |

**Checked after:** on the development theme at 1440: Support's button and cards, the hub's button "Download the guide (PDF)", Awards' three links, Donate's camp links, Contact's links, Stitched's two links, Upcoming events marked in the menu. On gordonsmithgallery.com: Contact and FAQ unchanged.

**Effect on the live site:** none. Staged text, buttons, cards, exhibition entries and the review menu aren't read by the live theme.

**Undo:** set the values in the before-snapshot back (staged text: the generators at the commits named there; FAQ and Contact: delete `custom.release_body`); `menuUpdate` the review menu without the Upcoming events item.

## 2026-09-28: DS-122 and DS-129, decided by Michael

**Why:** Michael, 2026-09-28: "DS-97 to DS-130 all look like great improvements, proceed with implementation". Two of them need store content: DS-122 (the Permanent Collection's Browse button lands on "Browse the collection") and DS-129 (Learning kits shows each kit, then its lesson plans, then its video).

**Checked first:** store `ed35ee-ea.myshopify.com`; the live theme 183162372393 and the review theme 184767250729, neither touched. Before-snapshot: `snapshots/site-review-decided-2026-09-28-before.json`.

| What | Through | IDs and notes |
| --- | --- | --- |
| Six new card groups: one for each kit (no heading) and one for each kit's video ("Clay Lesson Video", "Trace Monotype Lesson Video", headings for the gallery to confirm) | CLI | `artists-for-kids/load.py cards` (upserts by handle; the other cards and groups were written with the values they already had); IDs in `created/afk-card-groups.json`. The old `afk-kits` and `afk-kit-videos` groups stay in the store, on no page |
| Learning kits' card groups in the new order: each kit, its plans, its video | Connector | `metafieldsSet` on gid://shopify/Page/165838127401 (`content.py` page-fields, that row only) |
| The Permanent Collection's button: "Browse" now goes to `#collection-browse` (was `#collection-search`) | Connector | Same call, gid://shopify/Page/155720548649 `custom.cta` |

**Checked after:** Learning kits at 390 and 1440 on the development theme (kit, plans, video, for each of the four kits).

**Effect on the live site:** none. Card groups and these page fields aren't read by the live theme.

**Effect on the review theme:** its Browse button jumps nowhere until it has the new section id (`theme/sections/gs-collection-ways.liquid`, `id="collection-browse"`); push `main` to it after this branch merges.

**Undo:** set both page fields back from the snapshot; the six new groups can stay or be deleted.

## 2026-09-28: the menu by what visitors come to do (P-50 to P-57)

**Why:** Michael, 2026-09-28: "Proceed with implementing this new navigation and IA" (`proposals/navigation-review.md`).

**Checked first:** store `ed35ee-ea.myshopify.com` (connector: gordonsmithgallery.com); the live theme 183162372393 reads `new-website-menu-1` in its header and no page fields or entries (`baseline/theme/`, and the live pages fetched 2026-09-28). No menu with the handles `new-theme-main-2` or `new-theme-explore-2`; the artist definition had no `about_page` field. Before-snapshot: `snapshots/navigation-2026-09-28-before.json`.

| What | Through | IDs and notes |
| --- | --- | --- |
| New menu `new-theme-main-2`, "Main menu (new theme, 2026-09-28)": Exhibitions, Collection, Programs (with its three groups), Support, About, Shop | Connector | `menuCreate`, `gid://shopify/Menu/305944068393`; input `created/navigation-menus-input.json` from `navigation.py`. The group title "Scholarships and awards" links to "#" |
| New menu `new-theme-explore-2`, "Footer: Explore (new theme, 2026-09-28)" | Connector | `menuCreate`, `gid://shopify/Menu/305944330537` |
| Artist definition: new field About page (`about_page`, page reference) | Connector | `metaobjectDefinitionUpdate` on `gid://shopify/MetaobjectDefinition/23770661161` |
| Gordon Smith's artist entry: About page is Gordon and Marion | Connector | `metaobjectUpdate` on `gid://shopify/Metaobject/608899105065` |
| Donate and Gordon and Marion: eyebrow "The Smith Foundation" (links back, DS-80); Gordon and Marion's button "See Gordon Smith's works" to `/pages/artists/gordon-smith` | Connector | `metafieldsSet` on `gid://shopify/Page/155885863209` and `gid://shopify/Page/155692957993` (`custom.eyebrow`, `custom.cta`). The link field needs a full address; `gs-url` makes it relative |

Not changed: the review menus `new-theme-main` and `new-theme-explore`, which the review theme reads until this merges. The three Foundation pages planned in `proposals/smith-foundation-site.md` aren't made here; they join the new menu when they are (`navigation.py`, `LATER`), and the Foundation page's gala and scholarship cards get their links then.

**Checked after:** on the development theme 184755814697 (`theme dev` on port 9393, this branch): the bar at 1200 with each programme's logo and at 1280, 1366 and 1440, the drawer at 768 and 375, keyboard, and 33 pages each marking one section or none; the crumb "The Smith Foundation" on Donate and Gordon and Marion; "See Gordon Smith's works" on Gordon and Marion; "About Gordon Smith" on his artist page, and nothing on an artist without an About page. On gordonsmithgallery.com: the home page, Donate, Gordon and Marion and `/pages/artists/gordon-smith` unchanged (live theme, old header menu, no crumb or button).

**Effect on the live site:** none. The live theme doesn't read these menus, page fields or entries.

**Effect on the review theme:** none until this branch merges and `main` is pushed to it; then its header and footer read the new menus.

**Undo:** point `sections/header-group.json` and `footer-group.json` back at `new-theme-main` and `new-theme-explore`, then delete the two new menus; clear `custom.eyebrow` on the two pages and `custom.cta` on Gordon and Marion (neither had a value before); clear Gordon Smith's About page and delete the `about_page` field from the artist definition.

## 2026-09-28: the Smith Foundation's old website (P-41 to P-49, DS-138)

**Why:** Michael, 2026-09-28: "Yes to everything except integrating the older Year in Review content - the desire is to only show the most recent one for simplicity", then "Proceed with implementation". Plan: `proposals/smith-foundation-site.md`. Sources outside Git: the WordPress export of smithfoundation.co and its media library, downloaded the same day (the plan's "Sources").

**Checked first:** store `ed35ee-ea.myshopify.com` (through the connector and the CLI); the live theme 183162372393 "Colorblock: NEW WEBSITE" (live), the review theme 184767250729 (unpublished) and the development theme 184755814697, none touched (`shopify theme list`). Before-snapshots: `snapshots/foundation-2026-09-28-before.json` (all 15 exhibitions, the Foundation's five cards and their group, read through the CLI) and `snapshots/foundation-pages-2026-09-28-before.json` (the staged text of Gordon and Marion and of Awards and scholarships, read through the connector and checked paragraph by paragraph against their rendered pages). Speaker Series and Music at the Smith had no staged text, and their page text is unchanged since `snapshots/pages-2026-09-25.json`. No page, entry or file with these handles existed.

| What | Through | IDs and notes |
| --- | --- | --- |
| Exhibition field Videos and publications (`media`, list of links; DS-138) | Connector | `metaobjectDefinitionUpdate` on `gid://shopify/MetaobjectDefinition/23753359657`. The CLI can't see this definition |
| 52 photos, 5 logos (3 of them PNG) and 3 PDFs, each photo with alt text written from looking at it (`foundation/alt.json`; the logos named); the *Unfixed* book in a smaller copy (20.2 to 8.0 MB, P-40) | CLI | `created/foundation-files.json`, from `foundation/files.py` |
| 17 exhibitions, active, 2013 to 2019 (P-41): title, dates, curator, artists, summary and text, key image, caption, views | CLI | `created/foundation-exhibitions.json`, from `foundation/load.py exhibitions`. Three key images are works from the collection (Alistair Bell, Yung Wing Chow, Robert Young), and Dwelling's is Christopher Pratt's print from the collection, also listed as its work from the collection |
| 9 exhibitions gain fields (P-45, P-46): Play, Unfixed, Beyond the Horizon, We Can Only Hint at This with Words, Paths, Endless Summer (text, curators, artists, credits, logos, views); Prevailing Landscapes, Playhouse, Stitched (past programmes after their text, credits, videos) | CLI | Upserts by handle; their previous fields are in the before-snapshot |
| Cards: `foundation-scholarships` and `foundation-brilliance-gala` get links to their pages; new card `foundation-supporters`; the group `foundation-take-part` gains it, last | CLI | `created/foundation-cards.json`, from `load.py cards`; the card links' previous value was empty |
| 3 pages, published, title only, `seo.hidden` = 1, the live theme's On Now template name (P-35, P-42): Scholarships, Brilliance Gala, Supporters | Connector | `pageCreate`; `created/foundation-pages.json` |
| Their fields: programme Smith Foundation, eyebrow "The Smith Foundation" (DS-80), hero (Scholarships, Brilliance Gala), intro (Supporters), staged text | Connector | `metafieldsSet`, from `content.py page-fields` (`created/foundation-page-fields-input.json`). Brilliance Gala's text set three times: after a first look at 1440 its photos went from four or five a gala to two at most, and the 2018 and 2013 luncheons (photos only) came off |
| Staged text additions (P-44, P-57): Speaker Series (Past talks), Music at the Smith (Past concerts, the Steinway), Gordon and Marion (the obituary line, a second video), Awards and scholarships (one line linking the Foundation's scholarships) | Connector | `metafieldsSet`; each is the page's text as it was plus the addition |
| The new theme's menu `new-theme-main-2`: Smith Foundation scholarships first under Programs, Scholarships and awards; Brilliance Gala after Give to Artists for Kids and Supporters last under Support (P-52, P-53) | Connector | `menuUpdate` on `gid://shopify/Menu/305944068393`; every other item keeps its ID; `navigation.py` updated to match |

Not changed, by decision: the older Year in Review reports (P-47, only the newest shows); the Donate page's "donor page" link, which waits with the Supporters page for the gallery's word on the list (8.1); facts that may be out of date (P-49, questions 1.1, 1.4, 7.3, 8.3 and 8.4). Uploaded and unused: the photos taken off the gala page (three of 2026, four of 2025, four of 2023, and the 2018 and 2013 luncheons'), kept in Files for the gallery to swap in.

**Checked after:** on the review theme (it follows `main`, so it shows the content but not the Videos and publications section, which is on this branch): Past exhibitions lists 29, back to 2013; an older exhibition's page (summary, facts, text, views, credit); the three new pages; every staged paragraph and heading of the seven pages found on its rendered page (the three with off-site links differ only by the hidden "(external site)"); the Foundation page's cards link to the three pages; the menu has them. The section itself in `preview.html` at 1440 and 390. The development theme was in use by another session, so the section waits for the review theme after merge.

**Effect on the live site:** three new addresses that show a page title and nothing else, `noindex`, not in the sitemap, linked from nowhere (P-35). The exhibition entries' addresses are 404 and the live Past Exhibitions page is unchanged; no staged text, card or menu change shows.

**Undo:** `foundation/load.py restore` (the nine exhibitions' fields and the two cards' links back from the snapshot, the group's cards back, the 17 new exhibitions and the Supporters card deleted); set the four pages' staged text back from the snapshots (Speaker Series and Music at the Smith: delete `custom.release_body`); hide or delete the three pages; `menuUpdate` the menu without the three items; delete the files in `created/foundation-files.json`; delete the `media` field from the exhibition definition.

## 2026-09-28: Richard Savage leaves the Board of Directors

**Why:** Michael, 2026-09-28: "Remove Richard Savage from Board of Directors on https://gordonsmithgallery.com/pages/the-smith-foundation".

**Checked first:** store `ed35ee-ea.myshopify.com`; the live theme 183162372393 (live) and the review theme 184767250729 (unpublished), rechecked at the review theme push earlier the same hour. Before-snapshot: `snapshots/foundation-board-2026-09-28-before.json` (the group `foundation-board` and his card, read through the CLI).

| What | Through | IDs and notes |
| --- | --- | --- |
| Card group `foundation-board` ("Board of Directors"): `board-richard-savage` out of its cards; 13 left, in the same order | CLI | `metaobjectUpsert` on `gid://shopify/Metaobject/608367477033` |

His card (`gid://shopify/Metaobject/608367083817`: name, "Director", portrait) stays in the store in no group, so this can be undone; it can be deleted once no one needs it back. `programmes.py` no longer lists him, so a re-run can't bring him back. His name elsewhere is unchanged: the Brilliance Gala 2026 committee and the Supporters list, both as the old site had them.

**Checked after:** the review theme's Smith Foundation page lists 13 board members, Allison Kerr then Ed Tsumura.

**Effect on the live site:** none from this write: the live theme doesn't read card groups. The live page's board is in the live theme's own template (`templates/page.the-smith-foundation.json` in Colorblock, as `baseline/theme/` has it), and the live theme is never written to from here (AGENTS.md). It keeps showing him until release, unless someone removes his block in the live theme's editor.

**Undo:** put `gid://shopify/Metaobject/608367083817` back in the group's cards, ninth, from the snapshot.

## 2026-09-28: the Programs switcher's menu and page (DS-143, DS-147)

**Why:** Michael, 2026-09-28: "Go ahead with the three store changes". The row of links above the events list needs the four public programmes in a fixed order, the Past events page, and Programs leading to the full list (pull request 69).

**Checked first:** store `ed35ee-ea.myshopify.com` (Artists for Kids & The Gordon Smith Gallery); the live theme 183162372393 (live) and the review theme 184767250729 (unpublished), by `shopify theme list`. Before-snapshot: `snapshots/programmes-switcher-2026-09-28-before.json` (both menus whole, with item IDs; no menu `new-theme-programmes` and no page `past-events` existed). The live theme reads `new-website-menu-1` and `footer`, neither of which changed.

| What | Through | IDs and notes |
| --- | --- | --- |
| New menu `new-theme-programmes`, "Programs filter (new theme)": Speaker series, Music at the Smith, Explore + Create, Art in Good Company | Connector, `menuCreate` | `gid://shopify/Menu/305948229929` |
| New page Past events, `/pages/past-events`, no text, `seo.hidden` = 1 | Connector, `pageCreate` | `gid://shopify/Page/165857689897` |
| `new-theme-main-2`: the Programs section's own link points at Upcoming events in place of Public programs | Connector, `menuUpdate` | Item `gid://shopify/MenuItem/767723176233`; the other 31 items keep their IDs, titles and order |
| `new-theme-explore-2`: Programs points at Upcoming events in place of Public programs | Connector, `menuUpdate` | Item `gid://shopify/MenuItem/767723962665`; the other 7 items unchanged |

`release.py` lists `past-events` among the new pages, so it loses `seo.hidden` at release with the others.

**Checked after:** on the development theme 184804704553, the row reads All upcoming, Speaker Series, Music At The Smith, Explore + Create, Art In Good Company, Professional Development, Past events; Past events lists the one ended event; the footer's Programs link goes to Upcoming events.

**Effect on the live site:** one new address. `/pages/past-events` shows the page's title with nothing under it, marked `noindex,nofollow`; no live page links to it (the home page and Upcoming events checked). The live menus are untouched. On the review theme the footer's Programs link now goes to Upcoming events, which has no row of links there until pull request 69 merges and the review theme is pushed.

**Undo:** delete the menu `new-theme-programmes` and the page Past events; set the two Programs items back to `gid://shopify/Page/155718943017` from the snapshot.

## 2026-09-28: the Current events page (DS-149)

**Why:** Michael, 2026-09-28: "Go ahead with the Current events page". The main row of the Programming lists is Current, Upcoming and Past, each a page.

**Checked first:** store `ed35ee-ea.myshopify.com`; the live theme 183162372393 (live) and the review theme 184767250729 (unpublished), by `shopify theme list`. Before: no page with the handle `current-events` existed.

| What | Through | IDs and notes |
| --- | --- | --- |
| New page Current events, `/pages/current-events`, no text, `seo.hidden` = 1 | Connector, `pageCreate` | `gid://shopify/Page/165858115881` |

`release.py` lists `current-events` among the new pages, so it loses `seo.hidden` at release with the others.

**Checked after:** on the development theme 184804704553 the main row reads Current, Upcoming, Past, and the Current page says nothing is on today.

**Effect on the live site:** one new address. `/pages/current-events` shows the page's title with nothing under it, marked `noindex,nofollow`; no live page links to it. Nothing else changed.

**Undo:** delete the page Current events.

## 2026-09-28: Gordon and Marion's pull quote (DS-145)

**Why:** Michael, 2026-09-28: "Yes, add the Effervescent pull quote", for the story layout (DS-145, PR #71).

**Checked first:** store `ed35ee-ea.myshopify.com`; the live theme 183162372393 (live) and the review theme 184767250729 (unpublished), rechecked at the review theme push earlier the same hour. The live theme doesn't read `custom.release_body` (none of `baseline/theme/` does), so this is a field value the live theme doesn't read ("Store writes before release"). Before-snapshot: `snapshots/gordon-and-marion-2026-09-28-before.json` (the field's value, last changed 21:15 UTC, unchanged when read again just before the write).

| What | Through | IDs and notes |
| --- | --- | --- |
| Gordon and Marion's staged text (`custom.release_body`, DS-39): the paragraph "Effervescent, wildly creative, endlessly youthful, energetic and hard-working. An infectious, …" wrapped as a quote, `<figure class="gs-quote"><blockquote>…</blockquote></figure>`, where it was. Every word, and everything else in the text, unchanged | Shopify connector (`metafieldsSet`) | `gid://shopify/Metafield/190392604426537` on `gid://shopify/Page/155692957993`, updated 22:39:46 UTC |

**Checked after:** read back through the connector, the value is exactly the one intended, and its words match the snapshot's with the tags taken out. On the review theme the story shows it as a pull quote, offset left between the portrait (right) and the Magic video (right), with no Liquid error; the obituary paragraph and History video then flip, the video on the left.

**Effect on the live site:** none. gordonsmithgallery.com/pages/gordon-and-marion returns 200 with the same text and no quote; the live theme shows the page's own text, which this didn't touch. At release the staged text replaces it (store-changes §8), quote and all.

**Undo:** set `custom.release_body` on `gid://shopify/Page/155692957993` back to the snapshot's value (`metafieldsSet`, type `multi_line_text_field`).

## 2026-09-28: store settings review, fixes 1 to 4 (`proposals/store-settings-review.md`)

**Why:** Michael, 2026-09-28: "Apply fixes 1 to 4". Four prints couldn't be bought with shipping on the live site: two sat in a shipping profile with no rates, and two were set as not needing shipping.

**Checked first:** store `ed35ee-ea.myshopify.com` (through the connector); the live theme 183162372393 "Colorblock: NEW WEBSITE" (MAIN), not touched. Before-snapshot: `snapshots/store-settings-2026-09-28-before.json` (the two shipping profiles and their products, the two variants' shipping setting, and the checkout settings as read in the admin).

| What | Through | IDs and notes |
| --- | --- | --- |
| Anna Binta Diallo, *Red Feather* and Sandeep Johal, *I am easy to find* move from the profile "2024 Fall Portfolio (Unframed Prints)" to the general profile | Connector | `deliveryProfileUpdate` on `gid://shopify/DeliveryProfile/120468111657`, `variantsToDissociate`: `gid://shopify/ProductVariant/49338095501609`, `gid://shopify/ProductVariant/49338153271593` |
| Anna Binta Diallo, *Prairie Girl* and Elizabeth McIntosh, *Diamonds* are physical products (`requiresShipping` true) | Connector | `productVariantsBulkUpdate` on `gid://shopify/ProductVariant/53226473390377` and `gid://shopify/ProductVariant/52900916986153` |

The custom profile stays in the store, empty (no products, zones or rates), so nothing was deleted. It can be deleted in the admin once no one needs it.

**Fixes 3 and 4, made by Michael in the admin (Settings, Checkout), 2026-09-28:** Address line 2 from Required to Optional; "Preselect checkbox in certain regions" from All regions to Automated, which preselects in the United States only. The Admin API has no checkout settings, so these were made by hand. Their values before are in the snapshot.

**Checked after:** read back through the connector: all four variants are in the general profile and need shipping; the general profile holds 40 variants, the custom one none. Fixes 3 and 4 read back on the admin's Checkout page after Michael saved them: Address line 2 "Optional"; preselection "Automated, United States".

**Effect on the live site:** checkout now offers "Shipping within Canada" ($20) and pickup for all four prints. *Prairie Girl* and *Diamonds* now ask for a shipping address. The apartment field can be left empty, and the marketing checkbox starts unticked for buyers in Canada, the only market that can check out.

**Undo:** `deliveryProfileUpdate` on the custom profile with `variantsToAssociate` and the two variant IDs; `productVariantsBulkUpdate` with `requiresShipping: false` on the other two. Fixes 3 and 4: set both back in Settings, Checkout, from the snapshot.

## 2026-09-28: the US and International shipping zones deleted (`proposals/store-settings-review.md`, item 7)

**Why:** Michael, 2026-09-28: "delete the unused US and International shipping zones". Canada is the only market, so neither zone could be reached at checkout. The US zone carried what look like Shopify's starter rates, with free shipping on orders of $100 or more, which would have applied to every print if anyone added a market.

**Checked first:** store `ed35ee-ea.myshopify.com` (through the connector); the live theme 183162372393 "Colorblock: NEW WEBSITE" (MAIN), not touched; markets: Canada only, active. Before-snapshot: `snapshots/shipping-zones-2026-09-28-before.json` (the general profile's three zones, their countries, and every rate with its price and conditions).

| What | Through | IDs and notes |
| --- | --- | --- |
| Zone "International" (26 countries, Canada Post calculated rates) deleted | Connector | `deliveryProfileUpdate` on `gid://shopify/DeliveryProfile/120347820329`, `zonesToDelete`: `gid://shopify/DeliveryZone/528002416937` |
| Zone "US Cross-border" (United States, five flat rates) deleted | Connector | The same call: `gid://shopify/DeliveryZone/528002384169` |

**Checked after:** read back through the connector: the general profile has one zone, "Domestic" (Canada), with one rate, "Shipping within Canada", $20.00; it still holds 40 variants. The store ships to Canada only.

**Effect on the live site:** none for buyers in Canada, who see the same $20 rate and pickup. Buyers elsewhere couldn't check out before and can't now.

**Undo:** a deleted zone can't be restored, so recreate both from the snapshot: `deliveryProfileUpdate` with `locationGroupsToUpdate` on `gid://shopify/DeliveryLocationGroup/122038845737` and `zonesToCreate`, or in the admin under Settings, Shipping and delivery, General profile. The new zones and rates get new IDs.
