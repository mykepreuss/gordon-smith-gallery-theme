---
id: gsg:framework:zero-click
type: framework
title: Zero-click evaluation framework for the Gordon Smith Gallery
owner: gordon-smith-gallery
status: proposed
last_reviewed: 2026-09-28
source: new theme preview, read 2026-09-28
tags:
  - framework
  - zero-click
  - aeo
  - geo
  - ai-search
  - attribution
scope: organization
links:
  - rel: DEPENDS_ON
    href: "aeo/aeo-framework.md"
  - rel: DEPENDS_ON
    href: "aeo/aeo-query-set.md"
---

# Zero-click evaluation framework for the Gordon Smith Gallery

AI answers create a zero-click reality for galleries too.

People often decide whether to visit, bring their kids, book a class, buy a print or donate before they ever open the site. Many never open it. They ask for the hours, get an answer and walk in.

For a gallery that is a good result, as long as the answer was right.

Use this framework to:

- define what visibility means when the first contact happens in chat or on a map
- choose signals that match how people find a gallery
- decide which pages to fix first

## 1) AI answer presence

**Definition:** How often the Gordon Smith Gallery appears in AI answers for the right name, place and topic questions.

Name questions: "Gordon Smith Gallery hours". Place and topic questions: "art galleries in North Vancouver", "things to do with kids on the North Shore on Saturday", "art camps for kids in North Vancouver", "where to buy Canadian limited edition prints".

**How to measure:**

- a fixed prompt set from `aeo/aeo-query-set.md`, plus five place and topic prompts
- before that, `design-system/scripts/check_answers.py`, which confirms the site itself still holds each answer (DS-167). An engine can't repeat a fact the page has lost
- presence rate across answer engines
- citation rate for gordonsmithgallery.com pages

**How to improve:**

- a plain identity sentence on About and the home page. In the description and `/llms.txt` now; the sentence on the page waits for the gallery
- written meta descriptions. Drafted and staged for 40 pages and the home page (DS-160)
- visit and program questions on the FAQ page. Visiting questions are drafted for the gallery

## 2) Answer correctness

**Definition:** The facts in the answer are right today. For a place, a wrong answer costs a wasted trip.

**How to measure:**

- hours, address and admission match `/pages/plan-your-visit`
- the current exhibition and its dates match the exhibition page
- program ages, times and costs match the program page
- the answer does not show the office hours as the gallery hours

**How to improve:**

- one source for each fact. The footer, Plan your visit, the `ArtGallery` structured data and `/llms.txt` all read the hours from Theme settings, and `check_answers.py` fails if the data and the page disagree
- settle the office hours, which differ between Plan your visit and Contact
- state holiday and summer closures
- keep the map and business listings outside the site in step with the site

## 3) Branded demand and direct intent

**Definition:** More people arrive already knowing what the gallery is and what they came for.

**How to measure:**

- branded search for "Gordon Smith Gallery", "Artists for Kids" and "Smith Foundation"
- direct and typed-in visits
- visits that start on a deep page (an exhibition, a program, an edition) and not the home page
- messages to staff that name a program or exhibition

## 4) Entity clarity

**Definition:** AI systems hold a steady model of four things: the gallery, Artists for Kids, the Smith Foundation and Gordon Smith the artist.

**How to measure:**

- the gallery is called a public art gallery in North Vancouver, not a shop and not a commercial gallery
- Gordon Smith is described as the artist, with the right dates
- Artists for Kids and the Foundation are not swapped or merged
- founding dates are right: 1989 for the program, 2002 for the Foundation
- the same name and spelling come back across engines

**How to improve:**

- one first-mention name for the gallery, one spelling of Artists for Kids
- `Person` and `Organization` structured data with `sameAs` links. The data is built (DS-163). The `sameAs` links wait for the gallery's profiles
- a short comparison of the three organizations on About

## 5) Conversational fit-screening

**Definition:** Parents, teachers, collectors, donors and students use AI to decide whether the gallery is for them before they reach out.

| Who asks | What they screen for | Page that must answer |
| --- | --- | --- |
| Parents | Ages, cost, drop-in or registered, supervision | `/pages/explore-create`, `/pages/classes-and-camps` |
| Teachers | Class visits, grade fit, booking, professional development | `/pages/schools-and-teachers` |
| Seniors and caregivers | Time, cost, access | `/pages/art-in-good-company`, `/pages/plan-your-visit` |
| Collectors | Edition size, price, framing, shipping, where the money goes | Product pages, `/pages/shop`, `/pages/frequently-asked-questions` |
| Donors | Which organization, tax receipt, what a gift does | `/pages/donate`, `/pages/support-artists-for-kids` |
| Graduating students | Which award, who can apply, amount, deadline | `/pages/smith-foundation-scholarships`, `/pages/awards-and-scholarships` |
| Volunteers | Roles, how to apply | `/pages/volunteer` |

**How to measure:**

- how often staff answer questions the site should have answered
- whether enquiries reach the right organization first time
- registrations and applications from people who meet the criteria

**How to improve:**

- state who each program is for, and its limits, near the top
- explain the two donation routes and the two sets of scholarships side by side

## 6) Blurred attribution

**Definition:** The decision happens in chat or on a map. It shows up later as a walk-in, a direct visit, a phone call or a registration with no source.

**How to measure:**

- direct visits after an exhibition opens or a portfolio launches
- "how did you hear about us?" at the front desk, on registration forms and at events
- shop orders and donations with no referring site
- referrals from answer engines in the site's analytics

Walk-ins will never be fully attributed. A simple tally at the front desk is enough.

## 7) AI as first screener

**Definition:** The first reader is often an AI system summarizing the gallery to someone else. It may also be an agent that buys. The site's `/llms.txt` tells the first kind what the gallery is, where each fact lives and how to keep the four entities apart (DS-166). Shopify's `/agents.md` tells the second kind how to check out.

**How to improve:**

- write for extraction: direct answers, hours and prices in lists, dates in full, FAQs
- write for people: the gallery's own voice, its purpose, the artists' names
- keep structured data and visible text the same
- give product pages complete facts. Edition size, medium, dimensions, paper and signature are there already

## Gallery scorecard

Use a small monthly scorecard:

| Signal | Source | Target |
| --- | --- | --- |
| The site holds each answer | `check_answers.py` | No errors. Known gaps falling |
| Answer presence for the priority queries | Manual run of the query set | Rising |
| Hours, address and admission correct | Manual run | Every engine, every time |
| Current exhibition correct | Manual run | Every engine within two weeks of opening |
| Four entities kept apart | Manual run | No blended answers |
| Citations of gordonsmithgallery.com | Manual run | Rising |
| Branded search and direct visits | Site analytics, search console | Rising |
| Program registrations and event attendance | Registration records | Steady or rising |
| Shop orders and donations | Store and Foundation records | Steady or rising |
| Front desk "how did you hear about us?" | Tally | AI tools and maps named |

The baseline run waits for release. The preview is hidden from search engines and answer engines, so they still describe the current site.

## Upgrade priorities

If results are weak, upgrade in this order:

1. visit facts: one set of hours, closures stated, listings outside the site in step
2. entity clarity on About, Gordon and Marion, Artists for Kids and the Foundation
3. who each program is for, on the program and schools pages
4. the FAQ page, widened beyond the shop
5. shop limits: where it ships, what is pickup only
