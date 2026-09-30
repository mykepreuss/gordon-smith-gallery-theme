# The old Smith Foundation site's addresses (smithfoundation.co)

Status: **On the old server since 2026-09-29, 5:02 PM Pacific, the day the new site went live.** Every old address redirects. Where each goes is decided (P-63, Michael, 2026-09-29). What is left is under "Still to do".

Michael, 2026-09-29: "This is 404s but is technically still up and was not correctly 301 redirected to our new site, the them we're working on in this project. Please create a 301 redirect file I can upload to our server for when we get the new site live to properly redirect."

## Summary

- **The file:** `smithfoundation.co.htaccess`. On the old server it is named `.htaccess` and sits in the website's main folder, `public_html`.
- **It needs nothing else on the server.** WordPress comes down at release (Michael, 2026-09-29: "The entire wordpress site will be coming down and not exist"). Every old address, WordPress's own included, then leads to the new site.
- **The hosting account and the domain stay** (Michael, 2026-09-29: "The hosting account is staying, only WordPress is going"). The old server reads the file each time someone asks for an old address, so they stay for as long as the redirects are wanted ("After release").
- **What it does:** sends 174 old addresses to their new pages on gordonsmithgallery.com with permanent (301) redirects. Anything else goes to the new home page.
- **It waited for release.** 29 of the 51 new pages are exhibition pages, which answered 404 on the live site until the new theme was published.
- **One setting outside the file changed too:** the domain's forwarding, at GoDaddy, which took about half of all visits ("What was wrong before").
- **Checked** on the real server: 175 of 175 old addresses redirect. Tested before that on Apache on this Mac, as the only file on the server and beside WordPress: 4,634 requests, all answered as they should.

## What was wrong before

Checked 2026-09-29, before the changes.

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
| `/.well-known/` | The host's checks that renew the security certificate: a check's file is served. Without the certificate, no `https://` address redirects |
| `/robots.txt` | A `robots.txt` put on the server would be served. There is none, so the server turns to its "not found" page, and that address goes to the new home page like any other. Search engines find no rules there, so they may read every address, which is how they find the redirects |
| Any other website in the same hosting account | The rules apply to `smithfoundation.co` and `www.smithfoundation.co` only |

## What was done, 2026-09-29

After the new theme went live (4:08 PM Pacific), with Michael's yes to each change ("1. Yes and delete the old one we don't need to keep it 2. Yes, proceed 3. Approved, proced"). Through his GoDaddy account in Chrome, where he had signed in.

| Time (Pacific) | What | Result |
| --- | --- | --- |
| Before | Every new page asked of the live site (`targets`) | 51 of 51 answer |
| Before | The server's `.htaccess` read and copied to `server/htaccess-before-2026-09-29.txt` | 42 lines, 1,287 bytes: WordPress's rules, an https rule, a cache plugin's block. The copy matches byte for byte |
| 5:02 PM | `smithfoundation.co.htaccess` uploaded to `public_html` as `.htaccess`, over the old one (cPanel, File Manager, Upload) | On the server: 31,753 bytes, the same as the file in Git, byte for byte. The old lines are not kept on the server, at Michael's word |
| 5:03 PM | The firewall's cache cleared (GoDaddy Website Security, Firewall, Clear Cache) | Cleared |
| 5:05 PM | Every old address asked of the server through the firewall (`live --ip 192.124.249.10`) | 175 of 175 |
| 5:06 PM | The domain's forwarding deleted (GoDaddy, the domain, DNS, Forwarding) | Deleted. **GoDaddy then reset the domain's addresses:** both A records became "Parked", `sucuriip` went, and `www` was added as a CNAME |
| 5:09 PM | The A record set back to the firewall, `192.124.249.10`, by Michael. The agent is not allowed to edit DNS records | Both of GoDaddy's name servers gave it by 5:10 PM |
| 5:12 PM | Every old address again, at the address the name servers give | 175 of 175 |

For about four minutes GoDaddy's name servers gave its parked page for the domain. Lookups kept elsewhere from before held the old addresses through it.

**If this is ever done again:** set the A record to the firewall's address first, then delete the forwarding, and look at the DNS records straight after. Deleting the forwarding resets them.

## What is there now

| What | Now |
| --- | --- |
| `smithfoundation.co` | One address, the firewall's (`192.124.249.10`), which passes each request to the server |
| Any old address | A permanent redirect to its new page, or to the new home page |
| `http://` addresses, and `http://www.` | Redirect the same way |
| `https://www.smithfoundation.co` | Does not open: the firewall's certificate names `smithfoundation.co` only. Old links didn't use `www`: the Internet Archive has 15 such addresses, all from the 2017 "coming soon" page |
| WordPress | Still on the server, and nothing reaches it, its sign-in included |
| The forwarding | Gone |

## Still to do

| What | Who |
| --- | --- |
| Delete WordPress's files from `public_html`, all but `.htaccess`, when the Foundation has what it wants from them. The export and the media library were saved on 2026-09-28 (`proposals/smith-foundation-site.md`, "Sources"). The account's disk is 82.73 GB of 95 GB full | Michael |
| Optional: `https://www.` addresses. The firewall needs the `www` name added so its certificate covers it | Michael |
| Optional: tell Google, if the old domain is in Search Console (Settings, Change of address, to gordonsmithgallery.com) | Michael |

## Keeping it working

- **The hosting account and the domain stay** (Michael, 2026-09-29). The redirects work only while the server answers and the domain points at it. The account can be the host's smallest: it holds one file. Search engines need about a year to move everything over. Links on other sites need the redirects for as long as the links exist.
- **The firewall** (GoDaddy Website Security) can stay or go. If it goes, the domain's A record changes from the firewall's address to the server's own, at GoDaddy.
- **To change where an address goes:** change its row in `redirects.csv`, run `write` and `test`, upload the file over the one on the server, clear the firewall's cache, and run `live`.
- **If the hosting account ever ends**, this file has nowhere to run. The redirects then move to Shopify: `smithfoundation.co` becomes a domain of the store, and the list becomes URL redirects there. Shopify matches exact addresses only, so the list needs a second form, and an address not in it shows the new site's "page not found" instead of the home page.

## Undo

Upload `server/htaccess-before-2026-09-29.txt` to `public_html` as `.htaccess` and clear the firewall's cache. WordPress then answers again, as long as its files are there. The forwarding can be added again at GoDaddy; it changes the DNS records too. Browsers remember a permanent redirect, so a visitor who followed one may keep being sent on for a while.

## Checks

```bash
python3 proposals/foundation-redirects/redirects.py write
python3 proposals/foundation-redirects/redirects.py test
python3 proposals/foundation-redirects/redirects.py targets https://gordonsmithgallery.com
python3 proposals/foundation-redirects/redirects.py live
```

| Check | Result, 2026-09-29 |
| --- | --- |
| `test`: Apache 2.4.67 on this Mac, twice. Once with the file alone on the server, WordPress deleted. Once with WordPress's files there and its rules under ours. Every listed address, as written, without its last slash, in capitals, with a query, with a page under it, by its WordPress number, and as `www`. WordPress's own addresses, a picture and an address that never existed. Then what must be left alone. The test's server turns to a "not found" page as the real one does | 4,634 of 4,634 |
| `targets`, the review theme, before release | 51 of 51 new pages answer |
| `targets`, the live site, before release | 22 of 51. The 29 exhibition pages answered 404 until release, which is why the file waited |
| `targets`, the live site, after release | 51 of 51 |
| `live --ip 192.124.249.10`, the real server through the firewall, after the upload and again after the DNS change | 175 of 175, both times |
| By hand on the real server: a picture, a listed PDF, WordPress's sign-in and admin, a numbered address, a query, capitals, a feed, plain `http`, `http://www.` | Each redirects as it should. One followed to its end lands on its exhibition's page with 200, after one redirect |
| The file on the server against the file in Git (SHA-256) | The same: `03654f86...202c46` |
| Files and links on the old domain in the new site: 54 pages read on the review theme (the 50 new pages in the list and four more), and the repo searched | None |

`live` without `--ip` asks by this computer's own lookup, which held the old addresses for up to an hour after the change. The name servers and four public resolvers gave the firewall's address by 5:12 PM.
