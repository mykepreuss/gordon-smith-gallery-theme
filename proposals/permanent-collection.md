# The Permanent Collection on gordonsmithgallery.com

Status: **Proposed**, 2026-09-26, for Michael. Parts need the gallery (marked **Gallery**).

Michael, 2026-09-26: "I don't like that all of these assets are on an external site and would prefer them to be part of gordonsmithgallery.com... put together a plan to integrate all of the assets into our Shopify site rather than the external catalogue site."

## In short

- **Move the whole collection into the store as content entries.** That's every work, its images, its artist and its groupings. It follows the pattern the exhibitions already use (DS-14, P-10):
  - works at `/pages/collection/<work>`;
  - artists at `/pages/artists/<artist>`;
  - groupings such as Prints or Ecology at `/pages/browse/<grouping>`.
- **The Permanent Collection page becomes the front door.** It gets a search box, ways to browse, and the gallery's own introduction. Its "Browse" button stops sending people away.
- **Images come from the originals.** The catalogue's masters are TIFF files, 36 GB in all, which Shopify doesn't accept. They're converted once into large web images, and the masters stay where they are.
- **Nothing shows on the live site until release.** The entries are built and reviewed on the review theme, as the exhibitions were. At release, every old catalogue address forwards to its new page, and the catalogue can then be retired.

## What the catalogue holds

Read on 2026-09-26 through the catalogue's public API (Omeka S). `proposals/collection/inventory.py` repeats the count.

| | Count | Notes |
| --- | --- | --- |
| Works | 1,291 | All public. Identifier (accession number) on every one, 4 used twice |
| Artists | 313 spellings | About 204 names once dates typed into the name are removed. Some names have several spellings or different life dates |
| Images | 1,530 | 1,045 TIFF, 467 JPEG, 18 PNG. The catalogue's own web copies are only 800 px wide |
| Documents | 144 PDFs | Mostly "Text Resources": artists' press, exhibitions and photographs. 39 are over 20 MB |
| All files | 36.4 GB | 588 files over 20 MB; the largest is 346 MB |
| Groupings (item sets) | 101 | See below |
| Works without an image | 8 | |
| Works without a title | 7 | |

**How the catalogue's fields map to the site:**

| Catalogue field | Filled | What it holds | On the site |
| --- | --- | --- | --- |
| Title | 1,284 | Title; 237 "Artist Archives" titles carry the edition, e.g. "October Yellow (18/39)" | Title |
| Creator | 1,291 | Artist, sometimes with "(DOB: 1909 - 1998)" | Artist entry, with life dates |
| Date | 1,115 | Mostly a year; also "N.D.", ranges, "20th century" | Year, written as given |
| Format | 1,165 | Print 713, Painting 152, Drawing 132, Photograph 66, Sculpture 62, Ceramics 21, Printmaking 7, Textile 4 (capitals vary) | Category |
| Medium | 1,151 | Medium | Medium |
| Spatial Coverage | 1,137 | Dimensions, e.g. `28" x 36" x 1" (unframed)` | Dimensions |
| References | 263 | Edition numbers, e.g. "18/39", "AP 4/6" | Edition |
| Rights | 1,086 | "Collection of Artists for Kids and the Gordon Smith Gallery" | Credit line |
| Contributor | 691 | Mostly donors ("Alan & Elizabeth Bell" 150, "Lightheart Estate" 55), sometimes the artist | Credit line "Gift of …", if the gallery agrees |
| Subject | 735 | 30 themes: abstract, storytelling, creatures, landscape, ecology, indigenous, people… | Themes |
| Description | 480 | Visual descriptions, e.g. "black and white image of a bird against a colourful background" | The images' alt text |
| Type | 37 | **Storage locations**: "2nd FLR, Reception Waiting Area", "Queen Mary Elementary" | Not published |
| Provenance | 38 | Donation notes with names and dates | Not published |
| Alternative Title | 186 | Old identifiers, e.g. "*Previously: BARR-AA001" | Not published; kept for the redirects |

**The 101 groupings:**
- Categories: Paintings, Prints, Sculptures, Textiles, Ceramics, Drawings, Photography.
- Themes: People, Architecture, Creatures, Action, Social Change, Storytelling, Ecology, Invention.
- Indigenous.
- AFK Published Editions, collection copy: 103 works.
- Teaching Collection: 195 works.
- Three exhibitions: The Art of Conversation, Playhouse, From the Ground.
- Two donations: Lightheart Estate, Ian Thom.
- 17 artist sets ("… Artworks").
- 62 artist "Text Resources" sets.
- "Things On Loan to AFK": 6 works the collection doesn't own.

The catalogue shows storage locations and donor notes to anyone today. They stay behind in the move.

## How it works in the store

### Three new entry types

Each is a new definition, the kind of store write allowed before release. The pages return 404 under the live theme, so the live site doesn't change.

**Artwork** (`artwork`, web pages at `/pages/collection/<handle>`)

| Field | Type | From |
| --- | --- | --- |
| Title | single line | Title, without an edition in brackets |
| Artist | artist entry | Creator |
| Year | single line | Date, as written |
| Category | choice | Format, tidied: Painting, Print, Drawing, Photograph, Sculpture, Ceramic, Textile, Book |
| Medium | single line | Medium |
| Dimensions | single line | Spatial Coverage |
| Edition | single line | References, or the edition taken out of the title |
| Accession number | single line | Identifier |
| Credit line | single line | Rights, plus "Gift of …" if the gallery agrees |
| Images | list of files | The converted images, in the catalogue's order; alt text from Description |
| Themes | list of choices | Subject, tidied to the gallery's terms |
| About the work | rich text | Empty for now; for the gallery's own text later |
| In the Shop | product | The limited edition for sale, when one matches (AFK Published Editions) |
| Shown in | list of exhibition entries | The three exhibition groupings, linked to their exhibition pages |

**Artist** (`artist`, web pages at `/pages/artists/<handle>`)
- Fields: name, life dates, nationality or Nation (from the gallery), biography (empty for now), website.
- Documents: a list of files, from the Text Resources.

The page lists the artist's works and any editions in the Shop. Later, this entry can also build the Artists page, which today is a hand-typed list of 59 links.

**Browse grouping** (`collection_group`, web pages at `/pages/browse/<handle>`)
- Fields: name, kind (category, theme, grouping), introduction, works (a list of up to 1,024 works; Prints has 713).
- It carries the categories, themes, Indigenous artists, AFK Published Editions and the Teaching Collection, if the gallery wants it public.
- The artist sets become the artist pages. The donation sets become groupings only if the gallery wants donors named.

### Why entries, not products

Products would bring the store's search and filters for free. But entries fit this project better:

1. **Nothing leaks before release.** Entries without a template on the live theme return 404, which is how the exhibitions are staged today. Products published to the Online Store would show at once in the live site's search and product pages. Unpublished products couldn't be reviewed on the review theme at all.
2. **The collection isn't for sale.** 1,291 "products" would sit beside the 21 editions:
   - in the admin;
   - in sales channels;
   - in reports.
   Each would need a price of $0 and a sold-out state, and each would risk turning up in the Shop.
3. **It's the model we already have.** Exhibitions, events and cards are entries, and staff edit them in the same place.

### The gap, and how to close it

Shopify's site search covers only products, pages and articles, so the entries won't show in it. Two parts close the gap:

- **Collection search.** The collection pages publish a small index (title, artist, year, category, themes, one thumbnail), about 150 KB for 1,291 works. The search box on the Permanent Collection page filters it as you type, by words, artist, category, theme and decade.
  - Without JavaScript, the browse and artist pages still reach every work.
  - This follows DS-19: the site works first, and the script improves it.
- **Site search.** The site's search results page adds "In the collection" matches from the same index, under the store's own results.

### Limits checked (shopify.dev, 2026-09-26)

- **Entries:** up to 1,000,000 per type, and 40 fields each.
- **Reference lists:** up to 1,024 items.
- **Pages:** Liquid pages through entries up to 25,000.
- **Images:** JPEG, PNG, WEBP, HEIC or GIF, at most 20 MB and 4,472 × 4,472 px. TIFF isn't accepted.
- **Documents:** generic files are also capped. The 39 PDFs over 20 MB need compressing, or stay linked where they are.

## Pages and design (design system first)

Each new component goes into `design-system/` first, as for every page so far. New templates need a DS decision (§7.2).

- **Permanent Collection (`/pages/permanent-collection`):**
  - hero;
  - the gallery's introduction (kept word for word);
  - the collection search;
  - ways in, as cards for the categories and themes;
  - a row of featured works;
  - a line with the count ("1,291 works by 204 artists"), from the data.
- **Work page:** reuses the product page's artwork layout (DS-38) without price or cart.
  - Every image whole on the mat.
  - The museum label: artist, title, year, medium, dimensions, edition, accession number and credit line.
  - "In the Shop" when the edition is for sale.
  - "Shown in" the exhibition.
  - "More by this artist" in a row of artwork tiles.
- **Artist page:** name and life dates, then the works in a grid, editions in the Shop, and documents.
- **Browse page:** the grouping's name and introduction, then its works in artwork tiles, all of them in one list (lazy-loaded images). Liquid can't read page numbers from a list field, and a long list reads well with the search above it.
- **Links in from the rest of the site:**
  - exhibition pages ("Works in the collection");
  - Shop products ("A copy is in the permanent collection");
  - the Artists for Kids history.

## Images

1. **Get the masters.** Either download them from the catalogue (36 GB; ask the district's IT first) or copy them from the gallery's own drive, if that's where they came from (**Gallery**).
2. **Convert.** Each image becomes a JPEG 3,000 px on its long side, in sRGB with its colour profile applied, at quality 85. That's about 1 to 3 MB each, 2 to 3 GB for all of them. The conversion checks colour mode (CMYK scans convert differently) and keeps the full artwork: no cropping.
3. **Upload** with the Admin API (`fileCreate`) from a staging location. Record each file's ID against its accession number, so re-running changes nothing.
4. **Alt text:** "Artist, Title, year" (§6.4), then the catalogue's visual description where there is one (480 works).

The masters stay archived where they are. The site only ever needs the web copies.

## Cleaning the data

The script does the mechanical work and writes review sheets. The gallery corrects the sheets before anything is imported (**Gallery**):

- **Artists:** one row per name, with its spellings, suggested life dates and work count.
  - 313 spellings become about 204 names.
  - Conflicts are marked, e.g. Ann Meredith Barry has four different life dates.
- **Categories:** capitals made consistent. "Printmaking" becomes Print.
- **Themes:** 30 terms. Near-duplicates are merged, e.g. "creature" and "creatures".
- **Titles:** editions moved out of 237 titles into the Edition field.
- **Problems listed:** the 4 duplicate accession numbers, 7 works without titles and 8 without images.
- **Public or private:** a list of every field, marked public or not publishing (locations, provenance, old identifiers).

## Importing

Scripts go in `proposals/store-writes/collection/`, following the same rules as every store write so far:

1. `inventory.py`: a fresh read-only export.
2. `clean.py`: builds the review sheets, then reads back the gallery's corrections.
3. `images.py`: converts and uploads the images, and records the file IDs.
4. `import.py`: dry run first, then upserts artists, then works, then groupings, keyed by accession number. A re-run updates in place.
5. `verify.py`: counts, missing images, and a sample of pages checked against the catalogue.
6. `redirects.py`: the map from every old address to its new page.

Every run is logged in `proposals/store-writes/README.md`, with Michael's go-ahead and a before-snapshot. All of it is the allowed kind of write before release: new definitions, new files, and new entries that 404 under the live theme.

## Redirects and retiring the catalogue

- **At release:** the Permanent Collection page's "Browse" button points to the collection search on the page itself.
- **Every old address gets a new one:**
  - item pages (`/s/TheCollection/item/<id>`) go to their work;
  - the artist and category pages go to their artist or browse page;
  - the home page goes to `/pages/permanent-collection`.
- **Recommended way to forward:** once the gallery stops editing in the catalogue, point `afkcatalogue.sd44.ca` at Shopify as an extra domain. Shopify then forwards every old address with its own URL redirects from the map. It needs one DNS change by the school district's IT (**Gallery**).
- **Fallback:** the district keeps the catalogue server and adds forwarding rules from the same map.
- Keep the catalogue read-only for a few months after release, then retire it. The masters stay archived.

## Who edits where, afterwards

- **New acquisitions:** added in the Shopify admin (Content, Metaobjects, Artwork), with images in Files. A staff editing test covers it.
- **Private records (Gallery):** the catalogue also holds records the public shouldn't see: where each work is, provenance and donors. The gallery decides where those live after the catalogue retires:
  - a collections management tool or spreadsheet the gallery already keeps; or
  - an admin-only "Artwork record" entry in the store, which the site can't read.

## Order of work

| Step | What | Who | About |
| --- | --- | --- | --- |
| 0 | Decisions below | Michael, gallery | |
| 1 | Trial with 20 works end to end: definitions, images, three templates, the search index, one redirect. Proves the URLs, the index size and the image quality before the rest | Agent | 2 days |
| 2 | Design passes: Permanent Collection page, work, artist, browse and search, in the design system first | Agent, Michael approves | 3 to 4 days |
| 3 | Data clean-up sheets; the gallery reviews artists, categories and public fields | Agent, gallery | Depends on the gallery |
| 4 | Image conversion and upload | Agent | 1 to 2 days, mostly waiting |
| 5 | Full import, verification report, review on the review theme, staff editing test | Agent, staff | 2 days |
| 6 | At release, or right after it: the Browse button, the redirects, the catalogue read-only | Agent, district IT | |

It doesn't need to hold up the site's release. The collection is additive, so it can go live with the release or in a second release soon after.

## Decisions needed

**Michael**
1. Entries, as recommended, rather than products.
2. The addresses: `/pages/collection/`, `/pages/artists/`, `/pages/browse/`.
3. Whether the collection goes live with the site or after it.
4. Go-ahead for the trial (step 1): three definitions, 20 works and their images in the store, invisible to the live site.

**Gallery**
1. Licences: do the image permissions (CARFAC or artists' agreements) cover showing the works on gordonsmithgallery.com? The catalogue already shows them on a district address.
2. Public fields: credit lines naming donors ("Gift of Alan & Elizabeth Bell"), or the collection credit alone?
3. Scope:
   - Publish the Teaching Collection?
   - Leave out the 6 works on loan?
   - Publish the artists' Text Resources (press, exhibition lists)?
4. Artist names and life dates: review the sheet.
5. Where the masters are, and a contact at the district's IT for downloads and the DNS change.
6. Private records: where they live after the catalogue retires.

## Risks

- **Image rights:** needs the gallery's answer before anything is public.
- **Data quality:** the artist names need a real review. The mechanical clean-up gets most of the way, but not all.
- **Search depends on a script:** the no-JavaScript path through the browse and artist pages keeps every work reachable. The trial measures the index size.
- **Timing with the district:** the redirects depend on the district's IT. Until then, the catalogue keeps working as it does today.
