#!/usr/bin/env python3
"""Programme pages (Michael's go-ahead, 2026-09-25, "All seven pages"): page field, card and
card group definitions (content model parts 1, 4, 6), the cards and events the seven programme
pages carried in their old templates, and the field values on those pages. Text is the gallery's,
moved without rewriting. Prints the variables for each step's mutation.

  python3 proposals/store-writes/programmes.py card-definition
  python3 proposals/store-writes/programmes.py card-group-definition <card definition id>
  python3 proposals/store-writes/programmes.py page-field-definitions <card group definition id>
  python3 proposals/store-writes/programmes.py cards
  python3 proposals/store-writes/programmes.py card-groups <cards.json from the cards step>
  python3 proposals/store-writes/programmes.py events
  python3 proposals/store-writes/programmes.py page-fields <card-groups.json from that step>
"""
import json
import sys

IMAGE = [{"name": "file_type_options", "value": json.dumps(["Image"])}]
PROGRAMME = [{"name": "choices", "value": json.dumps(["Gallery", "Smith Foundation", "Artists for Kids"])}]
SITE = "https://gordonsmithgallery.com"


def img(n):
    return f"gid://shopify/MediaImage/{n}"


def page(n):
    return f"gid://shopify/Page/{n}"


def link(url, text=""):
    return json.dumps({"text": text, "url": url}, ensure_ascii=False)


def f(key, type_, name, description="", required=False, validations=None):
    out = {"key": key, "type": type_, "name": name, "required": required}
    if description:
        out["description"] = description
    if validations:
        out["validations"] = validations
    return out


PAGES = {
    "artists-for-kids": 155720810793,
    "public-programs-1": 155718943017,
    "the-smith-foundation": 155705409833,
    "speaker-series": 155719434537,
    "music-at-the-smith": 155719696681,
    "explore-create": 155720089897,
    "art-in-good-company": 155720253737,
}


def card_definition():
    return {"definition": {
        "type": "card", "name": "Card", "displayNameKey": "title",
        "description": "One card in a card group: image, title, text, link. With an image it shows as an image card, without as a text card.",
        "access": {"storefront": "PUBLIC_READ"},
        "fieldDefinitions": [
            f("image", "file_reference", "Image", "Optional. Set its focal point in Files.", validations=IMAGE),
            f("title", "single_line_text_field", "Title", required=True),
            f("text", "multi_line_text_field", "Text"),
            f("link", "link", "Link", "Leave the link text blank and the whole card links through its title. With link text, it shows as a link under the text. Off-site addresses get the external-site arrow."),
        ],
    }}


def card_group_definition(card_definition_id):
    return {"definition": {
        "type": "card_group", "name": "Card group", "displayNameKey": "heading",
        "description": "A grid of cards on a page, shown after the page text. Add it to a page's Card groups field.",
        "access": {"storefront": "PUBLIC_READ"},
        "fieldDefinitions": [
            f("heading", "single_line_text_field", "Heading", "Optional, for example: Board of Directors."),
            f("cards", "list.metaobject_reference", "Cards", required=True,
              validations=[{"name": "metaobject_definition_id", "value": card_definition_id}]),
        ],
    }}


def page_field_definitions(card_group_definition_id):
    defs = [
        ("hero_image", "file_reference", "Hero image", "The page's main image. Set its focal point in Files. Without one, the page gets a plain header.", IMAGE),
        ("hero_is_artwork", "boolean", "Hero image is an artwork", "An artwork shows whole, never cropped or covered.", None),
        ("hero_caption", "single_line_text_field", "Hero caption", "Photo credit or caption under the hero image, for example: Photo by Khim Mata Hipol.", None),
        ("eyebrow", "single_line_text_field", "Label above the title", "Only when it adds something the title doesn't, such as the programme the page belongs to. Blank on most pages.", None),
        ("intro", "multi_line_text_field", "Intro", "One or two sentences under the title, in bold.", None),
        ("cta", "link", "Call to action", "One button under the title, for example: Artists For Kids Website.", None),
        ("programme", "single_line_text_field", "Programme", "Sets the page's colours, and the programme's logo when there's no hero image. Blank means the Gallery.", PROGRAMME),
        ("card_groups", "list.metaobject_reference", "Card groups", "Grids of cards shown after the page text, in this order.",
         [{"name": "metaobject_definition_id", "value": card_group_definition_id}]),
        ("gallery_images", "list.file_reference", "Gallery images", "Optional image gallery at the end of the page.", IMAGE),
    ]
    out = {}
    for i, (key, type_, name, desc, validations) in enumerate(defs):
        d = {"namespace": "custom", "key": key, "name": name, "description": desc, "type": type_,
             "ownerType": "PAGE", "pin": True}
        if validations:
            d["validations"] = validations
        out[f"d{i}"] = d
    return out


def card(handle, title, image=None, text=None, url=None, link_text=""):
    fields = [{"key": "title", "value": title}]
    if image:
        fields.append({"key": "image", "value": img(image)})
    if text:
        fields.append({"key": "text", "value": text})
    if url:
        fields.append({"key": "link", "value": link(url, link_text)})
    return {"type": "card", "handle": handle, "fields": fields}


CARDS = {
    # Artists for Kids: its six programmes, on the Artists for Kids website (Q5, P-15).
    "afk": [
        card("afk-after-school-art", "After School Art Classes", 45746713854249, url="https://artistsforkids.sd44.ca/learn/after-school-art/"),
        card("afk-artists-in-residence", "Artist In Residence Enrichment Workshops", 45819820769577, url="https://artistsforkids.sd44.ca/learn/artists-in-residence/"),
        card("afk-day-camps", "Spring and Summer Day Camps", 45746720669993, url="https://artistsforkids.sd44.ca/learn/spring--summer-day-camps/"),
        card("afk-gallery-programs", "Gallery Programs", 45698058256681, url="https://artistsforkids.sd44.ca/learn/gallery-program/"),
        card("afk-paradise-valley", "Paradise Valley Summer School of Visual Art Camp", 45819842658601, url="https://artistsforkids.sd44.ca/learn/paradise-valley-summer-camps/"),
        card("afk-learning-kits", "Learning Kits and Outreach", 45819844952361, url="https://artistsforkids.sd44.ca/learn/learning-kits/"),
    ],
    # Public Programs: its four programmes. Images are each programme page's hero; Music at the
    # Smith gets the link it was missing.
    "programs": [
        card("programs-explore-create", "Explore + Create Saturdays", 45668902568233, url=f"{SITE}/pages/explore-create"),
        card("programs-art-in-good-company", "Art In Good Company", 45668975214889, url=f"{SITE}/pages/art-in-good-company"),
        card("programs-speaker-series", "Speaker Series", 45698097250601, url=f"{SITE}/pages/speaker-series"),
        card("programs-music-at-the-smith", "Music At The Smith", 45820261237033, url=f"{SITE}/pages/music-at-the-smith"),
    ],
    # The Smith Foundation: five ways to take part. "More" links become title links; the three
    # "More" links that went nowhere are left out.
    "foundation": [
        card("foundation-public-programs", "Public Programs", 45809575985449,
             "By attending our public programs, tours, and special events, including our Speaker Series and Music at The Smith, you directly support The Foundation while connecting with a community of people who share a passion for Canadian art and children's art education.",
             f"{SITE}/pages/public-programs-1"),
        card("foundation-donations", "Donations", 45808826155305,
             "You can help ensure that children and youth continue to experience the joy, confidence, and curiosity that come from making and encountering art at the Gordon Smith Gallery and through Artists for Kids.",
             f"{SITE}/pages/donate", "Donate Today"),
        card("foundation-brilliance-gala", "Brilliance Gala & Auctions", 45808448536873,
             "The Brilliance Gala is a chance to come together to support a key facet of Gordon Smith’s legacy: quality, artist- and educator-led arts education for children and youth across the Lower Mainland through Artists for Kids."),
        card("foundation-scholarships", "Smith Foundation Scholarships", 45717190967593,
             "The Gordon and Marion Smith Foundation is pleased to offer three scholarships to graduating students from North Vancouver, West Vancouver and Vancouver, who have completed or are enrolled in Grade 12."),
        card("foundation-endowment", "Endowment", 45809013457193,
             "The Gordon and Marion Smith Foundation established a permanent endowment fund whose increasing annual revenues ensure the success and viability of Artists for Kids and their programs and support the Gordon Smith Gallery of Canadian Art in perpetuity. The Vancouver Foundation, Canada's largest community foundation, manages our endowment."),
    ],
    # The Smith Foundation's board, in the old order.
    "board": [
        card(f"board-{h}", name, image, role) for h, name, role, image in [
            ("paul-killeen", "Paul Killeen", "Chair", 45739036213545),
            ("daylen-luchsinger", "Daylen Luchsinger", "Vice Chair", 45739053318441),
            ("meredith-preuss", "Meredith Preuss", "Executive Director", 45739179999529),
            ("tyler-quarles", "Tyler Quarles", "Treasurer", 45739187437865),
            ("virginia-engel", "Virginia Engel", "Director", 45739217125673),
            ("shannon-heth", "Shannon Heth", "Director", 45739218829609),
            ("john-david-james", "John David James", "Director", 45739211784489),
            ("allison-kerr", "Allison Kerr", "Director", 46307068936489),
            ("richard-savage", "Richard Savage", "Director", 45739198382377),
            ("ed-tsumura", "Ed Tsumura", "Director", 45739204182313),
            ("anne-watt", "Anne Watt", "Director", 45739206476073),
            ("ian-wallace", "Ian Wallace", "Director", 45739208442153),
            ("emmy-lee-wall", "Emmy Lee Wall", "Director", 45739213422889),
            ("krista-whitelock", "Krista Whitelock", "Director", 45739215094057),
        ]
    ],
}

GROUPS = [
    ("afk-programmes", "", "afk"),
    ("public-programs", "", "programs"),
    ("foundation-take-part", "", "foundation"),
    ("foundation-board", "Board of Directors", "board"),
]


def cards_payload():
    out = {}
    for group, items in CARDS.items():
        for c in items:
            out[c["handle"].replace("-", "_")] = c
    return out


def card_groups_payload(created):
    ids = {v["metaobject"]["handle"]: v["metaobject"]["id"] for v in created.values()}
    out = {}
    for handle, heading, group in GROUPS:
        fields = [{"key": "cards", "value": json.dumps([ids[c["handle"]] for c in CARDS[group]])}]
        if heading:
            fields.insert(0, {"key": "heading", "value": heading})
        out[handle.replace("-", "_")] = {"type": "card_group", "handle": handle, "fields": fields}
    return out


def event(handle, title, starts, ends=None, page_handle=None, location=None, summary=None, image=None):
    fields = [{"key": "title", "value": title}, {"key": "starts", "value": starts}]
    if ends:
        fields.append({"key": "ends", "value": ends})
    if location:
        fields.append({"key": "location", "value": location})
    if summary:
        fields.append({"key": "summary", "value": summary})
    if image:
        fields.append({"key": "image", "value": img(image)})
    if page_handle:
        fields.append({"key": "programme_page", "value": page(PAGES[page_handle])})
    return {"type": "event", "handle": handle, "capabilities": {"publishable": {"status": "ACTIVE"}}, "fields": fields}


ARBEL = "\n\n".join([
    "Doors 6 PM, talk begins 6:30 PM.",
    "Co-founder and Creative Director of Bocci and founder of Omer Arbel Office (OAO), Omer Arbel’s wide-ranging career offers a reflection on the lasting influence of creative education on his practice, which moves fluidly between architecture, sculpture, industrial design and materials research.",
    "Trained in architecture, Arbel's approach is grounded in critical inquiry, spatial awareness, and experimentation. His work reflects the broader premise of Art Education, for Life: that early engagement with art and creative education are not simply preparation for a particular profession, but a way of approaching ideas, materials and problems over a lifetime. Through sustained experimentation with glass, concrete, metals, and light, Arbel demonstrates how curiosity and craft can form the foundation of an evolving creative practice.",
    "This conversation offers audiences a rare opportunity to hear directly from Arbel about the experiences that have shaped that practice. Reaching back into childhood, he will reflect on formative encounters with art and making, and consider how they may have informed the interests, instincts and obsessions that continue to surface in his work today. For artists, designers, students and anyone curious about the creative process, the talk offers an inside look at what it means to build a life around inquiry, making and experimentation.",
])

MODESTINE = "\n\n".join([
    "Join us for an afternoon concert on Saturday, November 7th for Music at The Smith.",
    "La Modestine is a chamber music ensemble formed in 2016 by west coast musicians with a love of playing music of the 17th and 18th centuries together. The members bring a wealth of international experience to playing this enchanting repertoire on period instruments.",
    "Tickets Coming Soon",
])

EVENTS = [
    event("explore-create-2026-09-26", "Explore + Create", "2026-09-26T13:00:00-07:00", "2026-09-26T15:00:00-07:00", "explore-create", "Main Floor",
          "Join us for an activity inspired by Brendan Tang's work, Manga Ormolu 2.0-R."),
    event("explore-create-2026-10-03", "Explore + Create", "2026-10-03T13:00:00-07:00", "2026-10-03T15:00:00-07:00", "explore-create", "Main Floor"),
    event("explore-create-2026-10-10", "Explore + Create", "2026-10-10T13:00:00-07:00", "2026-10-10T15:00:00-07:00", "explore-create", "Main Floor"),
    event("explore-create-2026-10-17", "Explore + Create", "2026-10-17T13:00:00-07:00", "2026-10-17T15:00:00-07:00", "explore-create", "Main Floor"),
    event("art-in-good-company-2026-10-08", "Art In Good Company", "2026-10-08T14:30:00-07:00", "2026-10-08T16:00:00-07:00", "art-in-good-company",
          image=45845296087337),
    event("music-at-the-smith-la-modestine-2026-11-07", "La Modestine", "2026-11-07T13:00:00-08:00", "2026-11-07T15:00:00-08:00", "music-at-the-smith",
          summary=MODESTINE, image=45820498608425),
    event("speaker-series-omer-arbel-2026-11-26", "Art Education, For Life: Reflections from Omer Arbel", "2026-11-26T18:00:00-08:00", None, "speaker-series",
          summary=ARBEL, image=45668745576745),
]


def page_fields_payload(created_groups):
    ids = {v["metaobject"]["handle"]: v["metaobject"]["id"] for v in created_groups.values()}
    rows = [
        ("artists-for-kids", "hero_image", "file_reference", img(45746709102889)),
        ("artists-for-kids", "hero_caption", "single_line_text_field", "Photo by Khim Mata Hipol"),
        ("artists-for-kids", "programme", "single_line_text_field", "Artists for Kids"),
        ("artists-for-kids", "cta", "link", link("https://artistsforkids.sd44.ca/", "Artists For Kids Website")),
        ("artists-for-kids", "card_groups", "list.metaobject_reference", json.dumps([ids["afk-programmes"]])),
        ("public-programs-1", "hero_image", "file_reference", img(45739407114537)),
        ("public-programs-1", "card_groups", "list.metaobject_reference", json.dumps([ids["public-programs"]])),
        ("the-smith-foundation", "hero_image", "file_reference", img(45739448631593)),
        ("the-smith-foundation", "programme", "single_line_text_field", "Smith Foundation"),
        ("the-smith-foundation", "cta", "link", link(f"{SITE}/cdn/shop/files/SMITH_ANNUAL_REPORT_2025.pdf", "2025 A Year In Review")),
        ("the-smith-foundation", "card_groups", "list.metaobject_reference", json.dumps([ids["foundation-take-part"], ids["foundation-board"]])),
        ("speaker-series", "hero_image", "file_reference", img(45698097250601)),
        ("music-at-the-smith", "hero_image", "file_reference", img(45820259500329)),
        ("explore-create", "hero_image", "file_reference", img(45668902568233)),
        ("explore-create", "hero_caption", "single_line_text_field", "Photos by Khim Mata Hipol"),
        ("art-in-good-company", "hero_image", "file_reference", img(45668975214889)),
    ]
    return {"metafields": [
        {"ownerId": page(PAGES[h]), "namespace": "custom", "key": k, "type": t, "value": v} for h, k, t, v in rows
    ]}


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "card-definition":
        data = card_definition()
    elif step == "card-group-definition":
        data = card_group_definition(sys.argv[2])
    elif step == "page-field-definitions":
        data = page_field_definitions(sys.argv[2])
    elif step == "cards":
        data = cards_payload()
    elif step == "card-groups":
        data = card_groups_payload(json.load(open(sys.argv[2])))
    elif step == "events":
        data = {e["handle"].replace("-", "_"): e for e in EVENTS}
    elif step == "page-fields":
        data = page_fields_payload(json.load(open(sys.argv[2])))
    print(json.dumps(data, indent=2, ensure_ascii=False))
