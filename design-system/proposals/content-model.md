# Proposal: how content is stored

Status: **Proposed, needs gallery approval.** 2026-09-25. These are store-level changes (new fields and entry types in Shopify admin, template reassignment, redirects). Nothing has been created or changed in the store. Under the implementation plan they stay as reviewable definitions in Git until approved, then go through the preview and release gates.

## Summary

The site's inconsistency comes less from styling than from how pages are built: almost every page has its own template, so every page is designed separately. Three changes fix that at the source.

1. **Page fields.** Every content page gets the same few fields (hero image, whether that image is an artwork, a short label, an intro sentence, which programme it belongs to). Seven shared templates read those fields instead of 28 one-off templates.
2. **Exhibitions as structured entries.** An exhibition is entered once, as data: title, dates, artists, key image, text, installation photos. The On Now, Upcoming and Home lists build themselves from the dates, and every exhibition page uses the same design.
3. **Artwork label fields on products.** Artist, title, year, medium and edition are stored as fields and shown as a museum label, instead of typing decorative Unicode letters into product titles.

Each part can be approved on its own. Part 1 is the foundation for the page templates in DESIGN.md §7; parts 2 and 3 matter most for Exhibitions and the Shop.

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

**Recommendation: an Exhibition entry type (Shopify metaobject) with web pages turned on.** One place to create an exhibition, one template for every exhibition page, and lists that update themselves.

| Field | Type | Notes |
| --- | --- | --- |
| `title` | Single line text | Required |
| `subtitle` | Single line text | Optional |
| `artists` | List of single line text | Later could reference Artist entries |
| `start_date` | Date | Required |
| `end_date` | Date | Blank means ongoing |
| `key_image` | File (image) | Required; hero and card image |
| `key_image_is_artwork` | True or false | Artwork hero vs photo hero |
| `key_image_credit` | Single line text | Caption or photo credit |
| `summary` | Multi-line text | Card text and intro |
| `body` | Rich text | Headings, lists, links, bold, italic |
| `installation_views` | List of files (images) | Gallery section |
| `installation_credit` | Single line text | e.g. "Photos: Name" |
| `programme` | Single line text, choice | Usually Gallery |

**Status is computed, not typed.** A snippet compares today with the start and end dates (`liquid/snippets/gs-exhibition-status.liquid`), so an exhibition moves from Upcoming to On Now to Past on its own. Liquid can loop over up to 50 entries at once and paginate up to 250 per page ([Shopify: metaobject_definition](https://shopify.dev/docs/api/liquid/objects/metaobject_definition)); the gallery will stay well inside that.

**Staff workflow:** Content, then Metaobjects, then Exhibitions, then Add entry. Fill the fields and save. The exhibition gets its own page and appears in the right list on the right dates.

**Migration:** turn the six current exhibition pages into entries and redirect their old URLs to the new ones (URL redirects are a store-level change). Past Exhibitions keeps its current page and presentation (EXH-03; rebuilding the archive is out of scope). New exhibitions are created as entries from then on.

**Option B, if the current exhibition URLs must not change** (printed material, QR codes, press links): keep exhibition pages, store the data in an Exhibition entry, and connect them with a page field `custom.exhibition`. It works, but staff create two things and link them for every exhibition, which leaves room for mismatches.

**Tradeoffs and risks of the recommendation:**
- Six URLs change, covered by redirects.
- Staff learn one new admin area.
- The rich text field has no inline images; images go in the image fields, which is what keeps layouts consistent.
- The exact URL pattern and SEO fields for entry pages need confirming in the review theme ([Shopify: metaobject templates](https://shopify.dev/docs/storefronts/themes/architecture/templates/metaobject)).

**What would change the recommendation:** the gallery needing the current exhibition URLs unchanged (then Option B), or the review theme showing entry pages lack something the gallery relies on, such as social sharing images.

**Phase 2, not proposed now:** labelled works in each exhibition (artist, title, year, medium, credit per image) would need an Artwork entry type. The design system already has the "works" gallery layout for it.

## 3. Artwork label fields on products

Add to Products (namespace `custom`): `artist`, `artwork_title`, `year` (text, so "c. 1975" works), `medium`, `edition` (e.g. "Edition of 50"), optional `dimensions`.

- Product titles become plain text in the same order, e.g. `Arnold Shives, Seven Sisters Range, 2003`, which fixes search, order emails and screen readers.
- The theme builds the label from the fields: artist in bold, title in italics (a real `<cite>`), then year, medium and edition. If the fields are empty it falls back to the product title, so nothing breaks mid-migration.
- The two state-specific product templates fold into one. "Not available yet" comes from product data (a `custom.coming_soon` true/false field or inventory), and framing keeps using the existing `custom.featured_frame`.

This restructures information the store already has; it doesn't add shop functionality, so it stays inside the plan's scope. Updating the 21 Limited Edition products can be scripted through the Admin API once approved.

## What we need from the gallery

1. Approval, or not, for each of the three parts.
2. For exhibitions: do the current exhibition page URLs need to stay exactly as they are? That decides the recommendation or Option B.
3. Anything missing from the field lists (e.g. opening reception date, curator, venue within the building).
4. Who will create exhibition entries and fill page fields day to day.

## Definitions for review (not created)

```json
{
  "pageMetafields": [
    { "namespace": "custom", "key": "hero_image", "type": "file_reference", "validations": { "file_type_options": ["Image"] } },
    { "namespace": "custom", "key": "hero_is_artwork", "type": "boolean" },
    { "namespace": "custom", "key": "eyebrow", "type": "single_line_text_field" },
    { "namespace": "custom", "key": "intro", "type": "multi_line_text_field" },
    { "namespace": "custom", "key": "programme", "type": "single_line_text_field", "validations": { "choices": ["Gallery", "Smith Foundation", "Artists for Kids"] } },
    { "namespace": "custom", "key": "gallery_images", "type": "list.file_reference" }
  ],
  "metaobjectDefinition": {
    "type": "exhibition",
    "name": "Exhibition",
    "displayNameKey": "title",
    "capabilities": { "publishable": true, "onlineStore": true, "renderable": true },
    "fields": [
      { "key": "title", "type": "single_line_text_field", "required": true },
      { "key": "subtitle", "type": "single_line_text_field" },
      { "key": "artists", "type": "list.single_line_text_field" },
      { "key": "start_date", "type": "date", "required": true },
      { "key": "end_date", "type": "date" },
      { "key": "key_image", "type": "file_reference", "required": true },
      { "key": "key_image_is_artwork", "type": "boolean" },
      { "key": "key_image_credit", "type": "single_line_text_field" },
      { "key": "summary", "type": "multi_line_text_field" },
      { "key": "body", "type": "rich_text_field" },
      { "key": "installation_views", "type": "list.file_reference" },
      { "key": "installation_credit", "type": "single_line_text_field" },
      { "key": "programme", "type": "single_line_text_field" }
    ]
  },
  "productMetafields": [
    { "namespace": "custom", "key": "artist", "type": "single_line_text_field" },
    { "namespace": "custom", "key": "artwork_title", "type": "single_line_text_field" },
    { "namespace": "custom", "key": "year", "type": "single_line_text_field" },
    { "namespace": "custom", "key": "medium", "type": "single_line_text_field" },
    { "namespace": "custom", "key": "edition", "type": "single_line_text_field" },
    { "namespace": "custom", "key": "dimensions", "type": "single_line_text_field" },
    { "namespace": "custom", "key": "coming_soon", "type": "boolean" }
  ]
}
```

Field types and validation names follow the Admin API metafield and metaobject definition inputs; validate them with the Shopify GraphQL schema before creating anything.
