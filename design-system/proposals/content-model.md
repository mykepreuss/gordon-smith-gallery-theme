# Proposal: how content is stored

Status: **Approved 2026-09-25**, all three parts (answers recorded by Michael; `DECISIONS.md` DS-14 to DS-16, P-10 to P-12). Exhibitions use the recommended entry type, and the old exhibition addresses redirect. The exhibition fields were revised after a review of the content in use (part 2). Nothing has been created in the store yet: the definitions below are created when implementation starts, and template reassignment, redirects and hiding the old exhibition pages happen at release.

## Summary

The site's inconsistency comes less from styling than from how pages are built: almost every page has its own template, so every page is designed separately. Three changes fix that at the source.

1. **Page fields.** Every content page gets the same few fields (hero image, whether that image is an artwork, a short label, an intro sentence, which programme it belongs to). Seven shared templates read those fields instead of 28 one-off templates.
2. **Exhibitions as structured entries.** An exhibition is entered once, as data: title, dates, curator, artists, venue, opening reception, key image, text, credits, installation photos. The On Now, Upcoming and Home lists build themselves from the dates, and every exhibition page uses the same design.
3. **Artwork label fields on products.** Artist, title, year, medium and edition are stored as fields and shown as a museum label, instead of typing decorative Unicode letters into product titles.

Each part can be approved on its own. Part 1 is the foundation for the page templates in DESIGN.md §7; parts 2 and 3 matter most for Exhibitions and the Shop. Parts 4 to 6 (card groups, events, smaller field additions) were added and approved on 2026-09-25 for the new theme (P-13, P-16).

## What we found

Read-only snapshot of the live store (Admin API, 2026-09-25):

- **32 published pages use 28 page templates; 25 of those templates serve exactly one page.** Every exhibition has its own template (`exhibition-ftg`, `exhibition-ohad-2026`, `exhibition-playhouse`, `exhibition-prevailing`, `exhibition-stitched`, `exhibition-taoc`), as do On Now, Upcoming Exhibitions, Past Exhibitions, the Exhibitions overview and each programme page. Our Story uses the Shop template.
- **Why this happens:** in Shopify, a template's sections are shared by every page assigned to it. The only way to give one page its own hero image or intro inside a section is to copy the template. Each copy then drifts. This is the platform limitation the developer notes asked us to flag (REUSE-04).
- **Portfolios use three collection templates** (`collection-template`, `alt-collection-temp`, `all-products-template`) and **products use state-specific templates** (`not-available-yet-product`, `no-frame-product`).
- **Product titles fake italics with Unicode "mathematical" letters**, e.g. `Arnold Shives, 𝘚𝘦𝘷𝘦𝘯 𝘚𝘪𝘴𝘵𝘦𝘳𝘴 𝘙𝘢𝘯𝘨𝘦, 2003`. Mulish has no such characters, so those words render in a fallback system font (one cause of TYPE-03). Store search for "Seven Sisters" does not match them, and many screen readers read them letter by letter or skip them. Our font audit script flags them (`scripts/audit_fonts.py`).
- **No custom page fields or content entry types exist yet.** The store has Shopify's standard product-category definitions and one custom product field (`custom.featured_frame`).

## 1. Page fields

Add these fields to Pages (namespace `custom`):

| Field | Type | Used for |
| --- | --- | --- |
| `hero_image` | File (image) | Hero or page-header image. Focal point is set on the image in Files. |
| `hero_is_artwork` | True or false | Chooses the artwork hero (whole work, never cropped) or the photo hero. |
| `eyebrow` | Single line text | Optional label above the title, only when it adds something the title doesn't, e.g. the programme a page belongs to ("Artists for Kids"). Blank on most pages (DESIGN.md DS-18). |
| `intro` | Multi-line text | The bold intro paragraph. |
| `programme` | Single line text, choice of Gallery, Smith Foundation, Artists for Kids | Sets the programme colours (DESIGN.md §3.3). |
| `gallery_images` | List of files (images) | Optional image gallery section. |

**How it works:** the shared template's sections are connected to these fields through Shopify's dynamic sources in the theme editor ([Shopify: dynamic sources](https://shopify.dev/docs/storefronts/themes/architecture/settings/dynamic-sources)). The template stays the same for every page; each page supplies its own content.

**Staff workflow:** open the page in Shopify admin, write the body in the normal editor, fill the fields at the bottom of the page, pick the template once. No section editing.

**Migration:** move each page to its target template (mapping in DESIGN.md §7.4) and copy its current hero image and intro into the fields. Reassigning templates on existing pages is a store-level release action; before release, test with the unpublished theme and the `?view=` route.

## 2. Exhibitions

**Decided: an Exhibition entry type (Shopify metaobject) with web pages turned on** (P-10). One place to create an exhibition, one template for every exhibition page, and lists that update themselves. The current exhibition URLs can change; the old ones redirect to the new ones.

### What exhibitions carry today

Reviewed 2026-09-25, read-only: the six exhibition pages, On Now and Upcoming (both currently show *Collect, Assemble, Gather* in full), the Past Exhibitions archive and the exhibition templates in the baseline theme. Seven exhibitions have their own text today: the six pages plus *Collect, Assemble, Gather*.

| Fact | Where it appears today | Field |
| --- | --- | --- |
| Dates | All 7. Upcoming also lists a fall 2027 exhibition with no exact dates ("Coming soon, September 2027") | `start_date`, `end_date`, `dates_note` (new) |
| Curator | All 7, as a full credit whose wording varies: "Curated by", "Co-curated by" with each curator's role and organisation, "with support from the Artists For Kids team" | `curator_credit` (new) |
| Artists | 6 of 7. *One Hundred Artists Deep* lists "Founding Artists" and "Artists" separately; *From the Ground* names contemporary artists and collection artists as two groups | `artists`, `collection_artists` (new) |
| Opening reception | The current exhibition: September 25, 6 PM to 8 PM, welcome ceremony at 7 PM. The past pages don't keep it | `reception_start`, `reception_end`, `reception_note` (new) |
| Venue | The current exhibition: the gallery's name and street address, and student work "presented in the Mezzanine Gallery" | `venue` (new) |
| Other events | The current exhibition: a curatorial tour, October 26, 3:30 PM to 4:30 PM | Event entries that reference the exhibition (part 5) |
| Presenters, partners, sponsors, funders | 5 of 7, often with links; a Canada Council logo on the current exhibition | `credits`, `funder_logos` (new) |
| Key image caption | A photo credit on all 6 pages ("Photo by Rachel Topham"); a full artwork caption on the current exhibition (artist, italic title, year, medium, photo credit) | `key_image_caption` (was `key_image_credit`; now rich text so titles can be italic) |
| Installation photos | All 6 pages (1 to 9 images each); 3 carry a separate photo credit ("Photos by Rachel Topham") | `installation_views`, `installation_credit` |
| Programme | The Exhibitions overview: Artists For Kids exhibitions open each fall; Smith Foundation exhibitions run in spring and summer | `programme` |
| Land acknowledgement | Repeated on 4 exhibition pages in two shorter wordings; the footer already shows the full acknowledgement on every page | No field. The footer covers exhibition pages too |

Also found:

- *Stitched* has two start dates: April 2, 2025 in the archive and April 3, 2025 on its page. An entry holds one date, so this can't recur.
- Six older archive items (2020 to 2023) are labelled "View Exhibition" with no link set. The archive is out of scope (EXH-03); flagged for the gallery.
- Four exhibition pages carry markup pasted from the previous website (page-builder classes and a second `<main>` element, which gives screen readers two main regions), and two carry pasted Word formatting (inline Poppins 13.5pt on *One Hundred Artists Deep*, Word Online markup on *Collect, Assemble, Gather*). Moving the text into fields drops all of it (TYPE-03).

### Fields

Opening reception, curator and venue are required parts of the model (gallery answer 3). Every field except title, start date and key image is optional to fill, because past exhibitions have no reception on record and an upcoming show may not have its details yet. An empty field shows nothing.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `title` | Single line text | Yes | |
| `subtitle` | Single line text | | |
| `start_date` | Date | Yes | Sorting and status. For a show without exact dates, enter the expected opening day and fill `dates_note` |
| `end_date` | Date | | Blank means ongoing |
| `dates_note` | Single line text | | Shown instead of the dates, e.g. "Opens fall 2027" |
| `curator_credit` | Single line text | | The whole line as it should read, e.g. "Curated by Amelia Epp with support from the Artists For Kids team" |
| `artists` | List of single line text | | One name per item; a collective is one item |
| `collection_artists` | List of single line text | | Artists from the permanent collection, shown as a second group (label to confirm) |
| `venue` | Single line text | | Where in the building, e.g. "Main gallery and Mezzanine Gallery" |
| `reception_start` | Date and time | | Opening reception. Shown until the reception has passed |
| `reception_end` | Date and time | | |
| `reception_note` | Single line text | | e.g. "Welcome ceremony at 7 PM" |
| `key_image` | File (image) | Yes | Hero and card image |
| `key_image_is_artwork` | True or false | | Artwork hero (whole work, never cropped) or photo hero |
| `key_image_caption` | Rich text | | Artwork caption, photo credit, or both |
| `summary` | Multi-line text | | Card text, intro, and the description search engines and link previews use |
| `body` | Rich text | | Headings, lists, links, bold, italic |
| `installation_views` | List of files (images) | | Gallery section |
| `installation_credit` | Single line text | | e.g. "Photos by Rachel Topham" |
| `credits` | Rich text | | Presenters, partners, sponsors and funders, with links |
| `funder_logos` | List of files (images) | | Logos a funder requires, e.g. Canada Council for the Arts |
| `programme` | Single line text, choice | | Gallery, Smith Foundation or Artists for Kids |

**Status is computed, not typed.** A snippet compares today with the start and end dates (`theme/snippets/gs-exhibition-status.liquid`), so an exhibition moves from Upcoming to On Now to Past on its own. Liquid can loop over up to 50 entries at once and paginate up to 250 per page ([Shopify: metaobject_definition](https://shopify.dev/docs/api/liquid/objects/metaobject_definition)); the gallery will stay well inside that.

**Past Exhibitions (DS-24, decided by Michael 2026-09-25).** The Past page lists past entries automatically, newest first, above the existing archive, so an exhibition that closes appears there without anyone adding it. The six migrated exhibitions leave the hand-built archive at release; the six older items stay exactly as they are (EXH-03).

**Web address and search.** Entry pages live at `/pages/<type handle>/<entry handle>` ([Shopify: metaobject capabilities](https://shopify.dev/docs/apps/build/metaobjects/use-metaobject-capabilities)). With the type handle `exhibitions`, *Playhouse* becomes `/pages/exhibitions/playhouse`. The page title and description for search engines come from `title` and `summary`.

**Staff workflow:** the gallery's admin account creates entries and fills page fields (P-12). Content, then Metaobjects, then Exhibitions, then Add entry. Fill the fields and save. The exhibition gets its own page and appears in the right list on the right dates.

### Migration

1. Create the entries as drafts: the six exhibition pages, *Collect, Assemble, Gather* (from On Now), *Against the Latitude of "Progress"* (April 9 to June 19, 2027) and the fall 2027 exhibition (dates note only). Also the six older shows from the Past Exhibitions archive (title, dates, image): 15 entries in all. Copy the text into the fields; pasted formatting stays behind.
2. The new theme's Past Exhibitions page lists entries only (DS-25).
3. At release, in this order: set the entries to active, publish the theme, hide the six old exhibition pages, create the six redirects, then open each old address and check it lands on its entry. Clear the copy of the exhibition text from the On Now and Upcoming page bodies; it now lives in the entry.
4. Rollback: republish the baseline theme, unhide the six pages, delete the six redirects.

Redirects only work from addresses that no longer load a page ([Shopify Help: URL redirects](https://help.shopify.com/en/manual/online-store/menus-and-links/url-redirect)), which is why the old pages are hidden first. Hiding rather than deleting keeps them for rollback.

| Old address | New address (entry handles proposed) |
| --- | --- |
| `/pages/exhibition-one-hundred-artists-deep` | `/pages/exhibitions/one-hundred-artists-deep` |
| `/pages/exhibition-from-the-ground` | `/pages/exhibitions/from-the-ground` |
| `/pages/exhibition-stitched-merging-photography-and-textile-practices` | `/pages/exhibitions/stitched` |
| `/pages/exhibition-playhouse` | `/pages/exhibitions/playhouse` |
| `/pages/exhibition-prevailing-landscapes` | `/pages/exhibitions/prevailing-landscapes` |
| `/pages/exhibition-the-art-of-conversation` | `/pages/exhibitions/the-art-of-conversation` |

**Check in the review theme before release:**

- Whether draft entries can be previewed there, or need to be active (nothing links to an active entry until release).
- The link preview image (social sharing) on entry pages.
- The timezone Liquid uses for status and reception times.
- What an entry address shows under the live theme before release.

**Tradeoffs:** six addresses change, covered by redirects; staff learn one new admin area; the rich text fields have no inline images (images go in the image fields, which keeps layouts consistent).

**Option B** (keep exhibition pages and attach an entry to each) is not needed, because the addresses can change.

**Phase 2, not proposed now:** labelled works in each exhibition (artist, title, year, medium, credit per image) would need an Artwork entry type. The design system already has the "works" gallery layout for it.

## 3. Artwork label fields on products

Add to Products (namespace `custom`): `artist`, `artwork_title`, `year` (text, so "c. 1975" works), `medium`, `edition` (e.g. "Edition of 50"), optional `dimensions`.

- Product titles become plain text in the same order, e.g. `Arnold Shives, Seven Sisters Range, 2003`, which fixes search, order emails and screen readers.
- The theme builds the label from the fields: artist in bold, title in italics (a real `<cite>`), then year, medium and edition. If the fields are empty it falls back to the product title, so nothing breaks mid-migration.
- The two state-specific product templates fold into one. "Not available yet" comes from product data (a `custom.coming_soon` true/false field or inventory), and framing keeps using the existing `custom.featured_frame`.

This restructures information the store already has; it doesn't add shop functionality, so it stays inside the plan's scope. Updating the 21 Limited Edition products can be scripted through the Admin API once approved.

## 4. Card groups

Status: **Approved 2026-09-25** (P-16). Found by the content inventory for the new theme (`proposals/content-migration.md`): 5 pages show grids of cards (image, title, short text, link), and the approved fields have no place for them.

- **Card** entry: `image` (image), `title` (required), `text` (multi-line), `link` (link: label and address), `logo` (one of Gallery, Smith Foundation, Artists for Kids; added 2026-09-26, DS-50). External links get the external cue automatically. A card with a logo is about that organisation: the logo is its heading.
- **Card group** entry: `heading` (optional) and `cards` (list of cards, required).
- **Page field** `custom.card_groups`: list of card groups, shown in order after the page body.

In use for: About (the three organisations), Artists for Kids (6 programmes on its own site), Public Programs (4 programmes), The Smith Foundation (5 ways to take part, and the 14-person board), Donate (4 ways to give). Staff don't choose a layout: cards with images show as image cards, cards without as text cards, and a group of cards with logos as one organisation per row (DESIGN.md §6.5). About and About Us (the three organisations, each beside its logo) use the last since 2026-09-26.

## 5. Events

Status: **Approved 2026-09-25** (P-16). Four programme pages list dated events typed into their templates, and the current exhibition lists a curatorial tour; nothing removes them once they've passed.

**Event** entry, no page of its own:

| Field | Type | Notes |
| --- | --- | --- |
| `title` | Single line text | Required |
| `starts` | Date and time | Required |
| `ends` | Date and time | |
| `location` | Single line text | Blank means the gallery, e.g. "Main floor" |
| `summary` | Multi-line text | |
| `image` | Image | |
| `tickets` | Link | Label and address, e.g. "Buy tickets". Until tickets are on sale, say so in the summary |
| `programme_page` | Page | The programme page it belongs to (Explore + Create, Music at the Smith...) |
| `exhibition` | Exhibition entry | For tours and talks tied to an exhibition |

Each programme page lists its upcoming events; the Upcoming Events page lists all of them; an exhibition page lists its own. An event drops off every list once it has ended. This **replaces the approved exhibition field `events`** (P-11): one place for all events instead of a rich text field on exhibitions.

## 6. Smaller field additions

Status: **Approved 2026-09-25** (P-16).

| Where | Field | Type | Why |
| --- | --- | --- | --- |
| Pages | `custom.hero_caption` | Single line text | Photo credits under heroes ("Photo by Khim Mata Hipol") on 6 pages |
| Pages | `custom.cta` | Link | One call to action per page: Artists For Kids website, Browse the collection, Volunteer form, Year in review |
| Collections | `custom.photo_credit` | Single line text | "Photography by Rachel Topham" on portfolio pages |
| Products | `custom.availability_note` | Single line text | Shown with `coming_soon`, e.g. "Available September 25 at noon (PT)" |

## Answers, 2026-09-25

1. All three parts are approved (DS-14, DS-15, DS-16).
2. Exhibition addresses can change; redirect the old ones (P-10).
3. Opening reception date, curator and venue are required parts of the model; review what's in use. Done in part 2, which added the other new fields (P-11).
4. The admin account creates exhibition entries and fills page fields (P-12).

## Still open

| # | Question | For | Default until answered |
| --- | --- | --- | --- |
| 1 | Room names, if `venue` should be a fixed list instead of free text (only "Mezzanine Gallery" appears on the site today) | Gallery | Free text |
| 2 | Label for the second artist group (*One Hundred Artists Deep* used "Founding Artists") | Gallery | "From the collection" |
| 3 | *Stitched* start date: April 2 or April 3, 2025 | Gallery | April 3 (its own page) |

## Definitions for parts 4 to 6 (approved; not created yet)

```json
{
  "metaobjectDefinitions": [
    {"type": "card", "name": "Card", "displayNameKey": "title", "fields": [
      {"key": "image", "type": "file_reference", "validations": {"file_type_options": ["Image"]}},
      {"key": "title", "type": "single_line_text_field", "required": true},
      {"key": "text", "type": "multi_line_text_field"},
      {"key": "link", "type": "link"},
      {"key": "logo", "type": "single_line_text_field", "validations": {"choices": ["Gallery", "Smith Foundation", "Artists for Kids"]}}]},
    {"type": "card_group", "name": "Card group", "displayNameKey": "heading", "fields": [
      {"key": "heading", "type": "single_line_text_field"},
      {"key": "cards", "type": "list.metaobject_reference", "required": true, "validations": {"metaobject_definition_type": "card"}}]},
    {"type": "event", "name": "Event", "displayNameKey": "title", "capabilities": {"publishable": true}, "fields": [
      {"key": "title", "type": "single_line_text_field", "required": true},
      {"key": "starts", "type": "date_time", "required": true},
      {"key": "ends", "type": "date_time"},
      {"key": "location", "type": "single_line_text_field"},
      {"key": "summary", "type": "multi_line_text_field"},
      {"key": "image", "type": "file_reference", "validations": {"file_type_options": ["Image"]}},
      {"key": "tickets", "type": "link"},
      {"key": "programme_page", "type": "page_reference"},
      {"key": "exhibition", "type": "metaobject_reference", "validations": {"metaobject_definition_type": "exhibition"}}]}
  ],
  "pageMetafields": [
    {"namespace": "custom", "key": "card_groups", "type": "list.metaobject_reference", "validations": {"metaobject_definition_type": "card_group"}},
    {"namespace": "custom", "key": "hero_caption", "type": "single_line_text_field"},
    {"namespace": "custom", "key": "cta", "type": "link"}
  ],
  "collectionMetafields": [
    {"namespace": "custom", "key": "photo_credit", "type": "single_line_text_field"}
  ],
  "productMetafields": [
    {"namespace": "custom", "key": "availability_note", "type": "single_line_text_field"}
  ]
}
```

## Definitions (approved; not created yet)

```json
{
  "pageMetafields": [
    {"namespace": "custom", "key": "hero_image", "type": "file_reference", "validations": {"file_type_options": ["Image"]}},
    {"namespace": "custom", "key": "hero_is_artwork", "type": "boolean"},
    {"namespace": "custom", "key": "eyebrow", "type": "single_line_text_field"},
    {"namespace": "custom", "key": "intro", "type": "multi_line_text_field"},
    {"namespace": "custom", "key": "programme", "type": "single_line_text_field", "validations": {"choices": ["Gallery", "Smith Foundation", "Artists for Kids"]}},
    {"namespace": "custom", "key": "gallery_images", "type": "list.file_reference"}
  ],
  "metaobjectDefinition": {
    "type": "exhibition",
    "name": "Exhibition",
    "displayNameKey": "title",
    "access": {"storefront": "PUBLIC_READ"},
    "capabilities": {"publishable": true, "renderable": {"metaTitleKey": "title", "metaDescriptionKey": "summary"}, "onlineStore": {"urlHandle": "exhibitions"}},
    "fields": [
      {"key": "title", "type": "single_line_text_field", "required": true},
      {"key": "subtitle", "type": "single_line_text_field"},
      {"key": "start_date", "type": "date", "required": true},
      {"key": "end_date", "type": "date"},
      {"key": "dates_note", "type": "single_line_text_field"},
      {"key": "curator_credit", "type": "single_line_text_field"},
      {"key": "artists", "type": "list.single_line_text_field"},
      {"key": "collection_artists", "type": "list.single_line_text_field"},
      {"key": "venue", "type": "single_line_text_field"},
      {"key": "reception_start", "type": "date_time"},
      {"key": "reception_end", "type": "date_time"},
      {"key": "reception_note", "type": "single_line_text_field"},
      {"key": "key_image", "type": "file_reference", "required": true, "validations": {"file_type_options": ["Image"]}},
      {"key": "key_image_is_artwork", "type": "boolean"},
      {"key": "key_image_caption", "type": "rich_text_field"},
      {"key": "summary", "type": "multi_line_text_field"},
      {"key": "body", "type": "rich_text_field"},
      {"key": "installation_views", "type": "list.file_reference", "validations": {"file_type_options": ["Image"]}},
      {"key": "installation_credit", "type": "single_line_text_field"},
      {"key": "credits", "type": "rich_text_field"},
      {"key": "funder_logos", "type": "list.file_reference", "validations": {"file_type_options": ["Image"]}},
      {"key": "programme", "type": "single_line_text_field", "validations": {"choices": ["Gallery", "Smith Foundation", "Artists for Kids"]}}
    ]
  },
  "productMetafields": [
    {"namespace": "custom", "key": "artist", "type": "single_line_text_field"},
    {"namespace": "custom", "key": "artwork_title", "type": "single_line_text_field"},
    {"namespace": "custom", "key": "year", "type": "single_line_text_field"},
    {"namespace": "custom", "key": "medium", "type": "single_line_text_field"},
    {"namespace": "custom", "key": "edition", "type": "single_line_text_field"},
    {"namespace": "custom", "key": "dimensions", "type": "single_line_text_field"},
    {"namespace": "custom", "key": "coming_soon", "type": "boolean"}
  ]
}
```

Checked 2026-09-25 against the store's list of field types (`date_time`, `rich_text_field`, `list.file_reference` and the `choices` and `file_type_options` validations are all available), and a `metaobjectDefinitionCreate` mutation with these capabilities validates against the Admin API schema. Nothing has been run. In the mutation, validations are name and value pairs, e.g. `{name: "choices", value: "[\"Gallery\",\"Smith Foundation\",\"Artists for Kids\"]"}`.
