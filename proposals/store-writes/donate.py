#!/usr/bin/env python3
"""The Donate page pass (DS-60, Michael, 2026-09-26: "The improvements we made to /pages/volunteer
we need to look at /pages/donate and also improve"). Builds on the staged text of the DS-53 pass
(donate_gm.py), so no word is retyped, and checks none changed. Prints the variables for each
step's mutation.

  python3 proposals/store-writes/donate.py staged   # metafieldsSet: the staged text and the button
  python3 proposals/store-writes/donate.py cards    # metaobjectUpdate: Email and Phone get links
  python3 proposals/store-writes/donate.py group    # metaobjectUpdate: "How to give", without Online Form
  python3 proposals/store-writes/donate.py review   # the staged text

As on Volunteer (DS-58), the page's ways to act are what visitors can act on:
- The last cards are how to give. Email and Phone get links ("Email us", "Call us"), so a phone can
  open the email or dial the number. Online Form leaves the group: it points to a form "above"
  that isn't on the page (gallery question 3.1). Its entry stays, ready for when there is one.
- Their heading, "Ways To Give", becomes "How to give", so it no longer reads like the text's
  "Ways to Support" heading just above it: one says what kinds of gift there are, the other how
  to send one.
- The hero button says what it does, "Make a gift", and still jumps to those cards.
- A photo of a class visit sits beside "Ways to Support", whose $150 example is exactly that.

Then (Michael, 2026-09-26: "we can improve the presentation of the The impact of your gift and
Ways to Support text sections"): both sections' lists become lists of points (`gs-points`), and
the three example amounts a row of amounts (`gs-amounts`), each amount in bold. Only classes and
the bold on the amounts are added; the words and their order are the same.

  python3 proposals/store-writes/donate.py points   # metafieldsSet: the staged text with them
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import donate_gm  # noqa: E402  (the staged text as it is, DS-53)

BEFORE = json.loads((HERE / "snapshots" / "donate-2026-09-26-before.json").read_text())
PAGE = BEFORE["page"]
PHOTO = BEFORE["class_visit_photo"]
PHOTO_ALT = "Students sit on the gallery floor with a guide during a class visit"
SUPPORT = "<h2>Ways to Support</h2>"
CARDS = BEFORE["cards"]
EMAIL = "admin@smithfoundation.ca"
PHONE = "604-998-8563"


def staged():
    body = donate_gm.donate_staged()
    assert body == PAGE["custom_fields"]["release_body"]["value"], "Donate's staged text changed since the snapshot"
    assert body.count(SUPPORT) == 1
    w = 1200
    h = round(PHOTO["height"] * w / PHOTO["width"])
    photo = (f'<figure><img src="{html.escape(PHOTO["url"])}&amp;width={w}" alt="{PHOTO_ALT}" '
             f'width="{w}" height="{h}" loading="lazy"></figure>')
    new = body.replace(SUPPORT, SUPPORT + "\n" + photo, 1)
    assert donate_gm.words(new) == donate_gm.words(body), "Words changed"
    return new


AMOUNTS = ["$75", "$150", "$500"]


def presented():
    """The staged text with its two lists as points and the example amounts as a row of amounts."""
    body = staged()
    impact = "<p>Your donation supports programs that:</p>\n<ul>"
    support = "<p>Every contribution makes a difference:</p>\n<ul>"
    examples = "For example:\n<ul>"
    for marker in (impact, support, examples):
        assert body.count(marker) == 1, marker
    body = body.replace(impact, impact[:-4] + '<ul class="gs-points">', 1)
    body = body.replace(support, support[:-4] + '<ul class="gs-points">', 1)
    body = body.replace(examples, examples[:-4] + '<ul class="gs-amounts">', 1)
    for amount in AMOUNTS:
        item = f"<li>{amount} can "
        assert body.count(item) == 1, amount
        body = body.replace(item, f"<li><strong>{amount}</strong> can ", 1)
    assert donate_gm.words(body) == donate_gm.words(staged()), "Words changed"
    return body


def page_fields():
    url = json.loads(PAGE["custom_fields"]["cta"]["value"])["url"]
    return {"metafields": [
        {"ownerId": PAGE["id"], "namespace": "custom", "key": "release_body", "type": "multi_line_text_field", "value": staged()},
        {"ownerId": PAGE["id"], "namespace": "custom", "key": "cta", "type": "link", "value": json.dumps({"text": "Make a gift", "url": url})},
    ]}


def card_links():
    # The numbers and address stay in each card's text, as the gallery wrote them.
    assert CARDS["donate-email"]["text"].endswith(EMAIL) and CARDS["donate-phone"]["text"].endswith(PHONE)
    return {
        CARDS["donate-email"]["id"]: {"fields": [{"key": "link", "value": json.dumps({"text": "Email us", "url": f"mailto:{EMAIL}"})}]},
        CARDS["donate-phone"]["id"]: {"fields": [{"key": "link", "value": json.dumps({"text": "Call us", "url": "tel:+1" + PHONE.replace("-", "")})}]},
    }


def group():
    g = BEFORE["card_group"]
    cards = [c for c in g["cards"] if c != CARDS["donate-online-form"]["id"]]
    assert len(cards) == 3
    return {"id": g["id"], "metaobject": {"fields": [{"key": "heading", "value": "How to give"}, {"key": "cards", "value": json.dumps(cards)}]}}


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step == "staged":
        print(json.dumps(page_fields(), indent=2, ensure_ascii=False))
    elif step == "cards":
        print(json.dumps(card_links(), indent=2))
    elif step == "group":
        print(json.dumps(group(), indent=2))
    elif step == "points":
        print(json.dumps({"metafields": [{"ownerId": PAGE["id"], "namespace": "custom", "key": "release_body",
                                          "type": "multi_line_text_field", "value": presented()}]}, indent=2, ensure_ascii=False))
    elif step == "review":
        print(presented())
    else:
        sys.exit(__doc__)
