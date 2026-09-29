# Structured data: the kinds of page step 1 left out

Date: 2026-09-28. Decisions: DS-158 and DS-159, both **decided by Michael, 2026-09-28** ("approve DS-158 and DS-159 as built"). This adds to `proposals/aeo-geo-review.md`, whose step 1 built the gallery, exhibitions, events, works, artists and crumbs (DS-154, decided).

## How this came about

This branch began as a separate review of the theme's structured data. While it was being built, the review in `aeo-geo-review.md` merged to `main` and covered the same ground. Michael chose to keep `main`'s version and add only what it lacks (2026-09-28: "rework as you recommend"). The first build's snippets (`gs-schema-*`) were removed. Its five decisions, approved for that build, are replaced by DS-154 as decided on `main`, except the one noted under DS-159.

## What this adds

| Page | Data | Snippet | Decision |
| --- | --- | --- | --- |
| Lesson (27) | LearningResource with grade levels and date, and its video as a VideoObject | `gs-data-lesson` | DS-158 |
| Grouping (26) | CollectionPage: name, introduction, the collection it belongs to | `gs-data-list` | DS-158 |
| Portfolio | CollectionPage that names the editions on the page by their labels; the crumb | `gs-data-list`, `gs-data` | DS-158 |
| Page | WebPage, or ContactPage, with its description, picture and organisation | `gs-data-page` | DS-158 |
| Article | BlogPosting | `gs-data-page` | DS-158 |
| Limited edition | Product and VisualArtwork, in place of Shopify's filter | `gs-data-product` | DS-159 |

All follow DS-154's rule: the data repeats what the page shows and adds nothing. No page looks different.

## DS-159: why replace Shopify's product data

`aeo-geo-review.md` kept Shopify's filter and noted its faults. The theme's own data fixes three:

| Fault in Shopify's data | The theme's own |
| --- | --- |
| Names the edition in Unicode italic letters until the titles change at release (L-03). The check reported an error on every edition page | Named by the label in plain letters, "Artist, Title, year" (DS-156). The error is gone |
| Says a print not on sale yet is in stock | Out of stock when `custom.coming_soon` is on, as when sold out. Michael approved this wording on 2026-09-28 for the first build |
| Names the store as the brand and no artist | The artist, linked to the artist's page in the collection |

What it costs: Shopify keeps its own filter up to date with what Google's shopping results ask for. The theme's own is ours to keep up. To go back, put the filter's three lines back in `meta-tags.liquid` and remove the render of `gs-data-product` from `gs-data.liquid`.

## How it was checked

On the development theme `schema-seo` (184805556521), 2026-09-28, with `check_structured_data.py` on 20 saved pages:

- 20 pages, 0 errors: Home, Plan your visit, Contact, About us, Artists for Kids, FAQ, Upcoming events, Explore + Create, two exhibitions, a work, an artist, a grouping, two lessons, two portfolios and three editions.
- The three edition pages had one or more errors each on `main`. They have none now.
- Theme Check: no offences. The theme linter: no errors, no warnings. The check's tests: 13 pass (2 new).

The pages were saved with a preview cookie and checked with `--file`, since the check's own fetch gets the live theme for a development theme's link.

Not checked yet: Google's Rich Results Test and validator.schema.org. Paste a block from the page source into either.

## Decided

Michael approved all three as built, 2026-09-28. The alternatives are kept for the record.

| # | Question | Decided, as built | Alternative, not taken |
| --- | --- | --- | --- |
| 1 | DS-158: more kinds of page | As the table above | Leave any kind out |
| 2 | DS-159: the editions' own data | Replaces Shopify's | Keep Shopify's and wait for the titles to change at release |
| 3 | A page's organisation | From its programme field: Gallery, Artists for Kids or the Foundation, by name | The gallery on every page |

## Still open

These are in `aeo-geo-review.md` too, steps 2 to 4:

| Item | Why | Owner |
| --- | --- | --- |
| Social links and email | Theme settings has neither, so the gallery has no `sameAs` | Gallery |
| A logo file | The logos are drawn in the page. Search engines want an image's address | Michael |
| Returns and shipping on editions | Google's shopping results ask for both. The values are in the store's policies | Michael |
| An artist's own website as `sameAs` | The first build included it. `main`'s artist data doesn't. The field is filled for many artists | Michael |
| Exhibition videos | An exhibition's Videos and publications (DS-138) have no date or picture, which a video needs | Agent, if fields are added |

## The graph (DS-163 to DS-165, decided by Michael, 2026-09-28)

Michael, 2026-09-28: "I have a feeling we can do much better with the schema.org implementation and we're not close to done yet." He was right. The data was valid, and that was all.

### What an audit found

Read from 27 pages of the build before this one, against schema.org's vocabulary and Google's field lists:

| Finding | Measure |
| --- | --- |
| Separate notes, not a graph | 82 of 326 things had a name for machines (`@id`). An artist on a work's page and on their own page were two unrelated things |
| No page said what it is about | No `mainEntity` on any entry page |
| An exhibition's artists were plain things | 19 names on *Collect, Assemble, Gather*, none tied to the 171 artist pages |
| List pages said nothing | Artists, On now, Upcoming, Past exhibitions, Permanent Collection, ArtReach videos and Shop were bare pages |
| Three organisations, one described | Artists for Kids and the Foundation were a name |
| Every artist entry was a person | Three are groups: T&T Collective, Vancouver School Collective, West Baffin Eskimo Co-operative |
| Fields Google recommends | Events: no status, no registration link. Gallery: no logo, no map position |

### What changed

| Thing | Before | Now |
| --- | --- | --- |
| Names for machines | 82 of 326 | 629 of 1,103 on 33 pages. The rest are parts that need none (an address, an offer, a list row) |
| Entry pages | The thing alone | The thing, the page that is about it, and the crumb, each naming the others |
| Exhibition | Dates, place, summary, one picture, names | Also: status, its organisation, installation views, works from the collection, reception, events, and artists as the collection's own where names match (13 of 19) |
| Work | Label and facts | Also: every picture with its size, themes, the exhibitions that showed it, its edition in the Shop |
| Artist | A person | A person or a group, on a profile page, with their exhibitions and own website |
| List pages | Bare | Artists (171), exhibitions by status, lessons (27), portfolios |
| Organisations | The gallery | Also Artists for Kids and the Foundation, each with its page and logo |
| Gallery | Address, hours, phone | Also logo, map position, directions, description |
| Event | Separate copies in each list | One event by name, with status, organisation and registration link |
| Edition with options | One product | A group of products, one for each option |

### The check

`check_structured_data.py` now fails on a type or property schema.org doesn't have, on a property used on a type it isn't for, and on a mention of something the page doesn't describe. It warns about fields Google recommends. On 35 pages of the development theme: 0 errors, 18 warnings, all of them facts the store doesn't hold (an event without a summary or an end time, the gallery without social links).

The vocabulary check caught one real fault while this was built: an edition with options carried artwork fields on a type that doesn't take them.

### Decisions for Michael

Michael, 2026-09-28: "DS-163 to DS-165 approved, merge #92". Choices 1 to 4 stand as built. Choice 5 has no decision number and stays as built, one person, until he or the gallery says otherwise.

| # | Decision | Built as | Alternative |
| --- | --- | --- | --- |
| 1 | DS-163: one graph | As above | Any part can be left out |
| 2 | DS-163: an artist's own website as `sameAs` | Included. Gordon Smith's is his estate's page at Equinox Gallery | Leave out. #85's rework had dropped it |
| 3 | DS-164: groups | Three names in Theme settings | A field on the artist entry (a store write) |
| 4 | DS-165: an event's room | Inside the gallery, with its address | The name alone, as DS-154 had it. Google then reads no place for those events |
| 5 | Pat and Rosemarie Keough | One person, as before | Two artist entries, or a group |

### What would make it better still, and needs facts

Many of these were found on 2026-09-28: `proposals/structured-data-facts.md`.

| Item | Why it matters | Needs |
| --- | --- | --- |
| Wikidata and Getty (ULAN) addresses for artists | The strongest way to say which Gordon Smith. Assistants lean on these | A field on the artist entry, and the addresses |
| The gallery's social profiles and a Wikipedia or Wikidata entry | Ties the site to the gallery's other presences | The gallery |
| How the three organisations are related | The data names each and doesn't say which is part of which | The gallery. The brand guide calls the Gallery the umbrella identity, which is about logos |
| The organisations' kinds | The Foundation is likely a charity (NGO), Artists for Kids an education programme. Built as plain organisations | The gallery |
| Admission | "By donation" is text. Engines want free or a price | Michael |
| Returns and shipping on editions | Google's shopping results ask for both | Michael, from the store's policies |
| An event's price | Registration links have no price, so an offer has an address only | The event entry, if wanted |
| A work's height and width as numbers | The size is text, and the order of its sides isn't recorded | The gallery |
| Copyright and licence for images of works | Google's image results show a licence when given | The gallery |
| Curators as people | The curator credit is one line of text | A field, if wanted |
| Accessibility of the building | Engines answer "is it wheelchair accessible" from data | The gallery |
| An exhibition's videos | A video needs a date and a picture. The links have neither | Fields, if wanted |

## Google's Rich Results Test (DS-173, Proposed)

Run on 2026-09-28, at Michael's request, on the review theme's pages. The test can't open a preview link, which needs a cookie, so each page's structured data was pasted in as code.

### First run, on what was in `main`

| Page | Result | Fault |
| --- | --- | --- |
| Edition | Valid: Product snippets, Merchant listings, Breadcrumbs | None |
| Lesson | Valid: Videos, Breadcrumbs | The video's date had no time zone |
| Artist | Breadcrumbs only | **No Profile page.** The person was a separate block the page pointed to |
| Exhibition | Its workshop only | **The exhibition wasn't read as an event** |

### What the exhibition's fault was

Found by changing one thing at a time, 11 runs:

| Tried | Read as an event |
| --- | --- |
| The exhibition alone, as built | No |
| Both types together | No |
| A plain place; a picture as an address; times on its dates; a start in the future; a short run; no organiser; no artists | No, each time |
| The workshop that passed, retyped as ExhibitionEvent | No |
| The exhibition typed Event, with ExhibitionEvent as its further type | **Yes** |

So Google's test reads no ExhibitionEvent as an event, whatever it holds. Two more faults showed only once that was fixed:

- With its workshop on the page, the exhibition was dropped again. The workshop mentioned it as an ExhibitionEvent, so one thing had two types. Naming it by its name for machines alone fixed it.
- The artist's page passed with the person inside it, then failed again in full. The person pointed back at the page. Without that, it passed.

### Last run, on the fixes

| Page | Result | Notes left |
| --- | --- | --- |
| Home | Local business, Organization | Price range (optional) |
| Exhibition with its workshop | 2 events | Exhibition: 2 optional. Workshop: performer, and the price, currency, availability and start of its registration offer (all optional) |
| Artist | Profile page, Breadcrumbs | None |
| Lesson | Videos, Breadcrumbs | None |
| Edition | Product snippets, Merchant listings, Breadcrumbs | Reviews and ratings; a global identifier such as a brand; the carrier's delivery time (all optional) |
| Edition with options | The same | The same |
| On now | Carousel | One optional |
| FAQ | Not shown as a result | Google shows FAQ results for government and health sites only. The data is still read |

No page has an invalid item. Every note left is optional and is a fact the store doesn't hold.

### What the check now knows

`check_structured_data.py` fails on the two faults the test found that it could have caught: one thing with two types on a page, and a thing that points back at the page that is about it. 21 tests. On 34 pages of the development theme: 0 errors.

### For Michael

| # | Decision | Built as | Alternative |
| --- | --- | --- | --- |
| 1 | DS-173: an exhibition's type | Event, with ExhibitionEvent as its further type | ExhibitionEvent, as DS-154 had it. More exact, and Google reads no event |
| 2 | DS-173: the gallery where it is only mentioned | Organization | ArtGallery everywhere. Google then notes four missing fields on every page |

### Found in passing

The FAQ answers "How much is shipping?" with "calculated and confirmed at checkout". The shipping policy and the structured data say $20. Gallery question 11.11.

## A side effect to know about

Pushing to a named development theme made it the CLI's current development theme. Another session's `shopify theme dev` then synced its files into `schema-seo`, which is how this build's first test read stale pages. Later pushes here name the theme by its ID. Sessions that run `theme dev` may now be previewing on `schema-seo`: restart `theme dev` to give it its own theme again.
