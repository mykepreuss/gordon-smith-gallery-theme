#!/usr/bin/env python3
"""The admin's help text under six fields, brought in line with the site's style and the staff
handbook (Michael, 2026-10-01: "Yes, update the help text"). Staff see it; visitors don't.

  python3 proposals/store-writes/help_text.py [--go]

Reads each field's description first and sends only what still differs. Without --go it prints
the changes. With --go it saves the descriptions it replaces to
snapshots/help-text-2026-10-01-before.json and writes the store's answers to
created/help-text-2026-10-01.json. Undo: send the snapshot's descriptions back the same way.
"""
import datetime
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gallery_answers import read  # noqa: E402
from release_run import execute, user_errors  # noqa: E402

# Entry fields: type, key, then the help text.
ENTRY = {
    ("exhibition", "curator_credit"): "The whole line as it should read, for example: Curated by Amelia Epp with support from the Artists for Kids team.",
    ("artwork", "year"): "As the work is dated, for example: 1994, or circa 1960s. Undated: n.d.",
    ("artwork", "edition"): "For example: 30/40, or AP for an artist's proof.",
    ("artist", "website"): "Kept from the old Artists page's links. The site doesn't show it.",
}
# Owner fields: owner type, namespace.key, then the help text.
OWNER = {
    ("PAGE", "custom.cta"): "One button under the title. Its label says what happens, for example: Register a Grade 5 class.",
    ("COLLECTION", "custom.photo_credit"): "Credit for the collection's image, for example: Photo by Rachel Topham.",
    ("PRODUCT", "custom.featured_frame"): "The print's frame, offered on the print's page as Framed. The frame is its own product: product type Frame, status Unlisted.",
}
ENTRY_Q = "mutation($id: ID!, $definition: MetaobjectDefinitionUpdateInput!) { metaobjectDefinitionUpdate(id: $id, definition: $definition) { metaobjectDefinition { type } userErrors { field message } } }"
OWNER_Q = "mutation($definition: MetafieldDefinitionUpdateInput!) { metafieldDefinitionUpdate(definition: $definition) { updatedDefinition { namespace key description } userErrors { field message } } }"


def calls():
    out = []
    for (kind, key), text in ENTRY.items():
        d = read("query($t: String!) { metaobjectDefinitionByType(type: $t) { id fieldDefinitions { key description } } }", {"t": kind})["metaobjectDefinitionByType"]
        now = {f["key"]: f["description"] for f in d["fieldDefinitions"]}[key]
        if now != text:
            out.append((f"{kind}.{key}", ENTRY_Q, {"id": d["id"], "definition": {"fieldDefinitions": [{"update": {"key": key, "description": text}}]}}, now, text))
    for (owner, full), text in OWNER.items():
        ns, key = full.split(".")
        defs = read("query($o: MetafieldOwnerType!) { metafieldDefinitions(first: 100, ownerType: $o) { nodes { namespace key description } } }", {"o": owner})["metafieldDefinitions"]["nodes"]
        now = [d["description"] for d in defs if d["namespace"] == ns and d["key"] == key][0]
        if now != text:
            out.append((f"{owner} {full}", OWNER_Q, {"definition": {"namespace": ns, "key": key, "ownerType": owner, "description": text}}, now, text))
    return out


if __name__ == "__main__":
    todo = calls()
    for name, _, _, before, after in todo:
        print(f"{name}\n  before: {before}\n  after:  {after}")
    if "--go" not in sys.argv[1:]:
        print(f"{len(todo)} change(s) listed; nothing changed")
        sys.exit(0)
    if todo:
        (HERE / "snapshots" / "help-text-2026-10-01-before.json").write_text(json.dumps(
            {"taken": "2026-10-01", "what": "Field help text before help_text.py replaced it. Undo: send each back with the same mutation.",
             "fields": {name: before for name, _, _, before, _ in todo}}, ensure_ascii=False, indent=1) + "\n")
    log = []
    for name, q, variables, before, after in todo:
        data, err = execute(q, variables, True)
        errors = user_errors(data) if not err else [{"message": err}]
        log.append({"field": name, "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "answer": data, "errors": errors})
        (HERE / "created" / "help-text-2026-10-01.json").write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n")
        if errors:
            sys.exit(f"STOPPED at {name}: {errors}")
        print(f"done: {name}")
