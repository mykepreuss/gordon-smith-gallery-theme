#!/usr/bin/env python3
"""A read-only export of the Artists for Kids site, artistsforkids.sd44.ca
(proposals/artists-for-kids-integration.md, step 3). Nothing is submitted. The registration forms are
drawn by a script in the browser, so the export sees their pages without them.

  python3 inventory.py <folder>

Writes, in <folder>:
  pages/<path>.html   each page's content, cleaned to plain markup: headings, paragraphs, lists, tables,
                      bold, italic, links, pictures, embedded videos. Menus, breadcrumbs, slider and
                      accordion controls are left out. Links and picture addresses are made absolute.
  pages.json          for each page: address, title, headings, links, pictures, videos, whether it has a form
  assets.json         every picture, PDF and video, with the pages that use it, and each file's size

The site runs on the district's Terminalfour system; a page's content is its `.inner__content` (the home
page has none, so its `main` is used).
"""
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup, Comment, NavigableString

SITE = "https://artistsforkids.sd44.ca/"
AGENT = "Mozilla/5.0 (Gordon Smith Gallery site move, read-only)"
KEEP = {"h1", "h2", "h3", "h4", "h5", "p", "ul", "ol", "li", "table", "thead", "tbody", "tr", "th", "td",
        "strong", "em", "a", "img", "iframe", "figure", "figcaption", "blockquote", "br"}
RENAME = {"b": "strong", "i": "em"}
DROP = {"script", "style", "noscript", "button", "nav", "aside", "form", "input", "select", "textarea", "svg"}
CONTROLS = {"Previous Slide", "Next Slide", "Expand All", "Collapse All", "Expand section menu", "In This Section"}
FILES = re.compile(r"\.(pdf|docx?|xlsx?|pptx?|jpe?g|png|gif|webp|zip|mp4)(\?|$)", re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read().decode("utf-8", "replace")


def head_size(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            n = r.headers.get("Content-Length")
            return r.status, int(n) if n else None
    except Exception as e:  # noqa: BLE001 - reported, not fatal
        return str(e)[:80], None


def absolute(base, href):
    return urllib.parse.urljoin(base, href.strip()) if href else ""


def clean(node, base):
    """Plain markup from a content node: allowed tags only, no classes or styles."""
    for c in node.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    for tag in node.find_all(DROP):
        tag.decompose()
    for tag in [t for t in node.find_all(True) if t.get_text(" ", strip=True) in CONTROLS]:
        if not tag.decomposed and not tag.find(["img", "iframe"]):
            tag.decompose()
    for tag in list(node.find_all(True)):
        name = RENAME.get(tag.name, tag.name)
        if name not in KEEP:
            tag.unwrap()
            continue
        tag.name = name
        attrs = {}
        if name == "a" and tag.get("href"):
            attrs["href"] = absolute(base, tag["href"])
        elif name == "img":
            attrs["src"] = absolute(base, tag.get("src") or tag.get("data-src") or "")
            attrs["alt"] = (tag.get("alt") or "").strip()
        elif name == "iframe":
            attrs["src"] = absolute(base, tag.get("src") or tag.get("data-src") or "")
        elif name in ("td", "th"):
            for k in ("colspan", "rowspan"):
                if tag.get(k):
                    attrs[k] = tag[k]
        tag.attrs = attrs
    # Empty paragraphs and list items (the old editor leaves many).
    for tag in node.find_all(["p", "li", "strong", "em", "h2", "h3", "h4"]):
        if tag.decomposed:
            continue
        if not tag.get_text(strip=True).replace("​", "") and not tag.find(["img", "iframe"]):
            tag.decompose()
    html = node.decode_contents()
    html = html.replace("​", "").replace("\xa0", " ")
    html = re.sub(r"\n\s*\n+", "\n", html)
    return html.strip()


def content_node(soup):
    return soup.select_one(".inner__content") or soup.find("main") or soup.body


def crawl(folder):
    pages_dir = folder / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    queue, seen, pages, assets = [SITE], {SITE}, {}, {}
    while queue:
        url = queue.pop(0)
        try:
            status, html = fetch(url)
        except Exception as e:  # noqa: BLE001
            pages[url] = {"error": str(e)[:200]}
            continue
        soup = BeautifulSoup(html, "html.parser")
        title = (soup.title.string or "").replace(" | North Vancouver School District", "").strip() if soup.title else ""
        for a in soup.find_all("a", href=True):
            h = absolute(url, a["href"]).split("#")[0]
            if h.startswith(SITE) and h not in seen and not FILES.search(h) and "/search" not in h \
                    and "/media/" not in h and not h.endswith("gordonsmithgallery.com"):
                seen.add(h)
                queue.append(h)
        node = content_node(soup)
        has_form = bool(node.find("form")) or bool(node.find("input"))
        form_fields = [(lab.get_text(" ", strip=True)) for lab in node.find_all("label")]
        body = clean(node, url)
        path = urllib.parse.urlparse(url).path.strip("/") or "home"
        (pages_dir / (path.replace("/", "__") + ".html")).write_text(body)
        frag = BeautifulSoup(body, "html.parser")
        links = [{"text": a.get_text(" ", strip=True), "href": a["href"]} for a in frag.find_all("a", href=True)]
        images = [{"src": i["src"], "alt": i.get("alt", "")} for i in frag.find_all("img")]
        videos = [i["src"] for i in frag.find_all("iframe")]
        pages[url] = {"status": status, "title": title, "path": path,
                      "headings": [f"{h.name}: {h.get_text(' ', strip=True)}" for h in frag.find_all(["h1", "h2", "h3", "h4"])],
                      "links": links, "images": images, "videos": videos,
                      "form": has_form, "form_fields": form_fields}
        for i in images:
            assets.setdefault(i["src"], {"kind": "image", "alt": i["alt"], "pages": []})["pages"].append(path)
        for v in videos:
            assets.setdefault(v.split("?")[0], {"kind": "video", "pages": []})["pages"].append(path)
        for link in links:
            if re.search(r"\.pdf(\?|$)", link["href"], re.I):
                assets.setdefault(link["href"], {"kind": "pdf", "text": link["text"], "pages": []})["pages"].append(path)
        time.sleep(0.3)
    for url, a in assets.items():
        if a["kind"] != "video":
            a["status"], a["bytes"] = head_size(url)
    (folder / "pages.json").write_text(json.dumps(pages, indent=1, ensure_ascii=False))
    (folder / "assets.json").write_text(json.dumps(assets, indent=1, ensure_ascii=False))
    kinds = {}
    for a in assets.values():
        kinds[a["kind"]] = kinds.get(a["kind"], 0) + 1
    forms = sum(1 for p in pages.values() if p.get("form"))
    print(f"{len(pages)} pages ({forms} with a form), assets: {kinds}")


if __name__ == "__main__":
    crawl(pathlib.Path(sys.argv[1]))
