# LOGBOOK V17 — THE GREAT UNLOCK: main→sandbox channel PROVEN + V4 VO MIX DONE → 6/6 REELS FINAL (8 Aug 2026)

## The unlock (his frustration → the fix)
- User pushed 8 files to `main` (commit `82bc409` "Add files via upload") and said "fetch them from the git". DONE. `git fetch origin` → extracted all 8 to `/home/user/from_main/` (ephemeral). **The upload channel is now PROVEN both ways: he uploads to main → I fetch in seconds; I ship to `arena/019fc480-goop` → he downloads from GitHub.** Chat attachments STILL never reach the sandbox (4th confirmation); screenshots pasted inline DO arrive. New doctrine: **any file he wants me to touch → upload to main** (prefer .zip over .rar, see below).
- External file hosts (gofile/Drive) remain unreachable from my sandbox — network allowlist is GitHub/pypi/npm only. GitHub IS our file link.

## The 8 files decoded
1. **2 screenshots** (7 Aug 18:28) = cwcsubmission.in dashboard + F2 Flash Challenge #2 form. Confirmations: pledge ✓ Completed, MISSIONS PROGRESS **2/3**, tabs M1✓ F1✓ F2 active, deadline **12 Aug 2026**. Step-2 text: name / superpower / AI image; "inspired by the challenge you have chosen"; featured entries = page feature + **Bonus Points**.
2. **Welcome file.md** = the IBM SkillsBuild course he finished: *"Tech meets beauty: IBM & L'Oréal's partnership for sustainable cosmetics"* (AI foundation models for ingredient discovery, gen-AI formulation, waste reduction, personalization). Pop-quiz answers banked: Q1 "helps reduce pollution and protect ecosystems" · Q2 "generative AI" · Q3 = formulas + less waste + personalization. (Also points at "Make an Impact with AI" MDLPT-295, Fundamentals of Sustainability & Technology credential.)
3. **aarav Choudhary submission.pdf** = image-type PDF → extracted embedded full-res JPG (1079×1373): **his SkillsBuild completion screenshot — "Changemakers Learning Mission", Completed 2 of 2: Tech meets beauty ✅ 07 Aug + "Four ways AI can help tackle climate change | BBC" ✅ 07 Aug, Channel ID CNL_LCB_1785934317109 (exact match to the F2 form's required mission), owner Ruchi Khanna Arora (ruchi@onemoneb.org).** THIS IS THE Q1 UPLOAD. Exported to `vikaas-hq/cwc_buddy/q1_skillsbuild_completion.jpg` — upload that (or the PDF itself) at Q1.
4. **brain dmagae.rar** = his VERDE V3.0 chat export with a previous AI (504KB ESP32 master-engine saga — "be exactly like it or even better") + his 119KB prompt.txt (contains a Google Drive file ID — Drive still blocked from sandbox; if those Drive files matter → upload them to main as .zip). Style mirror noted: full-send, one-go, options-with-🚀. Skimmed; deep-read parked until he says it informs VERDE work.
5&6. **vo_out.zip + vo_out (1).zip** — THE VO WHODUNIT, CLOSED (see below).

## VO whodunit — final autopsy
- Both zips hold the same 8 edge-tts mp3s (vo1_pov..vo8_finale). Durations vs the design grid (rooms 3.3/3.6/7.6/4.9/5.7/10.4/6.6/4.6s):
  - `vo_out.zip` = the OLD slow set: atempo needed **1.28–1.78× on 4/8 lines** (chipmunk territory — exactly why we refused to ship it in V8).
  - `vo_out (1).zip` = the CORRECTED set: **5/8 lines at 1.000×**, worst line = mummy 1.355× (fast-scolding mummy = comedically legal). Correctly predicted in V10: the second download was the fix.
- V8's hypothesis confirmed by measurement. Case closed with receipts.

## V4 v3 MIXED + SHIPPED (the last open reel)
- Pre-flight: `frames_tmp/reD_v2` still intact (1224 frames @30) and PROVEN pixel-identical to the shipped FINALE V4 (mean abs diff 0.137/255 @f0300) → picture untouched, audio-only surgery.
- `bash mix_v3.sh /home/user/from_main/vo1 --encode` → per-line chain (silence-trim→highpass→comp→3.2k presence→tempo-fit→sidechain duck→loudnorm) → MIX_D_v3.m4a −19.2 LUFS → engine master −18.6 LUFS.
- **Bug family banked: ffmpeg `volume=2.6` = LINEAR (+8.3 dB!) → measured −11.9 LUFS (caught by always-measure rule). `volume=2.6dB` with the dB suffix is the correct form → −16.1 LUFS.** Rebuke to past self recorded; the remux recipe in all docs must carry the dB suffix.
- Manual remux to pack standard: `-c:v copy -af volume=2.6dB,alimiter=limit=0.89:level=false,aresample=44100 -ac 2 -ar 44100 -b:a 192k` → **−16.1 LUFS**, 40.80s, 1080×1920@30, h264 + aac stereo 44.1k 192k, faststart.
- QC: silencedetect @−38 dB/2.5s → **zero dropouts**. Both copies replaced (`drops/FINAL_PACK/` + `drops/FINALE/videos/`). New sha256 `54ca182b0a9f…` → `MANIFEST.sha256` resealed → **30/30 OK**. `README.md` table row updated (−19.6 → −16.1, "v3 VO mix DONE").
- **PACK STANDARD now: 01 −18.5 (ambient bed) · 02 −15.9 · 03 −18.4 (ambient) · 04 −16.1 · 05 −16.2 · 06 −16.0.** VO/beat reels live at ≈−16, ambient reels at ≈−18.5 by design.
- **ALL 6 REELS FINAL. THE FULL DROP (6 reels + 21 posts + 3 alt beds) IS COMPLETE — 30/30 VERIFIED.** Nothing left in the media pipeline's "waiting" column.
- Audio previews regenerated for his ears before posting V4: `studio/audio/VO3_preview.mp3` (full mix) + `VO3_AB_old-new.mp3` (4s old vs 4s new ×2).

## Crack notes (tooling)
- .rar defeated: apt no-root, github release-assets host blocked, 7za 16.02 (npm 7zip-bin) too old for this RAR5 → **node-unrar-js (WASM, pure JS) cracked it in one line.** Lesson → tell him: upload **.zip** next time, it opens natively.
- pypdf + rarfile installed to venv (ephemeral — re-install after any sandbox wipe; add to resurrect spell: `pip install pillow numpy imageio-ffmpeg soundfile scipy pypdf rarfile`).

## Buddy submission — HIS MOVE (deadline 12 Aug, 4 days)
- Q1 = `cwc_buddy/q1_skillsbuild_completion.jpg` (or the PDF from main) · Q2 = ReBee + one-liner (paste from BUDDY_BRIEF.md) · Q3 = superpower answer (BUDDY_BRIEF short/long) · Q4 = `art/rebee_hero_v2_challenger.png` · Confirm Submit → screenshot the confirmation back to me. Deadline buffer: do it TONIGHT, before the posting run.
- Mission-channel receipts perfect: same channel ID as the form demands; 2/2 items dated 07 Aug.

## Privacy flag (one-time, his call)
- `main` is a PUBLIC repo: the screenshots show his name/school/city + the skillsbuild org code; the PDF names him. He uploaded them knowingly — fine — but if he wants them gone after the buddy submission, delete from GitHub web (I keep working copies in our branch where needed).

## Still waiting on user
- Task-2 submission confirmation screenshot → log as M2 evidence.
- Posting launch proof (any post/reel) → start the 24h insights ritual.
- M2 dashboard screenshot when it unlocks.
- Portfolio PH3 green light.
