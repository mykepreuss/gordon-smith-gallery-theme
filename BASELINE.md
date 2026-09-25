# Baseline evidence index

What the live store and site looked like before any change (plan step 1). Everything here was gathered read-only. A finding here is not completion evidence for any requirement.

## Source theme

| Field | Value |
| --- | --- |
| Store | `ed35ee-ea.myshopify.com` (public `gordonsmithgallery.com`) |
| Live theme | `183162372393` "Colorblock: NEW WEBSITE", role MAIN, Colorblock 15.5.0 |
| Pulled into | `theme/` (untouched; first theme commit) |
| Pull time (UTC) | 2026-09-25, about 21:16 (file times of the pulled files) |
| Pulled by | Michael, on his Mac: `shopify theme pull --store ed35ee-ea.myshopify.com --theme 183162372393 --path theme`. The pull output didn't print the CLI version; discovery used 4.8.2 |
| Files | 402, committed unchanged as the first theme commit |

Before release, pull the then-current live theme into a separate folder and compare it with this commit file by file (plan, "Release gate and rollback").

## Checks on the untouched theme

| Check | Result | File |
| --- | --- | --- |
| Shopify Theme Check (no auto-correct), Shopify CLI 4.8.2 | 4 errors, 11 warnings in 11 files | `baseline/theme-check.json`, `baseline/theme-check.txt` |
| Design-system linter (`design-system/scripts/lint_theme.py theme/`) | 39 errors, 200 warnings with the design system 0.4.1 rules. Expected: the linter checks the target structure, which the current theme predates | `baseline/lint-theme.txt` |

### What the checks show

- **Theme Check errors:** all four are the `push` filter, which Theme Check doesn't recognise, in two "Cart frame upsells" blocks generated in the theme editor (`blocks/ai_gen_block_3c79063.liquid` in the cart template, `blocks/ai_gen_block_70a7f5b.liquid` in the home template). The frame suggestions they are meant to show probably never appear. Not tested on the storefront. Outside this project's scope; flagged for the gallery.
- **Rotating image banner:** used in 10 templates, it is another generated block (`blocks/ai_gen_block_72565eb.liquid`) with 85 staff settings, over Theme Check's limit of 40 (IMG-01, IMG-04, L-05).
- **Linter errors:** 32 of 39 are templates outside the approved set (L-01). The other seven are structure on the home, Shop, collection and Past Exhibitions templates. The first run reported 46 errors because the rules left out Shopify's seven customer account templates (`templates/customers/*`); design system 0.4.1 lists them as system templates and `lint-theme.txt` was re-run with those rules (the first run is in Git history).
- **Linter warnings:** 170 are staff design controls (sizes, alignments, layouts and colour schemes) whose values move into tokens, 18 are disabled sections left in templates, and 12 are sections outside the design system's section groups.
- **Apps:** no app embeds in `config/settings_data.json`, no app blocks in any template or section group, and no Mailchimp reference in theme files. All social link settings are empty.

## Store resources

`baseline/store-manifest.md`: themes, menus (with the live header menu's problems marked), 35 pages with template suffixes, 7 collections, 38 products, field definitions. Snapshot 2026-09-25, about 19:10 UTC.

## Storefront screenshots

`baseline/screenshots/`, captured 2026-09-25 from 19:18 to 19:30 UTC with headless Chromium (Playwright), `capture-log.json` records each URL, status and width.

- Pages: home, Exhibitions overview, On Now, Upcoming, Past, one exhibition (One Hundred Artists Deep), Shop landing, `/collections`, 2026 Fall Portfolio, one product (Gordon Smith, *Pender Harbour*), About, Artists for Kids, Public Programs, The Smith Foundation, Contact.
- Widths: 1440, 768 and 390 px, first screen as `<page>-<width>.jpg`; full pages for home, Shop, Exhibitions overview, On Now and `/collections` as `<page>-<width>-full.jpg`.
- Navigation: `nav-desktop-1.jpg` to `nav-desktop-5.jpg` (each dropdown open at 1440), `nav-mobile-open.jpg`, `nav-mobile-submenu.jpg`.

Findings recorded in `capture-log.json`:

- Five of six top-level items (About, Exhibitions, Programs, Smith Foundation, Shop) are dropdown buttons with no link, so their own pages are unreachable from the menu. Artists For Kids is a plain link.
- Hovering does not open dropdowns (click only).
- Computed font for body, headings, navigation and buttons: Assistant.

## Mailchimp

`baseline/mailchimp-audit.md`: the Mailchimp for Shopify app is connected (web pixel, one audience) and its storefront script loads through a ScriptTag, which Shopify stops injecting on 2027-03-01. No signup form is rendered anywhere on the site. The pulled theme has no Mailchimp app embed or app block. App settings and consent behaviour are not yet verified.

## Known drift during the snapshot

Staff were editing products while the baseline was taken (Arnold Shives prints and frame, 18:02 to 19:02 UTC). The live theme's "updated" time (19:02:55 UTC) matches one of those product saves to the second.
