# LOGBOOK V22 — V4 COMEDY CLUB: EMOTION VO RE-DO (11 Aug 2026)

**Order from Aarav:** "the comedy one has VERY BAD audio — use your speech generator
to get EMOTION audio and replace it."

## What was wrong
V4 (VIKAAS_04_COMEDY-CLUB, 40.8s) shipped with edge-tts voices (v3 mix, V17) —
robotic flat delivery. User demanded real emotional voices from the in-sandbox
speech generator.

## The re-do
1. **Script recovered** from `colab_voice_gen.ipynb` Cell A: 8 Hindi lines + beat
   grid (onsets 1.0/4.5/8.35/12.9/16.5/22.4/30.2/37.0, rooms 3.3–10.4s).
2. **4 voices registered via add_voice** (auditioned with the ACTUAL script lines):
   voice-00 narrator (entertainment), voice-01 मम्मी (feminine), voice-02 पापा,
   voice-03 कबाड़ी (gruff).
3. **8 generate_speech clips** — PERFECT fit: 7/8 at atempo 1.000, vo5 at 1.071.
   Zero chipmunk, zero stretch. (Banked: auditioning with real lines + right
   use_case gets grid-native pacing.)
4. **`mix_emotion.sh`** (new): per-line chain (silence-trim→highpass→comp→3.2k
   presence→atempo→gain→adelay) over TR_D bed @0.38 with sidechain duck, master
   loudnorm −19 → then remux to pack standard.
5. **Gain-trimmed twice** to hit pack standard: volume 2.6dB → −16.7, then 3.2dB
   → **−16.1 EXACT** on both masters (banked: measure→trim→re-measure).

## QC battery (all PASS)
- Video stream **byte-identical** (h264 extracted from backup vs new: cmp OK) —
  100% audio-only surgery.
- Duration 40.80s preserved · **zero dropouts** (silencedetect −38dB/2.5s).
- Per-slot VO presence: all 8 windows RMS −19.0…−21.7 dB (healthy, consistent).
- MANIFEST resealed (new shas) → all OK.
- Backups of v3 masters: `/tmp/v4_backup/` (sha 54ca182b0a9f = V17 master).

## Files changed
- `drops/FINALE/videos/VIKAAS_04_COMEDY-CLUB.mp4` + `drops/FINAL_PACK/…` (both −16.1)
- `audio/MIX_D_EMO.m4a` (stem) · `audio/VO_EMO_preview.mp3` (ears) ·
  `audio/VO_EMO_AB_old-new.mp3` (old vs new A/B)
- `mix_emotion.sh` (new, reusable) · FINALE README row · MANIFEST.sha256

## Waiting on user
- 🎧 EAR VERDICT on `audio/VO_EMO_preview.mp3` (or the A/B). If one voice is off
  → regenerate just that line (voice_id already registered), re-run mix_emotion.sh.
- ReBee submission TONIGHT (deadline 12 Aug) · posting run (Anuj is 8 posts ahead).
