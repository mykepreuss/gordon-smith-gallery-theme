#!/usr/bin/env python3
"""Metaobject definitions for exhibitions and events (content model parts 2 and 5, approved
2026-09-25, P-10 to P-12, P-16). Prints the variables for the metaobjectDefinitionCreate mutation.

  python3 proposals/store-writes/definitions.py exhibition
  python3 proposals/store-writes/definitions.py event <exhibition definition id>
"""
import json
import sys

IMAGE = [{"name": "file_type_options", "value": json.dumps(["Image"])}]
PROGRAMME = [{"name": "choices", "value": json.dumps(["Gallery", "Smith Foundation", "Artists for Kids"])}]


def f(key, type_, name, description="", required=False, validations=None):
    out = {"key": key, "type": type_, "name": name, "required": required}
    if description:
        out["description"] = description
    if validations:
        out["validations"] = validations
    return out


EXHIBITION = {
    "type": "exhibition",
    "name": "Exhibition",
    "description": "One exhibition. Its page is at /pages/exhibitions/<handle>. On now, Upcoming and Past follow the dates.",
    "displayNameKey": "title",
    "access": {"storefront": "PUBLIC_READ"},
    "capabilities": {
        "publishable": {"enabled": True},
        "renderable": {"enabled": True, "data": {"metaTitleKey": "title", "metaDescriptionKey": "summary"}},
        "onlineStore": {"enabled": True, "data": {"urlHandle": "exhibitions"}},
    },
    "fieldDefinitions": [
        f("title", "single_line_text_field", "Title", required=True),
        f("subtitle", "single_line_text_field", "Subtitle"),
        f("start_date", "date", "Start date", "Sets the order and whether it's upcoming, on now or past. Without exact dates, enter the expected opening day and fill Dates note.", required=True),
        f("end_date", "date", "End date", "Blank means ongoing."),
        f("dates_note", "single_line_text_field", "Dates note", "Shown instead of the dates, for example: Opens fall 2027."),
        f("curator_credit", "single_line_text_field", "Curator credit", "The whole line as it should read, for example: Curated by Amelia Epp with support from the Artists For Kids team."),
        f("artists", "list.single_line_text_field", "Artists", "One name per line. A collective is one line."),
        f("collection_artists", "list.single_line_text_field", "Artists from the collection", "Artists from the permanent collection, shown as a second group."),
        f("venue", "single_line_text_field", "Where in the building", "For example: Main gallery and Mezzanine Gallery."),
        f("reception_start", "date_time", "Opening reception starts", "Shown until the reception has ended."),
        f("reception_end", "date_time", "Opening reception ends"),
        f("reception_note", "single_line_text_field", "Opening reception note", "For example: Welcome ceremony at 7 PM."),
        f("key_image", "file_reference", "Key image", "The hero and card image. Set its focal point in Files.", required=True, validations=IMAGE),
        f("key_image_is_artwork", "boolean", "Key image is an artwork", "An artwork shows whole, never cropped or covered."),
        f("key_image_caption", "rich_text_field", "Key image caption", "Artwork caption, photo credit, or both."),
        f("summary", "multi_line_text_field", "Summary", "One or two sentences: the card text, the intro on the page, and the description search engines and link previews use. With no summary and no text, the card doesn't link."),
        f("body", "rich_text_field", "Text"),
        f("installation_views", "list.file_reference", "Installation views", validations=IMAGE),
        f("installation_credit", "single_line_text_field", "Installation views credit", "For example: Photos by Rachel Topham."),
        f("credits", "rich_text_field", "Credits", "Presenters, partners, sponsors and funders, with links."),
        f("funder_logos", "list.file_reference", "Funder logos", "Logos a funder requires, for example the Canada Council for the Arts. Give each one alt text naming the funder.", validations=IMAGE),
        f("programme", "single_line_text_field", "Programme", "Sets the page's colours. Blank means the Gallery.", validations=PROGRAMME),
    ],
}


def event(exhibition_definition_id):
    return {
        "type": "event",
        "name": "Event",
        "description": "A dated event. It lists on its programme page, its exhibition's page and the Upcoming Events page, and drops off once it has ended.",
        "displayNameKey": "title",
        "access": {"storefront": "PUBLIC_READ"},
        "capabilities": {"publishable": {"enabled": True}},
        "fieldDefinitions": [
            f("title", "single_line_text_field", "Title", required=True),
            f("starts", "date_time", "Starts", required=True),
            f("ends", "date_time", "Ends"),
            f("location", "single_line_text_field", "Location", "Blank means the gallery. For example: Main floor."),
            f("summary", "multi_line_text_field", "Summary"),
            f("image", "file_reference", "Image", validations=IMAGE),
            f("tickets", "link", "Tickets", "Label and address, for example: Buy tickets. Until tickets are on sale, say so in the summary."),
            f("programme_page", "page_reference", "Programme page", "The programme page it belongs to, for example Explore + Create."),
            f("exhibition", "metaobject_reference", "Exhibition", "For tours and talks tied to an exhibition.",
              validations=[{"name": "metaobject_definition_id", "value": exhibition_definition_id}]),
        ],
    }


if __name__ == "__main__":
    which = sys.argv[1]
    d = EXHIBITION if which == "exhibition" else event(sys.argv[2])
    print(json.dumps({"definition": d}, indent=2, ensure_ascii=False))
