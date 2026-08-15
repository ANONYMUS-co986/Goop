# 🏛️ VIKAAS UNIVERSE v3 — THE MASTER PLAN (FINAL, 12 Aug 2026)

> **This is the plan.** Locked after web-research on what actually wins awards.
> Every phase = a review gate. The user reviews → GO → next phase. No scope drift.
> The loader idea (auto-boot → scroll universe) is KEPT — it was the one thing
> the user loves. Everything else gets rebuilt to this spec.

---

## 0. THE RESEARCH (why this plan wins)

From Awwwards/FWA/CSSDA breakdowns (utsubo, hontran.dev, made-with-gsap):

| Criterion | Weight | What we do about it |
|---|---|---|
| **Design** | 40% | Strong single art direction: ink/acid/green universe, Anton display, glassmorphism, nebula depth, stamp system. Static frames must look like posters (Obys benchmark). |
| **Usability** | 30% | Every page: clear hierarchy, 3–4 screens max, working nav, no broken links, mobile + reduced-motion perfect. This is where I've been LOSING — now enforced by the QA gate. |
| **Creativity** | 20% | Custom interaction patterns: the drawer toy, the boot sequence, the scale, the scrap-scan demo. 3D + WebGL (Three.js). GSAP choreography with intent. |
| **Content** | 10% | Real receipts: 1.4 KG weighed, ₹40, 15 HSPCB recyclers, 0 doorsteps, 6 reels, 22 posts, ReBee. Truth beats hype (vs NIRMAN's fake blockchain). |

**The stack that wins:** Three.js/WebGL + GSAP ScrollTrigger + custom interactions +
fast framework (Vite+React ✓) + **60fps on a mid-range phone** (the performance
discipline is a judge criterion — this kills the "erroring/blanking" reputation).

**The benchmark names to beat:** Hubtown (3D monolith), Cartier Watches &
Wonders (six rooms), Sleep Well (scroll storytelling), Uncommon (GSAP camera
moves), By-Kin (Developer Award).

---

## 1. THE ARCHITECTURE (fixed)

```
vikaas-hq/v2-app/  (Vite + React 19 + React Router 7 + GSAP + Lenis + Three.js)
├── src/
│   ├── main.jsx            entry
│   ├── App.jsx             routes + PageWipe + Lenis
│   ├── shell/              Shell.jsx (nav/cursor/HUD/progress) + shell.css
│   ├── pages/
│   │   ├── Boot.jsx        (KEPT — the beloved loader)
│   │   ├── Gate.jsx        REBUILD (phase 2)
│   │   ├── Drawer.jsx      REBUILD (phase 3)
│   │   ├── Proof.jsx       NEW   (phase 4)
│   │   ├── Kabadi.jsx      NEW   (phase 5)
│   │   ├── Arsenal.jsx     NEW   (phase 6)
│   │   ├── Buddy.jsx       NEW   (phase 7)
│   │   ├── System.jsx      NEW   (phase 8)
│   │   └── NotFound.jsx    NEW   (phase 9)
│   ├── lib/
│   │   ├── fx/             the FX library (one file per effect)
│   │   ├── useLenis.js     smooth scroll hook
│   │   └── useReveal.js    shared scroll-reveal hook
│   └── assets/
├── public/                 fonts, audio, og-image
└── engine/ (repo-wide QA tools)
```

**Shared systems (built once, used everywhere):**
- `Shell`: glass nav + overlay (all rooms, live/locked states) · cursor v2 ·
  HUD clock/coords · scroll progress · grain/vignette · PageWipe transitions
- `lib/fx/`: TextScramble · BlurText · SplitReveal · GlitchText · ShinyText ·
  GradientText · SpotlightCard · TiltCard · Magnet · ClickSpark · PixelTransition ·
  CountUp · Aurora · Nebula · Particles · LetterGlitch · Hyperspeed · DotGrid
- Audio system: WebAudio UI blips + per-page generated ambient beds + mute toggle
- The QA gate (see §3) — non-negotiable before any phase ships

---

## 2. THE 12 PHASES (each with big implementations)

### PHASE 1 — FOUNDATION REBUILD + THE QA GATE (do first, once)
**Why:** the erroring/blanking happened because there was no enforced gate.
- Refactor app into the `shell/ + pages/ + lib/` structure above.
- **Build the QA GATE**: `engine/verify_all.sh` — one command that:
  1. compiles every route module (`curl` 200-check on each .jsx)
  2. boots the Vite server, walks every route with `suite.js` (overlap/CTA/
     console-error checks, desktop + mobile)
  3. captures a viewport screenshot per route + **blank-screen detector**
     (std < 8 → FAIL; this catches the "black page" class of bug)
  4. checks fonts load (`document.fonts.size >= 4`), checks no 404s
  5. prints a verdict table. Any FAIL = phase doesn't ship.
- Fix the browser-crash-in-probes issue (spawn one browser per route — done).
- Write `lib/fx/` skeleton with 5 core effects + tests.
- **Deliverable: a repo where `bash engine/verify_all.sh` = the definition of done.**

### PHASE 2 — THE GATE REBUILD (the home page must be PERFECT)
- Full-screen 3D hero: **a floating e-waste monolith** (Three.js — the drawer
  box + orbiting e-waste particles, mouse-parallax, scroll-reactive) instead of
  the static nebula. (Hubtown-style monolith, ours is the drawer.)
- Typography: VIKAAS with SplitType char-slam + gradient sheen sweep + hover
  glow on every interactive word.
- Marquee ticker (kept, refined) + manifesto blur-lines (kept) + room grid with
  **SpotlightCard + Tilt + Magnetic** (kept + polished).
- New: **live proof ribbon** — a thin strip that shows REAL-time-ish counters
  (1.4 KG · ₹40 · 15 · 0) with stamp pops as you scroll past.
- 3 screens max. Mobile perfect. 60fps.

### PHASE 3 — THE DRAWER REBUILD (the story room)
- Intro hero (kept) + **pinned cinematic story** (kept, polished pacing).
- **Interactive drawer toy v2**: the 3D drawer from the boot — now fully
  clickable/explorable in the browser (open → items float out → click item →
  holographic spec card + stamp). Reuse the Three.js scene from Boot.
- New: **the scale sequence** — a scroll-driven weighing animation (needle
  swings, 1.4 KG settles, receipt prints) — the "weighed, not guessed" moment.
- The 15/0 list (kept) + new: **mini-map** — a stylized Gurugram map with 15
  pulsing recycler dots and 0 doorstep markers (SVG, animated).

### PHASE 4 — THE PROOF (receipts, the ledger room)
- **Receipt printer**: paper prints line-by-line on scroll (clip-path +
  typewriter) with stamp slams (WEIGHED/SOURCED/ESTIMATE/DRAMATISED).
- **The scale toy**: interactive elastic slider (500 KG minimum vs 1.4 KG) with
  count-up and verdict gag ("SHORT BY 498.6 KG").
- **MagicBento stats grid**: 6–8 evidence cells (3 phones, 7 chargers, 10 homes,
  1.4 KG, ₹40, 0 doorsteps) with SpotlightCard + CountUp + hover expansions.
- **DotGrid data-viz**: animated dot matrix showing 3.2M tonnes / 22% with
  cursor warp (reactbits-style).
- Sources footer: HSPCB list + CWC track stats, cited.

### PHASE 5 — THE KABADI UNIVERSE (the world room)
- **Tier-list showdown**: animated tier cards (S→F) that flip in with tilt +
  glare; disputes fuel comments (callout CTA).
- **The ₹40 handshake**: looping micro-animation (cash → cables → handshake),
  scroll-scrubbed.
- **Kabadi lore cards**: 3 stories (the horn, the bicycle, the scale) with
  Flip-in + Spotlight.
- **Marquee chaos**: dual-speed opposing tickers.

### PHASE 6 — THE ARSENAL (the output room)
- **Glass Dock nav**: macOS-style magnifying dock for the 6 reels.
- **Reel cards**: poster frames (already extracted) + GlareHover + hover-play
  video + PixelTransition on hover + click → lightbox with player + caption +
  "use this sound" info.
- **The 22-post wall**: masonry grid with hover zoom + category filter chips
  (M/P/R) — animated with FLIP.
- **Audio lab**: A/B players for the phonk beds with generated waveform
  visualization (canvas) — the "we make our own music" flex.

### PHASE 7 — THE BUDDY (ReBee room)
- **Hyperspeed/Galaxy sky**: canvas star-warp background with mouse repulsion.
- **ReBee hero**: TiltedCard 3D + glare + parallax layers.
- **SCRAP-SCAN demo**: click any device (phone/charger/battery/PCB) → hologram
  scan-line sweeps over it → tag card pops (contents, ₹, nearest recycler) —
  the interactive superpower, playable.
- **Powers**: 3 SpotlightCards (SCRAP-SCAN / DOORSTEP DIAL / MATERIAL MATCH).
- Character parade: the 6 ReBee art variants in a scroll-stack.

### PHASE 8 — THE SYSTEM (the engine room)
- **The receipts of the receipts**: how the 6 reels / 22 posts were made —
  timeline of the campaign (logbook-condensed) with scroll-jacked reveals.
- **The stack display**: interactive code/terminal window typing the actual
  pipeline commands (render/encode/suite) — Meta vibe.
- **ImageTrail**: cursor-following images of the QA screenshots.
- **Threads viz**: flowing line canvas representing the studio pipelines.

### PHASE 9 — GENEVA + GLOBAL POLISH (the goal room / the finale)
- **The road to Geneva**: animated route (drawer → top 500 → top 100 → city
  showdown → Geneva · 20 Nov) with a progress line that fills on scroll.
- **Finale footer** on every page: giant "NO DRAWER LEFT BEHIND." grad-text,
  IG links, replay boot.
- **404 page**: playful (a lost drawer) — never a dead end.
- **Sound design pass**: ambient beds per room + UI blips + mute toggle +
  ear-check checklist for the user.
- **Performance audit**: 60fps on mid-range (devtools trace), bundle split,
  lazy-load three.js per page, image compression.

### PHASE 10 — THE SEO + SHAREABILITY PASS
- Meta/OG per route (title, description, og-image from the qa shots).
- Sitemap + robots · favicon set · PWA manifest + theme color.
- Social proof section: the live Insta grid embed (posts M1/M2/V2) with
  @1m1bfoundation tag — the CWC jury sees real activity.
- Preloader/a11y pass: keyboard nav, focus states, reduced-motion everywhere,
  aria labels.

### PHASE 11 — THE HARDENING (no more errors, ever)
- ESLint + strict mode + error boundary per route (friendly fallback, never blank).
- The QA gate runs on EVERY commit (a `pre-push` hook script).
- Stress: 10 browser restarts, slow-network simulation, 3G mobile, 390px+
  844px, fold states. Zero console errors = ship.
- The resurrection drill documented + scripted (`engine/resurrect.sh`).

### PHASE 12 — THE LAUNCH + THE RIVAL BEATER
- Final walkthrough video-style QA (headless capture of every route, all
  states) → the "go cry to every other website" reel.
- Compare checklist vs NIRMAN: receipts ✓ (we have them, he fakes them),
  3D ✓, character ✓, real deliverables ✓, performance ✓.
- Hand the user: the URL, the manual, the review checklist, the posting kit.

---

## 3. THE QA GATE (the anti-error doctrine — this is why I kept failing)

```
bash engine/verify_all.sh
```
1. **Compile gate**: every route .jsx returns 200 (no 500s — the class of bug
   that blanked the page).
2. **Render gate**: every route loads with `document.fonts.size >= 4`, main
   exists, scrollHeight > viewport (not a blank shell).
3. **Blank-screen detector**: viewport screenshot std >= 8 else FAIL
   (catches "black page" — the drawer bug class).
4. **Interaction gate**: suite.js overlap probes + CTA clickability + toy
   open-state, desktop + mobile.
5. **Console gate**: 0 pageerrors, 0 console errors, 0 failed requests.
6. **Verdict table** — every phase ships ONLY with all ✅.

**Error-prevention rules (banked):**
- After ANY patch: curl the changed module (200?) BEFORE opening the page.
- After ANY CSS change: check font/asset URLs resolve (the `../fonts` 404 class).
- Never trust a green suite alone — viewport-shoot + LOOK (pix.py ascii/stats).
- One browser per route in probes (sandbox crashes multi-page sessions).
- Commit after every phase (wipe doctrine: 6/6 wipes survived because of it).

---

## 4. THE USER'S PART (tiny)

1. Review each phase in the preview (~2 min): "GO" or "more juice here".
2. Ear-check at Phase 9.
3. Final approval at Phase 12.
That's it. Everything else is mine.

---

*Signed: the doctrine — think → research → map every anim → lock timeline → build
→ self-review → commit. Every phase. The loader stays. The rest gets rebuilt to
this spec, phase by phase, verified by the gate each time.* 🐝
