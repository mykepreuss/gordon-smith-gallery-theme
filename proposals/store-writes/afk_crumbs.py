#!/usr/bin/env python3
"""Crumbs on 13 Artists for Kids pages (option A of proposals/internal-linking-review.md;
Michael, 2026-09-29: "Go ahead with option A, the crumbs on the 14 pages", then "Take the crumb
off Professional Development").

Each page's Eyebrow field (custom.eyebrow) names the page it belongs to. The new theme shows an
eyebrow that names another page as a crumb, a link back to it (DS-80), and says the same in the
page's data (DS-184). The live theme doesn't read the field. No theme file changes.

  python3 proposals/store-writes/afk_crumbs.py set     # the variables for metafieldsSet
  python3 proposals/store-writes/afk_crumbs.py undo    # the variables for metafieldsDelete
  python3 proposals/store-writes/afk_crumbs.py check   # the pages against the snapshot

The two calls, checked against the Admin API's schema:

  mutation SetEyebrows($metafields: [MetafieldsSetInput!]!) {
    metafieldsSet(metafields: $metafields) { metafields { id value } userErrors { field message code } } }
  mutation ClearEyebrows($metafields: [MetafieldIdentifierInput!]!) {
    metafieldsDelete(metafields: $metafields) { deletedMetafields { ownerId key } userErrors { field message } } }

The pages and their IDs come from the before-snapshot, so a page that has since gained an
eyebrow, or gone, stops the run. The snapshot holds the 14 pages as they were; REMOVED names the
one whose crumb was written and taken off again the same day, so set and undo leave it alone.
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
BEFORE = json.loads((HERE / "snapshots" / "afk-crumbs-2026-09-29-before.json").read_text())

# The page each page belongs to, as the pages' own cards lead to them: Classes and camps and
# Schools and teachers list their programmes as cards, and Artists for Kids' menu group lists
# its four pages. The words are the crumb's label.
CRUMBS = {
    "Classes and camps": ["after-school-art", "day-camps", "paradise-valley-summer-camp"],
    "Schools and teachers": [
        "gallery-program",
        "artists-in-residence",
        "studio-art-academy",
        "learning-guides",
        "learning-kits",
        "artreach-videos",
    ],
    "Artists for Kids": [
        "classes-and-camps",
        "schools-and-teachers",
        "awards-and-scholarships",
        "support-artists-for-kids",
    ],
}

# Professional Development is a programme in the Programming rows, which stay in one place from
# view to view (DS-146): a crumb above its title moved them 33 px. The rows are its way around,
# as they are for the four public programmes, which have no crumb either.
REMOVED = {"professional-development": "Schools and teachers"}


def handleize(words):
    """As Liquid's handleize filter does, for these plain names."""
    return re.sub(r"[^a-z0-9]+", "-", words.lower()).strip("-")


def rows():
    pages = {p["handle"]: p for p in BEFORE["pages"]}
    out = []
    for words, handles in CRUMBS.items():
        assert handleize(words) in BEFORE["targets"], f"{words} names no page"
        for handle in handles:
            page = pages[handle]
            assert page["eyebrow"] is None, f"{handle} had an eyebrow already"
            assert handle != handleize(words), f"{handle} would name itself"
            out.append((page, words))
    assert len(out) == 13 and len({p["id"] for p, _ in out}) == 13
    assert not REMOVED.keys() & {p["handle"] for p, _ in out}
    return out


def main(argv):
    step = argv[1] if len(argv) > 1 else "check"
    if step == "set":
        print(json.dumps({"metafields": [
            {"ownerId": page["id"], "namespace": "custom", "key": "eyebrow", "value": words}
            for page, words in rows()
        ]}, indent=2))
    elif step == "undo":
        print(json.dumps({"metafields": [
            {"ownerId": page["id"], "namespace": "custom", "key": "eyebrow"} for page, _ in rows()
        ]}, indent=2))
    else:
        for page, words in rows():
            print(f"{page['handle']:30} {page['id']:36} -> {words} (/pages/{handleize(words)})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
