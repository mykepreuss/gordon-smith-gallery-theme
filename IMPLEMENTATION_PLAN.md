# Gordon Smith Gallery website improvement project

## Purpose and authority

Improve the existing Shopify storefront's navigation, visual consistency, image treatment, exhibition and Shop pathways, site-wide access points, and staff editing workflow. The [developer notes](reference/Gordon%20Smith%20Gallery%20Website%20Notes%20for%20Developer.docx.md) are the authoritative requirements. The [brand guide](reference/GordonSmith-BrandGuide_sm.pdf) and [logo guide](reference/GS-Logo-Guide.pdf) constrain visual implementation. The numbered workflow supplied with the request is the execution framework; no separate implementation-plan file was present at discovery.

**Approach, decided 2026-09-25 (P-13):** build a new theme for the same store, as if starting from scratch today, instead of modifying the current Colorblock theme. The developer notes, the approved decisions (`DECISIONS.md`) and `design-system/` drive the design. The current theme is a reference for content and placement only: `proposals/content-migration.md` lists everything it holds and where each item goes. The new theme starts from Shopify's Skeleton theme (P-14). It is still Shopify, with the same store, products, collections and pages. The live theme stays untouched until release and remains the rollback.

Work is GitHub-first. Theme code, the requirements register, proposed Shopify resource changes, decisions, and test evidence must be reviewable in a private GitHub pull request before production release. An unpublished Shopify theme is needed for realistic storefront and staff-editor review, but must never be treated as the live theme. Publishing and applying changes to live-referenced store resources require explicit release approval.

Keep four change surfaces distinct: **Git owns theme source and project records; the unpublished theme owns preview-specific code and settings; Shopify Admin resources are shared across themes; installed apps have their own configuration and theme-specific placements.** Theme preview is not a copy of the store. Use Shopify CLI as the default path for writing theme files and the connector or Admin only for verified, approved store-resource operations. Shopify's theme-file GraphQL mutation requires an additional exemption beyond `write_themes`, so the connector's scope alone does not establish a usable theme deployment path. [Shopify theme-file mutation](https://shopify.dev/docs/api/admin-graphql/2026-01/mutations/themeFilesUpsert).

## Where the project stands (2026-09-26)

- **Built:** the new theme on Shopify's Skeleton theme, every template, the header, footer and newsletter band (`theme/`, `design-system/DESIGN.md` 0.6.4).
- **Content:** everything the current theme held is in the store or the theme: 15 exhibitions, programme and information pages, card groups, events, product labels and three review menus (`proposals/store-writes/README.md`). Page text that changes at release is staged (DS-39).
- **Decisions:** every design decision is decided (DS-01 to DS-52, `DECISIONS.md`).
- **Review theme:** `184767250729` "New theme for review (do not publish)", matching `main` at 1ad4dba.
  - Preview: https://ed35ee-ea.myshopify.com?preview_theme_id=184767250729
  - Editor: https://ed35ee-ea.myshopify.com/admin/themes/184767250729/editor
- **Phase: iterating on the site.** Changes follow "How we iterate" below. **Release is on hold** until Michael decides to go ahead. Until then nothing the live site shows changes, and the release work in "Release backlog" waits.

## Discovery snapshot and preflight

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

Structural choices, updated 2026-09-25: a section with pages under it is a single button that opens its dropdown, and the section's main page is the first link inside it (DS-11); for Exhibitions that first link is **On Now**. This replaces the earlier choice of a linked parent label with a separate dropdown caret. On 2026-09-25 the gallery approved the menu map and labels, the page types, the contact and newsletter placement (P-15) and the content model (DS-14 to DS-16); Exhibitions is the first menu item (P-09). Gallery staff still supply editorial content.

The design specification is `design-system/DESIGN.md`, with tokens, components, scripts and checks in `design-system/`. The theme's `gs-` snippets live in `theme/snippets/`; `design-system/scripts/sync_theme.py` copies the shared CSS, JavaScript and logos into the theme and checks that the copies match. Design decisions (DS-01 onwards) and project decisions (P-01 onwards) are recorded in `DECISIONS.md`. The menu map (`proposals/store-changes.md` §1) follows this model:

- A section with pages under it is one button (a native `<details>`/`<summary>` disclosure) that opens its dropdown and never navigates; its main page is the first dropdown link, with its own label. Direct pages remain single links. No dropdown item repeats its section's label. Apply the same model to desktop and mobile, with visible focus, exposed expanded state, Enter/Space opening, and Escape closing with focus restored. Navigation must keep working without JavaScript (DS-19). Use ordinary site navigation semantics rather than ARIA application-menu roles. [Shopify accessibility guidance](https://shopify.dev/docs/storefronts/themes/best-practices/accessibility).
- Offer On Now, Upcoming, and Past directly. There is no Exhibitions overview page: it and its text are removed, and its address redirects to On Now at release (P-20, 2026-09-26). Exhibitions become structured entries at new addresses, with redirects from the old exhibition pages (P-10). Past Exhibitions lists past exhibitions automatically from those entries and keeps each current card's image, dates and title (DS-24, DS-25).
- Make Shop lead to the Limited Editions landing page, with a short portfolio hierarchy. Correct internal portfolio targets. Keep the landing page to one introduction, one portfolio navigation area, and a restrained featured image/hero; preserve individual portfolio layouts.
- Put a reusable newsletter band above the footer, Contact in a persistent header/utility and footer location, and social links in the footer. The band uses Shopify's own newsletter form (a `customer` form that tags the customer `newsletter` and records email marketing consent), and the installed Mailchimp for Shopify app syncs subscribed customers to the gallery's audience (option 1 in `baseline/mailchimp-audit.md`, P-18). It needs no ScriptTag and no new app, and it works in any theme. Before release, verify in the app that customer sync is on, that consent and the `newsletter` tag reach the right audience, and how double opt-in behaves; then run the test signup in the verification rules. If the sync can't be verified, fall back to a prominent link to a gallery-supplied Mailchimp signup page and record the limitation.

Use **Mulish** as the free Google Fonts option already identified in the brand guide. The guide specifies heavy uppercase headings/subheadings, bold introduction text, regular body text, and light captions. Bundle Mulish's licensed web font files with the new theme rather than offering a font picker, since fonts are not a staff choice. Do not rely on an undocumented fallback to Assistant. Set scale, weights, line heights, and any specified letter spacing through shared rules; leave font kerning at its normal browser behavior unless the guide requires an override. Preserve approved logo assets and brand colors, and evaluate header identity size in context. [Mulish license](https://github.com/googlefonts/mulish/blob/main/OFL.txt); [Shopify font guidance](https://shopify.dev/docs/storefronts/themes/architecture/settings/fonts).

Build shared Liquid/CSS rules and reusable hero, card, gallery, link, and CTA treatments. Keep page-specific words, images, captions, and links in page content or page-specific fields rather than hard-coding them into a shared template's configuration. Use Shopify image focal points where supported, preferably through `image_tag`; use a separate mobile image only where a single crop cannot work. Preserve existing content (page bodies, images, captions, links); the templates that hold it are replaced, and content they hold moves as `proposals/content-migration.md` sets out. [Shopify focal-point guidance](https://shopify.dev/docs/storefronts/themes/architecture/settings/input-settings).

Build new header and footer section groups in the new theme. A JSON template's section configuration is shared by every resource assigned that template, so test content isolation with two pages before calling the editor model complete. If a new alternate template exists only in the unpublished theme, preview it in that theme or with the supported `?view=` route; the normal Admin assignment menu draws from the live theme, and changing an existing resource's template assignment is a store-level release action. [Shopify template behavior](https://help.shopify.com/en/manual/online-store/themes/theme-structure/templates), [alternate-template preview](https://shopify.dev/docs/storefronts/themes/architecture/templates/alternate-templates).

The menu map, page hierarchy, component/editor model, shared access placement and the first store-level field definitions were approved on 2026-09-25. The additions found by the content inventory (card groups, events and a few smaller fields: content model parts 4 to 6, P-16) were approved the same day (P-16). The design decisions made during the build (DS-28 to DS-38) and the choices made while moving content into fields and entries (`proposals/store-writes/README.md`) were approved by Michael on 2026-09-25.

Michael is the approver for structural and design decisions and for content-moving choices (P-17). The gallery still supplies wording and values: labels, editorial copy, contact details and consent text (EXH-04, ACCESS-04). Record each new decision in `DECISIONS.md` as Proposed when it is built, and get Michael's approval before the release gate. Nothing still marked Proposed ships.

## GitHub-first delivery workflow

1. **Create the source of truth.** Initialize Git in this folder. Pull the exact verified live theme into `theme/` without changing Shopify, and commit it as the untouched baseline with the reference materials, requirement register, baseline evidence index, and a manifest of store resources. Create a private `mykepreuss/gordon-smith-gallery-theme` repository unless the gallery supplies an existing repository or organization destination. Keep credentials and tokens out of Git. Record the source theme ID, pull time, CLI version, and baseline Theme Check output. Add concise `PROJECT.md` for milestone/requirement status, `DECISIONS.md` for approvals, and repository `AGENTS.md` for store-target and release rules without overriding existing user instructions. *Done 2026-09-25: baseline commit 27ef593.*
2. **Build the new theme after the structural approval.** Work on a feature branch. Move the untouched baseline to `baseline/theme/` so that `theme/` holds the new theme; the baseline commit stays unchanged in history. Start from Shopify's Skeleton theme, add the design system's tokens, components and snippets, then build the approved template set (`design-system/DESIGN.md` §7), header, footer, newsletter band and commerce templates (product, collection, cart, search and system pages). The store uses Shopify's new customer accounts, so the theme needs no account templates. Prepare the content migration as scripts or instructions in Git. Creating definitions, entries and field values is a store write, even when it's invisible under the live theme: follow "Store writes before release" below. Separate theme-only changes from proposed store-level changes in both commits and the register. Theme-only changes include Liquid, CSS, JavaScript, JSON templates, section groups, and settings for the future unpublished theme. Store-level changes include menus, page content/fields and template assignments, products, collections, Files and shared image metadata, redirects, and Mailchimp configuration. A preview theme does not sandbox any of these Admin resources. Keep proposed store-level changes as reviewable manifests or instructions in Git until the relevant preview or release gate. Use CLI for theme file writes and only a verified connector/Admin capability for approved Admin writes. [Shopify store-resource behavior](https://help.shopify.com/en/manual/online-store/themes/customizing-themes/theme-editor/add-and-edit-store-resources). *Built 2026-09-25 on `build-new-theme`: the template set, then design passes with real content for Home, Exhibitions, the programme pages and Shop. All content migrated the same day, with the page text that changes at release staged (DS-39, `proposals/store-writes/README.md`). What's left is under "Iteration backlog" and "Release backlog".*
3. **Open a reviewable pull request before Shopify preview writes.** Include the code diff, requirement statuses, proposed menu map and store resource changes, missing gallery inputs, theme check output, and the content parity check against `proposals/content-migration.md`. Do not auto-deploy or connect the repository to production. *Done: [PR #4](https://github.com/mykepreuss/gordon-smith-gallery-theme/pull/4) (the build) merged 2026-09-25; [PR #6](https://github.com/mykepreuss/gordon-smith-gallery-theme/pull/6) (page passes, plan review, content migration) and [PR #5](https://github.com/mykepreuss/gordon-smith-gallery-theme/pull/5) (the design-system preview) merged 2026-09-26.* From here, make changes in smaller pull requests, one per page or topic, each passing the checks in "Verification and completion rules". Push the review theme only from `main` or a reviewed branch, and record the commit in the PR.
4. **Create the designated unpublished review theme.** Reverify the store and live theme ID, upload the new theme as a clearly named unpublished theme (`shopify theme push --unpublished`), and record its new ID and `UNPUBLISHED` role in the PR, `AGENTS.md` and `PROJECT.md`. Push only to that ID using CLI `--theme <verified ID>` and `--strict`; never use `--allow-live` or `theme push --publish`. A separate menu may be created and referenced only by this theme for realistic navigation testing. Prefer an existing resource or theme-editor preview for staff testing; a temporary page is still a store-level resource, so create one only if necessary and explicitly approved, and do not assume an unpublished page has a visitor preview URL. During review, change nothing the live theme shows: see "Store writes before release". [Theme push](https://shopify.dev/docs/api/shopify-cli/theme/theme-push). *Done 2026-09-26: review theme `184767250729`, "New theme for review (do not publish)", from `main` at 594eb01. Preview: https://ed35ee-ea.myshopify.com?preview_theme_id=184767250729. Before each push, bring any theme editor changes into Git first (`AGENTS.md`).*
5. **Keep the PR and preview synchronized.** Every preview change must correspond to a reviewed Git commit or a logged preview-only store resource. Record the exact theme ID, Git commit, changed files/resources, and preview URL in the PR. Recheck for concurrent edits to the live theme before release and reconcile drift deliberately. *Ongoing: see "How we iterate".*

GitHub can hold the code and proposed definitions for menus and other Shopify resources, but cannot itself host their working Admin state. The unpublished theme and separate preview resources are limited Shopify writes for review; they are not production changes. Record any preview-only Admin resource and its cleanup path separately from the theme. Use the theme ID and Git commit as durable review identifiers because shareable preview URLs may expire.

**Development theme and review theme.** `shopify theme dev` serves the branch you're working on as a development theme (ID 184755814697 so far). It's hidden, tied to the CLI session and temporary: logging the CLI out removes it, and a new session can make one with a different ID. Use it for working checks only. The review theme (`184767250729`) follows `main` and is what Michael and gallery staff review and edit. All evidence for the verification rules and the release gate is captured on the review theme.

### How we iterate

The loop for every change while release is on hold:

1. **Branch** from an up-to-date `main`, one page or topic per branch.
2. **Work** against the development theme: `shopify theme dev --store ed35ee-ea.myshopify.com --path theme` serves the branch at http://127.0.0.1:9292. Check design changes at 1440, 768 and 390.
3. **Design system first:**
   - Values go in `design-system/tokens.css` and shared styles in `components.css`; then run `sync_theme.py theme/`.
   - A new component or rule goes in `DESIGN.md` and `preview.html`.
   - Bump the version and add a changelog line.
4. **Decisions:** a new design or structural choice is recorded as Proposed in `DECISIONS.md` and `DESIGN.md` §12. Michael approves it (P-17); nothing Proposed ships.
5. **Store writes:** only the kinds under "Store writes before release", with Michael's go-ahead, a before-snapshot and an undo step, logged in `proposals/store-writes/README.md`. A change to a page's own text is staged in `custom.release_body` (DS-39), never written to the live page.
6. **Records in the same pull request:**
   - the affected `REQUIREMENTS.md` rows;
   - anything that must happen at release, in `proposals/store-changes.md` and "Release backlog";
   - `PROJECT.md` if a status or open question changes.
7. **Checks:** the ones under "Verification and completion rules" that a pull request needs: Theme Check, the linter and its tests, `check_contrast.py`, `sync_theme.py --check` and `git diff --check`.
8. **Pull request;** Michael reviews and merges.
9. **Review theme:** after the merge, update it from `main`.
   - Pull its `config/settings_data.json` and `templates/*.json` and compare them with Git. Bring any theme editor changes into Git first (`AGENTS.md`).
   - Push with `--strict`, and record the commit in `PROJECT.md`, milestone 4.
   - A reviewed branch may go to the review theme before it merges, when Michael wants to see it there. The review theme is then ahead of `main` until the merge, and the pull request says so.

### Store writes before release

Allowed with Michael's go-ahead, logged in `proposals/store-writes/README.md` with a before-snapshot and undo steps:

- New definitions (metafields and metaobjects).
- New entries, as long as their pages return 404 under the live theme.
- Field values the live theme doesn't read. Check `baseline/theme/` before writing, and check that the live pages still render normally afterwards.

Not allowed before release, because the live theme shows them:

- Page bodies and titles, product titles and descriptions.
- Page template assignments.
- The live menus.
- Redirects, and hiding or deleting pages.
- Anything else the live theme renders.

These go in the release change set.

### Iteration backlog

Open while iterating. Add what each review finds; take items off when they merge.

| Item | Owner | Notes |
| --- | --- | --- |
| Set the seven hero focal points in the admin (Content > Files), then check them on the review theme at phone width | Michael, then Agent | `proposals/hero-focal-points.md`, each point tried on the preview first (2026-09-26). Shopify's API can't set focal points. IMG-02, IMG-03 |
| Send the gallery its questions: values, exhibitions, content checks, brand | Michael | `proposals/gallery-questions.md` collects all of them in one place (2026-09-26) |

### Release backlog (on hold until Michael decides to release)

Done so far: every page's content, the 15 exhibitions, the card groups and events, the product labels and the three review menus (2026-09-25); the review fixes, a design pass on every page, every design decision, the frames decision (P-19), the product description decision (P-21, P-22) and the review theme (2026-09-26). Also on 2026-09-26: the release script with a dry run of every step (`proposals/store-writes/release.py`, `dry-runs/2026-09-26/`), and the agent's verification checks (`verification/2026-09-26.md`).

| Item | Owner | Notes |
| --- | --- | --- |
| The gallery approves the product description clean-up | Gallery | The before-and-after list: `proposals/store-writes/dry-runs/2026-09-26/products.md` |
| On the day: fresh exports of pages and the 21 prints, the dry runs again, then each step with `--vars` in order: publish, templates, addresses, staged text, products, frames | Agent, Michael | `release.py` docstring. Each step stops or reports before it changes anything |
| The date checks: an event dropping off after it ends, an exhibition changing status at midnight Pacific | Agent | `verification/2026-09-26.md`: the first can be seen after 3 PM on 2026-09-26; the second needs a real changeover or a test entry with Michael's go-ahead |
| The staff editing test and the newsletter test | Gallery staff, Mailchimp access | Staff use the review theme's editor |
| Mailchimp app settings: customer sync, audience, consent mapping, double opt-in | Gallery or Michael | ACCESS-01; needs app access |
| The release gate | Agent, Michael | "Release gate and rollback" |
| After release: remove the pre-release bridges, which are the staged-text fallback in `gs-page-text` (DS-39) and the list of old template names in `gs-is-programme-page` (L-08) | Agent | One follow-up pull request, once the release scripts have run |

## Verification and completion rules

Run Shopify Theme Check without auto-correction and validate all changed JSON templates. Capture its config/version. The new theme must have no Theme Check errors and no design-system linter errors (`design-system/scripts/lint_theme.py`); explain any remaining warning in the PR. Also run the linter's tests, `check_contrast.py` and `sync_theme.py theme/ --check` (all in `design-system/scripts/`). Run `audit_fonts.py` against the review theme: no text may render in a fallback font except the land acknowledgement characters in L-06. Run `git diff --check`, then require CLI `theme push --strict` to succeed against the verified unpublished ID. Theme Check does not prove browser behavior. [Shopify Theme Check](https://shopify.dev/docs/storefronts/themes/tools/theme-check/commands), [strict push](https://shopify.dev/docs/api/shopify-cli/theme/theme-push).

Test at approximately 1440, 768, and 390 pixel viewport widths, plus a real or emulated touch interaction and widths around actual breakpoints. Exercise mouse, touch, Tab, Enter/Space, Escape, focus states, and direct page links. Inspect Home, About, Artists for Kids, Programs, Smith Foundation, On Now, Upcoming, Past Exhibitions, an individual exhibition, Shop, a portfolio collection, a product, and Contact. Compare image focal points, responsive crops, typography, link states, and shared component spacing. Any retained autoplay slideshow needs accessible pause and next/previous controls. Verify all changed internal and external URLs, relevant console/network errors, and a representative product/cart path without placing an order. Check that every item in `proposals/content-migration.md` is present in the new theme or was deliberately dropped.

Test the date-driven behavior, which uses the store's time zone (America/Los_Angeles). An exhibition moves between upcoming, on now and past at midnight Pacific on its start and end dates, on the home page and every list. An event drops off once it has ended. The opening reception stops showing once it has ended. A draft entry never shows. Check on real date changes where they fall during review, or with a test entry made with Michael's go-ahead and deleted afterwards.

Have a gallery staff member or a representative editor update preview theme settings and, only where safely authorized, representative resource content using the documented workflow. Compare two resources on the same template to confirm that page-specific content does not leak while shared styling remains coherent. Staff will mostly edit entries and fields, so the test also covers them: create and edit an exhibition entry and an event, change a card in a card group, fill a page's hero and intro fields, and edit a product's label fields; check that each change shows where expected and nowhere else. Test newsletter signup with an approved test address and consent flow: the customer is created with the `newsletter` tag and email consent, and arrives in the Mailchimp audience with the right consent and double opt-in behavior. A storefront success message alone is insufficient. Remove the test subscriber from Shopify and Mailchimp afterwards. Record each result with requirement ID, Git commit, shop, theme ID/role, URL/resource, viewport/browser, expected and observed behavior, and PASS/FAIL/BLOCKED status. Store screenshots and retests in the PR evidence.

Do not mark a requirement complete until both storefront and relevant staff editing behavior have passed. If gallery input, Shopify behavior, or access prevents a test, mark the item **Blocked** with the exact dependency. Avoid optional extra testing once material risks are resolved.

## Release gate and rollback

Before requesting release approval, provide:

- The private GitHub PR and exact Git commit, review theme ID and name, and theme file snapshot or checksum manifest.
- Completed, blocked, and deferred requirement IDs; remaining issues; approved decisions (none still Proposed); and gallery inputs used.
- The exact live-store change set, in order, from `proposals/store-changes.md`:
  1. Before publishing: the theme settings values still to fill in the review theme (hours, email, phone, social links, consent wording), and the Mailchimp app configuration.
  2. Publishing the review theme.
  3. Reassigning every page's template, by script, straight after publishing (below).
  4. Switching or editing the main menu, and editing the footer menu.
  5. Hiding the six old exhibition pages and the Exhibitions overview, and creating their redirects (P-10, P-20). Hiding About and Our Story too, with `/pages/about` forwarded to About Us (P-24) and `/pages/our-story` to Artists for Kids (P-25).
  6. Moving the staged page text into its nine pages and deleting the temporary field (DS-39, `proposals/store-changes.md` §8). This clears the exhibition text repeated in On Now, Upcoming and Upcoming Events, adds Donate's tax receipt note and the Gordon and Marion video, makes the Artists names one list, leaves About Us's descriptions to its card group (DS-50), adds About's history to the Artists for Kids page (P-24), and tidies The Smith Foundation's text (DS-52).
  7. Plain-text titles and the description clean-up on the 21 limited editions, after a dry run the gallery approves (DS-16, P-21, P-22, `proposals/store-changes.md` §7).
  8. Setting the 16 active frame products to Unlisted, so they leave search (P-19, `proposals/store-changes.md` §9).
- A check that every active exhibition entry is ready to be seen. The entries are already active; their pages return 404 only because the live theme has no exhibition template, so publishing the new theme makes them public.
- Test evidence for storefront and staff editing, plus comparison against the latest live theme state.
- Rollback steps: retain the original live theme and its ID; republish it if needed; restore page template assignments from the script's snapshot; unhide the old exhibition pages and delete their redirects; restore product titles from `proposals/store-writes/snapshots/prints-2026-09-25.json` and descriptions from the snapshot taken before their clean-up, frame products to Active from `snapshots/frames-2026-09-26.json`, and page bodies from their before-snapshots; restore any separately changed live menu, page, File, or app resource from its own recorded pre-release snapshot. Theme rollback alone does not reverse store-resource changes.

**Template reassignment** (`release.py templates`, dry run 2026-09-26: 20 pages change; Our Story and About are hidden instead, P-24, P-25). Pages keep their old template names until release (L-08). The new theme doesn't have most of those templates, so after publishing, those pages fall back to the default page template. Since DS-48 and DS-49 every page still renders correctly that way: the exhibition lists come from Theme settings, and a page on the Shop template other than the Shop landing (Our Story, old template `shop`) reads as a plain page. So the gap after publishing no longer shows to visitors; the reassignment puts the right template name on each page in the admin, for staff. Before release, write a script in `proposals/store-writes/` that:

1. Snapshots every page's current template, for rollback.
2. Maps each page to its new template (`design-system/DESIGN.md` §7.4).
3. Prints the changes without making them (a dry run).

Michael checks the dry run. At release, run the script straight after publishing, then open every page to check it.

Immediately before release, pull the then-current live theme into a separate comparison location and inspect every change since the Git baseline. Snapshot affected store resources again and reconcile drift before publication; do not overwrite unreviewed staff or vendor changes. Confirm that the candidate theme still has the recorded `UNPUBLISHED` ID and matches the reviewed Git commit. The candidate may already reference a preview-only menu or app embed, which becomes publicly active when that theme is published; include every such dependency in the exact release change set. Publish the approved theme with a separate `theme publish` action, then apply any remaining approved live-referenced store changes in a coordinated sequence. Both actions require **explicit release approval**. Verify the public site, including the Mailchimp app embed or other chosen integration, after publication and record the final theme ID, commit, live resource versions, and smoke-test results.

## Inputs, exclusions, and known limits

Gallery inputs still needed (tracked in `PROJECT.md`, "Waiting on"):

- Signup wording and consent wording. No signup destination is needed: the band uses Shopify's form (P-18).
- Contact email addresses, phone, hours, social URLs, and any replacement images or captions. Menu labels were approved on 2026-09-25.
- Q10: room names for the exhibition venue field, the label for the second artist group, and the start date of *Stitched*.
- Q11: whether to accept Arial for the land acknowledgement characters Mulish lacks, or load a font made for BC Indigenous languages (L-06).
- The open content items in `proposals/store-writes/README.md`: Omer Arbel's biography and a medium for *Good Luck (wheelbarrow)*. The product description clean-up is decided (P-21, P-22); the gallery approves its dry run at release.

Existing copy remains in place until supplied or specifically approved for change. The brand guide and available logos are present in `reference/`; no paid Soleil web font files are present.

Replacing the theme is in scope (P-13). Do not expand into platform replacement, rebranding, general content rewriting, paid apps, checkout changes, new shop functionality, or archive reconstruction without a separate approval. Shopify focal-point support depends on the image source and how the theme renders it; verify it in the editor and preview before closing IMG-03. The new theme replaces the current page-specific JSON templates and generated blocks, so their content moves into fields and entries (`proposals/content-migration.md`). Document any remaining platform limit rather than treating an untested workaround as complete.
