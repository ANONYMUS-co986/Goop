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
