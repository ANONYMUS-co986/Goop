# LOGBOOK V21 — THE FINAL HERO IMAGE: research-backed, pixel-QA'd, locked (11 Aug 2026)

**Order from Aarav:** "one last chance at the hero image — search the web, learn,
make the image that forces the judges to give the juice bonus points."

## 0. Research (what actually wins — 4 rubric sources synthesized)
- ARTEFFECT scoring rubric: Creative Interpretation of the story 40% +
  Aesthetic Value 40% + Impact 20%.
- ITU AI for Good "Canvas of the Future": theme/SDG connection, clarity of
  message, visual impact, potential to inspire — creativity over technique.
- Youth photo-contest judging philosophy: "authentic storytelling consistently
  outperforms technically polished but emotionally flat work."
- CapCut CRE[AI]TE: continuity in character/world/style; a brand that plays a
  real role; a clear feeling for the audience.
- **Synthesis — the winning image must:** (1) scream theme relevance (e-waste)
  wordlessly, (2) carry an emotional human story, (3) have ONE clear focal
  point, (4) keep the established character 100% consistent, (5) be thumbnail-
  legible + poster-grade.

## 1. Three concepts forged (all reference-chained to v3_suitup for character lock)
| File | Concept | Emotional lever |
|---|---|---|
| `v5_drawer_awakening.png` | ReBee rising from the e-waste drawer in a warm Indian home, parts assembling, a little girl in a yellow dress watching in wonder | origin + human connection (THE story: matches Q2 "hatched from an electronics drawer in Gurugram") |
| `v5_doorstep_dawn.png` | ReBee holding the weighing scale with a phone at an Indian doorstep at sunrise, kabadiwala lane behind | mission + proof ("weighed, not guessed") |
| `v5_guardian_skyline.png` | ReBee on an e-waste mountain over the Gurugram skyline at dusk | epic scale (but research: emotionally flatter) |

## 2. Pixel QA (all vs v3 baseline)
| metric | v3 (old) | v5a | v5b | v5c |
|---|---|---|---|---|
| brightness (mean) | 55.2 dark | **102.7** | 108.1 | 91.7 |
| warm px | 84k | **1,019k** | 952k | 635k |
| copper (body) | 5.2k | **240k** | 175k | 66k |
| yellow (stripes) | 1.1k | **113k** | 37k | 13k |
| green (LED eyes) | 192k | 19k ⚠️ | 66k | 175k |
| edge darkness | 86% vignette | **35% open** | 51% | 44% |

v5a wins story + warmth + character-signature color, but its green eyes were
soft (19k) — ReBee's identity is the green LED visor.

## 3. The surgical fix → **v6_FINAL**
- Edit v5a with image-reference: "only change = BOTH green LED eyes glowing
  bright, with green glow reflecting on the girl's face."
- QA: green px **19.4k → 31.5k (+62%)**; scene preserved (mean abs diff
  4.19/255 — only the eyes changed); warmth 984k, copper 244k, yellow 108k,
  brightness/edge profile unchanged.
- `REBEE_FINAL_SHOWDOWN.png` = labeled before/after sheet for Aarav's eyes.

## 4. Why v6 wins the bonus points (the pitch, ready for the caption too)
1. **Theme relevance at a glance:** the frame IS the challenge — a drawer of
   dead phones/cables becoming a hero. Zero words needed.
2. **Emotional storytelling:** a child's wonder at the moment of birth — the
   "authentic > polished" criterion, in an Indian home (relatable to the
   judging org and its audience).
3. **Character consistency:** same copper/yellow/green signature as all prior
   art — reads as ONE designed character, not AI slop (the consistency
   criterion).
4. **Craft:** warm golden light, god-rays, low hero angle, shallow DOF —
   poster-grade, thumbnail-legible.
5. **It literally illustrates the Q2 answer** ("hatched from an electronics
   drawer in Gurugram") — the form's own "inspired by the challenge" test.

## 5. Docs updated + committed
- `SUBMIT_REBEE.md`: Q4 default + link → `rebee_hero_v6_FINAL.png`; art bank
  note; Q4 description rewritten.
- `BUDDY_BRIEF.md`: v6 FINAL rationale paragraph (v3 = fallback, alternates listed).
- `REBEE_FINAL_SHOWDOWN.png` added for the before/after.

## Still waiting on user
- **SUBMISSION — deadline TOMORROW 12 Aug. Do it tonight.** Q1 = jpg, Q4 = v6_FINAL.
- Confirmation screenshot → M2 evidence album · posting proof · M2 dashboard · PH3 word.
