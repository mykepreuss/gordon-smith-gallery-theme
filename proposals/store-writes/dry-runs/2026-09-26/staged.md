## Staged page text

8 pages. Stop if any page's live text changed since `snapshots/pages-2026-09-25.json`. After the pages, delete the staged values and the `release_body` definition. Rollback: restore each page's text from the snapshot.

| Page | Live text | At release |
| --- | --- | --- |
| `about` | matches the snapshot | 942 characters (was 2234) |
| `about-us` | matches the snapshot | cleared |
| `artists` | matches the snapshot | 7098 characters (was 9441) |
| `donate` | matches the snapshot | 3673 characters (was 3502) |
| `gordon-and-marion` | matches the snapshot | 2484 characters (was 2293) |
| `on-now` | matches the snapshot | cleared |
| `upcoming-events` | matches the snapshot | cleared |
| `upcoming-exhibitions` | matches the snapshot | cleared |

All pages match: ready.
