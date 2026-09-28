#!/usr/bin/env python3
"""Store writes from the whole-site design review (proposals/site-design-review.md, 2026-09-27).
Our own labels and markup only: no word of the gallery's changes, and nothing the live site shows.
Prints the variables for each mutation.

  python3 proposals/store-writes/site_review.py pages     # metafieldsSet: staged text and buttons
  python3 proposals/store-writes/site_review.py stitched  # metaobjectUpdate: Stitched's credits
  python3 proposals/store-writes/site_review.py menu      # menuUpdate: the review menu

- Donate's staged text: its camp links go to the camps' pages on this site instead of the old
  Artists for Kids site (P-30); each page links on to registration.
- FAQ and Contact get staged text (DS-39): the live text with its line-break paragraphs made
  paragraphs, so they take the prose rhythm, and Contact's phone number and email addresses as
  links (§6.2). The FAQ's question headings stay as they are (held).
- Stitched's credits: Artists For Kids and the Foundation link to their pages here; the Foundation's
  link was broken (it pointed at a non-existent address on smithfoundation.co).
- The review menu: Upcoming events joins Programs, after Public programs, so the page that lists
  every event can be found from the menu (its label is for the gallery to confirm, 8.x).

The Artists for Kids changes (Support's ways to give, the hub's button, Awards' requirement links,
the NVSD paragraph) are in artists-for-kids/content.py and go with its page-field and card steps.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import donate  # noqa: E402  (Donate's staged text as it is, DS-60)

DONATE = "gid://shopify/Page/155885863209"
FAQ = "gid://shopify/Page/154942865705"
CONTACT = "gid://shopify/Page/140660572457"
STITCHED = "gid://shopify/Metaobject/608388448553"
MENU = "gid://shopify/Menu/305860739369"
UPCOMING_EVENTS = "gid://shopify/Page/155669168425"

CAMPS = [
    ('<a href="https://artistsforkids.sd44.ca/learn/spring--summer-day-camps/" rel="noopener" target="_blank">Spring and Summer art camps</a>',
     '<a href="/pages/day-camps">Spring and Summer art camps</a>'),
    ('<a href="https://artistsforkids.sd44.ca/learn/paradise-valley-summer-camps/" rel="noopener" target="_blank">Paradise Valley Summer School of Visual Art</a>',
     '<a href="/pages/paradise-valley-summer-camp">Paradise Valley Summer School of Visual Art</a>'),
]


def donate_staged():
    body = donate.presented()
    for old, new in CAMPS:
        assert body.count(old) == 1, old
        body = body.replace(old, new)
    return body


# The live FAQ text (2026-09-27), with the last answer's line break made two paragraphs.
FAQ_STAGED = """<h2>Frequently Asked Questions</h2>
<h3>Are all prints limited edition?</h3>
<p>Yes. All prints offered through Artists for Kids are limited editions created in collaboration with Canadian artists and printmakers. The first edition of a limited edition series is archived in the Artists For Kids and the Gordon Smith Gallery Permanent Collection.</p>
<h3>Will the artwork look exactly like the images online?</h3>
<p>We make every effort to display artwork accurately. However, colours may vary slightly depending on your screen or device.</p>
<h3>What payment methods do you accept?</h3>
<p>Payments are processed securely through Shopify Payments. Accepted methods may include major credit cards and other options presented at checkout.</p>
<h3>How long does shipping take?</h3>
<p>Unframed prints are typically shipped within 3–5 business days. Delivery time will depend on your location.</p>
<h3>How much is shipping?</h3>
<p>Shipping costs are calculated and confirmed at checkout (or during the order process, depending on your location and purchase).</p>
<h3>Do you ship framed prints?</h3>
<p>Framed prints are available for pickup only. Arranged courier delivery can be arranged at the customer's expense.</p>
<h3>Do you offer in-store pickup?</h3>
<p>Yes! We offer free in-store pickup.</p>
<h3>How long does pickup take?</h3>
<p>Unframed prints: ready in 1–2 business days. Framed prints: ready in 2–3 weeks.</p>
<p>We will contact you when your order is ready!</p>"""

# The live Contact text (2026-09-27): each label with its lines as one paragraph, the phone number
# and email addresses as links, Office Hours its own paragraph.
CONTACT_STAGED = """<p><strong>Artists For Kids and the Gordon Smith Gallery of Canadian Art</strong></p>
<p><strong>Address</strong><br>2121 Lonsdale Avenue<br>North Vancouver, BC V7M 2K6</p>
<p><strong>Telephone</strong><br><a href="tel:+16049033798">(604) 903-3798</a></p>
<p><strong>Email</strong><br>Artists For Kids: <a href="mailto:artistsforkids@sd44.ca">artistsforkids@sd44.ca</a><br>Gordon and Marion Smith Foundation: <a href="mailto:admin@smithfoundation.ca">admin@smithfoundation.ca</a></p>
<p><strong>Office Hours</strong><br>Monday to Friday 8:30am - 4:30pm<br>Closed for Statutory Holidays, July and August</p>"""


def pages():
    return {"metafields": [
        {"ownerId": DONATE, "namespace": "custom", "key": "release_body", "type": "multi_line_text_field", "value": donate_staged()},
        {"ownerId": FAQ, "namespace": "custom", "key": "release_body", "type": "multi_line_text_field", "value": FAQ_STAGED},
        {"ownerId": CONTACT, "namespace": "custom", "key": "release_body", "type": "multi_line_text_field", "value": CONTACT_STAGED},
    ]}


STITCHED_LINKS = {
    "https://www.sd44.ca/school/artistsforkids/Pages/default.aspx#/=": "/pages/artists-for-kids",
    "https://smithfoundation.co/exhibitions-items/stitched-merging-photography-and-textile-practices/smithfoundation.ca": "/pages/the-smith-foundation",
}


def stitched(before):
    """Stitched's credits (rich text JSON, as read from the store) with the two links changed."""
    doc = json.loads(before)
    n = 0

    def walk(node):
        nonlocal n
        if node.get("type") == "link" and node.get("url") in STITCHED_LINKS:
            node["url"] = STITCHED_LINKS[node["url"]]
            n += 1
        for child in node.get("children", []):
            walk(child)

    walk(doc)
    assert n == 2, n
    return {"id": STITCHED, "metaobject": {"fields": [{"key": "credits", "value": json.dumps(doc, ensure_ascii=False)}]}}


def menu(before):
    """The review menu with Upcoming events after Public programs under Programs."""
    items = json.loads(before)

    def keep(item):
        out = {"id": item["id"], "title": item["title"], "type": item["type"], "url": item["url"]}
        if item.get("resourceId"):
            out["resourceId"] = item["resourceId"]
        out["items"] = [keep(i) for i in item.get("items", [])]
        return out

    items = [keep(i) for i in items]
    programs = next(i for i in items if i["title"] == "Programs")
    assert not any(i["url"] == "/pages/upcoming-events" for i in programs["items"])
    at = next(n for n, i in enumerate(programs["items"]) if i["title"] == "Public programs") + 1
    programs["items"].insert(at, {"title": "Upcoming events", "type": "PAGE", "resourceId": UPCOMING_EVENTS,
                                  "url": "/pages/upcoming-events", "items": []})
    return {"id": MENU, "title": "Main menu (new theme)", "handle": "new-theme-main", "items": items}


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step == "pages":
        print(json.dumps(pages(), indent=1, ensure_ascii=False))
    elif step == "stitched":
        print(json.dumps(stitched(sys.stdin.read()), indent=1, ensure_ascii=False))
    elif step == "menu":
        print(json.dumps(menu(sys.stdin.read()), indent=1, ensure_ascii=False))
    else:
        sys.exit(__doc__)
