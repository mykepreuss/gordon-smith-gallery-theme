#!/usr/bin/env python3
"""Shop (Michael's go-ahead, 2026-09-25, "Yes, all of it"): product label and availability field
definitions (content model parts 3 and 6), the collection photo credit field (part 6), label
values on the 21 limited editions, photo credits on the five portfolios, and the Shop landing
page's hero image and credit. Product titles are not changed here: plain-text titles (DS-16) are
a live change, made at release. Prints the variables for each step's mutation.

  python3 proposals/store-writes/shop.py definitions
  python3 proposals/store-writes/shop.py values          # every value, for the metafieldsSet calls
  python3 proposals/store-writes/shop.py review          # the parsed labels as a table, for checking

Label values come only from each print's own title and description (snapshots/prints-2026-09-25.json):
  artist, title, year   the title "Artist, Title, Year", with Unicode styled letters made plain
  medium                the description's "Technique:" line, as written
  edition               "Edition: 50" becomes "Edition of 50"; anything else ("AP (ed. of 30)") as written
  dimensions            "Dimensions:" or "Size:" as written; "Image size:" keeps its label
"""
import json
import pathlib
import re
import sys
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
PRINTS = json.loads((HERE / "snapshots" / "prints-2026-09-25.json").read_text())

COLLECTION_CREDITS = {
    "gid://shopify/Collection/505736429865": "Photography by Rachel Topham",  # 2026 Fall Portfolio
    "gid://shopify/Collection/501485797673": "Photo by Rachel Topham",        # 2026 Spring Portfolio
    "gid://shopify/Collection/495640445225": "Photo by Rachel Topham",        # 2025 Fall Portfolio
    "gid://shopify/Collection/484250386729": "Photo by Rachel Topham",        # 2025 Spring Portfolio
    "gid://shopify/Collection/479152668969": "Photo by Rachel Topham",        # 2024 Fall Portfolio
}
SHOP_PAGE = "gid://shopify/Page/155762786601"
SHOP_HERO = "gid://shopify/MediaImage/46274243363113"  # GSG_2026_Fall_Edition_1.jpg, the old banner's first slide


def definitions():
    product = [
        ("artist", "single_line_text_field", "Artist", "As it should read on the label, for example: Gordon Smith."),
        ("artwork_title", "single_line_text_field", "Artwork title", "Plain text; the site sets it in italics. For example: Pender Harbour."),
        ("year", "single_line_text_field", "Year", "Text, so c. 1975 works."),
        ("medium", "single_line_text_field", "Medium", "For example: 17-colour serigraph."),
        ("edition", "single_line_text_field", "Edition", "For example: Edition of 50, or AP (ed. of 30)."),
        ("dimensions", "single_line_text_field", "Dimensions", "For example: 30.25\" x 44\"."),
        ("coming_soon", "boolean", "Coming soon", "On: the work shows but can't be bought yet. Say when in Availability note."),
        ("availability_note", "single_line_text_field", "Availability note", "Shown with Coming soon, for example: Available September 25 at noon (PT)."),
    ]
    out = {}
    for i, (key, type_, name, desc) in enumerate(product):
        out[f"p{i}"] = {"namespace": "custom", "key": key, "name": name, "description": desc, "type": type_,
                        "ownerType": "PRODUCT", "pin": True}
    out["c0"] = {"namespace": "custom", "key": "photo_credit", "name": "Photo credit", "type": "single_line_text_field",
                 "description": "Credit for the collection's image, for example: Photography by Rachel Topham.",
                 "ownerType": "COLLECTION", "pin": True}
    return out


def plain(s):
    return unicodedata.normalize("NFKC", s).strip()


def label(p):
    parts = [x.strip() for x in plain(p["title"]).split(", ")]
    year = parts[-1] if re.fullmatch(r"(c\. )?\d{4}", parts[-1]) else p["facts"].get("date", "")
    body = parts[:-1] if year == parts[-1] else parts
    artist, title = body[0], ", ".join(body[1:])
    f = p["facts"]
    edition = f.get("edition", "")
    if re.fullmatch(r"\d+", edition):
        edition = f"Edition of {edition}"
    if "dimensions" in f:
        dims = f["dimensions"]
    elif "size" in f:
        dims = f["size"]
    elif "image size" in f:
        dims = f"Image size: {f['image size']}"
    else:
        dims = ""
    return {"artist": artist, "artwork_title": title, "year": year, "medium": f.get("technique", ""),
            "edition": edition, "dimensions": dims}


def values():
    rows = []
    for p in PRINTS:
        for key, value in label(p).items():
            value = re.sub(r"\s+", " ", value).strip()
            if value:
                rows.append({"ownerId": p["id"], "namespace": "custom", "key": key, "type": "single_line_text_field", "value": value})
    for cid, credit in COLLECTION_CREDITS.items():
        rows.append({"ownerId": cid, "namespace": "custom", "key": "photo_credit", "type": "single_line_text_field", "value": credit})
    rows.append({"ownerId": SHOP_PAGE, "namespace": "custom", "key": "hero_image", "type": "file_reference", "value": SHOP_HERO})
    rows.append({"ownerId": SHOP_PAGE, "namespace": "custom", "key": "hero_caption", "type": "single_line_text_field", "value": "Photography by Rachel Topham"})
    # metafieldsSet takes at most 25 at a time.
    return {f"m{i // 25}": rows[i:i + 25] for i in range(0, len(rows), 25)}


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "definitions":
        print(json.dumps(definitions(), indent=2, ensure_ascii=False))
    elif step == "values":
        print(json.dumps(values(), indent=2, ensure_ascii=False))
    elif step == "review":
        print("| Handle | Artist | Title | Year | Medium | Edition | Dimensions |")
        print("| --- | --- | --- | --- | --- | --- | --- |")
        for p in PRINTS:
            l = label(p)
            print(f"| {p['handle']} | {l['artist']} | {l['artwork_title']} | {l['year']} | {l['medium']} | {l['edition']} | {l['dimensions']} |")
