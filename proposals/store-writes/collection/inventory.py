#!/usr/bin/env python3
"""Inventory of the Permanent Collection catalogue (afkcatalogue.sd44.ca, Omeka S), read through its
public API. Read only: it downloads the public records and prints the counts the collection plan
(proposals/permanent-collection.md) rests on. Nothing is written anywhere but the output folder.

  python3 proposals/collection/inventory.py <output folder>

The folder gets items.json, item_sets.json and media.json (about 5 MB), for the import scripts to
start from. Don't commit them: run it again before each import, since the catalogue keeps changing.
"""
import collections
import json
import pathlib
import re
import sys
import time
import urllib.request

API = "https://afkcatalogue.sd44.ca/api"


def get(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "Mozilla/5.0 (collection inventory)"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def fetch_all(resource):
    out, page = [], 1
    while True:
        batch = get(f"/{resource}?per_page=100&page={page}")
        if not batch:
            return out
        out += batch
        page += 1
        time.sleep(0.3)


def values(item, key):
    return [x.get("@value") or x.get("@id") or x.get("o:label") for x in item.get(key, [])]


def main(folder):
    folder.mkdir(parents=True, exist_ok=True)
    data = {r: fetch_all(r) for r in ("items", "item_sets", "media")}
    for name, rows in data.items():
        (folder / f"{name}.json").write_text(json.dumps(rows))
    items, sets, media = data["items"], data["item_sets"], data["media"]

    print(f"Items {len(items)} (public {sum(i['o:is_public'] for i in items)}), item sets {len(sets)}, media {len(media)}")
    fields = collections.Counter(k for i in items for k, v in i.items() if k.startswith("dcterms:") and v)
    print("Fields:", ", ".join(f"{k.split(':')[1]} {n}" for k, n in fields.most_common()))
    creators = {c for i in items for c in values(i, "dcterms:creator")}
    names = {re.sub(r"\s*\(.*?\)", "", c).strip().lower() for c in creators}
    print(f"Creator spellings {len(creators)}, names once dates in brackets are removed {len(names)}")
    print("Formats:", collections.Counter(values(i, "dcterms:format")[0].strip().lower()
                                           for i in items if values(i, "dcterms:format")).most_common(10))
    types = collections.Counter(m.get("o:media_type") for m in media)
    size = sum(m.get("o:size") or 0 for m in media)
    big = sum(1 for m in media if (m.get("o:size") or 0) > 20e6)
    print(f"Media types {dict(types)}; {size / 1e9:.1f} GB in all; {big} files over 20 MB")
    ids = collections.Counter(values(i, "dcterms:identifier")[0] for i in items)
    print("Duplicate identifiers:", [k for k, n in ids.items() if n > 1])
    print("Items without an image:", sum(1 for i in items if not i.get("o:media")),
          "| without a title:", sum(1 for i in items if not values(i, "dcterms:title")))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(pathlib.Path(sys.argv[1]))
