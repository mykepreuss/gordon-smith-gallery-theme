# Links between pages: review, rules and what is built

Date: 2026-09-29. Decisions: DS-178 to DS-187, **decided by Michael, 2026-09-29** ("DS-178 to DS-187 approved, merge #118"), as built. Pull request #118.

## What Michael asked

"I want you to review our internal linking strategy and execution for our new site. I want an optimized internal linking implementation that balances human usability, SEO benefits, and ai agent experience."

## Summary

The site's links are in good order. Every link leads to a page that answers, every link has words, and every page is within three clicks of the home page. The menu, the crumbs, the lists and the names in texts (DS-175) already do most of the work.

The gaps are in how the entries link each other. An exhibition named its artists, but 35 times the artist's page didn't name the exhibition. 23 of 30 exhibitions had one link in, from the Past list. An edition didn't link to the work in the collection, and a work didn't link to its lessons. Five addresses that search engines may list had no link from any page and little to read.

Ten changes close these gaps. All are theme changes. None changes the gallery's words, the live site or the store.

| | Before | After |
| --- | --- | --- |
| Exhibitions with one link in | 23 of 30 | 0 |
| Fewest links in to an exhibition, from other pages' content | 1 | 2 |
| Times an exhibition names an artist whose page doesn't name it back | 35 | 0 |
| Artists' pages' links to exhibitions | 78 | 113 |
| Editions that link to their work in the collection | 0 of 21 | 14 of 21 (the other 7 have no work naming them) |
| Works that link to their lessons | 0 | 25 |
| Pages whose content links to Plan your visit | 2 | 3, and the footer of every page |
| Addresses in the sitemap that may be listed, with no link from any page | 14 | 10, all of them old pages that go at release |
| Links from one page's content to another page | 15,079 | 15,208 |
| Pages with a crumb that say so in their data | 0 of 9 | 9 of 9 |
| Links checked by a script | Their style only | Every link, on every page |

## How it was done

1. **Read every page.** A script started at the review theme's home page (`184767250729`, level with `main` at 55fbe63) and followed every link: 1,623 addresses, which are 1,501 pages and 122 further pages of the groupings' lists. For each link it kept the words, the address and the place: menu, content or footer.
2. **Read the sitemap.** 1,508 addresses, compared with the pages the links reach.
3. **Read the code** that makes the links: the menu, the footer, the crumbs, the cards and tiles, the "more" rows, the names in texts, the head tags and the structured data.
4. **Built the changes** on a development theme and read every page again.

The script is now a check in the repo, `check_links.py` (DS-187). It reads the whole site in under three minutes.

## Three readers

Links serve three readers. They want nearly the same thing, which is why one set of rules can serve all three.

| Reader | How they use links | What they need |
| --- | --- | --- |
| A visitor | Looks for the next step: from an exhibition to visiting, from a work to its artist | A way on from every page, words that say where a link leads, a way back |
| A search engine | Follows links to find pages, and reads a link's words and the number of links to judge what a page is about and how much it matters | Every page linked from another page's content, not only the menu; words that name the page; nothing listed that nobody links to |
| An AI agent or answer engine | Reads a page as text, picks links by their words alone, and reads the structured data as a map | Links as plain `<a href>` that work without JavaScript; words that make sense out of their sentence; data that says the same as the page |

Where they differ:

- **A visitor doesn't want every link.** Forty links in a paragraph help an engine and spoil the reading. So a name is linked once in a text (DS-175), and rows of "more" hold three cards.
- **An agent reads the menu on every page.** A visitor sees it once. See "The menu is printed twice" below.
- **An engine reads hidden words.** Words for screen readers count as a link's words. This is used, with care, where a link says only what it does (DS-185).

## The rules

These are the rules the site now follows. The first seven were already followed in most places. The check enforces 3, 4 and 8.

1. **Every page has a home.** An entry's page links back to the list it belongs to, as a crumb above its title, and its data says the same.
2. **Entries link both ways.** If an exhibition names an artist, the artist's page names the exhibition. The same for a work and its edition, a work and its lessons, a work and the exhibitions that showed it.
3. **Every page is linked from another page's content,** within three clicks of the home page. The menu and the footer are not enough: they say a page exists, not what it belongs to.
4. **A page nobody links to is not listed.** Either it gets a link or it asks search engines not to list it. It joins the listings by itself once it has something to say.
5. **A link's words name the page it leads to.** No "read more" or "click here". A link that says only what it does ("Register") names its subject for screen readers and engines.
6. **Names in a text link to their pages** (DS-175). Once in a text, never in a heading, never to the page itself.
7. **Every page ends with a way on:** more of the same, or how to act.
8. **Machines get the same map.** The sitemap, `/llms.txt` and the structured data name the same addresses as the links do. Links are plain links.

## What is sound already

| Check | Result |
| --- | --- |
| Links that fail | None, on 1,623 addresses |
| Links that are sent on to another address | None |
| Liquid errors | None |
| Links in content with no words | None |
| "Read more", "learn more", "click here" | None. The standalone links say where they lead: "All past exhibitions", "See the 2026 Fall Portfolio", "All works by Gordon Smith" |
| Clicks from the home page | Every page within three. 38 pages at one click, 242 at two, 1,224 at three (the works, the lessons and the older exhibitions) |
| Links that work without JavaScript | All. The menu and its dropdowns are `<details>` |
| Store addresses typed in full | Made relative (`gs-url`), so no link leaves for the `myshopify.com` domain |
| Links to other sites | Marked with the arrow and "(external site)"; a PDF says "(PDF)" |
| A crumb on every entry and edition | 1,428 entries and 21 editions, each with the same crumb in its data |
| Works | Each links to its artist, its category and themes, the exhibitions that showed it, and three more works by the artist |
| The lists' further pages | Each names itself and the pages before and after it (DS-168) |
| Names in texts | Linked from two lists in Theme settings (DS-175) |
| The structured data | One graph: a thing has one name, made from its address, wherever it is mentioned (DS-163) |
| `/llms.txt` | Names 18 pages; `check_answers.py` checks that each answers |

## Findings

### 1. Exhibitions and artists linked one way (high)

An exhibition's artists are typed names, linked where a name matches an artist entry (DS-161). An artist's exhibitions are a list on the artist entry, which came from the old catalogue. Nobody keeps the two in step, so they had drifted apart.

| | Count |
| --- | --- |
| Names on exhibition pages that link to an artist | 83, on 18 exhibitions |
| Of those, the artist's page doesn't name the exhibition | 35 |
| Artists' pages that name an exhibition | 78 links, on 54 pages |
| Of those, the exhibition doesn't name the artist | 30 |

Ross Penhall's page didn't name "Accidentally on Purpose: Ross Penhall", his own exhibition.

**Built (DS-178).** An artist's page lists the exhibitions in its own list and every exhibition whose lists of artists name the artist. An exhibition found both ways shows once. Staff keep one list, the exhibition's.

The other direction is option D, not built.

### 2. Most exhibitions had one link in (high)

"More exhibitions" showed what's on now, then the two most recent past exhibitions, on every exhibition's page. So four exhibitions had links from all 30 pages, and 23 had one link, from the Past list.

**Built (DS-179).** On a past exhibition's page the row is what's on now, then the exhibition after it in time and the one before. Every exhibition is linked from its neighbours, and a visitor can walk the archive from one end to the other. On an exhibition that is on now or coming up, the row is as before.

### 3. No way from an exhibition to visiting (high, for visitors)

Two pages linked to Plan your visit in their content: Home and About us. The page of the exhibition that is on now didn't. The header's opening line leads there, but it reads as hours, not as a way to the page.

**Built (DS-180).** An exhibition that is on now or coming up ends its title box with a button, "Plan your visit". A past one doesn't.

**Built (DS-186).** The footer's Visit column ends with a link, "Plan your visit", under the address and hours.

### 4. Editions, works and lessons linked one way (medium)

| From | To | Before |
| --- | --- | --- |
| A work | Its edition in the Shop | 16 works |
| An edition | The work in the collection | None |
| A lesson | The works that inspired it | 25 links, on 22 lessons |
| A work | The lessons it inspired | None |

**Built (DS-181).** An edition's page links to the work, "See this work in the collection", under the note about the archive. A work's facts gain a row, "Lessons", with each lesson by its title.

Seven editions have no work that names them, among them the three from 2026. For the gallery: are they in the collection yet (`gallery-questions.md` 12.2)?

### 5. Pages listed by search engines that nobody links to (medium)

The sitemap is the store's. It lists every page, entry and product, whatever the theme shows.

| Address | What it is | Built |
| --- | --- | --- |
| `/pages/exhibitions/against-the-latitude-of-progress`, `/pages/exhibitions/fall-2027-exhibition` | Exhibitions to come, with a title and dates only. Their cards are not links (DS-25) | Not listed until they have a summary or text |
| `/pages/browse/featured` | The featured works, which are a row on the Permanent Collection page | Not listed |
| `/blogs/news` | A blog with no articles | Not listed until it has one |
| `/collections/all` | Shopify's list of every product, frames included, titled "Products". Not in the sitemap, but every Shopify store has it at this address | Not listed |
| 16 frames | Sold only with their prints | Already not listed (DS-137) |
| 10 old pages | About, Our Story, Engage, the Exhibitions overview and six exhibition pages | Hidden and sent on at release (`store-changes.md` §5). Listed in `links.json` until then |
| `/agents.md` | Shopify's file for shopping agents | Nothing to do |

**Built (DS-182).** A page the site never links to, with nothing of its own to read, asks search engines not to list it, as a thin event's page already does (DS-176).

### 6. Names were linked in some texts only (medium)

DS-175 covers page text, cards, events, an exhibition's text, a biography and a grouping's introduction. It left out the texts about works. On all 21 editions the note "The first edition is archived in the Artists For Kids and the Gordon Smith Gallery Permanent Collection" named two pages and linked neither.

**Built (DS-183).** Names are linked in an edition's description and its archive note, a portfolio's description, a work's About, an exhibition's credits and a lesson's text. These texts link the names only, not the general words. The first build showed why: "the community kiln where she volunteers", in an edition's description, linked to the gallery's Volunteer page.

Three names join the list: "Gordon and Marion Smith Foundation for Young Artists", "Artists in Residence" and "Artist in Residence".

### 7. A crumb on the page, none in the data (low)

Nine pages show a crumb (DS-80): the five Foundation pages and the four residency pages. Their data had none, though every entry's page has both.

**Built (DS-184).** A page with a crumb says so in its data: Home, the page the crumb names, the page.

Fourteen Artists for Kids pages had no crumb at all. That was option A, done on 2026-09-29 for 13 of them (P-64): see "Since then".

### 8. Links that say only what they do (low)

"Register" led to 11 different forms and "See the edition" to 14 editions. In its row each is clear. In a screen reader's list of links, or to an engine that reads a link's words alone, they are all the same.

**Built (DS-185).** Each names its subject in words for screen readers: "Register: Curatorial Tour", "See the edition: Pender Harbour". Nothing changes on screen.

Left alone: a work's tile links by its title and year, so "Untitled, 1995" leads to ten works. The artist's name stands right above each, and the label is the museum's form (DS-16).

### 9. The menu is printed twice (note)

The header prints the menu for the drawer and again for the bar, and CSS shows one (DESIGN.md §6.1). So each page carries 57 header links to 28 places.

On Plan your visit, in the page as sent:

| Part | Size | Words |
| --- | --- | --- |
| Head (tags, data, Shopify's scripts) | 48 KB | |
| Header | 18 KB, of which the menu's second copy is 4 KB | 183 |
| Content | 7 KB | 271 |
| Footer | 46 KB, of which the three logos are 41 KB | 116 |

A search engine is not troubled by this. An agent that reads the page as text reads 183 words of menu before 271 words of content. Most agents skip to `<main>`, and the page has the landmarks they look for. Not built: see option C.

### 10. Pages with few links in from content (note)

| Page | Links in from other pages' content |
| --- | --- |
| About us | 0 |
| Frequently asked questions | 0 |
| Schools and teachers | 0 |
| Contact | 1 |
| Classes and camps | 1 |
| Four groupings of the collection | 1 each |

All but the FAQ are in the menu, and the FAQ is in the footer, so visitors find them. The links would have to come from page text, which is the gallery's. See option E.

Two pages end with no way on but the menu: Paradise Valley Summer Camps (its only links register for camp) and one residency page.

## Built

| Decision | What | Files |
| --- | --- | --- |
| DS-178 | An artist's page lists every exhibition that names the artist | `sections/gs-artist-exhibitions.liquid` |
| DS-179 | More exhibitions on a past exhibition: what's on now, then its neighbours in time. Amends DS-130 | `sections/gs-exhibition-more.liquid` |
| DS-180 | "Plan your visit" on an exhibition that is on now or coming up | `sections/gs-exhibition-hero.liquid`, `locales/en.default.json` |
| DS-181 | An edition links to its work in the collection; a work links to its lessons | `sections/gs-artwork-detail.liquid`, `sections/gs-work-detail.liquid`, `locales/en.default.json` |
| DS-182 | A page nobody links to, with nothing to read, is not listed | `snippets/meta-tags.liquid` |
| DS-183 | Names link in the texts about works, names only; three more names. Amends DS-175 | `snippets/gs-linked-names.liquid`, `snippets/gs-rich-text.liquid`, five sections, `config/settings_data.json`, `config/settings_schema.json` |
| DS-184 | A page with a crumb says so in its data | `snippets/gs-page-back.liquid` (new), `snippets/gs-data.liquid`, `snippets/gs-data-page.liquid` |
| DS-185 | A link that says only what it does names its subject for screen readers and engines | `snippets/gs-link.liquid`, `snippets/gs-event.liquid`, `sections/gs-work-detail.liquid` |
| DS-186 | The footer's Visit column links to Plan your visit | `sections/gs-footer.liquid`, `locales/en.default.json` |
| DS-187 | The links are checked by a script | `design-system/scripts/check_links.py`, `links.json`, `tests/test_check_links.py` |

New words, ours until the gallery says otherwise: "Plan your visit" (twice), "See this work in the collection", "Lessons".

## For Michael

Michael, 2026-09-29: "DS-178 to DS-187 approved, merge #118". All ten are decided as built. The options below, A to F, have no decision and stay unbuilt.

| # | Decision | Built as | Alternative |
| --- | --- | --- | --- |
| 1 | DS-178 | The artist's list and the exhibitions that name them | The artist's list only, kept by hand |
| 2 | DS-179 | On now, then the exhibition after and the one before | As it was: on now, then the two most recent. Or exhibitions that share an artist, which leaves the 12 exhibitions with no linked artist without neighbours |
| 3 | DS-180 | A button in the title box | A standalone link, quieter. Or nothing |
| 4 | DS-181 | A link under the archive note; a "Lessons" row in the work's facts | A panel on the edition's page, as the work has for its edition |
| 5 | DS-182 | Not listed | Link to them instead. They have nothing to read |
| 6 | DS-183 | Names only, in the texts about works | The general words too. They were wrong in the first text read |
| 7 | DS-184 | Data for the crumbs that show | |
| 8 | DS-185 | Hidden words after the label | Longer labels on screen |
| 9 | DS-186 | One link under the hours | |
| 10 | DS-187 | The check, run before a pull request that changes links and before release | |

### Not built: options

Options A and B were done on 2026-09-29. See "Since then".

| | Option | Why it isn't built | What it takes |
| --- | --- | --- | --- |
| A | Done for 13 of the 14, see "Since then". Crumbs on 14 Artists for Kids pages. After School Art, Day camps and Paradise Valley lead back to Classes and camps. Gallery program, Studio Art Academy, Learning guides, Learning kits, ArtReach videos, Professional development and Artists in Residence lead back to Schools and teachers. Those two, Awards and scholarships and Support Artists for Kids lead back to Artists for Kids | It is a store write: each page's Eyebrow field | Your go-ahead. The live theme doesn't read the field, so nothing shows before release. The theme needs no change: DS-80 and DS-184 do the rest |
| B | Built, see "Since then" (DS-188). Home links to the collection in its content. Home's content leads to the exhibition, the events, Artists for Kids, the editions, giving and visiting, but not to the collection, the site's largest part, or the Artists page | It changes what Home shows | A row of featured works, or a feature panel. A design decision |
| C | The menu printed once | The two copies are how the menu works without JavaScript at both widths. One copy needs the drawer and the bar to share markup | A rebuild of the header, tested on every browser. Gain: 4 KB and 85 words a page. Worth doing only with other header work |
| D | An exhibition names the artists of its works from the collection. Four exhibitions show works; their artists are named on the tiles, which lead to the works | It adds names to the gallery's list of artists | A row in the exhibition's facts, made from the works |
| E | Links in page text to About us, the FAQ, Plan your visit and Contact | The words are the gallery's | Sentences for the gallery to approve, staged as the other text changes are (DS-39). For example, the FAQ's answers on visiting, when written (`gallery-questions.md` 10.4), link to Plan your visit |
| F | The footer's logos as files. Three logos are 41 KB in every page | Not about links | Served as files, the browser keeps them. A small change to `gs-logo` |

## Since then

**2026-09-29, option A (P-64).** Michael: "Go ahead with option A, the crumbs on the 14 pages", then "Take the crumb off Professional Development, then merge #120". The Eyebrow field of 13 pages now names the page each belongs to, so each shows a crumb and says so in its data. A store write, logged in `proposals/store-writes/README.md` with its before-snapshot and how to undo it. No theme file changed, and the live site shows nothing different.

| | Before | After |
| --- | --- | --- |
| Pages with a crumb, on the page and in the data | 9 | 22 |
| Links in to Schools and teachers from other pages' content | 0 | 6 |
| Links in to Classes and camps | 1 | 4 |
| Paradise Valley Summer Camps' ways on, the menu apart | None | Its crumb |

Professional Development has no crumb. It is a programme in the Programming rows, which stay in one place from view to view (DS-146), and a crumb above its title moved them 33 px. The rows are its way around, as they are for the four public programmes. Its crumb was written with the others and taken off the same day.

A crumb names the page one step up. After School Art's data reads Home, Classes and camps, After School Art, without Artists for Kids between. The whole path would be a change to DS-184.

**2026-09-29, option B (DS-188).** Michael: "Go ahead with option B, Home links to the collection", then, after testing it on the review theme, "DS-188 approved, merge #122". Decided as built. Home has a new row after What's on, "From the collection": the first three featured works, the collection's size, and links to the Permanent Collection page and to Artists A to Z. A theme change only.

| | Before | After |
| --- | --- | --- |
| Links from Home's content to the collection's pages | 0 | 5: the Permanent Collection page, Artists A to Z and three works |
| Clicks from Home to the three featured works | 2, through the menu | 1 |
| Pages one click from Home | 38 | 41 |
| Pages three clicks from Home | 1,224 | 1,215 |

A row of works, not a feature panel: Home's rules allow it three listings and two panels, and it had two of each. The row sits after What's on, so the Artists for Kids panel is between it and the row of limited editions.

## For the gallery

| | Question |
| --- | --- |
| 1 | Two names on exhibition pages nearly match an artist entry: "Irene Whittome" (the entry is Irene F. Whittome) and "Leonhard Epp" (the entry is Leonard Epp). Which spelling is right? Once they match, the names link (`gallery-questions.md` 12.1) |
| 2 | Seven editions have no work in the collection that names them. Are they in the collection? |
| 3 | The names lists (DS-175, DS-183), with three more names |
| 4 | The new words: "Plan your visit", "See this work in the collection", "Lessons" |
| 5 | The 13 crumbs: is each Artists for Kids page filed under the right page (`gallery-questions.md` 12.5)? |
| 6 | The featured works: the first three now show on Home (`gallery-questions.md` 1.9). The words "From the collection" and "Browse the collection" (12.6) |

85 more names on exhibition pages have no artist entry, since the artists have no work in the collection. They stay plain text.

## The check

`python3 design-system/scripts/check_links.py <address>` reads every page and fails when:

1. a link leads to a page that doesn't answer, or a page shows a Liquid error;
2. a link in a page's content has no words;
3. a page that may be listed is more than three clicks from the home page;
4. an address in the sitemap may be listed and no page links to it;
5. no page's content links to an entry's page.

It reports, without failing, links that are sent on and pages with fewer than two links in from content. `links.json` holds the limits and the ten old pages that stay unlinked until release, each with its reason. After release that list is emptied.

| Theme | Result |
| --- | --- |
| Review theme before, `main` at 55fbe63 | 4 errors: the four addresses of finding 5 that are in the sitemap. 15 notes, among them 23 exhibitions with fewer than two links in |
| Review theme after, the branch at c4b8f22 | 0 errors, 14 notes, as the development theme |
| Development theme, this branch | 0 errors. 14 notes: the ten old pages, and the pages with fewer than two links in (4 pages, 4 groupings, the 4 policies and Search) |

## Tested

On the development theme (`184806277417`), rendered by Shopify:

- `check_links.py`: 1,627 addresses read (the four policy pages too), 0 errors. No link fails, none is without words, no Liquid error.
- Every exhibition's "More exhibitions" row read: 30 pages, three cards each, none its own. The oldest exhibition has two links in, every other three or more.
- All 21 editions read: 14 link to their work, every archive note links two names, no Liquid errors.
- Nine works with lessons read: each names its lessons.
- `check_structured_data.py` on seven pages of seven kinds: 0 errors.
- The exhibition's button and the footer's link at 1440 and 375 px: no sideways scroll; the footer's link is 44 px tall on touch.
- Theme Check: 0 offences. Linter: 0 errors, 0 warnings. `sync_theme.py --check`, `check_contrast.py` and every test pass.

## Limits

- The crawl reads what a visitor without an account sees. It doesn't read the cart, checkout or search results.
- Event pages answer 404 until the store shows events as pages, at release (DS-176). Their links are checked then.
- The 18 Artists for Kids pages and three Foundation pages are hidden from search engines until release (P-35). The check follows their links all the same.
- The numbers are of 2026-09-29. An exhibition's status changes with its dates, and so do its rows.
- Whether an engine ranks or cites a page more for these links can't be measured before release. The measures after release are in `proposals/aeo-geo-review.md` and `aeo/`.
