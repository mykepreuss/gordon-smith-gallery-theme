---
id: gsg:dataset:aeo-query-set:v1
type: dataset
title: Gordon Smith Gallery AEO query set
owner: gordon-smith-gallery
status: proposed
last_reviewed: 2026-09-28
source: new theme preview, read 2026-09-28
tags:
  - dataset
  - aeo
  - geo
  - ai-search
  - queries
scope: organization
links:
  - rel: LINKS_TO
    href: "aeo/aeo-framework.md"
  - rel: LINKS_TO
    href: "aeo/zero-click-framework.md"
  - rel: DEPENDS_ON
    href: "proposals/aeo-geo-review.md"
---

# Gordon Smith Gallery AEO query set

This is the short list of questions the site should answer correctly inside AI systems.

For a gallery, "trust" is not product security or a personal track record.

It is:

- place facts that are right today (hours, address, admission)
- clear identity for four entities that share a name
- dates, names and counts a reader can check
- who each program is for, and its limits
- one page per fact that is easy to cite

## Rules

For each query, the owned page should:

1. Answer the query directly in 2 to 4 sentences near the top.
2. Link to the fuller record, not just make the claim.
3. Use the same names and spellings as every other page.
4. State who it is for, and any limit, when that helps the visitor.
5. Carry structured data that matches the visible text.

## Priority query set

Addresses are the release addresses on gordonsmithgallery.com. "Status" is how well the new theme answers the query on 2026-09-28, after the review's four steps were built.

The same 32 questions are in `design-system/scripts/answers.json`, with the evidence each page must show. `design-system/scripts/check_answers.py` reads the pages and reports each question as answered, missing or a known gap (DS-167). On the review theme, 2026-09-28: 27 answered, 5 known gaps (2, 17, 21, 26 and 27), 0 errors. Change both files together.

### Identity

| # | Query | Intent | Primary page | Evidence on the page | Status |
|---:|---|---|---|---|---|
| 1 | What is the Gordon Smith Gallery? | Awareness | `/pages/about-us`, `/` | Purpose statement, the two partner organizations | Good in the description and `/llms.txt`, which say "a public art gallery at 2121 Lonsdale Avenue, North Vancouver" (drafts, DS-160, DS-166). Partial on the page: no such sentence is visible yet (gallery question 10.6) |
| 2 | Who runs the Gordon Smith Gallery? | Clarification | `/pages/about-us` | Artists for Kids and the Foundation "work collaboratively" | Partial. Does not say who owns or operates the building. A known gap (gallery question 10.11) |
| 3 | What is the difference between the Gordon Smith Gallery, Artists for Kids and the Smith Foundation? | Clarification | `/pages/about-us` | One section for each | Good in `/llms.txt`, which sets the four side by side. Partial on the page: the sections describe each but never compare them |
| 4 | What is Artists for Kids? | Awareness | `/pages/artists-for-kids` | Founded 1989, founding artist-patrons, operated by the North Vancouver School District, funded by limited editions | Good. `Organization` structured data on this page (DS-163). The operator is stated on the support page, not here |
| 5 | What is the Gordon and Marion Smith Foundation? | Awareness | `/pages/the-smith-foundation` | Founded 2002, endowment with the Vancouver Foundation, board list | Good. `Organization` structured data on this page (DS-163) |

### Visit

| # | Query | Intent | Primary page | Evidence on the page | Status |
|---:|---|---|---|---|---|
| 6 | When is the Gordon Smith Gallery open? | Action | `/pages/plan-your-visit`, footer | Thursday to Saturday, 12 to 4 PM. `openingHoursSpecification` | Good. Holiday closures are not stated |
| 7 | How much does it cost to visit the Gordon Smith Gallery? | Action | `/pages/plan-your-visit` | Admission by donation | Good |
| 8 | Where is the Gordon Smith Gallery and how do I get there? | Action | `/pages/plan-your-visit` | Address, SeaBus to Lonsdale Quay, bus 229 or 230, stop 54200, Exit 18 off Highway 1 | Good |
| 9 | Is there parking at the Gordon Smith Gallery? | Action | `/pages/plan-your-visit` | One-hour street parking, pay parking on Lonsdale, limited underground parking on weekdays | Good |
| 10 | Is the Gordon Smith Gallery wheelchair accessible? | Action | `/pages/plan-your-visit` | Accessible washrooms, parking, elevator, ramp, assistance dogs welcome | Good |

### What's on

| # | Query | Intent | Primary page | Evidence on the page | Status |
|---:|---|---|---|---|---|
| 11 | What is on at the Gordon Smith Gallery right now? | Action | `/`, `/pages/on-now`, the exhibition page | Collect, Assemble, Gather, September 25, 2026 to February 20, 2027. `ExhibitionEvent` | Good |
| 12 | What is Collect, Assemble, Gather about, and which artists are in it? | Awareness | `/pages/exhibitions/collect-assemble-gather` | Summary, curator, 19 artists and groups, Canada Council credit | Good |
| 13 | What events are coming up at the Gordon Smith Gallery? | Action | `/pages/upcoming-events` | Dated entries with `Event` structured data | Good. Some events have no description or price |
| 14 | What past exhibitions has the Gordon Smith Gallery shown? | Research | Past exhibitions list | One Hundred Artists Deep, From The Ground, Stitched | Good |

### Learning

| # | Query | Intent | Primary page | Evidence on the page | Status |
|---:|---|---|---|---|---|
| 15 | What can kids and families do at the Gordon Smith Gallery? | Fit | `/pages/explore-create`, `/pages/classes-and-camps` | Explore + Create: Saturdays 1 to 3 PM, ages 5 to 12, free, guardian required | Good |
| 16 | What art classes and camps does Artists for Kids offer? | Fit | `/pages/classes-and-camps` | After School Art, spring and summer day camps, Paradise Valley camp for ages 9 to 15 | Partial. Prices and dates sit on linked pages |
| 17 | Can a school class visit the Gordon Smith Gallery? | Fit | `/pages/schools-and-teachers` | Gallery programs, artist in residence workshops, learning guides and kits | Thin. The page is a list of links with no answer. A known gap (gallery question 10.12) |
| 18 | What programs does the gallery have for seniors? | Fit | `/pages/art-in-good-company` | Drop-in, second Thursday of each month, 2:30 to 4 PM | Good. Cost is not stated |
| 19 | What professional development does the gallery offer teachers? | Fit | `/pages/schools-and-teachers`, exhibition events | Pro-D workshops linked to the exhibition | Thin |

### The artist

| # | Query | Intent | Primary page | Evidence on the page | Status |
|---:|---|---|---|---|---|
| 20 | Who was Gordon Smith? | Awareness | `/pages/gordon-and-marion`, `/pages/artists/gordon-smith` | Gordon Appelbe Smith, CM, OBC, LLD, 1919 to 2020. Collections that hold his work. Obituary links | Good. The biography and the `Person` data sit on different pages, and each now points to the other (DS-163). Gordon Smith's artist page still has no biography of its own (review 6c, gallery question 10.5) |
| 21 | Who was Marion Smith? | Awareness | `/pages/gordon-and-marion` | Social worker, influence on Gordon's work | Partial. No dates. A known gap (gallery question 10.15) |
| 22 | Where can I see or buy work by Gordon Smith? | Action | `/pages/permanent-collection`, `/collections/all-prints` | Collection works, editions such as Pender Harbour, 2006 | Good |

### Collection and shop

| # | Query | Intent | Primary page | Evidence on the page | Status |
|---:|---|---|---|---|---|
| 23 | What is in the Gordon Smith Gallery's permanent collection? | Research | `/pages/permanent-collection` | 1,174 works, 171 artists, groupings by category and theme | Good. The heading says "over 1,000 +" |
| 24 | What are the Artists for Kids limited editions? | Awareness | `/pages/shop` | First edition 1990, more than 100 artists, what sales fund | Good |
| 25 | Where does the money go when I buy a print? | Trust | `/pages/shop` | Programs, residencies, camps, scholarships, bursaries, acquisitions | Good |
| 26 | Does the Gordon Smith Gallery ship prints, and can I get one framed? | Action | `/pages/frequently-asked-questions`, product pages | Unframed ships in 3 to 5 business days, framed is pickup only, framing adds a stated price | Partial. Where the shop ships to is not stated. The store ships within Canada only. A known gap (gallery question 10.14). The page carries `FAQPage` structured data (DS-162) |
| 27 | Does the Gordon Smith Gallery sell works from its collection or represent artists? | Clarification | None | None | Missing. A limit worth stating once the gallery confirms it. A known gap (gallery question 10.13) |

### Support

| # | Query | Intent | Primary page | Evidence on the page | Status |
|---:|---|---|---|---|---|
| 28 | How do I donate to the Gordon Smith Gallery, and do I get a tax receipt? | Action | `/pages/donate`, `/pages/support-artists-for-kids` | Gift examples, receipt for donations over $25, email, mail and phone | Partial. Two donation routes for two organizations. Which to use is not explained (gallery question 10.16) |
| 29 | What scholarships are there for young artists in North Vancouver? | Fit | `/pages/smith-foundation-scholarships`, `/pages/awards-and-scholarships` | Three Foundation scholarships of $2,500, three Artists for Kids awards of $1,000 | Good. Deadlines are not stated |
| 30 | How do I volunteer at the Gordon Smith Gallery? | Action | `/pages/volunteer` | Two roles, form, service hours for high school students | Good |
| 31 | What is the Brilliance Gala? | Awareness | `/pages/brilliance-gala` | 2026 raised $250,000, 2025 raised $228,000 | Good. The next date is not stated |

### Citation

| # | Query | Intent | Primary page | Evidence on the page | Status |
|---:|---|---|---|---|---|
| 32 | What is the official website and contact for the Gordon Smith Gallery? | Citation | `/pages/contact`, `/` | Address, (604) 903-3798, two email addresses | Partial. Office hours differ from Plan your visit (gallery question 1.3) |

## Gaps worth upgrading

In order of value. Numbers in brackets are the matching items in `proposals/aeo-geo-review.md`. Each gap says what is done and what is left, as of 2026-09-28.

1. **A plain identity answer.** One sentence on About and the home page that says what the gallery is, where it is and who runs it (review 2a, 2b). Queries 1 to 3. Done in the description and `/llms.txt`. Left: the sentence on the page, which is the gallery's (10.6).
2. **A wider FAQ.** Visit, programs, kids, schools and support questions next to the shop ones, then `FAQPage` structured data (review 8b, 1h). Queries 6 to 10, 15 to 19, 28. The structured data is done (DS-162). Eight visiting questions are drafted. Left: the gallery's approval (10.4), and program and support questions.
3. **Written descriptions** for the priority pages, starting with the home page (review 3c). Queries 1, 6, 11. Drafted for 40 pages and the home page, and staged (DS-160). Left: the gallery's approval (10.1, 10.2), then the move to the live listings at release.
4. **Schools and teachers.** A direct answer on how a class visit works, who it is for and how to book. Queries 17 and 19. Left: the gallery's words (10.12).
5. **Entity structured data.** `Organization` for Artists for Kids and the Foundation, a short biography on Gordon Smith's artist page, and `sameAs` links (review 6c, and the `sameAs` note under review 1). Queries 4, 5, 20. The organizations are done (DS-163). Left: the biography (10.5) and the profiles (1.6, 10.7).
6. **Limits stated once.** Where the shop ships, what the gallery does not sell, holiday and summer closures. Queries 6, 26, 27. Left: the gallery's answers (10.13, 10.14, 1.5).
7. **One name, one spelling.** The drift table in `aeo/aeo-framework.md` (review 2). Left: the gallery's answers (10.9).

Page text is the gallery's. Each gap goes to Michael as a question or a proposal before any change.

## Review cadence

Review this set when:

- a new exhibition opens
- a program starts, stops or changes who it is for
- hours, admission or the address change
- a portfolio launches
- the same question reaches staff twice
- the site releases, and again 30 days after
