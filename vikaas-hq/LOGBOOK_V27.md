# LOGBOOK V27 — LOADER PERFECTION + THE GATE + PER-PAGE ANIM MAP (11 Aug 2026)

**Order:** "proper and the best" — loader still has imperfections (native white
scrollbar, cursor weak, wants anims planned for every page). Doctrine: think →
research → map every anim → lock timeline → build → self-review → commit.

## Loader v3.1 polish (the imperfections)
- **Native scrollbar GONE** on loader (html.no-bar via shell.js; the progress
  rail + % readout is the indicator) + **branded scrollbar** (green→acid gradient
  thumb) on content pages.
- **CHAPTER HUD**: 00 IGNITION → 07 THE DOOR, synced to scroll progress.
- **Rail % readout** beside the progress rail.
- **Scan sweep** — a soft acid line drifts down the stage every 7s (CRT vibe).
- **Word float** after assemble (yoyo y -8) + existing pulse glow.
- **CURSOR v2** (reactbits-grade, shared shell.js): acid blob (lerp 0.16) + lag
  ring (lerp 0.07) + **velocity particle splash canvas** + hover labels
  ([data-cursor]) + scale-on-interactive. All pages.
- Shell: glass nav + overlay + wipes + Lenis + hover audio blips (single reused
  AudioContext) — shared across pages.

## PHASE 2 — THE GATE (index.html) BUILT
Aurora hero (3 drifting blobs) · SplitType VIKAAS char slam + विकास pop ·
BlurText sub (word blur-in) · chips + count-ups · manifesto blur-reveal lines ·
spotlight stat cards (radial --mx/--my + count) · rooms grid (stagger + 3D tilt +
status badges: LIVE/LOCKED) · ReBee band (parallax + tilt + 3 powers) · Geneva
footer (big line reveal) · glass nav + cursor + wipes + grain + HUD.

## Bugs caught by self-review (all fixed)
1. shell.css font paths `../assets/fonts` → `../fonts` (double-assets 404).
2. **SCRUB NEGATIVE/NaN progress crash**: `CHAPTERS[-1]` → `reading '0'` —
   clamped + isFinite guard (6× pageerror caught by suite).
3. suite.js: CTA selector now generic (`--cta=`) — gate has no #enter.

## SUITE RECEIPTS (all PASS)
- loader desktop: PASS · loader mobile: PASS
- gate desktop: PASS · gate mobile: PASS (--cta=.gnav-menu)
- pix ascii of gate hero: nav pill top, VIKAAS bright, chips visible — clean.

## NEXT
User GO → Phase 3 THE DRAWER. ReBee submission deadline TODAY (12 Aug) — PENDING.
