#!/usr/bin/env python3
"""The store changes from the follow-up questions (the gallery's follow-up doc, 2026-10-01),
the ones Michael answered himself or let us make without asking the gallery. Michael, 2026-10-01,
on the triage of the doc's 92 questions: "Yes to all my questions and apply all other changes".
The record: proposals/gallery-answers/2026-10-01-follow-up.md.

  python3 proposals/store-writes/followup_answers.py <step> [--go] [--full]
  steps: names, text, lessons, collection, alt, tiles, prints, frame

Each step reads the store first and sends only what still differs: a second run of a finished step
lists nothing. Without --go it prints each call and changes nothing. With --go it saves what it is
about to change to snapshots/follow-up-2026-10-01-before.json, makes the calls one at a time through
the Shopify CLI (`shopify store execute`), stops at the first error, and writes the store's answers
to created/follow-up-2026-10-01/<step>.json.

  names       Two artists' names (1, 50): Nuyaliaq Qimirpik and Leonhard Epp, their pages moved,
              the old addresses redirected. Irene F. Whittome and Leonhard Epp in the exhibitions'
              artist lists, so the names link (50). Lotus L. Kang on Unfixed (3). Curly quotes in
              Against the Latitude of "Progress" (40).
  text        Pages, cards and entries: names and typos (19, 20), the Paradise Valley photo's year
              (21), the volunteer email (25), Sara-Jeanne Bourget's page (63), "Artists for Kids"
              for "AFK" in running text, one spelling of Artists-in-Residence, programme names in
              sentence case and one name per programme (40), and link labels that say what they
              do (39).
  lessons     The works named in four ArtReach lessons, with the collection's years and title (22).
  collection  The collection's records (23) and style (24, 55): medium in sentence case, one
              spelling of watercolour, AP for artist's proofs, undated and estimated years written
              one way.
  alt         A full stop at the end of the 47 artwork image descriptions that are sentences (24).
  tiles       From the Ground shows Turtle Clan Searchers as one tile, not eight (48).
  prints      The 21 prints' descriptions without the lines that repeat the label (74; P-21, P-22,
              release.py's clean-up), one form of photo credit, and the Shop labels (75): medium in
              sentence case, a shorter medium for Russna Kaur's print (its full text stays in the
              description), one form of size, Pender Harbour's proof as "AP (ed. of 100)".
  frame       The Russna Kaur frame loses the photo named like an Adobe Stock preview, and shows the
              frame photo the other frames use (76).

Not here: the newsletter's automated sign-ups (16), unsubscribed through the Shopify connector,
since the CLI's store access can't read customers (README.md); the theme settings (15, 39, 40),
pushed to the live theme as small fixes (AGENTS.md).

Before the first write: the store, the live theme's ID and role, and the review theme's, are
rechecked by hand (AGENTS.md).
"""
import datetime
import json
import pathlib
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gallery_answers import entries, pages, read, replaced  # noqa: E402
from release_run import execute, user_errors  # noqa: E402

DAY = "2026-10-01"
SNAPSHOT = HERE / "snapshots" / f"follow-up-{DAY}-before.json"
CREATED = HERE / "created" / f"follow-up-{DAY}"
ERRORS = "userErrors { field message }"

Q = {
    "page": "mutation($id: ID!, $page: PageUpdateInput!) { pageUpdate(id: $id, page: $page) { page { id handle title updatedAt } " + ERRORS + " } }",
    "fields": "mutation($metafields: [MetafieldsSetInput!]!) { metafieldsSet(metafields: $metafields) { metafields { id namespace key value } " + ERRORS + " } }",
    "entry": "mutation($id: ID!, $metaobject: MetaobjectUpdateInput!) { metaobjectUpdate(id: $id, metaobject: $metaobject) { "
             "metaobject { id handle displayName updatedAt } " + ERRORS + " } }",
    "files": "mutation($files: [FileUpdateInput!]!) { fileUpdate(files: $files) { files { id alt fileStatus } " + ERRORS + " } }",
    "product": "mutation($product: ProductUpdateInput!) { productUpdate(product: $product) { product { id handle title updatedAt } " + ERRORS + " } }",
}

# ---------------------------------------------------------------------------
# names (1, 3, 50, 40)

ARTISTS = {
    # The gallery: "Yes, Nuyaliaq Qimirpik, 1937-2007". The name the catalogue had stays as another name.
    "newgaleak-qimirpik": {"handle": "nuyaliaq-qimirpik", "name": "Nuyaliaq Qimirpik", "sort_name": "Qimirpik, Nuyaliaq", "other_names": "Newgaleak"},
    # The City of Vancouver's Public Art Registry and his obituary (1932 to 2018) spell it Leonhard.
    "leonard-epp": {"handle": "leonhard-epp", "name": "Leonhard Epp", "sort_name": "Epp, Leonhard"},
}
# Exhibitions: field, then (old, new, how many times it must be there).
NAME_ENTRIES = {
    ("exhibition", "beyond-the-horizon"): {"artists": [('"Irene Whittome"', '"Irene F. Whittome"', 1)]},
    ("exhibition", "figurative-contemplation"): {"body": [("Irene Whittome", "Irene F. Whittome", 1)]},
    ("exhibition", "unfixed"): {"subtitle": [("Laurie Kang", "Lotus L. Kang", 1)],
                                "artists": [('"Laurie Kang"', '"Lotus L. Kang"', 1)],
                                "summary": [("Laurie Kang", "Lotus L. Kang", 1)]},
    ("exhibition", "against-the-latitude-of-progress"): {"title": [('Latitude of "Progress"', "Latitude of “Progress”", 1)]},
}

# ---------------------------------------------------------------------------
# text (19, 20, 21, 25, 39, 40, 63)

RESIDENCY = re.compile(r"\b(Artists?)[ -][Ii]n[ -][Rr]esidence\b")
AFK = re.compile(r"\bAFK('s)?\b(?!\))")
PROGRAMMES = [("Music At The Smith", "Music at the Smith"), ("Art In Good Company", "Art in Good Company"), ("Explore & Create", "Explore + Create")]

SARA_TITLE = "<h2>Drawing Artist-in-Residence Sara-Jeanne Bourget</h2>\n"
SARA = [("<p>This November, Artists for Kids is excited to offer an Artist-in-Residence program for secondary students in grades 10, 11, and 12. "
         "During two school days, students who are nominated will have the opportunity to work with artist Sara-Jeanne Bourget",
         "<p>In November 2025, Artists for Kids offered an Artist-in-Residence program for secondary students in grades 10, 11, and 12. "
         "During two school days, students who were nominated had the opportunity to work with artist Sara-Jeanne Bourget", 1),
        ("<h2>Artist Bio</h2>", "<h2>Sara-Jeanne Bourget Biography</h2>", 1)]
VOLUNTEER = ('volunteer form (PDF)</a>. Questions?',
             'volunteer form (PDF)</a> and email it with your CV to <a href="mailto:sgvolunteer1@gmail.com">sgvolunteer1@gmail.com</a>, as the form asks. Questions?', 1)

# Pages: handle, then field ("title", "body" or a page field), then (old, new, count).
PAGE_EDITS = {
    "permanent-collection": {"body": [("Graham Gilmore", "Graham Gillmore", 1)]},                       # 19
    "artist-in-residence-mark-johnsen": {"body": [("artist Mark Johnson", "artist Mark Johnsen", 1)]},   # 19
    "paradise-valley-summer-camp": {"body": [("Sara Jean Bourget", "Sara-Jeanne Bourget", 2)]},         # 19
    "after-school-art": {"body": [("If you child", "If your child", 1)]},                                # 20
    "smith-foundation-supporters": {"body": [("Misson Hill Winery", "Mission Hill Winery", 1),
                                             ("Benevity Community Impact Fun ", "Benevity Community Impact Fund ", 1)]},  # 20
    "artists-for-kids": {"body": [("At Paradise Valley Summer Camp in 1994", "At Paradise Valley Summer Camp in 1996", 1)],  # 21
                         "custom.cta": [('"text":"Download the guide"', '"text":"Get the program guide"', 1)]},              # 39
    "volunteer": {"body": [VOLUNTEER]},                                                                  # 25
    "artist-in-residence-sara-jeanne-bourget": {"body": SARA},                                           # 63
    "the-smith-foundation": {"custom.cta": [('"text":"2025 A Year In Review"', '"text":"Read the 2025 year in review"', 1)]},  # 39
    "artreach-videos": {"body": [(">Download Artists for Kids Learning Guides<", ">See the learning guides<", 1),
                                 (">Register to borrow Artists for Kids Learning Kits<", ">Borrow a learning kit<", 1)]},   # 39
}
ENTRY_EDITS = {
    ("card", "foundation-donations"): {"link": [('"text":"Donate Today"', '"text":"Donate"', 1)]},             # 39
    ("card", "programs-explore-create"): {"title": [("Explore + Create Saturdays", "Explore + Create", 1)]},  # 40
    ("card", "afk-explore-create"): {"title": [("Explore + Create Saturdays", "Explore + Create", 1)]},       # 40
}
# Where the names across the site (40) are changed: text only, never an address or a file name.
SWEEP_PAGE_FIELDS = ("title", "body", "custom.eyebrow", "custom.intro", "custom.hero_caption", "global.description_tag")
SWEEP_ENTRIES = {"card": ("title", "text"), "card_group": ("heading", "intro"), "exhibition": ("summary", "body", "installation_credit", "credits"),
                 "event": ("title", "summary", "body"), "document": ("title",), "lesson": ("summary", "body")}


def names_in(text):
    """Text with the names across the site made one (40)."""
    text = RESIDENCY.sub(lambda m: f"{m.group(1)}-in-Residence", text)
    text = AFK.sub(lambda m: "Artists for Kids'" if m.group(1) else "Artists for Kids", text)
    for old, new in PROGRAMMES:
        text = text.replace(old, new)
    return text


def outside_tags(html, fn):
    """fn applied to the words of an HTML text, never to its tags (addresses, file names, attributes)."""
    return "".join(part if part.startswith("<") else fn(part) for part in re.split(r"(<[^>]*>)", html))


def in_rich_text(value, fn):
    """fn applied to every text in a rich text field's JSON."""
    doc = json.loads(value)
    changed = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "text" and isinstance(node.get("value"), str):
                new = fn(node["value"])
                if new != node["value"]:
                    node["value"] = new
                    changed.append(new)
            for child in node.get("children", []):
                walk(child)
    walk(doc)
    return json.dumps(doc, ensure_ascii=False, separators=(",", ":")) if changed else value


def swept(value, kind):
    if value is None or value == "":
        return value
    if kind == "rich_text_field":
        return in_rich_text(value, names_in)
    if kind == "html":
        return outside_tags(value, names_in)
    return names_in(value)


def step_names():
    out, store = [], entries("artist")
    for old, new in ARTISTS.items():
        e = store.get(old) or store.get(new["handle"])
        change = {"fields": [{"key": k, "value": v} for k, v in new.items() if k != "handle" and e["values"].get(k) != v]}
        before = {f["key"]: e["values"].get(f["key"]) for f in change["fields"]}
        if e["handle"] != new["handle"]:
            change.update(handle=new["handle"], redirectNewHandle=True)
            before["handle"] = e["handle"]
        if not change["fields"]:
            del change["fields"]
        if change:
            out.append((f"artist {old}: {', '.join(before)}", "entry", {"id": e["id"], "metaobject": change}, before))
    out += entry_calls(NAME_ENTRIES)
    return out


def entry_calls(spec):
    out, kinds = [], {}
    for (kind, handle), fields in spec.items():
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


def step_text():
    out, store = [], pages()
    for handle, p in store.items():
        page_change, before, sets = {}, {}, []
        for field in SWEEP_PAGE_FIELDS:
            if field in ("title", "body"):
                now = p[field] or ""
                new = replaced(now, PAGE_EDITS.get(handle, {}).get(field, []), f"page {handle} {field}")
                new = swept(new, "html" if field == "body" else "text")
                if field == "body" and handle == "artist-in-residence-sara-jeanne-bourget" and new.startswith(SARA_TITLE):
                    new = new[len(SARA_TITLE):]  # 63: the first heading repeated the page's title
                if new != now:
                    page_change[field], before[field] = new, now
            else:
                m = p["fields"].get(field)
                if not m:
                    continue
                new = swept(m["value"], m["type"])
                if new != m["value"]:
                    ns, key = field.split(".")
                    sets.append({"ownerId": p["id"], "namespace": ns, "key": key, "type": m["type"], "value": new})
                    before[field] = m["value"]
        for field, edits in PAGE_EDITS.get(handle, {}).items():
            if field in ("title", "body"):
                continue
            m = p["fields"][field]
            new = replaced(m["value"], edits, f"page {handle} {field}")
            if new != m["value"]:
                ns, key = field.split(".")
                sets.append({"ownerId": p["id"], "namespace": ns, "key": key, "type": m["type"], "value": new})
                before[field] = m["value"]
        if page_change:
            out.append((f"page {handle} {' and '.join(page_change)}", "page", {"id": p["id"], "page": page_change},
                        {k: v for k, v in before.items() if k in page_change}))
        if sets:
            out.append((f"page {handle} {', '.join(s['namespace'] + '.' + s['key'] for s in sets)}", "fields", {"metafields": sets},
                        {k: v for k, v in before.items() if k not in page_change}))
    for kind, fields in SWEEP_ENTRIES.items():
        for handle, e in entries(kind).items():
            change, before = [], {}
            for field in fields:
                now = e["values"].get(field)
                if not now:
                    continue
                new = replaced(now, ENTRY_EDITS.get((kind, handle), {}).get(field, []), f"{kind} {handle} {field}")
                new = swept(new, e["types"][field])
                if new != now:
                    change.append({"key": field, "value": new})
                    before[field] = now
            for field, edits in ENTRY_EDITS.get((kind, handle), {}).items():
                if field in fields:
                    continue
                new = replaced(e["values"][field], edits, f"{kind} {handle} {field}")
                if new != e["values"][field]:
                    change.append({"key": field, "value": new})
                    before[field] = e["values"][field]
            if change:
                out.append((f"{kind} {handle} {' and '.join(before)}", "entry", {"id": e["id"], "metaobject": {"fields": change}}, before))
    return out


# ---------------------------------------------------------------------------
# lessons (22): the works as the collection records them. Josie Papialuk's print stays as the
# lesson names it ("All Kinds of Birds Flying North in Spring"): the collection's shorter title may
# be the one cut short, so that one waits for the gallery.

LESSONS = {
    ("lesson", "artists-for-kids-trace-monotype-kit-self-portraits"): {"inspired_by": [("Harlequin (2019)", "Harlequin (2003)", 1),
                                                                                        ("Plains Cree Chiefs (1996)", "Plains Cree Chiefs (1995)", 1)]},
    ("lesson", "transforming-words-into-art"): {"inspired_by": [('"value":" (2009)"', '"value":" (2004)"', 1)]},
    ("lesson", "landscape-painting"): {"inspired_by": [('"value":" (2009)"', '"value":" (2006)"', 1)]},
    ("lesson", "stencilling-with-found-objects-and-images"): {"inspired_by": [('"value":"Figure Maquette in Studio at Night"',
                                                                               '"value":"Painting and Figure Maquette in Studio at Night"', 1)]},
}


def step_lessons():
    return entry_calls(LESSONS)


# ---------------------------------------------------------------------------
# collection (23, 24, 55)

RECORDS = {  # 23: accession number's handle, then fields
    "reid001-2": {"year": "1988"},                                  # its other half's year; "General note" was a stray column
    "barr017": {"year": "n.d."}, "barr018": {"year": "n.d."}, "barr025": {"year": "n.d."},   # the artist's life, not the work's date
    "perr001": {"year": "n.d."}, "perr002": {"year": "n.d."}, "perr003": {"year": "n.d."},
    "jeff002": {"year": "n.d.", "medium": "Paper, rubber and graphite"},   # "Paper" slipped into the year; JEFF003 reads the same way
    "barr002": {"medium": "Lithograph on paper", "edition": "21/28"},
    "smit028": {"edition": "AP (ed. of 100)"},                      # Pender Harbour's proof, like Mount Orpheus' "AP (ed. of 30)"
    "vick-c001-7": {"accession_number": "VICK.C001.7"},
}
YEARS = {  # 55: undated and estimated years, one way. Ranges and signed dates stay as written.
    "ND": "n.d.", "N.D.": "n.d.", "N/A": "n.d.", "N.D. [20--]": "n.d.",
    "20th Century": "20th century", "circa 20th Century": "circa 20th century", "circa 20c": "circa 20th century",
    "n.d. [circa 20c]": "circa 20th century", "estimated date: 196-": "circa 1960s", "Circa 2012": "circa 2012",
}
EDITIONS = {"A/P": "AP", "A/P I/V": "AP I/V", "A/P V/V": "AP V/V", "A/P III/V": "AP III/V", "AP v/v": "AP V/V", "6/10AP": "AP 6/10"}
# Medium in sentence case (24). Kept as written: names (papers, brands, peoples, places) and capitals
# that are initials. Left alone: mediums that hold a work's own name or a typed size.
KEEP = {"Epson", "Premium", "Luster", "Hahnemühle", "BFK", "Rives", "Reeves", "Arches", "Somerset", "Natural", "Stonehenge", "Basingwerk",
        "Legacy", "Baryta", "Photorag", "Dibond", "Cintra", "Pentel", "Geofilm", "Varathane", "Lucite", "Xerox", "Flashe", "Styrofoam",
        "Conte", "Coast", "Salish", "MDF", "B&W", "3D"}
UNTOUCHED = ("Crow", "Tall Bird", "Large Gull", "Green Tree", "Red Heart", "Red tug", "Lonsdale Mountain View", "Northern Deep Sea Tug",
             '"Old One"', "Centenary Edition", '30" x 21"', "None", "BELL-AA", "AA011", "AA002", "Taupe Body Shape")
TYPOS = [("Line E ngraving", "Line engraving"), ("Arcylic", "Acrylic"), ("Aquantint", "Aquatint"), ("Montoype", "Monotype"),
         ("Prepratory", "Preparatory"), ("expoxy", "epoxy"), ("biege", "beige"), ("Conte' ", "Conte "), ("Mezzo Tint", "mezzotint"),
         ("Watercolor", "Watercolour"), ("watercolor", "watercolour"), ("c-print", "C-print")]


def sentence_case(medium):
    if not medium or any(u in medium for u in UNTOUCHED):
        return medium
    for old, new in TYPOS:
        medium = medium.replace(old, new)

    def word(m):
        w = m.group(0)
        if w in KEEP or (len(w) > 1 and w.isupper()) or any(c.isdigit() for c in w) or len(w) == 1:
            return w
        return w.lower()
    out = re.sub(r"[A-Za-zÀ-ÿ&0-9']+", word, medium)
    return out[0].upper() + out[1:]


def step_collection():
    out = []
    for handle, e in entries("artwork").items():
        v, change = e["values"], {}
        want = dict(RECORDS.get(handle, {}))
        year = want.get("year", v.get("year"))
        want["year"] = YEARS.get(year, year)
        edition = want.get("edition", v.get("edition"))
        want["edition"] = EDITIONS.get(edition, edition)
        want["medium"] = sentence_case(want.get("medium", v.get("medium")))
        for key, value in want.items():
            if value != v.get(key):
                change[key] = value
        if change:
            out.append((f"artwork {handle}: {', '.join(change)}", "entry",
                        {"id": e["id"], "metaobject": {"fields": [{"key": k, "value": x} for k, x in change.items()]}},
                        {k: v.get(k) for k in change}))
    return out


def step_alt():
    """24: a full stop after the artwork descriptions that are sentences ("Artist, Title, year. A tall ...").
    The label-only ones ("Artist, Title, year") stay as they are."""
    ids = []
    for e in entries("artwork").values():
        ids += json.loads(e["values"].get("images") or "[]")
    now = {}
    for i in range(0, len(ids), 250):
        for n in read("query($ids: [ID!]!) { nodes(ids: $ids) { ... on MediaImage { id alt } } }", {"ids": ids[i:i + 250]})["nodes"]:
            if n:
                now[n["id"]] = n["alt"]
    todo = {i: a for i, a in now.items() if a and ". " in a and not a.rstrip().endswith((".", "?", "!"))}
    keys = list(todo)
    return [(f"alt text: a full stop on {len(keys[i:i + 25])} artwork images", "files",
             {"files": [{"id": k, "alt": todo[k].rstrip() + "."} for k in keys[i:i + 25]]}, {k: todo[k] for k in keys[i:i + 25]})
            for i in range(0, len(keys), 25)]


# ---------------------------------------------------------------------------
# tiles (48): Turtle Clan Searchers's eight parts are one work; the exhibition keeps the first.

def step_tiles():
    art = {e["id"]: h for h, e in entries("artwork").items()}
    e = entries("exhibition")["from-the-ground"]
    now = json.loads(e["values"]["collection_works"])
    drop = {f"vick-c001-{n}" for n in range(2, 9)}
    new = [i for i in now if art.get(i) not in drop]
    if new == now:
        return []
    return [("exhibition from-the-ground collection_works: Turtle Clan Searchers as one tile", "entry",
             {"id": e["id"], "metaobject": {"fields": [{"key": "collection_works", "value": json.dumps(new, separators=(",", ":"))}]}},
             {"collection_works": e["values"]["collection_works"]})]


# ---------------------------------------------------------------------------
# prints (74, 75)

RUSSNA = "russna-kaur-what-remains-after-bloom-2026"
RUSSNA_MEDIUM = "Eleven-colour multi-plate photopolymer with chine collé and drawing"
MEDIUMS = {  # 75: sentence case, chine collé in lower case as a technique, "Lithograph" as on the other prints
    "archival pigment print": "Archival pigment print", "13-colour serigraph": "13-colour serigraph", "archival inkjet print": "Archival inkjet print",
    "Archival Inkjet print": "Archival inkjet print", "lithograph": "Lithograph", "four-colour drypoint etching": "Four-colour drypoint etching",
    "six-colour lithograph": "Six-colour lithograph", "five-colour serigraph": "Five-colour serigraph", "16-colour serigraph": "16-colour serigraph",
    "hand-printed embossed woodblock relief, serigraph, suspended copper pigment": "Hand-printed embossed woodblock relief, serigraph, suspended copper pigment",
    "Serigraph, woodcut, Chine Collé": "Serigraph, woodcut, chine collé", "Lithography, Chine Collé": "Lithograph, chine collé",
}


def size_form(value):
    """75: one form of size: straight inch marks, "(full bleed)" in brackets, no centimetres beside inches."""
    if not value:
        return value
    value = value.replace("”", '"').replace("“", '"')
    value = value.replace(' (74.9 x 86.4 cm) full bleed', ' (full bleed)')
    return value


def credit_form(html):
    """75: one form of photo credit, as the rest of the site writes it: "Photo by Rachel Topham"."""
    html = re.sub(r"Photo credit:\s*", "Photo by ", html)
    return html.replace(">Rachel Topham Photography<", ">Rachel Topham<")


def russna_technique(full):
    """The medium's detail, word for word, as a line after the paper line, so the shorter label loses nothing."""
    rest = full.split(". ", 1)[1] if ". " in full else ""
    return f"<p>{rest}</p>" if rest else ""


def step_prints():
    ids = [p["id"] for p in json.loads((HERE / "snapshots" / "prints-2026-09-25.json").read_text())]
    now = read("query($ids: [ID!]!) { nodes(ids: $ids) { ... on Product { id handle title status updatedAt descriptionHtml "
               "medium: metafield(namespace: \"custom\", key: \"medium\") { value } edition: metafield(namespace: \"custom\", key: \"edition\") { value } "
               "dimensions: metafield(namespace: \"custom\", key: \"dimensions\") { value } } } }", {"ids": ids})["nodes"]
    with tempfile.TemporaryDirectory() as folder:
        tmp = pathlib.Path(folder) / "products.json"
        tmp.write_text(json.dumps(now, ensure_ascii=False))
        done = subprocess.run([sys.executable, str(HERE / "release.py"), "products", str(tmp), "--vars"], capture_output=True, text=True, check=True)
    cleaned = {m["id"]: m["descriptionHtml"] for m in json.loads(done.stdout).values()}
    out = []
    for p in now:
        medium = (p.get("medium") or {}).get("value")
        desc = cleaned[p["id"]]
        if p["handle"] == RUSSNA and "Beva" not in desc and medium and ". " in medium:
            desc = desc.replace("Unframed.</p>", "Unframed.</p>" + russna_technique(medium), 1) if "Unframed.</p>" in desc else desc + russna_technique(medium)
        desc = credit_form(desc)
        product = {"id": p["id"]}
        before = {}
        if desc != p["descriptionHtml"]:
            product["descriptionHtml"], before["descriptionHtml"] = desc, p["descriptionHtml"]
        fields = []
        want_medium = RUSSNA_MEDIUM if p["handle"] == RUSSNA else MEDIUMS.get(medium, medium)
        if medium and want_medium and want_medium[0].islower():
            want_medium = want_medium[0].upper() + want_medium[1:]
        for key, now_value, want in (("medium", medium, want_medium),
                                     ("edition", (p.get("edition") or {}).get("value"), "AP (ed. of 100)" if p["handle"] == "gordon-smith-pender-harbour-2006" else None),
                                     ("dimensions", (p.get("dimensions") or {}).get("value"), size_form((p.get("dimensions") or {}).get("value")))):
            if want and want != now_value:
                fields.append({"namespace": "custom", "key": key, "type": "single_line_text_field", "value": want})
                before[key] = now_value
        if fields:
            product["metafields"] = fields
        if len(product) > 1:
            out.append((f"product {p['handle']}: {', '.join(before)}", "product", {"product": product}, before))
    return out


# ---------------------------------------------------------------------------
# frame (76)

FRAME = "russna-kaur-frame"
FRAME_FROM = "gathie-falk-frame"  # its photo is the generic frame photo the frames share


def step_frame():
    q = ("query($q: String!) { products(first: 1, query: $q) { nodes { id handle media(first: 10) { nodes { id ... on MediaImage { image { url } } } } } } }")
    frame = read(q, {"q": f"handle:{FRAME}"})["products"]["nodes"][0]
    source = read(q, {"q": f"handle:{FRAME_FROM}"})["products"]["nodes"][0]
    stock = [m for m in frame["media"]["nodes"] if "360_F_" in (m.get("image") or {}).get("url", "")]
    if not stock:
        return []
    generic = source["media"]["nodes"][0]
    return [(f"product {FRAME}: the stock-preview photo off, the shared frame photo on", "files",
             {"files": [{"id": stock[0]["id"], "referencesToRemove": [frame["id"]]},
                        {"id": generic["id"], "referencesToAdd": [frame["id"]]}]},
             {"media": [m["id"] for m in frame["media"]["nodes"]], "removed": stock[0]["id"], "added": generic["id"]})]


STEPS = {"names": step_names, "text": step_text, "lessons": step_lessons, "collection": step_collection, "alt": step_alt,
         "tiles": step_tiles, "prints": step_prints, "frame": step_frame}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in STEPS:
        sys.exit(__doc__)
    step, go = sys.argv[1], "--go" in sys.argv[2:]
    todo = STEPS[step]()
    if not go:
        for name, kind, variables, before in todo:
            print(f"would run {kind}: {name}")
            if "--full" in sys.argv[2:]:
                print("   before:", json.dumps(before, ensure_ascii=False)[:2500])
                print("   send:  ", json.dumps(variables, ensure_ascii=False)[:2500])
        print(f"{len(todo)} call(s) listed; nothing changed")
        sys.exit(0)
    if todo:
        snap = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {
            "taken": DAY, "what": "What each step of followup_answers.py was about to change, read from the store just before it ran. "
                                  "To undo a call, send its `before` values back with the same kind of call."}
        taken = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        snap.setdefault(step, []).extend({"call": name, "kind": kind, "id": variables.get("id") or variables.get("product", {}).get("id"),
                                          "read": taken, "before": before} for name, kind, variables, before in todo)
        SNAPSHOT.write_text(json.dumps(snap, ensure_ascii=False, indent=1) + "\n")
    CREATED.mkdir(parents=True, exist_ok=True)
    path = CREATED / f"{step}.json"
    log = json.loads(path.read_text()) if path.exists() else []
    for n, (name, kind, variables, before) in enumerate(todo):
        data, err = execute(Q[kind], variables, True)
        errors = user_errors(data) if not err else [{"message": err}]
        short = json.dumps(variables, ensure_ascii=False)
        log.append({"call": name, "kind": kind, "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                    "variables": variables if len(short) < 4000 else {"id": variables.get("id"), "sent": f"({len(short)} characters; see the snapshot)"},
                    "answer": data, "errors": errors})
        path.write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n")
        if errors:
            sys.exit(f"STOPPED at {name}: {errors}\n{n} call(s) made before it; see {path}")
        print(f"done {kind}: {name}")
    print(f"{len(todo)} call(s) made")
