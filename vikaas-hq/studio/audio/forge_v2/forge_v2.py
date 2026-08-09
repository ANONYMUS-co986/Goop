#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TR_V2 — DRIFT-FORGE: re-forged phonk bed with REAL studio one-shots (v2 of the phonk beds).
Sources (rights-audited, see FORGE_SOURCES.md):
  - GareBear99/Phonk_Producer_Toolkit (GitHub, '100% free — commercial use allowed')
      Drift_Phonk_Pack_V3/Cowbells/Cowbell_{F,Ab,C,G}.wav  (key-matched F minor)
      Drift_Phonk_Pack_V3/808s/Drift808_F.wav + Drift808_Slide_F.wav
      DARKDOMAIN_Original_Cinematic_Pack/Riser_1.wav
  - Boochi44/free-drum-samples (CC0 1.0; provenance: TR-808 samples by Edward Loveall, CC0)
      01-hard-trap: hard-kick-01, hard-snare-01, hi-hat-closed-01, open-hat-01, perc-rimshot
Design: 138 BPM, F minor, 16 bars (~27.8s loop), halftime drift skeleton:
  kick {0,14} (+{6,11} pumps later), snare on 8, hats rolling 16ths w/ swing + bar-end rolls,
  cowbell minor riff (F/Ab/C/G) = the genre signature, 808 root + slide into drop,
  sidechain duck under kick, tanh glue drive, master to -16.0 LUFS, limiter 0.89 peak.
Output: TR_V2_DRIFTFORGE_138_M17.wav + TR_V2_preview.mp3 (192k) in studio/audio/forge_v2/."""
import numpy as np, soundfile as sf, subprocess, os, glob

SR   = 44100
BPM  = 138.0
STEP = 60.0 / BPM / 4.0          # 16th
BAR  = 16 * STEP
BARS = 16
N    = int(BARS * BAR * SR) + SR

GB = "/tmp/phonk2/Phonk_Producer_Toolkit-main"
BO = "/tmp/phonk2/free-drum-samples-main/drum-samples/01-hard-trap"
OUTDIR = "/home/user/Goop/vikaas-hq/studio/audio/forge_v2"
os.makedirs(OUTDIR, exist_ok=True)
FF = glob.glob("/home/user/.studio_venv/lib/python*/site-packages/imageio_ffmpeg/binaries/ffmpeg*")[0]

def load(path, trim=None):
    x, sr0 = sf.read(path, dtype="float32", always_2d=True)
    x = x[:, 0]
    if sr0 != SR:
        t_old = np.arange(len(x)) / sr0
        x = np.interp(np.arange(0, t_old[-1], 1 / SR), t_old, x).astype(np.float32)
    if trim and len(x) > int(trim * SR):
        x = x[: int(trim * SR)]
    return x

CB = {n: load(f"{GB}/Drift_Phonk_Pack_V3/Cowbells/Cowbell_{n}.wav") for n in "F Ab C G".split()}
B808   = load(f"{GB}/Drift_Phonk_Pack_V3/808s/Drift808_F.wav")
SLIDE  = load(f"{GB}/Drift_Phonk_Pack_V3/808s/Drift808_Slide_F.wav")
KICK   = load(f"{BO}/kicks/hard-kick-01.wav")
SNARE  = load(f"{BO}/snares/hard-snare-01.wav")
RIM    = load(f"{BO}/percs/perc-rimshot.wav")
HAT    = load(f"{BO}/hi-hats/hi-hat-closed-01.wav", trim=0.12)
OHAT   = load(f"{BO}/open-hats/open-hat-01.wav", trim=0.6)
RISER  = load(f"{GB}/DARKDOMAIN_Original_Cinematic_Pack/Riser_1.wav")

tracks = {k: np.zeros(N, np.float32) for k in "bells b808 kick snare hats fx".split()}
kicks_at = []

def fade_tail(x, ms=25):
    n = int(ms / 1000 * SR)
    if len(x) > n: x[-n:] *= np.linspace(1, 0, n)
    return x

def put(tr, smp, t, gain=1.0, maxlen=None):
    i = int(t * SR)
    s = smp if maxlen is None else fade_tail(smp[: int(maxlen * SR)].copy())
    j = min(i + len(s), N)
    if i < N: tracks[tr][i:j] += s[: j - i] * gain

ACC = [1.0, .55, .7, .55, .85, .55, .7, .55, .95, .55, .7, .55, .85, .55, .7, .6]
riffA = {0: "F", 3: "F", 6: "Ab", 8: "F", 11: "C", 14: "Ab"}
riffB = {0: "F", 3: "Ab", 6: "F", 8: "C", 11: "F", 13: "G", 14: "Ab"}

for bar in range(BARS):
    t0 = bar * BAR
    phase = 0 if bar < 2 else (1 if bar < 12 else 2)     # intro / main / drop
    riff = riffA if bar % 2 == 0 else riffB
    # cowbell riff (teased in intro at half gain, full after)
    for st, note in riff.items():
        put("bells", CB[note], t0 + st * STEP, (0.55 if phase == 0 else 0.8 if phase == 1 else 0.88))
    if phase >= 1:
        ks = [0, 14] + ([6, 11] if phase == 2 or bar % 2 == 1 else [])
        for st in ks:
            put("kick", KICK, t0 + st * STEP, 1.0); kicks_at.append(t0 + st * STEP)
        put("snare", SNARE, t0 + 8 * STEP, 0.95)
        put("snare", RIM,   t0 + 8 * STEP, 0.5)
        if phase == 2 or bar % 2 == 1:
            put("snare", RIM, t0 + 15 * STEP, 0.4)      # ghost rim
        for st in range(16):                             # rolling hats + swing
            tt = t0 + st * STEP + (STEP * 0.06 if st % 2 == 0 else 0)
            put("hats", HAT, tt, 0.34 * ACC[st])
        if bar % 2 == 1: put("hats", OHAT, t0 + 14 * STEP, 0.3)
        if bar in (7, 11, 15):                           # 32nd roll into next bar
            for k in (0.0, 0.5): put("hats", HAT, t0 + (15 + k) * STEP, 0.42)
        put("b808", B808, t0, 0.95, maxlen=BAR * 0.5 - 0.03)
        put("b808", B808, t0 + 8 * STEP, 0.9, maxlen=BAR * 0.5 - 0.03)
        if bar in (13, 15):
            put("b808", SLIDE, t0 + 12 * STEP, 0.9, maxlen=BAR * 0.4)
    if bar == 11:                                        # riser into the last 4
        put("fx", RISER, t0, 0.5, maxlen=BAR * 1.05)

# sidechain: duck bells+808 under each kick (exp recovery)
for tk, depth, tau in (("bells", 0.30, 0.11), ("b808", 0.5, 0.13)):
    d = np.ones(N, np.float32)
    for t in kicks_at:
        i = int(t * SR); j = min(i + int(0.5 * SR), N)
        d[i:j] = np.minimum(d[i:j], 1 - depth * np.exp(-(np.arange(j - i) / SR) / tau))
    tracks[tk] *= d

mix = (tracks["bells"] * 0.62 + tracks["b808"] * 0.9 + tracks["kick"] * 1.05 +
       tracks["snare"] * 0.8 + tracks["hats"] * 0.85 + tracks["fx"] * 0.9)
mix = np.tanh(mix * 1.35) * 0.95                          # glue drive
mix = mix[: int(BARS * BAR * SR)]                         # exact loop length
stereo = np.stack([mix, mix], axis=1)

import re
def lufs(path):
    """Integrated LUFS from the ebur128 SUMMARY block only (running t-lines also carry
    'I: x LUFS' — anchor to the 'Integrated loudness:' marker or we parse garbage)."""
    out = subprocess.run([FF, "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = out.split("Integrated loudness:")[-1]
    mm = re.search(r"I:\s*(-?[\d.]+)\s*LUFS", m)
    tp = re.search(r"Peak:\s*(-?[\d.]+)\s*dBFS", m)
    return (float(mm.group(1)) if mm else None), (float(tp.group(1)) if tp else None)

tmp = f"{OUTDIR}/_pass1.wav"; sf.write(tmp, stereo, SR)
l1, tp1 = lufs(tmp); gain_db = -16.0 - l1
g = 10 ** (gain_db / 20)
final = np.clip(stereo * g, -0.89, 0.89)                  # limiter ceiling
wav = f"{OUTDIR}/TR_V2_DRIFTFORGE_138_M17.wav"
sf.write(wav, final, SR, subtype="PCM_16"); os.remove(tmp)
l2, tp2 = lufs(wav)
peak = float(np.abs(final).max())
subprocess.run([FF, "-y", "-v", "error", "-i", wav, "-codec:a", "libmp3lame", "-b:a", "192k",
                f"{OUTDIR}/TR_V2_preview.mp3"])
subprocess.run([FF, "-y", "-v", "error", "-i", wav, "-lavfi",
                "showspectrumpic=s=1200x360:legend=1", f"{OUTDIR}/qc_spec_v2.png"])
dur = len(final) / SR
print(f"pass1={l1} LUFS (TP {tp1} dBFS) -> gain {gain_db:+.2f} dB -> FINAL: {l2} LUFS (TP {tp2} dBFS) | sample-peak {peak:.3f} | {dur:.2f}s | kicks={len(kicks_at)}")
print("master:", wav)
