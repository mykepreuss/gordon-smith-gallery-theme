#!/usr/bin/env python3
"""Load the cleaned collection into the store (proposals/permanent-collection.md, P-27). Reads clean.py's
output and the file IDs images.py recorded. Every step upserts by handle, so a re-run updates in place.

  python3 import.py <step> <data folder> [--dry-run]

Steps, in order:
  artists    every artist: name, sort name, full and other names, dates, website, exhibitions
  works      every work: label fields, artists, images, themes, the edition in the Shop, exhibitions
  link       each artist's Works list and Documents
  groups     the categories, themes and groupings, with their works
  exhibitions  each exhibition's Works from the collection (from the works' Shown in and the
             catalogue's "Works in …" pages)
  --print <folder> writes each batch (mutation and variables) to a file, for running through the
  Shopify connector instead of the CLI; record the returned IDs with `import.py record`.

  products   prints the metafieldsSet variables for the editions' Artist pages field (run through the
             Shopify connector, which has product access)

Runs through the Shopify CLI (`shopify store execute`), authorised by Michael for this import. Created
IDs go to ../created/collection-<type>.json. Entries are active, so the review theme shows them; the
live theme has no template for them, so their addresses return 404 there.
"""
import json
import pathlib
import sys
import time

from images import CREATED as FILES, execute

HERE = pathlib.Path(__file__).parent
CREATED = HERE.parent / "created"
BATCH = 20
PRINT = None  # --print <folder>: write the batches for the Shopify connector instead of running them

UPSERT = "metaobjectUpsert(handle: $h{i}, metaobject: $m{i}) {{ metaobject {{ id handle }} userErrors {{ field message code }} }}"


def ids(name):
    p = CREATED / f"collection-{name}.json"
    return json.loads(p.read_text()) if p.exists() else {}


def save(name, data):
    (CREATED / f"collection-{name}.json").write_text(json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False))


def fields(**kw):
    out = []
    for k, v in kw.items():
        if v in (None, "", []):
            continue
        out.append({"key": k, "value": v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)})
    return out


def batches(type_, rows):
    for start in range(0, len(rows), BATCH):
        chunk = rows[start:start + BATCH]
        decl = ", ".join(f"$h{i}: MetaobjectHandleInput!, $m{i}: MetaobjectUpsertInput!" for i in range(len(chunk)))
        body = "\n".join(f"u{i}: " + UPSERT.format(i=i) for i in range(len(chunk)))
        variables = {}
        for i, (handle, f) in enumerate(chunk):
            variables[f"h{i}"] = {"type": type_, "handle": handle}
            variables[f"m{i}"] = {"fields": f, "capabilities": {"publishable": {"status": "ACTIVE"}}}
        yield chunk, f"mutation Upsert({decl}) {{\n{body}\n}}", variables


def upsert(type_, rows, record, dry):
    """rows: [(handle, fields)]. Records handle -> id in collection-<record>.json."""
    done = ids(record)
    if PRINT:
        # For the Shopify connector: one file per batch, with the mutation and its variables.
        out = pathlib.Path(PRINT)
        out.mkdir(parents=True, exist_ok=True)
        for n, (chunk, query, variables) in enumerate(batches(type_, rows)):
            (out / f"{record}-{n:02d}.json").write_text(json.dumps({"query": query, "variables": variables}, ensure_ascii=False))
        print(f"wrote {n + 1} batches to {out}")
        return done
    if dry:
        print(json.dumps(rows[:2], indent=1, ensure_ascii=False))
        print(f"dry run: {len(rows)} {type_} entries")
        return done
    errors = []
    for start, (chunk, query, variables) in zip(range(0, len(rows), BATCH), batches(type_, rows)):
        data = execute(query, variables)
        for i, (handle, _) in enumerate(chunk):
            res = data[f"u{i}"]
            if res["userErrors"]:
                errors.append((handle, res["userErrors"]))
            else:
                done[handle] = res["metaobject"]["id"]
        save(record, done)
        print(f"{type_}: {min(start + BATCH, len(rows))}/{len(rows)}", flush=True)
        time.sleep(0.5)
    for e in errors:
        print("ERROR", e)
    return done


def main(step, data, dry):
    artists = json.loads((data / "artists.json").read_text())
    works = json.loads((data / "works.json").read_text())
    store = json.loads((data / "products.json").read_text())
    exhibitions = {e["handle"]: e["id"] for e in json.loads((data.parent / "afk" / "store.json").read_text())["exhibitions"]}
    products = {p["handle"]: p["id"] for p in store}
    files = json.loads(FILES.read_text()) if FILES.exists() else {}
    artist_ids, work_ids = ids("artists"), ids("works")

    if step == "artists":
        rows = [(a["handle"], fields(
            name=a["name"], sort_name=a["sort_name"], full_name=a["full_name"], other_names=a["other_names"],
            life_dates=a["life_dates"],
            website={"text": "", "url": a["website"]} if a["website"] else None,
            exhibitions=[exhibitions[h] for h in sorted(a["exhibitions"]) if h in exhibitions])) for a in artists]
        upsert("artist", rows, "artists", dry)

    elif step == "works":
        rows = []
        for w in works:
            rows.append((w["handle"], fields(
                title=w["title"], artists=[artist_ids[h] for h in w["artists"] if h in artist_ids],
                year=w["year"], category=w["category"], medium=w["medium"], dimensions=w["dimensions"],
                edition=w["edition"], accession_number=w["accession"], credit_line=w["credit_line"],
                images=[files[str(m)] for m in w["images"] if str(m) in files], themes=w["themes"],
                in_the_shop=products.get(w["in_the_shop"]),
                shown_in=[exhibitions[h] for h in w["shown_in"] if h in exhibitions])))
        missing = sum(1 for w in works for m in w["images"] if str(m) not in files)
        print(f"images not yet in Files: {missing}")
        upsert("artwork", rows, "works", dry)

    elif step == "link":
        docs = {}
        documents = {d["media_id"]: d for d in json.loads((data / "documents.json").read_text())}
        for a in artists:
            for m in a["documents"]:  # the files clean.py chose to show, in its order
                if f"doc-{m}" in files and documents[m]["show"]:
                    docs.setdefault(a["handle"], []).append(files[f"doc-{m}"])
        # Both lists are always sent, so one that has become empty ("[]") is cleared in the store.
        rows = [(a["handle"], fields(name=a["name"], sort_name=a["sort_name"])
                 + [{"key": "works", "value": json.dumps([work_ids[h] for h in a["works"] if h in work_ids])},
                    {"key": "documents", "value": json.dumps(docs.get(a["handle"], []))}]) for a in artists]
        upsert("artist", rows, "artists", dry)

    elif step == "groups":
        groups = json.loads((data / "groups.json").read_text())
        rows = [(g["handle"], fields(name=g["name"], kind=g["kind"], introduction=g["introduction"],
                                     works=[work_ids[h] for h in g["works"] if h in work_ids])) for g in groups]
        upsert("collection_group", rows, "groups", dry)

    elif step == "exhibitions":
        lists = json.loads((data / "exhibitions.json").read_text())
        rows = [(h, fields(collection_works=[work_ids[w] for w in ws if w in work_ids])) for h, ws in sorted(lists.items())]
        upsert("exhibition", rows, "exhibition-works", dry)

    elif step == "products":
        mf = []
        for p in store:
            handles = p.get("artist_handles") or []
            if handles and all(h in artist_ids for h in handles):
                mf.append({"ownerId": p["id"], "namespace": "custom", "key": "artist_entries",
                           "type": "list.metaobject_reference", "value": json.dumps([artist_ids[h] for h in handles])})
        print(json.dumps({"metafields": mf}, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    if "--print" in sys.argv:
        PRINT = sys.argv[sys.argv.index("--print") + 1]
    main(sys.argv[1], pathlib.Path(sys.argv[2]), "--dry-run" in sys.argv)
