# 🐝 PLAN WEBSITE V7 — THE APP-FIRST REMAKED PLAN
### 19 Aug 2026 · VIKAAS (विकास) · 1M1B Changemakers World Cup 2026 — "Kill the E-Waste"
> V7 = full remake after the user's correction: **THE IDEA IS THE APP.** Not a drawer story, not a kabadiwala story — an APP like Swiggy/Zomato for e-waste, connected to collection centres, exactly like ScrapUncle BUT better: AI features, dedicated to e-waste, with a USP where others aren't. The portfolio SELLS that app. The drawer (1.4 kg · ₹40 · 15 recyclers · 0 doorsteps) is the PROOF that the flow works — the pilot, not the product.

---

## 0. THE IDEA (user-stated, fixed, non-negotiable)

**VIKAAS = an app like Swiggy/Zomato, but for e-waste.**
- You open the app → enter your waste (what it is, how much — or snap a photo, AI estimates).
- **Book a pickup.** A collection centre — kabadiwala + authorised recycler, recruited by us — comes to your door, weighs it in front of you, **pays cash**, and **receipts** it to a verified recycler (chain of custody).
- Market reference: **ScrapUncle** (on-demand scrap pickup) — VIKAAS is that model **but**: ① dedicated to E-WASTE (not mixed scrap), ② AI features (SCRAP-SCAN photo estimation, ReBee assistant, live rate cards), ③ HSPCB-verified chain of custody receipts, ④ works where they aren't (Gurugram, any quantity from 0.5 kg, doorstep weighing).
- **USP (one line): "Where others aren't — your door."**

**Proof (REAL, vs NIRMAN's fake screenshots):** 1.4 kg weighed on a kitchen scale · ₹40 cash paid · 15 HSPCB recyclers sourced · 0 doorsteps served by them. Every claim stamped: WEIGHED / SOURCED / ESTIMATE / DRAMATISED / RECEIPT #N / THE GAP.

---

## 1. WHAT THE PORTFOLIO IS (architecture)

The portfolio = a cinematic universe that **sells the app**:
- **THE GATE** (`/`) — the pitch. HERO: "THE APP THAT BOOKS E-WASTE PICKUP LIKE FOOD" + TRY THE APP CTA → **WHAT IS VIKAAS** (the app anatomy: OPEN → BOOK → WEIGH·PAY → RECEIPT + USP line) → CORE DIRECTIVE → THE DRAWER NATION (problem) → THE STRUCTURAL GAP (500kg vs 1.4kg) → THE APP'S 4 TAPS → THE IDEA in 4 moves → builders (Aarav + ReBee) → rooms grid → Geneva footer.
- **THE BOOT** (`/boot`) — loader: auto-boot + 3D drawer scroll universe (the SESAME).
- **THE DRAWER** (`/drawer`) — the pilot story (proof, not product).
- **THE TYPE** (`/type`) — styleguide.
- **THE APP** (`/app`) — the centerpiece: phone mock autoplay of the 4-tap flow + how-it-works + moat.
  - `/app/book` — 4-step pickup wizard → RECEIPT #0002 (live).
  - `/app/centres` — 8-centre roster (real HSPCB + kabadiwalas) + REGISTER YOUR CENTRE.
  - `/app/map` — SVG Gurugram: 15 pulsing recyclers + 10 households + click-to-route.
  - `/app/receipts` — **THE PROOF LIBRARY**: RECEIPT #0001 (the real pilot, chain of custody), #0002 (live wizard), #0003–25 slots ("your drawer is #0003").
  - `/app/assistant` — **REBEE AI chat** (SCRAP-SCAN / DOORSTEP DIAL / MATERIAL MATCH).
  - `/app/dashboard`, `/app/login`, `/app/admin` — Phase 17.
- **Rooms (later phases):** THE PROOF (16→ standalone), THE KABADI UNIVERSE (17), THE ARSENAL (18), THE BUDDY (19), THE SYSTEM (22), GENEVA (23).

---

## 2. THE STACK (NIRMAN-grade craft bar)

Vite 6 + React 19 + Router 7 · GSAP + ScrollTrigger + SplitType · Framer Motion · Lenis · Three.js (Monolith, drawer universe) · Zustand · custom cursor v3 + splash particles · PageWipe acid curtain · HUD/overlay shell · sound (boot/enter/ambient, hover blips) · Devanagari Anton + Space Grotesk + Noto Devanagari · acid-green (#B9FF3F) + glassmorphism + stamps.

NIRMAN mapping (their 16 sections → ours): GenesisLoader→Boot · HeroFluid→Monolith hero · MissionManifesto→Directive/Manifesto · Graveyard→Drawer Nation+Drawer room · Gaps→Structural Gap · Forge→/app phone mock · ProductScreens→Receipts+Buddy · Network/LiveMap→/app/map · EcosystemRoles→Centres · Cortex→Assistant/ReBee · TrustVerification→Chain-of-custody receipts · ImpactIntelligence→stats band · TechnologyArchitecture→/system · Feasibility/Roadmap→Geneva · Architects→Builders · Nexus→Geneva footer CTA.

---

## 3. PHASE TRACKER (V7 — DONE through 16)

| # | Phase | Status |
|---|---|---|
| 1–5 | Gate, Boot, Drawer, Type, Shell/FX | ✅ |
| 6–12 | /app family foundations, sound, tokens, probes | ✅ |
| 13 | /app/book wizard (4-step → RECEIPT #0002) | ✅ GATE 20/20 |
| 14 | /app/centres roster + register (the moat) | ✅ GATE 20/20 |
| 15 | /app/map network map (15 dots · 10 homes) | ✅ GATE 20/20 |
| 16 | **/app/receipts proof library + /app/assistant ReBee chat** | ✅ GATE 43/43 |
| 16.5 | ReBee real-AI brain (OpenRouter LLM, portfolio-aware) | ✅ GATE 44/44 |
| 17 | Dashboard + login + admin (the operator side) | ✅ GATE 51/51 |
| 18 | THE PROOF room (evidence vault, real photos, M2 live feed) | ✅ GATE 54/54 |
| 19 | **THE KABADI UNIVERSE (the network room — cast, economics, recruitment)** | ✅ GATE 57/57 |
| 19.5 | **THE INTERACTIVITY OVERHAUL** — global fixed 3D particle scape (Three.js, mouse-repel + parallax, every page) · magnetic buttons (data-mag finally live) · cursor-tracking card spotlight · 3D tilt on all big cards · scroll-velocity title skew · reactive stamps/chips | ✅ GATE 59/59 |
| 20 | THE ARSENAL (6 reels · 22 posts · VO clips) | ⏭ NEXT |
| 20 | THE ARSENAL (6 reels · 22 posts · VO clips) | ⏭ |
| 21 | THE BUDDY (ReBee full room) | ⏭ |
| 22 | THE SYSTEM (engine room: pipelines, QA law) | ⏭ |
| 23 | GENEVA + 404 | ⏭ |
| 24 | Sound/perf pass | ⏭ |
| 25 | SEO/a11y pass | ⏭ |
| 26 | Database (Supabase schema — see §5) | ⏭ |
| 27 | LAUNCH + missions weave | ⏭ |

---

## 4. THE QA GATE (the law — currently 43/43 PASS)

`vikaas-hq/studio/engine/verify_all.sh` — compile (every module/css/asset 200) → render (main, ≥4 fonts, scrollHeight>vh) → blank (std≥8) → console (0 errors) → JSX balance → clicks (menu + all links). Plus eyes 2.0: OCR (`engine/ocr.js`), vision desc, pix rig, suite.js scroll-beat probes, `video_review.sh` (+ new `OCR=1` frame-hunt mode for on-screen text). **Never ship with errors or blank pages.**

Banked laws: no manual DOM removal on React nodes · no GSAP pin:true · innerHTML only on empty JSX children · no AnimatePresence mode=wait for wizard steps · execFileSync timeout is ms · ScrollTrigger progress from captured instance · curl changed modules + JSX balance after every patch.

---

## 5. DATABASE (Phase 26, schema planned)

Supabase: `pickups` (id, user, items jsonb, kg, value, centre_id, slot, status, receipt_no) · `centres` (id, name, type[kabadi/recycler], hspcb_no, lat/lng, rate_kg, rating, area) · `receipts` (no, pickup_id, chain jsonb, photo_url) · `users` · `admin`. The wizard + centres + receipts already speak this language — wiring is swap-in.

---

## 6. THE MISSIONS (in parallel — see TASK2_FLASH3_MASTER V3)

- **Flash 3 (deadline 23 Aug):** answers DONE in `FLASH3_FINAL_ANSWERS.md` — submit NOW via Response Text. Divaa's video is now DELETED from YouTube → keep audio + screenshots as evidence.
- **Mission 2 (deadline 31 Aug):** Measure → Act → Measure Again. Physical checklist in TASK2_FLASH3_MASTER V3 (BEFORE photo+number, 2 neighbour talks, recycler call, weigh-day video, handover+₹40 receipt, AFTER photo+number, AGREEMENT photo). **Mission Password is VISUAL (on-screen in the M2 explainer)** — verified not in audio or description; Aarav watches the video (or commits the mp4 → our OCR frame-hunt finds it).
- **M2 physical evidence feeds the portfolio:** receipts #0003–25, the map's household dots, the proof room.

---

## 7. THE USER'S PART (always current)

1. Submit Flash 3 (paste from FLASH3_FINAL_ANSWERS.md) → screenshot confirmation.
2. Watch M2 explainer → find on-screen password → tell me (or commit the mp4).
3. Physical M2 evidence per checklist → commit photos/videos to `main`.
4. Say "continue!" per phase.
