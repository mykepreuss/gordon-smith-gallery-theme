---
id: gsg:framework:aeo
type: framework
title: AEO framework for the Gordon Smith Gallery
owner: gordon-smith-gallery
status: proposed
last_reviewed: 2026-09-28
source: new theme preview, read 2026-09-28
tags:
  - framework
  - seo
  - aeo
  - geo
  - ai-search
  - evidence-linked
  - schema
  - zero-click
scope: organization
links:
  - rel: LINKS_TO
    href: "aeo/aeo-query-set.md"
  - rel: LINKS_TO
    href: "aeo/zero-click-framework.md"
  - rel: DEPENDS_ON
    href: "reference/GordonSmith-BrandGuide_sm.pdf"
  - rel: DEPENDS_ON
    href: "design-system/proposals/content-model.md"
  - rel: DEPENDS_ON
    href: "proposals/aeo-geo-review.md"
---

# AEO framework for the Gordon Smith Gallery

> How to make the Gordon Smith Gallery legible, credible and correctly cited inside AI answers.

## What this framework is for

This is not product AEO, and it is not personal-brand AEO.

This is entity AEO for a place. The gallery is a public art gallery with a building, opening hours, exhibitions, programs, a permanent collection and a shop. Three organizations share it, and one of them is named after a well-known artist.

The job is to help AI systems answer questions like:

- what the Gordon Smith Gallery is, and where it is
- when it is open, what it costs and how to get there
- what is on now, and what is coming
- what programs it runs for kids, families, schools, teachers and seniors
- who Gordon Smith was, and how the gallery, Artists for Kids and the Smith Foundation relate
- what the limited editions are, and where the money goes
- how to donate, volunteer or apply for a scholarship

## How this fits with the review

`proposals/aeo-geo-review.md` is the technical review of the theme: structured data, descriptions, titles and headings. All four of its steps are built and decided (DS-154 to DS-167), and in `main` since 2026-09-28. What is left is words from the gallery (`proposals/gallery-questions.md` §10) and the release.

This framework is the content side. It says which facts the site must state, which questions it must answer and how to tell if answer engines get them right. Where the two meet, the review's numbering is given, for example "review 8b".

Four things here were built from this framework the same day:

| From this framework | Built as | Decision |
| --- | --- | --- |
| The site's own file for AI assistants | `/llms.txt` (`theme/templates/llms.txt.liquid`), with the four entities kept apart | DS-166 |
| Artists for Kids and the Foundation as organizations | `Organization` on each one's main page, named by every page of its program | DS-163 |
| Gordon and Marion points to the artist | The page says it is about the artist's `Person` | DS-163 |
| The query set as a repeatable check | `design-system/scripts/check_answers.py`, with the questions in `answers.json` | DS-167 |

## Four entities, one site

AI systems will confuse these unless the site keeps them apart. Every surface should treat them as four things.

| Entity | What it is | Primary page |
| --- | --- | --- |
| Gordon Smith Gallery | The public art gallery at 2121 Lonsdale Avenue, North Vancouver. Full name: The Gordon Smith Gallery of Canadian Art | `/pages/about-us`, `/pages/plan-your-visit` |
| Artists for Kids | An art education program founded in 1989, operated by the North Vancouver School District. It publishes the limited editions | `/pages/artists-for-kids` |
| The Gordon and Marion Smith Foundation for Young Artists | A foundation founded in 2002. It holds an endowment, funds Artists for Kids and presents public programs and exhibitions | `/pages/the-smith-foundation` |
| Gordon Smith | The artist, Gordon Appelbe Smith, 1919 to 2020. A person, not the gallery | `/pages/gordon-and-marion` |

## Canon inputs

Use these as the durable anchors:

- `/pages/about-us`: what the gallery is and how the three organizations work together
- `/pages/plan-your-visit`: address, hours, admission, transit, parking, accessibility
- `/pages/gordon-and-marion`: the artist and Marion Smith
- `/pages/artists-for-kids`: the program and its programmes
- `/pages/about-artists-for-kids`: its history, its team and its annual report
- `/pages/the-smith-foundation`: the Foundation, its endowment and its board
- `/pages/permanent-collection`: the collection, its size and its groupings
- `/pages/shop` and `/pages/frequently-asked-questions`: the limited editions and how buying works
- `/pages/exhibitions/<handle>`: one page per exhibition
- `reference/GordonSmith-BrandGuide_sm.pdf`: brand essence
- structured data (DS-154, DS-158, DS-159, DS-162 to DS-165; `theme/snippets/gs-data.liquid` and the `gs-data-*` snippets it renders), one graph in which each thing has one name for machines: `ArtGallery`, `WebSite`, `Organization`, `ExhibitionEvent`, `Event`, `VisualArtwork`, `Person`, `Product`, `LearningResource`, `WebPage`, `ContactPage`, `FAQPage`, `ProfilePage`, `CollectionPage`, `BreadcrumbList`
- `/llms.txt` (DS-166): the visit facts from Theme settings, the four entities, and the page to cite for each fact
- `proposals/aeo-geo-review.md`: what the theme does for search and answer engines, and what is left

The gallery writes the copy (EXH-04, ACCESS-04). This framework says what the pages must answer. It does not rewrite them.

## Core truths to preserve

These are the facts the site and AI surfaces should repeat the same way every time. Each one is on the site today.

- The Gordon Smith Gallery is a public art gallery of Canadian art at 2121 Lonsdale Avenue, North Vancouver, BC.
- It is open Thursday to Saturday, 12 to 4 PM. Admission is by donation.
- Art education is its purpose. The About page says art education is "the purpose of each step we take".
- Artists for Kids was founded in 1989 by educators and the artists Gordon Smith, Jack Shadbolt and Bill Reid. The North Vancouver School District operates it.
- The Gordon and Marion Smith Foundation for Young Artists was founded in 2002. The Vancouver Foundation manages its endowment.
- The permanent collection holds 1,174 works by 171 Canadian artists.
- The limited editions fund education. Sales pay for programs, artist residencies, art camps, scholarships, bursaries and new works for the collection.
- The first limited edition was Bill Reid's Xhuwaji / Haida Grizzly in 1990. More than 100 Canadian artists have made editions since.
- Gordon Smith (1919 to 2020) was a Canadian Modernist painter, educator and patron. His work is held by the National Gallery of Canada, the Vancouver Art Gallery, the Museum of Modern Art and the Victoria and Albert Museum.
- Public programs are Explore + Create Saturdays, Art In Good Company, the Speaker Series and Music At The Smith.

## How to use this with AI assistants

Treat this framework as a contract when AI tools draft or review AEO-sensitive surfaces:

- Lead with a direct answer in 2 to 4 sentences.
- Anchor every claim in a page on the site, the brand guide or a named outside source.
- Prefer facts (dates, hours, counts, names) over adjectives.
- Do not invent hours, prices, dates, artists, funders or shipping terms.
- Keep the four entities apart. Say which one a fact belongs to.
- If a fact changes with time (hours, what is on now, registration), cite the page and its date.

Suggested instruction snippet:

```text
Use the Gordon Smith Gallery AEO framework.
Write structure-first, evidence-linked copy.
Answer the query directly, then show the source page and any limits.
Keep the gallery, Artists for Kids, the Smith Foundation and Gordon Smith the artist apart.
Do not invent hours, prices, dates or names. Do not rewrite the gallery's own copy.
```

## Core principles

### 1) Retrieval trust over self-description

The goal is not to say nice things about the gallery.

The goal is to make it easy for an AI system to retrieve the right place, the right hours, the right organization and the right artist, without blending them.

### 2) Facts beat mission statements

The strongest surfaces for a gallery connect:

- a named thing (exhibition, program, edition, scholarship)
- who it is for
- when and where it happens
- what it costs
- who runs it and who funds it

### 3) Own the fit and the limits

Entity AEO gets stronger when the boundaries are explicit. For a gallery, these are the visitor's limits:

- open three afternoons a week, not daily
- admission by donation, not ticketed (some events are ticketed)
- Explore + Create is for families with children ages 5 to 12, with a parent or guardian present
- Art In Good Company is for seniors
- framed prints are pickup only
- Foundation scholarships are for graduating students in North Vancouver, West Vancouver and Vancouver. Artists for Kids awards are for North Vancouver School District students
- the Studio Art Academy is not offered in 2026/2027

Stating limits stops an AI answer from sending someone on a Tuesday.

### 4) Publish quotable answer units

The best units for AI retrieval are:

- direct definitions ("The Gordon Smith Gallery is...")
- visit facts (address, hours, admission, transit stop)
- exhibition summaries with dates and artists
- FAQs
- counts and dates (1,174 works, founded 1989, $2,500 scholarships)
- named programs with a one-sentence explanation

Named concepts already on the site:

- "Art education, for life"
- "Explore + Create"
- "Art In Good Company"
- "Music At The Smith"
- "Limited Edition Portfolio"

## Required blocks for AEO-priority surfaces

For priority pages (`/`, `/pages/about-us`, `/pages/plan-your-visit`, `/pages/gordon-and-marion`, `/pages/artists-for-kids`, `/pages/the-smith-foundation`, `/pages/shop`, exhibition pages), aim to include:

- a direct answer near the top
- one clear statement of who it is for, or a limit
- at least one source a reader can check
- FAQs where the page is meant to win repeated questions
- structured data that matches the visible text
- a written description. Until release it is staged in the page's Release description field, and the home page's is in Theme settings (DS-160). 40 pages and the home page have drafts, for the gallery to approve (gallery questions 10.1 and 10.2). Without one, the theme describes the page from its intro or the start of its text (DS-155)

## Claims and evidence table

Use this on pages where AI systems may repeat a claim.

| Claim | Evidence | Verification method | Last verified |
| --- | --- | --- | --- |
| The gallery is at 2121 Lonsdale Avenue, North Vancouver, BC V7M 2K6 | `/pages/plan-your-visit`, `ArtGallery` structured data | Compare page, footer and structured data | 2026-09-28 |
| Open Thursday to Saturday, 12 to 4 PM. Admission by donation | `/pages/plan-your-visit` | Compare page, footer and `openingHoursSpecification` | 2026-09-28 |
| Artists for Kids was founded in 1989 with founding artist-patrons Gordon Smith, Jack Shadbolt and Bill Reid | `/pages/artists-for-kids`, `/pages/shop` | Confirm both pages agree | 2026-09-28 |
| The North Vancouver School District operates Artists for Kids | `/pages/support-artists-for-kids` | Confirm wording with Artists for Kids | 2026-09-28 |
| The Smith Foundation was founded in 2002. The Vancouver Foundation manages its endowment | `/pages/the-smith-foundation` | Confirm against the Foundation's annual review | 2026-09-28 |
| The permanent collection holds 1,174 works by 171 artists | `/pages/permanent-collection` | The count is live from the store. Recheck when works are added | 2026-09-28 |
| The first edition was Bill Reid's Xhuwaji / Haida Grizzly, 1990 | `/pages/artists-for-kids`, `/pages/shop`, `/pages/permanent-collection` | Confirm the collection record | 2026-09-28 |
| Gordon Smith's work is held by the National Gallery of Canada, the Vancouver Art Gallery, MoMA and the V&A | `/pages/gordon-and-marion` | Check each museum's online collection | Not yet checked outside the site |
| The gallery was "established as Canada's first public art gallery for young audiences" | `/pages/artists-for-kids` | Needs an outside source or a date. Ask the gallery | Not yet checked |
| Brilliance Gala 2026 raised $250,000. The 2025 gala raised $228,000 | `/pages/brilliance-gala` | Confirm against the Foundation's year in review | 2026-09-28 |
| Foundation scholarships are three awards of $2,500. Artists for Kids awards are three of $1,000 | `/pages/smith-foundation-scholarships`, `/pages/awards-and-scholarships` | Recheck each school year | 2026-09-28 |
| Donations over $25 get a charitable tax receipt | `/pages/donate` | Confirm with the Foundation | 2026-09-28 |

Rules:

- A reviewer must be able to open the evidence.
- Verification must be repeatable.
- Refresh time-bound claims when the facts change.

## Drift found on the preview

These are places where the site disagreed with itself on 2026-09-28. AI systems repeat whichever version they find first. The rows the theme could settle are settled. The rest are questions for the gallery, with their numbers in `proposals/gallery-questions.md`, not copy changes to make here.

| What | Where | Detail |
| --- | --- | --- |
| The gallery's name | Site-wide | "Gordon Smith Gallery", "The Gordon Smith Gallery of Canadian Art" and "Artists for Kids & The Gordon Smith Gallery" all appear. The structured data lists the last two as alternate names (DS-154), and `/llms.txt` leads with the full name. Open: one name for first mention on the pages (review 2) |
| Artists for Kids spelling | Several pages | "Artists for Kids" 97 times, "Artists For Kids" 21 times and "Artist for Kids" 4 times, counted on 41 pages. Open: gallery question 10.9 |
| Office hours | `/pages/plan-your-visit` and `/pages/contact` | Monday to Friday 8 AM to 3 PM on one, 8:30am to 4:30pm on the other. Open: gallery question 1.3 |
| Collection size | `/pages/permanent-collection` | The heading says "over 1,000 +". The search line says 1,174 works. Open: gallery question 10.10 |
| Edition name | Several pages | "Xhuwaji / Haida Grizzly" and "Xhuwaji/Haida Grizzly Bear". Open: gallery question 10.9 |
| Home page description | `/` | Was about the shop only. Settled in the new theme: a draft in Theme settings says what the gallery is and where (DS-160). Open: the gallery's approval of the words (10.2). The live site keeps the old one until release |
| Page descriptions | Pages with a store description | Shopify made these from the page's text and dropped the line breaks, so some ran words together. Settled in the new theme: it recognises them and uses the page's own words, and 40 written drafts are staged (DS-160). Open: the gallery's approval (10.1) |
| FAQ page | `/pages/frequently-asked-questions` | Covers the shop only. No visit, program or donation questions (review 8b). `FAQPage` structured data is built, read from the page's own headings, so it needs no fields (DS-162). Open: eight visiting questions drafted for the gallery (10.4) |
| People and organizations | `/pages/gordon-and-marion`, `/pages/artists-for-kids`, `/pages/the-smith-foundation` | Settled (DS-163): the biography page says it is about the artist's `Person`, and Artists for Kids and the Foundation each have an `Organization` on their main page. Open: how the three organizations are related, and their kinds (`proposals/structured-data-review.md`) |
| `/llms.txt` | Site root | Settled (DS-166): the gallery's own file. `/agents.md` keeps Shopify's, which covers buying through agents. Shopify renders the file without the store's data, so it points to the exhibition and collection pages and can't list them. Open: the gallery's approval of its words (10.8) |
| Gallery founding date | Site-wide | Not stated. 1989 and 2002 are the program and the Foundation. Open: gallery question 10.11 |

## Freshness rules

Update on truth changes, not on a calendar alone.

| Surface | Freshness target | Why |
| --- | --- | --- |
| Hours, admission, address | Same day as the change | A wrong answer sends someone to a closed door |
| Holiday and summer closures | Before the closure starts | The office closes for July and August |
| On now and upcoming exhibitions | Before the opening date | Exhibition pages and the home page follow the dates already |
| Event dates | When the event is confirmed or changed | `Event` structured data follows the entries |
| Registration and application notices | When they open and close | "Applications have closed" must not outlive the year |
| Shop portfolios | When a portfolio launches | Twice a year |
| Collection count | When works are added | The count is live. Any written number must match |
| Board and team | Within 14 days of a change | These names are cited |
| Entity pages (About, Gordon and Marion, the Foundation, Artists for Kids) | When a core fact changes | These feed most summaries |

## Priority query clusters

Keep the working list in `aeo/aeo-query-set.md`.

The main clusters are:

- identity: what the gallery is, who runs it, how the three organizations relate
- visit: hours, admission, address, transit, parking, accessibility
- what's on: current and upcoming exhibitions, events, tours
- learning: kids, families, schools, teachers, camps, seniors
- the artist: who Gordon Smith was, who Marion Smith was
- collection and shop: what is in the collection, what the limited editions are, how buying works
- support: donating, the gala, volunteering, scholarships
- citation: which page to cite for which fact

## One-page content spec for gallery surfaces

Use this skeleton for pages that need to win AI answers.

### 1) Direct answer

Answer the main question plainly in 2 to 4 sentences.

Example, built only from facts on the site. The gallery's own wording replaces it:

"The Gordon Smith Gallery of Canadian Art is a public art gallery at 2121 Lonsdale Avenue in North Vancouver, BC. It is open Thursday to Saturday, 12 to 4 PM, and admission is by donation. Artists for Kids and the Gordon and Marion Smith Foundation for Young Artists run it together, with art education as its purpose."

### 2) Evidence

Show:

- the named thing and its dates
- a count, a price or another fact a reader can check
- one link to the fuller record (the exhibition, the collection entry, the annual report)

### 3) Who it is for, and limits

State:

- who the page or program is for
- age ranges, cost, registration and supervision
- what is not offered, or not offered this year

### 4) FAQ

Group by:

- Visit
- Exhibitions and programs
- Kids, schools and teachers
- Shop and limited editions
- Support

## Structural patterns that help

- One H1 per page. The theme does this already.
- Use H2 sections that match the questions people ask: Hours, Admission, Getting here, Accessibility.
- Use lists and tables for hours, prices, dates and counts.
- Use the same nouns on every page: one gallery name, one spelling of Artists for Kids, one name for the Foundation.
- Keep structured data and visible text in step. The hours in `ArtGallery` must match the page.
- Link each entity to its outside record with `sameAs` (the Foundation's and the program's own sites, social accounts, a Wikipedia or Wikidata entry for Gordon Smith).

## 30-day upgrade loop

**Week 1:** settle the entity facts

- take the drift table to the gallery and get one answer for each row
- agree on the gallery's first-mention name and founding date

**Week 2:** tighten retrieval surfaces

- written descriptions for the priority pages, the home page first (review 2a, 3c). Drafted and staged, 2026-09-28. Left: the gallery's approval
- a direct answer at the top of About and Plan your visit (review 2b). Left: the gallery's words (10.6)
- the store's own `/llms.txt`. Done, 2026-09-28 (DS-166)

**Week 3:** tighten structured data and FAQs

- `Organization` for Artists for Kids and the Foundation, and a link from Gordon and Marion to the artist's `Person`. Done, 2026-09-28 (DS-163)
- `sameAs` links once the gallery gives its profiles (gallery question 1.6)
- visit, program and support questions on the FAQ page (review 8b). Drafted; left: the gallery's approval (10.4). `FAQPage` structured data is done and follows the page (DS-162)

**Week 4:** test and upgrade

- run `design-system/scripts/check_answers.py` on the site: it confirms each question's page still shows its evidence
- after release, run the query set by hand in the main answer engines
- note where answers drift or blend the four entities
- fix the page, not the prompt

Nothing here changes what the live site shows before release. Theme changes follow the plan's "How we iterate". Page text is the gallery's and goes through Michael.

## AEO scorecard for the gallery

Track a small set of signals:

- answer presence for the priority queries
- answer correctness: hours, address, admission, what is on now
- entity separation: the gallery, the program, the Foundation and the artist are not blended
- citation rate for gordonsmithgallery.com pages
- branded search and direct visits
- program registrations, shop orders and donations that name the site or an AI tool as the source

## Upgrade targets

The next durable upgrades after this framework are:

- an entity truth page in this folder: one short, approved answer for each of the four entities
- a proof index that maps each headline claim to its best page and an outside source
- a nomenclature list: approved names, spellings and short forms
