# Project Verde — Definitive Documentation

A 34-page, print-ready documentation PDF for **Project Verde**, the smart IoT
irrigation & plant-care system built for **DAV ACON 5 — Tech Exhibition 2026**
by Aarav Choudhary & Anuj (Class X).

The document is generated from Python source with **ReportLab** (Platypus +
custom canvas), **matplotlib** (data charts), hand-authored **SVG diagrams**,
and **AI-generated imagery** for the cover and photo placeholders. It uses a
deep-navy + emerald + gold design system with Space Grotesk / Inter / JetBrains
Mono type.

## Quick start

```bash
./build.sh        # creates .venv, fetches fonts, builds the PDF
# or manually:
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python doc/build.py
```

Output: **`build/Project_Verde_Documentation.pdf`**

## What's inside

| File | Purpose |
|---|---|
| `doc/build.py` | Assembles the whole document (content + layout). |
| `doc/theme.py` | Design system: palette, fonts, drawing helpers. |
| `doc/diagrams.py` | Charts (matplotlib) + SVG vector diagrams. |
| `doc/flowables.py` | Custom flowables (cards, callouts, figures, quotes). |
| `doc/pages.py` | Page templates: cover, chapter dividers, content pages. |
| `doc/outline.py` | Post-processing: PDF bookmarks/outline + metadata. |
| `assets/img/*` | AI-generated cover art + photo placeholders. |
| `assets/charts/*` | Rendered diagrams (auto-generated). |
| `assets/fonts/*` | Inter, Space Grotesk, JetBrains Mono (static instances). |
| `UNIVERSAL_MASTER_PROMPT.md` | The original brief this was built from. |

## Self-review process

The build iterates through a render → inspect → audit → fix loop (see
`doc/REVIEW_SUMMARY.md`). Programmatic checks cover page count, blank pages,
text overflow beyond margins, image embedding, and the PDF outline.
