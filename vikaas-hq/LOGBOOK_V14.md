# LOGBOOK V14 — UNDERLINE EXTERMINATION + TAULO-1 (7 Aug 2026)
**Orders from Aarav:** (a) finale posts still have misalignments — "text or the line below them, underdashes"; verify all. (b) New task dropped: Flash Challenge #2 — Create 1M1Bee's AI Buddy (deadline 12 Aug) — wants to get FEATURED. (c) Watch the challenge tutorial video myself via a git video downloader. (d) Find more third-party sites like imginn + download good phonks/songs myself; generated audio = "bad". (e) Ask questions if unclear.

## 0. Environment resurrection (do this FIRST every fresh sandbox)
- Local checkout had reset to base `9c3a602`; remote branch held our tip `dd10675`. **Quirk:** this sandbox's `remote.origin.fetch` only maps `main`, so plain `git fetch` won't create `origin/arena/*` refs. Working spell:
  `git fetch origin 'refs/heads/arena/019fc480-goop:refs/remotes/origin/arena/019fc480-goop' && git reset --hard origin/arena/019fc480-goop`
- `.studio_venv` was wiped → recreated: `python3 -m venv ~/.studio_venv && pip install pillow numpy imageio-ffmpeg soundfile scipy` (pypi reachable ✓).
- `image-search/` cache (untracked) lost the meme blanks/photos. Re-pulled 11 assets via image_search, renamed to script-expected names. Verified originals where possible: kalm-panik-kalm = imgflip 228718970 EXACT ✓, dbf full version = 379293870 EXACT ✓, gru 5-panel = 205746517 EXACT ✓, cat HD = 211447548 EXACT ✓. Weaker replacements (log for future): drake now 300×292 (was bigger), two-buttons restoration now 640×968 (was 2400×3632), cmm now 2kj615 (was 3mfdo), screwdriver/gate/pole photos = alternates.
- **Decision:** did NOT re-ship rebuilt memes — committed masters (built from the big originals) are strictly better. Surgical ship: only fixed posts replaced. Backups in `/tmp/masters_backup/`.

## 1. UNDERLINE EXTERMINATION (his "underdashes" complaint) — root + fix
Root family: underlines placed by *estimated* text geometry (`f.size*1.06` guesses, fixed x-ranges) — Pillow line advance ≠ size estimate, so bars landed ON glyph bottoms / off-center / through letters.
- `build_posts.py` `build_poster`: underline now derived from `multiline_textbbox` (actual block top/bottom/center) → bar at bottom+24, centered on the real block, width = min(300, 45-50% of real block). P1–P6 rebuilt clean.
- `build_posts_v2.py` **R1**: fixed bar `[590,850]` → bbox-driven, and the Devanagari sub line was **~1440px wide at f_dev(46)** (touching both canvas edges — likely one of the exact misalignments he saw) → autosized to ≤1300.
- **R6**: fixed bar `[270..1170]` sliced through WANTED's lower strokes + "THE 2014 CHARGER" grazed the engraving → WANTED start 218→176, bar = textbbox width +34 below glyphs, sub at bbox+40. Clear arcs.
- **P6**: 3-line `MUMMY'S MUSEUM. EST. FOREVER.` — 3rd line overlapped the shelf art → headline cut to 2 lines (gag moves to caption usage). 2-lines = series rhythm.
- Verification: zoom crops of every fixed zone + regenerated `qc/` contact sheets from SHIPPED files; `MANIFEST.sha256` resealed (30 files, `sha256sum -c` = 0 failures).

## 2. FLASH CHALLENGE #2 — TAULO-1 (`vikaas-hq/cwc_buddy/`)
- Concept: **TAULO-1** — 1M1Bee's buddy, a bee-bot rebuilt literally FROM e-waste (capacitor body/bee stripes, phone-glass circuit wings, charger-LED eyes, earphone-copper antenna, weighing-dial chest, USB feet, flex-banner cape). Superpower **SCRAP-SCAN** (contents + ₹ + nearest of 15 HSPCB recyclers) + **DOORSTEP DIAL** (0→1 pickups). Mission: NO DRAWER LEFT BEHIND. Catchphrase: "Taulo karo. Weighed, not guessed." → ties the whole VIKAAS brand into the submission; if featured, viewers land on a feed that already speaks TAULO.
- Art (generate_image): `art/taulo_hero.png` (3D hero, submission image — first try, 10/10) + `art/taulo_poster_plate.png` (riso plate w/ blank top) → composed `taulo_poster.jpg`. Self-QA caught v1's mid-canvas sub crossing wing/antenna → removed; v2 clean.
- `BUDDY_BRIEF.md` = paste-ready name/ability/mission + Step-1 SkillsBuild tap-by-tap (link, Under 18, "Sponsored by 1M1B", code `cxuk`, channel link, completion screenshot) + featured-evening caption.
- Tutorial video: Drive/YouTube **unreachable from sandbox** (egress 000) — honest me-limit; steps on the challenge page are self-contained; he watches on his phone.

## 3. PHONK HUNT — verdict: found, vetted, REJECTED (integrity)
- Searched GitHub (only open pipe): found `dmitriimoiseev081015-code/PhonkDiscs` — 11 full phonk .ogg (1:53–2:51, hot masters −6.6..−13 LUFS). BUT its README: "high-quality audio (Kordhell, ZXKAI, and more)" = **ripped commercial masters**; MIT license covers the mod CODE, not the songs. Shipping = copyright risk (IG mute/removal) + off-brand.
- **Decision stands:** (1) trend-swap inside IG editor = the only clean way to real Kordhell/Dxrk (licensed by Meta; Anuj's own tactic; steps in HOW_TO_POST.md), (2) Aarav can ATTACH tracks in Arena chat (they land in `/home/user/uploads/`) → I'll master/reel them, (3) forged TR_A/B/C remain the always-safe default.
- Egress probe log: OK = github/api/codeload/npm/pypi · blocked = Drive, YouTube, SoundCloud, filesamples, archive.org, pixabay, skillsbuild, changemakersworldcup (fetch_page/web_search still work server-side).

## 4. Also answered
- Third-party viewers (his phone): imginn (verified by us), dumpor.com, greatfon.com — use for Sunday scouts + checking how our grid renders publicly.
- Branch state at close: 21 posts re-verified, arsenal sealed, buddy package committed.
- Still pending: `vo_out (1).zip` for V4 v3 mix · M2 dashboard screenshot · portfolio PH3 · posting launch confirmation (Day 1 V2).
