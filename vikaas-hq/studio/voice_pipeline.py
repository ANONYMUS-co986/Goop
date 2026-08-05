#!/usr/bin/env python3
"""
VIKAAS — HINDI VOICE PIPELINE (run on YOUR machine — any laptop, 5 minutes)
===========================================================================
Arena's sandbox can't download model weights (every model CDN is firewalled
there — verified). Your laptop's internet is open, so this script does the
whole job locally: downloads a proper open-source Hindi voice, speaks all 8
comedy lines WITH per-character emotion presets, and writes mp3-ready wavs.
Then send the vo_out/ files back to Arena — Aarav's agent mixes & re-encodes.

TWO MODES
  --piper   (RECOMMENDED) native Hindi voices प्रथम(m) + प्रीयम्वादा(f),
            Rhasspy Piper, MIT, runs on CPU, ~63MB, REAL Hindi + emotion knobs.
  --kokoro  Kokoro-82M v1.0 (hexgrad), Apache-2.0 code, CPU, very natural
            global voice, Hindi accent is "good" not "native". ~310MB.

USAGE (mac/linux)                       USAGE (windows powershell)
  python3 -m venv tt                    py -m venv tt
  source tt/bin/activate                tt\\Scripts\\activate
  pip install piper-tts kokoro-onnx     pip install piper-tts kokoro-onnx ^
      soundfile requests                    soundfile requests
  python voice_pipeline.py --piper      python voice_pipeline.py --piper

Output: vo_out/vo1_pov.wav ... vo_out/vo8_finale.wav  (+ a _REPORT.txt)
"""
import os, sys, argparse, urllib.request, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "vo_out")

# ---------- the 8 comedy lines (edit freely — filenames stay stable) ----------
LINES = {
    "vo1_pov":      "पी ओ वी — तुम घर का इकलौता ई-वेस्ट वॉरियर हो।",
    "vo2_mummy":    "मम्मी बोलीं — वो चार्जर मत फेंकना। कभी काम आएगा।",
    "vo3_narrator1": "नरेटर — वो चार्जर दो हज़ार चौदह से एक बार भी काम नहीं आया।",
    "vo4_papa":     "पापा बोले — पुराने फ़ोन में सोना होता है बेटा।",
    "vo5_narrator2": "नरेटर — तक़रीबन शून्य दशमलव शून्य तीन ग्राम सोना। रास्ते की चिंगम भी महँगी है।",
    "vo6_calc":     "रिसाइक्लर बोला — मिनिमम पाँच सौ किलो। मेरे पास — सवा किलो। शॉर्ट — सिर्फ़ चार सौ अट्ठानबे दशमलव छह किलो।",
    "vo7_kabadi":   "और कबाड़ीवाले ने बोला — पूरी तिजोरी के चालीस रुपये।",
    "vo8_finale":   "अच्छा। हँसी ख़त्म। अब अपना ड्रॉर खोलो।",
}

# ---------- emotion casting ----------
# Piper: length_scale (>1 = slower/graver), noise_scale (pitch variance),
#        noise_w (duration breathiness), sentence_silence (the em-dash BEATS)
PIPER_CAST = {
    "vo1_pov":      dict(voice="pratham",    length_scale=1.00, noise_scale=0.70, noise_w=0.75, sentence_silence=0.30),
    "vo2_mummy":    dict(voice="priyamvada", length_scale=1.02, noise_scale=0.75, noise_w=0.80, sentence_silence=0.30),
    "vo3_narrator1": dict(voice="pratham",   length_scale=1.12, noise_scale=0.62, noise_w=0.70, sentence_silence=0.40),  # grave deadpan
    "vo4_papa":     dict(voice="pratham",    length_scale=1.04, noise_scale=0.80, noise_w=0.80, sentence_silence=0.35),  # confident economist
    "vo5_narrator2": dict(voice="pratham",   length_scale=1.10, noise_scale=0.62, noise_w=0.70, sentence_silence=0.40),
    "vo6_calc":     dict(voice="pratham",    length_scale=1.04, noise_scale=0.60, noise_w=0.68, sentence_silence=0.30),  # tight/crisp for math
    "vo7_kabadi":   dict(voice="pratham",    length_scale=0.94, noise_scale=0.85, noise_w=0.85, sentence_silence=0.25),  # faster, gruffer
    "vo8_finale":   dict(voice="pratham",    length_scale=1.10, noise_scale=0.66, noise_w=0.72, sentence_silence=0.35),
}
# Kokoro voices: hm_omega/hm_psi (male hi), hf_alpha/hf_beta (female hi)
KOKORO_CAST = {
    "vo1_pov":      dict(voice="hm_omega", speed=0.98),
    "vo2_mummy":    dict(voice="hf_alpha", speed=1.00),
    "vo3_narrator1": dict(voice="hm_omega", speed=0.94),
    "vo4_papa":     dict(voice="hm_psi", speed=1.00),
    "vo5_narrator2": dict(voice="hm_omega", speed=0.94),
    "vo6_calc":     dict(voice="hm_omega", speed=0.97),
    "vo7_kabadi":   dict(voice="hm_psi", speed=1.05),
    "vo8_finale":   dict(voice="hm_omega", speed=0.95),
}

PIPER_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hi/hi_IN/{v}/medium/hi_IN-{v}-medium.onnx"
PIPER_CFG  = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/hi/hi_IN/{v}/medium/hi_IN-{v}-medium.onnx.json?download=true.json"
KOKORO_MODEL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
KOKORO_VOICES = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"


def fetch(url, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 500_000:
        print("  ✓ already have", os.path.basename(dst)); return dst
    print("  ↓ downloading", os.path.basename(dst), "...")
    with urllib.request.urlopen(url) as r, open(dst, "wb") as f:
        shutil.copyfileobj(r, f)
    print("  ✓", os.path.basename(dst), f"{os.path.getsize(dst)//1048576} MB")
    return dst


def run_piper():
    from piper import PiperVoice
    try:
        from piper import SynthesisConfig
    except ImportError:
        from piper.config import SynthesisConfig
    os.makedirs(OUT, exist_ok=True)
    voices = {}
    report = ["VIKAAS piper run — send all wavs to Arena chat", ""]
    need = sorted({c["voice"] for c in PIPER_CAST.values()})
    for vname in need:
        m = fetch(PIPER_BASE.format(v=vname), os.path.join(HERE, f"hi_IN-{vname}-medium.onnx"))
        c = fetch(PIPER_CFG.format(v=vname),  os.path.join(HERE, f"hi_IN-{vname}-medium.onnx.json"))
        print("  loading", vname, "...")
        voices[vname] = PiperVoice.load(m, config_path=c)
    for name, text in LINES.items():
        cast = PIPER_CAST[name]
        voice = voices[cast["voice"]]
        cfg = SynthesisConfig(
            length_scale=cast["length_scale"],
            noise_scale=cast["noise_scale"],
            noise_w=cast["noise_w"],
            sentence_silence=cast["sentence_silence"],
        )
        wav_path = os.path.join(OUT, f"{name}.wav")
        with open(wav_path, "wb") as wf:
            voice.synthesize_wav(text, wf, syn_config=cfg)
        print(f"  ✓ {name} [{cast['voice']}] -> {wav_path}")
        report.append(f"{name}: voice={cast['voice']} len={cast['length_scale']} :: {text}")
    with open(os.path.join(OUT, "_REPORT.txt"), "w") as f:
        f.write("\n".join(report))
    print("\nDONE. Zip vo_out/ and send it to the Arena chat.")


def run_kokoro():
    from kokoro_onnx import Kokoro
    os.makedirs(OUT, exist_ok=True)
    model = fetch(KOKORO_MODEL, os.path.join(HERE, "kokoro-v1.0.onnx"))
    vbin  = fetch(KOKORO_VOICES, os.path.join(HERE, "voices-v1.0.bin"))
    k = Kokoro(model, vbin)
    for name, text in LINES.items():
        cast = KOKORO_CAST[name]
        samples, sr = k.create(text, voice=cast["voice"], speed=cast["speed"], lang="hi")
        wav_path = os.path.join(OUT, f"{name}.wav")
        try:
            import soundfile as sf
            sf.write(wav_path, samples, sr)
        except ImportError:
            import wave, struct
            with wave.open(wav_path, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
                import numpy as np
                w.writeframes((np.clip(samples, -1, 1) * 32767).astype('<i2').tobytes())
        print(f"  ✓ {name} [{cast['voice']}] -> {wav_path}")
    print("\nDONE. Zip vo_out/ and send it to the Arena chat.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--piper", action="store_true")
    ap.add_argument("--kokoro", action="store_true")
    args = ap.parse_args()
    if not (args.piper or args.kokoro):
        print(__doc__); print("→ pick one: --piper (native Hindi) or --kokoro"); sys.exit(1)
    (run_piper if args.piper else run_kokoro)()
