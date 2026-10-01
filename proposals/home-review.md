# The home page: how to make it more engaging

Date: 2026-10-01. Status: **a review, for Michael's decisions.** Nothing is built.

Asked for by Michael, 2026-10-01: "let's now review our homepage to ensure it's as engaging as possible", with six sites to learn from: MoMA, The Polygon Gallery, Gagosian, Equinox Gallery, the Vancouver Art Gallery and the Louvre. Home was last designed on 2026-09-26 after MoMA, the Vancouver Art Gallery, Gagosian and David Zwirner (DS-54), then given the collection row (DS-188) and the gallery's sentence (DS-195).

## What Home is now

Read on the live site, 2026-10-01, at 1440 and 390 px. 6,454 px tall on desktop and 7,342 px on a phone, which is close to MoMA (8,429) and Gagosian (8,413).

| Section | What it shows |
| --- | --- |
| Hero | *Collect, Assemble, Gather*: one artwork, Samuel Roy-Bois's *My Sun*, whole on a grey mat in the left half, with the title box beside it and one button, "About the exhibition" |
| What's on | Six cards of equal size: five events (the next Explore + Create, Art in Good Company, the Curatorial Tour, La Modestine, Omer Arbel's talk) and an exhibition that opens in April 2027 |
| From the collection | Three works on grey mats with their labels |
| Artists for Kids panel | One photo, a sentence, two links |
| New limited editions | Three prints on grey mats with prices |
| Support panel | One photo, a sentence, Donate and Volunteer |
| Visit | The building at night, today's opening line, the gallery's sentence, address and hours |

What works: today's opening line, exhibitions and events together, a way in for each audience, the collection and the editions, and no pop-ups or autoplay.

## What the six do that we don't

| | First screen | People and place | Today | Stories and film | Movement |
| --- | --- | --- | --- | --- | --- |
| MoMA | Visitors in the galleries, full width, then "Welcome" with today's hours and Plan your visit | Throughout | Hours and Plan your visit in the first screen | "New ideas and perspectives" (magazine) | None |
| The Polygon | A full-bleed photograph under a giant wordmark | The show's own photographs | Hours on the page | News | Slides change as you scroll |
| Gagosian | One artwork full-bleed, the show's title over it | Through the art | Not needed | "From the Quarterly": essays and conversations | None |
| Equinox | An artwork detail the full width of the page, "Now on view" over it | Through the art | Not needed | None | A slideshow with arrows |
| Vancouver Art Gallery | A large photo of people, a headline beside it | Throughout | Today's hours in the header | Programmes as stories | A What's on slideshow with arrows |
| Louvre | Full-bleed photography | Throughout | "The museum is open today, 9:00 AM to 9:00 PM" in a bar that stays on screen | "Louvre +": a row of films | None |

The pattern: **every one of them leads with a large image that fills the width**, most show **people or the room**, three put **today's hours in the first screen**, and three have **a row of stories or film**. Ours leads with a small object on a mat, shows the room only at the very bottom, keeps the hours in small type in the header (and on a phone, not in the first screen at all), and has no stories or film, though the site holds 27 ArtReach videos and the exhibitions' own films.

## Recommendations

In order of what they would do for a visitor. H1 needs only photos; H2 to H5 are small changes to the theme; H6 and H7 are larger.

### H1. Installation photos of *Collect, Assemble, Gather* (content, no code)

**The single biggest change.** The hero already leads with the room when the exhibition has installation views (DS-30, DS-54): the photo fills the width and the title box overlaps its edge, as on MoMA, the Polygon and the Louvre. The current exhibition has none, so the hero falls back to one artwork on a mat. Six to ten installation photos would change the first screen at once, and fill the exhibition's own page too. Michael Love photographed *My Sun*; he may have photographed the rooms as well.

Needs: the photos from the gallery, then a store write adding them to the exhibition's entry. **Recommended.** A standing request to the gallery too: installation views for every new show, on opening week.

### H2. Today, in the first screen, on every screen size (small)

MoMA and the Louvre answer "can I go now?" before anything else. Ours does in the header's top row on desktop, in small type; on a phone the header shows only the logo and Menu, so the hours first appear under "What's on", a screen down.

Proposal: the hero's title box gains a line under its button: today's line ("Open now until 4 PM", or "Closed today. Open Thursday, 12 to 4 PM", which knows the closures since DS-191) and a link, "Plan your visit". **Recommended.**

### H3. A recurring programme says it recurs (small to medium)

Explore + Create runs every Saturday and Art in Good Company on the second Thursday of each month, but each card shows one date, so they read as one-off events, and a family that misses October 3 may think it's over.

Proposal: when a programme page has several upcoming events of the same title, its card on Home says the pattern and the next date: "Saturdays, 1 to 3 PM. Next: October 3". Worked out from the events themselves, so staff enter nothing new. **Recommended.**

### H4. A different set of works from the collection each day (small)

MoMA's collection row is a wall of works with "Find your favorites". Ours shows the same three works every visit.

Proposal: the gallery chooses up to twelve featured works (the field exists, `gallery-questions` 17); Home shows three of them, a different three each day, worked out from the date, with no script. Returning visitors see something new; the Permanent Collection page keeps the first six. **Recommended**, once the gallery has chosen more than three.

### H5. A wider hero when it is an artwork (small)

Gagosian and Equinox show the work large. When our hero has to be an artwork (no installation views), the picture takes half the content width: *My Sun*'s photo is 756 × 567 px at 1440, a third of the screen, and the work itself is smaller still inside the photo's own grey studio backdrop, so it reads as an object on a shelf.

Proposal: the artwork hero takes two thirds of the width, with a narrower title box beside it, so the picture is about 1,000 px wide; the work stays whole and never cropped (DS-05). **Recommended**, with H1, which makes the artwork hero rarer.

### H6. Watch and make: a row of films (medium)

The Louvre's "Louvre +", MoMA's magazine and Gagosian's Quarterly give a reason to stay that isn't a date. We have 27 ArtReach videos (artists and Artists for Kids teachers making art with children), the film about Gordon Smith, and the exhibitions' own films (DS-138).

Proposal: a row of the three newest ArtReach videos under the Artists for Kids panel, sharing its colour, titled "Make art with us", each card the video's cover with a play mark, linking to its lesson page. Home's rule allows three listings (DS-54); this would be a fourth, so the rule changes to four. **Recommended**, as the one new section.

### H7. What's on: what's soon, first (medium)

What's on gives six equal cards, and one of them is an exhibition that opens in six months, which pushes a nearer event off. The Polygon separates On now, Upcoming and Events.

Proposal: What's on shows events in the next eight weeks and exhibitions opening in the next three months; an exhibition further off moves to a single line under the row: "Coming in April: *Against the Latitude of "Progress"*". **Optional.**

### Not recommended

- **Slideshows and autoplay** (Equinox, the Vancouver Art Gallery). They hide all but one slide, and move under the reader; DS-08 rules them out.
- **A newsletter pop-up** (The Polygon). It covers the page on the first visit; the band at the foot of every page stays.
- **A giant wordmark over the hero** (The Polygon). The logo rules (§8) set its sizes, and the exhibition's title is the first thing to read.
- **A sticky booking bar** (the Louvre). Admission is by donation and nothing is booked; H2 puts today's line where it helps.

## Decisions for Michael

| # | Decision | Recommended |
| --- | --- | --- |
| H1 | Ask the gallery for installation photos of *Collect, Assemble, Gather* now, and of each new show on opening week | Yes |
| H2 | Today's line and "Plan your visit" in the hero's title box | Yes |
| H3 | A recurring programme's card says its pattern and next date | Yes |
| H4 | Three of up to twelve featured works, a different three each day | Yes |
| H5 | A wider artwork hero, two thirds of the width, the work whole | Yes |
| H6 | A "Make art with us" row of the three newest ArtReach videos; Home's rule becomes four listings | Yes |
| H7 | What's on keeps far-off exhibitions to one line | Optional |

H2 to H7 are built on a branch, against the development theme, with their design decisions recorded as Proposed, as usual.
