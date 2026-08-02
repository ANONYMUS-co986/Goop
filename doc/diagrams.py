"""Generate all charts (matplotlib PNG) and vector diagrams (ReportLab Drawing via SVG)."""
import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing

HERE = os.path.dirname(os.path.abspath(__file__))
CHART_DIR = os.path.join(HERE, "..", "assets", "charts")

NAVY = "#0A1B2E"; NAVY2 = "#0E2A47"; EM = "#17C96E"; EM2 = "#2BD576"
GOLD = "#F5B14C"; GOLD2 = "#E8A33D"; INK = "#122A3B"; GRID = "#DCE6E1"
RED = "#E4572E"; MUTED = "#5B6B78"; SOFT = "#EAF2EE"

def _smooth(y, k=3):
    y = np.asarray(y, float)
    for _ in range(k):
        y = np.convolve(y, [1.0, 2.0, 1.0], mode="same") / 4.0
    return y

def _style(ax, navy_text=True):
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color(GRID)
        ax.spines[s].set_linewidth(1.0)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)

def _read(img):
    return os.path.join(CHART_DIR, img)

def moisture_chart():
    os.makedirs(CHART_DIR, exist_ok=True)
    t = np.arange(0, 96)  # hours
    raw = []
    thresh = 35
    moisture = 68
    np.random.seed(4)
    for i in t:
        moisture -= 0.55 + np.random.rand() * 0.35
        if moisture < thresh + 0.5:
            moisture = 78 + np.random.rand() * 3   # watering event
        raw.append(max(8, moisture))
    y = _smooth(raw, 2)
    fig, ax = plt.subplots(figsize=(8.6, 2.9), dpi=200)
    ax.plot(t, y, color=NAVY, lw=2.2, solid_capstyle="round", zorder=3)
    # area fill under curve to threshold
    ax.fill_between(t, y, thresh, where=y <= thresh + 0.6, color=RED, alpha=0.18, zorder=2)
    ax.fill_between(t, y, thresh, where=y > thresh, color=EM, alpha=0.10, zorder=1)
    ax.axhline(thresh, color=RED, lw=1.8, ls=(0, (4, 3)), zorder=4)
    ax.text(1.5, thresh + 2.5, "watering threshold 35%", color=RED, fontsize=8.5, fontweight="bold")
    ax.axhline(75, color=GOLD, lw=1.3, ls=(0, (2, 4)), alpha=0.9, zorder=4)
    ax.text(1.5, 76.5, "post-water peak", color=GOLD2, fontsize=8.5)
    # watering markers
    for w in np.arange(0, 96, 96 / 5):
        pass
    for xm in [22, 42, 62, 82]:
        ax.plot(xm, 80, marker="o", ms=5, color=GOLD, mec="white", mew=1, zorder=6)
    ax.set_xlim(0, 95); ax.set_ylim(0, 92)
    ax.set_xlabel("hours", color=MUTED, fontsize=9)
    ax.set_ylabel("soil moisture %", color=MUTED, fontsize=9)
    ax.set_xticks(np.arange(0, 96, 12))
    _style(ax)
    ax.margins(x=0)
    fig.tight_layout(pad=0.4)
    fig.savefig(_read("moisture_chart.png"), transparent=True)
    plt.close(fig)
    return _read("moisture_chart.png")

def cost_chart():
    cats = ["Ours\n(Verde)", "Commercial\nsmart kits"]
    ours, comm = 1890, 8500
    fig, ax = plt.subplots(figsize=(7.6, 3.0), dpi=200)
    bars = ax.bar([0, 1], [ours, comm], width=0.55, color=[EM, "#C9D6D0"],
                  zorder=3, edgecolor="none")
    bars[0].set_color(EM)
    bars[1].set_color("#CFDAD6")
    ax.bar(0, ours, width=0.55, color=EM, zorder=3)
    # savings bracket
    ax.annotate("", xy=(1, comm), xytext=(0, comm + 400),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
    ax.text(0.5, comm + 500, "we built it for\n~22% of the price", color=RED,
            ha="center", fontsize=9, fontweight="bold")
    for i, (x, v, yy) in enumerate([(0, "₹1,890", ours), (1, "₹8,000+", comm)]):
        ax.text(x, yy + 120, v, ha="center", fontsize=12, fontweight="bold",
                color=NAVY if i == 0 else MUTED)
    ax.text(0, ours + 700, "all software on free tiers", color=NAVY, ha="center", fontsize=8)
    ax.set_xticks([0, 1]); ax.set_xticklabels(cats, color=NAVY, fontsize=9)
    ax.set_ylim(0, 9800); ax.set_yticks([])
    _style(ax)
    ax.spines["bottom"].set_visible(False)
    fig.tight_layout(pad=0.3)
    fig.savefig(_read("cost_chart.png"), transparent=True)
    plt.close(fig)
    return _read("cost_chart.png")

def heartbeat_timeline():
    """One-second heartbeat: read 10 metrics -> bundle -> 1 write /sensors -> 1 read /controls."""
    fig, ax = plt.subplots(figsize=(8.8, 2.5), dpi=200)
    ax.set_xlim(0, 100); ax.set_ylim(0, 10)
    # timeline bar
    ax.plot([2, 98], [5, 5], color=NAVY, lw=6, solid_capstyle="round", zorder=2)
    segs = [
        (2, 26, "read 10 sensors\n(millis non-blocking)", NAVY2),
        (30, 52, "bundle into one\nJSON payload", EM),
        (56, 78, "1× write  /sensors", EM),
        (82, 98, "1× read  /controls", GOLD),
    ]
    for x0, x1, label, col in segs:
        ax.plot([x0, x1], [5, 5], color=col, lw=8, solid_capstyle="butt", zorder=3, alpha=0.85)
        ax.plot([x0, x1], [5, 5], color="white", lw=2, ls=(0,(2,3)), zorder=4)
    # ticks at segment starts
    for x in [2, 26, 30, 52, 56, 78, 82, 98]:
        ax.plot([x, x], [4.4, 5.6], color=NAVY, lw=1.4, zorder=5)
    # labels above/below
    above = [(14, 0, "t≈0 ms", "read 10 sensors\nsoil · dht · ldr · tank · lux", NAVY2),
             (41, 0, "t≈120 ms", "JSON bundling\n+85% less latency", EM),
             (67, 0, "t≈300 ms", "1 HTTPS write\n10 metrics", EM),
             (90, 0, "t≈450 ms", "1 HTTPS read\n9 control keys", GOLD)]
    below = [(14, 0, "", "", MUTED)]
    for x, _, _t, lab, col in above:
        ax.text(x, 8.1, _t, ha="center", fontsize=8, fontweight="bold", color=col)
        ax.text(x, 6.35, lab, ha="center", fontsize=7.6, color=NAVY, linespacing=1.3)
    ax.text(50, 9.35, "the one-second heartbeat — the whole network does 2 calls/sec", ha="center",
            fontsize=10, color=NAVY, fontweight="bold")
    ax.text(90, 0.9, "≈ 450 ms  round trip", ha="center", fontsize=8, color=MUTED)
    ax.set_yticks([]); ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    fig.tight_layout(pad=0.3)
    fig.savefig(_read("heartbeat.png"), transparent=True)
    plt.close(fig)
    return _read("heartbeat.png")

def _svg(dwg_str, name, scale=None):
    """Render an SVG string to a ReportLab Drawing (vector)."""
    p = os.path.join(CHART_DIR, name + ".svg")
    with open(p, "w") as f:
        f.write(dwg_str)
    drawing = svg2rlg(p)
    if scale is not None:
        drawing.width *= scale; drawing.height *= scale
        drawing.scale(scale, scale)
    return drawing

# ---------------------------------------------------------------- SVG vector diagrams
def architecture():
    def node(x, y, w, h, title, lines, col, grad2=None):
        gid = "g" + str(len(__import__("builtins").list([0])))
        stops = f'<stop offset="0" stop-color="{col}"/><stop offset="1" stop-color="{grad2 or col}"/>'
        grad = f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">{stops}</linearGradient>'
        tx = x + w / 2; ty = y + h - 18
        body = "".join(f'<text x="{x+16}" y="{ty + 16 + i*15}" font-size="11.5" fill="#DFEBE4" font-family="Inter">{ln}</text>'
                       for i, ln in enumerate(lines))
        return (grad +
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="url(#{gid})" opacity="0.97"/>' +
                f'<text x="{tx}" y="{y+24}" font-size="15" font-weight="bold" fill="#fff" font-family="Space Grotesk" text-anchor="middle">{title}</text>' +
                body)
    W, H = 820, 560
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Inter">'
    # background panel
    s += f'<rect width="{W}" height="{H}" fill="#0A1B2E"/>'
    # tier 1 EDGE
    s += node(40, 60, 300, 170, "EDGE · the plant", ["ESP32 WROOM-32  (brain)", "5 sensors · pump · UV LED", "ESP32-CAM  (eyes)", "1-second heartbeat out"], "#14395E", "#0E2A47")
    # tier 2 CLOUD
    s += node(340, 200, 300, 160, "CLOUD · single truth", ["Firebase RTDB", "sensors / controls / logs", "public read · validated writes", "legacy DB secret for ESP32"], "#0EA35A", "#087A42")
    # tier 3 EXPERIENCE
    s += node(600, 320, 200, 150, "EXPERIENCE", ["Single-file web app", "dashboard · weather", "Plant Doctor · AI", "4 external APIs"], "#E8A33D", "#C8841F")
    # arrows
    def arrow(x1, y1, x2, y2, lab, labx, laby, col="#2BD576"):
        mx = (x1 + x2) / 2; my = (y1 + y2) / 2
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2.5" marker-end="url(#arr)"/>'
                f'<text x="{labx}" y="{laby}" font-size="11" fill="{col}" font-weight="bold" text-anchor="middle">{lab}</text>')
    s += f'<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#2BD576"/></marker></defs>'
    s += arrow(190, 230, 360, 250, "HTTPS JSON", 275, 220, "#2BD576")
    s += arrow(500, 360, 610, 375, "REST / polling", 555, 345, "#2BD576")
    s += arrow(660, 320, 560, 250, "controls back", 640, 295, "#F5B14C")
    # bottom stats band
    stats = [("5", "sensors"), ("2", "MCUs"), ("2", "calls/sec"), ("4", "APIs"), ("₹1,890", "total cost")]
    x = 40
    for num, lab in stats:
        s += f'<rect x="{x}" y="470" width="135" height="66" rx="10" fill="#0E2A47"/>'
        s += f'<text x="{x+12}" y="510" font-size="26" font-weight="bold" fill="#2BD576" font-family="Space Grotesk">{num}</text>'
        s += f'<text x="{x+12}" y="527" font-size="11" fill="#AFC3BB">{lab}</text>'
        x += 148
    s += '</svg>'
    return _svg(s, "architecture")

def circuit():
    # ESP32 module center with labelled sensor pins
    def pin(x, y, txt, col):
        return (f'<rect x="{x}" y="{y}" width="14" height="26" rx="4" fill="{col}"/>'
                f'<text x="{x+18}" y="{y+17}" font-size="10" fill="#E7F0EA">{txt}</text>')
    W, H = 760, 480
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Inter">'
    s += f'<rect width="{W}" height="{H}" fill="#0A1B2E"/>'
    # ESP32 board
    s += f'<rect x="300" y="150" width="180" height="150" rx="12" fill="#14395E"/>'
    s += f'<text x="390" y="180" text-anchor="middle" font-size="16" font-weight="bold" fill="#fff" font-family="Space Grotesk">ESP32 WROOM-32</text>'
    s += f'<text x="390" y="196" text-anchor="middle" font-size="10" fill="#AFC3BB">the brain</text>'
    # 3V3/5V/VIN power row
    s += pin(312, 250, "5V", "#0EA35A"); s += pin(345, 250, "3V3", "#0EA35A")
    s += pin(378, 250, "GND", "#5B6B78"); s += pin(411, 250, "GPIO23 → VCC gate", "#F5B14C")
    # sensor boxes around
    sensors = [
        (30, 330, "Soil moisture · LM393", "AO → GPIO34 · VCC gated → GPIO23\npower-gated 15 ms reads", "#0EA35A"),
        (560, 330, "DHT11", "DATA → GPIO4\n1 Hz", "#F5B14C"),
        (30, 70, "LDR module", "AO → GPIO35\nambient light → “dark”", "#2BD576"),
        (560, 70, "HC-SR04 ultrasonic", "TRIG → GPIO18 · ECHO → GPIO19\ntank level, 5-point filter", "#F5B14C"),
        (200, 30, "Relay 2-ch  (active-LOW)", "IN1 → GPIO5 → 5V water pump\nisolated COM/NO supply", "#0EA35A"),
        (470, 30, "UV grow LED", "GPIO12 (active-HIGH, 220Ω)\nphotosynthetic light", "#2BD576"),
    ]
    for x, y, title, body, col in sensors:
        lines = body.split("\n")
        h = 52 + len(lines) * 2
        s += f'<rect x="{x}" y="{y}" width="190" height="{52+len(lines)*13}" rx="10" fill="#0E2A47"/>'
        s += f'<rect x="{x}" y="{y}" width="6" height="{52+len(lines)*13}" rx="3" fill="{col}"/>'
        s += f'<text x="{x+16}" y="{y+22}" font-size="12.5" font-weight="bold" fill="#fff">{title}</text>'
        for i, ln in enumerate(lines):
            s += f'<text x="{x+16}" y="{y+40+i*13}" font-size="10" fill="#B9CCC4">{ln}</text>'
        # wire to esp32
        s += f'<line x1="{x+190}" y1="{y+20}" x2="300" y2="{y+20}" stroke="#3D5A6E" stroke-width="1.5" stroke-dasharray="4 4"/>'
    s += '</svg>'
    return _svg(s, "circuit")

def firebase_schema():
    def leaf(depth, txt):
        return (f'<rect x="{depth}" y="0" width="10" height="10" rx="2" fill="{EM if depth<200 else GOLD}"/>' +
                f'<text x="{depth+16}" y="9" font-size="11" fill="#DCEBE2" font-family="Mono">{txt}</text>')
    W, H = 800, 640
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Inter">'
    s += f'<rect width="{W}" height="{H}" fill="#0A1B2E"/>'
    s += f'<text x="30" y="40" font-size="18" font-weight="bold" fill="#fff" font-family="Space Grotesk">Firebase Realtime Database — verde-tech-haha</text>'
    groups = [
        ("sensors/", ["moisture · temperature · humidity", "light · tank_level · lux", "watchdog_status · voltage_sag", "successful_uploads · failed_uploads"], EM),
        ("controls/", ["manual_mode · pump_state", "light_manual_mode · grow_light_state", "capture_photo", "moisture_threshold · tank_threshold", "light_threshold · weather_override"], EM),
        ("latest_scan/", ["imageUrl (base64) · status", "captured_at · scientificName", "diseaseName · probability", "treatmentPlan"], GOLD),
        ("weather/", ["city · temp · condition", "description · humidity", "wind_speed · rain_expected", "synced_at"], GOLD),
        ("historical_logs/", ["moisture_log  [ {time, moisture} ]"], GOLD),
        ("actuators/", ["pump_actual · grow_light_actual", "mode"], GOLD),
    ]
    y = 78
    for name, leaves, col in groups:
        s += f'<rect x="30" y="{y}" width="250" height="30" rx="8" fill="{col if col==EM else "#8A6A2B"}"/>' if False else ""
        s += f'<rect x="30" y="{y}" width="240" height="26" rx="8" fill="{NAVY2}"/>'
        s += f'<text x="42" y="{y+18}" font-size="12.5" font-weight="bold" fill="#2BD576" font-family="Mono">{name}</text>'
        for i, ln in enumerate(leaves):
            s += f'<text x="52" y="{y+42+i*15}" font-size="10.5" fill="#C7D9D1" font-family="Mono">{ln}</text>'
        s += f'<rect x="30" y="{y+8}" width="6" height="10" rx="3" fill="{col}"/>'
        y += 40 + len(leaves) * 15 + 14
    s += '</svg>'
    return _svg(s, "firebase_schema")

def auto_flow():
    def box(x, y, w, h, txt, col, sub=None):
        lines = txt.split("\n")
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{col}"/>'
        cy = y + h/2 + (len(lines)-1)*8
        for i, ln in enumerate(lines):
            ty = cy + i*16
            s += f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#071525" font-family="Inter">{ln}</text>'
        return s
    def arrow(x1, y1, x2, y2, lab=None):
        s = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#3D8C63" stroke-width="2" marker-end="url(#arr)"/>')
        if lab:
            s += f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2 - 6}" text-anchor="middle" font-size="9.5" fill="#9BC7AF" font-style="italic">{lab}</text>'
        return s
    W, H = 700, 560
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Inter">'
    s += f'<rect width="{W}" height="{H}" fill="#0A1B2E"/>'
    s += (f'<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
          f'<path d="M0,0 L8,4 L0,8 z" fill="#3D8C63"/></marker></defs>')
    # decision diamonds
    def diamond(cx, cy, rw, rh, txt, col):
        s = f'<path d="M{cx} {cy-rh} L{cx+rw} {cy} L{cx} {cy+rh} L{cx-rw} {cy} Z" fill="{col}"/>'
        s += f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#071525">{txt}</text>'
        return s
    s += box(230, 30, 240, 44, "every 1 second (millis)", "#2BD576", "x")
    s += box(230, 110, 240, 44, "read 10 sensor values", "#A7E8C8")
    s += diamond(350, 205, 130, 42, "tank safe?\n≥ threshold", "#2BD576")
    s += diamond(350, 300, 130, 42, "soil < threshold?", "#2BD576")
    s += diamond(350, 395, 130, 42, "rain expected?", "#2BD576")
    s += box(230, 472, 240, 44, "PUMP ON  (relay, isolated)", "#2BD576")
    s += box(500, 472, 150, 44, "pump stays off", "#C9D6D0")
    s += arrow(350, 74, 350, 110)
    s += arrow(350, 154, 350, 163)
    s += arrow(350, 247, 350, 258)
    s += arrow(350, 342, 350, 353)
    s += arrow(350, 437, 350, 472)
    # no branches to off box
    s += arrow(490, 205, 490, 494, "no")   # tank not safe -> off
    s += arrow(220, 300, 130, 494)          # not dry
    s += arrow(220, 395, 130, 494)          # rain
    s += '<text x="40" y="200" font-size="10" fill="#9BC7AF" font-style="italic">tank lock —\nnever dry-pump</text>'
    s += '</svg>'
    return _svg(s, "auto_flow")

def before_after():
    W, H = 820, 430
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Inter">'
    s += f'<rect width="{W}" height="{H}" fill="#0A1B2E"/>'
    # BEFORE panel
    s += f'<rect x="30" y="40" width="360" height="350" rx="14" fill="#2A1410"/>'
    s += f'<text x="50" y="72" font-size="17" font-weight="bold" fill="#E4572E" font-family="Space Grotesk">BEFORE · the bug</text>'
    # 17 little request bars
    bx, by, bw, bh, gap = 50, 340, 26, 16, 8
    for i in range(17):
        col = RED if i < 17 else RED
        s += f'<rect x="{bx + i*(bw+gap)}" y="{by}" width="{bw}" height="{bh}" rx="3" fill="{col}" opacity="0.9"/>'
    s += f'<text x="50" y="390" font-size="11" fill="#F3B3A1">17 HTTPS calls / sec</text>'
    s += (f'<text x="50" y="120" font-size="12.5" fill="#F6D9D0" font-weight="bold">network stalls → watchdog reboot every ~10 s</text>'
          f'<text x="50" y="140" font-size="11" fill="#E9A898">pump clicks ON/OFF in a loop · battery of ~8 s reboots</text>')
    s += f'<text x="50" y="170" font-size="11.5" fill="#F6D9D0">17 calls/sec → 85% latency → crash loop</text>'
    # AFTER panel
    s += f'<rect x="430" y="40" width="360" height="350" rx="14" fill="#0B2A1C"/>'
    s += f'<text x="450" y="72" font-size="17" font-weight="bold" fill="#2BD576" font-family="Space Grotesk">AFTER · the fix</text>'
    for i in range(2):
        s += f'<rect x="{450 + i*150}" y="340" width="130" height="16" rx="3" fill="{EM}"/>'
    s += f'<text x="450" y="315" font-size="11" fill="#9ED6B6">JSON bundling: 1 write + 1 read</text>'
    s += f'<text x="450" y="390" font-size="11" fill="#9ED6B6">2 HTTPS calls / sec</text>'
    s += (f'<text x="450" y="120" font-size="12.5" fill="#C9F0DB" font-weight="bold">one bundled payload · zero reboots</text>'
          f'<text x="450" y="140" font-size="11" fill="#9ED6B6">pump stays ON until threshold reached</text>')
    s += (f'<text x="450" y="170" font-size="11" fill="#C9F0DB">2 calls/sec → ~85% less latency → smooth AUTO</text>')
    # big arrow
    s += f'<text x="410" y="220" font-size="40" text-anchor="middle" fill="#F5B14C" font-family="Space Grotesk">→</text>'
    s += '</svg>'
    return _svg(s, "before_after")

def power_lessons():
    W, H = 820, 360
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="Inter">'
    s += f'<rect width="{W}" height="{H}" fill="#0A1B2E"/>'
    lessons = [
        ("5 V / 2 A adapter", "NOT a USB-PD laptop charger — PD needs a handshake chip the ESP32 lacks, so it outputs ~0 mA.", "#0EA35A"),
        ("1000 µF capacitor", "across 5 V / GND soaks up pump + WiFi current spikes.", "#2BD576"),
        ("1N4007 flyback diode", "across the pump kills inductive spikes.", "#F5B14C"),
        ("isolated pump supply", "relay COM/NO carries its own 5 V — no brownout on the brain.", "#F5B14C"),
    ]
    y = 60
    for title, body, col in lessons:
        s += f'<rect x="40" y="{y}" width="740" height="60" rx="12" fill="#0E2A47"/>'
        s += f'<rect x="40" y="{y}" width="6" height="60" rx="3" fill="{col}"/>'
        s += f'<text x="62" y="{y+26}" font-size="14.5" font-weight="bold" fill="#fff">{title}</text>'
        s += f'<text x="62" y="{y+46}" font-size="11" fill="#B9CCC4">{body}</text>'
        y += 72
    s += '</svg>'
    return _svg(s, "power_lessons")
