#!/usr/bin/env python3
"""The Permanent Collection, cleaned for the store (proposals/permanent-collection.md, P-27).

Reads the catalogue export that inventory.py writes, and the store's current exhibitions and
editions (store.json, below), and writes:

- <out>/artists.json, works.json, groups.json, images.json, documents.json: what import.py and
  images.py load into the store. Not committed; run this again before each import.
- proposals/store-writes/collection/sheets/*.csv: the review sheets for the gallery (committed).

  python3 proposals/store-writes/collection/clean.py <export folder> <out folder>

<export folder>/store.json holds the store's exhibitions and editions:
  {"exhibitions": [{"handle", "title", "artists": [...], "collection_artists": [...]}],
   "products": [{"handle", "artist", "work", "year"}]}

Nothing here writes to the store. The rules for names, titles and themes are in the plan's
"Cleaning the data"; the choices below follow the gallery-questions defaults (§5) until the
gallery corrects the sheets.
"""
import collections
import csv
import html
import json
import pathlib
import re
import sys
import unicodedata

HERE = pathlib.Path(__file__).parent
SHEETS = HERE / "sheets"
REPO = HERE.parents[2]

LOANS_SET = 1619  # "Things On Loan to AFK": imported like the rest (P-28); noted in problems.csv
CREDIT = "Collection of Artists for Kids and the Gordon Smith Gallery"

# Catalogue item sets that become groupings (kind, handle, name). Categories and themes come from
# each work's own fields instead, so a work always shows in the groupings its label names.
SET_GROUPS = {
    1547: ("Grouping", "indigenous-artists", "Indigenous artists"),
    2215: ("Grouping", "published-editions", "Artists for Kids Published Editions"),
    4097: ("Grouping", "teaching-collection", "Teaching Collection"),
    4571: ("Grouping", "portfolio-collective-2021", "The Portfolio Collective's 2021 Artist for Artist Edition series"),
}
# The catalogue's curated theme sets: their works carry the theme, as if the Subject said so.
THEME_SETS = {3100: "People", 3101: "Architecture", 3102: "Creatures", 3103: "Action",
              3106: "Social change", 3107: "Storytelling", 3108: "Ecology", 3109: "Invention"}
# Catalogue exhibition sets and the site's exhibition entries.
EXHIBITION_SETS = {1303: "the-art-of-conversation", 1319: "playhouse", 4517: "from-the-ground"}
EXHIBITION_PAGES = {"works-in-the-art-of-conversation": "the-art-of-conversation", "worksinplayhouse": "playhouse",
                    "works-in-from-the-ground": "from-the-ground"}
MIN_THEME_GROUP = 5
MAX_DOCUMENT = 20_000_000  # Shopify's limit for a file
# The Permanent Collection page's featured row (the grouping "featured"): the three founding patrons,
# then a painting, a sculpture and a print from across the collection. The gallery can change them in
# the admin (Content, Metaobjects, Collection grouping, Featured works).
FEATURED = ["reid003", "smit001", "shad001", "hugh001", "davi001", "keno004"]  # a theme with fewer works stays a word on the label, without a page

CATEGORIES = {  # Format, lower case -> category
    "print": "Print", "printmaking": "Print", "painting": "Painting", "drawing": "Drawing",
    "photograph": "Photograph", "photography": "Photograph", "colour photograph (c-print)": "Photograph",
    "sculpture": "Sculpture", "ceramics": "Ceramic", "ceramic": "Ceramic", "textile": "Textile",
    "textiles": "Textile", "book": "Book",
}
CATEGORY_GROUPS = {  # category -> (handle, name)
    "Painting": ("paintings", "Paintings"), "Print": ("prints", "Prints"), "Drawing": ("drawings", "Drawings"),
    "Photograph": ("photography", "Photography"), "Sculpture": ("sculptures", "Sculptures"),
    "Ceramic": ("ceramics", "Ceramics"), "Textile": ("textiles", "Textiles"), "Book": ("books", "Books"),
}
THEMES = {  # Subject term, lower case -> theme; None drops it (not a theme)
    "abstract": "Abstract", "abstact": "Abstract", "storytelling": "Storytelling", "story": "Storytelling",
    "creatures": "Creatures", "creature": "Creatures", "landscape": "Landscape", "landscapes": "Landscape",
    "lanscape": "Landscape", "drawing of a landscape": "Landscape", "ecology": "Ecology", "nature": "Ecology",
    "people": "People", "plants": "Plants", "architecture": "Architecture", "still-life": "Still life",
    "still life": "Still life", "text": "Text", "words": "Text", "portrait": "Portrait", "portait": "Portrait",
    "portraits": "Portrait", "social change": "Social change", "invention": "Invention", "action": "Action",
    "place": "Place",
    # About the artist, and carried by the Indigenous artists grouping instead.
    "indigenous": None,
    # Not themes: a format, the credit line and a visual description typed into Subject.
    "photography": None, "collection of artists for kids and the gordon smith gallery": None,
    "photo of an orange sunset with palm trees": None,
}

# How the catalogue's Creator spellings map to artists. A spelling not listed here is cleaned by
# rule: the "(DOB: …)" and notes after "*" come off, "First (Nick) Last" becomes "Nick Last".
# Values: display names; several for a work by more than one artist.
ALIASES = {
    "Alexander Young (A.Y.) Jackson": ["A.Y. Jackson"],
    "Alistair Macready Bell": ["Alistair Bell"],
    "Angela Grossman": ["Angela Grossmann"],
    "Ann Meredith Barry": ["Anne Meredith Barry"],
    "Attila Richard Lukacs": ["Atilla Lukacs"],
    "Attlia Richard Lukacs": ["Atilla Lukacs"],
    "Barbara Zeigler and Joan Smith": ["Barbara Zeigler", "Joan Smith"],
    "Benjamin Kerry (Beau) Dick": ["Beau Dick"],
    "Bertram Charles (BC) Binning": ["B.C. Binning"],
    "Betty Roodish Goodwin": ["Betty Goodwin"],
    "Charles Noel Van Sandwyk": ["Charles Van Sandwyk"],
    "Damian George (Stalaston)": ["Damian George"],
    "David LLoyd Blackwood": ["David Blackwood"],
    "David Lloyd Blackwood": ["David Blackwood"],
    "Douglas Campbell Coupland": ["Douglas Coupland"],
    "E.J. (Edward John) Hughes": ["E.J. Hughes"],
    "Edward John (E.J.) Hughes": ["E.J. Hughes"],
    "Edward Hardy (Ted) Harrison": ["Ted Harrison"],
    "Gordon Appelbe Smith": ["Gordon Smith"],
    "Graham Gilllmore": ["Graham Gillmore"],
    "Graham Gillmore, Angela Grossman, Attila Richard Lukacs, Derek Root, Vikky Alexander, Rebecca Belmore, Dana Claxton":
        ["Graham Gillmore", "Angela Grossmann", "Atilla Lukacs", "Derek Root", "Vikky Alexander", "Rebecca Belmore", "Dana Claxton"],
    "Ian Hugh Wallace": ["Ian Wallace"],
    "Irene F. Whittome": ["Irene F. Whittome"],
    "Jack Leonard Shadbolt": ["Jack Shadbolt"],
    "Jean Albert McEwen": ["Jean McEwan"],
    "Jim Paull [James Edwin Gerald Paull]": ["Jim Paull"],
    "Karin Bubas": ["Karin Bubaš"],
    "Lauren Brevner and James Harry (Studio Lauren James)": ["Lauren Brevner", "James Harry"],
    "Norman Anthony (Toni) Onley": ["Toni Onley"],
    "Pat & Rosemarie Keough": ["Pat and Rosemarie Keough"],
    "Reid, Leslie (female)": ["Leslie Reid"],
    "Robert Davidson (Guud san glans)": ["Robert Davidson"],
    "Robert Davidson (Haida Name: Guud san glans)": ["Robert Davidson"],
    "Ross Ellsworth Penhall": ["Ross Penhall"],
    "Setsuko Nane Piroche": ["Setsuko Piroche"],
    "Tony Romano and Tyler Brett": ["T&T Collective"],
    "Unknown [Inuit Origins]": ["Unknown Inuit artist"],
    "Various Artists - West Baffin Eskimo Coop. LTD [Portfolio of Posters]": ["West Baffin Eskimo Co-operative"],
    "West Baffin Eskimo Coop. LTD portfolio of posters": ["West Baffin Eskimo Co-operative"],
    "William (Bill) Ronald Reid": ["Bill Reid"],
    "Xwalacktun (Rick Harry)": ["Xwalacktun"],
    "Yaahl Sgwansung [William (Bill) Ronald Reid]": ["Bill Reid"],
    "Yaahl Sgwansung [William Ronald (Bill) Reid]": ["Bill Reid"],
}
# Names that aren't "First Last": the sort name, and other names the artist is known by.
ARTISTS = {
    "A.Y. Jackson": {"full": "Alexander Young Jackson"},
    "Alistair Bell": {"full": "Alistair Macready Bell"},
    "Atilla Lukacs": {"full": "Attila Richard Lukacs"},
    "B.C. Binning": {"full": "Bertram Charles Binning"},
    "Beau Dick": {"full": "Benjamin Kerry Dick"},
    "Betty Goodwin": {"full": "Betty Roodish Goodwin"},
    "Bill Reid": {"full": "William Ronald Reid", "other": "Yaahl Sgwansung"},
    "Charles Van Sandwyk": {"full": "Charles Noel Van Sandwyk", "sort": "Van Sandwyk, Charles"},
    "Damian George": {"other": "Stalaston"},
    "David Blackwood": {"full": "David Lloyd Blackwood"},
    "Douglas Coupland": {"full": "Douglas Campbell Coupland"},
    "E.J. Hughes": {"full": "Edward John Hughes"},
    "George Hunt Jr.": {"sort": "Hunt, George, Jr."},
    "Gordon Smith": {"full": "Gordon Appelbe Smith"},
    "Gu Xiong": {"sort": "Gu Xiong"},
    "Ian Wallace": {"full": "Ian Hugh Wallace"},
    "Jack Shadbolt": {"full": "Jack Leonard Shadbolt"},
    "Jane Ash Poitras": {"sort": "Poitras, Jane Ash"},
    "Jean McEwan": {"full": "Jean Albert McEwen"},
    "Jim Paull": {"full": "James Edwin Gerald Paull"},
    "Kabubuwa Tunnillie": {"other": "Qavaroak"},
    "Newgaleak Qimirpik": {"other": "Nuyaliaq"},
    "Pat and Rosemarie Keough": {"sort": "Keough, Pat and Rosemarie"},
    "Robert Davidson": {"other": "Guud san glans"},
    "Ross Penhall": {"full": "Ross Ellsworth Penhall"},
    "Roy Henry Vickers": {"sort": "Vickers, Roy Henry"},
    "Setsuko Piroche": {"full": "Setsuko Nane Piroche"},
    "T&T Collective": {"full": "Tyler Brett and Tony Romano", "sort": "T&T Collective"},
    "Ted Harrison": {"full": "Edward Hardy Harrison"},
    "Toni Onley": {"full": "Norman Anthony Onley"},
    "Unknown Inuit artist": {"sort": "Unknown Inuit artist"},
    "Vancouver School Collective": {"full": "Douglas Coupland, Angela Grossmann, Graham Gillmore and Atilla Lukacs",
                                    "sort": "Vancouver School Collective"},
    "West Baffin Eskimo Co-operative": {"full": "West Baffin Eskimo Coop. Ltd.", "sort": "West Baffin Eskimo Co-operative"},
    "Xwalacktun": {"other": "Rick Harry", "sort": "Xwalacktun"},
    "Yung Wing Chow": {"sort": "Chow, Yung Wing"},
}
# Exhibition entries name some artists differently. Exhibition spelling -> display name.
EXHIBITION_NAMES = {
    "James Nexw'Kalus-Xwalacktun Harry": "James Harry",
    "T&T Collective (Tyler Brett and Tony Romano)": "T&T Collective",
    "Leonhard Epp": "Leonard Epp",
}

EDITION = re.compile(
    r"\s*[\(\[]\s*((?:\d+\s*/\s*\d+)|(?:A\.?\s*/?\s*P\.?|PP|P/P|TP|T/P|HC|H/C|BAT|E/A),?(?:[\s\-]*[A-Z0-9]+(?:\s*/\s*[A-Z0-9]+)?)?)\s*[\)\]]\s*$",
    re.I)
BARE_EDITION = re.compile(r"\s(\d+\s*/\s*\d+)\s*$")
DOB = re.compile(r"\s*[\(\[]\s*(?:DOB:?)?\s*(\d{4}\s*(?:-\s*(?:\d{4}|Present))?)?\s*[\)\]]\s*$", re.I)
# A work's Year shows on the site as written. These forms need no question: a year (1965), a range
# (1991-96, 1994/1995, 2000 to 2001), no date (ND, n.d.) and circa (circa 1965, circa 1950s,
# circa 20th century). Any other goes on problems.csv for the gallery to confirm or correct
# (gallery questions 5.14). Nothing here changes the value.
YEAR_OK = re.compile(
    r"\d{4}(?:\s*(?:-|/|to)\s*\d{2,4})?|n\.?\s?d\.?|no date|undated"
    r"|circa\s+(?:\d{4}s?(?:\s*(?:-|to)\s*\d{4}s?)?|\d{1,2}(?:st|nd|rd|th)\s+century)", re.I)
MONTH = r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+"
YEAR_REASONS = [  # (pattern, reason): the first that matches
    (r"^n\.?\s?d\.?\s*\[", "is no date with an estimate in brackets"),
    (r"^n/a$", "says not applicable rather than no date"),
    (r"\d{3}-$", "is an estimate with the last digit missing"),
    (r"\d{2}c$", "abbreviates the century"),
    (r"century", "gives only the century"),
    (r"\(signed and dated\)", "has a note after the date"),
    (MONTH + r"\d{1,2}(?:st|nd|rd|th)?,", "is a full date"),
    (MONTH + r"\d{4}", "gives the month too"),
    (r"^\d{4}\s+[a-z]", "has words after it that look like a note"),
    (r"^\D*$", "isn't a date"),
]


def values(item, key):
    return [(x.get("@value") or x.get("o:label") or x.get("@id") or "").strip() for x in item.get(key, [])]


def first(item, key):
    """The first value, on one line: the store's single-line fields refuse line breaks."""
    v = values(item, key)
    return re.sub(r"\s+", " ", v[0]).strip() if v else ""


def item_sets(item):
    return {x["o:id"] for x in item.get("o:item_set", [])}


def strip_note(value):
    """A cataloguer's note after "*" ("*it was replaced with 2/35...") -> (value without it, note)."""
    m = re.search(r"(^|\s)\*", value)
    if not m:
        return value, ""
    return value[:m.start()].strip(), value[m.start():].strip().lstrip("*").strip()


def ascii_fold(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def handleize(s):
    s = ascii_fold(s).lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def split_creator(raw):
    """A Creator value -> (spelling without dates or notes, dates as recorded, note)."""
    raw = raw.replace("\r", "")
    name, _, note = raw.partition("\n*")
    name = re.sub(r"\s+", " ", name).strip()
    dates = ""
    m = DOB.search(name)
    if m and ("DOB" in m.group(0).upper() or re.fullmatch(r"\s*\(\d{4}\)\s*", m.group(0))):
        dates = (m.group(1) or "").strip()
        name = name[:m.start()].strip()
    return name, dates, note.strip()


def display_names(spelling, known):
    if spelling in ALIASES:
        return ALIASES[spelling]
    if spelling.startswith("Vancouver School Collective"):
        return ["Vancouver School Collective"]
    m = re.fullmatch(r"(.+?) \(([^)]+)\)( .+)?", spelling)
    if m and m.group(3):  # "First (Nick) Middle Last" -> "Nick Last"
        return [f"{m.group(2)} {m.group(3).split()[-1]}"]
    if spelling in known:
        return [known[spelling]]
    return [spelling]


def life_dates(recorded):
    """All the dates recorded for one artist -> (dates for the site, conflict?)."""
    found = {re.sub(r"\s+", "", d).replace("-Present", "").replace("-present", "") for d in recorded if d}
    if not found:
        return "", False
    if len(found) > 1:
        return "", True
    d = found.pop()
    if "-" in d:
        a, b = d.split("-")
        return f"{a} to {b}", False
    return f"born {d}", False


def sort_name(name):
    if name in ARTISTS and "sort" in ARTISTS[name]:
        return ARTISTS[name]["sort"]
    parts = name.split()
    if len(parts) == 1:
        return name
    return f"{parts[-1]}, {' '.join(parts[:-1])}"


def edition_and_title(title, references):
    edition = references.strip()
    clean = title
    m = EDITION.search(title) or BARE_EDITION.search(title)
    if m:
        clean = title[:m.start()].rstrip(" ,;")
        if not edition:
            edition = re.sub(r"\s*/\s*", "/", m.group(1).strip())
    return clean.strip(), edition


def year_key(year):
    m = re.search(r"\d{4}", year or "")
    return int(m.group(0)) if m else 9999


def title_key(title):
    return re.sub(r"[^a-z0-9]+", " ", ascii_fold(title).lower()).strip()


def year_problem(year):
    """Why the gallery should check a work's Year, or "" when it's empty or a form in YEAR_OK."""
    if not year or YEAR_OK.fullmatch(year):
        return ""
    why = next((w for p, w in YEAR_REASONS if re.search(p, year, re.I)), "isn't a year, a range, no date or circa")
    return f"Year {why}: {year}"


def main(export, out):
    items = json.loads((export / "items.json").read_text())
    sets = {s["o:id"]: first(s, "dcterms:title") for s in json.loads((export / "item_sets.json").read_text())}
    media = {m["o:id"]: m for m in json.loads((export / "media.json").read_text())}
    store = json.loads((export / "store.json").read_text())
    site_links = site_artist_links()

    doc_sets = {sid for sid, t in sets.items() if "Text Resource" in t or t in ("Pat and Rosemarie Keough", "Christopher & Mary Pratt")}
    works_raw = [i for i in items if not (item_sets(i) & doc_sets)]
    docs_raw = [i for i in items if item_sets(i) & doc_sets]
    loans = [i for i in items if LOANS_SET in item_sets(i) and not (item_sets(i) & doc_sets)]
    # The catalogue's "Works in …" pages attach works by hand, as well as the exhibition sets.
    exhibition_items = collections.defaultdict(set)
    pages_path = export / "site_pages.json"
    for page in (json.loads(pages_path.read_text()) if pages_path.exists() else []):
        handle = EXHIBITION_PAGES.get(page.get("o:slug"))
        for block in page.get("o:block", []) if handle else []:
            for att in block.get("o:attachment") or []:
                if (att.get("o:item") or {}).get("o:id"):
                    exhibition_items[att["o:item"]["o:id"]].add(handle)

    # Names the site already uses, by their cleaned catalogue spelling: the Artists page's links,
    # the editions' labels and the exhibitions' artists.
    known = {}
    site_names = set(site_links) | {p["artist"] for p in store["products"] if p.get("artist")}
    for e in store["exhibitions"]:
        site_names |= set(e.get("artists") or []) | set(e.get("collection_artists") or [])
    by_tokens = collections.defaultdict(set)
    for n in site_names:
        t = handleize(n).split("-")
        if len(t) >= 2:
            by_tokens[(t[0], t[-1])].add(n)

    artists = {}  # display name -> record

    def artist(name):
        if name not in artists:
            info = ARTISTS.get(name, {})
            artists[name] = {"name": name, "handle": handleize(name), "sort_name": sort_name(name),
                             "full_name": info.get("full", ""), "other_names": info.get("other", ""),
                             "spellings": set(), "dates_recorded": [], "notes": set(), "works": [],
                             "exhibitions": set(), "documents": [], "website": site_links.get(name, ""),
                             "editions": []}
        return artists[name]

    works, problems, titles = [], [], []
    seen_handles = collections.Counter()
    for i in sorted(works_raw, key=lambda x: x["o:id"]):
        accession = first(i, "dcterms:identifier")
        if LOANS_SET in item_sets(i):
            # Two loans carry it in the number itself: "BOBA005 On Loan".
            accession = re.sub(r"\s*on loan\s*$", "", accession, flags=re.I)
            problems.append((accession, "In the catalogue's \"Things On Loan to AFK\"; imported like the rest (P-28). Check its credit line", i["o:id"]))
        creators = values(i, "dcterms:creator")
        names = []
        for raw in creators:
            spelling, dates, note = split_creator(raw)
            if spelling not in ALIASES:
                t = handleize(spelling).split("-")
                match = by_tokens.get((t[0], t[-1])) if len(t) >= 2 else None
                if match and len(match) == 1:
                    known[spelling] = next(iter(match))
            shown = display_names(spelling, known)
            for n in shown:
                a = artist(n)
                a["spellings"].add(re.sub(r"\s+", " ", raw.split("\n*")[0]).strip())
                if len(shown) == 1:
                    a["dates_recorded"].append(dates)
                    if spelling != n and not a["full_name"] and len(spelling.split()) > len(n.split()) and "(" not in spelling:
                        a["full_name"] = spelling
                if note:
                    a["notes"].add(note)
                names.append(a["handle"])
        title_raw = first(i, "dcterms:title")
        title_plain, note_t = strip_note(title_raw)
        refs, note_r = strip_note(first(i, "dcterms:references"))
        desc, note_d = strip_note(first(i, "dcterms:description"))
        for note in (note_t, note_r, note_d):
            if note:
                problems.append((accession, f"Catalogue note left off the site: {note}", i["o:id"]))
        title, edition = edition_and_title(title_plain, refs)
        if not title:
            title = "Untitled"
            problems.append((accession, "No title in the catalogue; shown as Untitled", i["o:id"]))
        if title != title_raw:
            titles.append((accession, title_raw, title, edition))
        fmt = first(i, "dcterms:format").lower()
        category = CATEGORIES.get(fmt, "")
        if not category:
            problems.append((accession, f"No category (Format: {fmt or 'empty'})", i["o:id"]))
        year = first(i, "dcterms:date")
        if why := year_problem(year):
            problems.append((accession, why, i["o:id"]))
        themes = []
        for s in values(i, "dcterms:subject"):
            for term in re.split(r"[,;]", s):
                term = term.strip().lower()
                if term:
                    t = THEMES.get(term, term.capitalize()) if term in THEMES else term.capitalize()
                    if t and t not in themes:
                        themes.append(t)
        for sid, t in THEME_SETS.items():
            if sid in item_sets(i) and t not in themes:
                themes.append(t)
        images = [m["o:id"] for m in i.get("o:media", []) if media.get(m["o:id"], {}).get("o:media_type", "").startswith("image/")]
        if not images:
            problems.append((accession, "No image in the catalogue", i["o:id"]))
        handle = handleize(accession) or f"item-{i['o:id']}"
        seen_handles[handle] += 1
        if seen_handles[handle] > 1:
            problems.append((accession, f"Same address as another work's number; this one is /pages/collection/{handle}-{seen_handles[handle]}", i["o:id"]))
            handle = f"{handle}-{seen_handles[handle]}"
        rights = re.sub(r"\s+", " ", first(i, "dcterms:rights")).strip()
        work = {
            "handle": handle, "item_id": i["o:id"], "accession": accession, "title": title,
            "artists": list(dict.fromkeys(names)), "year": year, "category": category,
            "medium": re.sub(r"\s+", " ", first(i, "dcterms:medium")), "dimensions": re.sub(r"\s+", " ", first(i, "dcterms:spatial")),
            "edition": edition, "credit_line": rights, "images": images, "themes": themes,
            "description": desc,
            "shown_in": sorted({h for sid, h in EXHIBITION_SETS.items() if sid in item_sets(i)} | exhibition_items[i["o:id"]]),
            "sets": sorted(item_sets(i)), "in_the_shop": "",
        }
        works.append(work)
        for h in work["artists"]:
            a = next(x for x in artists.values() if x["handle"] == h)
            a["works"].append(handle)
            a["exhibitions"] |= set(work["shown_in"])

    # Editions: the Shop's artists get entries too, and a work that is the collection's copy of an
    # edition links to it (same artist, same title).
    by_handle = {a["handle"]: a for a in artists.values()}
    for p in store["products"]:
        if not p.get("artist"):
            continue
        names = [n.strip() for n in re.split(r"\s*&\s*|\s+and\s+", p["artist"])] if p["artist"] not in artists else [p["artist"]]
        handles = []
        for n in names:
            a = artist(n)
            a["editions"].append(p["handle"])
            handles.append(a["handle"])
        p["artist_handles"] = handles
        by_handle = {a["handle"]: a for a in artists.values()}
        for w in works:
            if set(handles) & set(w["artists"]) and title_key(w["title"]) == title_key(p.get("work") or ""):
                w["in_the_shop"] = p["handle"]

    # Exhibitions name their artists as text: link the ones that have entries.
    names_index = {}
    for a in artists.values():
        for n in {a["name"], a["full_name"], *a["spellings"]}:
            if n:
                names_index[title_key(n)] = a["handle"]
    for e in store["exhibitions"]:
        for n in (e.get("artists") or []) + (e.get("collection_artists") or []):
            h = names_index.get(title_key(EXHIBITION_NAMES.get(n, n)))
            if h:
                by_handle[h]["exhibitions"].add(e["handle"])

    # Documents: each Text Resources set belongs to one artist, named as the catalogue spells them.
    spelled = {}
    for a in artists.values():
        for n in {a["name"], a["full_name"], *a["spellings"]} - {""}:
            spelled[title_key(re.sub(r"\s*[\(\[]DOB.*$", "", n))] = a["handle"]
    documents = []
    for i in docs_raw:
        owner, set_name = None, ""
        for sid in item_sets(i) & doc_sets:
            n = re.sub(r"\s*\(?Text Resources?\)?\s*$", "", sets[sid]).strip()
            n = {"B.C Binning": "B.C. Binning", "E.J Hughes": "E.J. Hughes", "Angela Grossman": "Angela Grossmann",
                 "Graham Gilmore": "Graham Gillmore", "Christopher & Mary Pratt": "Christopher Pratt",
                 "Irene Whittome": "Irene F. Whittome", "Jean McEwen": "Jean McEwan",
                 "Kabubuwa (Qavaroak) Tunnillie": "Kabubuwa Tunnillie", "Newgaleak (Nuyaliaq) Qimirpik": "Newgaleak Qimirpik",
                 "All Artist": ""}.get(n, n)
            h = handleize(n) if n and handleize(n) in by_handle else spelled.get(title_key(n)) if n else None
            if h:
                owner, set_name = h, re.sub(r"\s*\(?Text Resources?\)?\s*$", "", sets[sid]).strip()
        for m in i.get("o:media", []):
            md = media.get(m["o:id"])
            if not md:
                continue
            documents.append({"media_id": md["o:id"], "item_id": i["o:id"], "artist": owner or "", "set_name": set_name,
                              "title": first(i, "dcterms:title") or md.get("o:source", ""), "type": md["o:media_type"],
                              "size": md.get("o:size") or 0, "url": md["o:original_url"]})

    # Which files a document shows as. Most catalogue items are a PDF plus a small image of its cover:
    # the PDF is the document, so it's the one link. Items that are only photographs link their
    # photographs. A PDF over Shopify's 20 MB limit isn't on the site (large-documents.csv), and its
    # cover doesn't stand in for it.
    by_item = collections.defaultdict(list)
    for d in documents:
        d["show"] = False
        by_item[d["item_id"]].append(d)
    large = []
    for item_docs in by_item.values():
        artist_handle = item_docs[0]["artist"]
        if not artist_handle:
            continue
        a = by_handle[artist_handle]
        # On the artist's own page the name and "(Text Resource)" only repeat: "Robert Davidson -
        # Press (Text Resource)" reads as "Press".
        t = re.sub(r"\s*\(?Text Resources?\)?\s*$", "", item_docs[0]["title"], flags=re.I).strip()
        names = {a["name"], a["full_name"], item_docs[0]["set_name"], *a["spellings"]} - {""}
        for n in sorted(names, key=len, reverse=True):
            t = re.sub(r"^" + re.escape(n) + r"(\s*[-:]\s*|\s+|$)", "", t, flags=re.I)
        t = t.strip(" -:")
        t = t[:1].upper() + t[1:] if t else "Document"
        for d in item_docs:
            d["title"] = t
        pdfs = [d for d in item_docs if d["type"] == "application/pdf"]
        chosen = pdfs or [d for d in item_docs if d["type"].startswith("image/")]
        for d in chosen:
            if d["size"] > MAX_DOCUMENT:
                large.append(d)
        chosen = [d for d in chosen if d["size"] <= MAX_DOCUMENT]
        for n, d in enumerate(chosen, 1):
            d["show"] = True
            d["title"] = t if len(chosen) == 1 else f"{t}, {n} of {len(chosen)}"
    for a in artists.values():
        # Two links with the same words would be ambiguous: number the repeats ("Press", "Press 2").
        seen = collections.Counter()
        for d in sorted((d for d in documents if d["show"] and d["artist"] == a["handle"]), key=lambda d: d["media_id"]):
            seen[d["title"]] += 1
            if seen[d["title"]] > 1:
                d["title"] = f"{d['title']} {seen[d['title']]}"
            a["documents"].append(d["media_id"])

    # Each exhibition's works from the collection, for its page (Shown in, turned around).
    exhibition_works = {h: [] for h in set(EXHIBITION_SETS.values()) | set(EXHIBITION_PAGES.values())}

    # Life dates, sorted work lists, and the artists' sheet rows.
    work_by_handle = {w["handle"]: w for w in works}
    for a in artists.values():
        a["life_dates"], a["dates_conflict"] = life_dates(a["dates_recorded"])
        born = re.match(r"(?:born )?(\d{4})", a["life_dates"])
        made = [year_key(work_by_handle[h]["year"]) for h in a["works"] if year_key(work_by_handle[h]["year"]) < 9999]
        if born and made and int(born.group(1)) + 10 > min(made):
            # A birth year after, or just before, the artist's earliest work is a typing error.
            a["life_dates"], a["dates_conflict"] = "", "Dates don't fit the works"
        a["works"].sort(key=lambda h: (year_key(work_by_handle[h]["year"]), title_key(work_by_handle[h]["title"])))
    dup = collections.Counter(a["handle"] for a in artists.values())
    assert not [h for h, n in dup.items() if n > 1], [h for h, n in dup.items() if n > 1]

    # Groupings.
    groups = {}

    def group(handle, name, kind, intro=""):
        return groups.setdefault(handle, {"handle": handle, "name": name, "kind": kind, "introduction": intro, "works": []})

    def artist_sort(w):
        a = by_handle[w["artists"][0]] if w["artists"] else None
        return (ascii_fold(a["sort_name"]).lower() if a else "~", year_key(w["year"]), title_key(w["title"]))

    theme_counts = collections.Counter(t for w in works for t in w["themes"])
    for w in sorted(works, key=artist_sort):
        for h in w["shown_in"]:
            exhibition_works[h].append(w["handle"])
        if w["category"]:
            h, n = CATEGORY_GROUPS[w["category"]]
            group(h, n, "Category")["works"].append(w["handle"])
        for t in w["themes"]:
            if theme_counts[t] >= MIN_THEME_GROUP:
                group(handleize(t), t, "Theme")["works"].append(w["handle"])
        for sid, (kind, h, n) in SET_GROUPS.items():
            if sid in w["sets"]:
                group(h, n, kind, PUBLISHED_EDITIONS_INTRO if h == "published-editions" else "")["works"].append(w["handle"])

    featured = group("featured", "Featured works", "Grouping")
    featured["works"] = [h for h in FEATURED if h in {w["handle"] for w in works}]

    images = []
    for w in works:
        names = " and ".join(by_handle[h]["name"] for h in w["artists"])
        alt = ", ".join(x for x in (names, w["title"], w["year"] if w["year"] and w["year"].upper() != "N.D." else "") if x)
        if w["description"]:
            d = w["description"].rstrip(".")
            alt += ". " + d[:1].upper() + d[1:] + "."
        for pos, mid in enumerate(w["images"]):
            md = media[mid]
            images.append({"media_id": mid, "work": w["handle"], "position": pos, "url": md["o:original_url"],
                           "type": md["o:media_type"], "size": md.get("o:size") or 0,
                           "alt": alt if len(w["images"]) == 1 else f"{alt} View {pos + 1} of {len(w['images'])}."})

    out.mkdir(parents=True, exist_ok=True)
    artist_rows = sorted(artists.values(), key=lambda a: ascii_fold(a["sort_name"]).lower())
    serial = [{k: (sorted(v) if isinstance(v, set) else v) for k, v in a.items() if k not in ("dates_recorded",)} for a in artist_rows]
    (out / "artists.json").write_text(json.dumps(serial, ensure_ascii=False, indent=1))
    (out / "works.json").write_text(json.dumps(works, ensure_ascii=False, indent=1))
    (out / "groups.json").write_text(json.dumps(list(groups.values()), ensure_ascii=False, indent=1))
    (out / "images.json").write_text(json.dumps(images, ensure_ascii=False, indent=1))
    (out / "documents.json").write_text(json.dumps(documents, ensure_ascii=False, indent=1))
    (out / "products.json").write_text(json.dumps(store["products"], ensure_ascii=False, indent=1))
    (out / "exhibitions.json").write_text(json.dumps(exhibition_works, ensure_ascii=False, indent=1))

    SHEETS.mkdir(exist_ok=True)
    write_csv("artists.csv", ["Name on the site", "Sort name", "Full name", "Other names", "Life dates",
                              "Dates as recorded", "Spellings in the catalogue", "Works", "Editions in the Shop",
                              "Exhibitions", "Website", "Notes in the catalogue", "Check"],
              [[a["name"], a["sort_name"], a["full_name"], a["other_names"], a["life_dates"],
                "; ".join(sorted({d for d in a["dates_recorded"] if d})), "; ".join(sorted(a["spellings"])),
                len(a["works"]), len(a["editions"]), "; ".join(sorted(a["exhibitions"])), a["website"],
                "; ".join(sorted(a["notes"])),
                a["dates_conflict"] if isinstance(a["dates_conflict"], str) else ("Dates disagree" if a["dates_conflict"] else "")]
               for a in artist_rows])
    write_csv("titles.csv", ["Accession number", "Title in the catalogue", "Title on the site", "Edition"], titles)
    write_csv("problems.csv", ["Accession number", "Problem", "Catalogue item"],
              problems)
    write_csv("large-documents.csv", ["Artist", "Document", "Size (MB)", "In the catalogue"],
              [[by_handle[d["artist"]]["name"], d["title"], f"{d['size'] / 1e6:.0f}",
                f"https://afkcatalogue.sd44.ca/s/TheCollection/item/{d['item_id']}"]
               for d in sorted(large, key=lambda d: (ascii_fold(by_handle[d["artist"]]["sort_name"]).lower(), d["title"]))])
    raw_terms = collections.Counter(t.strip().lower() for i in works_raw for s in values(i, "dcterms:subject") for t in re.split(r"[,;]", s) if t.strip())
    write_csv("themes.csv", ["Subject in the catalogue", "Theme on the site", "Works"],
              [[t, (THEMES[t] if t in THEMES else t.capitalize()) or "(not a theme)", n] for t, n in raw_terms.most_common()])
    write_csv("groupings.csv", ["Grouping", "Kind", "Address", "Works"],
              [[g["name"], g["kind"], f"/pages/browse/{g['handle']}", len(g["works"])] for g in groups.values()])

    print(f"works {len(works)} (loans {len(loans)}), artists {len(artists)}, groupings {len(groups)}, images {len(images)}, "
          f"documents shown {sum(1 for d in documents if d['show'])} of {len(documents)} files, {len(large)} PDFs over 20 MB, "
          f"exhibitions with works {sum(1 for v in exhibition_works.values() if v)}")
    print(f"titles changed {len(titles)}, problems {len(problems)}, dates left off {sum(1 for a in artists.values() if a['dates_conflict'])}")
    print("works in the Shop:", {w["handle"]: w["in_the_shop"] for w in works if w["in_the_shop"]})


PUBLISHED_EDITIONS_INTRO = (
    "In 1990, with the support of art educators and artist patrons Gordon Smith and Jack Shadbolt, Bill Reid worked "
    "with Artists for Kids to publish the first Artists for Kids Limited Edition Portfolio print, Xhuwaji / Haida "
    "Grizzly - marking the beginning of a extraordinary partnership between Canadian artists and Artists for Kids. "
    "Entering its 37th year, Artists for Kids continues to work with renowned Canadian artists and print studios "
    "across Canada to publish contemporary limited editions; its portfolio is now revered as one of the most "
    "significant limited edition collections in Canada. The Artists for Kids Limited Edition Portfolio program funds "
    "educational programs, artist residencies, art camps, scholarships, bursaries, and future acquisitions for the "
    "Artists for Kids and the Gordon Smith Gallery Permanent Collection.")


def site_artist_links():
    """Today's Artists page: name -> the link it gives (from the 2026-09-25 pages snapshot)."""
    pages = json.loads((REPO / "proposals/store-writes/snapshots/pages-2026-09-25.json").read_text())
    body = next(p["body"] for p in walk(pages) if p.get("handle") == "artists")
    links = {}
    for url, text in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', body, flags=re.S):
        name = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text))).strip()
        if name:
            links[name] = html.unescape(url)
    return links


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def write_csv(name, header, rows):
    with open(SHEETS / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))
