#!/usr/bin/env python3
"""The first exhibition entries and one event, created for the build review (Michael's go-ahead,
2026-09-25). Text is the gallery's own, moved from the old exhibition pages without rewriting;
pasted formatting stays behind. Prints the variables for the metaobjectCreate mutations.

  python3 proposals/store-writes/entries.py exhibitions
  python3 proposals/store-writes/entries.py event <collect-assemble-gather entry id>
"""
import json
import sys


def t(value, bold=False, italic=False):
    node = {"type": "text", "value": value}
    if bold:
        node["bold"] = True
    if italic:
        node["italic"] = True
    return node


def p(*children):
    return {"type": "paragraph", "children": [c if isinstance(c, dict) else t(c) for c in children]}


def ul(*items):
    return {"type": "list", "listType": "unordered",
            "children": [{"type": "list-item", "children": [t(i)]} for i in items]}


def rich(*blocks):
    return json.dumps({"type": "root", "children": list(blocks)}, ensure_ascii=False)


def img(n):
    return f"gid://shopify/MediaImage/{n}"


def entry(handle, fields):
    return {
        "type": "exhibition",
        "handle": handle,
        "capabilities": {"publishable": {"status": "ACTIVE"}},
        "fields": [{"key": k, "value": v} for k, v in fields.items() if v not in (None, "")],
    }


CAG_ARTISTS = [
    "Kenojuak Ashevak", "Sara-Jeanne Bourget", "Victor Cicansky", "Douglas Coupland", "Christos Dikeakos",
    "Stan Douglas", "Sylvan Hamburger", "Sesemiya", "Roz Marshall", "Michelle Sound", "Brendan Tang",
    "Marlene Yuen", "Gu Xiong", "Robert Young", "T&T Collective (Tyler Brett and Tony Romano)",
    "Vancouver School Collective", "Samuel Roy-Bois", "Jack Shadbolt", "Gordon Smith",
]

EXHIBITIONS = [
    # From the On Now page (the exhibition that opens 2026-09-25).
    entry("collect-assemble-gather", {
        "title": "Collect, Assemble, Gather",
        "start_date": "2026-09-25",
        "end_date": "2027-02-20",
        "curator_credit": "Curated by Amelia Epp with support from the Artists For Kids team",
        "artists": json.dumps(CAG_ARTISTS, ensure_ascii=False),
        "reception_start": "2026-09-25T18:00:00-07:00",
        "reception_end": "2026-09-25T20:00:00-07:00",
        "reception_note": "Welcome ceremony at 7 PM",
        "key_image": img(45633111785769),
        "key_image_is_artwork": "true",
        "key_image_caption": rich(p("Samuel Roy-Bois, ", t("My Sun", italic=True), ", 2024. Wood, Paint, Object. Photo by Michael Love.")),
        "summary": "Collect, Assemble, Gather explores acts of collecting as both artistic process and everyday ritual. From the gathering of people in shared spaces to the sorting of materials such as seeds, stones, and fabric scraps, the exhibition presents work about assembling meaning, sustenance, and connection through creative and communal acts.",
        "body": rich(
            p("The exhibition frames the Gordon Smith Gallery as a shared space to engage with artwork, educational programming, and interactive installations, providing opportunities to explore the following questions:"),
            ul("What role does collecting play in the artistic process?",
               "How do the ways we collect and gather from the lands and waters reflect our relationship with the Earth?",
               "In what ways do objects tell stories about identity, place, and memory?",
               "How do collaboration and community-based practices build relationships and shape the meanings of an artwork?",
               "What connections can we make between learning and creative assembling?"),
            p(t("Collect, Assemble, Gather", italic=True),
              " brings together artworks from the Artists for Kids and the Gordon Smith Gallery Permanent Collection, alongside contributions from contemporary Canadian artists and student artists from across the Lower Mainland. The exhibition features works by ",
              t("Kenojuak Ashevak, Sara-Jeanne Bourget, Victor Cicansky, Douglas Coupland, Christos Dikeakos, Stan Douglas, Sylvan Hamburger, Sesemiya, Roz Marshall, Michelle Sound, Brendan Tang, Marlene Yuen, Gu Xiong, Robert Young, the T&T Collective (Tyler Brett and Tony Romano), the Vancouver School Collective, Samuel Roy-Bois, Jack Shadbolt, and Gordon Smith", bold=True),
              ". Perspectives from elementary and secondary students from the North Vancouver and Vancouver School Districts are also featured through linocut prints and collaborative collections presented in the Mezzanine Gallery."),
        ),
        "credits": rich(p(t("We acknowledge the support of the Canada Council for the Arts.", italic=True))),
        "funder_logos": json.dumps([img(45716498317609)]),
    }),
    # From the page exhibition-one-hundred-artists-deep and its template's gallery.
    entry("one-hundred-artists-deep", {
        "title": "One Hundred Artists Deep",
        "start_date": "2026-04-11",
        "end_date": "2026-06-20",
        "curator_credit": "Curated by Andrea Valentine-Lewis",
        "artists": json.dumps(["Corey Bulpitt", "Andrew Dadson", "Alex Gibson", "Chantal Gibson", "Tiziana La Melia", "veto monteiro", "Manuel Axel Strain", "Isabel Wynn"]),
        "collection_artists": json.dumps(["Bill Reid", "Jack Shadbolt", "Gordon Smith"]),
        "key_image": img(45566339481897),
        "key_image_caption": rich(p("Photo by Rachel Topham")),
        "summary": "In One Hundred Artists Deep, eight local artists were invited to create new work in response to artworks from the Artists for Kids and Gordon Smith Gallery Permanent Collection by founders Bill Reid (1920–1998), Jack Shadbolt (1909–1998), and Gordon Smith (1919–2020). Each of these founding artists left an enduring legacy, not only through their artistic practices but through their deep commitment to arts education.",
        "body": rich(
            p("Over the course of their lives, Reid, Shadbolt, and Smith taught and mentored thousands of young artists and apprentices. Their ideas, values, and approaches to making continue to circulate—sometimes visibly, sometimes quietly—through subsequent generations of artists."),
            p("The eight participating artists were selected for the strength and diversity of their practices, as well as for their sensitive and intuitive approaches to art-making. They were invited to respond to works by Reid, Shadbolt, and Smith from the Artists For Kids and Gordon Smith Gallery Permanent Collection, with full freedom in how that response took shape. The historical works and the contemporary responses are presented together in the gallery, creating a space for conversation across time."),
            p("The exhibition’s title is drawn from a phrase that Smith often used, saying he was “a hundred artists deep” and stood “on the shoulders” of artists past and present. Every artist emerges from a layered history of influence—artistic, personal, familial, educational, and cultural. ",
              t("One Hundred Artists Deep", italic=True),
              " reflects on this accumulated inheritance and the many ways artistic knowledge is carried forward."),
        ),
        "installation_views": json.dumps([img(n) for n in (45698187821353, 45698187952425, 45698187919657, 45698187985193, 45698187788585, 45716933574953, 45716928823593, 45698187886889, 45716935475497)]),
        "installation_credit": "Photos by Rachel Topham",
    }),
    # From the Upcoming Exhibitions card (no text yet, so its card doesn't link).
    entry("against-the-latitude-of-progress", {
        "title": "Against the Latitude of \"Progress\"",
        "start_date": "2027-04-09",
        "end_date": "2027-06-19",
        "key_image": img(45689287868713),
        "key_image_is_artwork": "true",
    }),
    # From the Past Exhibitions archive: one of the six older shows (DS-25), title, dates, image.
    entry("play", {
        "title": "Play",
        "start_date": "2020-09-25",
        "end_date": "2021-02-26",
        "key_image": img(45717203452201),
    }),
]


def event(cag_id):
    # From the On Now page: "Curatorial Tour: October 26 | 3:30 PM - 4:30 PM".
    return {
        "type": "event",
        "handle": "curatorial-tour-collect-assemble-gather",
        "capabilities": {"publishable": {"status": "ACTIVE"}},
        "fields": [
            {"key": "title", "value": "Curatorial Tour"},
            {"key": "starts", "value": "2026-10-26T15:30:00-07:00"},
            {"key": "ends", "value": "2026-10-26T16:30:00-07:00"},
            {"key": "exhibition", "value": cag_id},
        ],
    }


if __name__ == "__main__":
    if sys.argv[1] == "exhibitions":
        print(json.dumps({k: e for k, e in zip("abcd", EXHIBITIONS)}, indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"e": event(sys.argv[2])}, indent=2, ensure_ascii=False))
