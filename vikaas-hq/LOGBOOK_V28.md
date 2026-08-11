# LOGBOOK V28 — LOADER v4 FINALE: AUTO BOOT + LID-UP + NEBULA + EXPANDABLES (11 Aug 2026)

**Order:** caret opens DOWNWARD — must flip the lid UP · a 10s AUTOMATED boot then
scroll · nebulas in bg · glow-on-hover text everywhere · reactbits aesthetics ·
interactable/expandable boxes · study the rival site (nirmaan-portfolio.vercel.app)
and be way better · don't clutter.

## 0. RIVAL INTEL (fetched & studied)
NIRMAN OS: terminal-hype product pitch — "Initialize Engine" boot gate, HUD labels,
7 numbered sections, screenshot lightboxes, radar map, big claims (blockchain,
100% custody, OTP handover). STRONG aesthetic, but it's a concept pitch with no
receipts. OUR edge: real numbers (1.4 kg WEIGHED, ₹40, 15 HSPCB recyclers, 0
doorsteps), real 3D drawer, real character (ReBee), real deliverables (6 reels/22
posts), real story (CWC → Geneva). We match the OS/terminal energy and exceed on
truth + craft.

## 1. LOADER v4 — the fixes
1. **LID OPENS UP**: pivot at back edge, rotation.x tweened NEGATIVE (−1.95).
   Verified by probe: lidX 0.005 → −1.851 → −1.95 (was +1.28 = opening downward).
2. **AUTO BOOT (~10s) THEN SCROLL**: full-screen boot overlay — terminal TYPES
   7 lines char-by-char (18ms/char, cursor, progress bar, status labels:
   INITIALISING→SCANNING→WEIGHING→VERIFYING→SUMMONING→READY), VIKAAS scramble,
   then overlay slides UP revealing the stage + "SCROLL TO ENTER THE UNIVERSE".
   ScrollTrigger disabled during boot, enabled+refreshed on reveal. SKIP button.
   Probe receipts: T+1s typing (bar 3%) · T+7s all lines + READY · T+12s overlay
   gone, cue on, triggers enabled. 0 errors.
3. **NEBULA BACKGROUND**: 4 drifting blurred orbs (violet/acid/green/gold) on
   loader + gate hero — reactbits Aurora-family energy, CSS-only, cheap.
4. **TEXT FX everywhere** (shared shell): `.glow-hover` (acid glow on hover),
   `.shiny` animated eyebrows, `.grad-text` animated gradient (footer big line),
   section-title hover glow.
5. **EXPANDABLE ROOM BOXES** (gate): every room card click-expands a teaser
   panel + CTA, `+` rotates 45° — "interactable boxes", unlocked + locked cards
   both expand (locked show "PHASE n · IN BUILD").
6. **MAGNETIC buttons** ([data-mag]) + cursor v2 kept from V27.
7. 520-particle nebula dust in 3D (added violet to palette).

## 2. BUG CAUGHT BY THE LOOP (the important one)
**Infinite-repeat tween INSIDE the scrubbed timeline** → duration ∞ → ScrollTrigger
progress collapses → lid never opened, camera jumped to end. The lid-probe caught
it (lidX 0 at every scroll). Fix: infinite loops started via `tl.call()` as
separate tweens. Banked in MANUAL §9.
(Also: QA hook exposure must happen AFTER initThree — null-capture bug.)

## 3. SUITE RECEIPTS (all PASS)
loader desktop + mobile (--wait=11500 post-boot) · gate desktop + mobile
(--cta=.gnav-menu). lid probe: opens UP. boot probe: 10s flow exact. 0 errors all.

## NEXT
Phase 3 THE DRAWER (pinned cinematic story page). ReBee submission DUE TODAY 12 Aug.
