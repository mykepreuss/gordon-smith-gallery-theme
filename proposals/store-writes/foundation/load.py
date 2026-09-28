#!/usr/bin/env python3
"""The Smith Foundation's old site into the store: the writes that go through the Shopify CLI
(`shopify store execute`, as the collection's and Artists for Kids' did). Content is in content.py.
Each step is safe to run again: entries are upserted by handle.

  python3 load.py snapshot        the exhibitions and the Foundation's cards as they are now, to
                                  ../snapshots/foundation-2026-09-28-before.json (run once, first)
  python3 load.py exhibitions     the 17 older exhibitions (new, active) and the nine that gain text,
                                  credits, pictures or Videos and publications (P-41, P-45, P-46)
  python3 load.py cards           the Foundation page's scholarship and gala cards get their links;
                                  a Supporters card joins "Get involved" (P-42, P-57)

Definitions, pages, page fields and the menu go through the Shopify connector, which has page
access: `python3 content.py definition | pages | page-fields | menu` print their variables.
Created IDs go to ../created/foundation-*.json.

Undo: ../snapshots/foundation-2026-09-28-before.json holds every changed entry's fields as they
were; `python3 load.py restore` writes them back and deletes the new exhibitions and card.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "collection"))
sys.path.insert(0, str(HERE))
from images import execute  # noqa: E402

import content  # noqa: E402

CREATED = HERE.parent / "created"
SNAPSHOT = HERE.parent / "snapshots" / "foundation-2026-09-28-before.json"

READ = """query Read($type: String!, $after: String) {
  metaobjects(type: $type, first: 50, after: $after) {
    nodes { id handle updatedAt capabilities { publishable { status } } fields { key value } }
    pageInfo { hasNextPage endCursor }
  }
}"""
UPSERT = """mutation Upsert($handle: MetaobjectHandleInput!, $metaobject: MetaobjectUpsertInput!) {
  metaobjectUpsert(handle: $handle, metaobject: $metaobject) { metaobject { id handle } userErrors { field message code } }
}"""
DELETE = """mutation Delete($id: ID!) { metaobjectDelete(id: $id) { deletedId userErrors { field message } } }"""


def read(type_):
    out, after = {}, None
    while True:
        page = execute(READ, {"type": type_, "after": after})["metaobjects"]
        for n in page["nodes"]:
            out[n["handle"]] = {"id": n["id"], "updatedAt": n["updatedAt"],
                                "status": n["capabilities"]["publishable"]["status"] if n["capabilities"].get("publishable") else None,
                                "fields": {f["key"]: f["value"] for f in n["fields"]}}
        if not page["pageInfo"]["hasNextPage"]:
            return out
        after = page["pageInfo"]["endCursor"]


def snapshot():
    if SNAPSHOT.exists():
        raise SystemExit(f"{SNAPSHOT.name} exists: the before-state is taken once")
    cards = read("card")
    groups = read("card_group")
    data = {"taken": "2026-09-28, before the Smith Foundation's old site moved in (proposals/smith-foundation-site.md)",
            "exhibitions": read("exhibition"),
            "cards": {h: c for h, c in cards.items() if h.startswith("foundation-")},
            "card_groups": {h: g for h, g in groups.items() if h == content.TAKE_PART_GROUP}}
    SNAPSHOT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(data['exhibitions'])} exhibitions, {len(data['cards'])} cards, {len(data['card_groups'])} group -> {SNAPSHOT}")


def upsert(type_, handle, fields, active=True):
    meta = {"fields": [{"key": k, "value": v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)}
                       for k, v in fields.items() if v not in (None, "", [], "[]")]}
    if active:
        meta["capabilities"] = {"publishable": {"status": "ACTIVE"}}
    r = execute(UPSERT, {"handle": {"type": type_, "handle": handle}, "metaobject": meta})["metaobjectUpsert"]
    if r["userErrors"]:
        raise RuntimeError(f"{handle}: {r['userErrors']}")
    return r["metaobject"]["id"]


def check_uploaded(value):
    s = value if isinstance(value, str) else json.dumps(value)
    if "not uploaded" in s or "(img:" in s:
        raise SystemExit(f"a file isn't uploaded yet: {s[:200]}")


def exhibitions():
    before = json.loads(SNAPSHOT.read_text())["exhibitions"]
    made = {}
    for e in content.older_exhibitions():
        fields = {k: v for k, v in e.items() if k != "handle"}
        for v in fields.values():
            check_uploaded(v)
        if isinstance(fields.get("collection_works"), list):
            fields["collection_works"] = json.dumps(fields["collection_works"])
        made[e["handle"]] = upsert("exhibition", e["handle"], fields)
        print(f"new {e['handle']}", flush=True)
    for handle, fields in content.existing_exhibitions().items():
        fields = dict(fields)
        append = fields.pop("append", None)
        if append:
            body = json.loads(before[handle]["fields"]["body"])
            body["children"] += append
            fields["body"] = json.dumps(body, ensure_ascii=False)
        for v in fields.values():
            check_uploaded(v)
        made[handle] = upsert("exhibition", handle, fields, active=False)
        print(f"updated {handle}", flush=True)
    (CREATED / "foundation-exhibitions.json").write_text(json.dumps(made, indent=1, sort_keys=True) + "\n")


def cards():
    before = json.loads(SNAPSHOT.read_text())
    made = {}
    for handle, (title, url) in content.CARD_LINKS.items():
        made[handle] = upsert("card", handle, {"link": json.dumps({"text": "", "url": content.SITE + url})}, active=False)
    c = content.SUPPORTERS_CARD
    made[c["handle"]] = upsert("card", c["handle"], {
        "title": c["title"], "image": content.img(c["image"]), "text": content.txt(*c["text_block"]),
        "link": json.dumps({"text": "", "url": content.SITE + c["url"]})}, active=False)
    group = before["card_groups"][content.TAKE_PART_GROUP]
    ids = json.loads(group["fields"]["cards"])
    if made[c["handle"]] not in ids:
        ids.append(made[c["handle"]])
    made[content.TAKE_PART_GROUP] = upsert("card_group", content.TAKE_PART_GROUP, {"cards": json.dumps(ids)}, active=False)
    (CREATED / "foundation-cards.json").write_text(json.dumps(made, indent=1, sort_keys=True) + "\n")
    print(json.dumps(made, indent=1))


def restore():
    """Undo: the changed entries' fields back as they were; the new exhibitions and card deleted."""
    before = json.loads(SNAPSHOT.read_text())
    new = {e["handle"] for e in content.older_exhibitions()} - set(before["exhibitions"])
    made = json.loads((CREATED / "foundation-exhibitions.json").read_text())
    for handle in new:
        if handle in made:
            execute(DELETE, {"id": made[handle]})
    for handle in content.existing_exhibitions():
        old = before["exhibitions"][handle]["fields"]
        execute(UPSERT, {"handle": {"type": "exhibition", "handle": handle},
                         "metaobject": {"fields": [{"key": k, "value": v or ""} for k, v in old.items()]}})
    cards_made = json.loads((CREATED / "foundation-cards.json").read_text())
    for handle in content.CARD_LINKS:
        link = before["cards"][handle]["fields"].get("link")
        execute(UPSERT, {"handle": {"type": "card", "handle": handle},
                         "metaobject": {"fields": [{"key": "link", "value": link or ""}]}})
    group = before["card_groups"][content.TAKE_PART_GROUP]["fields"]["cards"]
    execute(UPSERT, {"handle": {"type": "card_group", "handle": content.TAKE_PART_GROUP},
                     "metaobject": {"fields": [{"key": "cards", "value": group}]}})
    execute(DELETE, {"id": cards_made[content.SUPPORTERS_CARD["handle"]]})


if __name__ == "__main__":
    step = sys.argv[1]
    {"snapshot": snapshot, "exhibitions": exhibitions, "cards": cards, "restore": restore}.get(
        step, lambda: sys.exit(__doc__))()
