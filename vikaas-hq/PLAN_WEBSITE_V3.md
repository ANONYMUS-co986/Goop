# 🏛️ VIKAAS UNIVERSE v3 — THE MASTER PLAN (FINAL v3.1, 24 PHASES)

> Locked after research on what actually wins awards. **24 micro-phases** — one
> attention-to-detail unit each, every one gate-verified before it ships.
> The loader (auto-boot → scroll universe) is KEPT. The user reviews per phase,
> says "continue!" → next phase.

---

## 0. THE RESEARCH (why this wins)

Awwwards criteria: **Design 40% · Usability 30% · Creativity 20% · Content 10%**.
Winners: Three.js/WebGL + GSAP choreography + custom interaction + 60fps mid-range.
Benchmarks: Hubtown (3D monolith), Cartier rooms, Sleep Well (scroll storytelling),
Uncommon (camera moves), By-Kin (Developer Award), Mat Voyce (kinetic type).
Stack that wins: **Vite + React + React Router + GSAP/ScrollTrigger + Lenis +
Three.js + our own lib/fx suite**. Ours beats NIRMAN on truth (real receipts).

---

## THE 24 PHASES (micro-granular, attention to the minutest detail)

### PHASE 1 — FOUNDATION + THE QA GATE (the anti-error power)
- Restructure app into `shell/ + pages/ + lib/fx/ + lib/hooks/`.
- **Build `engine/verify_all.sh`** — the gate: compile(200s) → render(main/fonts/h)
  → blank(std≥8) → console(0 errs) → per-route verdicts + exit code.
- **Resurrection script** `engine/resurrect.sh` (wipe-proof: venv + libs + npm).
- 5 core `lib/fx` effects + tests. **Definition of done = gate PASS.**

### PHASE 2 — DESIGN TOKENS + TYPOGRAPHY SYSTEM (the taste layer)
- One `tokens.css`: palette (ink/paper/acid/green/red/gold/violet), type scale,
  glass recipe, shadow/ease tokens, spacing rhythm, stamp styles.
- Typography detail: Anton display metrics (tracking, caps), Grotesk HUD,
  Devanagari fallback chain, line-height/letter-spacing per size.
- Every phase uses ONLY tokens (no magic numbers).

### PHASE 3 — THE SHELL v2 (nav + cursor + HUD, perfect)
- Glass nav: blur+saturate, brand, room tag, animated menu dots, overlay with
  staggered rooms, live/locked states, keyboard (Esc), focus rings.
- **Cursor v3**: blob + lag ring + velocity splash + label pills + state
  (hover/active/text) + reduced-motion + touch-safe.
- HUD: clock/coords/hashtags + scroll progress + grain/vignette/scanlines
  (token-driven) + audio mute toggle.

### PHASE 4 — ROUTE TRANSITIONS + LENIS v2 (between-page motion)
- **PageWipe**: acid curtain, room name in Anton, camera-style exit, 0.75s.
- **Lenis v2**: per-route instance, ScrollTrigger sync, anchor handling, pause
  during boot, reduced-motion off, mobile fallback.
- Route change: scroll reset + triggers refresh + wipe — no flash, no jump.

### PHASE 5 — THE BOOT POLISH (the beloved loader, made flawless)
- Keep auto-boot (typing terminal + scramble + lid-up + universe) — refine:
  timing curves, status line, skip, fast-mode, reduced-motion, mobile.
- New: **ambient audio bed for boot** (generated) + first-gesture unlock.
- Gate: boot route PASS (desktop+mobile+fast).

### PHASE 6 — THE GATE HERO v2 (3D monolith — the "wow")
- **Three.js e-waste monolith**: the drawer as a glowing monolith floating over
  a reflective grid; orbiting e-waste particles; mouse parallax; scroll-reactive
  (camera push as you scroll into the page).
- Performance: capped pixel ratio, lazy-loaded, fallback to nebula on low-end.

### PHASE 7 — THE GATE TYPOGRAPHY + PROOF RIBBON
- VIKAAS char-slam (SplitType, back.out, staggered) + gradient sheen sweep +
  hover glow on words · विकास pop · sub blur-in · chips pop + count-ups.
- **Proof ribbon**: thin strip, real counters (1.4 KG · ₹40 · 15 · 0) with
  stamp pops scrolling past.

### PHASE 8 — THE GATE ROOMS + MANIFESTO (the doors, perfect)
- Rooms grid: SpotlightCard + Tilt + Magnet + expandable teasers + status
  badges + keyboard-accessible.
- Manifesto: blur-reveal lines with rhythm, em pops, big "THE DOORSTEP IS."
- Ticker marquee refined (pause on hover, speed tokens).

### PHASE 9 — THE DRAWER INTRO + PINNED STORY (the story room)
- Intro hero (THE DRAWER, giant, glow) + scroll cue.
- Pinned story: photo clip-open + ken-burns, truth lines with intent pacing,
  15/0 slam + kicker. Timing curves locked.

### PHASE 10 — THE DRAWER TOY v2 (the interactive heart)
- The 3D drawer (from boot) becomes an explorable toy: open → items float out
  with physics-y ease → click item → **holographic spec card** (real audit
  line + stamp) → readout. Tilt + glow. Mobile tap-friendly.

### PHASE 11 — THE SCALE SEQUENCE (the "weighed, not guessed" moment)
- Scroll-driven weighing animation: drawer → scale → needle swings → settles
  at 1.4 KG → receipt prints. SVG needle + physics-y settle + stamp slam.

### PHASE 12 — THE 15/0 MAP (the data room moment)
- Stylized Gurugram map (SVG): 15 pulsing recycler dots + 0 doorstep markers
  + "the gap" callout + HSPCB source line. Animated on scroll.

### PHASE 13 — THE PROOF: RECEIPT PRINTER + STAMPS
- Receipt paper prints line-by-line (clip-path + typewriter) on scroll;
  stamps slam (WEIGHED/SOURCED/ESTIMATE/DRAMATISED) with rotation; tooltips.

### PHASE 14 — THE PROOF: ELASTIC SCALE TOY + MAGIC BENTO
- Interactive elastic slider (500 KG vs 1.4 KG) with count-up + verdict gag.
- MagicBento stats grid: 6–8 cells (3 phones/7 chargers/10 homes/1.4 KG/₹40/0
  doorsteps) with Spotlight + CountUp + hover expansion.

### PHASE 15 — THE PROOF: DOTGRID VIZ + SOURCES
- DotGrid data-viz: 3.2M tonnes / 22% animated dot matrix with cursor warp.
- Sources footer: HSPCB + CWC track, cited, stamped.

### PHASE 16 — THE KABADI UNIVERSE (the world room)
- Tier-list showdown: animated S→F cards, flip-in + tilt + glare; disputes CTA.
- ₹40 handshake looping micro-animation, scroll-scrubbed.
- Lore cards (horn/bicycle/scale) with Flip-in + Spotlight; dual-speed marquee.

### PHASE 17 — THE ARSENAL: DOCK + REEL LIGHTBOX
- Glass Dock (magnify on hover) for 6 reels.
- Reel cards: poster + GlareHover + hover-play + click → lightbox (player +
  caption + "use this sound" + stamp). Keyboard/Esc accessible.

### PHASE 18 — THE ARSENAL: 22-POST MASONRY + AUDIO LAB
- Masonry grid with FLIP animations + category filter (M/P/R) + hover zoom.
- Audio lab: A/B phonk players + **canvas waveform visualization** (generated).

### PHASE 19 — THE BUDDY: GALAXY SKY + REBEE HERO
- Hyperspeed/Galaxy canvas (mouse repulsion, star warp) background.
- ReBee TiltedCard 3D + glare + parallax layers.

### PHASE 20 — THE BUDDY: SCRAP-SCAN DEMO + POWERS
- **Playable SCRAP-SCAN**: click a device → hologram scan-line sweeps → tag
  card (contents/₹/nearest recycler). The superpower, interactive.
- 3 power SpotlightCards + mission line + character parade (scroll-stack).

### PHASE 21 — THE SYSTEM: MAKING-OF + TERMINAL
- The receipts-of-receipts: campaign timeline (logbook-condensed) with
  scroll-jacked reveals.
- Terminal window TYPES the real pipeline commands (render/encode/suite) —
  Meta-vibe, honest (these are the actual commands).

### PHASE 22 — GENEVA + FINALE FOOTER + 404
- Road-to-Geneva: animated route (drawer → top500 → top100 → showdown →
  Geneva · 20 NOV) with filling progress line.
- Finale footer on every page: giant grad-text + links + replay boot.
- Playful 404 (a lost drawer) — never a dead end.

### PHASE 23 — SOUND DESIGN + PERFORMANCE AUDIT (the craft pass)
- Ambient beds per room (generated, muted by default) + UI blips + whooshes +
  mute toggle. Ear-check checklist for the user.
- Performance: 60fps on mid-range (trace), code-split Three.js, lazy routes,
  image compression, font subsetting, bundle-size budget.

### PHASE 24 — SEO + A11Y + HARDENING + LAUNCH KIT (the finish)
- Per-route OG/meta/sitemap/robots/favicon/PWA manifest.
- a11y: keyboard nav, focus states, aria, reduced-motion everywhere.
- Error boundaries per route (friendly fallback, never blank) + pre-push gate
  hook + stress runs.
- Live Insta grid embed (M1/M2/V2 posted) + rival-beater checklist + handoff
  kit (URL, manual, review checklist, posting kit). **LAUNCH.**

---

## THE QA GATE (enforced every phase)

```
bash engine/verify_all.sh   # compile → render → blank → console → verdicts
```
- 18/18 PASS current baseline. Any FAIL = phase doesn't ship. Period.
- Error-prevention rules (banked): curl modules after patches · verify asset
  URLs after CSS · viewport-shoot + LOOK after any change · one browser per
  probe · commit after every phase.

## THE USER'S PART
Say **"continue!"** per phase (~30s review) · ear-check at Phase 23 · final
approval at Phase 24. That's all.

---

*24 phases. Minutest details. Gate-verified every step. The loader stays.* 🐝
