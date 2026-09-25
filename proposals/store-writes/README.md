# Store writes log

Every write to the store's Admin resources, with what it was for and how to undo it. Theme files aren't here: they're in Git and pushed only to the review theme (`AGENTS.md`).

Before any write: recheck the store domain, the live theme ID and role, and take a before-snapshot.

## 2026-09-25: exhibition and event definitions, first entries

**Why:** to review the exhibition pages with real content in the development theme. Michael's go-ahead, 2026-09-25 ("Create entries"). Definitions are content model parts 2 and 5 (approved, P-10 to P-12, P-16).

**Checked first:** store `ed35ee-ea.myshopify.com` (Artists for Kids & The Gordon Smith Gallery), timezone America/Los_Angeles; live theme `183162372393` "Colorblock: NEW WEBSITE", role MAIN (`shopify theme list`). Before-snapshot: the store had 20 metaobject definitions, all Shopify's standard product-taxonomy types (`shopify--*`), and no `exhibition` or `event` type.

**Made through the Shopify connector (Admin GraphQL):**

| What | ID | Source |
| --- | --- | --- |
| Definition `exhibition` (22 fields, publishable, renderable, web pages at `/pages/exhibitions/<handle>`, storefront read) | `gid://shopify/MetaobjectDefinition/23753359657` | `definitions.py exhibition` |
| Definition `event` (9 fields, publishable, storefront read; `exhibition` field limited to the definition above) | `gid://shopify/MetaobjectDefinition/23753392425` | `definitions.py event` |
| Exhibition `collect-assemble-gather`, active. From the On Now page: dates, curator credit, 19 artists, opening reception, key image (artwork) and caption, summary, text, credits, Canada Council logo | `gid://shopify/Metaobject/608352043305` | `entries.py exhibitions` |
| Exhibition `one-hundred-artists-deep`, active. From its page and template: dates, curator, 8 artists and 3 founding artists, key image and credit, summary, text, 9 installation views and credit | `gid://shopify/Metaobject/608352076073` | same |
| Exhibition `against-the-latitude-of-progress`, active. From the Upcoming card: title, dates, image (artwork). No text yet, so its card doesn't link | `gid://shopify/Metaobject/608352108841` | same |
| Exhibition `play`, active. From the Past archive (2020 to 2021): title, dates, image (DS-25) | `gid://shopify/Metaobject/608352141609` | same |
| Event `curatorial-tour-collect-assemble-gather`, active. From the On Now page: October 26, 2026, 3:30 to 4:30 PM, linked to Collect, Assemble, Gather | `gid://shopify/Metaobject/608352272681` | `entries.py event` |

Text is the gallery's, moved without rewriting. Pasted formatting (inline Poppins, Word markup) stayed behind. Two small format changes to fit the fields: the curator credit and reception note lost their trailing punctuation and pipes ("Welcome Ceremony | 7 PM" became "Welcome ceremony at 7 PM", the content model's example).

**Effect on the live site:** none seen. The entries' addresses return 404 on gordonsmithgallery.com, because the live theme has no exhibition template; nothing on the live theme reads these entries. Checked 2026-09-25 (`/pages/exhibitions/collect-assemble-gather`, `/pages/exhibitions/play`).

**Undo:** delete the five entries (Content, Metaobjects), then the `event` definition, then the `exhibition` definition. Nothing else refers to them.

**Still to create** (content model part 2, migration step 1): the other 11 exhibitions, the other events, and the page, card, product and collection fields (parts 1, 3, 4, 6).
