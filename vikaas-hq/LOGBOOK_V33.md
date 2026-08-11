# LOGBOOK V33 — THE BLANKING FIXED: fonts + drawer intro (12 Aug 2026)

**Order:** "still error and blanking and page not being completely built."

## THE ROOT CAUSES (found by real eye-verification)
1. **FONTS 404 = the "not built" look.** shell.css used `url('../fonts/…')` but
   the fonts lived in `src/assets/fonts/` → Vite resolved `../fonts/` to
   `/fonts/` (public/) which DIDN'T EXIST → browser fell back to default fonts
   → typography died, everything looked broken/blank. FIX: copied fonts to
   `public/fonts/` → now serve 200, `document.fonts.size` = 6, 0 warnings.
2. **DRAWER = pure black screen on load** (std 6.0, 99.8% dark — my viewport
   probe caught it, the full-page shot hid it). The page opened straight into
   the PINNED story whose content is hidden until scroll → first screen was
   empty. FIX: added a proper intro hero (THE DRAWER giant Anton title + sub +
   cue) visible on load, story pins after it. Verified: mean 28/std 60, title
   glyphs visible in ASCII map, 0 errors.

## VERIFICATION (all over HTTP, real)
- `/`: SUITE PASS · fonts 6 · chars/ticker/wipe/progress/cards present · 0 errors
- `/drawer`: SUITE PASS · intro hero visible · story pins · toy opens · 0 errors
- `/boot?fast=1`: SUITE PASS · 0 errors
- Browser multi-page crash in probes = sandbox quirk (separate processes work).

## Also
- Drawer intro title glow strengthened (acid/green shadow).
- probe_one.js / shoot_route.js added to engine (per-route single-browser probes).

## Next
User review → iterate. Phase 4 THE PROOF route.
