#!/usr/bin/env python3
"""Tests for check_links.py against small synthetic pages.

  python3 design-system/scripts/tests/test_check_links.py
"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check_links as check  # noqa: E402

BASE = "https://example.test"
HOSTS = {"example.test", "gallery.test"}
SPEC = {"max_depth": 3, "min_content_links": 2, "entries": ["pages/exhibitions"], "unlinked": []}


def html(content, menu="", footer="", robots=""):
    meta = f'<meta name="robots" content="{robots}">' if robots else ""
    return (
        f"<html><head><title>T</title>{meta}</head><body>"
        f'<div id="shopify-section-sections--1__header"><header><nav>{menu}</nav></header></div>'
        f'<main><div id="shopify-section-template--2__main">{content}</div></main>'
        f'<div id="shopify-section-sections--3__footer"><footer>{footer}</footer></div>'
        "</body></html>"
    )


def site(pages):
    """Pages as the crawl records them, from {address: html}."""
    out = {}
    for address, body in pages.items():
        record = {"status": 200, "links": [], "listed": True}
        if isinstance(body, int):
            record["status"] = body
        else:
            record.update(check.read_page(address, body, BASE, HOSTS))
        out[address] = record
    return out


def rules(found):
    return sorted((rule, address) for rule, address, _ in found)


class Addresses(unittest.TestCase):
    def test_a_store_address_typed_in_full_is_the_same_page(self):
        self.assertEqual(check.normalise("https://gallery.test/pages/visit/", BASE + "/", HOSTS), ("internal", "/pages/visit"))

    def test_a_relative_address_is_read_from_the_page_it_is_on(self):
        self.assertEqual(check.normalise("?page=2", BASE + "/pages/browse/prints", HOSTS), ("internal", "/pages/browse/prints?page=2"))

    def test_the_preview_and_tracking_words_are_dropped(self):
        self.assertEqual(check.normalise("/products/a?_pos=1&_sid=x&variant=3", BASE + "/", HOSTS), ("internal", "/products/a"))

    def test_another_site_mail_and_anchors(self):
        self.assertEqual(check.normalise("https://other.test/a", BASE + "/", HOSTS)[0], "external")
        self.assertEqual(check.normalise("mailto:a@example.test", BASE + "/", HOSTS)[0], "other")
        self.assertEqual(check.normalise("#main", BASE + "/", HOSTS)[0], "other")

    def test_what_is_a_page(self):
        self.assertTrue(check.is_page("/pages/visit"))
        self.assertTrue(check.is_page("/search"))
        self.assertFalse(check.is_page("/search?q=smith"))
        self.assertFalse(check.is_page("/cart"))
        self.assertFalse(check.is_page("/cdn/shop/files/guide.pdf"))

    def test_kinds(self):
        self.assertEqual(check.kind("/"), "home")
        self.assertEqual(check.kind("/pages/visit"), "pages")
        self.assertEqual(check.kind("/pages/artists/gordon-smith"), "pages/artists")
        self.assertEqual(check.kind("/products/a?x=1"), "products")


class Reading(unittest.TestCase):
    def test_a_link_knows_its_place(self):
        page = check.read_page("/", html('<a href="/a">A</a>', '<a href="/b">B</a>', '<a href="/c">C</a>'), BASE, HOSTS)
        self.assertEqual({l["to"]: l["place"] for l in page["links"]}, {"/a": "content", "/b": "menu", "/c": "footer"})

    def test_a_page_header_inside_main_is_content(self):
        page = check.read_page("/", html('<header class="gs-page-head"><a href="/back">Back</a></header>'), BASE, HOSTS)
        self.assertEqual(page["links"][0]["place"], "content")

    def test_without_sections_the_landmarks_say(self):
        body = '<header><a href="/b">B</a></header><main><a href="/a">A</a></main><footer><a href="/c">C</a></footer>'
        page = check.read_page("/", body, BASE, HOSTS)
        self.assertEqual([l["place"] for l in page["links"]], ["menu", "content", "footer"])

    def test_words_from_text_label_or_alt(self):
        body = html(
            '<a href="/a"> Plan  your\nvisit </a>'
            '<a href="/b" aria-label="Home"><svg></svg></a>'
            '<a href="/c"><img src="x.jpg" alt="Pender Harbour"></a>'
            '<a href="/d"><img src="x.jpg" alt=""></a>'
        )
        page = check.read_page("/", body, BASE, HOSTS)
        self.assertEqual([l["words"] for l in page["links"]], ["Plan your visit", "Home", "Pender Harbour", ""])

    def test_hidden_words_count(self):
        body = html('<a href="/a">Register<span class="gs-visually-hidden">: Curatorial Tour</span></a>')
        self.assertEqual(check.read_page("/", body, BASE, HOSTS)["links"][0]["words"], "Register: Curatorial Tour")

    def test_a_page_that_asks_not_to_be_listed(self):
        self.assertFalse(check.read_page("/", html("", robots="noindex"), BASE, HOSTS)["listed"])
        self.assertTrue(check.read_page("/", html("", robots="max-image-preview:large"), BASE, HOSTS)["listed"])


class Rules(unittest.TestCase):
    def test_a_sound_site(self):
        pages = site({
            "/": html('<a href="/pages/a">A</a><a href="/pages/b">B</a>'),
            "/pages/a": html('<a href="/pages/b">B</a><a href="/">Home</a>'),
            "/pages/b": html('<a href="/pages/a">A</a>'),
        })
        errors, notes = check.findings(pages, {"/", "/pages/a", "/pages/b"}, SPEC)
        self.assertEqual((errors, notes), ([], []))

    def test_a_link_to_a_page_that_fails(self):
        pages = site({"/": html('<a href="/pages/gone">Gone</a>'), "/pages/gone": 404})
        errors, _ = check.findings(pages, set(), SPEC)
        self.assertEqual(rules(errors), [("answers", "/pages/gone")])

    def test_a_link_without_words(self):
        pages = site({"/": html('<a href="/pages/a"><img src="x.jpg" alt=""></a>'), "/pages/a": html("")})
        errors, _ = check.findings(pages, set(), SPEC)
        self.assertEqual(rules(errors), [("words", "/")])

    def test_a_liquid_error(self):
        pages = site({"/": html("<p>Liquid error (sections/x line 3): nope</p>")})
        errors, _ = check.findings(pages, set(), SPEC)
        self.assertEqual(rules(errors), [("liquid", "/")])

    def test_too_many_clicks(self):
        chain = {"/": html('<a href="/pages/1">1</a>')}
        for n in range(1, 5):
            chain[f"/pages/{n}"] = html(f'<a href="/pages/{n + 1}">next</a>')
        chain["/pages/5"] = html("")
        errors, _ = check.findings(site(chain), set(), SPEC)
        self.assertEqual(rules(errors), [("depth", "/pages/4"), ("depth", "/pages/5")])

    def test_a_far_page_that_is_not_listed_is_left_alone(self):
        chain = {"/": html('<a href="/pages/1">1</a>')}
        for n in range(1, 4):
            chain[f"/pages/{n}"] = html(f'<a href="/pages/{n + 1}">next</a>')
        chain["/pages/4"] = html("", robots="noindex")
        errors, _ = check.findings(site(chain), set(), SPEC)
        self.assertEqual(errors, [])

    def test_a_sitemap_address_nobody_links_to(self):
        pages = site({"/": html(""), "/pages/alone": html("")})
        pages["/pages/alone"]["unlinked"] = True
        errors, _ = check.findings(pages, {"/", "/pages/alone"}, SPEC)
        self.assertEqual(rules(errors), [("unlinked", "/pages/alone")])

    def test_an_unlinked_page_that_asks_not_to_be_listed_is_fine(self):
        pages = site({"/": html(""), "/products/a-frame": html("", robots="noindex")})
        pages["/products/a-frame"]["unlinked"] = True
        errors, notes = check.findings(pages, {"/", "/products/a-frame"}, SPEC)
        self.assertEqual((errors, notes), ([], []))

    def test_an_unlinked_page_known_until_release_is_a_note(self):
        spec = dict(SPEC, unlinked=[{"address": "/pages/about", "why": "hidden at release"}])
        pages = site({"/": html(""), "/pages/about": html("")})
        pages["/pages/about"]["unlinked"] = True
        errors, notes = check.findings(pages, {"/", "/pages/about"}, spec)
        self.assertEqual(errors, [])
        self.assertEqual(rules(notes), [("unlinked", "/pages/about")])

    def test_an_unlinked_page_links_count_for_nothing(self):
        pages = site({"/": html(""), "/pages/alone": html('<a href="/pages/other">Other</a>'), "/pages/other": html("")})
        pages["/pages/alone"]["unlinked"] = True
        pages["/pages/other"]["unlinked"] = True
        errors, _ = check.findings(pages, {"/pages/alone", "/pages/other"}, SPEC)
        self.assertEqual(rules(errors), [("unlinked", "/pages/alone"), ("unlinked", "/pages/other")])

    def test_an_entry_linked_from_the_menu_only(self):
        pages = site({
            "/": html("", menu='<a href="/pages/exhibitions/a">A</a>'),
            "/pages/exhibitions/a": html(""),
        })
        errors, notes = check.findings(pages, set(), SPEC)
        self.assertEqual(rules(errors), [("content", "/pages/exhibitions/a")])
        self.assertEqual(rules(notes), [("few", "pages/exhibitions")])

    def test_a_page_with_one_link_in_is_a_note(self):
        pages = site({"/": html('<a href="/pages/a">A</a>'), "/pages/a": html("")})
        errors, notes = check.findings(pages, set(), SPEC)
        self.assertEqual(errors, [])
        self.assertEqual(rules(notes), [("few", "pages")])

    def test_a_link_to_itself_does_not_count(self):
        pages = site({
            "/": html('<a href="/pages/exhibitions/a">A</a>'),
            "/pages/exhibitions/a": html('<a href="/pages/exhibitions/a">A</a>'),
        })
        _, notes = check.findings(pages, set(), SPEC)
        self.assertEqual(rules(notes), [("few", "pages/exhibitions")])

    def test_a_link_that_is_sent_on_is_a_note(self):
        pages = site({"/": html('<a href="/pages/old">Old</a><a href="/pages/new">New</a>'), "/pages/old": html(""), "/pages/new": html('<a href="/pages/old">Old</a>')})
        pages["/pages/old"]["moved"] = "/pages/new"
        errors, notes = check.findings(pages, set(), SPEC)
        self.assertEqual(errors, [])
        self.assertIn(("moved", "/pages/old"), rules(notes))


class Clicks(unittest.TestCase):
    def test_the_shortest_way(self):
        out = {"/": {"/a", "/b"}, "/a": {"/c"}, "/b": {"/c", "/d"}, "/d": {"/"}}
        self.assertEqual(check.depths(out), {"/": 0, "/a": 1, "/b": 1, "/c": 2, "/d": 2})


class Settings(unittest.TestCase):
    def test_links_json_is_whole(self):
        import json
        spec = json.loads(check.SPEC.read_text())
        for key in ("sitemap", "hosts", "max_depth", "min_content_links", "entries", "unlinked"):
            self.assertIn(key, spec)
        for row in spec["unlinked"]:
            self.assertTrue(row["address"].startswith("/"))
            self.assertTrue(row["why"])


if __name__ == "__main__":
    unittest.main()
