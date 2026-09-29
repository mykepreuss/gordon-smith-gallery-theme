# Review for answer engines and generative engines

Status: **Step 1 built and decided by Michael, 2026-09-28. Steps 2 to 4 built 2026-09-28, for his review** (see "Built in steps 2 to 4"). Step 1: (DS-154 to DS-157; see "Built in step 1"). Michael, 2026-09-28: "Yes, start on step 1", then "DS-154 to DS-157 approved, merge the PR". Nothing in the store changed. Steps 2 to 4 wait for his go-ahead and the gallery's words.

## What this review asks

Answer engines (Google's AI answers, Bing Copilot, Perplexity, ChatGPT search, Claude) read a page, pick out facts and quote them. Two things decide whether they quote the gallery and get it right:

1. **Can a machine read the fact without guessing?** Plain HTML, clear headings, labelled data, structured data.
2. **Is the fact stated once, clearly, near the top?** Who, what, where, when, how much.

## How it was done

- Crawled the preview (`mifbwun5bb211saq-89595805993.shopifypreview.com`) three links deep from the home page: 400 pages, all answered 200. That is 171 artist pages, 125 work pages, 41 pages, 25 browse pages, 21 products, 6 collections and 4 exhibitions, of about 1,500 on the site.
- For each page, read the title, description, canonical address, link-preview tags, structured data, heading outline, word count, image alt text, and the `time`, `address` and `dl` elements.
- Read `theme/snippets/meta-tags.liquid`, `theme/layout/theme.liquid` and the entry sections.
- Read the live site's `robots.txt` and sitemaps for comparison.

Two things on the preview are the preview's own and not the theme's: its `robots.txt` blocks everything and every page carries `noindex,nofollow`. Shopify adds both to every preview address. The live `robots.txt` allows all crawlers, AI crawlers included.

## Summary

The foundation is strong. The content is in the HTML the server sends, the markup is semantic, and the entry pages carry real facts. The gaps are in what sits on top:

| | Finding | Size of gain | Who |
| --- | --- | --- | --- |
| 1 | Only products carry structured data. The gallery, exhibitions, events, works and artists carry none | High | Theme |
| 2 | The site never says in one sentence what the gallery is, and uses three names for it | High | Theme and gallery |
| 3 | Half the pages have no description, and their link preview shows the Shop's description | High | Theme and store |
| 4 | A work's page title leaves out the artist and year | Medium | Theme |
| 5 | 21 product titles are written in Unicode italic letters | High | Store |
| 6 | Most artist pages are very thin | Medium | Theme and gallery |
| 7 | An exhibition's artists are not linked to their pages | Medium | Theme |
| 8 | The FAQ covers the Shop only, and skips a heading level | Medium | Gallery and theme |
| 9 | The live sitemap lists about 1,200 pages the live theme answers with 404 | Note | Resolves at release |
| 10 | Smaller items | Low | Mixed |

## What already works

Keep these as they are.

- **Content is server-rendered.** No page needs JavaScript to show its text. Crawlers that don't run scripts (most AI crawlers) see everything. The opening hours line prints "Open Thursday to Saturday, 12 to 4 PM" in the HTML, and the script only improves it.
- **One `h1` on every page.** 400 of 400.
- **Dates are machine-readable.** Events use `<time datetime="2026-10-23T09:00:00-07:00">` with the time zone offset.
- **Facts are labelled.** Work pages use a `dl` for medium, edition, dimensions, credit and accession number. Exhibition pages do the same for curator, artists and events. Titles of works use `cite`. The address uses `address`.
- **Work images have good alt text.** "Alistair Bell, Boats At Steveston, 1985", often with a visual description after it.
- **Every page has a canonical address, and every entry page has its own preview image.**
- **Lists page with real links.** The browse pages link to pages 2, 3 and so on, so a crawler reaches all 210 abstract works.
- **The live sitemap includes the entry pages:** 1,174 works, 171 artists, 32 exhibitions, 27 lessons, 26 groupings.
- **Plain-text visit information** on Plan your visit: transit, parking, accessibility, admission. This is the kind of text answer engines quote.

## Findings and recommendations

### 1. Structured data (high)

`meta-tags.liquid` prints Shopify's `Product` data on product pages. No other page has any. Structured data is the clearest way to tell an engine "this is an art gallery at this address, open these hours, showing this exhibition until this date".

Recommended, in order of value:

| | Where | Type | From |
| --- | --- | --- | --- |
| 1a | Every page, or the home page | `ArtGallery` (a kind of `LocalBusiness`) with name, other names, address, telephone, opening hours, admission, logo, `sameAs` links | The footer's and the visit section's settings |
| 1b | Home page | `WebSite` with the site's name and its search address | Fixed |
| 1c | Exhibition pages | `ExhibitionEvent` with name, start and end dates, location, image, description, the curator and artists | The exhibition entry |
| 1d | Events | `Event` with name, start and end time, location, the registration link, and its exhibition or programme | The event entry |
| 1e | Work pages | `VisualArtwork` with name, creator, date, medium, edition, size, image, accession number, credit | The artwork entry |
| 1f | Artist pages | `Person` with name, birth and death dates, nationality | The artist entry |
| 1g | Work, artist, exhibition and product pages | `BreadcrumbList` | The crumb the page already shows |
| 1h | FAQ page | `FAQPage` | Needs questions as fields or blocks, not free text |
| 1i | Lessons and articles | `LearningResource` and `Article` | The entry |

Notes:

- One snippet for each type, rendered from `meta-tags.liquid`, keeps it in one place. Build values with the `json` filter so quotes in titles can't break the data.
- The theme check and linter don't validate structured data. A new check in `design-system/scripts/` should parse every block on a sample of pages.
- `sameAs` needs the gallery's profiles (Instagram, Facebook, and a Wikipedia or Wikidata entry if there is one). The footer shows no social links today. A question for the gallery.
- Artist `sameAs` links (Wikidata, Union List of Artist Names) would help engines match "Gordon Smith" the painter and not another Gordon Smith. This needs a new field on the artist entry, so it is a later step.

### 2. Say what the gallery is, with one name (high)

An engine asked "what is the Gordon Smith Gallery?" looks for a sentence to quote. The home page has none. Its outline is the name, the current exhibition, What's on, then the Shop. Its description is about the Shop only: "Shop limited-edition Canadian art works that directly fund...".

The name also varies:

| Where | Name |
| --- | --- |
| Page titles, home `h1` | Gordon Smith Gallery |
| `og:site_name`, footer copyright, policies | Artists for Kids & The Gordon Smith Gallery |
| About page heading | The Gordon Smith Gallery of Canadian Art |
| Visit page text | The Gordon Smith Gallery and Artists For Kids |

Recommended:

- 2a. A home page description that answers who, what and where. For example: what the gallery is, that it is in North Vancouver at 2121 Lonsdale Avenue, that it is open Thursday to Saturday and admission is by donation, and that it is home to Artists for Kids. The words are the gallery's to approve.
- 2b. One short "about" sentence on the home page near the Visit section, with a link to About. The words are the gallery's.
- 2c. `og:site_name` follows the programme's name as the title does (DS-121), so previews and titles agree.
- 2d. The structured data in 1a names the full name and lists the others as `alternateName`, so engines treat them as one place.

### 3. Descriptions (high)

| Group | Pages with no description |
| --- | --- |
| Pages | 20 of 41 |
| Browse pages | 24 of 25 |
| Collections | 0 of 6 |
| Artists, works, exhibitions, products | 0 |

Three problems:

- **The wrong fallback.** A page with no description prints none, which is right. But its `og:description` falls back to the store's, so a link to Classes and camps previews as "Shop limited-edition Canadian art works...". 44 sampled pages do this.
- **Run-together text.** Where the store has no description, Shopify makes one from the page's text and drops the line breaks: "2121 Lonsdale AvenueNorth Vancouver", "GORDON SMITHPENDER HARBOUR, 2006 Limited EditionAvailability". These come from the store, not the theme.
- **Duplicates.** On now and Upcoming events both start with the same exhibition text.

Recommended:

- 3a. Theme: when a page has no description, `og:description` uses the page's deck or the start of its text, never the store's. A browse page describes itself from its count and name ("210 abstract works in the permanent collection of ...").
- 3b. Theme: an exhibition's description starts with its dates, since "when is it on" is the first question. "September 25, 2026 to February 20, 2027. Collect, Assemble, Gather explores..."
- 3c. Store: a written description for each of the 41 pages and 21 products, 150 characters or so, facts first. A store write, so it needs Michael's go-ahead and the gallery's words. It also improves the live site.

### 4. Work page titles (medium)

A work's title tag is its title alone: "Boats At Steveston | Gordon Smith Gallery". The `h1` and description already say "Alistair Bell, Boats At Steveston, 1985". Titles like "Untitled" and "Cockatoos" repeat across works, and five sampled titles are duplicates.

- 4a. The title tag for a work follows its label: "Alistair Bell, Boats At Steveston, 1985 | Gordon Smith Gallery". The same for `og:title`.

### 5. Product titles in Unicode italics (high, store)

All 21 product titles write the work's title in mathematical italic letters: "Gordon Smith, 𝘗𝘦𝘯𝘥𝘦𝘳 𝘏𝘢𝘳𝘣𝘰𝘶𝘳, 2006". These are not letters to a machine. A search for "Pender Harbour" won't match them, screen readers skip or spell them out, and the title tag, `og:title` and the `Product` data all carry them. The page's `h1` is fine because the theme builds it from fields.

The design review already listed this for alt text (`site-design-review.md`, "needs an early go-ahead"). The titles matter more.

- 5a. Store: plain letters in the 21 titles. Already planned for release (L-03, `proposals/store-changes.md`); the question is only whether to do it sooner. The theme already sets the work's title in italics with `cite`. This changes the live site, for the better, so it needs Michael's go-ahead and a before-snapshot.
- 5b. Until then, theme: the title tag and `og:title` for a product use the same fields the `h1` does.
- 5c. The `Product` data names the store as the brand. Shopify writes that block, so adding the artist means a second `VisualArtwork` block on the product page (1e) and not a change to Shopify's.

### 6. Artist pages (medium)

| | Artist pages, of 171 |
| --- | --- |
| Under 80 words | 125 |
| Over 150 words | 22 |
| Description is the name and nothing else | 96 |

Gordon Smith's own page has no biography. It links to Gordon and Marion, where the biography is.

- 6a. Theme: an artist's description always adds what the gallery holds: "A.Y. Jackson, 1882 to 1974. 2 works in the permanent collection of the Gordon Smith Gallery." Every page then says something true and different.
- 6b. Gallery: short biographies for the artists most asked about, starting with the founders (Gordon Smith, Jack Shadbolt, Bill Reid). Two or three sentences each is enough.
- 6c. Gordon Smith's page carries a short biography of its own, and keeps the link to the longer one.

### 7. Link an exhibition's artists (medium)

The exhibition page lists 19 artists as plain text. None link to an artist page, though most have one. Links tell engines which Stan Douglas is meant and pass readers on.

- 7a. Where an exhibition's artist matches an artist entry, the name links to it. If the field is free text, match by name, or add a list of artist entries to the exhibition (a change to the content model).

### 8. The FAQ (medium)

The page has eight questions, all about the Shop. Its questions are `h3` straight under the `h1`.

- 8a. Theme: questions as `h2`, or under `h2` groups ("Visiting", "Buying prints").
- 8b. Gallery: add the questions people ask engines. When is the gallery open? How much is admission? Where do I park? Is it wheelchair accessible? Who was Gordon Smith? What is Artists for Kids? How do I register for a class? Each answer starts with the fact. The answers exist on other pages already, so this repeats them in question form.
- 8c. With 1h, the page then carries `FAQPage` data.

### 9. The live sitemap lists pages that answer 404 (note)

The live sitemap lists the entry pages, but the live theme has no template for works or exhibitions:

| Live address | Answer |
| --- | --- |
| `/pages/collection/bell-aa001` | 404 |
| `/pages/exhibitions/collect-assemble-gather` | 404 |
| `/pages/artists/gordon-smith` | 200 |

So crawlers are being sent to about 1,200 addresses that fail. It ends at release. If release stays on hold for weeks, engines may learn to distrust these addresses and come back to them slowly. This is a reason to weigh in the release timing, not a change to make now.

### 10. Smaller items (low)

- 10a. **Hero and installation images have empty alt text** (38 on the 4 exhibition pages). The design system says alt text comes from Files, so this is content: the gallery's words, already in `gallery-questions.md`.
- 10b. **Gordon and Marion** is 393 words under one `h1` with no subheadings. Two or three `h2`s ("Gordon Smith", "Marion Smith", "The foundation") make it quotable in parts.
- 10c. **Event cards show no place or price.** "Free, at the gallery" or similar on the event page answers the next question. With 1d this goes in the data too.
- 10d. **Preview image tags** have no `og:image:alt`, width or height. The alt text is on the file already.
- 10e. **`llms.txt` and `agents.md`** are written by Shopify and describe the site as a shop only: products, cart, checkout. They say nothing about exhibitions, visiting or the collection. Check whether Shopify lets a store add to them. If it does, add a short description of the gallery and links to Visit, Exhibitions, Collection and Programs. If not, leave them.
- 10f. **No dates on pages.** A visible "Updated" date on Plan your visit and the FAQ helps engines trust the hours. Optional.
- 10g. **Collection pages** in the sample included `.atom` feeds with no canonical address. These are Shopify's and need nothing.

## Suggested order

1. Theme only, no store writes, no new words: 1a to 1g, 2c, 3a, 3b, 4a, 5b, 6a, 8a, 10d. One branch, one pull request, with a check that parses the structured data.
2. Store writes that improve the live site now, with Michael's go-ahead: 5a, then 3c.
3. Words from the gallery: 2a, 2b, 6b, 6c, 8b, 10a, the `sameAs` links.
4. Content model changes: 7a (if by entry list), 1h, artist `sameAs`.

## Built in step 1

Theme only. No store writes and no new words on any page.

| Recommendation | What was built | Decision |
| --- | --- | --- |
| 1a, 1b | The gallery on Home, Plan your visit and Contact, and the site with its search on Home (`gs-data`, `gs-data-place`) | DS-154 |
| 1c | An exhibition's dates, place, summary, picture and artists | DS-154 |
| 1d | Each event, printed with its row or card (`gs-data-event`). Past events print none | DS-154 |
| 1e, 1f | A work and an artist | DS-154 |
| 1g | The crumb on work, artist, grouping, exhibition, lesson and edition pages | DS-154 |
| 2c | The link preview names the programme, as the title does | DS-155 |
| 3a | A page without a description uses its intro or the start of its text. Only the home page uses the store's | DS-155 |
| 3b | An exhibition's description starts with its dates | DS-155 |
| 6a | An artist without a biography, and a grouping without an introduction, say how many works the collection holds | DS-155 |
| 10d | The preview picture's width, height and alt text | DS-155 |
| 4a, 5b | A work's and an edition's title is "Artist, Title, year" in plain letters | DS-156 |
| 8a | The FAQ's questions are H2, and look the same | DS-157 |
| Check | `design-system/scripts/check_structured_data.py`, with 11 tests | DS-154 |

Two sentences are new and are for the gallery to approve. They show in descriptions only, never on a page: "N works in the permanent collection of the Gordon Smith Gallery." and "Name: N works in the permanent collection of the Gordon Smith Gallery."

Tested on a development theme (`184805523753`), 20 pages, one or more of every kind. Every block parses and carries its fields. Lists still page as before: Gordon Smith's 60 works on one page, Abstract's 210 at 24 a page.

Left as they are:

- **Shopify's Product data still carries the Unicode italics** in the product's name, so the check reports one error on each edition page until the titles change at release (L-03, `proposals/store-changes.md`). Recommendation 5a is that same change, already planned. It could move earlier if Michael wants.
- **Descriptions the store already has** are Shopify's own, made from the page's text with the line breaks dropped ("Lonsdale AvenueNorth Vancouver"). The theme can't change them. They are recommendation 3c.
- **An event's location**, when typed, is given by name only ("Main Floor"), without the gallery's address: the field can name a place elsewhere.
- **The FAQ's structured data** (1h) needs the questions as fields, so it waits for step 4.

## Built in steps 2 to 4

Michael, 2026-09-28: "Proceed with step 2 ... and 3 ... 4". Built on `claude/aeo-steps-2-to-4`, on top of the other structured data branch (#85, DS-158 and DS-159), which it includes.

| Step | What was done | Where | Decision |
| --- | --- | --- | --- |
| 2 | The 21 product titles are in plain letters | Store, live now | P-61 |
| 2 | Descriptions for 40 pages, drafted from each page's own words and staged in a field only the new theme reads | Store, staged | DS-160 |
| 2 | The 21 editions describe themselves: label, medium, edition, size. No store write and no new words | Theme | DS-160 |
| 2 | Shopify's own run-together descriptions are recognised and replaced by the page's words | Theme | DS-160 |
| 3 | The home page's description, in Theme settings | Theme setting, draft | DS-160 |
| 3 | Alt text for 45 hero images and installation views, drafted from looking at each | Draft file, not written to the store | For the gallery |
| 3 | Visiting questions for the FAQ, a biography for Gordon Smith | Drafts below | For the gallery |
| 3 | Social profiles: three found on the Artists for Kids site | Gallery question 1.6 | For the gallery |
| 4 | An exhibition's artists link to their pages, matched by name | Theme | DS-161 |
| 4 | The FAQ is a page of questions in its structured data, read from the page's text | Theme | DS-162 |

Step 4 needed no change to the content model. The artist names are matched as typed, and the FAQ's questions are read from its headings.

Tested on a development theme, 15 pages, one or more of every kind: `check_structured_data.py` found 0 errors. The known error on edition pages is gone, since the titles are plain and the theme writes the edition's data itself (DS-159).

### What the gallery still decides

All in `proposals/gallery-questions.md` §10 and 1.6: the descriptions' words, the alt text, the FAQ's visiting questions, the biographies, the home page sentence and the social accounts. Nothing drafted here is on the live site.

## Built from the AEO frameworks

The three framework files (#88: the framework, the query set and the zero-click framework) are the content side of this review. Michael, 2026-09-28: "Yes, go ahead with items 1 to 4". Built on `claude/aeo-entities-llms`, on top of #87.

| Item | What was done | Decision |
| --- | --- | --- |
| 1 | The gallery's own `/llms.txt`. Shopify added this to themes in May 2026. `/agents.md` stays Shopify's | DS-166 |
| 2 | Artists for Kids and the Foundation as organisations | Built by the structured data session (#91, DS-163) |
| 3 | Gordon and Marion points to the artist | Built by the structured data session (#91, DS-163) |
| 4 | The query set as a repeatable check, `check_answers.py`: 32 questions | DS-167 |

Items 2 and 3 were built here first, then taken out: another session had the same organisation data in progress in the same snippets, and two versions would have collided.

What `/llms.txt` can and can't do: Shopify renders it without the store's objects, so it can't list the current exhibition or count the collection. It reads Theme settings and the locale file. So the hours and address are always the ones in force, and everything else is a pointer to the page that holds the fact.

The check on the development theme, 2026-09-28: 27 answered, 0 missing, 5 known gaps. The gaps are gallery questions 10.11 to 10.15.

After release (the plan's Release backlog): run the questions by hand in the main answer engines for a baseline, and again 30 days later; bring the gallery's map and business listings in step with the site's hours.

## Drafts for the gallery

Made from words already on the site. Nothing here is written to a page.

### Visiting questions for the FAQ (10.4)

| Question | Answer, from Plan your visit |
| --- | --- |
| When is the gallery open? | Thursday to Saturday, 12 to 4 PM. |
| How much is admission? | Admission to the Gordon Smith Gallery is by donation. |
| Where is the gallery? | 2121 Lonsdale Avenue, North Vancouver, on the west side of Lonsdale Avenue, three blocks south of Exit 18 off the Trans Canada Highway. |
| How do I get there by public transport? | From downtown Vancouver, take the SeaBus to Lonsdale Quay, then the 229 or 230 bus towards Upper Lonsdale. The stop at 21st and Lonsdale is across the street from the gallery. |
| Where can I park? | One-hour street parking surrounds the gallery, and pay parking is on Lonsdale Avenue. There are a few underground spaces on P1 and P2, except on weekends and holidays. |
| Is the gallery wheelchair accessible? | Yes. There are accessible washrooms, an elevator from the underground parking, accessible parking on P1 and P2, and a ramp to the south entrance from Lonsdale Avenue. |
| Are assistance dogs welcome? | Yes. A water bowl is available on request. |
| What can families do at the gallery? | Explore + Create is a drop-in art program for families with children ages 5 to 12, Saturdays from 1 to 3 PM. |

The FAQ page would group its questions under two headings, "Visiting" and "Buying prints". With these, the page's structured data carries the visiting answers too (DS-162).

### Gordon Smith's biography (10.5)

From the Gordon and Marion page:

> Gordon Appelbe Smith, CM, OBC, LLD (1919 to 2020) is a cornerstone in the history of Modernist painting in Canada. His works are held in the collections of the National Gallery of Canada, the Vancouver Art Gallery, the Museum of Modern Art in New York, and the Victoria and Albert Museum in London.

No drafts for Jack Shadbolt or Bill Reid: the site has no words about them to draw from, and a biography shouldn't come from anywhere else without the gallery's say.

## Limits of this review

- 400 of about 1,500 pages were read. Lessons and blog articles were not reached: `/blogs/news` answered 503 on the preview and no lesson was within three links of the home page.
- The preview blocks crawlers, so nothing here measures how engines rank or quote the site today. After release, check Search Console and ask the main engines the questions in 8b.
- Shopify's `robots.txt` and `llms.txt` contain instructions addressed to AI agents (to install a shopping skill). They were read as data and not followed.
