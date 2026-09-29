# The old Smith Foundation site's addresses (smithfoundation.co)

Status: **Made 2026-09-29. Not uploaded. It waits for release.** Where each address goes is decided (P-63, Michael, 2026-09-29).

Michael, 2026-09-29: "This is 404s but is technically still up and was not correctly 301 redirected to our new site, the them we're working on in this project. Please create a 301 redirect file I can upload to our server for when we get the new site live to properly redirect."

## Summary

- **The file to upload:** `smithfoundation.co.htaccess`. Its rules go at the top of the `.htaccess` file in the old server's main folder.
- **What it does:** sends 174 old addresses to their new pages on gordonsmithgallery.com with permanent (301) redirects. Anything else goes to the new home page.
- **Don't upload it before release.** 29 of the 51 new pages are exhibition pages, which answer 404 on the live site until the new theme is published.
- **One setting outside the file has to change too:** the domain's forwarding, at GoDaddy. Today about half of all visits never reach the old server ("What is wrong today").
- **Tested** on Apache on this Mac: 2,309 requests, all answered as they should. Every new page answers on the review theme.

## What is wrong today

Checked 2026-09-29.

| What | Found |
| --- | --- |
| The domain has two addresses | `smithfoundation.co` points at two servers at once: `192.124.249.10` (GoDaddy's website firewall, in front of the WordPress server) and `3.33.251.168` (GoDaddy's domain forwarding). A browser picks either one |
| The forwarding | Sends the home page to `https://gordonsmithgallery.com` and answers 404 for every other address |
| The WordPress server | Still runs. 40 of its 44 pages were made private in August 2026, the home page among them, so they answer 404. The 35 exhibition and fundraiser pages and the 14 events still show, on the old design |
| `www.smithfoundation.co` | Has no address at all, so it doesn't open |
| The server | Apache with cPanel, so it reads an `.htaccess` file |

So the same old link gives the old page on one visit and an error on the next. No old address reaches its new page.

## The files

| File | What it is |
| --- | --- |
| `redirects.csv` | The list: each old address, its new address, the old page's WordPress number, what it was, and a note. Edited by hand. It is the record |
| `smithfoundation.co.htaccess` | The file for the server, made from the list. Not edited by hand |
| `redirects.py` | Makes the file and runs the checks |

## Where the old addresses come from

| Source | Addresses |
| --- | --- |
| The WordPress export (2026-09-28): 44 pages, 35 exhibitions and fundraisers, 14 events, and the earlier addresses WordPress kept for 5 of them | 100 |
| The Internet Archive's record of the site since 2017: pages since renamed or removed (`/curate/`, `/tickets/`, `/winter-appeal/`), lists (`/events/`, `/portfolio_category/past/`, `/product/`) and the sitemap | 40 |
| Documents (PDF) that have a page to go to: 32 from the media library, 2 more from the Internet Archive | 34 |

## How each address was matched

- **A page goes to the page that holds its content now.** Most of the Foundation's text moved (`proposals/smith-foundation-site.md`).
- **An exhibition goes to its own page.** Six had old addresses from the WordPress theme's sample content: `/exhibitions-items/clean-water/` is *Robert Davidson: Progression of Form*.
- **A fundraiser's photo page** (the luncheons, the galas) goes to Brilliance Gala, which holds them under "Past galas".
- **A past event goes to its programme's page**, or to its exhibition. The new site's own event pages start at release and hold other events (`proposals/store-changes.md` §8e).
- **Anything under a listed address goes where that address goes.** `/about/supporters/attachment/a-photo/` goes to Supporters.
- **The last slash, capital letters and anything after a "?" don't matter.** `/Visit`, `/visit/` and `/visit/?utm_source=news` all go to Plan your visit.
- **WordPress's numbered addresses** (`/?p=126`) go where their page goes.
- **Anything else** goes to the new home page: slides, author pages, feeds, photo pages, and the media library's pictures.

The choices, decided by Michael on 2026-09-29 (P-63): "Those choices are approved, mark P-63 as decided except "Pictures in the media library" redirect to the homepage".

| Old | Goes to | Why |
| --- | --- | --- |
| Job postings and calls: Work With Us, Curatorial Fellowship, Request for Proposals | Contact | The new site has no jobs page, and dated calls stay behind. Contact is where to ask |
| The old shop and its 12 products (catalogues, cards, a tote bag) | Shop | The gallery hasn't said if it still sells them (`gallery-questions.md` 8.7). The Shop sells the limited editions |
| About, the empty page over the old About section | The Smith Foundation | The old site was the Foundation's |
| Fund, Support Us, Friends of the Gallery, the appeals | Donate | Donate is the Support section's main page |
| Old forms: volunteer applications, scholarship forms from closed rounds | Volunteer, Scholarships | The page says what applies now |
| Year in Review reports, 2019 to 2025 | The Smith Foundation | Only the newest shows, from that page's button (P-47) |
| Pictures and other files in the media library | The new home page | Proposed: still served while they are on the old server. Michael decided otherwise ("Files") |
| Supporters | Supporters | **If Supporters is held back at release** (`store-changes.md` §8c), change its row to `/pages/the-smith-foundation`, then `write` and `test`. Change it back when the page goes live |

## Files

- **Documents with a page to go to** go to that page. There are 34, all in the list.
- **Pictures, videos and the other 7 documents** go to the new home page, whether or not the file is still on the server (P-63).
- **What that changes elsewhere:** a picture from the old site that an old email or another website shows stops showing there. The new site uses none of them: its pictures are in the store's Files ("Checks").
- **The media library can be deleted** from the server at any time. Nothing reads it once the rules are in.

## What the file leaves alone

| What | Why |
| --- | --- |
| WordPress's sign-in and admin (`/wp-login.php`, `/wp-admin/`) | So staff can still sign in to the old site. Its media library lists the files but shows no pictures, since their addresses redirect. Three lines in the file, marked, to delete when WordPress is removed |
| `/.well-known/` | The host's checks that renew the security certificate. Without the certificate, no `https://` address redirects |
| `/robots.txt` | The server has none once WordPress no longer answers, which tells search engines they may read every address. That is how they find the redirects |
| Any other website in the same hosting account | The rules apply to `smithfoundation.co` and `www.smithfoundation.co` only |

## On release day

After the new theme is published and the release scripts have run (`proposals/store-changes.md`).

1. **Check the new pages.** All 51 must answer:

   ```bash
   python3 proposals/foundation-redirects/redirects.py targets https://gordonsmithgallery.com
   ```

   If Supporters is held back, change its row first (above). For any other page that fails, fix the row, then `write` and `test`.
2. **Keep a copy of the server's `.htaccess`.** In cPanel's File Manager, turn on "Show hidden files" in Settings, open `public_html`, and download `.htaccess`.
3. **Add the file's rules.** Edit the server's `.htaccess` and paste everything in `smithfoundation.co.htaccess` at the very top, above what is there. Leave the rest: the host keeps its PHP settings in that file, and WordPress its own rules. Those rules no longer run for visitors, since ours answer first. If the server has no `.htaccess`, upload the file and rename it `.htaccess`.
4. **Clear the firewall's cache** (GoDaddy Website Security, Firewall, Clear cache). It keeps copies of pages, so the old answers can show for a while otherwise.
5. **Check the server**, asking it directly:

   ```bash
   python3 proposals/foundation-redirects/redirects.py live --ip 192.124.249.10
   ```

6. **Turn off the domain's forwarding.** At GoDaddy: the domain `smithfoundation.co`, DNS, Forwarding, delete. That removes `3.33.251.168`, so every visit reaches the server. Optional: add `www` as a CNAME to `smithfoundation.co`, so old links with `www` work too. The firewall has to know the `www` name for that.
7. **Check the domain** as visitors reach it. DNS changes take up to an hour:

   ```bash
   python3 proposals/foundation-redirects/redirects.py live
   ```

8. **Tell Google**, if the old domain is in Search Console: Settings, Change of address, to gordonsmithgallery.com.

## After release

- **Keep the hosting and the domain.** The redirects work only while the server answers and the domain points at it. Search engines need about a year to move everything over. Links on other sites need them for as long as the links exist.
- **WordPress can be deleted** once nobody needs it. The rules work alone, as the only thing in `.htaccess`. Delete the three marked lines in them then.
- **If the hosting is to end**, the redirects can move to Shopify: `smithfoundation.co` becomes a domain of the store, and the list becomes URL redirects there. The list would need a second form, since Shopify matches exact addresses only.

## Undo

Put the copy of the old `.htaccess` back, or delete our rules from the top of the file, and clear the firewall's cache. Browsers remember a permanent redirect, so a visitor who followed one may keep being sent on for a while.

## Checks

```bash
python3 proposals/foundation-redirects/redirects.py write
python3 proposals/foundation-redirects/redirects.py test
python3 proposals/foundation-redirects/redirects.py targets https://ed35ee-ea.myshopify.com --theme 184767250729
```

| Check | Result, 2026-09-29 |
| --- | --- |
| `test`: Apache 2.4.67 on this Mac, with the file at the top of its `.htaccess` and WordPress's rules under it. Every listed address, as written, without its last slash, in capitals, with a query, with a page under it, by its WordPress number, and as `www`. A picture that is still on the server, and one that is gone. Then what must be left alone | 2,309 of 2,309 |
| `targets`, the review theme | 51 of 51 new pages answer |
| `targets`, the live site | 22 of 51. The 29 exhibition pages answer 404 until release, which is why the file waits |
| Files and links on the old domain in the new site: 54 pages read on the review theme (the 50 new pages in the list and four more), and the repo searched | None |

`live` has not run: nothing is uploaded.
