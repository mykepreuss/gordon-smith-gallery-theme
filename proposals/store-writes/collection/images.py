#!/usr/bin/env python3
"""The collection's images and documents: download, convert, upload (proposals/permanent-collection.md,
"Images"). Reads clean.py's images.json and documents.json.

  python3 images.py convert <data folder> <image folder>   download each master, make the web copy, delete the master
  python3 images.py upload <data folder> <image folder>    upload the web copies to Files, record their IDs
  python3 images.py shrink <data folder> <doc folder>      a copy under 19 MB of each PDF over 20 MB (needs PyMuPDF and Pillow)
  python3 images.py docs <data folder> <doc folder>        the same for the artists' documents (20 MB and under, or shrunk)
  python3 images.py alts <data folder> <image folder>      update alt text in Files after a clean-up change
  python3 images.py docalts <data folder> <doc folder>     the documents' alt text: covers empty, files their titles

Web copy: a JPEG 3,000 px on its long side, in sRGB with the colour profile applied, quality 85, the
whole image (no cropping). macOS sips does the conversion. The masters stay on the catalogue.

Smaller copies of PDFs over Shopify's 20 MB limit (Michael, 2026-09-27: "Can you create the optimized
versions of all the Documents too large for the site"): these are scans, each page one picture at
300 dpi with the OCR text on top. Each picture is resampled to a lower resolution and saved as a JPEG,
at the gentlest setting in SHRINK_STEPS that brings the file under 19 MB. The text, the pages and any
black-and-white fax-compressed pictures are left as they are. What each file got goes to
shrunk-documents.json, which clean.py reads so the document's entry links its file.

Uploads go through the Shopify CLI (`shopify store execute`, authorised by Michael for this import,
P-27): a staged upload, then fileCreate, in batches. The file IDs go to ../created/collection-files.json,
keyed by the catalogue's media ID, so a re-run uploads only what's missing.
"""
import json
import pathlib
import subprocess
import sys
import tempfile
import time
import urllib.request

STORE = "ed35ee-ea.myshopify.com"
HERE = pathlib.Path(__file__).parent
CREATED = HERE.parent / "created" / "collection-files.json"
SRGB = "/System/Library/ColorSync/Profiles/sRGB Profile.icc"
AGENT = "Gordon Smith Gallery collection import"
MAX_BYTES = 20_000_000
SHRUNK = HERE / "shrunk-documents.json"
SHRINK_TARGET = 19_000_000  # under Shopify's limit with room to spare
# (dpi, JPEG quality), gentlest first. 150 dpi keeps a page of type readable on screen; below that
# only the largest scans go.
SHRINK_STEPS = [(200, 75), (150, 70), (150, 60), (130, 60), (120, 55), (110, 50), (100, 50)]


def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=300) as r, open(path, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)


def sips_size(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)], capture_output=True, text=True).stdout
    vals = [int(l.split(":")[1]) for l in out.splitlines() if "pixel" in l]
    return tuple(vals) if len(vals) == 2 else (0, 0)


def convert(data, folder):
    folder.mkdir(parents=True, exist_ok=True)
    manifest_path = folder / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    images = json.loads((data / "images.json").read_text())
    for n, im in enumerate(images, 1):
        key = str(im["media_id"])
        out = folder / f"{im['work']}-{im['position'] + 1}.jpg"
        if key in manifest and out.exists():
            continue
        master = folder / ("master" + pathlib.Path(im["url"]).suffix)
        try:
            download(im["url"], master)
            r = subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85", "-Z", "3000",
                                "-m", SRGB, str(master), "--out", str(out)], capture_output=True, text=True)
            if r.returncode or not out.exists():
                raise RuntimeError(r.stderr.strip() or "sips failed")
            w, h = sips_size(out)
            manifest[key] = {"file": out.name, "work": im["work"], "position": im["position"], "alt": im["alt"],
                             "width": w, "height": h, "bytes": out.stat().st_size, "master_bytes": master.stat().st_size}
        except Exception as e:  # noqa: BLE001 - record and carry on; a re-run retries
            manifest[key] = {"error": str(e), "work": im["work"]}
            print(f"{n}/{len(images)} {im['work']}: {e}", flush=True)
        finally:
            master.unlink(missing_ok=True)
        if n % 25 == 0:
            manifest_path.write_text(json.dumps(manifest, indent=1))
            print(f"{n}/{len(images)}", flush=True)
        time.sleep(0.1)
    manifest_path.write_text(json.dumps(manifest, indent=1))
    ok = [m for m in manifest.values() if "error" not in m]
    print(f"done: {len(ok)} converted, {len(manifest) - len(ok)} errors, {sum(m['bytes'] for m in ok) / 1e9:.2f} GB")


def execute(query, variables):
    """One Admin API call through the Shopify CLI. Returns the data, or raises on errors."""
    with tempfile.TemporaryDirectory() as tmp:
        q, v = pathlib.Path(tmp, "q.graphql"), pathlib.Path(tmp, "v.json")
        q.write_text(query)
        v.write_text(json.dumps(variables, ensure_ascii=False))
        r = subprocess.run(["shopify", "store", "execute", "-s", STORE, "-j", "--allow-mutations",
                            "--query-file", str(q), "--variable-file", str(v)], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[-1500:] or r.stdout.strip()[-1500:])
    text = r.stdout[r.stdout.find("{"):] if "{" in r.stdout else r.stdout  # progress lines come first
    out = json.loads(text)
    data = out.get("data", out)
    if out.get("errors"):
        raise RuntimeError(json.dumps(out["errors"])[:500])
    return data


STAGE = """mutation Stage($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) { stagedTargets { url resourceUrl parameters { name value } } userErrors { field message } }
}"""
CREATE = """mutation Create($files: [FileCreateInput!]!) {
  fileCreate(files: $files) { files { id alt } userErrors { field message } }
}"""


def upload_batch(entries, folder, content_type, mime):
    """entries: [(key, filename, alt)] -> {key: file id}"""
    stage = execute(STAGE, {"input": [{"filename": fn, "mimeType": mime, "resource": content_type,
                                       "httpMethod": "POST", "fileSize": str((folder / fn).stat().st_size)}
                                      for _, fn, _ in entries]})["stagedUploadsCreate"]
    if stage["userErrors"]:
        raise RuntimeError(stage["userErrors"])
    files = []
    for (key, fn, alt), t in zip(entries, stage["stagedTargets"]):
        args = ["curl", "-s", "-f", "-o", "/dev/null", "-w", "%{http_code}"]
        for p in t["parameters"]:
            args += ["-F", f"{p['name']}={p['value']}"]
        args += ["-F", f"file=@{folder / fn}", t["url"]]
        code = subprocess.run(args, capture_output=True, text=True).stdout
        if not code.startswith("2"):
            raise RuntimeError(f"upload of {fn} returned {code}")
        files.append({"originalSource": t["resourceUrl"], "contentType": "IMAGE" if content_type == "IMAGE" else "FILE",
                      "alt": alt[:512], "filename": fn})
    made = execute(CREATE, {"files": files})["fileCreate"]
    if made["userErrors"]:
        raise RuntimeError(made["userErrors"])
    return {key: f["id"] for (key, _, _), f in zip(entries, made["files"])}


def upload(data, folder, batch=25):
    created = json.loads(CREATED.read_text()) if CREATED.exists() else {}
    manifest = json.loads((folder / "manifest.json").read_text())
    todo = [(k, m["file"], m["alt"]) for k, m in manifest.items() if "error" not in m and k not in created]
    print(f"{len(todo)} to upload, {len(created)} already in Files", flush=True)
    for i in range(0, len(todo), batch):
        created.update(upload_batch(todo[i:i + batch], folder, "IMAGE", "image/jpeg"))
        CREATED.write_text(json.dumps(created, indent=1, sort_keys=True))
        print(f"{min(i + batch, len(todo))}/{len(todo)}", flush=True)


def shrink_pdf(src, dst, dpi, quality):
    """Resample every picture above `dpi` to it, as a JPEG at `quality`, and save to `dst`."""
    import io
    import math
    import pymupdf
    from PIL import Image

    doc = pymupdf.open(src)
    # A picture can be placed more than once: go by its largest placement (its lowest dpi).
    placed = {}
    for page in doc:
        for info in page.get_image_info(xrefs=True):
            a, b, c, d = info["transform"][:4]
            w_in, h_in = math.hypot(a, b) / 72, math.hypot(c, d) / 72
            if info["xref"] and w_in and h_in:
                low = min(info["width"] / w_in, info["height"] / h_in)
                placed[info["xref"]] = min(low, placed.get(info["xref"], low))
    for xref, have in placed.items():
        if have <= dpi * 1.1:
            continue
        keys = {k: doc.xref_get_key(xref, k)[1] for k in ("Filter", "ImageMask", "SMask", "Mask")}
        if "CCITT" in keys["Filter"] or "JBIG2" in keys["Filter"] or keys["ImageMask"] == "true" \
                or keys["SMask"] != "null" or keys["Mask"] != "null":
            continue  # black-and-white fax pictures are small already; masked pictures stay exact
        pix = pymupdf.Pixmap(doc, xref)
        if pix.alpha:
            pix = pymupdf.Pixmap(pix, 0)
        if pix.colorspace is None or pix.colorspace.n not in (1, 3):
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        gray = pix.n == 1
        im = Image.frombytes("L" if gray else "RGB", (pix.width, pix.height), pix.samples)
        scale = dpi / have
        im = im.resize((max(1, round(pix.width * scale)), max(1, round(pix.height * scale))), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
        # The new JPEG goes into the picture's own object, so every page that shows it gets it and
        # nothing is stored twice (Page.replace_image keeps its temporary copy on the page).
        doc.update_stream(xref, buf.getvalue(), compress=False)
        for key, value in (("Filter", "/DCTDecode"), ("DecodeParms", "null"), ("Decode", "null"),
                           ("Width", str(im.width)), ("Height", str(im.height)), ("BitsPerComponent", "8"),
                           ("ColorSpace", "/DeviceGray" if gray else "/DeviceRGB")):
            doc.xref_set_key(xref, key, value)
    doc.save(dst, garbage=3, deflate=True)
    return doc.page_count


def shrink(data, folder):
    """A copy under SHRINK_TARGET of each document over MAX_BYTES, in `folder` under the name docs
    uploads; the originals go to `folder`/originals and can be deleted afterwards."""
    import pymupdf

    originals = folder / "originals"
    originals.mkdir(parents=True, exist_ok=True)
    shrunk = json.loads(SHRUNK.read_text()) if SHRUNK.exists() else {}
    big = [d for d in json.loads((data / "documents.json").read_text())
           if d["artist"] and d["size"] > MAX_BYTES and d["type"] == "application/pdf"]
    for n, d in enumerate(sorted(big, key=lambda d: d["size"]), 1):
        fn = f"{d['artist']}-document-{d['media_id']}.pdf"
        out = folder / fn
        if str(d["media_id"]) in shrunk and out.exists():
            continue
        src = originals / fn
        if not src.exists() or src.stat().st_size != d["size"]:
            download(d["url"], src)
        text = [p.get_text() for p in pymupdf.open(src)]
        for dpi, quality in SHRINK_STEPS:
            pages = shrink_pdf(src, out, dpi, quality)
            if out.stat().st_size <= SHRINK_TARGET:
                break
        else:
            out.unlink()
            print(f"{n}/{len(big)} {fn}: still over {SHRINK_TARGET / 1e6:.0f} MB at {dpi} dpi; left out", flush=True)
            continue
        # The copy has to be the same document: every page, the text on each, and every page drawing
        # without an error.
        assert pages == len(text) and [p.get_text() for p in pymupdf.open(out)] == text, fn
        pymupdf.TOOLS.reset_mupdf_warnings()
        for p in pymupdf.open(out):
            p.get_pixmap(matrix=pymupdf.Matrix(0.2, 0.2))
        assert "error" not in pymupdf.TOOLS.mupdf_warnings().lower(), (fn, pymupdf.TOOLS.mupdf_warnings())
        shrunk[str(d["media_id"])] = {"file": fn, "original_bytes": d["size"], "bytes": out.stat().st_size,
                                      "pages": pages, "dpi": dpi, "quality": quality}
        SHRUNK.write_text(json.dumps(shrunk, indent=1, sort_keys=True) + "\n")
        print(f"{n}/{len(big)} {fn}: {d['size'] / 1e6:.0f} MB to {out.stat().st_size / 1e6:.1f} MB "
              f"({dpi} dpi, quality {quality}, {pages} pages)", flush=True)


def docs(data, folder, batch=10):
    folder.mkdir(parents=True, exist_ok=True)
    created = json.loads(CREATED.read_text()) if CREATED.exists() else {}
    shrunk = json.loads(SHRUNK.read_text()) if SHRUNK.exists() else {}
    documents = [d for d in json.loads((data / "documents.json").read_text())
                 if d["artist"] and (d["size"] <= MAX_BYTES or str(d["media_id"]) in shrunk)]
    todo = []
    for d in documents:
        key = f"doc-{d['media_id']}"
        if key in created:
            continue
        suffix = pathlib.Path(d["url"]).suffix.lower()
        fn = f"{d['artist']}-document-{d['media_id']}{suffix}"
        if not (folder / fn).exists():
            if str(d["media_id"]) in shrunk:
                sys.exit(f"{fn}: the smaller copy isn't in {folder}; run images.py shrink first")
            download(d["url"], folder / fn)
            time.sleep(0.1)
        todo.append((key, fn, d["title"], d["type"]))
    print(f"{len(todo)} documents to upload", flush=True)
    for mime in sorted({t[3] for t in todo}):
        group = [(k, fn, alt) for k, fn, alt, m in todo if m == mime]
        kind = "IMAGE" if mime.startswith("image/") else "FILE"
        for i in range(0, len(group), batch):
            created.update(upload_batch(group[i:i + batch], folder, kind, mime))
            CREATED.write_text(json.dumps(created, indent=1, sort_keys=True))
            print(f"{mime}: {min(i + batch, len(group))}/{len(group)}", flush=True)


UPDATE = """mutation Update($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) { files { id alt } userErrors { field message } }
}"""


def alts(data, folder, batch=25):
    """Bring the uploaded images' alt text up to date with clean.py (after a clean-up change)."""
    created = json.loads(CREATED.read_text())
    manifest_path = folder / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    todo = [(str(i["media_id"]), i["alt"]) for i in json.loads((data / "images.json").read_text())
            if str(i["media_id"]) in created and manifest.get(str(i["media_id"]), {}).get("alt") != i["alt"]]
    print(f"{len(todo)} alt texts to update", flush=True)
    for n in range(0, len(todo), batch):
        chunk = todo[n:n + batch]
        out = execute(UPDATE, {"files": [{"id": created[k], "alt": alt[:512]} for k, alt in chunk]})["fileUpdate"]
        if out["userErrors"]:
            raise RuntimeError(out["userErrors"])
        for k, alt in chunk:
            manifest[k]["alt"] = alt
        manifest_path.write_text(json.dumps(manifest, indent=1))
        print(f"{min(n + batch, len(todo))}/{len(todo)}", flush=True)


def docalts(data, folder, batch=25):
    """The documents' alt text (DS-63). A cover's is empty: its title is right under it on the tile, so
    a screen reader would hear the same words twice. A document's own file carries its title."""
    created = json.loads(CREATED.read_text())
    todo = {}
    for e in json.loads((data / "document-entries.json").read_text()):
        if e["file"] and f"doc-{e['file']}" in created:
            todo[created[f"doc-{e['file']}"]] = e["title"]
    for e in json.loads((data / "document-entries.json").read_text()):
        if e["cover"] and f"doc-{e['cover']}" in created:
            todo[created[f"doc-{e['cover']}"]] = ""
    todo = list(todo.items())
    for n in range(0, len(todo), batch):
        out = execute(UPDATE, {"files": [{"id": i, "alt": alt[:512]} for i, alt in todo[n:n + batch]]})["fileUpdate"]
        if out["userErrors"]:
            raise RuntimeError(out["userErrors"])
    print(f"{len(todo)} document files' alt text set")


if __name__ == "__main__":
    steps = {"convert": convert, "upload": upload, "shrink": shrink, "docs": docs, "alts": alts, "docalts": docalts}
    if len(sys.argv) != 4 or sys.argv[1] not in steps:
        sys.exit(__doc__)
    steps[sys.argv[1]](pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]))
