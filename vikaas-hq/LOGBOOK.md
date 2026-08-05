
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

## V4-1 — Audio sovereignty achieved (trackgen.py)
- 3 original loops synthesised in pure numpy: TR_B "TAPE AUDIT" (92bpm D-minor pad/clock-tick/bell investigative bed), TR_E "DOORSTEP PHONK" (140bpm F#-minor memphis cowbell + distorted 808 + hat rolls + riser), TR_D "KABADI BOUNCE" (100bpm oom-pah + slide-whistle/boing/honk gags on a param timeline). QA'd via spectrogram PNGs (structure visible: gaps/sweeps/gag glides) + astats peaks (−0.35..−0.96 dBFS).
- Banked skills: one-pole LP loop, Schroeder combs+allpass reverb, tanh drive chain, sidechain pump (unused in final — beds sit clear), tape_dress (hiss+crackle+flutter = identity). Rule: drama needs pad+air; phonk needs 8th grid + saturation; comedy needs silence between oom-pahs so the VO lands.
- pip → PyPI reachable: numpy in studio venv OK.

## V4-2 — EDIT γ2 "DOORSTEP PHONK PROTOCOL" (19.72s, 591 frames, beat-grid locked)
- All cuts on 140bpm 4-beat multiples (C(n)=n*0.4286). New transitions: VHS streak rows + whip-blur entrances + viewfinder brackets/REC pulse on photo cuts. Real imagery: drawer photo (own) + landfill photo (tapp.online, clean) + kapwing blank puppet (cropped to panels). "IT JUST…VANISHES." blur-out now hands off INTO the landfill ("THIS IS WHERE 'AWAY' LIVES.") — the best single beat in the drop.
- Bug banked: bare class selectors ('.bk1') match the FIRST scene only — always scope '#cN .bk1'. Lesson permanent.

## V4-3 — VID δ "MERE GHAR KA E-WASTE COMEDY CLUB" (40.8s) — first AI-voiceover film
- 8× generate_speech (lang=hi, masculine/characters) clips, deadpan narrator reads; durations probed then timeline built BACKWARD from VO so jokes land (bounce text at whistle-down, elastic calc at boing, tag swing at honk). Premixed bed 0.40 + VO 1.35, alimiter 0.95 → engine loudnorm.
- Puppet template lesson: kapwing temp-1 was a FILLED example ("what's that smell") not a blank — inspect every meme asset at 100% before compositing. Fix = temp-3 classic blank, cropped to panels; puppet now a running-gag across both new vids (comedy repetition = signature).
- Integrity: gold figure hedged "~0.034g/phone (un/epa estimates)" ON-SCREEN plus "recycler quotes dramatised" pattern from reel 2. Funny AND bulletproof.

## V4-4 — Post fleet P1–P7 + fixes logged
- 7 cards 1080×1350@2x: riso meme / 15-0 ledger / 3-panel saga SVG / blueprint mine / tier list / classic drake / receipts protocol. Self-review caught: P2 slash colliding with label (moved), P4 right callouts clipped past 1080 (reseeded+resized), P6 header wrap (nowrap). Re-shot, verified via fix sheet. UPLOAD_KIT_V4.md = calendar+captions+click-by-click+rules.
