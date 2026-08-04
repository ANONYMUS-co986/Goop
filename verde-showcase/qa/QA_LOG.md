# QA LOG — Verde Showcase (Night Lab)

Every batch ends the same way: serve → headless capture → judge-style review →
log → fix → re-capture → commit. Harness: `build/shot.js` (self-healing
@sparticuz/chromium + playwright-core). Command shape:

```bash
export NODE_PATH=build/tools/node_modules
node build/shot.js <url> <out.png> [waitMs] [scrollY] [waitForSelector] [clickSelector]
# mobile: QA_VW=390 QA_VH=844 · skip preloader ritual: QA_NOSKIP=1
```

Headless context of record: SwiftShader software GL renders the site at
~1–2 fps (real hardware is 60–120 fps). GSAP's default lag smoothing clamps
>500 ms frames to 33 ms, which makes timelines *appear* frozen headless-only.
Fix ∈ harness, not the site: the app exposes `window.__qaNoLag()` from
`SmoothScroll.tsx`, shot.js calls it post-hydration so GSAP tracks wall-clock.
With it, the boot timeline completes naturally in ~3.5 s wall — correct.

---

## Batch B1 — Home + chrome (2026-08-04) — **8/8 PASS**

| # | Capture | View | HTTP | Console errors | Verdict |
|---|---------|------|------|----------------|---------|
| 1 | `b1_preloader_mid.png` | desktop 1440×900 | 200 | none | PASS — boot log fully streamed, sprout drawn, 39% counter, rail fill |
| 2 | `b1_hero.png` | desktop | 200 | none | PASS — hologram plant + spores + grid + type lockup |
| 3 | `b1_saga.png` | desktop @y=1000 | 200 | none | PASS — bento, ghost numerals, LIVE chip, batch chips |
| 4 | `b1_burger.png` | desktop, menu open | 200 | none | PASS — command deck, session timer, ESC hint, close btn |
| 5 | `b1_fabgate.png` | desktop `/build` | 200 | none | PASS — in-fabrication interstitial, marquee, blueprint bg |
| 6 | `b1m_hero.png` | mobile 390×844 | 200 | none | PASS (after F5 fix) |
| 7 | `b1m_burger.png` | mobile, menu open | 200 | none | PASS (after F6 fix) |
| 8 | `b1m_saga.png` | mobile @y=900 | 200 | none | PASS |

### Findings & fixes this batch
- **F1 (harness)** playwright `click()` needs element stability; GSAP twitter
  mutates styles forever → clicks time out. Ritual switched to keyboard
  `Escape` (a real supported skip) + force-click fallback. No site change.
- **F2 (harness)** skip could land before hydration attached listeners →
  retry loop (15 × press+check) until `[role=dialog]` detaches.
- **F3 (harness)** GSAP lagSmoothing froze *all* timeline QA at 1–2 fps →
  `__qaNoLag()` bridge (see header). Boot verified wall-perfect at ~3.5 s.
- **F4 (site, fixed)** custom cursor dot rendered at (0,0) until first
  mousemove → stray "dead pixel" on load. Dot+ring now init offscreen.
  `Cursor.tsx`.
- **F5 (site, fixed)** mobile hero: hologram crowded the VERDE headline
  (lime-on-lime). Rig now dollies plant back in Z and drops it on portrait
  aspect (<0.78) — feet stay planted on the grid. Re-QA'd PASS.
  `HeroCanvas.tsx`.
- **F6 (site, fixed)** mobile command-deck footer slid under the fixed N
  mark. Footer left-padded to 4.5 rem on small screens. Re-QA'd PASS.
  `Burger.tsx`.

### Notes
- `b1_preloader_mid.png` is a deliberate early-flight capture (~39%).
  Standard ritual shots always skip the preloader first (deterministic).
- Interactions verified by capture, not just code: menu open (4/7),
  scroll position (3/8), preloader states (1), WebGL first frames (2/6).

---

## Batch B2 — /build (2026-08-04) — **5/5 PASS**

| # | Capture | View | HTTP | Console errors | Verdict |
|---|---------|------|------|----------------|---------|
| 1 | `b2_header.png` | desktop | 200 | none | PASS — THE BUILD., LIVE chip, stat chips |
| 2 | `b2_mid.png` | desktop @73% explode | 200 | none | PASS — constellation mid-air, slack wires |
| 3 | `b2_full.png` | desktop @100% WIRED | 200 | none | PASS — every module tethered to its pad |
| 4 | `b2_bom.png` | desktop receipts | 200 | none | PASS — 12 rows + ₹1,890 total + pin map |
| 5 | `b2m_explode.png` | mobile 390×844 @95% | 200 | none | PASS — narrow-aspect rig scale holds frame |

### Findings & fixes this batch
- **F7 (site, fixed)** first explode pass scattered parts out of frame →
  every dir vector tightened ~40%, camera pulled to z=7.4.
- **F8 (site, fixed)** 0.12 rad/s turntable over-rotated before captures →
  0.04 rad/s (classier live AND deterministic in QA).
- **F9 (site, fixed)** full-explode state drifted out of the top of frame →
  rig y re-centers with progress (`-0.9 - p·0.55`).
- **F10 (site, fixed)** pin headers rendered as one implausible gold plank
  (and an empty label chip) → twin 2.5u bars, label only on the first.
- **F11 (site, fixed)** soil probe near-black on ink + its label collided
  with the % rail → lightened to #48555F, explode y lifted.
- **F12 (site, fixed)** portrait viewports clipped the module orbit →
  narrow-aspect rig scale lerp to 0.58 (verified in `b2m_explode.png`).
- Accepted as designed: edge-of-orbit clipping of pump/soil labels as the
  turntable slowly rotates (parts drift in/out like a real exhibit).

---

## Batch B3 — /brain + interaction kit (2026-08-04) — **9/9 PASS**

| # | Capture | Subject | HTTP | Console errors | Verdict |
|---|---------|---------|------|----------------|---------|
| 1 | `b3_header.png` | THE BRAIN header + toggle | 200 | none | PASS |
| 2 | `b3_storm_before.png` | storm mode: 17-packet congestion | 200 | none | PASS — ANOMALY LIVE, calls 17/cycle |
| 3 | `b3_storm_after.png` | toggle flip → 2-call laminar flow | 200 | none | PASS — NOMINAL, counters 2/cycle (6 = 3×2 ✓) |
| 4 | `b3_hover_case.png` | case-file card hover | 200 | none | PASS — spotlight tracks cursor + title caught mid-scramble |
| 5 | `b3m_storm.png` | mobile storm | 200 | none | PASS (toggle-nowrap after F14) |
| 6 | `b_transition.png` | curtain mid-cover w/ strip gaps | 200 | none | PASS — page-switch loader fires |
| 7 | `b_transition_arrive.png` | arrival on /build after curtain | 200 | none | PASS — full cover→push→reveal loop (cursor lens showing "OPEN" too!) |
| 8 | `b3_burger.png` | command deck on /brain | 200 | none | PASS — active route lime, B2 now ● LIVE |
| 9 | `b_home_recheck.png` + rAF probe | hero after interaction upgrades | 200 | none | PASS (verification via DOM probe: stats count ₹1,863→target ✓) |

### Findings & fixes this batch
- **F13 (site, fixed)** framer-motion `useInView` never fired under headless
  QA → CountUp reverted to a hand-rolled IntersectionObserver. DOM probe
  verified live counting (₹1,863 → 1,890 mid-ease = correct behavior).
- **F14 (site, fixed)** mobile storm toggle wrapped its labels to two lines
  → whitespace-nowrap on both pills.
- **F15 (harness)** first transition test clicked the *same-route* card —
  Switch correctly no-ops `href === pathname`. Not a bug; harness target
  clarified (`#saga a[href='/build']`), full loop then proven (6+7).
- Accepted quirk: cursor lens label persists one beat after SPA nav if the
  mouse never moves (it heals on the first real mousemove — humans move).
- Infra: sandbox wiped node_modules again mid-batch → both toolchains
  reinstalled; al2023 libs self-healed via shot.js as designed.

---

## Batch B4 — /doctor + scroll/heavy-lift kit (2026-08-04) — **6/6 PASS**

| # | Capture | Subject | HTTP | Console errors | Verdict |
|---|---------|---------|------|----------------|---------|
| 1 | `b4_header.png` | AI DOCTOR + ghost Rx parallax | 200 | none | PASS |
| 2 | `b4_chain_kill.png` | kill-switch on crop.kindwise | 200 | none | PASS — strike-through, SERVING→gemini, revive btn, live tooltip ✓ |
| 3 | `b4_eye.png` | cam mock + scanline + spec chips | 200 | none | PASS |
| 4 | `b4m_doctor.png` | mobile chain + Rx | 200 | none | PASS (after F17) |
| 5 | `b_home_scrollfx.png` | saga w/ 4 LIVE doors + velocity marquee | 200 | none | PASS |
| 6 | `b3_casefx.png` | tilt case files + pipeline regroup | 200 | none | PASS |

### Findings & fixes this batch
- **F16 (verified behavior)** SplitText headers: animation completes then
  DOM reverts to plain text — settle-state captures prove clean final
  typography; mid-char-explosion frames are non-deterministic headless.
- **F17 (site, fixed)** mobile: the 13-char unbreakable "PRESCRIPTION."
  overflowed 390px → xs size 1.65rem, wraps clean on two lines.
- **F18 (performance contract, kit)** anti-stutter measures: `ViewportPause`
  kills R3F frameloops when any canvas leaves the viewport (hero + exploded
  rig), Lenis → `ScrollTrigger.update` glue + refresh on load/fonts, all
  reveals `once:true` transform/opacity-only, SplitText reverts its DOM
  after each blast. Nothing animates that isn't on screen.
- Saga board state: HOME / THE BUILD / THE BRAIN / AI DOCTOR all ● LIVE.

### Scroll & component kit shipped (React Bits ports, Night Lab flavor)
`SplitReveal` (GSAP SplitText char explosions on scroll-enter) ·
`Reveal/RevealGroup` (ScrollTrigger rise/blur/stagger) · `TiltCard`
(3D perspective tilt + spring return) · `ShinyText` (light sweep) ·
`ClickSpark` (global click tracers) · `RotatingText` (hero cue cycler) ·
`VelocityMarquee` (Lenis-velocity speed + skew) · `Parallax` (ghost
numeral drift) · `ViewportPause` (canvas sleep). Registered once via
`lib/gsap.ts`.

### Interaction kit shipped (all pages upgraded)
`Switch` curtain loader on every TransitionLink (burger rows, saga cards,
hero CTAs, next-door links, FabGate) · `ScrambleText` decode-on-hover ·
`Magnetic` spring buttons · `GlowCard` cursor-tracking spotlight + border
gleam · `Tip` global data-tip tooltip (hero stats, pin map stories, pipeline
stages) · `CountUp` hero stats · cursor **label lens** via data-cursor.
