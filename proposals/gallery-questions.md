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

| # | Question | Until then |
| --- | --- | --- |
| 5.1 | Do the image permissions (CARFAC or artists' agreements) cover showing the collection on gordonsmithgallery.com? The catalogue shows them today at afkcatalogue.sd44.ca | Nothing from the collection is made public |
| 5.2 | Credit lines: name donors ("Gift of Alan & Elizabeth Bell"), or the collection credit alone? | The collection credit alone |
| 5.3 | Publish the Teaching Collection (195 works) and the artists' Text Resources (press, exhibition lists)? Leave out the 6 works on loan? | Teaching Collection and Text Resources left out; loans left out |
| 5.4 | Review the artist names and life dates: 313 spellings become about 204 artists, and some conflict (Ann Meredith Barry has four sets of dates) | Names as the catalogue has them, dates left off where they conflict |
| 5.5 | Where are the original image files (the catalogue holds 36 GB of TIFFs), and who at the district's IT can help with the download and, later, the redirects? | The trial uses 20 works' files from the catalogue |
| 5.6 | Once the catalogue retires, where do the private records live (where each work is, provenance, donors)? | They stay in the catalogue |

## 6. Volunteer (DS-58)

| # | Question | Until then |
| --- | --- | --- |
| 6.1 | Where does a filled-in volunteer form go: an email address, dropped off at the gallery, or by mail? The page can say so in its last line | "To apply, fill in the volunteer form (PDF). Questions? Contact us." |
| 6.2 | Would you take volunteer applications through the site's contact form instead of a PDF, so nobody has to print and scan? | The PDF |
| 6.3 | Is there a photo of a gallery attendant at work, for example greeting visitors at the front desk? The role cards could show one each; the page's other banner photo shows an Explore + Create apron, which would misrepresent the role | The role cards are text only; an event photo sits beside "Join the team" |
| 6.4 | Hero photos across the site have no alt text in Files. Descriptions can be added at release (before then the live theme would show them too) | Hero photos are decorative |
| 6.5 | Check the new heading "Join the team" and the last line "To apply, fill in the volunteer form (PDF). Questions? Contact us." | As written |

## At release (later)

- The product description clean-up (P-21, P-22): the gallery approves a before-and-after list of the 21 descriptions before anything changes.
