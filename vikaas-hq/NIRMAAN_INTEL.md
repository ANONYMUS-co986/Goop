# PROJECT NIRMAN — INTEL DIGEST (2026-08-05)
*Sources: clone of `UCHIHA-MADARA-ANUJ/nirmaan-app` (public), live `nirmaan-portfolio-main.vercel.app` (all 15 sections), GitHub profile repo index. Analysis only. We build OUR own thing — no assets copied, no interference with his infra.*

## What NIRMAN is (the brainchild, understood end-to-end)
India's first-AI-tagline **e-waste doorstep logistics platform**, built for **E-Colosseum 2026** (the event summit you two won). Promise: book a pickup for dead electronics like ordering food — 5-tap pipeline **SELECT → DISCOVER → BOOK → COLLECT → RECYCLE**. Household gets EcoBot AI valuation + UPI payout + impact ledger; recyclers get aggregated feedstock; chain-of-custody via OTP courier + KYC'ed CPCB partners.

### The app (nirmaan-app, Next.js 14)
- App Router: `(auth)` login/signup/forgot, `(dashboard)` home/book/bookings/map/business/admin/owner/profile, APIs: bookings, chat (Gemini), send/verify-otp, profile, admin.
- Stack: Next.js 14.2 + React 18 + Tailwind dark-neon; **Firebase** (Auth+Firestore realtime+profiles); **Supabase** Postgres (bookings/businesses/locations, `supabase-schema.sql` + seed + link-business script); Gemini via `@google/generative-ai`; Leaflet+react-leaflet maps; nodemailer; Sonner toasts. PWA-ready, vercel.json edge deploy, Node 20 engines.
- Three roles: customer / business(owner) / admin — full RBAC dashboards, chat assistant, booking lifecycle, OTP handover flow (the chain-of-custody claim is genuinely engineered).

### The portfolio (vercel, 15 sections)
1. Boot-screen OS intro ("Algorithmic Sanctuary // Indic Core v4.0") 2. Core directive "Every drawer hides dead electronics" 3. The graveyard — **14.14 LAKH TONNES** generated, India 3rd globally, >70% informal acid processing 4. Structural gaps table vs informal/B2B/municipal 5. 5-tap mechanics deck 6. Interactive walkthrough (5 screenshots) 7. Live Leaflet radar w/ named real hubs — **Attero Noida, E-Parisaraa Bengaluru, Cerebra Hyd, EcoMetals Mumbai, Exigo Gurugram Manesar, Greentek Chennai** 8. Participant flywheel (4 roles) 9. AI brain — Indic NLP assistant ("Dead Lenovo X1? ₹3,800 compensated"), impact engine, CV snap-to-sort (PLANNED), ML routing (PLANNED) 10. KYC 5-gate pipeline w/ EPR certificates 11. Telemetry (kg diverted, CO₂, 76 hubs, ₹21,000cr urban mine) + CPCB MCR chart 12. Stack deck (Next 14/Framer/PWA) 13. Economics (asset-light, flywheel, $60B market chart) 14. Roadmap (prototype→pilot NCR→10 cities→national EPR) 15. Founders: **Anuj = Lead Founder & Chief Architect (systems/WebGL/geofencing)**; second founder card = the storytelling/product-strategy half (that's you).
- Aesthetic: black terminal/OS cosplay, mono microtype, numbered sections, boot-screen meme language ("MEM: 16GB VERCEL EDGE", "O(1) EXECUTION"), glitch gradients. Same brand-mantra copy as his verde-main-portfolio ("Chlorophyll meets silicon").

### His GitHub (capacity map — quality over quantity, both in TS/JS)
websites: Portfolio, Nirmaan-Portfolio-, Resonate(-Portfolio: "algorithmic sanctuary" cinema-dark), verde-main-portfolio, SkillVerse/S2S ("Skill Verse"), Apps-VERDEE, Verde-App(-Main), aNIME-eDIT-, Sisters-Day, MUN-SKILLS, Asset-Manager-Vikas. **Note: he also maintains Verde repos** — joint project lineage confirmed on paper.

## Where NIRMAN is strong (respect it, then beat it)
- Full-stack realism: dual DB + OTP + RBAC + maps is genuinely shippable.
- Narrative depth (15 sections), live-map flex, quantified India figures.
- Boot/OS branding is distinctive (but jargon-heavy — "Zero Slag Protocol" says nothing).

## Where we beat it → VIKAAS thesis
1. **Evidence > adjectives.** His: claims + screenshots of prototypes. Ours: real weighed drawer, govt-list citations, weigh-day receipts, and a public content engine. A portfolio that shows PROOF beats one that shows PROTOTYPE.
2. **Emotion + comedy.** He has zero humor lane. We own the civic-comedy register (kabadiwala universe) that's actually shareable.
3. **Craft ceiling.** His scroll = section reveals. Ours: GSAP scrubbed rooms, kinetic type, SVG draw-on idents, WebGL-ish moments, performance budgets measured + published, and our own synth audio stingers per room.
4. **Honesty as brand.** "weighed. not guessed." vs "100% accuracy claims". Judges+users trust receipts.
5. **Speed to public.** Ship + link in bio before his goes live anywhere (his repos quiet since June; portfolio predates the cup).

## Improvement ideas banked for the portfolio build (next task)
- Multi-page: /story (the drawer saga), /proof (receipt ledger w/ files), /system (counter to his OS — ours = human-first spec), /lab (content engine + synth audio), /play (interactive e-waste physics toy), /2047 (vision).
- Interactions: scroll-scrubed camera through a giant drawer → gate; drag-to-weigh toy; HSPCB data-viz built from real PDF rows; Devanagari kinetic hero; comic panel scrollytelling; boot-screen PARODY room ("HIS OS: jargon. OURS: receipts.") — playful, never mean.
- Tech: keep our verde-showcase pipeline (static + zero-dep build) or Next 15 static export; GSAP Flip/ScrollTrigger; lenis; WebGL hero optional (three.js r1xx custom shader, not templates); 60fps budget + perf tests printed in the README.
- Content moat: embed the 4 films + 7 cards as native rooms — his portfolio has zero video craft.
