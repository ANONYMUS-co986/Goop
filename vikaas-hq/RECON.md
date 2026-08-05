# 🕵️ RECON — Instagram scouting toolkit + live intel (verified 5 Aug 2026)

## A) The no-login viewer gauntlet — TESTED LIVE
| Tool | Status | Notes |
|---|---|---|
| **imginn.com** | ✅ **WORKS — primary channel** | Full profile + posts + reels + stories + tagged tabs, visible captions, **likes + comments + relative dates**, profile pic, media params. Fetch pattern: `imginn.com/<handle>/`, `/reels/<handle>/`, `/stories/<handle>/` |
| anonyig | ❌ blocked (proxy-blocked) | — |
| picuki/dumpor | 💀 dead per 2026 coverage | — |
| thepicuki/pixwox/instanavigation/getinstaview | ⏳ untested | backups if imginn dies |
| instagram direct | ❌ TLS/IP-blocked from sandbox; 403 for anonymous fetch | cannot be used |
| **google index trick** | ✅ backup | `site:instagram.com <handle>` via web search shows indexed posts |

**Ops promise: whenever Aarav posts, I can check both handles on demand and
report (likes/comments/new posts/dates). Say "scout" and I'll run it.**

## B) Scout report — @qwerty_aarav (US)
- Posts: **1** (flash meme), 28 Jul, caption = full drawer story **with the
  1.4 kg / 10-homes numbers** (numeric version, not SAFE)
- Engagement: 2 likes, 0 comments. Account is 8 days old. We're at zero.
- Tabs exist for reels/stories — nothing there yet.

## C) Scout report — @nirmaan.platform (THE RIVAL) — full grid mapped
~10 posts (all fetched and read):
| Post | Type | When | Likes | Notes |
|---|---|---|---|---|
| Flash meme "upgrade becomes e-waste 💀📱" | static | 28 Jul | 8 | his F1 submission |
| "Dynamic Island mila… common sense kho gaya?" | meme | 28 Jul | 7 | Hinglish POV format |
| "RGB productivity excuse" | meme | 28 Jul | 9 | 💻 "Bro... I still work." |
| "Loyal Phone. Disloyal Owner 💀" | meme | 28 Jul | 7 | |
| "Reality Check: It's Not the Laptop" | text card | 28 Jul | ~7 | |
| +1-2 more memes | | | | |
| **REEL**: "62 MILLION TONS. Har saal. Aur duniya chup hai 💀♻️" | reel ~40 s | 2 Aug | 2 | Dxrk RAVE phonk edit, anime/AMV lane, source: UN Global E-waste Monitor 2024 |
| **REEL**: "62 MILLION TONS of e-waste every. single. year." | reel ~30 s | 30 Jul | **9+1 cmt** | Murder in My Mind slowed+reverb; his best performer |

**His lane:** phonk-edit reels (dark, fast cuts, anime-edit energy, #phonk
#aesthetic tag stuffing) + text-heavy "POV:" memes, Repair-Don't-Replace
message, signature line *"The world needs me because…"* in every caption.
**Weaknesses we exploit:** (1) same stat 62Mt / 22% everywhere = one song,
no story arc; (2) zero receipts (no personal trigger, no real footage, no
local facts); (3) engagement ceiling ~9 likes; (4) graphics = stock edit
templates, no brand system (no logo ident, no consistent type).
**Our counter-lane:** premium studio craft + personal narrative + real
local data + sound-off legibility + integrity-gated numbers. Different
weight class entirely.

## D) Asset-access map for the studio (verified from THIS sandbox)
| Pipe | Verdict | Use |
|---|---|---|
| `image_search` tool | ✅ works (Brave index, saves files to workspace) | real photos + blank meme templates (query `site:unsplash.com`/`pexels` for free-license, `imgflip <name> template blank`) |
| `generate_image` | ✅ | custom photoreal + brand art (amateur-snapshot technique from logbook) |
| fetch_page | ✅ text/markdown | research, viewer pages, captions |
| direct curl (imginn/imgflip/unsplash/insta CDN) | ❌ TLS-blocked | — |
| npm/apt/github | ✅ | deps, fonts, GitHub-hosted assets |
- Meme-template access path: `image_search "imgflip <template> blank"` →
  composite our typography over it in the studio. Unlicensed editorial
  photos: avoid publishing; prefer unsplash/pexels queries or generated.
