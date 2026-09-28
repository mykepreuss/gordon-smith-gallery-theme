# Questions for the gallery

Everything still open that only the gallery can answer, in one place (2026-09-26). Each question says what the site does until it's answered. Nothing here blocks reviewing the site. The first group is needed before release.

Sources: `PROJECT.md` "Waiting on", the plan's "Inputs, exclusions, and known limits", `design-system/DESIGN.md` §12 (Q1 to Q11) and `proposals/store-writes/README.md`.

## 1. Values the site needs (before release)

| # | Question | Until then |
| --- | --- | --- |
| 1.1 | Which email address should the footer and Contact page show? The Contact page lists two: artistsforkids@sd44.ca and admin@smithfoundation.ca | No email in the footer; the Contact page's own text still lists both |
| 1.2 | Are these right: gallery hours "Thursday to Saturday, 12:00 PM - 4:00 PM" (from Plan Your Visit) and phone "(604) 903-3798" (from the Contact page)? | Shown in the footer as they are |
| 1.3 | The addresses of the gallery's social accounts: Instagram, Facebook, YouTube, Vimeo, LinkedIn, any that apply | No social links in the footer |
| 1.4 | The newsletter sign-up's wording and its consent sentence. It uses "Join Our Newsletter" and "Be the first to know about new programs, upcoming exhibitions, public events, limited edition releases and other exclusive offers." from the old Contact page | That wording, with no consent sentence |
| 1.5 | ~~Access to the Mailchimp for Shopify app's settings, or someone to check them: customer sync on, the right audience, consent carried over, double opt-in~~ Answered: Michael signed in and the settings were read, 2026-09-28 (`baseline/mailchimp-audit.md`) | |
| 1.6 | A staff member for the editing test: about half an hour in the review theme's editor, changing an exhibition, an event, a card, a page's fields and a product's label | Staff editing isn't verified |
| 1.7 | **Choose the featured works** for the Permanent Collection page: six works from the collection that the gallery wants people to see first. To change them: Shopify admin, Content, Metaobjects, Collection grouping, "Featured works", then pick the works in its Works field (the first six show, in that order). Details in 5.12 | Six chosen for the review (5.12) |

## 2. Exhibitions

| # | Question | Until then |
| --- | --- | --- |
| 2.1 | *Stitched*: did it open on April 2 or April 3, 2025? The Past card said April 2, its page April 3 | April 3 |
| 2.2 | The label for the second group of artists on an exhibition page (*One Hundred Artists Deep* used "Founding Artists") | "From the collection" |
| 2.3 | Room names for "where in the building", if it should be a fixed list (only "Mezzanine Gallery" appears on the site today) | Free text, empty for now |
| 2.4 | *Collect, Assemble, Gather*: is Carl Heywood one of the artists? The Upcoming Events page lists him; the newer On Now page doesn't | Not listed (follows On Now) |
| 2.5 | The five older shows' titles are written in title case from the old cards' capitals: *Endless Summer*, *Paths*, *We Can Only Hint at This with Words*, *Beyond the Horizon*, *Unfixed*. Are they right? | As written |
| 2.6 | The Upcoming placeholder "Fall 2027 Exhibition": its title and opening date when known | "Coming soon, September 2027", expected start September 1 |

## 3. Content to check

| # | Question | Until then |
| --- | --- | --- |
| 3.1 | Donate: the "Online Form" card talks about a form "above", but the donation form is switched off on the live page too. Turn the form back on, reword the card, or drop it? | The card is out of the "How to give" group (DS-60); its entry is kept, so it can go back when there is a form |
| 3.1a | Donate: check the new wording, "How to give" (was "Ways To Give"), "Make a gift" (was "Ways to give"), and the card links "Email us" and "Call us" (DS-60) | As written |
| 3.2 | *Stitched*'s credits link the Smith Foundation to `smithfoundation.co/…/smithfoundation.ca`, which doesn't open. The right address? | The broken link stays |
| 3.3 | Three names on the Artists page may be misspelled: "Atilla Lukacs" (his site is attilarichardlukacs.com), "Jean McEwan" (the link goes to Jean McEwen), "Graham Gillmore" (the Permanent Collection page says Graham Gilmore) | As written |
| 3.4 | Speaker Series: where should Omer Arbel's separate biography paragraph go (the page text or the event summary)? | Not on the site |
| 3.5 | *Good Luck (wheelbarrow)* by Samuel Roy-Bois: its description gives the medium as "archival pigment print on Legacy Baryta paper", so its label now says "archival pigment print". Right? | As filled in, 2026-09-26 |
| 3.6 | Our Story's sentence "This print by Bill Reid, based on a ceremonial drum, marked the beginning of an extraordinary partnership with now more than 100 Canadian artists - from Kenojuak Ashevak to Ian Wallace - …" was left off the Artists for Kids history because it repeated the sentences around it (P-25). Would the gallery like the ceremonial drum and the more than 100 artists mentioned in the history, in its own words? | Not mentioned |
| 3.7 | ~~Roz Marshall's link on the Artists page goes to `rozmarshall-artist.com`, which no longer exists.~~ No longer applies: artists' websites aren't shown on the site (DS-63, Michael, 2026-09-27) | |
| 3.8 | The Paradise Valley photo on the Artists for Kids page: its description says 1994, its caption 1996. Which year? | Both as written |
| 3.9 | The portfolio pages' switcher now reads "All editions, Fall 2026, Spring 2026, Fall 2025, Spring 2025, Fall 2024" instead of repeating "Portfolio" five times (DS-67). The portfolios' own titles are unchanged. Is that wording right? | As shown |
| 3.10 | The newsletter audience in Mailchimp has recent sign-ups that look automated (made-up names with numbers). Should someone clean them up? The new site's sign-up form will need spam protection too (`baseline/mailchimp-audit.md`) | Left as they are |

## 4. Brand

| # | Question | Until then |
| --- | --- | --- |
| 4.1 | The land acknowledgement's place names use letters Mulish doesn't have (ʔ, ɬ, θ, some accents), so those letters show in Arial. Accept that, or load a font made for BC Indigenous languages for that text (for example BC Sans)? (Q11) | Arial for those letters |
| 4.2 | Is there a "GS logo clusters document" (the brand guide refers to it on pages 3 to 5)? (Q1) The About Us page has a cluster image (`triad_logo_cluster.png`, 329 × 201 px); is that the approved cluster, and is there a vector version? | Logos shown side by side, not as a cluster. About Us shows each logo beside its own description instead (DS-50) |
| 4.3 | May the site use a teal version of the text-only Gallery logo, which the brand guide shows but wasn't supplied? (Q3) | Not used |
| 4.4 | Should gallery images open larger when clicked? (Q8) | They don't |

## 5. The Permanent Collection (`proposals/permanent-collection.md`)

The collection is on the review site as of 2026-09-27: 1,174 works, 171 artists, 26 groupings. The review sheets are in `proposals/store-writes/collection/sheets/`; a correction there goes back into the store by running the import again.

| # | Question | Until then |
| --- | --- | --- |
| 5.1 | ~~Do the image permissions cover showing the collection on gordonsmithgallery.com?~~ Answered by Michael, 2026-09-26: "We gave all the image rights" | |
| 5.2 | Credit lines: name donors ("Gift of Alan & Elizabeth Bell"), or the collection credit alone? | The collection credit alone, as the catalogue records it (84 works have none) |
| 5.3 | Michael asked for everything (2026-09-26), so the Teaching Collection (195 works) is its own grouping, the 6 works "on loan" are in (P-28, see 5.13), and the artists' documents show on their pages as tiles with their covers, as in the catalogue: 118 of them. The 39 PDFs over Shopify's 20 MB limit are on the site as smaller copies: see "Documents too large for the site" below | Smaller copies of the 39 are on the site |
| 5.4 | Review the artists sheet (`artists.csv`): names, sort names, full and other names, life dates. 313 spellings became 171 artists. Dates are left off for 10 where the catalogue's disagree or can't be right (Kenojuak Ashevak has 1909 to 1976 and 1927 to 2013; Jackson Beardy and Jean-Paul Riopelle have birth years after their works) | Names as the site or catalogue has them; those 10 without dates |
| 5.5 | ~~Where are the original image files, and who at the district's IT can help?~~ Answered: the images came from the catalogue's own masters (converted, and the masters left where they are), and Michael, 2026-09-26: "we won't change anything with DNS, that's outside of our scope" | |
| 5.6 | The catalogue keeps running as the district runs it. Its private records (where each work is, provenance, donors) stay there; nothing private moved. Is that right, or should they live somewhere the gallery controls? | They stay in the catalogue |
| 5.7 | The Artists page lists every artist with work in the collection or an edition in the Shop, 171 names, and each name opens the artist's page on the site, with the works, the documents, the editions and the exhibitions. The links to artists' own websites aren't shown (DS-63). Is there anyone who shouldn't be listed? | Everyone is listed |
| 5.8 | The Artists page's two paragraphs are about the Limited Edition Portfolio artists. With the whole collection listed under them, would the gallery like to adjust the wording? | As written |
| 5.9 | The catalogue's Published Editions paragraph (1990, Bill Reid's *Xhuwaji / Haida Grizzly*, "Entering its 37th year") is the introduction to the Artists for Kids Published Editions grouping, word for word. Keep it? | Kept as written |
| 5.10 | Check the other sheets: `titles.csv` (481 titles whose edition number moved to the Edition field, e.g. "Untitled (30/40)" is now "Untitled", edition 30/40), `problems.csv` (works without a title, image or category; accession numbers used twice; 11 cataloguer notes after "*" left off the site; 41 years to check, see 5.14), `themes.csv` (the catalogue's 30 subject words tidied to 15 themes) and `groupings.csv` | As in the sheets |
| 5.11 | Names chosen where the catalogue has no page for the artist: "Unknown Inuit artist" (catalogue: "Unknown [Inuit Origins]"), "West Baffin Eskimo Co-operative" ("West Baffin Eskimo Coop. LTD"), "T&T Collective" for Tyler Brett and Tony Romano (as *Collect, Assemble, Gather* names them), "Vancouver School Collective". Right? | As chosen |
| 5.12 | **The gallery needs to select the featured works** (also 1.7, before release). For the review there are six: Bill Reid's *Xhuwaji/Haida Grizzly Bear*, Gordon Smith's *Painting After Goya*, Jack Shadbolt's *Winter Garden*, E.J. Hughes's *The Mill at Mesachie Lake*, Robert Davidson's *Crab of the Woods* and Kenojuak Ashevak's *Untitled [Loons Protect The Owl]*. Change them in Content, Metaobjects, Collection grouping, Featured works | These six |
| 5.13 | The 6 works from the catalogue's "Things On Loan to AFK" are now on the site like the rest (P-28). Their records mix loans in and out: three George Rammell sculptures are noted "on permanent loan" to Lynn Valley Elementary, and *Before the Storm* (Gordon Smith) has "Morris & Kumyuen Saldov" as its credit line. Should their pages say they are on loan, and what should each credit line read (for example "Lent by …")? Their records also have gaps to fill: a year of "N/A", dimensions of "size" | Credit lines as the catalogue records them; nothing says "on loan" |
| 5.14 | The site shows each work's year as the catalogue writes it. `problems.csv` lists 41 years to check, each with a reason starting "Year". Eight look like slips: "1988 General note" (Bill Reid, REID001.2), "Paper" (Jack Jeffrey, JEFF002), and two ranges that look like the artist's life: "1932-2003" on three works by Anne Meredith Barry, which matches her dates in the catalogue, and "circa 1923-2006" on three by Frank Perry, a span of 83 years (the catalogue has no dates for him). The other 33 aren't a plain year (1965), a range (1991-96), no date (n.d.) or circa, and are the catalogue's own wording: "20th century" (9), "N/A" (7), a month or full date (6), "(Signed and Dated)" after the date (3), "circa 20c" (3) and estimates such as "N.D. [20--]" and "estimated date: 196-" (5). Is each one right as written, or what should it read? | As the catalogue writes them |

### Documents too large for the site

**Addressed 2026-09-27.** These 39 PDFs from the catalogue's Text Resources were over 20 MB, the most Shopify accepts for a file. Michael asked for smaller copies ("Can you create the optimized versions of all the Documents too large for the site"), and all 39 are now on the site, each opening from its tile on the artist's page. The 5 without a cover show a plain PDF tile.

Each is a scan: every page is one picture at 300 dpi, most with the words recognised as text on top. Each picture was resampled and saved as a JPEG, at the gentlest setting that brings the file under 19 MB: 34 keep 200 dpi, 3 have 150, and the two largest have 130 and 120 (Jack Shadbolt's Exhibitions, 215 MB, and David Blackwood's Press, Books, Works, 135 MB). The pages, their order and the text are unchanged, and the type reads cleanly on screen. Together they went from 1.9 GB to 378 MB. The catalogue keeps the originals.

**For the gallery:** if you have sharper copies under 20 MB (a PDF saved for the web, for example), send them and they can replace these. The list is also in `proposals/store-writes/collection/sheets/large-documents.csv`, and how each file was made in `proposals/store-writes/collection/shrunk-documents.json`.

| Artist | Document | Size (MB) | On the site (MB) | Pictures at | In the catalogue |
| --- | --- | --- | --- | --- | --- |
| Latcholassie Akesuk | Document | 38 | 14 | 200 dpi | [item 4778](https://afkcatalogue.sd44.ca/s/TheCollection/item/4778) |
| Anne Meredith Barry | Books | 24 | 9 | 200 dpi | [item 4790](https://afkcatalogue.sd44.ca/s/TheCollection/item/4790) |
| Anne Meredith Barry | Exhibitions | 30 | 12 | 200 dpi | [item 4786](https://afkcatalogue.sd44.ca/s/TheCollection/item/4786) |
| Anne Meredith Barry | Press | 33 | 15 | 200 dpi | [item 4794](https://afkcatalogue.sd44.ca/s/TheCollection/item/4794) |
| Anne Meredith Barry | Zines, Art | 22 | 9 | 200 dpi | [item 4787](https://afkcatalogue.sd44.ca/s/TheCollection/item/4787) |
| Robert Bateman | Biography | 23 | 10 | 200 dpi | [item 4800](https://afkcatalogue.sd44.ca/s/TheCollection/item/4800) |
| Robert Bateman | Press, Books, Exhibitions | 34 | 13 | 200 dpi | [item 4802](https://afkcatalogue.sd44.ca/s/TheCollection/item/4802) |
| David Blackwood | Exhibitions | 29 | 12 | 200 dpi | [item 4828](https://afkcatalogue.sd44.ca/s/TheCollection/item/4828) |
| David Blackwood | Press, Books, Works | 135 | 17 | 120 dpi | [item 4830](https://afkcatalogue.sd44.ca/s/TheCollection/item/4830) |
| Molly Lamb Bobak | Exhibitions, Press, Photos | 32 | 7 | 200 dpi | [item 4836](https://afkcatalogue.sd44.ca/s/TheCollection/item/4836) |
| Robert Davidson | Exhibitions, Photos | 36 | 7 | 200 dpi | [item 4870](https://afkcatalogue.sd44.ca/s/TheCollection/item/4870) |
| Wayne Eastcott | Exhibitions, Photos | 32 | 6 | 200 dpi | [item 4880](https://afkcatalogue.sd44.ca/s/TheCollection/item/4880) |
| Jamie Evrard | 'Painting in Italy' Book | 33 | 5 | 200 dpi | [item 4886](https://afkcatalogue.sd44.ca/s/TheCollection/item/4886) |
| Joe Fafard | Exhibitions, Photos | 35 | 7 | 200 dpi | [item 4894](https://afkcatalogue.sd44.ca/s/TheCollection/item/4894) |
| Joe Fafard | Press | 42 | 9 | 200 dpi | [item 4896](https://afkcatalogue.sd44.ca/s/TheCollection/item/4896) |
| Gathie Falk | Exhibitions, Photos | 66 | 14 | 200 dpi | [item 4902](https://afkcatalogue.sd44.ca/s/TheCollection/item/4902) |
| Gathie Falk | Press | 74 | 16 | 200 dpi | [item 4904](https://afkcatalogue.sd44.ca/s/TheCollection/item/4904) |
| Angela George | Exhibitions, Photos | 30 | 6 | 200 dpi | [item 4910](https://afkcatalogue.sd44.ca/s/TheCollection/item/4910) |
| Graham Gillmore | Exhibitions, Photographs | 53 | 11 | 200 dpi | [item 4920](https://afkcatalogue.sd44.ca/s/TheCollection/item/4920) |
| Betty Goodwin | Exhibitions, Photographs | 28 | 6 | 200 dpi | [item 5341](https://afkcatalogue.sd44.ca/s/TheCollection/item/5341) |
| Betty Goodwin | Press | 40 | 9 | 200 dpi | [item 5344](https://afkcatalogue.sd44.ca/s/TheCollection/item/5344) |
| J. Carl Heywood | Exhibitions, Images | 25 | 6 | 200 dpi | [item 4984](https://afkcatalogue.sd44.ca/s/TheCollection/item/4984) |
| E.J. Hughes | Images | 33 | 6 | 200 dpi | [item 5007](https://afkcatalogue.sd44.ca/s/TheCollection/item/5007) |
| E.J. Hughes | Press | 35 | 9 | 200 dpi | [item 5009](https://afkcatalogue.sd44.ca/s/TheCollection/item/5009) |
| Nuveeya Ipellie | Document | 40 | 6 | 200 dpi | [item 5028](https://afkcatalogue.sd44.ca/s/TheCollection/item/5028) |
| Pat and Rosemarie Keough | Press | 43 | 10 | 200 dpi | [item 5173](https://afkcatalogue.sd44.ca/s/TheCollection/item/5173) |
| Toni Onley | Press | 28 | 6 | 200 dpi | [item 5129](https://afkcatalogue.sd44.ca/s/TheCollection/item/5129) |
| Melia Padluq | Works | 20 | 3 | 200 dpi | [item 5180](https://afkcatalogue.sd44.ca/s/TheCollection/item/5180) |
| Ross Penhall | Press | 23 | 4 | 200 dpi | [item 5140](https://afkcatalogue.sd44.ca/s/TheCollection/item/5140) |
| Newgaleak Qimirpik | Works | 60 | 9 | 200 dpi | [item 5199](https://afkcatalogue.sd44.ca/s/TheCollection/item/5199) |
| Jack Shadbolt | Exhibitions | 215 | 18 | 130 dpi | [item 4637](https://afkcatalogue.sd44.ca/s/TheCollection/item/4637) |
| Jack Shadbolt | Press | 84 | 15 | 150 dpi | [item 4643](https://afkcatalogue.sd44.ca/s/TheCollection/item/4643) |
| Arnold Shives | Press | 24 | 6 | 200 dpi | [item 5219](https://afkcatalogue.sd44.ca/s/TheCollection/item/5219) |
| Gordon Smith | Exhibitions | 120 | 14 | 150 dpi | [item 4619](https://afkcatalogue.sd44.ca/s/TheCollection/item/4619) |
| Gordon Smith | Photographs | 38 | 7 | 200 dpi | [item 4623](https://afkcatalogue.sd44.ca/s/TheCollection/item/4623) |
| Gordon Smith | Press | 79 | 17 | 150 dpi | [item 4625](https://afkcatalogue.sd44.ca/s/TheCollection/item/4625) |
| Takao Tanabe | Exhibitions | 25 | 6 | 200 dpi | [item 5242](https://afkcatalogue.sd44.ca/s/TheCollection/item/5242) |
| Kabubuwa Tunnillie | Works | 104 | 16 | 200 dpi | [item 5253](https://afkcatalogue.sd44.ca/s/TheCollection/item/5253) |
| Charlene Vickers | Exhibitions, Images | 31 | 6 | 200 dpi | [item 5272](https://afkcatalogue.sd44.ca/s/TheCollection/item/5272) |

## 6. Volunteer (DS-58)

| # | Question | Until then |
| --- | --- | --- |
| 6.1 | Where does a filled-in volunteer form go: an email address, dropped off at the gallery, or by mail? The page can say so in its last line | "To apply, fill in the volunteer form (PDF). Questions? Contact us." |
| 6.2 | Would you take volunteer applications through the site's contact form instead of a PDF, so nobody has to print and scan? | The PDF |
| 6.3 | Is there a photo of a gallery attendant at work, for example greeting visitors at the front desk? The role cards could show one each; the page's other banner photo shows an Explore + Create apron, which would misrepresent the role | The role cards are text only; an event photo sits beside "Join the team" |
| 6.4 | Hero photos across the site have no alt text in Files. Descriptions can be added at release (before then the live theme would show them too) | Hero photos are decorative |
| 6.5 | Check the new heading "Join the team" and the last line "To apply, fill in the volunteer form (PDF). Questions? Contact us." | As written |

## 7. Plan your visit (DS-61)

| # | Question | Until then |
| --- | --- | --- |
| 7.1 | The page's address, gallery hours, admission and Artists for Kids office hours now come from Theme settings, Gallery details, so staff change them there, once, for this page, the home page, the contact page and the footer. Is that the right place for them? | As moved, words unchanged |
| 7.2 | Check the new wording: "Get directions" (opens Google Maps), and the visit details' labels "Gallery hours", "Admission", "Artists for Kids office hours" | As written |
| 7.3 | Holidays and one-off closures aren't known to the "open today" line. Is there a list of closures for the year, so the line can say "Closed for the holiday"? | The line follows the weekly days and times |

## At release (later)

- The product description clean-up (P-21, P-22): the gallery approves a before-and-after list of the 21 descriptions before anything changes.

## 6. Artists for Kids (`proposals/artists-for-kids-integration.md`)

The Artists for Kids site's pages moved here as written, 2026-09-27. These came up on the way, with the team's questions from the plan.

| # | Question | Until then |
| --- | --- | --- |
| 6.1 | Artists for Kids office hours: 8:30 to 4:30 on the old site and on Contact, 8:00 to 3:00 on Plan your visit. Which? | Both as written |
| 6.2 | The Foundation's phone (604.998.8563), "by appointment", and the summer closure (June 23 to September 18, 2026) are on the old site's Contact page but not on this site. Add them? | Not added |
| 6.3 | The old Contact page shows `admin@smithfoundation.ca` but its link writes to `info@smithfoundation.ca`. Which is right? | This site uses `admin@smithfoundation.ca`, as its Contact page does |
| 6.4 | Gallery Program: the self-guided tours text names *Collect, Assemble, Gather*, then "our spring exhibition, One Hundred Artists Deep" and "April through June"; "Class visits can be booked at the button below" has no button; the Spring 2027 text repeats the fall's (Grade 5, *Collect, Assemble, Gather*, September to February) and refers to a Register button that isn't there yet. Please send corrected text | As written |
| 6.5 | Gallery Program: the self-guided tour instructions (a PDF on the district's old server, which no longer answers). Please send the file | Left out |
| 6.6 | Learning Guides: "Creating a Paper Mural with Sandeep Johal" has a cover and no PDF. Please send the PDF | Its card is made but not shown |
| 6.7 | Samuel Roy-Bois, *My Sun*: 2024 in the caption, 2025 in the picture's description. Which? | As written |
| 6.8 | *The Art of Conversation* offered a 3D tour ("Explore The Art of Conversation in 3D!"), but its link is missing. The address? | No tour link |
| 6.9 | Names: "Sara Jean Bourget" (Paradise Valley) and "Sara-Jeanne Bourget"; "Mark Johnson" once on Mark Johnsen's page; "Elizabeth MacIntosh" and "McIntosh"; "Becky" and "Rebecca" Bair; "Artist for Kids" three times. Corrections? | As written |
| 6.10 | "AFK" in body text ("the founders of AFK", "the AFK studios", "the AFK Permanent Collection", "AFK's Paradise Valley"): may it be written out as "Artists for Kids" (P-39)? Titles, labels and headings already are | As written |
| 6.11 | Works named in lessons that differ from the collection's record: *Harlequin* (2019 in the lesson, 2003 in the collection), *Plains Cree Chiefs* (1996, 1995), *Einstein/Frankenstein* (2009 in one lesson, 2004 in another and the collection), *Pender Harbour* (2009, 2006), "Figure Maquette in Studio at Night" (the collection: *Painting and Figure Maquette in Studio at Night*), "All Kinds of Birds Flying North in Spring" (the collection: *All Kinds of Birds*). Each lesson shows the collection's work beside its own text | As written, work linked |
| 6.12 | Studio Art Academy isn't offered in 2026/2027. Show its page this year? | Shown, with its note |
| 6.13 | The Artists for Kids scholarships and the Foundation's scholarships are two sets of three. Should each page say how they differ, or link to the other? | No link |
| 6.14 | Check the new labels: the menu's Classes and camps, Schools and teachers, Support Artists for Kids; the buttons "Register for classes", "Register for camps", "Register for camp" (verb first, after the design review), "Register a Grade 5 class"; the groups "Also for families", "More classes and camps", "Awards and support", "How to give", "Learning guides" (on Sara-Jeanne Bourget's page) and "Lesson Videos"; the cards "Give online through CanadaHelps", "Give with a School Cash Online account", "Give by phone" with "Call us"; the link "Amelia Butcher at the gallery"; "Artists for Kids Classes and Camps" on Public programs and "Artists for Kids" in Donate's How to give | As shown |
| 6.15 | The team: how are fees collected after a registration form is sent? (T3) | The site says nothing about payment |
| 6.16 | The team: how do camps and scholarships take registrations when they open? (T4) | The buttons go to the old site's pages |
| 6.17 | The team: do the Microsoft Forms and the booking calendar get a new address each year? (T5) | The current addresses |
| 6.18 | The team: who keeps the "Fall 2026 at Artists For Kids" cards up to date each term? (T6) | The team, through the shared login |
| 6.19 | The After School Art photo (892 px wide) looks soft as a full-width hero. A larger copy? | The old site's copy |
| 6.20 | Classes and camps, Schools and teachers, Learning Kits and Learning Guides start straight with their cards. One or two sentences for each (who it's for; each programme page has its dates and registration)? Learning Guides could take its first heading, "Learning Guides Created by Artists with Artists For Kids", as that sentence, so the page doesn't open with two headings | No introduction |
| 6.21 | Larger copies of three small photos: Amelia Butcher in her studio (319 px wide), the clay kit event's picture (500 px) and Amelia Butcher's 2026 workshop (960 px) | The old site's copies |
| 6.22 | After School Art: "If you child requires support" (your child)? | As written |
| 6.23 | Artists-in-Residence: the two groups are "2026-2027 Artists In Residence" and "2025-2026 Artists-in-Residence". One form for both, as the page title "Artists-in-Residence"? | As written |
| 6.24 | Artists-in-Residence: the artists' cards show the old site's orange posters (name and dates set in the picture). Plain portraits would let the card's own title and date do that work. Do you have them? | The posters |
| 6.25 | Sara-Jeanne Bourget: the first heading repeats the page title; may it go, or be shortened to the drawing focus? And the residency has happened: should "This November ... is excited to offer" move to the past tense? | As written |
| 6.26 | Professional Development: the February workshop says more information comes in September 2026. Are the details ready? | As written |
| 6.27 | Support Artists for Kids: the second and third paragraphs say nearly the same thing. Keep both, or one? | Both |
| 6.28 | About Artists for Kids: the Paradise Valley photo's description says 1994 and its caption 1996. And which form of the Bill Reid print's title: *Xhuwaji / Haida Grizzly* (text) or *XHUWAJI/Haida Grizzly Bear* (caption)? | As written |

## 8. Whole-site design review (`proposals/site-design-review.md`)

Questions from the review of every page, 2026-09-27. Until the gallery answers, each shows as it does today.

| # | Question |
| --- | --- |
| 8.1 | Artists for Kids pages (add to 6.19, 6.20): a hero photo for Classes and camps, Schools and teachers and Support Artists for Kids; a larger day-camp photo than pvssa_25.jpg (889 px wide, visibly soft); on Sara-Jeanne Bourget's page, may the opening H2 that repeats the title go and 'Artist Bio' read 'Sara-Jeanne Bourget Biography' like the other three? |
| 8.2 | Names and casing (site-wide): 'Artists for Kids' or 'Artists For Kids' in running text (78 capital-F uses, including Theme settings text in Git); programme page titles in sentence case ('Music at the Smith'); one name per programme on cards and pages; one spelling of Artists-in-Residence; typographic quotes in Against the Latitude of “Progress”; the Shop menu label against the page title. |
| 8.3 | Exhibition list titles: could the three list pages be titled 'On now', 'Upcoming' and 'Past' to match the switcher and menu (the only fix for the switcher jump on phones; see DS-105)? |
| 8.4 | Collection data (add to 5.8, 5.14, 6.28): one form for undated works and ranges; medium casing and Watercolor/Watercolour; the jeff002, reid001-2, barr002, barr017/018/025 fixes; A/P vs AP and whether Pender Harbour's edition should read 'AP (ed. of N)'; 78 alts missing a full stop; 'Artist for Kids'' typo; REID008 title; nationality or Nation for artist entries; one or two sentences for three grouping introductions and a shorter Portfolio Collective name; the Permanent Collection intro wording; Pender Harbour 2009 or 2006 in the Landscape painting lesson. |
| 8.5 | Shop labels: sentence-case mediums, one size form, 'AP' written out, a shorter medium for Russna Kaur; one frame title pattern ('Frame for Pender Harbour'); one photo credit form and Donate's hero credit; a different Shop hero from the 2026 Fall Portfolio's; 'More from this portfolio' instead of 'You may also like'; cart policy ranges, the stray asterisk, which page is Terms of Service, and whether the policy sits before or under Check out (DS-124). |
| 8.6 | Shop landing: keep only the last paragraph (buying funds programs) as the introduction, staged in custom.release_body? The history paragraphs already live on three other pages. |
| 8.7 | Product descriptions: remove the typed caps block that repeats the label fields (artist, title, year, 'Limited Edition', 'Availability: Low Stock', 'PRINT DETAILS'), keeping Paper and Signature as one plain sentence or as fields; staged for release. |
| 8.8 | Programme and Artists for Kids copy: Explore + Create's typed 'PUBLIC PROGRAM' line, title line, email as a link and paragraphs; stale event notes and 'Tickets Coming Soon'; Art in Good Company's November and December dates; a sentence and booking route for the Curatorial Tour; Becky or Rebecca Bair; residency pages for Samuel Roy-Bois and Marlene Yuen; link labels that say what happens ('See the learning guides', 'Borrow a learning kit'); a Learning guides intro; whether the collagraph and trace monotype kits share one form; verb-first hero buttons ('Get the program guide', 'Read the year in review'); award names as point headings; one card-title pattern and phone format on Donate and Support; office hours 8 AM to 3 PM or 8:30 AM to 4:30 PM. |
| 8.9 | Foundation and Get involved labels: may '2025 A Year In Review' read 'Download the report', Public Programs get a link label like Donations, and 'Donate today' read 'Donate' as on Home? |
| 8.10 | Residency cards: can they use the plain portraits the name graphics were made from (each card shows the name three times)? |
| 8.11 | Contact form heading: may 'Contact us' under the H1 'Contact' read 'Send a message'? |
| 8.12 | Past exhibitions: are the Paths and Unfixed key images artworks or photos of the room? If photos, clear key_image_is_artwork on both (store write), update migration.py:281, 284 and preview.html:301. |
| 8.13 | From the Ground: list one entry per multi-part work (eight identical Charlene Vickers tiles today), or keep the parts? |
| 8.14 | Artists for Kids team: four separate portraits at least 800 px wide (then a people grid) and meanwhile a copy of the composite without its baked-in white frame? |
