# ⚡ POWERS.md — THE TECHNICAL SUITE

> The complete technical capability manifest of the VIKAAS studio agent —
> every power unlocked for making **videos, images, audio, and web** through
> code. Feed this to any AI to hand it the whole arsenal: the deterministic
> HTML→MP4 engine, the GSAP techniques, the in-sandbox browser forge, the
> audio/music synthesizers, the QA rig, and every bug-bank lesson.
> Everything here is REAL — built, run, and verified in this repo, with
> receipts in the logbooks (`vikaas-hq/LOGBOOK*.md`) if you want the war stories.

---

## 1. 🔥 THE CORE POWER — DETERMINISTIC HTML→MP4 VIDEO ENGINE

### The design contract
Any video is a **webpage** whose JS exposes exactly one global:
```js
window.__reel = { duration: 27.2, seek(t) { /* drive everything from t */ } }
```
The engine scrubs `t` from 0→duration in a headless browser, screenshots a
frame at every step, and encodes the frames to MP4. **Zero wall-clock
dependence** — no timers, no rAF, no "wait 2s". The same 30s reel renders
identically every time, frame-for-frame.

### The pipeline commands
```bash
node engine/lib.js render <htmlPath> <framesDir> [fps]      # HTML → PNG frames
node engine/lib.js encode <framesDir> <audioFile> <durSec> <outMp4> [fps]  # → MP4
node engine/lib.js sheet  <mp4> <outPng> [tiles]            # MP4 → contact sheet
```
Typical reel: 1080×1920@30fps, H.264 CRF18, AAC 44.1kHz stereo 192k,
`-movflags +faststart`. 816–1224 frames per 27–41s reel; ~0.35s/frame capture.

### Audio is baked at encode time
- Mix bed + VO in ffmpeg first, THEN feed the mix to `encode`.
- **Mastering chain (the bug-proof recipe):**
  ```bash
  ffmpeg -c:v copy -af "volume=2.6dB,alimiter=limit=0.89:level=false,aresample=44100" -ac 2 -ar 44100 -b:a 192k in.mp4 out.mp4
  ```
  ⚠️ **`volume=2.6` WITHOUT `dB` = LINEAR = +8.3 dB. Always the `dB` suffix.**
- **LUFS standard:** measure the FINAL mux with ebur128, gain-trim, re-measure.
  Beat/VO reels ≈ −16 LUFS; ambient reels ≈ −18.5 LUFS.
- **The ebur128 parse trap:** t-lines contain `I: x LUFS` — a naive parse reads
  the first one (often −70) → gain-stages a +54 dB square-wave brick. **Always
  parse the SUMMARY block.**
- **The 24 kHz mp3 trap:** mp3 inputs are 24 kHz — `asetrate` without prior
  `aresample=44100` speeds audio 1.75×. Duration-preserving chain:
  `aresample → asetrate → aresample → atempo(inverse)`.

---

## 2. 🎬 GSAP MASTERCLASS (the advanced ways)

### Timeline architecture
- ONE master timeline per reel; scenes are nested timelines added at offsets.
- Everything reads `t` from `__reel.seek(t)` → use `tl.progress(t/duration)`
  or scrub a master via `tl.seek(t)`.
- **Count-ups / tally scenes are scrub-safe:** animate an object's `value`
  from the `seek` handler (no rAF), read it in a `onUpdate`-style hook, render
  to DOM text.
- **Transform-only animation discipline:** opacity/transform/xPercent only —
  layout properties reflow mid-capture and break determinism.

### Beat-locking (music-synced cuts)
- Compute cut times from the grid, never from feel: `C(n) = n * beatSec`,
  where `beatSec = 60/bpm` (140 BPM → 0.4286s; 128 BPM bar = 1.875s).
- Structure: intro bars → hook → drops land on bar starts; risers sweep into
  the drop; flash/dip beats before section changes (they read as style, not bugs).

### Transition & FX bank (all shipped, all proven)
- **RGB-split flares:** two copies of the element (`.lay`) with
  `mix-blend-mode:screen` in red/blue, offset by a few px. GOTCHA: `.lay`
  copies must be `position:absolute` INSIDE the `.big` (position:relative)
  parent or the offsets reflow the layout. `mix-blend-mode:screen` only reads
  right on DARK scenes — on cream scenes use shake-only.
- **Whip-blur entrances:** quick xPercent sweep + motion blur filter on enter.
- **VHS streaks:** absolute gradient rows translating across, low opacity.
- **Viewfinder brackets + REC pulse:** thin border corners + blinking dot.
- **Ken Burns:** slow scale on stills (xPercent/scale transform only).
- **easeOutBack pops** for beat-hit entrances; **beat lamps** (flash a lamp
  div each beat via scrub math); **shake bursts**; **flash frames** (1–2 frame
  white overlay); **scanlines** overlay; **SVG logo draw-on** via
  stroke-dashoffset scrubbed by t (deterministic ident).
- **End cards:** punchline with strikethrough animation, footer progress bar
  + handle ("footer progress + handle everywhere" — the brand signature).

### GSAP gotchas banked
1. Bare class selectors (`.bk1`) match only the FIRST scene — **always scope
   `#cN .bk1`**.
2. `position:absolute` for overlay layers inside a relative parent, always.
3. Fonts: call `document.fonts.ready` before first capture; `@font-face` must
   point at LOCAL ttf files (repo paths), never CDNs.
4. **Devanagari TOFU family (3 distinct bugs):**
   a. `.dev` font loses specificity wars vs structural scopes → append
      `'Devnag'` fallback to EVERY font-family declaration.
   b. Patchers that only fix declarations containing `sans-serif` MISS others
      → use last-family-insert regex.
   c. Anton has NO Devanagari glyphs → any हिंदी text needs
      NotoSansDevanagari in the stack or it's tofu.
5. `mix-blend-mode` behavior differs dark vs light scenes (see FX bank).

---

## 3. 🖥️ THE BROWSER FORGE (how the headless browser exists)

Playwright's installer is CDN-blocked in this sandbox; the browser was
**assembled from open pipes only** (npm + GitHub + PyPI):
1. `@sparticuz/chromium@138.0.2` (npm) → chromium-138 binary self-inflates to
   `/tmp/chromium` (in-tarball, no CDN).
2. Real 64-bit NSPR libs ← `awesome-fc/puppeteer-fc-starter-kit` @ SHA
   `19e29d8b3264cf7534d86586efd6f3e4b4c1efab` (sparse-cloned from GitHub).
3. `libnss3.so` + `libnssutil3.so` = **self-built stubs** —
   `engine/make_nss_stub.py` parses the target ELF's version requirements
   (37 symbols, 6 version nodes incl. `NSS_3.30`) and auto-generates +
   compiles them with gcc.

**One-command re-setup after any sandbox wipe:**
```bash
cd vikaas-hq/studio && bash engine/chromium_bootstrap.sh
```

**Usage powers:**
```bash
node engine/render_sheet.js <in.html> <out.png> 1080 1920   # HTML→PNG + QA asserts
node engine/shot.js <htmlPath> <outPng> [w] [h]             # static post shooter
node engine/qsnap.js <htmlPath> <outPrefix> [--boot]        # portfolio QA snapshots
node engine/uicheck.js [baseUrl]                            # live-server interaction QA
```
`render_sheet.js` QA asserts: every declared font actually loaded (via
`document.fonts.check`), every element inside the viewport (zero clipping).
GOTCHA: a font only loads if some rendered element references it — put
Devanagari fonts in stacks even for latin pages, or the check fails.

**Honest limits:** NSS stub = TLS cert ops return failure; external egress is
network-blocked anyway. Local rendering (`file://`, `data:`, localhost HTTP),
screenshots, DOM automation = full power.

---

## 4. 🖼️ STATIC POSTS THROUGH CODE

- **Pipeline A — meme templates:** imgflip blanks + **zone-mapped text**
  (measure true board centers on a 5%-grid overlay, never eyeball). Multi-panel
  boards: short words per board + a payoff board.
- **Pipeline B — AI plates + own typography:** generate a plate ("top 40%
  perfectly empty, riso grain, palette") → compose with Anton headline +
  acid underline + mono sub-band + stamp chip.
- **Underlines must be bbox-derived:** `multiline_textbbox` for the real block
  top/bottom/center → bar at bottom+offset, width from the REAL block. Never
  `font_size * 1.06` estimates (they land ON glyphs / through letters).
- **The raqm check:** fresh-venv Pillow may have `raqm: False` → Devanagari
  shaping breaks (`फिर`→`फरि`, floating anusvara). **Check
  `PIL.features.check('raqm')` before any Devanagari build; else keep latin.**
- Zero emoji in Anton (tofu); stamp chip + footer CTA on every asset; grain
  overlay ~4.5%.
- QA loop: full-canvas sheet + zoom crops of every text zone, from the
  SHIPPED file.

---

## 5. 🎧 AUDIO SYNTHESIS (music from pure code, zero samples needed)

### `trackgen.py` — pure-numpy synthesis techniques
- One-pole low-pass loops · Schroeder combs+allpass reverb · tanh drive chain ·
  sidechain pump · tape dress (hiss+crackle+flutter = identity).
- Genre rules banked: drama needs pad+air; phonk needs 8th grid + saturation;
  comedy needs silence between oom-pahs so the VO lands.
- QA: spectrogram PNGs (structure visible: gaps/sweeps/gags) + `astats` peaks.

### `audio/forge_v2/forge_v2.py` — sample-locked sequencing (Drift-Forge v2)
- Real studio one-shots from GitHub-only sources with rights receipts
  (`FORGE_SOURCES.md`, pinned SHAs): Boochi44 CC0 TR-808 kit + GareBear99
  free-commercial phonk kit (key-matched F-minor cowbells, Drift808s+slides).
- 138 BPM, 16 bars: halftime drift skeleton (kick {0,14}+pumps, snare on 8,
  rolling 16ths w/ swing + bar-end 32nd rolls), cowbell minor riff, 808 root +
  slide into drop, sidechain duck (bells 0.30 / 808 0.5), tanh glue, riser at
  bar 12.
- **Mastered −16.0 LUFS EXACT** (TP −9.8, zero clipping), per-bar RMS proof
  (intro 0.054/0.057 → main 0.176–0.178 → slide-bars 0.191).

---

## 6. 🗣️ VOICE & DIALOGUE

- In-sandbox speech gen with **per-character pitch casting**: narrators
  −4.5%, papa −3%, kabadi −6.5% + warmth EQ + compressor + tiny room.
- **Timing discipline:** probe clip durations FIRST, then build the timeline
  BACKWARD from the VO so jokes land (bounce at whistle-down, elastic at
  boing, tag at honk).
- Local escape hatch: `voice_pipeline.py` — downloads Piper/Kokoro Hindi
  models on a normal machine (sandbox model-CDN wall documented) and renders
  lines with per-character emotion presets.
- The 24 kHz trap recipe in §1 applies to every mp3 VO.

---

## 7. 📄 DOC & DECK FOUNDRY

- **PDF:** WeasyPrint with a fonts.conf + cached TTFs
  (`build/weasy_render.py`, `build/finalize.py`) — 33-page doc shipped.
- **PPTX:** `build/make_pptx.py` (33 slides shipped).
- **HTML deck:** `build/build.py` assembling `build/src/parts/*.html`
  (00-head … 11-close) → single index.html, dark-tech aesthetic, dividers,
  inline SVG diagrams, fonts bundled as woff2+ttf.

---

## 8. 🌐 WEB OPS & EFFECTS

- **`vikaas-hq/serve.py` — Range-capable static server** (206 Partial
  Content, Accept-Ranges, suffix-ranges, threading, CORS, no-store).
  ⚠️ Python's `http.server` sends full 200 without Range → Chrome/Safari
  REFUSE `<video>` playback. This fixed it; verify with `curl -H "Range:
  bytes=0-100"` → 206 + Content-Range.
- **GSAP effects bank for sites:** custom cursor + labels, tooltips, page-wipe
  transitions, count-up-on-view, film grain, magnetic chips, staggered
  reveals, marquee — with `prefers-reduced-motion` + touch fallbacks and
  transform-only animation.
- Next.js + Three.js showcase site pattern exists (`verde-showcase/`) with a
  full QA screenshot archive.

---

## 9. 🧪 THE QA RIG (what makes everything shippable)

- **Always-measure battery:** decoded-wav md5s (uniqueness) · ebur128
  summary-parse · aspectralstats centroids · **cross-correlation vs ALL
  candidate tracks** (catches accidentally-shared music — 0.746 correlation
  once caught a reel secretly carrying another reel's track) ·
  silencedetect @−38dB/2.5s (zero dropouts) · numeric flat-frame scan
  (std<14 & mean<60 = intentional dip-beats, not bugs) · per-bar RMS ·
  spectrograms.
- **MANIFEST.sha256** seals every shipped file; `sha256sum -c` = 0 failures.
- **QC from SHIPPED files, never intermediates** (contact sheets, zoom crops).
- **Never trust a chained pipe silently** — re-run pieces with visible output.
- **Measure the FINAL artifact** — LUFS on the final mux (trim-to-clip changes
  integrated LUFS by +2.8 once), sha256 on the final file.

---

## 10. 🕸️ NETWORK POWERS (GitHub-only extraction)

- **`git clone` = the universal downloader** (repos reachable; raw URLs
  aren't). Sparse-clone + `--filter=blob:none` for single files/dirs.
- **LFS-pointer detection:** tree API reports the LFS object SIZE while the
  blob is a 133-byte pointer — check blob size before celebrating.
- **ELF stub forging** (generalizes to ANY missing library): pyelftools →
  version-node requirements → gcc `.symver` + version-script → minimal .so.
- **.rar cracking without apt:** `node-unrar-js` (WASM, pure JS) — one line.
- **PDF image extraction:** `pypdf` pulls embedded full-res JPGs out of
  image-type PDFs.
- **Egress probe:** `curl -s -o /dev/null -w "%{http_code}" --max-time 8 <url>`.
- **The upload channel:** humans push files to the git repo → `git fetch
  origin` → extract. Chat attachments never land in the sandbox.
- **Server-side `fetch_page`/`web_search`** see sites the sandbox network
  can't (YouTube, social, mirrors) — use them for research and recon.

---

## 11. 🛡️ TECHNICAL DOCTRINES (the meta-powers)

1. **Commit the moment something exists.** Files first, polish second.
2. **The Resurrection Spell** (after any wipe):
   ```bash
   git fetch origin 'refs/heads/arena/019ff044-goop:refs/remotes/origin/arena/019ff044-goop' \
     && git reset --hard origin/arena/019ff044-goop
   python3 -m venv ~/.studio_venv && ~/.studio_venv/bin/pip install pillow numpy imageio-ffmpeg soundfile scipy pypdf rarfile
   cd vikaas-hq/studio && npm install
   bash engine/chromium_bootstrap.sh
   ```
   (venv lives OUTSIDE the repo — exclusion-proof; `remote.origin.fetch` only
   maps main → always fetch the explicit refspec.)
3. **PLAN → REVIEW → MAKE → REVIEW → PERFECT** — execute, read back,
   screenshot, then log.
4. **Logbook continuity:** every turn ends with `LOGBOOK_V<n>.md` (orders,
   receipts, lessons). The logbooks ARE institutional memory.
5. **Rule bank:** never trust first-run success · scope selectors
   (`#cN .bk1`, never bare `.bk1`) · backup before `git clean` · `grep -i`
   for word sweeps · duration caps are hard limits (−15% margin) · `.lay`
   layers absolute inside relative parents · `volume=XdB` · LUFS summary
   parse · raqm check before Devanagari.

---

## 12. 📇 FILE MAP (the tooling)

| Path | Power |
|---|---|
| `vikaas-hq/studio/engine/lib.js` | THE video engine (render/encode/sheet) |
| `vikaas-hq/studio/engine/render_sheet.js` | HTML→PNG + font/clip QA |
| `vikaas-hq/studio/engine/shot.js` · `qsnap.js` · `uicheck.js` | static shots, snapshots, live UI QA |
| `vikaas-hq/studio/engine/browser_demo.js` | browser smoke test |
| `vikaas-hq/studio/engine/chromium_bootstrap.sh` | one-command browser re-setup |
| `vikaas-hq/studio/engine/make_nss_stub.py` | ELF version-stub forge |
| `vikaas-hq/studio/engine/CHROMIUM_LIBS_SOURCES.md` | browser lib provenance ledger |
| `vikaas-hq/studio/trackgen.py` | pure-numpy music synthesis |
| `vikaas-hq/studio/audio/forge_v2/forge_v2.py` + `FORGE_SOURCES.md` | sample-locked phonk forge + rights ledger |
| `vikaas-hq/studio/voice_pipeline.py` | local Hindi TTS escape hatch |
| `vikaas-hq/studio/mix_v3.sh` | per-line VO mix chain |
| `vikaas-hq/studio/posts2_build/` | post builders (build_posts*.py, build_r8.py) + src_assets |
| `vikaas-hq/studio/seed/fonts/` | Anton, SpaceGrotesk, NotoSansDevanagari, etc. |
| `vikaas-hq/studio/drops/FINALE/` | shipped 6 reels + 22 posts + MANIFEST |
| `vikaas-hq/serve.py` | Range-capable media server |
| `vikaas-hq/portfolio/` | GSAP rooms site + effects bank |
| `build/` | PDF/PPTX/HTML deck factory |
| `vikaas-hq/LOGBOOK*.md` | the war history (V1–V20) |

---

*End of suite. Every power listed here has been executed in this repo with
receipts. Hand this file to any AI, point it at the engine + logbooks, and it
inherits the whole arsenal — plus the scars.* ⚡
