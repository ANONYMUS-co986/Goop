# Project Verde — Definitive Documentation

A 21-page, presentation-grade documentation PDF for **Project Verde**, the smart
IoT irrigation & plant-care system built for **DAV ACON 5 — Tech Exhibition 2026**
by Aarav Choudhary & Anuj (Class X).

## Deliverables

| File | What it is |
|---|---|
| `Project_Verde_Documentation.pdf` | **The deliverable** — 21-page screen/read version (deep navy + emerald + gold, full FX) |
| `Project_Verde_Documentation_print.pdf` | Ink-friendly print variant (white pages, same layout) |
| `REVIEW_SUMMARY.md` | Self-review loop: issues found & fixed, fact audit, scorecard (96/100) |
| `make.sh` | One-command reproducible build |

## What's inside the document

Cover (AI-generated art) → The Whole Story in 60 Seconds → hyperlinked Contents →
Why → Three-Tier Architecture → Hardware (BOM, circuit, power lessons) →
Firmware + the 17→2 calls bug story → ESP32-CAM → Firebase schema → Web App
(2 pages) → AI & APIs with accuracy notes → Features → Testing (13/13) →
Troubleshooting journal (10 bugs) → Cost & Sustainability → Future Scope →
3-minute Judge Tour Script → Conclusion with live-data QR.

Everything is vector-drawn by hand in ReportLab: architecture diagram, circuit
pin map, Firebase schema tree, AUTO-mode flowchart, before/after bug
infographic, cost comparison chart, moisture watering-cycle chart with the 35%
threshold marker, 1-second heartbeat timeline, firmware scheduler, camera
pipeline, API fallback chains, and roadmap. Photography is AI-generated
(cover, hardware bench, plant doctor, future greenhouse) and colour-graded to
the palette. The PDF has a hyperlinked TOC, 20 bookmarks, and a scannable QR.

## Quick start

```bash
./make.sh     # venv -> fonts -> images -> PDF (dark + print) -> self-review
```

Requires internet for `pip` on first run. Source fonts (`fonts/*-var.ttf`) and
AI art (`assets/src/*.png`) are committed; everything else is regenerated.

| Dir | Purpose |
|---|---|
| `tools/build_verde.py` | Page assembly, bookmarks, hyperlinked TOC |
| `tools/verde_style.py` | Design system: palette, fonts, text engine, icons |
| `tools/verde_diagrams.py` | All vector infographics |
| `tools/pagekit.py` | KPI cards, callouts, pull quotes, tables, photos |
| `tools/pages_front|mid|back.py` | The 21 pages |
| `tools/prep_images.py` | Image grading, FX overlays, gradients, QR |
| `tools/bake_fonts.py` | Static font weights from variable fonts |
| `tools/review.py` | Rasterized QC: overflow, collisions, glyphs, fact audit |

## Self-review (mandatory loop, completed)

Every page was rasterized and machine-inspected for off-page text, margin
violations, blank/sparse pages, text collisions, missing glyphs, and a fact
audit against the brief. Iteration 1: 8 pages flagged → final: **0 flagged**
on both variants. Details and scorecard: `REVIEW_SUMMARY.md`.

## Original brief

`UNIVERSAL_MASTER_PROMPT.md` — the source of truth for every number in the
document (₹1,890 · 5 sensors · 17→2 calls/s · 94% · 8 MHz · thresholds 35/15/35 …).
