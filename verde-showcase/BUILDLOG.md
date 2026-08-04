# VERDE SHOWCASE — build log (Night Lab)

Round 2 cinematic showcase for Project Verde. Multi-page Next.js site.
Anuj's app = functional dashboard. This site = the judge-melting artifact.
Rule of the house: every batch ends with a headless QA pass (HTTP 200,
zero console errors, screenshot inspected like a judge).

## Locked stack (decoded 2026-08-04)

| Area | Choice | Why |
|---|---|---|
| Framework | Next.js 15.5 App Router + TS | Multi-file, Vercel deploy like their app |
| Styling | Tailwind 3.4 | Speed; token system = Night Lab |
| 3D | three 0.177 + @react-three/fiber 9.7 + drei 10.7 + @react-three/postprocessing | Hero hologram, exploded ESP32 |
| Motion | GSAP 3.15 (all plugins free since Apr 2025) + framer-motion 12.43 | ScrollTrigger choreography + UI springs |
| Scroll | lenis 1.3 (autoRaf) | studio-freight-grade kinetic feel |
| Fonts | @fontsource syne (600/700/800), sora (300/400/500), jetbrains-mono (500) | NEW identity vs the doc's Space Grotesk/Inter |
| Accel | React Bits patterns (TS+Tailwind) | Custom cursor, grain, marquees |
| 3D assets | Quaternius CC0 via poly.pizza (GLB) | Public-domain plant/nature models |

Fontnote: Clash Display + General Sans are Fontshare-only; Fontshare is
unreachable from the build sandbox and Fontsource does not carry them.
Syne + Sora keep the "nothing like the doc" mandate. Vendored via npm =
works offline at the venue.

## Night Lab tokens
ink `#050D0B` family · lime `#A6FF3F` · uv `#A78BFA` · hydro `#67E8F9` ·
dew `#E9FFF2` · amber `#FFC24B` · danger `#FF5C6C`
grain overlay (SVG turbulence, steps(8)) · thin grid bg · CRT scan util ·
custom cursor (lime dot + lerped reticle, coarse-pointer + reduced-motion safe)

## Batch record

### B0 — toolchain proof ✅ (2026-08-04)
- Scaffold: package/tsconfig/next.config/postcss/tailwind, layout with
  fontsource imports, SmoothScroll/Cursor/Grain in root layout.
- app/page.tsx: B0 proof shell (to be replaced by real hero in B1).
- QA harness: `build/shot.js` (headless chromium via build/tools; self-heals
  /tmp AL2023 libs after sandbox wipes). Usage:
  `NODE_PATH=build/tools/node_modules node build/shot.js <url> <out.png> [waitMs] [scrollY]`
- QA result: HTTP 200, zero console/page errors, `build/render/b0_home.png`
  inspected — fonts, stroke text, chips, marquee, grid, cursor all render.
- Infra notes: build/tools was wiped by a sandbox reset (gitignored) —
  reinstalled `@sparticuz/chromium@138.0.2 + playwright-core@1.49.1`;
  shot.js now inflates `al2023.tar.br` itself when missing.

### B1 — Home + site chrome ✅ (2026-08-04) — QA 8/8 PASS
- **Preloader** (`fx/Preloader.tsx`): 4-stage boot — kernel log stagger,
  % counter + rail, sprout stroke-draw, 5-strip scaleY exit explosion.
  sessionStorage fast re-boot; tap/Esc skips; reduced-motion → gone.
- **Hero** (`three/HeroCanvas.tsx` + `HeroSection.tsx`): fully procedural
  hologram (ZERO downloaded assets) — one shared GLSL fresnel shader
  (pot/stems/ribbon-leaves), looping 6.5 s scan-band rebuild soil→crown,
  random flicker, sparkles ×2 + grid floor; postprocessing stack =
  Bloom + ChromaticAberration 0.00045 + Noise + Vignette, NoToneMapping.
  Pointer-parallax rig; **portrait screens dolly the plant back in Z so the
  headline keeps clear air** (QA F5).
- **Burger nav** (`nav/Burger.tsx` + `nav.ts`): clip-circle wipe overlay,
  staggered route rows w/ LIVE+batch chips, ghost numerals, syscon footer
  (session uptime), Esc closes, Lenis pauses while open.
- **Home page**: hero + `#saga` bento (6 doors) + LEDGER marquee.
  Route transitions (`app/template.tsx`) blur-rise via framer-motion.
- **FabGate** (`sections/FabGate.tsx`): honest in-fabrication interstitial
  for /build /brain /doctor /proof /team until their batches land.
- QA: see `qa/QA_LOG.md` — 8/8 PASS, 3 harness fixes + 3 site fixes
  (cursor 0,0 artifact F4, mobile holo crowding F5, menu footer overlap F6).

### B2 — /build ✅ (2026-08-04) — QA 5/5 PASS
- **Sticky exploded rig** (`three/BuildCanvas.tsx`): 380vh scroll-scrubbed
  disassembly. 7 board parts stair-rise → 7 external modules orbit out →
  slack wires re-tether every module to its GPIO pad (14-seg arcs
  recomputed per frame). All procedural: PCB + lime edge trace, ESP32
  shield can w/ antenna zone, twin pin-header bars, USB, EN/BOOT, GPIO2
  LED (emissive), DHT11, soil probe, HC-SR04 (chrome eyes), LDR, relay,
  pump, UV strip (emissive uv). drei Html mono labels per part.
- **Stage rail**: DISASSEMBLY % + scaleX rail + 5 named stages
  (CHASSIS/BRAIN/SENSES/HANDS/WIRED) w/ swap captions + right-edge ticks.
- **Receipts**: 12-row BOM table — real haul, ₹1,890 total row.
- **Pin map**: 8 GPIO cards straight from firmware v3.0.7 (incl. the
  active-LOW pump relay + probe power gating callouts).
- Responsive: narrow-aspect rig scale 0.58, mobile stage rail, scroll
  progress via rAF-throttled listener (no ScrollTrigger dependency).
- QA: `qa/QA_LOG.md` — 5/5 PASS, fixes F7–F12 (spread, spin rate,
  framing, headers, probe visibility, portrait crop).

### B3 — /brain + interaction kit ✅ (2026-08-04) — QA 9/9 PASS
- **THE STORM** (`fx/StormCanvas.tsx`): pure Canvas2D viz of the 17→2 bug —
  before = 17 choked packets/cycle + hard "10s AUTO STUTTER" freeze wave;
  after = 2 laminar bundle packets. Slot-deterministic spawns (exactly 17
  or 2 per cycle), live cycle/call counters, pauses offscreen, static
  frame for reduced-motion. Animated before/after toggle (spring pill).
- **CASE FILE: THE 10s STUTTER** — 6 chapter cards (symptom → discharge)
  w/ per-chapter spotlight color (danger/amber/lime).
- **PIPELINE** — SENSE→FILTER→DECIDE→ACT→REPORT stage cards w/ hover
  tips carrying the real engineering notes (hysteresis, probe gating,
  ring filters, active-LOW).
- **TERMINAL** — line-staggered excerpt of actual v3.0.7 constants.
- **Interaction kit (new in `fx/`)**, wired through every shipped page:
  - `Switch` — page-switch loader: 5-strip ink curtain + destination
    flash, push-at-blackout, lifts when the new route mounts (failsafe
    2.4s), reduced-motion = instant nav. Driven by `TransitionLink`.
  - `ScrambleText` (decode-on-hover / on-mount), `Magnetic` (spring
    pull), `GlowCard` (spotlight + mask-composite border gleam),
    `Tip` (global data-tip follower), `CountUp` (IO-driven),
    cursor **label lens** (`data-cursor` → ring blooms w/ caption).
- QA: `qa/QA_LOG.md` — 9/9 PASS, fixes F13–F15.

## Up next
- B4: **/doctor** — the AI Plant Doctor: camera pipeline (ESP32-CAM →
  Vercel upload → crop.kindwise 94% vs Gemini), Rx card UI, three-tier
  AI fallback chain as an interactive route diagram.
