#!/usr/bin/env python3
"""Project Verde — back pages: troubleshooting, cost, future, judge tour, conclusion."""
from verde_style import (PAL, VARIANT, FB, PAGE_W, PAGE_H, M_L, M_R, M_T, M_B,
                         sw, rrect, hrule, grad_image, dotgrid, chip, icon, icon_circle,
                         parse_runs, draw_par, measure_par, section_header, footer)
from verde_diagrams import troubleshoot_timeline, roadmap, cost_chart
from pagekit import *

FUTURE = "assets/prep/future_prep.jpg"
QR = "assets/prep/qr.png"

# ------------------------------------------------------------------ 17 TROUBLESHOOTING
def troubleshooting_page(c, meta, page_no):
    bg(c, deep=True)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 12 — THE JOURNAL", "Ten Bugs We Hit. Ten Fixes We Kept.",
                       "Honesty is a feature. Every one of these cost us real evenings — and taught us more than any tutorial.", y)
    troubleshoot_timeline(c, M_L, 110, PAGE_W * 0.56, 520)
    rx = M_L + PAGE_W * 0.56 + 22
    rw = PAGE_W - M_R - rx
    callout(c, rx, y - 126, rw, 112, "alert", "Why we show the failures",
            "A demo that never broke teaches you nothing about the builders. The 17-calls bug, the "
            "USB-PD starvation, the FPC ribbon — each one is a real debugging story. "
            "Judges ask about the hard parts. We have receipts.",
            accent=PAL["gold"])
    callout(c, rx, y - 258, rw, 112, "gear", "The pattern in every fix",
            "Measure the symptom. Find the systemic cause — not the patch. Rebooting? It was the "
            "data flow. Not reading? It was power. That discipline is the actual engineering.",
            accent=PAL["emerald"])
    callout(c, rx, y - 390, rw, 112, "book", "What we’d tell next year’s team",
            "Start with the wiring diagram. Test the power rail first. Never debug the network until "
            "the watchdog is fed. And when a charger “doesn’t work”, check the handshake, not the wattage.",
            accent=PAL["gold"])
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 18 COST
def cost_page(c, meta, page_no):
    bg(c)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 13 — COST & SUSTAINABILITY", "₹1,890. Everything. Yes, Really.",
                       "The full system — hardware, power, mechanics, and every API on free tiers.", y)
    rows = [
        ["Electronics", "ESP32 · ESP32-CAM · 5 sensors · relay · pump · UV LED", "1,320"],
        ["Power & protection", "5 V / 2 A adapter · 1000 µF cap · 1N4007 diode", "220"],
        ["Mechanical", "breadboard · wires · enclosure", "350"],
        ["Software & APIs", "all free tiers — Firebase, OWM, crop.health, Gemini, OpenRouter", "0"],
    ]
    header = ["CATEGORY", "WHAT’S INSIDE", "INR"]
    col_w = [130, PAGE_W - M_L - M_R - 130 - 90, 90]
    table_grid(c, M_L, y - 22 - 20 - 17 * 4, PAGE_W - M_L - M_R, header, rows, col_w,
               row_h=17, align_cols=["l", "l", "r"])
    yy = y - 22 - 20 - 17 * 4 - 26
    # total strip
    shadow_rrect(c, M_L, yy - 40, PAGE_W - M_L - M_R, 34, 8, PAL["card2"])
    c.setFont(FB["body_b"], 8); c.setFillColor(PAL["slate"])
    c.drawString(M_L + 14, yy - 26, "TOTAL")
    c.setFont(FB["body_bl"], 15); c.setFillColor(PAL["gold"])
    c.drawRightString(PAGE_W - M_R - 14, yy - 28, "≈ ₹1,890  (≈ $23 USD)")
    yy -= 64
    yy = draw_par(c, M_L, yy, "**The chart below is the whole point:** {g:₹1,890 for the complete system} — camera, "
            "five sensors, AI, the works — versus ₹8,000+ for a starter kit that still can’t see the plant.",
            PAGE_W - M_L - M_R, size=8.6, leading=12.5) - 18
    cost_chart(c, M_L, yy - 160, PAGE_W - M_L - M_R, 150)
    yy -= 186
    sust = [
        ("leaf", "Low-power by design", "power-gated 15 ms sensor reads, non-blocking scheduler — "
         "runs happily on a phone adapter."),
        ("sun", "Solar-ready", "the roadmap adds a 12 V panel + charge controller + battery for "
         "off-grid autonomy."),
        ("db", "Free-tier cloud", "Firebase, weather, and AI all on free tiers — running cost ≈ ₹0/month."),
        ("gear", "Repairable by students", "no proprietary parts, no black boxes — every wire is "
         "traceable on the schematic."),
    ]
    bw = (PAGE_W - M_L - M_R - 3 * 12) / 4
    for i, (ic, t, d) in enumerate(sust):
        sx = M_L + i * (bw + 12)
        feature_card(c, sx, yy - 76, bw, 70, ic, t, d, accent=PAL["gold"] if i % 2 else PAL["emerald"])
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 19 FUTURE
def future_page(c, meta, page_no):
    bg(c, deep=True)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 14 — WHAT’S NEXT", "Future Scope: From One Pot to a Campus",
                       "Solar, smarter soil, and plants that message you. The architecture is ready for all of it.", y)
    photo_band(c, FUTURE, M_L, y - 170, PAGE_W - M_L - M_R, 148,
               caption="Where this is heading — a solar-powered smart greenhouse, at dusk, watching its own garden.",
               radius=10)
    yy = y - 192
    roadmap(c, M_L, yy - 156, PAGE_W - M_L - M_R, 150)
    yy -= 186
    bullets = [
        "**Solar autonomy** — 12 V panel + charge controller + battery. The pot waters itself off-grid.",
        "**NPK soil probe** — nitrogen, phosphorus, potassium. From “is it wet?” to “what does it need?”",
        "**Multi-plant zones** — one brain, many pots, per-plant watering schedules.",
        "**Telegram & WhatsApp alerts** — “your basil is thirsty” arrives as a chat message.",
        "**Predictive watering** — the moisture logs train a model that waters *before* the wilt.",
        "**Deployed dashboard** — a scaffolded Next.js app ready to grow beyond the single file.",
    ]
    yy = bullet_list(c, M_L, yy, PAGE_W - M_L - M_R, bullets, size=8.4, leading=14) - 22
    draw_par(c, M_L, yy, "The hardware already earns the roadmap: power-gated sensors, tank protection, "
            "and a watchdog that survives 10-minute runs. Scaling Verde is a software problem — "
            "and software is the cheap part.", PAGE_W - M_L - M_R, size=8.6, leading=12.5)
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 20 JUDGE TOUR
def tour_page(c, meta, page_no):
    bg(c)
    y = PAGE_H - 64
    y = section_header(c, "CHAPTER 15 — THE LIVE TOUR", "The 3-Minute Judge Script",
                       "Six stops. Practice it twice. The hardware and the app do the rest.", y)
    stops = [
        ("0:00", "The hook", "“This is a plant that waters itself — and it can tell us when it’s sick.” "
         "Point at the dashboard: 8 live tiles, already moving."),
        ("0:30", "The brain", "Open the pot. Show the ESP32 and five sensors. “It reads soil, air, light "
         "and the water tank — every second.”"),
        ("1:00", "The AUTO moment", "Dip the probe in water — the moisture tile climbs. “Watch the pump "
         "logic: below 35%, tank safe, no rain → water.”"),
        ("1:30", "The eyes", "Tap CAPTURE in Plant Doctor. Count to two — the photo appears. “That’s an "
         "ESP32-CAM, end to end, under 2 seconds.”"),
        ("2:00", "The AI", "“What’s wrong with this leaf?” — the diagnosis card and AI chat answer together. "
         "Mention the 94% on our test leaf."),
        ("2:30", "The honesty", "“And here’s the bug that nearly killed it — 17 cloud calls a second, "
         "reboots, the works. We fixed it with one bundled call.” Then: the cost — ₹1,890."),
    ]
    yy = y - 16
    for t, title, script in stops:
        hh = 74
        shadow_rrect(c, M_L, yy - hh, PAGE_W - M_L - M_R, hh, 9, PAL["card"])
        c.setFont(FB["mono_eb"], 13); c.setFillColor(PAL["gold"])
        c.drawString(M_L + 16, yy - 24, t)
        c.setFont(FB["body_b"], 9.4); c.setFillColor(PAL["ivory"])
        c.drawString(M_L + 78, yy - 24, title)
        draw_par(c, M_L + 78, yy - 38, script, PAGE_W - M_L - M_R - 96, size=7.6, leading=10.6, color=PAL["slate"])
        yy -= hh + 10
    draw_par(c, M_L, yy - 6, "Practice the transitions. The system runs itself — the tour is just "
            "pointing at the truth. {g:**Good luck. Not that you’ll need it.**}", PAGE_W - M_L - M_R,
            size=8.4, leading=12.5)
    footer(c, page_no, meta["total"])

# ------------------------------------------------------------------ 21 CONCLUSION
def conclusion_page(c, meta, page_no):
    bg(c, deep=True)
    y = PAGE_H - 64
    dotgrid(c, M_L, 40, PAGE_W - M_L - M_R, PAGE_H - 140, spacing=26, alpha=0.10)
    y = section_header(c, "IN CLOSING", "Two Students. One Watered Idea.",
                       "Project Verde is complete, tested, and demo-ready.", y)
    pull_quote(c, M_L, y - 40, PAGE_W * 0.8,
               "We didn’t build a gadget. We built a plant that can finally speak.",
               author="— Aarav & Anuj, Class X", size=17)
    yy = y - 140
    yy = draw_par(c, M_L, yy, "Five sensors, two microcontrollers, one honest database, one beautiful web app, "
            "and four APIs that never once billed us. The system waters, watches, diagnoses, and talks — "
            "for less than the price of a fancy dinner.", PAGE_W - M_L - M_R, size=9, leading=13.5) - 14
    draw_par(c, M_L, yy, "Thank you for reading — and for judging. The demo is live on the table next to us. "
            "The plant is ready. {g:**So are we.**}", PAGE_W - M_L - M_R, size=9, leading=13.5)
    # QR card
    qx, qy = PAGE_W - M_R - 132, 96
    shadow_rrect(c, qx, qy, 132, 168, 10, PAL["card"])
    rrect(c, qx + 22, qy + 70, 88, 88, 6, fill=PAL["white"] if VARIANT == "dark" else PAL["bg"], stroke=None)
    c.drawImage(QR, qx + 24, qy + 72, width=84, height=84, mask="auto")
    c.setFont(FB["body_b"], 7.2); c.setFillColor(PAL["ivory"])
    c.drawCentredString(qx + 66, qy + 56, "SCAN THE LIVE DATA")
    c.setFont(FB["body"], 5.8); c.setFillColor(PAL["slate"])
    c.drawCentredString(qx + 66, qy + 46, "verde-tech-haha — Firebase feed")
    c.drawCentredString(qx + 66, qy + 38, "(swap in your hosted demo URL)")
    # left column credits
    lx = M_L
    credits = [
        ("drop", "The system", "ESP32 brain · ESP32-CAM eyes · 5 sensors · 2 actuators · Firebase · single-file web app"),
        ("book", "The numbers", "₹1,890 total · 17→2 calls/s · 94% diagnosis · 13/13 tests · 8 MHz XCLK"),
        ("heart", "The builders", "Aarav Choudhary & Anuj — Class X, DAV — built, broke, fixed, and shipped every part"),
    ]
    cy = 150
    for ic, t, d in credits:
        callout(c, lx, cy, PAGE_W - M_R - 160, 66, ic, t, d, accent=PAL["gold"], tsize=8.2, bsize=6.4)
        cy += 76
    hrule(c, lx, 74, PAGE_W - M_L - M_R, PAL["line"], 0.8)
    c.setFont(FB["mono"], 6.4); c.setFillColor(PAL["slate_d"])
    c.drawString(lx, 62, "PROJECT VERDE — DAV ACON 5 TECH EXHIBITION · 2026 · DOCUMENTATION v1.0")
    c.drawRightString(PAGE_W - M_R, 62, "THAT’S THE WHOLE STORY. THANKS FOR READING.")
