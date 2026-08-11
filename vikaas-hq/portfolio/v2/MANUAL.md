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
├── loader.html        ← PHASE 1.1 (DONE): THE BOOT — scroll-cinematic entry
├── index.html         ← THE GATE (Phase 2): hero + manifesto + ticker + cursor v2
├── drawer.html        ← THE DRAWER (Phase 3): the story, pinned cinematic scrub
├── ledger.html        ← THE PROOF (Phase 4): receipts, scale toy, data viz, glass bento
├── kabadi.html        ← THE KABADI UNIVERSE (Phase 5): the world, tier list, the trade
├── films.html         ← THE ARSENAL (Phase 6): 6 reels, hover-play, audio lab, glass dock
├── rebee.html         ← THE BUDDY (Phase 7): ReBee page, tilt/parallax/3D energy
├── system.html        ← THE SYSTEM (Phase 8): the making-of, the engine, the receipts
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
| `boot.wav` — C5-E5-G5 ascending blips | loader (first gesture) | ✅ built (Phase 1) |
| `enter.wav` — thump + whoosh + chord stab | loader ENTER | ✅ built (Phase 1) |
| runtime whooshes (WebAudio noise sweeps) | loader beat transitions | ✅ built (Phase 1) |
| hover blip (tiny sine tick) | all interactive elements | Phase 2 |
| ambient beds (numpy-synthesized, VIKAAS scale) | every page, mute toggle | Phases 2–8 |
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
| **1** | **THE BOOT — loader v2** (done ✅) | **scroll-driven** · code-built 3D drawer (Three.js) · terminal reveal · scramble wordmark · glitch bursts · stats slam + stamps · ReBee fly-by · ENTER pill · synth audio | **review now** |
| 2 | **THE GATE** (index) | SplitText hero · Aurora · BlurText manifesto · ticker · glass nav · cursor v2 · hover glow | review |
| 3 | **THE DRAWER** | pinned cinematic scrub · photo clip reveal · scroll-jacked typography · LetterGlitch transition | review |
| 4 | **THE PROOF** (ledger) | MagicBento stats · scale toy (ElasticSlider) · receipts · SpotlightCards · DotGrid viz | review |
| 5 | **THE KABADI UNIVERSE** | the world · tier list · the ₹40 trade · marquee chaos | review |
| 6 | **THE ARSENAL** (films) | glass Dock nav · reel cards (GlareHover, PixelTransition, hover-play) · audio lab | review |
| 7 | **THE BUDDY** (rebee) | Hyperspeed/Galaxy sky · TiltedCard · spotlight powers · character parade | review |
| 8 | **THE SYSTEM** | the engine room · ImageTrail · Threads viz · powers.md interactive | review |
| 9 | **POLISH** | ambient soundscape full pass · perf 60fps audit · a11y · reduced-motion · final QC battery | final review |

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


---

## 9. THE BOOT — loader v4 (FINAL): AUTO BOOT → SCROLL UNIVERSE

### FLOW (two phases, one story)
**PHASE A — AUTO BOOT (~10s, no scroll needed):**
| t | beat |
|---|---|
| 0.0 | boot overlay in (nebula + glass card + sheen) |
| 0.3–7.0 | terminal TYPES 7 lines char-by-char (cursor, progress bar, status labels) |
| 7.0–8.4 | VIKAAS wordmark SCRAMBLE + glitch |
| 8.4–9.4 | "READY." + bar fills |
| 9.4–10.5 | overlay slides UP (acid) → reveals the 3D stage · "SCROLL TO ENTER THE UNIVERSE" |

**PHASE B — SCROLL UNIVERSE (460vh pinned, scrub):**
| progress | beat | animation |
|---|---|---|
| 0.00–0.02 | HUD + chapter + cue | fades in |
| 0.05–0.20 | camera | push-in (cam-object tween) · lid creaks 3° |
| 0.20–0.38 | THE OPEN | **LID FLIPS UP (rotation −1.95, negative x = rises up & back)** · light spill ignites (0→9) · e-waste floats + orbits |
| 0.38–0.52 | THE WORD | VIKAAS scramble-assembles · glitch bursts · pulse-glow + float (separate tween — infinite repeats MUST NOT live inside scrubbed timelines) |
| 0.52–0.64 | THE PROOF | stats slam (back.out) + stamps rotate in |
| 0.64–0.78 | THE FLIGHT | ReBee arcs across · विकास in · whoosh |
| 0.78–0.90 | THE LINE | big line char-stagger (SplitType) |
| 0.88–1.00 | THE DOOR | ENTER pill → acid exit → GATE |

**BANKED BUG (this build):** a `repeat:-1` tween inside a scrubbed timeline makes its
duration infinite → ScrollTrigger progress math collapses (lid never opened, camera
jumped to end). Infinite loops must be started via `tl.call()` as SEPARATE tweens.
Verified: lidX 0.005 → −1.851 → −1.95 (opens UP), camZ 7.13 → 6.6 → 5.2.

### NEBULA + TEXT FX (reactbits aesthetics, shared shell)
- `.nebula` — 4 drifting blurred gradient orbs (violet/acid/green/gold), screen blend
- `.glow-hover` — text glow on hover (acid double-shadow) · `.shiny` — animated
  sheen eyebrows · `.grad-text` — animated gradient big-lines · section-title
  hover glow · magnetic `[data-mag]` buttons
- Expandable room cards (`data-expand`): click to expand teaser + CTA, `+` rotates 45°

## 10. THE UNIVERSE MAP (the whole world, planned)

**One continuous story.** Every page is a ROOM in the VIKAAS machine. You enter
through the drawer and exit at Geneva. Each room has: a cinematic scroll intro,
2–4 over-the-top FX, at least one interactive moment, one stat with a stamp, and
a door to the next room.

```
LOADER "THE BOOT"        scroll-driven ignition · 3D drawer opens · e-waste flies
   │  ENTER THE DRAWER (acid exit)
   ▼
GATE (index)             THE MANIFESTO — SplitText hero · Aurora · BlurText copy ·
                         ticker · cursor v2 · hover-glows · the 4 stats
   │  scroll → story pin
   ▼
DRAWER                   the origin — pinned scrub · photo clip reveal ·
                         LetterGlitch transition · "15 RECYCLERS. 0 DOORSTEPS."
   │  the receipts → door to proof
   ▼
PROOF (ledger)           THE EVIDENCE — MagicBento stats · scale toy (elastic) ·
                         receipts · SpotlightCards · DotGrid viz · stamps everywhere
   │  the world → door to kabadi
   ▼
KABADI UNIVERSE          THE TRADE — tier list · the ₹40 handshake · kabadi lore ·
                         marquee chaos · interview cards
   │  the arsenal → door to films
   ▼
ARSENAL (films)          THE OUTPUT — glass dock nav · 6 reel cards (glare/pixel
                         hover, hover-play) · audio lab · poster wall
   │  the buddy → door to rebee
   ▼
BUDDY (rebee)            THE HERO — galaxy sky · TiltedCard · spotlight powers ·
                         character parade · SCRAP-SCAN demo
   │  the system → door to the engine room
   ▼
SYSTEM                   THE MAKING — ImageTrail · Threads viz · powers.md
                         interactive · the receipts of the receipts
   │  scroll → the goal
   ▼
GENEVA (footer/end)      NO DRAWER LEFT BEHIND. · @1m1bfoundation · the plan
```

**Rules of the universe:** every door is a page-wipe with the room name in Anton ·
every stat wears a stamp · every room has its own ambient bed (generated) · the
HUD (coords/hashtags/clock) persists everywhere · reduced-motion + touch fallbacks
are non-negotiable · the integrity gate never breaks (WEIGHED / SOURCED / ESTIMATE /
DRAMATISED).

## 11. THE FINALE POWER SUITE (my tools, now a CLI)

| Tool | What it does |
|---|---|
| `studio/engine/suite.js` | one-command self-review: scroll-beat walk, screenshots, console-error capture, **overlap probes** (elementFromPoint), ENTER clickability, `verify` mode exits 1 on any fail |
| `studio/engine/pix.py` | the sight rig: `stats` (mean/std/dark/acid/green) · `ascii` (luminance map) · `diff` (pixel diff + region map) · `region` (crop QA) |
| `studio/engine/shoot.js` | per-section screenshot walk for pages (multi-section) |
| `studio/engine/shoot_boot.js` | loader-specific beat walk |
| `studio/engine/make_nss_stub.py` | ELF stub forge (browser bootstrap) |
| `studio/engine/chromium_bootstrap.sh` | one-command browser rebuild after wipes |

**The loop (every phase, non-negotiable):** `node engine/suite.js verify <url>` +
`node engine/suite.js qa <url>` → `pix.py stats/ascii` on the beats → 0 errors +
0 overlaps + clickable CTAs = ship. Then YOU review. Then next phase.


---

## 12. PER-PAGE ANIMATION MAP (the complete plan — every room, every anim)

> Doctrine: think → research → map EVERY anim → lock timeline → build → self-review → commit.
> Every page below ships with this map executed. Self-review gates: `suite.js verify` desktop+mobile PASS.

### ROOM 00 — THE BOOT (loader.html) ✅ BUILT
| # | Anim | Trigger | Technique |
|---|---|---|---|
| 1 | HUD + chapter labels fade | scroll 0% | GSAP opacity, CHAPTERS array synced to progress |
| 2 | Terminal 7 lines reveal | scroll 2–10% | scroll-linked opacity per line |
| 3 | Camera push-in | 8–20% | cam-object tween (codrops pattern) + lerp loop |
| 4 | Lid creak → swing open | 12–38% | pivot rotation power2.inOut |
| 5 | LIGHT SPILL ignites | 22% | point light intensity 0→9 |
| 6 | E-waste floats + orbits | 21–38% | y tween + spin loop (bob+spin) |
| 7 | VIKAAS scramble-assembles | 38–52% | char scramble onUpdate + back.out pops |
| 8 | Glitch bursts | 40/46% | CSS glitch keyframes |
| 9 | Word pulse-glow + float | 50%+ | CSS pulseGlow + yoyo y-tween |
| 10 | Stats slam + stamps | 52–64% | back.out(2.2) + stamp rotate-in |
| 11 | ReBee arc fly | 64–78% | left tween + glow drop-shadow |
| 12 | विकास fades | 68% | opacity |
| 13 | Big line char-stagger | 78–90% | SplitType yPercent 120 + back.out |
| 14 | ENTER pill | 88–100% | pop + pulse glow + click → acid exit |
| FX | scan sweep · rail + % · dust canvas · whooshes | continuous | CSS scan + WebAudio |

### ROOM 01 — THE GATE (index.html) ✅ BUILT
| # | Anim | Trigger | Technique |
|---|---|---|---|
| 1 | Aurora blobs drift | load | CSS radial gradients, 3 blobs, 16–27s alternate |
| 2 | Glass nav drops | load 0.05s | y -80 → 0, vx ease |
| 3 | VIKAAS chars slam | load 0.2s | SplitType chars, back.out(1.7), stagger 0.05 |
| 4 | विकास pops | load 0.9s | scale pop ease |
| 5 | Sub words blur-in | load 1.05s | BlurText: filter blur(10px)→0, stagger 0.018 |
| 6 | Chips pop + count-up | load 1.4s | pop ease + countUp rAF |
| 7 | Cue fades | load 1.9s | opacity |
| 8 | Manifesto lines blur-reveal | scroll | blur(14px)→0 + y 46→0, once per line |
| 9 | Spotlight stats slam + count | scroll | radial --mx/--my spotlight + back.out + countUp |
| 10 | Room cards stagger + 3D tilt | scroll | back.out stagger + pointer rotateX/Y |
| 11 | ReBee parallax + tilt | scroll | yPercent scrub + perspective tilt |
| 12 | Powers reveal | scroll | staggered rise |
| 13 | Footer big line | scroll | y 50→0 vx |

### ROOM 02 — THE DRAWER (drawer.html) — PHASE 3 · PLANNED
| # | Anim | Trigger | Technique |
|---|---|---|---|
| 1 | Pinned photo reveal | scroll pin | clip-path inset sweep (drawer opens) |
| 2 | Truth lines rise | scrub | y+opacity per line, power3 |
| 3 | "15 RECYCLERS. 0 DOORSTEPS." slam | scrub | scale back.out + red flash |
| 4 | LetterGlitch transition | section change | clip-path slices + text-shadow rgb split |
| 5 | Drawer photo ken-burns | scroll | scale 1.02→1.12 scrub |
| 6 | Ticker speeds up | scroll | animation-duration scale |

### ROOM 03 — THE PROOF (ledger.html) — PHASE 4 · PLANNED
| 1 | MagicBento stats grid | scroll | bento cells stagger + spotlight |
| 2 | Scale toy (elastic) | scroll | ElasticSlider physics drag |
| 3 | Receipt print | scroll | clip-path top→bottom scrub |
| 4 | Stamps slam | once | back.out + rotate |
| 5 | DotGrid data viz | scroll | canvas dots + cursor warp |
| 6 | Count-ups everywhere | view | rAF countUp |

### ROOM 04 — THE KABADI UNIVERSE (kabadi.html) — PHASE 5 · PLANNED
| 1 | Tier list cards | scroll | stack reveal + tilt |
| 2 | ₹40 handshake loop | load | infinite yoyo scale/rotate |
| 3 | Marquee chaos | continuous | 2-speed opposing lanes |
| 4 | Interview cards | scroll | Flip-in + spotlight |
| 5 | Map dots pulse | scroll | SVG circle pulse |

### ROOM 05 — THE ARSENAL (films.html) — PHASE 6 · PLANNED
| 1 | Glass Dock nav | load | magnet + scale-on-hover |
| 2 | Reel cards glare | hover | GlareHover sheen sweep |
| 3 | Poster pixel-transition | hover | PixelTransition dissolve |
| 4 | Hover-play videos | hover | muted play/pause |
| 5 | ScrollStack | scroll | cards stack on scroll |
| 6 | Audio lab | click | play/AB/captions |

### ROOM 06 — THE BUDDY (rebee.html) — PHASE 7 · PLANNED
| 1 | Galaxy/Hyperspeed sky | load | canvas star warp + mouse repulsion |
| 2 | ReBee TiltedCard | hover | perspective tilt + glare |
| 3 | Power spotlight cards | scroll | radial spotlight |
| 4 | SCRAP-SCAN demo | click | hologram scan-line sweep + tags |
| 5 | Character parade | scroll | image trail / flip cards |

### ROOM 07 — THE SYSTEM (system.html) — PHASE 8 · PLANNED
| 1 | ImageTrail cursor | hover | images follow cursor |
| 2 | Threads viz | load | canvas flowing lines |
| 3 | powers.md interactive | scroll | typewriter + code window |
| 4 | Receipts of receipts | scroll | stacked receipt cards |

### ROOM ★ — GENEVA (footer of every page) ✅ (in GATE)
| 1 | Big line reveal | scroll | y + vx |
| 2 | Links magnet | hover | magnet pull |
| 3 | Replay boot | click | wipe to loader.html |

### SHARED (every room)
Cursor v2 (blob+ring+splash+labels) · glass nav + overlay · page wipes · grain/vignette/scanlines · HUD corners + clock · hover blips (WebAudio) · ambient beds per room · reduced-motion + touch fallbacks · suite.js verify PASS before ship.
