# A Wikidata entry for the gallery

Michael said yes on 2026-10-01 (follow-up doc, question 6). The gallery, Artists for Kids and the Foundation have no Wikidata entry. An entry tells search engines and AI assistants exactly which gallery is meant. Every statement below is a fact already on the site, with the page that says it as its reference.

Creating it needs a Wikimedia account, so Michael makes it. It takes about five minutes.

1. Sign in at wikidata.org.
2. Wikidata asks people to say when they edit about an organisation they work with. Add one line to your user page: "I help the Gordon Smith Gallery of Canadian Art with its website."
3. Open QuickStatements (quickstatements.toolforge.org), choose New batch, paste the block below, then Import V1 commands and Run.
4. Send the new entry's address (Q followed by a number). The site then names it in the gallery's data for search engines, as it does for the artists (DS-197).

```
CREATE
LAST	Len	"Gordon Smith Gallery of Canadian Art"
LAST	Aen	"Gordon Smith Gallery"
LAST	Den	"public art gallery in North Vancouver, British Columbia, Canada"
LAST	P31	Q1007870	S854	"https://gordonsmithgallery.com/pages/about-us"
LAST	P17	Q16
LAST	P131	Q1001626	S854	"https://gordonsmithgallery.com/pages/plan-your-visit"
LAST	P6375	en:"2121 Lonsdale Avenue, North Vancouver, BC"	S854	"https://gordonsmithgallery.com/pages/plan-your-visit"
LAST	P571	+2012-00-00T00:00:00Z/9	S854	"https://gordonsmithgallery.com/pages/about-us"
LAST	P127	Q7432191	S854	"https://gordonsmithgallery.com/pages/about-us"
LAST	P138	Q5584785
LAST	P856	"https://gordonsmithgallery.com"
```

| Statement | Value | From |
| --- | --- | --- |
| Instance of (P31) | art gallery (Q1007870) | About Us |
| Country (P17) | Canada (Q16) | Plan your visit |
| Located in (P131) | North Vancouver (Q1001626) | Plan your visit |
| Street address (P6375) | 2121 Lonsdale Avenue, North Vancouver, BC | Plan your visit |
| Inception (P571) | 2012 | About Us: "The Gallery opened in 2012" |
| Owned by (P127) | School District 44 North Vancouver (Q7432191) | About Us: "owned by the North Vancouver School District" |
| Named after (P138) | Gordon A. Smith (Q5584785) | Gordon and Marion Smith |
| Official website (P856) | https://gordonsmithgallery.com | |

The identifiers were checked against Wikidata's search on 2026-10-01. Gordon Smith's (Q5584785) is the one the site already gives his artist page (`proposals/store-writes/aeo/artist-identifiers.json`).
