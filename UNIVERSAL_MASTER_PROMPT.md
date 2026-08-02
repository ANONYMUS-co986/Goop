# 🌿 PROJECT VERDE — UNIVERSAL MASTER PROMPT & COMPLETE PROJECT BRIEF
### *A self-contained document that hands any AI model (or human designer) everything it needs to build the definitive Project Verde document/deliverable.*

**How to use this file:** Give this MD file to any AI (Replit Agent, Claude, ChatGPT, Gemini, Grok, Qwen, etc.) as an attachment — or paste it — and say: *"Use this file as your prompt. Read it word by word. You will understand the entire project. Then do the final task described at the end, to world-class standards, with your own self-review loop."*

---

# PART A — WHO WE ARE

| Field | Value |
|---|---|
| **Project name** | Project Verde (also "Verde Tech") |
| **Category** | Smart IoT Irrigation & Plant-Care System |
| **Competition** | DAV ACON 5 — Tech Exhibition, 2026 |
| **Creators** | Aarav Choudhary (Class X) & Anuj (Class X) |
| **Status** | COMPLETE & DEMO-READY — hardware, firmware, cloud, web app, AI all working |
| **Tagline** | "The plant that waters itself — and talks to AI." |
| **Total build cost** | ≈ Rs. 1,890 (≈ $23 USD) — all software/APIs on free tiers |

---

# PART B — THE COMPLETE PROJECT (EVERYTHING YOU NEED TO KNOW)

## B1. The Problem
Urban families forget to water plants, or over-water them. Plants die from a *lack of information*: nobody knows in real time how dry the soil is, whether the water tank is empty, or whether rain is coming. Commercial smart-garden kits cost ₹8,000+, lack cameras, lack AI, and often can't be opened/understood by students.

## B2. Our Solution
A three-tier IoT system where the plant "tells" us what it needs and the system acts automatically:

```
[EDGE]  ESP32 WROOM-32 (brain) + 5 sensors + pump/UV-LED actuators
        ESP32-CAM (eyes) — captures plant photos on demand
   │  HTTPS JSON (1-second heartbeat)
[CLOUD] Firebase Realtime Database — single source of truth
   │  REST / polling
[EXPERIENCE] Single-file Web App (HTML) — dashboard, controls, AI
        + 4 external AI/cloud APIs
```

## B3. Hardware (5 sensors, 2 actuators, 2 MCUs)
| Module | ESP32 pin | Role |
|---|---|---|
| Soil moisture (LM393) | AO→GPIO34, VCC gated→GPIO23 | % soil wetness (power-gated 15 ms reads to prevent corrosion) |
| DHT11 | DATA→GPIO4 | temperature + humidity |
| LDR module | AO→GPIO35 | ambient light → "dark" detection |
| HC-SR04 ultrasonic | TRIG→GPIO18, ECHO→GPIO19 | water tank level (5-point filter) |
| 2-ch relay | IN1→GPIO5 (active-LOW) | switches the 5 V water pump |
| UV grow LED | GPIO12 (active-HIGH, 220Ω) | photosynthetic light |
| ESP32-CAM (OV2640) | own board + MB programmer | captures SVGA photos → uploads to cloud |

**Power design (hard-won lessons):**
- Main supply: **5 V / 2 A phone adapter** (NOT a USB-PD laptop charger — PD requires a handshake chip the ESP32 lacks, so it outputs ~0 mA and starves the board)
- 1000 µF electrolytic capacitor across 5 V/GND (absorbs pump+WiFi current spikes)
- 1N4007 flyback diode across the pump (kills inductive spikes)
- Pump electrically isolated via relay COM/NO on its own 5 V source

## B4. Firmware (Code_1_Main_Brain.ino — V3.0.7-FINAL)
- Non-blocking `millis()` task scheduler: sensors 1 Hz · cloud 1 s · WiFi 10 s · logs 60 s
- Hardware watchdog (8 s) fed every loop
- **AUTO logic:** `pump_ON = moisture < threshold AND tank safe AND no rain`
- **Manual logic:** user-driven, still tank-protected
- Adjustable thresholds from the app: `moisture_threshold`, `tank_threshold` (0 = disabled), `light_threshold` — persisted in NVS flash
- **10-point moving averages** for soil/LDR; **5-point moving average + invalid-read rejection** for the tank (pump-splash garbage can't fake an empty tank)
- **±2% hysteresis** on light auto-switch (no LED flicker)
- 3-network WiFi fallback (home / hotspot / school)
- **THE BIG BUG (IMPORTANT STORY):** AUTO mode clicked pump ON/OFF every ~10 s. Root cause: 17 blocking Firebase HTTPS calls per second → network stall → 8 s watchdog reboot → loop. **Fix: JSON bundling** — 1 write to `/sensors` (10 metrics) + 1 read of `/controls` (9 keys) per second → ~85% less latency, zero reboots, pump stays ON continuously until threshold reached.

## B5. ESP32-CAM (Code_2_ESP32_CAM.ino — V3.0.4-FINAL)
- Polls `/controls/capture_photo` every 1.5 s → on trigger: flash LED → capture SVGA JPEG → POST raw bytes to Vercel upload API → lands in `/latest_scan` (base64) → app shows it ≤2 s
- Engineering: **8 MHz XCLK** (fixes RF interference with the WiFi antenna), **sequential boot** (camera first, WiFi after 500 ms — prevents brownout), **esp_camera_fb_return()** immediately (no heap fragmentation)

## B6. Cloud — Firebase RTDB Schema
```
verde-tech-haha (RTDB)
├── sensors/      moisture · temperature · humidity · light · tank_level · lux
│                 · watchdog_status · voltage_sag · successful_uploads · failed_uploads
├── controls/     manual_mode · pump_state · light_manual_mode · grow_light_state
│                 · capture_photo · moisture_threshold · tank_threshold
│                 · light_threshold · weather_override
├── latest_scan/  imageUrl (base64) · status · captured_at · scientificName
│                 · diseaseName · probability · treatmentPlan
├── weather/      city · temp · condition · description · humidity
│                 · wind_speed · rain_expected · synced_at
├── historical_logs/  moisture_log [ {time, moisture} ]
└── actuators/    pump_actual · grow_light_actual · mode
```
Rules: public read, validated writes (booleans, numbers 0–100), ESP32 uses legacy database secret.

## B7. The Web App (single-file HTML — "the face")
Four pages via burger menu:
1. **Dashboard** — 8 live telemetry tiles with sparklines + hover graphs (last-10 trend ▲/▼), all 8 controls, 3 threshold sliders, predicted actuator states, moisture history chart, system status strip, toasts, fullscreen demo mode, uptime timer
2. **Weather** — live Delhi weather, 5-day forecast chips, auto rain-override (checks every 3 min) with countdown
3. **Plant Doctor** — live CAM photo frame (auto-updates ≤2 s), CAPTURE button, upload-or-CAM modal: photo + crop.health diagnosis + AI chat that sees the same image
4. **AI Assistants** — Gemini image chat + OpenRouter sensor-aware chat (quick prompts)
- Tank calibration panel (SET EMPTY / SET FULL — app-side remap, no reflash)
- Image flip fix (CAM mounts upside-down)

## B8. The 4 APIs (researched, keyed, tested)
| API | Purpose | Auth | Mechanics | Accuracy notes |
|---|---|---|---|---|
| **OpenWeatherMap** | live weather + 5-day forecast → rain override | key in URL | GET `/data/2.5/weather?q=Delhi`; ids 2xx/3xx/5xx/6xx → rain → `weather_override=1` | live-tested: Delhi 35 °C, correct city id 1273294 |
| **crop.health (Plant.id)** | plant + disease identification | `Api-Key` header | POST `/api/v1/identification` with base64 image → `result.crop.suggestions[]` + `result.disease.suggestions[]` (name, probability, treatment) | identified test image as nutrient deficiency @94% with treatment plan |
| **Google Gemini 2.5 Flash** | vision chat on the analysed photo | `X-goog-api-key` header (AQ keys) | POST `/v1beta/models/gemini-flash-latest:generateContent` with inline image + diagnosis + telemetry | AQ keys need header; gemini-2.5-flash no longer offered to new users → use `gemini-flash-latest` |
| **OpenRouter** | sensor chat + vision fallback | `Authorization: Bearer sk-or-v1-…` | POST `/api/v1/chat/completions` (OpenAI-compatible), 8-model text chain + 5-model vision chain | 435 models accessible; free models rotate → fallback chains never dead-end |

## B9. Tested Results (13-point matrix, all PASS)
WiFi/boot · DHT11 breathe test · moisture water-dunk · LDR cover test · ultrasonic hand test · pump AUTO 120 s (no glitch) · OFF exactly at threshold · tank lock · rain override · CAM capture ≤2 s · Plant Doctor 94% diagnosis · AI chats + fallbacks · watchdog 10+ min (0 reboots)

## B10. Real Bugs We Hit & Fixed (honesty = credibility)
1. AUTO 10 s pump loop → 17 calls/s → JSON bundling (2 calls/s)
2. Camera probe 0x106 → FPC ribbon unseated → reseat gold-side down + power cycle
3. PSRAM not found → weak power → 5V/2A adapter
4. 0x20002 boot crash → camera+WiFi power surge → sequential boot
5. RF interference → 20 MHz XCLK → throttle to 8 MHz
6. 67 W USB-PD charger starved the board → 5V/2A adapter
7. Relay dead → split breadboard rails → bridge + to +, − to −
8. temp = 0 → DHT wrong pin → GPIO 4 + shared GND
9. Firebase "spurts" → 13 calls/s → one bundled call
10. Compile "missing terminating quote" → copy-paste corruption → re-download file

## B11. Costing
| Category | Cost (INR) |
|---|---|
| Electronics (ESP32, ESP32-CAM, 5 sensors, relay, pump, LED) | 1,320 |
| Power & protection (adapter, caps, diode) | 220 |
| Mechanical (breadboard, wires, enclosure) | 350 |
| Software & APIs (all free tiers) | 0 |
| **Total** | **≈ 1,890** |

## B12. Future Scope
Solar autonomy (12 V panel + charge controller + battery) · NPK soil probe · multi-plant zones · Telegram/WhatsApp alerts · predictive watering from logs · deployed Next.js dashboard (scaffolded)

---

# PART C — THE FINAL TASK (the actual request)

## C1. What we want
Create **the definitive, world-class documentation deliverable** for Project Verde — a document so good that judges *want* to read it, designers nod at it, and it makes a ₹1,890 student project look like a funded startup product.

## C2. Non-negotiable requirements (the brief)
1. **Format:** a polished PDF (or web page exportable to PDF) — approximately 20–35 pages
2. **Readability first:** short paragraphs (≤90 words), bullets, pull quotes, hero numbers, infographics, generous white space. **Nobody reads walls of text.** Every page must be skimmable in <10 seconds.
3. **Design system:** consistent palette (deep navy + emerald green + gold accents), 2–3 fonts max with clear hierarchy, consistent icons, full-bleed cover with AI-generated or SVG art
4. **Visuals required:** cover art · system architecture diagram · circuit/wiring diagram · Firebase schema tree · AUTO-mode flowchart · the bug BEFORE/AFTER infographic (17 calls → 2 calls) · cost comparison chart (ours vs commercial) · moisture watering-cycle chart with threshold marker · one-second heartbeat timeline · feature icons · photo placeholders (hardware bench, AI plant doctor)
5. **Structure (suggested, adapt freely):** Cover → "The Whole Story in 60 Seconds" → Contents → Why (problem) → How It Works (architecture) → Hardware (BOM, circuit, power lessons) → Firmware + the bug story → Cloud & App → AI & APIs (with accuracy notes) → Features (all live) → Testing + troubleshooting journal → Cost & sustainability → Future → Judge tour script → Conclusion
6. **Tone:** confident, human, slightly playful; honest about failures (credibility); zero "AI-slop" clichés; no mention of any AI tool used to make it
7. **Extra polish (go beyond if you can):** hyperlinked TOC, bookmarks, KPI cards, timelines, callouts, print-optimized variant, maybe a QR to the live demo

## C3. Self-review loop (mandatory)
You must iterate like a professional designer:
1. **Build** the document
2. **Render** it (convert pages to images) and **inspect** every page for: layout overflow, clipped text, blank pages, broken images, inconsistent spacing
3. **Audit** content: every section present, numbers accurate (Rs. 1,890, 5 sensors, 17→2 calls, 94%, 8 MHz, GPIO pins, thresholds 35/15/35)
4. **Score yourself** out of 100 on: Visual Design / Readability / Completeness / Accuracy / Engagement
5. **Fix** everything below 90 and rebuild
6. **Deliver** the final PDF + the build script/source + a one-page summary of what you changed during review

## C4. Technical freedom
- Use whatever stack you prefer (ReportLab, WeasyPrint, LaTeX, HTML/CSS→PDF, Figma export, etc.)
- Install libraries, generate AI images, draw SVGs — **no limits**
- If you're on **Replit Agent**: it supports Python/JS, checkpoints (rollback if a change breaks things), live preview, and deployment; free tier has ~5-min sleep + 512 MB RAM, so keep assets efficient and work incrementally with checkpoints before big changes
- If you have an internet connection, you may research annual-report design best practices first (bold hierarchy, 2–3 colors, photography/illustration consistency, data-viz clarity) — we already did; apply them

## C5. Acceptance criteria (how we know you nailed it)
- A judge can flip through it in 3 minutes and understand the whole project
- A parent/teacher can read any page and not feel lost
- All numbers and facts match Part B exactly
- No page looks empty, broken, or text-wall
- It makes us say: "This looks like a real product company made it"

---

*End of brief. You now know everything about Project Verde. Build us something beautiful. 🌿*
