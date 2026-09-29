# Artists for Kids on gordonsmithgallery.com

Status: **Built, 2026-09-27; in review.** Michael approved every recommendation under "Decisions for Michael" (P-30 to P-40 in `DECISIONS.md`), and the team answered the first two questions: they can take down or cut back the old site's pages (T1), and they share one Shopify login (T2). Everything below is in the store and the theme, on the branch's pull request; the design choices it needed are DS-69 to DS-71, Proposed. A design review of the 20 pages followed (one reviewer a page, each finding checked by a second): its fixes are built, with DS-73 to DS-83 Proposed (DESIGN.md 0.6.28). What the build and the review changed from this plan is under "Build notes"; what's left is under "Still open".

Michael, 2026-09-27: the Artists for Kids site (artistsforkids.sd44.ca) should become part of gordonsmithgallery.com. "The parts we do not want to transfer is anything related to registration, everything else we believe we can integrate."

Revised the same day after a second pass from two sides: the visitor's, and the Artists for Kids team's, who run both systems ("Is what we're proposing both logical from the website experience for viewers as well as the people operating the site?"). What changed is under "What the second pass changed".

## Summary

- The old site was read in full on 2026-09-27, read-only: 48 pages, 68 images, 22 documents (PDF) and 31 videos. It runs on the school district's Terminalfour system.
- 42 pages hold content and 6 are registration forms.
- About a third of the content is already on gordonsmithgallery.com: the exhibitions, the history, Gordon Smith's biography, the contact details, the volunteer roles and the portfolio. Those pages don't move; a few facts from them go to the gallery as questions.
- What moves: the ten programmes, 27 video lessons, 9 learning guides, 4 learning kits with 8 lesson plans, 4 artist residencies, the team, 13 donors, 3 scholarships, the annual report, the program guide and the old home page's notices.
- Where: **Artists for Kids becomes a section of the main menu** (DESIGN.md §6.1 already allows for this), with the Artists for Kids page as its first item. Every new page uses the programme template with the Artists for Kids logo and colours, which are built.
- What stays behind: registration. It runs on three systems, and only one of them is the old website.
- **Every piece of information has one home.** The plan only works if the old site's moved pages come down at release. That is the team's and the district's to agree, and it is the first thing to settle.
- New structures: one entry type (Lesson) and one event field. Everything else reuses what the site has: page fields, card groups and events. Guides and lesson plans are cards that open their PDF.
- The store would gain 18 pages, about 27 lessons, about 21 PDFs, about 45 cards and about 5 events.

Today the site links to the old one in seven places, all on the Artists for Kids page: its button and its six programme cards. After this work it links there for After School Art and camp registration only.

## How registration works today

Read from the old site's pages. Nothing was submitted.

| Programme | How people sign up | System | Needs the old website? |
| --- | --- | --- | --- |
| After School Art | A form for each class (6 this term), on the class's own page | Terminalfour, the district's website | Yes |
| Spring and summer day camps, Pro D day camps | Not open yet ("Registration coming soon") | Not visible. Most likely the same as After School Art | Most likely |
| Paradise Valley summer camp | Opens February 3, 2027 | Not visible | Most likely |
| Gallery Program | A booking calendar | Outlook Bookings, in the district's Microsoft 365 | No |
| Professional development | A form for each workshop | Microsoft Forms | No |
| Learning kits | Two reservation forms | Microsoft Forms | No |
| Awards and scholarships | Closed for 2025/2026 | Not visible | Not known |
| Artists in Residence | None: teachers nominate students | | No |

Three things follow:

1. **The After School Art form asks for a child's name, school, guardians, emergency contact, medical conditions and learning support needs.** That information belongs in the district's systems. The site never collects it, and no form like it is built in Shopify. This is the strongest reason registration stays where it is.
2. **The form has no payment step.** How fees are collected after the form is sent can't be seen from outside. A question for the team.
3. **"Full" is typed by hand** into the schedule. Nothing counts places. So the schedule and the forms are edited together, by the same person, at the moment a class fills.

## The line between content and registration

Two rules:

1. **If it takes a booking, it stays in the system that takes it.**
2. **A schedule stays beside its forms.** Classes and camps keep their dates, fees, places, teachers and "full" on the district's page, next to the forms. One person changes both in one sitting on registration day. Split across two systems, the site would show "Register" on a class that filled an hour ago.

| Stays | Where |
| --- | --- |
| The After School Art forms, and the camp forms when they open | The district's website |
| The schedules for After School Art, day camps and Paradise Valley: dates, fees, places, teachers, status | The district's website, beside the forms |
| Registration opening dates, waitlists, cancellation and refund policies for those three | The same pages |
| Booking for school visits, sign-up for workshops, kit reservations | Microsoft 365, as today |

How the site sends people there:

- **After School Art and the camps:** one button on the programme page, "This term's classes and registration", to that programme's page on the district's site.
- **Gallery Program, workshops, kits:** the site links **straight to the booking calendar or form**. The old website isn't in the path at all. These pages carry their own term details (which exhibition, which dates), because the site is now their only home.
- Every link out carries the external arrow and "(external site)" automatically (NAV-04).

Donation links (CanadaHelps, SchoolCash Online) are not registration. They move, as external links.

## For visitors

| Visitor | Wants | Path |
| --- | --- | --- |
| A parent | What's on this term, when, how much, is there room | Menu, Classes and camps, then the registration link beside the programme. Three steps to the schedule |
| A teacher | Book a visit, borrow a kit, find a lesson, sign up for a workshop | Menu, Schools and teachers, the programme, then the form. Guides, lesson plans and videos open on the site |
| A student | Scholarships | Menu, Awards and scholarships |
| A supporter | Give | Menu, Support Artists for Kids, or Donate |

What a visitor can't know is which organisation runs what. Explore + Create, the family drop-in, is a Foundation programme under Programs; After School Art is under Artists for Kids. So the two link to each other: Public programs gets a card for Classes and camps, and Classes and camps gets a card for Explore + Create. Both are cards in groups the site already has. The order of the main menu stays as decided (P-29).

The way back: the district's registration pages link to gordonsmithgallery.com, as the old site's menu does today ("Shop Limited Editions").

## For the team

### Who edits where

| Task | How often | Where | Steps |
| --- | --- | --- | --- |
| A term's classes, forms, "full", waitlists | Three terms and the camps | The district's website | As today |
| A term's notices: registration is open, a new guide, the residencies | A few each term | The site: the "This season" cards on the Artists for Kids page | Edit a card: image, title, text, link. As the old home page's promotions today |
| A workshop or tour for educators | About 11 a year | The site: one Event entry, with the Microsoft Forms address as its link | 1. It leaves every list by itself once it has ended |
| Gallery Program's term text and booking link | Twice a year | The site: the page's text | 1 |
| A video lesson | A few a year | The site: one Lesson entry | 1, with its cover image |
| A learning guide or lesson plan | About 5 a year | The site: the PDF and its cover in Files, a card (its link is the PDF's address, copied from Files), then the card group | 4 |
| A residency | About 4 a year | The site: a page, its photos, a card, the year's card group | 4 |
| What a programme is | Rarely | The site: the page's text and fields | 1 |
| Booking and sign-up forms | As today | Microsoft 365 | As today |

After release the team keeps three kinds of page on the district's website: After School Art, the camps, and their forms. Everything else is on the site. The team works in the same three systems as today (the website, Microsoft 365, Shopify for the shop and exhibitions); the work moves from the first to the third.

Two tasks take four steps, because a group's cards are a list kept on the group (Liquid can't find entries by a field's value). They are rare, and the staff editing test covers them.

### What the old site's pages become

This part is the team's, in Terminalfour. It is content editing, not DNS: the old site shows the team an "Edit this page" link. It happens at release, not before.

| Old pages | Become |
| --- | --- |
| After School Art, Spring & Summer Day Camps, Paradise Valley Summer Camps | Kept, cut down to the schedule, the forms and the policies, with a link to the programme's page on the site for the rest |
| The 6 class forms | Kept |
| The other 36 content pages | Taken down, or replaced by one line and a link to the new address |
| The old home page | A short list of what's open for registration, and a link to the site |
| The old menu | Registration, and a link to the site |

Why it matters: if the old pages stay up, every text exists twice and one copy goes stale; search engines keep sending people to the old copy; and a parent who follows the registration link lands in the old site's full menu. The integration then changes little for anyone.

### Questions for the team

| # | Question | Why | Answer |
| --- | --- | --- | --- |
| T1 | Can the team take down or cut back the old site's pages, or does the district's web team decide? | Decision 1 depends on it | The team can (Michael, 2026-09-27) |
| T2 | Who on the team has a Shopify login, and does the store's plan have a seat for each person who needs one? | P-12 names one admin account | One shared login; the people who need it can log in and make changes (Michael, 2026-09-27). It is the admin account in P-12 |
| T3 | How are fees collected after a registration form is sent? | The form has no payment step. It may change what the programme pages should say |
| T4 | How do camps and scholarships take registrations when they open? | Not visible today |
| T5 | Do the Microsoft Forms and the booking calendar get a new address each year? | If so, the link on the site changes with them |
| T6 | Who updates the old home page's promotions today, and how often? | They would keep the "This season" cards |

## Where each page goes

New addresses are proposals. Each old address has one new home, so the district can forward its addresses later if it chooses to.

### Home and About

| Old page | What it holds | Goes to |
| --- | --- | --- |
| Home | Five promotions: the exhibition opening, the 2026 Spring Portfolio, After School Art registration, the program guide, the residencies | "This season", a card group at the top of the Artists for Kids page, which the team keeps up as it keeps the old home page. The exhibition and the portfolio are already on the site's home page |
| About | The Gallery's opening in 2012 and Gordon Smith's life | Nothing moves. Gordon and Marion tells his life in newer words, and About Us covers the Gallery. "Opened its doors in 2012" is on neither; a question for the gallery |
| Who We Are | The Artists for Kids history, the programmes, the collection, the Foundation, the Spring Portfolio, the team | The Artists for Kids page (`/pages/artists-for-kids`). Its opening and history are already there (P-24). New: two paragraphs on how the print programme began, for the History section as written, and "Meet the Artists for Kids team" (four portraits with names and roles as cards, like the Foundation's board: built 2026-09-28). The rest repeats pages the site has |
| Annual Report | One PDF, 2024 to 2025 (14.3 MB) | A document on the Artists for Kids page |
| 2026-2027 Program Guide | One PDF (1.5 MB) | The Artists for Kids page's button, in place of "Artists For Kids Website" |
| Contact Us | The three organisations' addresses, phones, emails and hours | Nothing moves. Contact and Plan your visit hold these. Four differences go to the gallery (below) |

### Learn

| Old page | Goes to | What moves | Sign-up |
| --- | --- | --- | --- |
| Learn | The Artists for Kids page and two group pages | Its three headings become three card groups: Community programs, School programs, Learning and teaching resources | |
| After School Art | `/pages/after-school-art` | What the classes are, who teaches them, the important notes, bursaries, the photo | Button to the district's page, which keeps the schedule, fees, forms and cancellation policy |
| Spring & Summer Day Camps | `/pages/day-camps` | What the camps are, the photo | Button to the district's page, which keeps the dates, schedule and cancellation policy. The 2026 camps are past |
| Paradise Valley Summer Camps | `/pages/paradise-valley-summer-camp` | What the camp is, bursaries, the four camp films (2022 to 2025), the photo | Button to the district's page, which keeps the 2027 dates, fee and cancellation policy |
| Gallery Program | `/pages/gallery-program` | All of it: what the programme is, the Grade 5 and K to 12 visits with their term details, schools outside the district, self-guided tours and their instructions (a PDF, once the gallery sends it). The exhibition's text isn't copied: the page links to the exhibition | Straight to the booking calendar |
| Artists-in-Residence | `/pages/artists-in-residence` | What the programme is, and the eight residencies of 2025 to 2027 as cards, one group for each school year | None |
| Four residency pages (Amelia Butcher, Mark Johnsen, Becky Bair, Sara-Jeanne Bourget) | `/pages/artist-in-residence-<name>` | The workshop, the biography, past workshops, the photos. Amelia Butcher and Mark Johnsen have artist pages on the site, so theirs link to them | |
| Studio Art Academy | `/pages/studio-art-academy` | All of it, with its note that the academy isn't offered in 2026/2027 | None |
| Learning Guides | `/pages/learning-guides` | 9 guides as cards with their covers, each opening its PDF, under the old page's two headings | |
| Learning Kits, and its four kit pages | `/pages/learning-kits` | One page: the four kits (clay, collagraph, trace monotype, gel plate) as cards with their photo, text and reservation link, then each kit's lesson plans as a card group of their own, 8 in all, each opening its PDF. The two kit videos are lessons (below) | Straight to the two reservation forms |
| ArtReach Videos | `/pages/artreach-videos`, and a page for each lesson at `/pages/lessons/<name>` | 27 lessons as Lesson entries: title, video, what we're making, what inspired it, grade levels, the questions. The copyright note closes the list page | |
| Professional Development, and its 11 workshop pages | `/pages/professional-development` | The opening line. The workshops with a date become events, each tied to its exhibition: 5 today. The 6 without a date wait for one | Each event's link, straight to its form |

### Visit and Support

| Old page | What it holds | Goes to |
| --- | --- | --- |
| Visit | *Collect, Assemble, Gather* and four past exhibitions | Nothing moves. All five are exhibition entries on the site |
| Support | Four short parts pointing at the pages below | Nothing moves |
| Ways to give | Why to give, and two ways: CanadaHelps and SchoolCash Online | A new page, Support Artists for Kids (`/pages/support-artists-for-kids`), linked from Donate. These gifts go to the school district, not the Foundation, so they don't join the Foundation's Donate page |
| Our Donors | The thanks, a donor's quote, 13 donors with a paragraph each | The same page: the quote as a pull quote, the donors as text cards with their links |
| Volunteer | A recruiting line and a link to the site's own Volunteer page | Nothing moves. The email `sgvolunteer1@gmail.com` isn't on the site; a question for the gallery |
| Awards and Scholarships | Three $1,000 awards, each with a requirements PDF | `/pages/awards-and-scholarships`: the three awards as points, each with its requirements PDF. It links to the Foundation's own scholarships, which are different awards |

### Not pages

| What | Goes to |
| --- | --- |
| The old site's footer: X, Facebook, Instagram, YouTube | The social links in Theme settings, once the gallery confirms them (`gallery-questions.md`, ACCESS-03) |
| The district's links (Parents, Mail, Staff, NVSD Website) and the site search | Nothing moves |
| "Shop Limited Editions" in the old menu | It already points at this site |

## The menu

Artists for Kids changes from a link to a section (DS-11: the section is a button, its main page is the first link inside). The order of the main menu stays as decided (P-29).

| Item | Destination | Holds |
| --- | --- | --- |
| About Artists for Kids | `/pages/artists-for-kids` | This season, every programme in three groups, the history, the team, the annual report |
| Classes and camps | `/pages/classes-and-camps` | For families. After School Art, Spring and summer day camps, Paradise Valley summer camp, each with its registration link in the page's opening, and a card for Explore + Create |
| Schools and teachers | `/pages/schools-and-teachers` | For educators, in two groups. School programs: Gallery Program, Artists in Residence, Studio Art Academy. Learning and teaching resources: Learning guides, Learning kits, ArtReach videos, Professional development |
| Awards and scholarships | `/pages/awards-and-scholarships` | |
| Support Artists for Kids | `/pages/support-artists-for-kids` | Ways to give, the donors |

The items are named for who they serve, because a parent can't tell whether After School Art is a "community" or a "school" programme. The old site's three headings stay as the headings of the card groups. Each card is entered once and shown on its group page and on the Artists for Kids page. The gallery confirms the labels (EXH-04).

Made in the review menu (`new-theme-main`) first; the live menu follows at release. The footer's Explore menu keeps its Artists for Kids link.

## How it's stored

Reused as built:

| Need | Uses |
| --- | --- |
| 18 new pages | The programme template (`page.programme`) for the programme, group, awards and support pages; the standard page template for the four residency pages. Page fields: hero image, hero caption (the photo credits), intro, programme (Artists for Kids), call to action |
| This season, the programme groups, the team, the donors, the residencies by year | Card and card group entries (P-16) |
| Educators' workshops and tours | Event entries (P-16), tied to their exhibition, so they also show on the exhibition's page |
| PDFs | Files, opened from cards (a card whose link is a PDF shows its cover whole, like a document) or from links in the text, as the Foundation's annual report is. 21 |
| Camp films | Video in the page text (DS-53) |

New:

| Structure | What it is | Why |
| --- | --- | --- |
| **Lesson** entry (`lesson`), with a page at `/pages/lessons/<name>` | Title, video address, what we're making, what inspired it, works from the collection (a list of artwork entries), grade levels, the questions (a list), cover image | The old page holds 27 videos with their text on one page and grows through the school year. As entries, staff add a lesson by filling fields, each video loads on its own page, and a lesson can link to the works that inspired it in the Permanent Collection |
| Event field for the home page | True or false: keep this event off the home page's What's on | Six places on the home page shouldn't fill with workshops for teachers. They still show on Professional development, on their exhibition and on Upcoming events |

Theme work: the lesson list and lesson page, cards that open a PDF, and the home page's event filter. Design system first: they go into `DESIGN.md` and `preview.html` as Proposed decisions.

Files: 68 images, less the ones the store already has and the placeholders, each with alt text. 21 PDFs. Five are over Shopify's 20 MB limit, and one gave no size:

| Document | Size |
| --- | --- |
| Clay Tile Kit lesson plan | 26.5 MB |
| Lessons from Art Camp, Sara-Jeanne Bourget 2025 | 24.9 MB |
| Make Mini Monster, lesson by Lexy Ho-Tai | 23.7 MB |
| Charcoal Stencil Prints inspired by Sara-Jeanne Bourget | 23.4 MB |
| Gel Plate Monoprint Kit lesson plan | 22.0 MB |
| Zine Making Workshop using Frottage with Annie Canto | Not reported |

## Found while reading

For the gallery. The text moves as written (AGENTS.md, "Gallery-facing work"); these go into `proposals/gallery-questions.md` when the work starts.

| # | Where | What |
| --- | --- | --- |
| 1 | Contact Us, against the site | Artists for Kids office hours: 8:30 to 4:30 on the old site and on Contact, 8:00 to 3:00 on Plan your visit |
| 2 | Contact Us | The Foundation's phone (604.998.8563), "by appointment", and the summer closure (June 23 to September 18, 2026) aren't on the site |
| 3 | Contact Us | The Foundation's email reads `admin@smithfoundation.ca` but opens a message to `info@smithfoundation.ca` |
| 4 | Who We Are | The Paradise Valley photo is dated 1994 here. The site has 1994 and 1996 (gallery question 3.8) |
| 5 | Who We Are | The sentence about the ceremonial drum and more than 100 artists is here too (gallery question 3.6) |
| 6 | Gallery Program | The self-guided tours text names *Collect, Assemble, Gather*, then "our spring exhibition, One Hundred Artists Deep" and "April through June". The Spring 2027 text repeats the fall's, Grade 5 and dates included |
| 7 | Gallery Program | The self-guided instructions PDF is on the district's old intranet and didn't open. The gallery sends the file |
| 8 | Gallery Program, Visit, Home | Samuel Roy-Bois, *My Sun*: 2024 in the caption, 2025 in the image's description |
| 9 | Learning Guides | "Creating a Paper Mural with Sandeep Johal" has a cover and no file |
| 10 | ArtReach Videos | 28 players for 27 lessons: the clay video appears twice, once above the trace monotype lesson |
| 11 | Visit | *The Art of Conversation* offers a 3D tour, but the page has no link to it |
| 12 | Names | "Sara Jean Bourget" (Paradise Valley) and "Sara-Jeanne Bourget"; "Mark Johnson" once on Mark Johnsen's page; "Elizabeth MacIntosh" and "McIntosh"; "Becky" and "Rebecca" Bair; "Artist for Kids" three times |
| 13 | Throughout | "AFK" in public text ("AFK Learning Kits", "AFK ArtReach Videos"). The brand guide says to write "Artists for Kids" (DESIGN.md §2) |
| 14 | Home, Visit | Two links to the Gallery's site are broken: they open `artistsforkids.sd44.ca/gordonsmithgallery.com` |
| 15 | Studio Art Academy | Not offered in 2026/2027. Does the gallery want the page on the site this year? |
| 16 | Awards, and The Smith Foundation | Two sets of three scholarships. The pages should say how they differ |

## Decisions for Michael

Michael approved every recommendation on 2026-09-27 ("Decisions for Michael: all recommendations are approved"). They are P-30 to P-40 in `DECISIONS.md`.

| # | Decision | Recommended | The other way |
| --- | --- | --- | --- |
| 1 | What the old site becomes at release | The team cuts it back to registration: three programme pages, their forms, and links to the site. Settle this with the team (T1) before building | The old site stays as it is. Every text then exists twice, and the plan is better cut down to the teaching resources, which the old site does worst |
| 2 | Do class and camp schedules come over? | No. A schedule stays beside its forms, so dates, fees and "full" are changed in one place at the moment a class fills | Bring classes and camps over as events, each with a Register link. About 35 entries a year, and two systems to change on registration day |
| 3 | Where sign-up links point | Straight to the booking calendar or form where it stands alone (Gallery Program, workshops, kits). To the district's page only for After School Art and the camps | Every link to the district's page, which then has to stay up for all seven programmes |
| 4 | The menu | A section of five items, two of them for an audience: Classes and camps, Schools and teachers | Three group pages under the old site's headings; or no group pages, with the groups as headings on the Artists for Kids page |
| 5 | The team's notices | "This season" cards at the top of the Artists for Kids page, kept by the team | No notices on the site. Registration dates are then announced only on the district's site |
| 6 | New pages before release | Make them now so they can be reviewed: published with a title only, hidden from search engines and the sitemap (`seo.hidden`), their text staged in `custom.release_body` as DS-39 does. Under the live theme each is a bare title at an address nothing links to. This is a new kind of store write and needs its own go-ahead; try it on one page first | Create the pages at release. They can't be reviewed in the review theme before then |
| 7 | ArtReach videos | Lesson entries with their own pages | One page with 27 videos in its text, as today |
| 8 | Educators' events on the home page | Kept off the home page's What's on | Shown everywhere events show. No new field |
| 9 | Links to artists' own websites on the residency pages | None, as on artist pages (DS-63). Link to the artist's page on this site where there is one | Keep the four website links |
| 10 | "AFK" in the moved text | Written out in titles, labels and headings. In body text, the gallery approves each change | Left as written |
| 11 | PDFs over 20 MB | We make smaller copies and the gallery checks they read well | Ask the gallery for smaller copies, as with the collection's documents |

## Steps

One branch and one pull request: the pieces depend on each other, and Michael reviews them together on the review theme. Each step is its own commit. Store writes follow Michael's go-ahead of 2026-09-27 ("let's get started on implementation"), each with a before-snapshot and an undo step, logged in `proposals/store-writes/README.md`.

1. **Agree the split.** Done 2026-09-27: the team can cut back the old site (T1).
2. **Decide.** Done 2026-09-27: P-30 to P-40.
3. **Export.** A read-only script, `proposals/store-writes/artists-for-kids/inventory.py`, saves the old site as it is on the day: each page's text, images, PDFs and video addresses. Review sheets for the gallery come from it.
4. **Design.** The lesson card, the lesson page and cards that open a PDF, in the design system, as Proposed decisions for Michael.
5. **Definitions.** The Lesson entry type and the event field.
6. **Files.** Images with alt text, PDFs, the smaller copies.
7. **Entries.** Lessons, cards and card groups, events.
8. **Pages.** The 18 pages and their fields, as decision 6 sets out. The Artists for Kids page's new history paragraphs join its staged text.
9. **Theme.** The lesson list and page, cards that open a PDF, and the section in the review menu. The Artists for Kids page's cards and button point at the site's own pages. The two cards that link Public programs and Classes and camps.
10. **Checks.** Theme Check, the linter and its tests, contrast, sync, 1440, 768 and 390, every moved link, and the fonts audit on the new pages.
11. **Staff test.** A member of the team adds a lesson, a learning guide, an event and a "This season" card in the review theme ("Who edits where").
12. **Records.** `REQUIREMENTS.md` (NAV-03 and NAV-04 change: the external pathway becomes registration only), `DESIGN.md` §6.1 and §7.4, the content model, `proposals/store-changes.md` and the release backlog.

## At release

Added to the release change set (`proposals/store-changes.md`):

- The 18 pages: their template (`release.py templates`: programme, or the standard one for the residencies), their staged text into the page (`staged`), then `seo.hidden` off (`unhide`).
- The live menu gains the Artists for Kids section with the rest of the menu.
- The lesson pages go live with the theme: until then their addresses return 404 under the live theme, like the exhibitions and the collection.
- The team cuts the old site back the same day ("What the old site's pages become"), from the list of old and new addresses in the tables above. Until it does, the site's registration links still work: they point at pages that exist today.
- Rollback: hide the 18 pages. Entries and files can stay; nothing in the old theme reads them. The team's changes to the old site are theirs to undo; Terminalfour keeps page versions.

Forwarding the old addresses and DNS stay the district's, as with the catalogue (P-27).

## What the second pass changed

| First plan | Now | Why |
| --- | --- | --- |
| "The other system" was one system | Three: the district's website, Microsoft Forms and Outlook Bookings | Only After School Art has forms on the old website. The rest never needed it |
| Every programme's button went to its page on the old site | Four programmes link straight to their form or calendar | One step fewer for teachers, and four old pages that no longer have to stay up |
| What happens to the old site was the last decision, and the district's | The first decision, and the team's to make with the district | Without it every text exists twice |
| Three group pages under the old site's headings | Two, named for families and for educators | A parent can't place After School Art under "community" or "school" |
| The old home page's promotions didn't move | "This season" cards | The team had nowhere on the site to say registration is open |
| Gallery Program's term details stayed behind | They move with the page | Its booking is a calendar, so the site is the page's only home |
| No account of the team's work | "Who edits where" and the team's questions | The plan has to work for the people who keep it up |
| 19 pages | 18 | One group page fewer |

## Build notes

What the build changed from the plan above, and why. Each is small; none changes a decision.

| Plan | Build | Why |
| --- | --- | --- |
| A new page field, Documents, showing Document entries as tiles after the text | Cards that link to the PDF. A card whose link is a PDF shows its image whole on the mat, as a document tile does, and says "(PDF)" | Card groups have headings, so the guides keep their two groups and each kit keeps its own lesson plans. The team already uses cards, and the Foundation's annual report already works this way. One new structure fewer |
| The pages get their template at release | New pages get the programme template (or the standard one) when they're made | They're new, so there's nothing to reassign. Under the live theme, which has no programme template, they fall back to its plain page template and show their title only (decision 6) |
| The copyright note closes the ArtReach page | The note is in Theme settings and shows under every lesson's video and at the end of the list | Every lesson page has a video, so every lesson page needs the note. Typed once |
| New pages show "a bare title" on the live site | They carry the live theme's On Now template name until release | The live theme's default page template carries the About page's content, so a page it didn't know showed About's text under the new title (found on the test page, L-09). The On Now template shows the title only. The release script renames them |
| A lesson list section on the programme template | The page text section lists the lessons on the page chosen as ArtReach videos page | As the visit details on Plan your visit (DS-61), so the list shows before release too, when the page has its bridge template name. One section fewer |
| Residency cards titled "Spring 2027 \| Becky Bair", as the old site | "Becky Bair, Spring 2027" | The bar wrapped to the start of a line; the name first reads better beside the poster |
| Registration buttons "This term's classes and registration" | "Register for classes", "Register for camps", "Register for camp", "Register a Grade 5 class" | Verb first, one to three words (§6.2), after the design review. The gallery confirms the labels (`gallery-questions.md` §3) |
| Classes and camps holds only Artists for Kids' programmes | A second group, "Also for families", holds Explore + Create | Explore + Create is the Foundation's; it can't sit under Artists for Kids' Community Programs heading |
| Donate links to Support Artists for Kids | A fourth card in Donate's "How to give" | The page's other ways to give are cards; the new one uses the old site's own sentence about Artists for Kids |
| Support Artists for Kids on the programme template | The standard page template, with a "How to give" group (CanadaHelps, School Cash Online, phone) after its text | As Donate: the ways to give end the page. On the programme template the group would have split the giving text from the thanks to donors |
| Day camps and the About page link on to other programmes through the menu | Day camps ends with "More classes and camps"; About Artists for Kids gets "Awards and support"; Sara-Jeanne Bourget's page shows her two learning guides | Each page ends with somewhere to go next (design review) |
| Notes typed as separate lines ("5 days, 4 nights, inclusive", "not offered this year", "Applications have closed") | The page's intro, under the title | They're what a visitor needs first; the intro is the page field for it |
| Registration and the annual report as plain links in the text | Standalone links (DS-82) | A section's one action, at a touch target's size |

## Still open

- The gallery's and the team's answers: `proposals/gallery-questions.md` §6 (text corrections for Gallery Program, two missing PDFs, names, "AFK" in body text, the lessons' works, the new labels, and T3 to T6).
- Michael's review of DS-69 to DS-71 and DS-73 to DS-83 on the review theme once the pull request merges, and his choice on the rules the design review proposed but didn't build: DS-72 (a 58ch measure), DS-79 (pictures stay in the reading order on phones), DS-81 (the rule-colour hover fill), DS-70a (three lesson options), and Q12 (the Foundation logo and the navigation from 1200 to 1400 px).
- Held from the design review for a later pass across the site: the hero title's measure token, the hero photo's corner below 990 px, and the standalone link's arrow following its last word.
- Focal points to set by hand in Files: the Paradise Valley camp photo `pvssa_25` at about 50% across, 75% down; the 2026 residency hero at about 30%, 35%.
- The undated educators' workshops (a curator's tour of *Against the Latitude of "Progress"*, four printmaking kit introductions, portfolio building): events once they have dates.
- At release: templates, staged text, `seo.hidden` off, and the team's cut-back of the old site ("At release").
