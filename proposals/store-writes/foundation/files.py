#!/usr/bin/env python3
"""The Smith Foundation's old site's pictures and PDFs, into the store's Files
(proposals/smith-foundation-site.md, step 7; P-40, P-41 to P-47).

  python3 files.py prepare <media folder>   web copies of the chosen pictures, and a copy under 19 MB of
                                            the Unfixed book (20.2 MB), into <media folder>/upload
  python3 files.py upload <media folder>    upload what isn't in Files yet; IDs to ../created/foundation-files.json
  python3 files.py urls                     each uploaded file's address and size, into the same file

<media folder> is the download of the old site's media library (2026-09-28), outside Git:
~/Downloads/smithfoundation-media, whose files/ holds WordPress's year and month folders and whose
manifest.csv lists every file.

Pictures: a JPEG no more than 3,000 px on its long side, sRGB, quality 85, never cropped, a smaller one
kept at its size (as artists-for-kids/files.py). Logos stay PNG where they are PNG, so their
transparency survives. Alt text is written here from looking at each picture; the old site's was
the file's name, or nothing.

Chosen 2026-09-28 from numbered contact sheets of each set: five photos of each gala (from 98, 159
and 235), two of each Spring Luncheon, twelve views of Unfixed (from 32; the old page had them all),
and the Steinway piano. Three older exhibitions have no picture of their own on the old site; their
key image is a work of an exhibiting artist from the collection, already in Files (content.py).

Uploads go through the Shopify CLI (`shopify store execute`), as the collection's and Artists for
Kids' did: a staged upload, then fileCreate. Nothing is uploaded twice: the created file keeps each key.
"""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "collection"))
from images import execute, shrink_pdf, upload_batch  # noqa: E402

CREATED = HERE.parent / "created" / "foundation-files.json"
SRGB = "/System/Library/ColorSync/Profiles/sRGB Profile.icc"
MAX_BYTES = 20_000_000
SHRINK_TARGET = 19_000_000
SHRINK_STEPS = [(150, 70), (130, 65), (120, 60), (110, 55), (100, 50)]

# key: (the old site's file under files/, the name in Files, alt text)
IMAGES = {
    # Exhibitions, 2013 to 2019: key images (P-41)
    "ex-collection-connection": ("2017/10/PA1300021.jpg", "sf-exhibition-2013-collection-connection.jpg", ""),
    "ex-penner": ("2017/11/Beds_Rooms4317-36a.jpg", "sf-exhibition-2014-penner-beds-rooms.jpg", ""),
    "ex-gu-xiong": ("2017/07/Gu-Xiong-Installation-View.jpg", "sf-exhibition-2014-gu-xiong.jpg", ""),
    "ex-figurative": ("2017/10/Art-Inquiry-Station-w-Figurative-Contemplation-exhibition.jpg",
                      "sf-exhibition-2015-figurative-contemplation.jpg", ""),
    "ex-penhall": ("2017/11/IMG_3872.jpg", "sf-exhibition-2015-ross-penhall.jpg", ""),
    "ex-davidson": ("2017/07/Robert-Davidson-Installation-View.png", "sf-exhibition-2015-robert-davidson.jpg", ""),
    "ex-phantoms": ("2015/12/Sleepingmodernistmichaelabrahamemail.jpg",
                    "sf-exhibition-2015-phantoms-sleeping-modernist.jpg", ""),
    "ex-readymades": ("2017/07/DSC_5630.jpg", "sf-exhibition-2016-readymades.jpg", ""),
    "ex-readymades-view": ("2017/10/Readymades-Installation-View-1.png", "sf-exhibition-2016-readymades-view.jpg", ""),
    "ex-art-school-high": ("2017/07/GordonSmithGallery_ArtSchoolHigh_04.tif", "sf-exhibition-2017-art-school-high.jpg", ""),
    "ex-memory-history-story": ("2017/11/MemoryHistoryStory_Install-24-3.jpg",
                                "sf-exhibition-2017-memory-history-story.jpg", ""),
    "ex-ghosts": ("2017/11/SummonGhosts-50_WEBSITE.jpg", "sf-exhibition-2018-summon-ghosts.jpg", ""),
    "ex-ghosts-2": ("2018/06/SummonGhosts-56_Website.jpg", "sf-exhibition-2018-summon-ghosts-2.jpg", ""),
    "ex-ghosts-3": ("2017/10/SummonGhosts-6NEW.jpg", "sf-exhibition-2018-summon-ghosts-3.jpg", ""),
    "ex-ghosts-4": ("2017/10/SummonGhosts-68.jpg", "sf-exhibition-2018-summon-ghosts-4.jpg", ""),
    "ex-transformations": ("2019/01/Transformations3-1.jpg", "sf-exhibition-2018-transformations.jpg", ""),
    "ex-reframed": ("2019/02/Kerr_Before-the-Inferno-I-Had-a-Light-Heart-800px.jpeg",
                    "sf-exhibition-2019-reframed-tiko-kerr.jpg", ""),
    # Unfixed, 2021: installation views (twelve of the old page's 32)
    **{f"unfixed-{n}": (path, f"sf-exhibition-2021-unfixed-{n}.jpg", "") for n, path in enumerate([
        "2021/04/Unfixed-installation-photo_1.jpg",
        "2021/04/Unfixed-installation-photo_2.jpg",
        "2021/04/Handle-Chris-Curreri-142.2-x-104.1-cm-Chromogenic-print-2009_2.jpg",
        "2021/04/Knot-Laurie-Kang-8622-x-78-Unfixed-unprocessed-photographic-papeR_1.jpg",
        "2021/04/Knot-Laurie-Kang-8622-x-78-Unfixed-unprocessed-photographic-papeR_4.jpg",
        "2021/04/Knot-Laurie-Kang-8622-x-78-Unfixed-unprocessed-photographic-papeR_7.jpg",
        "2021/04/knots-Laurie-Kang-and-Handle-Chris-Curreri.jpg",
        "2021/04/Guts_Laurie-Kang_5.jpg",
        "2021/04/Medusa-and-Clay-Portfolio-Chris-Curreri_2.jpg",
        "2021/04/Medusa-and-Clay-Portfolio-Chris-Curreri_4.jpg",
        "2021/04/Mother-Laurie-Kang_1.jpg",
        "2021/04/Untitled-Clay-Portfolio-Chris-Curreri-14.6-x-19.7-cm-Gelatin-silver-print-2013_2.jpg",
    ], 1)},
    # Funder and sponsor logos (credits). Their alt text names the organisation.
    "logo-parc": ("2023/03/parc_logo_Colour_High-Resolution.jpg", "sf-logo-parc-retirement-living.jpg",
                  "Parc Retirement Living"),
    "logo-nvrc": ("2022/02/nvrc-horizontal-rgb.jpg", "sf-logo-nvrc-horizontal.jpg",
                  "North Vancouver Recreation and Culture Commission"),
    "logo-nvrc-stacked": ("2023/03/NVRC-Blue-Stacked.png", "sf-logo-nvrc-stacked.png",
                          "North Vancouver Recreation and Culture Commission"),
    "logo-mission-hill": ("2023/03/MHFE-2020-logo-PMS-01.png", "sf-logo-mission-hill-family-estate.png",
                          "Mission Hill Family Estate"),
    "logo-capture": ("2023/03/2021-Capture-Logo-Full.png", "sf-logo-capture-photography-festival.png",
                     "Capture Photography Festival"),
    # Pages: heroes and the pictures in their text
    "hero-scholarships": ("2021/03/AFK-Academy-8128.jpg", "sf-scholarships.jpg", ""),
    "piano": ("2017/07/Gordon-Smith-Gallery-Baby-Grand-Piano-Horiz.jpg", "sf-steinway-piano.jpg", ""),
    **{f"gala-2026-{n}": (f"2026/03/2026Brilliance_Fuoco{f}.jpg", f"sf-brilliance-gala-2026-{n}.jpg", "")
       for n, f in enumerate(["-3", "030", "036", "058", "086"], 1)},
    **{f"gala-2025-{n}": (f"2025/03/250307_galacampsmith-{f}.jpg", f"sf-gala-at-camp-smith-2025-{n}.jpg", "")
       for n, f in enumerate(["0004", "0086", "0249", "0792", "1011"], 1)},
    **{f"gala-2023-{n}": (path, f"sf-brilliance-gala-2023-{n}.jpg", "") for n, path in enumerate([
        "2023/06/230616_brilliance_gala-0881-scaled.jpg",
        "2023/06/230616_brilliance_gala-1370-scaled.jpg",
        "2023/06/230616_brilliance_gala-1427-scaled.jpg",
        "2023/06/230616_brilliance_gala-1809-scaled.jpg",
        "2023/07/230705_brilliance_gala-1329-scaled.jpg",
    ], 1)},
    "luncheon-2019-1": ("2019/06/2019_Smith_Luncheon-40.jpg", "sf-spring-luncheon-2019-1.jpg", ""),
    "luncheon-2019-2": ("2019/06/2019_Smith_Luncheon-64-1.jpg", "sf-spring-luncheon-2019-2.jpg", ""),
    "luncheon-2018-1": ("2018/06/IMG_7208.jpg", "sf-spring-luncheon-2018-1.jpg", ""),
    "luncheon-2018-2": ("2018/06/IMG_7177.jpg", "sf-spring-luncheon-2018-2.jpg", ""),
    "luncheon-2013-1": ("2018/06/MG_5002.jpg", "sf-spring-luncheon-2013-1.jpg", ""),
    "luncheon-2013-2": ("2018/06/MG_5240.jpg", "sf-spring-luncheon-2013-2.jpg", ""),
}

ALT = HERE / "alt.json"  # key: alt text, written from looking at each prepared picture

# key: (the old site's file, the name in Files)
PDFS = {
    "endless-summer-booklet": ("2023/07/EndlessSummer_ExhibitionBooklet.pdf", "endless-summer-exhibition-booklet.pdf"),
    "unfixed-book": ("2021/06/UnfixedInterior_spreadsNoFrame.pdf", "unfixed-the-entangled-works-of-chris-curreri-and-laurie-kang.pdf"),
    "auction-2019": ("2019/05/Auction-2019-catalogue-7x7-ONLINE.pdf", "smith-foundation-spring-luncheon-2019-auction-catalogue.pdf"),
}


def alt(key):
    """A picture's alt text: the logos' names, else what alt.json says."""
    written = IMAGES[key][2]
    if written:
        return written
    return json.loads(ALT.read_text()).get(key, "") if ALT.exists() else ""


def pixels(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)], capture_output=True, text=True).stdout
    vals = [int(l.split(":")[1]) for l in out.splitlines() if "pixel" in l]
    return tuple(vals) if len(vals) == 2 else (0, 0)


def web_copy(src, dst):
    """As artists-for-kids/files.py: JPEG (or PNG for a PNG logo), sRGB; over 3,000 px made smaller."""
    fmt = ["-s", "format", "png"] if dst.suffix == ".png" else ["-s", "format", "jpeg", "-s", "formatOptions", "85"]
    args = ["sips", *fmt, "--matchTo", SRGB]
    if max(pixels(src)) > 3000:
        args += ["-Z", "3000"]
    subprocess.run(args + [str(src), "--out", str(dst)], check=True, capture_output=True)


def prepare(media):
    media = pathlib.Path(media).expanduser()
    out = media / "upload"
    (out / "img").mkdir(parents=True, exist_ok=True)
    (out / "pdf").mkdir(parents=True, exist_ok=True)
    for key, (old, name, _alt) in IMAGES.items():
        dst = out / "img" / name
        if not dst.exists():
            web_copy(media / "files" / old, dst)
    for key, (old, name) in PDFS.items():
        dst = out / "pdf" / name
        if dst.exists():
            continue
        src = media / "files" / old
        if src.stat().st_size <= MAX_BYTES:
            dst.write_bytes(src.read_bytes())
            continue
        for dpi, quality in SHRINK_STEPS:  # the gentlest setting that fits (P-40)
            shrink_pdf(src, dst, dpi, quality)
            if dst.stat().st_size <= SHRINK_TARGET:
                print(f"{name}: {src.stat().st_size / 1e6:.1f} MB to {dst.stat().st_size / 1e6:.1f} MB at {dpi} dpi, quality {quality}")
                break
        else:
            raise RuntimeError(f"{name} is still over {SHRINK_TARGET} bytes")
    sizes = {n: pixels(out / "img" / n) for _, n, _ in IMAGES.values()}
    print(f"{len(sizes)} pictures, {len(PDFS)} PDFs in {out}")
    for n, (w, h) in sorted(sizes.items()):
        if max(w, h) < 1000:
            print(f"  small: {n} {w}x{h}")


def upload(media):
    out = pathlib.Path(media).expanduser() / "upload"
    created = json.loads(CREATED.read_text()) if CREATED.exists() else {}
    missing = [k for k in IMAGES if not alt(k)]
    if missing:
        raise SystemExit(f"alt text missing for {missing}")
    for ext, mime in ((".jpg", "image/jpeg"), (".png", "image/png")):
        todo = [(f"img:{k}", name, alt(k)) for k, (_old, name, _a) in IMAGES.items()
                if f"img:{k}" not in created and name.endswith(ext)]
        for i in range(0, len(todo), 20):
            created.update(upload_batch(todo[i:i + 20], out / "img", "IMAGE", mime))
            CREATED.write_text(json.dumps(created, indent=1, sort_keys=True))
            print(f"pictures ({ext}) {min(i + 20, len(todo))}/{len(todo)}", flush=True)
    pdfs = [(f"pdf:{k}", name, "") for k, (_old, name) in PDFS.items() if f"pdf:{k}" not in created]
    if pdfs:
        created.update(upload_batch(pdfs, out / "pdf", "FILE", "application/pdf"))
        CREATED.write_text(json.dumps(created, indent=1, sort_keys=True))
        print(f"PDFs {len(pdfs)}", flush=True)


URLS = """query Urls($ids: [ID!]!) {
  nodes(ids: $ids) {
    ... on MediaImage { id fileStatus image { url width height } }
    ... on GenericFile { id fileStatus url }
  }
}"""


def urls():
    created = json.loads(CREATED.read_text())
    ids = {v if isinstance(v, str) else v["id"]: k for k, v in created.items()}
    out = {}
    id_list = list(ids)
    for i in range(0, len(id_list), 50):
        for n in execute(URLS, {"ids": id_list[i:i + 50]})["nodes"]:
            url = (n.get("image") or {}).get("url") or n.get("url")
            out[ids[n["id"]]] = {"id": n["id"], "status": n["fileStatus"], "url": url}
            if n.get("image"):
                out[ids[n["id"]]].update(width=n["image"]["width"], height=n["image"]["height"])
    waiting = [k for k, v in out.items() if v["status"] != "READY" or not v["url"]]
    CREATED.write_text(json.dumps(out, indent=1, sort_keys=True))
    print(f"{len(out)} files, {len(waiting)} still processing: {waiting}")


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "prepare":
        prepare(sys.argv[2])
    elif step == "upload":
        upload(sys.argv[2])
    elif step == "urls":
        urls()
    else:
        raise SystemExit(__doc__)
