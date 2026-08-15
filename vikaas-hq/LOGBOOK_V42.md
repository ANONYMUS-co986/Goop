# LOGBOOK V42 — ENTER-BUG KILLED + PLAN v4 (THE FULL IDEA) (12 Aug 2026)

**Order:** "upon clicking enter the drawer it doesnt change blank" + "do u even
know the entire idea — remake the plan after NIRMAN; change the name to VIKAAS
and better."

## 1. THE ENTER → BLANK BUG — root-caused, killed
- Symptom: /boot ENTER → navigate / → blank (main=false, scrollH 900).
- Real cause (after 3-layer hunt): the `?fast=1` path did `abRef.current
  .remove()` — a MANUAL removal of a React-managed node → React's fiber kept
  tracking it → on unmount, `removeChild` "not a child" threw → React's whole
  tree corrupted → Gate never mounted.
- Also removed the same bug-class elsewhere: GSAP `pin:true` (kill reverts
  pin-spacers async → same crash) replaced with **CSS position:sticky** scrub
  on Boot stage + Drawer story (`.story-wrap` 100svh+2200px); innerHTML on
  JSX-with-text-children (#word/#abWord had literal children → now empty).
- **NEW LAW (banked): never manually remove/replace a React-managed DOM node —
  state + CSS only (conditional render, sticky instead of pin, empty JSX for
  innerHTML targets).**
- Verified: ENTER → Gate renders, 0 errors. Gate PASS 18/18. Full boot (non-
  fast) PASS.

## 2. PLAN v4 — THE FULL IDEA (after reading ALL of NIRMAN)
- Realized: **Aarav Choudhary is listed as NIRMAN's co-founder** — it's a shared
  product idea; our VIKAAS must tell the SAME complete narrative, real + better.
- Wrote PLAN_WEBSITE_V4.md: the one-paragraph idea ("The infrastructure isn't
  missing. The doorstep is.") + the **16-section NIRMAN→VIKAAS map** (boot,
  hero, powers, core directive, drawer nation, the gap, 4-tap flow, receipt/
  proof chain, map, ReBee-AI, arsenal, network roles, analytics, system,
  roadmap, founders, finale) with WHERE each lives on the site.
- Structure: the GATE becomes the full one-page product pitch (chapter-marked);
  rooms are deep-dives. Phases updated (6-8 build the narrative sections).

## Next
Phase 6 (Gate hero v2 — 3D monolith) on "continue!"
