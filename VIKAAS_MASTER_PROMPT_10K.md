# BUILD VIKAAS — MASTER BRIEF (read all, then build without questions)

## 1. MISSION
Build VIKAAS (विकास) — an award-level portfolio+product-pitch for an e-waste collection initiative. TWO jobs: (1) TELL the idea as a complete product narrative like NIRMAN's (nirmaan-portfolio-main.vercel.app — study all 16 sections: boot gate, hero, directive, problem data, structural gaps, pipeline, map, AI, custody, analytics, architecture, roadmap, founders), (2) PROVE it REAL — unlike NIRMAN's screenshots+marketing, we have real receipts. Every claim wears a stamp.

IDEA (lead everywhere): Every Indian home has a drawer of dead electronics. Recyclers exist — govt-authorised, waiting. What's missing is the doorstep. VIKAAS closes the gap: open drawer → weigh (real kitchen scale) → know value (₹40, real) → hand to network (kabadi + authorised recyclers) → get stamped receipt. "The infrastructure isn't missing. THE DOORSTEP IS." Proven: 1.4 kg weighed. Mission: NO DRAWER LEFT BEHIND. From one Gurugram drawer to UN Geneva, 20 Nov 2026 (1M1B Impact Summit).

REAL RECEIPTS (stamp each): 1.4 kg drawer (WEIGHED, photo) · ₹40 cash (RECEIPT #0001) · 15 HSPCB recyclers Gurugram (SOURCED) · 0 doorsteps (THE GAP) · 10/10 homes surveyed (OUR SURVEY) · 3.2M t/yr India e-waste, 22% reaches recyclers (SOURCED) · 500 kg recycler minimum (BULK-ONLY) · 3 phones/7 chargers/1 speaker 2022 (WEIGHED) · 25 households target (THE PLAN).

## 2. BRAND
Palette: ink #040605, ink2 #0a0f0c, paper #EFE9DC, dew #EAFFF4, acid #B9FF3F (primary), green #2EDE82, red #FF4D5E, gold #FFD34D, violet #A78BFA, mute #4c5851, line #16201a.
Fonts (self-host, never CDN): Anton (display caps), Space Grotesk (mono/HUD), Noto Sans Devanagari (विकास/री-बी).
STAMPS = identity: rotated −4°, 2px border, ink bg — WEIGHED(green) SOURCED(green) ESTIMATE(violet) DRAMATISED(violet) RECEIPT #N(gold) THE GAP(red). Slam-in spring.
Glass: linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.015)) + border rgba(255,255,255,.12) + blur(20px) saturate(150%) + inset highlight + sheen sweep.
Motion: hits = cubic-bezier(.34,1.56,.64,1); cinematic = .76,0,.24,1; reveals power3.out; stagger .04–.08s. Scroll = narrative.
Voice: Hinglish + receipts. Never hype without a stamp.

## 3. STACK
Vite6 + React19 + Router7 + GSAP/ScrollTrigger + Lenis + Framer Motion + Three/R3F/drei/postprocessing + split-type + zustand + clsx. DB: Supabase (Postgres+Auth+Storage+RLS) OR Node/Express+SQLite. Map: MapLibre/Leaflet+OSM. Charts: Recharts. QR: qrcode.react. Deploy: Vercel + Supabase.

## 4. PAGES (30+; all render, never blank, error-boundary, reduced-motion+touch+a11y safe)
Portfolio: /boot (auto-boot ~10s: terminal types 7 lines — drawer scan/1.4KG/10 homes/15 recyclers/0 doorsteps/ReBee/NO DRAWER LEFT BEHIND — status INITIALISING→READY, wordmark scramble+glitch, then scroll-universe: 3D drawer lid flips UP, light spill, e-waste floats/orbits, chapters IGNITION→THE DOOR, stats slam+stamps, ReBee fly-by, ENTER→wipe; SKIP+?fast=1; ambient bed after gesture) · / (GATE: full pitch — 3D e-waste monolith hero w/ parallax + VIKAAS char-slam + 4 chips; CORE DIRECTIVE; DRAWER NATION (3.2M/22%/10of10 count-ups); STRUCTURAL GAP (500kg/1.4kg/15:0/₹40 cards); 4-TAP FLOW (DRAWER KHOLO→SCALE PAR RAKHO→LIST KHOLO→PHOTO+DROP + ₹40 receipt + "imagine it as an app—that's VIKAAS" + CTA /app); IDEA 4 moves (DISCOVERY/GAP/METHOD/GOAL); MANIFESTO blur-lines "THE DOORSTEP IS."; ROOMS grid (expandable spotlight+tilt+magnet); BUILDERS (Aarav + ReBee); GENEVA finale) · /drawer (intro THE/DRAWER stagger; pinned story: photo clip-open, 4 truth lines, 15/0 slam; TOY v2: 3D drawer opens, items float, tap→holographic SCRAP-SCAN card: value ₹ + real recycler (Exigo Manesar/EcoMetals Gurugram/Cerebra HITEC/Attero Noida/E-Parisaraa Peenya) + stamp; scale sequence: needle→1.4kg→receipt; 15/0 map; list) · /proof (receipt printer line-by-line+stamps; elastic scale 500vs1.4 "SHORT BY 498.6KG"; magic bento 8 stats; dotgrid 3.2M/22% warp; sources) · /kabadi (tier list S-F showdown; ₹40 handshake loop; lore cards horn/bicycle/scale; 4 network roles; dual marquees) · /arsenal (glass dock; 6 reel cards hover-play+lightbox; 22-post FLIP masonry w/ M/P/R filters; audio lab waveforms) · /buddy (galaxy sky; ReBee tilt card; playable SCRAP-SCAN hologram; 3 powers; parade) · /system (timeline from logbooks; terminal typing real pipeline commands; QA-gate viz; imagetrail; threads) · /geneva (road: drawer→M1✓→M2✓→Top500→Top100→Showdown→GENEVA 20NOV, fills on scroll; pledge) · /type (styleguide) · /about · /404 (lost drawer) · /privacy /terms.
App: /app (hero "BOOK A PICKUP. WEIGH. EARN. RECYCLE." + phone mock + CTA) · /app/book (4-step wizard: items+photo→weigh+live ₹estimate→address+slot→confirm→pickup row + draft receipt QR) · /app/centres (roster + REGISTER YOUR CENTRE form — the moat) · /app/map (households dots + centre pins + route) · /app/receipts (proof library, print/share) · /app/assistant (ReBee chat: value/nearest centre/book, no API key) · /app/dashboard (ledger: kg diverted, ₹ paid, pickups, top centres) · /app/login (Supabase email+Google) · /app/admin (centre admin: accept/complete pickups, generate receipts).

## 5. DATABASE (Supabase SQL)
households(id uuid pk default gen_random_uuid(), user_id ref auth.users unique, name, phone, city default 'Gurugram', created_at)
centres(id pk, name not null, type check in('kabadiwala','recycler','both'), area, lat float, lng float, capacity_kg int default 100, pricing_per_kg numeric default 8, rating numeric default 5, verified bool default false, status text default 'pending', contact, created_at)
pickups(id pk, household_id ref, centre_id ref, items jsonb default '[]', kg numeric, est_value numeric, address, lat, lng, slot timestamptz, status text default 'pending', photo_url, receipt_no, created_at)
receipts(id pk, pickup_id ref, household_id ref, centre_id ref, kg, cash_paid, recycler_name, stamp default 'WEIGHED', qr, created_at)
impact_log(id pk, kg_diverted numeric, cash_paid numeric, pickup_id, created_at)
Seed: 15 HSPCB recyclers as centres; impact_log(1.4,40). RLS: household own rows, centre own pickups, admin all.

## 6. FX LIBRARY (reusable components)
TextScramble · BlurText · SplitReveal (revert-safe) · GlitchText · SpotlightCard · TiltCard · Magnet · ClickSpark · PixelTransition · CountUp · Aurora/Nebula · Particles · Hyperspeed · DotGrid · LetterGlitch · FlipIn · Marquee · Waveform · ReceiptPrinter · ScaleToy. All reduced-motion/touch safe, cleanup on unmount, token-driven, 0 console errors.

## 7. AUDIO
WebAudio ctx unlocked on first gesture. Hover blips, whoosh on transitions, click ticks. Ambient beds per room (generated, ~−18 LUFS, ≤30s loop, muted default). Mute toggle (zustand, persists). Ear-check at end.

## 8. CONTENT (paste-ready)
Hero chips: 1.4KG WEIGHED · ₹40 RECEIPT#1 · 15 SOURCED · 0 THE GAP. Manifesto: "The drawer waited four years. Ten homes asked. Ten drawers found. The infrastructure isn't missing. THE DOORSTEP IS." Taps: DRAWER KHOLO/SCALE PAR RAKHO/LIST KHOLO/PHOTO+DROP. Idea: DISCOVERY (nobody ever weighed the problem)/GAP (15/0, 500kg min)/METHOD (weighed, not guessed)/GOAL (25 households→UN). Builders: Aarav "the changemaker who weighed his drawer" + ReBee (री-बी) "built from the problem he solves". Finale: "NO DRAWER LEFT BEHIND. One drawer. One recycler. One cleaner India." Hinglish: "कभी काम आएगा" · "kuch kaam ka cheez" · "no returns on evidence". Assets in repo ANONYMUS-co986/Goop branch arena/019ff044-goop (vikaas-hq/): reels V1-V6, posts M1-8/P1-6/R1-8, ReBee art, fonts, audio.

## 9. QA LAW (never skip)
1 Compile: every module 200. 2 Render: main+fonts≥4+h>viewport. 3 Blank: screenshot std≥8. 4 Console: 0 errors/0 failed reqs. 5 JSX balance: <section> open==close. 6 Click gate: menu+all links clickable desktop+mobile. 7 NEVER manually remove/replace React-managed DOM — state+CSS only (sticky over pin, conditional render over remove()). 8 Curl changed module after every patch. 9 Commit after every phase. 10 Build verify_all.sh script, run before handoff.

## 10. BUILD ORDER (gate each)
1 Foundation+tokens+gate · 2 Shell+wipe+Lenis · 3 Boot · 4 Gate · 5 Drawer · 6 Proof · 7 Kabadi+Arsenal · 8 Buddy+System+Geneva · 9 Type/About/404/Legal · 10 Supabase+schema+auth · 11 Book+Centres+Map · 12 Receipts+Assistant+Dashboard+Admin · 13 Sound+perf · 14 SEO/a11y+boundaries · 15 Launch+walkthrough+handoff.

## 11. DEPLOY + HANDOFF
Vercel (env VITE_SUPABASE_URL/ANON_KEY) + Supabase. Deliver: URL+admin login, walkthrough video, QA report all ✅, posting kit link, "go cry to every other website" reel.

## 12. DON'TS + FINAL CHECKLIST
Don't: CDN assets (self-host), fake numbers (stamp or ESTIMATE/DRAMATISED), manual DOM surgery, console errors, clutter, dropping the loader, forgetting Devanagari fallback, shipping un-gated pages.
Checklist: 30+ routes render 0 errors · full narrative present · app E2E (signup→book→centre completes→receipt→dashboard) · SCRAP-SCAN playable · 6 reels+22 posts hover-play · audio+ear-check · mobile 390px + reduced-motion · OG/sitemap/manifest · admin sees real data · finale reel exists.
