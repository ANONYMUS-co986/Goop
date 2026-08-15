# LOGBOOK V47 — PHASE 9: DRAWER INTRO + STORY POLISH (12 Aug 2026)

**Order:** "cont" → Phase 9.

## What shipped
- **Intro hero stagger**: THE / DRAWER lines reveal line-by-line (yPercent 120,
  back.out(1.6), 0.15/0.35 offsets) + sub + cue — cinematic entrance.
- **Story progress rail** (left edge, like the boot's): fills with the pinned
  scrub (onUpdate progress → rail height), hidden on mobile.
- **CAUGHT + FIXED**: the `.story-wrap` sticky wrapper was NEVER in the JSX
  (a Phase-4 edit's anchor missed) — so the story was NOT pinned at all (it
  scrolled past). Added the wrapper + rail properly. The story now pins and
  scrubs as designed.

## QA GATE
- intro: 2 lines staggered + sub + cue visible ✓ · rail present ✓ · story
  scrubs (l1 at 1, big at 0 mid-story = correct pacing) ✓ · 0 errors
- **verify_all.sh: GATE PASS — 19/19** ✅

## Next
Phase 10 (Drawer toy v2) on "continue!"
