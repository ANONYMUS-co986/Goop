# LOGBOOK V48 — THE BLACK-SCREEN POSTMORTEM + JSX BALANCE GATE (12 Aug 2026)

**Order:** "why do i see a black only (is it the preview server not ref of c cont)"

## Postmortem — the black screen
- NOT the site being broken NOW: the Gate renders (probe: VIKAAS + chips +
  monolith, acid 308%, 0 errors, 19/19).
- CAUSE: during Phase 8 edits, Gate.jsx briefly had a double-`</section>` →
  Vite 500 → user's browser loaded the error state → black. Fixed at 10:25;
  user's browser kept the cached broken page.
- FIXES: (1) restarted preview fresh, (2) verified section balance 9/9,
  (3) **NEW JSX BALANCE GATE in verify_all.sh** — every page .jsx must have
  equal <section>/</section> counts (catches the transient-500 class before it
  ships). (4) fixed my verdict-inversion bug (BAL_OK=1 vs verdict's 0=pass).

## QA GATE — now 20/20 PASS (compile/render/blank/console/jsx-balance/clicks)

## Lesson banked
Never trust "it worked a minute ago" — the gate re-runs everything on every
phase; the JSX-balance check makes a mid-edit 500 impossible to ship.
