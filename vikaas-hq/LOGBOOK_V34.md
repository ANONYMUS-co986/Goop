# LOGBOOK V34 — THE MASTER PLAN v3 + THE QA GATE (12 Aug 2026)

**Order:** "finalise the plan, take hours, improve your powers, stop erroring,
remake the site (keep the loader idea), report with 10+ phases, big implementations."

## 0. 6TH SANDBOX WIPE (mid-planning)
- Worktree reset to base `1d869ad` mid-turn. Resurrection spell ran: fetch
  explicit refspec → reset --hard → venv rebuild → chromium bootstrap
  (stubs rebuilt, libs reinstalled). ZERO work lost — doctrine: 6/6.
- Lesson banked: bootstrap script must use the venv python for make_nss_stub
  (system python lacks elftools) — patched the run steps.

## 1. THE MASTER PLAN — `vikaas-hq/PLAN_WEBSITE_V3.md` (locked)
- Research: Awwwards criteria (Design 40/Usability 30/Creativity 20/Content 10),
  what actually wins (Three.js/WebGL + GSAP choreography + custom interaction +
  60fps mid-range), benchmarks (Hubtown monolith, Cartier rooms, Sleep Well
  scroll storytelling, Uncommon camera moves, By-Kin Developer Award).
- **12 PHASES**, each a review gate with BIG implementations:
  1. Foundation rebuild + THE QA GATE
  2. Gate rebuild — 3D e-waste monolith hero + proof ribbon
  3. Drawer rebuild — interactive 3D drawer toy v2 + scale sequence + mini-map
  4. Proof — receipt printer + elastic scale + MagicBento + DotGrid viz
  5. Kabadi universe — tier-list showdown + ₹40 handshake + lore cards
  6. Arsenal — glass dock + reel lightbox + 22-post masonry + audio lab
  7. Buddy — galaxy sky + SCRAP-SCAN hologram demo + powers
  8. System — receipts-of-receipts timeline + terminal window + ImageTrail
  9. Geneva + polish — road-to-Geneva + finale footer + sound design + perf
  10. SEO/share — per-route OG, sitemap, live Insta grid, a11y
  11. Hardening — error boundaries, pre-push gate, stress, resurrect script
  12. Launch — walkthrough QA + rival-beater checklist + handoff kit

## 2. THE QA GATE — `engine/verify_all.sh` (the anti-error power)
One command = definition of done:
1. COMPILE gate: every route module/css/asset = HTTP 200 (kills 500-blank class)
2. RENDER gate: main exists · fonts ≥ 4 · scrollHeight > viewport
3. BLANK gate: viewport screenshot luminance std ≥ 8 (kills black-page class)
4. CONSOLE gate: 0 pageerrors/console errors/failed requests
5. Per-route verdicts counted → exit code (any FAIL = no ship)
- **Current run: GATE: PASS — 18/18** (compile 15 + 3 routes × render/blank/console).
- Bug fixed en route: execFileSync timeout is ms not s (30 → 30000).

## 3. State
- Vite app on :5173 (routes / /drawer /boot) — verified PASS by the gate.
- Loader idea KEPT (user loves it). Everything else rebuilt per plan.
- Next: Phase 1 (foundation refactor) + Phase 2 (gate rebuild) on user GO.
