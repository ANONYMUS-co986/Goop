#!/usr/bin/env python3
"""VIKAAS STUDIO — trackgen.py
Pure-numpy audio synthesis. Three original loops, zero copyright risk:
  TR-B "TAPE AUDIT"      -> reel 2 (investigative, 92bpm, D minor, hiss+crackle)
  TR-E "DOORSTEP PHONK"  -> edit reel v2 (140bpm phonk, F# minor, memphis cowbell)
  TR-D "KABADI BOUNCE"   -> vid 4 comedy bed (100bpm oom-pah, slide-whistle gags + horn honks)
Output: 16-bit stereo wav 44.1k.
"""
import numpy as np, wave, sys, os

SR = 44100
TWO_PI = 2*np.pi

# ---------- primitives ----------
def note_hz(name):
    notes = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    n = name[:-1]; octv = int(name[-1])
    return 440.0 * 2 ** ((notes[n] + (octv-4)*12 - 9)/12)

def adsr(n, a, d, s, r, sr=SR):
    an, dn, rn = int(a*sr), int(d*sr), int(r*sr)
    sn = max(0, n-an-dn-rn)
    e = np.concatenate([
        np.linspace(0,1,an,endpoint=False),
        np.linspace(1,s,dn,endpoint=False),
        np.full(sn,s),
        np.linspace(s,0,rn) if rn else np.array([])])
    return e[:n]

def kick(n, f0=150, f1=48, hard=1.0):
    t = np.arange(n)/SR
    f = f1 + (f0-f1)*np.exp(-t*38)
    ph = np.cumsum(f)/SR*TWO_PI
    x = np.sin(ph) * np.exp(-t*11) * hard
    x += 0.6*np.sin(ph*2)*np.exp(-t*24)        # knock
    x += 0.25*np.sign(np.sin(ph))*0.4*np.exp(-t*90)  # click
    return x

def hat(n, open_=False, vel=1.0):
    t = np.arange(n)/SR
    x = np.random.randn(n)
    # crude highpass: difference
    x = np.diff(x, prepend=x[0])
    dec = np.exp(-t*(7 if open_ else 55))
    return x*dec*vel*0.5

def snare(n):
    t = np.arange(n)/SR
    x = np.random.randn(n)*np.exp(-t*18)*0.7
    x += np.sin(TWO_PI*182*t)*np.exp(-t*26)*0.6
    return x*0.8

def clap(n):
    t = np.arange(n)/SR
    x = np.zeros(n)
    for off in (0, 0.011, 0.023):
        o = int(off*SR)
        if o < n:
            b = np.random.randn(n-o)*np.exp(-np.arange(n-o)/SR*30)
            x[o:] += b
    return x*0.5

def cowbell(n, f=587, vel=1.0):
    t = np.arange(n)/SR
    x = (np.sign(np.sin(TWO_PI*f*t))*0.5 + np.sign(np.sin(TWO_PI*f*1.46*t))*0.5)
    x = np.tanh(x*2)
    return x*np.exp(-t*9)*vel*0.55

def tri(n, freq, vel=1.0, slide_to=None, vib=0.0, vib_hz=5.0):
    t = np.arange(n)/SR
    if slide_to:
        f = freq + (slide_to-freq)*(np.clip(t/t[-1],0,1)**1.5)
    else:
        f = np.full(n,freq)
    if vib: f = f*(1+vib*np.sin(TWO_PI*vib_hz*t))
    ph = np.cumsum(f)/SR*TWO_PI
    x = 2*np.abs(2*(ph/(TWO_PI)%1)-1)-1   # triangle
    return x*adsr(n,.01,.08,.75,.08)*vel*0.7

def saw_pad(n, freq, vel=1.0, detune_cents=(0,7,-7), attack=.4):
    t = np.arange(n)/SR
    x = np.zeros(n)
    for dc in detune_cents:
        f = freq*2**(dc/1200)
        ph = np.cumsum(np.full(n,f))/SR*TWO_PI
        x += ((ph/TWO_PI)%1)*2-1
    x /= len(detune_cents)
    e = adsr(n, attack, attack*0.5, .8, attack)
    return x*e*vel*0.28

def bass808(n, freq, vel=1.0, boom=1.0):
    t = np.arange(n)/SR
    x = np.sin(TWO_PI*freq*t)*np.exp(-t*3.2)
    x = np.tanh(x*3.5)*boom
    x += 0.3*np.sin(TWO_PI*freq*0.5*t)*np.exp(-t*2.4)
    return x*vel*0.8

def slide_whistle(n, f0=900, f1=1500, down=False, vel=1.0):
    t = np.arange(n)/SR
    f = np.linspace(f0,f1,n) if not down else np.linspace(f1,f0,n)
    ph = np.cumsum(f)/SR*TWO_PI
    x = np.sin(ph)*0.8 + 0.25*np.sin(2*ph)
    return x*adsr(n,.03,.1,.8,.1)*vel*0.5

def honk(n, vel=1.0):
    t = np.arange(n)/SR
    f = 620
    x = (np.sign(np.sin(TWO_PI*f*t))*0.6 + np.sign(np.sin(TWO_PI*f*1.5*t))*0.4)
    x = np.tanh(x*1.8)
    gate = (np.sin(TWO_PI*2.5*t)>0).astype(float)   # pep-pep-pep
    return x*gate*np.exp(-t*3.5)*vel*0.5

def riser(n, vel=1.0):
    t = np.arange(n)/SR
    x = np.random.randn(n)
    x = np.convolve(x, np.ones(32)/32, mode='same')  # smooth LP-ish
    f = np.linspace(200, 4000, n)
    ph = np.cumsum(f)/SR*TWO_PI
    sw = np.sin(ph)*0.4
    e = np.linspace(0,1,n)**2
    return (x*0.4+sw)*e*vel*0.5

def lp(x, fc=1200):
    # one-pole lowpass
    a = np.exp(-TWO_PI*fc/SR)
    y = np.empty_like(x); acc=0
    for i in range(len(x)):
        acc = (1-a)*x[i] + a*acc
        y[i]=acc
    return y

def softlimit(x, drive=1.0, ceiling=0.94):
    x = np.tanh(x*drive)/(np.tanh(drive)*1.02)
    m = np.max(np.abs(x))+1e-9
    return x/m*ceiling

def reverb(x, mix=0.18, rt=0.9):
    # 4 feedback combs + 2 allpass (Schroeder)
    combs = [(int(0.0297*SR),0.74),(int(0.0371*SR),0.72),(int(0.0411*SR),0.71),(int(0.0437*SR),0.70)]
    wet = np.zeros_like(x)
    for d,g in combs:
        y = np.zeros_like(x)
        y[:d] = x[:d]
        y[d:] = x[d:] + g*y[:-d]
        wet += y
    wet /= len(combs)
    for d in (int(0.005*SR), int(0.0017*SR)):
        g=0.5
        y = np.zeros_like(wet)
        y[:d] = wet[:d]*-g
        y[d:] = wet[d:]*-g + wet[:-d] + g*y[:-d]
        wet = y
    return x*(1-mix) + wet*mix

def sidechain_pump(n, beat, depth=0.45, sr=SR):
    e = np.ones(n)
    start = int(beat*sr)
    klen = int(beat*sr)
    shape = 1 - depth*np.exp(-np.arange(klen)/(0.09*sr))
    for s in range(start, n, klen):
        e[s:s+klen] *= shape[:max(0,min(klen,n-s))]
    return e

def to_stereo(x, width=0.15):
    d = int(0.012*SR)
    r = np.concatenate([np.zeros(d), x[:-d]]) if len(x)>d else x.copy()
    l = x*(1-width*0.2); r = r*(1+width*0.2)
    st = np.stack([l*0.95+r*0.05, r*0.95+l*0.05], axis=1)
    return st

def write_wav(path, st):
    st = np.clip(st,-1,1)
    with wave.open(path,'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st*32767).astype('<i2').tobytes())

def tape_dress(x, hiss=0.006, crackle=0.012, flutter=0.04, flutter_hz=0.6):
    n = len(x); t = np.arange(n)/SR
    x = x + np.random.randn(n)*hiss
    # crackle pops
    pops = (np.random.rand(n) < 0.00006).astype(float)
    x = x + pops*np.random.randn(n)*crackle*12*np.exp(-np.arange(n)/(0.002*SR))
    fl = 1 + flutter*np.sin(TWO_PI*flutter_hz*t + 0.4*np.sin(TWO_PI*0.11*t))
    return x*fl

class Track:
    def __init__(self, dur, bpm):
        self.n = int(dur*SR); self.x = np.zeros(self.n); self.bpm=bpm
        self.beat = 60/bpm
    def put(self, y, at, gain=1.0):
        s = int(at*SR); e = min(self.n, s+len(y))
        if e>s: self.x[s:e] += y[:e-s]*gain
    def bar(self, i): return i*self.beat*4

# ================= TR-B TAPE AUDIT (26.8s, 92bpm, D minor) =================
def build_tape_audit(path):
    bpm=92; dur=26.8; T=Track(dur,bpm)
    # pads Dm: D-F-A swells each 2 bars
    for b in range(0, int(dur/ (T.bar(1))) ):
        root = 'D3' if b%2==0 else 'F3'
        for iv in (0,4,7):
            n_ = note_hz(root[0]+('#' if '#' in root else '')+str(int(root[-1])+ (0 if iv==0 else 0))) if False else None
        padroot = note_hz('D3' if b%2==0 else 'A2')
        pad = saw_pad(int(T.bar(2)*SR), padroot, vel=.9, attack=T.bar(1)*0.4)
        pad += saw_pad(int(T.bar(2)*SR), padroot*2**(4/12), vel=.5, attack=T.bar(1)*0.5)
        T.put(lp(pad, 900), b*T.bar(2))
    # clock ticks = 16th closed hats from bar 2
    start_b = 2*T.bar(1)
    for i in range(int((dur-start_b)/(T.beat/4))):
        t = start_b + i*T.beat/4
        T.put(hat(int(0.05*SR), vel=0.5 if i%4==0 else 0.25), t)
    # kick enters 4s (bar ~1.5) subdued 4-floor
    k = kick(int(0.35*SR), hard=0.9)
    b0 = 4.0
    i=0
    while b0 + i*T.beat*2 < dur-1.2:
        T.put(k, b0+i*T.beat*2, gain=0.8)
        i+=1
    # rim/snare every bar 3
    sn_ = snare(int(0.2*SR))
    b0 = 4.0 + 2*T.beat
    while b0 < dur-1.5:
        T.put(sn_*0.5, b0)
        b0 += T.bar(1)
    # bell arps D F A C every 2 bars
    arp_notes = ['D4','F4','A4','C5']
    b0 = 8.0
    while b0 < dur-2:
        for j,nn in enumerate(arp_notes):
            f = note_hz(nn)
            bell = tri(int(0.5*SR), f, vel=.5) + tri(int(0.5*SR), f*2, vel=.18)
            T.put(reverb(bell,0.4,0.6), b0+j*T.beat)
        b0 += T.bar(2)
    # bass drone D2 pulses
    d2 = note_hz('D2')
    b0 = 4.0
    while b0 < dur-1.6:
        bs = bass808(int(T.beat*1.6*SR), d2, vel=.5, boom=.7)
        T.put(bs, b0)
        b0 += T.bar(1)
    # outro LP sweep feel: amplitude fade + thins
    tail = int(2.2*SR)
    env = np.ones(T.n); env[-tail:] *= np.linspace(1,0,tail)**1.5
    x = T.x*env
    x = tape_dress(x)
    x = reverb(x, 0.16, 0.9)
    T.x = x
    st = to_stereo(softlimit(T.x, drive=1.1))
    write_wav(path, st)

# ================= TR-E DOORSTEP PHONK (23.0s, 140bpm, F# minor) =================
def build_doorstep_phonk(path):
    bpm=140; dur=23.0; T=Track(dur,bpm)
    b=T.beat
    mel = ['F#3','A3','C#4','B3','A3','F#3','E3','A3']   # memphis line, 8ths per bar*? use 8ths
    # cowbell lead: 8th notes, swung slightly
    barcount = int(dur/T.bar(1))
    for bar in range(1, barcount):   # enter after intro bar
        base = bar*T.bar(1)
        for i,note in enumerate(mel):
            tpos = base + i*b/2 + (b*0.06 if i%2 else 0)
            if i%4==3:  # accent slide
                cb = cowbell(int(0.34*SR), note_hz(note)*2, vel=1.0)
            else:
                cb = cowbell(int(0.24*SR), note_hz(n := note), vel=0.8 if note!='F#3' else 1.0)
            T.put(cb, tpos, gain=0.9)
        # octave stab on beat 4 every 2 bars
        if bar%2==1:
            T.put(cowbell(int(0.4*SR), note_hz('F#4'), vel=1.1), base+3*b)
    # 808 bass roots F#2/A2 pattern halves
    roots = ['F#2','A2']
    for bar in range(1, barcount):
        rt = note_hz(roots[bar%2])
        bs = bass808(int(T.bar(1)*SR), rt, vel=1.0, boom=1.0)
        T.put(bs, bar*T.bar(1), gain=0.9)
        # 16th stutters at bar end
        T.put(bass808(int(b*0.3*SR), rt*2, vel=.4, boom=.8), bar*T.bar(1)+3.5*b)
    # drums
    k = kick(int(0.3*SR), f0=170, f1=52, hard=1.2); k = np.tanh(k*2.2)
    sn = snare(int(0.22*SR))
    for bar in range(1, barcount):
        base=bar*T.bar(1)
        if bar%8!=7:  # bar-8 break (no kick)
            for i in range(4): T.put(k, base+i*b, gain=1.0)
        T.put(sn, base+2*b, gain=0.95)             # snare on 3 (halftime)
        if bar%2==1: T.put(clap(int(0.2*SR)), base+2*b, gain=0.4)
        for i in range(8):
            T.put(hat(int(0.05*SR), vel=0.8 if i%2 else 0.5), base+i*b/2)
        T.put(hat(int(0.3*SR), open_=True, vel=0.5), base+2.5*b)
        # 32nd roll bar end every 2
        if bar%2==0:
            for i in range(4):
                T.put(hat(int(0.04*SR), vel=0.25+i*0.15), base+3*b+i*b/8)
    # intro: filtered riser + first-hit kick
    T.put(riser(int(T.bar(1)*SR), 0.9), 0.0)
    T.put(k, T.bar(1)-b, gain=0.9)
    # tape saturation + slight smear
    x = np.tanh(T.x*1.9)
    x = tape_dress(x, hiss=0.004, crackle=0.0, flutter=0.02, flutter_hz=0.7)
    x = reverb(x, 0.12, 0.7)
    # drop tail
    tail=int(1.4*SR); env=np.ones(len(x)); env[-tail:]*=np.linspace(1,0,tail)
    x=x*env
    st = to_stereo(softlimit(x, drive=1.25))
    write_wav(path, st)

# ================= TR-D KABADI BOUNCE (29.0s, 100bpm, C) =================
def build_kabadi_bounce(path, gags=((0.15,"up"),(8.35,"down"),(16.5,"down"),(22.4,"boing"),(30.4,"honk"))):
    bpm=100; dur=41.0; T=Track(dur,bpm)
    b=T.beat
    barcount=int(dur/T.bar(1))
    C=note_hz('C3'); G=note_hz('G2')
    # oom-pah bass: root 1&3, fifth 2&4 (tuba-ish square)
    for bar in range(barcount):
        base=bar*T.bar(1)
        for i,f in enumerate((C,G,C,G)):
            tn = int(b*0.9*SR)
            t=np.arange(tn)/SR
            sq = np.sign(np.sin(TWO_PI*f*t))*0.5 + np.sign(np.sin(TWO_PI*f*0.5*t))*0.5
            sq = np.tanh(sq*1.6)*adsr(tn,.005,.1,.5,.12)
            T.put(sq*0.5, base+i*b)
    # rim clicks 2&4
    rim = np.diff(np.random.randn(int(0.03*SR)), prepend=0)*np.exp(-np.arange(int(0.03*SR))/(0.008*SR))
    for bar in range(barcount):
        base=bar*T.bar(1)
        T.put(rim*0.9, base+1*b); T.put(rim*1.2, base+3*b)
        T.put(clap(int(0.15*SR)), base+3*b, gain=0.35)
    # triangle lead: cheeky motif every 2 bars, varies
    motif = ['C4','E4','G4','E4','F4','E4','D4','C4']
    motif2 = ['A4','G4','F4','E4','D4','E4','C4','C4']
    for pair in range(barcount//2):
        base=pair*T.bar(2)
        m = motif if pair%2==0 else motif2
        for i,note in enumerate(m):
            f=note_hz(note)
            ln = tri(int(b*0.82*SR), f, vel=.6, vib=0.006 if i%3==2 else 0.0)
            T.put(ln, base + i*b*0.5 + (b*0.04 if i%2 else 0))
    # gags
    for t_,kind in gags:
        if kind=='up':    T.put(slide_whistle(int(0.6*SR), vel=1.1), t_)
        elif kind=='down':T.put(slide_whistle(int(0.55*SR), down=True, vel=1.1), t_)
        elif kind=='boing':
            tn=int(0.7*SR); t=np.arange(tn)/SR
            fr = 180*np.exp(-t*2.2)*(1+0.9*np.abs(np.sin(TWO_PI*7*t)))
            ph=np.cumsum(fr)/SR*TWO_PI
            T.put(np.sin(ph)*np.exp(-t*3.2)*0.5, t_)
        elif kind=='honk': T.put(honk(int(1.1*SR)), t_)
    x = tape_dress(T.x, hiss=0.003, crackle=0.004, flutter=0.015, flutter_hz=0.9)
    x = reverb(x, 0.12, 0.6)
    tail=int(1.6*SR); env=np.ones(len(x)); env[-tail:]*=np.linspace(1,0,tail)
    x=x*env
    st = to_stereo(softlimit(x,1.15))
    write_wav(path, st)

if __name__=='__main__':
    outdir = sys.argv[1] if len(sys.argv)>1 else '.'
    os.makedirs(outdir, exist_ok=True)
    build_tape_audit(os.path.join(outdir,'TR_B_tape-audit.wav')); print('TR_B ok')
    build_doorstep_phonk(os.path.join(outdir,'TR_E_doorstep-phonk.wav')); print('TR_E ok')
    build_kabadi_bounce(os.path.join(outdir,'TR_D_kabadi-bounce.wav')); print('TR_D ok')
