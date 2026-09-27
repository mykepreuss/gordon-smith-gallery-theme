# The Permanent Collection on gordonsmithgallery.com

Status: **Built, 2026-09-27**, and on the review theme once the pull request merges. It goes live with the site (P-27). Decisions: P-26 (the menu), P-27 (the whole collection, now), P-28 (the works on loan too), DS-62 (the templates) and DS-63 (documents, no website links, exhibitions' works), all decided by Michael. What the gallery still has to check is in `proposals/gallery-questions.md` §5.

Michael, 2026-09-26: "I don't like that all of these assets are on an external site and would prefer them to be part of gordonsmithgallery.com." Then: "/pages/artists should not link out to the artist's website, it should link to their associated page like [the catalogue's artists page]. Moma does this as well." And: "The artists page should not be under the 'Shop' dropdown in the nav."

## What's on the site now

- **1,174 works**, the 6 "on loan" among them, each with its own page at `/pages/collection/<accession number>`: every image whole on the mat, the museum label (the artists link to their pages), medium, dimensions, edition, credit, accession number, the exhibitions that showed it, its category and themes as links, the edition in the Shop when there is one, and more by the artist.
- **171 artists**, each with a page at `/pages/artists/<name>`: names and dates, the works 24 to a page, their documents as text links, the editions in the Shop and the exhibitions at the gallery. No link to the artist's own website (DS-63).
- **The Artists page** is the index of every artist, A to Z, with dates and the number of works. Every name opens the artist's page on this site, as MoMA's does. The 59 links out to other sites are gone.
- **26 groupings** at `/pages/browse/<name>`: 8 categories, 13 themes, Indigenous artists, Artists for Kids Published Editions, the Teaching Collection, the Portfolio Collective's 2021 series, and Featured works.
- **The Permanent Collection page** is the front door: the gallery's introduction, a search that finds works by artist, title, year, medium, category or theme as you type, the groupings as cards, every category and theme with its count, and six featured works. Its Browse button opens the search instead of the catalogue.
- **The site's search page** shows the first six matching works from the collection, with a link to all of them.
- **The menu** has a Collection section, second after Exhibitions: The collection, Artists. Artists left the Shop and Permanent collection left About (P-26).
- **Editions** link their artist's name to the artist's page, and appear on it.
- **Exhibition pages** list their works from the collection after the installation views: *From the Ground* 26, *Playhouse* 25, *The Art of Conversation* 18 (DS-63).
- **1,420 images** and **180 document files** are in the store's Files. 79 documents are linked from artists' pages; the rest are the catalogue's small cover images of PDFs, which aren't linked (they can be deleted from Files).

Nothing shows on the live site: the live theme has no templates for these pages (`proposals/store-writes/README.md`, "Effect on the live site").

## How it's stored

Three entry types and one product field (content model part 7, `design-system/proposals/content-model.md`; fields in `proposals/store-writes/collection/definitions.py`):

| Type | Page | Holds |
| --- | --- | --- |
| Artist (`artist`) | `/pages/artists/<handle>` | Name, sort name, full name, other names, life dates, nationality or Nation, biography, portrait, website, exhibitions, documents, works |
| Artwork (`artwork`) | `/pages/collection/<handle>` | Title, artists, year, category, medium, dimensions, edition, accession number, credit line, images, themes, about the work, in the Shop, shown in |
| Collection grouping (`collection_group`) | `/pages/browse/<handle>` | Name, kind (category, theme, grouping), introduction, works |
| Product field `custom.artist_entries` | | The edition's artists |

Entries, not products: nothing leaks to the live site before release, the collection isn't for sale, and it's the model the exhibitions already use.

Liquid can't find entries by a field's value, so an artist's works and a grouping's works are lists on those entries. An edition names its artists once, on the product, and the artist's page finds it among All limited editions. Shopify's search doesn't cover entries, so the collection search reads the works in the browser from a data section, 250 a request; without the script, the browse and artist pages reach every work.

## Where the content came from

The catalogue at afkcatalogue.sd44.ca (Omeka S), read through its public API on 2026-09-26. It holds 1,291 records: 1,174 works (6 of them in "Things On Loan to AFK") and 117 documents (the artists' "Text Resources").

| Catalogue | On the site |
| --- | --- |
| Title | Title, with an edition number in brackets moved to Edition (481 titles) |
| Creator, with "(DOB: …)" | Artist, with life dates. 265 spellings became 171 artists: the site's own spelling first (Artists page, editions, exhibitions), then the catalogue's artist page, then the record |
| Date, Medium, Spatial Coverage, References, Rights | Year, Medium, Dimensions, Edition, Credit line, as written |
| Format | Category: Painting, Print, Drawing, Photograph, Sculpture, Ceramic, Textile, Book |
| Subject, and the curated theme sets | Themes, 15 of them |
| Description | The images' alt text, after "Artist, Title, year" |
| Identifier | Accession number and the page's address |
| The exhibition sets (*The Art of Conversation*, *Playhouse*, *From the Ground*) and the catalogue's "Works in …" pages | Shown in on the work, and Works from the collection on the exhibition |
| Indigenous, Published Editions (with its history paragraph), Teaching Collection, Portfolio Collective 2021 | Groupings |
| Text Resources | The artists' documents: one link per document, its PDF (20 MB and under), or its photographs when it has no PDF |
| Storage locations, provenance, old identifiers, donors | Not published |

The images are the catalogue's masters, converted once: JPEG, 3,000 px on the long side, sRGB, quality 85, never cropped. The masters stay on the catalogue.

## What changed from the plan

- **The whole collection now, not a 20-work trial first** (Michael: "I think we can do all the artists and everything").
- **No redirects, and the catalogue isn't retired by us.** Michael: "we won't change anything with DNS, that's outside of our scope." The catalogue keeps running as the district runs it; the site no longer links to it.
- **The image rights are given** (Michael: "We gave all the image rights").
- **Artists are those with work in the collection or an edition in the Shop.** Artists who appear only in an exhibition's list don't get pages; their names stay on the exhibition.
- **A work lists its artists** (a list, not one artist), for works made together, such as Lauren Brevner and James Harry's.
- **An edition names its artists on the product**, and the artist's page finds its editions, so an edition is linked once.
- **Featured works is a grouping** (`featured`) the gallery changes in the admin.
- **After Michael's review (DS-63):** documents are text links after the works, one per document; no website links; exhibitions list their works from the collection. The works on loan are imported too (P-28).

## Scripts

`proposals/store-writes/collection/`, run in this order. Each is safe to run again: entries are upserted by handle and files are keyed by the catalogue's media ID.

1. `inventory.py <folder>`: a fresh read-only export of the catalogue.
2. `clean.py <export> <data>`: the cleaned artists, works, groupings, images and documents, and the review sheets in `sheets/` (artists, titles, problems, themes, groupings).
3. `definitions.py`: the definitions (already created).
4. `images.py convert | upload | docs | alts | docalts`: the web copies, their upload to Files, the documents, and alt text updates.
5. `import.py artists | works | link | groups | exhibitions | products`: the entries, then the artists' Works and Documents lists, the groupings, the exhibitions' Works from the collection, and the editions' Artist pages field (through the connector).

To apply the gallery's corrections: edit the rules or names in `clean.py` (or the entries in the admin), run `clean.py`, then `import.py artists`, `works`, `link`, `groups` and `exhibitions`, and `images.py alts` if titles or descriptions changed.

## Who edits where

- **A new work:** Content, Metaobjects, Artwork, with its images in Files; then add it to its artist's Works list, to any grouping, and to an exhibition's Works from the collection, so it shows there.
- **A new artist:** one Artist entry; the Artists page picks it up.
- **A new edition in the Shop:** set its Artist pages field, and it shows on the artist's page.
- **Featured works:** the Collection grouping "Featured works".
- **Private records** (locations, provenance, donors) stay in the catalogue (gallery question 5.6).

## Still open

- The gallery's review of the sheets and names (§5 of the gallery questions): artists and dates, titles, themes, the names chosen for four artists, the featured works, and credit lines.
- 39 documents over 20 MB aren't on the site (Shopify's limit): listed with a note to address in `proposals/gallery-questions.md`, "Documents too large for the site".
- The featured works: the gallery chooses them (gallery questions 1.7).
- The works on loan: their credit lines and whether their pages should say so (5.13).
- A staff editing test that adds a work and an artist (plan, "Release backlog").
