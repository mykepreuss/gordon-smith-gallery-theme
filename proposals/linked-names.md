# Links between pages: names in a text link to their pages

Date: 2026-09-28. Decision: DS-175, **decided by Michael, 2026-09-28** ("DS-175 approved, merge #106"), as built.

## What Michael asked

About The Smith Foundation page on the new theme: "there are more links from some of the content", then "Donors should link to that page, Donate, etc. it's more an internal linking point".

## What the page had

| Part | Links | What was missing |
| --- | --- | --- |
| Opening text | 5: the four programmes and Gordon and Marion | Nothing |
| Six cards | 5: four cards link by their heading, one by a "Donate Today" link | The cards' text named seven things with pages of their own, none linked. A card that links by its heading shows no sign that it is a link |
| Board | 0 | No pages to link to |

A card's text is plain text, so it could not hold a link.

## What this does

Where a text names something the site has a page for, the name becomes a link to that page. It works on every page, not only this one. No words change.

The names are two lists in Theme settings, Links between pages. Staff change the lists; nobody edits the texts.

| List | Linked | As built |
| --- | --- | --- |
| Names | On every page | Gordon and Marion Smith Foundation, Smith Foundation, Artists for Kids, Speaker Series, Music at The Smith, Explore + Create, Art In Good Company, Brilliance Gala, Permanent Collection, public programs |
| General words | Only where the page they lead to belongs to the same organisation as the page they are on, or to the Gallery | donors, scholarships, volunteers |

## The rules

1. A name is linked once in a text, the first time it stands as whole words. Capitals don't matter.
2. Never to the page it is on.
3. Never inside a heading or another link, and never when the text already links to that page.
4. A longer name goes above a shorter one inside it, so "Gordon and Marion Smith Foundation" is taken before "Smith Foundation".

## Why general words are kept apart

The first build linked every word on every page. Read in their sentences, three links were wrong:

| Page | Sentence | Linked to | Wrong because |
| --- | --- | --- | --- |
| Support Artists for Kids | "we rely on the generosity of our donors" | The Foundation's supporters | These are Artists for Kids' donors |
| Support Artists for Kids | "To make a donation over the phone" | The Foundation's Donate page | This is a gift to Artists for Kids, a different route (gallery question 10.16) |
| Brilliance Gala | "collectors donate an original work" | Donate | It means giving a work of art |

So general words are linked only within their own organisation's pages, and "donate" and "donation" are left out.

## What it adds

On 21 pages of the development theme, against the review theme:

| Page | Links before | After |
| --- | --- | --- |
| The Smith Foundation | 11 | 20 |
| About us | 3 | 8 |
| Donate | 8 | 13 |
| Brilliance Gala | 6 | 9 |
| Supporters | 3 | 5 |
| Volunteer | 3 | 5 |
| Support Artists for Kids | 15 | 17 |
| Scholarships | 2 | 4 |
| Frequently asked questions | 0 | 2 |
| Each of two exhibitions, Speaker Series | | 2 more each |
| Home, Gordon Smith's artist page, Public programs, Explore + Create | | No change |

On every page the words are the same, no link sits inside another link, and there are no Liquid errors.

## For Michael

Michael, 2026-09-28: "DS-175 approved, merge #106". Choice 1 is decided. Choices 2 to 4 have no decision number and stay as built.

| # | Question | Built as | Alternative |
| --- | --- | --- | --- |
| 1 | DS-175 | As above | Links written by hand into each text. That is a store write for each page, and cards can't hold them |
| 2 | A name in a card that already links to that page ("donors" in the Supporters card) | Linked, as you asked. The card is also one link, by its heading | Leave it out, since the card goes there already |
| 3 | The same name in several cards on one page ("Artists for Kids" in three cards on the Foundation page) | Linked in each card, once | Once on the page. The theme can't count across cards, so this would need the cards' texts changed |
| 4 | Cards that link by their heading show no sign of it | Unchanged | A short link under the text, such as "More", as the live site has. Its words are the gallery's |

## Since then

2026-09-29, DS-183 (decided by Michael the same day; `proposals/internal-linking-review.md`, finding 6): names are linked in the texts about works too (an edition's description and its archive note, a portfolio's description, a work's About, an exhibition's credits, a lesson's text). Those texts link the names only, not the general words. Three names joined the list: Gordon and Marion Smith Foundation for Young Artists, Artists in Residence, Artist in Residence.

2026-09-29, Michael, on the Artists for Kids team: "These should link like the other peoples'". Allison Kerr's role says "Artist for Kids", as written, so the name didn't match. "Artist for Kids" joined the list below "Artists for Kids", as "Artist in Residence" did. The words stay as the gallery wrote them. On the development theme it adds one link on the site's pages (all but the collection's works): hers on About Artists for Kids. The history text there, which says "Artist for Kids" twice, links the name once already, so it gets no new link.

## Limits

- Pages only. A name can't lead to an exhibition, an artist or an edition.
- A name is matched as written. "Artists 4 Kids" or "AFK" would need their own lines.
- Where the first match in a text is part of a longer word, the name isn't linked in that text, even if it stands alone later.
- "Gordon Smith" is left out: it is inside "Gordon Smith Gallery", which is on most pages.
