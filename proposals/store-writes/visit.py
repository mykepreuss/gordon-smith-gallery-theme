#!/usr/bin/env python3
"""The Plan your visit pass (DS-61, Michael, 2026-09-26: "Let's improve /pages/plan-your-visit using
all our design skills - it looks really bad"). Builds the page's staged text (DS-39) from its own
text, so no word is retyped, and checks none is lost. Prints the variables for the mutation.

  python3 proposals/store-writes/visit.py staged   # metafieldsSet: the staged text
  python3 proposals/store-writes/visit.py review   # the staged text

The page was eight headings in one column. Its first four (Address, Gallery Hours, Artists For
Kids Office Hours, Admission) are the facts most visitors come for; they now come from Theme
settings, Gallery details, in the visit details at the top of the page (snippets/gs-visit-info),
under today's opening line and with a link for directions. So the staged text leaves them out,
and this script checks that each one is in Theme settings word for word. The rest keeps its words:
"Getting Here" with a photo of the entrance beside it, Public Transport and Parking as its points
(`gs-points`), then Accessibility. The headings lose the bold and line break pasted into them.
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BEFORE = json.loads((HERE / "snapshots" / "plan-your-visit-2026-09-26-before.json").read_text())
PAGE = BEFORE["page"]
PHOTO = BEFORE["entrance_photo"]
PHOTO_ALT = "The entrance at 2121 Lonsdale Avenue, with the gallery's sign above the doors"
# The four facts that move to Theme settings, and the setting each is in.
MOVED = {"Address": "address", "Gallery Hours": "hours", "Artists For Kids Office Hours": "office_hours", "Admission": "admission"}


def words(s):
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def sections():
    """The text as (heading, html after it) pairs."""
    parts = re.split(r"<h2>\s*<strong>(.*?)</strong>(?:<br>)?\s*</h2>\s*", PAGE["body"], flags=re.S)
    assert parts[0] == "" and len(parts) == 17, "Plan your visit's text changed since the snapshot"
    return [(parts[i], parts[i + 1].strip()) for i in range(1, len(parts), 2)]


def settings():
    raw = (ROOT / "theme" / "config" / "settings_data.json").read_text()
    return json.loads(re.sub(r"^\s*/\*.*?\*/", "", raw, flags=re.S))["current"]


def staged():
    secs = dict(sections())
    current = settings()
    for heading, key in MOVED.items():
        value = re.fullmatch(r"<p>(.*)</p>", secs[heading], flags=re.S).group(1)
        assert value.replace("<br>", "\n") == current[key], f"{heading} isn't in Theme settings as written"
    w = 1200
    h = round(PHOTO["height"] * w / PHOTO["width"])
    photo = (f'<figure><img src="{html.escape(PHOTO["url"])}&amp;width={w}" alt="{html.escape(PHOTO_ALT, quote=False).replace(chr(34), "&quot;")}" '
             f'width="{w}" height="{h}" loading="lazy"></figure>')
    point = lambda name: f"<li>\n<strong>{name}</strong><br>{re.fullmatch(r'<p>(.*)</p>', secs[name], flags=re.S).group(1)}</li>"
    body = "\n".join([
        "<h2>Getting Here</h2>", photo, secs["Getting Here"],
        '<ul class="gs-points">', point("Public Transport"), point("Parking"), "</ul>",
        "<h2>Accessibility</h2>", secs["Accessibility"],
    ])
    # Every word is kept: what stays reads as before, and what moved is in Theme settings.
    kept = [n for n, _ in sections() if n not in MOVED]
    expected = " ".join(words(f"<h2>{n}</h2>" + secs[n]) for n in kept)
    got = words(re.sub(r"<figure>.*?</figure>", "", body, flags=re.S))
    assert got == expected, "Words changed"
    return body


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step == "staged":
        print(json.dumps({"metafields": [{"ownerId": PAGE["id"], "namespace": "custom", "key": "release_body",
                                          "type": "multi_line_text_field", "value": staged()}]}, indent=2, ensure_ascii=False))
    elif step == "review":
        print(staged())
    else:
        sys.exit(__doc__)
