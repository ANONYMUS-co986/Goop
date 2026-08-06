#!/usr/bin/env bash
# VIKAAS — VID 04 v3 VO mix + master re-encode (one command after vo_out.zip lands)
# Usage: bash mix_v3.sh <dir-with-vo1_pov.mp3..vo8_finale.mp3> [--encode]
#   without --encode: only builds audio/MIX_D_v3.m4a + previews
#   with    --encode: also re-encodes drops/FINAL_PACK/VIKAAS_04_COMEDY-CLUB.mp4 (needs frames_tmp/reD_v2)
set -euo pipefail
cd "$(dirname "$0")"
VO_DIR="$1"; ENCODE="${2:-}"
FF=$(ls /home/user/.studio_venv/lib/python*/site-packages/imageio_ffmpeg/binaries/ffmpeg* 2>/dev/null | head -1)
[ -z "$FF" ] && FF=$(which ffmpeg)
SR=44100
BEATS=(1.0 4.5 8.35 12.9 16.5 22.4 30.2 37.0)     # design grid (from reel_d timeline)
ROOMS=(3.3 3.6 7.6 4.9 5.7 10.4 6.6 4.6)          # allowed rooms (sanctioned tail-overlap like v2 mix)
names=(vo1_pov vo2_mummy vo3_narrator1 vo4_papa vo5_narrator2 vo6_calc vo7_kabadi vo8_finale)

FILT=""; declare -a IN=(-i "audio/TR_D_kabadi-bounce.wav"); idx=1
for i in 0 1 2 3 4 5 6 7; do
  f="$VO_DIR/${names[$i]}.mp3"; [ -f "$f" ] || { echo "MISSING $f"; exit 1; }
  dur=$({ $FF -hide_banner -i "$f" 2>&1 || true; } | awk '/Duration/{split($2,a,":"); print a[1]*3600+a[2]*60+a[3]}')
  room=${ROOMS[$i]}
  factor=$(awk -v d="$dur" -v r="$room" 'BEGIN{printf "%.3f", d/(r*0.98)}')
  tempo=$(awk -v f="$factor" 'BEGIN{printf "%.3f", (f>1.0?f:1.0)}')
  over=$(awk -v t="$tempo" 'BEGIN{print (t>1.25)?"WARN(>1.25 chipmunk risk)":"ok"}')
  onset=${BEATS[$i]}
  echo "${names[$i]}: raw=${dur}s room=${room}s atempo=${tempo} [$over] -> onset ${onset}s"
  IN+=(-i "$f")
  # per-VO chain: trim silence, de-plosive, comp, presence, tempo-fit, gain, delay
  FILT="$FILT[$idx:a]aresample=$SR,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,\
silenceremove=stop_periods=-1:stop_threshold=-45dB:stop_duration=0.15:stop_silence=0.15,\
highpass=f=90,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2dB,\
equalizer=f=3200:t=q:w=1.0:g=1.5,atempo=$tempo,volume=1.3,apad,atrim=0:41,adelay=delays=$(awk -v s="$onset" 'BEGIN{printf "%d", s*1000}')|$(awk -v s="$onset" 'BEGIN{printf "%d", s*1000}')[v$idx];"
  idx=$((idx+1))
done
# bed (sidechain-ducked by VO sum) + all VO lines
FILT="$FILT[0:a]aresample=$SR,volume=0.38[bed];[v1][v2][v3][v4][v5][v6][v7][v8]amix=inputs=8:normalize=0,asplit=2[vosum][vomix];\
[bed][vosum]sidechaincompress=threshold=0.02:ratio=5:attack=25:release=350:level_sc=1[duck];\
[duck][vomix]amix=inputs=2:normalize=0[prem];[prem]atrim=0:41,alimiter=limit=-1.5dB,loudnorm=I=-19:LRA=7:TP=-1.5[out]"
FB=$(mktemp); printf '%b' "$FILT" > "$FB"
$FF -y -v error "${IN[@]}" -filter_complex_script "$FB" -map "[out]" -c:a aac -b:a 160k -t 41 audio/MIX_D_v3.m4a
rm -f "$FB"
$FF -y -v error -i audio/MIX_D_v3.m4a -c:a libmp3lame -q:a 4 audio/VO3_preview.mp3 2>/dev/null || $FF -y -v error -i audio/MIX_D_v3.m4a -c:a mp3 audio/VO3_preview.mp3
# AB sampler: 4s old vs 4s new around मम्मी→narrator beat + around calc beat
$FF -y -v error -i audio/MIX_D_v2.m4a -i audio/MIX_D_v3.m4a -filter_complex \
 "[0:a]atrim=4:8,asetpts=PTS-STARTPTS[a1];[1:a]atrim=4:8,asetpts=PTS-STARTPTS[b1];\
 [0:a]atrim=22:27,asetpts=PTS-STARTPTS[a2];[1:a]atrim=22:27,asetpts=PTS-STARTPTS[b2];\
 [a1][b1][a2][b2]concat=n=4:v=0:a=1,volume=1.0[out]" -map "[out]" -c:a mp3 audio/VO3_AB_old-new.mp3 || true
I=$($FF -nostats -i audio/MIX_D_v3.m4a -af ebur128 -f null - 2>&1 | grep -A6 "Summary:" | grep "I:" | head -1)
echo "MIX_D_v3 loudness: $I"
[ "$ENCODE" = "--encode" ] || { echo "audio done (no --encode)"; exit 0; }
[ -d frames_tmp/reD_v2 ] || { echo "frames missing — re-render first: node engine/lib.js render drops/v4/reel_d.html frames_tmp/reD_v2 30"; exit 1; }
node engine/lib.js encode frames_tmp/reD_v2 audio/MIX_D_v3.m4a 40.8 drops/FINAL_PACK/VIKAAS_04_COMEDY-CLUB.mp4 30
$FF -nostats -i drops/FINAL_PACK/VIKAAS_04_COMEDY-CLUB.mp4 -map 0:a -af ebur128 -f null - 2>&1 | grep -A6 "Summary:" | grep -E "I:|LRA:" | head -2
echo "MASTER 04 v3 DONE"
