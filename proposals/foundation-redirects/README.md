# The old Smith Foundation site's addresses (smithfoundation.co)

Status: **Made 2026-09-29. Not uploaded. It waits for release.** Where each address goes is decided (P-63, Michael, 2026-09-29).

Michael, 2026-09-29: "This is 404s but is technically still up and was not correctly 301 redirected to our new site, the them we're working on in this project. Please create a 301 redirect file I can upload to our server for when we get the new site live to properly redirect."

## Summary

- **The file to upload:** `smithfoundation.co.htaccess`. On the old server it is named `.htaccess` and sits in the website's main folder.
- **It needs nothing else on the server.** WordPress comes down at release (Michael, 2026-09-29: "The entire wordpress site will be coming down and not exist"). Every old address, WordPress's own included, then leads to the new site.
- **The hosting account and the domain stay** (Michael, 2026-09-29: "The hosting account is staying, only WordPress is going"). The old server reads the file each time someone asks for an old address, so they stay for as long as the redirects are wanted ("After release").
- **What it does:** sends 174 old addresses to their new pages on gordonsmithgallery.com with permanent (301) redirects. Anything else goes to the new home page.
- **Don't upload it before release.** 29 of the 51 new pages are exhibition pages, which answer 404 on the live site until the new theme is published.
- **One setting outside the file has to change too:** the domain's forwarding, at GoDaddy. Today about half of all visits never reach the old server ("What is wrong today").
- **Tested** on Apache on this Mac, as the only file on the server and beside WordPress: 4,628 requests, all answered as they should. Every new page answers on the review theme.

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
| Old addresses of documents (PDF) whose content has a page on the new site: 32 from the media library, 2 more from the Internet Archive | 34 |

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

## The old site's files

None of them has to stay on the old server. Each rule answers for an address, whether or not a file is behind it.

| Old addresses | Go to, on the new site |
| --- | --- |
| 14 scholarship forms (PDF) | Scholarships |
| 8 volunteer application forms (PDF) | Volunteer |
| 6 Year in Review reports (PDF) | The Smith Foundation |
| 3 from past fundraisers (PDF): the 2019 auction catalogue, two for To Gordon With Love | Brilliance Gala |
| The *Unfixed* book and the *Endless Summer* booklet (PDF) | Their exhibitions' pages, which hold them |
| The Music at the Smith rack card (PDF) | Music at the Smith |
| Every picture and video, and the other 7 documents | The new home page (P-63) |

**What that changes elsewhere:** a picture from the old site that an old email or another website shows stops showing there. The new site uses none of them: its pictures are in the store's Files ("Checks").

## What the file leaves alone

| What | Why |
| --- | --- |
| `/.well-known/` | The host's checks that renew the security certificate. Without the certificate, no `https://` address redirects |
| `/robots.txt` | The server has none once WordPress is gone, which tells search engines they may read every address. That is how they find the redirects |
| Any other website in the same hosting account | The rules apply to `smithfoundation.co` and `www.smithfoundation.co` only |

## On release day

After the new theme is published and the release scripts have run (`proposals/store-changes.md`).

1. **Check the new pages.** All 51 must answer:

   ```bash
   python3 proposals/foundation-redirects/redirects.py targets https://gordonsmithgallery.com
   ```

   If Supporters is held back, change its row first (above). For any other page that fails, fix the row, then `write` and `test`.
2. **Take WordPress down.** Keep a copy of what the Foundation wants to keep first. The export and the media library were saved on 2026-09-28 (`proposals/smith-foundation-site.md`, "Sources"). Then delete WordPress's files from `public_html` in cPanel's File Manager, its `.htaccess` among them ("Show hidden files" in Settings shows it).
3. **Put the file in.** Upload `smithfoundation.co.htaccess` to `public_html` and rename it `.htaccess`. It can be the only file there. It also works before WordPress is deleted: its rules then go at the very top of the `.htaccess` that is there, and WordPress's sign-in stops opening, since every address redirects.
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

- **The hosting account and the domain stay** (Michael, 2026-09-29). The redirects work only while the server answers and the domain points at it. The account can be the host's smallest: it holds one file. Search engines need about a year to move everything over. Links on other sites need the redirects for as long as the links exist.
- **The firewall** (GoDaddy Website Security) can stay or go. If it goes, the domain's address changes from the firewall's to the server's own, at GoDaddy.
- **If the hosting account ever ends**, this file has nowhere to run. The redirects then move to Shopify: `smithfoundation.co` becomes a domain of the store, and the list becomes URL redirects there. Shopify matches exact addresses only, so the list needs a second form, and an address not in it shows the new site's "page not found" instead of the home page.

## Undo

Delete the file from the server, or put back what was there, and clear the firewall's cache. Browsers remember a permanent redirect, so a visitor who followed one may keep being sent on for a while.

## Checks

```bash
python3 proposals/foundation-redirects/redirects.py write
python3 proposals/foundation-redirects/redirects.py test
python3 proposals/foundation-redirects/redirects.py targets https://ed35ee-ea.myshopify.com --theme 184767250729
```

| Check | Result, 2026-09-29 |
| --- | --- |
| `test`: Apache 2.4.67 on this Mac, twice. Once with the file alone on the server, WordPress deleted. Once with WordPress's files there and its rules under ours. Every listed address, as written, without its last slash, in capitals, with a query, with a page under it, by its WordPress number, and as `www`. WordPress's own addresses, a picture and an address that never existed. Then what must be left alone | 4,628 of 4,628 |
| `targets`, the review theme | 51 of 51 new pages answer |
| `targets`, the live site | 22 of 51. The 29 exhibition pages answer 404 until release, which is why the file waits |
| Files and links on the old domain in the new site: 54 pages read on the review theme (the 50 new pages in the list and four more), and the repo searched | None |

`live` has not run: nothing is uploaded.
