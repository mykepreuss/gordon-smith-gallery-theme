#!/usr/bin/env python3
"""Build the site's icons from the Gallery's simple stacked colour box logo (DS-189).

  python3 design-system/scripts/build_favicon.py           # write the three files
  python3 design-system/scripts/build_favicon.py --check   # exit 1 if the SVG differs

Written to design-system/logos/favicon/, then copied into the theme by sync_theme.py:

  gallery-favicon.svg           -> assets/gs-favicon.svg           browser tabs, bookmarks, search
  gallery-favicon-32.png        -> assets/gs-favicon-32.png        browsers without SVG icons
  gallery-apple-touch-icon.png  -> assets/gs-apple-touch-icon.png  home screens (iOS, Android)

The logo is drawn as supplied: not redrawn, recoloured or cropped (DESIGN.md §8.3). The SVG is the
logo on a square canvas, the box full width and centred, since browsers draw an icon square and
would otherwise shrink it to fit. It leaves out the content credentials and rounds the drawing to
a tenth of a unit, as the logo snippets do: 16.5 KB becomes about 4 KB.

The PNGs are drawn from that SVG by Google Chrome (headless), so they are only rewritten when the
script runs without --check. The home screen icon is the logo on white with a margin: iOS fills a
transparent icon with black and rounds all four corners, which would cut into the box.
"""
import argparse
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build_logo_snippets import round_paths  # noqa: E402

SOURCE = ROOT / "logos" / "gallery-simple-stacked-colour-box.svg"
OUT = ROOT / "logos" / "favicon"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TOUCH_SIZE, TOUCH_MARGIN = 180, 18  # a tenth each side: inside iOS's rounded mask
PAPER = "#ffffff"  # --gs-paper


def square_svg():
    svg = SOURCE.read_text()
    svg = re.sub(r"<metadata>.*?</metadata>\s*", "", svg, flags=re.S)
    svg = re.sub(r'\sxmlns:c2pa="[^"]*"', "", svg)
    svg = re.sub(r"<title>.*?</title>\s*", "", svg, flags=re.S)
    svg = re.sub(r'\srole="img" aria-label="[^"]*"', "", svg)
    svg = re.sub(r'\sfill-rule="nonzero"', "", svg)  # the default
    # The box is the first path, in the box colour; its bounds set the square.
    box = re.search(r'<path fill="#89a6ab" d="([^"]*)"', svg)
    if not box or svg.index("<path") != box.start():
        raise SystemExit("the logo's box is not the first path: check the source file")
    nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", box.group(1))]
    left, right = min(nums[0::2]), max(nums[0::2])
    top, bottom = min(nums[1::2]), max(nums[1::2])
    side = right - left
    if side < bottom - top:
        raise SystemExit("the logo's box is taller than wide: the square would crop it")
    pad = (side - (bottom - top)) / 2
    view = f"{left:g} {round(top - pad, 2):g} {round(side, 2):g} {round(side, 2):g}"
    svg = re.sub(r'\swidth="[^"]*" height="[^"]*" viewBox="[^"]*"', f' viewBox="{view}"', svg, count=1)
    # Black paths share one group's fill. They stay separate paths: joined, a letter's parts
    # drawn in opposite directions would cut holes where they overlap.
    svg = svg.replace(' fill="#000000"', "")
    first_black = svg.index("<path d=")
    svg = svg[:first_black] + "<g>" + svg[first_black:].replace("</svg>", "</g></svg>")
    svg = round_paths(svg)
    svg = re.sub(r">\s+<", "><", svg).strip()
    if "c2pa" in svg or "<g>" not in svg:
        raise SystemExit("unexpected SVG after optimising")
    return svg + "\n"


def render(svg_path, png_path, size, background=None, margin=0):
    """One PNG, size x size device pixels, from Chrome."""
    inner = size - 2 * margin
    bg = background or "transparent"
    html = (
        f'<html><body style="margin:0;background:{bg}">'
        f'<img src="{svg_path.as_uri()}" width="{inner}" height="{inner}" '
        f'style="display:block;margin:{margin}px"></body></html>'
    )
    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp) / "icon.html"
        page.write_text(html)
        shot = pathlib.Path(tmp) / "shot.png"
        subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
             "--default-background-color=00000000", f"--window-size={size},{size}",
             f"--screenshot={shot}", page.as_uri()],
            check=True, capture_output=True,
        )
        from PIL import Image
        im = Image.open(shot).convert("RGBA" if background is None else "RGB")
        im = im.crop((0, 0, size, size))
        if im.size != (size, size):
            raise SystemExit(f"{png_path.name}: Chrome drew {im.size}, expected {size}")
        im.save(png_path, optimize=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="report whether the SVG is out of date")
    args = ap.parse_args(argv)

    svg = square_svg()
    target = OUT / "gallery-favicon.svg"
    if args.check:
        ok = target.exists() and target.read_text() == svg
        print("favicon matches its source" if ok else f"out of date: {target} (run build_favicon.py)")
        return 0 if ok else 1

    OUT.mkdir(parents=True, exist_ok=True)
    target.write_text(svg)
    print(target, f"{len(svg.encode())} bytes")
    render(target, OUT / "gallery-favicon-32.png", 32)
    render(target, OUT / "gallery-apple-touch-icon.png", TOUCH_SIZE, PAPER, TOUCH_MARGIN)
    for name in ("gallery-favicon-32.png", "gallery-apple-touch-icon.png"):
        print(OUT / name, f"{(OUT / name).stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
