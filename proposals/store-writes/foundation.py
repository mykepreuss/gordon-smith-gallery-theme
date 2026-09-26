#!/usr/bin/env python3
"""The Smith Foundation page pass (DS-52, Michael, 2026-09-26: "improve the design of the page
while still adhering to the brand guidelines and design system").

Its text starts with the Foundation's full name on a line of its own, styled as a heading in the
Foundation's text colour, and the next sentence opens with the same words. The staged text (DS-39)
leaves that line out and keeps the two paragraphs word for word, without the pasted styling. The
link to Gordon and Marion stays on the site instead of opening a new tab, and the four programmes
the text names link to their pages. Prints the variables for the metafieldsSet mutation.

  python3 proposals/store-writes/foundation.py staged
  python3 proposals/store-writes/foundation.py review   # the staged text
  python3 proposals/store-writes/foundation.py heading  # "Get involved" over the five ways to take part

Michael, 2026-09-26: "DS-52 approved, add a Get involved heading".
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
PAGE = next(p for p in json.loads((HERE / "snapshots" / "pages-2026-09-25.json").read_text())
            if p["handle"] == "the-smith-foundation")
FULL_NAME = "The Gordon and Marion Smith Foundation for Young Artists"
PROGRAMMES = [("Explore + Create", "explore-create"), ("Art In Good Company", "art-in-good-company"),
              ("Speaker Series", "speaker-series"), ("Music at The Smith", "music-at-the-smith")]


def plain(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def words(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def staged_text():
    paras = re.findall(r"<p[^>]*>(.*?)</p>", PAGE["body"], flags=re.S)
    assert len(paras) == 3 and plain(paras[0]) == FULL_NAME, "The Foundation's text changed since the snapshot"
    first, second = paras[1], paras[2]
    assert plain(first).startswith(FULL_NAME + " was founded in 2002")
    first = plain(first)
    for name, handle in PROGRAMMES:
        assert first.count(name) == 1, name
        first = first.replace(name, f'<a href="/pages/{handle}">{name}</a>')
    link = re.search(r'<a href="https://gordonsmithgallery.com/pages/gordon-and-marion"[^>]*>(.*?)</a>', second, flags=re.S)
    before = plain(second[:link.start()].replace("<span>", ""))
    second = f'{before} <a href="/pages/gordon-and-marion">{plain(link.group(1))}</a>'
    # Words unchanged: the text without its tags matches the live text without its tags.
    assert words(second) == words(paras[2]) and words(first) == words(paras[1])
    return f"<p>{first}</p>\n<p>{second}</p>"


TAKE_PART = "gid://shopify/Metaobject/608367444265"  # card group foundation-take-part


def heading():
    return {"id": TAKE_PART, "metaobject": {"fields": [{"key": "heading", "value": "Get involved"}]}}


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step == "staged":
        print(json.dumps({"metafields": [{"ownerId": PAGE["id"], "namespace": "custom", "key": "release_body",
                                          "type": "multi_line_text_field", "value": staged_text()}]}, indent=2, ensure_ascii=False))
    elif step == "heading":
        print(json.dumps(heading(), indent=2))
    elif step == "review":
        print(staged_text())
    else:
        sys.exit(__doc__)
