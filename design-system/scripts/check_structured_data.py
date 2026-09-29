#!/usr/bin/env python3
"""Check the structured data (JSON-LD) and the head tags a page sends to search and answer engines.

Theme Check and lint_theme.py read the theme's files; they can't see what a page prints. This
reads the pages themselves, so it catches:
  - a JSON-LD block that doesn't parse (a stray comma, a quotation mark in a title)
  - a block without the fields its type needs (an exhibition without a start date or a place)
  - a date that isn't a date, an address that isn't a full web address
  - a title or a name in Unicode "italic" letters (U+1D400 to U+1D7FF), which engines can't read
  - a page without a title, a canonical address or exactly one h1
  - a type a page should carry and doesn't (--expect)

Standard library only.
Usage:
  python3 design-system/scripts/check_structured_data.py URL [URL ...] [--expect Type[,Type]] [--json report.json]
  python3 design-system/scripts/check_structured_data.py --file page.html [--expect Type]
Use the theme's preview link (?preview_theme_id=<id>) or the theme dev address.
Exit code 1 on any error.
"""
import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request

# The fields each type must carry. "a|b" means either.
REQUIRED = {
    "ArtGallery": ["name", "url", "address"],
    "WebSite": ["name", "url"],
    "ExhibitionEvent": ["name", "startDate", "location", "url"],
    "Event": ["name", "startDate", "location"],
    "VisualArtwork": ["name", "url"],
    "Person": ["name", "url"],
    "BreadcrumbList": ["itemListElement"],
    "FAQPage": ["mainEntity"],
    "Product": ["name", "offers"],
    "ProductGroup": ["name", "hasVariant|offers"],
}
DATE_FIELDS = ("startDate", "endDate", "birthDate", "deathDate", "dateCreated")
URL_FIELDS = ("url", "image", "item", "mainEntityOfPage")
DATE = re.compile(r"^\d{4}(-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2})?(Z|[+-]\d{2}:?\d{2})?)?)?$")
STYLED = re.compile("[\U0001D400-\U0001D7FF]")
BLOCK = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


def things(node):
    """Every typed object in a block, at any depth, with the @graph opened up."""
    if isinstance(node, list):
        for item in node:
            yield from things(item)
    elif isinstance(node, dict):
        if "@type" in node:
            yield node
        for value in node.values():
            yield from things(value)


def type_names(thing):
    kind = thing.get("@type")
    return kind if isinstance(kind, list) else [kind]


def check_thing(thing, top_level):
    errors = []
    for kind in type_names(thing):
        # A nested mention (a location, a creator, a larger event) may be short.
        if not top_level:
            continue
        for field in REQUIRED.get(kind, []):
            if not any(thing.get(f) not in (None, "", [], {}) for f in field.split("|")):
                errors.append(f"{kind}: no {field.replace('|', ' or ')}")
    label = "/".join(str(k) for k in type_names(thing))
    for field in DATE_FIELDS:
        value = thing.get(field)
        if isinstance(value, str) and not DATE.match(value):
            errors.append(f"{label}: {field} is not a date: {value!r}")
    for field in URL_FIELDS:
        value = thing.get(field)
        if isinstance(value, str) and not re.match(r"^https?://", value):
            errors.append(f"{label}: {field} is not a full web address: {value!r}")
    for field in ("name", "alternateName", "description"):
        value = thing.get(field)
        for text in value if isinstance(value, list) else [value]:
            if isinstance(text, str) and STYLED.search(text):
                errors.append(f"{label}: {field} has Unicode styled letters: {text[:60]!r}")
    if "BreadcrumbList" in type_names(thing):
        items = thing.get("itemListElement") or []
        positions = [i.get("position") for i in items if isinstance(i, dict)]
        if positions != list(range(1, len(items) + 1)):
            errors.append(f"BreadcrumbList: positions are {positions}, not 1 to {len(items)}")
    return errors


def check_page(text, expect=()):
    """Returns (types found, errors, warnings) for one page's HTML."""
    errors, warnings, found = [], [], []
    head = text.split("</head>")[0]

    title = re.search(r"<title>(.*?)</title>", head, re.S)
    title = html.unescape(title.group(1)).strip() if title else ""
    if not title:
        errors.append("no title")
    elif STYLED.search(title):
        errors.append(f"title has Unicode styled letters: {title[:60]!r}")
    if not re.search(r'<link\s+rel="canonical"\s+href="https?://[^"]+"', head):
        errors.append("no canonical address")
    if not re.search(r'<meta\s+name="description"\s+content="[^"]+"', head):
        warnings.append("no description")
    body = re.sub(r"<(script|style|template)\b.*?</\1>", "", text, flags=re.S)
    h1 = len(re.findall(r"<h1\b", body))
    if h1 != 1:
        errors.append(f"{h1} h1 headings, not 1")

    for number, raw in enumerate(BLOCK.findall(text), start=1):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"block {number} doesn't parse: {exc}")
            continue
        top = data.get("@graph", [data]) if isinstance(data, dict) else data
        top_ids = {id(t) for t in top if isinstance(t, dict)}
        for thing in things(data):
            is_top = id(thing) in top_ids
            if is_top:
                found.extend(str(k) for k in type_names(thing))
            errors.extend(check_thing(thing, is_top))

    for kind in expect:
        if kind not in found:
            errors.append(f"expected {kind}, found {', '.join(found) or 'no structured data'}")
    return found, errors, warnings


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (structured data check)"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "replace")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("urls", nargs="*")
    parser.add_argument("--file", action="append", default=[], help="a saved page instead of an address")
    parser.add_argument("--expect", default="", help="types every page must carry, comma-separated")
    parser.add_argument("--json", help="write the report here")
    args = parser.parse_args(argv)
    if not args.urls and not args.file:
        parser.error("give at least one address or --file")
    expect = [t.strip() for t in args.expect.split(",") if t.strip()]

    report, failed = [], False
    for source in args.urls + args.file:
        try:
            if source in args.file:
                with open(source, encoding="utf-8", errors="replace") as handle:
                    text = handle.read()
            else:
                text = fetch(source)
        except (OSError, urllib.error.URLError) as exc:
            print(f"ERROR   {source}: didn't load: {exc}")
            failed = True
            continue
        found, errors, warnings = check_page(text, expect)
        report.append({"page": source, "types": found, "errors": errors, "warnings": warnings})
        print(f"{source}\n        {', '.join(found) or 'no structured data'}")
        for message in errors:
            print(f"ERROR   {message}")
        for message in warnings:
            print(f"WARNING {message}")
        failed = failed or bool(errors)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, ensure_ascii=False)
    total = sum(len(r["errors"]) for r in report)
    print(f"\n{len(report)} page(s), {total} error(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
