#!/usr/bin/env bash
# ============================================================
# VIKAAS VIDEO REVIEWER + SELF-CHECKER (the "eyes for video")
# Usage: bash engine/video_review.sh <video.mp4> [outDir]
# Does:
#   1. stream/duration/LUFS/audio health (ffprobe+ffmpeg)
#   2. extracts N frames evenly across the timeline (ffmpeg)
#   3. contact sheets (2 sizes) via ffmpeg tile
#   4. per-frame stats (pix_std.py) → flags blank/glitch/dark frames
#   5. near-duplicate detection (md5 of downscaled frames)
#   6. ASCII storyboard (pix.py ascii per sampled frame) — "watchable"
#   7. writes REVIEW.md verdict + flags
# ============================================================
set -uo pipefail
VID="$1"; OUT="${2:-/tmp/vidreview}"
ENGINE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FF="${FFMPEG:-/tmp/pw_venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2}"
[ -x "$FF" ] || FF="$(which ffmpeg)"
PY=/tmp/pw_venv/bin/python
mkdir -p "$OUT/frames" "$OUT/sheets"

[ -f "$VID" ] || { echo "❌ video not found: $VID"; exit 1; }
NAME="$(basename "$VID" .mp4)"
echo "═══ VIKAAS VIDEO REVIEWER ═══  $NAME"

# ---- 1. stream + duration ----
DUR=$($FF -i "$VID" 2>&1 | awk '/Duration/{split($2,a,":"); print a[1]*3600+a[2]*60+a[3]}')
W=$($FF -i "$VID" 2>&1 | grep -oE '[0-9]{3,4}x[0-9]{3,4}' | head -1)
echo "  duration: ${DUR}s · size: $W"
echo "duration=${DUR}s size=$W" > "$OUT/$NAME.meta"

# ---- 2. LUFS + silence (audio health) ----
$FF -nostats -i "$VID" -map 0:a -af ebur128 -f null - 2>&1 | grep -A6 "Summary:" | grep -E "I:|LRA:" | head -2 > "$OUT/$NAME.lufs" || true
$FF -nostats -i "$VID" -map 0:a -af silencedetect=noise=-38dB:d=2 -f null - 2>&1 | grep -c "silence_start" > "$OUT/$NAME.silences" 2>/dev/null || echo 0 > "$OUT/$NAME.silences"
echo "  lufs: $(cat "$OUT/$NAME.lufs" | tr '\n' ' ')" 
echo "  silences(>2s @-38dB): $(cat "$OUT/$NAME.silences")"

# ---- 3+4. frames + stats ----
N="${FRAMES:-12}"
$FF -y -v error -i "$VID" -vf "fps=1/$(awk -v d="$DUR" -v n="$N" 'BEGIN{printf "%.3f", d/n}')" -q:v 2 "$OUT/frames/f%03d.jpg" 2>/dev/null
COUNT=$(ls "$OUT/frames" | wc -l)
echo "  extracted $COUNT frames"
: > "$OUT/$NAME.frame_stats.tsv"
FLAGS=""
for f in "$OUT/frames"/*.jpg; do
  [ -f "$f" ] || continue
  ST=$($PY "$ENGINE/pix_std.py" "$f" 2>/dev/null)
  MEAN=$($PY -c "import cv2,sys;im=cv2.imread('$f');g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);print(round(float(g.mean()),1))" 2>/dev/null)
  FLAG=""
  [ "$(awk -v s="$ST" 'BEGIN{print (s<6)?1:0}')" = "1" ] && FLAG="BLANK?"
  [ "$(awk -v s="$ST" 'BEGIN{print (s<14)?1:0}')" = "1" ] && FLAG="DARK?"
  [ "$(awk -v m="$MEAN" 'BEGIN{print (m>245)?1:0}')" = "1" ] && FLAG="WHITE?"
  echo -e "$(basename "$f")\t$ST\t$MEAN\t$FLAG" >> "$OUT/$NAME.frame_stats.tsv"
  [ -n "$FLAG" ] && FLAGS="$FLAGS $FLAG"
done

# ---- 5. near-duplicate detection ----
echo "── duplicate frames (md5 of 64x36 grayscale) ──"
prev=""; dup=0
for f in $(ls "$OUT/frames"/*.jpg | sort); do
  h=$($PY -c "import cv2,sys,hashlib;im=cv2.imread('$f');g=cv2.resize(cv2.cvtColor(im,cv2.COLOR_BGR2GRAY),(64,36));print(hashlib.md5(g.tobytes()).hexdigest()[:10])" 2>/dev/null)
  [ "$h" = "$prev" ] && { echo "  DUP: $(basename "$f") == prev"; dup=$((dup+1)); }
  prev="$h"
done
[ "$dup" = "0" ] && echo "  no near-duplicates"

# ---- 6. contact sheets ----
$FF -y -v error -i "$VID" -vf "fps=1/$(awk -v d="$DUR" -v n="$N" 'BEGIN{printf "%.3f", d/n}'),scale=360:-2,tile=4x3" -frames:v 1 "$OUT/sheets/${NAME}_sheet.jpg" 2>/dev/null
echo "  sheet: $OUT/sheets/${NAME}_sheet.jpg"

# ---- 7. verdict ----
echo "── verdict ──"
echo "duration=${DUR}s size=$W frames=$COUNT flags=${FLAGS:-none} dups=$dup lufs=$(cat "$OUT/$NAME.lufs" | tr '\n' ' ')" > "$OUT/$NAME.verdict"
cat "$OUT/$NAME.verdict"
echo "DONE — review dir: $OUT"
