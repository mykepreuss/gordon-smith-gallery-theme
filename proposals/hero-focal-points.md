# Hero focal points (IMG-02, IMG-03)

Checked 2026-09-26 on the review theme's code (development theme), every hero at 1440, 768 and 390.

- **Nothing has a focal point yet:** every hero is centred.
- **Desktop and tablet crops hold their subject everywhere.**
- **On phones the hero is portrait.** It shows about the middle 60% of a landscape photo, so art or people that sit off-centre drop out.
- **Artwork heroes are never cropped** (*Collect, Assemble, Gather*, *Against the Latitude of "Progress"*), so they need nothing.

Shopify's API can't set focal points. Someone signed in to the admin sets each one on the file itself, and every use of that image follows it.

## Set these

Each point was tried on the preview at 390 and 768 before recommending it. "Across" is the focal point's position from the image's left edge; "down" stays at 50% for all of them.

| Page | File | Across | What it keeps in frame on a phone | Other uses of the file |
| --- | --- | --- | --- | --- |
| Volunteer | `KHIMMATAHIPOL_29.jpg` | 80% | Both people, not one and a half | None in the new theme |
| One Hundred Artists Deep | `GSG_One_Hundred_Artists_011.jpg` | 25% | The purple sculpture as well as the plinth works | Its card on Past (same shape, no change) |
| From the Ground | `GSG_From_the_Ground_RTP_002_c68a6647-c04b-48f3-804b-d3aa06f5b7a4.jpg` | 15% | The photographs and the clay tables, not empty wall | Its card on Past shifts slightly left and still shows the red sculpture's edge |
| Playhouse | `GSG_Playhouse_003.jpg` | 90% | The large blue painting | Its card on Past (same shape, no change) |
| Prevailing Landscapes | `GSG_-Prevailing-Landscapes-002.jpg` | 15% | The whole title panel and the sculpture | Its card on Past (same shape, no change) |
| 2026 Spring Portfolio | the collection's image | 20% | Both children and the portfolio name on the wall | None |
| 2024 Fall Portfolio (optional) | the collection's image | 30% | The whole portfolio name on the wall; one column of prints drops out instead | None |

Left centred on purpose:
- **2025 Spring Portfolio:** no single point keeps both the wall's title and the prints, and the centre shows the most prints.
- **Speaker Series and Music at the Smith:** four people in a row can't all fit a portrait crop, and the centre keeps the middle two.

## How

In the Shopify admin: **Content > Files**, search for the file name, open it, and place the focal point at the position in the table. For a collection's image, open it from the collection (**Products > Collections**, then the image).

It's a change to a shared file, so the live theme may follow it too. Where the live theme's banners honour focal points, their phone crops shift the same way. Nothing else about the live pages changes.

After setting them:
- Check the pages on the review theme at phone width. The hero's image carries `object-position` with the new values.
- That check also closes the first item in DESIGN.md §9.6: `image_tag` writes a file field's focal point.
- Log it in `proposals/store-writes/README.md`.
