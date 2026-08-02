# Self-Review Summary — Project Verde Documentation

Build → render → audit → fix loop. Below is what changed between the first
render and the delivered PDF, plus the self-score.

## Review loop (what I checked)
1. **Render** — built the PDF, rasterised every page, measured ink/white
   coverage to catch blank or broken pages.
2. **Overflow audit** — extracted every word's bounding box and flagged any
   text spilling past the right margin or the page edge.
3. **Completeness audit** — every section from the brief present; all key
   numbers verified against Part B (₹1,890, 5 sensors, 2 MCUs, 17→2 calls,
   94% diagnosis, 8 MHz, GPIO pins, thresholds 35/15/35).
4. **Fixed below-90 issues** and rebuilt.

## Issues found & fixed
| # | Problem | Fix |
|---|---|---|
| 1 | Running header showed the *last* section on every page | Added a zero-size `Section` marker flowable + `onPageEnd` hook so each page's header reflects its own chapter. |
| 2 | Callout boxes drew body text as one unbroken line → overflowed the margin | Rewrote `Callout` to word-wrap body text and size its own height. |
| 3 | Plain-string table cells didn't wrap → BOM, market, and cost tables spilled off-page | Converted data cells to `Paragraph`s; fixed header row text colour. |
| 4 | Chapter divider titles too long → "Troubleshooting" ran off the page | Divider title now word-wraps across up to two lines. |
| 5 | Moisture watering-cycle chart was built but never placed | Added it to the Firmware chapter with a threshold-marker caption. |
| 6 | Figure captions could overflow at long lengths | Shortened the long caption; added wrapping to the figure caption flowable. |
| 7 | No bookmarks / metadata | Added a PDF outline (12 entries) + title/author metadata. |
| 8 | Blank-page risk from full-bleed pages + template switches | `FullPage` leaves a small sliver so `NextPageTemplate` lands on the same page — zero blank pages (34/34 carry content). |

## Final self-score (out of 100)
- **Visual design** — 93  (full-bleed cover, gradient dividers, cohesive palette, vector diagrams)
- **Readability** — 94  (short paragraphs, bullets, KPI cards, pull quotes, generous whitespace)
- **Completeness** — 98  (all briefed sections + figures present)
- **Accuracy** — 99  (all figures cross-checked against Part B)
- **Engagement** — 93  (bug story, judge tour script, honesty callouts)

**Overall: 95 / 100**

*Caveat: automated layout QA (overflow, blanks, image embedding, page count,
bookmarks) was verified programmatically; final visual polish benefits from a
human eyes-on pass of the rendered previews in `build/render/`.*
