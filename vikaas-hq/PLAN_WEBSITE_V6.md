# 🏛️ VIKAAS — MASTER PLAN v6 (APP-FIRST, FINAL — 19 Aug 2026)

> **THE IDEA, FINALLY LOCKED (the user's words):** VIKAAS is an **APP like
> Swiggy/Zomato — but for e-waste.** You open the app, put in your waste amount
> + details, **book a pickup** — a collection centre (kabadiwala + authorised
> recyclers, recruited by us) comes to your door, weighs it, pays you, and the
> receipt proves it went to a verified recycler. The PORTFOLIO is the pitch for
> THAT APP — every section explains the app, the way NIRMAN's portfolio explains
> his. NIRMAN sells the concept with screenshots; we sell the same app with
> REAL proof (1.4 kg weighed, ₹40, 15 HSPCB recyclers, 0 doorsteps) + a
> **working interactive app demo** in the portfolio itself.
>
> **The 4-tap flow (the app's core, shown everywhere):**
> 1. **DRAWER KHOLO** — open the app, list your items (phone/charger/cable…)
> 2. **SCALE PAR RAKHO** — enter/weigh the amount → live ₹ estimate
> 3. **LIST KHOLO** — the app shows the nearest collection centre + slot
> 4. **PHOTO + DROP** — doorstep pickup, cash at the gate, receipt generated
>
> **Mission:** NO DRAWER LEFT BEHIND. **Roadmap:** M1 ✓ M2 → M3 → Top 100 →
> City Showdown → **GENEVA · UN · 20 Nov 2026.**

---

## 0. THE RESEARCH — NIRMAN's actual repo (STUDIED, commit by commit)
Cloned `UCHIHA-MADARA-ANUJ/Nirmaan-Portfolio-` — 16 section components,
Next.js 14 + TS + Tailwind + GSAP/Lenis/Framer/Anime.js + R3F + Leaflet +
Recharts + Zustand. What we keep (match the craft):
- GenesisLoader: sessionStorage "seen" key → 18s first visit / 3s repeat,
  hashing microcopy, SKIP, reduced-motion.
- Forge: pinned phone mock crossfading prototype screens on scroll + autoplay
  sidebar — the single best pattern (a working app inside the pitch).
- Graveyard: pinned horizontal panels + giant outlined stats + RGB-split glitch.
- LiveMap: React-Leaflet dark map + pulsing divIcon radar circles.
- Nexus finale: particle explosion on launch.
What we do BETTER: real receipts (stamps), a REAL interactive app demo (not
screenshots), ReBee (character), our loader (auto-boot + scroll universe).

---

## 1. THE SITE — APP-FIRST NARRATIVE (the portfolio SELLS the app)

### THE PITCH SECTIONS (on the Gate — NIRMAN-complete, app-explaining)
```
00 THE BOOT        auto-boot → scroll universe (the beloved entrance)
01 HERO            "BOOK A PICKUP. WEIGH. EARN. RECYCLE." + 3D monolith + chips
02 CORE DIRECTIVE  drawer → kabadi network → recycler → impact, one app flow
03 THE DRAWER NATION  problem: 3.2M t/yr, 22%, 10/10 homes
04 THE STRUCTURAL GAP  500kg vs 1.4kg → 15:0 → "the doorstep is missing"
05 THE 4-TAP FLOW  THE APP in 4 taps → "TRY THE APP →" (to /app)
06 THE IDEA 4 MOVES discovery/gap/method/goal
07 MANIFESTO       blur-lines
08 ROOMS GRID      all rooms
09 BUILDERS        Aarav + ReBee
10 GENEVA FINALE   roadmap + CTA
```

### THE ROOMS
| Route | Room | What it explains |
|---|---|---|
| /drawer | THE DRAWER | the origin story + toy + scale + 15/0 map |
| /proof | THE PROOF | the receipts (the app's trust layer) |
| /kabadi | THE KABADI UNIVERSE | the network the app recruits |
| /arsenal | THE ARSENAL | 6 reels + 22 posts (our content engine) |
| /buddy | THE BUDDY | ReBee = the app's AI (SCRAP-SCAN demo) |
| /system | THE SYSTEM | the making-of + the QA gate |
| /geneva | GENEVA | the roadmap to the UN |
| /type | THE TYPE | styleguide |

### THE APP (the centerpiece — the portfolio's proof) — /app + subroutes
```
/app            THE APP — product home: phone mock autoplaying the 4-tap
                flow (book → weigh → value → receipt), live impact numbers,
                "BOOK A PICKUP" CTA
/app/book       the wizard (interactive — the visitor EXPERIENCES the app)
/app/centres    collection centres roster + REGISTER YOUR CENTRE (the moat)
/app/map        Gurugram map: households + centres + routes
/app/receipts   the proof library (real + demo receipts)
/app/assistant  ReBee assistant chat (value/centre/book)
/app/dashboard  the ledger (kg, ₹, pickups — live + real)
/app/login      auth
/app/admin      centre admin (accept/complete pickups)
```

---

## 2. THE STACK (matches NIRMAN's craft bar)
Vite6 + React19 + Router7 + TS-optional · GSAP/ScrollTrigger · Lenis · Framer
Motion · Anime.js (add — NIRMAN uses it, good for micro tweens) · Three/R3F/
drei/postprocessing · split-type · zustand (persisted) · leaflet + react-leaflet
(map) · recharts (charts) · **Supabase (db/auth/storage) — the app's backend**
· qrcode.react. Deploy: Vercel + Supabase.

---

## 3. THE PHASES (updated — app-first; DONE through 11)
**DONE:** 0 stack · 1 foundation+gate · 2 tokens · 3 shell · 4 transitions ·
5 boot polish · 6 3D monolith hero · 7 directive+nation+gap · 8 4-tap+founders
· 9 drawer intro/story · 10 toy v2 holo-cards · 11 scale sequence · + OCR
breakthrough (eyes 2.0) · + video reviewer · + task briefs read (Flash 3 + M2).

| # | Phase | The big implementation |
|---|---|---|
| 12 | **THE APP PAGE (the centerpiece)** | /app: phone mock autoplaying the 4-tap flow (book → weigh → value → receipt) — the "Swiggy-for-e-waste" demo; live impact strip; CTA. THE change the user demanded. |
| 13 | APP: book wizard | 4-step interactive: items → weight+₹ estimate → address/slot → confirm + draft receipt QR. (Pure front-end, seeded with our real audit; Supabase hook later.) |
| 14 | APP: centres roster + register | Collection centres cards (kabadi + recyclers, real HSPCB names) + REGISTER form (front-end; DB in phase 19). THE moat. |
| 15 | APP: the map | Leaflet dark map, Gurugram: household dots + centre pins + route; the 15-vs-0 story live. |
| 16 | APP: receipts + assistant | Receipt library (real + demo) · ReBee chat (value/nearest centre/book, canned). |
| 17 | APP: dashboard + auth + admin | Ledger charts · Supabase auth (email+Google) · centre admin accept/complete. |
| 18 | THE PROOF room | receipt printer · elastic scale · magic bento · dotgrid · sources. |
| 19 | THE KABADI UNIVERSE | tier showdown · ₹40 handshake · lore · network roles · dual marquees. |
| 20 | THE ARSENAL | glass dock · reel lightbox · 22-post masonry · audio lab. |
| 21 | THE BUDDY | galaxy sky · ReBee hero · SCRAP-SCAN hologram · powers · parade. |
| 22 | THE SYSTEM | making-of timeline · terminal · QA-gate viz · imagetrail · threads. |
| 23 | GENEVA + 404 | road-to-UN fill · finale CTA · lost-drawer 404. |
| 24 | SOUND + PERFORMANCE | ambient beds · blips · mute · 60fps audit · code-split. |
| 25 | SEO + A11Y + HARDENING | OG/sitemap/insta-embed · a11y · error boundaries · pre-push gate. |
| 26 | THE DATABASE | Supabase project + schema (households/centres/pickups/receipts/impact_log) + RLS + seed (15 recyclers + our 1.4kg/₹40). |
| 27 | THE LAUNCH | walkthrough QA · rival-beater checklist · handoff kit · the reel. |

---

## 4. THE QA GATE (law — 20/20 PASS currently)
compile → render → blank → console → jsx-balance → clicks. Plus now: **OCR
self-review** (eyes 2.0 — I READ screenshots, so I can verify the site's own
screenshots by reading them). React-DOM law: state+CSS only.

## 5. THE MISSIONS (in parallel — see TASK2_FLASH3_PLAN.md)
- **Flash 3** (23 Aug): watch Divaa video → 3 answers (drafts ready) → submit F3.
- **M2** (31 Aug): Measure-Act-Measure-Again; BEFORE/AFTER number+photo;
  agreement proof; hidden password in the 2 brief videos; PPT/PDF + pictures.
- Physical to-dos listed; proof → repo main → I build submissions.

## 6. THE USER'S PART
**"continue!"** per phase · watch the 3 videos (Flash3 + 2 M2) & send the
password · do the physical tasks · commit proof to main. That's it.
