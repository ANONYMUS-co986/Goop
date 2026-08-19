#!/usr/bin/env bash
# ============================================================
# VIKAAS BRIEF TRANSCRIBER — run THIS on YOUR laptop/phone
# (your internet can download models; the sandbox can't)
# 1) puts the 3 brief mp3s in ./briefs/
# 2) runs faster-whisper (auto-downloads the model from HF)
# 3) writes transcripts/*.txt
# 4) commit the transcripts back to repo main → I read them.
# ============================================================
set -e
echo "=== VIKAAS BRIEF TRANSCRIBER ==="
mkdir -p briefs transcripts
echo "→ Put the 3 mp3s in ./briefs/ (you already have them)"
echo "→ Installing faster-whisper..."
pip install -q faster-whisper 2>/dev/null || pip3 install -q faster-whisper

python3 - <<'PY'
import os, glob
from faster_whisper import WhisperModel
print("Downloading whisper 'small' model (first run, ~460MB)...")
print("(If slow, edit this file: model_size='tiny' for ~75MB)")
model = WhisperModel("small", device="cpu", compute_type="int8")
for f in sorted(glob.glob("briefs/*.mp3")):
    name = os.path.basename(f).replace(".mp3", "")
    print(f"Transcribing {name}...")
    segments, info = model.transcribe(f, language="en")
    lines = [f"[{s.start:.1f}-{s.end:.1f}] {s.text}" for s in segments]
    txt = "\n".join(lines)
    open(f"transcripts/{name}.txt", "w").write(txt)
    print(f"  ✓ transcripts/{name}.txt ({len(txt)} chars)")
print("DONE — now: git add transcripts && git commit && git push")
print("(or just send me the .txt files)")
PY
