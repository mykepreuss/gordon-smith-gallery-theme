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
    else:
        sys.exit(__doc__)
    print(json.dumps(result, indent=2, ensure_ascii=False))
