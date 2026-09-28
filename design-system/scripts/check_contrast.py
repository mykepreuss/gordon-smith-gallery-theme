#!/usr/bin/env python3
"""Check every allowed text/background pairing in the design system against WCAG 2.2.

Reads raw colour values from design-system/tokens.css, so a palette edit is re-checked
automatically. Pairings mirror DESIGN.md §3 (surfaces x programmes). Standard library only.

  python3 design-system/scripts/check_contrast.py            # table + exit 1 on any failure
  python3 design-system/scripts/check_contrast.py --markdown # same table as Markdown for DESIGN.md
"""
import pathlib
import re
import sys

TOKENS = pathlib.Path(__file__).resolve().parent.parent / "tokens.css"

AA_TEXT = 4.5   # normal text
AA_LARGE = 3.0  # >= 24px regular or >= 18.66px bold; also UI boundaries / focus (1.4.11)

# (context, role, fg token, bg token, minimum)
REQUIRED = []
PROGRAMMES = {
    "Gallery": {"box": "gsg-box", "tint": "gsg-tint", "rule": "gsg-rule", "accent_text": "gsg-text", "link": "gsg-text"},
    "Foundation": {"box": "gsf-box", "tint": "gsf-tint", "rule": "gsf-rule", "accent_text": "ink", "link": "ink"},
    "Artists for Kids": {"box": "afk-box", "tint": "afk-tint", "rule": "afk-rule", "accent_text": "ink", "link": "ink"},
}
for name, p in PROGRAMMES.items():
    REQUIRED += [
        (f"{name} · paper", "body text", "ink", "paper", AA_TEXT),
        (f"{name} · paper", "muted text", "ink-soft", "paper", AA_TEXT),
        (f"{name} · paper", "eyebrow / accent text", p["accent_text"], "paper", AA_TEXT),
        (f"{name} · paper", "inline-link underline", p["link"], "paper", AA_LARGE),
        (f"{name} · paper", "input / secondary-button border", "ink-soft", "paper", AA_LARGE),
        (f"{name} · paper", "primary button", "ink", p["box"], AA_TEXT),
        (f"{name} · paper", "link hover fill (tint)", "ink", p["tint"], AA_TEXT),
        (f"{name} · paper", "switcher current bar, link underline", p["link"], "paper", AA_LARGE),
        (f"{name} · paper", "error text", "error", "paper", AA_TEXT),
        (f"{name} · paper", "button hover (inverted)", "paper", "ink", AA_TEXT),
        (f"{name} · tint", "body text", "ink", p["tint"], AA_TEXT),
        (f"{name} · tint", "muted text", "ink-soft", p["tint"], AA_TEXT),
        (f"{name} · tint", "inline-link underline", p["link"], p["tint"], AA_LARGE),
        (f"{name} · tint", "primary button (ink fill, DS-31)", "paper", "ink", AA_TEXT),
        (f"{name} · tint", "primary button edge against the band", "ink", p["tint"], AA_LARGE),
        (f"{name} · tint", "button hover (paper fill)", "ink", "paper", AA_TEXT),
        (f"{name} · tint", "link hover fill (rule)", "ink", p["rule"], AA_TEXT),
        (f"{name} · tint", "error text", "error", p["tint"], AA_TEXT),
        (f"{name} · accent box", "text, focus ring", "ink", p["box"], AA_TEXT),
        (f"{name} · accent box", "button (ink fill)", "paper", "ink", AA_TEXT),
        (f"{name} · accent box", "strong chip (ink, paper text, DS-128)", "paper", "ink", AA_TEXT),
        (f"{name} · ink", "body text", "paper", "ink", AA_TEXT),
        (f"{name} · ink", "muted text", "ink-faint", "ink", AA_TEXT),
        (f"{name} · ink", "eyebrow / accent text, link underline", p["box"], "ink", AA_TEXT),
        (f"{name} · ink", "primary button", "ink", p["box"], AA_TEXT),
        (f"{name} · ink", "link hover fill (box)", "ink", p["box"], AA_TEXT),
        (f"{name} · ink", "error text", "error-light", "ink", AA_TEXT),
    ]
REQUIRED += [
    ("Gallery · paper", "accent heading (h3+ only)", "gsg-text", "paper", AA_LARGE),
    ("Gallery · tint", "accent heading (h3+ only)", "gsg-text", "gsg-tint", AA_LARGE),
    ("any · mat", "placeholder / muted text near artwork", "ink-soft", "mat", AA_TEXT),
    ("any · input", "invalid-field border on the white input", "error", "paper", AA_LARGE),
]

# Pairs the system forbids. Listed so the reason is visible; they are expected to fail AA text.
FORBIDDEN = [
    ("Gallery box colour as text on paper", "gsg-box", "paper"),
    ("Gallery teal as small text on its tint", "gsg-text", "gsg-tint"),
    ("White text on Gallery box", "paper", "gsg-box"),
    ("Foundation green as text on paper", "gsf-text", "paper"),
    ("Artists for Kids orange as text on paper", "afk-swoosh", "paper"),
    ("White text on Artists for Kids orange", "paper", "afk-swoosh"),
    ("Gallery teal as text on ink", "gsg-text", "ink"),
    ("Error red as text on the Gallery box (accent surfaces use ink)", "error", "gsg-box"),
    ("Error red as text on ink (ink surfaces use the light error)", "error", "ink"),
]


def load_palette(path):
    css = path.read_text()
    root = css[css.index(":root"):css.index("}", css.index(":root"))]
    return {m.group(1): m.group(2).lower() for m in re.finditer(r"--gs-([a-z0-9-]+):\s*(#[0-9a-fA-F]{6})\b", root)}


def luminance(hex_):
    rgb = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main():
    md = "--markdown" in sys.argv
    pal = load_palette(TOKENS)
    failures = 0
    rows = []
    for ctx, role, fg, bg, need in REQUIRED:
        r = ratio(pal[fg], pal[bg])
        ok = r >= need
        failures += not ok
        rows.append((ctx, role, f"{fg} {pal[fg]}", f"{bg} {pal[bg]}", f"{r:.2f}", f"{need:g}", "pass" if ok else "FAIL"))
    if md:
        print("| Context | Use | Foreground | Background | Ratio | Needs | Result |")
        print("| --- | --- | --- | --- | --- | --- | --- |")
        for row in rows:
            print("| " + " | ".join(f"`{c}`" if i in (2, 3) else c for i, c in enumerate(row)) + " |")
        print()
        print("| Forbidden pairing | Foreground | Background | Ratio |")
        print("| --- | --- | --- | --- |")
        for label, fg, bg in FORBIDDEN:
            print(f"| {label} | `{pal[fg]}` | `{pal[bg]}` | {ratio(pal[fg], pal[bg]):.2f} |")
    else:
        w = max(len(r[0]) for r in rows)
        for row in rows:
            print(f"{row[6]:4}  {row[4]:>5} (≥{row[5]:>3})  {row[0]:<{w}}  {row[1]}  [{row[2]} on {row[3]}]")
        print(f"\n{len(rows) - failures}/{len(rows)} required pairings pass.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
