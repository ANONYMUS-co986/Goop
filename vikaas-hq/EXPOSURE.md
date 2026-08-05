# 🔐 EXPOSURE SWEEP — public repos of aarav-choudhary-pro (+ Goop org)

**Scanned: 5 Aug 2026.** Method: full clones + pattern sweeps
(`github_pat_`, Google API key prefix, Firebase refs, password contexts).
Values are deliberately NOT reproduced below — files + types only.

## Verdict: 🔴 live secrets are in public GitHub right now

| Repo | File (pattern) | Secret type | Severity |
|---|---|---|---|
| `aarav-choudhary-pro/posts` | the two committed chat-transcript `.txt` files | GitHub personal access token (`github_pat_…`), **account passwords pasted in chat** (incl. an Instagram password) | 🔴 critical |
| `aarav-choudhary-pro/Poem-writer-` | "all the chat …" transcript `.txt` | GitHub personal access token | 🔴 critical |
| `aarav-choudhary-pro/Poem-writer-` | firmware + docs (`AIza…` prefix in 8 files: `Code_1_Main_Brain.ino`, `Code_2_ESP32_CAM.ino`, `ESP32_CAM_Testing_Manual`/`Setup_Manual` etc.) | Google API keys (Gemini-class) + Firebase RTDB wiring | 🟠 high |
| `aarav-choudhary-pro/Poem-writer-` | firmware + CONTEXT docs | home/hotspot WiFi SSID + password, x-api-key for upload endpoint | 🟠 high |
| `ANONYMUS-co986/Goop` | — | no secrets found in sweep | ✅ |

`aarav-choudhary-pro/insta-time` → 404 (already private/deleted) ✅

## Action checklist for Aarav (order matters)
1. **Now:** make `posts` and `Poem-writer-` private. Local clones of both
   (all branches + full history) are already secured in my workspace, so
   nothing is lost.
2. **Today — rotate, don't just hide:** making private does NOT revoke
   anything that was scraped in the meantime.
   - Revoke/rotate the GitHub PAT at github.com/settings/tokens.
   - Change the Instagram password (and the other one posted in chat).
   - Rotate the Google API keys (AIza…): Firebase console / Google AI
     Studio — delete the old, create new, restrict by HTTP referrer/app.
   - Rotate the Vercel upload `x-api-key` and check Firebase RTDB rules.
   - WiFi password: change if it's really the one in the repo.
3. **Later (optional, thorough):** scrub history with `git filter-repo`
   /BFG on both repos before ever re-publishing.
4. **Rule going forward:** paste secrets into NOTHING — not chat, not
   docs, not firmware comments. A `.env` that never gets committed, or it
   doesn't exist.

## What I did locally
- Full mirrors cloned: `posts` (all branches incl. the recovered
  Changemakers2026 workspace), `Poem-writer-` (full history).
- Working-file inventory of the campaign workspace is in `SITREP.md`.
