# LOGBOOK V23 — VIKAAS PORTFOLIO v2: THE HUB, Awwwards-push (11 Aug 2026)

**Order from Aarav:** "make me a banger website cum portfolio for VIKAAS — we began
making but took a detour." + "set that all up" (the browser/self-review suite).

## What shipped — `vikaas-hq/portfolio/` v2
The hub (`index.html`) rebuilt as a one-page cinematic experience, layered on the
existing juice shell (site.js/site.css — vbar, vnav overlay, cursor, tooltips,
wipes, grain, magnets, count-ups — untouched, so ledger.html + films.html keep
working).

### The stack (all VENDORED locally — zero CDN deps, self-review renders pixel-true)
- `assets/vendor/gsap.min.js` + `ScrollTrigger.min.js` + `CustomEase.min.js` (from studio node_modules)
- `assets/vendor/lenis.min.js` (npm, v1.3.26) — smooth scroll wired to ScrollTrigger
- `assets/vendor/SplitType.min.js` (npm, v0.3.4 umd) — char-level hero surgery

### The choreography (`assets/site2.js`, `assets/site2.css`)
1. **BOOT** — terminal sequence types 7 lines (drawer scan → 1.4 KG → 10 homes →
   15 recyclers → 0 doorsteps → NO DRAWER LEFT BEHIND), progress bar, skip button.
2. **HERO** — SplitType char stagger (yPercent 120 + rotate, power4.out), eyebrow,
   sub, 4 stat chips (1.4 KG / ₹40 / 15 / 0, count-up via site.js), scroll cue.
3. **TICKER** — infinite marquee of brand beats.
4. **STORY** — PINNED scrub (1900px): drawer photo clip-path opens, 4 lines reveal,
   "15 RECYCLERS. 0 DOORSTEPS." slams in, kicker lands.
5. **RECEIPT** — paper prints via clip-path scrub, 4 stamps (WEIGHED/SOURCED/
   ESTIMATE/DRAMATISED) slam in with rotation, tooltips on stamps.
6. **SCALE** — 500 KG vs 1.4 KG bars grow, "SHORT BY 498.6 KG" punch, link to ledger.
7. **ARSENAL** — PINNED horizontal scroll of 6 reel cards (real posters extracted
   from the masters, hover-play video on desktop, tap on mobile) + 22-post marquee.
8. **REBEE** — v6 hero image with pointer-tilt + parallax, 3 power cards, mission.
9. **PLAN** — vertical road to GENEVA · UN · 20 NOV 2026, gradient line draws on scrub.
10. **FOOTER** — giant NO DRAWER LEFT BEHIND., room links, handles, reboot button.

## THE SELF-REVIEW LOOP (the "set it up" part)
`vikaas-hq/studio/engine/shoot_site.js` — headless-Chromium harness: walks all 8
sections, captures /tmp/qa/*.png, reports every console/page error. Run:
`cd vikaas-hq/studio && node engine/shoot_site.js`
Then pixel-analysis + ASCII luminance maps (the no-vision sight rig) verify each
frame. This cycle caught/fixed: boot typewriter span-clobbering bug (rewrote
renderer to append finished lines once), capture-timing artifacts (story copy IS
visible at mid-scrub — verified op=1 at prog 0.77).

## QA receipts (11 Aug)
- Desktop 1440×900: all 8 sections captured · **0 console/page errors** ·
  story scrub progress 0.24→0.77 animates lines correctly · all 4 stamps op=1 ·
  arsenal horizontal pin scrolls (5 cards in view, track x=-301) · plan/foot fine.
- Mobile 390×844: hero + chips render, 0 errors.
- Fonts self-hosted (Anton/Archivo/SpaceGrotesk/NotoSansDevanagari) — no Google
  Fonts dependency, headless screenshots are pixel-true.
- Reel posters: 6 extracted from masters (assets/posters/VIKAAS_0X.jpg).

## Still open
- Room pages (ledger/films) keep old chrome — could get v2 polish next round.
- Sound design (hover blips, boot beep) — ears off for me; user does final ear-check.
- Deployment: serve.py serves vikaas-hq root (Range support for videos) — preview
  URL = the live check.

## Waiting on user
- Look at the preview (serve.py) — verdict: which section needs MORE juice.
- ReBee submission (deadline TOMORROW 12 Aug) · posting run (Anuj 8 posts ahead).
