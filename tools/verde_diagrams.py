#!/usr/bin/env python3
"""Project Verde — vector infographics, all drawn programmatically on canvas."""
import math
from verde_style import (PAL, VARIANT, FB, parse_runs, draw_par, sw, rrect, hrule,
                         icon, icon_circle, grad_image, chip, dotgrid)

def _dtext(c, x, y, t, font="body", size=8, color=None, align="left"):
    color = color if color is not None else PAL["ivory"]
    c.setFont(FB[font], size)
    if align == "right":
        c.drawRightString(x, y, t)
    elif align == "center":
        c.drawString(x - sw(t, FB[font], size) / 2, y, t)
    else:
        c.drawString(x, y, t)

def _dbox(c, x, y, w, h, title=None, sub=None, fill=None, border=None, r=6,
          title_color=None, sub_color=None, tsize=8.5, ssize=7, mono_title=False):
    if fill is None:
        fill = PAL["card"]
    if border is None:
        border = PAL["line"]
    rrect(c, x, y, w, h, r, fill=fill, stroke=border, sw_=0.9)
    yy = y + h - 12
    if title:
        tlines = title.split("\n")
        for li, tl in enumerate(tlines):
            _dtext(c, x + 10, yy - tsize + 2 - li * (tsize + 2.5), tl,
                   font=("mono_b" if mono_title else "body_b"),
                   size=tsize, color=title_color if title_color else PAL["ivory"])
        yy -= len(tlines) * (tsize + 4.5)
    if sub:
        if sw(sub, FB["body"], ssize) > w - 20:
            draw_par(c, x + 10, yy - ssize + 2, sub, w - 20, size=ssize,
                     leading=ssize + 2.6, color=sub_color if sub_color else PAL["slate"])
        else:
            _dtext(c, x + 10, yy - ssize + 1, sub, font="body", size=ssize,
                   color=sub_color if sub_color else PAL["slate"])
    return x, y, w, h

def _arrow_down(c, x, y0, y1, color=None, label=None, label2=None, lsize=7):
    color = color or PAL["emerald"]
    c.saveState()
    c.setStrokeColor(color); c.setLineWidth(1.4)
    c.line(x, y0, x, y1)
    c.setFillColor(color)
    p = c.beginPath()
    p.moveTo(x - 4, y1 + 6); p.lineTo(x + 4, y1 + 6); p.lineTo(x, y1)
    p.close(); c.drawPath(p, stroke=0, fill=1)
    c.restoreState()
    if label:
        c.setFont(FB["mono_b"], lsize)
        c.setFillColor(PAL["gold"] if VARIANT == "dark" else PAL["gold_d"])
        c.drawCentredString(x, (y0 + y1) / 2 + 10, label)
    if label2:
        c.setFont(FB["mono"], lsize - 1)
        c.setFillColor(PAL["slate_d"])
        c.drawCentredString(x, (y0 + y1) / 2 - 4, label2)

# ------------------------------------------------------------------------------
def arch_diagram(c, x, y, w, h):
    """Three-tier architecture: EDGE / CLOUD / EXPERIENCE."""
    y0, y1, y2 = y, y + h * 0.42, y + h * 0.66
    # ---- EXPERIENCE (bottom tier) ----
    grad_image(c, "navy_v", x, y, w, h * 0.42, alpha=0.55)
    _dtext(c, x + 2, y1 - 16, "EXPERIENCE", font="mono_b", size=8.5, color=PAL["gold"])
    bx = x + 2
    _dbox(c, bx, y + 14, w * 0.46, 56, "Single-file Web App — “the face”",
          "Dashboard · Weather · Plant Doctor · AI Assistants", fill=PAL["card2"])
    bx += w * 0.46 + 10
    _dbox(c, bx, y + 14, w * 0.5, 56, "4 external AI & cloud APIs",
          "OpenWeatherMap · crop.health · Gemini 2.5 Flash · OpenRouter",
          fill=PAL["card2"])
    # api chips
    cx = x + w * 0.5
    for i, t in enumerate(["OPENWEATHER", "CROP.HEALTH", "GEMINI", "OPENROUTER"]):
        _dtext(c, cx - 118 + i * 60, y + 26, t, font="mono_b", size=5.6, color=PAL["slate"])
    # ---- CLOUD (middle tier) ----
    grad_image(c, "navy_up", x, y + h * 0.42, w, h * 0.24, alpha=0.4)
    _dtext(c, x + 2, y2 - 16, "CLOUD", font="mono_b", size=8.5, color=PAL["gold"])
    _dbox(c, x + w * 0.22, y + h * 0.42 + 12, w * 0.56, 62, "Firebase Realtime Database",
          "verde-tech-haha — single source of truth: sensors · controls · latest_scan · weather",
          fill=PAL["card2"], border=PAL["emerald_d"])
    icon(c, x + w * 0.22 + 26, y + h * 0.42 + 40, "db", 20, PAL["emerald"])
    # ---- EDGE (top tier) ----
    _dtext(c, x + 2, y2 + h * 0.34 - 6, "EDGE — in the pot", font="mono_b", size=8.5, color=PAL["gold"])
    _dbox(c, x, y2 + 8, w * 0.52, 84, "ESP32 WROOM-32 — the brain",
          "5 sensors · 2 actuators · non-blocking scheduler · watchdog",
          fill=PAL["card2"], border=PAL["emerald_d"])
    _dbox(c, x + w * 0.52 + 10, y2 + 8, w * 0.48 - 10, 84, "ESP32-CAM — the eyes",
          "OV2640 · SVGA photos on demand · 8 MHz XCLK",
          fill=PAL["card2"], border=PAL["emerald_d"])
    for i, t in enumerate(["SOIL", "DHT11", "LDR", "TANK", "LIGHT"]):
        _dtext(c, x + 8 + i * 30, y2 + 16, t, font="mono_b", size=5.4, color=PAL["mint"])
    _arrow_down(c, x + w / 2, y2 - 2, y + h * 0.42 + 62, label="HTTPS JSON  ·  1-SECOND HEARTBEAT",
                label2="10 metrics write / 9 keys read — one bundled call")
    _arrow_down(c, x + w / 2, y + h * 0.42 - 2, y + 56, color=PAL["gold"],
                label="REST / POLLING", label2="web app + ESP32-CAM")

# ------------------------------------------------------------------------------
def circuit_diagram(c, x, y, w, h):
    """Schematic pin map: ESP32 brain to every module."""
    cx, cy = x + w / 2, y + h / 2
    # central MCU
    _dbox(c, cx - 62, cy - 40, 124, 80, "ESP32\nWROOM-32", sub="the brain", fill=PAL["card2"],
          border=PAL["gold"], tsize=11, ssize=8, mono_title=True)
    _dtext(c, cx, cy + 46, "5 V / 2 A adapter — power", font="mono", size=6.4, color=PAL["slate"], align="center")
    # modules (cx offsets, cy offsets)
    mods = [
        ("SOIL MOISTURE", 0.34, 0.30, "LM393 · AO → GPIO34", "VCC gated → GPIO23", "drop"),
        ("DHT11", -0.36, 0.30, "DATA → GPIO4", "temp + humidity", "sun"),
        ("LDR MODULE", -0.42, -0.30, "AO → GPIO35", "ambient light", "eye"),
        ("HC-SR04", 0.42, -0.30, "TRIG → GPIO18 · ECHO → GPIO19", "tank level, 5-pt filter", "signal"),
        ("2-CH RELAY", 0.36, 0.0, "IN1 → GPIO5 · active-LOW", "switches 5 V pump", "bolt"),
        ("UV GROW LED", -0.34, 0.0, "GPIO12 · active-HIGH · 220 Ω", "photosynthetic light", "sun"),
    ]
    for title, fx_, fy_, pin, role, ic in mods:
        mx, my = cx + fx_ * w * 0.55, cy + fy_ * h * 0.62
        bw, bh = 108, 46
        if fx_ > 0 and fy_ == 0:
            my = cy  # relay mid right
        if fx_ < 0 and fy_ == 0:
            my = cy
        _dbox(c, mx - bw / 2, my - bh / 2, bw, bh, title, role, fill=PAL["card"], border=PAL["line"], tsize=7.5, ssize=6)
        icon(c, mx - bw / 2 + 13, my + 6, ic, 12, PAL["emerald"])
        _dtext(c, mx, my + 10, pin, font="mono", size=5.2, color=PAL["gold"], align="center")
        # wire to MCU
        c.saveState()
        c.setStrokeColor(PAL["slate_d"]); c.setLineWidth(0.8)
        x0, y0 = cx + (62 if mx > cx else -62), cy
        x1, y1 = mx + (bw / 2 if mx > cx else -bw / 2), my
        c.line(x0, y0, x1, y1)
        c.restoreState()
    # power components row
    py = y + 12
    _dbox(c, x + w * 0.02, py, w * 0.3, 40, "1000 µF electrolytic", "across 5 V/GND — absorbs pump + WiFi spikes",
          fill=PAL["card"], border=PAL["line"], tsize=7, ssize=5.8)
    _dbox(c, x + w * 0.36, py, w * 0.3, 40, "1N4007 flyback diode", "across the pump — kills inductive spikes",
          fill=PAL["card"], border=PAL["line"], tsize=7, ssize=5.8)
    _dbox(c, x + w * 0.7, py, w * 0.28, 40, "Relay isolation", "pump on its own 5 V rail via COM/NO",
          fill=PAL["card"], border=PAL["line"], tsize=7, ssize=5.8)

# ------------------------------------------------------------------------------
def schema_tree(c, x, y, w, h):
    """Firebase RTDB schema tree."""
    rows = [
        ("sensors/", "moisture · temperature · humidity · light · tank_level · lux · watchdog_status · voltage_sag · successful_uploads · failed_uploads", "drop", PAL["emerald"]),
        ("controls/", "manual_mode · pump_state · light_manual_mode · grow_light_state · capture_photo · moisture_threshold · tank_threshold · light_threshold · weather_override", "gear", PAL["gold"]),
        ("latest_scan/", "imageUrl (base64) · status · captured_at · scientificName · diseaseName · probability · treatmentPlan", "camera", PAL["emerald"]),
        ("weather/", "city · temp · condition · description · humidity · wind_speed · rain_expected · synced_at", "cloud", PAL["gold"]),
        ("historical_logs/", "moisture_log  [ { time, moisture } ]", "clock", PAL["emerald"]),
        ("actuators/", "pump_actual · grow_light_actual · mode", "bolt", PAL["gold"]),
    ]
    # root
    _dbox(c, x + w * 0.28, y + h - 44, w * 0.44, 36, "verde-tech-haha  (Realtime Database)",
          fill=PAL["card2"], border=PAL["emerald_d"], mono_title=True, tsize=9)
    _dtext(c, x + w * 0.28 + 20, y + h - 24, "", font="body", size=6)
    icon(c, x + w * 0.28 + 20, y + h - 26, "db", 13, PAL["emerald"])
    rh = h - 60
    step = rh / len(rows)
    for i, (name, kids, ic, col) in enumerate(rows):
        ry = y + h - 60 - (i + 1) * step
        bh = step - 6
        # branch line
        c.saveState()
        c.setStrokeColor(PAL["line"]); c.setLineWidth(0.9)
        c.line(x + w * 0.28, y + h - 26, x + w * 0.28, ry + step * 0.55)
        c.line(x + w * 0.28, ry + step * 0.55, x + w * 0.31, ry + step * 0.55)
        c.restoreState()
        bx = x + w * 0.31
        rrect(c, bx, ry, w * 0.66, bh, 6, fill=PAL["card"], stroke=PAL["line"], sw_=0.8)
        c.setFont(FB["mono_b"], 7.5); c.setFillColor(PAL["ivory"])
        c.drawString(bx + 26, ry + bh - 14, name)
        draw_par(c, bx + 26, ry + bh - 20, kids, w * 0.66 - 34, size=6.1, leading=8.4, color=PAL["slate"])
        icon(c, bx + 15, ry + bh / 2 + 4, ic, 11, col)

# ------------------------------------------------------------------------------
def auto_flowchart(c, x, y, w, h):
    """AUTO-mode decision flow."""
    cx = x + w / 2
    def box(cy_, ww, hh, title, sub, fill=None, border=None, tsize=8):
        _dbox(c, cx - ww / 2, cy_ - hh / 2, ww, hh, title, sub, fill=fill, border=border, tsize=tsize)
    def diamond(cy_, ww, hh, title):
        rrect(c, cx - ww / 2, cy_ - hh / 2, ww, hh, 2, fill=PAL["card2"], stroke=PAL["gold"], sw_=1)
        _dtext(c, cx, cy_ + 3, title, font="body_b", size=7.6, color=PAL["gold"], align="center")
    def vconn(y0, y1, color=None, label=None):
        _arrow_down(c, cx, y0, y1, color=color, label=label, lsize=5.6)
    top = y + h - 8
    box(top - 30, 150, 40, "AUTO mode active?", "user toggled in app", fill=PAL["card2"], border=PAL["emerald_d"])
    vconn(top - 50, top - 78)
    diamond(top - 108, 170, 54, "soil moisture <\nthreshold (35%)?")
    vconn(top - 135, top - 158)
    diamond(top - 188, 170, 54, "tank level safe\n(≥ 15%)?")
    vconn(top - 215, top - 238)
    diamond(top - 268, 170, 54, "rain expected\n(weather_override)?")
    vconn(top - 295, top - 318)
    box(top - 348, 150, 44, "Pump ON", "relay IN1 → GPIO5, active-LOW", fill=PAL["green_bg"], border=PAL["emerald"], tsize=8.5)
    _dtext(c, cx, top - 348 - 30, "stays ON until moisture ≥ threshold — no 10 s toggling", font="body", size=6.4, color=PAL["slate"], align="center")
    # side rails: NO exits
    c.saveState(); c.setStrokeColor(PAL["red"]); c.setLineWidth(1.1); c.setLineCap(1)
    c.setFillColor(PAL["red"])
    for dy, lbl in [(top - 108, "NO"), (top - 188, "NO"), (top - 268, "NO")]:
        c.line(cx + 92, dy, cx + 118, dy)
        p = c.beginPath()
        p.moveTo(cx + 118, dy - 3.4); p.lineTo(cx + 118, dy + 3.4); p.lineTo(cx + 124, dy)
        p.close(); c.drawPath(p, stroke=0, fill=1)
        _dtext(c, cx + 106, dy + 5, lbl, font="mono_b", size=5.8, color=PAL["red"], align="center")
    c.restoreState()
    _dtext(c, cx + 118, top - 340, "pump stays OFF", font="body", size=6, color=PAL["slate"])

# ------------------------------------------------------------------------------
def before_after(c, x, y, w, h):
    """THE BIG BUG — BEFORE / AFTER infographic."""
    bw = (w - 24) / 2
    # BEFORE (red)
    bx = x
    grad_image(c, "grad_ink", bx, y, bw, h, alpha=0.5)
    rrect(c, bx, y, bw, h, 10, fill=PAL["red_bg"] if VARIANT == "dark" else PAL["red_bg"], stroke=PAL["red"], sw_=1.2)
    chip(c, bx + 14, y + h - 24, "BEFORE — v3.0.6", size=7, bg=None, color=PAL["red"], border=PAL["red"])
    _dtext(c, bx + bw / 2, y + h - 52, "17 HTTPS calls every second", font="mono_eb", size=13, color=PAL["red"], align="center")
    _dtext(c, bx + bw / 2, y + h - 64, "1 write + 1 read per API key, individually", font="body", size=6.6, color=PAL["slate"], align="center")
    steps = ["Firebase blocks pile up → network stalls",
             "8 s watchdog fires → ESP32 reboots",
             "loop restarts → AUTO mode re-evaluates",
             "pump clicks ON / OFF every ~10 s"]
    sy = y + h - 92
    for i, s in enumerate(steps):
        c.saveState()
        c.setFillColor(PAL["red"])
        c.circle(bx + 30, sy + 2, 3, stroke=0, fill=1)
        if i < len(steps) - 1:
            c.setStrokeColor(PAL["red"]); c.setLineWidth(1); c.setDash(2, 2)
            c.line(bx + 30, sy - 4, bx + 30, sy - 22)
        c.restoreState()
        _dtext(c, bx + 44, sy - 3, s, font="body", size=7.4, color=PAL["ivory"])
        sy -= 30
    # AFTER (emerald)
    ax = x + bw + 24
    grad_image(c, "grad_emerald", ax, y, bw, h, alpha=0.22)
    rrect(c, ax, y, bw, h, 10, fill=PAL["green_bg"] if VARIANT == "dark" else PAL["green_bg"], stroke=PAL["emerald"], sw_=1.2)
    chip(c, ax + 14, y + h - 24, "AFTER — v3.0.7-FINAL", size=7, bg=None, color=PAL["emerald"], border=PAL["emerald"])
    _dtext(c, ax + bw / 2, y + h - 52, "2 bundled calls per second", font="mono_eb", size=13, color=PAL["emerald"], align="center")
    _dtext(c, ax + bw / 2, y + h - 64, "1 write of 10 metrics + 1 read of 9 keys", font="body", size=6.6, color=PAL["slate"], align="center")
    steps2 = ["JSON bundling → ~85% less latency",
              "watchdog fed every loop → 0 reboots",
              "pump stays ON until threshold reached",
              "plant actually gets watered"]
    sy = y + h - 92
    for i, s in enumerate(steps2):
        c.saveState()
        c.setFillColor(PAL["emerald"])
        c.circle(ax + 30, sy + 2, 3, stroke=0, fill=1)
        if i < len(steps2) - 1:
            c.setStrokeColor(PAL["emerald"]); c.setLineWidth(1); c.setDash(2, 2)
            c.line(ax + 30, sy - 4, ax + 30, sy - 22)
        c.restoreState()
        _dtext(c, ax + 44, sy - 3, s, font="body", size=7.4, color=PAL["ivory"])
        sy -= 30
    # center arrow
    c.saveState()
    c.setFillColor(PAL["gold"])
    cx_, cy_ = x + w / 2, y + h / 2
    p = c.beginPath()
    p.moveTo(cx_ - 5, cy_ + 12); p.lineTo(cx_ + 5, cy_ + 12); p.lineTo(cx_, cy_)
    p.close(); c.drawPath(p, stroke=0, fill=1)
    p = c.beginPath()
    p.moveTo(cx_ - 5, cy_ - 12); p.lineTo(cx_ + 5, cy_ - 12); p.lineTo(cx_, cy_)
    p.close(); c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

# ------------------------------------------------------------------------------
def cost_chart(c, x, y, w, h, compare=8000):
    """Horizontal bar comparison: ours vs commercial kits."""
    bars = [
        ("PROJECT VERDE — full system", 1890, PAL["emerald"], "5 sensors + camera + AI, all included"),
        ("Commercial smart-garden kit", compare, PAL["gold"], "typical starter price, no camera, no AI"),
        ("High-end IoT garden systems", 15000, PAL["slate_d"], "premium tier, needs subscription"),
    ]
    maxv = 16000
    left_w = w * 0.42
    # axis
    hrule(c, x, y + 6, w, PAL["line"], 0.8)
    _dtext(c, x + left_w, y + h - 6, "COST (INR)", font="mono_b", size=5.8, color=PAL["slate_d"])
    for tick in [0, 4000, 8000, 12000, 16000]:
        tx = x + left_w + tick / maxv * (w - left_w)
        c.saveState()
        c.setStrokeColor(PAL["line"]); c.setLineWidth(0.5)
        c.line(tx, y + 4, tx, y + 8)
        c.restoreState()
        _dtext(c, tx, y - 8, f"₹{tick//1000}k", font="body", size=5.4, color=PAL["slate_d"], align="center")
    bh = 34
    gap = (h - 12 - len(bars) * bh) / (len(bars) - 1)
    yy = y + h - 8
    for name, val, col, note in bars:
        _dtext(c, x, yy - bh + 9, name, font="body_b", size=7.6, color=PAL["ivory"])
        _dtext(c, x, yy - bh + 0, note, font="body", size=6, color=PAL["slate_d"])
        bw_ = (val / maxv) * (w - left_w)
        rrect(c, x + left_w, yy - bh + 2, max(6, bw_ - 2), bh - 8, 3, fill=col)
        _dtext(c, x + left_w + bw_ + 6, yy - bh + 12, f"₹{val:,}", font="body_b", size=8.5, color=col)
        yy -= bh + gap

# ------------------------------------------------------------------------------
def moisture_chart(c, x, y, w, h):
    """24-hour soil moisture cycle with threshold marker."""
    pad_l, pad_b = 34, 22
    cw, ch = w - pad_l - 8, h - pad_b - 10
    # grid + labels
    _dtext(c, x + 6, y + h - 8, "SOIL MOISTURE %  —  24-HOUR CYCLE", font="mono_b", size=7, color=PAL["slate"])
    for v in [0, 20, 40, 60, 80, 100]:
        gy = y + pad_b + v / 100 * ch
        c.saveState()
        c.setStrokeColor(PAL["line"]); c.setLineWidth(0.4); c.setDash(1, 3)
        c.line(x + pad_l, gy, x + pad_l + cw, gy)
        c.restoreState()
        _dtext(c, x + pad_l - 6, gy - 2, str(v), font="mono", size=5.6, color=PAL["slate_d"], align="right")
    for hr, lbl in [(0, "00:00"), (6, "06:00"), (12, "12:00"), (18, "18:00"), (24, "24:00")]:
        gx = x + pad_l + hr / 24 * cw
        _dtext(c, gx, y + 2, lbl, font="mono", size=5.6, color=PAL["slate_d"], align="center")
    # threshold line 35%
    ty = y + pad_b + 35 / 100 * ch
    c.saveState()
    c.setStrokeColor(PAL["gold"]); c.setLineWidth(1.4); c.setDash(4, 3)
    c.line(x + pad_l, ty, x + pad_l + cw, ty)
    c.restoreState()
    chip(c, x + pad_l + cw - 58, y + pad_b + 35 / 100 * ch + 12, "THRESHOLD 35%", size=5.6,
         bg=PAL["gold_bg"], color=PAL["gold"], border=None, padx=5, pady=2)
    # data: moisture % over 24h (illustrative real pattern)
    pts = [
        (0, 68), (1, 64), (2, 61), (3, 58), (4, 56), (5, 54), (6, 52), (7, 50),
        (8, 48), (9, 46), (10, 44), (11, 42), (12, 40), (13, 38), (14, 36),
        (15, 34), (15.2, 33),  # pump ON at threshold
        (15.4, 42), (15.8, 58), (16, 66), (17, 70), (18, 69), (19, 66),
        (20, 63), (21, 60), (22, 58), (23, 55), (24, 52),
    ]
    def px(t): return x + pad_l + t / 24 * cw
    def py_(v): return y + pad_b + v / 100 * ch
    # area fill (under curve to threshold zone)
    c.saveState()
    p = c.beginPath()
    p.moveTo(px(0), py_(30))
    for t, v in pts:
        p.lineTo(px(t), py_(v))
    p.lineTo(px(24), py_(30)); p.close()
    c.setFillColor(PAL["emerald"]); c.setFillAlpha(0.16)
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()
    # curve
    c.saveState()
    c.setStrokeColor(PAL["emerald"]); c.setLineWidth(2); c.setLineJoin(1)
    p = c.beginPath()
    p.moveTo(px(0), py_(pts[0][1]))
    for t, v in pts[1:]:
        p.lineTo(px(t), py_(v))
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()
    # pump-on marker
    c.saveState()
    c.setFillColor(PAL["gold"])
    c.circle(px(15.2), py_(33), 3.4, stroke=0, fill=1)
    c.restoreState()
    _dtext(c, px(15.2) - 26, py_(33) - 12, "PUMP ON", font="mono_b", size=5.8, color=PAL["gold"])
    _dtext(c, px(16.6) + 10, py_(66) + 4, "watering", font="body", size=6, color=PAL["slate"])

# ------------------------------------------------------------------------------
def heartbeat_timeline(c, x, y, w, h):
    """One-second heartbeat: 1 bundled write + 1 bundled read."""
    c.saveState()
    c.setStrokeColor(PAL["line"]); c.setLineWidth(1)
    c.line(x, y + h / 2, x + w, y + h / 2)
    c.restoreState()
    t0 = x + 20
    _dtext(c, t0 - 8, y + h / 2 + 8, "t=0 s", font="mono", size=6, color=PAL["slate_d"])
    # write packet
    rrect(c, t0 + 6, y + h / 2 + 16, 150, 40, 6, fill=PAL["card2"], stroke=PAL["emerald"], sw_=1)
    icon(c, t0 + 24, y + h / 2 + 36, "upload", 11, PAL["emerald"])
    _dtext(c, t0 + 36, y + h / 2 + 38, "WRITE /sensors — 10 metrics", font="mono_b", size=6.4, color=PAL["mint"])
    _dtext(c, t0 + 36, y + h / 2 + 26, "moisture · temp · humidity · light…", font="body", size=5.6, color=PAL["slate"])
    # read packet
    rrect(c, t0 + 176, y + h / 2 + 16, 150, 40, 6, fill=PAL["card2"], stroke=PAL["gold"], sw_=1)
    icon(c, t0 + 194, y + h / 2 + 36, "cloud", 11, PAL["gold"])
    _dtext(c, t0 + 206, y + h / 2 + 38, "READ /controls — 9 keys", font="mono_b", size=6.4, color=PAL["gold_l"])
    _dtext(c, t0 + 206, y + h / 2 + 26, "mode · pump · thresholds · capture…", font="body", size=5.6, color=PAL["slate"])
    # ticks
    for i in range(6):
        tx_ = t0 + 26 + i * 60
        c.saveState()
        c.setStrokeColor(PAL["slate_d"]); c.setLineWidth(1)
        c.line(tx_, y + h / 2 - 6, tx_, y + h / 2 + 6)
        c.restoreState()
    _dtext(c, t0 + 346, y + h / 2 + 8, "t=1 s → repeat", font="mono", size=6, color=PAL["slate_d"])
    chip(c, x + w - 158, y + 6, "2 CALLS / SECOND — 85% LESS LATENCY", size=6, bg=PAL["green_bg"], color=PAL["emerald"])

# ------------------------------------------------------------------------------
def scheduler_timeline(c, x, y, w, h):
    """Firmware non-blocking task scheduler lanes."""
    lanes = [
        ("SENSORS", "every 1 s", "10-pt MA soil/LDR · 5-pt MA tank · invalid-read rejection", "drop"),
        ("CLOUD", "every 1 s", "bundled write /sensors + read /controls", "cloud"),
        ("WIFI", "every 10 s", "signal health + 3-network fallback (home / hotspot / school)", "wifi"),
        ("WATCHDOG", "fed every loop", "8 s hardware timeout — never starved again", "shield"),
        ("LOGS", "every 60 s", "historical moisture log to Firebase", "clock"),
    ]
    lh = (h - 30) / len(lanes)
    c.saveState()
    c.setStrokeColor(PAL["line"]); c.setLineWidth(0.8)
    c.line(x, y + 6, x, y + h - 6)
    c.restoreState()
    for i, (name, when, desc, ic) in enumerate(lanes):
        ly = y + h - 8 - (i + 1) * lh + 4
        c.saveState()
        c.setFillColor(PAL["gold"])
        c.circle(x, ly + 4, 2.6, stroke=0, fill=1)
        c.restoreState()
        _dtext(c, x + 14, ly - 1, name, font="mono_b", size=7.6, color=PAL["emerald"])
        chip(c, x + 14 + sw(name, FB["mono_b"], 7.6) + 10, ly + 10, when, size=6, bg=PAL["card"], color=PAL["gold"], border=PAL["line"])
        _dtext(c, x + 14, ly - 11, desc, font="body", size=6.6, color=PAL["slate"])
        icon(c, x + w - 12, ly + 4, ic, 10, PAL["slate_d"])

# ------------------------------------------------------------------------------
def photo_pipeline(c, x, y, w, h):
    """ESP32-CAM capture flow, ≤2 s end to end."""
    stages = [
        ("POLL", "/controls/capture_photo — every 1.5 s", "clock", PAL["slate"]),
        ("FLASH + SHOOT", "flash LED → SVGA JPEG capture", "camera", PAL["gold"]),
        ("UPLOAD", "raw bytes → Vercel upload API", "upload", PAL["emerald"]),
        ("STORE", "base64 lands in /latest_scan", "db", PAL["gold"]),
        ("SHOW", "app frame updates ≤ 2 s", "eye", PAL["emerald"]),
    ]
    n = len(stages)
    bw = (w - (n - 1) * 18) / n
    for i, (t, s, ic, col) in enumerate(stages):
        sx = x + i * (bw + 18)
        rrect(c, sx, y + 6, bw, h - 12, 8, fill=PAL["card"], stroke=PAL["line"], sw_=0.8)
        icon(c, sx + bw / 2, y + h - 26, ic, 14, col)
        _dtext(c, sx + bw / 2, y + h - 44, t, font="mono_b", size=6.8, color=col, align="center")
        draw_par(c, sx + 4, y + 26, s, bw - 8, size=5.6, leading=7.6, color=PAL["slate"], align="center")
        if i < n - 1:
            c.saveState()
            c.setStrokeColor(PAL["emerald"]); c.setLineWidth(1.2)
            c.line(sx + bw + 2, y + h / 2, sx + bw + 16, y + h / 2)
            p = c.beginPath()
            p.moveTo(sx + bw + 16, y + h / 2 - 3); p.lineTo(sx + bw + 16, y + h / 2 + 3)
            p.lineTo(sx + bw + 21, y + h / 2); p.close()
            c.setFillColor(PAL["emerald"]); c.drawPath(p, stroke=0, fill=1)
            c.restoreState()

# ------------------------------------------------------------------------------
def api_chain(c, x, y, w, h):
    """OpenRouter fallback chains: 8-model text + 5-model vision."""
    col_w = (w - 20) / 2
    # text chain
    rrect(c, x, y, col_w, h, 10, fill=PAL["card"], stroke=PAL["emerald"], sw_=0.9)
    _dtext(c, x + 12, y + h - 22, "TEXT CHAIN — 8 MODELS", font="mono_b", size=7.2, color=PAL["emerald"])
    _dtext(c, x + 12, y + h - 32, "sensor-aware chat, OpenAI-compatible", font="body", size=6.2, color=PAL["slate"])
    models = ["meta-llama · mistral · qwen · deepseek", "command-r · gpt-4o-mini · gemini · free tier rotation"]
    yy = y + h - 44
    for m in models:
        _dtext(c, x + 12, yy - 5, m, font="mono", size=6.4, color=PAL["ivory"])
        yy -= 14
    c.saveState()
    c.setStrokeColor(PAL["emerald_d"]); c.setLineWidth(1); c.setDash(2, 3)
    c.line(x + 12, yy + 2, x + col_w - 12, yy + 2)
    c.restoreState()
    _dtext(c, x + 12, yy - 14, "if model A fails → try B → … never a dead end", font="body", size=6.4, color=PAL["slate"])
    icon(c, x + col_w / 2, y + 26, "gear", 13, PAL["emerald"])
    # vision chain
    x2 = x + col_w + 20
    rrect(c, x2, y, col_w, h, 10, fill=PAL["card"], stroke=PAL["gold"], sw_=0.9)
    _dtext(c, x2 + 12, y + h - 22, "VISION CHAIN — 5 MODELS", font="mono_b", size=7.2, color=PAL["gold"])
    _dtext(c, x2 + 12, y + h - 32, "sees the same plant photo + diagnosis", font="body", size=6.2, color=PAL["slate"])
    _dtext(c, x2 + 12, y + h - 52, "gemini-flash-latest (primary)", font="mono", size=6.4, color=PAL["ivory"])
    _dtext(c, x2 + 12, y + h - 68, "4 vision-capable fallbacks", font="mono", size=6.4, color=PAL["ivory"])
    _dtext(c, x2 + 12, y + h - 92, "435 models accessible via one key", font="body", size=6.4, color=PAL["slate"])
    icon(c, x2 + col_w / 2, y + 26, "eye", 13, PAL["gold"])

# ------------------------------------------------------------------------------
def troubleshoot_timeline(c, x, y, w, h):
    """10 bugs → 10 fixes, vertical journal timeline."""
    bugs = [
        ("AUTO pump clicked ON/OFF every ~10 s", "17 blocking HTTPS calls/s → JSON bundling: 2 calls/s"),
        ("Camera probe 0x106 — not found", "FPC ribbon unseated → reseat, gold-side down, power cycle"),
        ("PSRAM not found", "Weak power → dedicated 5 V / 2 A adapter"),
        ("Boot crash 0x20002", "Camera + WiFi power surge → sequential boot, camera first"),
        ("RF interference killed WiFi", "20 MHz XCLK → throttled to 8 MHz"),
        ("67 W USB-PD charger starved the board", "PD needs a handshake chip → plain 5 V / 2 A adapter"),
        ("Relay dead — pump never switched", "Split breadboard rails → bridge + to +, − to −"),
        ("temp always 0 °C", "DHT11 on wrong pin → GPIO 4 + shared GND"),
        ("Firebase “spurts” — 13 calls/s", "One bundled call per second"),
        ("Compile error: missing terminating quote", "Copy-paste corruption → re-download the file"),
    ]
    step = h / len(bugs)
    c.saveState()
    c.setStrokeColor(PAL["gold"]); c.setLineWidth(1.2)
    c.line(x + 14, y + 4, x + 14, y + h - 4)
    c.restoreState()
    for i, (bug, fix) in enumerate(bugs):
        by = y + h - 6 - (i + 1) * step
        c.saveState()
        c.setFillColor(PAL["gold"])
        c.circle(x + 14, by + 6, 3, stroke=0, fill=1)
        c.restoreState()
        _dtext(c, x + 30, by - 2, f"{i+1:02d}", font="mono_eb", size=8, color=PAL["gold"])
        _dtext(c, x + 52, by - 2, bug, font="body_b", size=7.4, color=PAL["ivory"])
        _dtext(c, x + 52, by - 13, "→  " + fix, font="body", size=6.6, color=PAL["slate"])

# ------------------------------------------------------------------------------
def roadmap(c, x, y, w, h):
    """Future scope roadmap timeline."""
    items = [
        ("NOW", "Solar autonomy", "12 V panel + charge controller + battery", PAL["emerald"]),
        ("Q3", "Smarter soil", "NPK probe: nitrogen, phosphorus, potassium", PAL["gold"]),
        ("Q4", "Multi-plant", "one brain, many pots, per-plant watering", PAL["emerald"]),
        ("2027", "Talks to you", "Telegram & WhatsApp alerts", PAL["gold"]),
        ("2027", "Learns", "predictive watering from logs", PAL["emerald"]),
        ("2028", "Scales", "deployed Next.js dashboard", PAL["gold"]),
    ]
    n = len(items)
    bw = (w - (n - 1) * 16) / n
    c.saveState()
    c.setStrokeColor(PAL["line"]); c.setLineWidth(1.4)
    c.line(x, y + h * 0.28, x + w, y + h * 0.28)
    c.restoreState()
    for i, (tag, t, d, col) in enumerate(items):
        sx = x + i * (bw + 16)
        cx_ = sx + bw / 2
        c.saveState()
        c.setFillColor(col)
        c.circle(cx_, y + h * 0.28, 4, stroke=0, fill=1)
        c.setStrokeColor(col); c.setLineWidth(1)
        c.line(cx_, y + h * 0.28, cx_, y + h * 0.28 + 18)
        c.restoreState()
        chip(c, cx_ - 14, y + h * 0.28 + 14, tag, size=5.8, bg=PAL["card"], color=col, border=PAL["line"])
        _dtext(c, cx_, y + h * 0.28 - 14, t, font="body_b", size=7.4, color=PAL["ivory"], align="center")
        draw_par(c, sx + 2, y + h * 0.28 - 26, d, bw - 4, size=5.7, leading=7.4,
                 color=PAL["slate"], align="center")

# ------------------------------------------------------------------------------
def rain_flow(c, x, y, w, h):
    """Weather rain-override logic."""
    stages = [
        ("EVERY 3 MIN", "app polls OpenWeatherMap — Delhi, city id 1273294", "clock"),
        ("CHECK CODES", "ids 2xx · 3xx · 5xx · 6xx  →  rain", "eye"),
        ("OVERRIDE", "weather_override = 1  (countdown shown in app)", "bolt"),
        ("AUTO GATES", "pump_ON = moisture < 35% AND tank ≥ 15% AND no rain", "shield"),
    ]
    n = len(stages)
    bw = (w - (n - 1) * 14) / n
    for i, (t, s, ic) in enumerate(stages):
        sx = x + i * (bw + 14)
        rrect(c, sx, y + 6, bw, h - 12, 8, fill=PAL["card"], stroke=PAL["line"], sw_=0.8)
        icon(c, sx + bw / 2, y + h - 24, ic, 12, PAL["emerald"] if i % 2 == 0 else PAL["gold"])
        _dtext(c, sx + bw / 2, y + h - 42, t, font="mono_b", size=6.4, color=PAL["gold"], align="center")
        _dtext(c, sx + 6, y + 16, s, font="body", size=5.7, color=PAL["slate"], align="center")
        if i < n - 1:
            _arrow_down(c, sx + bw + 7, y + h - 20, y + 20, color=PAL["slate_d"])
