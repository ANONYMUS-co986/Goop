# 🎬 DROP V3 — the finale content drop (plan of record, 5 Aug 2026)

Deliverables: **2 reels ("the finales") + a post arsenal + full upload kit.**
Everything studio-built, self-reviewed frame-by-frame, integrity-gated.

## A) The stack decision (researched 5 Aug — full notes)
| Candidate | Verdict |
|---|---|
| Custom studio v3 (HTML/CSS/JS + **GSAP-driven, seek-scrubbed timeline** → headless Chromium frame capture → ffmpeg) | ✅ **CHOSEN** — same paradigm as 2026's `nexu-io/html-video` ("Hyperframes": per-frame HTML → headless render → ffmpeg concat) but with full control + offline resilience + zero license risk |
| Remotion | ❌ heavy, source-available license w/ fees above 4 devs, redundant vs our proven path |
| Motion Canvas / Revideo (TS canvas) | ⏳ strong for future explainers (M3 pitch); overkill now |
| MoviePy 2 | ⏳ optional assembly helper only |
| **ffmpeg** (xfade, loudnorm, overlays) | ✅ encoder + transition finisher |
| openshot/filmora | ❌ GUI tools; can't drive them code-first here — our pipeline beats them anyway |

**The v3 engine upgrade:** previous drop hand-rolled per-frame JS easing.
V3 drives a **GSAP master timeline** (staggers, overshoot/back eases,
MotionPath logo traces, SplitText char/word explosions — the same GSAP
that powers the showcase site) scrubbed deterministically:
`window.seek(t) → tl.progress(t/duration)` → screenshot frame f. Time is
no longer attached to wall-clock → zero dropped frames, easing identical
every render. ~900 frames per 30 s reel.

Audio: `Thinking_Music.mp3` (Kevin MacLeod, CC-BY 4.0 — credit in
caption) quiet-register mix (lesson from Entry 18), loudnorm to ≈ -19
LUFS, highpass 90 Hz. Runtime budget: **25–30 s per reel (Vision-2047
rule: budget = hard cap × 0.85).**

## B) REEL α — "THE DRAWER" v3 (the flagship, ~27 s, 1080×1920@30)
Identity: his **SVG logo draws itself on** (stroke-dashoffset) as the
cold open — the signature no template-editor can ship.
Storyboard (12 beats, sound-off readable, big-number pops on 0 and 15):
1. Logo ident draw-on (~2.2 s) → acid wipe
2. HOOK (0.5 s legible): "Open the drawer you've been ignoring." + 3-2-1 removed per v1 feedback → direct
3. Photoreal drawer (rebuilt, amateur-snapshot cues) + "you call it a drawer."
4. Item callouts stagger: 3 phones · 7 chargers · 1 swollen power bank
5. **1.4 kg** count-up (scale pop, eases)
6. Pattern interrupt: comic flip — "10 homes. Same drawer."
7. Tally marks animate (diagonal 5th stroke)
8. **0** (red pop) — "recyclers they could name."
9. **15** (green count-up 1→15) — "in Gurugram alone. HSPCB list."
10. "The infrastructure exists."
11. "Nobody told us."
12. Punchline card: "The world didn't need me. My drawer did." + handle + waveshape end-plate
Transitions: cross-dissolve 0.3 s w/ motion, acid wipe across intro cut, white flash ONLY on beats 8/9 (34%→20%), eased Ken Burns, film grain + vignette, progress bar, per-scene parity with the poster system so grid + reel feel like one universe.

## C) REEL β — "15 RECYCLERS. 0 DOORSTEPS." (~24 s) — the argument nobody else has
Zero integrity risk (it's about the system, not our numbers).
Storyboard (10 beats):
1. HOOK: "Gurugram has **15** government-authorised e-waste recyclers." (Brutalist data style, source topbar: HSPCB)
2. "I checked the government list myself." (PDF ghost behind, stamp: GOVT SOURCE)
3. "Then I did something nobody does." — phone-call UI card
4. **TALLY of calls**: 5 calls dialed (real once Aarav does them; ✂️ gate until then — fallback copy: "Ask one out loud")
5. Answers montage: "bulk only." "minimum 500 kg." "who is this?" (Hinglish gag: "बेटा, minimum 500 किलो" comic beat)
6. **0** — "doorsteps they'll ever collect from."
7. Contrast beat: kabadiwala horn vs recycler hold-music (text-led)
8. Punchline: "The doorstep is missing. Not the infrastructure."
9. CTA: "So this Sunday, my drawer becomes 1.4 kg of proof." (✂️ swap to generic if unverified)
10. Brand end-plate: logo draw-on micro + #EWasteOff

## D) POST ARSENAL (7 cards, 1080×1350, each a distinct art direction)
1. `P1_riso_meme` — risograph street-poster meme v3 (acid green/magenta misregistration; NEW punchline; humour-first)
2. `P2_15_zero` — editorial data card: "15 recyclers. 0 doorsteps." (the β anchor, cream paper + bar)
3. `P3_comic_hinglish` — 3-panel Hinglish saga v3 ("E-waste recycle करने चला था" universe, new joke)
4. `P4_blueprint_mine` — technical blueprint: "it isn't rubbish, it's a mine" (gold/copper/gram math per phone — verified figures)
5. `P5_tierlist_hinglish` — meme tier list v3 (कबाड़ीवाला stays, new tiers)
6. `P6_template_classic` — **real-template meme** (imgflip-blank composite, e.g. Drake/Distracted adapted to "new phone vs drawer") — answers the "real images meme" ask properly
7. `P7_method_receipts` — "How I'll prove it" (weigh-scale photoreal, 01–04)
+ `P0_pfp` refresh only if needed; alt-English variants for humour cards.

## E) Captions + upload kit
Per asset: full caption (Hinglish where the art is, ✂️-gated numbers,
the sourced 15-recyclers + 3.2Mt+22% lines always available), hashtag
set (mix niche+broad, NOT his phonk tag-soup), pinned-comment for reels,
posting schedule (2 reels first to juice the dormant account, then
alternate cards), 7–9 pm IST, tag @1m1bfoundation when scored, story
re-share step, and the reel audio credit line.
Metrics to send me every Sunday: screenshots of insights (or just tell
me likes/comments via a "scout" request — I'll pull both handles).

## F) QA loop (non-negotiable)
HTML render → full-size PNG review of EVERY card → fix → re-render →
extract 6+ frames per reel at story beats → inspect → captions/loudness
verified by ffprobe/astats → only then the upload kit ships. Logged in
this HQ.
