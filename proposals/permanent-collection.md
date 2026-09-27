# The Permanent Collection on gordonsmithgallery.com

Status: the plan of 2026-09-26 (morning) is **Approved by Michael** ("Everything is approved"). **Revised 2026-09-26 (evening)** for the Artists page and the menu; the new parts are **Proposed** (P-26, DS-62) and need his approval. Parts that need the gallery are marked **Gallery**.

Michael, 2026-09-26: "I don't like that all of these assets are on an external site and would prefer them to be part of gordonsmithgallery.com... put together a plan to integrate all of the assets into our Shopify site rather than the external catalogue site."

Michael, 2026-09-26, on the revision: "we want to integrate all of this content because /pages/artists should not link out to the artist's website, it should link to their associated page like this page: afkcatalogue.sd44.ca/s/TheCollection/page/artists. MoMA does this as well... The artists page should not be under the 'Shop' dropdown in the nav."

## In short

- **Move the whole collection into the store as content entries.** That's every work, its images, its artist and its groupings. It follows the pattern the exhibitions already use (DS-14, P-10):
  - works at `/pages/collection/<work>`;
  - artists at `/pages/artists/<artist>`;
  - groupings such as Prints or Ecology at `/pages/browse/<grouping>`.
- **The Artists page becomes the index of every artist** (revised). One list for everyone with work in the collection or an edition in the Shop, about 208 names, A to Z. Each name opens the artist's page on this site, as MoMA's Artists page does: the works, the editions in the Shop, the exhibitions and the documents in one place. The artist's own website becomes one link on that page. Today's 59 links out to dealers and personal sites go.
- **Artists leaves the Shop menu** (revised, P-26). Recommended: a Collection section in the main menu, with The collection and Artists in it.
- **The Permanent Collection page becomes the front door.** It gets a search box, ways to browse, and the gallery's own introduction. Its "Browse" button stops sending people away.
- **Images come from the originals.** The catalogue's masters are TIFF files, 36 GB in all, which Shopify doesn't accept. They're converted once into large web images, and the masters stay where they are.
- **Nothing shows on the live site until release.** The entries are built and reviewed on the review theme, as the exhibitions were. At release, every old catalogue address forwards to its new page, and the catalogue can then be retired.

## What the catalogue holds

Read on 2026-09-26 through the catalogue's public API (Omeka S); `proposals/collection/inventory.py` repeats the counts, and they were the same in the evening.

| | Count | Notes |
| --- | --- | --- |
| Works | 1,291 | All public. Identifier (accession number) on every one, 4 used twice |
| Artists | 313 spellings | 204 names once dates typed into the name are removed. Some names have several spellings or different life dates |
| Images | 1,530 | 1,045 TIFF, 467 JPEG, 18 PNG. The catalogue's own web copies are only 800 px wide |
| Documents | 144 PDFs | Mostly "Text Resources": artists' press, exhibitions and photographs. 39 are over 20 MB |
| All files | 36.4 GB | 588 files over 20 MB; the largest is 346 MB |
| Groupings (item sets) | 101 | See below |
| Its own pages (site pages) | 81 | See "The catalogue's pages" |
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
- 16 artist sets ("… Artworks").
- 62 artist "Text Resources" sets.
- "Things On Loan to AFK": 6 works the collection doesn't own.

The catalogue shows storage locations and donor notes to anyone today. They stay behind in the move.

### The catalogue's pages

The catalogue also has 81 hand-built pages. Read through the API on 2026-09-26 (`/api/site_pages`). Each has a place on the site:

| Catalogue page | What it holds | On the site |
| --- | --- | --- |
| Home | One paragraph (the same one as the site's Permanent Collection page), a random work, and "Browse By" cards: Categories, Artists, Published Editions, Exhibitions, Sculptures, Paintings, Prints, Photography, Textiles, Ceramics, Indigenous Artists | The Permanent Collection page: the paragraph, the search, the ways in |
| Artists | "Artists in the Collection", a note that it is being updated, and 54 names linking to the artist pages below | The Artists page: the index of every artist |
| 58 artist pages | The name (sometimes the full name, "Gordon Appelbe Smith"), the artist's works, and "Text Resources" (PDFs of exhibitions, press and photographs). No biographies and no portraits | One artist page each. Every other artist gets one too, from the data |
| 15 category and theme pages | A list of works, no text | Browse pages |
| 4 exhibition pages and their "Works in …" pages | The Art of Conversation, Playhouse, From the Ground and Paths: an introduction, images, and the works from the collection in the show | The site already has those exhibitions as entries with their own text. Their "works in" lists become "Works in the collection" on the exhibition's page |
| Artists for Kids Published Editions | A paragraph on the history of the editions programme (1990, Bill Reid's first print), "Purchase Limited Editions Here", and the 103 collection copies | The Published Editions browse page, with the paragraph as its introduction if the gallery agrees (**Gallery**) |
| Exhibitions | Three season links (2023 to 2026) | Not needed: the site's exhibition pages |

## Artists (revised)

**Today.** The site's Artists page, under Shop in the menu, thanks the artists who have given work to the Limited Edition Portfolio and lists 59 names. Each name links out: to the artist's own site, a dealer's page, a PDF at the National Gallery. The catalogue has a separate Artists page with 54 names, each linking to a page in the catalogue. The two lists mostly overlap: 53 of the site's 59 names are in the catalogue, and the other six are four portfolio artists with no work in the collection (Lauren Brevner, Amelia Butcher, James Harry, Marlene Yuen) and two recorded under fuller names (B.C. Binning as Bertram Charles Binning, Atilla Lukacs as Attila Richard Lukacs, twice).

**The pattern.** MoMA's Artists page is "a list of artists with work in our collection or who have been included in a MoMA exhibition": every name, A to Z, with nationality, dates and the number of works, and each name opens the artist's page (works, exhibitions, publications). The catalogue's Artists page works the same way at a smaller scale. The site does the same:

- **One index for everyone**: every artist with a work in the collection, an edition in the Shop, or a place in an exhibition entry. About 208 names.
- **Names link to the artist's page on this site**, never out. The artist's own website is one link on that page, marked as external as every other outside link is.
- **The page is generated from the entries.** Staff never edit the list: adding an artist entry adds the name.

**The Artists page** (`/pages/artists`, template `page.artists`, DS-62):
- hero or page header, as now;
- the page's two paragraphs, word for word (they are about the portfolio artists; whether they should change is the gallery's call, question 5.8);
- the index: A to Z by surname, with letter links across the top (A, B, C…); each name with its life dates and "60 works", "2 editions in the Shop"; three columns from 990 px (the same columns as DS-45). Names come from the artist entries, sorted by their sort name.
- A search box that filters the list as you type, when the script runs. Without it, the whole list is on the page.

**The artist page** (`/pages/artists/<handle>`, template `metaobject/artist`):
- name as the H1, with the full name under it when it differs ("Gordon Appelbe Smith"), life dates, and nationality or Nation when the gallery has supplied it;
- [portrait and biography, when there are some; none today];
- **Works in the collection**: artwork tiles, 24 to a page, newest work last, each opening the work's page;
- **In the Shop**: the artist's editions as artwork tiles with prices, when there are any;
- **Exhibitions**: the exhibition entries that name the artist, as compact cards;
- **Documents**: the Text Resources PDFs, if the gallery wants them public (question 5.3);
- **Artist's website**: the link from today's Artists page, with the external cue (question 3.7 for the dead one).

**The names** (**Gallery**, question 5.4): the display name as the site uses it today ("Gordon Smith", "E.J. Hughes"), the full name as the catalogue records it, and a sort name (surname first). The clean-up sheet lists all three for every artist, with the spellings folded in.

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
| Shown in | list of exhibition entries | The four exhibition groupings and "works in" pages, linked to their exhibition pages |

**Artist** (`artist`, web pages at `/pages/artists/<handle>`)

| Field | Type | From |
| --- | --- | --- |
| Name | single line | The site's Artists page, else the catalogue's page title, else the Creator |
| Full name | single line | Creator, when it says more than the name |
| Sort name | single line | Surname first, for the index |
| Life dates | single line | The dates typed into Creator, e.g. "1919 to 2020" |
| Nationality or Nation | single line | Empty; the gallery may fill it |
| Biography | rich text | Empty for now |
| Portrait | file | Empty for now |
| Website | link | The link on today's Artists page |
| Works | list of artwork entries | Every work whose Creator is this artist, oldest first |
| Number of works | number | The count, so the index needn't read every list |
| Editions | list of products | The Shop's editions whose Artist label matches |
| Exhibitions | list of exhibition entries | The exhibition entries whose artists or collection artists name this artist |
| Documents | list of files | The Text Resources, if public |

The lists live on the artist entry because Liquid can't look up "every work whose artist is X": a loop reads at most 50 entries unless it paginates, and pagination has no filter. A list of entry references holds up to 1,024 items (Alistair Bell has 170 works), a list of products 128 (no artist has more than two editions). Both kinds can be paginated. Checked on shopify.dev, 2026-09-26.

Afterwards, a new work is one Artwork entry plus one line on its artist: adding the work to the artist's Works list. The staff editing test covers that; the import keeps the counts right for everything it imports.

**Browse grouping** (`collection_group`, web pages at `/pages/browse/<handle>`)
- Fields: name, kind (category, theme, grouping), introduction, works (a list of up to 1,024 works; Prints has 713).
- It carries the categories, themes, Indigenous artists, AFK Published Editions and the Teaching Collection, if the gallery wants it public.
- The artist sets become the artist pages. The donation sets become groupings only if the gallery wants donors named.

**One new product field:** `custom.artist_entry`, the artist entry for a limited edition. The museum label's artist name then links to the artist's page on product pages and tiles. Nineteen of the 21 editions match a catalogue artist by name; Marlene Yuen and Amelia Butcher get entries of their own.

**Exhibition entries don't change.** Their artists stay as typed names (P-11). The import matches those names to artist entries to fill each artist's Exhibitions list, and "Shown in" on the works from the catalogue's exhibition groupings.

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

- **Collection search.** The import publishes a small index to Files (title, artist, year, category, themes, one thumbnail), about 150 KB for 1,291 works. The search box on the Permanent Collection page filters it as you type, by words, artist, category, theme and decade; the Artists page's box filters the names the same way.
  - Without JavaScript, the browse and artist pages still reach every work, and the Artists page lists every name.
  - This follows DS-19: the site works first, and the script improves it.
- **Site search.** The site's search results page adds "In the collection" matches from the same index, under the store's own results.

### Limits checked (shopify.dev, 2026-09-26)

- **Entries:** up to 1,000,000 per type, and 40 fields each.
- **Reference lists:** up to 1,024 entry references; 128 for every other list type, products included.
- **Loops:** 50 items unless paginated. `paginate` works on a type's entries (`metaobjects.artist.values`) and on a list field, 1 to 250 a page, so the whole index fits on one page and an artist's works page by page. (Shopify now says `shop.metaobjects` is deprecated in favour of `metaobjects`; the exhibition code still uses the old form and can switch when the collection templates are built.)
- **Pages:** Liquid pages through entries up to 25,000.
- **Images:** JPEG, PNG, WEBP, HEIC or GIF, at most 20 MB and 4,472 × 4,472 px. TIFF isn't accepted.
- **Documents:** generic files are also capped. The 39 PDFs over 20 MB need compressing, or stay linked where they are.

## Pages and design (design system first)

Each new component goes into `design-system/` first, as for every page so far. **Five templates** join the closed set (§7.2 rule 1; DS-62, Proposed): `page.permanent-collection`, `page.artists`, `metaobject/artwork`, `metaobject/artist` and `metaobject/collection_group`. The two page templates carry the names of the pages' existing template suffixes (`permanent-collection`, `artists`), so the new theme picks them up on its own, as `page.shop` does, with nothing to reassign at release.

- **Permanent Collection (`/pages/permanent-collection`, `page.permanent-collection`):**
  - hero;
  - the gallery's introduction (kept word for word);
  - the collection search;
  - ways in, as cards: the categories and themes, Artists, Published Editions, Indigenous artists, the exhibitions;
  - a row of featured works;
  - a line with the count ("1,291 works by 204 artists"), from the data.
- **Artists (`/pages/artists`, `page.artists`):** hero or page header · the page text · the index, as above.
- **Work page (`metaobject/artwork`):** reuses the product page's artwork layout (DS-38) without price or cart.
  - Every image whole on the mat.
  - The museum label: artist (linking to the artist's page), title, year, medium, dimensions, edition, accession number and credit line.
  - "In the Shop" when the edition is for sale.
  - "Shown in" the exhibition.
  - "More by this artist" in a row of artwork tiles, and a link to the artist's page.
- **Artist page (`metaobject/artist`):** as above.
- **Browse page (`metaobject/collection_group`):** the grouping's name and introduction, then its works in artwork tiles, 24 to a page. Long lists read well with the search above them.
- **Links in from the rest of the site:**
  - exhibition pages ("Works in the collection", from the works' Shown in);
  - Shop products: the label's artist name, and "A copy is in the permanent collection";
  - the Artists for Kids history.

## The menu (P-26, Proposed)

Michael, 2026-09-26: "The artists page should not be under the 'Shop' dropdown in the nav."

Recommended: a **Collection** section, second in the menu after Exhibitions:

| Section | Items |
| --- | --- |
| Collection | The collection (`/pages/permanent-collection`), Artists (`/pages/artists`) |

Permanent collection leaves About, and Artists leaves Shop. Reasons: the collection becomes the site's largest part (1,291 works, about 208 artists), and the index belongs beside it, not with the shop. MoMA and the Vancouver Art Gallery both put the collection at the top level. The header has room: at 1200 px, where the bar starts, today's six sections take about 450 px of the width.

The alternative, Artists under About beside Permanent collection, adds no section but buries the site's largest part in the dropdown that also holds Volunteer.

During review the change is made to the review-only menu `new-theme-main` (a store write with Michael's go-ahead, logged in `proposals/store-writes/README.md`); at release the live menu follows (`proposals/store-changes.md` §1). The gallery approval doc in Cowork needs the same change, alongside the Newsletter removal (DS-56).

## Images

1. **Get the masters.** Either download them from the catalogue (36 GB; ask the district's IT first) or copy them from the gallery's own drive, if that's where they came from (**Gallery**).
2. **Convert.** Each image becomes a JPEG 3,000 px on its long side, in sRGB with its colour profile applied, at quality 85. That's about 1 to 3 MB each, 2 to 3 GB for all of them. The conversion checks colour mode (CMYK scans convert differently) and keeps the full artwork: no cropping.
3. **Upload** with the Admin API (`fileCreate`) from a staging location. Record each file's ID against its accession number, so re-running changes nothing.
4. **Alt text:** "Artist, Title, year" (§6.4), then the catalogue's visual description where there is one (480 works).

The masters stay archived where they are. The site only ever needs the web copies.

## Cleaning the data

The script does the mechanical work and writes review sheets. The gallery corrects the sheets before anything is imported (**Gallery**):

- **Artists:** one row per artist, with the display name, full name, sort name, spellings, suggested life dates, work count, editions, exhibitions and website.
  - 313 spellings become 204 names, plus the four portfolio artists who aren't in the catalogue.
  - Conflicts are marked, e.g. Ann Meredith Barry has four different life dates.
- **Categories:** capitals made consistent. "Printmaking" becomes Print.
- **Themes:** 30 terms. Near-duplicates are merged, e.g. "creature" and "creatures".
- **Titles:** editions moved out of 237 titles into the Edition field.
- **Problems listed:** the 4 duplicate accession numbers, 7 works without titles and 8 without images.
- **Public or private:** a list of every field, marked public or not publishing (locations, provenance, old identifiers).

## Importing

Scripts go in `proposals/store-writes/collection/`, following the same rules as every store write so far:

1. `inventory.py`: a fresh read-only export (in `proposals/collection/` today; it moves).
2. `clean.py`: builds the review sheets, then reads back the gallery's corrections.
3. `images.py`: converts and uploads the images, and records the file IDs.
4. `import.py`: dry run first, then upserts artists, then works, then groupings, keyed by accession number; fills each artist's lists and counts, the products' artist entries and the search index. A re-run updates in place.
5. `verify.py`: counts, missing images, and a sample of pages checked against the catalogue.
6. `redirects.py`: the map from every old address to its new page.

Every run is logged in `proposals/store-writes/README.md`, with Michael's go-ahead and a before-snapshot. All of it is the allowed kind of write before release: new definitions, new files, new entries that 404 under the live theme, and field values the live theme doesn't read (the product's artist entry; the Artists page's staged text, which drops its list of links once the index replaces it).

## Redirects and retiring the catalogue

- **At release:** the Permanent Collection page's "Browse" button points to the collection search on the page itself.
- **Every old address gets a new one:**
  - item pages (`/s/TheCollection/item/<id>`) go to their work;
  - the 58 artist pages (`/s/TheCollection/page/<slug>`) go to their artist page;
  - the category and theme pages go to their browse page; the Published Editions page to its browse page;
  - the exhibition and "works in" pages go to the exhibition's page on the site;
  - the Artists page goes to `/pages/artists`, the home page to `/pages/permanent-collection`.
- **Recommended way to forward:** once the gallery stops editing in the catalogue, point `afkcatalogue.sd44.ca` at Shopify as an extra domain. Shopify then forwards every old address with its own URL redirects from the map. It needs one DNS change by the school district's IT (**Gallery**).
- **Fallback:** the district keeps the catalogue server and adds forwarding rules from the same map.
- Keep the catalogue read-only for a few months after release, then retire it. The masters stay archived.

## Who edits where, afterwards

- **New acquisitions:** added in the Shopify admin (Content, Metaobjects, Artwork), with images in Files, then added to the artist's Works list. A new artist is one Artist entry, and the index picks it up. A staff editing test covers both.
- **Private records (Gallery):** the catalogue also holds records the public shouldn't see: where each work is, provenance and donors. The gallery decides where those live after the catalogue retires:
  - a collections management tool or spreadsheet the gallery already keeps; or
  - an admin-only "Artwork record" entry in the store, which the site can't read.

## Order of work

| Step | What | Who | About |
| --- | --- | --- | --- |
| 0 | Decisions below | Michael, gallery | |
| 1 | Trial with 20 works end to end: the three definitions and the product field, images, the five templates with two artists' pages and the index, the search index, one redirect. Proves the URLs, the index size, the sorting and the image quality before the rest | Agent | 2 to 3 days |
| 2 | Design passes: Permanent Collection page, Artists index, artist, work, browse and search, in the design system first | Agent, Michael approves | 3 to 4 days |
| 3 | Data clean-up sheets; the gallery reviews artists, categories and public fields | Agent, gallery | Depends on the gallery |
| 4 | Image conversion and upload | Agent | 1 to 2 days, mostly waiting |
| 5 | Full import, verification report, review on the review theme, staff editing test | Agent, staff | 2 days |
| 6 | The review menu: Artists out of Shop, the Collection section (P-26) | Agent, with Michael's go-ahead | An hour |
| 7 | At release, or right after it: the Browse button, the redirects, the live menu, the catalogue read-only | Agent, district IT | |

It doesn't need to hold up the site's release. The collection is additive, so it can go live with the release or in a second release soon after.

## Decisions needed

**Michael**
1. ~~Entries, as recommended, rather than products.~~ Approved 2026-09-26.
2. ~~The addresses: `/pages/collection/`, `/pages/artists/`, `/pages/browse/`.~~ Approved 2026-09-26.
3. Whether the collection goes live with the site or after it.
4. **P-26:** the Collection section in the menu (The collection, Artists), or Artists under About.
5. **DS-62:** the five templates and the Artists index as described.
6. Go-ahead for the trial (step 1): three definitions and one product field, 20 works and their artists in the store, invisible to the live site.

**Gallery** (`proposals/gallery-questions.md` §5)
1. Licences: do the image permissions (CARFAC or artists' agreements) cover showing the works on gordonsmithgallery.com? The catalogue already shows them on a district address.
2. Public fields: credit lines naming donors ("Gift of Alan & Elizabeth Bell"), or the collection credit alone?
3. Scope:
   - Publish the Teaching Collection?
   - Leave out the 6 works on loan?
   - Publish the artists' Text Resources (press, exhibition lists)?
4. Artist names, life dates and websites: review the sheet.
5. Where the masters are, and a contact at the district's IT for downloads and the DNS change.
6. Private records: where they live after the catalogue retires.
7. The Artists page's two paragraphs, once the whole collection is listed under them.
8. The Published Editions history paragraph: carry it over as that browse page's introduction?

## Risks

- **Image rights:** needs the gallery's answer before anything is public.
- **Data quality:** the artist names need a real review. The mechanical clean-up gets most of the way, but not all.
- **Search depends on a script:** the no-JavaScript path through the browse, artist and index pages keeps every work and name reachable. The trial measures the index size.
- **Sorting in Liquid:** the index sorts entries by their sort name in Liquid. If sorting a paginated list proves unreliable, the import creates the entries in order and re-sorts by handle; the trial settles it.
- **Timing with the district:** the redirects depend on the district's IT. Until then, the catalogue keeps working as it does today.
