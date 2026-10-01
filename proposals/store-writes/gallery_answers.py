#!/usr/bin/env python3
"""The store changes that follow from the gallery's answers of 2026-10-01
(proposals/gallery-answers/). Michael, 2026-10-01: "Proceed", on the plan that lists them.

  python3 proposals/store-writes/gallery_answers.py <step> [--go]
  steps, in order: text, artists, alt, descriptions, listing, unstage, identifiers, pages
  at the next release (store-changes §9c): faq, unstage again, definition

Each step reads the store first, so it sends only what still differs: a second run of a finished
step lists nothing. Without --go it prints each call and changes nothing. With --go it saves what
it is about to change to snapshots/gallery-answers-2026-10-01-before.json, makes the calls one at
a time through the Shopify CLI (`shopify store execute`), stops at the first error, and writes the
store's answers to created/gallery-answers-2026-10-01/<step>.json.

  text         Words in pages and entries: "Artists for Kids" with a small f, "Artist for Kids"
               corrected, Bill Reid's first edition as "Xhuwaji/Haida Grizzly Bear", the office
               hours on Contact, the FAQ's shipping answer, "over 1,200" on Permanent Collection.
  artists      Four names and their addresses (the old addresses redirect), nine life dates, four
               biographies.
  alt          The 11 image descriptions the gallery changed (aeo/alt.json).
  descriptions The 14 page descriptions the gallery changed, in the staged field the theme reads
               (aeo/descriptions.json).
  listing      Every page's approved description in its search engine listing (store-changes §8d).
  unstage      The staged descriptions deleted, once `listing` is read back.
  definition   The staged field's definition deleted, once the live pages are seen to keep their
               descriptions without it.
  pages        Four additions to page text, from the gallery's answers (Michael, 2026-10-01: "Yes
               to all four page text additions, proceed"): About Us's text, Marion Smith's
               years, "What does the gallery sell?" on the FAQ, a booking line on Schools and
               teachers.
  faq          The FAQ's eight visiting questions under "Visiting", and "Buying prints" over the
               rest. Only once the live theme stops an answer at any heading (store-changes §9c).
  identifiers  A new field on the artist entry, "Described elsewhere", and its 101 values
               (aeo/artist-identifiers.json). The live theme doesn't read it.

The shipping policy is not here: the CLI's store access can't read or write policies, so that one
change went through the Shopify connector (README.md).

Before the first write: the store, the live theme's ID and role, and the review theme's, are
rechecked by hand (AGENTS.md).
"""
import datetime
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from release_run import execute, user_errors  # noqa: E402

DAY = "2026-10-01"
SNAPSHOT = HERE / "snapshots" / f"gallery-answers-{DAY}-before.json"
CREATED = HERE / "created" / f"gallery-answers-{DAY}"
ARTIST_DEFINITION = "gid://shopify/MetaobjectDefinition/23770661161"
STAGED_DEFINITION = "gid://shopify/MetafieldDefinition/273366122793"
ERRORS = "userErrors { field message }"

F = ("Artists For Kids", "Artists for Kids")       # the gallery, 3.1
TYPO = ("Artist for Kids", "Artists for Kids")      # the gallery, 3.2
REID = ("Xhuwaji / Haida Grizzly", "Xhuwaji/Haida Grizzly Bear")  # the gallery, 3.3

# Pages: handle, then field, then (old, new, how many times it must be there).
# Only pages a visitor can reach. The ten pages hidden at the release keep their old words.
PAGES = {
    "contact": {"body": [F + (2,), ("Monday to Friday 8:30am - 4:30pm", "Monday to Friday 8am - 3pm", 1)]},  # 1.1
    "frequently-asked-questions": {"body": [F + (1,), (
        "<p>Shipping costs are calculated and confirmed at checkout (or during the order process, depending on your location and purchase).</p>",
        "<p>Shipping is a flat rate of $20 within Canada.</p>\n<h3>Do you ship outside Canada?</h3>\n<p>Not at this time. We ship within Canada only.</p>",
        1)]},  # 4.2, 4.3, 4.4
    "plan-your-visit": {"body": [F + (2,)]},
    "music-at-the-smith": {"body": [F + (1,)]},
    "artists-for-kids": {"title": [F + (1,)]},
    "artist-in-residence-mark-johnsen": {"body": [F + (2,)]},
    "professional-development": {"body": [F + (1,)]},
    "smith-foundation-scholarships": {"body": [F + (2,)]},
    "brilliance-gala": {"body": [F + (2,)]},
    "artists": {"body": [TYPO + (1,)]},
    "about-artists-for-kids": {"body": [TYPO + (2,), REID + (1,)]},
    "shop": {"body": [REID + (1,)]},
    "permanent-collection": {"custom.intro": [("over 1,000 + Works", "over 1,200 + Works", 1)]},  # the gallery's own number
}

# Entries: (type, handle), then field, then (old, new, how many).
ENTRIES = {
    ("exhibition", "collect-assemble-gather"): {"curator_credit": [F + (1,)]},
    ("exhibition", "one-hundred-artists-deep"): {"body": [F + (1,)]},
    ("exhibition", "from-the-ground"): {"credits": [F + (1,)]},
    ("exhibition", "stitched"): {"credits": [F + (1,)]},
    ("exhibition", "playhouse"): {"credits": [F + (1,)]},
    ("exhibition", "prevailing-landscapes"): {"credits": [F + (1,)]},
    ("exhibition", "robert-young-spatial-understanding"): {"summary": [TYPO + (1,)]},
    ("event", "pd-clay-kit-2026-10-05"): {"title": [F + (1,)]},
    ("event", "pd-clay-kit-2026-10-19"): {"title": [F + (1,)]},
    ("card", "about-artists-for-kids"): {"text": [F + (1,)]},
    ("card", "afk-team-chantal-pinard"): {"text": [F + (1,)]},
    ("card", "afk-team-allison-kerr"): {"text": [TYPO + (1,)]},
    ("card_group", "afk-this-season"): {"heading": [F + (1,)]},
    ("card_group", "afk-guides-by-artists"): {"heading": [F + (1,)]},
    ("document", "george-littlechild-5052"): {"title": [F + (1,)]},
    ("document", "george-littlechild-5056"): {"title": [F + (1,)]},
    ("collection_group", "published-editions"): {"introduction": [REID + (1,)]},
}

# Artists: the handle today, then what changes. A new handle moves the page; the old address redirects.
ARTISTS = {
    "patterson-ewen": {"handle": "paterson-ewen", "name": "Paterson Ewen", "sort_name": "Ewen, Paterson"},          # 3.4
    "charles-gagon": {"handle": "charles-gagnon", "name": "Charles Gagnon", "sort_name": "Gagnon, Charles"},        # 3.4
    "atilla-lukacs": {"handle": "attila-lukacs", "name": "Attila Lukacs", "sort_name": "Lukacs, Attila"},           # 3.4
    "jean-mcewan": {"handle": "jean-mcewen", "name": "Jean McEwen", "sort_name": "McEwen, Jean"},                   # 3.4
    "vancouver-school-collective": {"full_name": "Douglas Coupland, Angela Grossmann, Graham Gillmore and Attila Lukacs"},
    "david-blackwood": {"life_dates": "1941 to 2022"},       # 3.5
    "christopher-pratt": {"life_dates": "1935 to 2022"},     # 3.5
    "joe-fafard": {"life_dates": "1942 to 2019"},            # 3.5
    "gathie-falk": {"life_dates": "1928 to 2025"},           # 3.5
    "victor-cicansky": {"life_dates": "1935 to 2025"},       # 3.5
    "audrey-capel-doray": {"life_dates": "1931 to 2025"},    # 3.5
    "molly-lamb-bobak": {"life_dates": "1920 to 2014"},      # 3.6
    "josie-p-papialuk": {"life_dates": "1918 to 1996"},      # 8.1: "Yes, record dates are correct"
    "newgaleak-qimirpik": {"life_dates": "1937 to 2007"},    # 8.1: "Yes, Nuyaliaq Qimirpik, 1937-2007"
    "ann-kipling": {"life_dates": "1934 to 2023"},           # 6.3: her biography's own years
}
# The Smith Foundation's description starts as its page text does, for 40 letters. The live theme
# takes such a search listing for one Shopify made from the text, and drops it (meta-tags, DS-160).
# So its staged description stays until the release that compares more of the two (DS-196); then
# `unstage` deletes it and `definition` deletes the field.
KEEP_STAGED = {"the-smith-foundation"}
# Four additions to page text (proposals/gallery-answers/README.md, "Left for Michael"), each the
# gallery's own answer with its typing mistakes fixed.
# About Us had no text: the gallery's five sentences on what it is (2.3), then who owns it and
# when it opened (2.1, 2.2).
ABOUT_US = "\n".join(f"<p>{p}</p>" for p in [
    "The Gordon Smith Gallery is open to the entire community through admission by donation, with engaged Art Education programs and experiences integrated into every exhibition through Artists for Kids. The Gordon Smith Gallery is a space to consider, to ask, to witness, to open spaces to understand about ourselves and each other.",
    "The Artists for Kids and Gordon Smith Gallery permanent collection houses a collection of over 1,200 artworks by Canadian Artists from across the country, and has published over 150 limited edition prints from renowned Canadian Artists. We are the only gallery in Canada dedicated to Young Artists, with art education at the forefront of every curatorial choice.",
    "Artists for Kids has collaborated with almost every collaborative printer in Canada, in every region in Canada, the archive of our extensive collection of limited editions from renowned Canadian Artists has become a national resource of print activity in Canada of almost 40 years.",
    "The Gallery opened in 2012. It is owned by the North Vancouver School District, activated jointly by Artists for Kids and the Smith Foundation, and funded jointly through the school district and the Smith Foundation.",
])
# Marion Smith's years, as the gallery gave them (3.7). Michael: trust the document.
MARION = ("<strong>Marion Smith</strong> was said to have two careers", "<strong>Marion Smith</strong> (1941 to 2018), was said to have two careers")
# "His wife", not "His late wife", now that the sentence gives her years. Michael, 2026-10-01:
# "could just be 'His wife, Marion Smith (1941 to 2018), was said to have two careers' because
# they are both dead".
LATE = ("His late wife, <strong>Marion Smith</strong>", "His wife, <strong>Marion Smith</strong>")
# What the gallery sells (2.5), as the FAQ's first question.
FAQ_FIRST = "<h3>Are all prints limited edition?</h3>"
FAQ_SELLS = ("<h3>What does the gallery sell?</h3>\n<p>The Gallery sells limited edition prints from renowned Canadian Artists that were gifted directly "
             "to Artists for Kids to directly fund Art Education programming.</p>\n")
# How a class visit is booked (4.1), as Schools and teachers' opening line. The page had no text.
SCHOOLS = '<p>To book a class visit, use the registration link on the <a href="/pages/gallery-program">Gallery Program</a> page.</p>'

# The FAQ's visiting questions (the gallery, 4.5: "Yes"). The answers are Plan your visit's own
# words, as drafted in proposals/aeo-geo-review.md, "Drafts for the gallery".
FAQ_TITLE = "<h2>Frequently Asked Questions</h2>"
FAQ_VISITING = [
    ("When is the gallery open?", "Thursday to Saturday, 12 to 4 PM."),
    ("How much is admission?", "Admission to the Gordon Smith Gallery is by donation."),
    ("Where is the gallery?", "2121 Lonsdale Avenue, North Vancouver, on the west side of Lonsdale Avenue, three blocks south of Exit 18 off the Trans Canada Highway."),
    ("How do I get there by public transport?", "From downtown Vancouver, take the SeaBus to Lonsdale Quay, then the 229 or 230 bus towards Upper Lonsdale. The stop at 21st and Lonsdale is across the street from the gallery."),
    ("Where can I park?", "One-hour street parking surrounds the gallery, and pay parking is on Lonsdale Avenue. There are a few underground spaces on P1 and P2, except on weekends and holidays."),
    ("Is the gallery wheelchair accessible?", "Yes. There are accessible washrooms, an elevator from the underground parking, accessible parking on P1 and P2, and a ramp to the south entrance from Lonsdale Avenue."),
    ("Are assistance dogs welcome?", "Yes. A water bowl is available on request."),
    ("What can families do at the gallery?", "Explore + Create is a drop-in art program for families with children ages 5 to 12, Saturdays from 1 to 3 PM."),
]
RENAMED = {new["handle"]: old for old, new in ARTISTS.items() if "handle" in new}
BIOGRAPHIES = json.loads((HERE / "gallery-answers" / "biographies.json").read_text())
BIOGRAPHY_ARTISTS = ["gordon-smith", "jack-shadbolt", "bill-reid", "ann-kipling"]

Q = {
    "page": "mutation($id: ID!, $page: PageUpdateInput!) { pageUpdate(id: $id, page: $page) { "
            "page { id handle title updatedAt } " + ERRORS + " } }",
    "fields": "mutation($metafields: [MetafieldsSetInput!]!) { metafieldsSet(metafields: $metafields) { "
              "metafields { id namespace key type value owner { ... on Page { id handle } } } " + ERRORS + " } }",
    "entry": "mutation($id: ID!, $metaobject: MetaobjectUpdateInput!) { metaobjectUpdate(id: $id, metaobject: $metaobject) { "
             "metaobject { id handle displayName updatedAt } " + ERRORS + " } }",
    "files": "mutation($files: [FileUpdateInput!]!) { fileUpdate(files: $files) { files { id alt fileStatus } " + ERRORS + " } }",
    "unset": "mutation($metafields: [MetafieldIdentifierInput!]!) { metafieldsDelete(metafields: $metafields) { "
             "deletedMetafields { ownerId namespace key } " + ERRORS + " } }",
    "definition": "mutation($id: ID!) { metafieldDefinitionDelete(id: $id, deleteAllAssociatedMetafields: false) { "
                  "deletedDefinitionId " + ERRORS + " } }",
    "artist_field": "mutation($id: ID!, $definition: MetaobjectDefinitionUpdateInput!) { metaobjectDefinitionUpdate(id: $id, definition: $definition) { "
                    "metaobjectDefinition { id fieldDefinitions { key name type { name } } } " + ERRORS + " } }",
}
READ_PAGES = ("query($first: Int!, $after: String) { pages(first: $first, after: $after, sortKey: ID) { nodes { id handle title isPublished body "
              "metafields(first: 40) { nodes { namespace key type value } } } pageInfo { hasNextPage endCursor } } }")
READ_ENTRIES = ("query($first: Int!, $after: String, $type: String!) { metaobjects(type: $type, first: $first, after: $after) { "
                "nodes { id handle fields { key type value } } pageInfo { hasNextPage endCursor } } }")
READ_FILES = "query($ids: [ID!]!) { nodes(ids: $ids) { ... on MediaImage { id alt } } }"
READ_ARTIST_FIELDS = "query { metaobjectDefinitionByType(type: \"artist\") { id fieldDefinitions { key } } }"


def read(query, variables=None):
    data, err = execute(query, variables or {}, False)
    if err:
        sys.exit(err)
    return data


def read_all(query, root, variables=None):
    out, after = [], None
    while True:
        conn = read(query, dict(variables or {}, first=100, after=after))[root]
        out += conn["nodes"]
        if not conn["pageInfo"]["hasNextPage"]:
            return out
        after = conn["pageInfo"]["endCursor"]


def pages():
    out = {}
    for p in read_all(READ_PAGES, "pages"):
        p["fields"] = {f"{m['namespace']}.{m['key']}": m for m in p.pop("metafields")["nodes"]}
        out[p["handle"]] = p
    return out


def entries(kind):
    out = {}
    for e in read_all(READ_ENTRIES, "metaobjects", {"type": kind}):
        e["values"] = {f["key"]: f["value"] for f in e["fields"]}
        e["types"] = {f["key"]: f["type"] for f in e.pop("fields")}
        out[e["handle"]] = e
    return out


def replaced(text, edits, where):
    """The text with each edit made. An edit already made is skipped; one that fits neither way stops the run."""
    for old, new, count in edits:
        if text.count(old) == count:
            text = text.replace(old, new)
        elif old in text or new not in text:
            sys.exit(f"STOPPED: {where}: expected {count} of {old!r}, found {text.count(old)}")
    return text


def rich_text(paragraphs):
    return json.dumps({"type": "root", "children": [
        {"type": "paragraph", "children": [{"type": "text", "value": p}]} for p in paragraphs]}, ensure_ascii=False)


def plain(rich):
    """A rich text value's paragraphs, for comparing with what we would write."""
    if not rich:
        return []
    return ["".join(c.get("value", "") for c in block.get("children", [])) for block in json.loads(rich)["children"]]


def step_text():
    out, store = [], pages()
    for handle, fields in PAGES.items():
        p = store[handle]
        if not p["isPublished"]:
            sys.exit(f"STOPPED: page {handle} is hidden")
        change, before = {}, {}
        for field, edits in fields.items():
            if field in ("title", "body"):
                new = replaced(p[field], edits, f"page {handle} {field}")
                if new != p[field]:
                    change[field], before[field] = new, p[field]
            else:
                m = p["fields"][field]
                new = replaced(m["value"], edits, f"page {handle} {field}")
                if new != m["value"]:
                    ns, key = field.split(".")
                    out.append((f"page {handle} {field}", "fields", {"metafields": [
                        {"ownerId": p["id"], "namespace": ns, "key": key, "type": m["type"], "value": new}]}, {field: m["value"]}))
        if change:
            out.append((f"page {handle} {' and '.join(change)}", "page", {"id": p["id"], "page": change}, before))
    kinds = {}
    for (kind, handle), fields in ENTRIES.items():
        kinds.setdefault(kind, entries(kind))
        e = kinds[kind][handle]
        change, before = [], {}
        for field, edits in fields.items():
            new = replaced(e["values"][field], edits, f"{kind} {handle} {field}")
            if new != e["values"][field]:
                change.append({"key": field, "value": new})
                before[field] = e["values"][field]
        if change:
            out.append((f"{kind} {handle} {' and '.join(before)}", "entry", {"id": e["id"], "metaobject": {"fields": change}}, before))
    return out


def step_artists():
    out, store = [], entries("artist")
    for old, new in ARTISTS.items():
        e = store.get(old) or store.get(new.get("handle"))
        if not e:
            sys.exit(f"STOPPED: no artist {old}")
        change = {"fields": [{"key": k, "value": v} for k, v in new.items() if k != "handle" and e["values"].get(k) != v]}
        before = {f["key"]: e["values"].get(f["key"]) for f in change["fields"]}
        if "handle" in new and e["handle"] != new["handle"]:
            change.update(handle=new["handle"], redirectNewHandle=True)
            before["handle"] = e["handle"]
        if not change["fields"]:
            del change["fields"]
        if change:
            out.append((f"artist {old}: {', '.join(before)}", "entry", {"id": e["id"], "metaobject": change}, before))
    for handle in BIOGRAPHY_ARTISTS:
        e = store[handle]
        if plain(e["values"].get("biography")) != BIOGRAPHIES[handle]:
            out.append((f"artist {handle}: biography", "entry", {"id": e["id"], "metaobject": {"fields": [
                {"key": "biography", "value": rich_text(BIOGRAPHIES[handle])}]}}, {"biography": e["values"].get("biography")}))
    return out


def step_alt():
    words = json.loads((HERE / "aeo" / "alt.json").read_text())
    ids = {f["filename"]: f["id"] for f in json.loads((HERE / "snapshots" / "alt-text-2026-09-29-before.json").read_text())["files"]}
    now = {n["id"]: n["alt"] for n in read(READ_FILES, {"ids": list(ids.values())})["nodes"]}
    todo = [(name, ids[name], w["alt"]) for name, w in words.items() if now[ids[name]] != w["alt"]]
    if not todo:
        return []
    return [(f"alt text on {len(todo)} images: {', '.join(t[0] for t in todo)}", "files",
             {"files": [{"id": i, "alt": alt} for _, i, alt in todo]}, {i: now[i] for _, i, _ in todo})]


def descriptions():
    return json.loads((HERE / "aeo" / "descriptions.json").read_text())["pages"]


def step_descriptions():
    """The staged field, which the theme reads first, on the pages that still hold one. So visitors
    and engines got the approved words at once. A page without a staged description is `listing`'s."""
    store = {p["id"]: p for p in pages().values()}
    sets, before = [], {}
    for handle, d in descriptions().items():
        now = store[d["id"]]["fields"].get("custom.release_description", {}).get("value")
        if now is not None and now != d["description"]:
            sets.append({"ownerId": d["id"], "namespace": "custom", "key": "release_description", "type": "multi_line_text_field", "value": d["description"]})
            before[handle] = now
    return [(f"staged descriptions: {', '.join(before)}", "fields", {"metafields": sets}, before)] if sets else []


def step_listing():
    """Each page's description in its search engine listing (global.description_tag), 25 to a call."""
    store = {p["id"]: p for p in pages().values()}
    sets, before = [], {}
    for handle, d in descriptions().items():
        now = store[d["id"]]["fields"].get("global.description_tag", {}).get("value")
        if now != d["description"]:
            sets.append({"ownerId": d["id"], "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": d["description"]})
            before[handle] = now
    return [(f"search listing descriptions {i + 1} to {i + len(sets[i:i + 25])}", "fields", {"metafields": sets[i:i + 25]},
             {h: before[h] for h in list(before)[i:i + 25]}) for i in range(0, len(sets), 25)]


def step_unstage():
    """Delete the staged descriptions, but only where the search listing already says the same."""
    store = pages()
    gone, before = [], {}
    for handle, p in store.items():
        staged = p["fields"].get("custom.release_description", {}).get("value")
        if staged is None or handle in KEEP_STAGED:
            continue
        listed = p["fields"].get("global.description_tag", {}).get("value")
        if listed != staged:
            sys.exit(f"STOPPED: {handle}: its search listing doesn't say what its staged description says. Run `listing` first.")
        gone.append({"ownerId": p["id"], "namespace": "custom", "key": "release_description"})
        before[handle] = staged
    return [(f"staged descriptions {i + 1} to {i + len(gone[i:i + 25])} deleted", "unset", {"metafields": gone[i:i + 25]},
             {h: before[h] for h in list(before)[i:i + 25]}) for i in range(0, len(gone), 25)]


def step_definition():
    """Delete the staged field's definition, once no page holds a staged description."""
    left = [h for h, p in pages().items() if "custom.release_description" in p["fields"]]  # KEEP_STAGED too
    if left:
        sys.exit(f"STOPPED: {len(left)} pages still hold a staged description. Run `unstage` first.")
    have = read("query { metafieldDefinitions(first: 50, ownerType: PAGE, namespace: \"custom\") { nodes { id key } } }")["metafieldDefinitions"]["nodes"]
    if STAGED_DEFINITION not in [d["id"] for d in have]:
        return []
    return [("release_description definition deleted", "definition", {"id": STAGED_DEFINITION},
             {"definition": {"id": STAGED_DEFINITION, "namespace": "custom", "key": "release_description", "name": "Release description",
                             "type": "multi_line_text_field", "ownerType": "PAGE", "pinned": True, "access": "storefront read"}})]


def step_pages():
    """Four additions to page text. Each is skipped once its words are on the page."""
    store, out = pages(), []

    def write(handle, body, what):
        p = store[handle]
        out.append((f"page {handle} body: {what}", "page", {"id": p["id"], "page": {"body": body}}, {"body": p["body"]}))

    for handle, text, what in (("about-us", ABOUT_US, "what the gallery is, who owns it and when it opened"),
                               ("schools-and-teachers", SCHOOLS, "how a class visit is booked")):
        body = store[handle]["body"] or ""
        if not body.strip():
            write(handle, text, what)
        elif "".join(text.split()) not in "".join(body.split()):
            sys.exit(f"STOPPED: page {handle} has text of its own now; add the new words by hand")
    body = new = store["gordon-and-marion"]["body"]
    if MARION[1] not in new:
        if new.count(MARION[0]) != 1:
            sys.exit("STOPPED: Gordon and Marion no longer has the sentence about Marion Smith as it was")
        new = new.replace(MARION[0], MARION[1])
    if LATE[0] in new:
        if new.count(LATE[0]) != 1:
            sys.exit("STOPPED: Gordon and Marion says \"His late wife\" more than once")
        new = new.replace(LATE[0], LATE[1])
    if new != body:
        write("gordon-and-marion", new, "Marion Smith's years, and \"His wife\"")
    body = store["frequently-asked-questions"]["body"]
    if "<h3>What does the gallery sell?</h3>" not in body:
        if body.count(FAQ_FIRST) != 1:
            sys.exit("STOPPED: the FAQ no longer starts with its first question")
        write("frequently-asked-questions", body.replace(FAQ_FIRST, FAQ_SELLS + FAQ_FIRST), "What does the gallery sell?")
    return out


def step_faq():
    """The visiting questions lead the FAQ under their own heading; "Buying prints" heads the rest."""
    p = pages()["frequently-asked-questions"]
    if "<h2>Visiting</h2>" in p["body"]:
        return []
    if p["body"].count(FAQ_TITLE) != 1:
        sys.exit("STOPPED: the FAQ no longer starts with its title as a heading")
    visiting = "\n".join(f"<h3>{q}</h3>\n<p>{a}</p>" for q, a in FAQ_VISITING)
    body = p["body"].replace(FAQ_TITLE, f"<h2>Visiting</h2>\n{visiting}\n<h2>Buying prints</h2>")
    return [("page frequently-asked-questions body: visiting questions", "page", {"id": p["id"], "page": {"body": body}}, {"body": p["body"]})]


def step_identifiers():
    out = []
    have = [f["key"] for f in read(READ_ARTIST_FIELDS)["metaobjectDefinitionByType"]["fieldDefinitions"]]
    if "described_at" not in have:
        out.append(("artist field: Described elsewhere", "artist_field", {"id": ARTIST_DEFINITION, "definition": {"fieldDefinitions": [{"create": {
            "key": "described_at", "name": "Described elsewhere", "type": "list.url",
            "description": "Addresses that describe this artist elsewhere: Wikidata, Wikipedia, the Getty's list of artists. For search engines; not shown on the page."}}]}},
            {"fields": have}))
    store = entries("artist")
    for a in json.loads((HERE / "aeo" / "artist-identifiers.json").read_text())["artists"]:
        if not a.get("same_as"):
            continue
        e = store.get(a["handle"]) or store.get({v: k for k, v in RENAMED.items()}.get(a["handle"]))
        if not e:
            sys.exit(f"STOPPED: no artist {a['handle']}")
        value = json.dumps([a["same_as"][k] for k in ("wikidata", "wikipedia", "getty_ulan") if k in a["same_as"]])
        if json.loads(e["values"].get("described_at") or "[]") != json.loads(value):
            out.append((f"artist {e['handle']}: described elsewhere", "entry",
                        {"id": e["id"], "metaobject": {"fields": [{"key": "described_at", "value": value}]}},
                        {"described_at": e["values"].get("described_at")}))
    return out


STEPS = {"text": step_text, "artists": step_artists, "alt": step_alt, "descriptions": step_descriptions,
         "listing": step_listing, "unstage": step_unstage, "definition": step_definition, "identifiers": step_identifiers,
         "pages": step_pages, "faq": step_faq}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in STEPS:
        sys.exit(__doc__)
    step, go = sys.argv[1], "--go" in sys.argv[2:]
    todo = STEPS[step]()
    if not go:
        for name, kind, variables, before in todo:
            print(f"would run {kind}: {name}")
            if "--full" in sys.argv[2:]:
                print("   before:", json.dumps(before, ensure_ascii=False)[:1500])
                print("   send:  ", json.dumps(variables, ensure_ascii=False)[:1500])
        print(f"{len(todo)} call(s) listed; nothing changed")
        sys.exit(0)
    if todo:
        snap = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {
            "taken": DAY, "what": "What each step of gallery_answers.py was about to change, read from the store just before it ran. To undo a call, send its `before` values back with the same kind of call."}
        taken = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        snap.setdefault(step, []).extend({"call": name, "kind": kind, "id": variables.get("id"), "read": taken, "before": before} for name, kind, variables, before in todo)
        SNAPSHOT.write_text(json.dumps(snap, ensure_ascii=False, indent=1) + "\n")
    CREATED.mkdir(parents=True, exist_ok=True)
    path = CREATED / f"{step}.json"
    log = json.loads(path.read_text()) if path.exists() else []
    for n, (name, kind, variables, before) in enumerate(todo):
        data, err = execute(Q[kind], variables, True)
        errors = user_errors(data) if not err else [{"message": err}]
        short = json.dumps(variables, ensure_ascii=False)
        log.append({"call": name, "kind": kind, "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                    "variables": variables if len(short) < 4000 else {"id": variables.get("id"), "sent": f"({len(short)} characters; the words are in this script and its data files)"},
                    "answer": data, "errors": errors})
        path.write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n")
        if errors:
            sys.exit(f"STOPPED at {name}: {errors}\n{n} call(s) made before it; see {path}")
        print(f"done {kind}: {name}")
    print(f"{len(todo)} call(s) made")
