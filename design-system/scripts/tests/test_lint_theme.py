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
        self.write("templates/page.exhibitions.json", template([
            ("head", {"type": "gs-page-head"}),
            ("switch", {"type": "gs-switcher"}),
            ("list", {"type": "gs-exhibition-list"}),
        ]))
        self.write("templates/metaobject/exhibition.json", template([
            ("hero", {"type": "gs-hero"}),
            ("body", {"type": "gs-rich-text"}),
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
            ("text", {"type": "gs-rich-text", "settings": {"surface": "tint"}}),
            ("text2", {"type": "gs-rich-text", "settings": {"surface": "tint"}}),
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
