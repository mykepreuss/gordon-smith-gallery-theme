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
| 1.5 | Access to the Mailchimp for Shopify app's settings, or someone to check them: customer sync on, the right audience, consent carried over, double opt-in | The sign-up form can't be tested end to end |
| 1.6 | A staff member for the editing test: about half an hour in the review theme's editor, changing an exhibition, an event, a card, a page's fields and a product's label | Staff editing isn't verified |

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
| 3.7 | Roz Marshall's link on the Artists page goes to `rozmarshall-artist.com`, which no longer exists. A new address, or remove the link? | The dead link stays |
| 3.8 | The Paradise Valley photo on the Artists for Kids page: its description says 1994, its caption 1996. Which year? | Both as written |

## 4. Brand

| # | Question | Until then |
| --- | --- | --- |
| 4.1 | The land acknowledgement's place names use letters Mulish doesn't have (ʔ, ɬ, θ, some accents), so those letters show in Arial. Accept that, or load a font made for BC Indigenous languages for that text (for example BC Sans)? (Q11) | Arial for those letters |
| 4.2 | Is there a "GS logo clusters document" (the brand guide refers to it on pages 3 to 5)? (Q1) The About Us page has a cluster image (`triad_logo_cluster.png`, 329 × 201 px); is that the approved cluster, and is there a vector version? | Logos shown side by side, not as a cluster. About Us shows each logo beside its own description instead (DS-50) |
| 4.3 | May the site use a teal version of the text-only Gallery logo, which the brand guide shows but wasn't supplied? (Q3) | Not used |
| 4.4 | Should gallery images open larger when clicked? (Q8) | They don't |

## 5. The Permanent Collection (`proposals/permanent-collection.md`)

The collection is on the review site as of 2026-09-27: 1,168 works, 171 artists, 26 groupings. The review sheets are in `proposals/store-writes/collection/sheets/`; a correction there goes back into the store by running the import again.

| # | Question | Until then |
| --- | --- | --- |
| 5.1 | ~~Do the image permissions cover showing the collection on gordonsmithgallery.com?~~ Answered by Michael, 2026-09-26: "We gave all the image rights" | |
| 5.2 | Credit lines: name donors ("Gift of Alan & Elizabeth Bell"), or the collection credit alone? | The collection credit alone, as the catalogue records it (84 works have none) |
| 5.3 | Michael asked for everything (2026-09-26), so the Teaching Collection (195 works) is its own grouping and the artists' Text Resources are on their pages (180 files). Left out: the 6 works on loan, and 39 PDFs over 20 MB, Shopify's limit (listed in `problems.csv`). Are smaller copies of those 39 available? | Those 39 aren't on the site |
| 5.4 | Review the artists sheet (`artists.csv`): names, sort names, full and other names, life dates. 313 spellings became 171 artists. Dates are left off for 10 where the catalogue's disagree or can't be right (Kenojuak Ashevak has 1909 to 1976 and 1927 to 2013; Jackson Beardy and Jean-Paul Riopelle have birth years after their works) | Names as the site or catalogue has them; those 10 without dates |
| 5.5 | ~~Where are the original image files, and who at the district's IT can help?~~ Answered: the images came from the catalogue's own masters (converted, and the masters left where they are), and Michael, 2026-09-26: "we won't change anything with DNS, that's outside of our scope" | |
| 5.6 | The catalogue keeps running as the district runs it. Its private records (where each work is, provenance, donors) stay there; nothing private moved. Is that right, or should they live somewhere the gallery controls? | They stay in the catalogue |
| 5.7 | The Artists page lists every artist with work in the collection or an edition in the Shop, 171 names, and each name opens the artist's page on the site, with the works, the editions, the exhibitions and one link to the artist's own website. Is there anyone who shouldn't be listed, or a website link to drop? | Everyone is listed; the 59 links moved as they were (see 3.7) |
| 5.8 | The Artists page's two paragraphs are about the Limited Edition Portfolio artists. With the whole collection listed under them, would the gallery like to adjust the wording? | As written |
| 5.9 | The catalogue's Published Editions paragraph (1990, Bill Reid's *Xhuwaji / Haida Grizzly*, "Entering its 37th year") is the introduction to the Artists for Kids Published Editions grouping, word for word. Keep it? | Kept as written |
| 5.10 | Check the other sheets: `titles.csv` (481 titles whose edition number moved to the Edition field, e.g. "Untitled (30/40)" is now "Untitled", edition 30/40), `problems.csv` (works without a title, image or category; accession numbers used twice; 11 cataloguer notes after "*" left off the site), `themes.csv` (the catalogue's 30 subject words tidied to 15 themes) and `groupings.csv` | As in the sheets |
| 5.11 | Names chosen where the catalogue has no page for the artist: "Unknown Inuit artist" (catalogue: "Unknown [Inuit Origins]"), "West Baffin Eskimo Co-operative" ("West Baffin Eskimo Coop. LTD"), "T&T Collective" for Tyler Brett and Tony Romano (as *Collect, Assemble, Gather* names them), "Vancouver School Collective". Right? | As chosen |
| 5.12 | Featured works on the Permanent Collection page: Bill Reid's *Xhuwaji/Haida Grizzly Bear*, Gordon Smith's *Painting After Goya*, Jack Shadbolt's *Winter Garden*, E.J. Hughes's *The Mill at Mesachie Lake*, Robert Davidson's *Crab of the Woods* and Kenojuak Ashevak's *Untitled [Loons Protect The Owl]*. Which six should it show? (Content, Metaobjects, Collection grouping, Featured works) | These six |

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
