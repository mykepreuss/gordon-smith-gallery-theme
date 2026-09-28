"""The main menu and footer menu by what visitors come to do (P-50 to P-57, DS-132 to DS-134).

Michael, 2026-09-28: "Proceed with implementing this new navigation and IA"
(`proposals/navigation-review.md`).

Writes `created/navigation-menus-input.json`: the input for two new menus, made with `menuCreate`
through the Shopify connector. They sit beside the review menus (`new-theme-main`,
`new-theme-explore`), which stay unchanged until this work merges, so the review theme keeps its
menu until its code can show the new one. The development theme reads the new menus from
`theme/sections/header-group.json` and `footer-group.json`. Neither is read by the live theme.

The three Foundation pages planned in `proposals/smith-foundation-site.md` (Scholarships, Brilliance
Gala, Supporters) don't exist yet. `LATER` lists where each goes when it does: add it with
`menuUpdate`, keeping the other items' IDs.

Run: python3 proposals/store-writes/navigation.py
"""
import json
from pathlib import Path

HERE = Path(__file__).parent


def page(title, page_id, items=None):
    item = {"title": title, "type": "PAGE", "resourceId": f"gid://shopify/Page/{page_id}"}
    if items:
        item["items"] = items
    return item


def heading(title, items):
    """A group title with no page of its own (DS-133): the link is "#"."""
    return {"title": title, "type": "HTTP", "url": "#", "items": items}


ON_NOW = 155763999017
PERMANENT_COLLECTION = 155720548649
ARTISTS = 140886573353
PUBLIC_PROGRAMS = 155718943017
UPCOMING_EVENTS = 155669168425
SPEAKER_SERIES = 155719434537
MUSIC = 155719696681
EXPLORE_CREATE = 155720089897
GOOD_COMPANY = 155720253737
ARTISTS_FOR_KIDS = 155720810793
CLASSES_CAMPS = 165837734185
SCHOOLS_TEACHERS = 165837766953
AWARDS = 165838225705
DONATE = 155885863209
SUPPORT_AFK = 165838258473
VOLUNTEER = 155902738729
ABOUT_US = 155687813417
PLAN_VISIT = 155670151465
GORDON_MARION = 155692957993
FOUNDATION = 155705409833
SHOP = 155762786601
FAQ = 154942865705

MAIN = {
    "title": "Main menu (new theme, 2026-09-28)",
    "handle": "new-theme-main-2",
    "items": [
        page("Exhibitions", ON_NOW),
        page("Collection", PERMANENT_COLLECTION, [
            page("The collection", PERMANENT_COLLECTION),
            page("Artists", ARTISTS),
        ]),
        page("Programs", PUBLIC_PROGRAMS, [
            page("Upcoming events", UPCOMING_EVENTS),
            page("Public programs", PUBLIC_PROGRAMS, [
                page("Speaker series", SPEAKER_SERIES),
                page("Music at the Smith", MUSIC),
                page("Explore + Create", EXPLORE_CREATE),
                page("Art in Good Company", GOOD_COMPANY),
            ]),
            page("Artists for Kids", ARTISTS_FOR_KIDS, [
                page("Classes and camps", CLASSES_CAMPS),
                page("Schools and teachers", SCHOOLS_TEACHERS),
            ]),
            heading("Scholarships and awards", [
                page("Artists for Kids awards", AWARDS),
            ]),
        ]),
        page("Support", DONATE, [
            page("Give to the Smith Foundation", DONATE),
            page("Give to Artists for Kids", SUPPORT_AFK),
            page("Volunteer", VOLUNTEER),
        ]),
        page("About", ABOUT_US, [
            page("About the gallery", ABOUT_US),
            page("Plan your visit", PLAN_VISIT),
            page("Gordon and Marion Smith", GORDON_MARION),
            page("The Smith Foundation", FOUNDATION),
        ]),
        page("Shop", SHOP),
    ],
}

EXPLORE = {
    "title": "Footer: Explore (new theme, 2026-09-28)",
    "handle": "new-theme-explore-2",
    "items": [
        page("Exhibitions", ON_NOW),
        page("Collection", PERMANENT_COLLECTION),
        page("Programs", PUBLIC_PROGRAMS),
        page("Artists for Kids", ARTISTS_FOR_KIDS),
        page("Support", DONATE),
        page("About", ABOUT_US),
        page("Shop", SHOP),
        page("Frequently asked questions", FAQ),
    ],
}

# Where the planned Foundation pages go once they exist (proposals/navigation-review.md, N11, N12).
LATER = [
    {"page": "/pages/smith-foundation-scholarships", "title": "Smith Foundation scholarships",
     "where": "Programs, Scholarships and awards, first"},
    {"page": "/pages/brilliance-gala", "title": "Brilliance Gala",
     "where": "Support, after Give to Artists for Kids"},
    {"page": "/pages/smith-foundation-supporters", "title": "Supporters", "where": "Support, last"},
]

if __name__ == "__main__":
    out = HERE / "created" / "navigation-menus-input.json"
    out.write_text(json.dumps({"main": MAIN, "explore": EXPLORE, "later": LATER}, indent=1) + "\n")
    print(f"wrote {out}")
