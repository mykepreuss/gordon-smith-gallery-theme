#!/usr/bin/env python3
"""The rest of the content (Michael's go-ahead, 2026-09-25: "migrate all content into our new theme
so we can review and improve comprehensively"). The other 11 exhibitions, the About and Donate card
groups, the remaining pages' fields, and the page text staged for release (DS-39). Text is the
gallery's, moved without rewriting; exhibition text is read from the page snapshot, so nothing is
retyped. Prints the variables for each step's mutation.

  python3 proposals/store-writes/migration.py release-body-definition
  python3 proposals/store-writes/migration.py exhibitions
  python3 proposals/store-writes/migration.py cards
  python3 proposals/store-writes/migration.py card-groups <created/migration-cards.json>
  python3 proposals/store-writes/migration.py page-fields <created/migration-card-groups.json>
  python3 proposals/store-writes/migration.py review      # the exhibition fields as text, for checking
  python3 proposals/store-writes/migration.py page-pass   # the staged text changed by the page pass (2026-09-26)

Staged page text (custom.release_body): the page's text as it will read at release. The review
theme shows it instead of the live text (sections/gs-page-body.liquid). At release a script moves
it into the page and deletes the field; it stops if the live text no longer matches
snapshots/pages-2026-09-25.json. CLEARED means the page will have no text of its own.
"""
import html
import json
import pathlib
import re
import sys
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).resolve().parent
PAGES = {p["handle"]: p for p in json.loads((HERE / "snapshots" / "pages-2026-09-25.json").read_text())}
SITE = "https://gordonsmithgallery.com"
CLEARED = "<!-- Cleared at release: this page's text now lives in the exhibition entries. -->"


def img(n):
    return f"gid://shopify/MediaImage/{n}"


def link(url, text=""):
    return json.dumps({"text": text, "url": url}, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Page HTML to Shopify rich text. Paragraphs split on <p> and on a double <br>; a single <br>
# becomes a space. Keeps italics, bold and links; drops pasted wrappers and styles.

class Inline(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.nodes, self.marks, self.href, self.link_nodes, self.brs = [], [], [], None, None, 0

    def _flush(self):
        nodes = self.nodes
        while nodes and nodes[0]["type"] == "text" and not nodes[0]["value"].strip():
            nodes.pop(0)
        if nodes:
            if nodes[0]["type"] == "text":
                nodes[0]["value"] = nodes[0]["value"].lstrip()
            last = nodes[-1] if nodes[-1]["type"] == "text" else None
            if last:
                last["value"] = last["value"].rstrip()
            self.blocks.append([n for n in nodes if n["type"] != "text" or n["value"]])
        self.nodes = []

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.brs += 1
            if self.brs == 2:
                self._flush()
            return
        self._space_for_br()
        if tag in ("p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush()
        elif tag in ("em", "i"):
            self.marks.append("italic")
        elif tag in ("strong", "b"):
            self.marks.append("bold")
        elif tag == "a":
            self.href = dict(attrs).get("href")
            self.link_nodes = []

    def handle_endtag(self, tag):
        if tag in ("em", "i") and "italic" in self.marks:
            self.marks.remove("italic")
        elif tag in ("strong", "b") and "bold" in self.marks:
            self.marks.remove("bold")
        elif tag == "a" and self.link_nodes is not None:
            self.nodes.append({"type": "link", "url": self.href, "children": self.link_nodes})
            self.href, self.link_nodes = None, None
        elif tag in ("p", "div", "li"):
            self._flush()

    def _space_for_br(self):
        if self.brs == 1:
            self._text(" ")
        self.brs = 0

    def handle_data(self, data):
        if not data.strip() and not self.nodes:
            return
        self._space_for_br()
        self._text(re.sub(r"\s+", " ", data.replace(" ", " ")))

    def _text(self, value):
        node = {"type": "text", "value": value}
        for m in set(self.marks):
            node[m] = True
        target = self.link_nodes if self.link_nodes is not None else self.nodes
        prev = target[-1] if target else None
        if prev and prev["type"] == "text" and {k for k in prev if k not in ("type", "value")} == {k for k in node if k not in ("type", "value")}:
            prev["value"] += value
        else:
            target.append(node)


def paragraphs(page_html):
    """The page's paragraphs, each a list of rich text nodes, skipping headings (dates, credits)."""
    body = re.sub(r"<h[1-6][^>]*>.*?</h[1-6]>", "", page_html, flags=re.S)
    parser = Inline()
    parser.feed(body)
    parser._flush()
    return [b for b in parser.blocks if b]


def plain(nodes):
    out = ""
    for n in nodes:
        out += n["value"] if n["type"] == "text" else plain(n["children"])
    return re.sub(r"\s+", " ", out).strip()


def rich(*blocks):
    return json.dumps({"type": "root", "children": [{"type": "paragraph", "children": b} for b in blocks]}, ensure_ascii=False)


def text(value, italic=False):
    node = {"type": "text", "value": value}
    if italic:
        node["italic"] = True
    return [node]


def split_after(nodes, sentences):
    """Split a paragraph after its first n sentences (for a summary that stays in reading order)."""
    joined = plain(nodes)
    parts = re.split(r"(?<=[.?!])\s+", joined)
    head = " ".join(parts[:sentences])
    # Walk the nodes and cut at the character where the head ends.
    cut, first, rest = len(head), [], []
    for n in nodes:
        v = n["value"] if n["type"] == "text" else None
        if v is None or cut <= 0:
            (first if cut > 0 else rest).append(n)
            if n["type"] != "text":
                cut -= len(plain(n["children"]))
            continue
        if len(v) <= cut:
            first.append(n)
            cut -= len(v)
        else:
            a, b = dict(n), dict(n)
            a["value"], b["value"] = v[:cut], v[cut:].lstrip()
            first.append(a)
            if b["value"]:
                rest.append(b)
            cut = 0
    return first, rest


# ---------------------------------------------------------------------------
# Exhibitions (content model part 2), from their pages and the Past and Upcoming cards.

def entry(handle, fields):
    return {
        "type": "exhibition",
        "handle": handle,
        "capabilities": {"publishable": {"status": "ACTIVE"}},
        "fields": [{"key": k, "value": v} for k, v in fields.items() if v not in (None, "", "[]")],
    }


def names(s):
    """An artist list as written ("A, B, C and D"), one name per item."""
    items = [x.strip() for x in s.split(",")]
    last = items.pop()
    if " and " in last and last.count(" and ") == 1 and not items[-1:] == [""]:
        items += [x.strip() for x in last.split(" and ")]
    else:
        items.append(last)
    return [re.sub(r"^and ", "", x) for x in items if x]


def exhibitions():
    out = []

    # From the Ground: its page. Curator and artists are read from the text, which keeps them too.
    p = paragraphs(PAGES["exhibition-from-the-ground"]["body"])
    out.append(entry("from-the-ground", {
        "title": "From the Ground",
        "start_date": "2025-09-19",
        "end_date": "2026-02-26",
        "curator_credit": "Curated by Holly Schmidt and Amelia Epp",
        "artists": json.dumps(["Amelia Butcher", "Xinwei Che", "Genevieve Robertson"]),
        "collection_artists": json.dumps(names("Lauren Brevner, James Nexw'Kalus-Xwalacktun Harry, Karin Bubaš, Edward Burtynsky, Victor Cicansky, Anna Binta Diallo, Toni Onley, Gordon Smith, and Charlene Vickers"), ensure_ascii=False),
        "key_image": img(45716969259305),
        "key_image_caption": rich(text("Photo by Rachel Topham")),
        "summary": plain(p[0]),
        "body": rich(p[1], p[3]),
        "credits": rich(p[2]),
        # The gallery's first image repeats the key image, so it's left out here.
        "installation_views": json.dumps([img(n) for n in (45717016903977, 45717016314153, 45717016674601, 45717016412457, 45717016445225, 45717016838441, 45717016936745, 45717016772905)]),
        "installation_credit": "Photography by Rachel Topham",
    }))

    # Stitched: its page. Start date April 3 (its own page), the content model's default (Q10).
    p = paragraphs(PAGES["exhibition-stitched-merging-photography-and-textile-practices"]["body"])
    summary, rest = split_after(p[0], 2)
    out.append(entry("stitched", {
        "title": "Stitched",
        "subtitle": "Merging Photography and Textile Practices",
        "start_date": "2025-04-03",
        "end_date": "2025-06-21",
        "curator_credit": "Co-curated by Emmy Lee Wall, Executive Director and Chief Curator, Capture Photography Festival, and Chelsea Yuill, Assistant Curator, Capture Photography Festival",
        "artists": json.dumps(["Simranpreet Kaur Anand", "Barbara Astman", "Maya Beaudry", "Dana Claxton", "Liz Ikiriko", "Jayce Salloum", "Michaëlle Sergile", "Michelle Sound", "Lan “Florence” Yee"], ensure_ascii=False),
        "key_image": img(45716987380009),
        "key_image_caption": rich(text("Photo by Rachel Topham")),
        "summary": plain(summary),
        "body": rich(rest, p[1]),
        "credits": rich(p[2]),
        # The gallery's third image repeats the key image, so it's left out here.
        "installation_views": json.dumps([img(n) for n in (45717041742121, 45717041807657, 45717041676585, 45717041774889, 45717041578281)]),
        "installation_credit": "Photography by Rachel Topham",
    }))

    # Playhouse: its page.
    p = paragraphs(PAGES["exhibition-playhouse"]["body"])
    out.append(entry("playhouse", {
        "title": "Playhouse",
        "start_date": "2024-09-20",
        "end_date": "2025-02-27",
        "curator_credit": "Curated by Annie Canto and Amelia Epp",
        "artists": json.dumps(names("Anne Meredith Barry, Karin Bubaš, Annie Canto, Victor Cicansky, Leonhard Epp, Gathie Falk, Geoffrey Farmer, Whess Harman, Guná Jensen, Hannah Jickling and Reed H. Reed, Sandeep Johal, Helen Kalvak, Sara Khan, Roz Marshall, Cindy Mochizuki, Parvin Peivandi, Setsuko Piroche, Jane Ash Poitras, Jack Shadbolt, Sylvia Tait, Tukuki, Vancouver School Collective, Etienne Zack, Barbara Zeigler and Joan Smith"), ensure_ascii=False),
        "key_image": img(45716991508777),
        "key_image_caption": rich(text("Photo by Rachel Topham")),
        "summary": plain(p[0]),
        "body": rich(p[1], p[2]),
        "credits": rich(p[3]),
    }))

    # Prevailing Landscapes: its page. Its one gallery image repeats the key image.
    p = paragraphs(PAGES["exhibition-prevailing-landscapes"]["body"])
    out.append(entry("prevailing-landscapes", {
        "title": "Prevailing Landscapes",
        "start_date": "2024-04-12",
        "end_date": "2024-06-22",
        "curator_credit": "Curated by Jackie Wong",
        "artists": json.dumps(names("Kim Dorland, Stan Douglas, Tim Gardner, Cameron Kerr, Krystle Silverfox, Ian Wallace, Jin-Me Yoon and Karen Zalamea")),
        "key_image": img(45717190508841),
        "key_image_caption": rich(text("Photo by Rachel Topham")),
        "summary": plain(p[0]),
        "body": rich(p[1]),
    }))

    # The Art of Conversation: its page. The page's banner is the key image; the Past card's
    # image becomes its one installation view.
    p = paragraphs(PAGES["exhibition-the-art-of-conversation"]["body"])
    out.append(entry("the-art-of-conversation", {
        "title": "The Art of Conversation",
        "start_date": "2023-09-23",
        "end_date": "2024-02-22",
        "curator_credit": "Curated by Janet Wang and Amelia Epp",
        "key_image": img(45717423227177),
        "key_image_caption": rich(text("Photo by Rachel Topham")),
        "summary": plain(p[0]),
        "credits": rich(p[1]),
        "installation_views": json.dumps([img(45717171667241)]),
    }))

    # The five other older shows on the Past card list: title, dates and image (DS-25).
    for handle, title, start, end, image, artwork in [
        ("endless-summer", "Endless Summer", "2023-04-15", "2023-06-17", 45717189919017, False),
        ("paths", "Paths", "2022-09-24", "2023-02-23", 45717172257065, True),
        ("we-can-only-hint-at-this-with-words", "We Can Only Hint at This with Words", "2022-04-23", "2022-06-25", 45717172322601, False),
        ("beyond-the-horizon", "Beyond the Horizon", "2021-09-25", "2022-02-24", 45717190967593, False),
        ("unfixed", "Unfixed", "2021-04-08", "2021-06-05", 45717198831913, True),
    ]:
        out.append(entry(handle, {
            "title": title, "start_date": start, "end_date": end, "key_image": img(image),
            "key_image_is_artwork": "true" if artwork else None,
        }))

    # The Upcoming page's third card: no title yet, "Coming soon, September 2027".
    out.append(entry("fall-2027-exhibition", {
        "title": "Fall 2027 Exhibition",
        "start_date": "2027-09-01",
        "dates_note": "Coming soon, September 2027",
        "key_image": img(45716856832297),
    }))
    return out


# ---------------------------------------------------------------------------
# Cards and card groups (content model part 4).

CARDS = {
    # About: the three organisation columns from the old default template. The logos were the
    # columns' only titles; since DS-50 each card's Logo field shows its logo as its heading.
    "about-artists-for-kids": {
        "title": "Artists for Kids",
        "text": "Established in 1989 by renowned BC artist patrons Gordon Smith, Jack Shadbolt and Bill Reid, Artists For Kids was founded with the singular intent to support children, their art education, and their future.",
        "link": link("https://artistsforkids.sd44.ca/", "Website + Programs"),
        "logo": "Artists for Kids",  # DS-50, 2026-09-26
    },
    "about-gordon-smith-gallery": {
        "title": "The Gordon Smith Gallery of Canadian Art",
        "text": "The Gordon Smith Gallery is a space where education is seen not as an after-thought to curation, but as the purpose of each step we take. The Gordon and Marion Smith Foundation for Young Artists and Artists for Kids work collaboratively to program the Gordon Smith Gallery of Canadian Art and the exhibitions.",
        "link": link(f"{SITE}/pages/on-now", "Exhibitions"),
        "logo": "Gallery",  # DS-50, 2026-09-26
    },
    "about-smith-foundation": {
        "title": "The Gordon and Marion Smith Foundation for Young Artists",
        "text": "The Gordon and Marion Smith Foundation for Young Artists was founded in 2002 to establish an endowment fund, the interest from which would fund ongoing visual arts enrichment opportunities for the children of British Columbia. The Foundation’s role has evolved to include the presentation of a diverse and accessible range of visual arts programming and the curation of high profile exhibitions at the Gordon Smith Gallery of Canadian Art.",
        "link": link(f"{SITE}/pages/the-smith-foundation", "The Foundation"),
        "logo": "Smith Foundation",  # DS-50, 2026-09-26
    },
    # Donate: "Ways To Give", four text cards.
    "donate-online-form": {
        "title": "Online Form",
        "text": "Donate directly through our website with the secure Blackbaud Etapestry form above. Your submission will be processed when you finalize your secure payment information.",
    },
    "donate-email": {
        "title": "Email",
        "text": "To make a gift or for more information about the various giving options, email us at admin@smithfoundation.ca",
    },
    "donate-mail": {
        "title": "Mail",
        "text": "Address:\nThe Gordon and Marion Smith Foundation for Young Artists\n2121 Lonsdale Avenue, North Vancouver\nBritish Columbia, Canada\nV7M 2K6",
    },
    "donate-phone": {
        "title": "Phone",
        "text": "Contact us by telephone at 604-998-8563",
    },
}

GROUPS = {
    "about-organisations": (None, ["about-artists-for-kids", "about-gordon-smith-gallery", "about-smith-foundation"]),
    "donate-ways-to-give": ("Ways To Give", ["donate-online-form", "donate-email", "donate-mail", "donate-phone"]),
}


def cards():
    return {h.replace("-", "_"): {"type": "card", "handle": h,
                                  "fields": [{"key": k, "value": v} for k, v in c.items()]}
            for h, c in CARDS.items()}


def card_groups(created_cards):
    ids = {v["metaobject"]["handle"]: v["metaobject"]["id"] for v in created_cards.values()}
    out = {}
    for handle, (heading, members) in GROUPS.items():
        fields = [{"key": "cards", "value": json.dumps([ids[m] for m in members])}]
        if heading:
            fields.insert(0, {"key": "heading", "value": heading})
        out[handle.replace("-", "_")] = {"type": "card_group", "handle": handle, "fields": fields}
    return out


# ---------------------------------------------------------------------------
# Staged page text (DS-39) and the remaining pages' fields.

def release_body_definition():
    return {"definition": {
        "namespace": "custom", "key": "release_body", "ownerType": "PAGE", "type": "multi_line_text_field",
        "name": "Text at release (temporary)",
        "description": "Used only until the new theme goes live. The review theme shows this instead of the page's text. At release it replaces the page's text and this field is deleted. Don't edit.",
    }}


GORDON_AND_MARION_VIDEO = (
    "<h2>Video: Gordon Smith's Magic</h2>\n"
    '<iframe src="https://player.vimeo.com/video/392350371?dnt=1" title="Gordon Smith\'s Magic" '
    'allow="fullscreen; picture-in-picture" loading="lazy"></iframe>'
)
DONATE_NOTE = (
    "<p>All donations over $25 are eligible for a charitable tax receipt in accordance with CRA regulations. "
    "Any donation of $1,000 or above will be recognized in the Gordon and Marion Smith Foundation and Artists "
    "for Kids’ Annual Report, including the donor page of each website.</p>"
)


# Donate's "Ways to Support" heading holds two phrases in one heading, split by line breaks, so it
# reads as two headings. The words stay; the second phrase becomes the paragraph it is (page pass,
# 2026-09-26).
DONATE_HEADING_OLD = (
    '<h2>\n<strong><span style="color: #b8bc49; font-size: 24pt; font-family: Poppins,sans-serif;">'
    '<br>Ways to Support<br></span></strong><br>Every contribution makes a difference:</h2>'
)
DONATE_HEADING_NEW = "<h2>Ways to Support</h2>\n<p>Every contribution makes a difference:</p>"


def donate_body():
    body = PAGES["donate"]["body"]
    assert body.count(DONATE_HEADING_OLD) == 1, "Donate's heading changed since the snapshot"
    return body.replace(DONATE_HEADING_OLD, DONATE_HEADING_NEW) + "\n" + DONATE_NOTE


def artists_body():
    """The Artists page: its two paragraphs, then its artist links as one list, in the same order
    and with the same addresses. Today they're loose links and line breaks centred in two blocks,
    so they can't be laid out; as a list they flow into columns (DS-45). Page pass, 2026-09-26."""
    body = PAGES["artists"]["body"]
    intro = [f"<p>{plain_text(m.group(1))}</p>" for m in re.finditer(r"<p[^>]*>((?:(?!<a ).)*?)</p>", body, flags=re.S)
             if plain_text(m.group(1))]
    links = []
    for m in re.finditer(r'<a href="([^"]+)"[^>]*>(.*?)</a>', body, flags=re.S):
        name = plain_text(m.group(2))
        if name:
            links.append(f'<li><a href="{m.group(1)}" rel="noopener" target="_blank">{name}</a></li>')
    return "\n".join(intro + ["<ul>"] + links + ["</ul>"])


def plain_text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def release_bodies():
    return {
        "on-now": CLEARED,
        "upcoming-exhibitions": CLEARED,
        "upcoming-events": CLEARED,
        "donate": donate_body(),
        "gordon-and-marion": PAGES["gordon-and-marion"]["body"] + "\n" + GORDON_AND_MARION_VIDEO,
        "artists": artists_body(),
    }


def page_fields(created_groups):
    ids = {v["metaobject"]["handle"]: v["metaobject"]["id"] for v in created_groups.values()}
    rows = [
        # About: superseded on 2026-09-26 by about_us.py about-afk (P-23: the Bill Reid print as hero,
        # no card groups). A re-run would put these two back.
        ("about", "hero_image", "file_reference", img(45637943591209)),
        ("about", "card_groups", "list.metaobject_reference", json.dumps([ids["about-organisations"]])),
        ("about-us", "hero_image", "file_reference", img(45637943591209)),
        ("exhibitions-1", "hero_image", "file_reference", img(45566339481897)),
        ("exhibitions-1", "hero_caption", "single_line_text_field", "Photography by Rachel Topham"),
        ("donate", "hero_image", "file_reference", img(45739508990249)),
        ("donate", "card_groups", "list.metaobject_reference", json.dumps([ids["donate-ways-to-give"]])),
        ("permanent-collection", "hero_image", "file_reference", img(45669029970217)),
        ("permanent-collection", "intro", "multi_line_text_field", "Explore over 1,000 + Works by Canadian Artists in the Collection"),
        ("permanent-collection", "cta", "link", link("https://afkcatalogue.sd44.ca/s/TheCollection/page/home", "Browse")),
        ("volunteer", "hero_image", "file_reference", img(45689877954857)),
        ("volunteer", "cta", "link", link(f"{SITE}/cdn/shop/files/GSF-Volunteer-Application-Form_202603.pdf", "Volunteer Form")),
        ("gordon-and-marion", "hero_image", "file_reference", img(45698031780137)),
        ("plan-your-visit", "hero_image", "file_reference", img(45633125712169)),
    ]
    rows += [(h, "release_body", "multi_line_text_field", v) for h, v in release_bodies().items()]
    out = [{"ownerId": PAGES[h]["id"], "namespace": "custom", "key": k, "type": t, "value": v} for h, k, t, v in rows]
    return {f"m{i // 25}": out[i:i + 25] for i in range(0, len(out), 25)}


def review():
    for e in exhibitions():
        print(f"## {e['handle']}")
        for f in e["fields"]:
            v = f["value"]
            if v.startswith('{"type": "root"'):
                v = " / ".join(plain(b["children"]) for b in json.loads(v)["children"])
            print(f"- {f['key']}: {v}")
        print()


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "release-body-definition":
        print(json.dumps(release_body_definition(), indent=2, ensure_ascii=False))
    elif step == "exhibitions":
        print(json.dumps({e["handle"].replace("-", "_"): e for e in exhibitions()}, indent=2, ensure_ascii=False))
    elif step == "cards":
        print(json.dumps(cards(), indent=2, ensure_ascii=False))
    elif step == "card-groups":
        print(json.dumps(card_groups(json.loads(pathlib.Path(sys.argv[2]).read_text())), indent=2, ensure_ascii=False))
    elif step == "page-fields":
        print(json.dumps(page_fields(json.loads(pathlib.Path(sys.argv[2]).read_text())), indent=2, ensure_ascii=False))
    elif step == "review":
        review()
    elif step == "page-pass":
        rows = [{"ownerId": PAGES[h]["id"], "namespace": "custom", "key": "release_body", "type": "multi_line_text_field", "value": v}
                for h, v in release_bodies().items() if h in ("donate", "artists")]
        print(json.dumps({"m0": rows}, indent=2, ensure_ascii=False))
