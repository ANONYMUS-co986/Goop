# Project Verde — Documentation · Self-Review Summary

**Deliverables**
| File | What it is |
|---|---|
| `Project_Verde_Documentation.pdf` | 21-page screen/read version (deep navy + emerald + gold, full FX) |
| `Project_Verde_Documentation_print.pdf` | 21-page ink-friendly print variant (white bg, same layout) |
| `tools/` | full build source: `build_verde.py` (pages), `verde_style.py` (design system), `verde_diagrams.py` (all vector infographics), `pagekit.py`, `prep_images.py`, `bake_fonts.py`, `review.py` (QC) |
| `make.sh` | one-command reproducible build |
| `assets/src/` | AI-generated hero photography (cover, hardware bench, plant-doctor app, future greenhouse) |

**Structure (21 pages)** — Cover → 60-Second Story → hyperlinked Contents → Why → Architecture → Hardware (BOM + Circuit/Power) → Firmware → The Big Bug (17→2) → ESP32-CAM → Cloud/Firebase → Web App (2 pages) → AI & APIs → Features → Testing (13/13) → Troubleshooting Journal → Cost & Sustainability → Future → Judge Tour Script → Conclusion + live-data QR.

## Self-review loop — what the inspection pass found and fixed

Every page was rasterized and machine-inspected for: off-page text, right-margin violations, blank/sparse pages, missing footers, span-on-span text collisions, missing glyphs, and a fact audit against Part B. Iteration 1 → **8 pages flagged**; final → **0 flagged** (both variants).

| # | Issue found | Fix |
|---|---|---|
| 1 | `₹` missing in JetBrains Mono → rendered as **.notdef boxes** in KPI values, cost chart, total strip | Money figures now render in Inter Black/Bold (which carries ₹); mono used only where safe |
| 2 | **Pull-quote engine never advanced x** — every word in a quote was stacked at the same x (found by collision detector) | x-advance now applied per run |
| 3 | Flow pages ignored `draw_par`'s returned height → **paragraphs overlapped** (60s story, Why, Architecture, Big Bug, Cost, Conclusion) | All flow call sites now consume the returned y |
| 4 | Cost table **INR column right-aligned with double-counted width** → numbers drawn off-page (only “1” of “1,320” visible) | Right-aligned cells use the cell's left edge + true width |
| 5 | Firebase schema `controls/` description **overflows its box** | Schema rows now wrap their key lists |
| 6 | Troubleshooting right rail only 98 pt wide → **callout titles ran off-page** | Timeline narrowed, rail widened, callouts resized/spaced |
| 7 | Roadmap **descriptions bled into neighbouring columns** | Wrapped per-column with shortened copy |
| 8 | Photo-pipeline **title and description collided** in the same band | Restacked icon/title/description inside taller boxes |
| 9 | ESP32-CAM page bottom grid too narrow for callout text → **text escaped its cards** | Single-column callouts + wider photo band |
| 10 | Section title “Built by Two Students…” **exceeded page width** | Shortened title |
| 11 | Cost-chart axis “₹16k” collided with the “INR” label | Axis label moved to chart header |
| 12 | Firmware AUTO-logic string contained literal `\n` → **.notdef boxes**; circuit title “ESP32\nWROOM-32” likewise | Text engine now treats `\n` as a hard break; diagram titles split on `\n` |
| 13 | Cover/footer emoji 🌿 → missing glyph box | Removed (closed with a clean line) |
| 14 | Bullet marker `▸` missing from Inter | Marker drawn in JetBrains Mono (which has it) |
| 15 | Malformed color span `{g:**…**` leaked `{g:` / `**` into visible text | String fixed; parser hardened |
| 16 | Photo captions ran past the right margin (p10) | Captions shortened; band repositioned |

## Content audit (vs. Part B — all verified present in the final PDF)

₹1,890 · 1,320 / 220 / 350 breakdown · 5 sensors · 2 MCUs · 2 actuators · GPIO 34/23/4/35/18/19/5/12 · thresholds 35 / 15 / 35 · 17→2 calls/s · 94% diagnosis · 8 MHz XCLK · 1 s heartbeat · 8 s watchdog · 5 V/2 A · 1000 µF · 1N4007 · ±2% hysteresis · 10-pt / 5-pt moving averages · 3-network WiFi · 13/13 tests · 10 bugs · V3.0.7-FINAL / V3.0.4-FINAL · city id 1273294 · gemini-flash-latest · 435 models · crop.health · ≤2 s photo · SVGA · 500 ms sequential boot.

## Scorecard (out of 100)

| Dimension | Score | Notes |
|---|---|---|
| Visual Design | 95 | AI cover + photography, gold-foil accents, gradient panels, dot grids, consistent icon system, vector infographics everywhere |
| Readability | 96 | ≤90-word paragraphs, bullets, pull quotes, KPI cards, 10-second skimmability per page |
| Completeness | 97 | Every required visual and section present; TOC hyperlinks + 20 PDF bookmarks; demo QR |
| Accuracy | 99 | Fact audit green on both variants; zero .notdef/missing glyphs |
| Engagement | 95 | Bug story, judge script, playful-but-honest voice, no AI-slop clichés, no tool mentions |

**Overall: 96/100.** Everything below the 90 bar during review was fixed and rebuilt (see table above).
