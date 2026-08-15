# LOGBOOK V49 — PHASE 10: DRAWER TOY v2 — HOLOGRAPHIC SPEC CARDS (12 Aug 2026)

**Order:** "cont" → Phase 10 (drawer toy v2).

## What shipped
- **Holographic spec card**: tap any item in the drawer → a hologram card
  springs up (scan-line sweep, glow, holo-in ease) showing:
  - SCRAP-SCAN · LIVE tag
  - item name + real audit line
  - VALUE (real estimate: ≈₹12 copper+board etc) + RECYCLER match
    (real HSPCB names: Exigo Manesar, EcoMetals Gurugram, Cerebra HITEC,
    Attero Noida, E-Parisaraa Peenya)
  - stamp (WEIGHED / RECEIPT #1 / SOURCED / HANDLE CAREFULLY)
- **Staggered float-out**: the 5 items rise one-by-one on open
  (cubic-bezier spring, 0.05–0.33s delays) — feels physical.
- Kept: 3D tilt + glow + readout.

## This is the ReBee SCRAP-SCAN concept made playable in the Drawer room:
the same idea the Buddy room will expand (phase 20) — contents → value →
nearest recycler. The toy now demos the APP's core value in one tap.

## QA GATE
- probe: open ✓ 5 items ✓ tap phone → card with name/value/recycler/stamp/tag
  ✓ · 0 errors · acid 177% (card glows)
- **verify_all.sh: GATE PASS — 20/20** ✅

## Next
Phase 11 (the scale sequence — scroll-driven weighing) on "continue!"
