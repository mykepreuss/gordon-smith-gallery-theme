#!/usr/bin/env python3
"""The Volunteer page pass (DS-58, Michael, 2026-09-26: "Proceed", after the review of
/pages/volunteer). Builds the payloads from the page's own text, so no word of the gallery's is
retyped, and checks that none changed. Prints the variables for each step's mutation.

  python3 proposals/store-writes/volunteer.py cards           # metaobjectCreate, one per card
  python3 proposals/store-writes/volunteer.py group <created> # metaobjectCreate, with the cards' IDs
  python3 proposals/store-writes/volunteer.py fields <created-group>  # metafieldsSet on the page
  python3 proposals/store-writes/volunteer.py review          # the staged text and the cards

The two roles, which were paragraphs opening with a bold name, become two cards between the
opening sentence and the rest (the programme layout, DS-51). The rest goes under a "Join the team"
heading, beside a photo from the page's old banner of an event, and ends with how to apply: the
form and a contact link, so the page no longer ends without a way to act. The hero button says
what it does: "Download the form".
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
BEFORE = json.loads((HERE / "snapshots" / "volunteer-2026-09-26-before.json").read_text())
PAGE = BEFORE["page"]
FORM = "https://gordonsmithgallery.com/cdn/shop/files/GSF-Volunteer-Application-Form_202603.pdf"
FORM_PATH = "/cdn/shop/files/GSF-Volunteer-Application-Form_202603.pdf"
PHOTO = BEFORE["event_photo"]
PHOTO_ALT = "Guests are served drinks at a gallery event"
HEADING = "Join the team"
ROLES = [("Gallery Attendant", "volunteer-gallery-attendant"), ("Event Assistant", "volunteer-event-assistant")]


def words(s):
    """The text a reader sees, for checking nothing was reworded."""
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s).replace("\xa0", " ")).strip()


def parts():
    first, second = re.findall(r"<p>(.*?)</p>", PAGE["body"], flags=re.S)
    pieces = [x.strip() for x in re.split(r"<br\s*/?>\s*<br\s*/?>", first)]
    assert len(pieces) == 4, "Volunteer's text changed since the snapshot"
    intro, attendant, assistant, values = pieces
    roles = {}
    for piece, (name, _) in zip((attendant, assistant), ROLES):
        m = re.fullmatch(rf"<strong>{name}</strong>: (.+)", piece, flags=re.S)
        assert m, name
        text = m.group(1).strip()
        roles[name] = text[0].upper() + text[1:]  # the sentence now starts the card
    return words(intro), roles, words(values), words(second)


def staged_text():
    intro, _, values, students = parts()
    w = 1200
    h = round(PHOTO["height"] * w / PHOTO["width"])
    photo = (f'<figure><img src="{html.escape(PHOTO["url"])}&amp;width={w}" alt="{PHOTO_ALT}" '
             f'width="{w}" height="{h}" loading="lazy"></figure>')
    apply = (f'<p>To apply, fill in the <a href="{FORM_PATH}">volunteer form (PDF)</a>. '
             'Questions? <a href="/pages/contact">Contact us</a>.</p>')
    return "\n".join([f"<p>{html.escape(intro, quote=False)}</p>", f"<h2>{HEADING}</h2>", photo,
                      f"<p>{html.escape(values, quote=False)}</p>", f"<p>{html.escape(students, quote=False)}</p>", apply])


def check():
    """Every word of the page is still there, in order: the staged text without the new heading
    and apply line, with the roles back in their place, reads as the page did. Only the first
    letter of each role's sentence changed case."""
    intro, roles, values, students = parts()
    rebuilt = " ".join([intro] + [f"{n}: {t[0].lower() + t[1:]}" for n, t in roles.items()] + [values, students])
    assert rebuilt == words(PAGE["body"]), "Words changed"
    staged = staged_text()
    kept = re.sub(rf"<h2>{HEADING}</h2>|<figure>.*?</figure>|<p>To apply.*?</p>", "", staged, flags=re.S)
    assert words(kept) == " ".join([intro, values, students])


def cards():
    _, roles, _, _ = parts()
    return {h.replace("-", "_"): {"type": "card", "handle": h, "fields": [
        {"key": "title", "value": name}, {"key": "text", "value": roles[name]}]} for name, h in ROLES}


def group(created):
    ids = {v["metaobject"]["handle"]: v["metaobject"]["id"] for v in created.values()}
    return {"volunteer_roles": {"type": "card_group", "handle": "volunteer-roles",
                                "fields": [{"key": "cards", "value": json.dumps([ids[h] for _, h in ROLES])}]}}


def fields(created_group):
    gid = created_group["volunteer_roles"]["metaobject"]["id"]
    return {"metafields": [
        {"ownerId": PAGE["id"], "namespace": "custom", "key": "card_groups", "type": "list.metaobject_reference", "value": json.dumps([gid])},
        {"ownerId": PAGE["id"], "namespace": "custom", "key": "release_body", "type": "multi_line_text_field", "value": staged_text()},
        {"ownerId": PAGE["id"], "namespace": "custom", "key": "cta", "type": "link",
         "value": json.dumps({"text": "Download the form", "url": FORM})},
    ]}


if __name__ == "__main__":
    check()
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    out = None
    if step == "cards":
        out = cards()
    elif step == "group":
        out = group(json.loads(pathlib.Path(sys.argv[2]).read_text()))
    elif step == "fields":
        out = fields(json.loads(pathlib.Path(sys.argv[2]).read_text()))
    elif step == "review":
        print(staged_text(), "\n")
        for c in cards().values():
            print(" / ".join(f["value"] for f in c["fields"]))
        sys.exit()
    else:
        sys.exit(__doc__)
    print(json.dumps(out, indent=2, ensure_ascii=False))
