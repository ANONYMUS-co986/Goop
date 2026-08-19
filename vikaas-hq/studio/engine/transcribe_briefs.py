#!/usr/bin/env python3
"""transcribe_briefs.py — WINDOWS-FRIENDLY transcriber (also works on Mac/Linux).
Run:  python transcribe_briefs.py
Transcribes all mp3s in the briefs/ folder (../briefs relative to this file,
or ./briefs if you're in the repo root) using faster-whisper.
Writes transcripts/*.txt next to the briefs.
"""
import os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
# the mp3s live in vikaas-hq/briefs/ (two levels up from engine/)
BRIEFS = os.path.normpath(os.path.join(HERE, "..", "briefs"))
OUT = os.path.join(BRIEFS, "transcripts")
os.makedirs(OUT, exist_ok=True)

def main():
    print("=== VIKAAS BRIEF TRANSCRIBER (Windows OK) ===")
    print(f"Looking for mp3s in: {BRIEFS}")
    files = sorted(glob.glob(os.path.join(BRIEFS, "*.mp3")))
    if not files:
        print("No mp3s found. Check the folder above — the 3 briefs should be there.")
        print("If not: git pull, or copy your mp3s into vikaas-hq/briefs/")
        sys.exit(1)
    print(f"Found {len(files)} audio files.")

    print("\nInstalling faster-whisper (first run)...")
    import subprocess, sys as s
    subprocess.run([s.executable, "-m", "pip", "install", "-q", "faster-whisper"], check=False)

    from faster_whisper import WhisperModel
    print("Downloading whisper model ('small' ~460MB first run)...")
    print("(If slow/out-of-memory, edit this file: model_size = 'tiny')")
    model_size = "small"  # <-- change to "tiny" for a faster/75MB model
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    for f in files:
        name = os.path.basename(f).replace(".mp3", "")
        print(f"\nTranscribing {name} ({os.path.getsize(f)//1024} KB)...")
        segments, info = model.transcribe(f, language="en")
        lines = [f"[{seg.start:.1f}-{seg.end:.1f}] {seg.text}" for seg in segments]
        txt = "\n".join(lines)
        outp = os.path.join(OUT, name + ".txt")
        with open(outp, "w", encoding="utf-8") as fh:
            fh.write(txt)
        print(f"  ✓ saved: {outp} ({len(txt)} chars)")

    print("\nDONE — now send me the transcripts/ folder OR:")
    print("  git add vikaas-hq/briefs/transcripts && git commit -m briefs && git push")

if __name__ == "__main__":
    main()
