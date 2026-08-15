# 🏛️ VIKAAS — THE APP + PORTFOLIO · MASTER PLAN v5 (FINAL, 12 Aug 2026)

> **The idea (locked):** VIKAAS is an **e-waste collection app** — households
> book doorstep pickups; the app **recruits collection centres** (the kabadiwala
> network + authorised recyclers) to serve every doorstep; weigh → value →
> pickup → receipt → verified recycling. **We build it before NIRMAN can steal
> the lane.** The portfolio sells the app — the same way NIRMAN's does — but with
> our REAL proof (1.4 kg weighed, ₹40, 15 HSPCB recyclers, 0 doorsteps).
> Mission: **NO DRAWER LEFT BEHIND.** Roadmap: M1 ✓ M2 ✓ → Top 100 → City
> Showdown → **GENEVA · UN · 20 Nov 2026.**

---

## PHASE 0 — DONE (the stack + foundation + gates)
0 stack (Vite/React/GSAP/Lenis/Three/R3F/Framer/Zustand) · 1 foundation+QA gate
· 2 tokens · 3 shell v2 · 4 transitions+Lenis v2 · 5 boot polish · V41 idea
narrative + routing · V42 ENTER-bug killed · V43 **menu clickability killed +
CLICK GATE (19/19 PASS)**.

---

## THE 30+ PHASES

### THE PORTFOLIO (the pitch that sells the app) — Phases 6–24
| # | Phase | Big implementation |
|---|---|---|
| 6 | **Gate hero v2 — 3D monolith** | Drawer-as-monolith over reflective grid, orbiting e-waste particles, mouse parallax, scroll-reactive camera (R3F + postprocessing). |
| 7 | **Gate: THE DRAWER NATION + THE GAP** | The problem (3.2M t/yr · 22% · 10/10 homes) + the structural gap (15/0/500-vs-1.4) — scroll-jacked stats, dotgrid, source stamps. |
| 8 | **Gate: core directive + THE 4-TAP FLOW + founders** | The directive; interactive pipeline (drawer→scale→list→drop→₹40 receipt); founder + ReBee strip. |
| 9 | **Drawer intro + pinned story polish** | CSS-sticky scrub pacing, photo treatment, truth-line rhythm. |
| 10 | **Drawer toy v2** | 3D drawer explorable: items float, holographic spec cards, tilt+glow. |
| 11 | **The scale sequence** | Scroll-driven weighing: needle swings → 1.4 KG settles → receipt prints. |
| 12 | **The 15/0 map** | SVG Gurugram map: 15 pulsing recyclers, 0 doorsteps, gap callout, HSPCB source. |
| 13 | **Proof: receipt printer + stamps** | Paper prints line-by-line, stamps slam, tooltips. |
| 14 | **Proof: elastic scale + magic bento** | Physics slider 500 vs 1.4, bento stats. |
| 15 | **Proof: dotgrid viz + sources** | 3.2M/22% matrix, cursor warp; cited sources. |
| 16 | **Kabadi universe** | Tier showdown, ₹40 handshake loop, lore, network roles (household/kabadi/recycler/ReBee). |
| 17 | **Arsenal: dock + reel lightbox** | Glass dock, reel cards, hover-play, lightbox. |
| 18 | **Arsenal: masonry + audio lab** | 22-post FLIP masonry, filters, waveform audio lab. |
| 19 | **Buddy: galaxy sky + ReBee hero** | Hyperspeed canvas, TiltedCard, parallax. |
| 20 | **Buddy: SCRAP-SCAN demo + powers** | Playable hologram scan, 3 power cards, parade. |
| 21 | **System: making-of + terminal** | Timeline + terminal typing the real pipelines + QA-gate viz. |
| 22 | **Geneva: roadmap + finale + 404** | Road-to-UN fill, finale CTA, playful 404. |
| 23 | **Sound + performance** | Ambient beds, UI blips, mute; 60fps audit, code-split. |
| 24 | **SEO + a11y + hardening + launch** | OG/sitemap/insta-embed, a11y, error boundaries, pre-push gate, handoff kit. |

### THE APP (the real product — the moat) — Phases 25–34
| # | Phase | Big implementation |
|---|---|---|
| 25 | **APP: architecture + data model** | Vite+React app `/app` (separate route group); models: Household, PickupRequest, CollectionCentre, Kabadiwala, Receipt, Recycler; localStorage/IndexedDB seed (real demo data from our audit). |
| 26 | **APP: the request flow** | Book a pickup: address, drawer estimate (kg), photo → auto-value (₹40/kg-ish model) → slot pick. Working wizard with validation. |
| 27 | **APP: the centre recruitment flow** | "Register your collection centre": kabadiwala/recycler onboarding — name, area, capacity, pricing; a live roster. THE moat feature (NIRMAN doesn't have real centres). |
| 28 | **APP: the map** | Interactive Gurugram map: households (dots), centres (pins), routes — the doorstep network made visible. |
| 29 | **APP: the receipt engine** | Generated receipt per pickup: weigh-in, ₹ paid, centre, recycler, stamp. Print/share. |
| 30 | **APP: ReBee assistant** | In-app SCRAP-SCAN (choose device → value + centre match) + DOORSTEP DIAL (auto-book). |
| 31 | **APP: the ledger dashboard** | Impact stats: kg diverted, ₹ paid out, pickups served, households — per centre + total. |
| 32 | **APP: state + persistence + demo seed** | Zustand store, IndexedDB, a "demo mode" that replays our real audit (1.4 kg → ₹40 → centre X). |
| 33 | **APP: polish + the pitch tie-in** | The portfolio's CTA now points INTO the working app ("Book your first pickup") — the portfolio is the pitch, the app is the proof. |
| 34 | **THE LAUNCH** | Full walkthrough QA (portfolio + app), rival-beater checklist, the "go cry to every other website" reel, handoff kit. |

---

## THE QA GATE (law — every phase)
`bash engine/verify_all.sh`: compile → render → blank → console → **clicks**
(menu + all links) → verdicts. **Current: 19/19 PASS.** DOM law: never manually
remove/replace React nodes (state + CSS only).

## THE USER'S PART
**"continue!"** per phase. Ear-check at 23. Final GO at 34. That's it.

---
*The idea, fully told, then built. Before him. Real. VIKAAS.* 🐝
