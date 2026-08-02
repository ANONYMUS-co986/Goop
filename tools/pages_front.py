#!/usr/bin/env python3
"""Project Verde — front pages: cover, 60s story, contents, why, architecture,
hardware, firmware, the big bug, ESP32-CAM."""
from verde_style import (PAL, VARIANT, FB, PAGE_W, PAGE_H, M_L, M_R, M_T, M_B,
                         sw, rrect, hrule, grad_image, dotgrid, chip, icon, icon_circle,
                         parse_runs, draw_par, measure_par, section_header, footer)
from verde_diagrams import (arch_diagram, circuit_diagram, before_after, moisture_chart,
                            heartbeat_timeline, scheduler_timeline, photo_pipeline)
from pagekit import *

COVER = "assets/prep/cover_prep.jpg"
BENCH = "assets/prep/bench_prep.jpg"
DOCTOR = "assets/prep/doctor_prep.jpg"
FUTURE = "assets/prep/future_prep.jpg"
QR = "assets/prep/qr.png"

# ------------------------------------------------------------------ 01 COVER
def cover(c, meta):
    c.setFillColor(PAL["bg"]); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.drawImage(COVER, 0, 0, width=PAGE_W, height=PAGE_H, mask="auto", preserveAspectRatio=False)
    # top bar
    hrule(c, M_L, PAGE_H - 52, 46, PAL["gold"], 2.2)
    c.setFillColor(PAL["gold"]); c.circle(M_L + 50, PAGE_H - 52.6, 1.8, stroke=0, fill=1)
    chip(c, M_L, PAGE_H - 70, "DAV ACON 5 — TECH EXHIBITION · 2026", size=7.4, bg=None,
         color=PAL["gold_l"], border=PAL["gold"], radius=11)
    # title block
    c.setFont(FB["mono_b"], 11); c.setFillColor(PAL["emerald"])
    c.drawString(M_L, PAGE_H - 300, "SMART IOT IRRIGATION & PLANT-CARE SYSTEM")
    c.setFont(FB["disp_bl"], 62); c.setFillColor(PAL["ivory"])
    c.drawString(M_L, PAGE_H - 372, "PROJECT")
    c.drawString(M_L, PAGE_H - 434, "VERDE")
    hrule(c, M_L, PAGE_H - 456, 120, PAL["gold"], 3)
    c.setFont(FB["disp_sb"], 16.5); c.setFillColor(PAL["ivory"])
    c.drawString(M_L, PAGE_H - 490, "The plant that waters itself — and talks to AI.")
    # bottom meta band
    c.saveState()
    c.setFillColor(PAL["bg"]); c.setFillAlpha(0.78)
    c.rect(0, 0, PAGE_W, 118, stroke=0, fill=1)
    c.restoreState()
    hrule(c, 0, 118, PAGE_W, PAL["gold"], 1.2)
    c.setFont(FB["body_b"], 9.5); c.setFillColor(PAL["ivory"])
    c.drawString(M_L, 78, "Aarav Choudhary  ·  Anuj")
    c.setFont(FB["body"], 8.5); c.setFillColor(PAL["slate"])
    c.drawString(M_L, 62, "Class X — a ₹1,890 system with a ₹8,000+ commercial-feel")
    # bottom KPIs
    stats = [("5", "SENSORS"), ("2", "MCUs"), ("2/s", "CLOUD CALLS"), ("₹1,890", "TOTAL COST")]
    bw = 118
    for i, (v, l) in enumerate(stats):
        sx = PAGE_W - M_R - (len(stats) - i) * bw
        c.setFont(FB["body_bl"], 19); c.setFillColor(PAL["gold"] if i % 2 else PAL["emerald"])
        c.drawRightString(sx + 8, 74, v)
        c.setFont(FB["body_b"], 6.2); c.setFillColor(PAL["slate"])
        c.drawRightString(sx + 8, 56, l)
        if i:
            c.saveState(); c.setStrokeColor(PAL["line"]); c.setLineWidth(0.8)
            c.line(sx - 8, 48, sx - 8, 96); c.restoreState()

# ------------------------------------------------------------------ 02 STORY
def story_60s(c, meta, page_no):
    bg(c, deep=True)
    y = PAGE_H - 64
    dotgrid(c, M_L, 40, PAGE_W - M_L - M_R, PAGE_H - 140, spacing=26, alpha=0.10)
    y = section_header(c, "READ THIS FIRST — 90 SECONDS MAX", "The Whole Story in 60 Seconds",
                       "Everything a judge needs before the demo even starts.", y)
    y = draw_par(c, M_L, y, "Most plants don’t die from neglect — they die from {g:**no information**}. "
            "Nobody knows in real time how dry the soil is, whether the tank is empty, or whether rain is coming. "
            "Project Verde removes that blind spot: a three-tier IoT system where the plant {g:**tells us what it needs**}, "
            "and the system acts on its own.", PAGE_W - M_L - M_R, size=10, leading=15) - 12
    y = draw_par(c, M_L, y, "At the edge, an {m:**ESP32 WROOM-32**} reads 5 sensors and drives 2 actuators while an "
            "{m:**ESP32-CAM**} acts as the plant’s eyes. Every second, one bundled HTTPS call carries 10 live metrics "
            "to a {m:**Firebase Realtime Database**} — the single source of truth. On top sits a single-file web app: "
            "live dashboard, weather with automatic rain-override, a Plant Doctor that identifies diseases at "
            "{g:**94% confidence**}, and AI assistants that chat about the same photo you’re looking at.", PAGE_W - M_L - M_R, size=10, leading=15) - 12
    y = draw_par(c, M_L, y, "Total build cost: {g:**≈ ₹1,890**}. All software and APIs are on free tiers. "
            "Everything is student-built, student-understood, and demo-ready — with a genuinely fun bug story "
            "inside (17 cloud calls per second → 2).", PAGE_W - M_L - M_R, size=10, leading=15) - 24
    # KPI row
    kpis = [
        ("₹1,890", "TOTAL BUILD COST", "vs ₹8,000+ commercial kits", PAL["gold"]),
        ("5", "SENSORS", "soil · DHT11 · LDR · tank · light", PAL["emerald"]),
        ("2/s", "CLOUD CALLS", "was 17/s — the big fix", PAL["gold"]),
        ("94%", "DIAGNOSIS", "crop.health on a real leaf", PAL["emerald"]),
        ("13/13", "TESTS PASS", "full matrix, zero reboots", PAL["gold"]),
        ("≤2 s", "CAM PHOTO", "trigger to on-screen", PAL["emerald"]),
    ]
    bw = (PAGE_W - M_L - M_R - 5 * 12) / 6
    for i, (v, l, s, ac) in enumerate(kpis):
        kpi_card(c, M_L + i * (bw + 12), y - 96, bw, 88, v, l, s, accent=ac)
    y -= 118
    # stack strip
    shadow_rrect(c, M_L, y - 52, PAGE_W - M_L - M_R, 52, 8, PAL["card2"])
    labels = [("ESP32 + CAM", "edge — 5 sensors, 2 actuators"), ("FIREBASE RTDB", "single source of truth"),
              ("WEB APP", "dashboard + controls"), ("4 AI APIS", "weather · vision · chat")]
    bw2 = (PAGE_W - M_L - M_R - 3 * 24) / 4
    for i, (t, s) in enumerate(labels):
        sx = M_L + i * (bw2 + 24)
        c.setFont(FB["mono_b"], 8); c.setFillColor(PAL["gold"])
        c.drawString(sx + 14, y - 24, t)
        c.setFont(FB["body"], 6.4); c.setFillColor(PAL["slate"])
        c.drawString(sx + 14, y - 38, s)
        if i < 3:
            c.saveState(); c.setStrokeColor(PAL["emerald"]); c.setLineWidth(1.2)
            c.line(sx + bw2 + 6, y - 28, sx + bw2 + 18, y - 28)
            p = c.beginPath()
            p.moveTo(sx + bw2 + 18, y - 31); p.lineTo(sx + bw2 + 18, y - 25); p.lineTo(sx + bw2 + 23, y - 28)
            p.close(); c.setFillColor(PAL["emerald"]); c.drawPath(p, stroke=0, fill=1)
            c.restoreState()
    y -= 96
    pull_quote(c, M_L, y - 10, PAGE_W * 0.72,
               "A ₹1,890 student project that behaves like a funded startup product.",
               author="— the goal, stated plainly", size=16)
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 03 CONTENTS
def contents(c, meta, page_no, toc_entries):
    bg(c)
    y = PAGE_H - 64
    y = section_header(c, "NAVIGATION", "Contents", "Hyperlinked — click any entry to jump. Bookmarks in your PDF reader too.", y)
    entries = toc_entries
    col_w = (PAGE_W - M_L - M_R - 40) / 2
    per_col = (len(entries) + 1) // 2
    for idx, (num, title, pnum, dest) in enumerate(entries):
        col = idx // per_col
        row = idx % per_col
        ex = M_L + col * (col_w + 40)
        ey = y - 8 - row * 34
        if idx == 0:
            pass
        rrect(c, ex, ey - 26, col_w, 30, 6, fill=PAL["card"] if row % 2 == 0 else PAL["card2"], stroke=None)
        c.setFont(FB["mono_eb"], 11); c.setFillColor(PAL["gold"])
        c.drawString(ex + 12, ey - 13, f"{num:02d}")
        c.setFont(FB["body_b"], 9); c.setFillColor(PAL["ivory"])
        c.drawString(ex + 42, ey - 13, title)
        c.setFont(FB["mono_b"], 9); c.setFillColor(PAL["emerald"])
        c.drawRightString(ex + col_w - 12, ey - 13, f"{pnum}")
        c.linkRect("", dest, (ex, ey - 26, ex + col_w, ey + 4), relative=1)
    # side note card
    ny = y - 8 - len(entries) * 0 * 0 - 0
    nx, ny = M_L + col_w + 40, y - 8 - (per_col - 1) * 34
    callout(c, nx, ny - 120, col_w, 108, "book", "How this document works",
            "Short pages, honest numbers, zero walls of text. Every page is skimmable in "
            "under 10 seconds — the demo script at the end turns it into a live tour.",
            accent=PAL["gold"])
    callout(c, nx, ny - 236, col_w, 104, "shield", "The numbers are real",
            "Rs. 1,890 · 5 sensors · 2 MCUs · 17→2 calls/s · 94% diagnosis · 8 MHz XCLK. "
            "Every figure in here matches the build log exactly.", accent=PAL["emerald"])
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 04 WHY
def why_page(c, meta, page_no):
    bg(c, deep=True)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 01 — THE PROBLEM", "Why? Because Plants Die of Ignorance",
                       "Not from neglect. From a lack of information.", y)
    y = draw_par(c, M_L, y, "Urban families forget to water plants. Or they over-water them out of guilt. "
            "Both kill the plant — and neither is really the problem. The problem is that nobody "
            "{g:**knows**}: how dry is the soil right now? Is the tank empty? Is rain on the way?",
            PAGE_W - M_L - M_R, size=10, leading=15) - 26
    problems = [
        ("drop", "FORGOTTEN", "Life gets busy. The plant is the first thing to slip — silently, for days."),
        ("bolt", "OVER-WATERED", "Guilt-watering drowns roots. Enthusiasts kill plants with kindness."),
        ("eye", "NO VISIBILITY", "No real-time soil, tank, or weather data — decisions made blind."),
        ("money", "PRICE WALL", "Commercial smart kits start at ₹8,000+, and still lack cameras and AI."),
    ]
    bw = (PAGE_W - M_L - M_R - 3 * 14) / 4
    for i, (ic, t, d) in enumerate(problems):
        sx = M_L + i * (bw + 14)
        shadow_rrect(c, sx, y - 118, bw, 110, 10, PAL["card"])
        icon_circle(c, sx + bw / 2, y - 40, ic, 30, PAL["gold"] if i % 2 else PAL["emerald"])
        c.setFont(FB["body_b"], 8.4); c.setFillColor(PAL["ivory"])
        c.drawCentredString(sx + bw / 2, y - 72, t)
        draw_par(c, sx + 10, y - 84, d, bw - 20, size=6.6, leading=9, color=PAL["slate"], align="center")
    y -= 148
    shadow_rrect(c, M_L, y - 74, PAGE_W - M_L - M_R, 66, 8, PAL["card2"])
    c.setFont(FB["mono_b"], 8.6); c.setFillColor(PAL["gold"])
    c.drawString(M_L + 16, y - 22, "THE COST OF IGNORANCE")
    draw_par(c, M_L + 16, y - 40, "Commercial smart-garden kits: {g:**₹8,000+**}, no camera, no AI, "
            "closed hardware a student can’t open or understand. The gap isn’t money — it’s information. "
            "So we built the information.", PAGE_W - M_L - M_R - 32, size=8, leading=12)
    y -= 108
    pull_quote(c, M_L, y - 8, PAGE_W * 0.76,
               "A plant doesn’t need a gardener with a schedule. It needs a gardener with sensors.",
               author="— Project Verde, in one line", size=15)
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 05 ARCHITECTURE
def architecture_page(c, meta, page_no):
    bg(c, deep=True)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 02 — HOW IT WORKS", "Three Tiers, One Truth",
                       "Edge sensors → one cloud → an experience you can actually read.", y)
    arch_diagram(c, M_L, 96, PAGE_W - M_L - M_R, 425)
    y2 = y - 30
    y2 = draw_par(c, M_L, y2, "Every second, the ESP32 bundles {m:**10 live metrics**} into one write to "
            "{m:`/sensors`} and reads back {m:**9 control keys**} from {m:`/controls`} in one call. "
            "The web app polls the same database over REST. Both sides see the exact same truth — "
            "no sync layers, no conflicts, one source.", PAGE_W - M_L - M_R, size=8.6, leading=12.5) - 24
    tiers = [
        ("EDGE", "5 sensors, 2 actuators, watchdog, power-gated reads — the plant’s nervous system."),
        ("CLOUD", "Firebase RTDB as the single source of truth, with validated writes and public read."),
        ("EXPERIENCE", "A single-file web app: dashboard, weather, Plant Doctor, and AI chat."),
    ]
    bw = (PAGE_W - M_L - M_R - 2 * 14) / 3
    for i, (t, d) in enumerate(tiers):
        sx = M_L + i * (bw + 14)
        shadow_rrect(c, sx, y2 - 64, bw, 56, 8, PAL["card"])
        chip(c, sx + 12, y2 - 14, t, size=6.8, bg=PAL["green_bg"], color=PAL["emerald"])
        draw_par(c, sx + 12, y2 - 34, d, bw - 24, size=6.4, leading=9, color=PAL["slate"])
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 06 HARDWARE BOM
def hardware_bom(c, meta, page_no):
    bg(c)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 03 — HARDWARE · PART 1", "The Brain & The Eyes",
                       "Two ESP32 boards, five sensors, two actuators — one very patient plant.", y)
    photo_band(c, BENCH, M_L, y - 168, PAGE_W - M_L - M_R, 152,
               caption="The whole bench: ESP32 brain, ESP32-CAM eyes, sensors, relay, pump — under ₹1,900.",
               radius=10)
    y -= 196
    rows = [
        ["`LM393` soil moisture", "AO → `GPIO34`", "% soil wetness — power-gated 15 ms reads, anti-corrosion"],
        ["`DHT11`", "DATA → `GPIO4`", "temperature + humidity"],
        ["`LDR` module", "AO → `GPIO35`", "ambient light → “dark” detection"],
        ["`HC-SR04` ultrasonic", "TRIG → `GPIO18` · ECHO → `GPIO19`", "water-tank level, 5-point filter"],
        ["`2-ch relay`", "IN1 → `GPIO5` (active-LOW)", "switches the 5 V water pump"],
        ["`UV grow LED`", "`GPIO12` (active-HIGH, 220 Ω)", "photosynthetic light"],
        ["`ESP32-CAM` OV2640", "own board + MB programmer", "SVGA photos → cloud, on demand"],
    ]
    header = ["MODULE", "ESP32 PIN", "ROLE"]
    col_w = [150, 150, PAGE_W - M_L - M_R - 150 - 150]
    table_grid(c, M_L, y - 7 - 20 - 17 * len(rows), PAGE_W - M_L - M_R, header, rows, col_w, row_h=17)
    yy = y - 7 - 20 - 17 * len(rows) - 22
    stat_strip(c, M_L, yy - 64, PAGE_W - M_L - M_R,
               [("5", "SENSORS"), ("2", "ACTUATORS"), ("2", "MCUs"), ("5V/2A", "POWER SUPPLY")], h=52)
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 07 CIRCUIT & POWER
def circuit_page(c, meta, page_no):
    bg(c, deep=True)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 03 — HARDWARE · PART 2", "Wiring & The Power Wars",
                       "Every pin, every lesson — the stuff that actually took the longest.", y)
    circuit_diagram(c, M_L, 170, PAGE_W - M_L - M_R, 400)
    y -= 16
    draw_par(c, M_L, y, "The wiring diagram above is the real, final revision — each of those lines is "
            "a wire we physically pulled, swore at, and re-pulled. The interesting part is below the schematic: "
            "{g:**power design is where this project was won**.}", PAGE_W - M_L - M_R, size=8.6, leading=12.5)
    y -= 34
    lessons = [
        ("bolt", "5 V / 2 A — never USB-PD", "A 67 W laptop charger starved the board: PD needs a handshake chip "
         "the ESP32 lacks, so it delivered ~0 mA. A plain phone adapter fixed it."),
        ("drop", "1000 µF across the rail", "The electrolytic capacitor absorbs pump + WiFi current spikes that "
         "were crashing brownouts into resets."),
        ("shield", "1N4007 flyback diode", "Across the pump, it kills the inductive voltage spike every switch-off "
         "would otherwise send back into the logic."),
        ("cpu", "Relay isolation", "The pump runs on its own 5 V source via relay COM/NO — electrically isolated "
         "from the ESP32’s power, so motor noise never corrupts sensor reads."),
    ]
    bw = (PAGE_W - M_L - M_R - 3 * 14) / 4
    for i, (ic, t, d) in enumerate(lessons):
        sx = M_L + i * (bw + 14)
        shadow_rrect(c, sx, y - 118, bw, 112, 10, PAL["card"])
        icon_circle(c, sx + bw / 2, y - 38, ic, 28, PAL["gold"] if i % 2 else PAL["emerald"])
        c.setFont(FB["body_b"], 7.8); c.setFillColor(PAL["ivory"])
        draw_par(c, sx + 10, y - 52, t, bw - 20, size=7.8, leading=10, color=PAL["ivory"], align="center")
        draw_par(c, sx + 10, y - 70, d, bw - 20, size=6.2, leading=8.8, color=PAL["slate"], align="center")
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 08 FIRMWARE
def firmware_page(c, meta, page_no):
    bg(c)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 04 — FIRMWARE", "The Brain: Non-Blocking by Design",
                       "Code_1_Main_Brain.ino — V3.0.7-FINAL. Nothing blocks. Nothing freezes. Nothing starves.", y)
    scheduler_timeline(c, M_L, y - 208, PAGE_W - M_L - M_R, 176)
    y -= 216
    # auto logic + thresholds
    bw = (PAGE_W - M_L - M_R - 14) / 2
    shadow_rrect(c, M_L, y - 128, bw, 122, 10, PAL["card"])
    chip(c, M_L + 14, y - 26, "AUTO LOGIC — ONE LINE", size=6.8, bg=PAL["green_bg"], color=PAL["emerald"])
    c.setFont(FB["mono"], 8.2); c.setFillColor(PAL["mint"])
    draw_par(c, M_L + 14, y - 44, "pump_ON = moisture < threshold\n        AND tank ≥ safe\n        AND no rain",
             bw - 28, size=8.2, leading=12.5, mono=True, color=PAL["mint"])
    draw_par(c, M_L + 14, y - 96, "Manual mode overrides but never skips the tank check — a dry tank can’t be pumped.",
             bw - 28, size=6.8, leading=10, color=PAL["slate"])
    sx = M_L + bw + 14
    shadow_rrect(c, sx, y - 128, bw, 122, 10, PAL["card"])
    chip(c, sx + 14, y - 26, "THRESHOLDS — LIVE FROM THE APP", size=6.8, bg=PAL["gold_bg"], color=PAL["gold"])
    vals = [("moisture_threshold", "35%"), ("tank_threshold", "15%  (0 = disabled)"), ("light_threshold", "35")]
    yy = y - 46
    for k, v in vals:
        c.setFont(FB["mono"], 7.2); c.setFillColor(PAL["slate"])
        c.drawString(sx + 14, yy - 3, k)
        c.setFont(FB["mono_b"], 7.6); c.setFillColor(PAL["gold"])
        c.drawRightString(sx + bw - 14, yy - 3, v)
        yy -= 16
    draw_par(c, sx + 14, yy - 8, "Persisted in NVS flash — survive reboots, adjustable from the app, no reflash.",
             bw - 28, size=6.6, leading=9.6, color=PAL["slate"])
    y -= 148
    extras = [
        ("signal", "3-network WiFi fallback", "home → hotspot → school. The demo never dies on a captive portal."),
        ("shield", "8 s hardware watchdog", "fed every loop — a reboot now means a real fault, not a stall."),
        ("clock", "±2% hysteresis", "light auto-switch can’t flicker at the boundary."),
        ("drop", "10-pt moving averages", "soil/LDR smoothed; tank uses 5-pt + invalid-read rejection — "
         "pump splash can’t fake an empty tank."),
    ]
    bw2 = (PAGE_W - M_L - M_R - 3 * 12) / 4
    for i, (ic, t, d) in enumerate(extras):
        sx2 = M_L + i * (bw2 + 12)
        shadow_rrect(c, sx2, y - 74, bw2, 68, 8, PAL["card2"])
        icon_circle(c, sx2 + 18, y - 24, ic, 22, PAL["gold"] if i % 2 else PAL["emerald"])
        c.setFont(FB["body_b"], 7.2); c.setFillColor(PAL["ivory"])
        c.drawString(sx2 + 36, y - 28, t)
        draw_par(c, sx2 + 10, y - 44, d, bw2 - 20, size=5.9, leading=8.2, color=PAL["slate"])
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 09 THE BIG BUG
def bug_page(c, meta, page_no):
    bg(c, deep=True)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 05 — THE STORY THEY’LL REMEMBER", "The Bug That Almost Killed AUTO",
                       "AUTO mode clicked the pump ON and OFF every ~10 seconds. Here’s why — and the fix.", y)
    before_after(c, M_L, 108, PAGE_W - M_L - M_R, 330)
    yy = y - 16
    yy = draw_par(c, M_L, yy, "**Root cause:** 17 blocking Firebase HTTPS calls per second — one per key, per sensor, "
            "per second. The network stalled, the {r:**8-second watchdog**} rebooted the board, and every reboot "
            "re-evaluated AUTO with a dry sensor reading. Loop. The pump never stayed on long enough to water anything.",
            PAGE_W - M_L - M_R, size=9, leading=13.5) - 14
    draw_par(c, M_L, yy, "**The fix:** {g:**JSON bundling**} — one write of all 10 metrics to {m:`/sensors`} plus one "
            "read of 9 control keys from {m:`/controls`} per second. Latency dropped ~85%, reboots hit zero, "
            "and the pump finally stays ON continuously until the soil reaches threshold. This is the bug that "
            "taught us the whole project: {g:**design the data flow before the feature**}.", PAGE_W - M_L - M_R,
            size=9, leading=13.5)
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 10 ESP32-CAM
def cam_page(c, meta, page_no):
    bg(c)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 06 — THE EYES", "ESP32-CAM: A Photo Every 2 Seconds",
                       "Code_2_ESP32_CAM.ino — V3.0.4-FINAL. The plant has a camera now.", y)
    photo_pipeline(c, M_L, y - 104, PAGE_W - M_L - M_R, 84)
    y -= 128
    photo_band(c, DOCTOR, M_L + PAGE_W * 0.50, 400, PAGE_W - M_R - (M_L + PAGE_W * 0.50), 160,
               caption="The Plant Doctor: photo → diagnosis → AI chat.",
               radius=10)
    fixes = [
        ("8 MHz XCLK", "Camera clock throttled from 20 to 8 MHz — RF interference with the WiFi antenna gone."),
        ("Sequential boot", "Camera first, WiFi 500 ms later — no power surge, no crash 0x20002."),
        ("esp_camera_fb_return()", "Frame buffer returned instantly — no heap fragmentation after hours."),
        ("Poll-triggered", "Polls {m:`capture_photo`} every 1.5 s → photo on screen in ≤2 s."),
    ]
    bw = PAGE_W * 0.5 - 7
    for i, (t, d) in enumerate(fixes):
        sy = y - 16 - i * 78
        callout(c, M_L, sy - 66, bw, 66, "camera", t, d, accent=PAL["emerald"], tsize=7.8, bsize=6.2)
    draw_par(c, M_L, 176, "The photo pipeline runs independent of the brain — the ESP32-CAM is its own "
            "little computer with one job: {g:**see the plant, tell the cloud**}. Later pages show what the "
            "cloud and AI do with that photo.", PAGE_W - M_L - M_R, size=8.2, leading=12)
    footer(c, page_no, meta["total"])
