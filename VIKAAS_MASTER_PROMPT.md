# 🤖 MASTER PROMPT — BUILD VIKAAS: THE MAXIMUS PORTFOLIO + APP

> **Give this entire document to Claude (or any capable coding agent) as ONE prompt.
> It is fully self-contained: the idea, the design system, 30+ defined pages, the
> database, the animations, the content, the QA law, the build order. Do not ask
> the user questions — everything you need is here. Build it.**
>
> Source repo (reference + assets): `github.com/ANONYMUS-co986/Goop`
> (branch `arena/019ff044-goop` — contains `vikaas-hq/` with all art, reels,
> posts, audio, logbooks, and a working Vite app at `vikaas-hq/v2-app/`).
> Study the existing app, then rebuild it to THIS spec (bigger, better, with
> everything added here — including the database and app routes).

---

## PAGE 1 — THE MISSION (read first, never forget)

Build **VIKAAS (विकास)** — the most impressive, award-level **portfolio + product
pitch** for an e-waste collection initiative. It has TWO jobs:

1. **TELL THE IDEA** the way NIRMAN's portfolio tells his — as a complete
   product narrative (problem → gap → pipeline → proof → AI → roadmap). Every
   section of the story must be on the site.
2. **PROVE THE IDEA IS REAL** — unlike NIRMAN (which sells screenshots and
   marketing claims), VIKAAS has **real receipts**: a drawer actually weighed,
   money actually earned, recyclers actually found. Every claim is stamped.

**The idea in one paragraph (lead with this everywhere):**
> Every Indian home has a drawer of dead electronics. The recyclers exist —
> government-authorised, licensed, waiting. What's missing is the doorstep.
> **VIKAAS is the door-to-door e-waste flow that closes the gap:** open the
> drawer → weigh it (real kitchen scale) → know what it's worth (₹40, real) →
> hand it to the network (kabadi + authorised recyclers) → get a receipt
> (stamped, real). The infrastructure isn't missing. **The doorstep is.**
> And we proved it. Mission: **NO DRAWER LEFT BEHIND.** From one drawer in
> Gurugram to the 1M1B Impact Summit at the United Nations — 20 Nov 2026.

**THE REAL RECEIPTS (use these exact numbers, stamp every one):**
| Fact | Stamp |
|---|---|
| 1.4 kg — what our drawer weighed (kitchen scale, photographed) | WEIGHED |
| ₹40 — cash earned at the gate (real) | RECEIPT #0001 |
| 15 — government-authorised recyclers in Gurugram (HSPCB public list) | SOURCED |
| 0 — doorsteps served by them (the gap) | THE GAP |
| 10/10 — homes we surveyed had the same drawer | OUR SURVEY · REAL |
| 3.2M tonnes — India's e-waste per year (CWC track page) | SOURCED |
| 22% — only this much reaches authorised recyclers | SOURCED |
| 500 KG — a recycler's minimum lot (we called) | BULK-ONLY |
| 3 phones · 7 chargers · 1 speaker (2022) — our drawer's inventory | WEIGHED |
| 25 households — our M2 target, every device weighed+logged+delivered | THE PLAN |

---

## PAGE 2 — THE COMPETITOR (study it, then beat it)

**Study:** `https://nirmaan-portfolio-main.vercel.app/` — read ALL 16 sections.

What NIRMAN does well (match this): a boot-gate entrance · terminal/HUD
aesthetic · numbered chapters (01–16) · every section explains the product
(problem data, structural gaps, 5-tap pipeline, live map, AI brain, chain of
custody, analytics, architecture, roadmap, founders) · consistent dark-tech
design language · "launch" CTA at the end.

What NIRMAN fakes (beat this with truth): screenshots instead of working
proof · "0.0 kg diverted" (nothing real) · marketing claims (blockchain,
100% accuracy) · a roadmap that's a pitch deck.

**Your mandate:** build the SAME narrative completeness, with REAL proof.
Where NIRMAN says "concept", you say "1.4 kg, weighed, photographed."
Where he shows a screenshot, you show an interactive demo.
Where he claims, you stamp (WEIGHED / SOURCED / ESTIMATE / DRAMATISED).

---

## PAGE 3 — THE BRAND SYSTEM (fixed, use only this)

**Name:** VIKAAS (विकास) — "development / growth". Tagline: **"receipts with
taste."** Mission line: **"NO DRAWER LEFT BEHIND."**

**Palette:**
```
--ink:#040605 (near-black, bg)  --ink2:#0a0f0c
--paper:#EFE9DC (cream, display text)   --dew:#EAFFF4 (body text)
--acid:#B9FF3F (primary accent — the brand color)
--green:#2EDE82 (secondary accent — "weighed/verified")
--red:#FF4D5E (the 0 / the gap / warnings)
--gold:#FFD34D (the ₹40 / receipts)
--violet:#A78BFA (ReBee / AI)
--mute:#4c5851  --mute2:#7d867f  --line:#16201a  --line2:#1d2622  --line3:#24302a
```

**Fonts (self-hosted, never CDN):** Anton (display, uppercase, tight) ·
Space Grotesk (mono/HUD/labels) · Noto Sans Devanagari (विकास, री-बी).

**The Stamp System (THE identity):** every claim wears a rotated stamp —
`WEIGHED` (green) · `SOURCED` (green) · `ESTIMATE` (violet) · `DRAMATISED`
(violet) · `RECEIPT #N` (gold) · `THE GAP` (red). Stamps slam in with a
spring, rotate −4°, border-2px, ink background.

**Glass recipe:** `linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.015))`
+ border `rgba(255,255,255,.12)` + `backdrop-filter:blur(20px) saturate(150%)`
+ inset top highlight + deep shadow + sheen sweep animation.

**Motion language:** display hits = `cubic-bezier(.34,1.56,.64,1)` (spring) ·
cinematic = `cubic-bezier(.76,0,.24,1)` · reveals = `power3.out` · staggers
0.04–0.08s · durations 0.5–1.1s. Scroll = the narrative device.

**Voice:** Hinglish warmth + receipt-grade precision. Never hype without a
stamp. The humour is self-aware ("kuch kaam ka cheez", "0 words used").

---

## PAGE 4 — THE STACK (the full modern arsenal)

**Frontend:** Vite 6 + React 19 + React Router 7 · TypeScript optional but
encouraged · GSAP + ScrollTrigger (scroll choreography) · Lenis (smooth scroll)
· Framer Motion (micro-interactions, AnimatePresence exits) · Three.js +
@react-three/fiber + drei + postprocessing (3D scenes, bloom/glitch) ·
split-type (char splitting) · zustand (state: audio/UI) · clsx.

**The database & backend (THIS is the part that takes it beyond a portfolio — build it):**
- **Supabase** (free tier) — Postgres + Auth + Storage + Realtime. OR a
  self-hosted **Node/Express + SQLite** if you prefer zero-config.
- **Tables** (full schema in Page 26): households, pickups, centres,
  kabadiwalas, recyclers, receipts, messages, impact_log.
- **Auth:** email + Google OAuth (Supabase handles it).
- **Image upload:** device photos → Supabase Storage.
- **Why:** the portfolio's "Book a pickup" CTA should feed a REAL database —
  the visitor can actually submit a pickup request; the owner sees it in a
  dashboard. THAT is the proof NIRMAN can't fake.

**Map:** MapLibre GL (open) or Leaflet + OpenStreetMap tiles (no API key).
**Charts:** Recharts (analytics). **QR:** qrcode.react (receipts).

**Deploy:** Vercel (frontend) + Supabase (db) — both free. Custom domain.

---

## PAGE 5 — THE ARCHITECTURE

```
src/
├── main.jsx / App.jsx        routes + PageWipe + Lenis + providers
├── shell/                    Shell.jsx (nav/cursor/HUD/progress/mute) + shell.css
├── lib/
│   ├── tokens.css            THE design source of truth
│   ├── fx.css                effect styles
│   ├── sound.js              WebAudio blips/whoosh (muted-gated)
│   ├── db.js                 Supabase client + typed helpers
│   ├── hooks/                useLenis, useReveal, useCountUp, useScrollProgress
│   └── fx/                   TextScramble, BlurText, SplitReveal, GlitchText,
│                             SpotlightCard, TiltCard, Magnet, ClickSpark,
│                             PixelTransition, CountUp, Aurora, Nebula,
│                             Particles, Hyperspeed, DotGrid, LetterGlitch
├── components/               Monolith (3D drawer), ReceiptPrinter, ScaleToy,
│                             FlowSteps, NetworkMap, ScrapScan, AudioLab,
│                             ReelCard, Dock, Masonry, BentoGrid, RoadToGeneva
├── pages/                    (30+ pages — Page 6 onwards)
└── assets/                   fonts, img, audio (self-hosted)
public/                       og-image, favicon, robots, manifest
supabase/                     migrations (schema SQL)
```

**Every route must:** render instantly · never blank (error boundary) ·
prefers-reduced-motion safe · touch safe · keyboard accessible.

---

## PAGE 6 — THE 30+ PAGES (overview)

| # | Route | Page | Type |
|---|---|---|---|
| 00 | /boot | THE BOOT — auto-boot → scroll universe | cinematic loader |
| 01 | / | THE GATE — the full narrative pitch | portfolio |
| 02 | /drawer | THE DRAWER — origin story + interactive toy | portfolio |
| 03 | /proof | THE PROOF — receipts, scale, analytics | portfolio |
| 04 | /kabadi | THE KABADI UNIVERSE — the network | portfolio |
| 05 | /arsenal | THE ARSENAL — reels, posts, audio | portfolio |
| 06 | /buddy | THE BUDDY — ReBee, the AI buddy | portfolio |
| 07 | /system | THE SYSTEM — the making-of | portfolio |
| 08 | /geneva | GENEVA — the roadmap to the UN | portfolio |
| 09 | /type | THE TYPE — the living styleguide | meta |
| 10 | /app | THE APP — product home (download/launch CTA) | app |
| 11 | /app/book | BOOK A PICKUP — the wizard | app |
| 12 | /app/centres | COLLECTION CENTRES — the roster | app |
| 13 | /app/map | THE NETWORK MAP — live | app |
| 14 | /app/receipts | MY RECEIPTS — the proof library | app |
| 15 | /app/assistant | REBEE ASSISTANT — the AI chat | app |
| 16 | /app/dashboard | THE LEDGER — impact analytics | app |
| 17 | /app/login | LOGIN / SIGN UP | app |
| 18 | /app/admin | CENTRE ADMIN — manage requests | app |
| 19 | /about | THE BUILDER — Aarav + ReBee | portfolio |
| 20 | /404 | THE LOST DRAWER | fun |
| 21 | /privacy · /terms | legal | meta |
| 22+ | /app/… | deep routes (pickup/:id, centre/:id, receipt/:id) | app |

Each page is specced below with: purpose · sections · animations ·
interactions · content · data.

---

## PAGE 7 — PAGE 00: THE BOOT (the entrance)

**Purpose:** the beloved entrance — a ~10s automated boot, then the user scrolls
a 3D universe.

**Phase A — AUTO BOOT (~10s):** full-screen glass card over a nebula;
a terminal TYPES these lines char-by-char (cursor blinks, progress bar, status
label flips INITIALISING→SCANNING→WEIGHING→VERIFYING→SUMMONING→READY):
```
scanning drawer inventory — 3 phones · 7 chargers · 1 speaker (2022)
weighing … 1.4 KG — receipt logged
surveying 10 homes … 10/10 have the same drawer
querying HSPCB registry … 15 authorised recyclers found
doorsteps served … 0
summoning ReBee … scrap-scan online
mounting universe … NO DRAWER LEFT BEHIND
```
Then VIKAAS wordmark SCRAMBLES in (matrix chars → settle) with glitch bursts;
"READY." flashes; overlay slides up in acid revealing the 3D stage.
SKIP button + `?fast=1` for repeat visits. Ambient audio bed (deep pad + clock
ticks + sub pulse) starts on first gesture.

**Phase B — SCROLL UNIVERSE (pinned, scroll-scrubbed):** a 3D drawer (Three.js)
— lid FLIPS UP (rotation −1.95, pivot at back edge), light spill ignites,
e-waste floats out and orbits (phone/cables/battery/charger/PCB — code-built),
dust particles, reflective grid. Chapters synced to progress: IGNITION →
THE OPEN → THE WORD → THE PROOF → THE FLIGHT → THE LINE → THE DOOR.
VIKAAS scramble-assembles char-by-char; stats slam (1.4 KG / ₹40 / 15 / 0)
with stamps; **ReBee flies across the sky**; "NO DRAWER LEFT BEHIND."
reveals char-staggered; ENTER THE DRAWER pill → acid wipe → /.

**Animations:** terminal typing · char scramble · glitch · lid-up · light spill
· item float+spin · stats slam · ReBee fly-by · char-stagger line · pulse-glow
· scan sweep · rail + % · dust canvas.

**QA:** boot route PASS desktop+mobile+fast. Zero console errors.

---

## PAGE 8 — PAGE 01: THE GATE (the full narrative pitch)

**Purpose:** the one-page product pitch — NIRMAN's 16 sections, our truth.
Chapter-marked (sticky chapter nav + progress bar along the right).

**Sections in order:**
1. **HERO** — 3D e-waste monolith (the drawer as a glowing monolith over a
   reflective grid, orbiting e-waste particles, mouse parallax, scroll-reactive
   camera) + VIKAAS char-slam + विकास pop + 4 proof chips (1.4 KG WEIGHED ·
   ₹40 RECEIPT #1 · 15 SOURCED · 0 THE GAP) + scroll cue.
2. **CORE DIRECTIVE** — "Every drawer hides dead electronics… VIKAAS connects
   drawer → kabadi network → authorised recycler → impact — one weighed,
   receipted flow. Not a concept. A drawer we actually opened."
3. **THE DRAWER NATION** — the problem: 3.2M tonnes/yr (SOURCED) · only 22%
   reaches recyclers (THE REST BURNS) · 10/10 homes surveyed (OUR SURVEY ·
   REAL). Count-up stats. "Nobody knows where to go."
4. **THE STRUCTURAL GAP** — 500 KG (BULK-ONLY) · 1.4 KG (WEIGHED) · 15:0
   recyclers:doorsteps (the glowing hero card) · ₹40 (THE NETWORK). "The
   infrastructure isn't missing. The doorstep is. Connect them — that's the app."
5. **THE 4-TAP FLOW** — DRAWER KHOLO → SCALE PAR RAKHO → LIST KHOLO → PHOTO +
   DROP — four interactive cards + the ₹40 receipt stamp. "Now imagine it as
   an app… That's VIKAAS." + **CTA: "TRY THE APP →" (to /app)**.
6. **THE IDEA — four moves** (DISCOVERY / GAP / METHOD / GOAL) — the manifesto
   cards with stamps.
7. **THE MANIFESTO** — blur-reveal lines: "The drawer waited four years. Ten
   homes asked. Ten drawers found. The infrastructure isn't missing.
   THE DOORSTEP IS."
8. **THE ROOMS GRID** — the 9 rooms (boot/gate/drawer/proof/kabadi/arsenal/
   buddy/system/geneva) as expandable SpotlightCards with tilt + magnet +
   status badges.
9. **THE BUILDERS** — Aarav Choudhary (the changemaker who weighed his drawer)
   + ReBee (री-बी) with art + stamps.
10. **GENEVA FINALE** — gradient "NO DRAWER LEFT BEHIND." + roadmap CTA +
    Instagram links + replay boot.

**Animations:** monolith parallax · SplitReveal · BlurText · count-ups ·
spotlight cards · tilt+magnet · blur-reveal manifesto · scroll-jacked stats.

---

## PAGE 9 — PAGE 02: THE DRAWER (the origin room)

**Purpose:** the story + the playable audit.
1. **Intro hero** — giant "THE / DRAWER" line-stagger + glow + sub + cue.
2. **PINNED STORY** (CSS sticky scrub) — the real drawer photo clip-opens with
   ken-burns; truth lines land one-by-one ("The drawer had been waiting four
   years." / "Inside — 1.4 kg of 'kuch kaam ka cheez'." / "Ten homes asked.
   Ten drawers found." / "Not one could name a single authorised recycler.");
   "15 RECYCLERS. 0 DOORSTEPS." slams (15 green / 0 red); kicker. Story
   progress rail on the left edge.
3. **THE DRAWER TOY v2** — a 3D drawer that clicks open (front panel flips up,
   items float out staggered); **tap any item → holographic spec card**:
   SCRAP-SCAN · LIVE tag, item name + audit line, VALUE (real estimate) +
   RECYCLER match (real HSPCB names: Exigo Manesar · EcoMetals Gurugram ·
   Cerebra HITEC City · Attero Noida · E-Parisaraa Peenya) + stamp.
4. **THE SCALE SEQUENCE** — scroll-driven weighing: needle swings → settles at
   1.4 KG → receipt prints. SVG needle + spring settle + stamp slam.
5. **THE 15/0 MAP** — stylized Gurugram map (SVG): 15 pulsing recycler dots, 0
   doorstep markers, "the gap" callout, HSPCB source line.
6. **THE LIST** — 500 KG / 1.4 KG / 498.6 KG gap cards + CTA to /proof and /app.

---

## PAGE 10 — PAGE 03: THE PROOF (the receipts room)

1. **RECEIPT PRINTER** — the paper prints line-by-line on scroll (clip-path +
   typewriter): items (3 phones · 7 chargers · 1 speaker · 10 homes) → TOTAL
   EVIDENCE 1.4 KG · CASH ₹40 · WORDS 0 → stamps slam (WEIGHED / SOURCED /
   ESTIMATE / DRAMATISED) → "no returns on evidence."
2. **THE ELASTIC SCALE** — interactive physics slider: 500 KG (recycler min)
   vs 1.4 KG (ours) with count-up + verdict gag "SHORT BY 498.6 KG — SO WE
   STARTED THE DRAWER REVOLUTION."
3. **MAGIC BENTO STATS** — 8 evidence cells (3 phones · 7 chargers · 1 speaker
   · 10 homes · 1.4 KG · ₹40 · 15 recyclers · 0 doorsteps) with Spotlight +
   CountUp + hover expansion.
4. **DOTGRID VIZ** — 3.2M tonnes / 22% animated dot matrix with cursor warp.
5. **SOURCES** — HSPCB list + CWC track stats, cited, stamped.

---

## PAGE 11 — PAGE 04: THE KABADI UNIVERSE (the network room)

1. **TIER-LIST SHOWDOWN** — animated S→F cards (S: कबाड़ीवाला 👑 · A: repair
   bhaiya · B: authorised recycler · C: drawer hoarding · F: dustbin).
   Flip-in + tilt + glare. Disputes CTA ("weigh your drawer before you type").
2. **THE ₹40 HANDSHAKE** — looping scroll-scrubbed micro-animation (cash →
   cables → handshake) with the receipt.
3. **LORE CARDS** — the horn, the bicycle, the scale (Flip-in + Spotlight).
4. **THE NETWORK ROLES** — 4 roles (household · kabadiwala · recycler · ReBee)
   — who does what in the flow.
5. **DUAL MARQUEES** — opposing-speed tickers.

---

## PAGE 12 — PAGE 05: THE ARSENAL (the output room)

1. **GLASS DOCK** — macOS-style magnifying dock for the 6 reels.
2. **REEL CARDS** — poster frames + GlareHover + hover-play video + click →
   lightbox (player + caption + "use this sound" + stamp). Keyboard/Esc.
3. **THE 22-POST WALL** — masonry with FLIP animations + filter chips
   (M memes / P posters / R remixes) + hover zoom.
4. **AUDIO LAB** — A/B phonk players + canvas waveform visualization (the
   "we make our own music" flex). Mute toggle.

**The 6 reels (real, in the repo):** V1 THE DRAWER · V2 15 RECYCLERS 0
DOORSTEPS · V3 KABADI PARADOX · V4 COMEDY CLUB · V5 DOORSTEP PHONK · V6
MEME-REEL. Post assets M1–M8, P1–P6, R1–R8 (all in `studio/drops/FINALE/`).

---

## PAGE 13 — PAGE 06: THE BUDDY (ReBee, the AI room)

1. **GALAXY/HYPERSPEED SKY** — canvas star-warp background with mouse
   repulsion.
2. **REBEE HERO** — TiltedCard 3D + glare + parallax layers (art:
   `cwc_buddy/art/rebee_hero_v6_FINAL.png` — the research-backed hero).
3. **PLAYABLE SCRAP-SCAN** — click any device (phone/charger/battery/PCB) →
   hologram scan-line sweeps over it → tag card pops: contents, ₹ value,
   nearest recycler. THE interactive superpower.
4. **THE 3 POWERS** — SpotlightCards: SCRAP-SCAN · DOORSTEP DIAL · MATERIAL
   MATCH (each with the film-anchored explanation — "Four ways AI can help
   tackle climate change": satellite-AI→scan, traffic-AI→routing,
   materials-AI→match).
5. **CHARACTER PARADE** — the 6 ReBee art variants in a scroll-stack.
6. **MISSION** — "NO DRAWER LEFT BEHIND." + the Q2/Q3 submission answers as
   the "origin file" (the CWC flash-challenge entry).

---

## PAGE 14 — PAGE 07: THE SYSTEM (the making-of room)

1. **THE TIMELINE** — the campaign condensed from the logbooks: drawer weighed
   → 10 homes → 15 recyclers → ReBee art → 6 reels → 22 posts → the site.
   Scroll-jacked reveals, real dates.
2. **THE TERMINAL** — a terminal window that TYPES the real pipeline commands
   (the studio's actual render/encode/suite commands) — "this site was built
   with a machine."
3. **THE QA GATE VISUAL** — show the verify_all.sh gate: compile → render →
   blank → console → clicks → 20/20 PASS. The rigor as a feature.
4. **IMAGETRAIL** — cursor-following images of the QA screenshots.
5. **THREADS VIZ** — canvas flowing lines = the studio pipelines.

---

## PAGE 15 — PAGE 08: GENEVA (the roadmap room)

1. **THE ROAD TO GENEVA** — animated route: drawer → M1 PLEDGE ✓ → M2 ACT ✓
   (ReBee submitted) → TOP 500 → TOP 100 → CITY SHOWDOWN → **GENEVA · UN ·
   20 NOV 2026**. Progress line fills on scroll; each stop reveals + stamps.
2. **THE FINALE CTA** — giant "NO DRAWER LEFT BEHIND." + "Open your drawer
   today." → links to /app/book and Instagram.
3. **THE PLEDGE** — "25 households. Every device weighed, logged, delivered."

---

## PAGE 16 — PAGES 09 & 19–21: TYPE · ABOUT · 404 · LEGAL

- **/type** — the living styleguide: full type scale, fx demo grid, stamps,
  glass, tokens. (A styleguide page is an award-site flex.)
- **/about** — the builder: Aarav Choudhary (real story: 4-year-old drawer,
  1.4 kg, 10 homes, 15 recyclers, ReBee, CWC track) + ReBee origin + the
  integrity gate ("every number stamped or sourced").
- **/404** — "THE LOST DRAWER" — playful (a drawer with one stray charger),
  links back to / and /boot.
- **/privacy · /terms** — clean, short, real.

---

## PAGE 17 — PAGE 10: THE APP HOME (/app)

**Purpose:** the product landing — this is where the portfolio becomes a
product. Sections:
1. **Hero** — "BOOK A PICKUP. WEIGH. EARN. RECYCLE." + app-store-style mock
   (phone frame with the 4-tap flow animated inside) + CTA "START A PICKUP".
2. **How it works** — the 4 taps, each with a micro-demo.
3. **For households** — doorstep pickup, cash at the gate, receipt proof.
4. **For collection centres** — "REGISTER YOUR CENTRE" (the moat: kabadiwalas
   + recyclers onboard; the roster in /app/centres).
5. **Impact so far** — LIVE numbers from the database (kg diverted, ₹ paid,
   pickups, centres).
6. **CTA** — /app/book + /app/login.

---

## PAGE 18 — PAGE 11: BOOK A PICKUP (/app/book) — the wizard

A 4-step wizard (each step animated, progress rail, back/next, validation):
1. **What's in your drawer?** — pick items (phone/charger/cable/battery/
   speaker/laptop/other) with count; optional photo upload (→ Storage).
2. **Weigh it** — enter kg (or "estimate" — we show a live ₹ estimate:
   ≈₹8–12/kg mixed, phones more) + live value counter.
3. **Where + when** — address (map pick on /app/map), date + slot.
4. **Confirm** — summary + "book" → creates a PICKUP row (status: pending) →
   success screen with a generated RECEIPT draft (QR) + "we'll notify your
   centre" + email confirmation.

**Data:** insert into `pickups` (household_id, items json, kg, est_value,
address, lat/lng, slot, status, photo_url). Auth required to book (or
guest→prompt login).

---

## PAGE 19 — PAGES 12 & 13: CENTRES + MAP

- **/app/centres — THE ROSTER (the moat):** cards for each collection centre
  (name, type kabadiwala/recycler, area, capacity, pricing, rating, verified
  badge, "accepting pickups" status). **"REGISTER YOUR CENTRE"** form (name,
  type, area, capacity, pricing, phone) → inserts into `centres` (status:
  pending → owner approves in admin). This is what NIRMAN can't do: real
  centres, real onboarding.
- **/app/map — THE NETWORK MAP:** MapLibre/Leaflet map of Gurugram: household
  pickup dots (from DB) + centre pins (from DB) + a route line for a selected
  pickup. Legend: "15 authorised recyclers · 0 doorsteps — until now."

---

## PAGE 20 — PAGES 14–16: RECEIPTS · ASSISTANT · DASHBOARD

- **/app/receipts — MY RECEIPTS:** the proof library — every pickup's receipt
  (weigh-in, ₹ paid, centre, recycler, stamp, QR, print/share). Empty state:
  "Your first receipt is one drawer away."
- **/app/assistant — REBEE ASSISTANT:** a chat UI (rule-based + canned
  intelligence — no API key needed): "how much is my old phone worth?" →
  ≈₹8–12 · "where do I drop it?" → nearest centre from DB · "book it" →
  prefills the wizard. Typing animation, scan-line header, the ReBee character.
- **/app/dashboard — THE LEDGER:** analytics (Recharts): kg diverted over
  time, ₹ paid out, pickups by status, top centres, the 15-vs-0 story as a
  live chart. "THE LEDGER — receipts with taste."

---

## PAGE 21 — PAGES 17–18: AUTH + ADMIN

- **/app/login** — Supabase auth: email + Google. Sign-up asks: name, role
  (household / centre / admin), city. Post-login → redirect by role.
- **/app/admin — CENTRE ADMIN:** (role: centre/admin) manage incoming pickup
  requests (accept → status assigned → notify), update centre capacity/pricing,
  mark pickups completed → auto-generate the receipt + ₹ record. A simple
  table UI with status chips. This is the operational proof.

---

## PAGE 22 — THE DATABASE SCHEMA (Supabase SQL — create exactly this)

```sql
create table households (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users unique,
  name text, phone text, city text default 'Gurugram',
  created_at timestamptz default now()
);
create table centres (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  type text check (type in ('kabadiwala','recycler','both')),
  area text, lat float, lng float,
  capacity_kg int default 100,
  pricing_per_kg numeric default 8,
  rating numeric default 5,
  verified boolean default false,
  status text default 'pending',          -- pending | active | paused
  contact text,
  created_at timestamptz default now()
);
create table pickups (
  id uuid primary key default gen_random_uuid(),
  household_id uuid references households,
  centre_id uuid references centres,
  items jsonb default '[]',
  kg numeric, est_value numeric,
  address text, lat float, lng float,
  slot timestamptz, status text default 'pending',
  -- pending | assigned | completed | cancelled
  photo_url text,
  receipt_no text,
  created_at timestamptz default now()
);
create table receipts (
  id uuid primary key default gen_random_uuid(),
  pickup_id uuid references pickups,
  household_id uuid references households,
  centre_id uuid references centres,
  kg numeric, cash_paid numeric,
  recycler_name text, stamp text default 'WEIGHED',
  qr text, created_at timestamptz default now()
);
create table impact_log (
  id uuid primary key default gen_random_uuid(),
  kg_diverted numeric, cash_paid numeric,
  pickup_id uuid, created_at timestamptz default now()
);
-- seed: the 15 real HSPCB recyclers (as centres) + our 1.4kg pickup as impact
insert into impact_log (kg_diverted, cash_paid) values (1.4, 40);
```
RLS: households see own rows; centres see own pickups; admin sees all.

---

## PAGE 23 — THE FX LIBRARY (build these components, reuse everywhere)

1. `TextScramble` — matrix scramble → settle.
2. `BlurText` — words blur→focus, staggered.
3. `SplitReveal` — char-split yPercent/rotate reveal (GSAP, revert-safe).
4. `GlitchText` — rgb-split glitch burst on hover.
5. `SpotlightCard` — cursor radial spotlight (CSS var).
6. `TiltCard` — 3D perspective tilt + glare.
7. `Magnet` — magnetic pull on hover.
8. `ClickSpark` — particle burst on click.
9. `PixelTransition` — pixel-dissolve on hover.
10. `CountUp` — eased number counter (rAF).
11. `Aurora` / `Nebula` — drifting gradient orbs (CSS).
12. `Particles` — canvas dust.
13. `Hyperspeed` / `Galaxy` — star warp with mouse repulsion.
14. `DotGrid` — interactive dot matrix.
15. `LetterGlitch` — full-screen letter-grid glitch.
16. `FlipIn` — card flip reveals (for tier lists / lore).
17. `Marquee` — dual-speed tickers.
18. `Waveform` — canvas audio visualization.
19. `ReceiptPrinter` — clip-path + typewriter receipt.
20. `ScaleToy` — physics slider.

Every component: reduced-motion safe · touch safe · cleanup on unmount ·
token-driven · zero console errors.

---

## PAGE 24 — THE AUDIO SYSTEM

- WebAudio shared context, unlocked on first gesture.
- Hover blips (subtle sine ticks) on interactive elements · whoosh on
  transitions/section changes · click ticks.
- **Ambient beds per room** (generated, low volume, muted by default): boot
  bed (deep pad + clock ticks + sub pulse) · gate bed (pad + sparkle) · drawer
  bed (room tone) · buddy bed (ethereal). Generate with numpy or an AI audio
  tool; keep ≤ 30s loops, ~−18 LUFS.
- **Mute toggle** (zustand) in the shell — persists.
- Autoplay-safe: nothing plays before a gesture. Final ear-check by the user.

---

## PAGE 25 — THE CONTENT LIBRARY (all copy, ready to paste)

- **Hero chips:** 1.4 KG WEIGHED · ₹40 RECEIPT #1 · 15 SOURCED · 0 THE GAP.
- **Manifesto:** "The drawer waited four years. Ten homes asked. Ten drawers
  found. The infrastructure isn't missing. THE DOORSTEP IS."
- **Directive:** "Every drawer hides dead electronics… one weighed, receipted
  flow. Not a concept. A drawer we actually opened."
- **The 4 taps:** DRAWER KHOLO / SCALE PAR RAKHO / LIST KHOLO / PHOTO + DROP.
- **Idea moves:** DISCOVERY (1.4 kg — nobody had ever weighed the problem) ·
  GAP (15 recyclers, 0 doorsteps, 500-kg minimum) · METHOD (weigh → earn →
  recycle, "weighed, not guessed") · GOAL (25 households → UN Geneva).
- **Builders:** Aarav Choudhary — "the changemaker who weighed his drawer."
  ReBee (री-बी) — "built from the problem he solves."
- **Finale:** "NO DRAWER LEFT BEHIND. One drawer. One recycler. One cleaner
  India."
- **Captions/social** (from the repo's FINALE/CAPTIONS.md) for the Arsenal.
- **Hinglish stamps everywhere:** "कभी काम आएगा" · "kuch kaam ka cheez" ·
  "weighed, not guessed" · "no returns on evidence."

---

## PAGE 26 — THE QA LAW (non-negotiable, every build)

1. **Compile gate:** every route module returns 200 (curl each .jsx/css/asset).
2. **Render gate:** every route: main exists, fonts ≥ 4, scrollHeight > viewport.
3. **Blank gate:** viewport screenshot luminance std ≥ 8 (no black pages).
4. **Console gate:** 0 pageerrors, 0 console errors, 0 failed requests.
5. **JSX balance:** every page file: equal <section> open/close tags.
6. **Click gate:** every nav link + menu opens/closes + navigation works
   (desktop AND mobile).
7. **React DOM law:** NEVER manually remove/replace a React-managed node —
   state + CSS only (sticky instead of GSAP pin, conditional render instead of
   remove(), empty JSX for innerHTML targets).
8. **After ANY patch:** curl the changed module (200?) BEFORE opening the page.
9. **Commit after every phase** (the user's sandbox wipes — 7 times survived
   by commit-early).
10. **Build the gate as a script** (`verify_all.sh` like the source repo) and
    run it before every handoff.

---

## PAGE 27 — THE BUILD ORDER (phases — one at a time, gate each)

1. Foundation + tokens + QA gate script.
2. Shell (nav/cursor/HUD/progress/mute) + PageWipe + Lenis.
3. The BOOT (auto-boot + scroll universe + 3D drawer).
4. The GATE (hero monolith + full narrative sections).
5. The DRAWER (intro + pinned story + toy v2 + scale + map).
6. The PROOF (receipt printer + scale + bento + dotgrid).
7. The KABADI universe + ARSENAL.
8. The BUDDY (galaxy + SCRAP-SCAN) + SYSTEM + GENEVA.
9. The TYPE + ABOUT + 404 + LEGAL.
10. **The APP:** Supabase project + schema + auth.
11. APP: book wizard + centres + map.
12. APP: receipts + assistant + dashboard + admin.
13. Sound design pass + performance audit (60fps, code-split, lazy routes).
14. SEO/a11y (OG per route, sitemap, manifest) + error boundaries.
15. THE LAUNCH — full walkthrough QA, the "go cry to every other website"
    reel, handoff kit.

---

## PAGE 28 — DEPLOYMENT + THE HANDOFF KIT

- **Deploy:** Vercel (frontend: `npm run build` → vercel) + Supabase (db).
  Environment vars: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`.
- **Domain:** vikaas.earth (or similar) — set in Vercel + Supabase auth redirect.
- **Handoff kit (deliver to the user):**
  1. The live URL + admin login.
  2. A walkthrough video/GIF of every page + the app flow.
  3. The QA gate report (all ✅).
  4. The posting kit link (repo FINALE docs).
  5. The "go cry to every other website" one-liner reel.

---

## PAGE 29 — WHAT NOT TO DO (the hard rules)

- No CDN fonts/assets — self-host everything (the sandbox + judges need it).
- No fake numbers — every stat is in the receipts table or stamped ESTIMATE/
  DRAMATISED. (NIRMAN's "0.0 kg diverted" is the cautionary tale.)
- No manual DOM surgery in React (the law in Page 26).
- No console errors, ever — the gate is the law.
- No clutter — every page has ONE focal point; the narrative has a rhythm.
- Don't drop the loader idea — it's the beloved entrance.
- Don't forget Devanagari — विकास and री-बी must render (Noto Devanagari,
  fallback chain everywhere).
- Don't ship a page that hasn't passed the gate.

---

## PAGE 30 — THE FINAL CHECKLIST (before you say "done")

- [ ] All 30+ routes render, 0 console errors, gate 20/20 (or better).
- [ ] The full NIRMAN narrative is present (all 16 sections → ours).
- [ ] The app works end-to-end: signup → book pickup → centre sees it →
      completes → receipt generated → dashboard shows impact.
- [ ] ReBee SCRAP-SCAN playable in the Drawer AND the Buddy room.
- [ ] The 6 reels + 22 posts are in the Arsenal with hover-play.
- [ ] Audio: ambient beds + UI blips + mute toggle + ear-checked.
- [ ] Mobile perfect (390px) + reduced-motion perfect.
- [ ] OG image + meta per route · sitemap · manifest · favicon set.
- [ ] The user can log in as admin and see real data.
- [ ] The "go cry to every other website" reel exists.

---

*End of the master prompt. 30 pages, everything defined. Build it, gate it,
ship it. — The VIKAAS war room* 🐝
