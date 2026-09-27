#!/usr/bin/env python3
"""The Artists for Kids site's pictures and PDFs, into the store's Files
(proposals/artists-for-kids-integration.md, steps 6 and 11; P-40).

  python3 files.py prepare <export folder>   web copies of the pictures and lesson covers, and copies
                                             under 19 MB of the PDFs over Shopify's 20 MB limit
  python3 files.py upload <export folder>    upload what isn't in Files yet; IDs to ../created/afk-files.json
  python3 files.py urls                      each uploaded file's address, into the same file
  python3 files.py revise <export folder>    after the design review (2026-09-27): the program guide's and
                                             Mini Monster's covers rendered from their PDFs' first page, the
                                             collage without its white border, the black bars cut from seven
                                             lesson covers (all replaced in place, same IDs), and the lesson
                                             covers' alt text cleared: each cover's title follows it (DS-58)
  python3 files.py replace <export folder>   upload fresh web copies over pictures already in Files
                                             (fileUpdate, same IDs): used once, 2026-09-27, when the
                                             first upload had enlarged the smaller pictures to 3,000 px

Pictures: a JPEG no more than 3,000 px on its long side, sRGB, quality 85, never cropped (as the
collection's, collection/images.py). Alt text is written here from looking at each picture; the old
site's was mostly the file's name. The pictures the store already has (the Artists for Kids page's,
the programme cards') aren't uploaded again.

PDFs over 20 MB get a smaller copy with collection/images.py's shrink_pdf: each page's picture
resampled, the text left as it is. Five need it (P-40): the gallery checks they read well.

Lesson covers are each video's own thumbnail, from the gallery's YouTube channel (lessons.py youtube).

Uploads go through the Shopify CLI (`shopify store execute`), as the collection's did: a staged upload,
then fileCreate. Nothing is uploaded twice: the created file keeps each key.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "collection"))
from images import execute, shrink_pdf, upload_batch  # noqa: E402

CREATED = HERE.parent / "created" / "afk-files.json"
SRGB = "/System/Library/ColorSync/Profiles/sRGB Profile.icc"
AGENT = "Mozilla/5.0 (Gordon Smith Gallery site move, read-only)"
ASSETS = "https://artistsforkids.sd44.ca/media/nvsd/nvsd---schools/nvsd---artists-for-kids/content-assets/"
MAX_BYTES = 20_000_000
SHRINK_TARGET = 19_000_000
SHRINK_STEPS = [(200, 75), (150, 70), (150, 60), (130, 60), (120, 55), (110, 50), (100, 50)]

# key: (the old site's file, the name in Files, alt text)
IMAGES = {
    "team": ("AFK-Staff-(1).jpg", "afk-team.jpg",
             "The four members of the Artists for Kids team, each holding art materials, in an orange-toned photo"),
    "after-school-art": ("after_school_art_afk_25.jpg", "afk-after-school-art.jpg",
                         "Three students in orange aprons painting at a table in an After School Art class"),
    "program-guide": ("2026-2027-Program-Cover-Image.jpg", "afk-program-guide-2026-2027.jpg",
                      "Cover of the Gordon Smith Gallery 2026-27 program guide: students with their sculptures, and the Gallery, Smith Foundation and Artists for Kids logos"),
    "air-2026": ("photoenrichment2026-55-crop.jpg", "afk-artists-in-residence-2026.jpg",
                 "Artist Rebecca Bair talks with students sitting on the ground in a courtyard during her 2026 Artist in Residence workshop"),
    "paradise-valley": ("PVSSVA.jpeg", "afk-paradise-valley-camp.jpg",
                        "Nine photos from Paradise Valley camp: campers drawing at picnic tables, on a dock, in a canoe and painting on the grass in the forest"),
    "studio-art-academy": ("thumbnail_IMG_0161.jpg", "afk-studio-art-academy.jpg",
                           "Students painting at tables in a classroom studio, seen from above"),
    "air-2026-samuel-roy-bois": ("AIR2026SamuelRoyBois.jpeg", "afk-air-2026-samuel-roy-bois.jpg",
                                 "Samuel Roy-Bois. Artist in residence, November 2026"),
    "air-2027-amelia-butcher": ("AIR2027AMELIABUTCHER.jpeg", "afk-air-2027-amelia-butcher.jpg",
                                "Amelia Butcher. Artist in residence, February 2027"),
    "air-2027-mark-johnsen": ("AIR2027MARKJOHNSEN.jpeg", "afk-air-2027-mark-johnsen.jpg",
                              "Mark Johnsen. Artist in residence, April 2027"),
    "air-2027-rebecca-bair": ("AIR2027REBECCABAIR.jpeg", "afk-air-2027-rebecca-bair.jpg",
                              "Rebecca Bair. Artist in residence, May 2027"),
    "air-2025-sara-jeanne-bourget": ("AIR2025_SARAJEANNEBOURGET.jpeg", "afk-air-2025-sara-jeanne-bourget.jpg",
                                     "Sara-Jeanne Bourget. Artist in residence, November 2025"),
    "air-2026-marlene-yuen": ("AIR-2026-MARLENE-YUEN.jpeg", "afk-air-2026-marlene-yuen.jpg",
                              "Marlene Yuen. Artist in residence, January 2026"),
    "air-2026-amelia-butcher": ("AIR-2026-AMELIA-BUTCHER.jpeg", "afk-air-2026-amelia-butcher.jpg",
                                "Amelia Butcher. Artist in residence, February 2026"),
    "air-2026-rebecca-bair": ("AIR-2026-REBECCA-BAIR.jpeg", "afk-air-2026-rebecca-bair.jpg",
                              "Rebecca Bair. Artist in residence, May 2026"),
    "amelia-butcher-studio": ("Amelia-Butcher2.jpg", "afk-amelia-butcher-studio.jpg",
                              "Amelia Butcher pouring clay slip into a mould in her studio"),
    "amelia-butcher-workshop": ("thumbnail_Image4.jpg", "afk-amelia-butcher-workshop-2026.jpg",
                                "A student pressing shapes into a clay slab during Amelia Butcher's 2026 workshop"),
    "mark-johnsen-studio": ("mark.jpg", "afk-mark-johnsen-studio.jpg",
                            "Mark Johnsen holding up a print beside a press in a printmaking studio"),
    "becky-bair-workshop-1": ("photoenrichment2026-76.jpg", "afk-becky-bair-workshop-1.jpg",
                              "Rebecca Bair speaking to a long table of students in the Shadbolt Studio"),
    "becky-bair-workshop-2": ("photoenrichment2026-23.jpg", "afk-becky-bair-workshop-2.jpg",
                              "Blue cyanotype prints of leaves soaking in a tray of water"),
    "becky-bair-workshop-3": ("photoenrichment2026-18.jpg", "afk-becky-bair-workshop-3.jpg",
                              "Rebecca Bair kneeling with students as they arrange cyanotype papers outdoors"),
    "guide-art-camp": ("Lessons-from-Art-Camp-Sara-Jeanne-Bourget-2025.jpeg", "afk-guide-lessons-from-art-camp.jpg",
                       "Cover: six charcoal drawings of bark and stone textures under the title Lessons from Art Camp"),
    "guide-charcoal": ("2d6d2e11ffa6fd3a.jpg", "afk-guide-charcoal-stencil-prints.jpg",
                       "Cover: grey charcoal stencil prints of stones scattered across a white page"),
    "guide-mail-art": ("71298dd83f4faf14.jpg", "afk-guide-mail-art.jpg",
                       "Cover: a collage of patterned papers with white paper tree shapes"),
    "guide-mini-monster": ("0984dc8710d7dd15.jpg", "afk-guide-mini-monster.jpg",
                           "Cover: a small gold monster sculpture with googly eyes and paper wings"),
    "guide-zine-collage": ("bf3c11e35d0cbb90.png", "afk-guide-zine-collage.jpg",
                           "Cover: two zine pages of collaged photos and drawings, headed Step 1 set the table and Step 2 gather ingredients"),
    "guide-zine-frottage": ("162eea7b58527942.png", "afk-guide-zine-frottage.jpg",
                            "Cover: a hand-drawn zine, Division 5 Class Menu, with a rubbing of chicken and rice"),
    "guide-paper-mural": ("ff90d1444a56b24a2.jpg", "afk-guide-paper-mural.jpg",
                          "A colourful paper mural of creatures and flowers cut from painted paper"),
    "guide-narrative-scrolls": ("6d5818c713d398f8.png", "afk-guide-narrative-scrolls.jpg",
                                "Cover: a detailed black ink drawing of mushrooms and swirls on grey paper, with pens"),
    "guide-fragmented-faces": ("71f0ebdf152b985b.png", "afk-guide-fragmented-faces.jpg",
                               "Cover: a portrait built from bold coloured shapes in pastel and paint"),
    "kit-clay": ("d2d71657fc1438d4.jpg", "afk-kit-clay.jpg",
                 "A student pressing a tool into a clay tile at a classroom desk"),
    "kit-collagraph": ("55e2ce560f253065.jpg", "afk-kit-collagraph.jpg",
                       "A collagraph print in blue and green lifted from its printing plate on a small press"),
    "kit-trace-monotype": ("edba8b2f336d11a5.jpg", "afk-kit-trace-monotype.jpg",
                           "A student tracing over a printed self portrait photo to make a monotype"),
    "kit-gel-plate": ("d95572f990665486.jpg", "afk-kit-gel-plate.jpg",
                      "Colourful gel plate monoprints of shapes laid out on a table, with a four-panel comic"),
    "kit-clay-tile": ("27d0ab54f9b5a107.jpg", "afk-kit-clay-tile.jpg",
                      "A painted clay tile covered in pressed fossil shapes, shells and gears"),
    "kit-clay-log": ("7ff928e9246b1338.jpg", "afk-kit-clay-log.jpg",
                     "A clay log sculpture with mushrooms and a snail growing from it"),
    "kit-collagraph-tools": ("e5342880e6dbe827.jpg", "afk-kit-collagraph-tools.jpg",
                             "A tray of brayers and carving tools with a small print of stones"),
    "lesson-foam-butterflies": ("4e892070544adc5a.jpg", "afk-lesson-foam-butterflies.jpg",
                                "Cover: a dark blue butterfly printed from a foam plate"),
    "lesson-garbage-press": ("55e2ce560f253065.jpg", "afk-lesson-garbage-press.jpg",
                             "Cover: a collagraph print in blue and green lifted from its printing plate on a small press"),
    "lesson-lego-press": ("14af1d6a669faa57.jpg", "afk-lesson-lego-press.jpg",
                          "Cover: winding prints made with Lego bricks in black, green, red and blue"),
    "lesson-textured-landscapes": ("ef0e40607d79f544.jpg", "afk-lesson-textured-landscapes.jpg",
                                   "Cover: two textured landscape prints in black, green and gold"),
    "lesson-trace-monotype": ("ea7634961ddc78be.jpg", "afk-lesson-trace-monotype.jpg",
                              "Cover: a trace monotype self portrait in profile, lines in red, blue and black"),
    "kit-trace-monotype-student": ("19ca6cfdcb322b52.jpg", "afk-kit-trace-monotype-student.jpg",
                                   "A student painting a pink collage self portrait"),
    "lesson-gel-plate": ("05531342846be523.png", "afk-lesson-gel-plate.jpg",
                         "Cover: a folding four-panel comic made with gel plate monoprints"),
    "event-clay-kit": ("Clay-Kit-Image.jpeg", "afk-clay-kit-workshop.jpg",
                       "Clay tiles pressed with fossil and shell shapes, drying on a board"),
}

# key: (the old site's address, after ASSETS; the name in Files)
PDFS = {
    "guide-art-camp": ("documents/learn/learning-guides/Lessons-from-Art-Camp_Sara-Jeanne-Bourget_2025.pdf", "afk-lessons-from-art-camp-sara-jeanne-bourget-2025.pdf"),
    "guide-charcoal": ("documents/learn/learning-guides/Charcoal-Stencil-Prints-Inspired-by-Sara-Jeanne-Bourget---Grades-8-12.pdf", "afk-charcoal-stencil-prints-grades-8-12.pdf"),
    "guide-mail-art": ("documents/learn/learning-guides/A-Mail-Art-Collaboration---Lesson-by-Clare-Yow---Grades-K-12.pdf", "afk-mail-art-collaboration-grades-k-12.pdf"),
    "guide-mini-monster": ("documents/learn/learning-guides/Make-Mini-Monster---Lesson-by-Lexy-Ho-Tai---Grades-K-12.pdf", "afk-make-mini-monster-grades-k-12.pdf"),
    "guide-zine-collage": ("documents/learn/learning-guides/Collage-Food-for-Thought_Zine-Lesson_AFK.pdf", "afk-zine-lesson-collage.pdf"),
    "guide-zine-frottage": ("documents/learn/learning-guides/Frottage-Food-for-Thought_Zine-Lesson_AFK.pdf", "afk-zine-lesson-frottage.pdf"),
    "guide-narrative-scrolls": ("documents/learn/learning-guides/Visual-Narrative-Scrolls-Inspired-by-Sean-Karemaker---Grades-8-12.pdf", "afk-visual-narrative-scrolls-grades-8-12.pdf"),
    "guide-fragmented-faces": ("documents/learn/learning-guides/Fragmented-Faces---Portraits-in-Pastel-and-Paint---K-3.pdf", "afk-fragmented-faces-grades-k-3.pdf"),
    "kit-clay-tile": ("documents/learn/learning-kits/AFK-Clay-Kit_Lesson-Plan_Materials-List-(1).pdf", "afk-clay-tile-kit-lesson-plan.pdf"),
    "kit-clay-log": ("documents/learn/learning-kits/AFK-Clay-Kit_Log-Lesson-Plan_Materials-List.pdf", "afk-clay-log-kit-lesson-plan.pdf"),
    "lesson-foam-butterflies": ("documents/learn/learning-kits/AFK-Collagraph-Kit_Lesson-Plan_Foam-Butterflies.pdf", "afk-collagraph-lesson-1-foam-butterflies.pdf"),
    "lesson-garbage-press": ("documents/learn/learning-kits/AFK-Collagraph-Kit_Lesson-Plan_Garbage-Press.pdf", "afk-collagraph-lesson-2-garbage-press.pdf"),
    "lesson-lego-press": ("documents/learn/learning-kits/AFK-Collagraph-Kit_Lesson-Plan_Lego-Press.pdf", "afk-collagraph-lesson-3-lego-press.pdf"),
    "lesson-textured-landscapes": ("documents/learn/learning-kits/AFK-Collagraph-Kit_Lesson-Plan_Textured-Landscapes-Inspired-by-Ted-Harrison.pdf", "afk-collagraph-lesson-4-textured-landscapes.pdf"),
    "lesson-trace-monotype": ("documents/learn/learning-kits/AFK_-Trace-Monotype-Kit_Lesson-Plan_Self-Portrait.pdf", "afk-trace-monotype-kit-lesson-plan.pdf"),
    "lesson-gel-plate": ("documents/learn/learning-kits/AFK_Gel-Plate-Monoprint-Kit_Lesson-Plan.pdf", "afk-gel-plate-monoprint-kit-lesson-plan.pdf"),
    "award-shadbolt": ("documents/Jack_Shadbolt_Multiple_Arts_Excellence_Award_Requirements-2026.pdf", "afk-jack-shadbolt-award-requirements-2026.pdf"),
    "award-bateman": ("documents/Robert_Bateman_Future_Teacher_Scholarship_Requirements-2026.pdf", "afk-robert-bateman-award-requirements-2026.pdf"),
    "award-gordon-smith": ("documents/Gordon_Smith_Outstanding_Visual_Artist_Scholarship_Requirements-2026.pdf", "afk-gordon-smith-award-requirements-2026.pdf"),
    "annual-report": ("documents/Annual-Report-2024-25-FINAL.pdf", "afk-annual-report-2024-2025.pdf"),
    "program-guide": ("documents/program-guides/2026-2027-GSG_AFK_Program-Guide.pdf", "gordon-smith-gallery-program-guide-2026-2027.pdf"),
}


def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=300) as r, open(path, "wb") as f:
        shutil.copyfileobj(r, f)


def pixels(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)], capture_output=True, text=True).stdout
    return [int(line.split(":")[1]) for line in out.splitlines() if "pixel" in line]


def web_copy(src, dst):
    """JPEG, sRGB, quality 85 (macOS sips); a picture over 3,000 px on its long side is made smaller,
    a smaller one keeps its size (sips -Z alone would enlarge it)."""
    args = ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85", "--matchTo", SRGB]
    if max(pixels(src)) > 3000:
        args += ["-Z", "3000"]
    subprocess.run(args + [str(src), "--out", str(dst)], check=True, capture_output=True)


def prepare(export):
    export = pathlib.Path(export)
    out = export / "upload"
    (out / "img").mkdir(parents=True, exist_ok=True)
    (out / "pdf").mkdir(parents=True, exist_ok=True)
    for key, (old, name, _alt) in IMAGES.items():
        dst = out / "img" / name
        if not dst.exists():
            web_copy(export / "img" / old, dst)
    lessons = json.loads((export / "youtube.json").read_text())
    for lesson in lessons:
        dst = out / "img" / f"afk-lesson-cover-{lesson['handle']}.jpg"
        if not dst.exists():
            web_copy(export / "covers" / f"{lesson['handle']}.jpg", dst)
    shrunk = {}
    for key, (path, name) in PDFS.items():
        dst = out / "pdf" / name
        if dst.exists():
            continue
        original = out / "pdf" / ("original-" + name)
        if not original.exists():
            download(ASSETS + path, original)
        size = original.stat().st_size
        if size <= MAX_BYTES:
            original.rename(dst)
            continue
        for dpi, quality in SHRINK_STEPS:
            pages = shrink_pdf(original, dst, dpi, quality)
            if dst.stat().st_size <= SHRINK_TARGET:
                shrunk[name] = {"from_bytes": size, "to_bytes": dst.stat().st_size, "dpi": dpi, "quality": quality, "pages": pages}
                print(f"{name}: {size / 1e6:.1f} MB to {dst.stat().st_size / 1e6:.1f} MB at {dpi} dpi, quality {quality}", flush=True)
                break
        else:
            raise RuntimeError(f"{name} stays over {SHRINK_TARGET} bytes")
    if shrunk:
        (HERE / "shrunk-pdfs.json").write_text(json.dumps(shrunk, indent=1))


def cover_alt(lesson_title):
    """None: the lesson's title follows its cover, so the cover is decorative (DS-58)."""
    return ""


def upload(export):
    export = pathlib.Path(export)
    out = export / "upload"
    created = json.loads(CREATED.read_text()) if CREATED.exists() else {}
    lessons = {l["handle"]: l for l in json.loads((export / "lessons.json").read_text())}
    todo = [(f"img:{k}", name, alt) for k, (_old, name, alt) in IMAGES.items() if f"img:{k}" not in created]
    for handle, lesson in lessons.items():
        key = f"cover:{handle}"
        if key not in created:
            todo.append((key, f"afk-lesson-cover-{handle}.jpg", cover_alt(lesson["title"])))
    for i in range(0, len(todo), 20):
        created.update(upload_batch(todo[i:i + 20], out / "img", "IMAGE", "image/jpeg"))
        CREATED.write_text(json.dumps(created, indent=1, sort_keys=True))
        print(f"pictures {min(i + 20, len(todo))}/{len(todo)}", flush=True)
    pdfs = [(f"pdf:{k}", name, "") for k, (_path, name) in PDFS.items() if f"pdf:{k}" not in created]
    for i in range(0, len(pdfs), 5):
        created.update(upload_batch(pdfs[i:i + 5], out / "pdf", "FILE", "application/pdf"))
        CREATED.write_text(json.dumps(created, indent=1, sort_keys=True))
        print(f"PDFs {min(i + 5, len(pdfs))}/{len(pdfs)}", flush=True)


REPLACE = """mutation Replace($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) { files { id } userErrors { field message } }
}"""


def replace(export):
    """New web copies of every picture, uploaded over the old ones: staged upload, then fileUpdate
    with the new source. The IDs, names and alt text stay."""
    from images import STAGE
    export = pathlib.Path(export)
    folder = export / "upload" / "img"
    created = json.loads(CREATED.read_text())
    lessons = json.loads((export / "youtube.json").read_text())
    todo = [(f"img:{k}", name, export / "img" / old) for k, (old, name, _alt) in IMAGES.items()]
    todo += [(f"cover:{l['handle']}", f"afk-lesson-cover-{l['handle']}.jpg", export / "covers" / f"{l['handle']}.jpg") for l in lessons]
    for _key, name, src in todo:
        web_copy(src, folder / name)
    for i in range(0, len(todo), 20):
        batch = todo[i:i + 20]
        stage = execute(STAGE, {"input": [{"filename": name, "mimeType": "image/jpeg", "resource": "IMAGE", "httpMethod": "POST",
                                           "fileSize": str((folder / name).stat().st_size)} for _k, name, _s in batch]})["stagedUploadsCreate"]
        if stage["userErrors"]:
            raise RuntimeError(stage["userErrors"])
        files = []
        for (key, name, _src), t in zip(batch, stage["stagedTargets"]):
            args = ["curl", "-s", "-f", "-o", "/dev/null", "-w", "%{http_code}"]
            for prm in t["parameters"]:
                args += ["-F", f"{prm['name']}={prm['value']}"]
            args += ["-F", f"file=@{folder / name}", t["url"]]
            code = subprocess.run(args, capture_output=True, text=True).stdout
            if not code.startswith("2"):
                raise RuntimeError(f"upload of {name} returned {code}")
            files.append({"id": created[key]["id"], "originalSource": t["resourceUrl"]})
        made = execute(REPLACE, {"files": files})["fileUpdate"]
        if made["userErrors"]:
            raise RuntimeError(made["userErrors"])
        print(f"replaced {min(i + 20, len(todo))}/{len(todo)}", flush=True)


def revise(export):
    """Replace the revised pictures in place and clear the lesson covers' alt text."""
    from images import STAGE
    export = pathlib.Path(export)
    folder = export / "revise"
    created = json.loads(CREATED.read_text())
    todo = [("img:program-guide", "afk-program-guide-2026-2027.jpg"), ("img:guide-mini-monster", "afk-guide-mini-monster.jpg"),
            ("img:paradise-valley", "afk-paradise-valley-camp.jpg")]
    todo += [(f"cover:{f.stem.replace('afk-lesson-cover-', '')}", f.name) for f in sorted(folder.glob("afk-lesson-cover-*.jpg"))]
    stage = execute(STAGE, {"input": [{"filename": name, "mimeType": "image/jpeg", "resource": "IMAGE", "httpMethod": "POST",
                                       "fileSize": str((folder / name).stat().st_size)} for _k, name in todo]})["stagedUploadsCreate"]
    if stage["userErrors"]:
        raise RuntimeError(stage["userErrors"])
    files = []
    for (key, name), t in zip(todo, stage["stagedTargets"]):
        args = ["curl", "-s", "-f", "-o", "/dev/null", "-w", "%{http_code}"]
        for prm in t["parameters"]:
            args += ["-F", f"{prm['name']}={prm['value']}"]
        args += ["-F", f"file=@{folder / name}", t["url"]]
        code = subprocess.run(args, capture_output=True, text=True).stdout
        if not code.startswith("2"):
            raise RuntimeError(f"upload of {name} returned {code}")
        files.append({"id": created[key]["id"], "originalSource": t["resourceUrl"]})
    made = execute(REPLACE, {"files": files})["fileUpdate"]
    if made["userErrors"]:
        raise RuntimeError(made["userErrors"])
    print(f"replaced {len(files)}", flush=True)
    covers = [{"id": v["id"], "alt": ""} for k, v in created.items() if k.startswith("cover:")]
    for i in range(0, len(covers), 25):
        made = execute(REPLACE, {"files": covers[i:i + 25]})["fileUpdate"]
        if made["userErrors"]:
            raise RuntimeError(made["userErrors"])
    print(f"cleared alt on {len(covers)} covers", flush=True)


URLS = """query($ids: [ID!]!) { nodes(ids: $ids) {
  ... on MediaImage { id fileStatus image { url width height } }
  ... on GenericFile { id fileStatus url } } }"""


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
    elif step == "replace":
        replace(sys.argv[2])
    elif step == "revise":
        revise(sys.argv[2])
