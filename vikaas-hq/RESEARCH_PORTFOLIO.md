# PORTFOLIO RESEARCH PACK — for the upcoming VIKAAS site (2026-08-05)
*Pre-work so the next prompt hits a fully-loaded runway. All references are open-source or public.*

## 1) Component arsenals to ADAPT (never copy-paste naked — we re-skin to Vikas tokens)
- **reactbits.dev** (37k★, #2 JS Rising Stars 2025; MIT): 110+ text/3D/motion components, GSAP+Three.js optional, NO framer lock-in. High-value picks for us: **TiltedCard** (3D hover), **CardSwap / Stack** (interactive card layouts on touch), **ScrollStack**, **CircularGallery (3D bend)**, **SpotlightCard**, **Dock**, **ImageTrail**, **PixelTransition**, **Magnet**.
- **Aceternity UI** (Tailwind+Framer; heavier but dramatic): 3D Card, Spotlight beams, expandable cards, sticky scroll reveals. Trade-off: template-y if used raw → we port patterns, not skins.
- **Magic UI / cult-ui / kokonutui / 21st.dev**: micro-interaction refs (gooey navs, animated counters, text reveals).
- **ayush013/folio** (GitHub): senior-dev portfolio using Next+GSAP+Tilt with PERF notes (layer mgmt, repaint budgets) — our perf playbook template.

## 2) The over-the-top archetypes (what "maximus optimus" means concretely)
- **Bruno Simon portfolio** (three.js driving-game site) — interaction-as-personality. Our analog: **drive-the-kabadiwala-cart** mini-room (matter.js physics, avoid CRT TVs, deliver to the gate).
- **Awwwards 2025-26 patterns**: scroll-jacked horizontal stories, sticky pinned chapters, WebGL shader heroes (r3f/drei), kinetic variable-font type, cursor-reactive magnetic UI, page transitions (FLIP), masked image reveals, split-text word staggers, LOTS of quiet moments between loud ones.
- Specimen refs seen in search trail: linear.app polish, vercel ship pages, Ali-Sanati awwwards-portfolio (R3F scroll rig).

## 3) Chosen architecture (my call as architect — answer to his "you decide")
- **Stack: zero-dep static multi-page** (our verde-showcase engine wins again) — instant loads, GitHub Pages/Vercel free deploy, total control; GSAP 3 (ScrollTrigger+Flip) + Lenis smooth-scroll + three.js (custom lightweight scenes, no R3F) + Howler for our synth stingers/cumulations. Multi-page = /story /proof /films /system /kabadi-universe /lab /2047 (+/404 funny guilt page).
- Perf contract: LCP < 1.4s on 4G, 60fps scroll on low-end Android, every heavy scene behind IntersectionObserver + prefers-reduced-motion variants, `.ttf` subset fonts w/ unicode-range. Measured & published in README (receipts, even for perf).
- Identity (his pick): **personal(builder) × VIKAAS flagship merge** — Aarav the builder; the drawer as the origin myth; films/cards embedded natively.
- Signature rooms (first-pass sitemap):
  1. **Hero: THE DRAWER** — scroll opens a 3D drawer (CSS 3D + real photo planes); items fly out with labels; each is a card = reactbits-adapted TiltedCard with touch-flip showing "2014 lie" vs "fact".
  2. **PROOF LEDGER** — archival table: weigh-day receipt, HSPCB 15 rows, source stamps; drag-to-weigh toy (SliderTrack physics, number counter).
  3. **FILMS** — 4 videos embedded as cinema cards w/ custom scroll-gated playheads.
  4. **KABADI UNIVERSE** — comic scrollytelling + PhysicsDump toy (matter.js: throw chargers into the right bin; wrong bin = smoke).
  5. **SYSTEM** — our counter-spec to his OS-jargon: human-first spec sheet, "0 buzzwords, 15 recyclers" grid, mini boot-screen parody room ("HIS OS: jargon. OURS: receipts.").
  6. **LAB** — the engine showcase: trackgen synth players, probe sheets, commit graph — "built with code, on purpose".
  7. **2047 / CWC** — mission timeline, #EWasteOff wall, CTA.
- Audio: per-room stinger from `trackgen.py` + silent-by-default, click-to-enable (polite + legal).

## 4) Explicit non-goals
No copying his copy/brand; no live interference with his repos/sites; no fake stats anywhere on site (same charter as the feed).
