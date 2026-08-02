#!/usr/bin/env python3
"""Project Verde — middle pages: cloud, web app (2), AI & APIs, features, testing."""
from verde_style import (PAL, VARIANT, FB, PAGE_W, PAGE_H, M_L, M_R, M_T, M_B,
                         sw, rrect, hrule, grad_image, dotgrid, chip, icon, icon_circle,
                         parse_runs, draw_par, measure_par, section_header, footer)
from verde_diagrams import schema_tree, api_chain, rain_flow, cost_chart
from pagekit import *

DOCTOR = "assets/prep/doctor_prep.jpg"

# ------------------------------------------------------------------ 11 CLOUD
def cloud_page(c, meta, page_no):
    bg(c, deep=True)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 07 — THE CLOUD", "Firebase: One Truth, Six Branches",
                       "Every byte the system knows lives in one Realtime Database: verde-tech-haha.", y)
    schema_tree(c, M_L, 108, PAGE_W - M_L - M_R, 396)
    yy = y - 22
    rules = [
        ("shield", "Rules that behave", "Public read for the demo, validated writes — booleans stay booleans, "
         "numbers stay 0–100. ESP32 auth: legacy database secret."),
        ("db", "10 metrics, 1 write", "sensors/ carries moisture, temp, humidity, light, tank, lux, watchdog "
         "status, voltage sag, upload counters — bundled per second."),
        ("bolt", "Controls are shared state", "mode, pump, light, thresholds, capture trigger and weather "
         "override live in controls/ — written by the app, obeyed by the ESP32."),
    ]
    bw = (PAGE_W - M_L - M_R - 2 * 14) / 3
    for i, (ic, t, d) in enumerate(rules):
        sx = M_L + i * (bw + 14)
        callout(c, sx, yy - 116, bw, 108, ic, t, d, accent=PAL["gold"] if i == 1 else PAL["emerald"], tsize=7.8, bsize=6.2)
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 12 WEB APP I
def webapp_dash(c, meta, page_no):
    bg(c)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 08 — THE FACE · PART 1", "Dashboard & Weather",
                       "A single-file HTML app — four pages via the burger menu. No frameworks, no build step.", y)
    # left: dashboard mock
    mx, my, mw, mh = M_L, y - 268, PAGE_W * 0.52, 258
    shadow_rrect(c, mx, my, mw, mh, 10, PAL["card"])
    # phone-ish browser chrome
    rrect(c, mx, my + mh - 26, mw, 26, 10, fill=PAL["card2"], stroke=None)
    c.setFillColor(PAL["slate_d"])
    c.circle(mx + 14, my + mh - 13, 4, stroke=0, fill=1)
    c.circle(mx + 26, my + mh - 13, 4, stroke=0, fill=1)
    c.setFillColor(PAL["line"]); c.circle(mx + 38, my + mh - 13, 4, stroke=0, fill=1)
    rrect(c, mx + 54, my + mh - 20, mw - 100, 14, 7, fill=PAL["bg"], stroke=None)
    c.setFont(FB["mono"], 6); c.setFillColor(PAL["slate"])
    c.drawCentredString(mx + mw / 2, my + mh - 17, "verde-tech — dashboard")
    # tiles 3x2
    tiles = [("MOISTURE", "42%", "▲ +6 since 10:00", PAL["emerald"]),
             ("TEMP", "31°C", "▼ −1 · DHT11", PAL["gold"]),
             ("HUMIDITY", "58%", "▲ +3", PAL["emerald"]),
             ("TANK", "74%", "5-pt filter · safe", PAL["gold"]),
             ("LIGHT", "bright", "hysteresis ±2%", PAL["emerald"]),
             ("LUX", "12,400", "LDR module", PAL["gold"])]
    tw = (mw - 30) / 3
    th = (mh - 64) / 2
    for i, (t, v, s, ac) in enumerate(tiles):
        tx_ = mx + 8 + (i % 3) * (tw + 3)
        ty_ = my + mh - 40 - (i // 3) * (th + 4)
        rrect(c, tx_, ty_ - th, tw, th, 6, fill=PAL["card2"], stroke=PAL["line"], sw_=0.6)
        c.setFont(FB["body_b"], 6.2); c.setFillColor(PAL["slate"])
        c.drawString(tx_ + 8, ty_ - 14, t)
        c.setFont(FB["mono_eb"], 12); c.setFillColor(ac)
        c.drawString(tx_ + 8, ty_ - 32, v)
        c.setFont(FB["body"], 5.6); c.setFillColor(PAL["slate_d"])
        c.drawString(tx_ + 8, ty_ - 42, s)
        # sparkline
        import random
        random.seed(i)
        pts = [ty_ - 8 + random.uniform(-4, 4) for _ in range(8)]
        c.saveState(); c.setStrokeColor(ac); c.setLineWidth(0.8)
        c.setDash(0.5, 2)
        c.line(tx_ + tw - 34, ty_ - 16, tx_ + tw - 8, ty_ - 16)
        c.restoreState()
        c.saveState()
        p = c.beginPath()
        p.moveTo(tx_ + tw - 34, pts[0])
        for k in range(1, 8):
            p.lineTo(tx_ + tw - 34 + k * (26 / 7), pts[k])
        c.setStrokeColor(ac); c.setLineWidth(0.9)
        c.drawPath(p, stroke=1, fill=0)
        c.restoreState()
    # right: weather mock
    rx = M_L + mw + 16
    rw = PAGE_W - M_R - rx
    shadow_rrect(c, rx, my, rw, mh, 10, PAL["card"])
    rrect(c, rx, my + mh - 26, rw, 26, 10, fill=PAL["card2"], stroke=None)
    rrect(c, rx + 54, my + mh - 20, rw - 100, 14, 7, fill=PAL["bg"], stroke=None)
    c.setFont(FB["mono"], 6); c.setFillColor(PAL["slate"])
    c.drawCentredString(rx + rw / 2, my + mh - 17, "verde-tech — weather")
    c.setFont(FB["disp_b"], 26); c.setFillColor(PAL["ivory"])
    c.drawString(rx + 14, my + mh - 66, "35°C")
    c.setFont(FB["body_b"], 8); c.setFillColor(PAL["slate"])
    c.drawString(rx + 14, my + mh - 80, "NEW DELHI · LIVE")
    icon(c, rx + rw - 34, my + mh - 52, "sun", 22, PAL["gold"])
    chips_ = [("TUE", "36°"), ("WED", "33°"), ("THU", "31°"), ("FRI", "34°"), ("SAT", "37°")]
    for i, (d, t) in enumerate(chips_):
        cx_ = rx + 14 + i * ((rw - 28) / 5)
        rrect(c, cx_, my + 46, (rw - 28) / 5 - 4, 34, 6, fill=PAL["card2"], stroke=None)
        c.setFont(FB["body_b"], 6.4); c.setFillColor(PAL["slate"])
        c.drawCentredString(cx_ + (rw - 28) / 10, my + 68, d)
        c.setFont(FB["mono_b"], 7); c.setFillColor(PAL["gold"])
        c.drawCentredString(cx_ + (rw - 28) / 10, my + 56, t)
    rrect(c, rx + 14, my + 14, rw - 28, 26, 6, fill=PAL["green_bg"], stroke=None)
    c.setFont(FB["body_b"], 6.4); c.setFillColor(PAL["mint"])
    c.drawString(rx + 24, my + 26, "RAIN OVERRIDE ACTIVE — pump gated · 2:41 remaining")
    # bullets below
    yy = my - 26
    bullets = [
        "**8 live telemetry tiles** with sparklines — hover any tile for a last-10 trend, ▲/▼ arrows",
        "**All 8 controls + 3 threshold sliders** — thresholds persist to NVS, no reflash",
        "**Weather page** — live Delhi conditions, 5-day forecast chips, auto rain-override checked every 3 min",
        "**Predicted actuator states** — the app shows what the ESP32 *will* do before it does it",
        "System status strip · toasts · fullscreen demo mode · uptime timer · moisture history chart",
    ]
    bullet_list(c, M_L, yy, PAGE_W - M_L - M_R, bullets, size=8, leading=13)
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 13 WEB APP II
def webapp_doctor(c, meta, page_no):
    bg(c, deep=True)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 08 — THE FACE · PART 2", "Plant Doctor & AI Assistants",
                       "The pages that make judges say “wait, this is a school project?”", y)
    photo_band(c, DOCTOR, M_L, y - 172, PAGE_W - M_L - M_R, 152,
               caption="Plant Doctor: live camera frame, capture button, diagnosis card, and AI chat on the same image.",
               radius=10)
    yy = y - 196
    colw = (PAGE_W - M_L - M_R - 14) / 2
    callout(c, M_L, yy - 128, colw, 120, "camera", "Plant Doctor",
            "A live camera frame auto-refreshes every ≤2 s. Press CAPTURE — or upload a photo — and "
            "crop.health identifies the plant and any disease, with probability and a treatment plan. "
            "The diagnosis lands back in the same view, and the AI chat sees the same image.",
            accent=PAL["emerald"], tsize=8.6, bsize=6.8)
    callout(c, M_L + colw + 14, yy - 128, colw, 120, "eye", "AI Assistants",
            "Two assistants on demand: a Gemini vision chat that reasons over the analysed photo, and an "
            "OpenRouter chat that reads live sensor telemetry. Quick prompts get the plant talked about "
            "in plain language — “should I water it tonight?”",
            accent=PAL["gold"], tsize=8.6, bsize=6.8)
    yy -= 146
    extras = [
        ("gear", "Tank calibration panel", "SET EMPTY / SET FULL in the app — the tank remaps to real "
         "millimetres with no reflash."),
        ("upload", "Camera flip fix", "The CAM mounts upside-down on the pot; one toggle flips the image. "
         "Physics solved in CSS."),
        ("clock", "Photo ≤2 s", "poll → flash → capture → upload → base64 → screen. The whole loop fits "
         "inside one camera refresh."),
        ("db", "Upload or CAM", "Don’t have the hardware at hand? Upload any plant photo and the whole "
         "pipeline still runs."),
    ]
    bw = (PAGE_W - M_L - M_R - 3 * 12) / 4
    for i, (ic, t, d) in enumerate(extras):
        sx = M_L + i * (bw + 12)
        feature_card(c, sx, yy - 88, bw, 82, ic, t, d, accent=PAL["gold"] if i % 2 else PAL["emerald"])
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 14 AI & APIS
def ai_page(c, meta, page_no):
    bg(c)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 09 — AI & APIS", "Four APIs, Zero Drama",
                       "Researched, keyed, and live-tested. With the accuracy notes to prove it.", y)
    apis = [
        ("OpenWeatherMap", "live weather + 5-day forecast", "key in URL",
         "GET /data/2.5/weather?q=Delhi — ids 2xx/3xx/5xx/6xx set weather_override=1",
         "live-tested: Delhi 35 °C, correct city id 1273294", "sun"),
        ("crop.health (Plant.id)", "plant + disease identification", "Api-Key header",
         "POST /api/v1/identification with base64 image → crop + disease suggestions",
         "test leaf: nutrient deficiency @94% with treatment plan", "leaf"),
        ("Gemini 2.5 Flash", "vision chat on the analysed photo", "X-goog-api-key (AQ keys)",
         "POST /v1beta/models/gemini-flash-latest:generateContent — inline image + diagnosis + telemetry",
         "gemini-2.5-flash no longer offered to new users → gemini-flash-latest", "eye"),
        ("OpenRouter", "sensor chat + vision fallback", "Authorization: Bearer sk-or-v1-…",
         "POST /api/v1/chat/completions (OpenAI-compatible) — 8-model text + 5-model vision chains",
         "435 models; free models rotate → fallback chains never dead-end", "gear"),
    ]
    yy = y - 14
    for name, role, auth, mech, note, ic in apis:
        hh = 86
        shadow_rrect(c, M_L, yy - hh, PAGE_W - M_L - M_R, hh, 9, PAL["card"])
        icon_circle(c, M_L + 26, yy - 26, ic, 26, PAL["gold"])
        c.setFont(FB["body_b"], 9.4); c.setFillColor(PAL["ivory"])
        c.drawString(M_L + 48, yy - 20, name)
        c.setFont(FB["body"], 6.8); c.setFillColor(PAL["slate"])
        c.drawString(M_L + 48, yy - 31, role + "  ·  " + auth)
        draw_par(c, M_L + 48, yy - 40, mech, PAGE_W - M_L - M_R - 56, size=6.4, leading=9, color=PAL["slate"])
        draw_par(c, M_L + 48, yy - 62, "{g:▲} " + note, PAGE_W - M_L - M_R - 56, size=6.6, leading=9, color=PAL["slate"])
        yy -= hh + 10
    api_chain(c, M_L, yy - 90, PAGE_W - M_L - M_R, 84)
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 15 FEATURES
def features_page(c, meta, page_no):
    bg(c, deep=True)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 10 — EVERYTHING LIVE", "Features: All Working, All Demo-Ready",
                       "Not a roadmap. A checklist. Every item here ran in the real demo.", y)
    feats = [
        ("signal", "1-second heartbeat", "10 metrics up, 9 controls down — one bundled call each second."),
        ("drop", "AUTO watering", "moisture < 35% AND tank ≥ 15% AND no rain → pump on, stays on."),
        ("sun", "Smart grow light", "LDR-based, ±2% hysteresis, manual override, threshold from the app."),
        ("cloud", "Live weather", "Delhi conditions + 5-day forecast + rain override with countdown."),
        ("camera", "Plant Doctor", "Live CAM frame, capture ≤2 s, 94% diagnosis with treatment plan."),
        ("eye", "AI vision chat", "Gemini sees the same photo, with the diagnosis as context."),
        ("gear", "AI sensor chat", "OpenRouter reads live telemetry and answers in plain language."),
        ("bolt", "Tank protection", "AUTO and manual both refuse to run a dry pump. Physics, enforced."),
        ("db", "Moisture history", "logged every 60 s — watch the watering cycle chart come alive."),
        ("shield", "Watchdog + NVS", "8 s watchdog, thresholds persisted in flash, reboot-safe."),
        ("upload", "Tank calibration", "SET EMPTY / SET FULL — remap the tank in-app, no reflash."),
        ("clock", "Demo mode", "fullscreen kiosk view with uptime timer — judges love the counter."),
    ]
    cols, rows_ = 3, 4
    bw = (PAGE_W - M_L - M_R - (cols - 1) * 14) / cols
    bh = 92
    for i, (ic, t, d) in enumerate(feats):
        r_, c_ = i // cols, i % cols
        sx = M_L + c_ * (bw + 14)
        sy = y - 10 - r_ * (bh + 12) - bh
        feature_card(c, sx, sy, bw, bh, ic, t, d, accent=PAL["gold"] if i % 3 == 2 else PAL["emerald"])
    y2 = y - 10 - rows_ * (bh + 12) - 4
    draw_par(c, M_L, y2, "Everything above is driven by the same single-file web app — the one the judges "
            "will hold on a phone. {g:**Tap. Water. Diagnose. Chat.**}", PAGE_W - M_L - M_R, size=8.4, leading=12.5)
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 16 TESTING
def testing_page(c, meta, page_no):
    bg(c)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 11 — PROOF", "13 Tests, 13 Passes",
                       "A 13-point test matrix. Everything green — including a 10-minute watchdog run with 0 reboots.", y)
    tests = [
        ["WiFi + boot", "PASS", "3-network fallback verified"],
        ["DHT11 breathe test", "PASS", "stable temp/humidity readings"],
        ["Soil moisture dunk test", "PASS", "water → reading jumps correctly"],
        ["LDR cover test", "PASS", "dark → light threshold triggers"],
        ["Ultrasonic hand test", "PASS", "tank level tracks hand distance"],
        ["Pump AUTO 120 s", "PASS", "no glitch, continuous run"],
        ["OFF at threshold", "PASS", "pump stops exactly at 35%"],
        ["Tank lock", "PASS", "dry tank blocks pumping"],
        ["Rain override", "PASS", "weather_override gates AUTO"],
        ["CAM capture ≤2 s", "PASS", "trigger → screen"],
        ["Plant Doctor", "PASS", "94% diagnosis on test leaf"],
        ["AI chats + fallbacks", "PASS", "8-model / 5-model chains"],
        ["Watchdog 10+ min", "PASS", "0 reboots, 0 stalls"],
    ]
    rows = [[t, f"{'✓' if v=='PASS' else v}  {v}", d] for t, v, d in tests]
    header = ["TEST", "RESULT", "EVIDENCE"]
    col_w = [180, 90, PAGE_W - M_L - M_R - 270]
    table_grid(c, M_L, y - 22 - 20 - 17 * len(tests), PAGE_W - M_L - M_R, header, rows, col_w,
               row_h=17, header_color=PAL["emerald"])
    yy = y - 22 - 20 - 17 * len(tests) - 24
    kpi_card(c, M_L, yy - 70, (PAGE_W - M_L - M_R - 28) / 3, 62, "13/13", "TESTS PASSED",
             "full matrix, all green", PAL["emerald"], value_size=16)
    kpi_card(c, M_L + (PAGE_W - M_L - M_R - 28) / 3 + 14, yy - 70, (PAGE_W - M_L - M_R - 28) / 3, 62,
             "0", "REBOOTS IN 10+ MIN", "watchdog fed every loop", PAL["gold"], value_size=16)
    kpi_card(c, M_L + 2 * (PAGE_W - M_L - M_R - 28) / 3 + 28, yy - 70, (PAGE_W - M_L - M_R - 28) / 3, 62,
             "94%", "BEST DIAGNOSIS", "nutrient deficiency, treatment plan", PAL["emerald"], value_size=16)
    footer(c, page_no, meta["total"])
