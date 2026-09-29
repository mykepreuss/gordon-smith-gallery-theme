# Event pages: a page for each event

Date: 2026-09-29. Decision: DS-176, **Proposed**. Nothing is built, and nothing in the store changed.

Asked for by Michael, 2026-09-29 ("Write up the proposal for event pages"), from the open item in `proposals/aeo-geo-review.md`, "Technical follow-up".

## The problem

An event has no address of its own. It shows as a row in a list or a card on the home page, and its link goes to its exhibition or its programme.

That costs two things:

| Cost | Detail |
| --- | --- |
| Google shows none of the events | Google's guidelines for events say: "Each event MUST have a unique URL (a leaf page) and markup on that URL", and "The event experience on Google only supports pages that focus on a single event" ([Google, Event structured data](https://developers.google.com/search/docs/appearance/structured-data/event), read 2026-09-29). The site's event data is sound (DS-154, DS-163) and sits on list pages, so it doesn't qualify |
| Nothing to cite or share | An answer engine asked "when is the Omer Arbel talk?" can only point to Upcoming Events, a list of 12. A person can't send a friend a link to one event |

## What the store holds

Read through the connector, 2026-09-29. 14 event entries:

| | Events |
| --- | --- |
| With a summary | 9 |
| With no summary | 5: three Explore + Create dates, Art In Good Company, the Curatorial Tour |
| With a picture of their own | 5 |
| With a registration or tickets link | 4 |
| Tied to an exhibition | 5 |
| Ended | 1 |

The event entry has ten fields (content model part 5): title, starts, ends, location, summary, image, tickets, programme page, exhibition, and keep off the home page. It can be published and read by the storefront. It can't be shown as a page: its definition has no web pages setting.

## What is proposed

Each event with a summary gets a page at `/pages/events/<handle>`, made from the fields the entry already has. No new field, no new words, and nothing for staff to do differently.

### The page

In this order, each part only when its field is filled:

| Part | From |
| --- | --- |
| A link back | The programme page, else Upcoming events |
| The title, as the page's heading | `title` |
| When | `starts`, `ends`, in the site's one format |
| Where | `location`, else the gallery's name and address from Theme settings |
| The picture | `image`, else the exhibition's key image, else the programme page's picture, as the rows do (DS-150) |
| The summary | `summary` |
| Register or tickets | `tickets`. Not shown once the event has ended (DS-147) |
| Its exhibition | A link to the exhibition's page |
| More in this programme | The programme's next events, as rows |

An event that has ended keeps its page and says so, as a past exhibition does. The registration link goes.

This is one new template, `metaobject/event`, which joins the closed set of templates (`design-system/templates.rules.json`, DESIGN.md §7). It is built from parts the site has: the page header, the details list, the event rows. No new component is expected.

### The lists

An event's title in a row or a card links to the event's own page. The line under it still names the exhibition or the programme, linked, as now (DS-71, DS-115).

### For search and answer engines

| Tag | Value |
| --- | --- |
| Title | The event's title and date: "Art Education, For Life: Reflections from Omer Arbel, November 26, 2026" |
| Description | The date, the place and the start of the summary |
| Structured data | The event is what its page is about. Rows and cards in lists name it by the same name for machines and give the page's address |
| Crumb | Home, the programme, the event |

## The thin page question

Five of the 14 events have no summary. A page for "Explore + Create, October 10" would hold a title, a date and a room, and four such pages would be the same but for the date. Search engines treat pages like that as low in value, and they can count against the site.

Shopify turns pages on for a whole entry type, not for one entry. So the theme decides:

| An event | Its page | In lists |
| --- | --- | --- |
| Has a summary | Shown in full, and search engines may list it | The title links to its page |
| Has no summary | Still answers, and asks search engines not to list it | The title links to the programme, as now |

Once a summary is added to an entry, its page turns itself on. Nobody flips a switch.

## What it needs

| Change | Where | Kind |
| --- | --- | --- |
| Web pages turned on for the event entry type, at `/pages/events/<handle>`, with the title and summary as its search listing | Store | A store write: a change to a definition |
| The template `metaobject/event`, its section, and the links in rows and cards | Theme | Code |
| The template added to the closed set | Design system | Rules file and DESIGN.md §7 |
| The event's structured data moved to its page | Theme | Code, in the `gs-data` snippets |
| `check_answers.py`: question 13 also reads an event's page | Checks | One entry in `answers.json` |

## When to turn the pages on

Turning on web pages for events adds each event to the store's sitemap. Under the live theme those addresses answer 404, as the exhibition and work pages do today (`proposals/aeo-geo-review.md`, finding 9).

| Choice | For | Against |
| --- | --- | --- |
| At release (recommended) | The live sitemap gains no more addresses that fail. The theme can be built and tested now against a development theme, with the store change made the same day the theme is published | The review theme can't show event pages until then, so Michael reviews them on a development theme |
| Now | The review theme shows the pages at once | 14 more addresses in the live sitemap answer 404 until release |

## What it costs to run

Nothing new for staff. They add an event as now. One habit helps: an event with a summary gets a page and can be found, so a sentence or two is worth typing.

The yearly tidy-up of ended events (DS-148) stays as it is. A deleted event's page then answers 404, which is right for an event two years gone.

## Left out on purpose

| Item | Why |
| --- | --- |
| A price or "free" on each event | The entry has no field for it. Google recommends it and doesn't require it. A field could come later if the gallery wants it |
| One page for a run of dates ("Explore + Create, Saturdays") | The programme page is that page already |
| Calendar files to download | Not asked for |
| New words on any page | Every part comes from a field the entry has |

## For Michael

| # | Question | Recommended | Alternative |
| --- | --- | --- | --- |
| 1 | DS-176: a page for each event | Yes, as above | Leave events as rows. Google then shows none of them, and no event can be cited or shared by link |
| 2 | Events with no summary | Their page asks not to be listed, and their rows keep linking to the programme | A page for every event, listed. Five thin pages today, four of them alike |
| 3 | When the store change is made | At release | Now, with 14 more failing addresses in the live sitemap until then |
| 4 | The address | `/pages/events/<handle>` | Another word than "events". The handle is each entry's own, such as `speaker-series-omer-arbel-2026-11-26` |
| 5 | Ended events | Keep their page, marked as ended, until the yearly tidy-up | Hide a page the day its event ends. Links to it then fail |

## If approved, the order of work

1. The template and its section, against a development theme, with the entry type's pages turned on in a way that can be undone. This is the one step that needs choice 3 settled first.
2. The links in rows and cards, and the structured data.
3. The rule for events with no summary.
4. The checks: Theme Check, the linter with the new template in its rules, `check_structured_data.py` on an event page, `check_answers.py`.
5. A pull request, with the store change logged in `proposals/store-writes/README.md` and listed in `proposals/store-changes.md` for release.

## Limits

- Whether Google then shows the events can't be tested before release. The preview is hidden from search engines.
- The count of 14 is today's. The proposal doesn't depend on it.
