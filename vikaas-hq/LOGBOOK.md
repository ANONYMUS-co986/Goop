
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

## V4-5 — Voice v2 pipeline + sandbox resilience
- Arena snapshot pruned .venv node_modules mid-turn; hard-reset from origin recovered full tree (all masters/posts/tracks were tracked — zero loss). Venv rehomed OUTSIDE repo (/home/user/.studio_venv — exclusion-proof), engine/lib.js now has ffmpeg fallback chain.
- Vidδ audio v2: narration voice (idx0, steadier phonemes) for POV+mummy; per-character pitch casting for the rest (narrators −4.5%, papa −3%, kabadi −6.5% + warmth EQ + compressor + tiny room). FIXED the trap: mp3 inputs are 24kHz — asetrate without prior aresample=44100 speeds 1.75×. Duration-preserving chain = aresample→asetrate→aresample→atempo(inverse).
- 10 clips/turn generate_speech cap: hit mid-set; remaining 6 narration variants queued for next turn (cap resets). Kokoro Route A docs ready in TTS_UPGRADE.md for true-final Hindi.
- TTS sandbox verdict (banked): HF/github-assets/bing all TLS-blocked; edge-tts dead here; kokoro deps installed + voices pending Route A.

## V4-6 — The Great Model Hunt (why sandbox TTS must exit the sandbox)
- User demanded open-source Hindi TTS with emotion. Ran the full gauntlet: edge-tts (bing TLS), piper pratham/priyamvada (Git LFS pointers; media.githubusercontent + LFS S3 + raw + objects + jsdelivr + zenodo all dead), kokoro release assets (EOF), kittentts (no bundled weights), npm piper-tts-web 160MB (wasm only), HF models (blocked). VERDICT: egress policy = github.com+npm+PyPI+apt only; every model CDN on the planet is outside it. Documented per-attempt in TTS_UPGRADE.md (credibility artefact, shows the work).
- SHIPPED the escape hatch: studio/voice_pipeline.py — one-command script (auto-download Piper native-Hindi pratham/priyamvada OR Kokoro-82M; 8 comedy lines with per-character emotion presets: narrator deadpan grave vs kabadi fast/gruff vs mummy female voice; em-dash beat silences; wav out + report). Validated piper-tts imports + SynthesisConfig surface in-sandbox (root import, not piper.config — fixed).
- Skill banked: GitHub contents API reports LFS OBJECT size (63.5MB) while raw blob is a 133B pointer — always blob-check before celebrating.

## V5 — FINAL PACK & QC SWEEP (2026-08-05)
- Assembled `studio/drops/FINAL_PACK/`: all 5 video masters in one folder, canonically renamed (`VIKAAS_01..05`).
- QC battery on finals: decoded-wav md5s (all unique) · ebur128 (−18.2…−19.6 LUFS, spread 1.4 LU) · aspectralstats centroids (0.7k lo-fi → 4.8k phonk) · cross-correlation vs all candidate tracks.
- **CAUGHT & FIXED 1:** vid03 secretly carried the same music as vid01 (corr 0.746 vs Thinking Music). Regenerated `TR_F_bounce-lite.wav` from trackgen (`build_kabadi_bounce(gags=())`), bar-grid window 4.8–20.2s @100bpm, fades + loudnorm −16.5, remuxed. Now corr 0.80 TR-F fam / 0.058 Thinking Music.
- **CAUGHT & FIXED 2:** Devanagari TOFU in vid04 master — `.dev` font lost specificity wars vs `.qcard .q`/`.nm` (Anton scopes). Surgical fix: appended `'Devnag'` fallback to every font-family decl in reel_d/e/e2.html. Full re-render (1224 frames) + re-encode; audio mix byte-identical in final (md5 match proves mix preserved). मम्मी/कैलकुलेटर cards verified glyph-perfect.
- **CAUGHT & FIXED 3:** vid03 & vid05 shared two verbatim cards ("HIS SCALE: AT MY GATE TOO." + plan chips). Re-cut 03 only (05 = flagship, untouched): hook → "EVERYTHING. EXCEPT MY DRAWER.", close → dark-ink counter-plan ("1 DRAWER · 1.4 KG · GATE, DIRECT."). Re-rendered + encoded with TR-F.
- New docs: `FINAL_PACK/README.md` (index) + `FINAL_PACK/QC_REPORT.md` (method receipts) + `qc_all5_contact_sheet.png` (4 frames × 5 vids). UPLOAD_KIT_V4 paths → FINAL_PACK.
