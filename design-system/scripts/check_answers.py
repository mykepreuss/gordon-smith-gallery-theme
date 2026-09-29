#!/usr/bin/env python3
"""Check that the site still answers the questions people ask answer engines.

check_structured_data.py checks that a page's data is sound. This checks that the facts are
there at all: for each question in answers.json it reads the page meant to answer it and looks
for the evidence in the words a visitor sees, and for the structured data the page should carry.
It also checks that /llms.txt answers and that every page it names answers.

A question marked "gap" is one the site doesn't answer yet (a question for the gallery). It is
reported, never an error, and the report says when a gap has closed so answers.json can be
updated.

Standard library only.
Usage:
  python3 design-system/scripts/check_answers.py BASE [--json report.json] [--only N[,N]]
BASE is the theme dev address or a preview address, without a path, for example
http://127.0.0.1:9292 . Exit code 1 when a question that should be answered isn't.
"""
import argparse
import html
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

QUESTIONS = pathlib.Path(__file__).resolve().parent / "answers.json"
BLOCK = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S)
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (answers check)"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", "replace")


def visible_text(page):
    """The words a visitor sees, with the description, which engines read as the page's summary."""
    body = re.sub(r"<(script|style|template|svg)\b.*?</\1>", " ", page, flags=re.S)
    body = body.split("</head>", 1)[-1]
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    found = re.search(r'<meta\s+name="description"\s+content="(.*?)"', page, re.S)
    if found:
        text += " " + html.unescape(found.group(1))
    return re.sub(r"\s+", " ", text.replace(" ", " "))


def data_types(page):
    types = []

    def walk(node):
        if isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            kind = node.get("@type")
            types.extend(kind if isinstance(kind, list) else [kind] if kind else [])
            for value in node.values():
                walk(value)

    for raw in BLOCK.findall(page):
        try:
            walk(json.loads(raw))
        except json.JSONDecodeError:
            types.append("INVALID")
    return types


def check_question(question, page):
    """Returns the evidence and the data types the page lacks."""
    text = visible_text(page)
    missing = [e for e in question.get("evidence", []) if not re.search(e, text, re.I)]
    types = data_types(page)
    missing += [f"structured data: {t}" for t in question.get("data", []) if t not in types]
    return missing


def check_hours(page):
    """The opening days in the gallery's structured data are the days the page says."""
    errors = []
    text = visible_text(page)
    for raw in BLOCK.findall(page):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for thing in data.get("@graph", [data]) if isinstance(data, dict) else []:
            spec = thing.get("openingHoursSpecification") if isinstance(thing, dict) else None
            if not spec:
                continue
            days = [d.rsplit("/", 1)[-1] for d in spec.get("dayOfWeek", [])]
            order = [DAYS.index(d) for d in days if d in DAYS]
            if not order:
                errors.append("the gallery's data has no opening days")
            elif order == list(range(order[0], order[-1] + 1)) and len(order) > 1:
                said = f"{days[0]} to {days[-1]}"
                if said.lower() not in text.lower():
                    errors.append(f"the data says {said}; the page doesn't")
            else:
                errors += [f"the data says {d}; the page doesn't" for d in days if d.lower() not in text.lower()]
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("base")
    parser.add_argument("--json", help="write the report here")
    parser.add_argument("--only", default="", help="question numbers, comma-separated")
    args = parser.parse_args(argv)
    base = args.base.rstrip("/")
    only = {int(n) for n in args.only.split(",") if n.strip()}
    spec = json.loads(QUESTIONS.read_text())

    pages, report, failed, closed = {}, [], 0, []

    def get(path):
        if path not in pages:
            try:
                pages[path] = fetch(base + path)
            except (OSError, urllib.error.URLError) as exc:
                pages[path] = exc
        return pages[path]

    for question in spec["questions"]:
        if only and question["n"] not in only:
            continue
        page = get(question["page"])
        if isinstance(page, Exception):
            missing = [f"the page didn't load: {page}"]
        else:
            missing = check_question(question, page)
        gap = question.get("gap")
        if gap:
            state = "gap" if missing else "closed"
            if not missing:
                closed.append(question["n"])
        else:
            state = "missing" if missing else "answered"
            failed += 1 if missing else 0
        report.append({"n": question["n"], "question": question["question"], "page": question["page"],
                       "state": state, "missing": missing, "gap": gap})
        label = {"answered": "OK     ", "missing": "ERROR  ", "gap": "GAP    ", "closed": "CLOSED "}[state]
        print(f"{label} {question['n']:>2}  {question['question']}  ({question['page']})")
        for item in missing if state == "missing" else []:
            print(f"            not found: {item}")
        if state == "gap":
            print(f"            {gap}")

    if not only:
        visit = get(spec["hours_page"])
        for message in [] if isinstance(visit, Exception) else check_hours(visit):
            print(f"ERROR       hours: {message}")
            failed += 1
        try:
            llms = fetch(base + "/llms.txt")
            links = sorted(set(re.findall(r"\]\((https?://[^)\s]+)\)", llms)))
            if spec["llms_title"] not in llms:
                print("ERROR       /llms.txt is not the gallery's own file")
                failed += 1
            for link in links:
                path = "/" + link.split("/", 3)[3] if link.count("/") > 2 else "/"
                if isinstance(get(path), Exception):
                    print(f"ERROR       /llms.txt names {path}, which doesn't answer")
                    failed += 1
            print(f"OK          /llms.txt names {len(links)} pages")
        except (OSError, urllib.error.URLError) as exc:
            print(f"ERROR       /llms.txt didn't load: {exc}")
            failed += 1

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    states = [r["state"] for r in report]
    print(f"\n{states.count('answered')} answered, {states.count('missing')} missing, "
          f"{states.count('gap')} known gaps, {failed} error(s)")
    if closed:
        print(f"Gaps that have closed, to update in answers.json: {', '.join(str(n) for n in closed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
