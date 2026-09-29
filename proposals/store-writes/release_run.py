#!/usr/bin/env python3
"""Runs the release's store changes from files, through the Shopify CLI (`shopify store execute`),
so each value reaches the store exactly as release.py printed it. Michael, 2026-09-29: "Proceed with
your recommendation" (verification/2026-09-29-release-gate.md, "How the writes are made").

  python3 proposals/store-writes/release_run.py <step> <pages.json> [--go]
  steps: event, templates, addresses, staged, unhide, frames, readback

Without --go it prints each call and changes nothing. With --go it makes them one at a time, stops at
the first error, and writes what the store answered to created/release-<date>/<step>.json.
`readback` reads the store to a file and changes nothing.

Before the first write: the store, the live theme's ID and role, and the review theme's, are rechecked
by hand (AGENTS.md). The CLI's store access comes from `shopify store auth`, which Michael approves.
"""
import datetime
import json
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import release  # noqa: E402

STORE = "ed35ee-ea.myshopify.com"
EVENT_DEFINITION = "gid://shopify/MetaobjectDefinition/23753392425"
RELEASE_BODY_DEFINITION = "gid://shopify/MetafieldDefinition/272804249897"
ERRORS = "userErrors { field message }"

Q = {
    "event": "mutation($id: ID!, $definition: MetaobjectDefinitionUpdateInput!) { metaobjectDefinitionUpdate(id: $id, definition: $definition) { "
             "metaobjectDefinition { id type capabilities { renderable { enabled data { metaTitleKey metaDescriptionKey } } "
             "onlineStore { enabled data { urlHandle } } } } " + ERRORS + " } }",
    "page": "mutation($id: ID!, $page: PageUpdateInput!) { pageUpdate(id: $id, page: $page) { "
            "page { id handle templateSuffix isPublished } " + ERRORS + " } }",
    "redirect": "mutation($urlRedirect: UrlRedirectInput!) { urlRedirectCreate(urlRedirect: $urlRedirect) { "
                "urlRedirect { id path target } " + ERRORS + " } }",
    "repoint": "mutation($id: ID!, $urlRedirect: UrlRedirectInput!) { urlRedirectUpdate(id: $id, urlRedirect: $urlRedirect) { "
               "urlRedirect { id path target } " + ERRORS + " } }",
    "fields": "mutation($metafields: [MetafieldIdentifierInput!]!) { metafieldsDelete(metafields: $metafields) { "
              "deletedMetafields { ownerId namespace key } " + ERRORS + " } }",
    "definition": "mutation($id: ID!) { metafieldDefinitionDelete(id: $id, deleteAllAssociatedMetafields: false) { "
                  "deletedDefinitionId " + ERRORS + " } }",
    "frame": "mutation($product: ProductUpdateInput!) { productUpdate(product: $product) { "
             "product { id handle status } " + ERRORS + " } }",
    "readback": "query { pages(first: 100, sortKey: ID) { nodes { id handle title templateSuffix isPublished updatedAt body "
                "staged: metafield(namespace: \"custom\", key: \"release_body\") { id value } "
                "hidden: metafield(namespace: \"seo\", key: \"hidden\") { id value } } } "
                "urlRedirects(first: 50) { nodes { id path target } } "
                "frames: products(first: 50, query: \"product_type:Frame\") { nodes { id handle status } } "
                "event: metaobjectDefinitionByType(type: \"event\") { id capabilities { renderable { enabled } "
                "onlineStore { enabled data { urlHandle } } } } "
                "definitions: metafieldDefinitions(first: 50, ownerType: PAGE, namespace: \"custom\") { nodes { id key name } } }",
}


def calls(step, pages):
    """The step's calls, in order: (name, query, variables)."""
    if step == "event":
        return [("event pages on", "event", {"id": EVENT_DEFINITION, "definition": {"capabilities": {
            "renderable": {"enabled": True, "data": {"metaTitleKey": "title", "metaDescriptionKey": "summary"}},
            "onlineStore": {"enabled": True, "data": {"urlHandle": "events", "createRedirects": False}}}}})]
    if step == "templates":
        return [(k, "page", v) for k, v in release.templates(pages, True).items()]
    if step == "addresses":
        out = []
        for k, v in release.addresses(pages, True).items():
            if k.startswith("hide"):
                out.append((k, "page", v))
            elif k.startswith("r"):
                out.append((k, "redirect", {"urlRedirect": v}))
            else:
                out.append((k, "repoint", v))
        return out
    if step == "staged":
        v = release.staged(pages, True)
        out = [(k, "page", m) for k, m in v["pages"].items()]
        d = v["metafieldsDelete"]
        out += [(f"staged values {i + 1} to {i + len(d[i:i + 25])}", "fields", {"metafields": d[i:i + 25]}) for i in range(0, len(d), 25)]
        return out + [("release_body definition", "definition", {"id": RELEASE_BODY_DEFINITION})]
    if step == "unhide":
        d = release.unhide(pages, True)["metafields"]
        return [(f"seo.hidden {i + 1} to {i + len(d[i:i + 25])}", "fields", {"metafields": d[i:i + 25]}) for i in range(0, len(d), 25)]
    if step == "frames":
        return [(k, "frame", {"product": v}) for k, v in release.frames(True).items()]
    sys.exit(f"Unknown step: {step}")


def execute(query, variables, mutate):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "q.graphql").write_text(query)
        (tmp / "v.json").write_text(json.dumps(variables, ensure_ascii=False))
        cmd = ["shopify", "store", "execute", "--store", STORE, "--query-file", str(tmp / "q.graphql"),
               "--variable-file", str(tmp / "v.json"), "--json", "--output-file", str(tmp / "out.json")]
        done = subprocess.run(cmd + (["--allow-mutations"] if mutate else []), capture_output=True, text=True)
        if done.returncode != 0 or not (tmp / "out.json").exists():
            return None, (done.stdout + done.stderr)[-1500:]
        out = json.loads((tmp / "out.json").read_text())
        return out.get("data", out), None


def user_errors(data):
    found = []
    for payload in (data or {}).values():
        if isinstance(payload, dict):
            found += payload.get("userErrors") or []
    return found


if __name__ == "__main__":
    step, args = sys.argv[1], sys.argv[2:]
    go = "--go" in args
    files = [a for a in args if not a.startswith("--")]
    if step == "readback":
        data, err = execute(Q["readback"], {}, False)
        if err:
            sys.exit(err)
        pathlib.Path(files[0]).write_text(json.dumps(data, ensure_ascii=False, indent=1))
        print(f"read: {len(data['pages']['nodes'])} pages, {len(data['urlRedirects']['nodes'])} redirects, "
              f"{len(data['frames']['nodes'])} frames; written to {files[0]}")
        sys.exit(0)
    pages = json.loads(pathlib.Path(files[0]).read_text()) if files else None
    todo = calls(step, pages)
    log = []
    folder = HERE / "created" / f"release-{datetime.date.today().isoformat()}"
    for name, kind, variables in todo:
        short = json.dumps(variables, ensure_ascii=False)
        if not go:
            print(f"would run {kind}: {name}: {short[:150]}{'...' if len(short) > 150 else ''}")
            continue
        data, err = execute(Q[kind], variables, True)
        errors = user_errors(data) if not err else [{"message": err}]
        log.append({"call": name, "kind": kind, "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                    "variables": variables if kind != "page" or "body" not in variables.get("page", {})
                    else {"id": variables["id"], "page": {"body": f"({len(variables['page']['body'])} characters)"}},
                    "answer": data, "errors": errors})
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{step}.json").write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n")
        if errors:
            sys.exit(f"STOPPED at {name}: {errors}\n{len(log) - 1} call(s) made before it; see {folder / (step + '.json')}")
        print(f"done {kind}: {name}")
    print(f"{len(todo)} call(s) {'made' if go else 'listed; nothing changed'}")
