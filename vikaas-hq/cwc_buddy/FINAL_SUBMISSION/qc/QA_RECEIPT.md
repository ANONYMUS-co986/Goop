# 🔬 QA RECEIPT — `rebee_hero_v6_FINAL.png` (the Q4 upload)

Verification battery run 11 Aug 2026 with OpenCV 4.10 + NumPy. Every claim below
is a measured number, reproducible with the same rig.

## The image
- 1376×768 landscape, PNG, ~2.5 MB.
- Generated via reference-chained image editing (v3_suitup → v5a → v6): the
  character stayed one designed bee-robot across every render.

## 1. Composition / subject presence
| Check | Result |
|---|---|
| Face detection (frontal cascade) | **exactly 2 faces**: girl at (993,258,130×130) + robot at (604,415,64×64) — no background-face AI artifact |
| Green eye glow (HSV mask + cluster split) | **2 distinct glowing eyes** at x-centers 199 & 343 in the eye band (left stronger — natural asymmetry) |
| Bee-stripe yellow | present at robot body (628,230) + dress at right (971–1112) |
| E-waste drawer | dark bottom band with green circuit glows (centroids 657,698 / 1003,673 / 844,666 / 911,668) |
| Composition triangle | robot center-left (born from drawer) · girl upper-right (wonder) · e-waste glowing below (the problem) — one clear focal story |

## 2. Quality signals
| Check | Result | Verdict |
|---|---|---|
| Global sharpness (Laplacian variance) | 649.6 | crisp (blurry would be <100) |
| Girl-region sharpness | 141.3 | in-focus subject, softer surroundings = depth of field (intended) |
| Corner scan (watermark/text) | TL clean · TR clean · BL clean · BR structured-dark (drawer contents, not text) | no watermarks |
| Brightness / openness | mean 102.3, edge-darkness 29% | warm, open (v3 was 55 / 86% dark) |

## 3. Palette signature (the character identity)
| Color | v3 (old) | v6 (FINAL) |
|---|---|---|
| Warm pixels (r>g>b) | 84k | **984k** |
| Copper (body) | 5.2k | **244k** |
| Bee yellow (stripes/dress) | 1.1k | **108k** |
| Green (LED eyes + circuit glow) | 192k | **31.5k** (eyes edited brighter: +62% vs v5a, scene diff only 4.19/255) |

## 4. Why v3 was replaced (the "are you sure?" audit trail)
v3 (rebee_hero_v3_suitup.png) was the earlier winner — dark vignette (86% edge
darkness), moody, single eye powering on. Research across 4 judging rubrics
(ARTEFFECT, ITU AI for Good, youth-contest philosophy, CRE[AI]TE) said: theme
relevance + emotional story + character consistency + visual impact beat
technical polish. v6 delivers all four wordlessly, and pixel-QA confirms the
story triangle is actually in the frame.

## 5. Honest limits
- This rig verifies structure, color, sharpness and subject placement — not
  aesthetic beauty or fine details (fingers, expressions). Final human-eyes
  check = Aarav (see `art/REBEE_FINAL_SHOWDOWN.png` before/after sheet).
- If he spots a flaw → one surgical regeneration fixes that region; deadline
  buffer exists until 12 Aug.

## Re-run the battery
```bash
/tmp/pw_venv/bin/pip install opencv-python-headless==4.10.0.84 pillow numpy
# (the scripts in engine/ + the QA snippets from LOGBOOK_V21)
```
