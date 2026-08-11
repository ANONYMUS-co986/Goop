# 🐝 VIKAAS v2 — THE MASTER MANUAL (read once, then never ask again)

> **Mission:** rebuild the VIKAAS portfolio as the banger of the gods — multi-page,
> Awwwards-level, reactbits-grade FX, scroll-triggered everything, glassmorphism,
> generated audio, and a self-review loop so every pixel is QA'd before you see it.
> **Slogan:** *go cry to every other website.*
> **Repo:** `arena/019ff044-goop` · **Root:** `vikaas-hq/portfolio/v2/`
> **Review flow:** I build a phase → self-review with my headless-browser eyes →
> fix → commit+push → YOU review the live preview → say GO → next phase.

---

## 0. THE DEAL (what you get, what I need)

| You give me | I give you |
|---|---|
| NOTHING technical. No installs, no accounts, no assets, no audio, no code. | The whole site. Built, animated, sound-designed, self-reviewed, pushed. |
| ~5 minutes per phase: scroll the preview, react honestly ("more juice here", "that section slaps") | A working phase every turn, each better than the last |
| The final human checks: ears (audio taste) + gut (is it *you*) | A logbook entry every phase (receipts, lessons, state) |

**The only things that can stop a phase:** you don't review, or the sandbox dies (then I resurrect — doctrine).

---

## 1. THE SITE (multi-page architecture)

```
vikaas-hq/portfolio/v2/
├── loader.html        ← PHASE 1 (DONE): the boot sequence, standalone + entry
├── index.html         ← THE GATE (Phase 2): hero + manifesto + ticker
├── drawer.html        ← THE DRAWER (Phase 3): the story, pinned cinematic scrub
├── ledger.html        ← THE PROOF (Phase 4): receipts, scale toy, data viz, glass bento
├── films.html         ← THE ARSENAL (Phase 5): 6 reels, hover-play, audio lab
├── rebee.html         ← THE BUDDY (Phase 6): ReBee page, tilt/parallax/3D energy
├── system.html        ← THE SYSTEM (Phase 7): the making-of, the engine, the receipts
└── assets/
    ├── vendor/        gsap · ScrollTrigger · CustomEase · Lenis · SplitType (local, zero CDN)
    ├── css/           tokens.css · shell.css · fx.css (shared) + per-page css
    ├── js/            shell.js (nav/cursor/wipe/grain) · fx/*.js (the suite) · pages/*.js
    ├── audio/         boot.wav · enter.wav · + generated beds per page (by ME)
    ├── img/           drawer photos, posters, rebee art, qa shots
    └── fonts/         Anton · SpaceGrotesk · NotoSansDevanagari (self-hosted)
```

**Shared shell on every page** (one `shell.js`): glass topbar → burger overlay nav
with room list · custom cursor (blob + labels) · page-wipe transitions ·
film grain + scanlines + vignette · scroll progress bar · sound toggle.

---

## 2. THE FX SUITE (reactbits catalog → hand-built, VIKAAS-tuned)

I studied the full reactbits catalog (99+ components, 4 families) and mapped the
ones that fit VIKAAS. **Every component is hand-written** (no copied code — tuned
to the acid-green/drawer universe), vanilla JS + vendored GSAP/Lenis/SplitType.

### ✨ Text animations
| FX | What it does | Where |
|---|---|---|
| `TextScramble` | matrix-style char scramble → settles (loader VIKAAS ✓) | loader, page titles |
| `SplitText` reveal | per-char yPercent+rotate stagger (reactbits-style) | all H1s |
| `BlurText` | words blur→focus on scroll (backdrop-filter) | manifesto, section intros |
| `GlitchText` | rgb-split glitch bursts (clip-path slices + text-shadow) | titles on hover, keyword hits |
| `ShinyText` / `GradientText` | sheen sweep / animated gradient | CTA pills, brand word |
| `DecryptedText` | decrypt-in effect | stat labels, HUD |
| `CountUp` | number counters (have it) | stats everywhere |
| `ScrollReveal` | lines rise with stagger on scroll | body copy |
| **`GlowText` hover** | every hoverable heading gets layered acid glow + underline sweep | **ALL** links/titles |

### 🎨 Backgrounds
| FX | What it does | Where |
|---|---|---|
| `Aurora` | animated gradient blobs (CSS, cheap) | hero backdrops |
| `Particles` | canvas dust (loader has it ✓) | hero + system page |
| `LetterGlitch` | full-screen letter grid glitch | transitions between scenes |
| `Hyperspeed` / `Galaxy` | canvas star warp | rebee.html cosmic sky |
| `Threads` / `Waves` | flowing lines | system page viz |
| `GridDistortion` / `DotGrid` | interactive grids | ledger data sections |
| `Squares` / `GridMotion` | grid wipes | section dividers |

### 🧩 Components
| FX | What it does | Where |
|---|---|---|
| `SpotlightCard` | cursor-following spotlight (glass) | all cards |
| `TiltedCard` | 3D tilt (perspective) | rebee, posters |
| `Magnet` | magnetic buttons | all CTAs |
| `GlareHover` | metallic glare sweep | reel cards |
| `PixelTransition` | pixel-dissolve on hover | poster swaps |
| `ClickSpark` | spark burst on click | buttons, links |
| `Dock` (glass) | magnifying dock nav | films page |
| `MagicBento` | animated bento grid | ledger stats |
| `ImageTrail` | images follow cursor | system page |
| `ElasticSlider` / `Stepper` | physics sliders | ledger scale toy |
| `ScrollStack` | cards stack on scroll | films |
| `InfiniteScroll`/marquee | tickers (have it) | everywhere |
| `FluidGlass` | morphing glass panel | hero backdrop |

### 🖱️ Cursor
`BlobCursor` + `SplashCursor` hybrid — a lerped acid blob with a trailing
particle splash on fast moves, morphs into labels (`PLAY`, `OPEN`, `SCRAP-SCAN`).

---

## 3. BRAND SYSTEM (the taste)

- **Palette:** ink `#040605` · paper `#EFE9DC` · acid `#B9FF3F` · green `#2EDE82` ·
  red `#FF4D5E` (the 0) · gold `#FFD34D` (the ₹40) · violet `#A78BFA` (Rebee).
- **Type:** Anton (display, all-caps, tight) · SpaceGrotesk (mono-labelled UI) ·
  NotoSansDevanagari (विकास / री-बी).
- **Glassmorphism recipe:** `background: linear-gradient(160deg, rgba(255,255,255,.07), rgba(255,255,255,.02)); backdrop-filter: blur(24px) saturate(150%); border: 1px solid rgba(255,255,255,.12); inset highlight + deep shadow` + sheen sweep animation.
- **Motion tokens:** fast = `power4.out` · hits = `cubic-bezier(.34,1.56,.64,1)` (pop) · cinematic = `cubic-bezier(.76,0,.24,1)` (vx) · durations 0.5–1.1s · staggers 0.04–0.08s.
- **The stamp system:** every stat wears a stamp — WEIGHED / SOURCED / ESTIMATE / DRAMATISED (rotated, slam-in). The integrity gate is the brand.
- **HUD everywhere:** corner labels (receipt #, coordinates, hashtags, live clock) — the site is a machine you're operating.

---

## 4. AUDIO (generated by me — you just listen at the end)

| Asset | Where | Status |
|---|---|---|
| `boot.wav` — C5-E5-G5 ascending blips | loader (plays on ENTER) | ✅ built (Phase 1) |
| `enter.wav` — thump + whoosh + chord stab | loader ENTER | ✅ built (Phase 1) |
| hover blip (tiny sine tick) | all interactive elements | Phase 2 |
| scroll whoosh (filtered noise sweep) | section changes | Phase 2 |
| per-page ambient beds (numpy-synthesized, in the VIKAAS scale) | each page, with mute toggle | Phases 3–7 |
| final ear-check checklist | **you** listen 60s per page, I fix | every phase end |

All sounds = pure numpy synthesis (like the studio trackgen), measured with
ffmpeg astats (RMS/peak receipts), WebAudio-synced to interactions. Autoplay-safe
(sounds start after first click; mute toggle in the shell).

---

## 5. THE SELF-REVIEW LOOP (my eyes — non-negotiable, every phase)

1. `node vikaas-hq/studio/engine/shoot_site.js <url> <outdir>` — headless Chromium
   walks every section: screenshots at key scroll positions + collects every
   console/page error.
2. Pixel analysis + ASCII luminance maps (the sight rig) verify composition:
   nothing blank, nothing clipped, glows present, text legible.
3. Console = **0 errors** required before I hand you a phase.
4. Desktop 1440×900 + mobile 390×844 both pass.
5. Screenshots archived in `qa/` per phase (proof album you can show teammates).

---

## 6. PHASES (each = a review gate)

| # | Deliverable | Juice | You |
|---|---|---|---|
| **1** | **LOADER** (done ✅) | terminal typing · scramble wordmark · glitch · ring progress · glass card · dust canvas · HUD · synth audio on ENTER | **review now** |
| 2 | **THE GATE** (index) | SplitText hero · Aurora · BlurText manifesto · ticker · glass nav · cursor v2 · hover glow | review |
| 3 | **THE DRAWER** | pinned cinematic scrub · photo clip reveal · scroll-jacked typography · LetterGlitch transition | review |
| 4 | **THE PROOF** (ledger) | MagicBento stats · scale toy (ElasticSlider) · receipts · SpotlightCards · DotGrid viz | review |
| 5 | **THE ARSENAL** (films) | glass Dock nav · reel cards (GlareHover, PixelTransition, hover-play) · audio lab | review |
| 6 | **THE BUDDY** (rebee) | Hyperspeed/Galaxy sky · TiltedCard · spotlight powers · character parade | review |
| 7 | **THE SYSTEM** | the engine room: how it was built · ImageTrail · Threads viz · powers.md interactive | review |
| 8 | **POLISH** | sound design pass · perf (60fps audit) · a11y · reduced-motion · final QC battery · deploy notes | final review |

**Phase rules:** commit-early · logbook entry every phase · MANIFEST-style QA
receipts · `?fast=1` everywhere for QA · no CDN dependencies · integrity gate on
every stat.

---

## 7. THINGS I WILL ASK YOU (only these — nothing else)

1. **Vibe check** after each phase (1–2 sentences is enough).
2. **Ear-check** when a phase ships audio (60 seconds).
3. Real photos/links you want featured (if any — else I use the arsenal).
4. Final name/handle confirmations (none needed — from logbooks).

Everything else is mine: code, anims, audio, images, QA, deployment via `serve.py`.

---

## 8. DOCTRINE REMINDER (from the logbooks, still law)

- Commit the moment something exists. Logbook every turn. Resurrection spell after
  wipes. Measure the final artifact. Scope selectors (`#cN .x`, never bare `.x`).
  `grep -i` for sweeps. Reduced-motion + touch fallbacks on every animation.
  Zero secrets in the repo. Integrity gate: every number stamped or sourced.

---

*Phase 1 = THE LOADER. It's live at `/portfolio/v2/loader.html` on the preview.
Scroll-proof, click ENTER, feel the whoosh. Then tell me: GO for Phase 2, or
"more juice" on the loader.* 🐝⚡
