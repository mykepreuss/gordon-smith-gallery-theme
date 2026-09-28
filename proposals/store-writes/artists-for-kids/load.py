#!/usr/bin/env python3
"""Artists for Kids into the store (proposals/artists-for-kids-integration.md; P-30 to P-40). The content
is in content.py; this runs the writes, in this order, each safe to run again (entries are upserted by
handle, definitions are skipped when they exist):

  python3 load.py definitions            prints the variables for the Lesson entry type (P-36,
                                         metaobjectDefinitionCreate) and the event's Keep off the home page
                                         field (P-37, metaobjectDefinitionUpdate), run through the Shopify
                                         connector: the CLI's app may not create store-owned types. Done
                                         2026-09-27 (../created/afk-definitions.json)
  python3 load.py lessons <export>       the 27 lessons, active, with their covers and the works that
                                         inspired them
  python3 load.py cards                  the cards and card groups (new and changed)
  python3 load.py events                 the educators' workshops, and the curator's tour's programme page

Through the Shopify CLI (`shopify store execute`, as the collection's import). Pages, their fields and
the menu go through the Shopify connector, which has page access: `python3 content.py pages` and
`content.py page-fields` print their variables. Created IDs go to ../created/afk-*.json.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "collection"))
from images import execute  # noqa: E402

import content  # noqa: E402

CREATED = HERE.parent / "created"
ARTWORK_DEF = "gid://shopify/MetaobjectDefinition/23770693929"
EVENT_DEF = "gid://shopify/MetaobjectDefinition/23753392425"
IMAGE = [{"name": "file_type_options", "value": json.dumps(["Image"])}]


def f(key, type_, name, description="", required=False, validations=None):
    out = {"key": key, "type": type_, "name": name, "required": required}
    if description:
        out["description"] = description
    if validations:
        out["validations"] = validations
    return out


def lesson_definition():
    return {"definition": {
        "type": "lesson", "name": "Lesson",
        "description": "An ArtReach video lesson from Artists for Kids. Its page is at /pages/lessons/<handle>, and the "
                       "ArtReach videos page lists every lesson, newest first by its Posted date.",
        "displayNameKey": "title",
        "access": {"storefront": "PUBLIC_READ"},
        "capabilities": {"publishable": {"enabled": True},
                         "renderable": {"enabled": True, "data": {"metaTitleKey": "title", "metaDescriptionKey": "making"}},
                         "onlineStore": {"enabled": True, "data": {"urlHandle": "lessons"}}},
        "fieldDefinitions": [
            f("title", "single_line_text_field", "Title", required=True),
            f("video", "url", "Video", "The video's YouTube address, for example https://www.youtube.com/watch?v=… "
              "It plays on the lesson's page.", required=True),
            f("posted", "date", "Posted", "The day the lesson was posted. The ArtReach videos page lists the newest first."),
            f("cover", "file_reference", "Cover image", "Shown on the lesson's card, at the video's shape (16:9). "
              "The video's own thumbnail works well.", validations=IMAGE),
            f("making", "multi_line_text_field", "We're making"),
            f("inspired_by", "rich_text_field", "We're inspired by", "The artworks and ideas the lesson starts from. "
              "Titles in italics."),
            f("works", "list.metaobject_reference", "Works from the collection", "The works named above that are in the "
              "Permanent Collection. They show as tiles on the lesson's page.",
              validations=[{"name": "metaobject_definition_id", "value": ARTWORK_DEF}]),
            f("grades", "single_line_text_field", "Suggested grade levels", "For example: Grades 4-7 & 8-9."),
            f("questions", "list.single_line_text_field", "We're wondering", "One question to an item."),
        ]}}


def event_field():
    return {"id": EVENT_DEF, "definition": {"fieldDefinitions": [{"create": f(
        "keep_off_home", "boolean", "Keep off the home page",
        "For events meant for a smaller audience, such as workshops for teachers. They still show on their programme "
        "page, their exhibition's page and Upcoming events.")}]}}


DEFS = """query { metaobjectDefinitions(first: 50) { nodes { id type fieldDefinitions { key } } } }"""
CREATE_DEF = """mutation($definition: MetaobjectDefinitionCreateInput!) {
  metaobjectDefinitionCreate(definition: $definition) { metaobjectDefinition { id type } userErrors { field message code } } }"""
UPDATE_DEF = """mutation($id: ID!, $definition: MetaobjectDefinitionUpdateInput!) {
  metaobjectDefinitionUpdate(id: $id, definition: $definition) { metaobjectDefinition { id type } userErrors { field message code } } }"""
UPSERT = """mutation($handle: MetaobjectHandleInput!, $metaobject: MetaobjectUpsertInput!) {
  metaobjectUpsert(handle: $handle, metaobject: $metaobject) { metaobject { id handle } userErrors { field message code } } }"""


def definitions():
    """The variables for the two definition mutations, for the Shopify connector."""
    print(json.dumps({"metaobjectDefinitionCreate": lesson_definition(), "metaobjectDefinitionUpdate": event_field()}, indent=1, ensure_ascii=False))


def definitions_by_cli():
    """Kept for reference: the CLI's app gets NOT_AUTHORIZED ("reserved for use by another application")."""
    have = {d["type"]: d for d in execute(DEFS, {})["metaobjectDefinitions"]["nodes"]}
    out = {}
    if "lesson" in have:
        out["lesson"] = have["lesson"]["id"]
    else:
        r = execute(CREATE_DEF, lesson_definition())["metaobjectDefinitionCreate"]
        if r["userErrors"]:
            raise RuntimeError(r["userErrors"])
        out["lesson"] = r["metaobjectDefinition"]["id"]
    if "keep_off_home" not in [k["key"] for k in have["event"]["fieldDefinitions"]]:
        r = execute(UPDATE_DEF, event_field())["metaobjectDefinitionUpdate"]
        if r["userErrors"]:
            raise RuntimeError(r["userErrors"])
    out["event"] = EVENT_DEF
    save("definitions", out)
    print(out)


def save(name, data):
    path = CREATED / f"afk-{name}.json"
    old = json.loads(path.read_text()) if path.exists() else {}
    old.update(data)
    path.write_text(json.dumps(old, indent=1, sort_keys=True, ensure_ascii=False))
    return old


def upsert_all(type_, entries, name):
    made = {}
    for handle, fields in entries:
        r = execute(UPSERT, {"handle": {"type": type_, "handle": handle},
                             "metaobject": {"fields": fields, "capabilities": {"publishable": {"status": "ACTIVE"}}}
                             if type_ in ("lesson", "event") else {"fields": fields}})["metaobjectUpsert"]
        if r["userErrors"]:
            raise RuntimeError(f"{handle}: {r['userErrors']}")
        made[handle] = r["metaobject"]["id"]
        print(f"{type_} {handle}", flush=True)
    return save(name, made)


def lessons(export):
    upsert_all("lesson", content.lesson_entries(export), "lessons")


GROUP = """query($h: MetaobjectHandleInput!) { metaobjectByHandle(handle: $h) { id field(key: "cards") { value } } }"""


def cards():
    made = upsert_all("card", content.card_entries(), "cards")
    upsert_all("card_group", content.group_entries(made), "card-groups")
    # Existing groups that gain a card at the end (Public programs, Donate's How to give).
    for handle, card_handle in content.GROUPS_EXTENDED:
        g = execute(GROUP, {"h": {"type": "card_group", "handle": handle}})["metaobjectByHandle"]
        ids = json.loads(g["field"]["value"])
        if made[card_handle] not in ids:
            ids.append(made[card_handle])
            upsert_all("card_group", [(handle, [{"key": "cards", "value": json.dumps(ids)}])], "card-groups-extended")


def events():
    pages = json.loads((CREATED / "afk-pages.json").read_text())
    upsert_all("event", content.event_entries(pages), "events")


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "definitions":
        definitions()
    elif step == "lessons":
        lessons(sys.argv[2])
    elif step == "cards":
        cards()
    elif step == "events":
        events()
