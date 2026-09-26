#!/usr/bin/env python3
"""Donate and Gordon and Marion design pass (DS-53, Michael, 2026-09-26: "using our design skills
let's improve these pages"). Builds each page's staged text (DS-39) from the migration's own
staged text, so no word is retyped, and checks the words are unchanged. Prints the variables for
each step's mutation.

  python3 proposals/store-writes/donate_gm.py gm-staged
  python3 proposals/store-writes/donate_gm.py donate-staged
  python3 proposals/store-writes/donate_gm.py donate-cta
  python3 proposals/store-writes/donate_gm.py review      # both staged texts

Gordon and Marion: the biography's paragraphs, which were one paragraph split by line breaks,
become paragraphs, and the photo of Gordon and Marion becomes a figure with a description, so it
sits beside the biography from 990 px (DS-51).

Donate: "The impact of your gift" becomes the heading it looks like, level with "Ways to Support".
Asha's words become a quote with her name under it, set beside the list of what a gift does from
990 px. The page's call to action, "Ways to give", jumps to its Ways To Give cards. Line breaks typed
at the end of list items for spacing go, the Explore + Create link stays in the same tab, and a space
inside a link moves out of it.
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import migration  # noqa: E402  (the staged text as migrated, 2026-09-25 and the page pass)

SITE = "https://gordonsmithgallery.com"
GM_PHOTO_ALT = "Gordon and Marion Smith looking at a print together"


def words(s):
    """The text a reader sees, for checking nothing was reworded."""
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s).replace(" ", " ")
    s = s.replace("“", "").replace("”", "").replace("—", "")
    return re.sub(r"\s+", " ", s).strip()


def gm_staged():
    before = migration.PAGES["gordon-and-marion"]["body"] + "\n" + migration.GORDON_AND_MARION_VIDEO
    body = before
    bio = re.match(r"<p>(.*?)</p>", body, flags=re.S)
    parts = [x.strip() for x in re.split(r"<br\s*/?>\s*<br\s*/?>", bio.group(1)) if x.strip()]
    assert len(parts) == 6 and parts[0].startswith("<strong>Gordon Appelbe Smith</strong>"), parts[:1]
    parts = [re.sub(r"<strong>Marion Smith </strong>", "<strong>Marion Smith</strong> ", x) for x in parts]
    body = body.replace(bio.group(0), "\n".join(f"<p>{x}</p>" for x in parts), 1)
    img = re.search(r'<p><img src="([^"]+)" alt=""[^>]*></p>', body)
    assert img, "The photo changed since the snapshot"
    figure = (f'<figure><img src="{img.group(1)}&amp;width=1200" alt="{GM_PHOTO_ALT}" width="1200" '
              f'height="1490" loading="lazy"></figure>')
    body = body.replace(img.group(0), figure, 1)
    body = body.replace("<p><br></p>\n", "", 1)
    assert words(body).replace(" ", "") == words(before).replace(" ", ""), "Words changed"
    return body


QUOTE = re.compile(r'<p style="text-align: center;"><em>(“.*?”)<br></em>—<span> </span><strong>(.*?)</strong></p>', flags=re.S)


def donate_staged():
    before = migration.donate_body()
    body = before
    old_head = "<p><strong>The impact of your gift</strong></p>"
    assert body.count(old_head) == 1
    body = body.replace(old_head, "<h2>The impact of your gift</h2>", 1)
    q = QUOTE.search(body)
    assert q, "Asha's quote changed since the snapshot"
    quote = (f'<figure class="gs-quote"><blockquote><p>{q.group(1)}</p></blockquote>'
             f"<figcaption><strong>{q.group(2)}</strong></figcaption></figure>")
    body = body.replace(q.group(0), quote, 1)
    body = body.replace("<span> </span>", " ").replace("<span> </span>", " ")
    # Spacing typed as line breaks at the end of list items; the list sets its own spacing.
    body = re.sub(r"(<br>)+\s*</li>", "\n</li>", body)
    # Links within the site open in the same tab; a space sat inside one link.
    body = body.replace('<a href="https://gordonsmithgallery.com/pages/explore-create" rel="noopener" target="_blank">',
                        '<a href="/pages/explore-create">')
    body = body.replace('courses,<a href="https://artistsforkids.sd44.ca/learn/spring--summer-day-camps/" rel="noopener" target="_blank"> Spring',
                        'courses, <a href="https://artistsforkids.sd44.ca/learn/spring--summer-day-camps/" rel="noopener" target="_blank">Spring')
    assert "<br><br>" not in body and 'target="_blank"> ' not in body and "explore-create\" rel" not in body
    assert words(body) == words(before), "Words changed"
    return body


def donate_cta():
    return {"ownerId": migration.PAGES["donate"]["id"], "namespace": "custom", "key": "cta", "type": "link",
            "value": json.dumps({"text": "Ways to give", "url": f"{SITE}/pages/donate#donate-ways-to-give"})}


def staged(handle, value):
    return {"ownerId": migration.PAGES[handle]["id"], "namespace": "custom", "key": "release_body",
            "type": "multi_line_text_field", "value": value}


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step == "gm-staged":
        print(json.dumps({"metafields": [staged("gordon-and-marion", gm_staged())]}, indent=2, ensure_ascii=False))
    elif step == "donate-staged":
        print(json.dumps({"metafields": [staged("donate", donate_staged())]}, indent=2, ensure_ascii=False))
    elif step == "donate-cta":
        print(json.dumps({"metafields": [donate_cta()]}, indent=2, ensure_ascii=False))
    elif step == "review":
        print(gm_staged(), "\n\n----\n\n", donate_staged(), sep="")
    else:
        sys.exit(__doc__)
