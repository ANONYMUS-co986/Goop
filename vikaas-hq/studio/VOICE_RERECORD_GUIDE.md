# VOICE RERECORD — kill the robot, get real emotion (10 minutes, zero installs)

**Why this exists:** the Arena speech generator's Hindi is wooden (you were right).
The sandbox here cannot reach any TTS/model server (verified: edge-tts endpoint, HuggingFace,
GitHub release assets — all TLS-blocked from inside). Your normal internet CAN, so the actual
voice generation happens on YOUR side, in 2 clicks, in a browser tab. No Python install needed.

## Route 1 — Google Colab (RECOMMENDED, easiest — works on your PHONE, ~5 min)
**Direct link (skip manual upload):**
`https://colab.research.google.com/github/ANONYMUS-co986/Goop/blob/arena/019fc480-goop/vikaas-hq/studio/colab_voice_gen.ipynb`
1. Open that link (Chrome on Android / Safari on iPhone) → **Sign in** (your Google account, stays with you).
2. Yellow trust banner → **"Run anyway"**.
3. Tap the round **▶️** on **Cell A** (edge-tts) → wait 1–3 min, screen ON, stay in tab (mobile browsers pause background tabs). It prints `✓ vo1_pov`…`✓ vo8_finale` + a fit-check table. Red errors? Tap ▶️ again; still red → screenshot → Arena.
4. Tap **▶️** on **Cell C** → `vo_out.zip` auto-downloads:
   - **Android:** Downloads folder / notification.
   - **iPhone:** Safari ⬇️ icon → Downloads → Files app (iCloud Drive → Downloads).
   - Nothing downloaded? Colab left sidebar 📁 folder icon → long-press `vo_out.zip` → Download.
5. Attach the zip in the Arena chat and send. (Skip Cell B unless asked — it's the optional OSS backup.)

**Desktop/laptop version of the same:** open colab.research.google.com → File → Open notebook →
GitHub tab → paste the file URL above → Run Cell A, then Cell C.

*(Optional Cell B = pure open-source Piper voices प्रथम/प्रीयम्वादा — runs fully offline; slightly
less glossy than edge-tts. Generate both if you want, I'll pick per line.)*

## Route 2 — your laptop directly (if you prefer local)
Repo already has the script: `vikaas-hq/studio/voice_pipeline.py` (pip install, one command —
header comment has copy-paste steps for mac/linux/windows).

## The 8 lines + the timing windows they must land in (VID 04)
| File | Beat at | Window | Character |
|------|--------|--------|-----------|
| vo1_pov | 1.00s | ≤3.5s | POV intro |
| vo2_mummy | 4.50s | ≤3.8s | मम्मी |
| vo3_narrator1 | 8.35s | ≤4.5s | grave narrator |
| vo4_papa | 12.90s | ≤3.6s | पापा |
| vo5_narrator2 | 16.50s | ≤5.9s | narrator + gold math |
| vo6_calc | 22.40s | ≤7.8s | recycler-vs-drawer math |
| vo7_kabadi | 30.20s | ≤6.8s | कबाड़ीवाला ₹40 |
| vo8_finale | 37.00s | ≤3.8s | mic-drop CTA |
The notebook prints a fit-check per line. If any says TIGHT, still send it — I can speed-fit ±8%
in the mix without chipmunking.

## What I do the moment the zip lands (nothing for you to do)
1. Mix: VO at ~1.3× over the kabadi-bounce bed at ~0.38×, per-line EQ/compression/room,
   em-dash beat drops on the gag timeline (slide-whistle at 8.35/16.5/22.4/30.4 stays).
2. Re-encode VID 04 master (re-render if the sandbox pruned the frames — costs me 8 min, not you).
3. Push `VIKAAS_04_COMEDY-CLUB.mp4` v3 + a comparison WAV so you can hear before/after, then the
   QC battery re-runs (LUFS/duration/glyph sheet).
4. You review in GitHub — if any single voice sounds off, regenerate just that one line (the
   notebook runs per-line in seconds) and I re-mix only that stem.

**Rules that don't move:** no account passwords, ever — Colab is YOUR Google login, stays with you.
The zip is the only thing that crosses.
