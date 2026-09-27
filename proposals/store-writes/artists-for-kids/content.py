#!/usr/bin/env python3
"""The Artists for Kids content for the store (proposals/artists-for-kids-integration.md): the 18 new pages
and their fields, the cards and card groups, the educators' events, and the lessons. load.py writes the
entries through the CLI; the pages, page fields and menu go through the Shopify connector:

  python3 content.py pages                 pageCreate variables for the new pages (P-35)
  python3 content.py page-fields <n>       metafieldsSet variables, batch n (25 to a batch), from 0
  python3 content.py page-fields-count     how many batches
  python3 content.py menu                  menuUpdate variables for the review menu (P-33)
  python3 content.py check                 prints every page's staged text, for reading

Text is the old site's, moved as written (AGENTS.md, "Gallery-facing work"). What changed, and why:

- Schedules, fees, forms, registration dates and cancellation policies for After School Art and the
  camps stay on the district's site beside their forms (P-31); each page's button goes there.
- "Read more" and "Register" buttons become links on the card title or the page's button. Sentences that
  pointed at the old buttons ("See below for info and to register!", "Click below ...") are left out.
- "AFK" in titles, labels and headings is written out (P-39); body text keeps it for the gallery to
  approve.
- The residency pages link to the artist's page on this site, not their website (P-38). Mark Johnsen's
  page repeated his biography under his 2024 workshop, and an empty "Photos From the Workshop" heading:
  both are left out.
- Email addresses become links. Two missing spaces are put back ("artist,Sara-Jeanne", "theexhibition").
  Links to PDFs in page text say "(PDF)", as the site's other pages do.
- The residencies' card titles put the name first ("Becky Bair, Spring 2027"); the old site's
  "Spring 2027 | Becky Bair" wrapped with the bar at the start of a line.
- The Gallery Program page doesn't repeat Collect, Assemble, Gather's text: it links to the exhibition.
  The self-guided tour instructions (a PDF on the district's old server, which no longer answers) wait
  for the gallery to send the file.
- Creating a Paper Mural with Sandeep Johal has a cover and no PDF on the old site: its card is made but
  kept out of the group until the file comes.

Pages get the live theme's On Now template name until release (`current-on-now-exhibition`), the only
live template besides Artists that shows a page's title and nothing else; the new theme has no template
by that name, so it shows them with its standard page template. At release the release script gives
them the programme template (the residency pages the standard one).
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
CREATED = HERE.parent / "created"
SITE = "https://gordonsmithgallery.com"
BRIDGE_TEMPLATE = "current-on-now-exhibition"

# Sign-up and giving addresses (P-31, P-32): registration stays where it is.
ASA_REG = "https://artistsforkids.sd44.ca/learn/after-school-art/"
CAMPS_REG = "https://artistsforkids.sd44.ca/learn/spring--summer-day-camps/"
PV_REG = "https://artistsforkids.sd44.ca/learn/paradise-valley-summer-camps/"
GALLERY_BOOKING = "https://outlook.office.com/book/ArtistsforKidsFallGalleryProgram2223@sd44O365.onmicrosoft.com/?ismsaljsauthenabled"
FORMS = "https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=RtUantX4ek-GDic4Z6NToCanCe_oocJFsBRzMm8rYAZ"
CLAY_KIT_FORM = FORMS + "UN1VURFA5VFRNR0RORFpGWTBXODUzWUROSS4u"
KIT_FORM = FORMS + "UOElXRDJCWU02RFlRTDVKSE1POExEWVhLNi4u"
CLAY_WORKSHOP_FORM = FORMS + "UNVJBSk1ERDJVTU5WMzBMR1hSM01EUEFMSy4u"
PROD_OCT23_FORM = FORMS + "URTIxOE9SRllIN0dEMUlWUEY3N1U3MTM2Ty4u"
CANADAHELPS = "https://www.canadahelps.org/en/dn/66477"
SCHOOLCASH = "https://sd44.schoolcashonline.com/Fee/Details/299/69/false/true"
EMAIL = '<a href="mailto:artistsforkids@sd44.ca">artistsforkids@sd44.ca</a>'

# Entries already in the store.
EXHIBITIONS = {"collect-assemble-gather": "gid://shopify/Metaobject/608352043305",
               "against-the-latitude-of-progress": "gid://shopify/Metaobject/608352108841"}
AFK_PAGE = "gid://shopify/Page/155720810793"
EXISTING_IMAGES = {  # already in Files
    "gallery-program": 45746709102889,   # KMH853740.jpg, the Artists for Kids page's hero
    "day-camps": 45746720669993,         # pvssa_25.jpg, the day camps card
    "card-after-school-art": 45746713854249,
}
EXPLORE_CREATE_CARD = "gid://shopify/Metaobject/608366526761"


def files():
    return json.loads((CREATED / "afk-files.json").read_text())


def img(key):
    """A picture's ID, from its key in files.py, or one already in Files."""
    if key in EXISTING_IMAGES:
        return f"gid://shopify/MediaImage/{EXISTING_IMAGES[key]}"
    return files()[key if ":" in key else f"img:{key}"]["id"]


def pdf(key):
    """A PDF's address on the site's own domain, so links to it aren't marked as leaving the site."""
    url = files()[f"pdf:{key}"]["url"]
    return f"{SITE}/cdn/shop/files/{url.split('/')[-1].split('?')[0]}"


def pdf_path(key):
    """The same, as a path, for links in page text (which the theme doesn't rewrite)."""
    return pdf(key).replace(SITE, "")


def link(url, text=""):
    return json.dumps({"text": text, "url": url}, ensure_ascii=False)


def page_url(handle):
    return f"{SITE}/pages/{handle}"


def figure(key, caption=None, artwork=False):
    """A picture in page text, as the Artists for Kids page's are: its Files address, size and alt text."""
    f = files()[f"img:{key}"]
    import files as filesmod  # the alt text lives with the picture
    alt = filesmod.IMAGES[key][2]
    url, w, h = f["url"], f["width"], f["height"]
    if w > 1440:
        h, w = round(h * 1440 / w), 1440
        url += "&width=1440"
    cls = ' class="gs-figure--artwork"' if artwork else ""
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure{cls}><img src="{html.escape(url)}" alt="{html.escape(alt)}" width="{w}" height="{h}" loading="lazy">{cap}</figure>'


def video(video_id, caption):
    return (f'<figure><iframe src="https://www.youtube-nocookie.com/embed/{video_id}" title="{html.escape(caption)}" '
            f'width="560" height="315" loading="lazy" allowfullscreen></iframe><figcaption>{caption}</figcaption></figure>')


def artist(handle, name):
    return f'<a href="/pages/artists/{handle}">{name}</a>'


CAG = '<a href="/pages/exhibitions/collect-assemble-gather"><em>Collect, Assemble, Gather</em></a>'


# ---------------------------------------------------------------------------------------------------
# Pages. Each: title, template after release, fields, staged text (custom.release_body, DS-39).
# ---------------------------------------------------------------------------------------------------

def pages():
    return [
        {"handle": "classes-and-camps", "title": "Classes and camps", "template": "programme",
         "groups": ["afk-community-programs", "afk-also-for-families"]},
        {"handle": "schools-and-teachers", "title": "Schools and teachers", "template": "programme",
         "groups": ["afk-school-programs", "afk-learning-resources"]},
        {"handle": "after-school-art", "title": "After School Art", "template": "programme",
         "hero": "after-school-art", "cta": (ASA_REG, "Classes and registration"),
         "body": "\n".join([
             "<p>Artists for Kids offers After School Art classes for students each Fall, Winter and Spring term.</p>",
             "<p>Led by BC certified art specialist teachers and assisted by secondary art students, our classes provide the opportunity to build skills and foster creative growth within the visual arts. Students will have the opportunity to expand their artistic abilities in a multitude of different mediums, including painting, felting, printmaking, and sculpting.</p>",
             "<p>Classes vary in duration, price, and medium. All art materials are included in the price of the program.</p>",
             "<h2>Important Notes</h2>",
             "<ul>",
             "<li>Artists for Kids does not provide supervision before class start times. Parents/Guardians are responsible for the supervision of their child from the end of the school day until the start of the After School Art class.</li>",
             "<li>Class start times do not change on professional development days or early dismissal days.</li>",
             f"<li>Artists for Kids is unable to provide 1:1 support. If you child requires support at school, or will be attending classes with a support worker, please contact {EMAIL} as soon as possible after registering.</li>",
             "<li>A limited number of bursaries of up to 50% of program fees are available for those in need of financial support. In an effort to support as many families as possible, there is a limit of one bursary per child, per term for After School Art classes. Please contact Artists for Kids for more information on bursaries.</li>",
             "</ul>"])},
        {"handle": "day-camps", "title": "Spring & Summer Day Camps", "template": "programme",
         "hero": "day-camps", "caption": "Photo by Khim Mata Hipol", "cta": (CAMPS_REG, "Camp dates and registration"),
         "body": "<p>Students enjoy a week full of studio art activities including drawing, painting and printmaking taught by BC certified art specialist teachers. Each week is unique and campers learn in small cohorts. Campers experiment with many art materials and techniques while having opportunity to explore outdoor art making and recreation time.</p>"},
        {"handle": "paradise-valley-summer-camp", "title": "Paradise Valley Summer Camps", "template": "programme",
         "cta": (PV_REG, "This year's camp and registration"),
         "body": "\n".join([
             "<p><strong>5 days, 4 nights, inclusive</strong></p>",
             "<p>Young artists ages 9 - 15 will explore their surroundings in the beautiful setting of Paradise Valley. This environment provides an ideal source to explore concepts of form and colour. Students will receive in-depth instruction in collage, drawing, painting and printmaking. Working in small studio groups, teachers support individual skill development and artistic voice. This week long camp is thoughtfully balanced with outdoor recreation and studio time.</p>",
             figure("paradise-valley"),
             "<h2>Bursaries</h2>",
             f"<p>Bursaries are available for families in need of financial support. Please contact {EMAIL} for more information.</p>",
             "<h2>Past camps</h2>",
             video("-by8rt8rGvM", "Sara Jean Bourget was the visiting Artist In Residence in July 2025. Campers focused on drawing and printmaking."),
             video("C7jmm9VTn6g", "Paradise Valley Summer School of Visual Art Camp 2024 with artist Samuel Roy-Bois"),
             video("bExdIeVLnLg", "Paradise Valley Summer School of Visual Art Camp 2023 with artist Charlene Vickers"),
             video("cBllGmwNrgw", "Paradise Valley Summer School of Visual Art Camp 2022 with artist Annie Canto")])},
        {"handle": "gallery-program", "title": "Gallery Program", "template": "programme",
         "hero": "gallery-program", "caption": "Photo by Khim Mata Hipol, Spring 2025 Gallery Program.",
         "cta": (GALLERY_BOOKING, "Register a Grade 5 class"),
         "body": "\n".join([
             "<p>Artists for Kids' Gallery Program brings contemporary Canadian Art to a class full of eager young people which introduces the students to the art and culture of our country. Our Gallery Program offers students a deep, engaged dive into responding to and making art. Classes spend time in both the gallery and in the studio making work that responds to the exhibition they have studied in the gallery. All sessions are co-taught by the classroom teacher and an art expert teacher provided by Artists for Kids.</p>",
             "<h2>Grade 5 Gallery Program | Fall 2026 - Winter 2027</h2>",
             f"<p>We are excited to welcome Grade 5 classes to the Gordon Smith Gallery of Canadian Art for the Fall 2026 exhibition {CAG}. Teachers can sign up for a full-day gallery visit during which Artists for Kids art educators will lead classes in an interactive tour of the exhibition and a hands-on artmaking activity. Classes can visit from 9:30am - 2:30pm on select dates from October to February.</p>",
             "<p>The program fee for North Vancouver School District classes is covered by NVSD.</p>",
             "<p><strong>North Vancouver School District</strong> classes can register September 11, 2026.</p>",
             f'<p><a href="{html.escape(GALLERY_BOOKING)}">Register</a></p>',
             "<h2>Out of District Schools</h2>",
             "<p>Registration for <strong>out-of-district schools</strong> opens September 24th, 2026.<br>TOUR + WORKSHOP (4 hours of instructional time plus 1 hour break time)<br>The fee for out-of-district schools: $500</p>",
             f"<p>Please email {EMAIL} or call to inquire about availability.</p>",
             "<h2>Self-Guided Tours of <em>Collect, Assemble, Gather</em></h2>",
             "<p>Artists for Kids invites K-12 teachers to use the Gordon Smith Gallery as their classroom, by booking a time to bring a class for a half day self-guided tour at our spring exhibition, <em>One Hundred Artists Deep</em>.</p>",
             "<p>This is a unique opportunity for your students to engage directly with diverse works by Canadian artists and to learn through the lens of the arts.</p>",
             "<p>Teachers can book self-guided tour slots (morning or afternoon) that are available on select dates in April through June.</p>",
             "<p>We encourage teachers to attend an orientation of <em>Collect, Assemble, Gather</em> prior to visiting with your class.</p>",
             "<p><strong>Orientation for teachers will take place on September 28th at 1:00 - 3:30pm.</strong></p>",
             "<p>Class visits can be booked at the button below or by calling 604-903-3798.</p>",
             "<h2>Spring K - 12 Gallery Program 2027</h2>",
             "<p>We are excited to welcome Grade 5 classes to the Gordon Smith Gallery of Canadian Art for the Fall 2026 exhibition <em>Collect, Assemble, Gather.</em> Teachers can sign up for a half-day gallery visits. Artists for Kids art educators will lead classes in an interactive tour of the exhibition and a hands-on artmaking activity. Classes can visit from 9:30am-11:45am or 12:30pm-2:30pm on select dates from September to February.</p>",
             "<p>Registration for <strong>North Vancouver School District schools</strong> is available by clicking the <strong>Register</strong> button below. The program fee for North Vancouver School District classes is covered by NVSD.</p>",
             "<p><em><strong>Registration Opens February 24th, 2027</strong></em></p>"])},
        {"handle": "artists-in-residence", "title": "Artists-in-Residence", "template": "programme",
         "hero": "air-2026", "caption": "Photo by Khim Mata Hipol",
         "groups": ["afk-air-2026-2027", "afk-air-2025-2026"],
         "body": "\n".join([
             "<p>The Artists in Residence Program brings together artists, teachers, and students. From ceramics and painting to collage and photography, this vital program provides full-day, skill specific training that gives young artists the rare opportunity to immerse themselves in critical thinking and art making. Students who are nominated by their school district teachers have the opportunity to step outside the regular classroom stream to work closely with a professional artist at the Artists for Kids studios.</p>",
             "<p>Past Artists In Residence include " + ", ".join([
                 artist("gordon-smith", "Gordon Smith"), artist("kenojuak-ashevak", "Kenojuak Ashevak"),
                 artist("george-littlechild", "George Littlechild"), artist("rodney-graham", "Rodney Graham"),
                 artist("gu-xiong", "Gu Xiong"), artist("russna-kaur", "Russna Kaur"), artist("karen-zalamea", "Karen Zalamea")])
             + ", and " + artist("angela-george", "Angela George") + ", amongst many others.</p>"])},
        {"handle": "artist-in-residence-amelia-butcher", "title": "Amelia Butcher", "template": "",
         "eyebrow": "Artists in Residence",
         "body": "\n".join([
             "<p><strong>February 2027</strong></p>",
             f"<p>This winter, grade 7 students will have the privilege of working with artist Amelia Butcher. They will respond to the current exhibition {CAG}.</p>",
             "<h2>Amelia Butcher Biography</h2>",
             figure("amelia-butcher-studio"),
             "<p>Amelia Butcher is a visual artist based in British Columbia with a sculptural and drawing practice centered in clay.</p>",
             "<p>She graduated from Emily Carr University in 2013 and is a founding member of the Dusty Babes Collective. From 2015-2021 she lived and worked out of their communal studio, built by the late great Don Hutchinson, in Surrey, BC.</p>",
             "<p>She has exhibited widely and instructs classes and workshops in ceramics, sculpture and comic-making for all ages. She is a board member of the BC Potters Guild and currently works out of a studio in Vancouver, the unceded, ancestral territories of the xʷməθkʷəy̓əm (Musqueam), Sḵwx̱wú7mesh (Squamish), and səlilwətaɬ (Tsleil-Waututh) Nations.</p>",
             f"<p>{artist('amelia-butcher', 'Amelia Butcher in the Permanent Collection')}</p>",
             "<h2>Past Workshops with Amelia Butcher</h2>",
             "<p><strong>February 2026</strong></p>",
             '<p>This winter grade 7 students will have the privilege of working with Amelia Butcher. They will respond to the current exhibition <a href="/pages/exhibitions/from-the-ground"><em>From The Ground</em></a>. The artworks illustrate the natural world and the varying types of views we have of the world around us.</p>',
             figure("amelia-butcher-workshop")])},
        {"handle": "artist-in-residence-mark-johnsen", "title": "Mark Johnsen", "template": "",
         "eyebrow": "Artists in Residence",
         "body": "\n".join([
             "<p><strong>April 2027</strong></p>",
             "<p>This April, Artists For Kids is excited to offer an Artist-in-Residence program for grade 9 students, providing an opportunity to work for two school days at the Artists For Kids studios with artist Mark Johnsen. The Artist-in-Residence programs provide vital skills training and the necessary dedicated time and focus that gives young artists the rare opportunity to immerse themselves in creativity and art making. Selected art students who are nominated by their school will work with professional printmaker, Mark Johnsen.</p>",
             "<h2>Mark Johnsen Biography</h2>",
             figure("mark-johnsen-studio"),
             "<p>Mark Johnsen (he/him) is an American visual artist living and working in Vancouver, British Columbia. His print-based practice examines the possibilities of the unique, hand-pulled impression in an era of digital reproduction. Through studies of material exploration, traditional and non-traditional printing techniques: he works to capture gestural and representational time stamps. He is the co-founder of <em>Patio Press</em>, a hybrid printmaking residency run alongside artist, Sara-Jeanne Bourget. He holds a BFA in Photography from California College of the Arts (2012) and an MFA from Emily Carr University of Art + Design (2020). He has exhibited throughout The United States, Canada, The United Kingdom, Turkey, Bosnia, Japan, Switzerland, and New Zealand and is currently an Assistant Professor in Print Media at Emily Carr University of Art + Design.</p>",
             f"<p>{artist('mark-johnsen', 'Mark Johnsen in the Permanent Collection')}</p>",
             "<h2>Past Workshops with Mark Johnsen</h2>",
             "<p><strong>February 2024 • Grades 10 to 12</strong></p>",
             "<p>This February, AFK is excited to offer an Artist-in-Residence program for senior art students, providing an opportunity to work for two school days at the AFK studios with artist Mark Johnson. The AFK Artist-in-Residence programs provide vital skills training and the necessary dedicated time and focus that gives young artists the rare opportunity to immerse themselves in creativity and art making. During two school days, senior art students who are nominated by their school will work with professional printmaker, Mark Johnsen.</p>"])},
        {"handle": "artist-in-residence-becky-bair", "title": "Becky Bair", "template": "",
         "eyebrow": "Artists in Residence",
         "body": "\n".join([
             "<p><strong>May 2027</strong></p>",
             "<p>This spring, grade 8 and 9 students will have the privilege of working with Becky Bair on a photography project. They will respond to the exhibition in the Gordon Smith Gallery of Canadian Art, with a focus on cyanotypes.</p>",
             "<h2>Becky Bair Biography</h2>",
             figure("becky-bair-workshop-1", "Photo by Khim Mata Hipol"),
             "<p>Rebecca Bair (b. 1995, Toronto, Canada) is an interdisciplinary artist based in Vancouver - the traditional and ancestral territories of the Coast Salish peoples. Her research aims to explore the possibilities of specific representation and of identity through abstraction and non-figuration. Bair uses multimedia approaches and Sun collaborations to illustrate her exploration of identity and intersectionality, through the lens of her own experience as a Black Woman on Turtle Island. Her artistic, professional and educational goals revolve around common themes of celebrating Black plurality, as well as enabling interpersonal and intercultural care, and her work acts as a vehicle through which the complexities of history and identity can be uncovered, redefined and expressed.</p>",
             figure("becky-bair-workshop-2", "Photo by Khim Mata Hipol"),
             figure("becky-bair-workshop-3", "Photo by Khim Mata Hipol")])},
        {"handle": "artist-in-residence-sara-jeanne-bourget", "title": "Sara-Jeanne Bourget", "template": "",
         "eyebrow": "Artists in Residence",
         "body": "\n".join([
             "<h2>Drawing Artist-in-Residence Sara-Jeanne Bourget</h2>",
             "<h3>November 2025</h3>",
             "<p>This November, Artists for Kids is excited to offer an Artist-in-Residence program for secondary students in grades 10, 11, and 12. During two school days, students who are nominated will have the opportunity to work with artist Sara-Jeanne Bourget at the Artists for Kids Studios.</p>",
             "<p>Traditionally, drawing has been used to record and make sense of the world. In this workshop, we will use drawing to reveal the often overlooked or unseen details of our immediate environment. Moving from observation to imagination, drawing becomes a tool to discover new perspectives. Participants will begin with direct observational techniques, gradually transitioning to material- and process-based approaches. Through this progression, students will create a series of works that engage with and respond to their natural surroundings. The workshop is an invitation to explore the expanded possibilities of drawing, with a particular focus on working with charcoal.</p>",
             "<h3>Artist Bio</h3>",
             "<p>Artist Sara-Jeanne Bourget’s drawing and printmaking practice engages with cyclical processes that echo natural rhythms and phenomena. Through this work, the artist explores how the act of “mining”—traditionally associated with extraction and destruction—can be re-imagined as a method of uncovering ideas, relationships, and possibilities.</p>",
             "<p>Observing how non-human individuals mine their environment offers new perspectives to foster relationships with the world. A fascination with surfaces altered by animal/plant/human/time-based erosion creates space for new forms and future possibilities.</p>",
             "<p>In Bourget’s practice, materials and methods intrinsic to drawing and printmaking intertwine, creating hybrid images that blur the boundaries of both disciplines. The artist often works by “mining” from old or discarded charcoal drawings, using them as the foundation for new matrices. These are built through layering, covering, and excavating marks—actions that mirror natural and emotional cycles. Repeated patterns and forms appear seasonally, evolving through intuitive gestures and sustained repetition.</p>",
             "<p>Bourget is currently an assistant professor in Drawing at Emily Carr University.</p>"])},
        {"handle": "studio-art-academy", "title": "Studio Art Academy", "template": "programme",
         "body": "\n".join([
             "<p>*Please note that this academy is not offered for the 2026/2027 school year.*</p>",
             figure("studio-art-academy"),
             "<p>Artists for Kids Studio Art Academy offers young artists immersive experiences where they develop thoughtful, independent perspectives on visual arts and culture. Through hands‑on learning with professional artists, visits to galleries, and access to high‑quality studio materials, students build a personalized portfolio that reflects their voice, skill, and growth.</p>",
             "<p>This advanced Academy places art‑making at the centre of inquiry—encouraging creativity, communication, critical thinking, and collaboration. Working in the Artists for Kids’ Shadbolt Studio and the Gordon Smith Gallery, students gain the skills, independence, and confidence needed to thrive as emerging art practitioners. The year culminates in a professionally mounted exhibition showcasing their work.</p>",
             "<p>Students explore a wide range of artistic processes, including drawing, painting, printmaking, and sculpture, offering both depth and breadth in studio practice. Intensive hands‑on work is complemented by artists in residence and post‑secondary and gallery collaborations, giving students a clear understanding of the skills, dedication, and pathways required for future studies in the visual arts.</p>",
             "<p>The opportunity to engage with artists in residence each term enriches the learning environment and provides students with meaningful connections to the broader arts community. The Artists for Kids Studio Art Academy not only prepares students for post‑secondary success—it empowers them to see themselves as artists now.</p>",
             "<p>Students in the Academy are encouraged to:</p>",
             "<ul>",
             "<li>Explore identity, sense of belonging and express a personal philosophy of art through personally relevant imagery</li>",
             "<li>Reflect critically and respond to personal work and the artworks of others</li>",
             "<li>Enhance understanding of contemporary Canadian art</li>",
             "<li>Understand that growth as an artist is dependent on perseverance, resilience, refinement, reflection and risk taking</li>",
             "<li>Understand the career elements and habits required of professional artists</li>",
             "<li>Participate in a year-end exhibition</li>",
             "</ul>"])},
        {"handle": "learning-guides", "title": "Learning Guides", "template": "programme",
         "groups": ["afk-guides-by-artists", "afk-guides-primary"]},
        {"handle": "learning-kits", "title": "Learning Kits", "template": "programme",
         "groups": ["afk-kits", "afk-kit-clay-plans", "afk-kit-collagraph-plans", "afk-kit-trace-monotype-plan",
                    "afk-kit-gel-plate-plan", "afk-kit-videos"]},
        {"handle": "artreach-videos", "title": "ArtReach Videos", "template": "programme",
         "body": "\n".join([
             "<p>This series of videos guides classrooms or individuals at home through art activities focused on principles of creative inquiry and play. Videos are posted to our website throughout the school year. Enjoy!</p>",
             '<p><a href="/pages/learning-guides">Download Artists for Kids Learning Guides</a></p>',
             '<p><a href="/pages/learning-kits">Register to borrow Artists for Kids Learning Kits</a></p>'])},
        {"handle": "professional-development", "title": "Professional Development", "template": "programme",
         "body": "\n".join([
             "<p>Each year, Artists For Kids hosts professional development opportunities for K - 12 educators to enhance learning through the lens of the visual arts.</p>",
             "<p><strong>Mark your calendars!</strong></p>"])},
        {"handle": "awards-and-scholarships", "title": "Awards and Scholarships", "template": "programme",
         "body": "\n".join([
             "<p>Applications have closed for the 2025/2026 school year.</p>",
             "<p>Artists for Kids is pleased to offer the following three Scholarships for North Vancouver School District graduating students who have completed or are enrolled in Grade 12 level Visual and Performing Arts courses.</p>",
             "<ul>",
             f'<li><p>The $1,000 Jack Shadbolt Multiple Arts Excellence award is available to a graduating student who has demonstrated excellence in two or more of the Visual and/or Performing Arts disciplines (i.e. art &amp; music, film &amp; theatre, drama &amp; dance) and is planning to continue their education in the arts.</p><p><a href="{pdf_path("award-shadbolt")}">Requirements (PDF)</a></p></li>',
             f'<li><p>The $1,000 Robert Bateman Future Teacher award is available to a graduating student who has demonstrated excellence in Visual Arts and is planning to pursue a future teaching career in the field of Elementary or Secondary education.</p><p><a href="{pdf_path("award-bateman")}">Requirements (PDF)</a></p></li>',
             f'<li><p>The $1,000 North Shore Community Foundation - Gordon Smith Outstanding Visual Artist award is available to a graduating student who has demonstrated excellence in the Visual Arts and is planning to continue their education in the Visual Arts (visual arts include traditional media as well as photographic and digital media).</p><p><a href="{pdf_path("award-gordon-smith")}">Requirements (PDF)</a></p></li>',
             "</ul>",
             f"<p>If you have questions or encounter any problems with the application process, please email {EMAIL} or call (604) 903-3798.</p>"])},
        {"handle": "support-artists-for-kids", "title": "Support Artists for Kids", "template": "programme",
         "cta": (CANADAHELPS, "Donate"),
         "body": "\n".join([
             "<p>Artists for Kids is a unique, not-for-profit, self-sustaining art education program operated by the North Vancouver School District (NVSD) in British Columbia. In addition to receiving support through the NVSD, we rely on the generosity of our donors to offer a range of Artist- and Educator-led programs in schools and the community, as well as scholarships for students pursuing post-secondary studies in arts education.</p>",
             "<p>Your contribution helps make quality arts education accessible to all children and youth and enables us to continue creating meaningful, life-changing opportunities through the arts.</p>",
             "<p>Your donations help make quality art education accessible to all and ensure that we can continue creating life changing opportunities to children and youth.</p>",
             f'<p>Donations can be made with an <a href="{SCHOOLCASH}">NVSD School Cash Online account</a>, or through <a href="{CANADAHELPS}">CanadaHelps</a>. To make a donation over the phone, please call (604) 903-3798.</p>',
             "<p>Every donation makes a difference. Thank you for supporting arts education in our community.</p>",
             "<h2>A heartfelt thank you to our donors and sponsors</h2>",
             "<p>Artists for Kids has been fortunate to have a variety of donors and supporters who have embraced the work we do and the programs we offer. With their generosity and contributions, we have been able to expand our offerings, and provide financial assistance for those families whose kids could otherwise not discover the untapped creativity inside of them.</p>",
             "<figure class=\"gs-quote\"><blockquote><p>\"...opened Oliver's most wonderful thank you note to my parents' memorial fund for some scholarship assistance to him...Please tell him how much I appreciated and enjoyed all parts of his note. And to you: this is why we give support to your summer camp. I hope Gordon Smith gets as much enjoyment from his support as I do from ours.\"</p></blockquote><figcaption>Irene</figcaption></figure>",
             "<p>Our Donors and Sponsors contribute in a variety of ways. Whether it's with financial support, in-kind donations, or gifts of significant pieces of work for the AFK Permanent Collection, we are grateful for our community's continued trust and support of our programs and gallery.</p>",
             '<ul class="gs-points">',
             '<li><strong>The Gordon and Marion Smith Foundation for Young Artists</strong><br><a href="/pages/the-smith-foundation">The Gordon and Marion Smith Foundation for Young Artists</a> established a permanent endowment fund, whose increasing annual revenues is granted to Artists for Kids, to ensure the success and viability of Artists for Kids and their programs and to support the Gordon Smith Gallery of Canadian Art in perpetuity.</li>',
             "<li><strong>The Tuey Charitable Foundation</strong><br>The Tuey Charitable Foundation generously supports our Gallery Program to bring art and stories to children through our \"Windows to Canadian Art\" program at the Gordon Smith Gallery. The Foundation also supports Artists for Kids to bring materials and equipment to students and classrooms with curated art kits.</li>",
             '<li><strong>The Christopher Foundation for the Arts</strong><br><a href="https://cffta.org/">The Christopher Foundation</a> generously supports Artists for Kids\' Gallery Program to continue to offer the exceptional experiences in Art Education that we bring to our community. The Foundation has been instrumental in providing resources to bring to our programing, experiences that build connection and belonging to all that we do, and to ensure that all children and youth have access to be involved.</li>',
             '<li><strong>The Idea Partner Marketing Inc.</strong><br><a href="https://www.theideapartner.com/">The Idea Partner Marketing Inc.</a> has generously worked with Artists for Kids to create their logos and visual mark. Additionally, The Idea Partner consistently provides financial support for campers to attend our Paradise Valley Summer School of Visual Arts Camp each year.</li>',
             "<li><strong>The Edwina and Paul Heller Memorial Fund</strong><br>Over many years, the Edwina and Paul Heller Memorial Fund has assisted countless of students to attend camp, participate in our after school art programs and day camps. Funding has also provided the ability to acquire materials and equipment to allow students to have access to experiences in a range of visual art.</li>",
             "<li><strong>The North Vancouver School District</strong><br>In 1989, the North Vancouver School District listened carefully to the founders of Artists for Kids. The District learned about Artists for Kids' model for fund-raising and their passion to ensure Arts Education for all, existed and continued. With this, the NVSD funded the first limited edition that AFK published, with Bill Reid.<br><br>From this point, the District has never stopped cheering on Artists for Kids, including being open to build a cultural space at the Education Services Centre. In 2012, the Smith Foundation, brought together multiple funding sources, including a generous 2 million donation from Michael Audain, that enabled the Gordon Smith Gallery of Canadian Art to be built at the Education Services Centre, and to become an integral space for our community to gather.</li>",
             '<li><strong>The Beech Foundation</strong><br><a href="https://beechfoundation.ca/">The Beech Foundation</a> has been a long standing patron of Artists for Kids, supporting children and youth by providing funding for bursaries and materials for our Paradise Valley Summer School of Visual Arts camp.</li>',
             '<li><strong>OPUS</strong><br><a href="https://opusartsupplies.com/">OPUS</a> has been a community patron since Artists for Kids\' inception. Opus supports AFK with materials for: our camps, professional development workshops, and our Artist in Residence programs which has made a significant difference to our programming and ability to offer to our children, educators and artists the exceptional experiences and resources that Artists for Kids is known for.</li>',
             '<li><strong>ArtStarts</strong><br><a href="https://artstarts.com/">ArtStarts</a> brings artists into our community through their funding, allowing all of us, to learn from each other through our collective stories. Our Artist in Residence Program as well as teacher workshops are supported by ArtStarts\' annual grant.</li>',
             '<li><strong>CUPE 389</strong><br><a href="https://cupe389.ca/">CUPE 389</a> has supported Artists for Kids for many years by providing funding for bursaries to support children and youth to attend AFK\'s Paradise Valley Summer School of Visual Arts camp.</li>',
             '<li><strong>Heffel</strong><br><a href="https://www.heffel.com/">Heffel</a> has continued to support Artists for Kids through their appraisals and sales. Heffel\'s expertise has been pivotal to allow the vision of the AFK Permanent Collection and AFK Print Program come to fruition.</li>',
             "<li><strong>RBC Foundation</strong><br>RBC Foundation has generously committed to Artists for Kids by offering a community engagement grant each year to support our Gallery Program in addition to volunteering to help with our programming.</li>",
             "<li><strong>Individual donors</strong><br>We are grateful to the individual donors who have supported us for over thirty years.</li>",
             "</ul>"])},
    ]


# The Artists for Kids page (existing): its history gains two paragraphs from Who We Are, then the team
# and the annual report (P-24's History section).
AFK_HISTORY_ADD = "\n".join([
    "<p>In 1989, the founders of AFK sought to find a financial model to support arts education in our schools, one that was sustainable, and in turn, would support visual arts enrichment. By purchasing art from artists, then in turn inviting each artist to create original, limited-edition prints that the program could sell, the founders created a unique and lasting fundraising vehicle. With the generosity, commitment and support of founding artist-patrons Gordon Smith, Jack Shadbolt and Bill Reid, Artists for Kids was born, and with it, the acclaimed Artist for Kids and Gordon Smith Gallery Permanent Collection of Canadian Art.</p>",
    "<p>Thanks to the ongoing support of our community, artist-patrons, and the North Vancouver School District, Artist for Kids has grown from an idea onto a world-class art program.</p>",
])
AFK_HISTORY_AFTER = "<p>Artists for Kids was founded in 1989 with the singular intent to support art education, for all.</p>"


def afk_team_and_report():
    return "\n".join([
        "<h2>Meet the Artists for Kids Team</h2>",
        figure("team"),
        "<p>From left to right:</p>",
        "<ul>",
        "<li>Allison Kerr, Director, Artist for Kids and Gordon Smith Gallery, and District Principal, Arts Education</li>",
        "<li>Amelia Epp, District Visual Arts Teacher, Educational Coordinator</li>",
        "<li>Chantal Pinard, Artists For Kids Administrative and Program Assistant</li>",
        "<li>Emily Neufeld, Artists for Kids Studio Technician, Gallery Collection Preparator</li>",
        "</ul>",
        "<h2>Annual Report</h2>",
        f'<p><a href="{pdf_path("annual-report")}">Annual Report 2024-2025 (PDF)</a></p>',
    ])


def afk_release_body(current):
    """The Artists for Kids page's staged text with the additions, from its current value."""
    assert AFK_HISTORY_AFTER in current, "the History section's first paragraph has changed: check by hand"
    if "In 1989, the founders of AFK" in current:
        return current  # already added
    body = current.replace(AFK_HISTORY_AFTER, AFK_HISTORY_AFTER + "\n" + AFK_HISTORY_ADD, 1)
    return body.rstrip() + "\n" + afk_team_and_report()


# ---------------------------------------------------------------------------------------------------
# Cards and card groups (P-16). Existing cards change only their link: to the site's own page.
# ---------------------------------------------------------------------------------------------------

def card(title, image=None, text=None, url=None, link_text=""):
    fields = [{"key": "title", "value": title}]
    if image:
        fields.append({"key": "image", "value": img(image)})
    if text:
        fields.append({"key": "text", "value": text})
    if url:
        fields.append({"key": "link", "value": link(url, link_text)})
    return fields


def relink(url):
    """An existing card's link, changed to the site's page (the card keeps its title and image)."""
    return [{"key": "link", "value": link(url)}]


def cards():
    c = {
        # Existing programme cards: now the site's own pages (were artistsforkids.sd44.ca).
        "afk-after-school-art": relink(page_url("after-school-art")),
        "afk-day-camps": relink(page_url("day-camps")),
        "afk-paradise-valley": relink(page_url("paradise-valley-summer-camp")),
        "afk-gallery-programs": relink(page_url("gallery-program")),
        "afk-artists-in-residence": relink(page_url("artists-in-residence")),
        "afk-learning-kits": relink(page_url("learning-kits")),
        # New programme cards.
        "afk-studio-art-academy": card("Studio Art Academy", "studio-art-academy", url=page_url("studio-art-academy")),
        "afk-learning-guides": card("Learning Guides", "guide-paper-mural", url=page_url("learning-guides")),
        "afk-artreach-videos": card("ArtReach Videos", "cover:paths-abstract-painting", url=page_url("artreach-videos")),
        "afk-professional-development": card("Professional Development", "event-clay-kit", url=page_url("professional-development")),
        # This season (P-34): the old home page's promotions, which the team keeps up each term.
        "afk-season-after-school-art": card("After School Art Registration", "after-school-art",
            "Registration is open for fall 2026 After School Art Classes. Classes vary in duration, price, and medium. All art materials are included in the price of the program.",
            page_url("after-school-art")),
        "afk-season-program-guide": card("The Gordon Smith Gallery 2026-27 Program Guide", "program-guide",
            "The Gordon Smith Gallery Program Guide includes information on upcoming exhibitions, enrichment programs, workshops, resources, professional development opportunities and more.",
            pdf("program-guide")),
        "afk-season-artists-in-residence": card("Artists In Residence Programs 2026-2027", "air-2026",
            "Artists In Residence Workshops returns this Fall 2026", page_url("artists-in-residence")),
        # Cross-links between the two organisations' programmes for families.
        "programs-afk-classes-and-camps": card("Artists for Kids Classes and Camps", "card-after-school-art",
            url=page_url("classes-and-camps")),
        "donate-artists-for-kids": card("Artists for Kids",
            text="Artists for Kids is a unique, not-for-profit, self-sustaining art education program operated by the North Vancouver School District (NVSD) in British Columbia.",
            url=page_url("support-artists-for-kids"), link_text="Support Artists for Kids"),
        # Artists in residence: the old page's two school years. The pictures are the residency posters.
        "afk-air-2026-samuel-roy-bois": card("Samuel Roy-Bois, Fall 2026", "air-2026-samuel-roy-bois",
            "In November 2026, artist Samuel Roy-Bois will be leading a workshop with grade 10 - 12 students",
            f"{SITE}/pages/artists/samuel-roy-bois"),
        "afk-air-2027-amelia-butcher": card("Amelia Butcher, Winter 2027", "air-2027-amelia-butcher",
            "In February 2027, artist Amelia Butcher will lead a clay and ceramic-based Artist In Residence workshop with Grade 7 students.",
            page_url("artist-in-residence-amelia-butcher")),
        "afk-air-2027-mark-johnsen": card("Mark Johnsen, Spring 2027", "air-2027-mark-johnsen",
            "In April 2027, artist Mark Johnsen will be leading a printmaking artist in residence workshop for Grade 9 students.",
            page_url("artist-in-residence-mark-johnsen")),
        "afk-air-2027-becky-bair": card("Becky Bair, Spring 2027", "air-2027-rebecca-bair",
            "In May 2027, artist Becky Bair will be leading a photography enrichment workshop for Grade 8 students.",
            page_url("artist-in-residence-becky-bair")),
        "afk-air-2025-sara-jeanne-bourget": card("Sara-Jeanne Bourget, Fall 2025", "air-2025-sara-jeanne-bourget",
            "Artist Sara-Jeanne Bourget’s drawing and printmaking practice engages with cyclical processes that echo natural rhythms and phenomena.",
            page_url("artist-in-residence-sara-jeanne-bourget")),
        "afk-air-2026-marlene-yuen": card("Marlene Yuen, Winter 2026", "air-2026-marlene-yuen",
            "Marlene Yuen leads Grade 3 Students in printmaking processes during her two-day Artist In Residence enrichment workshop in January.",
            f"{SITE}/pages/artists/marlene-yuen"),
        "afk-air-2026-amelia-butcher": card("Amelia Butcher, Winter 2026", "air-2026-amelia-butcher",
            "Artist Amelia Butcher leads Grade 7 students in clay processes in February 2026 during her two-day Artist In Residence enrichment workshop.",
            page_url("artist-in-residence-amelia-butcher")),
        "afk-air-2026-rebecca-bair": card("Rebecca Bair, Spring 2026", "air-2026-rebecca-bair",
            "Artist Rebecca Bair leads Grade 8 and 9 students in cyanotype photographic processes in May 2026 during her two-day Artist in Residence enrichment workshop.",
            page_url("artist-in-residence-becky-bair")),
        # Learning guides: each card opens its PDF (DS-69).
        "afk-guide-art-camp": card("Lessons from Art Camp Sara-Jeanne Bourget 2025", "guide-art-camp", url=pdf("guide-art-camp")),
        "afk-guide-charcoal": card("Charcoal Stencil Prints Inspired by Sara-Jeanne Bourget", "guide-charcoal", url=pdf("guide-charcoal")),
        "afk-guide-mail-art": card("A Mail Art Collaboration - Lesson by Clare Yow", "guide-mail-art", url=pdf("guide-mail-art")),
        "afk-guide-mini-monster": card("Make Mini Monster - Lesson by Lexy Ho-Tai", "guide-mini-monster", url=pdf("guide-mini-monster")),
        "afk-guide-zine-collage": card("Zine Making Workshop using Collage with Annie Canto", "guide-zine-collage", url=pdf("guide-zine-collage")),
        "afk-guide-zine-frottage": card("Zine Making Workshop using Frottage with Annie Canto", "guide-zine-frottage", url=pdf("guide-zine-frottage")),
        "afk-guide-paper-mural": card("Creating a Paper Mural with Sandeep Johal", "guide-paper-mural"),  # no PDF yet
        "afk-guide-narrative-scrolls": card("Visual Narrative Scrolls with Sean Karemaker", "guide-narrative-scrolls", url=pdf("guide-narrative-scrolls")),
        "afk-guide-fragmented-faces": card("Fragmented Faces - Portraits in Pastel and Paint with Tiko Kerr", "guide-fragmented-faces", url=pdf("guide-fragmented-faces")),
        # Learning kits: the kit, its reservation form, then its lesson plans.
        "afk-kit-clay": card("Clay Lesson Plans and Kits", "kit-clay",
            "Teachers in the North Vancouver School District can book a clay kit for a two-week period, which contains all the tools and the step-by-step instructions to bring these clay lesson into your classroom.",
            CLAY_KIT_FORM, "Reserve a Clay Kit"),
        "afk-kit-collagraph": card("Collagraph Lesson Plans and Kit", "kit-collagraph",
            "Teachers in the North Vancouver School District can book the Collagraph Kit for a two-week period, which contains all the tools and the step-by-step instructions to bring 4 printmaking lessons into your classroom.\n\nTeachers can choose from four different collagraph lesson plans that have been designed for K-7 classrooms. Lesson plans are linked, below, and laminated copies are included in the kit.\n\n** Please note, teachers will need to supply ink and paper separately. For more information on the ink and paper required for each lesson and where to purchase these supplies, please refer to the lesson plans below.",
            KIT_FORM, "Reserve Collagraph Printmaking Kit"),
        "afk-kit-trace-monotype": card("Trace Monotype Lesson Plan and Kit", "kit-trace-monotype",
            "Students will use trace monotype printmaking and mixed media collage techniques to create a self-portrait that communicates feelings and ideas about self through colour, gesture, and symbols.",
            KIT_FORM, "Reserve Trace Monotype Kit"),
        "afk-kit-gel-plate": card("Gel Plate Lesson Plan and Kit", "kit-gel-plate",
            "Using the materials in this kit students will create a four-panel comic using gel plate monoprint techniques. Students will experiment with textures, colors, and shapes to create both visual interest and meaning in their comic panels.",
            KIT_FORM, "Reserve Gel Plate Kit"),
        "afk-plan-clay-tile": card("Clay Tile Kit | Lesson Plan", "kit-clay-tile", url=pdf("kit-clay-tile")),
        "afk-plan-clay-log": card("Clay Log Kit | Lesson Plan", "kit-clay-log", url=pdf("kit-clay-log")),
        "afk-plan-foam-butterflies": card("Foam Butterflies with Jack Shadbolt", "lesson-foam-butterflies", "Lesson 1 (for grades 4-7)", pdf("lesson-foam-butterflies")),
        "afk-plan-garbage-press": card("Garbage Press with Big Rock Candy Mountain with Jack Shadbolt", "lesson-garbage-press", "Lesson 2 (for grades 4-7)", pdf("lesson-garbage-press")),
        "afk-plan-lego-press": card("Lego Press with Reed H. Reed", "lesson-lego-press", "Lesson 3 (for grades K-7)", pdf("lesson-lego-press")),
        "afk-plan-textured-landscapes": card("Textured Landscapes Inspired by Ted Harrison", "lesson-textured-landscapes", "Lesson 4 (for grades K-3)", pdf("lesson-textured-landscapes")),
        "afk-plan-trace-monotype": card("Trace Monotype Kit Lesson Plan | Self Portrait", "lesson-trace-monotype", url=pdf("lesson-trace-monotype")),
        "afk-plan-gel-plate": card("Gel Plate Monoprint Kit Lesson Plan", "lesson-gel-plate", url=pdf("lesson-gel-plate")),
        "afk-kit-video-clay": card("Artists for Kids Clay Kit: Ancient and Future Fossils", "cover:artists-for-kids-clay-kit-ancient-and-future-fossils",
            url=f"{SITE}/pages/lessons/artists-for-kids-clay-kit-ancient-and-future-fossils"),
        "afk-kit-video-trace-monotype": card("Artists for Kids Trace Monotype Kit: Self Portraits", "cover:artists-for-kids-trace-monotype-kit-self-portraits",
            url=f"{SITE}/pages/lessons/artists-for-kids-trace-monotype-kit-self-portraits"),
    }
    return c


GROUPS = [
    # (handle, heading, cards). The same card can sit in more than one group.
    ("afk-this-season", "Fall 2026 at Artists For Kids",
     ["afk-season-after-school-art", "afk-season-program-guide", "afk-season-artists-in-residence"]),
    ("afk-community-programs", "Community Programs", ["afk-after-school-art", "afk-day-camps", "afk-paradise-valley"]),
    ("afk-also-for-families", "Also for families", [EXPLORE_CREATE_CARD]),
    ("afk-school-programs", "School Programs", ["afk-gallery-programs", "afk-artists-in-residence", "afk-studio-art-academy"]),
    ("afk-learning-resources", "Learning & Teaching Resources",
     ["afk-learning-guides", "afk-learning-kits", "afk-artreach-videos", "afk-professional-development"]),
    ("afk-air-2026-2027", "2026-2027 Artists In Residence",
     ["afk-air-2026-samuel-roy-bois", "afk-air-2027-amelia-butcher", "afk-air-2027-mark-johnsen", "afk-air-2027-becky-bair"]),
    ("afk-air-2025-2026", "2025-2026 Artists-in-Residence",
     ["afk-air-2025-sara-jeanne-bourget", "afk-air-2026-marlene-yuen", "afk-air-2026-amelia-butcher", "afk-air-2026-rebecca-bair"]),
    ("afk-guides-by-artists", "Learning Guides Created by Artists with Artists For Kids",
     ["afk-guide-art-camp", "afk-guide-charcoal", "afk-guide-mail-art", "afk-guide-mini-monster", "afk-guide-zine-collage",
      "afk-guide-zine-frottage", "afk-guide-narrative-scrolls"]),
    ("afk-guides-primary", "Primary (K - Grade 3) Resources", ["afk-guide-fragmented-faces"]),
    ("afk-kits", "", ["afk-kit-clay", "afk-kit-collagraph", "afk-kit-trace-monotype", "afk-kit-gel-plate"]),
    ("afk-kit-clay-plans", "Clay Lesson Plans", ["afk-plan-clay-tile", "afk-plan-clay-log"]),
    ("afk-kit-collagraph-plans", "Collagraph Lesson Plans",
     ["afk-plan-foam-butterflies", "afk-plan-garbage-press", "afk-plan-lego-press", "afk-plan-textured-landscapes"]),
    ("afk-kit-trace-monotype-plan", "Trace Monotype Lesson Plan", ["afk-plan-trace-monotype"]),
    ("afk-kit-gel-plate-plan", "Gel Plate Lesson Plan", ["afk-plan-gel-plate"]),
    ("afk-kit-videos", "Lesson Videos", ["afk-kit-video-clay", "afk-kit-video-trace-monotype"]),
]
# Existing groups that gain a card: (handle, card added at the end).
GROUPS_EXTENDED = [("public-programs", "programs-afk-classes-and-camps"), ("donate-ways-to-give", "donate-artists-for-kids")]
AFK_PAGE_GROUPS = ["afk-this-season", "afk-community-programs", "afk-school-programs", "afk-learning-resources"]


def card_entries():
    return list(cards().items())


def group_entries(made_cards):
    """made_cards: every card's handle to its ID (from load.py's afk-cards.json)."""
    out = []
    for handle, heading, members in GROUPS:
        ids = [m if m.startswith("gid://") else made_cards[m] for m in members]
        fields = [{"key": "cards", "value": json.dumps(ids)}]
        fields.insert(0, {"key": "heading", "value": heading})
        out.append((handle, fields))
    return out


# ---------------------------------------------------------------------------------------------------
# Events (P-16, P-31, P-37): the educators' workshops with a date. Undated ones wait for one.
# ---------------------------------------------------------------------------------------------------

CLAY_SUMMARY = "\n\n".join([
    "Part 1: October 5, 3:30-5:00pm\nPart 2: October 19, 3:30-5:00pm",
    "In this two-part hands-on clay workshop, ceramics artist Amelia Butcher will walk you through a lesson designed specifically for elementary grades. The artist will share practical tips and techniques for managing materials and teaching clay techniques to elementary students. Teachers are able to sign out the Artists for Kids Clay Kit to use in their schools for a two-week period. In this kit, teachers will have all the tools needed to complete the clay lesson taught in this two-part workshop series.",
    "Workshops will cover the following topics: managing materials in the classroom, hand building techniques, sculpting with clay, press molds, planning and design process, drying and firing clay artworks. There will be a cup variation of the project shared for those who have attended the log workshop previously.",
])


def event(title, starts, ends, pd_page, summary=None, location=None, image=None, tickets=None, exhibition=None):
    fields = [{"key": "title", "value": title}, {"key": "starts", "value": starts}, {"key": "ends", "value": ends},
              {"key": "programme_page", "value": pd_page}, {"key": "keep_off_home", "value": "true"}]
    if summary:
        fields.append({"key": "summary", "value": summary})
    if location:
        fields.append({"key": "location", "value": location})
    if image:
        fields.append({"key": "image", "value": img(image)})
    if tickets:
        fields.append({"key": "tickets", "value": link(tickets, "Register")})
    if exhibition:
        fields.append({"key": "exhibition", "value": EXHIBITIONS[exhibition]})
    return fields


def event_entries(pages_made):
    pd = pages_made["professional-development"]
    studios = "Artists for Kids studios (2121 Lonsdale Avenue, North Vancouver)"
    return [
        ("pd-clay-kit-2026-10-05", event("Introduction to the Artists For Kids Clay Kit", "2026-10-05T15:30:00-07:00",
            "2026-10-05T17:00:00-07:00", pd, CLAY_SUMMARY, studios, "event-clay-kit", CLAY_WORKSHOP_FORM)),
        ("pd-clay-kit-2026-10-19", event("Introduction to the Artists For Kids Clay Kit", "2026-10-19T15:30:00-07:00",
            "2026-10-19T17:00:00-07:00", pd, CLAY_SUMMARY, studios, "event-clay-kit", CLAY_WORKSHOP_FORM)),
        ("pd-printmaking-transfer-assemblage-2026-10-23", event("Printmaking, Transfer, and Assemblage: A Gallery Workshop",
            "2026-10-23T09:00:00-07:00", "2026-10-23T11:30:00-07:00", pd,
            "This hands-on workshop introduces \"Collect, Assemble, Gather\", the Gordon Smith Gallery’s Fall 2026 exhibition. Participants will use linocut printmaking, rubbing, and image transfer to create an assembled artwork exploring memory, consumer culture, resources, and sustainability, with Social Studies connections.\n\nLed by Raph Choi",
            tickets=PROD_OCT23_FORM, exhibition="collect-assemble-gather")),
        ("pd-print-repeat-collect-2026-10-23", event("Print, Repeat, Collect: A Block Printmaking Workshop",
            "2026-10-23T12:30:00-07:00", "2026-10-23T15:00:00-07:00", pd,
            "Join artist Marlene Yuen for a hands-on block-printing workshop inspired by her artwork Pockets of Time, on exhibit at the Gordon Smith Gallery. You will learn about Marlene’s block-printing process and explore how repetition and collections can be used to tell visual stories. You will learn the fundamentals of transferring an image to linoleum, carving a printing block, and producing a unique print inspired by a meaningful collection.\n\nLed by artist Marlene Yuen",
            tickets=PROD_OCT23_FORM, exhibition="collect-assemble-gather")),
        ("pd-hands-on-collect-assemble-gather-2027-02-12", event("Hands-On Pro-D Art Workshop \"Collect, Assemble, Gather\"",
            "2027-02-12T09:00:00-08:00", "2027-02-12T15:00:00-08:00", pd,
            "With art specialist teachers and artists exhibited in Collect, Assemble, Gather.\n\nFor Elementary and Secondary Teachers\n\n**More Information to come September 2026**",
            exhibition="collect-assemble-gather")),
        ("pd-hands-on-against-the-latitude-2027-04-26", event("Hands-On Pro-D Art Workshop \"Against the Latitude of 'Progress'\"",
            "2027-04-26T09:00:00-07:00", "2027-04-26T15:00:00-07:00", pd,
            "With art specialist teacher and artists exhibited in Against the Latitude of “Progress” at the Gordon Smith Gallery of Canadian Art.\n\n**More information to come January 2027**",
            exhibition="against-the-latitude-of-progress")),
        # The curator's tour is already an event (from On Now): it gains Professional development as its page, and
        # stays on the home page, named by its exhibition there (DS-71).
        ("curatorial-tour-collect-assemble-gather", [{"key": "programme_page", "value": pd}]),
    ]


# ---------------------------------------------------------------------------------------------------
# Lessons (P-36, DS-70), from the export (lessons.py) and YouTube (lessons.py youtube).
# ---------------------------------------------------------------------------------------------------

WORKS = {  # a lesson's handle to the collection works it names (artwork entry handles)
    "artists-for-kids-trace-monotype-kit-self-portraits": ["gill001", "litt003"],
    "paths-abstract-painting": ["kaur001-11"],
    "painting-the-north-shore": ["barr008"],
    "made-up-machines": ["smit023"],
    "paper-fruit": ["cica003"],
    "drawn-to-birds": ["papi001"],
    "mapping-our-own-perspectives": ["mack001"],
    "paper-playgrounds": ["smit022"],
    "transforming-words-into-art": ["gill002"],
    "drawing-what-we-hear": ["kipl004"],
    "stencils-and-storytelling": ["blac003"],
    "the-stories-we-carry-with-us": ["keno006"],
    "playing-with-food-and-the-frame": ["baxt001", "prat-m001"],
    "collaged-characters-on-the-go": ["buba003"],
    "visual-listening-journal": ["poit001"],
    "landscape-painting": ["smit028"],
    "experiments-in-drawing": ["kipl004"],
    "playing-with-words": ["gill001", "gill002"],
    "abstract-paper-sculpture": ["shad010"],
    "drawing-sound": ["barr002"],
    "stencilling-with-found-objects-and-images": ["mopp001"],
    "drawing-balance-in-an-ecosystem": ["keno007-1"],
}


def tidy_em(s):
    """Formatting only: a space before italics that lost it, and spaces or an opening bracket caught inside
    the italics moved out ("print<em>Swqaqaan" , "<em>LG III (</em>2006)", "<em>Dog in Sky </em>(1999)")."""
    s = re.sub(r"([A-Za-z])<em>", r"\1 <em>", s)
    s = re.sub(r"<em>([^<]*?)\s*\(</em>", r"<em>\1</em> (", s)
    s = re.sub(r"<em>([^<]*?)\s+</em>", r"<em>\1</em> ", s)
    s = re.sub(r"\s+\)", ")", s)
    return re.sub(r"\s{2,}", " ", s).strip()


def rich_text(inline_html):
    """Shopify rich text from simple HTML with italics: one paragraph."""
    children = []
    for part in re.split(r"(<em>.*?</em>)", tidy_em(inline_html)):
        if not part:
            continue
        if part.startswith("<em>"):
            children.append({"type": "text", "value": html.unescape(part[4:-5]), "italic": True})
        else:
            children.append({"type": "text", "value": html.unescape(re.sub(r"<[^>]+>", "", part))})
    return json.dumps({"type": "root", "children": [{"type": "paragraph", "children": children}]}, ensure_ascii=False)


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def artwork_ids():
    ids = {}
    for name in ("collection-works.json",):
        p = CREATED / name
        if p.exists():
            ids.update(json.loads(p.read_text()))
    return ids


def lesson_entries(export):
    export = pathlib.Path(export)
    lessons = json.loads((export / "lessons.json").read_text())
    youtube = {y["handle"]: y for y in json.loads((export / "youtube.json").read_text())}
    works = artwork_ids()
    out = []
    for l in lessons:
        h = l["handle"]
        fields = [{"key": "title", "value": l["title"]}, {"key": "video", "value": l["video"]},
                  {"key": "cover", "value": img(f"cover:{h}")}]
        if youtube.get(h, {}).get("posted"):
            fields.append({"key": "posted", "value": youtube[h]["posted"]})
        if l["making"]:
            fields.append({"key": "making", "value": plain(l["making"])})
        if l["inspired_by"]:
            fields.append({"key": "inspired_by", "value": rich_text(l["inspired_by"])})
        if l["grades"]:
            fields.append({"key": "grades", "value": plain(l["grades"])})
        if l["questions"]:
            fields.append({"key": "questions", "value": json.dumps([plain(q) for q in l["questions"]], ensure_ascii=False)})
        if WORKS.get(h):
            fields.append({"key": "works", "value": json.dumps([works[w] for w in WORKS[h]])})
        out.append((h, fields))
    return out


# ---------------------------------------------------------------------------------------------------
# Connector payloads: pages, their fields, the menu.
# ---------------------------------------------------------------------------------------------------

def pages_payload():
    """pageCreate for each new page not yet made (P-35): published, title only, hidden from search engines,
    the sitemap and the store's search, with the live theme's On Now template name until release."""
    made = json.loads((CREATED / "afk-pages.json").read_text()) if (CREATED / "afk-pages.json").exists() else {}
    return {f"p{i}": {"title": p["title"], "handle": p["handle"], "body": "", "isPublished": True,
                      "templateSuffix": BRIDGE_TEMPLATE,
                      "metafields": [{"namespace": "seo", "key": "hidden", "type": "number_integer", "value": "1"}]}
            for i, p in enumerate(pages()) if p["handle"] not in made}


def page_fields():
    made = json.loads((CREATED / "afk-pages.json").read_text())
    groups = json.loads((CREATED / "afk-card-groups.json").read_text())
    rows = []
    for p in pages():
        owner = made[p["handle"]]
        rows.append((owner, "programme", "single_line_text_field", "Artists for Kids"))
        if p.get("hero"):
            rows.append((owner, "hero_image", "file_reference", img(p["hero"])))
        if p.get("caption"):
            rows.append((owner, "hero_caption", "single_line_text_field", p["caption"]))
        if p.get("eyebrow"):
            rows.append((owner, "eyebrow", "single_line_text_field", p["eyebrow"]))
        if p.get("cta"):
            rows.append((owner, "cta", "link", link(*p["cta"])))
        if p.get("groups"):
            rows.append((owner, "card_groups", "list.metaobject_reference", json.dumps([groups[g] for g in p["groups"]])))
        if p.get("body"):
            rows.append((owner, "release_body", "multi_line_text_field", p["body"]))
    rows.append((AFK_PAGE, "card_groups", "list.metaobject_reference", json.dumps([groups[g] for g in AFK_PAGE_GROUPS])))
    before = json.loads((HERE.parent / "snapshots" / "afk-2026-09-27-before.json").read_text())
    rows.append((AFK_PAGE, "release_body", "multi_line_text_field",
                 afk_release_body(before["pages"]["artists-for-kids"]["custom.release_body"])))
    rows.append((AFK_PAGE, "cta", "link", link(pdf("program-guide"), "2026-2027 Program Guide")))
    return [{"ownerId": o, "namespace": "custom", "key": k, "type": t, "value": v} for o, k, t, v in rows]


def menu_payload(current_items):
    """The review menu with Artists for Kids as a section (P-33). current_items: the menu's items as read."""
    made = json.loads((CREATED / "afk-pages.json").read_text())

    def page_item(title, handle, gid=None):
        return {"title": title, "type": "PAGE", "resourceId": gid or made[handle], "url": f"/pages/{handle}"}

    items = []
    for it in current_items:
        if it["url"] == "/pages/artists-for-kids":
            items.append({**page_item("Artists for Kids", "artists-for-kids", AFK_PAGE), "items": [
                page_item("About Artists for Kids", "artists-for-kids", AFK_PAGE),
                page_item("Classes and camps", "classes-and-camps"),
                page_item("Schools and teachers", "schools-and-teachers"),
                page_item("Awards and scholarships", "awards-and-scholarships"),
                page_item("Support Artists for Kids", "support-artists-for-kids")]})
        else:
            items.append(it)
    return items


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "pages":
        print(json.dumps(pages_payload(), indent=1, ensure_ascii=False))
    elif step == "page-fields-count":
        print((len(page_fields()) + 24) // 25)
    elif step == "page-fields":
        n = int(sys.argv[2])
        print(json.dumps({"metafields": page_fields()[n * 25:(n + 1) * 25]}, indent=1, ensure_ascii=False))
    elif step == "check":
        for p in pages():
            print(f"\n==== {p['handle']} ({p['title']})\n{p.get('body', '(no text)')}")
