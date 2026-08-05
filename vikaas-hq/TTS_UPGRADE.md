# TTS UPGRADE REPORT — Hindi voice with real emotion (2026-08-05)

## Verdict of the deep search (open-source landscape 2026)
| Model | Quality (MOS) | Hindi | Emotion | Can we run in OUR sandbox? |
|---|---|---|---|---|
| **AI4Bharat IndicF5** | 4.4 | ✅ native, best-in-class | strong | ❌ PyTorch+GPU ~6GB RAM (we have 2GB), weights on HuggingFace (blocked) |
| **Kokoro-82M v1.0** (hexgrad) | 4.5 | ✅ hf/hm voices | natural prosody | ⚠️ Code + deps installed ✅ (kokoro-onnx+onnxruntime+espeakng-loader), but **model 310MB + voices 26MB live on GitHub release-assets / HF — both firewalled here** |
| **IndicParler-TTS** | 4.1 | ✅ prompt-emotion tags | ✅ promptable | ❌ 880M params + HF |
| **Supertonic 3** (supertone-inc) | 4.2 | ✅ 31 langs | decent | ❌ weights HF only; repo ships no binaries |
| Piper (Indic) | 3.6 | ✅ rohan/madhur | flat | ❌ voices repo files blocked |
| **edge-tts** (MS neural, FREE, madhur/swara + mstts styles) | ~4.3 | ✅ excellent | ✅ styles | ❌ speech.platform.bing.com TLS-blocked in sandbox |
| Arena `generate_speech` (current) | 3.6 | ⚠️ robotic Hindi | flat-deadpan | ✅ WORKS — this is what V4 uses |

**Why the good ones failed here, exactly:** sandbox egress whitelist = github.com (git protocol + API) + npm/PyPI only. Model weights live on `huggingface.co`, `release-assets.githubusercontent.com`, `objects.githubusercontent.com`, `speech.platform.bing.com` — all refused at TLS. Git-LFS unusable; no repo commits 88–310MB models raw; npm `kokoro-js` bundles only voice bins and fetches `onnx-community/Kokoro-82M-v1.0-ONNX` from HF at runtime.

## Route A — LOCAL KOKORO RUN (10 min, proper Hindi) — RECOMMENDED
Everything except the two model files is already prepared; on your laptop the internet is open.

```bash
# any laptop/PC, Python 3.10+
python -m venv kokoro && kokoro/bin/pip install kokoro-onnx
# (on Windows use kokoro\Scripts\pip)
python - << 'EOF'
from kokoro_onnx import Kokoro
import soundfile as sf  # pip install soundfile
k = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")   # download these 2 from:
# github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
LINES = {
 "vo1_pov":      "पी ओ वी — तुम घर का इकलौता ई-वेस्ट वॉरियर हो।",
 "vo2_mummy":    "मम्मी बोलीं — वो चार्जर मत फेंकना। कभी काम आएगा।",
 "vo3_narrator1":"नरेटर — वो चार्जर दो हज़ार चौदह से एक बार भी काम नहीं आया।",
 "vo4_papa":     "पापा बोले — पुराने फ़ोन में सोना होता है बेटा।",
 "vo5_narrator2":"नरेटर — तक़रीबन शून्य दशमलव शून्य तीन ग्राम सोना। रास्ते की चिंगम भी महँगी है।",
 "vo6_calc":     "रिसाइक्लर बोला — मिनिमम पाँच सौ किलो। मेरे पास — सवा किलो। शॉर्ट — सिर्फ़ चार सौ अट्ठानबे दशमलव छह किलो।",
 "vo7_kabadi":   "और कबाड़ीवाले ने बोला — पूरी तिजोरी के चालीस रुपये।",
 "vo8_finale":   "अच्छा। हँसी ख़त्म। अब अपना ड्रॉर खोलो।",
}
for name, text in LINES.items():
    s, sr = k.create(text, voice="hm_omega", speed=0.96, lang="hi")
    sf.write(f"{name}.wav", s, sr); print(name, "ok")
EOF
```
Then send me the 8 wavs — I re-mix (bed @0.40, VO @1.35) and re-encode `04_REEL_comedy-club.mp4` without re-rendering frames. Voice options: `hf_alpha`/`hf_beta` (female), `hm_omega`/`hm_psi` (male). Slow 0.94–0.96 = gravitas.

## Route B — arena voice polish (already staged)
Generated 3 blind-taste variants of the narrator line:
- `studio/audio/testA_narration.mp3` — narration voice A (steadier, clearer phonemes)
- `studio/audio/testB_narration2.mp3` — narration voice B
- `studio/audio/testC_characters2.mp3` — characters voice C (more acted)
**Listen to all three, tell me which letter wins** → I regenerate all 8 clips with that voice + warmer mix (gentle EQ+room, slight slowdown) as comedy-club audio v2.

(And when Route A happens one day, that becomes audio v3 — final master.)
