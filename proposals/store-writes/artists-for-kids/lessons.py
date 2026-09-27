#!/usr/bin/env python3
"""The ArtReach videos as lessons (P-36, DS-70), read from the export of the old site's ArtReach Videos
page (inventory.py). Each lesson there is a bold title, a YouTube player, then "We're making",
"We're inspired by", "Suggested grade levels" and "We're wondering" with a list of questions. The text
moves as written; only the labels go, because the lesson page prints them.

  python3 lessons.py parse <export folder>          the lessons as JSON, to check
  python3 lessons.py youtube <export folder>        each video's owner, title and upload date (read-only),
                                                    and its thumbnail, saved as the lesson's cover

The first player on the old page has no title: it is the clay kit's video, which the page shows again
under its own title ("AFK Clay Kit: Ancient and Future Fossils"), so it is left out (27 lessons). Some
lessons have their labelled parts in the player's paragraph, others in the paragraph after it; both
are read the same way.

"AFK" in a lesson's title is written out as "Artists for Kids" (P-39). Body text keeps it until the
gallery approves each change.
"""
import html
import json
import pathlib
import re
import sys
import urllib.request

from bs4 import BeautifulSoup, NavigableString

AGENT = "Mozilla/5.0 (Gordon Smith Gallery site move, read-only)"
LABELS = {
    "we're making": "making",
    "we’re making": "making",
    "we're inspired by": "inspired_by",
    "we’re inspired by": "inspired_by",
    "suggested grade levels": "grades",
    "we're wondering": "wondering",
    "we’re wondering": "wondering",
}


def video_id(src):
    m = re.search(r"/embed/([^?&/#]+)", src)
    return m.group(1) if m else None


def handle(title):
    t = title.lower().replace("&", "and")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t


def public_title(title):
    return re.sub(r"\bAFK\b", "Artists for Kids", title)


def inline_html(nodes):
    """Text and italics from a run of nodes, as simple HTML (only <em> kept)."""
    out = []
    for n in nodes:
        if isinstance(n, NavigableString):
            out.append(html.escape(str(n), quote=False))
        elif n.name == "em":
            inner = n.get_text()
            if inner.strip():
                out.append(f"<em>{html.escape(inner, quote=False)}</em>")
            else:
                out.append(html.escape(inner, quote=False))
        elif n.name == "br":
            out.append("\n")
        else:
            out.append(inline_html(n.contents))
    return "".join(out)


def is_title(node):
    """A paragraph that is only bold text, with no player in it."""
    if getattr(node, "name", None) != "p" or node.find("iframe"):
        return False
    strong = node.find("strong")
    return bool(strong) and node.get_text(" ", strip=True) == strong.get_text(" ", strip=True) \
        and strong.get_text(" ", strip=True).rstrip(":").strip().lower() not in LABELS


def parse(folder):
    """The lessons in page order. A lesson is everything from its title to the next title: the player
    (in the title's next paragraph, alone or followed by the labelled parts), the labelled parts, and
    the list of questions."""
    page = (pathlib.Path(folder) / "pages" / "learn__artreach-videos.html").read_text()
    soup = BeautifulSoup(page, "html.parser")
    blocks = [b for b in soup.children if not isinstance(b, NavigableString)]
    groups, current = [], None
    for b in blocks:
        if is_title(b):
            current = {"title": b.get_text(" ", strip=True), "nodes": []}
            groups.append(current)
        elif current is not None:
            current["nodes"].append(b)
    lessons = []
    for g in groups:
        frame = None
        inline, questions = [], []
        for b in g["nodes"]:
            if b.name == "ul":
                questions += [li.get_text(" ", strip=True) for li in b.find_all("li")]
                continue
            if b.name == "iframe":
                frame = frame or b
                continue
            if b.name == "p":
                for n in b.contents:
                    if getattr(n, "name", None) == "iframe":
                        frame = frame or n
                        continue
                    inline.append(n)
                inline.append(BeautifulSoup("<br/>", "html.parser").br)
        if frame is None:
            continue
        fields, label, run = {}, None, []
        for n in inline:
            if getattr(n, "name", None) == "strong":
                text = n.get_text(" ", strip=True).rstrip(":").strip().lower()
                if text in LABELS:
                    if label:
                        fields[label] = inline_html(run)
                    label, run = LABELS[text], []
                    continue
            run.append(n)
        if label:
            fields[label] = inline_html(run)
        clean = {k: re.sub(r"\s+", " ", v).strip().strip(":").strip() for k, v in fields.items()}
        vid = video_id(frame["src"])
        title = public_title(g["title"])
        lessons.append({
            "handle": handle(title),
            "title": title,
            "old_title": g["title"],
            "video": f"https://www.youtube.com/watch?v={vid}",
            "video_id": vid,
            "making": clean.get("making", ""),
            "inspired_by": clean.get("inspired_by", ""),
            "grades": clean.get("grades", ""),
            "questions": [q for q in questions if q],
        })
    return lessons


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": AGENT, "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def youtube(folder):
    folder = pathlib.Path(folder)
    covers = folder / "covers"
    covers.mkdir(exist_ok=True)
    out = []
    for lesson in parse(folder):
        vid = lesson["video_id"]
        info = json.loads(fetch(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"))
        watch = fetch(f"https://www.youtube.com/watch?v={vid}").decode("utf-8", "replace")
        m = re.search(r'"uploadDate":"([0-9-]{10})', watch) or re.search(r'itemprop="uploadDate" content="([0-9-]{10})', watch) \
            or re.search(r'"publishDate":"([0-9-]{10})', watch)
        cover = covers / f"{lesson['handle']}.jpg"
        size = None
        for name in ("maxresdefault", "sddefault", "hqdefault"):
            try:
                data = fetch(f"https://i.ytimg.com/vi/{vid}/{name}.jpg")
            except Exception:  # noqa: BLE001 - try the next size
                continue
            cover.write_bytes(data)
            size = name
            break
        out.append({"handle": lesson["handle"], "video_id": vid, "author": info.get("author_name"),
                    "youtube_title": info.get("title"), "posted": m.group(1) if m else None, "cover": size})
        print(out[-1], flush=True)
    (folder / "youtube.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    step, folder = sys.argv[1], sys.argv[2]
    if step == "parse":
        print(json.dumps(parse(folder), indent=1, ensure_ascii=False))
    elif step == "youtube":
        youtube(folder)
