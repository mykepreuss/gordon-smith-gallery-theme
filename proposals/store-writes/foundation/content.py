#!/usr/bin/env python3
"""The Smith Foundation's old site, into the store (proposals/smith-foundation-site.md; P-41 to P-49,
DS-138, decided by Michael 2026-09-28). What goes where; load.py and the connector payloads below
write it.

  python3 content.py check                 every entry's fields and every page's text, for reading
  python3 content.py sheet                 the review sheet, foundation-sheet.md, beside this file

Text is the old site's, taken from its WordPress export by post and block number (source.py), so
nothing is typed again (AGENTS.md, "Gallery-facing work"). What changed, and why:

- Headings and labels the old site wrote in capitals are in sentence or title case ("NORTH
  VANCOUVER" is "North Vancouver"); paragraphs its page builder styled as headings are paragraphs.
- Curator lines taken from a sentence ("… was guest-curated by Robin Laurence") read as the site's
  other curator lines do: "Guest-curated by Robin Laurence" (gallery-questions.md 4.7).
- Summaries are the text's first sentence or two, and the text carries on after them, as the
  migration's were; nothing is repeated.
- Dated calls to action stay behind (P-45): RSVP links, ticket prices, "PLEASE MARK YOUR
  CALENDARS!", "Applications are closed", "Reception to follow". Past events stay as history.
- "AFK" in titles, labels and headings is written out (P-39): Transformations' subtitle.
- Titles follow each text's own spelling where the old title and text differ (Robert Young's
  "Spatial Understanding", "Thirteen Ways to Summon Ghosts"; 4.6), and Victor John Penner's
  February 29, 2014, which didn't exist, is February 28 until the gallery says.
- Three older exhibitions have no picture on the old site (Alistair Bell's, Work Is Art, Robert
  Young's): their key image is a work of theirs from the collection, as an artwork, with its
  caption from the collection's record. Dwelling's picture is Christopher Pratt's print, which the
  collection holds: its image and record are used, and it is the exhibition's work from the
  collection.
- Links get their plain address (a tracking parameter comes off the CBC link).
- A few words are ours, where a page needs to say what it is: the Artists for Kids awards page's
  line pointing to the Foundation's scholarships, the headings of the gala page's sections, the
  figures' captions naming a photographer the old text names. The gallery checks them (8.10 to 8.12).
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import files  # noqa: E402
import source  # noqa: E402

CREATED = HERE.parent / "created"
SITE = "https://gordonsmithgallery.com"
BRIDGE_TEMPLATE = "current-on-now-exhibition"  # P-35: the live theme shows a bare title

_POSTS = None


def posts():
    global _POSTS
    if _POSTS is None:
        _POSTS = source.load()
    return _POSTS


def block(pid, n):
    return source.blocks(posts()[pid]["content"])[n][1]


def txt(pid, n):
    return source.plain(block(pid, n))


def strip_marks(nodes):
    """Nodes without bold: the old page builder bolded whole paragraphs and labels."""
    out = []
    for nd in nodes:
        nd = dict(nd)
        nd.pop("bold", None)
        if nd["type"] == "link":
            nd["children"] = strip_marks(nd["children"])
        out.append(nd)
    return out


def split(nodes, sentences):
    """The first n sentences, and the rest, keeping italics and links."""
    whole = source.plain(nodes)
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z“\"(])", whole)
    head = " ".join(parts[:sentences])
    cut, first, rest = len(head), [], []
    for nd in nodes:
        size = len(nd["value"]) if nd["type"] == "text" else len(source.plain(nd["children"]))
        if cut <= 0:
            rest.append(nd)
        elif size <= cut:
            first.append(nd)
            cut -= size
        elif nd["type"] == "text":
            a, b = dict(nd), dict(nd)
            a["value"], b["value"] = nd["value"][:cut].rstrip(), nd["value"][cut:].lstrip()
            first.append(a)
            if b["value"]:
                rest.append(b)
            cut = 0
        else:
            first.append(nd)
            cut = 0
    return first, rest


def drop_prefix(nodes, prefix):
    nodes = [dict(n) for n in nodes]
    assert nodes[0]["type"] == "text" and nodes[0]["value"].startswith(prefix), (prefix, nodes[0])
    nodes[0]["value"] = nodes[0]["value"][len(prefix):].lstrip()
    return nodes


def drop_suffix(nodes, suffix):
    """The nodes without their last words, which may span a link: a dated line at a paragraph's end."""
    whole = source.plain(nodes)
    assert whole.endswith(suffix), (suffix, whole[-80:])
    keep = len(whole) - len(suffix)
    out, count = [], 0
    for nd in nodes:
        size = len(nd["value"]) if nd["type"] == "text" else len(source.plain(nd["children"]))
        if count + size <= keep:
            out.append(dict(nd))
        elif nd["type"] == "text" and count < keep:
            out.append({**nd, "value": nd["value"][: keep - count]})
        count += size
    if out and out[-1]["type"] == "text":
        out[-1] = {**out[-1], "value": out[-1]["value"].rstrip()}
    return out


# Old links: the old site's own pages are gone, and Artists for Kids' pages moved onto this site (P-30).
LINKS = [
    (r"smithfoundation\.co/exhibitions-items/one-hundred-artists-deep", "/pages/exhibitions/one-hundred-artists-deep"),
    (r"sd44\.ca/school/artistsforkids/learn/paradisevalleysummervisualartscamps", "/pages/paradise-valley-summer-camp"),
    (r"sd44\.ca/school/artistsforkids/(Pages/default|About/Pages/Who-We-Are)\.aspx", "/pages/artists-for-kids"),
]
UNLINK = [r"smithfoundation\.co", r"eventbrite\.", r"list-manage\.com"]  # gone, or past sign-ups


def fix_links(nodes):
    """Old links pointed at their new pages, or unwrapped to their words; tracking parameters off."""
    out = []
    for nd in nodes:
        if nd["type"] != "link":
            out.append(dict(nd))
            continue
        url = nd["url"] or ""
        url = re.sub(r"[?&](fbclid|aff|ab_channel)=[^&#]*", "", url).replace("&amp;", "&")
        for pat, new in LINKS:
            if re.search(pat, url):
                url = new
                break
        else:
            if any(re.search(pat, url) for pat in UNLINK):
                out.extend(fix_links(nd["children"]))
                continue
        out.append({**nd, "url": url, "children": fix_links(nd["children"])})
    return out


def tidy(nodes):
    """One space between words where the old text put spaces inside its italics or links; no empty
    text; links fixed (fix_links); a space put back where the old text lost one."""
    nodes = fix_links(nodes)
    out = []
    for nd in nodes:
        nd = dict(nd)
        if nd["type"] == "link":
            kids = [dict(k) for k in nd["children"]]
            lead = kids and kids[0]["type"] == "text" and kids[0]["value"][:1] == " "
            trail = kids and kids[-1]["type"] == "text" and kids[-1]["value"][-1:] == " "
            if lead:
                kids[0]["value"] = kids[0]["value"].lstrip()
                if not (out and out[-1]["type"] == "text" and out[-1]["value"].endswith(" ")):
                    out.append({"type": "text", "value": " "})
            if trail:
                kids[-1]["value"] = kids[-1]["value"].rstrip()
            nd["children"] = [k for k in kids if k["type"] != "text" or k["value"]]
            out.append(nd)
            if trail:
                out.append({"type": "text", "value": " "})
            continue
        if nd["type"] == "text":
            nd["value"] = nd["value"].replace("Gallery.Hosted", "Gallery. Hosted")
            if out and out[-1]["type"] == "text" and out[-1]["value"].endswith(" "):
                nd["value"] = nd["value"].lstrip(" ")
            if not nd["value"]:
                continue
        out.append(nd)
    return out


def t(value, **marks):
    return {"type": "text", "value": value, **{k: True for k, v in marks.items() if v}}


# ---------------------------------------------------------------------------------------------------
# Rich text (exhibition fields) and page HTML (staged text)

def rp(nodes):
    return {"type": "paragraph", "children": tidy(nodes)}


def rh(level, nodes):
    return {"type": "heading", "level": level, "children": nodes if isinstance(nodes, list) else [t(nodes)]}


def rul(items):
    return {"type": "list", "listType": "unordered",
            "children": [{"type": "list-item", "children": i} for i in items]}


def rich(blocks):
    return json.dumps({"type": "root", "children": blocks}, ensure_ascii=False)


def hp(nodes):
    """A paragraph of page text: italics and links kept, the old page builder's bold dropped."""
    return f"<p>{source.to_html(tidy(strip_marks(nodes)))}</p>"


def hh(level, value):
    return f"<h{level}>{source.to_html(value) if isinstance(value, list) else html.escape(value, quote=False)}</h{level}>"


# ---------------------------------------------------------------------------------------------------
# Files: the uploaded pictures and PDFs (files.py), and works already in the collection

def created_files():
    path = CREATED / "foundation-files.json"
    return json.loads(path.read_text()) if path.exists() else {}


def img(key):
    """A picture's ID: an uploaded one (files.py key) or, with 'media:', one already in Files."""
    if key.startswith("media:"):
        return f"gid://shopify/MediaImage/{key[6:]}"
    f = created_files().get(f"img:{key}")
    return (f["id"] if isinstance(f, dict) else f) if f else f"(img:{key} not uploaded)"


def pdf_path(key):
    f = created_files().get(f"pdf:{key}")
    if not f or not isinstance(f, dict) or not f.get("url"):
        return f"(pdf:{key} not uploaded)"
    return "/cdn/shop/files/" + f["url"].split("/")[-1].split("?")[0]


def figure(key, caption=None):
    """A picture in page text, as the Artists for Kids pages' are: its Files address, size, alt text."""
    f = created_files().get(f"img:{key}")
    alt = files.alt(key)
    if not isinstance(f, dict) or not f.get("url"):
        return f'<figure><img src="(img:{key})" alt="{html.escape(alt)}"></figure>'
    url, w, h = f["url"], f["width"], f["height"]
    if w > 1440:
        h, w = round(h * 1440 / w), 1440
        url += ("&" if "?" in url else "?") + "width=1440"
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure><img src="{html.escape(url)}" alt="{html.escape(alt)}" width="{w}" height="{h}" loading="lazy">{cap}</figure>'


def vimeo(video_id, title, width, height, caption=None):
    """A Vimeo video in page text, as Gordon and Marion's is (DS-53): its own shape, no tracking."""
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure><iframe src="https://player.vimeo.com/video/{video_id}?dnt=1" title="{html.escape(title)}" '
            f'width="{width}" height="{height}" allow="fullscreen; picture-in-picture" loading="lazy"></iframe>{cap}</figure>')


# Works in the collection used as key images (their records' images and captions)
BELL_TALL_BIRD = "46348479070505"      # Alistair Bell, Tall Bird, 1961, Woodcut on Paper (bell002)
CHOW_FLUX = "46348482642217"           # Yung Wing Chow, Flux I, 2013, Screen Print on Canvas (chow001)
YOUNG_JAZZ_PLAYER = "46348537004329"   # Robert Young, The Jazz Player/ Sounds Inside, 1973, Screenprint (youn030)
PRATT_CHRISTMAS_EVE = "46348513313065"  # Christopher Pratt, Christmas Eve at 12 O'Clock, 1995, Lithograph on Paper (prat-c001)
PRATT_WORK = json.loads((CREATED / "collection-works.json").read_text())["prat-c001"]


def caption(artist, title, rest):
    return rich([rp([t(f"{artist}, "), t(title, italic=True)] + ([t(rest)] if rest else []))])


def names(text, lead=""):
    """A list of names from an 'including a, b and c' sentence part."""
    s = text[len(lead):] if lead and text.startswith(lead) else text
    s = re.sub(r"\s+(?:and|&)\s+(?=[^,]+$)", ", ", s.strip().rstrip("."))
    return [n.strip() for n in s.split(",") if n.strip()]


# ---------------------------------------------------------------------------------------------------
# Exhibitions, 2013 to 2019: 17 new entries (P-41)

def older_exhibitions():
    E = []

    def ex(handle, title, start, end, pid, n, sentences=1, **extra):
        head, rest = split(strip_marks(block(pid, n)), sentences)
        body = [rp(rest)] if rest else []
        body += extra.pop("more", [])
        E.append({"handle": handle, "title": title, "start_date": start, "end_date": end,
                  "summary": source.plain(head), "body": rich(body) if body else None, **extra})

    ex("collection-connection-and-the-making-of-meaning", "Collection, Connection and the Making of Meaning",
       "2013-05-13", "2013-09-14", "1216", 2, 1, curator_credit="Guest-curated by Robin Laurence",
       key_image=img("ex-collection-connection"))
    ex("expressionist-renderings-the-prints-of-alistair-bell", "Expressionist Renderings: The Prints of Alistair Bell",
       "2013-10-09", "2013-12-20", "1213", 2, 1, curator_credit="Guest-curated by Ian M. Thom", artists=["Alistair Bell"],
       key_image=img(f"media:{BELL_TALL_BIRD}"), key_image_is_artwork="true",
       key_image_caption=caption("Alistair Bell", "Tall Bird", ", 1961. Woodcut on Paper. Collection of Artists for Kids and the Gordon Smith Gallery."))
    ex("victor-john-penner-not-safe-to-occupy", "Victor John Penner: Not Safe to Occupy",
       "2014-01-15", "2014-02-28", "1210", 2, 1, curator_credit="Guest-curated by Michael Love", artists=["Victor John Penner"],
       key_image=img("ex-penner"), key_image_is_artwork="true",
       key_image_caption=rich([rp([t("Victor John Penner, "), t("Beds / Rooms #4317-36a", italic=True),
                                   t(txt("1210", 3).split("#4317-36a", 1)[1])])]))
    ex("gu-xiong-a-journey-exposed", "Gu Xiong: A Journey Exposed", "2014-05-07", "2014-08-23", "1206", 2, 2,
       curator_credit="Curated by Astrid Heyerdahl", artists=["Gu Xiong"], key_image=img("ex-gu-xiong"))
    work = txt("1194", 2)
    ex("work-is-art", "Work Is Art", "2014-09-10", "2014-10-15", "1194", 2, 1,
       curator_credit="Curated by Gordon Smith", artists=names(work.split(": ", 1)[1]),
       key_image=img(f"media:{CHOW_FLUX}"), key_image_is_artwork="true",
       key_image_caption=caption("Yung Wing Chow", "Flux I", ", 2013. Screen Print on Canvas. Collection of Artists for Kids and the Gordon Smith Gallery."))
    ex("robert-young-spatial-understanding", "Robert Young: Spatial Understanding", "2014-10-22", "2015-01-03", "1188", 2, 1,
       curator_credit="Curated by Astrid Heyerdahl", artists=["Robert Young"],
       key_image=img(f"media:{YOUNG_JAZZ_PLAYER}"), key_image_is_artwork="true",
       key_image_caption=caption("Robert Young", "The Jazz Player/ Sounds Inside", ", 1973. Screenprint. Collection of Artists for Kids and the Gordon Smith Gallery."))
    ex("figurative-contemplation", "Figurative Contemplation", "2014-10-22", "2015-05-02", "1191", 2, 1,
       curator_credit="Curated by Astrid Heyerdahl", key_image=img("ex-figurative"))
    ex("accidentally-on-purpose-ross-penhall", "Accidentally on Purpose: Ross Penhall", "2015-03-03", "2015-05-02", "1183", 2, 1,
       artists=["Ross Penhall"], key_image=img("ex-penhall"))
    ex("robert-davidson-progression-of-form", "Robert Davidson: Progression of Form", "2015-05-15", "2015-08-29", "441", 2, 1,
       curator_credit="Guest-curated by Ian M. Thom", artists=["Robert Davidson"], key_image=img("ex-davidson"))
    ex("phantoms-in-the-front-yard-over-the-counter-culture", "Phantoms in the Front Yard: Over the Counter Culture",
       "2015-10-01", "2015-12-18", "92", 2, 2,
       artists=["Michael Abraham", "Jeremiah Birnbaum", "Jay Senetchko", "Paul Morstad", "Bruce Pashak", "Jonathan Sutton",
                "Caroline Weaver", "James Knight"],
       key_image=img("ex-phantoms"), key_image_is_artwork="true",
       key_image_caption=rich([rp([t("Sleeping Modernist", italic=True),
                                   t(txt("92", 3).split("Sleeping Modernist", 1)[1])])]))
    ready = txt("94", 2)
    ex("readymades", "Readymades", "2016-05-05", "2016-08-26", "94", 2, 2, curator_credit="Curated by Bill Jeffries",
       artists=names(ready.split("chosen by Gordon Smith: ", 1)[1].split(". The exhibition")[0]),
       key_image=img("ex-readymades"), installation_views=[img("ex-readymades-view")])
    ash = txt("442", 2)
    ex("art-school-high", "Art School High", "2017-05-13", "2017-08-26", "442", 2, 1,
       curator_credit="Guest-curated by Patrik Andersson",
       artists=names(ash.split("Exhibiting artists were ", 1)[1].split(". Art School High")[0]),
       key_image=img("ex-art-school-high"))
    # Its first paragraph is one sentence: the summary. The other three are the text.
    ex("memory-history-story", "Memory, History, Story", "2017-09-29", "2018-04-07", "183", 2, 1,
       more=[rp(strip_marks(block("183", n))) for n in (3, 4, 5)], key_image=img("ex-memory-history-story"))
    ghosts = txt("443", 3)
    ex("thirteen-ways-to-summon-ghosts", "Thirteen Ways to Summon Ghosts", "2018-05-16", "2018-08-31", "443", 2, 1,
       more=[rp(strip_marks(block("443", 3)))], curator_credit="Guest-curated by Kimberly Phillips",
       artists=names(ghosts.split("features the work of ", 1)[1]),
       key_image=img("ex-ghosts"), key_image_caption=rich([rp([t(txt("443", 4))])]),
       installation_views=[img("ex-ghosts-2"), img("ex-ghosts-3"), img("ex-ghosts-4")],
       installation_credit=txt("443", 4))
    ex("transformations", "Transformations", "2018-09-28", "2019-04-13", "2539", 3, 1,
       subtitle="Selected works from the Artists for Kids Collection", key_image=img("ex-transformations"))
    ex("reframed-painting-and-collage-by-tiko-kerr", "Reframed: Painting and Collage by Tiko Kerr", "2019-05-08", "2019-08-30",
       "2591", 6, 1, more=[rp(strip_marks(block("2591", n))) for n in (7, 8, 9)]
       + [rh(2, "Public Programs"), rp(strip_marks(block("2591", 4))), rp(strip_marks(block("2591", 5)))],
       curator_credit="Curated by Meredith Preuss", artists=["Tiko Kerr"],
       key_image=img("ex-reframed"), key_image_is_artwork="true",
       key_image_caption=caption("Tiko Kerr", "Before the Inferno I Had a Light Heart", ""))
    ex("dwelling-people-and-place", "Dwelling: People and Place", "2019-09-27", "2020-04-16", "3245", 3, 1,
       key_image=img(f"media:{PRATT_CHRISTMAS_EVE}"), key_image_is_artwork="true",
       key_image_caption=caption("Christopher Pratt", "Christmas Eve at 12 O'Clock", ", 1995. Lithograph on Paper. Collection of Artists for Kids and the Gordon Smith Gallery."),
       collection_works=[PRATT_WORK])
    return E


# ---------------------------------------------------------------------------------------------------
# Exhibitions already in the store: what each gains. "append" adds to the entry's current text.

VIDEO = {  # the platforms' own titles, for the Videos and publications field
    "unfixed-talk": ("ARTIST TALK: Unfixed, The Entangled Works of Chris Curreri and Laurie Kang", "https://vimeo.com/540733448"),
    "unfixed-conversation": ("IN CONVERSATION: Unfixed, The Entangled Works of Chris Curreri and Laurie Kang", "https://vimeo.com/562546859"),
    "wcohatww-panel": ("Virtual Contributor Panel: We Can Only Hint at this with Words", "https://youtu.be/I6kppMVojnw"),
    "prevailing-unveiled": ("Art Education Unveiled: Perspectives from Prevailing Landscapes", "https://vimeo.com/945344575"),
    "playhouse-feature": ("Artist Feature: Guná Jensen discussing her painting \"Self Portrait\"", "https://youtu.be/pXIHQ2Kqkgc"),
    "playhouse-conversation": ("In Conversation: Artist Guná Jensen and Guest Curator Annie Canto", "https://youtu.be/duhCy3QJgI8"),
    "playhouse-extended": ("In Conversation (extended): Artist Guná Jensen and Guest Curator Annie Canto", "https://www.youtube.com/watch?v=nO27zYXNVwI"),
    "stitched-vocaleye": ("VocalEye Described Tour of Stitched", "https://www.youtube.com/watch?v=6vK-DuZvYa0"),
}


def media(*items):
    """The Videos and publications field: [(label, url)] as a list of links (DS-138). A link field
    needs a full address; the theme makes the site's own relative again (gs-url)."""
    return json.dumps([{"text": label, "url": SITE + url if url.startswith("/") else url} for label, url in items],
                      ensure_ascii=False)


def plain_heading(pid, n, drop=None):
    s = txt(pid, n)
    if drop:
        s = s.replace(drop, "").strip()
    return s


def existing_exhibitions():
    """handle: fields to set (P-41 to P-46). Fields not named stay as they are."""
    U = {}
    # Play: the paragraph as summary, the three questions as the text
    U["play"] = {"summary": txt("3356", 7),
                 "body": rich([rul([strip_marks(block("3356", n)) for n in (3, 4, 5)])])}
    # Unfixed
    head, rest = split(strip_marks(block("3352", 29)), 1)
    U["unfixed"] = {
        "subtitle": "The Entangled Works of Chris Curreri and Laurie Kang",
        "artists": json.dumps(["Laurie Kang", "Chris Curreri"]),
        "curator_credit": "Curated by Meredith Preuss",
        "summary": source.plain(head),
        "body": rich([rp(rest)] + [rp(strip_marks(block("3352", n))) for n in (30, 31, 32)]),
        "installation_views": json.dumps([img(f"unfixed-{n}") for n in range(1, 13)]),
        "installation_credit": txt("3352", 33),
        "media": media(VIDEO["unfixed-talk"], VIDEO["unfixed-conversation"],
                       ("Unfixed, The Entangled Works of Chris Curreri and Laurie Kang", pdf_path("unfixed-book"))),
    }
    # Beyond the Horizon (the later of its two versions, the archive item)
    head, rest = split(strip_marks(block("3885", 6)), 1)
    U["beyond-the-horizon"] = {
        "curator_credit": txt("3885", 4),
        "artists": json.dumps(names(txt("3885", 5), "Featuring works by ")),
        "summary": source.plain(head),
        "body": rich([rp(rest)]) if rest else None,
    }
    # We Can Only Hint at This with Words
    head, rest = split(strip_marks(block("3904", 8)), 2)
    U["we-can-only-hint-at-this-with-words"] = {
        "artists": json.dumps(["Russna Kaur", "M.E. Sparks", "Andrea Taylor"]),
        "curator_credit": txt("3904", 5),
        "summary": source.plain(head),
        "body": rich([rp(rest), rp(strip_marks(block("3904", 9))), rp(strip_marks(block("3904", 10))),
                      rh(2, "Artist Bios")] + [rp(strip_marks(block("3904", n))) for n in (12, 13, 14)]
                     + [rh(2, "Contributor Bios")] + [rp(strip_marks(block("3904", n))) for n in (16, 17, 18)]),
        "credits": rich([rp(strip_marks(block("3904", n))) for n in (20, 21, 22)]),
        "funder_logos": json.dumps([img("logo-parc"), img("logo-nvrc")]),
        "media": media(VIDEO["wcohatww-panel"], ("View the Zine", "https://issuu.com/smithfoundation/docs/issuu_file_final")),
    }
    # Paths
    head, rest = split(strip_marks(block("5109", 4)), 1)
    U["paths"] = {
        "curator_credit": txt("5109", 5),
        "summary": source.plain(head),
        "body": rich(([rp(rest)] if rest else []) + [rh(2, "Curator"), rp(strip_marks(block("5109", 6)))]),
    }
    # Endless Summer
    head, rest = split(strip_marks(block("4261", 3)), 1)
    programmes = []
    for title_n, text_n in ((16, 17), (18, 19), (20, 21)):
        programmes += [rh(3, strip_marks(block("4261", title_n))), rp(strip_marks(block("4261", text_n)))]
    U["endless-summer"] = {
        "artists": json.dumps(["Katie Kozak", "Lucien Durey"]),
        "curator_credit": "Curated by Jenn Jackson",
        "summary": source.plain(head),
        "body": rich([rp(rest), rp(strip_marks(block("4261", 4))), rp(strip_marks(block("4261", 5))),
                      rh(2, "Artists"), rp(strip_marks(block("4261", 11))), rp(strip_marks(block("4261", 12))),
                      rh(2, "Curator"), rp(strip_marks(block("4261", 14))),
                      rh(2, "Public Programs")] + programmes),
        "credits": rich([rp(strip_marks(block("4261", 22)))]),
        "funder_logos": json.dumps([img("logo-parc"), img("logo-mission-hill"), img("logo-nvrc-stacked"), img("logo-capture")]),
        "media": media(("Exhibition Booklet", pdf_path("endless-summer-booklet"))),
    }
    # Prevailing Landscapes: credits (none today), past programmes, the talk's video
    prog = []
    for title_n, text_ns in ((9, (10,)), (11, (12,)), (13, (14,)), (15, (16, 17))):
        prog.append(rh(3, [t(plain_heading("5026", title_n))]))
        for n in text_ns:
            nodes = strip_marks(block("5026", n))
            if n == 17:
                nodes = drop_suffix(nodes, "Reception to follow, supported by Polygon Homes.")
            prog.append(rp(nodes))
    U["prevailing-landscapes"] = {
        "append": [rh(2, "Public Programs")] + prog,
        "credits": rich([rp(strip_marks(block("5026", n))) for n in (19, 20, 21)]),
        "media": media(VIDEO["prevailing-unveiled"]),
    }
    # Playhouse: past programmes, the three videos
    U["playhouse"] = {
        "append": [rh(2, "Public Programs"),
                   rh(3, strip_marks(block("5293", 7))), rp(strip_marks(block("5293", 8))),
                   rh(3, strip_marks(block("5293", 9))), rp(strip_marks(block("5293", 10))),
                   rh(3, strip_marks(block("5293", 11))), rp(strip_marks(block("5293", 12))), rp(strip_marks(block("5293", 13)))],
        "media": media(VIDEO["playhouse-feature"], VIDEO["playhouse-conversation"], VIDEO["playhouse-extended"]),
    }
    # Stitched: past programmes, the described tour
    U["stitched"] = {
        "append": [rh(2, "Public Programs")]
        + [rp(drop_suffix(strip_marks(block("5432", n)), "RSVP")) for n in (5, 6, 7)]
        + [rp(strip_marks(block("5432", 8)))],
        "media": media(VIDEO["stitched-vocaleye"]),
    }
    return U


# ---------------------------------------------------------------------------------------------------
# Pages. Three new (P-42, made as P-35); staged text added to four (DS-39).

def scholarships_body():
    note = strip_marks(block("3386", 18))
    note = drop_prefix(note, "**")
    return "\n".join([
        hp(block("3386", 6)), hp(block("3386", 7)), hp(block("3386", 8)),
        hh(2, "North Vancouver"), hp(strip_marks(block("3386", 10))),
        hh(2, "West Vancouver"), hp(strip_marks(block("3386", 13))),
        hh(2, "Vancouver"), hp(strip_marks(block("3386", 16))),
        f'<p>{source.to_html(note)} <a href="/pages/awards-and-scholarships">{html.escape(txt("3386", 19))}</a></p>',
    ])


def gala_body():
    """Two pictures to a gala at most (a video counts as one), so the pictures beside each gala's
    text end near where its words do. The Spring Luncheons have only 2019's, the one with words; the
    2018 and 2013 luncheons were photos alone on the old site. The other photos chosen from the
    old site (files.py) are in Files, unused, for the gallery to swap in."""
    return "\n".join([
        hp(block("29", 10)),
        hh(2, txt("6069", 0)),
        hp(block("6069", 1)), hp(block("6069", 2)), hp(block("6069", 3)), hp(block("6069", 4)),
        figure("gala-2026-2"), figure("gala-2026-4"), hp(block("6069", 5)),
        hh(2, txt("5471", 0)),
        hp(block("5471", 1)), hp(block("5471", 2)), hp(block("5471", 3)),
        vimeo("1066659420", "The Gala at Camp Smith", 426, 224, html.escape(txt("5471", 5))),
        figure("gala-2025-1"), hp(block("5471", 6)),
        hh(2, "Brilliance 2023"),
        hh(3, txt("4635", 0)),
        hp(block("4635", 1)), hp(block("4635", 2)), hp(block("4635", 3)),
        figure("gala-2023-1"),
        hh(3, txt("4635", 4)),
        hp(block("4635", 5)),
        "<p>Guests: 300. Raised: $471,000.</p>",
        f'<p><a class="gs-cta-link" href="https://issuu.com/smithfoundation/docs/gordon_smith_catalogue_digital">{html.escape(txt("4635", 6))}</a></p>',
        vimeo("832771624", "Brilliance 2023 - Tribute to Gordon Smith", 426, 240, "Brilliance 2023: Tribute to Gordon Smith"),
        hh(2, "Spring Luncheons"),
        hh(3, txt("1720", 25)),
        "<p>Guests: 150. Raised: $148,000.</p>",
        f'<p><a class="gs-cta-link" href="{pdf_path("auction-2019")}">2019 auction catalogue (PDF)</a></p>',
        figure("luncheon-2019-2"),
        hh(2, txt("29", 11)),
        hp(block("29", 12)),
    ])


def supporters_body():
    """The old page's three tabs as headings; the names as it ran them, with bullets between."""
    def run(n):
        return hp(block("1597", n))
    parts = [run(1), hh(2, "Donors")]
    for head_n, list_n in ((2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13)):
        parts += [hh(3, txt("1597", head_n)), run(list_n)]
    parts += [run(14),
              hh(2, "Sponsors and Granting Organizations"), run(15), run(16), run(17),
              hh(2, "Volunteers"), run(18), run(19)]
    return "\n".join(parts)


NEW_PAGES = [
    {"handle": "smith-foundation-scholarships", "title": "Scholarships", "hero": "hero-scholarships",
     "body": scholarships_body},
    {"handle": "brilliance-gala", "title": "Brilliance Gala", "hero": "gala-2026-1", "body": gala_body},
    {"handle": "smith-foundation-supporters", "title": "Supporters", "intro_block": ("1597", 0), "body": supporters_body},
]


def speaker_series_additions():
    art = [hh(3, txt("5892", 1)), "<p>June 6, 2026</p>", hp(block("5892", 3)), hp(block("5892", 4))]
    title = txt("5892", 15).replace("Speaker Series - ", "", 1)
    rebecca = [hh(3, title), "<p>May 2, 2026</p>", hp(block("5892", 17)),
               vimeo("1191311881", "Speaker Series: Art Education, For Life. Rebecca Baker-Grenier", 426, 240,
                     "Video: " + html.escape("Speaker Series: Art Education, For Life. Rebecca Baker-Grenier"))]
    unveiled = [hh(3, plain_heading("5026", 15, "| May 9, 6pm")), "<p>May 9, 2024</p>", hp(block("5026", 16)),
                hp(drop_suffix(block("5026", 17), "Reception to follow, supported by Polygon Homes.")),
                vimeo("945344575", "Art Education Unveiled: Perspectives from Prevailing Landscapes", 426, 240,
                      html.escape(txt("5026", 18)))]
    return "\n".join(["<h2>Past talks</h2>", *art, *rebecca, *unveiled])


def music_additions():
    shapes_first, _ = split(strip_marks(block("5940", 4)), 1)
    season = []
    for date_n, title_n, people in ((6, 7, (8, 9, 10)), (12, 13, (14, 15, 16)), (18, 19, (20, 21, 22)),
                                    (25, 26, (27, 28, 29, 30, 31, 32))):
        lines = [txt("4077", date_n), txt("4077", title_n)] + [txt("4077", p) for p in people]
        esc = lambda x: html.escape(x, quote=False)  # noqa: E731
        season.append("<li><strong>" + esc(lines[0]) + "</strong><br>" + esc(lines[1]) + "<br>"
                      + "<br>".join(esc(x) for x in lines[2:]) + "</li>")
    _, curator = split(strip_marks(block("4077", 1)), 1)
    return "\n".join([
        "<h2>Past concerts</h2>",
        hh(3, txt("5940", 2)), "<p>June 13, 2026</p>", hp(shapes_first),
        hh(3, "Fall 2023"), hp(strip_marks(block("4077", 0))), hp(curator),
        "<ul>" + "".join(season) + "</ul>",
        "<h2>The Steinway</h2>",
        hp(block("57", 6)),
        f'<figure class="gs-quote"><blockquote>{hp(block("57", 7))}</blockquote><figcaption><strong>Kathryn Allison</strong></figcaption></figure>',
        figure("piano", html.escape(txt("57", 9))),
    ])


def gordon_and_marion_additions():
    nodes = block("126", 2)
    for n in nodes:  # the CBC link without its tracking parameter
        if n["type"] == "link" and "?fbclid" in (n["url"] or ""):
            n["url"] = n["url"].split("?")[0]
    return "\n".join([hp(nodes),
                      vimeo("310422332", "Gordon A. Smith: A History", 640, 360, "Video: Gordon A. Smith: A History")])


DONATE_OLD = "including the donor page of each website."
DONATE_NEW = 'including the <a href="/pages/smith-foundation-supporters">donor page</a> of each website.'
AWARDS_LINE = ('<p>The Gordon and Marion Smith Foundation offers its own '
               '<a href="/pages/smith-foundation-scholarships">Young Artist Scholarships</a>, separate from these awards.</p>')

# The Foundation's page: its two cards get their links, and a Supporters card joins them (P-57).
CARD_LINKS = {
    "foundation-scholarships": ("Smith Foundation Scholarships", "/pages/smith-foundation-scholarships"),
    "foundation-brilliance-gala": ("Brilliance Gala & Auctions", "/pages/brilliance-gala"),
}
SUPPORTERS_CARD = {"handle": "foundation-supporters", "title": "Supporters", "image": "luncheon-2019-1",
                   "text_block": ("1597", 0), "url": "/pages/smith-foundation-supporters"}
TAKE_PART_GROUP = "foundation-take-part"

# The new theme's menu (P-52, P-53; navigation.py LATER)
MENU = [
    {"handle": "smith-foundation-scholarships", "title": "Smith Foundation scholarships",
     "where": ("Programs", "Scholarships and awards", 0)},
    {"handle": "brilliance-gala", "title": "Brilliance Gala", "where": ("Support", None, 2)},
    {"handle": "smith-foundation-supporters", "title": "Supporters", "where": ("Support", None, None)},
]


PAGE_IDS = {"speaker-series": "gid://shopify/Page/155719434537", "music-at-the-smith": "gid://shopify/Page/155719696681",
            "gordon-and-marion": "gid://shopify/Page/155692957993", "awards-and-scholarships": "gid://shopify/Page/165838225705"}


def before_pages():
    snap = json.loads((HERE.parent / "snapshots" / "foundation-pages-2026-09-28-before.json").read_text())["pages"]
    old = {p["handle"]: p for p in json.loads((HERE.parent / "snapshots" / "pages-2026-09-25.json").read_text())}
    return {"speaker-series": old["speaker-series"]["body"], "music-at-the-smith": old["music-at-the-smith"]["body"],
            "gordon-and-marion": snap["gordon-and-marion"]["custom.release_body"],
            "awards-and-scholarships": snap["awards-and-scholarships"]["custom.release_body"]}


def page_fields():
    """metafieldsSet inputs: the three new pages' fields and staged text (P-35, P-42), and the staged
    text of four pages with the old site's additions (DS-39; P-44)."""
    made = json.loads((CREATED / "foundation-pages.json").read_text())
    rows = []
    for p in NEW_PAGES:
        owner = made[p["handle"]]
        rows.append((owner, "programme", "single_line_text_field", "Smith Foundation"))
        rows.append((owner, "eyebrow", "single_line_text_field", "The Smith Foundation"))
        if p.get("hero"):
            rows.append((owner, "hero_image", "file_reference", img(p["hero"])))
        if p.get("intro_block"):
            rows.append((owner, "intro", "multi_line_text_field", txt(*p["intro_block"])))
        rows.append((owner, "release_body", "multi_line_text_field", p["body"]()))
    before = before_pages()
    rows.append((PAGE_IDS["speaker-series"], "release_body", "multi_line_text_field",
                 before["speaker-series"] + "\n" + speaker_series_additions()))
    rows.append((PAGE_IDS["music-at-the-smith"], "release_body", "multi_line_text_field",
                 before["music-at-the-smith"] + "\n" + music_additions()))
    rows.append((PAGE_IDS["gordon-and-marion"], "release_body", "multi_line_text_field",
                 before["gordon-and-marion"] + "\n" + gordon_and_marion_additions()))
    rows.append((PAGE_IDS["awards-and-scholarships"], "release_body", "multi_line_text_field",
                 before["awards-and-scholarships"] + "\n" + AWARDS_LINE))
    for r in rows:
        if "not uploaded" in r[3] or "(img:" in r[3]:
            raise SystemExit(f"a file isn't uploaded yet: {r[0]} {r[1]}")
    return [{"ownerId": o, "namespace": "custom", "key": k, "type": t, "value": v} for o, k, t, v in rows]


def check():
    for e in older_exhibitions():
        print(f"\n==== NEW {e['handle']}")
        for k, v in e.items():
            if k != "handle" and v:
                print(f"  {k}: {v if not isinstance(v, str) or len(v) < 400 else v[:400] + '…'}")
    for h, fields in existing_exhibitions().items():
        print(f"\n==== UPDATE {h}")
        for k, v in fields.items():
            s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
            print(f"  {k}: {s if len(s) < 500 else s[:500] + '…'}")
    for p in NEW_PAGES:
        print(f"\n==== PAGE {p['handle']} ({p['title']})\n{p['body']()}")
    print("\n==== speaker-series +\n" + speaker_series_additions())
    print("\n==== music-at-the-smith +\n" + music_additions())
    print("\n==== gordon-and-marion +\n" + gordon_and_marion_additions())


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "check":
        check()
    elif step == "page-fields":
        fields = page_fields()
        out = HERE.parent / "created" / "foundation-page-fields-input.json"
        out.write_text(json.dumps({"metafields": fields}, indent=1, ensure_ascii=False) + "\n")
        for f in fields:
            print(f["ownerId"].split("/")[-1], f["key"], len(f["value"]))
    else:
        raise SystemExit(__doc__)
