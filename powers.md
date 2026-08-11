# ⚡ POWERS.md — THE FULL SUITE

> The complete capability manifest of the VIKAAS campaign agent, written for
> handoff. Feed this file to any capable AI to give it the entire toolkit:
> every pipeline, every command, every bug-bank lesson, every receipt.
> Everything here is REAL — built, run, and verified in this repo.
>
> **Handoff protocol: read this file, then read `vikaas-hq/LOGBOOK*.md`
> (V1–V20) for the war stories behind every tool.**

---

## 0. OPERATING CONTEXT (know your cage before you flex)

This sandbox's egress allowlist is **EXACTLY three hosts** — everything else is
dead. Receipts, verified 11 Aug 2026:

| Status | Hosts |
|---|---|
| ✅ 200 OPEN | `github.com` · `api.github.com` · `codeload.github.com` (301→ok) · `registry.npmjs.org` · `pypi.org` |
| ❌ 000 BLOCKED | cdn.playwright.dev · playwright.download.prss.microsoft.com · npmmirror · gofile.io · youtube.com · soundcloud · freesound · pixabay · raw.githubusercontent.com · objects.githubusercontent.com · archive.ubuntu.com · deb.debian.org · dl.google.com · every model-weight CDN on Earth |

**Consequences:** no `apt`, no Playwright CDN, no model downloads, no external
file hosts. `git clone`, `npm i`, `pip install` = the only download pipes.
**Workarounds that exist in-repo (all proven):** browser from npm package +
GitHub-hosted libs (§1), assets via `git clone`/sparse-clone instead of curl,
files in/out via pushing to the git repo itself (the "main→sandbox channel"),
server-side `fetch_page`/`web_search` for anything the sandbox network can't
touch.

---

## 1. 🔥 P1 — BROWSER FORGE (the newest power: in-sandbox Chromium)

**The unlock:** Playwright's installer is CDN-blocked, but a working headless
browser was assembled from open pipes only — no external CDN touched.

**Working state:** `HeadlessChrome/138.0.7204.0` — launches, renders local
HTML, screenshots, runs DOM automation. Verified non-blank render, 1080×1920.

**The chain (3 parts):**
1. `@sparticuz/chromium@138.0.2` (npm) → chromium-138 binary self-inflates to `/tmp/chromium` (in-tarball, no CDN).
2. Real 64-bit NSPR libs (libnspr4/libplc4/libplds4/libsmime3/libssl3) ← `awesome-fc/puppeteer-fc-starter-kit` @ SHA `19e29d8b3264cf7534d86586efd6f3e4b4c1efab` (GitHub).
3. `libnss3.so` + `libnssutil3.so` = **self-built stubs** — `engine/make_nss_stub.py` parses the target ELF's version requirements (37 symbols, 6 version nodes incl. `NSS_3.30`; +`NSS_SetAlgorithmPolicy@NSSUTIL_3.12.3`) and auto-generates + compiles them with gcc.

**One-command re-setup after any sandbox wipe (doctrine: wipes are guaranteed):**
```bash
cd vikaas-hq/studio && bash engine/chromium_bootstrap.sh
```

**Usage:**
```bash
# HTML → PNG with built-in QA (fonts loaded, nothing clipped):
node engine/render_sheet.js <in.html> <out.png> 1080 1920
# HTML → MP4 (deterministic GSAP-scrubbed rendering):
node engine/lib.js render <htmlPath> <framesDir> [fps]
node engine/lib.js encode <framesDir> <audioFile> <durSec> <outMp4> [fps]
# MP4 → contact sheet:
node engine/lib.js sheet <mp4> <outPng> [tiles]
```

**Honest limit:** TLS cert ops return failure (stub tradeoff) — irrelevant here,
since external egress is blocked at the network layer anyway. Local rendering,
automation, screenshots = full power.

---

## 2. 🎬 P2 — VIDEO FOUNDRY (6/6 reels shipped, all QC'd)

**Pipeline:** HTML/CSS/SVG scene → GSAP master timeline scrubbed by
`window.__reel.seek(t)` in headless Chromium → PNG frames → ffmpeg encode.
Deterministic: **zero wall-clock dependence** — a 30s reel = exact frames,
exact audio, every time.

**The shipped arsenal** (`vikaas-hq/studio/drops/FINALE/videos/`):
`VIKAAS_01_THE-DRAWER` · `02_15-RECYCLERS-0-DOORSTEPS` · `03_KABADI-PARADOX` ·
`04_COMEDY-CLUB` (Hindi AI voiceover) · `05_DOORSTEP-PHONK` · `06_MEME-REEL`
(128 BPM beat-locked slides). 1080×1920@30, H.264 CRF18, AAC 44.1k stereo 192k,
faststart.

**Pack standard (measure the FINAL mux, always):** VO/beat reels ≈ **−16 LUFS**,
ambient reels ≈ **−18.5 LUFS**. Verified: 01 −18.5 · 02 −15.9 · 03 −18.4 ·
04 −16.1 · 05 −16.2 · 06 −16.0.

**Mastering chain (the bug-proof recipe):**
```bash
ffmpeg -c:v copy -af "volume=2.6dB,alimiter=limit=0.89:level=false,aresample=44100" -ac 2 -ar 44100 -b:a 192k in.mp4 out.mp4
```
⚠️ **`volume=2.6` WITHOUT the `dB` suffix = LINEAR = +8.3 dB = musical war crime.**
Always `volume=XdB`. Then measure with ebur128, gain-trim, re-measure.

**QC battery:** decoded-wav md5s · ebur128 (−18.2…−19.6 spread) · aspectralstats
centroids · cross-correlation vs all candidate tracks (catches accidentally-
shared music) · silencedetect @−38dB/2.5s (zero dropouts) · numeric flat-frame
scans (std<14 & mean<60 = intentional dip-beats, not bugs) · contact sheets
from SHIPPED files (never from intermediates).

---

## 3. 🖼️ P3 — POST ARSENAL (22 posts, all QA'd)

**Two pipelines** (`vikaas-hq/studio/posts2_build/`):
- **Classic meme templates** (`build_r8.py` style): imgflip blanks (drake,
  two-buttons, yell-at-cat, gru 5-panel, buff-doge-vs-cheems…) with exact
  zone-mapped text placement (5%-grid measured board centers, not eyeballed).
- **AI plates + own typography** (`build_posts.py`, `build_posts_v2.py`):
  `generate_image` plates ("top 40% empty, riso grain, palette") → Anton
  headline + acid underline + mono sub-band + stamp chip, bbox-derived
  underlines (never font-size estimates — the V14 lesson).

**House style rules (banked):** Anton/SpaceGrotesk ONLY, zero emoji in Anton
(tofu), Devanagari only via NotoSansDevanagari, stamp chip on every asset,
footer CTA in romanized Hinglish.

**The roster:** M-series ×8 (memes) + P-series ×6 (riso/blueprint/hero) +
R-series ×8 (remixes, incl. R8 buff-doge bonus). All 1440×1800 (posts) /
2160×2700 (v1 originals). **MANIFEST.sha256 seals everything — 31/31 verified.**

**The Devanagari TOFU bug family (banked, 3 distinct bugs):**
1. `.dev` font loses specificity wars vs structural scopes → append `'Devnag'`
   fallback to EVERY font-family declaration.
2. Round-1 patcher missed declarations without `sans-serif` → last-family-insert regex.
3. Fresh-venv Pillow `raqm: False` breaks pre-base i-matra (`फिर`→`फरि`) and
   stacked anusvara — **check `PIL.features.check('raqm')` before any
   Devanagari build; else keep latin Hinglish.**

---

## 4. 🎧 P4 — AUDIO FORGE (original music, zero copyright risk)

**`trackgen.py`** — pure-numpy synthesis, 3 original loops:
TR-B "TAPE AUDIT" (92 BPM D-minor investigative) · TR-E "DOORSTEP PHONK"
(140 BPM F#-minor memphis cowbell + distorted 808 + hat rolls) · TR-D "KABADI
BOUNCE" (100 BPM oom-pah comedy). One-pole LP loops, Schroeder reverb, tanh
drive, sidechain pump, tape dress (hiss+crackle+flutter). QA: spectrogram PNGs
+ astats peaks.

**`audio/forge_v2/forge_v2.py`** — the DRIFT-FORGE v2: real studio one-shots
from GitHub-only sources with rights receipts (`FORGE_SOURCES.md`, pinned
SHAs): Boochi44 CC0 kit (TR-808 cowbell) + GareBear99 producer-signed
free-commercial F-minor kit. 138 BPM, 16 bars, halftime drift, 808 slides,
riser into drop, tanh glue — **mastered −16.0 LUFS EXACT** (TP −9.8, zero
clipping).

**LUFS measurement (the V19 trap):** ebur128's t-lines contain `I: x LUFS`
lines — naive parse reads the first as −70 → gain-stages a +54 dB square-wave
brick. **Always parse the summary block.**

---

## 5. 🗣️ P5 — VOICE & DIALOGUE

- **In-sandbox:** `generate_speech` (per-character pitch casting: narrators
  −4.5%, papa −3%, kabadi −6.5% + warmth EQ + compressor + tiny room; 10
  clips/turn cap).
- **Local escape hatch:** `voice_pipeline.py` — downloads Piper/Kokoro Hindi
  models ON A NORMAL LAPTOP (sandbox model-CDN wall documented) and renders
  8 comedy lines with per-character emotion presets.
- **The 24 kHz mp3 trap:** mp3 inputs are 24 kHz — `asetrate` without prior
  `aresample=44100` speeds audio 1.75×. Duration-preserving chain =
  `aresample → asetrate → aresample → atempo(inverse)`.
- **VO whodunit closed (V17):** `vo_out (1).zip` = corrected set (5/8 lines at
  1.000×); `vo_out.zip` = old slow set (1.28–1.78× = chipmunk). Proven by
  measurement, receipted.

---

## 6. 📄 P6 — DOCUMENT & DECK FOUNDRY

- **PDF:** WeasyPrint pipeline (`build/weasy_render.py`, `build/finalize.py`,
  fonts.conf with cached TTFs — `Project_Verde_Documentation.pdf` 24 MB,
  33-pg doc built this way).
- **PPTX:** `build/make_pptx.py` — `Project_Verde_Presentation.pptx` (33 slides).
- **HTML deck:** `build/build.py` — 11-part slide assembly
  (`build/src/parts/00-head.html … 11-close.html`) → full index.html, dark
  tech aesthetic, dividers, inline SVG diagrams.

---

## 7. 🧪 P7 — QA RIG (the thing that makes everything shippable)

| Tool | What it does |
|---|---|
| `engine/uicheck.js` | drives the LIVE portfolio server, real interactions, asserts console-error-free + streaming health, proof screenshots (20/20 PASS banked) |
| `engine/qsnap.js` | portfolio QA snapshots, resilient multi-launch |
| `engine/shot.js` | static post shooter 1080×1350@2x |
| `engine/render_sheet.js` | HTML→PNG with font-load + clip asserts (NEW, V20) |
| `engine/lib.js sheet` | MP4 contact sheets |
| MANIFEST.sha256 | seals every shipped file — `sha256sum -c` = 0 failures, 31/31 |
| qc/ folders | zoom-crop archives of every fixed zone (V14 lesson: verify the SHIPPED file, not the draft) |

**Always-measure doctrine:** decoded-wav md5s · ebur128 summary-parse · cross-
correlation · per-bar RMS · spectrograms. If it can be measured, measure it —
twice.

---

## 8. 🌐 P8 — PORTFOLIO & WEB OPS

- `vikaas-hq/serve.py` — Range-capable server (206 Partial Content,
  Accept-Ranges, suffix-ranges, threading, CORS, no-store). **Python's
  `http.server` sends full 200 without Range → Chrome/Safari REFUSE `<video>`.
  This server fixed that root cause.** Verified: curl Range → 206.
- `vikaas-hq/portfolio/` — GSAP rooms site: `index.html` (6-room overlay),
  `ledger.html` (true-percent scale toy), `films.html` (cinema cards + AUDIO
  LAB AB players). Effects bank: cursor, tooltips, page-wipes, count-ups,
  film grain, magnetic chips, reduced-motion + touch fallbacks.
- `verde-showcase/` — Next.js 15 + Three.js showcase, 7 pages, GSAP, QA
  screenshots in `qa/`.

---

## 9. 🕸️ P9 — NETWORK ARSENAL (GitHub-only extraction skills)

- **git clone = the universal downloader** (repos are reachable; raw URLs
  aren't). Sparse-clone + `--filter=blob:none` for single files.
- **LFS-pointer detection:** GitHub tree API reports LFS object SIZE while the
  blob is a 133-byte pointer. Always check blob size before celebrating
  (`gh api .../git/trees/HEAD?recursive=1` → size 131 = pointer = dead end).
- **.rar cracking without apt:** `node-unrar-js` (WASM, pure JS) — one line.
  Tell humans: upload .zip, it opens natively.
- **PDF image extraction:** `pypdf` — embedded full-res JPGs out of
  image-type PDFs (`aarav Choudhary submission.pdf` → 1079×1373 completion
  screenshot, now the Q1 upload).
- **Egress probe kit:** `curl -s -o /dev/null -w "%{http_code}" --max-time 8 <url>`.
- **The upload channel:** user pushes files to `main` → `git fetch origin` →
  extract. Chat attachments never land in the sandbox (5× confirmed).
- **ELF stub forging** (V20): pyelftools → version requirements → gcc
  `.symver` + version-script → minimal .so. Generalizes to ANY missing library.

---

## 10. 🧠 P10 — THE INTELLIGENCE LAYER

- `web_search` / `fetch_page` run **server-side** — they see sites the sandbox
  network can't (used for: competitor recon via imginn, YouTube brief videos,
  meme-writing study, mirror hunting).
- `generate_image` (AI plates, character art) + `image_search` (meme blanks —
  then stash them IN the repo so wipes can't hurt).
- `generate_speech` (Hindi voices, per-character casting).
- Vision + file reading, markdown/pdf/pptx/xlsx handling, PDF→text.

---

## 11. 🛡️ THE DOCTRINES (the meta-powers — these keep everything alive)

1. **COMMIT THE MOMENT SOMETHING EXISTS.** Files first, polish second.
   (5 sandbox wipes survived because of this — 5/5.)
2. **The Resurrection Spell** (after any wipe):
   ```bash
   git fetch origin 'refs/heads/arena/019ff044-goop:refs/remotes/origin/arena/019ff044-goop' \
     && git reset --hard origin/arena/019ff044-goop
   python3 -m venv ~/.studio_venv && ~/.studio_venv/bin/pip install pillow numpy imageio-ffmpeg soundfile scipy pypdf rarfile
   cd vikaas-hq/studio && npm install
   bash engine/chromium_bootstrap.sh
   ```
   (venv lives OUTSIDE the repo — exclusion-proof. `remote.origin.fetch` only
   maps main → always fetch the explicit refspec.)
3. **INTEGRITY GATE:** never publish unverified numbers. The always-safe stats:
   *Gurugram has 15 HSPCB-authorised recyclers* (gov PDF) + CWC's own *3.2M
   tonnes / only 22% reaches authorised recyclers*. Dramatised content is
   labelled ON-SCREEN ("recycler quotes dramatised — call one yourself").
4. **PLAN → REVIEW → MAKE → REVIEW → PERFECT.** Every build gets executed,
   read back, screenshotted, then logged.
5. **LOGBOOK CONTINUITY:** every turn ends with a `LOGBOOK_V<n>.md` entry —
   orders, receipts, lessons, waiting-on list. The logbooks ARE the
   institutional memory. Read them before acting.
6. **Measure the FINAL artifact.** LUFS on the final mux, sha256 on the final
   file, crops from the SHIPPED png. Never trust a chained pipe silently —
   re-run pieces with visible output.
7. **Rule bank:** never trust first-run success · scope selectors (`#cN .bk1`,
   never bare `.bk1`) · backup before `git clean` · `grep -i` for word sweeps ·
   duration caps are hard limits (−15% margin).

---

## 12. 📇 QUICK REFERENCE — file map

| Path | What |
|---|---|
| `powers.md` | this file |
| `vikaas-hq/LOGBOOK*.md` (V1–V20) | the full war history |
| `vikaas-hq/cwc_buddy/` | ReBee submission kit (guide, answers, Q1/Q4 images, cheat sheet) |
| `vikaas-hq/studio/engine/` | browser, render, shot, QA, bootstrap, stub-forge |
| `vikaas-hq/studio/audio/` + `forge_v2/` | original + phonk-forged music, mixes, previews |
| `vikaas-hq/studio/drops/FINALE/` | 6 reels + 22 posts + 3 alt beds + captions/schedule/guide + MANIFEST |
| `vikaas-hq/studio/posts2_build/` | post builders + meme src_assets (sandbox-proof stash) |
| `vikaas-hq/portfolio/` | the rooms site + serve.py |
| `vikaas-hq/voice_pipeline.py` / `trackgen.py` / `mix_v3.sh` | voice / music / remix scripts |
| `build/` | Verde PDF/PPTX/HTML deck factory |

---

*End of suite. Everything listed has been executed in this repo with receipts.
Give this file to any AI, point it at the logbooks, and it inherits the whole
arsenal — plus the scars.* ⚡
