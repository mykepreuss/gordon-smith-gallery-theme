#!/usr/bin/env python3
"""About Us: each organisation's description beside its own logo (DS-50, Michael, 2026-09-26:
"use the correct logo for each text description and integrate the logo and text better").

The page's three descriptions move from its text into a card group, one card per organisation,
and the card's new Logo field picks the logo the theme shows beside the text. The words are the
gallery's, read from the page snapshot, so nothing is retyped. The page's text is staged empty
(DS-39): at release it loses the three descriptions and the combined logo image above them.
Prints the variables for each step's mutation.

  python3 proposals/store-writes/about_us.py logo-field
  python3 proposals/store-writes/about_us.py cards
  python3 proposals/store-writes/about_us.py card-group <created/about-us-cards.json>
  python3 proposals/store-writes/about_us.py page-fields <created/about-us-card-group.json>
  python3 proposals/store-writes/about_us.py about-logos   # About's three cards (Michael, 2026-09-26)
  python3 proposals/store-writes/about_us.py about-afk     # About becomes About Artists for Kids (below)
  python3 proposals/store-writes/about_us.py about-afk-review   # its staged text and caption, as text
  python3 proposals/store-writes/about_us.py afk-merge     # About merged into Artists for Kids (below)
  python3 proposals/store-writes/about_us.py afk-merge-review

Then (Michael, 2026-09-26: "Add that content you identified word for word"), from Our Story, which
leaves the Shop (P-25): its sentence on art specialists after the founding, its sentence on the
ceremonial drum and the more than 100 artists after the paragraph on the first print, and its fuller
caption for the print. "contemporary limited editions" links to the Shop, which Our Story used to
sit under.

About Artists for Kids (Michael, 2026-09-26: "/about should be /about-artists-for-kids and be
focused on that part of the organization"). About's text is Artists for Kids' history, but the page
shared About Us's hero photo and three organisation rows, so the two looked alike. Now, invisible to
the live theme: the Artists for Kids programme (its logo and colours, DS-47), the first portfolio
print as an artwork hero with the page's own caption, no organisation rows (they stay on About Us),
and its text staged without the print and caption, which the hero now carries. The title and address
change at release (release.py addresses), because the live theme shows them.

Superseded the same day (P-24; Michael: "Should /pages/artists-for-kids and /pages/about be merged?
I prefer /pages/artists-for-kids"): About's history joins the Artists for Kids page, under a
"History" heading after the page's own text, with the print where the text names it. About is hidden
at release and its address forwarded to Artists for Kids (release.py addresses), so its own staged
text is removed.
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
PAGE = next(p for p in json.loads((HERE / "snapshots" / "pages-2026-09-25.json").read_text())
            if p["handle"] == "about-us")
SITE = "https://gordonsmithgallery.com"
CARD_DEFINITION = "gid://shopify/MetaobjectDefinition/23754375465"
PROGRAMMES = ["Gallery", "Smith Foundation", "Artists for Kids"]
STAGED = "<!-- Cleared at release: this page's text now lives in its card group, each organisation beside its logo. -->"

# Heading in the page text (all capitals there), the card's title, its logo, its link.
ORGS = [
    ("THE GORDON SMITH GALLERY OF CANADIAN ART", "about-us-gallery",
     "The Gordon Smith Gallery of Canadian Art", "Gallery",
     f"{SITE}/pages/plan-your-visit", "Plan your visit"),
    ("ARTISTS FOR KIDS", "about-us-artists-for-kids",
     "Artists for Kids", "Artists for Kids",
     f"{SITE}/pages/artists-for-kids", "More about Artists for Kids"),
    ("THE GORDON AND MARION SMITH FOUNDATION FOR YOUNG ARTISTS", "about-us-foundation",
     "The Gordon and Marion Smith Foundation for Young Artists", "Smith Foundation",
     f"{SITE}/pages/the-smith-foundation", "More about the Foundation"),
]


def plain(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def descriptions():
    """Each heading's next paragraph, as plain text."""
    paras = [plain(m.group(1)) for m in re.finditer(r"<p[^>]*>(.*?)</p>", PAGE["body"], flags=re.S)]
    paras = [p for p in paras if p]
    out = {}
    for heading, *_ in ORGS:
        i = paras.index(heading)
        out[heading] = paras[i + 1]
    assert len(paras) == 6, "About Us's text changed since the snapshot"
    return out


def link(url, text):
    return json.dumps({"text": text, "url": url}, ensure_ascii=False)


def logo_field():
    return {"id": CARD_DEFINITION, "definition": {"fieldDefinitions": [{"create": {
        "key": "logo", "type": "single_line_text_field", "name": "Logo",
        "description": "For a card about the Gallery, the Foundation or Artists for Kids: shows that logo as the card's heading. Blank on other cards.",
        "validations": [{"name": "choices", "value": json.dumps(PROGRAMMES)}],
    }}]}}


def cards():
    text = descriptions()
    out = {}
    for heading, handle, title, logo, url, label in ORGS:
        out[handle.replace("-", "_")] = {"type": "card", "handle": handle, "fields": [
            {"key": "title", "value": title},
            {"key": "logo", "value": logo},
            {"key": "text", "value": text[heading]},
            {"key": "link", "value": link(url, label)},
        ]}
    return out


def card_group(created_cards):
    ids = {v["metaobject"]["handle"]: v["metaobject"]["id"] for v in created_cards.values()}
    return {"about_us_organisations": {"type": "card_group", "handle": "about-us-organisations",
                                      "fields": [{"key": "cards", "value": json.dumps([ids[o[1]] for o in ORGS])}]}}


# About's organisation cards (migration.py), the same logos (Michael, 2026-09-26: "DS-50 approved,
# apply logos to the About page too"). Only the Logo field changes.
ABOUT_CARDS = {
    "gid://shopify/Metaobject/608389267753": "Artists for Kids",   # about-artists-for-kids
    "gid://shopify/Metaobject/608389300521": "Gallery",            # about-gordon-smith-gallery
    "gid://shopify/Metaobject/608389333289": "Smith Foundation",   # about-smith-foundation
}


def about_logos():
    return {gid: {"fields": [{"key": "logo", "value": logo}]} for gid, logo in ABOUT_CARDS.items()}


ABOUT = next(p for p in json.loads((HERE / "snapshots" / "pages-2026-09-25.json").read_text())
             if p["handle"] == "about")
REID = "gid://shopify/MediaImage/40274179096873"  # Reid_REID002_Xhuwaji_HaidaGrizzly.jpg, 3589 x 3629
REID_ALT = "Bill Reid, Xhuwaji / Haida Grizzly Bear, 1990"


def clean_inline(s):
    s = re.sub(r"\s+data-[\w-]+=\"[^\"]*\"", "", s)
    s = s.replace("\u00a0", " ").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", s).strip()


def about_afk_text():
    """About's four paragraphs, word for word, as paragraphs; and its print's caption."""
    body = ABOUT["body"]
    paras = [clean_inline(m.group(1)) for m in re.finditer(r'<div class="x_elementToProof"[^>]*>(.*?)</div>', body, flags=re.S)]
    paras = [x for x in paras if plain(x)]
    assert len(paras) == 4 and paras[0].startswith("Artists for Kids was founded in 1989"), "About's text changed since the snapshot"
    caption = plain(re.search(r"<h5[^>]*>(.*?)</h5>", body, flags=re.S).group(1))
    assert caption.startswith("Bill Reid, (Canadian, 1920"), caption
    return "\n".join(f"<p>{x}</p>" for x in paras), caption


def about_afk():
    staged, caption = about_afk_text()
    page = ABOUT["id"]
    return {
        "metafieldsSet": {"m0": [
            {"ownerId": page, "namespace": "custom", "key": "programme", "type": "single_line_text_field", "value": "Artists for Kids"},
            {"ownerId": page, "namespace": "custom", "key": "hero_image", "type": "file_reference", "value": REID},
            {"ownerId": page, "namespace": "custom", "key": "hero_is_artwork", "type": "boolean", "value": "true"},
            {"ownerId": page, "namespace": "custom", "key": "hero_caption", "type": "single_line_text_field", "value": caption},
            {"ownerId": page, "namespace": "custom", "key": "release_body", "type": "multi_line_text_field", "value": staged},
        ]},
        "metafieldsDelete": [{"ownerId": page, "namespace": "custom", "key": "card_groups"}],
        "fileUpdate": [{"id": REID, "alt": REID_ALT}],
    }


AFK = next(p for p in json.loads((HERE / "snapshots" / "pages-2026-09-25.json").read_text())
           if p["handle"] == "artists-for-kids")
OUR_STORY = next(p for p in json.loads((HERE / "snapshots" / "pages-2026-09-25.json").read_text())
                 if p["handle"] == "our-story")
SHOP = "/pages/shop"


def our_story_parts():
    """Our Story's three things the Artists for Kids page lacked, word for word."""
    body = OUR_STORY["body"]
    blocks = [clean_inline(m.group(1)) for m in re.finditer(r"<(?:p|div)[^>]*>(.*?)</(?:p|div)>", body, flags=re.S)]
    specialists = next(b for b in blocks if b.startswith("Through art specialists"))
    first_print = next(b for b in blocks if b.startswith("In 1990, the group published"))
    drum = first_print[first_print.index("This print by Bill Reid"):]
    assert drum.endswith("collections in the country."), drum
    caption = clean_inline(re.search(r"<h5[^>]*>(.*?)</h5>", body, flags=re.S).group(1))
    caption = re.sub(r"</?span[^>]*>", "", caption).strip()
    # The italics moved inside the comma; words unchanged.
    caption = caption.replace("1998)<em> XHUWAJI/Haida Grizzly Bear, </em>(1990)", "1998) <em>XHUWAJI/Haida Grizzly Bear</em>, (1990)")
    assert caption == "Bill Reid, (Canadian, 1920 – 1998) <em>XHUWAJI/Haida Grizzly Bear</em>, (1990) Serigraph, 22 in x 22 in.", caption
    return specialists, drum, caption


REID_SRC = "https://cdn.shopify.com/s/files/1/0895/9580/5993/files/Reid_REID002_Xhuwaji_HaidaGrizzly.jpg?v=1728074721&width=1440"


def figure(src, alt, caption, width, height, artwork=False, caption_html=False):
    cls = ' class="gs-figure--artwork"' if artwork else ""
    cap = caption if caption_html else html.escape(caption, quote=False)
    return (f'<figure{cls}><img src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}" width="{width}" height="{height}" loading="lazy">'
            f"<figcaption>{cap}</figcaption></figure>")


def afk_merge_text():
    """The Artists for Kids page's own text, then About's history under a heading, word for word.
    Both pages' pictures become figures with their own captions; pasted formatting stays behind."""
    body = AFK["body"]
    paras = [clean_inline(re.sub(r"<span[^>]*></span>", "", m.group(1))) for m in re.finditer(r"<p[^>]*>(.*?)</p>", body, flags=re.S)]
    assert len(paras) == 2 and paras[0].startswith("Artists for Kids brings together"), "Artists for Kids' text changed since the snapshot"
    img = re.search(r'<img src="([^"]+)" alt="([^"]*)"', body)
    caption = plain(re.findall(r'<div style="text-align: left;">(.*?)</div>', body, flags=re.S)[0])
    assert caption.startswith("Gordon Smith and a group of young artists"), caption
    history, reid_caption = about_afk_text()
    history = history.split("\n")
    assert "<em>Xhuwaji / Haida Grizzly</em>" in history[1]
    out = [f"<p>{x}</p>" for x in paras]
    out.append(figure(img.group(1), html.unescape(img.group(2)), caption, 1764, 993))
    specialists, drum, full_caption = our_story_parts()
    editions = "contemporary limited editions"
    assert history[2].count(editions) == 1
    history[2] = history[2].replace(editions, f'<a href="{SHOP}">{editions}</a>')
    out.append("<h2>History</h2>")
    out.append(history[0])
    out.append(f"<p>{specialists}</p>")
    out.append(history[1])
    out.append(figure(REID_SRC, REID_ALT, full_caption, 1440, 1456, artwork=True, caption_html=True))
    out.append(f"<p>{drum}</p>")
    out += history[2:]
    return "\n".join(out)


def afk_merge():
    return {
        "metafieldsSet": {"m0": [
            {"ownerId": AFK["id"], "namespace": "custom", "key": "release_body", "type": "multi_line_text_field", "value": afk_merge_text()},
        ]},
        "metafieldsDelete": [{"ownerId": ABOUT["id"], "namespace": "custom", "key": "release_body"}],
    }


def page_fields(created_group):
    group = created_group["about_us_organisations"]["metaobject"]["id"]
    return {"m0": [
        {"ownerId": PAGE["id"], "namespace": "custom", "key": "card_groups", "type": "list.metaobject_reference",
         "value": json.dumps([group])},
        {"ownerId": PAGE["id"], "namespace": "custom", "key": "release_body", "type": "multi_line_text_field",
         "value": STAGED},
    ]}


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "logo-field":
        result = logo_field()
    elif step == "cards":
        result = cards()
    elif step == "card-group":
        result = card_group(json.loads(pathlib.Path(sys.argv[2]).read_text()))
    elif step == "page-fields":
        result = page_fields(json.loads(pathlib.Path(sys.argv[2]).read_text()))
    elif step == "about-logos":
        result = about_logos()
    elif step == "about-afk":
        result = about_afk()
    elif step == "afk-merge":
        result = afk_merge()
    elif step == "afk-merge-review":
        sys.exit(print(afk_merge_text()))
    elif step == "about-afk-review":
        staged, caption = about_afk_text()
        sys.exit(print(f"Hero caption: {caption}\nHero alt: {REID_ALT}\n\nStaged text:\n{staged}"))
    else:
        sys.exit(__doc__)
    print(json.dumps(result, indent=2, ensure_ascii=False))
