# Mailchimp integration audit (ACCESS-01)

Status: **partial**. Storefront evidence gathered 2026-09-25 from the public page source of https://gordonsmithgallery.com/. Theme settings (app embeds) are checked from the pulled theme in `theme/config/settings_data.json` once the baseline pull lands. Mailchimp account settings (audience, consent, double opt-in) need Mailchimp access and are **blocked** until the gallery provides it or confirms them.

## What the storefront loads today

| Mechanism | Evidence in the page source | Implication |
| --- | --- | --- |
| **Storefront ScriptTag** | `asyncLoad` injects `https://chimpstatic.com/mcjs-connected/js/users/9d362fac2ec011c28a53ad33c/0e4fb2f239b3e69534cf37505.js?shop=ed35ee-ea.myshopify.com` | Mailchimp's "connected site" script (site tracking and any Mailchimp pop-up forms) arrives through a ScriptTag. Shopify stops creating or updating storefront ScriptTags on 2026-10-01 and stops injecting existing ones on 2027-03-01 ([Shopify ScriptTag timeline](https://shopify.dev/docs/apps/build/online-store/script-tag-deprecation/storefront)). Anything that depends on this script stops working then unless Mailchimp moves it to an app embed. |
| Web pixel | `webPixelsConfigList` entry with `mailchimp_store_id`, `mailchimp_user_id` and `mailchimp_list_id` (audience `702493bf65`) | The Mailchimp for Shopify app is installed and connected to one audience. Pixels are for analytics and marketing events, not signup forms. |
| Theme app embed or app block | None found in the rendered home page | Confirm in `settings_data.json` after the pull. |
| Email signup form | None rendered. The footer's newsletter area shows only Shopify's "Follow on Shop" button; the plan's discovery found the footer newsletter section disabled | There is currently no visible signup anywhere on the site. |

## Options for ACCESS-01, in order of preference

1. **Native Shopify newsletter form** (theme `customer` form with marketing consent) in the reusable newsletter band (DESIGN.md §6.9, §6.12), with the Mailchimp for Shopify app syncing subscribed customers to audience `702493bf65`. No new app, no ScriptTag, works in every theme. Needs: confirmation that the app's customer sync is on and maps consent correctly, and the gallery's consent wording.
2. **Mailchimp app embed or app block**, if the installed app version offers one. Enabled per theme, so it must be checked on the review theme and again after publishing (plan, "Discovery snapshot and preflight").
3. **Link to a Mailchimp hosted signup page** supplied by the gallery. The fallback the plan names if neither of the above can be verified.

Do not build on the ScriptTag script (plan: "Do not build a new signup around ScriptTags").

## Still to verify

- [ ] `theme/config/settings_data.json`: app embeds present and enabled (after the pull).
- [ ] Mailchimp for Shopify app settings: customer sync on, audience, consent mapping, double opt-in.
- [ ] Whether any Mailchimp pop-up form is active through the ScriptTag today (if yes, it disappears on 2027-03-01).
- [ ] Test signup to an approved test address reaches the audience with correct consent (plan verification rules).
