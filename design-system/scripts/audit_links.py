#!/usr/bin/env python3
"""Find links that fell back to the browser's own link style, on the rendered page.

Every link in the theme gets its colour and underline from the design system (DESIGN.md §6.2):
inline links, standalone links, quiet list links, buttons. A link that no rule reaches shows the
browser default: blue text (rgb(0, 0, 238)) and a thin underline of automatic thickness. A source
check can't find these reliably (a bare <a> is fine inside .gs-prose, a card or a list), so this
asks the browser for each link's computed style in <main> and the footer.

Flags a visible link whose colour is the default blue, or whose underline has automatic thickness
(the design system always sets it). Links drawn in forced colours are not checked.

Needs Playwright:  pip install playwright && python -m playwright install chromium
Usage:
  python3 design-system/scripts/audit_links.py URL [URL ...] [--width 1440] [--json report.json]
Use the theme's preview link (?preview_theme_id=<id>). Exit code 1 if any link is flagged.
"""
import argparse
import json
import sys

FIND_DEFAULT_LINKS = """
() => {
  const out = [];
  const links = document.querySelectorAll('main a[href], footer a[href], .gs-footer a[href]');
  const seen = new Set();
  for (const a of links) {
    if (seen.has(a)) continue;
    seen.add(a);
    const r = a.getBoundingClientRect();
    const cs = getComputedStyle(a);
    if (!r.width || !r.height || cs.visibility === 'hidden' || cs.display === 'none') continue;
    const blue = cs.color === 'rgb(0, 0, 238)';
    const underlined = cs.textDecorationLine.includes('underline');
    const autoThickness = underlined && cs.textDecorationThickness === 'auto';
    if (blue || autoThickness) {
      out.push({
        text: (a.innerText || a.getAttribute('aria-label') || '').trim().replace(/\\s+/g, ' ').slice(0, 60),
        href: a.getAttribute('href'),
        parent: (a.parentElement.className || a.parentElement.tagName.toLowerCase()).toString().slice(0, 60),
        color: cs.color,
        thickness: cs.textDecorationThickness,
        why: [blue && 'default blue', autoThickness && 'automatic underline thickness'].filter(Boolean).join(', '),
      });
    }
  }
  return out;
}
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--json", help="write the full report here")
    args = ap.parse_args(argv)
    from playwright.sync_api import sync_playwright

    results, failed = [], False
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": args.width, "height": 900})
        for url in args.urls:
            # "load", not "networkidle": a theme preview keeps connections open.
            page.goto(url, wait_until="load", timeout=90000)
            page.wait_for_timeout(1000)
            flagged = page.evaluate(FIND_DEFAULT_LINKS)
            results.append({"url": url, "flagged": flagged})
            print(f"\n{url}")
            if not flagged:
                print("  ok  every link takes the design system's style")
            for f in flagged:
                print(f"  !!  {f['text']!r} -> {f['href']} in .{f['parent']}: {f['why']}")
            failed |= bool(flagged)
        browser.close()
    if args.json:
        with open(args.json, "w") as fh:
            json.dump(results, fh, indent=2)
    print("\nFAIL: links with the browser's default style found" if failed else "\nPASS: no link falls back to the browser's style")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
