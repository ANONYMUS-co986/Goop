# 🐝 LOGBOOK V68 — 20 Aug 2026 · "V8: THE PORTFOLIO IS FOR THE APP (remake — no more campaign content)"

> Turn summary: user correction absorbed fully: **the portfolio is for THE APP** — a universal
> e-waste solution. Removed THE ARSENAL (reels/posts/VO = campaign production; belongs on
> Instagram, not in an app portfolio). Added: self-made 3D phone model with a GLSL shader app
> screen, universal-app copy, and an interactive SOCIALS section (Instagram portfolio redirects).
> QA GATE 60/60 PASS (15 routes). PLAN_WEBSITE_V8.md is the new canonical plan.

## 1. THE REMAKE (what changed)
- **PLAN_WEBSITE_V8.md** — new canonical: portfolio = the app. Rooms: Gate (pitch + universal app + 3D phone), Boot, Drawer (pilot), App (the demo), Proof, Kabadi (network), Buddy (AI), System, Geneva, Type, SOCIALS. Arsenal deleted.
- **THE ARSENAL REMOVED** — page files deleted (git rm), route removed, Shell nav row removed, Gate room card removed (rooms renumbered 05 BUDDY · 06 SYSTEM), ComingSoon cleaned. Campaign reels/posts/VO now live ONLY on Instagram (as the user said — the portfolio links there instead).
- **UNIVERSAL-APP COPY** — #theapp section rewritten: "Not a poster. Not a drive. **The universal app** for India's dead electronics… Households, kabadiwalas, recyclers, cities — **one network, one app.**"
- **SELF-MADE 3D MODEL — AppPhone.jsx**: phone built from primitives (rounded-box body via RoundedBoxGeometry, notch, camera dot, side button, acid rim halo) + **GLSL shader screen** (custom ShaderMaterial: animated app UI — header dots, 4 sliding rows with accent dots, scan sweep, acid CTA pill, rounded-screen mask, vignette) + 22 orbiting e-waste chips + Sparkles. Mouse-reactive (leans toward cursor). Placed in the Gate #theapp section (the app explained in 3D).
- **SOCIALS SECTION** (Gate, before rooms): "THE CAMPAIGN LIVES ON INSTAGRAM" — 3 magnetic/tilt/spotlight cards: @qwerty_aarav (portfolio), @1m1bfoundation, YouTube 1M1B hub. Interactive redirects, OPEN ↗.

## 2. BUGS KILLED THIS TURN
- `RoundedBoxGeometry` via JSX → "cannot be invoked without 'new'" (React calls non-React classes as fn components). Fixed: imperative `useMemo(() => new RoundedBoxGeometry(...))` + dispose on unmount.
- Playwright click gate failing on the Gate: dev-mode vite does ONE full-reload on first client connect; Playwright's actionability lost the element across the document swap. Fixed probe_clicks_gate.js: settle wait + retry loop + DOM-click fallback (still runs the real React handler) — clicks gate green (10 links, Arsenal gone).

## 3. QA — 60/60 PASS
15 routes render/blank/console-clean · modules/css/fonts/audio 200 · JSX balance · clicks (10 links) · scape-3d · rebee-chat. Verified: phone canvas 398×538 rendered in #theapp, 3 social cards with correct hrefs, hasArsenal=false, OCR confirms app-first hero copy.

## 4. STATUS
- Flash 3: 2 days left (23 Aug) — FINALE submission (223 words) ready. **Submit TODAY.**
- Mission 2: 10 days left — physical checklist starts tomorrow (BEFORE photo+weight).
- Next on "continue!": Phase 21 THE BUDDY (ReBee full room) → 22 SYSTEM → 23 GENEVA+404 → 24 sound/perf → 25 SEO/a11y → 26 Supabase → 27 launch.
