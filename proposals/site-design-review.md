# Whole-site design review

Status: **Built on the branch, 2026-09-27; in review.** Every page of the new site was reviewed with the design skills and the fixes are built on `claude/site-design-review`, which sits on the Artists for Kids branch (pull request 42). The new rules are **Proposed** (DS-84 to DS-130) for Michael. Nothing the live site shows has changed.

## Why

Michael, 2026-09-27: "Do the same using all of our design skills ... on every page of our new version of the site ... we want the design to be as good and consistent as possible while respecting the design system and brand guideline. Overall, we like what we have but want to improve where we can. We also want to use consistent components and reduce duplication, drift, or any slight variance when it is not warranted."

## How it was done

1. **Review.** 29 reviewers, each reading the design skills first (frontend-design, better-ui and the other interfaces skills, emil-design-eng and Emil's motion skills, with the design system winning over any skill):
   - 15 page groups: home; the exhibition lists; exhibition pages; the Permanent Collection; Artists A to Z and artist pages; work pages; the Gallery's programme pages; About, visit, volunteer, contact and FAQ; the Foundation; three groups of Artists for Kids pages; the Shop; product pages; cart, search, 404 and blog.
   - 14 parts of the system, across every page: header and navigation; footer and newsletter; heroes and page heads; cards and grids; rich text; links, buttons and states; layout and spacing; colour and brand; forms and commerce; motion; CSS code; Liquid code; accessibility; typography.
   Each worked from screenshots of 62 pages at 390, 768 and 1440 px, took more at 320, 990 and 1200, measured in the browser and read the code.
2. **Verify.** A second agent for each reviewer tried to refute every finding by reproducing it. Of 474 findings, 269 were confirmed, 150 kept with a corrected fix, and 55 refuted.
3. **Merge.** Five area mergers turned the 419 kept findings into one change per root cause, preferring the fix that removes a variant or duplicated code. A final planner ordered them, design system first, and split out decisions, store changes, gallery questions and holds.
4. **Build.** Seven batches, each by one implementer who tested on the development theme, ran every check and committed.
5. **Check.** Every page captured again and compared with the first captures, each regression confirmed by a second agent, then fixed (see "Verification").

## What changed

Bugs visitors hit, fixed:
- The event's exhibition link showed in the browser's default blue.
- The Menu drawer stayed open when focus tabbed out of it.
- The sticky letter bar on Artists A to Z covered focused names.
- The contact form could post an empty message; every required field is now checked, with one error pattern for both forms.
- Empty sections added extra space on three pages.
- The artwork hero's caption floated up to 120 px below the work.
- Photo heroes looked soft on phones; they now ask for their real width.
- Pages scrolled sideways at 320 px (Foundation pages, Learning kits), and focus rings were clipped in the phone rails and on the logo.
- Dates and times broke inside a date or before "PM".

Variance removed:
- One rich-text path (`gs-rich-text`), so every staff text gets the external-link cue, same-tab links and a `srcset`, whether it's page text, exhibition text, a biography, a lesson or a product description.
- Link states written once: standalone links, crumbs, pagination and card titles thicken on hover and press; quiet links (dropdowns, footer, lists) underline.
- One button that wraps, with the Menu toggle a real secondary button; one field geometry.
- One title block for cart, search and 404; one empty state (`gs-empty`); one date format.
- The count rules (DS-44, DS-52) on every grid of cards, and a lone card takes the spare room anywhere (DS-92).
- Alt text never repeats a title that follows the image.
- Tokens for the remaining raw values; fixed colour uses named as roles (DS-84).
- Shared snippets for repeated logic: `gs-title-block`, `gs-paragraphs`, `gs-names`, `gs-tel`, `gs-lead-exhibition`, `gs-grid-sizes`, `gs-set-card`, `gs-open-hours`.
- Dead sections (`gs-shop-feature`, `gs-page-head`), unused CSS and an unused logo removed; logo files about 40% smaller.
- Search: headed groups with pages first, and an empty state that points on. Tab titles in our words. Curly apostrophes in our UI words.
- New lint rules (raw durations and ratios, `transition: all`, palette primitives outside tokens, hover outside the fine-pointer query, lists without a role) and `design-system/scripts/audit_links.py` for browser-default links.

Commits: `ad533c5` tokens and components, `28ffd46` components, `f197898` scripts, `bf529ad` snippets, `77ee7a9` and `8f7099e` sections, `65f737f` locales, settings, docs and checks.

## Decisions for Michael

Built on the branch as Proposed (each small or backed by measurements; each can be reverted on its own):

| ID | Title | Decision and reason |
| --- | --- | --- |
| DS-84 | Fixed ink and paper uses become named roles | Components use named fixed roles (field, on-colour hover, skip link, editor warning) instead of raw --gs-ink, --gs-paper and --gs-afk-rule, and the lint flags primitives outside tokens.css. Both file headers forbid raw palette in components; 19 uses make a deliberate fixed colour indistinguishable from a slip. No visible change |
| DS-85 | Every title-box H1 uses the heading measure | The hero box title uses --gs-measure-heading (20ch) like the page header, replacing the raw 16ch. Resolves the held hero-title-measure item: 9 of 23 photo-hero titles lose a line at 1440 and siblings stop wrapping differently on a 24 px margin |
| DS-86 | Below 990 px the photo hero box spans the image | Below 990 px the title box runs the image's full width, so only its own rounded corner shows. Resolves the held hero-corner item: today a 16 to 28 px photo strip cuts the curve into two partial corners (DS-03) |
| DS-87 | Closing rows share one column split | From 990 px Visit, the newsletter band and the footer use two equal columns and the gutter gap, so their right columns start on one line. Three right-column edges and three gaps (64, 48, 32) for one job in the last two screens of every page |
| DS-88 | Events lists keep one reading edge | Once any event in a full list has a picture, every row uses the picture column, so titles share one left edge (extends DS-51). Upcoming events titles alternate between x 120 and 552 at 1440 across 13 rows |
| DS-89 | Figure cap for videos and phones (amends DS-77) | Videos in text stop at the photo cap, and on phones the cap is 80svh so photos fill the column. A square video draws 682 px tall beside photos capped at 512; phone portraits fall 17 px short for no gain |
| DS-90 | Stacked details keep one column | §6.13 records that .gs-details--stack is one column at every width (the built behaviour), with two across at tablet width as Michael's alternative. The rule is declared three times and §6.13 describes the dead version |
| DS-91 | One 'belongs to' rule marks the nav section | An exhibition page marks Exhibitions, a product or portfolio marks Shop, and an artist, work or grouping marks Collection, at most one section. Exhibition, product and collection pages mark nothing today while the work page marks Collection (§6.1: 'so people still see where they are') |
| DS-92 | A lone card in any grid takes the spare room (extends DS-74) | Any grid of cards with one card uses the single-card layout, not only card groups. Four exhibition pages and 39 artist pages end with one card on a third of the row |
| DS-93 | One order for an edition's facts | The work page lists medium, edition, dimensions, as the product page and tiles do. The same object shows its facts in two orders on sibling pages |
| DS-94 | A picture that opens a part leads below 990 px (first slice of DS-79) | A page-text part whose text opens with a figure shows the figure first below 990 px; DS-79's record is corrected to say what is true. DS-79 claims a mitigation that doesn't exist: Studio Art Academy's opening picture shows after 1,445 px of text at 390 |
| DS-95 | What's on doesn't repeat the hero's image (amends DS-71) | When the lead exhibition has no installation views, its event card tries the programme page's hero before the key image. The same photo is the hero and the Curatorial Tour card on one first screen |
| DS-96 | Gallery hours from one source | Footer, Visit, Plan your visit and Contact render the hours from the structured opening settings; the free-text field is only a fallback. Staff type the same hours twice and two formats sit on one page |

Proposed only, not built (they change a Decided rule, reach far, or need a choice):

| ID | Title | Decision and reason |
| --- | --- | --- |
| DS-97 | Q12: Foundation header logo at one size | The Foundation header logo is the simple lockup at 72 px at every width, with a 32 px gap from 1200, so the bar fits one row from 1240 (option B: the full lockup per brand guide p.8). The Foundation bar wraps to two rows on 1280 and 1366 laptops, moving the nav between programmes |
| DS-98 | Nav ends at the utility row's right edge | From 1200 px the main nav aligns right, so labels stay put between programmes. The nav's start moves up to 140 px by programme; build only with DS-97 |
| DS-99 | Photo hero narrows to the text column from 990 to 1391 px | In that band image, box, credit and text share one left edge. An 11 px near miss at 1366; the recommendation is to keep today's geometry |
| DS-100 | Photo hero credit beside the box | From 990 px a photo hero's credit sits under the photo, right of the title box. The credit sits 497 to 549 px below its photo while the space under the photo is empty |
| DS-101 | Artist header names line gets a type role | Both header lines are decks (recommended), replacing the one-off regular-weight deck. The lighter line carries the name and the bold line the lesser fact; the style exists nowhere else |
| DS-102 | Edition and frame pages open with a crumb | Product pages open with a crumb to Limited editions (or the product's portfolio), as the work page does. Every other detail page has a crumb; frames have no way back (adds to DS-38, DS-80) |
| DS-103 | Open dropdown button loses the current underline | On the bar only the current section is underlined; the chevron and panel edge show which dropdown is open. Two sections look current when a dropdown is open |
| DS-104 | Drawer sections open independently (revisits DS-11) | In the Menu drawer several sections can be open; the bar keeps one at a time. Tapping a section collapses the one above and the tapped row jumps 232 px |
| DS-105 | Heading measure 22ch | --gs-measure-heading goes from 20ch to 22ch. 'Upcoming Exhibitions' wraps while its siblings don't, so the switcher jumps 38 to 68 px between them |
| DS-106 | A one-paragraph description is the page header's deck | A single-paragraph description in a page header renders as the deck. All limited editions shows its sentence as regular prose where every other header has a bold deck |
| DS-107 | Wide exhibition card side by side from 990 px (amends Decided DS-34) | The wide card stacks below 990 px and goes 7:5 from 990, as the other 7:5 splits do. At 768 the summary runs 10 lines of 31 characters beside a 300 px image |
| DS-108 | One document tile (amends DS-69, DS-75) | Document shelves use the Decided DS-63 tile; a document among photo cards keeps the 4:3 card. The same PDF renders two ways, and caps titles wrap to 4 or 5 lines on phones |
| DS-109 | Blank mat for a work without an image | A work tile without an image shows the blank mat, as a document tile does. A missing image leaves a 368 px hole that pushes the label 384 px above its neighbours' |
| DS-110 | Detail pages lead with one image below 990 px | Below 990 px work and product pages show the first image, then the label, price and action, then the other views. Multi-view works put the title 9,884 px down at 390 |
| DS-111 | Detail mats follow the work's shape (extends DS-55) | Detail mats take the work's ratio between 4:5 and 4:3, with a height cap, as the artwork hero does. A 3.33:1 print floats in a square mat and pushes the label down |
| DS-112 | Work label follows long runs of views | From 990 px on tall screens the collection work page's label sticks while views scroll. barr025 leaves about 20,000 px of empty right column |
| DS-113 | Site search finds exhibitions, lessons and artists | Search page 1 adds exhibition, lesson and artist matches. No exhibition can be found by name once old pages are hidden at release |
| DS-114 | Search results as text cards | Page and article results render as compact text cards in a one-column list. A second 'text under a rule' pattern with 24 px targets |
| DS-115 | Event rows name their programme | Outside its own programme page, an event row names and links its programme page. Rows on Upcoming events don't say who they are for |
| DS-116 | Link cards with a note are rows on phones (amends DS-73) | Below 750 px a link card with a short note is a row like the others. One card with a note turns a group into 1,148 px of full-width photos |
| DS-117 | Beside layout written once | The single, rows and event picture-beside-text layouts share one rule keyed on a column variable. Five copies with different ratios; offers and shelves on one page don't line up |
| DS-118 | Tile prices sit level | Prices in a row of artwork tiles align to the tile bottom. A two-line medium drops one price 22 px |
| DS-119 | Section-head links under the heading below 990 px | Below 990 px a section head's 'more' links sit under the heading. Where the link lands depends on label length, so neighbouring heads differ |
| DS-120 | Artwork tiles are decorative when the label follows | Tile and cart images have empty alt because the museum label follows (as DS-63), amending §6.4. Every Shop tile reads artist and title twice; §6.4 and DS-58 disagree |
| DS-121 | Page titles end with the programme | Browser titles end with the header logo's programme name instead of the store name. Every title ends with 'Artists for Kids & The Gordon Smith Gallery' against §2.1 |
| DS-122 | Where 'Browse' lands | The Permanent Collection button either keeps opening the search (A) or lands on Browse the collection (B, store write). The button's word matches the next heading, not its target |
| DS-123 | Chevrons turn with their panels | Two durations: 120 ms for every reveal and state change, 160 ms for the press. The chevron is still turning after its panel has gone |
| DS-124 | Cart summary before the policy on small screens | Below 990 px the cart shows subtotal and Check out before the policy text. Check out sits 913 to 1,370 px down at 390 |
| DS-125 | Offer a print's frame in the cart | A cart line whose print has a linked frame offers 'Add its frame' under it. Buying print and frame takes a round trip today |
| DS-126 | Eyebrow and deck rhythm | §5.1 records the built 12 px above H2s and 16 px above H1s (recommended), or the CSS builds §5.1's 12/16/24. The spec matches neither built pattern |
| DS-127 | Switcher groups with its title | The switcher sits closer to the page title than to the content. Tabs sit as far from the title as from the content |
| DS-128 | On now chip on the accent box | The strong chip is ink with paper text on paper and accent. In the hero box the chip is dimmer than the button beside it (DS-21 follow-on) |
| DS-129 | Engage page and Learning kits order | Engage is hidden and forwarded to Public programs at release, and Learning kits groups each kit with its plans. Every text has one home (P-30); related things sit together |
| DS-130 | More exhibitions fills its row | When fewer than three current shows remain, More exhibitions tops up with recent past shows. Four exhibition pages end with one lone card |

Already waiting from earlier reviews, with new evidence in DESIGN.md §12: DS-72 (a 58ch measure: three desktop reading widths today), DS-79 (a figure partway through a part), DS-81 (option B added: inline links thicken on hover instead of a new fill colour), DS-70a (lesson options). Q12 now has a proposed answer, DS-97.

## Store changes

Written in this round (our own words and markup only; logged in `proposals/store-writes/README.md` with a before-snapshot): Support Artists for Kids gives like Donate ("Make a gift" to its How to give cards, named Online, School Cash Online and Phone); the Artists for Kids button says "Download the guide"; Awards' requirement links are standalone links; staged text for FAQ and Contact with proper paragraphs and Contact's phone and emails as links; Donate's camp links and Stitched's credit links go to pages on this site (the Foundation's was broken); Upcoming events joins the Programs menu. None of it shows on the live site.

Waiting for Michael:
- Edition image alt text in plain letters instead of Unicode italics (21 products). This also improves the live site, so it needs an early go-ahead.
- Real alt text for installation views and edition images: words from the gallery.
- Covers for the 8 documents without one; cropped copies of three white-padded edition photos (at release).
- The DS-80 crumb on ten Artists for Kids subpages (their Eyebrow field), once DS-80 is approved.
- Smith Foundation in the footer's Explore menu, once the gallery agrees.

## For the gallery

`proposals/gallery-questions.md` §8 (14 questions): names and casing, list page titles, collection data, Shop labels, the Shop introduction, product descriptions, programme copy, Foundation labels, residency portraits, the contact heading, two past exhibitions' key images, From the Ground's multi-part works, the team photo.

## Held

- Standalone link arrow following its last word when the label wraps: held (the inline-link fix is built; the inline-block rewrite for standalone links drops vertical centring and the nudge and was tested only on a mock page).
- Installation views and the count rules: only Stitched's 2, 2, 1 at 768 is a clear case; fixing it needs three installation rules and a §5.2 change. Revisit after gallery-uses-grid if Michael wants it.
- One label snippet for both tiles and a <template> for the script tile: a no-visible-change refactor, scheduled after tile-snippets lands; touches search and the finder.
- Frames in search (P-19): a release check that fails if any Frame product is Active and a staff note to create frames Unlisted; waits for the release backlog. Don't filter inside the paginated search loop.
- Menu drawer as a card from 750 px: adds a width-based form against 'prefer removing a variant'; the harm is mild. Revisit if tablet testing shows confusion.
- Facts lists at 16 px everywhere (sec-css-7): would move five templates and write a new rule; the two outliers join the details rhythm instead (section-rhythm).
- A --gs-prog-* token layer: small saving, no visible change; only the §3.3 wording is fixed.
- FAQ questions promoted from H3 to H2: advisory (H42), and both fixes cost something (a hidden H2 repeats the H1; real H2s make all eight a size larger). Revisit with the FAQ content pass; the paragraph split is staged meanwhile.
- List links at 44 px on touch: AA 2.5.8 already passes after the row-target fix, and it would add about 940 px to the Artists page on phones. Recommend not building unless touch complaints appear.
- A visible submit button on Shopify's privacy opt-out form: Enter already submits and the invisible hCaptcha flow is untested. Hold unless the gallery wants it.
- Portfolio card titles shortened to 'Fall 2026' like the switcher: keep the full title (it matches the destination H1 and Home) and accept the wrap at tablet width.
- Whole-dollar prices site-wide: a taste choice, not a fix; only preview.html is aligned to the build's cents.
- Already waiting for Michael and not changed here beyond added evidence: DS-72 (58ch measure), DS-79 full split, DS-81 (rule-colour hover; option B added), DS-70a lesson options.
- Heading accent class (.gs-heading--accent): unused; delete only if Michael agrees, then drop 'accent headings' from DESIGN.md §3 and tokens.css:59.
- Dropped as not worth a change: a shared mailto/tel snippet beyond gs-tel, a shared crumb snippet, letter-weighted gs-fit, linked footer logos, a new year-format rule, a hero-frame snippet, merging .gs-signup into .gs-form, the clay kit duplicate (fixes itself on October 5).

## Flags from the build

- Office hours now read "Monday to Friday, 8 AM to 3 PM" in Theme settings (format only); the gallery still has to say which hours are right (question 6.1).
- DESIGN.md §6.10 now describes the legal line as it renders (below 990 px the long opt-out link takes its own line), which differs from DS-57's aim that no link sits alone.
- A busy button can still grow ("Signing up" is wider than "Sign up"); a one-cell grid would stop it.
- Some attributes use `| t | escape`, which would show an apostrophe or ampersand as an entity; no string has one today except a lesson title in the video's name.
- DS-95 changes nothing visible until Professional development has a hero image or the curatorial tour its own image.
- Theme settings and `templates/index.json` changed (hours format, the What's on heading, the home rows' link settings). Before the review theme is updated, compare its editor JSON as usual.
- The password page can't be shown on this store; its logo rule was checked in code only.

## Verification

- Checks after every batch and after the fixes: Theme Check (132 files, no offences), the linter with `--strict` (0 errors, 0 warnings) and its 15 tests, contrast (85 of 85 pairings), `sync_theme.py --check`, `git diff --check`.
- Regression check: every page captured again at 390, 768 and 1440 and compared frame by frame with the first captures, plus 320, 990 and 1200, by 17 checkers (14 page groups; header, navigation and footer; links, buttons, forms and motion; accessibility at 320 px and 200% zoom). Each reported regression was reproduced by a second agent. 22 were reported and 17 confirmed, none high: 12 fixed in code, 5 in the records.
- Fixed after the check: a Word-pasted product description lost the gap before "PRINT DETAILS"; a keyboard-focused card in a phone rail could sit half off screen (now scrolls into view, keyboard only); the Menu drawer stayed open when Tab moved into an embedded video; "(PDF)" could break inside itself in narrow tile titles, and a long document title widened its tile; the first page link's focus ring was cut off at the screen edge; the exhibition switcher's counts sat above the label's baseline; a focused A to Z name's ring crossed its count; the privacy opt-out field stayed at Shopify's 375 px; empty-state sentences wrapped at a narrower measure than the deck; the pagination landmark shared "Pages" with the search heading (now "Page numbers").
- Checked again after the fixes on the development theme: no "(PDF)" splits and no sideways scroll at 320, 330, 360 and 390 on Learning guides, Learning kits, Sara-Jeanne Bourget and Gordon Smith; the drawer closes when Tab reaches the Gordon and Marion video; the second rail card lands whole (16 to 309 px at 390); the opt-out field is 640 px at 1440 and 358 at 390; the empty search sentence is one line at 1440.
- Not checked: the password page (the store isn't password protected), a real form post, WebKit beyond the drawer and arrows, real touch devices.
