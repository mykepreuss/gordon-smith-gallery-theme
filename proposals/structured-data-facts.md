# Facts for the structured data: what was found, and where

Date: 2026-09-28. Asked by Michael: "Can you find the facts we need from the gallery?"

`proposals/structured-data-review.md` lists the facts that would make the structured data better. This is what could be found without asking, where each came from and how sure it is. **Nothing here is in the theme or the store yet.** The gallery confirms; Michael decides.

How sure:

| Word | Means |
| --- | --- |
| Stated | The gallery's own site, store or old site says it |
| On record | A public register or the organisation's listing says it |
| Matched | Found elsewhere and checked against a fact we hold |
| To confirm | Found, with nothing of ours to check it against |

## 1. Artists: which person is meant

Each of the 171 artist entries was searched for on Wikidata. A match counts as confirmed only when the years of birth and death in our entry agree with Wikidata's.

| Result | Artists | With a Getty (ULAN) number | With a Wikipedia page |
| --- | --- | --- | --- |
| Confirmed: our years agree | 59 | 41 | 49 |
| Likely: one Canadian artist of that name, no year of ours to check | 34 | 23 | 26 |
| Possible: a name that matches, or found under another spelling | 8 | 2 | 3 |
| Not found | 70 | 0 | 0 |
| **All** | **171** | **66** | **78** |

The full list, with each address, is `proposals/store-writes/aeo/artist-identifiers.json`.

Gordon Smith is confirmed: Wikidata `Q5584785` ("Gordon A. Smith", 1919 to 2020), Getty `500009414`, Wikipedia "Gordon A. Smith". So are the founding patrons Jack Shadbolt (`Q6115081`) and Bill Reid (`Q615962`).

Most of the 70 not found are living artists with no Wikidata entry, such as Marlene Yuen, Russna Kaur and Sandeep Johal. Their own websites, which 60 or so entries already hold, do the same job.

**To use them** the artist entry needs a field, a list of addresses ("Described elsewhere"). That is a store write: a field definition, then 101 values. The theme already gives an artist's own website as `sameAs` and would add these to it.

## 2. What the search found wrong in our own records

These came up while matching. Each needs the gallery's check: Wikidata is not always right, and one of its dates below is almost certainly wrong.

| Artist | Our entry | Found | Note |
| --- | --- | --- | --- |
| David Blackwood | born 1941 | Died 2022 | |
| Christopher Pratt | born 1935 | Died 2022 | |
| Joe Fafard | born 1942 | Died 2019 | |
| Gathie Falk | born 1928 | Died 2025 | |
| Victor Cicansky | born 1935 | Died 2025 | |
| Audrey Capel Doray | born 1931 | Died 2025 | |
| Ian Wallace | born 1943 | Wikidata says died 2007 | Likely Wikidata's mistake: he is listed on the Foundation's board today |
| Molly Lamb Bobak | 1922 to 2014 | Born 1920 | |
| Patterson Ewen | No dates | "Paterson Ewen", 1925 to 2002 | Spelling |
| Charles Gagon | No dates | "Charles Gagnon", 1934 to 2003 | Spelling |
| Atilla Lukacs | Full name "Attila Richard Lukacs" | "Attila Richard Lukacs" | Our name and our full name spell it two ways |
| Jean McEwan | Full name "Jean Albert McEwen" | "Jean McEwen" | The same |
| Taiga Chiba | 1927 to 2013 | A Taiga Chiba born 1950 | May be two people. Not matched |

The six deaths matter most. The pages say "born 1941" of artists who have died, and the structured data repeats it.

## 3. The three organisations

| Fact | Value | Source | How sure |
| --- | --- | --- | --- |
| Foundation's full name | The Gordon and Marion Smith Foundation for Young Artists | About us, Support Artists for Kids | Stated |
| Foundation's legal name | THE GORDON AND MARION SMITH FOUNDATION FOR YOUNG ARTISTS | Benevity's listing of the register | On record |
| Foundation's charity number | 866075658RR0001 | Benevity's listing. Check it on the CRA's own list before use | On record |
| Foundation founded | 2002 | About us, The Smith Foundation | Stated |
| Foundation's purpose | An endowment whose revenue is granted to Artists for Kids and supports the gallery | Support Artists for Kids | Stated |
| Foundation's kind | A registered charity: gifts over $25 get a tax receipt | Donate | Stated |
| Artists for Kids established | 1989 | About us, Support Artists for Kids | Stated |
| Artists for Kids' kind | "a unique, not-for-profit, self-sustaining art education program operated by the North Vancouver School District" | Support Artists for Kids | Stated |
| Artists for Kids' parent | North Vancouver School District. Wikidata `Q7432191`, "School District 44 North Vancouver" | The same page; Wikidata | Stated; matched |
| The gallery built | 2012, at the Education Services Centre | Support Artists for Kids | Stated. An opening date is still question 10.11 |
| Who runs the gallery | Artists for Kids and the Foundation together, by the site's account. Benevity's listing says the Foundation "manages" it | About us; Benevity | To confirm. The two accounts differ |
| Wikidata entries | None for the gallery, Artists for Kids or the Foundation | Searched 2026-09-28 | |

So the data can say, from the site's own words: Artists for Kids is part of the North Vancouver School District, and the Foundation funds Artists for Kids. It can't yet say who the gallery belongs to.

## 4. Social profiles

All from the organisations' own sites: the Artists for Kids pages on sd44.ca, and the footer of all 53 saved pages of the Foundation's old site.

| Whose | Profile | Address |
| --- | --- | --- |
| Artists for Kids and the gallery | Instagram | `https://www.instagram.com/afk_smithgallery` |
| | Facebook | `https://www.facebook.com/afksmithgallery` |
| | X | `https://twitter.com/afksmithgallery` |
| | YouTube | `https://www.youtube.com/channel/UCBo3tcqxdV8lTdNEnT1lCwg` |
| The Foundation | Instagram | `https://www.instagram.com/the_smith_foundation` |
| | Facebook | `https://www.facebook.com/gordonandmarionsmithfoundation` |

How sure: stated. To confirm: that each is still in use, and whether the gallery and Artists for Kids share theirs or the gallery has its own.

The theme has one set of social links, for the gallery, in Theme settings. The Foundation's would need their own.

## 5. Contact

| Fact | Value | Source |
| --- | --- | --- |
| Email | `artistsforkids@sd44.ca` | The store's contact policy, refund policy and privacy policy |
| Foundation's email | `admin@smithfoundation.ca` | The live theme |
| Office hours | Two versions. Monday to Friday, 8 AM to 3 PM in Theme settings. Monday to Friday, 8:30 AM to 4:30 PM, closed July and August, in the store's contact policy | To confirm which |

## 6. Visiting

| Fact | Value | Source | For the data |
| --- | --- | --- | --- |
| Admission | By donation | Plan your visit | Free to enter. "By donation" can be said in words beside it |
| Wheelchair access | "wheelchair accessible, with accessible washrooms on the Main level and level 1" | Plan your visit | Stated |
| Parking | One-hour street parking; pay parking on Lonsdale; underground on P1 and P2, not weekends or holidays; accessible parking on P1 and P2 | Plan your visit | Stated |
| Transit | SeaBus to Lonsdale Quay, then the 229 or 230 bus. Stop 54200 | Plan your visit | Stated |
| Map position | 49.3291934, -123.0726507 | The store's address record | In the theme since DS-163 |

## 7. The Shop

All from the store's own policies, read 2026-09-28.

| Fact | Value | For the data |
| --- | --- | --- |
| Returns | "all sales are final. Refunds, returns, or exchanges are not offered." | No returns |
| Damaged or wrong item | Contact within 7 days of delivery or pickup | Said in words |
| Shipping, unframed | $20 within Canada | A flat rate of 20 CAD, to Canada |
| Ships to | Canada only: the store's one shipping zone (`proposals/store-settings-review.md`) | Canada |
| Handling | 3 to 5 business days | 3 to 5 days |
| Pickup | Free, at the gallery. 1 to 2 business days | Said in words |
| Framed prints | Pickup only, 2 to 3 weeks | Said in words |

One thing to settle first. The shipping policy says $20 and also that shipping "will be calculated and confirmed with you at the time of the order". That is item 12 of the store settings review. The data should wait for one answer.

## 8. Not found

| Fact | Why |
| --- | --- |
| Marion Smith's dates | Not on the site or the old sites. Question 10.15 |
| When the gallery opened | 2012 is when it was built. Question 10.11 |
| Who owns the building | Question 10.11 |
| Copyright and licence for images of works | A rights question for the gallery |
| A work's height and width as numbers | The size is text. Which side is the height isn't recorded |
| Curators as people | The curator credit is one line of text |
| An event's price | Registration links give none |

## What can be built, and what each needs

| Step | Facts | Needs |
| --- | --- | --- |
| A. Returns and shipping on each edition | Section 7 | Michael's go-ahead. The gallery's answer on the $20. Theme only |
| B. The gallery's social profiles and email | Sections 4 and 5 | The gallery confirms them. Theme settings only |
| C. Admission and access on the gallery | Section 6 | Michael's go-ahead. Theme only, from words the page already shows |
| D. The organisations: dates founded, the Foundation's full name and charity number, the school district as Artists for Kids' parent | Section 3 | The gallery confirms. Theme only |
| E. Artists described elsewhere | Section 1 | A new field on the artist entry and 101 values: a store write, so Michael's go-ahead and a before-snapshot |
| F. Corrections to artists' dates and names | Section 2 | The gallery's check, then a store write |

## How the search was done

- Wikidata's public search, by each artist's name and other names, then each candidate's type, occupation, citizenship and years. A person was accepted only as a human with an artist's occupation or a Canadian description.
- The second pass searched by text for the artists not found, and kept a match only when the names were close. Four were kept as possible; three were thrown out as different people (a New Zealand painter, a glass artist, a wildlife artist).
- The store's policies and settings through the Admin API, read only.
- The site's own pages on the review theme.
- The Foundation's old site from the saved copy (`~/Downloads/smithfoundation-media/pages`), and the Artists for Kids pages on sd44.ca.
- Nothing was written to the store, the theme or Wikidata.

## Sources

- Wikidata: https://www.wikidata.org
- Benevity, the Foundation's listing: https://causes.benevity.org/causes/124-866075658RR0001
- Artists for Kids on sd44.ca: https://www.sd44.ca/school/artistsforkids/Pages/default.aspx
- Wikipedia, Gordon A. Smith: https://en.wikipedia.org/wiki/Gordon_A._Smith
