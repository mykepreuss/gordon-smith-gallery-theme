#!/usr/bin/env python3
"""Tests for check_structured_data.py against small synthetic pages.

  python3 design-system/scripts/tests/test_check_structured_data.py
"""
import json
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check_structured_data as check  # noqa: E402

PLACE = {"@type": "ArtGallery", "name": "Gordon Smith Gallery", "url": "https://example.com/",
         "address": "2121 Lonsdale Avenue"}


def page(*blocks, title="A page | Gordon Smith Gallery", h1=1, canonical=True, description=True):
    head = f"<title>{title}</title>"
    if canonical:
        head += '<link rel="canonical" href="https://example.com/a">'
    if description:
        head += '<meta name="description" content="About the page.">'
    scripts = "".join(
        '<script type="application/ld+json">' + (b if isinstance(b, str) else json.dumps(b)) + "</script>"
        for b in blocks
    )
    return f"<html><head>{head}{scripts}</head><body>{'<h1>A page</h1>' * h1}</body></html>"


class CheckStructuredData(unittest.TestCase):
    def test_a_good_exhibition_passes(self):
        block = {"@context": "https://schema.org", "@type": "ExhibitionEvent",
                 "@id": "https://example.com/a#exhibition", "name": "Playhouse",
                 "url": "https://example.com/a", "startDate": "2026-09-25", "endDate": "2027-02-20",
                 "location": PLACE, "description": "A show.", "image": "https://example.com/a.jpg",
                 "eventStatus": "https://schema.org/EventScheduled", "organizer": PLACE}
        found, errors, warnings = check.check_page(page(block), ["ExhibitionEvent"])
        self.assertEqual(found, ["ExhibitionEvent"])
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_a_lesson_with_its_video_passes(self):
        block = {"@type": "LearningResource", "name": "Paths", "url": "https://example.com/a",
                 "video": {"@type": "VideoObject", "name": "Paths",
                           "thumbnailUrl": "https://example.com/a.jpg", "uploadDate": "2022-10-20"}}
        found, errors, _ = check.check_page(page(block), ["LearningResource"])
        self.assertEqual(found, ["LearningResource"])
        self.assertEqual(errors, [])

    def test_a_page_without_its_address(self):
        _, errors, _ = check.check_page(page({"@type": "CollectionPage", "name": "Prints"}))
        self.assertIn("CollectionPage: no url", errors)

    def test_a_month_is_a_date(self):
        block = {"@type": "ExhibitionEvent", "@id": "https://example.com/a#exhibition", "name": "Fall show",
                 "url": "https://example.com/a", "startDate": "2027-09", "location": PLACE}
        _, errors, _ = check.check_page(page(block))
        self.assertEqual(errors, [])
        block["startDate"] = "fall 2027"
        _, errors, _ = check.check_page(page(block))
        self.assertTrue(any("startDate is not a date" in e for e in errors))

    def test_a_property_on_the_wrong_type(self):
        vocabulary = {"types": {"Thing": [], "Product": ["Thing"], "ProductGroup": ["Product"],
                                "CreativeWork": ["Thing"], "VisualArtwork": ["CreativeWork"]},
                      "properties": {"name": ["Thing"], "artMedium": ["VisualArtwork"]}}
        block = {"@type": "ProductGroup", "@id": "https://example.com/a#product", "name": "A print",
                 "hasVariant": [], "artMedium": "Woodcut"}
        _, errors, _ = check.check_page(page(block), vocabulary=vocabulary)
        self.assertIn("ProductGroup: artMedium is not for this type (it is for VisualArtwork)", errors)
        self.assertIn("ProductGroup: hasVariant is not a schema.org property", errors)
        block["@type"] = ["ProductGroup", "VisualArtwork"]
        del block["hasVariant"]
        _, errors, _ = check.check_page(page(block), vocabulary=vocabulary)
        self.assertEqual([e for e in errors if "artMedium" in e], [])

    def test_a_type_schema_org_does_not_have(self):
        vocabulary = {"types": {"Thing": []}, "properties": {"name": ["Thing"]}}
        _, errors, _ = check.check_page(page({"@type": "Gallery", "name": "A"}), vocabulary=vocabulary)
        self.assertIn("Gallery: not a schema.org type", errors)

    def test_a_mention_of_something_the_page_does_not_describe(self):
        web = {"@type": "WebPage", "@id": "https://example.com/a#webpage", "name": "A",
               "url": "https://example.com/a", "mainEntity": {"@id": "https://example.com/a#work"}}
        _, errors, _ = check.check_page(page(web))
        self.assertIn("a mention of https://example.com/a#work, which the page doesn't describe", errors)
        work = {"@type": "VisualArtwork", "@id": "https://example.com/a#work", "name": "A",
                "url": "https://example.com/a"}
        _, errors, _ = check.check_page(page(work, web))
        self.assertEqual(errors, [])

    def test_one_thing_with_two_types(self):
        show = {"@type": "Event", "@id": "https://example.com/a#exhibition", "name": "A",
                "url": "https://example.com/a", "startDate": "2026-09-25", "location": PLACE}
        talk = {"@type": "Event", "@id": "https://example.com/#event-talk", "name": "Talk",
                "startDate": "2026-10-01", "location": PLACE,
                "superEvent": {"@type": "ExhibitionEvent", "@id": "https://example.com/a#exhibition", "name": "A"}}
        _, errors, _ = check.check_page(page(show, talk))
        self.assertIn("https://example.com/a#exhibition has different types on one page: Event, ExhibitionEvent", errors)
        talk["superEvent"] = {"@id": "https://example.com/a#exhibition"}
        _, errors, _ = check.check_page(page(show, talk))
        self.assertEqual(errors, [])

    def test_an_organisation_typed_more_or_less_closely(self):
        full = dict(PLACE, **{"@id": "https://example.com/#gallery"})
        web = {"@type": "WebPage", "@id": "https://example.com/a#webpage", "name": "A", "url": "https://example.com/a",
               "publisher": {"@type": "Organization", "@id": "https://example.com/#gallery", "name": "Gallery"}}
        _, errors, _ = check.check_page(page(full, web))
        self.assertEqual(errors, [])

    def test_a_thing_that_points_back_at_its_page(self):
        web = {"@type": "ProfilePage", "@id": "https://example.com/a#webpage", "name": "A", "url": "https://example.com/a",
               "mainEntity": {"@type": "Person", "@id": "https://example.com/a#artist", "name": "A",
                              "url": "https://example.com/a",
                              "mainEntityOfPage": {"@id": "https://example.com/a#webpage"}}}
        _, errors, _ = check.check_page(page(web))
        self.assertIn("https://example.com/a#artist points back at the page that is about it (mainEntityOfPage)", errors)
        del web["mainEntity"]["mainEntityOfPage"]
        _, errors, _ = check.check_page(page(web))
        self.assertEqual(errors, [])

    def test_a_main_thing_without_a_name_for_machines(self):
        block = {"@type": "Person", "name": "A", "url": "https://example.com/a"}
        _, _, warnings = check.check_page(page(block))
        self.assertIn("Person: no name for machines (@id)", warnings)

    def test_a_block_that_does_not_parse(self):
        _, errors, _ = check.check_page(page('{"@type": "Person", "name": "A",}'))
        self.assertTrue(any("doesn't parse" in e for e in errors))

    def test_a_missing_field(self):
        block = {"@type": "ExhibitionEvent", "name": "Playhouse", "url": "https://example.com/a",
                 "location": PLACE}
        _, errors, _ = check.check_page(page(block))
        self.assertIn("ExhibitionEvent: no startDate", errors)

    def test_a_nested_mention_may_be_short(self):
        block = {"@type": "Event", "name": "Tour", "startDate": "2026-10-26T15:30:00-07:00",
                 "location": PLACE, "superEvent": {"@type": "ExhibitionEvent", "name": "Playhouse"}}
        found, errors, _ = check.check_page(page(block))
        self.assertEqual(found, ["Event"])
        self.assertEqual(errors, [])

    def test_a_date_that_is_not_a_date(self):
        block = {"@type": "VisualArtwork", "name": "Beach", "url": "https://example.com/a",
                 "dateCreated": "n.d."}
        _, errors, _ = check.check_page(page(block))
        self.assertTrue(any("dateCreated is not a date" in e for e in errors))

    def test_an_address_that_is_not_full(self):
        block = {"@type": "Person", "name": "A", "url": "/pages/artists/a"}
        _, errors, _ = check.check_page(page(block))
        self.assertTrue(any("not a full web address" in e for e in errors))

    def test_styled_letters_in_a_title_and_a_name(self):
        styled = "Gordon Smith, \U0001D617\U0001D626\U0001D62F\U0001D625\U0001D626\U0001D633, 2006"
        block = {"@type": "Product", "name": styled, "offers": {"@type": "Offer"}}
        _, errors, _ = check.check_page(page(block, title=styled))
        self.assertTrue(any(e.startswith("title has Unicode styled letters") for e in errors))
        self.assertTrue(any(e.startswith("Product: name has Unicode styled letters") for e in errors))

    def test_the_graph_is_opened_up(self):
        block = {"@context": "https://schema.org", "@graph": [PLACE, {"@type": "WebSite", "name": "G",
                                                                         "url": "https://example.com/"}]}
        found, errors, _ = check.check_page(page(block), ["ArtGallery", "WebSite"])
        self.assertEqual(found, ["ArtGallery", "WebSite"])
        self.assertEqual(errors, [])

    def test_breadcrumb_positions(self):
        block = {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/"},
            {"@type": "ListItem", "position": 3, "name": "Here", "item": "https://example.com/a"}]}
        _, errors, _ = check.check_page(page(block))
        self.assertTrue(any("positions are [1, 3]" in e for e in errors))

    def test_an_expected_type_that_is_missing(self):
        _, errors, _ = check.check_page(page(), ["Person"])
        self.assertIn("expected Person, found no structured data", errors)

    def test_head_tags(self):
        _, errors, warnings = check.check_page(page(h1=2, canonical=False, description=False))
        self.assertIn("no canonical address", errors)
        self.assertIn("2 h1 headings, not 1", errors)
        self.assertIn("no description", warnings)


if __name__ == "__main__":
    unittest.main()
