# Structured data: the kinds of page step 1 left out

Date: 2026-09-28. Decisions: DS-158 and DS-159, both **Proposed**. This adds to `proposals/aeo-geo-review.md`, whose step 1 built the gallery, exhibitions, events, works, artists and crumbs (DS-154, decided).

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

## For Michael

| # | Question | Built as | Alternative |
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

## A side effect to know about

Pushing to a named development theme made it the CLI's current development theme. Another session's `shopify theme dev` then synced its files into `schema-seo`, which is how this build's first test read stale pages. Later pushes here name the theme by its ID. Sessions that run `theme dev` may now be previewing on `schema-seo`: restart `theme dev` to give it its own theme again.
