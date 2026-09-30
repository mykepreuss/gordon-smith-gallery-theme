#!/usr/bin/env python3
"""About Artists for Kids, a page of its own under About, modelled on the Smith Foundation's page
(Michael, 2026-09-29: "We want to create a new about page for Artists for Kids, it should be
modelled after the Smith Foundation About page in that section. We want it under About and this
content to be moved to it": the team and the History part of the Artists for Kids page).

The Foundation's page is a hero with the annual report as its button, a short text with no
heading, then its card groups. The new page is the same: the first portfolio print as an artwork
hero, with its caption (as P-23 had it), the annual report as its button, the history as its
text, then the team. The Artists for Kids page keeps its opening text and its programmes. The text
is the gallery's, moved word for word; only the "History" and "Annual Report" headings stay behind,
since the page's title says it and the report is its button.

  python3 proposals/store-writes/afk_about.py create   # pageCreate variables: the new page
  python3 proposals/store-writes/afk_about.py links    # menuUpdate and metaobjectUpdate variables
  python3 proposals/store-writes/afk_about.py hub      # pageUpdate and metafieldsSet variables
  python3 proposals/store-writes/afk_about.py undo     # the same calls, back to the snapshot
  python3 proposals/store-writes/afk_about.py check    # what moves where, from the snapshot

The order is create, links, hub, so the history is never off the site. Each step reads from the
before-snapshot, so a change to the store since then should be read into a new snapshot first.

The calls, checked against the Admin API's schema:

  mutation CreatePage($page: PageCreateInput!) {
    pageCreate(page: $page) { page { id handle } userErrors { field message code } } }
  mutation UpdateMenu($id: ID!, $title: String!, $handle: String, $items: [MenuItemUpdateInput!]!) {
    menuUpdate(id: $id, title: $title, handle: $handle, items: $items) { menu { id } userErrors { field message code } } }
  mutation UpdateCard($id: ID!, $metaobject: MetaobjectUpdateInput!) {
    metaobjectUpdate(id: $id, metaobject: $metaobject) { metaobject { id } userErrors { field message code } } }
  mutation UpdatePage($id: ID!, $page: PageUpdateInput!) {
    pageUpdate(id: $id, page: $page) { page { id } userErrors { field message code } } }
  mutation SetFields($metafields: [MetafieldsSetInput!]!) {
    metafieldsSet(metafields: $metafields) { metafields { id key } userErrors { field message code } } }
  mutation DeletePage($id: ID!) { pageDelete(id: $id) { deletedPageId userErrors { field message code } } }
"""
import copy
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
BEFORE = json.loads((HERE / "snapshots" / "afk-about-2026-09-29-before.json").read_text())
CREATED = HERE / "created" / "afk-about.json"

HANDLE = "about-artists-for-kids"
TITLE = "About Artists for Kids"
MENU_LABEL = "About Artists for Kids"
SITE = "https://gordonsmithgallery.com"
REPORT = SITE + "/cdn/shop/files/afk-annual-report-2024-2025.pdf"
TEAM = "gid://shopify/Metaobject/609458585897"  # card group afk-team
# The page's description for search engines, as the other pages' (DS-160). Michael's to approve.
DESCRIPTION = (
    "How Artists for Kids began in 1989 with Gordon Smith, Jack Shadbolt and Bill Reid, "
    "its Limited Edition Portfolio, its team and its annual report."
)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def split_hub():
    """The hub's text before History, the history without the print, the print's caption."""
    body = BEFORE["hub"]["body"]
    opening, rest = body.split("\n<h2>History</h2>\n")
    history, report = rest.split("\n<h3>Annual Report</h3>\n")
    assert report == (
        '<p><a class="gs-cta-link" href="/cdn/shop/files/afk-annual-report-2024-2025.pdf">'
        "Annual Report 2024-2025 (PDF)</a></p>"
    ), report
    figure = re.search(r'\n<figure class="gs-figure--artwork">.*?</figure>', history, flags=re.S)
    assert "Reid_REID002_Xhuwaji_HaidaGrizzly" in figure.group(0)
    caption = plain(re.search(r"<figcaption>(.*?)</figcaption>", figure.group(0)).group(1))
    history = history.replace(figure.group(0), "")
    assert history.startswith("<p>Artists for Kids was founded in 1989"), history[:60]
    assert history.count("<p>") == 7 and "<h" not in history and "<figure" not in history
    assert opening.count("<p>") == 2 and opening.count("<figure>") == 1 and "<h" not in opening
    assert caption == "Bill Reid, (Canadian, 1920 – 1998) XHUWAJI/Haida Grizzly Bear, (1990) Serigraph, 22 in x 22 in.", caption
    return opening, history, caption


def field(key, kind, value):
    return {"namespace": "custom", "key": key, "type": kind, "value": value}


def create():
    _, history, caption = split_hub()
    return {"page": {
        "title": TITLE,
        "handle": HANDLE,
        "templateSuffix": "programme",
        "isPublished": True,
        "body": history,
        "metafields": [
            field("hero_image", "file_reference", BEFORE["reid_print"]["id"]),
            field("hero_is_artwork", "boolean", "true"),
            field("hero_caption", "single_line_text_field", caption),
            field("programme", "single_line_text_field", "Artists for Kids"),
            field("eyebrow", "single_line_text_field", "Artists for Kids"),
            field("cta", "link", json.dumps({"text": "Annual Report 2024-2025", "url": REPORT})),
            field("card_groups", "list.metaobject_reference", json.dumps([TEAM])),
            field("release_description", "multi_line_text_field", DESCRIPTION),
        ],
    }}


def menu_input(items):
    def clean(item):
        out = {k: item[k] for k in ("id", "title", "type") if k in item}
        if item.get("resourceId"):
            out["resourceId"] = item["resourceId"]
        if item.get("url"):
            out["url"] = item["url"]
        out["items"] = [clean(i) for i in item.get("items", [])]
        return out
    m = BEFORE["menu"]
    return {"id": m["id"], "title": m["title"], "handle": m["handle"], "items": [clean(i) for i in items]}


def new_page_id():
    if not CREATED.exists():
        sys.exit(f"Run create first and write the new page's ID to {CREATED.name}")
    return json.loads(CREATED.read_text())["page"]


def links():
    items = copy.deepcopy(BEFORE["menu"]["items"])
    about = next(i for i in items if i["title"] == "About")
    assert [i["title"] for i in about["items"]][-1] == "The Smith Foundation"
    about["items"].append({"title": MENU_LABEL, "type": "PAGE", "resourceId": new_page_id(), "items": []})
    card = BEFORE["about_us_card"]
    link = json.loads(card["link"])
    assert link == {"text": "More about Artists for Kids", "url": SITE + "/pages/artists-for-kids"}, link
    link["url"] = SITE + "/pages/" + HANDLE
    return {
        "menuUpdate": menu_input(items),
        "metaobjectUpdate": {"id": card["id"], "metaobject": {"fields": [{"key": "link", "value": json.dumps(link)}]}},
    }


def hub():
    opening, _, _ = split_hub()
    groups = BEFORE["hub"]["card_groups"]["value"]
    assert groups[-1] == TEAM
    return {
        "pageUpdate": {"id": BEFORE["hub"]["id"], "page": {"body": opening}},
        "metafieldsSet": {"metafields": [{
            "ownerId": BEFORE["hub"]["id"], "namespace": "custom", "key": "card_groups",
            "type": "list.metaobject_reference", "value": json.dumps(groups[:-1]),
        }]},
    }


def undo():
    """Back to the snapshot, in the reverse order: the hub, the links, then the page."""
    card = BEFORE["about_us_card"]
    return {
        "1 pageUpdate": {"id": BEFORE["hub"]["id"], "page": {"body": BEFORE["hub"]["body"]}},
        "2 metafieldsSet": {"metafields": [{
            "ownerId": BEFORE["hub"]["id"], "namespace": "custom", "key": "card_groups",
            "type": "list.metaobject_reference", "value": json.dumps(BEFORE["hub"]["card_groups"]["value"]),
        }]},
        "3 menuUpdate": menu_input(BEFORE["menu"]["items"]),
        "4 metaobjectUpdate": {"id": card["id"], "metaobject": {"fields": [{"key": "link", "value": card["link"]}]}},
        "5 pageDelete": {"id": new_page_id() if CREATED.exists() else "<the new page's ID>"},
    }


def check():
    opening, history, caption = split_hub()
    print(f"New page /pages/{HANDLE}, '{TITLE}', template programme, crumb 'Artists for Kids'")
    print(f"  hero: the Reid print as an artwork, caption: {caption}")
    print(f"  button: Annual Report 2024-2025 -> {REPORT}")
    print(f"  text: {history.count('<p>')} paragraphs, from '{plain(history)[:60]}...'")
    print(f"  card groups: afk-team")
    print(f"  description ({len(DESCRIPTION)} characters): {DESCRIPTION}")
    print(f"Menu: About gets '{MENU_LABEL}' after The Smith Foundation")
    print(f"About Us: 'More about Artists for Kids' -> /pages/{HANDLE}")
    print(f"Artists for Kids page: text is its opening ({opening.count('<p>')} paragraphs and the Paradise Valley photo);")
    print(f"  card groups: {', '.join(BEFORE['hub']['card_groups']['handles'][:-1])}")


def main(argv):
    step = argv[1] if len(argv) > 1 else "check"
    steps = {"create": create, "links": links, "hub": hub, "undo": undo}
    if step in steps:
        print(json.dumps(steps[step](), indent=2, ensure_ascii=False))
    else:
        check()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
