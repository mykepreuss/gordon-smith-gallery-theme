#!/usr/bin/env python3
"""Check a Shopify theme against the design system's structural rules.

Turns DESIGN.md §7 and §9 into checks that run on every change, so the site stays coherent
as different people edit it. Standard library only.

  python3 design-system/scripts/lint_theme.py theme/            # report, exit 1 on errors
  python3 design-system/scripts/lint_theme.py theme/ --strict   # warnings also fail

What it checks
  templates   Every JSON template is one of the approved templates (no one-off page.* templates),
              follows its composition rules (which kinds of section, how many, what comes first,
              no repeated listings, no two tinted bands in a row), and has no disabled leftovers.
  settings    Section and block schemas don't give staff design controls: colour pickers,
              colour schemes, font pickers, padding/size/opacity sliders (lockedSettings).
  code        gs- assets, sections and snippets don't hard-code colours, palette values, px font
              sizes, durations, line heights or ratios; no transition on all, no :has() inside
              :has(), :hover only for a mouse, and grid and event lists keep role="list".
  renders     Snippet calls pass the parameters they need (e.g. gs-media gets a preset, so images
              are sized for where they sit).

Rules live in design-system/templates.rules.json.
"""
import argparse
import fnmatch
import json
import pathlib
import re
import sys

RULES = pathlib.Path(__file__).resolve().parent.parent / "templates.rules.json"


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, where, message):
        self.items.append((level, where, message))

    def count(self, level):
        return sum(1 for i in self.items if i[0] == level)


def load_json_template(path):
    """Shopify writes a /* ... */ banner at the top of generated JSON templates."""
    text = path.read_text()
    text = re.sub(r"^\s*/\*.*?\*/", "", text, count=1, flags=re.S)
    return json.loads(text)


def template_key(theme, path):
    rel = path.relative_to(theme / "templates").as_posix()
    return rel[: -len(".json")]


def group_of(section_type, groups):
    for name, types in groups.items():
        if section_type in types:
            return name
    return None


def check_templates(theme, rules, report):
    groups = rules["sectionGroups"]
    g = rules["global"]
    approved = rules["templates"]
    tdir = theme / "templates"
    if not tdir.is_dir():
        report.add("error", "templates/", "folder not found")
        return
    for path in sorted(tdir.rglob("*.json")):
        key = template_key(theme, path)
        where = f"templates/{key}.json"
        try:
            data = load_json_template(path)
        except json.JSONDecodeError as exc:
            report.add("error", where, f"invalid JSON: {exc}")
            continue
        spec = approved.get(key)
        if spec is None:
            if g.get("templatesAreClosedSet"):
                report.add("error", where, "not an approved template. Move this page to one of the approved templates "
                           "and put its unique content in page fields (DESIGN.md §7.3)")
            continue

        sections = data.get("sections", {})
        order = data.get("order", list(sections))
        enabled = []
        for sid in order:
            sec = sections.get(sid, {})
            if sec.get("disabled"):
                if g.get("warnDisabledSections"):
                    report.add("warning", where, f"disabled section '{sid}' ({sec.get('type')}): delete it rather than hide it")
                continue
            enabled.append((sid, sec))

        if spec.get("legacy"):
            for need in spec.get("require", []):
                if not any(group_of(s.get("type"), groups) == need for _, s in enabled):
                    report.add("error", where, f"missing required {need} section")
            continue

        if len(enabled) > g["maxSections"]:
            report.add("error", where, f"{len(enabled)} sections; the limit is {g['maxSections']}")

        kinds = []
        for sid, sec in enabled:
            kind = group_of(sec.get("type"), groups)
            if kind is None and g.get("warnUnknownSectionTypes"):
                report.add("warning", where, f"section '{sid}' has type '{sec.get('type')}', which isn't in any sectionGroup")
            kinds.append(kind)

        first = spec.get("firstGroups", g["firstGroups"])
        if enabled and kinds[0] not in first:
            report.add("error", where, f"must start with {' or '.join(first)}, starts with '{enabled[0][1].get('type')}'")

        for need in spec.get("require", []):
            if need not in kinds:
                report.add("error", where, f"missing required {need} section")

        limits = dict(g["maxPerGroup"])
        limits.update(spec.get("maxPerGroup", {}))
        for kind, limit in limits.items():
            n = kinds.count(kind)
            if n > limit:
                report.add("error", where, f"{n} {kind} sections; at most {limit} allowed")

        repeated = g.get("noRepeatedSurface", [])
        prev = None
        for sid, sec in enabled:
            surface = sec.get("settings", {}).get("surface")
            if surface in repeated and surface == prev:
                report.add("error", where, f"two {surface} sections in a row ('{sid}')")
            prev = surface


SCHEMA_RE = re.compile(r"{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema\s*-?%}", re.S)


def iter_settings(schema):
    for s in schema.get("settings", []):
        yield None, s
    for block in schema.get("blocks", []):
        for s in block.get("settings", []):
            yield block.get("type"), s


def check_settings(theme, rules, report):
    locked = rules["lockedSettings"]
    id_re = re.compile(locked["idPattern"])
    for path in sorted((theme / "sections").glob("*.liquid")) if (theme / "sections").is_dir() else []:
        m = SCHEMA_RE.search(path.read_text())
        if not m:
            continue
        where = f"sections/{path.name}"
        try:
            schema = json.loads(m.group(1))
        except json.JSONDecodeError as exc:
            report.add("error", where, f"invalid schema JSON: {exc}")
            continue
        own = path.name.startswith("gs-")
        for block, s in iter_settings(schema):
            sid, stype = s.get("id"), s.get("type")
            if not sid or sid in locked["allowIds"]:
                continue
            reason = None
            if stype in locked["types"]:
                reason = f"type '{stype}'"
            elif stype in ("range", "number", "select", "radio") and id_re.search(sid):
                reason = f"{stype} '{sid}'"
            if reason:
                scope = f" (block '{block}')" if block else ""
                report.add("error" if own else "warning", where,
                           f"design control for staff{scope}: {reason}. Remove it; the value belongs in tokens")


def blank_out(match):
    """Replace a skipped block with its line breaks, so line numbers stay right."""
    return "\n" * match.group(0).count("\n")


SKIP_BLOCKS = [
    re.compile(r"{%-?\s*schema\s*-?%}.*?{%-?\s*endschema\s*-?%}", re.S),
    re.compile(r"{%-?\s*doc\s*-?%}.*?{%-?\s*enddoc\s*-?%}", re.S),
    re.compile(r"{%-?\s*comment\s*-?%}.*?{%-?\s*endcomment\s*-?%}", re.S),
]
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.S)


def code_files(theme, files, skip):
    for path in sorted(theme.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(theme).as_posix()
        if not any(fnmatch.fnmatch(rel, pat) for pat in files):
            continue
        if any(fnmatch.fnmatch(rel, pat) for pat in skip):
            continue
        yield path, rel


def code_text(path, rel):
    """The file's code without schemas, doc and comment blocks (Liquid) or comments (CSS)."""
    text = path.read_text(errors="replace")
    blocks = [CSS_COMMENT] if rel.endswith(".css") else SKIP_BLOCKS
    for rx in blocks:
        text = rx.sub(blank_out, text)
    return text


def check_code(theme, rules, report):
    code = rules["codeRules"]
    patterns = []
    for name, spec in code["patterns"].items():
        if name.startswith("$"):
            continue
        if isinstance(spec, str):
            spec = {"pattern": spec}
        patterns.append((name, re.compile(spec["pattern"]), spec.get("files"), spec.get("level", "error"),
                         spec.get("message", f"{name}; use a token from tokens.css")))
    for path, rel in code_files(theme, code["files"], code["skipFiles"]):
        text = code_text(path, rel)
        original = path.read_text(errors="replace").splitlines()
        for lineno, line in enumerate(text.splitlines(), 1):
            if "gs-lint-ignore" in original[lineno - 1]:
                continue
            for name, rx, files, level, message in patterns:
                if files and not any(fnmatch.fnmatch(rel, pat) for pat in files):
                    continue
                if rx.search(line):
                    report.add(level, f"{rel}:{lineno}", message)
    check_hover(theme, code, report)


HOVER_MEDIA = re.compile(r"@media[^{]*\(\s*hover\s*:\s*hover\s*\)[^{]*\(\s*pointer\s*:\s*fine\s*\)"
                         r"|@media[^{]*\(\s*pointer\s*:\s*fine\s*\)[^{]*\(\s*hover\s*:\s*hover\s*\)")


def check_hover(theme, code, report):
    """Every :hover selector sits inside @media (hover: hover) and (pointer: fine) (DESIGN.md §5.4).
    A small brace scanner: each block's prelude is the text since the last ; { or }."""
    spec = code.get("hoverOutsideMedia")
    if not spec:
        return
    for path, rel in code_files(theme, spec["files"], code["skipFiles"]):
        text = code_text(path, rel)
        original = path.read_text(errors="replace").splitlines()
        stack = []  # one entry per open block: True if it is (or is inside) a hover media query
        prelude_start = 0
        for i, ch in enumerate(text):
            if ch == "{":
                prelude = text[prelude_start:i]
                inside = bool(stack and stack[-1])
                is_hover_media = bool(HOVER_MEDIA.search(prelude))
                if ":hover" in prelude and not prelude.lstrip().startswith("@") and not inside:
                    first = text.count("\n", 0, prelude_start + len(prelude) - len(prelude.lstrip())) + 1
                    last = text.count("\n", 0, i) + 1
                    if not any("gs-lint-ignore" in original[n - 1] for n in range(first, last + 1)):
                        report.add("error", f"{rel}:{first}", spec["message"])
                stack.append(inside or is_hover_media)
                prelude_start = i + 1
            elif ch == "}":
                if stack:
                    stack.pop()
                prelude_start = i + 1
            elif ch == ";":
                prelude_start = i + 1


RENDER_RE = re.compile(r"render\s+['\"]([\w-]+)['\"]")


def render_args(text, start):
    """Text of one render call's parameters: up to the tag's %}, or, inside a {% liquid %} block,
    to the end of the line unless the line ends with a comma (parameters continued)."""
    out = []
    i = start
    while i < len(text) and not text.startswith("%}", i) and not text.startswith("-%}", i):
        if text[i] == "\n" and not "".join(out).rstrip().endswith(","):
            break
        out.append(text[i])
        i += 1
    return "".join(out)


def check_renders(theme, rules, report):
    spec = rules.get("renderRules")
    if not spec:
        return
    wanted = spec["snippets"]
    for path in sorted(theme.rglob("*.liquid")):
        rel = path.relative_to(theme).as_posix()
        if not any(fnmatch.fnmatch(rel, pat) for pat in spec["files"]):
            continue
        text = path.read_text(errors="replace")
        for m in RENDER_RE.finditer(text):
            name = m.group(1)
            rule = wanted.get(name)
            if not rule:
                continue
            args = render_args(text, m.end())
            need = rule.get("requireOneOf", [])
            if need and not any(re.search(rf"\b{re.escape(k)}\s*:", args) for k in need):
                lineno = text.count("\n", 0, m.start()) + 1
                report.add("error", f"{rel}:{lineno}", f"render '{name}' without {' or '.join(need)}: {rule['message']}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("theme", type=pathlib.Path)
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--rules", type=pathlib.Path, default=RULES)
    args = ap.parse_args(argv)
    rules = json.loads(args.rules.read_text())
    report = Report()
    check_templates(args.theme, rules, report)
    check_settings(args.theme, rules, report)
    check_code(args.theme, rules, report)
    check_renders(args.theme, rules, report)
    for level, where, msg in sorted(report.items, key=lambda i: (i[0] != "error", i[1])):
        print(f"{level.upper():7} {where}: {msg}")
    errors, warnings = report.count("error"), report.count("warning")
    print(f"\n{errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
