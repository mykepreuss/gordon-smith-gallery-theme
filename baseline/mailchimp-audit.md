# Mailchimp integration audit (ACCESS-01)

Status: **settings checked; the end-to-end test is still to do**. Storefront evidence gathered 2026-09-25 from the public page source of https://gordonsmithgallery.com/. Theme settings were checked in the pulled baseline theme on 2026-09-25: no app embeds, no app blocks. The Mailchimp account and the app's connection settings were read on 2026-09-28 with Michael signed in (below). Nothing was changed in Mailchimp or Shopify.

## What the storefront loads today

| Mechanism | Evidence in the page source | Implication |
| --- | --- | --- |
| **Storefront ScriptTag** | `asyncLoad` injects `https://chimpstatic.com/mcjs-connected/js/users/9d362fac2ec011c28a53ad33c/0e4fb2f239b3e69534cf37505.js?shop=ed35ee-ea.myshopify.com` | Mailchimp's "connected site" script (site tracking and any Mailchimp pop-up forms) arrives through a ScriptTag. Shopify stops creating or updating storefront ScriptTags on 2026-10-01 and stops injecting existing ones on 2027-03-01 ([Shopify ScriptTag timeline](https://shopify.dev/docs/apps/build/online-store/script-tag-deprecation/storefront)). Anything that depends on this script stops working then unless Mailchimp moves it to an app embed. |
| Web pixel | `webPixelsConfigList` entry with `mailchimp_store_id`, `mailchimp_user_id` and `mailchimp_list_id` (audience `702493bf65`) | The Mailchimp for Shopify app is installed and connected to one audience. Pixels are for analytics and marketing events, not signup forms. |
| Theme app embed or app block | None found in the rendered home page | Confirmed in the pulled theme: no app embeds in `config/settings_data.json`, no app blocks in any template or section group, no Mailchimp reference in any theme file. |
| Email signup form | None rendered. The footer's newsletter area shows only Shopify's "Follow on Shop" button; the plan's discovery found the footer newsletter section disabled | There is currently no visible signup anywhere on the site. |

## Mailchimp settings (read 2026-09-28)

Read in the Mailchimp account (Audience settings, Forms settings, Integrations, Shopify) and in Shopify admin (Settings, Apps, Mailchimp). Nothing was changed.

| Setting | Found | What it means for the sign-up form |
| --- | --- | --- |
| Audience `702493bf65` | "Gordon Smith Gallery Newsletter and Events", the main list: 5,174 contacts, 2,171 email subscribers. The account has 12 audiences | The pixel and the Shopify connection both point at the right list |
| Shopify connection | Connected since 2024-10-02, synced to that audience | Sign-ups reach Mailchimp through the app, as P-18 assumes |
| Double opt-in | Off in the Shopify connection, and the audience is set to single opt-in | No confirmation email. The form's message "You're signed up for the newsletter." is right as it stands |
| Sync new non-subscribed contacts | Off | Only customers who agreed to email marketing are added, as subscribers. Customers who didn't agree stay out of Mailchimp |
| Sync Shopify customer tags | On, all tags | The `newsletter` tag should arrive in Mailchimp, so the gallery can pick out website sign-ups. Confirm in the test |
| Sync new subscribers to Shopify | Off | People who join through Mailchimp's own forms don't become Shopify customers. No effect on our form |
| Customer event syncing | On | Analytics only |
| Pop-up forms | 0 active, on the Shopify store and on a disconnected `www.sd44.ca` connection | Nothing the gallery uses stops working when the ScriptTag stops on 2027-03-01 |
| Site tracking | Active on `https://gordonsmithgallery.com`. Mailchimp shows a notice: "Enable the Mailchimp app embed", because the pixel it needs for site tracking and pop-up analytics isn't on | Tracking runs on the connected-site script from the ScriptTag, which loads with any theme until 2027-03-01. After that it needs the app embed (open item 2) |
| GDPR fields and reCAPTCHA on Mailchimp's own forms | Both off | Mailchimp's own forms have no bot check (open item 3) |
| App in Shopify admin | Opening it shows an "Update" screen asking for new permissions. Theme extensions: "0 active, available for Online Store" | See open item 1. Option 2 above (an app embed) now exists |

### Open from this check

1. **The app's permission update.** Mailchimp asks for a new set of permissions, and the app's screens in Shopify admin don't open until someone approves it. Compared with what it has now, the request narrows most access: customers from view and edit to view, orders from all history to the last 60 days, Online Store from view and edit to view, discounts dropped. It adds edit access to marketing events. Syncing sign-ups needs only view access to customers. Not approved: it changes an installed app on the live store, so it's Michael's call and would be logged in `proposals/store-writes/README.md`.
2. **Site tracking after 2027-03-01.** To keep it, turn on the Mailchimp app embed in the new theme (a theme setting, per theme, so it would be a new theme change and a decision). Without it, site tracking and pop-up analytics stop; the sign-up form isn't affected.
3. **Automated sign-ups.** The newest contacts in the audience include a run of generated-looking addresses (common first and last names with numbers, repeated across providers). Some arrived through "Mailchimp for Shopify" (78 contacts in the audience came from that source), so bots already reach the store's customer form even though the live theme shows no sign-up. The new form puts one on every page. Checked 2026-09-28: Shopify's spam protection (Online Store, Preferences) is already on for contact and comment forms, which include the newsletter form, and for login, create account and password recovery; nothing was changed (P-59). The automated sign-ups came in with it on, since hCaptcha challenges only traffic it finds suspicious. If more arrive after release, look up a few under Customers in Shopify to see how they came in. The gallery decides whether to clean up these contacts (`proposals/gallery-questions.md` 1.8).

## Options for ACCESS-01, in order of preference

1. **Native Shopify newsletter form** (theme `customer` form with marketing consent) in the reusable newsletter band (DESIGN.md §6.9, §6.12), with the Mailchimp for Shopify app syncing subscribed customers to audience `702493bf65`. No new app, no ScriptTag, works in every theme. Needs: confirmation that the app's customer sync is on and maps consent correctly, and the gallery's consent wording.
2. **Mailchimp app embed or app block**, if the installed app version offers one. Enabled per theme, so it must be checked on the review theme and again after publishing (plan, "Discovery snapshot and preflight").
3. **Link to a Mailchimp hosted signup page** supplied by the gallery. The fallback the plan names if neither of the above can be verified.

Do not build on the ScriptTag script (plan: "Do not build a new signup around ScriptTags").

## Still to verify

- [x] `baseline/theme/config/settings_data.json` (then `theme/`): app embeds present and enabled. Result: none (checked 2026-09-25 in the baseline pull).
- [x] Mailchimp for Shopify app settings: customer sync on, audience, consent mapping, double opt-in. Result: synced to audience `702493bf65`, only subscribed customers, tags synced, single opt-in (checked 2026-09-28, above).
- [x] Whether any Mailchimp pop-up form is active through the ScriptTag today (if yes, it disappears on 2027-03-01). Result: none active (checked 2026-09-28).
- [ ] Test signup to an approved test address reaches the audience with correct consent (plan verification rules).
