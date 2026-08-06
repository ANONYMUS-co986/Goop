#!/usr/bin/env python3
"""BEAT FORGE — real drift-phonk arrangements from GareBear99/Phonk_Producer_Toolkit samples
(GitHub free pack, royalty-free). Track A: DRAWER DRIFT 128bpm Fmin. Track B: DOORSTEP DRIVE 138bpm Gmin.
Track C: COMMUNITY CUT (100% pack loops layered). Output: studio/audio/finale/*.wav"""
import numpy as np, soundfile as sf, os

SR = 44100
PACK = "/tmp/phonkpacks/Phonk_Producer_Toolkit/Drift_Phonk_Pack_V3"
GP   = "/tmp/phonkpacks/Phonk_Producer_Toolkit/GamePhonk"
OUT  = "/home/user/Goop/vikaas-hq/studio/audio/finale"
os.makedirs(OUT, exist_ok=True)

def L(p):
    d, sr = sf.read(p, dtype="float32", always_2d=True)
    assert sr == SR, p
    return d.mean(axis=1)

KICK   = L(f"{PACK}/Drums/Kicks/Kick_1.wav")
HOUSEK = L(f"{PACK}/Drums/Kicks/HouseKick_1.wav")
SNARE  = L(f"{PACK}/Drums/Snares/Snare_1.wav")
SNARE2 = L(f"{PACK}/Drums/Snares/Snare_2.wav")
CLAP   = L(f"{PACK}/Drums/Claps/Clap_1.wav")
HAT    = L(f"{PACK}/Drums/HiHats/Hat_1.wav")
D808F  = L(f"{PACK}/808s/Drift808_F.wav")
D808C  = L(f"{PACK}/808s/Drift808_C.wav")
D808G  = L(f"{PACK}/808s/Drift808_G.wav")
SLIDEF = L(f"{PACK}/808s/Drift808_Slide_F.wav")
SLIDEG = L(f"{PACK}/808s/Drift808_Slide_G.wav")
RISER  = L(f"{PACK}/FX/PhonkRiser.wav")
SCREECH= L(f"{PACK}/FX/TireScreech.wav")
VINYL  = L(f"{PACK}/FX/VinylNoiseLoop.wav")
def CB(root, octv): return L(f"{PACK}/Cowbells_Fminor/Cowbell_{root}_{octv}.wav")

def tile(sig, n):
    reps = int(np.ceil(n / len(sig)))
    return np.tile(sig, reps)[:n]

class Track:
    def __init__(self, secs):
        self.n = int(secs * SR)
        self.mix = np.zeros(self.n, np.float32)
        self.duck_me = []         # stems that receive sidechain
    def put(self, sig, t, g=1.0, stem=None):
        i = int(t * SR); j = min(self.n, i + len(sig))
        if i >= self.n: return
        seg = sig[:j - i] * g
        target = self.mix if stem is None else stem
        target[i:i + len(seg)] += seg
    def duck_env(self, kicks, floor=0.35, hold=0.06, rel=0.18):
        env = np.ones(self.n, np.float32)
        for t in kicks:
            i0 = int(t * SR); i1 = min(self.n, i0 + int((hold + rel) * SR))
            a = i0 + int(0.03 * SR)
            seg = np.arange(i1 - i0) / SR
            e = np.ones(i1 - i0, np.float32)
            for k, s in enumerate(seg):
                if s < 0.03: e[k] = 1 - (1 - floor) * (s / 0.03)
                elif s < 0.03 + hold: e[k] = floor
                else: e[k] = floor + (1 - floor) * ((s - 0.03 - hold) / rel)
            env[i0:i1] = np.minimum(env[i0:i1], e)
        return env

def softclip(x, drive=1.5):
    return np.tanh(x * drive) / np.tanh(drive)

def finish(tr, name, drive=1.5, out=None):
    mix = tr.mix
    for st in tr.duck_me: mix = mix + st
    mix = softclip(mix, drive)
    peak = np.abs(mix).max()
    if peak > 0: mix *= 0.92 / peak
    p = f"{OUT}/{name}.wav"
    sf.write(p, mix, SR)
    print("wrote", p, f"{len(mix)/SR:.2f}s peak-ok")

# ============ TRACK A — DRAWER DRIFT 128bpm Fmin ============
def track_a():
    bpm, bars = 128, 16
    bar = 60 / bpm * 4
    t16 = bar / 16
    tr = Track(bars * bar)
    s808 = np.zeros(tr.n, np.float32)
    bells = np.zeros(tr.n, np.float32)
    kicks = []
    for b in range(bars):
        t0 = b * bar
        in_drop = 4 <= b < 12 or 14 <= b < 16
        # kicks: quarter 1 & 3; extra ghost on drop
        for q in ([0, 8, 10, 12] if in_drop else [0, 8]):
            kt = t0 + q * t16
            tr.put(KICK if not (q == 10) else HOUSEK, kt, 1.0 if q != 10 else 0.55)
            kicks.append(kt)
        # snare halftime on beat 3 + clap
        if b >= 1:
            tr.put(SNARE, t0 + 8 * t16, 0.95)
            tr.put(CLAP,  t0 + 8 * t16, 0.45)
        # hats: 16ths w/ velocity, triplet roll at bar end (every 2 bars)
        for s in range(16):
            v = [0.7, 0.3, 0.5, 0.3][s % 4]
            if not in_drop and s in (10, 11, 13, 14, 15): v *= 0.6
            tr.put(HAT, t0 + s * t16, v * 0.55)
        if b % 2 == 1:  # triplet roll last beat
            for k in range(3):
                tr.put(HAT, t0 + 12 * t16 + k * (bar / 12), 0.5 + 0.15 * k)
        # 808: root per 2-bar cell: F F C G cycle on drop; single F drone elsewhere
        root = [D808F, D808C, D808F, D808G][(b // 2) % 4] if in_drop else D808F
        gain = 0.95 if in_drop else 0.5
        tr.put(root, t0, gain, stem=s808)
        if in_drop and b % 2 == 1:
            tr.put(SLIDEF if (b // 2) % 4 < 2 else SLIDEG, t0 + 12 * t16, 0.8, stem=s808)
        # cowbell riff
        riff = [(0, ('F', 2)), (3, ('F', 1)), (4, ('G', 1)), (7, ('Ab', 1))] if b % 2 == 0 else \
               [(0, ('C', 2)), (3, ('Ab', 1)), (4, ('G', 1)), (6, ('F', 2))]
        for e, (rt, oc) in riff:
            g = 0.9 if in_drop else 0.35
            if not in_drop and e in (3, 4): continue   # sparse intro
            tr.put(CB(rt, oc), t0 + e * t16 * 2, g, stem=bells)
            if in_drop: tr.put(CB(rt, min(oc + 1, 3)), t0 + e * t16 * 2, 0.28, stem=bells)
    # vinyl bed
    tr.mix += tile(VINYL, tr.n) * 0.05
    # dull the vinyl a touch (one-pole LP)
    # risers + screech at drop heads
    tr.put(RISER, 4 * bar - 2.5, 0.8)
    tr.put(SCREECH, 4 * bar + 0.02, 0.75)
    tr.put(RISER, 14 * bar - 2.5, 0.65)
    tr.put(SCREECH, 14 * bar + 0.02, 0.55)
    # sidechain
    env = tr.duck_env(kicks)
    s808 *= env; bells *= (0.75 + 0.25 * env)
    finish(tr, "TR_A_DRAWER_DRIFT_128")

# ============ TRACK B — DOORSTEP DRIVE 138bpm Gmin ============
def track_b():
    bpm, bars = 138, 12
    bar = 60 / bpm * 4
    t16 = bar / 16
    tr = Track(bars * bar)
    s808 = np.zeros(tr.n, np.float32)
    bells = np.zeros(tr.n, np.float32)
    kicks = []
    for b in range(bars):
        t0 = b * bar
        in_drop = 2 <= b < 10
        for q in ([0, 8, 10, 12] if in_drop else [0, 8]):
            kt = t0 + q * t16
            tr.put(KICK, kt, 1.0 if q in (0, 8) else 0.6)
            kicks.append(kt)
        if b >= 1:
            tr.put(SNARE2, t0 + 8 * t16, 0.95)
            tr.put(CLAP,   t0 + 8 * t16, 0.4)
        for s in range(16):
            v = [0.75, 0.3, 0.55, 0.3][s % 4]
            tr.put(HAT, t0 + s * t16, v * 0.55)
        if b % 2 == 1:
            for k in range(4):  # 32nd burst
                tr.put(HAT, t0 + 15 * t16 + k * (t16 / 4), 0.45 + 0.12 * k)
        root = [D808G, D808C, D808G, D808F][(b // 2) % 4] if in_drop else D808G
        gain = 0.95 if in_drop else 0.45
        tr.put(root, t0, gain, stem=s808)
        riff = [(0, ('G', 2)), (2, ('G', 1)), (4, ('Ab', 1)), (6, ('G', 1))] if b % 2 == 0 else \
               [(0, ('C', 2)), (2, ('Ab', 1)), (4, ('G', 2)), (6, ('F', 1))]
        for e, (rt, oc) in riff:
            g = 0.9 if in_drop else 0.3
            if not in_drop and e in (2, 6): continue
            tr.put(CB(rt, oc), t0 + e * t16 * 2, g, stem=bells)
    tr.mix += tile(VINYL, tr.n) * 0.05
    tr.put(RISER, 2 * bar - 2.0, 0.8)
    tr.put(SCREECH, 6 * bar - 1.3, 0.5)
    tr.put(RISER, 10 * bar - 2.0, 0.7)
    env = tr.duck_env(kicks)
    s808 *= env; bells *= (0.75 + 0.25 * env)
    finish(tr, "TR_B_DOORSTEP_DRIVE_138")

# ============ TRACK C — COMMUNITY CUT (pack loops layered) ============
def track_c():
    bar128 = 60 / 128 * 4
    from scipy.signal import resample_poly
    def loopfit(path):
        d = L(path)
        target = int(round(len(d) / SR / bar128) * bar128 * SR) or int(bar128 * SR)
        ratio = len(d) / target
        up_dn = (target, len(d))
        out = resample_poly(d, target, len(d))
        return out
    drums = loopfit(f"{GP}/Drum_Loops/DrumLoop_1.wav")
    bass  = loopfit(f"{GP}/Bass_Loops/BassLoop_1.wav")
    bells = loopfit(f"{GP}/Cowbell_Lead_Loops/CowbellLoop_1.wav")
    syn   = loopfit(f"{GP}/Synth_Loops/SynthLoop_1.wav")
    bars = 16
    tr = Track(bars * bar128)
    for b in range(bars):
        t0 = b * bar128
        tr.put(drums, t0, 1.0)
        if b >= 2: tr.put(bass, t0, 0.8)
        if b >= 4: tr.put(bells, t0, 0.75)
        if b >= 6: tr.put(syn, t0, 0.6)
    tr.mix += tile(VINYL, tr.n) * 0.045
    tr.put(SCREECH, 4 * bar128 + 0.03, 0.5)
    finish(tr, "TR_C_COMMUNITY_CUT_128")

track_a(); track_b(); track_c()
print("FORGE DONE")
