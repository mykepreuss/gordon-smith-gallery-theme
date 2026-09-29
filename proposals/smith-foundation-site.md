# The Smith Foundation's old website on gordonsmithgallery.com

Status: **Built, 2026-09-28; in review.** Decided by Michael ("Yes to everything except integrating the older Year in Review content - the desire is to only show the most recent one for simplicity"), then "Proceed with implementation". Every recommendation under "Decisions for Michael" is approved except the Year in Review shelf: only the newest report shows (P-47). Recorded as P-41 to P-49 and DS-138 in `DECISIONS.md`. The content is in the store and the Videos and publications section in the theme, on this branch's pull request; what the build changed from the plan is under "Build notes", and what's left under "Still open". The plan was revised the same day for the new menu ("After the menu review").

Michael, 2026-09-28, sharing a WordPress export of the old Gordon and Marion Smith Foundation site: "is there any valuable content we are missing in our new Shopify Gordon Smith Gallery site?", then "let's create a plan for what content gets integrated where (text and images)". After the menu review merged (pull request #45): "I've updated the navigation and IA of our site - please review and update our content integration plan".

## Summary

- **Sources:** the WordPress export of smithfoundation.co and its media library, downloaded 2026-09-28 (1,402 of 1,404 files, 1.96 GB, web sizes). Both are outside Git ("Sources").
- **The old site:** 44 pages (40 of them already private), 35 archive items (exhibitions and fundraisers), 14 events from 2026 and the media library.
- **The old site is still running, but its address no longer reaches it.** smithfoundation.co forwards its home page to gordonsmithgallery.com and gives an error for every other address. The server answers only when asked for directly, so it can go at any time. Everything below works from the export and the download.
- **Already on the site:** most of the Foundation's current copy. That covers the Foundation page and its board, Gordon and Marion, Donate, Volunteer, the programme pages, the six recent exhibitions in full and the 2025 annual report.
- **What moves:**
  - the text, curators, artists and images for the six exhibitions that show only a title and dates (2020 to 2023), and the missing credits and programmes of three recent ones;
  - 17 exhibitions from 2013 to 2019, as new entries, so Past Exhibitions covers the Gallery's history from its first show;
  - three Foundation pages that the Foundation page already points toward: Scholarships, the Brilliance Gala, and Supporters (the donor list the Donate page promises). The new menu already has their places: Scholarships in Programs, the gala and Supporters in Support (P-52, P-53);
  - past talks on Speaker Series; past concerts and the Steinway piano on Music at the Smith;
  - 12 videos and 5 publications, from their exhibitions and pages;
  - a few facts for the Foundation page, Donate, Plan your visit, Volunteer and Gordon and Marion, once the gallery confirms them.
- **New structures:** one exhibition field, Videos and publications. Everything else reuses what the site has: exhibition entries, page fields, card groups, staged text, and from the Artists for Kids work (pull request #42, merged) the way new pages are made before release (P-35), cards that open a PDF (DS-69), photos in page text (DS-77), the eyebrow that links back (DS-80) and the video snippet.
- **The store would gain** 17 exhibition entries, 3 pages, about 100 images, 3 PDFs, 1 card and three links in the new menu.
- **Stays behind by decision:** the Year in Review reports before 2025. The Foundation page keeps only the newest (P-47).
- **Found while reading:** the Foundation's online donation form still works, which answers half of question 3.1. The five 3D tours of past exhibitions are gone. Both are under "Found while reading".

## After the menu review

The menu review (`proposals/navigation-review.md`, P-50 to P-57, DS-132 to DS-136) merged on 2026-09-28. It sorts the menu by what visitors come to do: Exhibitions, Collection, Programs, Support, About, Shop. The Smith Foundation section is gone, and the review already placed this plan's three pages. What that changes here:

| Before | Now | Why |
| --- | --- | --- |
| The three pages in a Smith Foundation section, with About the Foundation, Gordon and Marion and Donate | Scholarships in Programs, in the group "Scholarships and awards", first, labelled "Smith Foundation scholarships" (P-52). Brilliance Gala in Support after Give to Artists for Kids; Supporters last in Support (P-53) | Students look for scholarships among programs, beside Artists for Kids' awards; the gala is a way to give; Supporters is the thanks that follows giving. The places and labels are in `proposals/store-changes.md` §1 and `navigation.py` (`LATER`) |
| The Foundation's pages held together by the menu section | Held together by the Foundation's page, now in About: its cards link to the scholarships and the gala (P-57), and it gains a Supporters card, so it links to all six of the Foundation's pages (N13). Each new page carries the Foundation's logo and colours (programme field) and "The Smith Foundation" as its eyebrow, which links back (DS-80) | P-57: the Foundation's page is the hub |
| Donate and Gordon and Marion as the Foundation's menu items | "Give to the Smith Foundation" (Donate) in Support and "Gordon and Marion Smith" in About. Both already carry the eyebrow back to the Foundation's page, and Gordon and Marion has a button to Gordon Smith's works (P-57) | Their staged text additions here are unchanged; the new video goes in the text, not in place of the button |
| The next gala as an event on the gala page | The same, and as an event it also shows in Upcoming events (first in Programs) and the home page's What's on (N11) | Nothing new to build |
| Pull request #42 still open | Merged. P-35, P-39, P-40 are decided; DS-69, DS-77 and DS-80 are built and Proposed | This plan's steps no longer wait for it |
| DS-131 for Videos and publications | DS-138. DS-131 went to the whole-site review, and DS-137 to selling a print with its frame (#48) | Numbering |

Nothing about the exhibitions changes. Exhibitions is now a plain link to On now and Past is one step away on its switcher (P-51); the older exhibitions with text also show in More exhibitions when fewer than three current shows remain (DS-130).

## Sources

| What | Where | Notes |
| --- | --- | --- |
| The text of every page, archive item and event | `~/Downloads/gordonandmarionsmithfoundationforyoungartists.WordPress.2026-09-28.xml` | The file starts with five blank lines, which a parser must skip |
| The media library | `~/Downloads/smithfoundation-media/files/` | In WordPress's year and month folders. `manifest.csv` gives each file's pixel size, caption, upload date, old address and the pages that use it |
| The public pages as they looked | `~/Downloads/smithfoundation-media/pages/` | 53 pages. The private pages need a WordPress login; their text is in the export |

The copies stay out of Git: they are large, and Git holds source and records (AGENTS.md). The scripts that prepare the store writes take the two paths as arguments and record what they upload in `proposals/store-writes/created/`, as the collection's did.

## Rules for moving content

- **Text word for word** (EXH-04, AGENTS.md). Choosing which paragraphs move is allowed; rewriting them isn't. Where the old site has two versions of a text, the later one moves and the difference goes to the gallery.
- **Nothing dated moves as a call to action.** Ticket prices, RSVP links, deadlines, "Applications are closed", appeals and job postings stay behind. Events that have passed move only as history, under headings such as "Past talks".
- **Pasted formatting stays behind** (TYPE-03). Titles written in Unicode italic letters in the old text become real italics (L-03). "AFK" in titles, labels and headings is written out (P-39).
- **Images** are the web sizes from the download:
  - Images over Shopify's limits (25 megapixels, 20 MB) are made smaller.
  - Each gets alt text.
  - Each credit comes from the old text, such as "Photos by Rachel Topham". Where the old site names nobody, the gallery is asked.
  - Images under 1,000 px on the long side are flagged.
- **Store writes** follow "Store writes before release" in the plan. Each needs Michael's go-ahead, a before-snapshot and an undo step, and is logged in `proposals/store-writes/README.md`. Text on existing pages is staged in `custom.release_body` (DS-39). New pages follow P-35.

## Where each piece goes

### Exhibitions: the six with only a title and dates

Their entries exist, each with a key image. Filling the summary or text makes their cards in the Past list link (DS-25).

| Exhibition | From the old site | Goes to |
| --- | --- | --- |
| *Play*, 2020 to 2021 | Three questions and a paragraph | Summary: the paragraph. Text: the three questions. The line "Artists for Kids and the Smith Gallery have gone virtual…" is dated and stays behind |
| *Unfixed*, 2021 | Subtitle, the two artists, the curator, four paragraphs, about 30 images, the installation credit, the book, two videos | Subtitle: "The Entangled Works of Chris Curreri and Laurie Kang". Artists: Laurie Kang, Chris Curreri. Curator: "Curated by Meredith Preuss" (the old site writes "CURATOR: Meredith Preuss"). Summary: the first paragraph; text: the other three. Installation views: the old page's images, about 30. Installation credit: "All Installation Photography by Michael Love. Courtesy AFK and The Gordon Smith Gallery of Canadian Art". Videos and publications: the artist talk (68 minutes) and the conversation (54 minutes) on Vimeo, and the book as a PDF, in a smaller copy because it is 20.2 MB (P-40) |
| *Beyond the Horizon*, 2021 to 2022 | The curator, 20 artists, a paragraph | Curator: "Curated by Guest Student Curator, Karl Hipol". Artists: the 20. Summary: the paragraph, from the later of its two versions |
| *We Can Only Hint at This with Words*, 2022 | The three artists, the curator, three paragraphs, bios of the artists and contributors, credits, the zine, a panel video | Artists: Russna Kaur, M.E. Sparks, Andrea Taylor. Curator: "Curated by Kate Henderson". Summary: the first paragraph. Text: the other two, then "Artist Bios" and "Contributor Bios" as headed sections (P-45). Credits: the three lines ("Presented by…", "Generously supported by Parc Retirement Living", "Additional support…"), with the Parc and North Vancouver Recreation and Culture logos. Installation credit: "Rachel Topham Photography". Videos and publications: the contributor panel on YouTube and the zine on Issuu |
| *Paths*, 2022 to 2023 | The curator, a paragraph, the curator's bio | Curator: "Curated by Amelia Epp". Summary: the paragraph. Text: her bio under "Curator" |
| *Endless Summer*, 2023 | The two artists, the curator, three paragraphs, bios, three past programmes, sponsors, the booklet | Artists: Katie Kozak, Lucien Durey. Curator: "Curated by Jenn Jackson". Summary: the first paragraph. Text: the other two, "Artists", "Curator" and "Public Programs" (P-45). Credits: "Endless Summer is made possible by the generosity of the following sponsors:" with the four sponsor logos. Videos and publications: the exhibition booklet (PDF, 18.9 MB) |

### Exhibitions: three recent ones with parts missing

| Exhibition | Adds |
| --- | --- |
| *Prevailing Landscapes*, 2024 | Credits, which the entry lacks: "Prevailing Landscapes is presented by…", the supporters and "Select Public Programs are also supported by…". "Public Programs" in the text: the curatorial tour, Cameron Kerr's live carving and conversation, and *Art Education Unveiled* (P-45). Videos and publications: *Art Education Unveiled* on Vimeo (52 minutes) |
| *Playhouse*, 2024 to 2025 | "Public Programs" in the text: the opening, the curator's tour and *The Giant Strawberry* workshop with Cindy Mochizuki. Videos and publications: the three Guná Jensen videos on YouTube (the artist feature, the conversation and its extended version) |
| *Stitched*, 2025 | "Public Programs" in the text: the opening, the tour and the artist talk. Videos and publications: VocalEye's described tour on YouTube |

*The Art of Conversation*, *From the Ground* and *One Hundred Artists Deep* are complete. The old site adds only their 3D tours, which are gone, and events that belong to Speaker Series.

### Exhibitions: 17 new entries, 2013 to 2019 (P-41)

Each gets title, dates, curator and artists where the old text names them, the old text as summary and text, and a key image. Where the key image is one work, it's marked as an artwork and its caption comes from the old text ("Featured Image: …"). The list grows from 12 past exhibitions to 29; all 32 entries stay under the 50 that one list reads (L-07).

| Exhibition | Dates | Curator (old wording) | Key image |
| --- | --- | --- | --- |
| *Collection, Connection and the Making of Meaning* | May 13 to September 14, 2013 | "guest-curated by Robin Laurence" | `2017/10/PA1300021.jpg`, 1920 px |
| *Expressionist Renderings: The Prints of Alistair Bell* | October 9 to December 20, 2013 | "guest-curated by Ian M. Thom" | Its image is gone from the server. A print by Alistair Bell from the collection, as an artwork |
| *Victor John Penner: Not Safe to Occupy* | January 15 to February 29, 2014 (see "Found while reading") | "guest-curated by Michael Love" | `Beds_Rooms4317-36a.jpg`, artwork, with its "Featured Image" caption |
| *Gu Xiong: A Journey Exposed* | May 7 to August 23, 2014 | "curated by Astrid Heyerdahl" | `Gu-Xiong-Installation-View.jpg` |
| *Work Is Art* | September 10 to October 15, 2014 | "Curated by Gordon Smith himself" | None on the old site. A work from the collection by one of its artists (George Rammell or Wing Chow), as an artwork |
| *Robert Young: Spatial Understanding* | October 22, 2014 to January 3, 2015 | "curated by Astrid Heyerdahl" | None on its page. `2017/10/young-smitysmall.jpg` if the gallery confirms it's his, else a work of his from the collection |
| *Figurative Contemplation* | October 22, 2014 to May 2, 2015 | "curated by Astrid Heyerdahl" | `2017/10/Art-Inquiry-Station-w-Figurative-Contemplation-exhibition.jpg` |
| *Accidentally on Purpose: Ross Penhall* | March 3 to May 2, 2015 | None named | `IMG_3872.jpg` |
| *Robert Davidson: Progression of Form* | May 15 to August 29, 2015 | "guest-curated by Ian M. Thom" | `2017/07/Robert-Davidson-Installation-View.png`, 705 px, flagged as small. `2017/12/Robert-Davidson.jpg` (3469 px) may be the catalogue's cover; to check |
| *Phantoms in the Front Yard: Over the Counter Culture* | October 1 to December 18, 2015 | "collaborated with curator Pennylane Shen" | Michael Abraham, *Sleeping Modernist*, 704 px, artwork, flagged as small |
| *Readymades* | May 5 to August 26, 2016 | "curated by Bill Jeffries" | `DSC_5630.jpg`, and `2017/10/Readymades-Installation-View-1.png` (935 px) as a view |
| *Art School High* | May 13 to August 26, 2017 | "guest-curated by Patrik Andersson" | `GordonSmithGallery_ArtSchoolHigh_04`, from the TIFF |
| *Memory, History, Story* | September 29, 2017 to April 7, 2018 | None named (the Artists for Kids teaching exhibition) | `MemoryHistoryStory_Install-24-3.jpg` |
| *Thirteen Ways to Summon Ghosts* | May 16 to August 31, 2018 | "guest-curated by Kimberly Phillips" | `SummonGhosts-50_WEBSITE.jpg`, and three more views. Credit: "Photograph by SITE Photography" |
| *Transformations* | September 28, 2018 to April 13, 2019 | None named. Subtitle: "Selected works from the AFK Collection", with AFK written out (P-39) | `Transformations3-1.jpg` |
| *Reframed: Painting and Collage by Tiko Kerr* | May 8 to August 30, 2019 | "Curated by Meredith Preuss" | Tiko Kerr, *Before the Inferno I Had a Light Heart* (title from the file's name), 800 px, artwork, flagged as small |
| *Dwelling: People and Place* | September 27, 2019 to April 16, 2020 | None named | `pratt-prat.jpg`, 1024 px |

The curator lines are taken from sentences ("… was guest-curated by Robin Laurence"). They go in as "Guest-curated by Robin Laurence", which the gallery checks.

Works from the collection shown in these exhibitions (`collection_works`) are not part of this plan: the old site doesn't list them. The gallery can add them later.

### The Smith Foundation's pages

**The Smith Foundation** (staged text and fields):

- **Card links (P-57).** The "Smith Foundation Scholarships" and "Brilliance Gala & Auctions" cards link to their new pages. A sixth card in "Get involved", Supporters, opens with the old Supporters page's first line ("Thank you to our generous community of donors for their support!") and links to its page, so the hub reaches all six of the Foundation's pages. The Endowment card stays without a link.
- **Year in review (P-47).** Only the newest report shows, as today: the page's button links to it (2025 now), and staff change the button when a new one comes out. The older reports (2019, 2021 to 2024) don't move. Michael, 2026-09-28: "the desire is to only show the most recent one for simplicity".
- **With the gallery's confirmation (P-49):**
  - the mission: the vision line, the four values and the three "We advance the public's appreciation of the visual arts…" lines;
  - "Our impact" from the old Our Impact page: 95% of revenue from non-governmental sources; the endowment since 2010, "close to 3 million dollars"; "over 3 million dollars to Artists For Kids since 2002, supporting over 55,000 young artists". These figures date from 2018 or later, so the gallery updates or confirms them.

**Scholarships**, new, `/pages/smith-foundation-scholarships` (P-42). In the menu: Programs, Scholarships and awards, first, as "Smith Foundation scholarships". Eyebrow "The Smith Foundation"; programme Smith Foundation:

- The old Scholarship Opportunity page's two opening paragraphs and its portfolio line.
- The three $2,500 Young Artist Scholarships (North Vancouver, West Vancouver, Vancouver), each under its own heading, as written.
- A line linking the Artists for Kids awards, and on that page a line back. The menu puts the two side by side (P-52); the lines say the difference on the pages themselves, which settles found item 16 in the Artists for Kids plan.
- The application forms go up with each year's round. The 2026 ones are for a closed round, so the page says only what the gallery gives it (for example, when applications open).
- Hero: a photo from the library or the gallery.

**Brilliance Gala**, new, `/pages/brilliance-gala` (P-42). In the menu: Support, after Give to Artists for Kids. Eyebrow and programme as Scholarships:

- **Opening:** the Brilliance Gala paragraph from the old Fund page, which the Foundation's card already uses in part.
- **"Past galas"**, newest first, each with its text as written and 4 to 6 photos in the text:
  - Brilliance Gala 2026: $250,000, the co-chairs and committee. Photography by Jamie Lee Fuoco; 99 photos to choose from.
  - The Gala at Camp Smith, 2025: $228,000, the 30th anniversary of Paradise Valley. A 45-second video; photography by When They Find Us; 159 photos.
  - Brilliance 2023: the Friends of Gordon Collection, 300 guests, $471,000. The catalogue on Issuu and a four-minute tribute video; 235 photos. The photographer's credit was an image, so the gallery names them.
  - The Spring Luncheons: 2013, 2018 and 2019 (the 16th, 150 guests, $148,000). Two photos each, and the 2019 auction catalogue (PDF).
  - Off the Wall, the collectors' auction: the old Fund page's paragraph. Its press quote ("more than $115,000 raised") names no source, so it waits for the gallery.
- **The next gala** is an event entry for this page when it's announced. The page's events section shows it, and so do Upcoming events and the home page's What's on (N11).

**Supporters**, new, `/pages/smith-foundation-supporters` (P-42, P-43). In the menu: Support, last. Eyebrow and programme as Scholarships:

- The old Supporters page: its thanks and the donors by level, from "$50,000 or more" to "$1,000 or more", and "We also extend our gratitudes to".
- The sponsors, the foundations and grant agencies, and the volunteers, each as a headed list, as written.
- The gallery confirms the list is current before release: see "Found while reading" for the repeats and misspellings.
- The Donate page's sentence "…including the donor page of each website" links "donor page" here, with its words unchanged.

**In the menu** (P-52, P-53): each page is added to the new theme's menu (`new-theme-main-2`) when it is made, from `navigation.py`'s `LATER` list with `menuUpdate`, keeping the other items' IDs. Support then holds five: Give to the Smith Foundation, Give to Artists for Kids, Brilliance Gala, Volunteer, Supporters. The live site doesn't read this menu; publishing the new theme switches to it.

**Donate** (staged text; "Give to the Smith Foundation" in Support):

- The "Online Form" card links to the Foundation's online form, which still works (question 3.1, with the gallery's confirmation).
- The old Donate page's three sponsorship paragraphs ("Event Sponsorship", "Exhibition and Public Program Sponsorship", "It's all in the name!") go under a heading, if the gallery still offers them (P-49).

**Gordon and Marion** (staged text; "Gordon and Marion Smith" in About). Its eyebrow and its button to Gordon Smith's works stay as P-57 set them:

- A second video, *Gordon A. Smith: A History* (14 minutes), in the text as the first is.
- The old page's sentence naming his obituaries (The Globe and Mail, the Vancouver Sun) and the CBC interview with Paul Killeen, with its links. The Globe and Mail and CBC links work; the Vancouver Sun's refused the check, so it is checked by hand.

### Programme pages (P-44)

| Page | Adds, in the staged text after the page's own |
| --- | --- |
| Speaker Series | "Past talks", newest first: *Artistic Approaches in Dialogue: Responses to Jack Shadbolt* (June 6, 2026); *Art Education, For Life* with Rebecca Baker-Grenier (May 2, 2026), with its video (54 minutes); *Art Education Unveiled: Perspectives from Prevailing Landscapes* (May 9, 2024), "the first installment of our new Speaker Series", with its video (52 minutes). Each gets its title, date, speakers and description; the speakers' bios stay behind. The live page's empty "Past Speaker Series" headings, 2022 to 2026, suggest the gallery has more for 2025 |
| Music at the Smith | "Past concerts": *The Giving Shapes* (June 13, 2026) and the fall 2023 season chosen by Guest Music Curator Sarah Ballantyne (four concerts). Each gets its date, title and performers. And the Steinway: the old Public Programs page's two paragraphs about the 100-year-old baby grand given by Kathryn Allison, with the photo of Lixia Li playing it (photo by Cindy Goodman) |

### Publications (P-48)

The old shop sold 11 titles by email: seven of the Foundation's catalogues and four books. The catalogues are for *Unfixed*, *Gu Xiong*, *Readymades*, *Collection, Connection and the Making of Meaning*, *Art School High*, *Robert Davidson* and *Reframed*. The books are *Alistair Bell: Prints 1982 to 1992*, *Ross Penhall's Vancouver…*, *Alpine Anatomy: The Mountain Art of Arnold Shives* and *Gordon Smith: Don't Look Back* (sold out). The library has Khim Mata Hipol's photographs of them (2021).

If the gallery still sells them, they become products in a Publications collection in the Shop, with the gallery's prices and stock. Until then nothing is added.

### Where the other facts go (P-49)

Each goes in only when the gallery confirms it's still true. Until then each is a question.

| Fact on the old site | Goes to |
| --- | --- |
| Admission by donation, "$5 suggested", and where the donations go | Theme settings, Gallery details, admission (question 7.1) |
| "Backpacks, large bags, food, drinks, and umbrellas are not permitted in the exhibition spaces…" | Plan your visit, staged text |
| Gallery docents | Volunteer, a third role card, as written |
| The Foundation's phone and emails (info@, executivedirector@, programs@, coordinator@) | Contact, with question 1.1 |

## How it's stored

Reused as built:

| Need | Uses |
| --- | --- |
| Old exhibitions | Exhibition entries (P-10, P-11); the Past list picks them up by date |
| Three new pages | The standard page template: hero, text with photos and videos, card groups, events. Page fields: hero image, hero caption, intro, programme (Smith Foundation), eyebrow "The Smith Foundation" (DS-80). Made before release as P-35. Menu links from `navigation.py` `LATER` |
| The scholarships' forms, when there are some | Cards whose link is a PDF (DS-69), or links in the page's text |
| Past talks, concerts, galas | Page text, staged (DS-39), with photos (DS-77) and videos |
| The next gala | An event entry for the Brilliance Gala page |

New (P-46, DS-138):

| Structure | What it is | Why |
| --- | --- | --- |
| Exhibition field **Videos and publications** (`media`, a list of links) | Shown after the exhibition's text. A Vimeo or YouTube link plays in the page, as video does in page text; any other link is a row with its label, "(PDF)" or the external cue | Six exhibitions have talks, tours or catalogues, and new ones will. The text field can't hold a video, and links buried in paragraphs are hard to find |

The field and its display go into `DESIGN.md` and `preview.html` first, as a Proposed decision. They reuse `snippets/gs-video.liquid`.

## Decisions for Michael

Michael, 2026-09-28: "Yes to everything except integrating the older Year in Review content - the desire is to only show the most recent one for simplicity". Every row below is decided as recommended except P-47. They are P-41 to P-49 and DS-138 in `DECISIONS.md`.

| # | Decision | Recommended | The other way |
| --- | --- | --- | --- |
| P-41 | How far back Past Exhibitions goes | To 2013: 17 more entries, the Gallery's whole history. Amends DS-25 | From 2020, as today |
| P-42 | The Foundation's scholarships, gala and supporters | Three pages, made before release as P-35, where the menu review placed them (P-52, P-53), each linked from the Foundation's page and linking back (P-57) | Sections on the Foundation page, which becomes very long and leaves the menu's three places empty; or no pages |
| P-43 | The donor list | Published as the old site had it, once the gallery confirms it's current. The Donate page already promises it | No list, and the gallery rewords the Donate page's promise |
| P-44 | Past talks and concerts | On Speaker Series and Music at the Smith, under "Past talks" and "Past concerts": title, date, speakers or performers, the talk's description and its video. Bios stay behind | With the speakers' bios; or no past programmes |
| P-45 | An exhibition's own past programmes and bios | In its text under "Public Programs", "Artists" or "Curator" headings, as written, without RSVP or ticket links | Left out |
| P-46 | Videos and catalogues on exhibition pages | A new field, Videos and publications, that plays videos in the page (DS-138) | A last paragraph of links in the exhibition's text; videos open on Vimeo or YouTube |
| P-47 | The Year in Review reports | ~~A document shelf on the Foundation page, 2019 to 2025 (DS-69, DS-75)~~ **Decided otherwise: only the newest report, from the page's button, as today** | Links in the Foundation page's text |
| P-48 | Publications | Ask the gallery. If they still sell them, Shop products in a Publications collection | A list on the Foundation page now |
| P-49 | Facts that may be out of date: the mission lines, the impact figures, the suggested donation, the bag rule, docents, sponsorship and naming, the Foundation's emails, the online form | In only once the gallery confirms each one | In now, as written |

## Steps

One branch and one pull request after the decisions, as the Artists for Kids work did. Each step is its own commit.

1. **Decide.** Done 2026-09-28: P-41 to P-49 and DS-138.
2. **Ask.** The new questions go to the gallery (`gallery-questions.md`, now in its sections 1, 4, 7 and 8), with the rest.
3. **Review sheet.** A read-only script, `proposals/store-writes/foundation/inventory.py`, reads the export and the manifest. It writes every entry's fields and each page's staged text to a sheet, with the chosen images. Michael checks the sheet before anything is written.
4. **Photos to choose.** For each gala and for *Unfixed*, a contact sheet of the proposed photos; Michael swaps any.
5. **Design.** The Videos and publications section, in the design system first (DS-138).
6. **Definitions.** The exhibition field.
7. **Files.** About 100 images with alt text, made smaller where Shopify needs it. 3 PDFs: the *Endless Summer* booklet, the *Unfixed* book in a smaller copy and the 2019 auction catalogue.
8. **Entries.** 17 exhibitions; fields on nine existing ones; the Supporters card on the Foundation page.
9. **Pages.** The three new pages (P-35) with their fields and eyebrows; the Foundation page's card links and its Supporters card; staged text on the Foundation page, Speaker Series, Music at the Smith and Gordon and Marion; Donate and the rest as the gallery answers.
10. **Theme and menu.** The field's section on exhibition pages. The three pages join `new-theme-main-2` from `navigation.py` `LATER` (a store write with its own before-snapshot); check the Programs and Support dropdowns at 1200 px and in the drawer, and that each new page marks its section as current.
11. **Checks.** Theme Check, the linter and its tests, contrast, sync, 1440, 768 and 390, every link, and the fonts audit on the new pages.
12. **Records.** `REQUIREMENTS.md`, `DESIGN.md` §7.5, the content model, `proposals/store-changes.md` §1 (the three "once its page exists" become real), `navigation.py` (`LATER` emptied) and the release backlog.

## At release

- The three pages: their template (the standard one), their staged text into the page, then `seo.hidden` off (as P-35).
- The menu: nothing more to do. The pages are already in `new-theme-main-2`, which the header uses once the new theme is published.
- The staged text on existing pages moves in with everyone else's (DS-39).
- The old site's addresses: every one but the home page already gives an error. Two ways to fix that sit outside Shopify's own redirects, which only work on the store's domains:
  - the Foundation's domain forwarder sends old paths to their new addresses, for example `/exhibitions-items/unfixed/` to `/pages/exhibitions/unfixed`;
  - or smithfoundation.co becomes a domain of the store, and Shopify redirects handle the paths.

  Either is the Foundation's to choose, with its DNS. The old and new addresses are in the review sheet.

  Chosen 2026-09-29 (P-63, Proposed): a third way, since the old server still runs. A file on it sends each old address to its new page, and the domain's forwarding is turned off so every visit reaches the server. The file, its list of 174 addresses and the steps for the day: `proposals/foundation-redirects/`.
- Rollback: hide the three pages. Entries, files and the field can stay; the old theme reads none of them.

## Found while reading

| # | What | Where |
| --- | --- | --- |
| 1 | **The Foundation's online donation form still works** (eTapestry, "Give Now"). The Donate page has no online way to give today (question 3.1) | Donate |
| 2 | **The 3D tours are gone.** Five exhibitions (*Endless Summer*, *The Art of Conversation*, *Prevailing Landscapes*, *Playhouse*, *Stitched*) had Matterport tours; each now reports the model not found. The gallery may be able to restore them from its Matterport account | Exhibitions |
| 3 | Every old address except the home page gives an error today, including ones other sites link to (Capture Photography Festival's artist pages, Issuu) | At release |
| 4 | *Victor John Penner* is dated "January 15 to February 29, 2014". 2014 had no February 29 | New entry: February 28 until the gallery says |
| 5 | *Robert Young: Spacial Understanding* (the title) and "Spatial Understanding" (the text); "13 Ways to Summon Ghosts" (the title) and "Thirteen Ways…" (the text) | New entries: the text's spellings |
| 6 | *Stitched*'s opening reception was April 1, 2025, the festival's launch. The dates question (2.1) is about the exhibition's first public day | Question 2.1 |
| 7 | The old site writes "We Can Only Hint at This With Words" and "Unfixed, The Entangled Works of Chris Curreri and Laurie Kang" | Question 2.5 |
| 8 | *Dwelling* closed early: "temporarily closed, effective March 19th, 2020". Its planned end was April 16, 2020 | New entry: the planned dates |
| 9 | *Beyond the Horizon* has two versions: an earlier one with a dictionary footnote, and a later one with a curator and slightly different wording | The later one |
| 10 | The donor list repeats names across levels ("Richard and Annette Savage", "Annette & Richard Savage"; "Lisa Turner") and has misspellings: "Dr Marla Kiess" and "Dr. Marla Keiss", "Misson Hill Winery", "The Benevity Community Impact Fun" | Supporters, for the gallery |
| 11 | The *Unfixed* book is 20.2 MB, just over Shopify's limit | Smaller copy (P-40) |
| 12 | The exhibition field `programme` exists but no page shows it. The old site's label "Artists for Kids Teaching Exhibition" (*Beyond the Horizon*, *Paths*, *The Art of Conversation*) has no home until it does | Later, not in this plan |

## Build notes

Built 2026-09-28 on branch `claude/gordon-smith-content-audit-dc74c6`. Scripts in `proposals/store-writes/foundation/`: `source.py` reads the export, `content.py` says what goes where, `files.py` prepares and uploads the files, `load.py` writes the entries and cards (and undoes them). Log: `proposals/store-writes/README.md`.

What the build changed from the plan:

| Plan | Built | Why |
| --- | --- | --- |
| Four to six photos a gala | Two at most (a video counts as one); the Spring Luncheons have 2019's photo only | At 1440 the photos stacked beside the text far past its words; the page went from 11,276 to 5,072 px. The 2018 and 2013 luncheons were photos alone on the old site. The other photos are in Files, unused, for the gallery to swap in |
| *Unfixed*: about 30 installation views | 12 | Chosen from contact sheets for variety: the room, each artist's main works. The rest stay on the download |
| *Dwelling*'s key image from the old site (1024 px) | Christopher Pratt's *Christmas Eve at 12 O'Clock*, 1995, from the collection, with its record's caption; it is also *Dwelling*'s work from the collection | Looking at the old picture showed it is his print, which the collection holds at full size |
| Three older shows' key images from the collection | Alistair Bell's *Tall Bird*, 1961; Yung Wing Chow's *Flux I*, 2013 (*Work Is Art*); Robert Young's *The Jazz Player/ Sounds Inside*, 1973 (his show was inspired by jazz) | The old site has no picture for them. Captions from the collection's records; the gallery checks the choice (8.11) |
| *Phantoms in the Front Yard*: curator line | None | The old text says the collective "collaborated with curator Pennylane Shen"; a curator line would say more than that. The sentence stays in the text |
| The Donate page links "donor page" to Supporters | Not yet | Supporters goes live only when the gallery confirms the list (P-43, 8.1); the link goes in with it (`proposals/store-changes.md` §8c) |
| Foundation page: scholarship and gala cards linked | Also a sixth card, Supporters, with the old page's first line and a 2019 luncheon photo | So the hub reaches all six Foundation pages (P-57, N13) |
| Music at the Smith: the Steinway | Under a heading of ours, "The Steinway", with Kathryn Allison's words as a quote naming her | The old page had the paragraphs with no heading; the quote is hers, as the paragraph before it says |
| Speaker Series: *Art Education Unveiled* | Without its last sentence, "Reception to follow, supported by Polygon Homes." | Dated (P-45) |
| Alt text written from looking at each picture | Written by a reviewer who looked at each of the 52 photos, then checked | For the gallery to review with the rest (8.12) |

Checked on the review theme (it follows `main`, so it shows the content and not yet the new section): Past exhibitions lists 29, back to 2013; an older exhibition's page; the three new pages; every staged paragraph and heading on its rendered page; the Foundation page's cards and the menu link to the three pages; the new pages' header shows the Foundation's logo and marks Support or Programs. The Videos and publications section was checked in `design-system/preview.html` at 1440 (two across) and 390 (one column, no sideways scrolling); the shared development theme was in use by another session, so the section waits for the review theme after merge. Theme Check, the linter and its tests, contrast and sync pass. The live site shows the three new pages' titles only (`noindex`, not in the sitemap); nothing else changed there.

## Still open

- The gallery's answers (`gallery-questions.md` §8, and 1.1, 1.4, 4.6, 4.7, 4.9, 7.3), and its word on the menu labels (§3). Supporters and Donate's link to it wait for 8.1 (`proposals/store-changes.md` §8c).
- The Videos and publications section on the review theme once this merges: *Unfixed*, *We Can Only Hint at This with Words*, *Endless Summer*, *Prevailing Landscapes*, *Playhouse*, *Stitched*.
- Michael's decisions on DS-69, DS-77 and DS-80, which are built and Proposed. This plan uses all three.
