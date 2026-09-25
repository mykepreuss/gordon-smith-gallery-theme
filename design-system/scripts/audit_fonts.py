#!/usr/bin/env python3
"""Report which fonts actually draw the text on each page, and flag anything that isn't the brand font.

Computed CSS only says which fonts were *asked for*. This asks the browser which font files it
really used (Chrome DevTools Protocol, CSS.getPlatformFontsForNode), so it catches:
  - a web-font weight that failed to load, so the text fell back to a system font
  - sections or app embeds that set their own font
  - text pasted in with inline fonts
  - characters the brand font doesn't have, e.g. Unicode "italic" letters typed into
    product titles (U+1D400 to U+1D7FF), which also break search and screen readers

Needs Playwright:  pip install playwright && python -m playwright install chromium
Usage:
  python3 design-system/scripts/audit_fonts.py URL [URL ...] [--allow Mulish] [--json report.json]
Exit code 1 if any text renders in a font outside --allow, or if Unicode styled letters are found.
"""
import argparse
import json
import sys

MARK_TEXT_NODES = """
() => {
  const out = [];
  let i = 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  for (let el = walker.currentNode; el; el = walker.nextNode()) {
    if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE'].includes(el.tagName)) continue;
    const own = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
    if (!own) continue;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    if (!r.width || !r.height || cs.visibility === 'hidden' || cs.display === 'none') continue;
    el.setAttribute('data-font-audit', String(i));
    out.push({ i, tag: el.tagName.toLowerCase(), cls: el.className && el.className.baseVal === undefined ? el.className : '',
               text: own.slice(0, 60), styled: /[\\u{1D400}-\\u{1D7FF}]/u.test(own), declared: cs.fontFamily });
    i++;
  }
  return out;
}
"""


def audit(page, url, allow):
    page.goto(url, wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    elements = page.evaluate(MARK_TEXT_NODES)
    cdp = page.context.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    root = cdp.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
    node_ids = cdp.send("DOM.querySelectorAll", {"nodeId": root, "selector": "[data-font-audit]"})["nodeIds"]
    fonts = {}
    for node_id in node_ids:
        attrs = cdp.send("DOM.getAttributes", {"nodeId": node_id})["attributes"]
        idx = int(attrs[attrs.index("data-font-audit") + 1])
        el = elements[idx]
        for f in cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node_id})["fonts"]:
            entry = fonts.setdefault(f["familyName"], {"glyphs": 0, "custom": f.get("isCustomFont", False), "examples": []})
            entry["glyphs"] += f["glyphCount"]
            if len(entry["examples"]) < 3:
                entry["examples"].append(f"<{el['tag']}> {el['text']!r}")
    allowed = [a.lower() for a in allow]
    bad = {name: v for name, v in fonts.items() if not any(name.lower().startswith(a) for a in allowed)}
    styled = [e for e in elements if e["styled"]]
    return {"url": url, "fonts": fonts, "outside_allow": sorted(bad), "styled_unicode": styled}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--allow", action="append", default=None, help="font family allowed (repeatable). Default: Mulish")
    ap.add_argument("--json", help="write the full report here")
    ap.add_argument("--width", type=int, default=1440)
    args = ap.parse_args(argv)
    allow = args.allow or ["Mulish"]
    from playwright.sync_api import sync_playwright

    results, failed = [], False
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": args.width, "height": 900})
        for url in args.urls:
            r = audit(page, url, allow)
            results.append(r)
            print(f"\n{url}")
            for name, v in sorted(r["fonts"].items(), key=lambda kv: -kv[1]["glyphs"]):
                flag = "!!" if name in r["outside_allow"] else "ok"
                kind = "web font" if v["custom"] else "system font"
                print(f"  {flag} {name:32} {v['glyphs']:>7} glyphs  ({kind})  e.g. {v['examples'][0]}")
            for e in r["styled_unicode"]:
                print(f"  !! Unicode styled letters in <{e['tag']}>: {e['text']!r}")
            failed |= bool(r["outside_allow"] or r["styled_unicode"])
        browser.close()
    if args.json:
        with open(args.json, "w") as fh:
            json.dump(results, fh, indent=2)
    print("\nFAIL: text outside the brand font found" if failed else "\nPASS: all text renders in the brand font")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
