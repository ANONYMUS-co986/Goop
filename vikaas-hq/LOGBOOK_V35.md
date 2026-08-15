# LOGBOOK V35 — STACK UPGRADE: Framer Motion + R3F suite (12 Aug 2026)

**Order:** "install framer and any other libs u feel like that will help, setup
urself."

## Installed (all clean, 0 vulnerabilities)
- **framer-motion 13** — declarative micro-interactions, AnimatePresence exits
- **@react-three/fiber 9.7 + drei 10.7 + @react-three/postprocessing 3.0.5 +
  postprocessing 6.39** — the 3D renderer stack (bloom/glitch/DoF effects)
- **maath 0.10 + three-stdlib 2.36 + zustand 5** (UI/audio state) + clsx
- **three 0.185.1 + @types/three** — modern three (peer-conflict fixed:
  postprocessing needs >=0.182 → latest aligned)
- Fontsource vars for future use.

## Role split (the modern pattern)
- **Framer Motion** = component micro-motion (hover/tap/AnimatePresence page exits)
- **GSAP/ScrollTrigger** = scroll choreography + timelines
- **R3F** = 3D scenes (monolith hero, drawer toy v2, galaxy)
- **Zustand** = audio/ui state (mute toggle, theme)
- Verified app still compiles + Vite up (200).

## Next
Phase 0 recorded → Phase 1 (foundation + QA gate) on "continue!"
