#!/usr/bin/env python3
"""Check the links between the site's pages, as a visitor, a search engine and an AI agent find them.

Starts at the home page and follows every link to a page of the site, then reads the store's
sitemap, and checks that (DESIGN.md §10, proposals/internal-linking-review.md):

  1. every link leads to a page that answers, and no page shows a Liquid error;
  2. every link in a page's content has words: its text, its label, or its picture's alt text;
  3. every page a search engine may list is within a few clicks of the home page;
  4. every address in the sitemap that a search engine may list is linked from some page
     (a page nobody links to either gets a link or asks not to be listed, DS-182);
  5. every entry's page (an exhibition, an artist, a work, a lesson, an edition) is linked from
     another page's content, not only from the menu.

It also reports, without failing: links that are sent on to another address, and pages with few
links in from other pages' content.

A link's place is read from the page: the menu and the footer are the header and footer section
groups, and the content is everything in <main>. links.json holds the limits and the addresses
that stay unlinked until release, each with its reason.

Standard library only. Read only: plain GET requests.
Usage:
  python3 design-system/scripts/check_links.py BASE [--theme ID] [--sitemap URL] [--json report.json]
BASE is the site's address without a path: the theme dev address (http://127.0.0.1:9292), or the
store's with --theme for an unpublished theme, as check_answers.py reads one. The sitemap is the
store's own (it lists the same addresses for every theme); --sitemap none leaves rule 4 out.
Exit code 1 when a rule fails.
"""
import argparse
import http.cookiejar
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser

SPEC = pathlib.Path(__file__).resolve().parent / "links.json"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
# Shopify adds these to addresses as it goes; they don't name another page.
DROP_PARAMS = {"preview_theme_id", "_pos", "_sid", "_ss", "_psq", "_fid", "pb", "variant"}
# Not pages to read: the cart, accounts, checkout, files and Shopify's own services.
SKIP_PREFIX = ("/cart", "/account", "/checkout", "/cdn/", "/services/", "/apps/", "/tools/",
               "/customer_authentication", "/challenge")
FILES = re.compile(r"\.(pdf|jpe?g|png|gif|webp|svg|mp4|zip|atom|xml|txt|md|json)$", re.I)

# Cookies are kept between pages: a preview of an unpublished theme is held in one.
OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


class Page(HTMLParser):
    """A page's links, each with its words and its place, and what the page says of itself."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, classes, id) of the open elements
        self.links = []
        self.link = None
        self.title = ""
        self.robots = ""
        self.canonical = ""
        self._in_title = False

    def place(self):
        """content, menu or footer: by the section the element is in, else by its landmark."""
        for tag, classes, ident in reversed(self.stack):
            if ident.startswith("shopify-section-"):
                if ident.startswith("shopify-section-template--"):
                    return "content"
                if ident.endswith("__header") or "header" in ident.rsplit("__", 1)[-1]:
                    return "menu"
                return "footer"
        tags = [tag for tag, _, _ in self.stack]
        if "main" in tags:
            return "content"
        if "footer" in tags:
            return "footer"
        if "header" in tags or "nav" in tags:
            return "menu"
        return "other"

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and (a.get("name") or "").lower() == "robots":
            self.robots = (self.robots + "," + (a.get("content") or "")).strip(",")
        if tag == "link" and (a.get("rel") or "") == "canonical":
            self.canonical = a.get("href") or ""
        if tag == "img" and self.link is not None:
            self.link["alt"].append(a.get("alt") or "")
        if tag in VOID:
            return
        if tag == "title" and not self.title:
            self._in_title = True
        if tag == "a" and a.get("href") is not None:
            self.link = {"href": a.get("href"), "text": [], "alt": [], "label": a.get("aria-label") or "",
                         "place": self.place()}
        self.stack.append((tag, (a.get("class") or "").split(), a.get("id") or ""))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag == "title":
            self._in_title = False
        if tag == "a" and self.link is not None:
            text = re.sub(r"\s+", " ", "".join(self.link["text"])).strip()
            alt = " ".join(x.strip() for x in self.link["alt"] if x.strip())
            self.link["words"] = text or self.link["label"].strip() or alt
            del self.link["text"], self.link["alt"], self.link["label"]
            self.links.append(self.link)
            self.link = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self.link is not None:
            self.link["text"].append(data)


def normalise(href, base, hosts):
    """Returns (kind, address): internal with the site's path, external, or other (mail, #)."""
    href = (href or "").strip()
    if not href or href.startswith(("#", "javascript:", "mailto:", "tel:", "sms:")):
        return "other", href
    joined = urllib.parse.urljoin(base, href)
    parts = urllib.parse.urlsplit(joined)
    if parts.scheme not in ("http", "https"):
        return "other", href
    if parts.netloc.lower() not in hosts:
        return "external", joined
    query = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True) if k not in DROP_PARAMS]
    path = parts.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")
    return "internal", path + ("?" + urllib.parse.urlencode(query) if query else "")


def is_page(address):
    """Whether an address is a page to read, not a file, the cart or a search."""
    path = address.split("?", 1)[0]
    if path.startswith(SKIP_PREFIX) or FILES.search(path):
        return False
    return not (path == "/search" and "?" in address)


def kind(address):
    """The kind of page, from its address: home, pages, pages/artists, products, collections."""
    path = address.split("?", 1)[0]
    parts = path.strip("/").split("/")
    if path == "/":
        return "home"
    if parts[0] == "pages" and len(parts) > 2:
        return "pages/" + parts[1]
    return parts[0]


def read_page(address, html, base, hosts):
    """A page's record from its HTML."""
    page = Page()
    page.feed(html)
    links = []
    for link in page.links:
        where, to = normalise(link["href"], base + address, hosts)
        links.append({"to": to, "kind": where, "place": link["place"], "words": link["words"]})
    return {
        "title": re.sub(r"\s+", " ", page.title).strip(),
        "listed": "noindex" not in page.robots.lower(),
        "canonical": page.canonical,
        "liquid_error": "Liquid error" in html,
        "links": links,
    }


def depths(out, start="/"):
    """Clicks from the start to each address, by the shortest way."""
    found = {start: 0}
    queue = deque([start])
    while queue:
        here = queue.popleft()
        for there in out.get(here, ()):
            if there not in found:
                found[there] = found[here] + 1
                queue.append(there)
    return found


def graph(pages):
    """Who links to whom: every link, and the links in pages' content only."""
    out, into, into_content = defaultdict(set), defaultdict(set), defaultdict(set)
    for address, page in pages.items():
        if page.get("unlinked"):
            continue
        for link in page.get("links", []):
            if link["kind"] != "internal" or link["to"] == address:
                continue
            out[address].add(link["to"])
            into[link["to"]].add(address)
            if link["place"] == "content":
                into_content[link["to"]].add(address)
    return out, into, into_content


def findings(pages, sitemap, spec):
    """Returns (errors, notes), each a list of (rule, address, message)."""
    errors, notes = [], []
    out, into, into_content = graph(pages)
    crawled = {a: p for a, p in pages.items() if not p.get("unlinked")}

    for address, page in sorted(crawled.items()):
        if page["status"] != 200:
            sources = sorted(into[address])
            errors.append(("answers", address, f"answers {page['status'] or 'nothing'}; linked from "
                           f"{len(sources)} page(s), such as {', '.join(sources[:3])}"))
            continue
        if page.get("moved"):
            sources = sorted(into[address])
            notes.append(("moved", address, f"is sent on to {page['moved']}; linked from {len(sources)} page(s), "
                          f"such as {', '.join(sources[:3])}"))
        if page.get("liquid_error"):
            errors.append(("liquid", address, "shows a Liquid error"))
        if "?" in address:
            continue
        wordless = [l["to"] for l in page.get("links", []) if l["place"] == "content" and l["kind"] != "other" and not l["words"]]
        for to in sorted(set(wordless)):
            errors.append(("words", address, f"a link to {to} has no words"))

    found = depths(out)
    for address, page in sorted(crawled.items()):
        if page["status"] != 200 or "?" in address or not page.get("listed"):
            continue
        clicks = found.get(address)
        if clicks is not None and clicks > spec["max_depth"]:
            errors.append(("depth", address, f"is {clicks} clicks from the home page; the most is {spec['max_depth']}"))

    known = {row["address"]: row["why"] for row in spec.get("unlinked", [])}
    linked = {a.split("?", 1)[0] for a in crawled}
    for address in sorted(sitemap):
        if address in linked or not is_page(address):
            continue
        page = pages.get(address)
        if page is None or page["status"] != 200 or not page.get("listed", True):
            continue
        if address in known:
            notes.append(("unlinked", address, f"no page links to it, until release: {known[address]}"))
        else:
            errors.append(("unlinked", address, "is in the sitemap and may be listed, but no page links to it"))

    entries = tuple(spec.get("entries", []))
    few = Counter()
    for address, page in sorted(crawled.items()):
        if page["status"] != 200 or "?" in address or not page.get("listed") or address == "/":
            continue
        count = len(into_content[address])
        if count < spec["min_content_links"]:
            few[kind(address)] += 1
        if count == 0 and kind(address) in entries:
            errors.append(("content", address, "no page's content links to it"))
    for name, count in sorted(few.items()):
        notes.append(("few", name, f"{count} page(s) with fewer than {spec['min_content_links']} links in from other pages' content"))
    return errors, notes


def fetch(url, tries=5):
    """Returns (status, final address, body). Waits and tries again when the store says to."""
    wait = 2
    for attempt in range(tries):
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (links check; read only)"})
        try:
            with OPENER.open(request, timeout=60) as response:
                return response.status, response.geturl(), response.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 430, 502, 503, 504) and attempt < tries - 1:
                time.sleep(wait)
                wait *= 2
                continue
            return exc.code, exc.geturl(), ""
        except (OSError, urllib.error.URLError):
            if attempt < tries - 1:
                time.sleep(wait)
                wait *= 2
                continue
    return 0, url, ""


def theme_shown(page):
    found = re.search(r'Shopify\.theme = \{[^}]*"id":(\d+)', page)
    return found.group(1) if found else ""


def read(address, base, hosts):
    status, final, body = fetch(base + address)
    record = {"status": status, "links": [], "listed": True}
    where, final_address = normalise(final, base, hosts)
    if status == 200 and where == "internal" and final_address.split("?", 1)[0] != address.split("?", 1)[0]:
        record["moved"] = final_address
    if status == 200 and "<html" in body[:2000].lower():
        record.update(read_page(address, body, base, hosts))
    return address, record


def read_sitemap(url):
    """Every page address the store's sitemap names, as paths."""
    status, _, body = fetch(url)
    if status != 200:
        return None
    addresses = set()
    for part in re.findall(r"<loc>(.*?)</loc>", body):
        part = part.replace("&amp;", "&")
        if "<sitemapindex" in body:
            status, _, inner = fetch(part)
            for found in re.findall(r"<url>\s*<loc>(.*?)</loc>", inner if status == 200 else ""):
                addresses.add(urllib.parse.urlsplit(found.replace("&amp;", "&")).path or "/")
        else:
            addresses.add(urllib.parse.urlsplit(part).path or "/")
    return {a.rstrip("/") or "/" for a in addresses}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("base")
    parser.add_argument("--theme", help="read the pages as this theme shows them (a theme id)")
    parser.add_argument("--sitemap", help="the sitemap's address; 'none' leaves it out. Default: the store's own")
    parser.add_argument("--json", help="write the report here")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--limit", type=int, default=6000, help="the most pages to read")
    args = parser.parse_args(argv)
    base = args.base.rstrip("/")
    spec = json.loads(SPEC.read_text())
    hosts = {urllib.parse.urlsplit(base).netloc.lower(), *spec["hosts"]}

    if args.theme:
        status, _, body = fetch(f"{base}/?preview_theme_id={args.theme}")
        if theme_shown(body) != args.theme:
            print(f"ERROR   asked for theme {args.theme}, the store showed {theme_shown(body) or 'no theme id'}")
            return 1
        print(f"Reading theme {args.theme}")

    pages, queue, seen = {}, ["/"], {"/"}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        while queue and len(pages) < args.limit:
            batch, queue = queue[:40], queue[40:]
            for address, record in pool.map(lambda a: read(a, base, hosts), batch):
                pages[address] = record
                for link in record["links"]:
                    if link["kind"] == "internal" and is_page(link["to"]) and link["to"] not in seen:
                        seen.add(link["to"])
                        queue.append(link["to"])
        if queue:
            print(f"NOTE    stopped at {len(pages)} pages; {len(queue)} not read")

        sitemap = set()
        if args.sitemap != "none":
            sitemap = read_sitemap(args.sitemap or spec["sitemap"])
            if sitemap is None:
                print("NOTE    the sitemap didn't load, so rule 4 is left out")
                sitemap = set()
            linked = {a.split("?", 1)[0] for a in pages}
            missing = sorted(a for a in sitemap if a not in linked and is_page(a))
            for address, record in pool.map(lambda a: read(a, base, hosts), missing):
                record["unlinked"] = True
                pages[address] = record

    errors, notes = findings(pages, sitemap, spec)
    crawled = [a for a, p in pages.items() if not p.get("unlinked")]
    kinds = Counter(kind(a) for a in crawled if "?" not in a)
    print(f"{len(crawled)} pages read: " + ", ".join(f"{n} {k}" for k, n in sorted(kinds.items())))
    out, _, _ = graph(pages)
    found = depths(out)
    clicks = Counter(found[a] for a in crawled if "?" not in a and a in found)
    print("Clicks from home: " + ", ".join(f"{n} page(s) at {c}" for c, n in sorted(clicks.items())))
    for rule, address, message in notes:
        print(f"NOTE    {rule:9} {address} {message}")
    for rule, address, message in errors:
        print(f"ERROR   {rule:9} {address} {message}")
    if args.json:
        report = {"pages": len(crawled), "kinds": kinds, "clicks": clicks,
                  "errors": [dict(zip(("rule", "address", "message"), e)) for e in errors],
                  "notes": [dict(zip(("rule", "address", "message"), n)) for n in notes]}
        pathlib.Path(args.json).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"\n{len(errors)} error(s), {len(notes)} note(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
