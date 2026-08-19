# 🐝 VIKAAS — DEFINITIVE GOD-MODE BUILD PROMPT (v2.0)
### "The app that books e-waste pickup like food. Chaos into cash. Drawers into receipts."
> Give this file to any AI (Claude, ChatGPT, Gemini, Grok, Replit Agent, Qwen) as an attachment — or paste it — and say: *"Use this file as your prompt. Read it word by word. Build the VIKAAS portfolio to world-class, Awwwards-grade standards, then run your own self-review loop before showing me anything."*

---

# PART A — THE IDEA (fixed, non-negotiable)

**VIKAAS is an APP — like Swiggy/Zomato, but for e-waste.** Not a poster. Not a drive. Not a kabadiwala story. An app.

**The flow (the whole product, 4 taps):**
1. **OPEN THE APP** — list your dead devices (phone, charger, cable, speaker) or snap a photo; the AI estimates weight + value.
2. **BOOK A PICKUP** — pick a slot; the app routes your door to the nearest collection centre.
3. **WEIGH · PAY** — the centre (a kabadiwala or an authorised recycler, recruited by us) arrives, weighs in front of you, pays cash.
4. **RECEIPT** — a receipt with a chain of custody: door → collection partner → HSPCB-verified recycler → refiner.

**Market position:** exactly the ScrapUncle model (on-demand doorstep scrap pickup) BUT better:
- Dedicated to **e-waste only** (not mixed scrap)
- **AI features**: SCRAP-SCAN (photo → weight/value), ReBee chat assistant, live rate cards
- **Chain of custody** receipts to HSPCB-verified recyclers
- **Works where they aren't**: Gurugram, any quantity from 0.5 kg, doorstep weighing
- **USP one-liner: "Where others aren't — your door."**

**The proof (REAL, this is the portfolio's superpower vs competitors' fake screenshots):**
1.4 kg of dead electronics weighed on a kitchen scale · ₹40 paid cash at the door · 15 HSPCB govt-authorised recyclers sourced · 0 doorsteps served by them before us · 10/10 homes surveyed had a drawer · 500 kg minimum lot demanded by recyclers. **Every claim carries a stamp: WEIGHED / SOURCED / ESTIMATE / DRAMATISED / RECEIPT #N / THE GAP.**

---

# PART B — THE EXPERIENCE (screen by screen)

## 0. THE BOOT (`/boot`)
Auto-boot on load (no click). Terminal boot sequence → **3D scroll universe**: a massive interactive drawer that opens as you scroll, e-waste particles (chargers, phones, cables, batteries) tumbling out, national-scan vibes. Repeat visits: fast boot, SKIP override, prefers-reduced-motion fallback. Persistent `vikaas_intro_seen` key. The user LOVES this loader — never remove it.

## 1. THE GATE (`/`)
The pitch — the portfolio SELLS the app:
- **HERO**: 3D monolith + "VIKAAS विकास" SplitText choreography. Sub-line: *"The app that books e-waste pickup like food."* Stat chips (1.4 KG WEIGHED · ₹40 RECEIPT #1 · 15 RECYCLERS · 0 DOORSTEPS) + **TRY THE APP CTA in the hero**.
- **WHAT IS VIKAAS (01)**: "AN APP LIKE SWIGGY. FOR E-WASTE." — the 4-tap anatomy cards (OPEN → BOOK → WEIGH·PAY → RECEIPT) + USP line: *"Scrap apps exist. E-waste doorstep doesn't."* CTA: TRY THE APP.
- **CORE DIRECTIVE (02)**: one intelligent flow — drawer → doorstep → weighed → paid → receipted → verified recycler.
- **THE DRAWER NATION (03)**: 3.2M tonnes/yr · 22% recycled · 10/10 homes have a drawer.
- **THE STRUCTURAL GAP (04)**: 500 KG minimum vs 1.4 KG in a home · 15 recyclers : 0 doorsteps · ₹40 at the door.
- **THE APP'S 4 TAPS (05)**: OPEN → ESTIMATE → BOOK → WEIGH·PAY·RECEIPT (the pilot by hand was 1.4 kg/₹40).
- **THE IDEA in 4 moves**: discovery (weighed the problem) → gap (15/0) → method (weigh, earn, recycle) → goal (25 households → UN Geneva 20 Nov 2026).
- **THE BUILDERS (06)**: Aarav Choudhary + ReBee (capacitor body, phone-glass wings, charger-LED eyes, weighing-scale chest).
- Rooms grid → footer: NO DRAWER LEFT BEHIND.

## 2. THE DRAWER (`/drawer`)
The pilot story — pinned cinematic scroll (CSS sticky, NO GSAP pin), interactive 3D drawer toy that opens and reveals clickable e-waste items, each writing its real audit line, the scale sequence (1.4 kg), 15/0 map, the list.

## 3. THE APP (`/app`) — the centerpiece
Phone mock with **autoplaying 4-tap flow** (like NIRMAN's Forge): OPEN → WEIGH → VALUE → RECEIPT, crossfading with live fake UI, plus: how-it-works grid, the moat (we recruit the network), CTAs everywhere.

## 4. THE APP ROOMS
- `/app/book` — 4-step wizard (items → weight/estimate → slot/address → confirm) → **PICKUP BOOKED + RECEIPT #0002** (live, ₹8/kg).
- `/app/centres` — 8 collection centres (real HSPCB + kabadiwalas): capacity, pricing, rating, status + REGISTER YOUR CENTRE form.
- `/app/map` — self-contained SVG Gurugram map: 15 pulsing recycler dots + 10 household dots + click-to-route animated pickup line.
- `/app/receipts` — **PROOF LIBRARY**: RECEIPT #0001 (real: 1.4 kg · ₹40 · chain of custody), #0002 (live wizard), slots #0003–25 ("YOUR DRAWER IS #0003") + stamp legend + *"Some portfolios show screenshots of apps that don't exist. This one shows a receipt from a drawer that did."*
- `/app/assistant` — **REBEE AI chat**: working mock chat (chips → canned replies with typing indicator + stamps), 3 powers (SCRAP-SCAN / DOORSTEP DIAL / MATERIAL MATCH). *"That's the AI feature scrap apps don't have."*
- `/app/dashboard`, `/app/login`, `/app/admin` — operator side (Phase 17).

## 5. LATER ROOMS
THE PROOF (evidence vault) · THE KABADI UNIVERSE (the network as a room) · THE ARSENAL (6 reels + 22 posts + VO) · THE BUDDY (ReBee full room) · THE SYSTEM (engine room) · GENEVA (UN 20 Nov 2026) + 404.

---

# PART C — STYLE LAWS (every screen, every phase)

- **Awwwards-grade motion**: GSAP + ScrollTrigger + SplitType + Framer Motion + Lenis; Three.js for the monolith and drawer universe.
- **Glassmorphism** on dark void; acid green `#B9FF3F` + green `#2EDE82` + gold `#FFD34D`; Anton (Devanagari variant) display + Space Grotesk body + Noto Devanagari.
- **STAMPS ON EVERY CLAIM**: WEIGHED / SOURCED / ESTIMATE / DRAMATISED / RECEIPT #N / THE GAP — rotated bordered labels. Hinglish warmth: "kabhi kaam aayega", "drawer kholo", "receipts with taste".
- **NO DRAWER LEFT BEHIND** is the motto. Keep the loader. Keep the PageWipe acid curtain.
- **Proof over polish**: every number real, stamped, sourced — or labelled DRAMATISED/ESTIMATE. Never fake a receipt.

---

# PART D — TECH STACK

Vite 6 + React 19 + React Router 7 · GSAP + ScrollTrigger · Framer Motion · Lenis · Three.js + @react-three/fiber (optional) · Zustand (muted/progress state) · custom cursor v3 (blob + ring + canvas splash particles) · Web Audio (boot/enter/ambient wavs, hover blips, mute toggle) · tokens.css design system · no Tailwind (hand-rolled CSS, tokens).

---

# PART E — THE QA LAW (the definition of done)

1. **COMPILE**: every route module, css, font, audio asset returns 200 (curl).
2. **RENDER**: `<main>` exists, ≥4 fonts loaded, scrollHeight > viewport (no empty pages).
3. **BLANK**: viewport screenshot luminance std ≥ 8 (no black/blank pages).
4. **CONSOLE**: 0 pageerrors / 0 console errors / 0 failed requests (headless Chromium).
5. **JSX BALANCE**: open == close sections in every page file.
6. **CLICKS**: menu opens, every link navigates, CTAs clickable (headless).
7. **EYES 2.0**: OCR every new screen (tesseract, dark-mode preprocessing), verify the actual rendered text says what the design says; ASCII/vision-desc checks on every new layout.
8. **Never ship with errors or blank pages.** Fix, re-verify, then show.

**Banked bug laws:** never manually remove/replace React-managed DOM · no GSAP `pin:true` (use CSS sticky) · `innerHTML` targets must have empty JSX children · no `AnimatePresence mode="wait"` for wizard steps · `execFileSync` timeout is milliseconds · read ScrollTrigger progress from the captured instance · curl the changed module + JSX-balance after every patch.

---

# PART F — THE MISSIONS (what the portfolio feeds)

**Flash Challenge #3 (deadline 23 Aug)** — answers ready in `FLASH3_FINAL_ANSWERS.md` (Forbes 30-under-30 method · Divaa's "intentional YOLO" · the 1.4-kilogram question). Divaa's video is deleted from YouTube — audio + screenshots are the evidence.

**Mission 2 (deadline 31 Aug)** — Measure → Act → Measure Again with physical evidence (BEFORE/AFTER photos + same-method numbers, conversations, weigh-day video, handover + ₹ receipt, continuation agreement). The **Mission Password is VISUAL** — on-screen in the M2 explainer (not in audio, not in the description). The receipts #0003–25 and map household dots in the portfolio ARE the Mission 2 evidence trail.

**The end goal:** Top 3 → 1M1B Impact Summit, UN Geneva, **20 Nov 2026**. The portfolio is the weapon. Build it like the prize is already yours — because receipts beat screenshots, every single time.
