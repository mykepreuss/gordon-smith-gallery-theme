#!/usr/bin/env python3
"""Definitions for the Permanent Collection (proposals/permanent-collection.md, DS-62, P-27): the
artist, artwork and collection grouping entry types, and the editions' link to their artists.
Prints the variables for each mutation; they're run through the Shopify connector in this order,
since the types refer to each other:

  python3 definitions.py artist                     metaobjectDefinitionCreate (no Works field yet)
  python3 definitions.py artwork <artist def id>    metaobjectDefinitionCreate
  python3 definitions.py works <artist def id> <artwork def id>   metaobjectDefinitionUpdate: adds Works
  python3 definitions.py group <artwork def id>     metaobjectDefinitionCreate
  python3 definitions.py product <artist def id>    metafieldDefinitionCreate (custom.artist_entries)
  python3 definitions.py exhibition_works <artwork def id>   metaobjectDefinitionUpdate: the exhibition's
                                                    Works from the collection (DS-63)
  python3 definitions.py artist_notes <artist def id>        metaobjectDefinitionUpdate: Website isn't shown,
                                                    Documents follow the works (DS-63)
  python3 definitions.py document                   metaobjectDefinitionCreate: a document, with its cover (DS-63)
  python3 definitions.py artist_documents <artist def id> <document def id>
                                                    metaobjectDefinitionUpdate: Documents becomes a list of
                                                    document entries (run after the old list is emptied
                                                    and its field deleted)
"""
import json
import sys

EXHIBITION = "gid://shopify/MetaobjectDefinition/23753359657"
IMAGE = [{"name": "file_type_options", "value": json.dumps(["Image"])}]
CATEGORIES = ["Painting", "Print", "Drawing", "Photograph", "Sculpture", "Ceramic", "Textile", "Book"]
THEMES = ["Abstract", "Action", "Architecture", "Creatures", "Ecology", "Invention", "Landscape", "People",
          "Place", "Plants", "Portrait", "Social change", "Still life", "Storytelling", "Text"]


def f(key, type_, name, description="", required=False, validations=None):
    out = {"key": key, "type": type_, "name": name, "required": required}
    if description:
        out["description"] = description
    if validations:
        out["validations"] = validations
    return out


def refs(definition_id):
    return [{"name": "metaobject_definition_id", "value": definition_id}]


def page_type(type_, name, description, display, url_handle, fields, meta_description=None):
    renderable = {"metaTitleKey": display}
    if meta_description:
        renderable["metaDescriptionKey"] = meta_description
    return {"definition": {
        "type": type_, "name": name, "description": description, "displayNameKey": display,
        "access": {"storefront": "PUBLIC_READ"},
        "capabilities": {"publishable": {"enabled": True},
                         "renderable": {"enabled": True, "data": renderable},
                         "onlineStore": {"enabled": True, "data": {"urlHandle": url_handle}}},
        "fieldDefinitions": fields}}


def artist():
    return page_type("artist", "Artist", "An artist with work in the Permanent Collection or an edition in the Shop. "
                     "Their page is at /pages/artists/<handle>, and the Artists page lists every artist, A to Z by sort name.",
                     "name", "artists", [
        f("name", "single_line_text_field", "Name", "As it reads on the site, for example: Gordon Smith.", required=True),
        f("sort_name", "single_line_text_field", "Sort name", "Surname first, for the A to Z list, for example: Smith, Gordon. "
          "A single name or a collective's name stays as it is.", required=True),
        f("full_name", "single_line_text_field", "Full name", "Only when it says more than the name, for example: Gordon Appelbe Smith."),
        f("other_names", "single_line_text_field", "Other names", "A traditional or Indigenous name, for example: Guud san glans."),
        f("life_dates", "single_line_text_field", "Life dates", "For example: 1919 to 2020, or born 1966."),
        f("nationality", "single_line_text_field", "Nationality or Nation", "For example: Haida, or Canadian."),
        f("biography", "rich_text_field", "Biography"),
        f("portrait", "file_reference", "Portrait", "A photograph of the artist, with its credit in the alt text or biography.", validations=IMAGE),
        f("website", "link", "Website", "The artist's own site, or a gallery that represents them. Shown on the artist's page."),
        f("exhibitions", "list.metaobject_reference", "Exhibitions", "Exhibitions at the gallery that included the artist.", validations=refs(EXHIBITION)),
        f("documents", "list.file_reference", "Documents", "Press, exhibition lists and photographs about the artist. "
          "Shown as links, named by each file's alt text."),
    ])


def artwork(artist_id):
    return page_type("artwork", "Artwork", "A work in the Permanent Collection. Its page is at /pages/collection/<handle> "
                     "(the accession number). Add it to its artist's Works list too, so it shows on the artist's page.",
                     "title", "collection", [
        f("title", "single_line_text_field", "Title", "Without the edition number, which has its own field.", required=True),
        f("artists", "list.metaobject_reference", "Artists", "Usually one. A work made together lists each artist.", validations=refs(artist_id)),
        f("year", "single_line_text_field", "Year", "As the work is dated, for example: 1994, or N.D."),
        f("category", "single_line_text_field", "Category", validations=[{"name": "choices", "value": json.dumps(CATEGORIES)}]),
        f("medium", "single_line_text_field", "Medium"),
        f("dimensions", "single_line_text_field", "Dimensions"),
        f("edition", "single_line_text_field", "Edition", "For example: 30/40, or A/P."),
        f("accession_number", "single_line_text_field", "Accession number", required=True),
        f("credit_line", "single_line_text_field", "Credit line"),
        f("images", "list.file_reference", "Images", "The first is the main image. Each needs alt text in Files: artist, "
          "title, year, then what it shows.", validations=IMAGE),
        f("themes", "list.single_line_text_field", "Themes", validations=[{"name": "choices", "value": json.dumps(THEMES)}]),
        f("about", "rich_text_field", "About the work"),
        f("in_the_shop", "product_reference", "In the Shop", "The limited edition on sale, when this is the collection's copy of it."),
        f("shown_in", "list.metaobject_reference", "Shown in", "Exhibitions at the gallery that showed the work.", validations=refs(EXHIBITION)),
    ])


def works(artist_id, artwork_id):
    return {"id": artist_id, "definition": {"fieldDefinitions": [{"create": f(
        "works", "list.metaobject_reference", "Works", "The artist's works in the collection, in the order they show on "
        "the artist's page (oldest first).", validations=refs(artwork_id))}]}}


def group(artwork_id):
    return page_type("collection_group", "Collection grouping", "A way into the Permanent Collection: a category, a theme "
                     "or a grouping. Its page is at /pages/browse/<handle>, and the Permanent Collection page links to it.",
                     "name", "browse", [
        f("name", "single_line_text_field", "Name", required=True),
        f("kind", "single_line_text_field", "Kind", "Where the Permanent Collection page lists it.", required=True,
          validations=[{"name": "choices", "value": json.dumps(["Category", "Theme", "Grouping"])}]),
        f("introduction", "multi_line_text_field", "Introduction"),
        f("works", "list.metaobject_reference", "Works", validations=refs(artwork_id)),
    ], meta_description="introduction")


def product(artist_id):
    return {"definition": {
        "name": "Artist pages", "namespace": "custom", "key": "artist_entries", "ownerType": "PRODUCT",
        "type": "list.metaobject_reference", "pin": True,
        "description": "The artist's entry in the collection, so the label's artist name links to the artist's page and "
                       "the edition shows there. A work made together lists each artist.",
        "validations": refs(artist_id)}}


def exhibition_works(artwork_id):
    return {"id": EXHIBITION, "definition": {"fieldDefinitions": [{"create": f(
        "collection_works", "list.metaobject_reference", "Works from the collection",
        "Works from the Permanent Collection in the exhibition. They show on its page, after the installation views.",
        validations=refs(artwork_id))}]}}


def artist_notes(artist_id):
    return {"id": artist_id, "definition": {"fieldDefinitions": [
        {"update": {"key": "website", "name": "Website (not shown)",
                    "description": "Kept from the old Artists page's links. The site doesn't show it (DS-63)."}},
        {"update": {"key": "documents", "name": "Documents",
                    "description": "Press, catalogues, books and photographs, shown as links after the works, "
                                   "named by each file's alt text. A PDF over 20 MB can't be uploaded."}}]}}


def document():
    return {"definition": {
        "type": "document", "name": "Document",
        "description": "A document about an artist: press, a catalogue, a book, photographs. It shows on the artist's "
                       "page as a tile with its cover, after the works, and opens its file.",
        "displayNameKey": "title", "access": {"storefront": "PUBLIC_READ"},
        "capabilities": {"publishable": {"enabled": True}},
        "fieldDefinitions": [
            f("title", "single_line_text_field", "Title", "As it reads under the cover, for example: Press.", required=True),
            f("cover", "file_reference", "Cover", "An image of the cover or first page. Its alt text describes it.",
              validations=IMAGE),
            f("file", "file_reference", "File", "The PDF, or the photograph itself. Files can be 20 MB at most; "
              "without one, the tile shows its cover and doesn't open."),
        ]}}


def artist_documents(artist_id, document_id):
    return {"id": artist_id, "definition": {"fieldDefinitions": [{"create": f(
        "documents", "list.metaobject_reference", "Documents", "Press, catalogues, books and photographs, shown as "
        "tiles with their covers after the works.", validations=refs(document_id))}]}}


if __name__ == "__main__":
    which, args = sys.argv[1], sys.argv[2:]
    out = {"artist": artist, "artwork": artwork, "works": works, "group": group, "product": product,
           "exhibition_works": exhibition_works, "artist_notes": artist_notes, "document": document,
           "artist_documents": artist_documents}[which](*args)
    print(json.dumps(out, indent=1, ensure_ascii=False))
