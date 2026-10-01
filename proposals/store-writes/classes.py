#!/usr/bin/env python3
"""Class and camp listings (P-68, proposals/class-listings.md): the Class entry's definition, and
After School Art's fall 2026 classes, typed from the district's After School Art page
(artistsforkids.sd44.ca/learn/after-school-art/, read 2026-10-01) word for word. Michael,
2026-10-01: "All seven decisions approved, merge #141 and build it" (decision 7: the agent types
in the first classes; the team takes over from the next term).

  python3 proposals/store-writes/classes.py <step> [--go]
  steps: definition, fall-2026

Each step reads the store first and sends only what is missing, so a second run lists nothing.
Without --go it prints each call and changes nothing. With --go it makes them one at a time
through the Shopify CLI, stops at the first error, and writes the store's answers to
created/classes-2026-10-01/<step>.json.

The live theme reads no Class entry until the release that carries the class list (DS-198), so
neither step changes what a visitor sees before then.
"""
import datetime
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from release_run import execute, user_errors  # noqa: E402

CREATED = HERE / "created" / "classes-2026-10-01"
AFTER_SCHOOL_ART = "gid://shopify/Page/165837373737"
STATUSES = ["Open", "Full", "Waitlist", "Opens soon", "Closed"]


def f(key, kind, name, description="", required=False, validations=None):
    d = {"key": key, "type": kind, "name": name, "required": required}
    if description:
        d["description"] = description
    if validations:
        d["validations"] = validations
    return d


DEFINITION = {
    "type": "class",
    "name": "Class",
    "description": "A class or camp from Artists for Kids. It lists on its programme page, with a link to its own registration page, and leaves the list after its last day.",
    "displayNameKey": "name",
    "access": {"storefront": "PUBLIC_READ"},
    "capabilities": {"publishable": {"enabled": True}},
    "fieldDefinitions": [
        f("name", "single_line_text_field", "Name", required=True),
        f("programme_page", "page_reference", "Programme page", "The page that lists it: After School Art, Spring & Summer Day Camps or Paradise Valley Summer Camps.", required=True),
        f("group", "single_line_text_field", "Listed under", "The heading it is listed under, the same for every class in the group. For example: Fall 2026 classes, or Pro D day camps."),
        f("description", "multi_line_text_field", "Description", "As on the district's page. A blank line starts a new paragraph."),
        f("when", "single_line_text_field", "When", "As the team writes it. For example: 8 Tuesdays from Oct. 13 to Dec. 1"),
        f("time", "single_line_text_field", "Time", "For example: 3:00 - 4:30 pm"),
        f("first_day", "date", "First day", "Puts the list in order."),
        f("last_day", "date", "Last day", "The class leaves the list the day after."),
        f("for", "single_line_text_field", "For", "Grades or ages. For example: Grades 3-5"),
        f("fee", "single_line_text_field", "Fee", "For example: $230, or TBD"),
        f("teacher", "single_line_text_field", "Teacher"),
        f("location", "multi_line_text_field", "Where", "One line for each part. For example: Boundary Elementary, then Room 011."),
        f("places", "number_integer", "Places", "Optional. The most it takes, for example 18."),
        f("status", "single_line_text_field", "Status", "Open shows the Register button. Full, Waitlist, Opens soon and Closed say so. Change it the moment the class fills, in the same sitting as on the district's page.",
          validations=[{"name": "choices", "value": json.dumps(STATUSES)}]),
        f("opens_on", "date", "Registration opens", "Optional. Shown with the status Opens soon."),
        f("register", "url", "Registration link", "The class's own registration page on the district's site."),
    ],
}

D = "https://artistsforkids.sd44.ca/learn/after-school-art/"
FALL_2026 = [
    {"handle": "fall-2026-wonderful-watercolours", "name": "Wonderful Watercolours",
     "description": "Welcome to the vibrant world of watercolours! In this class young artists will embark on exciting journey of creativity and self-expression through the medium of watercolours. Using a variety of materials we will spend time using nature as inspiration and students will develop their observation skills, brush techniques, colour mixing and blending.",
     "when": "8 Tuesdays from Oct. 13 to Dec. 1", "time": "3:00 - 4:30 pm", "first_day": "2026-10-13", "last_day": "2026-12-01",
     "for": "Grades 3-5", "fee": "$230", "teacher": "Caroline Falconer", "location": "Boundary Elementary\nRoom 011",
     "register": D + "wonderful-watercolours/"},
    {"handle": "fall-2026-brushstrokes-and-beyond", "name": "Brushstrokes and Beyond: Art through the Ages",
     "description": "Students will explore artists and art movements through fun and playful mixed media projects. Each week, we use prominent works of art to inspire our own creations, using drawing, painting, and a variety of exciting mediums.",
     "when": "8 Tuesdays from Oct. 13 to Dec. 1", "time": "2:50 - 4:20 pm", "first_day": "2026-10-13", "last_day": "2026-12-01",
     "for": "Grades 1-3", "fee": "$230", "teacher": "Marcel Eugene", "location": "Eastview Elementary\nRoom 129",
     "register": D + "brushstrokes-and-beyond-art-through-the-ages/"},
    {"handle": "fall-2026-natures-fall-wonders", "name": "Nature's Fall Wonders",
     "description": "Inspired by the changes in nature, autumnal colours, and natural materials, students will create fun and whimsical projects using a variety of techniques and mediums.",
     "when": "8 Tuesdays from Oct. 13 to Dec. 1", "time": "3:45 - 5:15 pm", "first_day": "2026-10-13", "last_day": "2026-12-01",
     "for": "Grades 1-3", "fee": "$230", "teacher": "Lisa Pedersen", "location": "Artists for Kids\nShadbolt Studio",
     "register": D + "natures-fall-wonders/"},
    {"handle": "fall-2026-mural-club", "name": "Mural Club",
     "description": "Plan, design, and create a mural based on a theme (e.g., nature) that you can display at your school or home! We will look at local Vancouver artists to gain inspiration as you go through the design process. Materials will be paint and 2’x4’ plywood canvas.",
     "when": "8 Tuesdays from Oct. 13 - Dec. 1", "time": "3:00 - 4:30 pm", "first_day": "2026-10-13", "last_day": "2026-12-01",
     "for": "Grades 4-7", "fee": "$230", "teacher": "Kaira Pena", "location": "Capilano Elementary\nAtrium",
     "register": D + "mural-club/"},
    {"handle": "fall-2026-print-it-sculpt-it", "name": "Print it! Sculpt it!",
     "description": "In this hands‑on art adventure, students explore how artists turn flat ideas into 3D creations. Young makers will experiment with foam printmaking, then transform everyday “junk” materials into imaginative sculptures. They’ll build with wire, nylon, clay, cardboard, and found objects, discovering how shapes, textures, and patterns can leap off the page.",
     "when": "7 Wednesdays from Oct. 14 to Dec. 2 (no class on Nov. 11)", "time": "3:00 - 4:30 pm", "first_day": "2026-10-14", "last_day": "2026-12-02",
     "for": "Grades 2-4", "fee": "$200", "teacher": "Michelle Phillips", "location": "Carisbrooke Elementary\nRoom 207\nArt Studio",
     "register": D + "print-it-sculpt-it/"},
    {"handle": "fall-2026-clay-sculpture", "name": "Clay Sculpture: Inspired by Nature!",
     "description": "Students will explore the forms, textures, and patterns found in the natural world to create original clay sculptures. They will develop skills in hand-building, sculpting, and surface design.",
     "when": "8 Thursdays from Oct. 15 - Dec. 3", "time": "3:45 - 5:15 pm", "first_day": "2026-10-15", "last_day": "2026-12-03",
     "for": "Grades 4-7", "fee": "$230", "teacher": "Laurel Newton", "location": "Artists for Kids\nShadbolt Studio",
     "register": D + "clay-sculpture-inspired-by-nature/"},
]
GROUP = "Fall 2026 classes"

Q = {
    "definition": "mutation($definition: MetaobjectDefinitionCreateInput!) { metaobjectDefinitionCreate(definition: $definition) { "
                  "metaobjectDefinition { id type fieldDefinitions { key } } userErrors { field message } } }",
    "entry": "mutation($metaobject: MetaobjectCreateInput!) { metaobjectCreate(metaobject: $metaobject) { "
             "metaobject { id handle displayName } userErrors { field message } } }",
}


def read(query, variables=None):
    data, err = execute(query, variables or {}, False)
    if err:
        sys.exit(err)
    return data


def step_definition():
    have = read('query { metaobjectDefinitionByType(type: "class") { id } }')["metaobjectDefinitionByType"]
    return [] if have else [("definition: Class", "definition", {"definition": DEFINITION})]


def step_fall_2026():
    if not read('query { metaobjectDefinitionByType(type: "class") { id } }')["metaobjectDefinitionByType"]:
        sys.exit("STOPPED: no Class definition yet. Run `definition` first.")
    have = {n["handle"] for n in read('query { metaobjects(type: "class", first: 250) { nodes { handle } } }')["metaobjects"]["nodes"]}
    out = []
    for c in FALL_2026:
        if c["handle"] in have:
            continue
        values = dict(c, programme_page=AFTER_SCHOOL_ART, group=GROUP, status="Open")
        fields = [{"key": k, "value": v} for k, v in values.items() if k != "handle"]
        out.append((f"class: {c['name']}", "entry", {"metaobject": {
            "type": "class", "handle": c["handle"], "fields": fields,
            "capabilities": {"publishable": {"status": "ACTIVE"}}}}))
    return out


STEPS = {"definition": step_definition, "fall-2026": step_fall_2026}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in STEPS:
        sys.exit(__doc__)
    step, go = sys.argv[1], "--go" in sys.argv[2:]
    todo = STEPS[step]()
    if not go:
        for name, kind, variables in todo:
            print(f"would run {kind}: {name}")
            if "--full" in sys.argv[2:]:
                print("   send:", json.dumps(variables, ensure_ascii=False)[:2000])
        print(f"{len(todo)} call(s) listed; nothing changed")
        sys.exit(0)
    CREATED.mkdir(parents=True, exist_ok=True)
    path = CREATED / f"{step}.json"
    log = json.loads(path.read_text()) if path.exists() else []
    for n, (name, kind, variables) in enumerate(todo):
        data, err = execute(Q[kind], variables, True)
        errors = user_errors(data) if not err else [{"message": err}]
        log.append({"call": name, "kind": kind, "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                    "variables": variables, "answer": data, "errors": errors})
        path.write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n")
        if errors:
            sys.exit(f"STOPPED at {name}: {errors}\n{n} call(s) made before it; see {path}")
        print(f"done {kind}: {name}")
    print(f"{len(todo)} call(s) made")
