# src_assets — meme blanks & photo stash (TRACKED, sandbox-immortal)
All builder scripts read from HERE (never from the volatile `image-search/` cache).

## Rebuild-ready (verified identical to the shipped masters' sources)
| file | source | used by |
|---|---|---|
| `buttons.png` (640×968) | reddit r/MemeRestoration two-buttons-at-once (Jake-Clark sig kept) | M2 |
| `dbf.png` (800×1433) | imgflip 379293870 "Distracted Boyfriend Full Version" | M6 |
| `cat.jpg` (2153×1711) | imgflip 211447548 "Woman Yelling At A Cat HD" | M7 |
| `gru.png` (624×639) | imgflip 205746517 "Gru's plan 5 panel" | M8 |
| `photo_pole.jpg` (574×800) | pinimg pole w/ posters (same as shipped R2) | R2 |
| `photo_drawer.jpg` / `photo_ewaste.jpg` / `photo_kabadi.png` / `photo_screwdriver.jpg` | stash photos | R5 |

## Parked — rebuilds of these need a re-source + zone re-verification FIRST
| file | issue | affects |
|---|---|---|
| `drake.jpg` (640×550) | layout UNSURE (may not be the 2-panel vertical zones assume) | M1 |
| `panik_cand1/2.jpg` (~250px) | panel ORDER unknown; shipped M5 = imgflip **228718970 "Kalm-panik-kalm"** (765×1020) | M5 |
| `cmm.jpg` (1420×1113) | = imgflip 155418953; shipped M3 used 3mfdo — sign board geometry differs → rotcover zone re-tune needed | M3 |
| `puppet.png` (631×484) | believed same family as shipped M4; verify side-by-side before rebuild | M4 |
| `photo_gate.png` (140px) | placeholder (accio supplier thumb) | R5 future |

**Rule:** M1/M3/M4/M5 masters in `drops/FINALE/posts/` are FROZEN — do not overwrite from these sources without visual QC vs the committed master.

| `doge_cheems_247758660.png` (880×480) | imgflip template **247758660 "Buff Doge and Crying Cheems"** community blank; white bg, corners verified clean (no watermark); fetched 8 Aug via brave image search | R8 |
**R8 note:** built by `build_r8.py` (one-off, house-style). Footer caption kept in latin Hinglish on purpose: fresh-venv Pillow reports `raqm=False` → Devanagari pre-base i-matra ("फिर") + stacked matra-anusvara ("लाशें") break. If Devanagari needed in future builds, verify `PIL.features.check('raqm')` first or stay latin.
