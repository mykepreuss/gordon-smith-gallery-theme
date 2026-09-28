# Store settings review

Read 2026-09-28 through the Shopify connector (Admin API), the Shopify admin's Settings pages with Michael signed in, and the public site. Nothing was changed. Every fix below is a store write, so each waits for Michael's go-ahead and a before-snapshot, and is logged in `proposals/store-writes/README.md` (`AGENTS.md`). Most of these settings affect the live site today, whichever theme is published.

## 1. Fix first: these affect buyers today

| # | Found | Why it matters | Proposed fix |
| --- | --- | --- | --- |
| 1 | Two prints can't be shipped. Anna Binta Diallo, *Red Feather* and Sandeep Johal, *I am easy to find* sit in a custom shipping profile, "2024 Fall Portfolio (Unframed Prints)", which has no zones and no rates | A buyer who wants either print shipped gets no shipping option. Pickup is the only choice | **Done 2026-09-28:** both are in the general profile. The custom profile stays, empty |
| 2 | Two prints are set as not needing shipping: Anna Binta Diallo, *Prairie Girl* ($450) and Elizabeth McIntosh, *Diamonds* ($3,200) | Checkout treats them like a digital product: no shipping address, no $20 charge, no pickup choice. The gallery gets an order with no delivery method | **Done 2026-09-28:** both are physical products |
| 3 | Checkout requires "Address line 2 (apartment, unit)" | Anyone in a house has to type something in the apartment field to pay | **Done 2026-09-28** by Michael in the admin: Optional |
| 4 | The checkout's "Email me with news and offers" box is preselected in all regions | Canada's anti-spam law (CASL) asks for consent the buyer gives themselves; a box ticked for them generally doesn't count. Mailchimp then adds these buyers as subscribers | **Done 2026-09-28** by Michael in the admin: set to Automated, which preselects in the United States only. The gallery's own counsel decides what the law requires |
| 5 | The store has one user, the owner login (`afkinfo@sd44.ca`), with no secure sign-in method required | A shared password with no second step is the store's weakest point: it guards payouts, customer data and the theme | Turn on two-step sign-in for the owner. Give each staff member their own user |

## 2. Decide: shipping, tax and policies

| # | Found | Why it matters | Options |
| --- | --- | --- | --- |
| 6 | All 17 frames are set to not charge tax. All 21 prints charge tax | Frames are normally taxable in BC (GST and PST). This may be a mistake or a decision by the District's finance team | Ask finance. If it's a mistake, turn "Charge tax" on for the frames |
| 7 | Canada is the only market, but the general shipping profile has a US zone and an International zone (26 countries). The US zone carries what look like Shopify's starter rates: free over $100, then $7.90 to $34.90 by weight. International uses Canada Post's calculated rates | As far as I can tell these zones never apply, since only Canada can check out. But if anyone adds a market, a $3,200 print ships to the US free. The admin reports 610 international visitors in the last 30 days | Canada only: delete both zones. Selling abroad: a project of its own (market, weights, customs codes, real rates, duties) |
| 8 | 37 of 38 variants weigh 0 kg. No variant has a country of origin or customs code | No effect on the flat $20 rate. Calculated or weight-based rates would come out wrong | Only needed if item 7 goes the "selling abroad" way |
| 9 | Nothing in the shipping settings keeps a frame to pickup only. The shipping policy says framed prints are pickup only | The flat $20 rate applies to any order. Whether a framed order can ship depends on what the theme offers | Gallery decides. A pickup-only profile for the frames would enforce it |
| 10 | No terms of service. The privacy policy refers to "our Terms of Service" | The checkout footer links the policies that exist; this one is missing | Gallery or District supplies the text |
| 11 | Hours disagree: the pickup instructions say Monday to Friday, 8:30 AM to 4:00 PM; the contact policy says 8:30am to 4:30pm, closed July and August | A buyer picking up reads one or the other | Gallery confirms (add to `gallery-questions.md`) |
| 12 | The shipping policy says shipping is $20, and also that "shipping will be calculated and confirmed with you at the time of the order" | Two answers to one question | Gallery's wording; ask with item 11 |

## 3. Apps and integrations

| # | Found | Proposed |
| --- | --- | --- |
| 13 | "Shopify ChatGPT MCP App" is installed with write access to nearly everything (products, orders, customers, themes, checkout) | Uninstall it if nobody uses it |
| 14 | Mailchimp: the permission update is still waiting, and site tracking still runs on the ScriptTag that stops on 2027-03-01 | Already recorded in `baseline/mailchimp-audit.md`; Michael's decision before release |
| 15 | Search & Discovery, Order Printer, the Claude connector and the CLI connector | Expected. No change |
| 16 | No Shopify Functions, no checkout rules, no webhooks of concern, one pixel (Mailchimp) | Nothing to do. There is no Google Analytics; Shopify's own analytics is the only traffic record |

## 4. For release

| # | Found | Proposed |
| --- | --- | --- |
| 17 | An existing redirect sends `/pages/who-we-are` to `/pages/our-story`. At release Our Story is hidden and redirected to `/pages/artists-for-kids` (`store-changes.md` §5) | Add to `release.py addresses`: point `/pages/who-we-are` straight at `/pages/artists-for-kids`, so it isn't a chain of two |
| 18 | Every product's first image has no alt text | Check that the new theme builds alt text from the label fields on every product image; if not, fill them in |

## 5. Housekeeping

| # | Found | Proposed |
| --- | --- | --- |
| 19 | Five old unpublished themes (four Dawn copies and Studio), last touched July to September | Delete after release. Keep Colorblock for rollback |
| 20 | Three development themes besides the main one (`programs-switcher`, `event-list-limit`, `exhibition-lesson-list-limit`) | From other sessions today. They expire on their own |
| 21 | Discount codes RACHEL10 (used once, its limit) and CORPORATE30-SNOW (30% off, unused, no end date) are both active | Deactivate RACHEL10. Give the other an end date or deactivate it once used |
| 22 | "Artists for Kids Warehouse" is an active location with no stock that doesn't fulfil online orders | Deactivate it if the gallery doesn't use it |
| 23 | The customer accounts and order status pages are at `shopify.com/89595805993/account` | Optional: move to `account.gordonsmithgallery.com`. Needs a DNS record |
| 24 | `gordonsmithgallery.com` has no SPF or DMARC record. It sends no email; the store sends from `sd44.ca`, which is authenticated and has DMARC set to reject | Optional, for whoever manages the DNS: `v=spf1 -all` and a DMARC reject record, so nobody can send as the gallery's domain |
| 25 | Staff order emails go to one address, `afkinfo@sd44.ca`. Customers are told to write to `artistsforkids@sd44.ca` | Fine if both are read. Add a second recipient if one person covers orders |
| 26 | No product has a SKU. Jack Shadbolt, *Toward a White Garden* has no product type (already in `baseline/store-manifest.md`) | Optional |

## 6. Checked and fine

- Domain: `gordonsmithgallery.com` is primary; `www`, `http` and the `myshopify.com` address all redirect to it. SSL on, HSTS on.
- Store details: address, phone, CAD, Pacific time, metric. Legal business: North Vancouver School District, non-profit. No admin alerts.
- Taxes: collecting in Canada (GST and BC PST), prices shown before tax, tax on shipping worked out automatically.
- Payments: Shopify Payments active, payouts to the bank account on file, 0% chargebacks. Shop Pay, Apple Pay and Google Pay on. PayPal off.
- Checkout: guest checkout allowed, no tipping, add-to-cart limit on. Abandoned checkout emails go after 10 hours to anyone who leaves a checkout, not only subscribers; the gallery may want "Email subscribers" instead, for the same reason as item 4.
- Customer accounts: the new version, optional, sign-in links shown.
- Privacy: privacy policy published; cookie banner not required for Canada and set to automatic; data sharing opt-out page active for Canada and eight US states.
- Email: sender domain authenticated.
- Shipping in Canada: flat $20, all provinces and territories. Pickup in store on; local delivery off.
- Inventory: tracked on every variant, and nothing can be oversold.
- Plan: Basic, billed yearly. Nothing found that needs a higher plan.
- Themes: live `183162372393` is MAIN, review `184767250729` is UNPUBLISHED, as `AGENTS.md` says.

## 7. Not read

- Online Store, Preferences (home page title, password, spam protection). The page didn't load for reading. Spam protection was checked earlier today (P-59).
- Payment capture method, gift card expiry, and the notification templates' wording.
- The connector can't read script tags, gift card settings or Shopify Payments details; the admin pages covered what mattered.
