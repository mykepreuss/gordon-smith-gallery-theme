# The main menu and how the site is organised

Status: **Decided by Michael and built, 2026-09-28** ("Proceed with implementing this new navigation and IA"). Recorded as P-50 to P-57 and DS-132 to DS-134 in `DECISIONS.md` (the mapping is under "Decisions for Michael"); what was built is under "Built". The review below is kept as it was argued.

Michael, 2026-09-28: "What we have currently is fine but my gut says we can improve it." Then, on the first draft, which gave Visit its own place in the menu: "Consider Visit moving into About", with MoMA, Gagosian and the Vancouver Art Gallery to look at. This version follows that: Visit stays in About, and the header says when the gallery is open. Then: "I like Exhibitions as a plain link and the recommendation for the new navigation makes a lot of sense." So Exhibitions is a plain link too. Then: "What about Artists for Kids moving into Programs?" See "Artists for Kids in Programs" (N10). Then: "We're also planning on adding 3 new pages associated with the Gordon and Marion Smith Foundation: Scholarships, Brilliance Gala, Supporters." See "Three new Foundation pages" (N11 to N13). And on the sketch of the menu: "This looks good but 'Gordon and Marion' doesn't seem right." See "Gordon and Marion Smith" (N14).

This review is about structure: what the menu holds, what it calls things and in what order. How the header looks and behaves was reviewed in the whole-site design review (pull request #43, DS-91, DS-97, DS-98, DS-103, DS-104) and isn't repeated here.

## Summary

The menu works, and four of its seven sections are already named for what visitors come to do: Exhibitions, Collection, Programs, Shop. The other three are named for who runs things: About (the Gallery), Artists for Kids, Smith Foundation. That second group is where the menu makes visitors think:

- Giving is in three sections, and the founders' story is under the Foundation.
- The two longest labels in the bar are the two organisations' names, and the bar is full.

The recommendation keeps the menu at seven items and keeps everything that was decided for good reasons: one button per section, Exhibitions first, Collection as it is, Artists for Kids under its own name, Plan your visit in About. It changes three things and adds one:

1. Support takes the Smith Foundation's place, with both ways to give and Volunteer.
2. The Foundation's page and Gordon and Marion join About.
3. Exhibitions and Shop become plain links, because their pages already carry their own navigation.
4. New: today's opening line in the header's utility row, linking to Plan your visit.

The menu keeps two levels. The Foundation's three pages don't become a third level: see "The Foundation's pages".

One further step is proposed on top of this (N10): Artists for Kids moves into Programs as a headed group, which brings the menu to six items. The seven-item menu below stands if N10 isn't taken.

Three Foundation pages are on their way: Scholarships, Brilliance Gala and Supporters. They fit without a new section: the gala and the supporters in Support, the scholarships in Programs beside Artists for Kids' awards (N11 to N13).

No page moves and no address changes.

## The menu today

The review menu (`new-theme-main`) as it stands on 2026-09-28, with the Artists for Kids section (P-33) and Upcoming events from the two open pull requests (#42, #43):

| Section | Items |
| --- | --- |
| Exhibitions | On now, Upcoming, Past exhibitions |
| Collection | The collection, Artists |
| Programs | Public programs, Upcoming events, Speaker series, Music at the Smith, Explore + Create, Art in Good Company |
| About | About the gallery, Plan your visit, Volunteer |
| Artists for Kids | About Artists for Kids, Classes and camps, Schools and teachers, Awards and scholarships, Support Artists for Kids |
| Smith Foundation | About the Foundation, Gordon and Marion, Donate |
| Shop | Limited editions, and the five portfolios |

Utility row: Contact, Search, Cart. Footer, Explore: Exhibitions, Limited editions, Artists for Kids, Frequently asked questions.

Seven sections, 28 links, and every section is a button that opens a dropdown (DS-11), so every page is two clicks from anywhere.

## The evidence

### Visitors

Shopify's analytics, 2026-03-01 to 2026-09-20. The days since are left out: they are mostly our own review and checking (95% desktop, and pages that exist only in the new theme).

| | |
| --- | --- |
| Sessions | About 4,100 |
| Start on the home page | 2,763 (67%) |
| On a phone | 960 (23%) |
| Arrive from the school district's sites (sd44) | 585 (14%) |
| Arrive from Google | 212 (5%) |
| Arrive from the Foundation's old site | 102 (2%) |
| Start on Plan your visit | 8 |
| Start on Donate | Fewer than 3 |

- Two in three visits start on the home page, so most people find their way with the menu. It carries more weight here than on a site people reach through search.
- Artists for Kids' audience is a large share: one visit in seven comes from the school district's sites, before the Artists for Kids site has moved in.
- Almost nobody arrives on Plan your visit or Donate directly. People who want them have to find them on the site.
- The store's search (56 searches) is nearly all artists' names and prints: "gordon smith", "robert davidson", "russna kaur", "all artists". A few look for people: "board of directors", "staff", "volunteers".

### The three sites Michael named

Read in a browser on 2026-09-28, with each dropdown's contents.

| | MoMA | Gagosian | Vancouver Art Gallery |
| --- | --- | --- | --- |
| Main menu | Visit, Exhibitions and events, Art and artists, Store | Exhibitions, Artists, Fairs & Collecting, Quarterly, News, Locations, Shop, Premieres | Visit, What's On, Learn, Support, About, Shop, Future Gallery |
| Dropdowns | Three; Store is a plain link | None: all eight are plain links | Six; Future Gallery is a plain link |
| Beside the menu | Membership, Donate, Tickets | Subscribe, Search | Today's hours beside the logo; Search, Become a member, Donate, Book tickets |
| Visit | 12 pages: tickets, hours, map, tours, restaurants, accessibility, families | "Locations", sixth | 6 pages: tickets, passes, hours, dining, groups, rentals |
| Opening times | "The museum is open 10:30 a.m. to 5:30 p.m. today" under the home page's first image, and in the footer | On each location's page | "Today's hours: 10 AM to 5 PM" in the header of every page |
| Support | Buttons beside the menu | None | Membership, Volunteer, Donate |
| About | Footer only | Footer only: About the Gallery, About Larry Gagosian | About Us, History, Vancouver Art Gallery Foundation, reports, leadership |
| Footer | About us, Support, Research, Teaching, address, today's hours | About, press, jobs, social links | The main menu again, contact, the week's hours |

What they show:

1. **Visit is a main item where visiting is a section of its own.** MoMA's holds 12 pages and the Vancouver Art Gallery's 6, and both sell tickets. Ours is one page of 272 words, admission is by donation, and there is nothing to book. The Polygon Gallery, the nearest gallery of a similar size, keeps Plan your visit under About. Visit in About is the right size for this gallery.
2. **Both museums answer "are you open?" outside the menu.** The Vancouver Art Gallery puts today's hours in the header of every page; MoMA puts them under the first image and in the footer. Neither makes a visitor open a menu to find out. This is the part worth borrowing, and the theme already works the line out (`snippets/gs-open-today.liquid`: "Open now until 4 PM", "Closed today. Open Thursday, 12 to 4 PM").
3. **Where the art is the point, the art comes first.** Gagosian opens with Exhibitions and Artists. The two museums open with Visit because they sell tickets. That supports Exhibitions first (P-09) and Collection second.
4. **None names a section for an organisation.** The Vancouver Art Gallery's Foundation is a page under About. Gagosian's founder has a page beside About the Gallery, as Gordon and Marion would.
5. **The Vancouver Art Gallery's Support section is Membership, Volunteer, Donate.** Nearly the section proposed here.
6. **Plain links land on pages that do their own wayfinding.** Gagosian has no dropdowns at all, and MoMA's Store is a plain link. Our Shop page and our exhibition lists already carry their own navigation.
7. **Both museums put the events calendar with the exhibitions** ("Exhibitions and events", "What's On"). Ours is under Programs. See "Options considered".

### Eight galleries, the wider survey

Home pages read on 2026-09-28: the Polygon Gallery, Vancouver Art Gallery, Audain Art Museum, MoMA, Contemporary Art Gallery, Surrey Art Gallery, Tate, and the Art Gallery of Ontario (its home page couldn't be read, so its ticketing site's menu stands in).

| | |
| --- | --- |
| How many items | 4 to 7, most often 5 or 6 |
| The order most share | Visit, What's on or Exhibitions, Art or Collection, Learn, Support, About, Shop |
| Visit | Its own item at 7 of 8. Under About at the Polygon |
| Support | A main item or a button beside the menu at every one |
| Shop | Always in the main menu, last or near last, mostly a plain link |
| A foundation | Never a main item: under About at Vancouver Art Gallery, Audain and Surrey |
| A named education programme | Under the learning item by its own name (Tate Kids, the Polygon's Kids First) |
| Organised by who runs it | Only the two city galleries, which inherit their city's menu |

### The bar's width

Measured on the review theme at 1200 px, the narrowest width that shows the bar, with the Gallery's logo:

| Menu | Width used, of 1,012 px | To spare |
| --- | --- | --- |
| Today's seven sections | 1,011 px | 1 px |
| The proposed seven items | 886 px | 126 px |

The labels are shorter, and Exhibitions and Shop have no chevron. The room matters most on Foundation pages, where the wider logo wraps the bar on 1280 and 1366 px laptops (DS-97).

## What works and stays

- One button per section, the main page first inside it (DS-11). It fixed the old menu's mixed behaviour.
- Exhibitions first (P-09), and its three lists: On now, Upcoming, Past, with the switcher between them (DS-13).
- Collection with Artists beside it (P-26). The search data agrees: people look for artists by name.
- Artists for Kids under its own name. Parents and teachers know it, and they are a large share of visitors.
- Plan your visit in About, second, where it is today.
- Contact, Search and Cart in the utility row (DS-29).
- The home page. It already speaks in the visitor's terms: What's on, For kids, families and schools, New limited editions, Support art education, Visit. The menu is the part that doesn't yet.

## Findings

1. **The menu mixes two ways of sorting.** Exhibitions, Collection, Programs and Shop are things to see and do. About, Artists for Kids and Smith Foundation are organisations. A visitor has to know which of the three runs something to find it.
2. **Giving is in three places.** Donate is under Smith Foundation, Support Artists for Kids under Artists for Kids, and Volunteer under About. The two gifts go to different bodies (the Foundation, and the school district for Artists for Kids), which is a good reason to show them side by side where the difference can be seen.
3. **The header doesn't say when the gallery is open.** The gallery is open three afternoons a week, so it is the first thing a visitor needs to know. Today the answer is on the home page, in the footer and on Plan your visit, two clicks into About.
4. **Smith Foundation is the weakest section.** It holds three pages, its label is the longest in the bar, and the page most people want from it is Donate. No gallery looked at gives a foundation a main item.
5. **About is told in three sections.** About the gallery, About Artists for Kids and About the Foundation each sit in a different dropdown, and Gordon and Marion, the story behind the gallery's name, is under the Foundation.
6. **Two dropdowns repeat what their pages already do.** The Shop page shows the portfolios as cards and each portfolio has the switcher. The dropdown lists them a third time, and staff must add to it twice a year. The content inventory found the same problem in the old theme: hand-picked lists go stale. Exhibitions' dropdown holds the same three links as the switcher on On now, Upcoming and Past, so the page most people want, what's on now, takes two clicks where one would do.
7. **The footer's Explore list is short.** Four links. The footer is where people look for what the menu doesn't show, and it has room.

Already covered elsewhere: pages below the menu (After School Art, the residencies, lessons) get a link back up and mark their section in #43 (DS-80, DS-91).

## The proposed menu

| # | Item | Type | Holds |
| --- | --- | --- | --- |
| 1 | Exhibitions | Link | On now (`/pages/on-now`). Its switcher leads to Upcoming and Past |
| 2 | Collection | Section | The collection, Artists |
| 3 | Programs | Section | Public programs, Upcoming events, Speaker series, Music at the Smith, Explore + Create, Art in Good Company |
| 4 | Artists for Kids | Section | About Artists for Kids, Classes and camps, Schools and teachers, Awards and scholarships |
| 5 | Support | Section | Give to the Smith Foundation (`/pages/donate`), Give to Artists for Kids (`/pages/support-artists-for-kids`), Volunteer (`/pages/volunteer`) |
| 6 | About | Section | About the gallery (`/pages/about-us`), Plan your visit (`/pages/plan-your-visit`), Gordon and Marion Smith (`/pages/gordon-and-marion`), The Smith Foundation (`/pages/the-smith-foundation`) |
| 7 | Shop | Link | Limited editions (`/pages/shop`) |

Utility row: today's opening line, then Contact, Search, Cart.

Seven items, 21 links (19 in dropdowns, and the two plain links). Exhibitions and Shop take one click instead of two.

### Today's opening line in the header

The first thing in the utility row, on every page: "Open now until 4 PM", "Open today, 12 to 4 PM" or "Closed today. Open Thursday, 12 to 4 PM". It links to Plan your visit.

- It comes from the opening days and times in Theme settings, the one source for the gallery's hours (DS-96), so staff change nothing new.
- In the Menu drawer it sits with the utility links.
- Without JavaScript it shows the week's hours ("Open Thursday to Saturday, 12 to 4 PM"), as the home page's line does.
- Holidays and one-off closures aren't known to it, as today. Plan your visit carries those.

### What moves

| Page | From | To |
| --- | --- | --- |
| Donate | Smith Foundation | Support, first item |
| Support Artists for Kids | Artists for Kids | Support |
| Volunteer | About | Support |
| About the Foundation | Smith Foundation | About, as "The Smith Foundation" |
| Gordon and Marion | Smith Foundation | About, as "Gordon and Marion Smith" |
| The five portfolios | Shop's dropdown | Out of the menu. The Shop page and the portfolio switcher list them |
| Upcoming, Past exhibitions | Exhibitions' dropdown | Out of the menu. The switcher on On now leads to both, with their counts |

### The Foundation's pages

Michael, 2026-09-28: "Would the subpages currently part of Smith Foundation become 3rd level links in the nav then?"

No. The menu keeps two levels, and the three pages become second-level links in two sections:

| Page | Section | Label |
| --- | --- | --- |
| The Smith Foundation (`/pages/the-smith-foundation`) | About | The Smith Foundation |
| Gordon and Marion (`/pages/gordon-and-marion`) | About | Gordon and Marion Smith |
| Donate (`/pages/donate`) | Support | Give to the Smith Foundation |

Why not a third level under About:

- The theme shows two levels on purpose (`snippets/gs-nav.liquid` ignores a third). A third needs a menu that opens sideways from a menu, which is hard to hold with a mouse and slower on a phone and a keyboard.
- None of the three sites has one: MoMA and the Vancouver Art Gallery stop at two levels, Gagosian at one.
- It would rebuild the grouping by organisation inside About, and put Donate three levels down.

What keeps the three together:

- Each still carries the Foundation's logo and colours (DS-47).
- The Foundation's page is their hub. It links to Gordon and Marion in its text and to Donate from its Donations card and its button (checked on the review theme, 2026-09-28).
- Missing today: Gordon and Marion and Donate have no link back to the Foundation's page. Proposed: each gets "The Smith Foundation" as its eyebrow, which the theme turns into a link back (DS-80, in #43). A field value on two pages, which the live theme doesn't read.

Three more of the Foundation's pages are planned. They get places in the menu by what they are for, and the Foundation's page stays the hub for all of them: see "Three new Foundation pages".

### Artists for Kids in Programs

Michael, 2026-09-28: "What about Artists for Kids moving into Programs?"

It finishes what the rest of the proposal starts: Artists for Kids is the last organisation's name on the bar. With it in Programs the menu is the six items most galleries share: Exhibitions, Collection, Programs, Support, About, Shop.

What speaks for it:

- **The gallery already presents its programs as one.** Its printed guide is "The Gordon Smith Gallery 2026-27 Program Guide", one guide for all of them. The Public programs page has a card for Artists for Kids classes and camps, and Classes and camps has one for Explore + Create ("Also for families"). The two hubs point at each other today (checked on the review theme, 2026-09-28).
- **"Programs" is Artists for Kids' own word.** Its page groups them as Community programs and School programs.
- **A parent needn't know who runs what.** Explore + Create is a family program under Programs; After School Art is one under Artists for Kids.
- **It treats the two organisations alike.** The brand guide makes the Gallery the umbrella over both (p.2). With the Foundation inside About and Support, Artists for Kids alone on the bar would be the odd one out.
- **The other galleries do it.** A named education programme sits under the learning item by its own name: Tate Kids under Learn, the Polygon's Kids First under Engagement.

What it costs:

- **The name leaves the bar.** Parents and teachers are a large share of visitors, and the name is what they know. It becomes the first thing they see when Programs opens, one click in. Its pages keep the Artists for Kids logo in the header, the home page keeps its Artists for Kids panel, and the footer keeps its link.
- **The dropdown is the hard part.** Programs has six links and Artists for Kids four. One plain list of ten, kids' classes beside talks for adults, wouldn't say who each is for.
- **How the Artists for Kids team sees it.** They run their own pages, and this changes where their name sits. Michael's to judge.

Two ways to do it:

| | A panel with two headed groups (recommended) | One short list |
| --- | --- | --- |
| Programs holds | Upcoming events. Then "Public programs": Speaker series, Music at the Smith, Explore + Create, Art in Good Company. Then "Artists for Kids": Classes and camps, Schools and teachers, Awards and scholarships | Upcoming events, Public programs, Classes and camps, Schools and teachers, Awards and scholarships, About Artists for Kids |
| Links | 10, all in view when Programs opens | 6 |
| The four series | Stay in the menu | Leave it, reached from the Public programs page |
| The name Artists for Kids | A heading that links to its page | One item, last |
| Who each is for | The headings say it | The labels must: "Classes and camps" alone doesn't say kids |
| What it needs | A new panel pattern in the design system and `gs-nav.liquid` | Menu edits and new labels |

The recommendation is the panel. Each heading is a link to its hub page, so "About Artists for Kids" isn't needed as an item. The order of preference: the panel, then Artists for Kids staying on the bar (the seven-item menu above), then the short list, which hides both the gallery's series and the name.

A headed group is not a third level in the sense of "The Foundation's pages": nothing opens from inside the panel, and every link shows at once. It does use the menu editor's third level to draw the groups, so `gs-nav.liquid` would read three levels where it reads two today. MoMA's and the Vancouver Art Gallery's panels work this way (12 links under Visit, 10 under Learn).

The menu with N10:

| # | Item | Type | Holds |
| --- | --- | --- | --- |
| 1 | Exhibitions | Link | On now. Its switcher leads to Upcoming and Past |
| 2 | Collection | Section | The collection, Artists |
| 3 | Programs | Section, two groups | Upcoming events. Public programs: the four series. Artists for Kids: Classes and camps, Schools and teachers, Awards and scholarships |
| 4 | Support | Section | Give to the Smith Foundation, Give to Artists for Kids, Volunteer |
| 5 | About | Section | About the gallery, Plan your visit, Gordon and Marion Smith, The Smith Foundation |
| 6 | Shop | Link | Limited editions |

Six items, 21 links. At 1200 px the bar uses 690 of 1,012 px.

### Gordon and Marion Smith

Michael, 2026-09-28, on the sketch of the menu: "This looks good but 'Gordon and Marion' doesn't seem right."

The label was written for its old section. Under Smith Foundation, the section's name gave the surname and said who they were. Under About it is two first names between Plan your visit and The Smith Foundation, and a new visitor can't tell who they are.

| | Today | Proposed |
| --- | --- | --- |
| Label in the menu | Gordon and Marion | Gordon and Marion Smith |
| Reads with | Smith Foundation, the section above it | The Smith Foundation, the item below it |

The page's own title stays "Gordon and Marion" until the gallery says otherwise: a title shows on the live site, so it changes at release, and the wording is the gallery's (EXH-04).

Not proposed: "Our founders" or "Our story". The page doesn't call them founders of the gallery, and an Our Story page has just left the site (P-25).

**The two pages about Gordon Smith don't know each other** (checked on the review theme, 2026-09-28):

| Page | Holds | Missing |
| --- | --- | --- |
| Gordon and Marion (`/pages/gordon-and-marion`) | His life and Marion's, 340 words, and the film | Any link: to his works, his editions, or anywhere else |
| Gordon Smith, the artist (`/pages/artists/gordon-smith`) | 60 works, his documents, his editions in the Shop, his exhibitions | His biography, and a link to his story |

"gordon smith" is the most searched name on the site. Someone who finds either page should find the other. Proposed: the artist's page links to the story, and the story links to his works in the collection. His words aren't changed; the story gains one link after its text.

The page keeps the Foundation's logo (DS-47): the words are the Foundation's, from its old site.

### Three new Foundation pages

Michael, 2026-09-28: "We're also planning on adding 3 new pages associated with the Gordon and Marion Smith Foundation: Scholarships, Brilliance Gala, Supporters."

What each holds, from the old Foundation site's export (`smithfoundation.co`, its pages last changed June to August 2026):

| Page | Holds | Who comes for it | What they do |
| --- | --- | --- | --- |
| Scholarships | Three $2,500 Young Artist Scholarships for graduating Grade 12 students in North Vancouver, West Vancouver and Vancouver, each with its form. Applications closed on April 24, 2026 | Students, their teachers and parents | Apply |
| Brilliance Gala | The gala and auction (March 11, 2026; 2025 and 2023 before it), its co-chairs, the call for artists. Its proceeds support Artists for Kids | Guests, sponsors, donors, artists giving work | Buy a seat, sponsor, give |
| Supporters | The Foundation's thanks and its donors by level of giving, about 1,650 words of names | Donors, and people deciding whether to give | Read, be thanked |

Where each goes:

| Page | Section | Why |
| --- | --- | --- |
| Brilliance Gala | Support | It is a way to give. When it has a date it is also an event, so it shows in Upcoming events and on the home page's What's on |
| Supporters | Support, last | It is the thanks that follows giving. Artists for Kids' donors are already on its own giving page |
| Scholarships | Programs | Students come for it, not donors. The old site filed it under Fund, which is how the Foundation sees it, not how an applicant looks for it |

Support then holds five: Give to the Smith Foundation, Give to Artists for Kids, Brilliance Gala, Volunteer, Supporters.

**The scholarships meet Artists for Kids' awards.** Artists for Kids' page, Awards and scholarships, offers three $1,000 awards to graduating Grade 12 students of the North Vancouver School District. So the site will hold six awards for the same students on two pages from two organisations, open and closed in the same season. A North Vancouver student can apply for four of them. It is the giving problem again: the student shouldn't need to know who runs which.

| | A. A third group in the Programs panel (recommended) | B. One page for all six | C. Each with its organisation |
| --- | --- | --- | --- |
| In the menu | "Scholarships and awards": Smith Foundation scholarships, Artists for Kids awards | One link, Scholarships and awards | Scholarships under Support, Awards and scholarships under Artists for Kids |
| The pages | Two, as planned. Each links to the other | One, the two organisations' words under their own headings | Two |
| A student sees both | Yes, side by side | Yes, on one page | Only by following a link |
| Needs | N10's panel, with a heading that isn't a link | The gallery and Artists for Kids to agree on one page, and whose logo it carries | Nothing new |

Recommended: A. Each organisation keeps its page, its words and its logo, and the student finds both under one heading. The Artists for Kids group then holds Classes and camps and Schools and teachers. If N10 isn't taken, Scholarships is the last item in Programs and Awards and scholarships stays with Artists for Kids.

**Two ways to every Foundation page.** Someone who thinks of the task finds each page in the menu. Someone who thinks of the Foundation finds all six from its page:

- The Foundation's page has cards for the gala and the scholarships already, without links. They get their links, and Supporters gets a card or a link from Donate, which promises a donor list.
- Each new page carries the Foundation's logo and colours (the programme field) and "The Smith Foundation" as its link back (N9).
- A Foundation page marks its own section in the menu: the gala and Supporters mark Support, Scholarships marks Programs.

Addresses, as `proposals/smith-foundation-site.md` proposes them: `/pages/smith-foundation-scholarships`, `/pages/brilliance-gala`, `/pages/smith-foundation-supporters`. The pages themselves are separate work. They would be made as the Artists for Kids pages were (P-35): published with their title only, hidden from search, their text staged until release, word for word from the old site.

The menu with N10 to N12:

| # | Item | Type | Holds |
| --- | --- | --- | --- |
| 1 | Exhibitions | Link | On now. Its switcher leads to Upcoming and Past |
| 2 | Collection | Section | The collection, Artists |
| 3 | Programs | Section, three groups | Upcoming events. Public programs: the four series. Artists for Kids: Classes and camps, Schools and teachers. Scholarships and awards: Smith Foundation scholarships, Artists for Kids awards |
| 4 | Support | Section | Give to the Smith Foundation, Give to Artists for Kids, Brilliance Gala, Volunteer, Supporters |
| 5 | About | Section | About the gallery, Plan your visit, Gordon and Marion Smith, The Smith Foundation |
| 6 | Shop | Link | Limited editions |

Six items, 24 links.

**Does this bring back a Smith Foundation section?** Six pages would fill one. The reasons against it are the ones in the findings, and the new pages add one: a section by organisation would put the scholarships where students don't look and the gala apart from the other ways to give. The Foundation is more present in this menu than in today's, not less: it is named in Support, About and Programs, and three of Support's five pages are its own.

### What doesn't change

- Every page, its address and its content. Nothing is hidden, merged or redirected by this proposal.
- The three organisations keep their pages, logos and colours. A Foundation page still carries the Foundation's logo (DS-47).
- Collection and Programs, the three exhibition lists and their switcher, and Plan your visit's place in About.
- How the menu behaves (DS-11, DS-19).
- The Artists for Kids page keeps its own link to Support Artists for Kids, and the Foundation's page its link to Donate.

### The order

Exhibitions, Collection, Programs, Artists for Kids, Support, About, Shop. What the gallery offers comes first, then how to help and who it is, then the Shop. It is the Vancouver Art Gallery's order from Learn onwards (Learn, Support, About, Shop).

It differs from P-29 in one place: About moves from fourth to sixth, after Support. If About should stay fourth, P-29's order holds with Support in the Foundation's place: Exhibitions, Collection, Programs, About, Artists for Kids, Support, Shop.

### Labels

The labels are proposals, and the gallery confirms them (EXH-04). Two are new wording: "Give to the Smith Foundation" and "Give to Artists for Kids". They say where each gift goes, which "Donate" and "Support Artists for Kids" side by side would not.

### The footer

Explore lists each section's main page, so the whole site is one click from the foot of every page: Exhibitions, Collection, Programs, Artists for Kids, Support, About, Shop, Frequently asked questions. Visit and Contact already have their own footer columns.

## Options considered

| Option | What it is | Why not |
| --- | --- | --- |
| A. Leave it | The seven sections as decided (P-29, P-33) | It works. The findings above stay |
| **B. By what visitors do, Visit in About (recommended)** | The proposed menu above | |
| C. Visit as its own item | The first draft: a plain Visit link in the main menu, eight items | A main item for one page. The opening line in the header answers the question sooner, and the menu stays at seven |
| D. Six items, by joining exhibitions and programs | What's on (exhibitions, events and programs together), Collection, Artists for Kids, Support, About, Shop | Closest to MoMA and the Vancouver Art Gallery. But it takes the word Exhibitions out of the menu |
| **E. Six items, Artists for Kids in Programs (recommended on top of B)** | "Artists for Kids in Programs", N10 | |

Also considered and not proposed:

- **A third level in the menu** for the Foundation's pages. See "The Foundation's pages".
- **Upcoming events with the exhibitions**, as MoMA and the Vancouver Art Gallery have it. It would rename the first section "Exhibitions and events", the longest label in the bar. The home page's What's on row already shows both together.
- **A Donate button beside the menu**, as both museums have. Support in the main menu does the job, and the header stays quiet.
- **Renaming Artists for Kids "Learn".** The name is known, and its audience arrives looking for it.
- **Listing a page in two sections** (Support Artists for Kids under both Artists for Kids and Support). One home for each page keeps the menu short. The Artists for Kids page links to it.

Not part of this proposal: the Engage page is published and in no menu. The gallery decides whether to keep it (`proposals/content-migration.md`).

## What it takes to build

Small, and the menu can be put back.

| Where | Change |
| --- | --- |
| Store | Two new menus for the new structure, beside the two review menus, set only in the development theme while it's built. The review theme switches to them when the pull request merges; `new-theme-main` and `new-theme-explore` stay unchanged until then, for rollback. Editing the review menus in place would change the review theme before its code can show the new shape: today's `gs-nav.liquid` drops the Programs panel's groups. A store write: Michael's go-ahead, a before-snapshot and a line in `proposals/store-writes/README.md`. The live menu follows at release, as already planned |
| Design system, then theme | The opening line in the utility row: its style in `components.css` and `preview.html`, its place in `DESIGN.md` §6.1, then `snippets/gs-header.liquid`. A design decision, recorded as Proposed |
| Store, page fields | The eyebrow "The Smith Foundation" on Gordon and Marion and on Donate, for the link back. The same kind of store write, with its own before-snapshot |
| Theme, `snippets/gs-nav.liquid` | The rule that marks a section for pages the menu can't list (DS-91, in #43) reads a section's dropdown. It needs to read a plain link too: an exhibition, and the Upcoming and Past lists, mark Exhibitions; a limited edition or portfolio marks Shop. A page below the Foundation's page marks About: today the rule looks only at a section's first page |
| With N10: design system, then theme | The panel with headed groups: `components.css`, `preview.html`, `DESIGN.md` §6.1, then `snippets/gs-nav.liquid` reads the menu's third level as groups, in the bar and in the drawer. A page below Artists for Kids marks Programs. A design decision, recorded as Proposed |
| Theme, styles | The last two dropdowns open leftwards. Check that still holds with About second to last and Shop a plain link |
| Checks | The bar at 1200, 1280, 1366 and 1440 px with each of the three logos; the drawer at 390 px; keyboard; without JavaScript; the opening line on an open day, a closed day and after closing |
| Records | `DESIGN.md` §6.1, `proposals/store-changes.md` §1 and §2, `DECISIONS.md`, the NAV-02, EXH-01, EXH-02 and ACCESS-02 rows in `REQUIREMENTS.md` |

### Effect on the live site

Checked 2026-09-28 against the live site (theme `183162372393`, Colorblock, role main):

- Its header reads `new-website-menu-1`, not the review menus. The only store fields it reads are two product fields (`custom.featured_frame`, `custom.featured_product`, in `baseline/theme/`): no page fields and no entries.
- So the menus, the theme code, the labels, the opening line, the eyebrows, the Foundation's card links and the story's staged text change nothing it shows.
- The one trace: a new page exists at its address on the live site too. The Artists for Kids pages show how that looks (P-35): `/pages/classes-and-camps` on the live site is its title and nothing else, marked `noindex,nofollow`, linked from nowhere. The three Foundation pages would be the same. Their addresses are free today (404).
- Waiting for release, as the plan's "Store writes before release" says: the live menu, page titles, unhiding the new pages and moving their staged text in.

Order of work: after #42 and #43 merge, because both change the menu, `gs-nav.liquid` and the opening hours' source. Then one branch and one pull request for this.

## Decisions for Michael

All decided by Michael, 2026-09-28, as recommended ("Proceed with implementing this new navigation and IA"), with Exhibitions as a plain link (N8) and Artists for Kids in Programs as groups (N10, option A for the scholarships). In `DECISIONS.md`:

| Here | Recorded as |
| --- | --- |
| N1, N6 | P-50 (the order: Exhibitions, Collection, Programs, Support, About, Shop) |
| N2 | P-54 and DS-132 |
| N3, N11 | P-53 |
| N4, N14's label | P-54 |
| N5 | P-55 |
| N7 | P-56 |
| N8 | P-51 and DS-134 |
| N9, N10, N12 | P-52 and DS-133 |
| N13, N14's links | P-57 |


| # | Decision | Recommendation |
| --- | --- | --- |
| N1 | Sort the menu by what visitors come to do. The organisations keep their pages, logos and colours | Yes (option B) |
| N2 | Visit stays in About. Today's opening line goes in the header's utility row, linking to Plan your visit | Yes |
| N3 | Support replaces Smith Foundation as a section: the two ways to give, and Volunteer. Support Artists for Kids leaves the Artists for Kids section (changes P-33) | Yes |
| N4 | About holds About the gallery, Plan your visit, Gordon and Marion Smith and The Smith Foundation | Yes |
| N5 | Shop is a plain link to the Shop page; the portfolios leave the menu | Yes |
| N6 | The order: Exhibitions, Collection, Programs, Artists for Kids, Support, About, Shop (changes P-29: About moves after Support) | Yes. Or keep P-29's order, with Support in the Foundation's place |
| N7 | The footer's Explore list names every section's main page, and Frequently asked questions | Yes |
| N8 | Exhibitions is a plain link to On now; Upcoming and Past are reached from its switcher (changes P-15's three links) | Michael's choice, 2026-09-28 ("I like Exhibitions as a plain link") |
| N9 | No menu opens from inside a menu. Gordon and Marion and Donate get a link back to the Foundation's page | Yes |
| N10 | Artists for Kids moves into Programs as a headed group beside Public programs; the menu has six items (changes P-33 and P-29) | Yes, as the panel with two groups. If not the panel, Artists for Kids stays on the bar |
| N11 | Brilliance Gala and Supporters join Support, which holds five. The gala is also an event when it has a date | Yes |
| N12 | Scholarships goes in Programs, in a group "Scholarships and awards" with Artists for Kids' awards; each organisation keeps its own page | Yes (option A). The gallery and Artists for Kids may prefer one page (B) |
| N13 | The Foundation's page is the hub for its six pages: its cards link to them, and each links back | Yes |
| N14 | The menu says "Gordon and Marion Smith". The story and Gordon Smith's artist page link to each other | Yes. The gallery confirms the label |

## Built

2026-09-28, on branch `claude/site-nav-ia-review-8925d4`, after #42, #43 and #44 merged.

- **Menus:** `new-theme-main-2` and `new-theme-explore-2`, new, read only by the new theme (`sections/header-group.json`, `footer-group.json`). The review menus stay as they were until this merges, so the review theme keeps a working menu. `proposals/store-writes/navigation.py`; log in `proposals/store-writes/README.md`.
- **Theme:** groups in a dropdown (DS-133) and plain links marked as the current section (DS-134) in `snippets/gs-nav.liquid`; today's opening line in the utility row (DS-132) in `gs-header.liquid` and `gs-open-today.liquid`; the artist's About page link in `sections/gs-entry-head.liquid`. Styles in `design-system/components.css`, shown in `preview.html`.
- **Store fields:** the artist field About page, set for Gordon Smith; "The Smith Foundation" as the eyebrow on Donate and Gordon and Marion; Gordon and Marion's button to his works.
- **Not built here:** the three Foundation pages. They belong to `proposals/smith-foundation-site.md`, which is still waiting for Michael's decisions; when they're made they join the menu where §1 of `proposals/store-changes.md` says, and the Foundation page's gala and scholarship cards get their links.
- **Checked** on the development theme: the bar at 1200 with each programme's logo and at 1280, 1366 and 1440, one row each time; the drawer at 768 and 375; the keyboard at 1200; 33 pages for the current section. Theme Check, the linter and its tests, contrast and sync pass. The live site is unchanged.

### Since then

- 2026-09-29: About gets a fifth item, About Artists for Kids (`/pages/about-artists-for-kids`), after The Smith Foundation. The history and the team moved there from the Artists for Kids page, which keeps its programmes (P-65). Its label says "About" because Programs already has an "Artists for Kids" that goes to the main page.
