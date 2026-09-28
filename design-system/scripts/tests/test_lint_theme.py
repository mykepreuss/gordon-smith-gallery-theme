#!/usr/bin/env python3
"""Tests for lint_theme.py against a small synthetic theme.

  python3 design-system/scripts/tests/test_lint_theme.py
"""
import contextlib
import io
import json
import pathlib
import sys
import tempfile
import textwrap
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import lint_theme  # noqa: E402

BANNER = "/*\n * IMPORTANT: The contents of this file are auto-generated.\n */\n"


def section(name, settings):
    schema = json.dumps({"name": name, "settings": settings})
    return f"<div>{name}</div>\n{{% schema %}}\n{schema}\n{{% endschema %}}\n"


def template(sections):
    body = {"sections": {sid: spec for sid, spec in sections}, "order": [sid for sid, _ in sections]}
    return BANNER + json.dumps(body, indent=2)


class LintTheme(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.theme = pathlib.Path(self.tmp.name)
        for d in ("templates", "sections", "assets", "snippets", "templates/metaobject"):
            (self.theme / d).mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        (self.theme / rel).write_text(text)

    def run_lint(self, *extra):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = lint_theme.main([str(self.theme), *extra])
        return code, out.getvalue()

    def test_clean_theme_passes(self):
        self.write("sections/gs-hero.liquid", section("Hero", [
            {"type": "image_picker", "id": "image", "label": "Image"},
            {"type": "text", "id": "heading", "label": "Heading"},
            {"type": "select", "id": "surface", "label": "Surface", "options": [{"value": "paper", "label": "Paper"}]},
        ]))
        self.write("templates/page.json", template([
            ("head", {"type": "gs-page-hero"}),
            ("switch", {"type": "gs-switcher"}),
            ("list", {"type": "gs-exhibition-list"}),
        ]))
        self.write("templates/metaobject/exhibition.json", template([
            ("hero", {"type": "gs-hero"}),
            ("body", {"type": "gs-exhibition-body"}),
            ("views", {"type": "gs-gallery", "settings": {"surface": "tint"}}),
            ("works", {"type": "gs-gallery", "settings": {"surface": "paper"}}),
        ]))
        self.write("assets/gs-components.css", ".x { color: var(--gs-color-fg); }\n")
        code, out = self.run_lint("--strict")
        self.assertEqual(code, 0, out)

    def test_one_off_template_is_rejected(self):
        self.write("templates/page.exhibition-ftg.json", template([("hero", {"type": "gs-hero"})]))
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("page.exhibition-ftg.json: not an approved template", out)

    def test_overloaded_shop_landing(self):
        self.write("templates/page.shop.json", template([
            ("banner", {"type": "image-banner"}),
            ("portfolios", {"type": "collection-list"}),
            ("more", {"type": "featured-collection"}),
            ("old", {"type": "rich-text", "disabled": True}),
        ]))
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("2 listing sections; at most 1 allowed", out)
        self.assertIn("disabled section 'old'", out)

    def test_order_and_repeated_tint(self):
        self.write("templates/page.json", template([
            ("text", {"type": "gs-page-body", "settings": {"surface": "tint"}}),
            ("text2", {"type": "gs-page-body", "settings": {"surface": "tint"}}),
        ]))
        code, out = self.run_lint()
        self.assertIn("must start with hero or pageHead", out)
        self.assertIn("two tint sections in a row", out)

    def test_locked_settings(self):
        self.write("sections/image-banner.liquid", section("Banner", [
            {"type": "range", "id": "padding_top", "min": 0, "max": 100, "step": 4, "default": 36, "label": "Top padding"},
            {"type": "color_scheme", "id": "color_scheme", "label": "Colour scheme", "default": "scheme-1"},
        ]))
        self.write("sections/gs-feature.liquid", section("Feature", [
            {"type": "select", "id": "heading_size", "label": "Heading size", "options": [{"value": "h2", "label": "H2"}]},
        ]))
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("WARNING sections/image-banner.liquid: design control for staff: range 'padding_top'", out)
        self.assertIn("type 'color_scheme'", out)
        self.assertIn("ERROR   sections/gs-feature.liquid: design control for staff: select 'heading_size'", out)

    def test_raw_values_in_gs_code(self):
        self.write("assets/gs-components.css", ".x { color: #89a6ab; font-size: 14px; }\n.y { color: #fff; } /* gs-lint-ignore */\n")
        self.write("assets/gs-tokens.css", ":root { --gs-ink: #231f20; }\n")
        code, out = self.run_lint()
        self.assertIn("assets/gs-components.css:1: raw colour", out)
        self.assertIn("assets/gs-components.css:1: px font size", out)
        self.assertNotIn("gs-components.css:2", out)
        self.assertNotIn("gs-tokens.css", out)

    def test_gs_media_needs_a_preset(self):
        self.write("sections/gs-card-grid.liquid",
                   "{%- render 'gs-media', image: card.image, mode: 'photo' -%}\n"
                   "{%- render 'gs-media',\n    image: card.image,\n    preset: 'card'\n-%}\n"
                   "{%- liquid\n  render 'gs-media', image: x, sizes: '50vw'\n  render 'gs-media', image: y\n-%}\n")
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("sections/gs-card-grid.liquid:1: render 'gs-media' without preset or sizes", out)
        self.assertIn("sections/gs-card-grid.liquid:8: render 'gs-media' without preset or sizes", out)
        self.assertNotIn("gs-card-grid.liquid:2:", out)
        self.assertNotIn("gs-card-grid.liquid:7:", out)


    def test_raw_palette_value(self):
        self.write("assets/gs-components.css",
                   ".a { color: var(--gs-ink); }\n.b { background: var(--gs-afk-rule); }\n"
                   ".c { color: var(--gs-color-fg); border-color: var(--gs-ink-soft, red); }\n"
                   ".d { color: var(--gs-color-field-fg); }\n")
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        for line in (1, 2, 3):
            self.assertIn(f"gs-components.css:{line}: raw palette value", out)
        self.assertNotIn("gs-components.css:4", out)

    def test_raw_duration(self):
        self.write("assets/gs-components.css",
                   ".a { transition: color 120ms ease; }\n.b { animation: fade .2s; }\n"
                   ".c { transition: color var(--gs-duration-fast) var(--gs-ease); }\n")
        code, out = self.run_lint()
        self.assertIn("gs-components.css:1: raw duration", out)
        self.assertIn("gs-components.css:2: raw duration", out)
        self.assertNotIn("gs-components.css:3", out)

    def test_transition_all(self):
        self.write("assets/gs-components.css",
                   ".a { transition: all var(--gs-duration-fast); }\n.b { transition-property: all; }\n"
                   ".c { transition-property: color, background-color; }\n")
        code, out = self.run_lint()
        self.assertIn("gs-components.css:1: transition on all", out)
        self.assertIn("gs-components.css:2: transition on all", out)
        self.assertNotIn("gs-components.css:3", out)

    def test_raw_ratio(self):
        self.write("snippets/gs-thing.liquid",
                   "{%- render 'gs-media', image: i, preset: 'card', ratio: '4 / 3' -%}\n"
                   "{%- render 'gs-media', image: i, preset: 'card', ratio: 'var(--gs-ratio-card)' -%}\n"
                   "{% doc %}\n  {% render 'gs-media', image: i, preset: 'card', ratio: '1' %}\n{% enddoc %}\n")
        code, out = self.run_lint()
        self.assertIn("snippets/gs-thing.liquid:1: raw ratio", out)
        self.assertNotIn("gs-thing.liquid:2", out)
        self.assertNotIn("gs-thing.liquid:4", out)

    def test_brace_in_output_tag(self):
        self.write("snippets/gs-thing.liquid",
                   "<p data-text=\"{{ 'count' | t: number: '{n}' }}\"></p>\n"
                   "<p data-text=\"{{ 'count' | t: number: '[n]' }}\">{{ a }}{{ b }}</p>\n")
        code, out = self.run_lint()
        self.assertIn("snippets/gs-thing.liquid:1: a closing brace inside", out)
        self.assertNotIn("gs-thing.liquid:2", out)

    def test_unitless_line_height(self):
        self.write("assets/gs-components.css",
                   ".a { line-height: 1.4; }\n.b { line-height: 0; }\n.c { line-height: 1; }\n"
                   ".d { line-height: var(--gs-leading-body); }\n.e { font: 700 1rem / 1.4 sans-serif; }\n"
                   ".f { font: 700 var(--gs-text-small) / var(--gs-leading-small) sans-serif; }\n"
                   "/* line-height: 1.6 in a comment */\n.g { line-height: 1.25 }\n")
        code, out = self.run_lint()
        self.assertIn("gs-components.css:1: unitless line height;", out)
        self.assertIn("gs-components.css:5: unitless line height in font shorthand", out)
        self.assertIn("gs-components.css:8: unitless line height;", out)
        for line in (2, 3, 4, 6, 7):
            self.assertNotIn(f"gs-components.css:{line}:", out)

    def test_nested_has(self):
        self.write("assets/gs-components.css",
                   ".a:has(> li:has(.x)) { color: var(--gs-color-fg); }\n"
                   ".b:has(> li:not(.y)) { color: var(--gs-color-fg); }\n"
                   ".c:has(.x), .d:has(.y) { color: var(--gs-color-fg); }\n")
        code, out = self.run_lint()
        self.assertIn("gs-components.css:1: a :has() inside a :has()", out)
        self.assertNotIn("gs-components.css:2", out)
        self.assertNotIn("gs-components.css:3", out)

    def test_hover_outside_media(self):
        self.write("assets/gs-components.css",
                   ".a:hover { color: var(--gs-color-fg); }\n"
                   "@media (hover: hover) and (pointer: fine) {\n"
                   "  .b:hover { color: var(--gs-color-fg); }\n"
                   "  @supports (display: grid) { .c:hover { color: var(--gs-color-fg); } }\n"
                   "}\n"
                   "@media (min-width: 750px) {\n"
                   "  .d,\n  .e:hover { color: var(--gs-color-fg); }\n"
                   "}\n"
                   "/* .f:hover { } */\n"
                   ".g:active { color: var(--gs-color-fg); }\n")
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("gs-components.css:1: :hover outside", out)
        self.assertIn("gs-components.css:7: :hover outside", out)
        for line in (3, 4, 10, 11):
            self.assertNotIn(f"gs-components.css:{line}:", out)

    def test_list_without_role(self):
        self.write("sections/gs-list.liquid",
                   '<ul class="gs-grid gs-grid--cards">\n'
                   '<ul class="gs-grid{{ mods }}" role="list">\n'
                   '<ul class="gs-events" role="list">\n'
                   '<ul class="gs-events">\n'
                   '<ul class="gs-names">\n')
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)
        self.assertIn("WARNING sections/gs-list.liquid:1: a grid or event list without role", out)
        self.assertIn("WARNING sections/gs-list.liquid:4:", out)
        for line in (2, 3, 5):
            self.assertNotIn(f"gs-list.liquid:{line}:", out)
        code, out = self.run_lint("--strict")
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
