#!/usr/bin/env python3
"""Copy the design system's shared files into the theme, or check that the theme's copies match.

design-system/ is the source for the files below; the theme ships copies because Shopify serves
assets only from the theme's own folders (DESIGN.md §0, §9.1). Edit the source, then sync.

  python3 design-system/scripts/sync_theme.py theme/           # copy
  python3 design-system/scripts/sync_theme.py theme/ --check   # exit 1 if a copy differs

Copied
  tokens.css        -> assets/gs-tokens.css
  components.css    -> assets/gs-components.css
  js/*.js           -> assets/<same name>
  logos/*.svg       -> snippets/gs-logo-*.liquid (through build_logo_snippets.py)
  three logos       -> assets/gs-logo-<organisation>.svg (LOGO_FILES, for structured data)
"""
import argparse
import filecmp
import pathlib
import shutil
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_logo_snippets  # noqa: E402


LOGO_FILES = {
    "gs-logo-gallery.svg": "gallery-full-stacked-colour-box.svg",
    "gs-logo-artists-for-kids.svg": "artists-for-kids-full-colour-box.svg",
    "gs-logo-foundation.svg": "foundation-full-colour-box.svg",
}


def pairs(theme):
    yield ROOT / "tokens.css", theme / "assets" / "gs-tokens.css"
    yield ROOT / "components.css", theme / "assets" / "gs-components.css"
    for js in sorted((ROOT / "js").glob("*.js")):
        yield js, theme / "assets" / js.name
    # Each organisation's logo as a file, for its structured data (DS-163): search engines want
    # a logo's address, and the page's own logos are drawn inline.
    for name, logo in LOGO_FILES.items():
        yield ROOT / "logos" / logo, theme / "assets" / name


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("theme", type=pathlib.Path)
    ap.add_argument("--check", action="store_true", help="report copies that differ instead of copying")
    args = ap.parse_args(argv)

    stale = []
    for src, dst in pairs(args.theme):
        if args.check:
            if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
                stale.append(dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            print(dst)

    with tempfile.TemporaryDirectory() as tmp:
        built = build_logo_snippets.build(pathlib.Path(tmp))
        for path in built:
            dst = args.theme / "snippets" / path.name
            if args.check:
                if not dst.exists() or not filecmp.cmp(path, dst, shallow=False):
                    stale.append(dst)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, dst)
                print(dst)

    if args.check:
        for path in stale:
            print(f"out of date: {path} (run design-system/scripts/sync_theme.py without --check)")
        print("theme copies match design-system/" if not stale else f"{len(stale)} file(s) out of date")
        return 1 if stale else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
