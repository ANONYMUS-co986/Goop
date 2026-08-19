# LOGBOOK V54 — THE 3 BRIEF AUDIOS + STT BLOCK + THE TRANSCRIBER PATH (19 Aug 2026)

**Order:** "extract audio and all images... run long tasks... use python to its max."

## WHAT LANDED (user downloaded + pushed to main — brilliant)
3 mp3s = the 3 brief videos' AUDIO:
1. **High on Purpose Show (Manav + Divaa)** — 19:08 — the Flash-3 inspiration video
2. **Mission 2 Changemakers World Cup** — 6:09 — the M2 announcement (password hidden here?)
3. **What are the judges actually looking for** — 3:59 — the "How to Stand Out" video
I pulled all 3 + saved to vikaas-hq/briefs/ + /tmp/brief_mp3s/.

## THE STT WALL (tried everything)
- faster-whisper: installed ✓ but model from HF → TLS-blocked
- whisper.cpp: model is GitHub-LFS → pointer (133B), LFS object host
  (github-cloud.githubusercontent) → 000 blocked. LFS batch API on github.com
  WORKS (returns signed URL) but the URL host is blocked.
- @napi-rs/whisper: no bundled model, macOS-only.
- transformers.js: no bundled model. vosk: model host blocked.
- No STT model reachable from the sandbox. PERIOD (network, not tools).

## THE PATH (the user's internet CAN download models)
- `engine/transcribe_briefs.sh` — one command on the user's laptop: installs
  faster-whisper → downloads 'small' model → transcribes all 3 mp3s →
  transcripts/*.txt → user commits them back → I read + act.
- The mp3s are IN the repo (vikaas-hq/briefs/) so the user just clones/pulls
  and runs the script.

## ALSO banked
- Audio structure probed (6-min M2 announcement).
- The LFS-batch-on-github trick (works for metadata, object host blocked).

## Next
Portfolio Phase 13 (book wizard) — and waiting on transcripts to nail Flash 3 +
M2 (password hunt in the M2 audio).
