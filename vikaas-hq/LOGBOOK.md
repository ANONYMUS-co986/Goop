
## Entry V3-1 — 2026-08-05 🏭 STUDIO ENGINE v3 + REEL α MASTER
- Built the deterministic render engine (`vikaas-hq/studio/engine/`): GSAP
  master timeline scrubbed via `window.__reel.seek(t)` → headless Chromium
  frame capture (self-healing AL2023 libs) → static ffmpeg (venv
  imageio-ffmpeg 7.0.2) encode. Zero wall-clock dependence.
- Assets: photoreal drawer + scale "receipt" shots generated with the
  amateur-snapshot technique (no studio-gloss cues) — drawer reads as a
  genuine phone photo (2 cracked phones, cable nest, power bank).
- QA loop: 14-frame probe → caught photo letterboxing (xPercent cover fix),
  hidden parent containers (#chips/#kg), kicker placeholder; draft 10fps
  sheet → final 30fps master. 816 frames @0.35s/frame.
- SHIPPED: `drops/v3/01_REEL_the-drawer_v3.mp4` — 1080×1920 · 27.2s ·
  H.264 CRF18 · 8.6MB · CC-BY Thinking Music quiet mix (loudnorm -19 LUFS).
  12 beats: SVG logo draw-on ident → hook → drawer → 3/7/1 chips → 1.4 KG
  → homes flip → tally → 0 → 15 (+HSPCB source chip) → quotes → punchline
  card with strike. Footer progress + handle everywhere.
- NEXT: Reel β ("15 recyclers. 0 doorsteps."), post arsenal (7 cards),
  upload kit (captions/tags/schedule).

## V3-2 — REEL β "15 RECYCLERS. 0 DOORSTEPS." shipped (c50272b)
- 26.0s, 30fps, 780 frames, H.264 3.5MB. Beats: 15-count (HSPCB source bar) → govt-list card + GOVT SOURCE stamp → call-dial UI w/ hold-music EQ → answers montage (3 quote cards, Devanagari №3) → red **0** hero → recycler-vs-kabadiwala VS → cream punch ("THE INFRASTRUCTURE ISN'T MISSING." struck → "THE DOORSTEP IS.") → weigh-day polaroid CTA → end plate.
- INTEGRITY GATE LANDED: no fake call tally; quotes are labelled ON-SCREEN "dramatised — call one yourself & see. we dare you." Zero becomes "**advertise** doorstep pickup for a 1–2 kg lot" — defensible from the public list. This is the lesson from the charter codified: turn the disclaimer into engagement.
- Probe (19 beats) reviewed: all land; count-ups deterministic on scrub; eq-bar yoyo repeats scrub fine; polaroid image load OK.

## V3-3 — EDIT γ "THE KABADIWALA PARADOX" shipped
- 14.6s phonk-style kinetic cut: 10 hard cuts, RGB-split flares (screen-blend red/blue layers), shake bursts, flash frames, scanlines. Stats used = the always-safe two (3.2Mt/yr, ~22% — sourced on-screen to CWC climate track). Hinglish card "तो भैया… डिलीवरी मैं ही करूँगा।" is the meme heart.
- Learning: `.lay` RGB copies must be `position:absolute` INSIDE the .big (relative) so flare offsets don't reflow; `mix-blend-mode:screen` only reads right on dark scenes — so flare used on ink cuts, cream cuts get shake only.
- First encode chain glitched transiently (render output eaten); rerun clean. Rule banked: never trust a chained pipe silently — re-run pieces with visible output.
- AUDIO: both baked with the CC-BY quiet mix (Thinking Music fade/hp/loudnorm). Edit γ's upload note = swap trending audio in-app (IG library), Original Audio → 0. Legit phonk without copyright strikes.
