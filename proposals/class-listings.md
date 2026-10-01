# Class and camp listings: each class on the site, with its own Register link

Date: 2026-10-01. Status: **a proposal, for Michael's decision.** Nothing is built and nothing in the store changed.

Asked for by the gallery, in a note on its answers of 2026-10-01 (`proposals/gallery-answers/2026-10-01-answers.md`, last lines), and set aside by Michael as a project of its own (P-67). Michael, 2026-10-01: "Write the class listings proposal".

## What the gallery asked for

> Registration for camps and other Artists for Kids programs should have all the specific info about each camp offering (times, teacher, theme, ages) on the Artists for Kids page with links that bypass the sd44 landing page entirely and each would go right to each registration page directly.

Its example: After School Art on this site should hold the table that is on the district's After School Art page, and each class should link to its own registration page, such as `artistsforkids.sd44.ca/learn/after-school-art/wonderful-watercolours/`.

## What a parent does today

1. Opens After School Art on this site. Reads what the programme is. Sees no classes, dates or fees.
2. Presses "Register for classes (external site)". Lands on the district's After School Art page, which repeats the same introduction.
3. Scrolls to the table, picks a class and presses Register.
4. Lands on that class's page, which holds the form.

Three pages and two sites before a form. The middle page adds only the table. The same holds for the day camps.

## What the district's pages hold

Read on 2026-10-01. Nothing was submitted.

| Programme | Listed now | What each row gives | Its Register link |
| --- | --- | --- | --- |
| After School Art | 6 classes for fall 2026 | Name, a description, "8 Tuesdays from Oct. 13 to Dec. 1", the time, grades, fee ($200 or $230), teacher, the school and room, and a status | The class's own page on the district's site, which is the form |
| Pro D day camps | 4 camps, October 2026 to April 2027 | Name, grades, "Max: 18 campers", teacher, date, time, cost ("TBD"), place, status ("Registration coming soon") | None yet |
| Spring and summer day camps | Weeks for 2027, not open | The same kind of row | None yet |
| Paradise Valley summer camp | One camp: July 5 to 9, 2027, $960 | Dates, fee, ages, when registration opens (February 3, 2027), the cancellation dates | None yet |

So a term is about 6 classes, a year about 4 Pro D camps, a handful of camp weeks and one summer camp. About 25 rows a year.

Two facts from the earlier review still stand (`proposals/artists-for-kids-integration.md`, "How registration works today"):

- **The forms ask for a child's name, school, guardians, medical conditions and support needs.** They stay on the district's site. Nothing here moves a form.
- **"Full" is typed by hand.** Nothing counts places.

## This changes a decision

On 2026-09-27 Michael decided that schedules stay on the district's pages, beside their forms (P-31), and that After School Art and the camps link to the district's page, not past it (P-32). The reason was one risk: with the schedule in one place and the forms in another, the site could show "Register" on a class that filled an hour ago.

The gallery now asks for the opposite, and it runs the programme. The risk is real but small, and it can be handled (see "Keeping it true"). This proposal replaces P-31 and amends P-32 for After School Art and the camps. Everything else in them stands.

## Three ways to do it

| | A. A class entry (recommended) | B. A table typed into the page | C. Read the district's page automatically |
| --- | --- | --- | --- |
| What it is | A new kind of entry, "Class", like Event. The page lists its programme's entries | Staff retype the table in the page's text each term | A script copies the district's table to the site each day |
| For the team | A short form for each class. Copy last term's and change it | Editing a table in the text editor, which is fiddly, more so on a phone | Nothing, but the district's page must stay as it is, which is the page the gallery wants to bypass |
| For the visitor | A designed list that works on a phone, a Register button for each class, and a class drops off by itself when it ends | Whatever the table looks like. Wide tables scroll sideways on phones | Up to a day out of date |
| A class that has ended | Leaves the list on its last day | Stays until someone deletes it | Follows the district's page |
| For search and answer engines | Each class can be given as data: name, dates, ages, fee, where | Text only | Text only |
| To build | The entry, the list on three pages, the data | Nothing | A scheduled job outside Shopify, and it breaks when the district changes its page |

**Recommended: A.** It is how events already work, so the team learns nothing new, and it is the only one that tidies itself. B is the fallback if the team would rather type a table. C keeps the page the gallery wants gone.

## The Class entry

One entry for each class or camp. The fields follow the district's own columns.

| Field | Example | Notes |
| --- | --- | --- |
| Name | Wonderful Watercolours | |
| Programme page | After School Art | Which page lists it: After School Art, Day camps or Paradise Valley |
| Description | "Welcome to the vibrant world of watercolours! …" | The team's own words, as on the district's page |
| When | 8 Tuesdays, October 13 to December 1 | A line of text, as the team writes it today. "No class on Nov. 11" goes here |
| Time | 3:00 to 4:30 PM | Text |
| First day and last day | 2026-10-13, 2026-12-01 | Two dates. They put the list in order and take the class off the list after its last day |
| For | Grades 3 to 5 | Text: grades or ages |
| Fee | $230 | Text, so "TBD" works |
| Teacher | Caroline Falconer | |
| Where | Boundary Elementary, Room 011 | Text |
| Places | 18 | Optional ("Max: 18 campers") |
| Status | Open | One of: Open, Full, Waitlist, Opens soon, Closed |
| Opens on | September 11, 2026 | Optional, shown with "Opens soon" |
| Register link | The class's own form page | The button shows only when the status is Open or Waitlist |

No picture: the district's rows have none, and 6 pictures a term is work nobody asked for. No page for each class: the form's page is the class's page.

## What the visitor sees

**After School Art.** Under the introduction, a heading for the term ("Fall 2026 classes") and the classes in date order. Each is a block:

- the name;
- one line of facts: when, time, grades, fee;
- teacher and place;
- the description;
- **Register** (external site), or a plain "Full", or "Registration opens September 11".

Then "Important Notes", bursaries and the rest, as now. With no class entries, the page shows what it shows today: the introduction and one button to the district's page. So the page never looks empty between terms.

**Day camps.** The same list, under two headings as the district has them: Pro D day camps, and Spring and summer day camps.

**Paradise Valley.** One block at the top of the story: the next camp's dates, fee, ages and when registration opens. The page's own text has these typed in today; they would move to the entry, so they are changed in one place.

**Classes and camps, and the Artists for Kids page.** No change in the first step. The "Fall 2026 at Artists for Kids" cards (P-34) stay hand-kept. Drawing them from the entries is a later step, if the team wants it.

On a phone each block is one column, the button full width and 44 px tall. No table, so nothing scrolls sideways.

The design is new: a "class list" component in the design system, close to the event row (DESIGN.md §6.13), decided as Proposed design decisions when it is built. No new colours or type sizes.

## Keeping it true

The risk P-31 named: the site says "Register" after a class has filled.

| Guard | How |
| --- | --- |
| The form's page is the last word | Each class's page on the district's site still says when it is full. A parent who gets there late is told so there, as today |
| One person, one sitting | Whoever marks a class full on the district's site changes its status on this site in the same sitting. It is one dropdown on one entry |
| A class can't outlive its dates | After its last day it leaves the list by itself. Before registration opens it says so, with the date |
| A fallback that needs nobody | If the team prefers, the site shows no status at all: every class has a Register button, and the form's page says if it is full. Less helpful, never wrong |

The second guard is the one that matters, and it depends on the team. That is the first question below.

## What happens to the district's site

- **Each class's form page stays.** It is where registration happens.
- **The landing pages** (After School Art, Day camps) are no longer in the path. The team can cut each back to one line and a link to this site, as P-30 already plans, or leave them. If they stay, the table lives in two places, and the two will drift. Recommended: cut them back.
- **Each term** the team makes the new classes' form pages on the district's site, as today, then makes the entries here with those addresses.

## For search and answer engines

Each class can be given as an event in the page's data: its name, first and last day, place, the organiser (Artists for Kids), ages and fee. "After school art classes in North Vancouver for grade 4" is then a question the site answers by itself. It is a small addition once the entry exists, and it follows the events' own data (DS-154). Whether Google shows anything special for it was not looked into; it is there for answer engines first.

`check_answers.py` gains a question: "What art classes are on this term, and how do I register?"

## Questions for the team

The first four are open since 2026-09-27 (`proposals/gallery-questions.md` 6.9 to 6.12). None stops the build; 1 and 2 shape it.

| # | Question | Why |
| --- | --- | --- |
| 1 | Who will keep the classes up to date on this site: make them each term, and mark one full when it fills? | The whole proposal rests on it. If nobody can promise the second half, the site shows no status (the fallback above) |
| 2 | Does each class get a new form page each term, with a new address? | It seems so. Then last term's entries can't be reused as they are, only copied |
| 3 | How are fees collected after a form is sent? (6.9) | The site says nothing about payment. One line under the list may be due |
| 4 | How do the camps and Paradise Valley take registrations when they open: a form page each, like the classes? (6.10) | Their Register links don't exist yet |
| 5 | Is there a waitlist, and how does a parent join it? | Whether "Waitlist" is a status worth having |
| 6 | Should a class that is full stay on the list, marked Full, or leave it? | The district's page keeps it. Recommended: keep it, so parents see what ran |

## Decisions for Michael

| # | Decision | Recommended |
| --- | --- | --- |
| 1 | Replace P-31, and amend P-32: class and camp schedules move onto this site, each with a link straight to its own registration page | Yes: the gallery asks for it |
| 2 | How: a Class entry (A), a typed table (B), or an automatic copy (C) | A |
| 3 | Status on the site (Open, Full, Waitlist, Opens soon), or a Register button alone | Status, if the team answers question 1 with a name. Otherwise the button alone |
| 4 | Where first | After School Art, since its 6 classes are open now. Day camps and Paradise Valley follow when their registration opens |
| 5 | The district's landing pages are cut back to a link, once this site lists the classes | Yes, by the team (P-30) |
| 6 | Classes as data for search and answer engines | Yes, with the first step |
| 7 | Who types in the first 6 classes | The agent, from the district's page, word for word, with Michael's go-ahead for the store write. The team takes over from the next term |

## Steps, once decided

1. **Design system:** the class list component, in `DESIGN.md` and the preview, as Proposed decisions.
2. **Content model:** the Class entry's definition (`design-system/proposals/content-model.md`), then created in the store. A new definition changes nothing a visitor sees.
3. **Theme:** the list on the programme template, the entry's data, the answers check's new question. On a branch, against the development theme.
4. **Entries:** the 6 fall classes, written while the live theme can't show them yet.
5. **Review:** on the review theme, with the team if they can. The staff editing test (still open, `gallery-questions.md` 1.10) can use this: make a class, mark it full.
6. **Release**, on Michael's approval. After School Art's button to the district's landing page goes when the list shows.
7. **A page of instructions for the team:** making a term's classes, marking one full. Half a page.
8. **Day camps and Paradise Valley** when their registration opens: entries only, no new code.

## What this is not

- No form on this site. No child's details are collected here.
- No payments, no counting of places, no waitlist system. Shopify could sell a class as a product, but the forms' medical and guardian questions don't belong in a shop's checkout.
- No change to the Gallery Program, workshops or learning kits. They already link straight to their booking calendar or form (P-32).
