# ⚡ POWERS.md — THE COMPLETE TECHNICAL SUITE (BRAIN + HANDS)

> The full capability manifest of the VIKAAS studio agent — **every power
> unlocked, top to bottom, nothing omitted**. Feed this to any AI to hand it
> the whole arsenal: the deterministic HTML→MP4 engine, the GSAP techniques,
> the in-sandbox browser forge, the audio synthesizers, the FX component
> library, the AI-native generation powers, the QA rig, the research brain,
> the memory system, and every bug-bank lesson.
>
> Everything here is REAL — built, run, and verified in this repo
> (`vikaas-hq/studio/`, `build/`, `verde-showcase/`, `vikaas-hq/portfolio/`).
> The logbooks (`vikaas-hq/LOGBOOK*.md` V1–V20) hold the war stories and
> receipts behind every claim.

---

# PART A — THE BRAIN 🧠

## A1. AI-NATIVE GENERATION POWERS

| Power | What it does | Techniques banked |
|---|---|---|
| **generate_image** | text-to-image + image-edit (reference-based) | **"amateur-snapshot" technique**: prompt for phone-photo realism (no studio-gloss cues) so AI art passes as a genuine photo; **"plate" technique**: `"top 40% perfectly empty, no text, riso grain, palette"` → clean typography space (6/6 first-try success); **character consistency**: feed the SAME character image as reference for every new pose (copper body, green visor eyes, gauge chest — the bee stayed one character across 6 renders) |
| **image_search** | pulls real images from the web | meme-template sourcing (imgflip blanks verified by template ID); **stash everything in-repo** (`src_assets/`) so sandbox wipes can't lose them; verify originals against known template IDs |
| **generate_speech** | TTS with per-character voice casting | pitch casting: narrator −4.5%, papa −3%, kabadi −6.5% + warmth EQ + compressor + tiny room; **10 clips/turn cap** — budget VO scripts around it |
| **add_voice** | audition + register a voice for reuse | multi-voice consistency across clips — one voice_id per character |
| **web_search / fetch_page** | SERVER-SIDE browsing — sees sites the sandbox network can't | competitive recon (social viewers: imginn/greatfon/dumpor), YouTube brief videos, meme-writing study, mirror hunting, license vetting. **THE research pipe for everything the sandbox can't reach** |
| **Vision + file reading** | read images inline, parse PDF/PPTX/XLSX/MD | pypdf extracts embedded full-res JPGs from image-type PDFs; PDF→text; spreadsheet roundtrip verification |

## A2. THE RESEARCH & INTELLIGENCE METHOD

- **Recon loop:** search → verify (2 sources minimum) → cite → stash evidence files in-repo.
- **Competitive intel:** public-profile study via server-side viewers; learn the rival's tactics (audio, caption structure, meme formats, hashtags), then counter with receipts.
- **Licensing diligence:** every asset (music, samples, images) gets a rights verdict BEFORE shipping: CC0 / producer-signed-free / CC-BY (with the attribution line stored in `seed/CREDIT.md`) / rejected. `FORGE_SOURCES.md` and `CHROMIUM_LIBS_SOURCES.md` are the receipt ledgers.
- **"Study from the web" loop:** before building a content type, search for the principles, bank them (meme formats: proven templates first, 5–12 words/line, ONE idea per meme, spoken language, platform-fit crops).
- **TTS/model gauntlet docs:** every attempted model download (piper, kokoro, edge-tts, HF) logged with per-attempt results — the failure map is itself a power (knows exactly what's blocked where).

## A3. THE MEMORY SYSTEM (institutional brain)

- **Logbook continuity:** every work turn ends with `LOGBOOK_V<n>.md` — orders, what shipped, receipts, lessons banked, bug family, waiting-on list. V1–V20 exist. **A new AI reads the logbooks first, then acts.**
- **Format:** `## Entry` → order quoted → deliverables → QA receipts → lessons → branch state → "still waiting on".
- **Commit-early doctrine:** commit the moment something exists; polish second. (Survived 5 sandbox wipes — 5/5.)
- **The Resurrection Spell** (after any wipe — see B11).
- **The Rule Bank** (see B12) — every hard-won bug lesson, codified.

## A4. JUDGMENT & QA BRAIN

- **PLAN → REVIEW → MAKE → REVIEW → PERFECT.** Every build executed, read back, screenshotted, then logged.
- **Always-measure:** if it can be measured, measure it — twice. Final artifact only (see B9).
- **Integrity judgment:** never publish unverified claims; dramatised content labelled on-screen; safe variants for everything.
- **Self-review catches:** the QA rig exists because self-review catches real bugs (letterboxing, hidden parents, tofu, clipped callouts, duplicate music, misordered panels).
- **Phased delivery:** go slow, stay phased — one build per turn, verified, then the next.

---

# PART B — THE HANDS 🛠️

## B1. 🔥 THE CORE POWER — DETERMINISTIC HTML→MP4 VIDEO ENGINE

### The design contract
Any video is a **webpage** whose JS exposes exactly one global:
```js
window.__reel = { duration: 27.2, seek(t) { /* drive everything from t */ } }
```
The engine scrubs `t` from 0→duration in a headless browser, screenshots a
frame at every step, encodes to MP4. **Zero wall-clock dependence** — no
timers, no rAF. The same reel renders identically every time, frame-for-frame.

### Commands
```bash
node engine/lib.js render <htmlPath> <framesDir> [fps]      # HTML → PNG frames
node engine/lib.js encode <framesDir> <audioFile> <durSec> <outMp4> [fps]  # → MP4
node engine/lib.js sheet  <mp4> <outPng> [tiles]            # MP4 → contact sheet
node engine/probe.js      <htmlPath> <outPng> [times...]    # seek KEY BEATS → tiled probe sheet
```
- Typical reel: 1080×1920@30, H.264 CRF18, AAC 44.1k stereo 192k, faststart.
- **Probe discipline:** before full render, probe 14 key beats into ONE tiled
  sheet (14 frames = 30 seconds of QA) — catch layout/beat bugs at 2% of the cost.
- 816–1224 frames per 27–41s reel; ~0.35s/frame capture.

### Audio baked at encode time
- Mix bed + VO in ffmpeg first, feed the mix to `encode`.
- **Mastering chain (bug-proof):**
  ```bash
  ffmpeg -c:v copy -af "volume=2.6dB,alimiter=limit=0.89:level=false,aresample=44100" -ac 2 -ar 44100 -b:a 192k in.mp4 out.mp4
  ```
  ⚠️ **`volume=2.6` WITHOUT `dB` = LINEAR = +8.3 dB. Always the `dB` suffix.**
- **LUFS standard:** measure the FINAL mux (ebur128), gain-trim, re-measure.
  Beat/VO reels ≈ −16 LUFS; ambient ≈ −18.5.
- **ebur128 parse trap:** t-lines contain `I: x LUFS` — naive parse reads −70 →
  +54 dB square-wave brick. **Parse the SUMMARY block.**
- **24 kHz mp3 trap:** `asetrate` without prior `aresample=44100` speeds audio
  1.75×. Duration-preserving: `aresample → asetrate → aresample → atempo(inverse)`.

## B2. 🎬 GSAP MASTERCLASS

### Timeline architecture
- ONE master timeline per reel; nested scenes added at offsets; scrub via
  `tl.progress(t/duration)` or `tl.seek(t)`.
- Count-ups/tallies: animate a `value` object from the seek handler, render in
  an update hook — scrub-safe, no rAF.
- Transform-only discipline: opacity/transform/xPercent only (layout props
  reflow mid-capture and break determinism).

### Beat-locking
- Cut times from math, never feel: `C(n) = n * 60/bpm` (140 BPM → 0.4286s;
  128 BPM bar = 1.875s).
- Structure: intro bars → hook → drop lands on a bar start; risers sweep into
  the drop; flash/dip beats before section changes (read as style, not bugs).

### The FX bank (all shipped)
- **RGB-split flares:** two `.lay` copies, `mix-blend-mode:screen`, red/blue,
  few px offset. GOTCHAS: `.lay` copies must be `position:absolute` INSIDE a
  relative `.big` parent (else reflow); screen blend only reads on DARK scenes
  — cream scenes get shake-only.
- Whip-blur entrances · VHS streaks · viewfinder brackets + REC pulse · Ken
  Burns (scale transforms) · easeOutBack pops · beat lamps · shake bursts ·
  flash frames · scanlines · SVG logo draw-on (stroke-dashoffset scrubbed by
  t) · strikethrough punchlines · footer progress + handle.

### GSAP gotchas banked
1. Bare class selectors match only the FIRST scene — **scope `#cN .bk1`**.
2. Overlay layers absolute inside relative parents, always.
3. `document.fonts.ready` before first capture; `@font-face` → local TTFs only.
4. **Devanagari TOFU family (3 bugs):** (a) `.dev` loses specificity wars →
   append `'Devnag'` fallback to EVERY font-family decl; (b) patchers that
   only fix decls containing `sans-serif` miss others → last-family-insert
   regex; (c) Anton has NO Devanagari glyphs — Hindi needs
   NotoSansDevanagari in the stack.
5. Blend-mode behavior differs dark vs light scenes.

## B3. 🖥️ THE BROWSER FORGE (how the headless browser exists)

Playwright's installer is CDN-blocked; the browser is **assembled from open
pipes only** (npm + GitHub + PyPI). TWO working paths:

**Path 1 — legacy (`/tmp/al2023`, used by qsnap/shot/uicheck/probe):**
brotli-decompress `al2023.tar.br` from inside the `@sparticuz/chromium` npm
package → extract to `/tmp/al2023` → `LD_LIBRARY_PATH=/tmp/al2023/lib`.
Self-healing: each tool checks for the libs and re-extracts if missing.

**Path 2 — V20 (`/tmp/chromelibs` + system install):**
1. `@sparticuz/chromium@138.0.2` (npm) → binary self-inflates to `/tmp/chromium`.
2. Real 64-bit NSPR libs ← `awesome-fc/puppeteer-fc-starter-kit` @ SHA
   `19e29d8b3264cf7534d86586efd6f3e4b4c1efab` (sparse-cloned, GitHub).
3. `libnss3.so`/`libnssutil3.so` = self-built stubs — `make_nss_stub.py`
   parses the ELF version requirements (37 symbols, 6 nodes incl. `NSS_3.30`)
   and compiles them with gcc.
4. `sudo cp` + `ldconfig` → zero env vars needed.

**One-command re-setup after any wipe:**
```bash
cd vikaas-hq/studio && bash engine/chromium_bootstrap.sh
```

**Honest limits:** NSS stub = TLS cert ops fail (irrelevant — egress is
network-blocked anyway). Local rendering, screenshots, DOM automation = full.

## B4. 🖼️ STATIC POSTS THROUGH CODE

- **Pipeline A — meme templates:** imgflip blanks + **zone-mapped text**
  (5%-grid measured board centers, never eyeballed). Multi-panel: short words
  per board + payoff board.
- **Pipeline B — AI plates + own typography:** generate plate ("top 40%
  empty, riso grain, palette") → Anton headline + acid underline + mono
  sub-band + stamp chip.
- **Underlines bbox-derived:** `multiline_textbbox` → real block geometry.
  Never `font_size * 1.06` estimates.
- **raqm check:** `PIL.features.check('raqm')` before Devanagari builds, else
  latin Hinglish (`फिर`→`फरि` shaping breaks otherwise).
- Zero emoji in Anton; stamp chip + footer CTA; grain ~4.5%.
- QA: full-canvas sheet + zoom crops of every text zone, from the SHIPPED file.

## B5. 🎧 AUDIO SYNTHESIS (music from pure code)

### `trackgen.py` — pure-numpy techniques
- One-pole LP loops · Schroeder combs+allpass reverb · tanh drive chain ·
  sidechain pump · tape dress (hiss+crackle+flutter).
- Genre rules: drama = pad+air; phonk = 8th grid + saturation; comedy =
  silence between oom-pahs so VO lands.
- QA: spectrogram PNGs + `astats` peaks.

### `forge_v2.py` — sample-locked sequencing (Drift-Forge v2)
- Real one-shots from GitHub-only sources, rights-ledgered
  (`FORGE_SOURCES.md`, pinned SHAs): Boochi44 CC0 TR-808 kit + GareBear99
  free-commercial phonk kit.
- 138 BPM, 16 bars: halftime drift (kick {0,14}+pumps, snare on 8, rolling
  16ths w/ swing + 32nd rolls), cowbell riff, 808 slide into drop, sidechain
  duck (bells 0.30/808 0.5), tanh glue, riser at bar 12.
- **Mastered −16.0 LUFS EXACT** (TP −9.8, zero clipping), per-bar RMS proof.

### Licensed-bed stack
- `seed/Thinking_Music.mp3` (CC-BY Kevin MacLeod) with the REQUIRED
  attribution line stored in `seed/CREDIT.md` — never ship CC-BY without it.
- Finale alt beds: TR_A/B/C + M16 masters (`audio/finale/`).
- VO clips: `audio/fx/c1..c8.m4a` (8 comedy character lines).

## B6. 🗣️ VOICE & DIALOGUE

- In-sandbox speech with per-character pitch casting (see A1).
- **Timing discipline:** probe clip durations FIRST, build the timeline
  BACKWARD from the VO so jokes land (bounce at whistle-down, elastic at
  boing, tag at honk).
- **Local escape hatch:** `voice_pipeline.py` — downloads Piper/Kokoro Hindi
  models on a NORMAL machine (sandbox model-CDN wall documented), renders
  lines with per-character emotion presets. `colab_voice_gen.ipynb` = Colab
  route. `VOICE_RERECORD_GUIDE.md` = human re-record protocol.
- `mix_v3.sh` = per-line VO chain: silence-trim → highpass → comp → 3.2k
  presence → tempo-fit → sidechain duck → loudnorm.

## B7. 📄 DOC & DECK FOUNDRY

- **HTML deck:** `build/build.py` assembles `build/src/parts/*.html`
  (00-head … 11-close) → single index.html, dark-tech aesthetic, dividers,
  inline SVG, fonts bundled woff2+ttf.
- **PDF, two routes:**
  - Chromium print-to-PDF: `build/render.js` (pixel-perfect, page-classed).
  - WeasyPrint: `build/weasy_render.py` + `build/finalize.py` + fonts.conf.
- **Slides:** `build/render_slides.js` — deviceScaleFactor 3.125 = exactly
  300 DPI on A4 portrait.
- **PPTX:** `build/make_pptx.py` (33 slides shipped).
- **PDF visual review:** `build/preview.py` — PyMuPDF renders every PDF page
  to PNG + contact sheets.
- **Self-healing system libs:** `build/stack/gperf.py` (gperf-compatible
  generator — lets fontconfig build from source without gperf) + fonts.conf.
  The pattern: when a system tool is missing and apt is blocked, build it
  from source with a tiny stand-in for its exotic deps.

## B8. 🌐 WEB OPS, SITES & THE FX COMPONENT LIBRARY

- **`vikaas-hq/serve.py` — Range-capable static server** (206 Partial
  Content, Accept-Ranges, suffix-ranges, threading, CORS, no-store).
  ⚠️ Python `http.server` sends full 200 without Range → Chrome/Safari REFUSE
  `<video>`. Verify: `curl -H "Range: bytes=0-100"` → 206 + Content-Range.
- **The full FX component library** (`verde-showcase/components/fx/` — 22
  components, all ship-ready):
  ClickSpark · CountUp · Cursor · GlowCard · Grain · Magnetic · Parallax ·
  PixelCard · Preloader · Reveal · RotatingText · Scramble · ScrollStack ·
  ShinyText · SmoothScroll · SplitReveal · StarBorder · StormCanvas · Switch ·
  TiltCard · Tip · VelocityMarquee
- **Nav:** Burger (animated menu) · TransitionLink (page-wipe routing) ·
  nav.ts (scroll-aware).
- **Three.js:** HeroCanvas (3D hero) · BuildCanvas (product build viz) ·
  HeroSection · ViewportPause (perf).
- **Section:** FabGate (floating action gate).
- **Portfolio effects layer** (`vikaas-hq/portfolio/assets/site.js` +
  `site.css`): burger topbar + room overlay, custom cursor with labels,
  tooltip engine (clamped), reveal-on-scroll (io-staggered), page-wipe
  transitions, magnetic chips, count-up-on-view, film grain, marquee, boot
  bar — ALL with `prefers-reduced-motion` + touch fallbacks, transform-only.
- **Live QA on real servers:** `engine/uicheck.js` drives the LIVE server
  (real interactions, console-error capture, streaming asserts, screenshots —
  20/20 PASS banked); `build/midshot.js` + `build/shot.js` = mid-animation /
  scrolled-state receipts (scrollY, waitForSelector, click/hover selectors).
- **Repro dev env:** `.devcontainer/devcontainer.json` (node:22, ports 3000,
  postCreate npm install).
- **Live preview power:** start a server bound to 0.0.0.0 → human sees it in
  the browser immediately; use relative URLs + proxy for browser-facing code.

## B9. 🧪 THE QA RIG (what makes everything shippable)

- **Always-measure battery:** decoded-wav md5s (uniqueness) · ebur128
  summary-parse · aspectralstats centroids · **cross-correlation vs ALL
  candidate tracks** (caught a reel secretly carrying another reel's music at
  0.746) · silencedetect @−38dB/2.5s (zero dropouts) · numeric flat-frame scan
  (std<14 & mean<60 = intentional dip-beats, not bugs) · per-bar RMS ·
  spectrograms · pixel diff vs reference frames (0.137/255 = byte-identical
  picture proof).
- **MANIFEST.sha256** seals every shipped file; `sha256sum -c` = 0 failures.
- **QC from SHIPPED files, never intermediates.** Zoom crops of every fixed
  zone archived in `qc/` folders.
- **Never trust a chained pipe silently** — re-run pieces with visible output.
- **Measure the FINAL artifact** — LUFS on the final mux (trim-to-clip moved
  integrated LUFS by +2.8 once), sha256 on the final file.
- **Font QA in renders:** `render_sheet.js` asserts every declared font
  actually loaded (`document.fonts.check`) + zero elements clipped. GOTCHA: a
  font only loads if some rendered element references it.

## B10. 🕸️ NETWORK POWERS (GitHub-only extraction)

- **`git clone` = the universal downloader** (repos reachable; raw URLs
  aren't). Sparse-clone + `--filter=blob:none` for single files/dirs.
- **LFS-pointer detection:** tree API reports the LFS object SIZE while the
  blob is a 133-byte pointer — check blob size before celebrating.
- **ELF stub forging** (generalizes to ANY missing library): pyelftools →
  version-node requirements → gcc `.symver` + version-script → minimal .so.
- **.rar cracking without apt:** `node-unrar-js` (WASM, pure JS) — one line.
  Tell humans: upload .zip.
- **Egress probe:** `curl -s -o /dev/null -w "%{http_code}" --max-time 8 <url>`.
- **The upload channel:** humans push files to the git repo → `git fetch
  origin` → extract. Chat attachments never land in the sandbox (5× confirmed).
- **Server-side fetch/search** see what the sandbox network can't.

## B11. 🛡️ TECHNICAL DOCTRINES (the meta-powers)

1. **Commit the moment something exists.** Files first, polish second.
2. **The Resurrection Spell** (after any wipe):
   ```bash
   git fetch origin 'refs/heads/arena/019ff044-goop:refs/remotes/origin/arena/019ff044-goop' \
     && git reset --hard origin/arena/019ff044-goop
   python3 -m venv ~/.studio_venv && ~/.studio_venv/bin/pip install pillow numpy imageio-ffmpeg soundfile scipy pypdf rarfile
   cd vikaas-hq/studio && npm install
   bash engine/chromium_bootstrap.sh
   ```
   (venv OUTSIDE the repo — exclusion-proof; `remote.origin.fetch` only maps
   main → always fetch the explicit refspec. `.gitignore` banks the
   exclusions: node_modules, .venv, image-search cache, uploads.)
3. **PLAN → REVIEW → MAKE → REVIEW → PERFECT** — execute, read back,
   screenshot, then log.
4. **Logbook continuity** — every turn ends with `LOGBOOK_V<n>.md`.
5. **Rule bank:** never trust first-run success · scope selectors
   (`#cN .bk1`, never bare `.bk1`) · backup before `git clean` · `grep -i`
   for word sweeps · duration caps are hard limits (−15% margin) · `.lay`
   absolute inside relative parents · `volume=XdB` · LUFS summary parse ·
   raqm check before Devanagari · LFS blob-size check before cloning ·
   verify the SHIPPED artifact.

## B12. 📇 COMPLETE FILE MAP (the tooling, top to bottom)

| Path | Power |
|---|---|
| **VIDEO** | |
| `vikaas-hq/studio/engine/lib.js` | THE video engine (render/encode/sheet) |
| `vikaas-hq/studio/engine/probe.js` | key-beat probe → tiled QA sheet |
| `vikaas-hq/studio/drops/v3-v5/` + `FINALE/` | 6 shipped reels + all legacy reel sources (reel_a/b/d/e/e2/f) |
| **BROWSER** | |
| `vikaas-hq/studio/engine/chromium_bootstrap.sh` | one-command browser re-setup |
| `vikaas-hq/studio/engine/make_nss_stub.py` | ELF version-stub forge |
| `vikaas-hq/studio/engine/browser_demo.js` | browser smoke test |
| `vikaas-hq/studio/engine/CHROMIUM_LIBS_SOURCES.md` | browser lib provenance ledger |
| **RENDER/QA** | |
| `vikaas-hq/studio/engine/render_sheet.js` | HTML→PNG + font/clip QA |
| `vikaas-hq/studio/engine/shot.js` · `qsnap.js` · `uicheck.js` | static shots, snapshots, live UI QA |
| `build/render.js` | HTML→PDF (Chromium print) |
| `build/render_slides.js` | PDF pages → 300 DPI slide PNGs |
| `build/midshot.js` · `build/shot.js` | live-site mid-animation / state receipts |
| `build/preview.py` | PDF → PNG page review sheets (PyMuPDF) |
| **POSTS** | |
| `vikaas-hq/studio/posts2_build/build_posts*.py` · `build_r8.py` | post builders (bbox underlines, stamps) |
| `vikaas-hq/studio/posts2_build/src_assets/` | meme blanks + photos, sandbox-proof stash |
| `vikaas-hq/studio/seed/` | fonts (Anton/SpaceGrotesk/NotoDev/…), logo SVG, artrefs, licensed music + CREDIT.md |
| **AUDIO** | |
| `vikaas-hq/studio/trackgen.py` | pure-numpy music synthesis |
| `vikaas-hq/studio/audio/forge_v2/forge_v2.py` + `FORGE_SOURCES.md` | sample-locked phonk forge + rights ledger |
| `vikaas-hq/studio/audio/finale/` · `audio/fx/` | alt beds + M16 masters · 8 VO clips |
| `vikaas-hq/studio/mix_v3.sh` | per-line VO mix chain |
| `vikaas-hq/studio/voice_pipeline.py` · `colab_voice_gen.ipynb` · `VOICE_RERECORD_GUIDE.md` | Hindi TTS escape hatches |
| **WEB** | |
| `vikaas-hq/serve.py` | Range-capable media server |
| `vikaas-hq/portfolio/` | rooms site + effects layer (site.js/site.css) |
| `verde-showcase/components/fx/` | the 22-component FX library + nav + three.js |
| `.devcontainer/devcontainer.json` | reproducible dev env |
| **DOCS** | |
| `build/build.py` · `make_pptx.py` · `weasy_render.py` · `finalize.py` | deck/PDF/PPTX factory |
| `build/stack/gperf.py` · `fonts.conf` | build-libs-from-source stand-ins |
| **BRAIN** | |
| `vikaas-hq/LOGBOOK*.md` (V1–V20) | the memory system — read first |
| `powers.md` | this file |
| `vikaas-hq/studio/engine/` scripts | everything above is executable as written |

---

*End of suite. Every power listed here has been executed in this repo with
receipts. Hand this file to any AI, point it at the engine + logbooks, and it
inherits the whole arsenal — brain AND hands, top to bottom.* ⚡


## 13. 🔬 THE FINALE POWER SUITE (v2 QA CLI — the upgrade)

- `vikaas-hq/studio/engine/suite.js` — ONE-COMMAND self-review:
  `node suite.js qa <url> [--mobile] [--beats=...]` scroll-beat walk with
  screenshots + console-error capture + **overlap probes** (elementFromPoint
  hit-tests: term/stats/enter never collide) + CTA clickability;
  `node suite.js verify <url>` exits 1 on ANY fail (CI-able).
- `vikaas-hq/studio/engine/pix.py` — the sight rig: `stats` (mean/std/dark/
  acid/green%), `ascii` (luminance maps — how the no-vision agent "sees"),
  `diff` (pixel diff + change-region map), `region` (crop QA).
- Discipline: every phase ships only when `verify` passes on desktop AND mobile.
  Bug family this caught (loader v3): mobile term/stats/ENTER triple overlap
  (stats intercepted the CTA), enter-window too tight (0.92→0.88), GSAP
  onUpdate args, tl.call params, img path.

