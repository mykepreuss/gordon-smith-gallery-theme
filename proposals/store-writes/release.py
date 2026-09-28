#!/usr/bin/env python3
"""The release's store changes, as dry runs first (plan, "Release gate and rollback";
proposals/store-changes.md §3, §5, §7, §8, §9). Nothing here writes to the store. Each step reads a
fresh read-only export of the store, prints what would change as Markdown for review, and with
--vars prints the variables for the mutations to run through the Shopify connector at release.

Exports (take them again on the day, just before running):
  pages     query { pages(first: 100) { nodes { id handle title templateSuffix isPublished updatedAt
            body staged: metafield(namespace: "custom", key: "release_body") { id value }
            hidden: metafield(namespace: "seo", key: "hidden") { id value } } } }
            saved as the nodes list. (53 pages since the Artists for Kids pages, 2026-09-27.)
  products  query($ids: [ID!]!) { nodes(ids: $ids) { ... on Product { id handle title status
            updatedAt descriptionHtml } } }, with the 21 IDs in snapshots/prints-2026-09-25.json.

  python3 proposals/store-writes/release.py templates <pages.json> [--vars]
  python3 proposals/store-writes/release.py staged    <pages.json> [--vars]
  python3 proposals/store-writes/release.py unhide    <pages.json> [--vars]
  python3 proposals/store-writes/release.py addresses <pages.json> [--vars]
  python3 proposals/store-writes/release.py products  <products.json> [--vars]
  python3 proposals/store-writes/release.py frames    [--vars]

Order at release (plan): publish, templates, addresses, staged, unhide, products, frames. Every step's
Markdown doubles as its rollback record: it lists the values before the change.
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import shop  # noqa: E402  (label parsing and plain titles, 2026-09-25)

SNAP_PAGES = {p["handle"]: p for p in json.loads((HERE / "snapshots" / "pages-2026-09-25.json").read_text())}
SNAP_BY_ID = {p["id"]: p for p in SNAP_PAGES.values()}  # by ID, so a changed handle can't break the check
CLEARED_PREFIX = "<!--"

# ---------------------------------------------------------------------------
# 1. Template names (store-changes §3; DESIGN.md §7.4). Since DS-48 and DS-49 every page already
# shows correctly on the template it falls back to; this puts the right name on it for staff.

PROGRAMME = {"artists-for-kids", "the-smith-foundation", "public-programs-1", "speaker-series",
             "music-at-the-smith", "explore-create", "art-in-good-company",
             "volunteer"}  # Volunteer: its roles are cards between its text's parts (DS-58)
# The Artists for Kids pages made before release (P-35, proposals/artists-for-kids-integration.md): they
# carry the live theme's On Now template name until now, so the live site shows only their title.
AFK_PROGRAMME = {"classes-and-camps", "schools-and-teachers", "after-school-art", "day-camps",
                 "paradise-valley-summer-camp", "gallery-program", "artists-in-residence", "studio-art-academy",
                 "learning-guides", "learning-kits", "artreach-videos", "professional-development",
                 "awards-and-scholarships"}
# Support Artists for Kids: its ways to give follow all of its text, as on Donate (design review 2026-09-27).
AFK_STANDARD = {"artist-in-residence-amelia-butcher", "artist-in-residence-mark-johnsen",
                "artist-in-residence-becky-bair", "artist-in-residence-sara-jeanne-bourget",
                "support-artists-for-kids"}
AFK_NEW = AFK_PROGRAMME | AFK_STANDARD
# The Smith Foundation's pages made before release the same way (P-35, P-42; proposals/smith-foundation-site.md),
# on the standard page template. Supporters waits for the gallery to confirm its donor list (P-43,
# gallery-questions.md 8.1): until then it stays hidden at release, and its card leaves the Foundation page's
# "Get involved" group. Take it out of HOLD_AT_RELEASE when the gallery confirms.
FOUNDATION_NEW = {"smith-foundation-scholarships", "brilliance-gala", "smith-foundation-supporters"}
HOLD_AT_RELEASE = {"smith-foundation-supporters"}
NEW_PAGES = AFK_NEW | FOUNDATION_NEW
# Story pages: long reads whose text is one column with its pictures set into it (DS-145, Proposed).
STORY = {"gordon-and-marion", "brilliance-gala"}
HIDDEN_AT_RELEASE = {"exhibition-one-hundred-artists-deep", "exhibition-from-the-ground",
                     "exhibition-stitched-merging-photography-and-textile-practices", "exhibition-playhouse",
                     "exhibition-prevailing-landscapes", "exhibition-the-art-of-conversation", "exhibitions-1",
                     "about",       # About: its history joins Artists for Kids (P-24)
                     "our-story",   # Our Story: removed from the Shop (P-25)
                     "engage"}      # Engage: its one paragraph is Public programs' opening, and nothing links to it (DS-129)


def new_template(page):
    h = page["handle"]
    if h in HIDDEN_AT_RELEASE or not page["isPublished"]:
        return None  # left as it is: hidden at release, or already unpublished
    if h in PROGRAMME or h in AFK_PROGRAMME:
        return "programme"
    if h in STORY:
        return "story"
    if h == "contact":
        return "contact"
    if h == "shop":
        return "shop"
    return ""  # the standard page template


def templates(pages, want_vars):
    rows, muts = [], []
    for p in sorted(pages, key=lambda p: p["handle"]):
        new = new_template(p)
        old = p["templateSuffix"] or ""
        if new is None:
            rows.append(f"| `{p['handle']}` | `{old or '(default)'}` | unchanged ({'hidden at release' if p['handle'] in HIDDEN_AT_RELEASE else 'unpublished'}) |")
        elif new == old:
            rows.append(f"| `{p['handle']}` | `{old or '(default)'}` | already right |")
        else:
            rows.append(f"| `{p['handle']}` | `{old or '(default)'}` | **`{new or '(default)'}`** |")
            muts.append({"id": p["id"], "page": {"templateSuffix": new}})
    if want_vars:
        return {f"p{i}": m for i, m in enumerate(muts)}
    return "\n".join(["## Template names", "", f"{len(muts)} pages change. Rollback: set each back to the \"Now\" value.", "",
                      "| Page | Now | At release |", "| --- | --- | --- |"] + rows)


# ---------------------------------------------------------------------------
# 2. Addresses (store-changes §5): hide ten pages, then ten redirects.

REDIRECTS = [
    ("/pages/exhibition-one-hundred-artists-deep", "/pages/exhibitions/one-hundred-artists-deep"),
    ("/pages/exhibition-from-the-ground", "/pages/exhibitions/from-the-ground"),
    ("/pages/exhibition-stitched-merging-photography-and-textile-practices", "/pages/exhibitions/stitched"),
    ("/pages/exhibition-playhouse", "/pages/exhibitions/playhouse"),
    ("/pages/exhibition-prevailing-landscapes", "/pages/exhibitions/prevailing-landscapes"),
    ("/pages/exhibition-the-art-of-conversation", "/pages/exhibitions/the-art-of-conversation"),
    ("/pages/exhibitions-1", "/pages/on-now"),
    ("/pages/about", "/pages/about-us"),                 # P-24, Michael 2026-09-26
    ("/pages/our-story", "/pages/artists-for-kids"),     # P-25: its history is on Artists for Kids
    ("/pages/engage", "/pages/public-programs-1"),       # DS-129: Public programs opens with its text
]


def addresses(pages, want_vars):
    by = {p["handle"]: p for p in pages}
    hide = [by[h] for h in sorted(HIDDEN_AT_RELEASE) if h in by]
    if want_vars:
        out = {f"hide{i}": {"id": p["id"], "page": {"isPublished": False}} for i, p in enumerate(hide)}
        out.update({f"r{i}": {"path": a, "target": b} for i, (a, b) in enumerate(REDIRECTS)})
        return out
    rows = [f"| `{p['handle']}` | {'published' if p['isPublished'] else 'hidden'} | hidden |" for p in hide]
    rrows = [f"| `{a}` | `{b}` |" for a, b in REDIRECTS]

    return "\n".join(["## Addresses", "", "Hide first: a redirect only works from an address that no longer loads a page.", "",
                      "| Page | Now | At release |", "| --- | --- | --- |"] + rows +
                     ["", "| Redirect from | To |", "| --- | --- |"] + rrows +
                     ["", f"Rollback: delete the {len(REDIRECTS)} redirects, publish the {len(hide)} pages."])


# ---------------------------------------------------------------------------
# 3. Staged page text (store-changes §8, DS-39).

def staged(pages, want_vars):
    rows, muts, deletes, stop = [], [], [], []
    for p in sorted(pages, key=lambda p: p["handle"]):
        if not p.get("staged") or p["handle"] in HOLD_AT_RELEASE:
            continue
        snap = SNAP_BY_ID.get(p["id"], {}).get("body")
        if snap is None and p["handle"] in NEW_PAGES:
            snap = ""  # made empty before release (P-35); its text is all staged
        new = p["staged"]["value"]
        new_body = "" if new.strip().startswith(CLEARED_PREFIX) and new.strip().endswith("-->") else new
        same = snap is not None and p["body"] == snap
        if not same:
            stop.append(p["handle"])
        what = "cleared" if new_body == "" else f"{len(new_body)} characters (was {len(p['body'])})"
        rows.append(f"| `{p['handle']}` | {'matches the snapshot' if same else '**changed since the snapshot: rebuild its staged text first**'} | {what} |")
        muts.append({"id": p["id"], "page": {"body": new_body}})
        deletes.append({"ownerId": p["id"], "namespace": "custom", "key": "release_body"})
    if want_vars:
        if stop:
            sys.exit(f"Stopped: live text changed since the snapshot on {', '.join(stop)}.")
        return {"pages": {f"p{i}": m for i, m in enumerate(muts)}, "metafieldsDelete": deletes,
                "then": "metafieldDefinitionDelete for custom.release_body on PAGE"}
    return "\n".join(["## Staged page text", "",
                      f"{len(muts)} pages. Stop if any page's live text changed since `snapshots/pages-2026-09-25.json`. "
                      "After the pages, delete the staged values and the `release_body` definition. Rollback: restore each page's text from the snapshot.", "",
                      "| Page | Live text | At release |", "| --- | --- | --- |"] + rows +
                     ([""] + [f"**Stopped:** {', '.join(stop)}"] if stop else [""] + ["All pages match: ready."]))


# ---------------------------------------------------------------------------
# 3b. The Artists for Kids pages become visible to search engines and the store's search (P-35).

def unhide(pages, want_vars):
    todo = [p for p in sorted(pages, key=lambda p: p["handle"])
            if p["handle"] in NEW_PAGES - HOLD_AT_RELEASE and p.get("hidden")]
    missing = sorted(NEW_PAGES - {p["handle"] for p in pages})
    if want_vars:
        return {"metafields": [{"ownerId": p["id"], "namespace": "seo", "key": "hidden"} for p in todo]}
    rows = [f"| `{p['handle']}` | hidden (`seo.hidden` = {p['hidden']['value']}) | shown |" for p in todo]
    return "\n".join(["## New pages (Artists for Kids, the Smith Foundation): search engines and the store's search", "",
                      f"{len(todo)} pages lose `seo.hidden` (metafieldsDelete). Rollback: set it back to 1 on each.", "",
                      "| Page | Now | At release |", "| --- | --- | --- |"] + rows +
                     ([""] + [f"**Missing from the export:** {', '.join(missing)}"] if missing else []))


# ---------------------------------------------------------------------------
# 4. Product titles and descriptions (store-changes §7; DS-16, P-21, P-22).

from html.parser import HTMLParser

BLOCK_TAGS = {"p", "div", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "li", "ul", "ol"}
INLINE_TAGS = {"strong", "b", "em", "i", "span", "u", "a", "font"}
REMOVE_KEYS = ("edition", "dimensions", "size", "paper size", "image size", "technique", "date", "availability")


class Tokens(HTMLParser):
    """The description as raw tokens, so kept parts come back exactly as written."""
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.tokens = []

    def handle_starttag(self, tag, attrs):
        self.tokens.append(["start", tag, self.get_starttag_text()])

    def handle_startendtag(self, tag, attrs):
        self.tokens.append(["startend", tag, self.get_starttag_text()])

    def handle_endtag(self, tag):
        self.tokens.append(["end", tag, f"</{tag}>"])

    def handle_data(self, data):
        self.tokens.append(["data", None, data])

    def handle_entityref(self, name):
        self.tokens.append(["data", None, f"&{name};"])

    def handle_charref(self, name):
        self.tokens.append(["data", None, f"&#{name};"])


def text_of(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment)).replace(" ", " ")).strip()


def norm(s):
    return re.sub(r"[\s.,:;]+$", "", re.sub(r"\s+", " ", s.replace(" ", " "))).strip().lower()


def split_lines(tokens):
    """Groups token indexes into lines: a line ends at <br> and at any block tag."""
    lines_, cur = [], []
    for i, (kind, tag, raw) in enumerate(tokens):
        if tag == "br" or tag in BLOCK_TAGS or tag == "meta":
            if cur:
                lines_.append(cur)
            cur = []
            continue
        cur.append(i)
    if cur:
        lines_.append(cur)
    return lines_


def line_text(tokens, idx):
    return re.sub(r"\s+", " ", html.unescape("".join(tokens[i][2] for i in idx if tokens[i][0] == "data")).replace(" ", " ")).strip()


def tidy(markup):
    """Drops the empty tags and stray breaks that removed lines leave behind (opening block only)."""
    inline = r"(?:strong|b|em|i|span|u|font)"
    block = r"(?:p|div|blockquote|h[1-6]|li)"
    markup = re.sub(r"<meta[^>]*>", "", markup)
    prev = None
    while prev != markup:
        prev = markup
        markup = re.sub(rf"<({inline})\b[^>]*>(\s|<br\s*/?>)*</\1>", "", markup)
        markup = re.sub(r"(<br\s*/?>\s*){2,}", "<br>", markup)
        markup = re.sub(rf"(<{block}\b[^>]*>)((?:<{inline}\b[^>]*>)*)(\s*<br\s*/?>)+", r"\1\2", markup)
        markup = re.sub(rf"(\s*<br\s*/?>)+((?:</{inline}>)*\s*</{block}>)", r"\2", markup)
        markup = re.sub(rf"<({block})\b[^>]*>\s*</\1>", "", markup)
    return re.sub(r"\n{3,}", "\n\n", markup).strip()


def clean_description(product, label):
    """Returns (new_html, removed_lines, short_line, medium_found)."""
    parser = Tokens()
    parser.feed(product["descriptionHtml"])
    parser.close()
    tokens = parser.tokens
    lines_ = split_lines(tokens)
    texts = [line_text(tokens, l) for l in lines_]
    sig = next((i for i, t in enumerate(texts) if re.match(r"signature\s*:", t, re.I)), None)
    if sig is None:
        return product["descriptionHtml"], [], None, None
    artist, title_year = norm(label["artist"]), norm(f"{label['artwork_title']}, {label['year']}")
    removed, fields, frame_word, medium = [], {}, None, None
    drop, last_key, in_details = set(), None, False
    for n in range(sig + 1):
        t = texts[n]
        if not t:
            continue
        low = norm(t)
        key = norm(t.split(":", 1)[0]) if re.match(r"^[A-Za-z ]{3,20}:", t) else None
        if low in (artist, title_year, "limited edition", "art edition"):
            drop.add(n); removed.append(t)
        elif low in ("print details", "details") or re.fullmatch(r"(availability: .+ )?print details:?", low):
            drop.add(n); removed.append(t); in_details = True; last_key = None
        elif key in REMOVE_KEYS:
            drop.add(n); removed.append(t); last_key = key
        elif key in ("paper", "signature"):
            fields[key] = t.split(":", 1)[1].strip(); drop.add(n); removed.append(t); last_key = key
        elif low in ("unframed", "framed"):
            frame_word = t.strip().capitalize(); drop.add(n); removed.append(t)
        elif in_details and last_key:
            # A line with no label inside the details continues the one above (a paper's maker, a long size).
            if last_key in fields:
                fields[last_key] += ", " + t.strip()
            drop.add(n); removed.append(t)
    # The second repeat of the details (Samuel Roy-Bois, Sara Khan): medium on paper, size and edition, unframed.
    pats = [r".+ on .+ paper", r".*edition of \d+", r"unframed"]
    n = sig + 1
    while n < len(texts) and (not texts[n] or any(re.fullmatch(p, texts[n], re.I) for p in pats)):
        if texts[n]:
            removed.append(texts[n]); drop.add(n)
            if re.fullmatch(pats[0], texts[n], re.I) and not medium:
                medium = re.sub(r"\s+on\s+.+$", "", texts[n])
        n += 1
    parts = [f"Paper: {fields['paper'].rstrip('.')}"] if "paper" in fields else []
    if "signature" in fields:
        parts.append(f"Signature: {fields['signature'].rstrip('.')}")
    if frame_word:
        parts.append(frame_word)
    short = ". ".join(parts) + "." if parts else None
    # Rebuild: drop the text of removed lines and the inline tags wholly inside them; the signature
    # line carries the short line instead.
    out = [tok[2] for tok in tokens]
    for n in drop:
        idx = lines_[n]
        depth, opened = {}, []
        for i in idx:
            kind, tag, raw = tokens[i]
            if kind == "data":
                out[i] = ""
            elif kind == "start" and tag in INLINE_TAGS:
                opened.append(i)
            elif kind == "end" and tag in INLINE_TAGS:
                match = next((j for j in reversed(opened) if tokens[j][1] == tag), None)
                if match is not None:
                    out[match] = ""; out[i] = ""; opened.remove(match)
        if n == sig and short:
            first = next(i for i in idx if tokens[i][0] == "data")
            out[first] = html.escape(short, quote=False)
    # Tidy only the opening block that changed; everything after it stays exactly as written.
    last = max(drop | {sig})
    k = next((lines_[n][0] for n in range(last + 1, len(lines_)) if texts[n]), len(tokens))
    tail = "".join(out[k:])
    assert tail == "".join(tok[2] for tok in tokens[k:]), "the text after the details changed"
    head = tidy("".join(out[:k]))
    if short:
        # The kept line reads as plain text, whatever formatting the old details had around it.
        s = re.escape(html.escape(short, quote=False))
        prev = None
        while prev != head:
            prev = head
            head = re.sub(rf"<(strong|b|em|i|span|u|font)\b[^>]*>({s})</\1>", r"\2", head)
    return head + tail, removed, short, medium


def lines(fragment):
    h = re.sub(r"<br\s*/?>", "\n", fragment)
    h = re.sub(r"</(p|li|h\d|div)>", "\n", h)
    return [l.strip() for l in html.unescape(re.sub(r"<[^>]+>", "", h)).replace(" ", " ").split("\n") if l.strip()]


def products(prods, want_vars):
    labels = {p["id"]: shop.label(p) for p in shop.PRINTS}
    out, muts = [], []
    for p in prods:
        label = labels[p["id"]]
        new_desc, removed, short, medium = clean_description(p, label)
        new_title = shop.plain(p["title"])
        muts.append({"id": p["id"], "title": new_title, "descriptionHtml": new_desc})
        if want_vars:
            continue
        out += [f"### {new_title}", "", f"- Title: `{p['title']}` becomes `{new_title}`" + (" (unchanged)" if new_title == p["title"] else "")]
        out += ["- Lines removed: " + "; ".join(f"\"{r}\"" for r in removed)]
        if short:
            out += [f"- Paper and signature kept as one line: \"{short}\""]
        if medium:
            out += [f"- Medium found in the second repeat: \"{medium}\""]
        out += ["- Description after (first lines):", ""] + [f"  > {l}" for l in lines(new_desc)[:4]] + [""]
    if want_vars:
        return {f"p{i}": m for i, m in enumerate(muts)}
    return "\n".join(["## Product titles and descriptions", "",
                      "For the gallery to approve before release (P-21, P-22). Removed: the lines that repeat the label (artist, title and year, "
                      "\"Limited Edition\", edition, sizes, technique, date), \"Print details\", the Availability lines, and the second repeat of the details. "
                      "Kept: paper and signature as one short line, and everything after them as written. Rollback: "
                      "`snapshots/prints-descriptions-2026-09-26.json` holds every title and description before the change (take it again on the day).", ""] + out)


# ---------------------------------------------------------------------------
# 5. Frames (store-changes §9, P-19).

def frames(want_vars):
    snap = json.loads((HERE / "snapshots" / "frames-2026-09-26.json").read_text())["frames"]
    active = [f for f in snap if f["status"] == "ACTIVE"]
    if want_vars:
        return {f"f{i}": {"id": f["id"], "status": "UNLISTED"} for i, f in enumerate(active)}
    return "\n".join(["## Frames", "", f"{len(active)} active frames become Unlisted; the draft one stays a draft. Rollback: set them back to Active.", "",
                      "| Frame | Now | At release |", "| --- | --- | --- |"] +
                     [f"| `{f['handle']}` | {f['status'].lower()} | {'unlisted' if f['status'] == 'ACTIVE' else 'unchanged'} |" for f in snap])


if __name__ == "__main__":
    step, args = sys.argv[1], sys.argv[2:]
    want_vars = "--vars" in args
    files = [a for a in args if not a.startswith("--")]
    data = json.loads(pathlib.Path(files[0]).read_text()) if files else None
    result = {"templates": lambda: templates(data, want_vars), "addresses": lambda: addresses(data, want_vars),
              "staged": lambda: staged(data, want_vars), "unhide": lambda: unhide(data, want_vars),
              "products": lambda: products(data, want_vars),
              "frames": lambda: frames(want_vars)}[step]()
    print(json.dumps(result, indent=2, ensure_ascii=False) if want_vars else result)
