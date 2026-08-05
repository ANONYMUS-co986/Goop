# QC REPORT — FINAL PACK (2026-08-05)

Every master below passed the full battery **after** this folder was assembled. Receipts included.
Visual proof: `qc_all5_contact_sheet.png` (4 frames/video, timestamped 15/38/62/85%).

## 1 · Audio identity check — all 5 DIFFERENT
Decoded each file's audio (mono 22.05 kHz wav) → md5 + integrated loudness + spectral centroid:

| File | LUFS (I) | Audio md5 | Spectral centroid | Verdict |
|------|----------|-----------|-------------------|---------|
| 01 | −18.5 | dc6c754f4a… | ~0.7 kHz (warm lo-fi) | ✓ unique |
| 02 | −18.2 | 915221c7ba… | ~4.6 kHz (bright synth) | ✓ unique |
| 03 | −18.4 | beae3f7d40… | bounce instrumental | ✓ unique |
| 04 | −19.6 | d75ed7a518… | ~2.9 kHz (speech + bed) | ✓ unique |
| 05 | −19.3 | 8ef833cb92… | ~4.8 kHz, highest flatness (perc) | ✓ unique |

Cross-correlation v. every candidate track (Thinking Music / TR-B / TR-D / TR-E / TR-F / comedy mixes)
confirmed each file carries its intended audio. Loudness spread 1.4 LU — consistent in-app feel.

## 2 · Bugs caught & fixed during this QC pass
1. **03 carried the same music as 01** (corr 0.746 v. Thinking Music). → Re-built from `trackgen.py`
   (`build_kabadi_bounce(gags=())` → `audio/TR_F_bounce-lite.wav`), windowed 4.8–20.2 s on the
   100 bpm bar grid, faded + loudnorm −16.5 LUFS, remuxed with video untouched. New corr: 0.80 v.
   TR-F family, 0.058 v. Thinking Music. ✅
2. **Devanagari tofu in 04** — dev text was inside Anton-only scopes (`.qcard .q`, `.nm`…), the
   `.dev` fallback lost every specificity fight → missing-glyph boxes. Fix: appended `'Devnag'`
   fallback to every `font-family` declaration in `reel_d.html` (and same prevention pass on
   `reel_e.html`/`reel_e2.html`). 04 fully re-rendered (1224 frames) + re-encoded with the
   identical VO mix (`MIX_D_v2.m4a` — audio md5 of final file unchanged = mix preserved). ✅
3. **03/05 shared two verbatim cards** ("HIS SCALE: AT MY GATE TOO." + plan chips). 03 re-cut:
   hook → "HE BUYS BOTTLES. PAPERS. WHOLE CYCLES. / EVERYTHING. EXCEPT MY DRAWER." and the
   close → dark-ink counter-plan ("1 DRAWER · 1.4 KG · GATE, DIRECT. — no middleman math").
   05 (flagship phonk edit) untouched. ✅

## 3 · Stream verification (all)
H.264 High yuv420p 1080×1920 (SAR 1:1) 30 fps + AAC-LC 96 kHz stereo ~164 kb/s · durations match
timelines (27.20 / 26.00 / 14.60 / 40.80 / 19.73 s) · no silent tracks · no missing video stream.

## Method receipts
Probe tool: `engine/probe.js` seeked-beat screenshots (font/layout) · `engine/lib.js render/encode`
· ffmpeg 7.0.2 static (ebur128, aspectralstats, afade/loudnorm) · md5 of decoded PCM as fingerprint.

## ADDENDUM (same day, full-branch audit)
Glyph-level audit extended to all 7 posts after the user challenged the inventory. Found real tofu on
p5/p6 (three-bug font family: CSS specificity; regex hole on declarations lacking generic family;
self-inflicted @font-face descriptor mangling). All 10 source HTMLs cleaned to single-name @font-face
+ per-glyph 'Devnag' fallbacks; all 7 posts + reels 03/04/05 re-baked; audio bitstreams preserved from
verified masters (-c:a copy). Post-fix proof: `drops/v4/posts/posts_final7_sheet.png` — every
Devanagari string live on P1/P3/P4/P5/P6/P7. Inventory cert: 5 videos (git history A-commits) + 7 posts
= 12 deliverables. No more, no less.
