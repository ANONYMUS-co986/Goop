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

## Up next
- B1: mind-bending preloader (boot kernel → particle gather → split-text
  explosion → reveal) + holographic hero canvas + burger menu shell.
