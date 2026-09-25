# Baseline evidence index

What the live store and site looked like before any change (plan step 1). Everything here was gathered read-only. A finding here is not completion evidence for any requirement.

## Source theme

| Field | Value |
| --- | --- |
| Store | `ed35ee-ea.myshopify.com` (public `gordonsmithgallery.com`) |
| Live theme | `183162372393` "Colorblock: NEW WEBSITE", role MAIN, Colorblock 15.5.0 |
| Pulled into | `theme/` (untouched; first theme commit) |
| Pull time (UTC) | PULL_TIME |
| Pulled by | Shopify CLI PULL_CLI on Michael's Mac |
| Files | THEME_FILES |

Before release, pull the then-current live theme into a separate folder and compare it with this commit file by file (plan, "Release gate and rollback").

## Checks on the untouched theme

| Check | Result | File |
| --- | --- | --- |
| Shopify Theme Check (no auto-correct), Shopify CLI 4.8.2 | THEME_CHECK | `baseline/theme-check.json`, `baseline/theme-check.txt` |
| Design-system linter (`design-system/scripts/lint_theme.py theme/`) | LINT_RESULT | `baseline/lint-theme.txt` |

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

`baseline/mailchimp-audit.md`: the Mailchimp for Shopify app is connected (web pixel, one audience) and its storefront script loads through a ScriptTag, which Shopify stops injecting on 2027-03-01. No signup form is rendered anywhere on the site. App settings and consent behaviour are not yet verified.

## Known drift during the snapshot

Staff were editing products while the baseline was taken (Arnold Shives prints and frame, 18:02 to 19:02 UTC). The live theme's "updated" time (19:02:55 UTC) matches one of those product saves to the second.
