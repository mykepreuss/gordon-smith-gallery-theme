# Gordon Smith Gallery website improvement project

## Purpose and authority

Improve the existing Shopify storefront's navigation, visual consistency, image treatment, exhibition and Shop pathways, site-wide access points, and staff editing workflow. The [developer notes](reference/Gordon%20Smith%20Gallery%20Website%20Notes%20for%20Developer.docx.md) are the authoritative requirements. The [brand guide](reference/GordonSmith-BrandGuide_sm.pdf) and [logo guide](reference/GS-Logo-Guide.pdf) constrain visual implementation. The numbered workflow supplied with the request is the execution framework; no separate implementation-plan file was present at discovery.

**Approach, decided 2026-09-25 (P-13):** build a new theme for the same store, as if starting from scratch today, instead of modifying the current Colorblock theme. The developer notes, the approved decisions (`DECISIONS.md`) and `design-system/` drive the design. The current theme is a reference for content and placement only: `proposals/content-migration.md` lists everything it holds and where each item goes. The new theme starts from Shopify's Skeleton theme (P-14). It is still Shopify, with the same store, products, collections and pages. The old theme stayed untouched until the release on 2026-09-29, and it remains the rollback.

Work is GitHub-first. Theme code, the requirements register, proposed Shopify resource changes, decisions, and test evidence must be reviewable in a private GitHub pull request before production release. An unpublished Shopify theme is needed for realistic storefront and staff-editor review, but must never be treated as the live theme. Publishing and applying changes to live-referenced store resources require explicit release approval.

Keep four change surfaces distinct: **Git owns theme source and project records; the unpublished theme owns preview-specific code and settings; Shopify Admin resources are shared across themes; installed apps have their own configuration and theme-specific placements.** Theme preview is not a copy of the store. Use Shopify CLI as the default path for writing theme files and the connector or Admin only for verified, approved store-resource operations. Shopify's theme-file GraphQL mutation requires an additional exemption beyond `write_themes`, so the connector's scope alone does not establish a usable theme deployment path. [Shopify theme-file mutation](https://shopify.dev/docs/api/admin-graphql/2026-01/mutations/themeFilesUpsert).

## Where the project stands (2026-09-29)

- **Released.** The new theme went live on 2026-09-29 at 23:08 UTC (4:08 PM Pacific), with Michael's approval. The record: `verification/2026-09-29-release-gate.md` and `proposals/store-writes/README.md`, "2026-09-29: the release". A second release followed the same evening, at 00:51 UTC on the 30th (5:51 PM Pacific), and a third at 01:19 UTC: "The second release, 2026-09-29" and "The third release" below. The fourth went live on 2026-10-01 at 20:15 UTC, the fifth at 21:33 UTC and the sixth at 22:54 UTC: "The fourth release", "The fifth release" and "The sixth release" below.
- **Live theme:** `184857461033` "Gordon Smith Gallery", published from `main` at 0f91be7 at the sixth release. It was the review theme until then. Only small fixes go to it (`AGENTS.md`).
- **Rollback theme:** `184856445225` "Gordon Smith Gallery (rollback, fifth release)", the live theme from the fifth release to the sixth. Unpublished and unchanged. Nothing is pushed to it.
- **Older themes:** none. Deleted 2026-10-01 at Michael's request (P-69): the three earlier rollbacks, Colorblock, the five pre-project drafts and five old development themes. The fourth release's rollback, `184824725801`, followed at the sixth release. Each rollback matched a commit in Git when it was deleted (first release dee1885, second c48901c, third 1f7d899, fourth 220213c) and Colorblock matched `baseline/theme/` file for file, so any of them can be pushed again as a new unpublished theme from that commit. The rollback steps for the first four releases below name themes that are gone: to use one, push its commit as a new unpublished theme and publish that.
- **Review theme:** `184858575145` "Review theme (do not publish)", made from `main` at 6204cb1 at the sixth release. It follows `main`.
  - Preview: https://ed35ee-ea.myshopify.com?preview_theme_id=184858575145
  - Editor: https://ed35ee-ea.myshopify.com/admin/themes/184858575145/editor
- **Built:** the new theme on Shopify's Skeleton theme, every template, the header, footer and newsletter band (`theme/`, `design-system/DESIGN.md` 0.6.83).
- **Content:** 45 published pages, 32 exhibitions, 14 events, 27 lessons, and the Permanent Collection's 1,174 works and 171 artists, with the card groups, product labels and menus (`proposals/store-writes/README.md`). The Artists for Kids site and the Smith Foundation's old site are on this one. No text is staged any more: each page's text is its own (DS-39).
- **Decisions:** every decision that is built is decided (`DECISIONS.md`). DS-70a is Proposed and not built.
- **Phase: improving the live site.** Changes follow "How we iterate" below. A merged change reaches the live site only at a release Michael approves. What is left from the release: "Open after the release".

## Discovery snapshot and preflight

This section is the record of 2026-09-23, before the build. The live theme it names is the old theme since the release (`AGENTS.md`, "Store target").

Read-only checks on 2026-09-23 found:

- The connected store is **Artists for Kids & The Gordon Smith Gallery**, with Shopify domain `ed35ee-ea.myshopify.com` and public domain `gordonsmithgallery.com`.
- The live theme is **Colorblock: NEW WEBSITE**, ID `183162372393`. Five other themes are unpublished. This folder contains reference materials, but no Git repository or local theme source. Shopify CLI 4.8.2 and GitHub CLI are installed; `mykepreuss` is the active GitHub account, and no matching repository was found under that account.
- The live header uses menu `new-website-menu-1`. Its parent items with children render as dropdown controls, so their configured page links are not available from the parent labels. Several submenu entries repeat the parent. The Exhibitions menu omits an existing Upcoming Exhibitions page. The 2025 Fall Portfolio item uses an absolute myshopify URL although the collection exists in this store.
- The active theme uses Assistant for headings and body copy. Its header logo width is set to 250 pixels. The custom rotating banner uses fixed desktop/mobile heights and `object-fit: cover` without a focal-point setting.
- A footer newsletter section exists but is disabled. Mailchimp is installed. Footer social display is enabled, but the theme's social URLs are empty. The live Shop template has one enabled collection list plus several disabled older sections; public page crawls may lag current theme edits.
- The Shopify connector exposes read and write Admin tools and the relevant read/write scopes. Its app permission uses the account default, **Allow low-risk actions**. Tool capability is not approval to change this store.

This snapshot is evidence for planning, not the implementation baseline. Before any write, recheck the store domain, live theme ID, relevant resource timestamps, CLI account and target, and current storefront. Inventory the Shopify connector's actual tools, permission setting, and relevant API scopes again rather than assuming this snapshot still applies. Capture desktop, tablet, and mobile screenshots and interaction recordings or notes for the reported issues. Inventory all relevant theme files, templates, page assignments, menu trees, installed app embeds, Mailchimp configuration, pages, collections, and content resources. Record what was observed, what could not be reproduced, and any conflicting edits made since this snapshot. Do not edit the live theme or existing live-store resources during discovery.

Audit Mailchimp before selecting a signup implementation. Determine whether the storefront uses a theme app embed, app block, legacy ScriptTag, hard-coded script, native form, or external destination; check the active audience and consent behavior. Shopify says new storefront ScriptTags cannot be created or updated from **2026-10-01**, and existing ones stop being injected on **2027-03-01**. Do not build a new signup around ScriptTags. App embeds are enabled per theme and must be checked on the review theme and again after publication. [Shopify ScriptTag timeline](https://shopify.dev/docs/apps/build/online-store/script-tag-deprecation/storefront).

## Requirements register

Create a tracked register in GitHub with one row per item below. Each row must retain the source wording, owner, change surface (`theme`, `store`, `editorial`, or `mixed`), dependency, status, baseline evidence, changed files/resources, and test evidence. All items start **Not started**. A finding from read-only discovery is not completion evidence.

| ID | Requirement from developer notes | Primary acceptance evidence |
| --- | --- | --- |
| NAV-01 | Make main navigation and dropdowns consistent and reliably triggerable. | Mouse, touch, and keyboard tests on desktop and mobile. |
| NAV-02 | Remove confusing parent-item duplication and inconsistent behavior inside dropdowns. | Approved menu map and inspected rendered menus. |
| NAV-03 | Apply consistent behavior to sections with children and direct-link sections. | One section button per section with children, main page first inside its dropdown (DS-11); direct pages as single links; works without JavaScript; expanded state, focus, Enter/Space, and Escape tests. |
| NAV-04 | Make Artists for Kids external-site paths intentional and integrated. | Clear external destination cue and verified target URLs. |
| TYPE-01 | Apply brand typography across navigation, headings, subheadings, body, and links. | Brand-guide mapping and representative page screenshots. |
| TYPE-02 | Set font scale, line spacing, margins, padding, tracking, and whitespace globally. | Shared tokens/rules and cross-template comparisons. |
| TYPE-03 | Remove unintended generic/default typography. | Computed-font checks across page types. |
| TYPE-04 | Improve the header's Gordon Smith Gallery identity scale relative to navigation. | Desktop/mobile header review against approved design. |
| TYPE-05 | Make links and CTAs consistently designed, beyond default underline treatment. | Normal, hover, focus, visited, and disabled state review. |
| IMG-01 | Support large-format hero imagery consistently across relevant templates. | Representative page templates using the shared hero pattern. |
| IMG-02 | Prevent responsive crops from losing the important part of images. | Desktop/tablet/mobile crop screenshots for selected artwork. |
| IMG-03 | Give editors focal-point/crop control where Shopify permits. | Staff editor sets a focal point, preview respects it, and other uses of the same image remain acceptable. |
| IMG-04 | Keep hero/slideshow placement and treatment consistent across page types. | Cross-template comparison and documented exceptions. |
| EXH-01 | Remove duplicated Exhibitions hierarchy and repeated parent/child entries. | Approved menu map and rendered navigation. |
| EXH-02 | Shorten paths among current, upcoming, and past exhibitions where useful. | Click-path tests from header and exhibition pages. |
| EXH-03 | Preserve the useful Past Exhibitions presentation and archive. | Before/after visual comparison and existing links checked. |
| EXH-04 | Leave final labels and editorial copy to gallery staff. | Approved labels recorded; no unapproved copy rewrite. |
| SHOP-01 | Reduce overload and repetition on the Limited Editions landing page. | Before/after page hierarchy review. |
| SHOP-02 | Use the portfolio/Collections navigation without unnecessary repeated listings lower on the page. | One clear portfolio pathway and no redundant enabled sections. |
| SHOP-03 | Preserve the clarity of individual portfolio pages. | Representative collection/portfolio comparison. |
| SHOP-04 | Align Shop hero/slideshow hierarchy with the broader site system. | Desktop/mobile visual review of Shop and peer pages. |
| ACCESS-01 | Add or restore prominent, reusable site-wide newsletter/Mailchimp signup access. | Integration mechanism audited; review theme activated; approved test reaches the intended audience with correct consent; post-release recheck. |
| ACCESS-02 | Make Contact access persistent without requiring a Contact-page search. | Header/footer pathway tests across page types. |
| ACCESS-03 | Add appropriate site-wide social links/handles. | Footer/mobile display and target verification. |
| ACCESS-04 | Use gallery-supplied wording, addresses, signup destination, and social URLs. | Input log and approval of exact production values. |
| REUSE-01 | Build reusable components or templates that reduce staff design decisions. | Staff creates/updates a representative page using documented controls. |
| REUSE-02 | Make common typography, spacing, image proportions, buttons, cards, and galleries inherit shared styling. | Cross-template visual checks after a shared style change. |
| REUSE-03 | Keep the site coherent as different staff members add and update content. | Staff editing walkthrough with two resources sharing a template: content stays independent while styling is shared. |
| REUSE-04 | Flag theme/platform limits requiring custom code or a different structure. | Limitation log with evidence and recommended path. |

## Approved direction

Structural choices, updated 2026-09-25: a section with pages under it is a single button that opens its dropdown, and the section's main page is the first link inside it (DS-11); for Exhibitions that first link is **On Now**. This replaces the earlier choice of a linked parent label with a separate dropdown caret. On 2026-09-25 the gallery approved the menu map and labels, the page types, the contact and newsletter placement (P-15) and the content model (DS-14 to DS-16); Exhibitions is the first menu item (P-09). Gallery staff still supply editorial content. On 2026-09-28 the menu was set out by what visitors come to do (P-50 to P-57, `proposals/navigation-review.md`): Exhibitions and Shop are plain links, and Programs, Support and About are sections. Where the points below say otherwise, `proposals/store-changes.md` §1 holds the menu as it is.

The design specification is `design-system/DESIGN.md`, with tokens, components, scripts and checks in `design-system/`. The theme's `gs-` snippets live in `theme/snippets/`; `design-system/scripts/sync_theme.py` copies the shared CSS, JavaScript and logos into the theme and checks that the copies match. Design decisions (DS-01 onwards) and project decisions (P-01 onwards) are recorded in `DECISIONS.md`. The menu map (`proposals/store-changes.md` §1) follows this model:

- A section with pages under it is one button (a native `<details>`/`<summary>` disclosure) that opens its dropdown and never navigates; its main page is the first dropdown link, with its own label. Direct pages remain single links. No dropdown item repeats its section's label. Apply the same model to desktop and mobile, with visible focus, exposed expanded state, Enter/Space opening, and Escape closing with focus restored. Navigation must keep working without JavaScript (DS-19). Use ordinary site navigation semantics rather than ARIA application-menu roles. [Shopify accessibility guidance](https://shopify.dev/docs/storefronts/themes/best-practices/accessibility).
- Offer On Now, Upcoming, and Past directly. There is no Exhibitions overview page: its address redirects to On Now (P-20, 2026-09-26). Exhibitions are structured entries at their own addresses, with redirects from the old exhibition pages (P-10). Both since the release. Past Exhibitions lists past exhibitions automatically from those entries and keeps each current card's image, dates and title (DS-24, DS-25).
- Make Shop lead to the Limited Editions landing page, with a short portfolio hierarchy. Correct internal portfolio targets. Keep the landing page to one introduction, one portfolio navigation area, and a restrained featured image/hero; preserve individual portfolio layouts.
- Put a reusable newsletter band above the footer, Contact in a persistent header/utility and footer location, and social links in the footer. The band uses Shopify's own newsletter form (a `customer` form that tags the customer `newsletter` and records email marketing consent), and the installed Mailchimp for Shopify app syncs subscribed customers to the gallery's audience (option 1 in `baseline/mailchimp-audit.md`, P-18). It needs no ScriptTag and no new app, and it works in any theme. Still to do, since it wasn't done before the release: verify in the app that customer sync is on, that consent and the `newsletter` tag reach the right audience, and how double opt-in behaves; then run the test signup in the verification rules. The band is live without consent wording, which the gallery has yet to supply (Michael, 2026-09-29: release as it is). If the sync can't be verified, fall back to a prominent link to a gallery-supplied Mailchimp signup page and record the limitation.

Use **Mulish** as the free Google Fonts option already identified in the brand guide. The guide specifies heavy uppercase headings/subheadings, bold introduction text, regular body text, and light captions. Bundle Mulish's licensed web font files with the new theme rather than offering a font picker, since fonts are not a staff choice. Do not rely on an undocumented fallback to Assistant. Set scale, weights, line heights, and any specified letter spacing through shared rules; leave font kerning at its normal browser behavior unless the guide requires an override. Preserve approved logo assets and brand colors, and evaluate header identity size in context. [Mulish license](https://github.com/googlefonts/mulish/blob/main/OFL.txt); [Shopify font guidance](https://shopify.dev/docs/storefronts/themes/architecture/settings/fonts).

Build shared Liquid/CSS rules and reusable hero, card, gallery, link, and CTA treatments. Keep page-specific words, images, captions, and links in page content or page-specific fields rather than hard-coding them into a shared template's configuration. Use Shopify image focal points where supported, preferably through `image_tag`; use a separate mobile image only where a single crop cannot work. Preserve existing content (page bodies, images, captions, links); the templates that hold it are replaced, and content they hold moves as `proposals/content-migration.md` sets out. [Shopify focal-point guidance](https://shopify.dev/docs/storefronts/themes/architecture/settings/input-settings).

Build new header and footer section groups in the new theme. A JSON template's section configuration is shared by every resource assigned that template, so test content isolation with two pages before calling the editor model complete. If a new alternate template exists only in the unpublished theme, preview it in that theme or with the supported `?view=` route; the normal Admin assignment menu draws from the live theme, and changing an existing resource's template assignment is a store-level release action. [Shopify template behavior](https://help.shopify.com/en/manual/online-store/themes/theme-structure/templates), [alternate-template preview](https://shopify.dev/docs/storefronts/themes/architecture/templates/alternate-templates).

The menu map, page hierarchy, component/editor model, shared access placement and the first store-level field definitions were approved on 2026-09-25. The additions found by the content inventory (card groups, events and a few smaller fields: content model parts 4 to 6, P-16) were approved the same day (P-16). The design decisions made during the build (DS-28 to DS-38) and the choices made while moving content into fields and entries (`proposals/store-writes/README.md`) were approved by Michael on 2026-09-25.

Michael is the approver for structural and design decisions and for content-moving choices (P-17). The gallery still supplies wording and values: labels, editorial copy, contact details and consent text (EXH-04, ACCESS-04). Record each new decision in `DECISIONS.md` as Proposed when it is built, and get Michael's approval before a release. Nothing still marked Proposed ships.

## GitHub-first delivery workflow

1. **Create the source of truth.** Initialize Git in this folder. Pull the exact verified live theme into `theme/` without changing Shopify, and commit it as the untouched baseline with the reference materials, requirement register, baseline evidence index, and a manifest of store resources. Create a private `mykepreuss/gordon-smith-gallery-theme` repository unless the gallery supplies an existing repository or organization destination. Keep credentials and tokens out of Git. Record the source theme ID, pull time, CLI version, and baseline Theme Check output. Add concise `PROJECT.md` for milestone/requirement status, `DECISIONS.md` for approvals, and repository `AGENTS.md` for store-target and release rules without overriding existing user instructions. *Done 2026-09-25: baseline commit 27ef593.*
2. **Build the new theme after the structural approval.** Work on a feature branch. Move the untouched baseline to `baseline/theme/` so that `theme/` holds the new theme; the baseline commit stays unchanged in history. Start from Shopify's Skeleton theme, add the design system's tokens, components and snippets, then build the approved template set (`design-system/DESIGN.md` §7), header, footer, newsletter band and commerce templates (product, collection, cart, search and system pages). The store uses Shopify's new customer accounts, so the theme needs no account templates. Prepare the content migration as scripts or instructions in Git. Creating definitions, entries and field values is a store write, even when it's invisible under the live theme: follow "Store writes" below. Separate theme-only changes from proposed store-level changes in both commits and the register. Theme-only changes include Liquid, CSS, JavaScript, JSON templates, section groups, and settings for the future unpublished theme. Store-level changes include menus, page content/fields and template assignments, products, collections, Files and shared image metadata, redirects, and Mailchimp configuration. A preview theme does not sandbox any of these Admin resources. Keep proposed store-level changes as reviewable manifests or instructions in Git until the relevant preview or release gate. Use CLI for theme file writes and only a verified connector/Admin capability for approved Admin writes. [Shopify store-resource behavior](https://help.shopify.com/en/manual/online-store/themes/customizing-themes/theme-editor/add-and-edit-store-resources). *Built 2026-09-25 on `build-new-theme`: the template set, then design passes with real content for Home, Exhibitions, the programme pages and Shop. All content migrated the same day, with the page text that changes at release staged (DS-39, `proposals/store-writes/README.md`). What's left is under "Iteration backlog" and "Open after the release".*
3. **Open a reviewable pull request before Shopify preview writes.** Include the code diff, requirement statuses, proposed menu map and store resource changes, missing gallery inputs, theme check output, and the content parity check against `proposals/content-migration.md`. Do not auto-deploy or connect the repository to production. *Done: [PR #4](https://github.com/mykepreuss/gordon-smith-gallery-theme/pull/4) (the build) merged 2026-09-25; [PR #6](https://github.com/mykepreuss/gordon-smith-gallery-theme/pull/6) (page passes, plan review, content migration) and [PR #5](https://github.com/mykepreuss/gordon-smith-gallery-theme/pull/5) (the design-system preview) merged 2026-09-26.* From here, make changes in smaller pull requests, one per page or topic, each passing the checks in "Verification and completion rules". Push the review theme only from `main` or a reviewed branch, and record the commit in the PR.
4. **Create the designated unpublished review theme.** Reverify the store and live theme ID, upload the new theme as a clearly named unpublished theme (`shopify theme push --unpublished`), and record its new ID and `UNPUBLISHED` role in the PR, `AGENTS.md` and `PROJECT.md`. Push only to that ID using CLI `--theme <verified ID>` and `--strict`; never use `--allow-live` or `theme push --publish`. A separate menu may be created and referenced only by this theme for realistic navigation testing. Prefer an existing resource or theme-editor preview for staff testing; a temporary page is still a store-level resource, so create one only if necessary and explicitly approved, and do not assume an unpublished page has a visitor preview URL. During review, change nothing the live theme shows without Michael's go-ahead: see "Store writes". [Theme push](https://shopify.dev/docs/api/shopify-cli/theme/theme-push). *Done 2026-09-26: review theme `184767250729`, "New theme for review (do not publish)", from `main` at 594eb01. Preview: https://ed35ee-ea.myshopify.com?preview_theme_id=184767250729. Before each push, bring any theme editor changes into Git first (`AGENTS.md`). That theme was published at the first release, 2026-09-29, and is the rollback since the second. The next review theme, `184823611689`, made the same day from `main` at f6bf867, was published at the second release and is the live theme. The review theme since then: `184824398121`, "Review theme (do not publish)", from `main` at 8bcfaa7. Preview: https://ed35ee-ea.myshopify.com?preview_theme_id=184824398121.*
5. **Keep the PR and preview synchronized.** Every preview change must correspond to a reviewed Git commit or a logged preview-only store resource. Record the exact theme ID, Git commit, changed files/resources, and preview URL in the PR. Recheck for concurrent edits to the live theme before release and reconcile drift deliberately. *Ongoing: see "How we iterate".*
6. **Release with approval.** Give Michael the release gate package, publish the review theme and make the approved store changes only on his explicit approval, then check the live site and record the result ("Release gate and rollback"). *First done 2026-09-29: `verification/2026-09-29-release-gate.md`.*

GitHub can hold the code and proposed definitions for menus and other Shopify resources, but cannot itself host their working Admin state. The unpublished theme and separate preview resources are limited Shopify writes for review; they are not production changes. Record any preview-only Admin resource and its cleanup path separately from the theme. Use the theme ID and Git commit as durable review identifiers because shareable preview URLs may expire.

**Development theme and review theme.** `shopify theme dev` serves the branch you're working on as a development theme. It's hidden, tied to the CLI session and temporary: logging the CLI out removes it, and a new session can make one with a different ID. Use it for working checks only. The review theme (`184824398121`) follows `main` and is what Michael and gallery staff review and edit. All evidence for the verification rules and the release gate is captured on the review theme.

Two things learned on 2026-09-29. When another session's server holds port 9292, run a second one on its own port and its own development theme (`--port 9293 --theme <a development theme's ID>`), so neither overwrites the other's files. And don't run the full links check through `theme dev`: the CLI's local server fails under it (401, then 502). Run it with `--theme <id>` against the store, or on the live site.

### How we iterate

The loop for every change:

1. **Branch** from an up-to-date `main`, one page or topic per branch.
2. **Work** against the development theme: `shopify theme dev --store ed35ee-ea.myshopify.com --path theme` serves the branch at http://127.0.0.1:9292. Check design changes at 1440, 768 and 390.
3. **Design system first:**
   - Values go in `design-system/tokens.css` and shared styles in `components.css`; then run `sync_theme.py theme/`.
   - A new component or rule goes in `DESIGN.md` and `preview.html`.
   - Bump the version and add a changelog line.
4. **Decisions:** a new design or structural choice is recorded as Proposed in `DECISIONS.md` and `DESIGN.md` §12. Michael approves it (P-17); nothing Proposed ships.
5. **Store writes:** every one shows on the live site at once. Each needs Michael's go-ahead, a before-snapshot and an undo step, and is logged in `proposals/store-writes/README.md` ("Store writes" below).
6. **Records in the same pull request:**
   - the affected `REQUIREMENTS.md` rows;
   - anything that must happen at the next release, in `proposals/store-changes.md` and "Open after the release";
   - `PROJECT.md` if a status or open question changes.
7. **Checks:** the ones under "Verification and completion rules" that a pull request needs: Theme Check, the linter and its tests, `check_contrast.py`, `sync_theme.py --check` and `git diff --check`.
8. **Pull request;** Michael reviews and merges.
9. **Review theme:** after the merge, update it from `main`.
   - Pull its `config/settings_data.json` and `templates/*.json` and compare them with Git. Bring any theme editor changes into Git first (`AGENTS.md`).
   - Push with `--strict`, and record the commit in `PROJECT.md`, milestone 4.
   - A reviewed branch may go to the review theme before it merges, when Michael wants to see it there. The review theme is then ahead of `main` until the merge, and the pull request says so.
10. **Release:** a merged change is on the live site only after a release Michael approves ("Release gate and rollback"). Until then the review theme is ahead of the live theme, and `PROJECT.md` says by what.

### Store writes

Since the release, the live theme reads the store's fields, entries, menus and pages, so a store write shows to visitors the moment it is made. There is no staging field any more.

Every store write needs:

- Michael's go-ahead for that write.
- A before-snapshot, and an undo step written down before the write.
- A recheck first of the store's domain, the live theme's ID and role, and the account (`AGENTS.md`).
- A read back afterwards, and a look at the live pages it touches.
- An entry in `proposals/store-writes/README.md`.

A write that needs theme code the live site doesn't have yet waits for the release that carries the code, or is made at it. A new definition, or a value in a field the live theme doesn't read, can be written ahead: check the live theme's code first, which is the commit it was published from (`PROJECT.md`).

The release's writes went through the Shopify CLI from files (`shopify store execute`, `proposals/store-writes/release_run.py`), at Michael's choice, so each value reached the store as the script printed it. Every write before the release went through the Shopify connector. Which one a later write uses is settled when Michael gives the go-ahead.

**Before the release (the record).** From 2026-09-25 to the release, only what the old theme couldn't show was written: new definitions, new entries whose pages answered 404 under it, and field values it didn't read. Page text, titles, templates, menus, redirects and hidden pages waited for the release. Page text that was to change was staged in `custom.release_body` (DS-39), which the release moved into the pages and deleted.

### Iteration backlog

Open while iterating. Add what each review finds; take items off when they merge.

| Item | Owner | Notes |
| --- | --- | --- |
| The links between pages, reviewed 2026-09-29 (`proposals/internal-linking-review.md`): every page read, 1,623 addresses, and ten changes built and decided by Michael the same day (DS-178 to DS-187, "DS-178 to DS-187 approved, merge #118"). The crumbs on 13 Artists for Kids pages were written the same day (option A, P-64; Professional Development has none, so the Programming rows stay in place, DS-146). Home's row from the collection is built and decided (option B, DS-188, "DS-188 approved, merge #122"). Left: options C to F, which have no decision; the gallery's answers (`gallery-questions.md` §12, 1.9) | Michael, gallery, then Agent | Exhibitions and artists link both ways, each past exhibition links to its neighbours in time, an edition links to its work and a work to its lessons, pages nobody links to are not listed. New check: `check_links.py` |
| Links between pages (DS-175, decided by Michael 2026-09-28, as built). Left: the gallery looks over the two lists of names; choices 2 to 4 in the proposal stay as built unless Michael says otherwise | Gallery | `proposals/linked-names.md`. Asked for on The Smith Foundation page; built for every page |
| Google's Rich Results Test, run 2026-09-28 (DS-173, decided): run it again on the review theme after any change to the structured data | Agent | `proposals/structured-data-review.md`, "Google's Rich Results Test". Every kind of page passes. validator.schema.org is not run: the check reads schema.org's own vocabulary instead |
| Facts for the structured data, found 2026-09-28: steps A to D are built (DS-170, DS-171, DS-174). The gallery confirmed them on 2026-10-01 (`proposals/gallery-answers/`): the corrections to artists' names and dates are made (F), and 101 artists carry their addresses elsewhere in the store (E). The theme reads those addresses, and gives the charity numbers, since the fourth release (2026-10-01). **Done** | Agent | `proposals/structured-data-facts.md`; `proposals/store-writes/aeo/artist-identifiers.json` |
| Structured data as one graph (DS-163 to DS-165, decided by Michael 2026-09-28, as built). Left: the facts listed under "What would make it better still". Pat and Rosemarie Keough stay one artist entry (the gallery, 2026-10-01) | Michael, Gallery, then Agent | `proposals/structured-data-review.md`, "The graph". Built on #87's branch |
| For search and answer engines (`proposals/aeo-geo-review.md`): step 1 decided 2026-09-28 (DS-154 to DS-157); lessons, lists, pages, articles and the editions' own data added and decided the same day (DS-158, DS-159); steps 2 to 4 built 2026-09-28 (DS-160 to DS-162, Proposed; P-61, the product titles, done). The gallery answered on 2026-10-01 (`proposals/gallery-answers/`): the descriptions, four biographies, the image descriptions and the social accounts are done; the FAQ's visiting questions went live at the fourth release, the same day. Also built 2026-09-28: the gallery's own `/llms.txt` and `check_answers.py` (DS-166, DS-167). Technical follow-up built and decided 2026-09-28 (DS-168, DS-169). Pages for events, decided and built 2026-09-29 (DS-176, `proposals/event-pages.md`), are on since the release. The descriptions moved to the pages' search engine listings on 2026-10-01 (`store-changes.md` §8d) | Agent, then a release | The alt text of 45 images is in Files (P-62, 2026-09-29); the gallery approved 34 and changed 11 (2026-10-01) |
| Set the seven hero focal points in the admin (Content > Files), then check them on the review theme at phone width | Michael, then Agent | `proposals/hero-focal-points.md`, each point tried on the preview first (2026-09-26). Shopify's API can't set focal points. IMG-02, IMG-03 |
| The Smith Foundation's old website: built 2026-09-28 (P-41 to P-49, DS-138). Supporters went live at the release with Donate's link to it (Michael, 2026-09-29: "Supporters confirmed, keep in"). Left: the gallery's other answers (`gallery-questions.md` §8) | Gallery, then Agent | `proposals/smith-foundation-site.md`, "Build notes" and "Still open"; log in `proposals/store-writes/README.md`. The export and the media download are outside Git, in `~/Downloads` on Michael's Mac |
| Send the gallery its questions: values, exhibitions, content checks, brand | Michael | `proposals/gallery-questions.md` collects all of them in one place (2026-09-26) |
| The Permanent Collection: the gallery checks the review sheets and names, and chooses the featured works | Gallery, then Agent | Built 2026-09-27 (P-26, P-27, P-28, DS-62, DS-63): 1,174 works, 171 artists, 26 groupings, 1,420 images and 118 linked documents in the store (the 39 PDFs over 20 MB as smaller copies, 2026-09-27); the Artists page is the A to Z of every artist, each with a page on the site; the Permanent Collection page searches and browses the collection; Collection in the menu. `proposals/permanent-collection.md` ("Still open"), `proposals/gallery-questions.md` §5. Live since the release |
| Artists for Kids: the gallery's and the team's answers (text corrections, the missing PDFs, names, "AFK" in body text, the labels), DS-69 to DS-71 decided by Michael 2026-09-29 | Gallery, team, Michael | Built 2026-09-27 (P-30 to P-40): `proposals/artists-for-kids-integration.md`, `proposals/gallery-questions.md` §6. The 18 pages, lessons, cards and events are live since the release, with their text, and open to search engines (P-35). The team still has to cut the old site back to registration (P-30) |
| Class and camp listings (P-68, decided by Michael 2026-10-01): built the same day, the class list DS-198 decided, merged as #142, live at the fifth release the same day with After School Art's 6 fall classes. Left: the team's six questions and a name for who keeps the classes; day camps and Paradise Valley as entries when their registration opens | Michael, then Agent; Artists for Kids team | `proposals/class-listings.md`, with the team's instructions; `proposals/store-writes/classes.py` |

### Open after the release

**Done at the release, 2026-09-29** (`verification/2026-09-29-release-gate.md`): the release gate package; fresh exports and dry runs; event pages on (DS-176); the theme published; 38 template names; 10 old pages hidden, with 10 redirects and one older redirect sent straight on; 32 staged texts moved into their pages, Supporters among them; 23 new pages opened to search engines, the Artists for Kids and Smith Foundation pages among them; 16 frames Unlisted. Checked on the live site: links, answers, structured data, every published page, the old addresses, a framed print in the cart.

**Done after it, the same day:** the list of unlinked addresses in `links.json` emptied and the links check run on the live site (1,636 pages, 0 errors); the pre-release bridges out of the theme (#123); a new review theme; the live theme renamed. An event was seen to drop off Upcoming after it ended.

**Done at the second release, the same evening:** #123, the favicon (#127) and the artwork mat in Safari (#128) live; a new review theme; the two newest themes renamed ("The second release, 2026-09-29").

| Item | Owner | Notes |
| --- | --- | --- |
| The redirect file on smithfoundation.co's server, and GoDaddy's forwarding off (P-63) | Michael | `proposals/foundation-redirects/README.md`, "On release day". The new pages it points to are live now |
| The Artists for Kids team cuts the old site back to registration and gets the list of old and new addresses (P-30) | Michael, Artists for Kids team | `proposals/artists-for-kids-integration.md`, "At release" and "Where each page goes" |
| The print description clean-up (`release.py products`). **Done 2026-10-01** on Michael's yes in place of the gallery's (P-71), with the Shop labels | Agent | The before-and-after list: `proposals/store-writes/dry-runs/2026-09-29/products.md`. The titles are done (P-61). `proposals/store-changes.md` §7 |
| The descriptions: approved by the gallery and moved to the pages' search engine listings on 2026-10-01; the last staged one and the field went at the fourth release, the same day, with the FAQ's visiting questions. **Done** | Agent | `proposals/store-changes.md` §8d and §9c |
| Newsletter consent wording. **Done 2026-10-01:** set by Michael (P-71); the gallery can change it in the theme editor | Michael | ACCESS-01, ACCESS-04 |
| Mailchimp app settings: customer sync, audience, consent mapping, double opt-in; the app's permission update; its app embed for site tracking after 2027-03-01 | Gallery or Michael | ACCESS-01; needs app access. `baseline/mailchimp-audit.md`, "Open from this check" |
| The staff editing test and the newsletter test | Gallery staff, Mailchimp access | Staff use the review theme's editor. The test includes adding a work and an artist to the Permanent Collection (`proposals/permanent-collection.md`, "Who edits where"). An entry or a field a staff member changes is live at once, so the test uses entries made for it, with Michael's go-ahead |
| The date check: an exhibition changing status at midnight Pacific | Agent | The next real change is *Collect, Assemble, Gather* closing on February 20, 2027. Sooner needs a test entry with Michael's go-ahead, which would show on the live site while it exists |
| Answer engines: ask the 32 questions of `answers.json` by hand in the main answer engines for a baseline, and again 30 days later (hours, address, admission, the current exhibition, the four names kept apart); bring the map and business listings outside the site in step with the site's hours | Agent, Michael | `proposals/aeo-geo-review.md`, "Built from the AEO frameworks". `check_answers.py` passes on the live site (32 answered, no known gap, since the gallery's answers of 2026-10-01) |
| Search and answer engines, outside the site (`proposals/aeo-geo-review.md`, "Technical follow-up"): Search Console and Bing Webmaster Tools; the map listings' hours and name; a Wikidata entry (ready for Michael to submit, `aeo/wikidata-gallery.md`); Merchant Center; Google's Rich Results Test on one live page of each kind; referrals from AI assistants in analytics | Michael, gallery, the school district for its domain | Account and listing tasks. None changes the theme |
| Tidy the store. **Done 2026-10-01:** themes (P-69: 14 deleted, 4 kept), then the ten pages hidden at the release and the three old menus (P-70), each saved whole in Git first. Left: three older hidden pages that predate the project (2025 Spring Portfolio, Public Programs, Exhibition Tours), for Michael to decide | Michael decides, then Agent | `proposals/store-writes/README.md`, "2026-10-01: the old themes deleted" and "the old pages and menus deleted" |

## Verification and completion rules

Run Shopify Theme Check without auto-correction and validate all changed JSON templates. Capture its config/version. The new theme must have no Theme Check errors and no design-system linter errors (`design-system/scripts/lint_theme.py`); explain any remaining warning in the PR. Also run the linter's tests, `check_contrast.py` and `sync_theme.py theme/ --check` (all in `design-system/scripts/`). Run `audit_fonts.py` against the review theme: no text may render in a fallback font except the land acknowledgement characters in L-06. Run `git diff --check`, then require CLI `theme push --strict` to succeed against the verified unpublished ID. Theme Check does not prove browser behavior. After any change to a page's template, in the theme or in the store, run `check_links.py` where the change shows: it is the check that found the release's one fault. [Shopify Theme Check](https://shopify.dev/docs/storefronts/themes/tools/theme-check/commands), [strict push](https://shopify.dev/docs/api/shopify-cli/theme/theme-push).

Test at approximately 1440, 768, and 390 pixel viewport widths, plus a real or emulated touch interaction and widths around actual breakpoints. Exercise mouse, touch, Tab, Enter/Space, Escape, focus states, and direct page links. Inspect Home, About, Artists for Kids, Programs, Smith Foundation, On Now, Upcoming, Past Exhibitions, an individual exhibition, Shop, a portfolio collection, a product, and Contact. Compare image focal points, responsive crops, typography, link states, and shared component spacing. Any retained autoplay slideshow needs accessible pause and next/previous controls. Verify all changed internal and external URLs, relevant console/network errors, and a representative product/cart path without placing an order. Check that every item in `proposals/content-migration.md` is present in the new theme or was deliberately dropped.

Test the date-driven behavior, which uses the store's time zone (America/Los_Angeles). An exhibition moves between upcoming, on now and past at midnight Pacific on its start and end dates, on the home page and every list. An event drops off once it has ended. The opening reception stops showing once it has ended. A draft entry never shows. Check on real date changes where they fall during review, or with a test entry made with Michael's go-ahead and deleted afterwards.

Have a gallery staff member or a representative editor update preview theme settings and, only where safely authorized, representative resource content using the documented workflow. Compare two resources on the same template to confirm that page-specific content does not leak while shared styling remains coherent. Staff will mostly edit entries and fields, so the test also covers them: create and edit an exhibition entry and an event, change a card in a card group, fill a page's hero and intro fields, and edit a product's label fields; check that each change shows where expected and nowhere else. Test newsletter signup with an approved test address and consent flow: the customer is created with the `newsletter` tag and email consent, and arrives in the Mailchimp audience with the right consent and double opt-in behavior. A storefront success message alone is insufficient. Remove the test subscriber from Shopify and Mailchimp afterwards. Record each result with requirement ID, Git commit, shop, theme ID/role, URL/resource, viewport/browser, expected and observed behavior, and PASS/FAIL/BLOCKED status. Store screenshots and retests in the PR evidence.

Do not mark a requirement complete until both storefront and relevant staff editing behavior have passed. If gallery input, Shopify behavior, or access prevents a test, mark the item **Blocked** with the exact dependency. Avoid optional extra testing once material risks are resolved.

## Release gate and rollback

A release puts the review theme on the live site and makes the store changes that go with it. Each release needs Michael's explicit approval, after he has the package below.

Before requesting release approval, provide:

- The exact Git commit, the review theme's ID and name, and a checksum of the theme's files (the Git tree of `theme/`).
- The decisions it carries (none still Proposed), the requirement rows it touches, and what stays open.
- The exact store change set, in order, from `proposals/store-changes.md`, with a dry run of each step made from a fresh export. Read each row of a dry run against the specification (`design-system/DESIGN.md` §7.4 for templates), not only for its shape.
- The checks on the review theme: Theme Check, the linter, contrast, the theme copies, links, answers, structured data and fonts.
- A comparison of the live theme with the commit it was published from. Staff can edit the live theme in its editor: bring those changes into Git and onto the review theme first, so a release never drops them.
- Rollback steps for the theme and for each store change.

At the release:

1. Recheck the store, the live theme's ID and role, the review theme's ID and `UNPUBLISHED` role, and the account. Read the store again: nothing the change set touches may have changed since the export.
2. Make the store changes that must come before the theme, and check them on the review theme.
3. Publish the review theme with `shopify theme publish`. No push goes to a live theme.
4. Make the remaining store changes in order, each stopping at its first error.
5. Read the store back and compare it with what was sent. Open every page on the live site. Run the links, answers and structured data checks on the live site.
6. Make a new review theme from `main`, and write the three themes' IDs in `AGENTS.md`, `CLAUDE.md` and `PROJECT.md`. The theme that was live is kept, unchanged, as the rollback.

Rollback: republish the theme that was live before, then undo each store change from its record. Republishing a theme alone does not reverse store changes.

### The first release, 2026-09-29

The package, the change set, the results and the rollback steps are in `verification/2026-09-29-release-gate.md`; each call and the store's answer, in `proposals/store-writes/created/release-2026-09-29/`.

- **Approval:** Michael, 2026-09-29: "Everything is approved", "Supporters confirmed, keep in", "All good, release as is" (the consent wording), "Proceed with your recommendation" (the writes from files), "Everything can be put live now".
- **In order:** event pages on; publish; template names; addresses; staged text; new pages shown; frames. The print descriptions and the search engine listings were left for the gallery's approval.
- **Rollback for it:** republish `183162372393`, which is unchanged; set the 38 template names back from `dry-runs/2026-09-29/templates.md`; publish the 10 hidden pages, delete their redirects and send `/pages/who-we-are` back to `/pages/our-story`; restore each page's text from `dry-runs/2026-09-29/pages-now.json`; set `seo.hidden` back on the 23 pages and the 16 frames back to Active; turn the event pages off.
- **The fault.** The release script gave Permanent Collection and Artists the standard page template, when each has its own under the name it already had (§7.4). It was written the day before the collection moved in and not brought up to date, and the dry run showed both rows without the fault being seen. For about eight minutes the two pages had no search, browse or A to Z. The links check on the live site found it, and both were set back. The rule about reading dry runs row by row, and the links check after a template change, come from this.

### The second release, 2026-09-29

At 00:51 UTC on the 30th (5:51 PM Pacific), the review theme `184823611689` was published from `main` at 8bcfaa7. The record: `PROJECT.md`, rows 4c and 6b.

- **Approval:** Michael: "Proceed with getting this live".
- **What went live:** the artwork sits in the middle of its mat in Safari, which had pushed the home page hero's work down on iPhones (#128); the favicon (#127, DS-189); the pre-release bridges out of the theme (#123). No store changes.
- **In order:** both themes' editor JSON compared with Git (no editor changes); `main` pushed to the review theme and read back; the checks; publish; the live theme renamed "Gordon Smith Gallery" and the one it replaced "Gordon Smith Gallery (rollback, 2026-09-29)"; a new review theme, `184824398121`, pushed from `main` with `--unpublished` and read back; the checks on the live site (links 1,637 pages, 0 errors; answers 27, 0 errors; structured data 0 errors).
- **Rollback for it:** `shopify theme publish --store ed35ee-ea.myshopify.com --theme 184767250729`. There are no store changes to undo.
- **A release without store changes** takes these steps alone. The package is the commit, the checks and what the release carries.

### The third release

At 01:19 UTC on 2026-09-30 (6:19 PM Pacific on the 29th), the review theme `184824398121` was published from `main` at 1168190. The record: `PROJECT.md`, rows 4d and 6c.

- **Approval:** Michael: "put it live", after seeing the header still scroll away on his phone on the live site.
- **What went live:** the header stays at the top of the screen on phones and small tablets (#132, DS-190). The only other theme change since the second release, the "Artist for Kids" settings line (#129), was already live (#133). No store changes.
- **In order:** as the second release. Both themes' editor JSON compared with Git (no editor changes); the review theme downloaded, matching `main` file for file; the checks; publish; renames; a new review theme, `184824725801`, pushed from `main` with `--unpublished` and read back; the checks on the live site (links 1,637 pages, 0 errors; answers 27, 0 errors; structured data 0 errors).
- **Rollback for it:** `shopify theme publish --store ed35ee-ea.myshopify.com --theme 184823611689`. There are no store changes to undo.

### The fourth release

At 20:15 UTC on 2026-10-01 (1:15 PM Pacific), the review theme `184824725801` was published from `main` at 220213c. The record: `PROJECT.md`, rows 4e and 6d.

- **Approval:** Michael: "can we do our release now?", after #138 was merged and pushed to the review theme.
- **What went live:** the theme changes from the gallery's answers (#138, DS-191 to DS-197): closures in the "open today" line, Plan your visit, the data and `/llms.txt`; the Foundation's accounts in the footer; the gallery's year, owner, funders and the two charity numbers in the data; Artists for Kids in the gallery's words in `/llms.txt`; the gallery's sentence in Home's Visit block; an FAQ answer stops at a group heading, and a written description is compared over 120 letters; artists' addresses elsewhere in their data.
- **Store changes at it** (`proposals/store-changes.md` §9c, `gallery_answers.py`): the FAQ's eight visiting questions under "Visiting", with "Buying prints" over the rest; The Smith Foundation's staged description deleted, then the staged field's definition. §8d is finished.
- **In order:** as the third release, with the store changes after the publish. Both themes downloaded whole and compared with Git (no editor changes); the checks; the store steps' dry runs; publish; renames; the three store steps, each read back; a new review theme, `184856445225`, pushed from `main` with `--unpublished` and read back; the checks on the live site.
- **Rollback for it:** `shopify theme publish --store ed35ee-ea.myshopify.com --theme 184824398121`, then the FAQ's text and The Smith Foundation's staged description back from `proposals/store-writes/snapshots/gallery-answers-2026-10-01-before.json` (the definition first: `custom.release_description`, multi-line text, pinned, storefront read). The old theme reads a staged description first, and its FAQ data would let the last visiting answer take the next heading with it, so both matter.

### The fifth release

At 21:33 UTC on 2026-10-01 (2:33 PM Pacific), the review theme `184856445225` was published from `main` at a03a1e4. The record: `PROJECT.md`, rows 4f and 6e.

- **Approval:** Michael: "Merge #143 and do the release".
- **What went live:** the class list (#142, P-68, DS-198). After School Art lists its six fall classes, each with a Register button straight to its own registration page on the district's site.
- **Store change at it** (`proposals/store-changes.md` §9d): After School Art's button to the district's landing page (`custom.cta`) deleted, its value saved first (`proposals/store-writes/snapshots/after-school-art-cta-before-release.json`). The answers check's question 33 lost its gap.
- **In order:** both themes downloaded whole and compared with Git (no editor changes); the checks; the store step's dry run; publish; renames; the store step, read back; a new review theme, `184857461033`, pushed from `main` with `--unpublished` and read back; the checks on the live site.
- **Rollback for it:** `shopify theme publish --store ed35ee-ea.myshopify.com --theme 184824725801`, then After School Art's `custom.cta` back from the snapshot (`metafieldsSet`, type link). The six Class entries can stay: the old theme doesn't read them.
- **For the team:** the district's After School Art landing page can now be cut back to a link to this site (P-30, P-68).

### The sixth release

At 22:54 UTC on 2026-10-01 (3:54 PM Pacific), the review theme `184857461033` was published from `main` at 0f91be7 (6204cb1 adds records only). The record: `PROJECT.md`, rows 4g and 6f.

- **Approval:** Michael: "Merge #151 and do the release".
- **What went live:** the home page (#150, DS-199 to DS-204, `proposals/home-review.md`): today's opening line and Plan your visit in the hero; a run that repeats says its pattern and next date ("Saturdays, 1 to 3 PM. Next: October 3"); a wider artwork hero from 1200 px; "Make art with us", the three newest ArtReach videos; photo credits kept on one line; What's on without a second today's line; Home's rows follow the count rule.
- **No store change at it.**
- **In order:** both themes downloaded whole and compared with Git (no editor changes); the checks; publish; renames; a new review theme, `184858575145`, pushed from `main` with `--unpublished` and read back; the checks on the live site; then the fourth release's rollback, `184824725801`, deleted (P-69), after it matched 220213c file for file.
- **Rollback for it:** `shopify theme publish --store ed35ee-ea.myshopify.com --theme 184856445225`. Nothing in the store to undo.

## Inputs, exclusions, and known limits

Gallery inputs still needed (tracked in `PROJECT.md`, "Waiting on"):

- Signup wording and consent wording. No signup destination is needed: the band uses Shopify's form (P-18).
- Contact email addresses, phone, hours, social URLs, and any replacement images or captions. Menu labels were approved on 2026-09-25.
- Q10: room names for the exhibition venue field and the label for the second artist group. *Stitched* opened April 3, as the old site's post says.
- Q11, answered: the land acknowledgement characters Mulish lacks show in Arial (L-06; P-58, Michael, 2026-09-28).
- The open content items in `proposals/store-writes/README.md`: Omer Arbel's biography, and the gallery's word on the medium given to *Good Luck (wheelbarrow)*. The product description clean-up is decided (P-21, P-22); the gallery approves its dry run, and it is made after that.

Existing copy remains in place until supplied or specifically approved for change. The brand guide and available logos are present in `reference/`; no paid Soleil web font files are present.

Replacing the theme is in scope (P-13). Do not expand into platform replacement, rebranding, general content rewriting, paid apps, checkout changes, new shop functionality, or archive reconstruction without a separate approval. Shopify focal-point support depends on the image source and how the theme renders it; verify it in the editor and preview before closing IMG-03. The new theme replaced the old theme's page-specific JSON templates and generated blocks, so their content moved into fields and entries (`proposals/content-migration.md`). Document any remaining platform limit rather than treating an untested workaround as complete.
