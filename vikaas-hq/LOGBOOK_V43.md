# LOGBOOK V43 — MENU CLICKABILITY KILLED + THE APP IDEA (12 Aug 2026)

**Order:** "the menu nothing is clickable" + "the idea is as it is but we must do
it before him so he can't steal — it's going to be an APP that recruits
collection centres for collection of e-waste."

## 1. THE MENU BUG (root-caused via click probe)
- Symptom: menu overlay visible but nothing clickable (user screenshot).
- Cause: `.gnov` base CSS = `pointer-events:none` (hidden state); Framer's
  `animate` set opacity but never restored pointer-events → overlay links had
  `pe:none`. FIX: pointerEvents auto in animate + `.gnov a{pointer-events:auto}`.
- SECOND bug: after Esc, overlay stayed mounted (`display:flex`, pe:auto) and
  blocked the menu button → re-open impossible. FIX: full React unmount via
  `navMounted` state (400-500ms after close) + Esc handler wired in effect +
  all link onClicks unmount.
- NEW CLICK GATE (verify_all.sh #6): probe opens menu, checks ALL overlay links
  pe:auto, closes, re-opens, navigates → FAIL = no ship.
- **verify_all: GATE PASS — 19/19** (was 18; clicks gate added).

## 2. THE REAL IDEA — the APP (do it before NIRMAN)
- VIKAAS = an **e-waste collection app**: households book doorstep pickups;
  the app **recruits collection centres** (kabadiwala network + authorised
  recyclers) to serve the doorsteps; weigh → value → pickup → receipt →
  verified recycling. The portfolio sells THIS app (like NIRMAN sells its app)
  — but with our real proof (1.4 kg, ₹40, 15 recyclers, 0 doorsteps).
- Plan v5 coming: 30+ phases, portfolio-then-app.

## Next
Plan v5 (30+ phases) → Phase 6 (Gate hero v2 — 3D monolith).
