# Review: structured data (schema.org) in the new theme

Date: 2026-09-28. Decision: DS-154, **decided by Michael, 2026-09-28**, all five choices as built. Specification: `design-system/DESIGN.md` §9.7.

## What we found

The theme had structured data in one place: Shopify's `structured_data` filter on product pages, as Skeleton ships it. Every other page had none.

| Page | Before | Problem |
| --- | --- | --- |
| Home | None | Nothing names the gallery, its address, phone or opening hours for search engines or assistants |
| Exhibition | None | Dates, place, artists and the opening reception are on the page but not readable as an event |
| Events | None | Events have no page of their own, so nothing described them at all |
| Work in the collection (1,174) | None | Artist, year, medium and accession number are fields, but only shown as text |
| Artist (171) | None | No link between an artist, their works and their own website |
| Lesson (27) | None | The video isn't described, so it can't show as a video result |
| Limited edition | Shopify's filter | Named by the product title. Said "in stock" for a print that isn't on sale yet. Didn't name the artist |
| Any page with a crumb | None | The way back wasn't readable |

The page title, description, canonical address and link-preview tags in `snippets/meta-tags.liquid` were already sound. One note under "Still open".

## What this change does

Every page now describes itself as schema.org data (JSON-LD), built from the same fields the page shows. The table of pages and types is in `DESIGN.md` §9.7. No page looks different.

Three rules keep it honest:

1. The data says what the page says. An empty field is left out.
2. Nothing is guessed. A year like "ND" gives no date. Life dates become dates only when they are plain years.
3. Each thing has one name (`@id`), so an artist on a work's page and on their own page is the same artist.

## How it was checked

On the development theme `schema-seo` (184805556521), 2026-09-28:

- Every block on 20 pages parses as valid JSON: Home, Plan your visit, Contact, About us, Upcoming events, Explore + Create, Past exhibitions, two exhibitions, a work, an artist, a grouping, a lesson, a portfolio, a limited edition, the blog, search and cart.
- Values read back against the store: the address splits into street, city, province and postcode; the hours are Thursday to Saturday, 12:00 to 16:00; event times carry the Pacific offset; the two collectives in *Collect, Assemble, Gather* are organisations, not people.
- Theme Check: no offences. The theme linter: no errors, no warnings.

Not checked yet: Google's Rich Results Test and validator.schema.org. Both need a public address, so they run against the review theme's preview link after merge.

## Decisions

Michael approved all five as built, 2026-09-28 ("approve all five decisions as built"). The alternatives are kept for the record.

| # | Question | Decided, as built | Alternative, not taken |
| --- | --- | --- | --- |
| 1 | The gallery's type | `ArtGallery` | `ArtGallery` and `Museum` together, since it holds a permanent collection and is a public gallery |
| 2 | The gallery's name | "Gordon Smith Gallery", as the tab title (DS-121) | Add the full name, "Gordon Smith Gallery of Canadian Art", as a second name, if the gallery confirms it |
| 3 | An artist's own website as `sameAs` | Included. It tells a search engine which Robert Davidson this is | Leave it out. The page itself doesn't link out (DS-63), though this is data, not a link a visitor sees |
| 4 | Artists typed on an exhibition | Each a person; a name with "Collective" in it an organisation | Leave artists out of the data until exhibitions link to artist entries |
| 5 | A print not on sale yet | Out of stock, since it can't be ordered | Pre-order, only if the gallery takes orders ahead |

## Still open (needs facts from the gallery or the store)

| Item | Why | Owner |
| --- | --- | --- |
| Social links | Theme settings, Social links are empty, so the gallery has no `sameAs`. These links are how search engines tie the site to its Instagram and other accounts | Gallery |
| The gallery's email | Theme settings, Gallery details has none | Gallery |
| A logo file | The logos are drawn in the page (inline SVG). Search engines want a logo as an image file's address. Needs a PNG in Files and a setting | Michael |
| Artists for Kids and the Foundation as organisations | They are named, with no address, founding date or charity number. Those facts would make each one a full entry | Gallery |
| Wikipedia or Wikidata addresses | For the gallery and for Gordon Smith. The strongest signal for assistants about who is who | Michael |
| Returns and shipping on editions | Google's shopping results ask for a returns policy and shipping details. The values are in the store's policies, not in the theme | Michael |
| Map coordinates | The address is enough for most uses. Latitude and longitude would need two settings | Michael |
| Nationality or Nation | No artist has the field filled yet. When filled it should join the artist's data | Agent, after the gallery's review |
| Link previews | `og:image` has no width, height or alt text. Small gain | Agent |

## Not done, on purpose

- No FAQ, review or rating data: the site has none of that content.
- No search box data: Google retired that feature in 2024.
- Past events aren't described. Past exhibitions are, since each has its own page.
- Nothing in the store changed. This is theme code only.
