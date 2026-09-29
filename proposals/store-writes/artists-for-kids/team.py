#!/usr/bin/env python3
"""The Artists for Kids team as a grid of people, like the Smith Foundation's Board of Directors: a card
group of four portrait cards (name, then role) in place of the one group photo with its caption.

  python3 team.py prepare <folder>   JPEG copies of the four portraits (1.webp to 4.webp, left to right
                                     in the old group photo), into <folder>
  python3 team.py upload <folder>    the portraits into Files; IDs to ../created/afk-team.json
  python3 team.py cards              the four cards and the group afk-team, through the CLI
  python3 team.py page-fields        metafieldsSet variables for the Artists for Kids page, for the connector:
                                     the group last in its card groups, and the staged text without the
                                     heading and group photo

Michael, 2026-09-28, sent the four portraits. The names and roles are the old caption's, word for word.
The pictures have no alt text: each card's name follows its picture, as on the board.
"""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "collection"))
from images import execute, upload_batch  # noqa: E402

import content  # noqa: E402
from load import UPSERT  # noqa: E402

CREATED = HERE.parent / "created" / "afk-team.json"
SNAPSHOT = HERE.parent / "snapshots" / "afk-team-2026-09-28-before.json"
SRGB = "/System/Library/ColorSync/Profiles/sRGB Profile.icc"
HEADING = "Meet the Artists for Kids Team"

# (handle, source, name, role), left to right as in the old group photo.
TEAM = [
    ("allison-kerr", "1.webp", "Allison Kerr", "Director, Artist for Kids and Gordon Smith Gallery, and District Principal, Arts Education"),
    ("amelia-epp", "2.webp", "Amelia Epp", "District Visual Arts Teacher, Educational Coordinator"),
    ("chantal-pinard", "3.webp", "Chantal Pinard", "Artists For Kids Administrative and Program Assistant"),
    ("emily-neufeld", "4.webp", "Emily Neufeld", "Artists for Kids Studio Technician, Gallery Collection Preparator"),
]


def filename(handle):
    return f"afk-team-{handle}.jpg"


def created():
    return json.loads(CREATED.read_text()) if CREATED.exists() else {}


def save(data):
    CREATED.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")


def prepare(folder):
    for handle, src, _, _ in TEAM:
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85", "-m", SRGB,
                        str(folder / src), "--out", str(folder / filename(handle))], check=True, capture_output=True)
        print(filename(handle))


def upload(folder):
    data = created()
    todo = [(f"img:{h}", filename(h), "") for h, _, _, _ in TEAM if f"img:{h}" not in data]
    if todo:
        data.update(upload_batch(todo, folder, "IMAGE", "image/jpeg"))
        save(data)
    print(json.dumps(data, indent=1))


def cards():
    data = created()
    ids = []
    for handle, _, name, role in TEAM:
        fields = [{"key": "title", "value": name}, {"key": "image", "value": data[f"img:{handle}"]},
                  {"key": "text", "value": role}]
        r = execute(UPSERT, {"handle": {"type": "card", "handle": f"afk-team-{handle}"},
                             "metaobject": {"fields": fields}})["metaobjectUpsert"]
        if r["userErrors"]:
            raise RuntimeError(f"{handle}: {r['userErrors']}")
        data[f"afk-team-{handle}"] = r["metaobject"]["id"]
        ids.append(r["metaobject"]["id"])
    r = execute(UPSERT, {"handle": {"type": "card_group", "handle": "afk-team"},
                         "metaobject": {"fields": [{"key": "heading", "value": HEADING},
                                                   {"key": "cards", "value": json.dumps(ids)}]}})["metaobjectUpsert"]
    if r["userErrors"]:
        raise RuntimeError(r["userErrors"])
    data["afk-team"] = r["metaobject"]["id"]
    save(data)
    print(json.dumps(data, indent=1))


def release_body(current):
    """The staged text less the team's heading and group photo (the last thing in it)."""
    start = current.index(f"<h2>{HEADING}</h2>")
    rest = current[start:]
    assert rest.endswith("</figure>") and rest.count("<figure") == 1, "the team is no longer last: check by hand"
    return current[:start].rstrip()


def page_fields():
    before = json.loads(SNAPSHOT.read_text())
    groups = json.loads(before["custom.card_groups"]["value"])
    group = created()["afk-team"]
    if group not in groups:
        groups.append(group)
    body = release_body(before["custom.release_body"]["value"])
    return {"metafields": [
        {"ownerId": content.AFK_PAGE, "namespace": "custom", "key": "card_groups", "type": "list.metaobject_reference",
         "value": json.dumps(groups)},
        {"ownerId": content.AFK_PAGE, "namespace": "custom", "key": "release_body", "type": "multi_line_text_field",
         "value": body},
    ]}


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "prepare":
        prepare(pathlib.Path(sys.argv[2]))
    elif step == "upload":
        upload(pathlib.Path(sys.argv[2]))
    elif step == "cards":
        cards()
    elif step == "page-fields":
        print(json.dumps(page_fields(), indent=1, ensure_ascii=False))
