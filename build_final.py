#!/usr/bin/env python3
"""
Project Verde — V2 Polished
Fixes: Rs. encoding, TOC overflow, hyperlinked TOC, enhanced cover art, improved KPI
"""
from pathlib import Path
ASSETS_DIR = Path("assets")
ASSETS_DIR.mkdir(exist_ok=True)

def generate_charts():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    NAVY = "#0B1D3A"
    EMERALD = "#10B981"
    EMERALD_DARK = "#059669"
    GOLD = "#F59E0B"
    GRAY = "#9CA3AF"

    # Cost comparison - using Rs.
    fig, ax = plt.subplots(figsize=(6,3.2), dpi=200)
    categories = ['Verde\n(Our Build)', 'Basic Kit\n(Amazon)', 'Premium\nGardena']
    costs = [1890, 8000, 12500]
    colors = [EMERALD, "#CBD5E1", "#94A3B8"]
    bars = ax.bar(categories, costs, color=colors, width=0.55, edgecolor='white', linewidth=1.2, zorder=3)
    for bar, cost in zip(bars, costs):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+250, f"Rs. {cost:,}", ha='center', va='bottom', fontsize=11, fontweight='bold', color=NAVY)
    ax.set_ylabel('Cost (INR)', fontsize=10, color=NAVY)
    ax.set_ylim(0, 15000)
    ax.grid(axis='y', alpha=0.15, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.annotate('76% cheaper\nthan basic kits', xy=(0,1890), xytext=(0.7, 7000),
                fontsize=9, color=EMERALD_DARK, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=EMERALD_DARK, lw=1.2),
                ha='center', bbox=dict(boxstyle='round,pad=0.4', fc='#D1FAE5', ec='none'))
    plt.tight_layout()
    plt.savefig(ASSETS_DIR / "cost_comparison.png", bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots(figsize=(6,3.2), dpi=200)
    t = np.linspace(0, 120, 200)
    moisture = np.piecewise(t, [t<75, t>=75],
                            [lambda tt: 27 + (35-27)*(tt/75) + 0.4*np.sin(tt*0.3),
                             lambda tt: 35 + (42-35)*(1 - np.exp(-(tt-75)/25))])
    moisture += np.random.normal(0,0.15,size=t.shape)
    ax.plot(t, moisture, color=EMERALD, linewidth=2.5, label='Soil Moisture')
    ax.axhline(35, color=GOLD, linestyle='--', linewidth=1.5, label='Threshold 35%')
    ax.fill_between(t, 0, 100, where=(t<75), color=EMERALD, alpha=0.08, label='Pump ON')
    ax.text(25, 70, 'PUMP ON\n(AUTO)', ha='center', fontsize=8, fontweight='bold', color=EMERALD_DARK,
            bbox=dict(facecolor='#D1FAE5', edgecolor='none', boxstyle='round,pad=0.3'))
    ax.text(95, 70, 'PUMP OFF - Target Reached', ha='center', fontsize=8, color=GRAY)
    ax.set_xlabel('Time (seconds)', fontsize=10)
    ax.set_ylabel('Moisture %', fontsize=10)
    ax.set_ylim(20,75)
    ax.set_xlim(0,120)
    ax.grid(alpha=0.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc='lower right')
    plt.tight_layout()
    plt.savefig(ASSETS_DIR / "moisture_cycle.png", bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots(figsize=(6,3.0), dpi=200)
    labels = ['BEFORE\n17 calls / sec', 'AFTER\n2 calls / sec\n(JSON Bundled)']
    values = [17, 2]
    colors = ["#EF4444", EMERALD]
    bars = ax.bar(labels, values, color=colors, width=0.5, edgecolor='white', linewidth=1.5, zorder=3)
    for bar, v in zip(bars, values):
        ax.text(bar.get_x()+bar.get_width()/2, v+0.4, f"{v}", ha='center', va='bottom', fontsize=14, fontweight='bold', color=NAVY)
    ax.set_ylabel('HTTPS Requests / sec')
    ax.set_ylim(0,20)
    ax.annotate('', xy=(1,2.5), xytext=(0,16),
                arrowprops=dict(arrowstyle='->,head_width=0.6,head_length=0.6', color=GOLD, lw=2.5, connectionstyle='arc3,rad=0.3'))
    ax.text(0.5, 10, '-85%\nlatency\n0 reboots', ha='center', fontsize=10, fontweight='bold', color=GOLD,
            bbox=dict(facecolor='#FEF3C7', edgecolor='none', boxstyle='round,pad=0.5'))
    ax.grid(axis='y', alpha=0.15, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(ASSETS_DIR / "api_before_after.png", bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots(figsize=(6,2.0), dpi=200)
    ax.set_xlim(0,1000)
    ax.set_ylim(0,3)
    ax.axis('off')
    ax.plot([0,1000], [1.5,1.5], color=NAVY, linewidth=2, solid_capstyle='round', alpha=0.2)
    events = [
        (50, "Sensors\n1 Hz", EMERALD),
        (250, "10-pt Avg\nFilter", "#6366F1"),
        (450, "JSON Bundle\n10 metrics -> /sensors", NAVY),
        (650, "Read /controls\n9 keys", GOLD),
        (850, "Auto Logic\nDecision", EMERALD_DARK),
    ]
    for x, label, col in events:
        ax.plot([x,x], [1.5,2.2], color=col, linewidth=2)
        ax.scatter([x], [1.5], s=90, color=col, zorder=5, edgecolor='white', linewidth=1.5)
        ax.text(x, 2.4, label, ha='center', va='bottom', fontsize=7, fontweight='bold', color=NAVY)
        ax.text(x, 0.6, f"{x}ms", ha='center', fontsize=6, color=GRAY)
    ax.text(500, 0.15, '<---- 1-Second Heartbeat - repeats every 1000 ms ---->', ha='center', fontsize=8, color=NAVY, fontweight='bold')
    plt.tight_layout()
    plt.savefig(ASSETS_DIR / "heartbeat.png", bbox_inches='tight')
    plt.close()
    print("Charts V2 generated")

def generate_placeholders():
    from PIL import Image, ImageDraw, ImageFont
    def make_placeholder(path, title, subtitle, accent):
        W,H = 800, 480
        img = Image.new('RGB', (W,H), color="#F3F4F6")
        draw = ImageDraw.Draw(img)
        for x in range(0,W,40):
            draw.line([(x,0),(x,H)], fill="#E5E7EB", width=1)
        for y in range(0,H,40):
            draw.line([(0,y),(W,y)], fill="#E5E7EB", width=1)
        draw.ellipse([W-300, -100, W+100, 300], fill=accent)
        draw.ellipse([ -100, H-200, 250, H+100], fill="#D1FAE5")
        try:
            f_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
            f_sub = ImageFont.truetype("DejaVuSans.ttf", 16)
        except:
            f_title = ImageFont.load_default()
            f_sub = ImageFont.load_default()
        draw.text((40, 160), title, fill="#0B1D3A", font=f_title)
        draw.text((40, 210), subtitle, fill="#4B5563", font=f_sub)
        draw.rounded_rectangle([40,280, 340,315], radius=8, fill="white", outline="#E5E7EB")
        draw.text((55,288), "Photo Placeholder - Replace", fill="#9CA3AF", font=f_sub)
        img.save(path)
    make_placeholder(ASSETS_DIR / "hardware_placeholder.png",
                     "Hardware Bench", "ESP32 WROOM-32 + 5 Sensors + Pump\n1000uF cap + flyback diode + isolation", "#10B981")
    make_placeholder(ASSETS_DIR / "plant_doctor_placeholder.png",
                     "Plant Doctor - AI Vision", "ESP32-CAM OV2640 @ 8MHz XCLK\nCapture -> Vercel -> Base64 -> 94%", "#F59E0B")
    print("Placeholders V2")

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, Table, TableStyle, Image, NextPageTemplate, Flowable)
from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Polygon, Line

W, H = A4
NAVY = HexColor("#0B1D3A")
NAVY_LIGHT = HexColor("#1E3A5F")
EMERALD = HexColor("#10B981")
EMERALD_DARK = HexColor("#059669")
EMERALD_LIGHT = HexColor("#D1FAE5")
EMERALD_PALE = HexColor("#ECFDF5")
GOLD = HexColor("#F59E0B")
GOLD_LIGHT = HexColor("#FEF3C7")
GOLD_DARK = HexColor("#D97706")
GRAY_50 = HexColor("#F9FAFB")
GRAY_100 = HexColor("#F3F4F6")
GRAY_200 = HexColor("#E5E7EB")
GRAY_400 = HexColor("#9CA3AF")
GRAY_600 = HexColor("#4B5563")
GRAY_800 = HexColor("#1F2937")

class Anchor(Flowable):
    def __init__(self, name, label=None):
        Flowable.__init__(self)
        self.name = name
        self.label = label or name
        self.width = 0
        self.height = 0
    def draw(self):
        self.canv.bookmarkPage(self.name)
        # outline level based on prefix
        lvl = 0 if self.name.startswith('h1_') else 1
        try:
            self.canv.addOutlineEntry(self.label, self.name, level=lvl, closed=False)
        except:
            pass
        self.canv.showOutline()

def make_architecture_drawing():
    d = Drawing(500, 220)
    def box(x,y,w,h, fill, stroke, title, items):
        d.add(Rect(x,y,w,h, fillColor=fill, strokeColor=stroke, strokeWidth=1.2, rx=8, ry=8))
        d.add(String(x+10, y+h-18, title, fontName='Helvetica-Bold', fontSize=10, fillColor=NAVY))
        for i, it in enumerate(items):
            d.add(String(x+10, y+h-32 - i*13, f"* {it}", fontName='Helvetica', fontSize=7, fillColor=GRAY_800))
    box(10,20,150,180, EMERALD_PALE, EMERALD, "EDGE", ["ESP32 WROOM-32 (brain)", "ESP32-CAM (eyes) OV2640", "Soil LM393 % AO->34", "DHT11 -> GPIO4", "LDR -> GPIO35", "HC-SR04 18/19", "Relay GPIO5 + UV LED 12"])
    box(185,20,130,180, colors.white, GRAY_200, "CLOUD", ["Firebase RTDB", "/sensors 10 metrics", "/controls 9 keys", "/latest_scan b64", "/weather live", "public read + secret", "1 write + 1 read / sec"])
    box(340,20,150,180, HexColor("#FFFBEB"), GOLD, "EXPERIENCE", ["Single-file HTML", "Dashboard 8 tiles", "Weather + 5-day", "Plant Doctor CAM <2s", "Gemini + OpenRouter", "Tank calibration SET", "Demo mode + toasts"])
    def arrow(x1,y1,x2,y2, color=GRAY_400):
        d.add(Line(x1,y1,x2,y2, strokeColor=color, strokeWidth=1.2))
        d.add(Polygon([x2-6,y2-3, x2, y2, x2-6,y2+3], fillColor=color, strokeColor=color))
    arrow(160,110,185,110, EMERALD)
    d.add(String(163,124,"HTTPS JSON\n1-sec heartbeat", fontName='Helvetica', fontSize=6, fillColor=GRAY_600, textAnchor='middle'))
    arrow(315,110,340,110, GOLD)
    d.add(String(327,124,"REST / polling", fontName='Helvetica', fontSize=6, fillColor=GRAY_600, textAnchor='middle'))
    return d

def make_firebase_tree():
    d = Drawing(500, 240)
    d.add(Rect(180,200,140,30, fillColor=NAVY, strokeColor=NAVY, rx=6))
    d.add(String(250,218,"verde-tech-haha (RTDB)", fontName='Helvetica-Bold', fontSize=9, fillColor=white, textAnchor='middle'))
    branches = [
        ("sensors/", ["moisture, temp, humidity, light, tank", "lux, watchdog, voltage_sag", "uploads / fails"], 0),
        ("controls/", ["manual_mode, pump_state", "light_manual, grow_light", "capture_photo, thresholds", "weather_override"], 1),
        ("latest_scan/", ["imageUrl b64, status", "scientificName, disease", "probability, treatment"], 2),
        ("weather/", ["city, temp, condition", "humidity, wind, rain"], 3),
        ("historical_logs/", ["moisture_log [{time, moisture}]"], 4),
        ("actuators/", ["pump_actual, grow_light_actual, mode"], 5),
    ]
    cols = [EMERALD, GOLD, HexColor("#6366F1"), HexColor("#EC4899"), HexColor("#06B6D4"), HexColor("#84CC16")]
    for idx, (name, items, _) in enumerate(branches):
        x = 10 + (idx % 3)*170
        y = 140 - (idx // 3)*110
        fill = [EMERALD_PALE, GOLD_LIGHT, HexColor("#EEF2FF"), HexColor("#FDF2F8"), HexColor("#ECFEFF"), HexColor("#F7FEE7")][idx]
        stroke = cols[idx]
        d.add(Rect(x,y,155,75, fillColor=fill, strokeColor=stroke, strokeWidth=1, rx=6))
        d.add(String(x+8, y+58, name, fontName='Helvetica-Bold', fontSize=8, fillColor=NAVY))
        for j, it in enumerate(items[:3]):
            d.add(String(x+8, y+45-j*10, f"- {it}", fontName='Helvetica', fontSize=6, fillColor=GRAY_600))
        d.add(Line(250,200, x+77, y+75, strokeColor=GRAY_200, strokeWidth=0.8))
    return d

def make_auto_flowchart():
    d = Drawing(460, 260)
    def rbox(x,y,w,h, txt, fill=white, stroke=NAVY, bold=False):
        d.add(Rect(x,y,w,h, fillColor=fill, strokeColor=stroke, rx=6, strokeWidth=1))
        d.add(String(x+w/2, y+h/2-3, txt, fontName='Helvetica-Bold' if bold else 'Helvetica', fontSize=7.5, fillColor=NAVY, textAnchor='middle'))
    def diamond(x,y,w,h, txt):
        cx = x+w/2; cy = y+h/2
        points = [cx, y+h, x+w, cy, cx, y, x, cy]
        d.add(Polygon(points, fillColor=GOLD_LIGHT, strokeColor=GOLD, strokeWidth=1))
        lines = txt.split('\n')
        for i, l in enumerate(lines):
            d.add(String(cx, cy+6 - i*9, l, fontName='Helvetica-Bold', fontSize=7, fillColor=NAVY, textAnchor='middle'))
    rbox(160,220,140,28, "Start: 1-sec Loop", EMERALD_PALE, EMERALD, True)
    rbox(160,180,140,28, "Read: moisture % (10-pt avg)")
    diamond(160,135,140,35, "moisture <\nthreshold (35%)?")
    rbox(20,100,100,28, "Pump OFF", GRAY_100, GRAY_400)
    diamond(160,85,140,35, "tank safe?\nlevel >15%?")
    rbox(20,30,100,28, "Tank Lock OFF", HexColor("#FEF2F2"), HexColor("#FCA5A5"))
    diamond(160,20,140,35, "rain expected?\nweather_override?")
    rbox(300,20,120,28, "Pump ON - Continuous", EMERALD, EMERALD, True)
    d.add(String(360, 30, "Runs till threshold", fontName='Helvetica', fontSize=6, fillColor=white, textAnchor='middle'))
    rbox(300,100,120,28, "Pump OFF + Wait", GRAY_100, GRAY_400)
    def conn(x1,y1,x2,y2):
        d.add(Line(x1,y1,x2,y2, strokeColor=NAVY, strokeWidth=0.8))
    conn(230,220,230,208); conn(230,180,230,170); conn(160,152,120,152); conn(120,152,120,128)
    conn(70,100,230,100); conn(230,100,230,120); conn(230,85,230,70); conn(160,102,120,102)
    conn(120,102,120,58); conn(160,37,120,37); conn(120,37,120,30); conn(230,20,300,33); conn(300,85,300,33)
    d.add(String(305,155,"No", fontName='Helvetica-Bold', fontSize=7, fillColor=GOLD_DARK))
    d.add(String(250,138,"Yes", fontName='Helvetica-Bold', fontSize=7, fillColor=EMERALD_DARK))
    d.add(String(305,105,"No", fontName='Helvetica-Bold', fontSize=7, fillColor=GOLD_DARK))
    d.add(String(250,88,"Yes", fontName='Helvetica-Bold', fontSize=7, fillColor=EMERALD_DARK))
    d.add(String(305,40,"Yes -> OFF", fontName='Helvetica-Bold', fontSize=7, fillColor=GOLD_DARK))
    d.add(String(250,40,"No", fontName='Helvetica-Bold', fontSize=7, fillColor=EMERALD_DARK))
    return d

def make_bug_infographic():
    d = Drawing(500, 170)
    d.add(Rect(10,10,220,150, fillColor=HexColor("#FEF2F2"), strokeColor=HexColor("#FECACA"), rx=10, strokeWidth=1))
    d.add(String(20,145,"BEFORE - The Loop Bug", fontName='Helvetica-Bold', fontSize=10, fillColor=HexColor("#DC2626")))
    bullet_before = ["17 Firebase HTTPS calls / sec","Network stalls -> 8s WDT reboot","Pump clicks ON/OFF every ~10s","Voltage sag, logs spurt, jitter"]
    for i, b in enumerate(bullet_before):
        d.add(Circle(25, 125 - i*14, 3, fillColor=HexColor("#DC2626"), strokeColor=HexColor("#DC2626")))
        d.add(String(32, 123 - i*14, b, fontName='Helvetica', fontSize=7, fillColor=GRAY_800))
    d.add(String(20,25,"Result: Plant drowns/dries, demo fails", fontName='Helvetica-Oblique', fontSize=7, fillColor=HexColor("#991B1B")))
    d.add(Rect(240,65,40,40, fillColor=GOLD_LIGHT, strokeColor=GOLD, rx=20))
    d.add(String(260,84,"FIX", fontName='Helvetica-Bold', fontSize=10, fillColor=GOLD_DARK, textAnchor='middle'))
    d.add(Line(230,85,240,85, strokeColor=GOLD, strokeWidth=1.2))
    d.add(Line(280,85,290,85, strokeColor=GOLD, strokeWidth=1.2))
    d.add(Polygon([290,82, 298,85, 290,88], fillColor=GOLD, strokeColor=GOLD))
    d.add(Rect(300,10,190,150, fillColor=EMERALD_PALE, strokeColor=EMERALD, rx=10, strokeWidth=1.2))
    d.add(String(310,145,"AFTER - JSON Bundling", fontName='Helvetica-Bold', fontSize=10, fillColor=EMERALD_DARK))
    bullet_after = ["1 write -> /sensors (10 metrics)","1 read -> /controls (9 keys)","~85% latency cut, zero reboots","Pump ON continuous to threshold","Watchdog happy 10+ min"]
    for i, b in enumerate(bullet_after):
        d.add(Circle(315, 125 - i*14, 3, fillColor=EMERALD, strokeColor=EMERALD))
        d.add(String(322, 123 - i*14, b, fontName='Helvetica', fontSize=7, fillColor=GRAY_800))
    d.add(String(310,25,"2 calls/sec - Clean logs - Stable", fontName='Helvetica-Bold', fontSize=7, fillColor=EMERALD_DARK))
    return d

def make_circuit_diagram():
    d = Drawing(500, 220)
    d.add(Rect(200,40,100,140, fillColor=NAVY, strokeColor=NAVY, rx=8))
    d.add(String(250,155,"ESP32\nWROOM-32\nBRAIN", fontName='Helvetica-Bold', fontSize=8, fillColor=white, textAnchor='middle', leading=10))
    pins_left = [("GPIO23 -> VCC Soil", 170), ("GPIO34 <- AO Soil", 150), ("GPIO4 <- DHT11", 130), ("GPIO35 <- LDR AO", 110), ("GPIO18 -> TRIG", 90), ("GPIO19 <- ECHO", 70)]
    pins_right = [("GPIO5 -> Relay IN1 (LOW)", 170), ("GPIO12 -> UV LED (HIGH)", 130), ("5V / 2A Adapter + 1000uF", 90), ("GND Shared Bus", 50)]
    for label, y in pins_left:
        d.add(Line(100,y,200,y, strokeColor=GRAY_400, strokeWidth=0.8))
        d.add(Circle(100,y,4, fillColor=EMERALD_LIGHT, strokeColor=EMERALD))
        d.add(String(5,y-3, label, fontName='Helvetica', fontSize=6, fillColor=GRAY_800))
    for label, y in pins_right:
        d.add(Line(300,y,400,y, strokeColor=GRAY_400, strokeWidth=0.8))
        d.add(Circle(400,y,4, fillColor=GOLD_LIGHT, strokeColor=GOLD))
        d.add(String(410,y-3, label, fontName='Helvetica', fontSize=6, fillColor=GRAY_800))
    d.add(Rect(10,5,180,35, fillColor=GOLD_LIGHT, strokeColor=GOLD, rx=6))
    d.add(String(15,28,"Power Lessons:", fontName='Helvetica-Bold', fontSize=7, fillColor=GOLD_DARK))
    d.add(String(15,18,"* 5V/2A adapter, not PD charger\n* 1000uF cap, 1N4007 diode, relay isolated", fontName='Helvetica', fontSize=6, fillColor=GRAY_800, leading=7))
    d.add(Rect(310,5,180,35, fillColor=HexColor("#EEF2FF"), strokeColor=HexColor("#6366F1"), rx=6))
    d.add(String(315,28,"Safety:", fontName='Helvetica-Bold', fontSize=7, fillColor=HexColor("#4338CA")))
    d.add(String(315,18,"* Watchdog 8s, NVS thresholds\n* Tank lock, rain override, hysteresis +-2%", fontName='Helvetica', fontSize=6, fillColor=GRAY_800, leading=7))
    return d

def build_pdf():
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    styles = getSampleStyleSheet()
    s_title_cover = ParagraphStyle('CoverTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=54, leading=56, textColor=white, alignment=0, spaceAfter=10)
    s_tagline = ParagraphStyle('Tagline', parent=styles['Normal'], fontName='Helvetica', fontSize=14, leading=18, textColor=HexColor("#A7F3D0"), spaceAfter=20)
    s_body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=15, textColor=GRAY_800, spaceAfter=8, alignment=4)
    s_body_small = ParagraphStyle('BodySmall', parent=s_body, fontSize=9, leading=13)
    s_h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=26, leading=30, textColor=NAVY, spaceBefore=6, spaceAfter=10)
    s_h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=EMERALD_DARK, spaceBefore=12, spaceAfter=6)
    s_h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=11, leading=13, textColor=NAVY, spaceBefore=8, spaceAfter=4)
    s_kicker = ParagraphStyle('Kicker', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=GOLD_DARK, spaceAfter=4)
    s_quote = ParagraphStyle('Quote', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=11, leading=15, textColor=NAVY_LIGHT, leftIndent=12, borderPadding=(0,0,0,12), spaceAfter=10, backColor=HexColor("#F0FDF4"), borderColor=EMERALD)
    s_caption = ParagraphStyle('Caption', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=GRAY_400, alignment=1, spaceBefore=4)
    s_cover_meta = ParagraphStyle('CoverMeta', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=HexColor("#CBD5E1"))
    s_white_small = ParagraphStyle('WhiteSmall', parent=s_body_small, textColor=HexColor("#E5E7EB"))
    s_toc = ParagraphStyle('Toc', parent=s_body, fontSize=10, leading=12, leftIndent=0)

    def make_kpi_card(title, value, sub, accent=EMERALD):
        inner = [
            [Paragraph(f"<font color='{accent.hexval()}'><b>{title}</b></font>", s_kicker)],
            [Paragraph(f"<b><font size=16 color='#0B1D3A'>{value}</font></b>", ParagraphStyle('val', parent=s_body, fontSize=16, leading=18))],
            [Paragraph(f"<font size=8 color='#6B7280'>{sub}</font>", s_body_small)],
        ]
        t = Table(inner, colWidths=[108])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.8, GRAY_200),
            ('ROUNDEDCORNERS', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        return t

    class VerdeDocTemplate(BaseDocTemplate):
        def __init__(self, filename, **kwargs):
            BaseDocTemplate.__init__(self, filename, **kwargs)
            frame_cover = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='cover')
            frame_content = Frame(36, 48, 523, 720, id='content')
            self.addPageTemplates([
                PageTemplate(id='cover', frames=frame_cover, onPage=cover_page),
                PageTemplate(id='content', frames=frame_content, onPage=content_page),
            ])

    def cover_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0,0,A4[0],A4[1], fill=1, stroke=0)
        # Emerald blobs with gradient simulation
        canvas.setFillColor(EMERALD_DARK)
        canvas.circle(A4[0]-80, 120, 260, fill=1, stroke=0)
        canvas.setFillColor(HexColor("#0E8A5F"))
        canvas.circle(A4[0]-150, 100, 180, fill=1, stroke=0)
        canvas.setFillColor(EMERALD)
        canvas.circle(A4[0]-100, 180, 110, fill=1, stroke=0)
        # Gold lines
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(0.6)
        for i in range(5):
            y = 320 + i*90
            canvas.line(0, y, A4[0], y+40)
        # Plant icon stylized - stem + leaves on cover
        # stem
        canvas.setStrokeColor(white)
        canvas.setLineWidth(2.5)
        canvas.setFillColor(EMERALD_LIGHT)
        # draw leaves as polygons
        # central stem
        canvas.line(460, 80, 460, 280)
        # left leaf
        canvas.setFillColor(HexColor("#34D399"))
        p = canvas.beginPath()
        p.moveTo(460, 220)
        p.curveTo(400, 250, 390, 200, 460, 180)
        p.close()
        canvas.drawPath(p, fill=1, stroke=0)
        # right leaf
        p = canvas.beginPath()
        p.moveTo(460, 200)
        p.curveTo(520, 230, 530, 180, 460, 160)
        p.close()
        canvas.drawPath(p, fill=1, stroke=0)
        # top leaf
        p = canvas.beginPath()
        p.moveTo(460, 280)
        p.curveTo(430, 330, 490, 330, 460, 280)
        p.close()
        canvas.drawPath(p, fill=1, stroke=0)
        # dots grid
        canvas.setFillColor(HexColor("#12305E"))
        for x in range(0, int(A4[0]), 28):
            for y in range(0, int(A4[1]), 28):
                canvas.circle(x, y, 0.6, fill=1, stroke=0)
        canvas.setFillColor(GOLD)
        canvas.rect(0, A4[1]-8, A4[0], 8, fill=1, stroke=0)
        canvas.rect(0,0,A4[0],4, fill=1, stroke=0)
        # small icons row at top: sensor icons?
        canvas.setFont("Helvetica-Bold", 7)
        canvas.setFillColor(EMERALD_LIGHT)
        canvas.drawString(36, A4[1]-24, "ESP32  |  5 SENSORS  |  2 ACTUATORS  |  FIREBASE  |  4 AI APIS  |  Rs. 1,890")
        canvas.restoreState()

    def content_page(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(2.5)
        canvas.line(36, A4[1]-28, A4[0]-36, A4[1]-28)
        canvas.setStrokeColor(GRAY_200)
        canvas.setLineWidth(0.6)
        canvas.line(36, 32, A4[0]-36, 32)
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(GRAY_400)
        canvas.drawString(36, 18, "PROJECT VERDE - DAV ACON 5 - 2026 - Aarav & Anuj - Class X")
        canvas.drawRightString(A4[0]-36, 18, f"{doc.page}")
        canvas.setFillColor(EMERALD)
        canvas.circle(24, A4[1]/2, 3, fill=1, stroke=0)
        canvas.restoreState()

    OUTPUT_PDF = "Project_Verde_Definitive_Documentation.pdf"
    story = []
    story.append(NextPageTemplate('cover'))
    story.append(Spacer(1, 60))
    story.append(Paragraph("PROJECT", ParagraphStyle('coverkicker', parent=s_kicker, textColor=GOLD, fontSize=11, leading=13)))
    story.append(Paragraph("VERDE", s_title_cover))
    story.append(Spacer(1, 4))
    story.append(Paragraph("The plant that waters itself -<br/>and talks to AI.", s_tagline))
    story.append(Spacer(1, 16))
    badge_data = [[Paragraph("<b>COMPLETE & DEMO-READY</b><br/><font size=8>Hardware - Firmware - Cloud - Web App - AI</font>", ParagraphStyle('badge', parent=s_body_small, textColor=white, fontName='Helvetica-Bold', leading=10))]]
    badge_table = Table(badge_data, colWidths=[220])
    badge_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), EMERALD_DARK), ('ROUNDEDCORNERS', (0,0), (-1,-1), 8), ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12), ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10)]))
    story.append(badge_table)
    story.append(Spacer(1, 22))
    story.append(Paragraph("Aarav Choudhary (Class X) & Anuj (Class X)<br/>DAV ACON 5 - Tech Exhibition, 2026", s_cover_meta))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Total Build Cost  ~ Rs. 1,890 (~ $23) - All software on free tiers - 5 Sensors - 2 Actuators - 2 MCUs - 4 AI APIs", ParagraphStyle('covercost', parent=s_white_small, fontSize=8, leading=11, textColor=HexColor("#A7F3D0"))))
    story.append(Spacer(1, 90))
    strip_data = [[Paragraph("<b>EDGE</b><br/>ESP32 WROOM-32 + ESP32-CAM", s_white_small), Paragraph("<b>CLOUD</b><br/>Firebase RTDB - source of truth", s_white_small), Paragraph("<b>EXPERIENCE</b><br/>Single-file Web App + AI Doctor", s_white_small)]]
    strip = Table(strip_data, colWidths=[160,160,160])
    strip.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), HexColor("#11294F")), ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10), ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8), ('ROUNDEDCORNERS', (0,0), (-1,-1), 6)]))
    story.append(strip)
    story.append(PageBreak())
    story.append(NextPageTemplate('content'))

    # 60 seconds
    story.append(Anchor("h1_60sec", "The Whole Story in 60 Seconds"))
    story.append(Paragraph("<font color='#D97706'>TL;DR</font> - THE WHOLE STORY", s_kicker))
    story.append(Paragraph("The Whole Story in 60 Seconds", s_h1))
    story.append(Paragraph("If you read only one page, read this. Urban families kill plants not from neglect, but from <b>lack of information</b>. Verde fixes that with a Rs. 1,890 brain that watches soil, weather, and water - and acts.", s_body))
    story.append(Spacer(1,8))
    kpi_cards = [make_kpi_card("BUILD COST", "Rs. 1,890", "vs Rs. 8,000+ kits", EMERALD), make_kpi_card("API CALLS", "17 -> 2 / sec", "-85% latency, 0 reboots", GOLD_DARK), make_kpi_card("DIAGNOSIS", "94%", "Plant.id test", EMERALD_DARK), make_kpi_card("HEARTBEAT", "1 sec", "JSON 10 metrics", NAVY)]
    kpi_table = Table([kpi_cards], colWidths=[118]*4, spaceBefore=4, spaceAfter=8)
    kpi_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'), ('LEFTPADDING',(0,0),(-1,-1),3), ('RIGHTPADDING',(0,0),(-1,-1),3)]))
    story.append(kpi_table)
    story.append(Paragraph("Three tiers, one heartbeat:", s_h3))
    bullets_60 = [
        "<b>EDGE (Hands & Eyes):</b> ESP32 WROOM-32 reads 5 sensors every second. Soil power-gated 15 ms to prevent corrosion. ESP32-CAM polls trigger every 1.5 s, SVGA JPEG, raw bytes to Vercel. Sequential boot + 8 MHz XCLK solved brownout + RF.",
        "<b>CLOUD (Memory):</b> Firebase RTDB holds /sensors, /controls, /latest_scan (base64), /weather, /historical_logs, /actuators. One write + one read per second. Not 17. That was the bug.",
        "<b>EXPERIENCE (Face):</b> Single-file HTML. Four pages via burger. Live tiles + sparklines, sliders, tank calibration SET EMPTY/FULL, 5-day forecast rain override, Plant Doctor <=2 s, Gemini + OpenRouter chats.",
        "<b>INTELLIGENCE:</b> OWM rain ids 2xx/3xx/5xx/6xx -> weather_override=1. crop.health gives disease + probability + treatment. Gemini 2.5 Flash via gemini-flash-latest. OpenRouter 8+5 fallback chains never dead-end.",
    ]
    for b in bullets_60:
        story.append(Paragraph(f"- {b}", s_body))
    story.append(Spacer(1,6))
    story.append(Paragraph("\"The plant that waters itself - and talks to AI.\" It is not a slogan. It is what happens when moisture < 35% and tank safe and rain not coming.", s_quote))
    story.append(PageBreak())

    # TOC - hyperlinked
    story.append(Anchor("h1_contents", "Contents"))
    story.append(Paragraph("NAVIGATE", s_kicker))
    story.append(Paragraph("Contents", s_h1))
    toc_items = [
        ("01", "Why - The Problem", "h1_why", "Urban death + Rs. 8k gap"),
        ("02", "How It Works - Architecture", "h1_arch", "EDGE->CLOUD->EXPERIENCE + heartbeat"),
        ("03", "Hardware - 5 Sensors, 2 Actuators", "h1_hardware", "BOM, pin map, power lessons"),
        ("04", "Firmware - Bug Story 17->2", "h1_firmware", "Scheduler, auto logic, fix"),
        ("05", "Cloud - Firebase Schema", "h1_cloud", "Single source of truth"),
        ("06", "Web App - Single File, Four Worlds", "h1_webapp", "Dashboard, Weather, Doctor, AI"),
        ("07", "AI & APIs - 4 Integrations", "h1_ai", "OWM, Plant.id, Gemini, OpenRouter"),
        ("08", "Features - Everything Live", "h1_features", "8 tiles, sparklines, calibration"),
        ("09", "Testing - 13-Point PASS", "h1_testing", "DHT breathe to watchdog"),
        ("10", "Bugs We Hit & Fixed", "h1_bugs", "10 war stories"),
        ("11", "Cost & Sustainability", "h1_cost", "Rs. 1,890 breakdown"),
        ("12", "Future - Solar, NPK, Zones", "h1_future", "Roadmap"),
        ("13", "Judge Tour - 3-Min Demo", "h1_tour", "How to wow in 180 sec"),
        ("14", "Conclusion - Why We Win", "h1_conclusion", "QR to live demo"),
    ]
    toc_data = []
    for num, title, anchor, desc in toc_items:
        link_title = f"<a href=\"#{anchor}\" color=\"#0B1D3A\"><b>{title}</b></a><br/><font size=7 color='#6B7280'>{desc}</font>"
        toc_data.append([
            Paragraph(f"<b><font color='#10B981'>{num}</font></b>", ParagraphStyle('num', parent=s_body, fontSize=10, leading=11)),
            Paragraph(link_title, s_toc),
            Paragraph("<font color='#9CA3AF'>-></font>", s_body_small)
        ])
    toc_table = Table(toc_data, colWidths=[34, 430, 18])
    toc_table.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LINEBELOW',(0,0),(-1,-2),0.4, GRAY_100),
        ('LEFTPADDING',(0,0),(-1,-1),4),
        ('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(toc_table)
    story.append(Spacer(1,8))
    story.append(Paragraph("How to use this doc: Judges -> 3-min flip. Parents/teachers -> any page standalone. Engineers -> pin maps + schema. Click TOC to jump (PDF bookmarks).", ParagraphStyle('use', parent=s_body_small, textColor=GRAY_600, borderPadding=(6,6,6,6), backColor=GRAY_50)))
    story.append(PageBreak())

    # Why
    story.append(Anchor("h1_why", "Why"))
    story.append(Paragraph("PART 01 - WHY", s_kicker))
    story.append(Paragraph("The Problem Worth Solving", s_h1))
    story.append(Paragraph("Urban families love plants. Plants die anyway. Why? Not cruelty - <b>lack of real-time data</b>.", s_body))
    story.append(Spacer(1,6))
    left = [Paragraph("<b>What we saw</b>", s_h3), Paragraph("- Mom waters daily by habit -> root rot.<br/>- Dad forgets for a week -> wilt.<br/>- Tank empties mid-pump -> motor burns.<br/>- Rain comes, pump still waters -> waste.<br/>- No camera, so disease spotted 10 days late.", s_body)]
    right = [Paragraph("<b>What exists</b>", s_h3), Paragraph("- Smart kits Rs. 8,000+ (Gardena, Xiaomi)<br/>- No camera, no AI diagnosis<br/>- Closed-source, not student-hackable<br/>- Subscriptions for cloud<br/>- No tank level, no rain override", s_body)]
    prob_table = Table([[left[0], right[0]],[left[1], right[1]]], colWidths=[260,260], spaceBefore=6, spaceAfter=10)
    prob_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'), ('LEFTPADDING',(0,0),(-1,-1),8), ('RIGHTPADDING',(0,0),(-1,-1),8), ('BACKGROUND',(0,1),(0,1), EMERALD_PALE), ('BACKGROUND',(1,1),(1,1), GRAY_50), ('BOX',(0,0),(-1,-1),0.6, GRAY_200), ('ROUNDEDCORNERS',(0,0),(-1,-1),8)]))
    story.append(prob_table)
    story.append(Paragraph("Pull quote:", s_h3))
    story.append(Paragraph("\"A Rs. 1,890 plant that texts its mood is more useful than a Rs. 12,000 kit that just waters on a timer.\"", s_quote))
    story.append(Paragraph("Our insight: The plant must <b>tell us</b> what it needs, and <b>act</b> when we are not looking. Moisture < 35% AND tank safe AND no rain -> pump ON. No human needed. But human can always override.", s_body))
    story.append(Spacer(1,8))
    hero = Table([[Paragraph("<font size=20 color='#0B1D3A'><b>70%</b></font><br/><font size=8>urban plants die in 3 months</font>", s_body_small), Paragraph("<font size=20 color='#059669'><b>Rs. 1,890</b></font><br/><font size=8>our total vs Rs. 8k+ market</font>", s_body_small), Paragraph("<font size=20 color='#D97706'><b>94%</b></font><br/><font size=8>AI disease ID accuracy</font>", s_body_small)]], colWidths=[170,170,170])
    hero.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'), ('BOX',(0,0),(-1,-1),0.6,GRAY_200), ('BACKGROUND',(0,0),(-1,-1), colors.white)]))
    story.append(hero)
    story.append(PageBreak())

    # Architecture
    story.append(Anchor("h1_arch", "Architecture"))
    story.append(Paragraph("PART 02 - ARCHITECTURE", s_kicker))
    story.append(Paragraph("How It Works", s_h1))
    story.append(Paragraph("Three tiers. One heartbeat every second. No magic, just disciplined engineering.", s_body))
    story.append(Spacer(1,6))
    story.append(make_architecture_drawing())
    story.append(Paragraph("System architecture - EDGE (brain + eyes + 5 sensors), CLOUD (single source), EXPERIENCE (single-file web app + 4 AI APIs).", s_caption))
    story.append(Spacer(1,8))
    story.append(Paragraph("One-Second Heartbeat Timeline", s_h2))
    story.append(Image(str(ASSETS_DIR / "heartbeat.png"), width=480, height=160))
    story.append(Paragraph("Every 1000 ms: read sensors -> 10-pt moving avg (soil/LDR) + 5-pt + invalid rejection (tank) -> bundle 10-metric JSON -> one write /sensors -> one read /controls (9 keys) -> decision -> actuator update. Watchdog fed every loop.", s_body_small))
    story.append(Spacer(1,8))
    ed = [[Paragraph("<b>Why 1 sec?</b>", s_h3), Paragraph("<b>Why bundled?</b>", s_h3)],[Paragraph("Fast enough to catch splash noise in tank sensor. Slow enough for Firebase free-tier. Feels live. Matches dashboard sparkline rate.", s_body_small), Paragraph("17 calls/sec -> stall -> 8s watchdog reboot -> pump flicker loop. 1+1 calls/sec -> -85% latency, zero reboots, continuous pumping until threshold.", s_body_small)]]
    ed_table = Table(ed, colWidths=[250,250], spaceBefore=4)
    ed_table.setStyle(TableStyle([('BACKGROUND',(0,0),(0,1), EMERALD_PALE), ('BACKGROUND',(1,0),(1,1), GOLD_LIGHT), ('BOX',(0,0),(-1,-1),0.6,GRAY_200), ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]))
    story.append(ed_table)
    story.append(PageBreak())

    # Hardware
    story.append(Anchor("h1_hardware", "Hardware"))
    story.append(Paragraph("PART 03 - HARDWARE", s_kicker))
    story.append(Paragraph("5 Sensors, 2 Actuators, 2 Brains", s_h1))
    story.append(Paragraph("Everything bought from local Lajpat Nagar + Amazon. Total Rs. 1,890. No PCB - breadboard, so judges can see every wire.", s_body))
    story.append(Spacer(1,6))
    bom_data = [["Module","ESP32 Pin","Role & Trick"],["Soil moisture LM393","AO->GPIO34, VCC->GPIO23","15 ms power-gated reads -> no corrosion. 10-pt avg."],["DHT11 Temp+Humidity","DATA->GPIO4","Breathe test: blow -> temp/hum spike. Shared GND critical."],["LDR Module","AO->GPIO35","Dark detection. Hysteresis +-2% -> no LED flicker."],["HC-SR04 Ultrasonic","TRIG->18, ECHO->19","Tank level 5-pt filter + invalid rejection. Splash-proof."],["2-ch Relay (active-LOW)","IN1->GPIO5","Switches 5V pump. Isolated COM/NO on own 5V."],["UV Grow LED","GPIO12 HIGH, 220ohm","Photosynthetic light. Auto on when LDR < threshold."],["ESP32-CAM OV2640","Own board + MB","SVGA JPEG. 8 MHz XCLK, sequential boot 500 ms delay."],["Power: 5V/2A Adapter","-","NOT PD charger. 1000uF cap across 5V/GND."],["Protection","-","1N4007 flyback diode across pump."]]
    bom_table_data = []
    for i,row in enumerate(bom_data):
        if i==0:
            bom_table_data.append([Paragraph(f"<b>{c}</b>", s_body_small) for c in row])
        else:
            bom_table_data.append([Paragraph(c, s_body_small) for c in row])
    bom_table = Table(bom_table_data, colWidths=[120,110,270], repeatRows=1)
    bom_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), NAVY), ('TEXTCOLOR',(0,0),(-1,0), white), ('ALIGN',(0,0),(-1,0),'CENTER'), ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'), ('FONTSIZE',(0,0),(-1,0),8), ('BACKGROUND',(0,1),(-1,-1), colors.white), ('BOX',(0,0),(-1,-1),0.6, GRAY_200), ('GRID',(0,0),(-1,-1),0.4, GRAY_100), ('ROWBACKGROUNDS',(0,1),(-1,-1), [white, GRAY_50]), ('LEFTPADDING',(0,0),(-1,-1),5), ('RIGHTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(bom_table)
    story.append(Spacer(1,10))
    story.append(Paragraph("Photo placeholders - replace with real bench shots for final judging", s_h3))
    story.append(Image(str(ASSETS_DIR / "hardware_placeholder.png"), width=500, height=300))
    story.append(Paragraph("Hardware bench - ESP32 WROOM-32 (left), relay + pump, rails bridged + to +, - to - (lesson #7).", s_caption))
    story.append(PageBreak())

    story.append(Paragraph("Hardware Continued", s_h2))
    story.append(Paragraph("Circuit / Wiring (Simplified, not EDA)", s_h3))
    story.append(make_circuit_diagram())
    story.append(Paragraph("Wiring map - every GPIO noted. VCC gated via GPIO23 prevents corrosion. Relay active-LOW, UV LED active-HIGH.", s_caption))
    story.append(Spacer(1,10))
    story.append(Paragraph("Power Design - Hard-Won Lessons", s_h2))
    power_lessons = [["Lesson","We tried","What failed","Fix"],["PD Charger","67W USB-PD brick","PD needs handshake chip ESP32 lacks -> ~0 mA","5V/2A phone adapter."],["Cap","No capacitor","Pump + WiFi spike -> brownout reboot","1000uF electrolytic 5V/GND"],["Diode","Pump direct to relay","Inductive kick -> ESP32 reset","1N4007 flyback across pump"],["Isolation","Pump + ESP32 same 5V rail","Noise + sag","Relay COM/NO own 5V source"],["Rail","Split breadboard","Relay dead - no power","Bridge + to +, - to -"],["GND","DHT on separate GND","temp=0 always","Shared GND bus, GPIO4"]]
    pl_data = [[Paragraph(f"<b>{c}</b>" if i==0 else c, s_body_small) for c in row] for i,row in enumerate(power_lessons)]
    pl_table = Table(pl_data, colWidths=[55,105,145,180], repeatRows=1)
    pl_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), HexColor("#FEF3C7")), ('TEXTCOLOR',(0,0),(-1,0), HexColor("#92400E")), ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'), ('GRID',(0,0),(-1,-1),0.4, GRAY_200), ('ROWBACKGROUNDS',(0,1),(-1,-1), [white, GRAY_50]), ('LEFTPADDING',(0,0),(-1,-1),5), ('RIGHTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),4), ('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story.append(pl_table)
    story.append(Spacer(1,6))
    story.append(Paragraph("Key spec check (for audit): thresholds 35% moisture / 15% tank / 35% light. 8 MHz XCLK. Pins 34,23,4,35,18,19,5,12. All verified.", ParagraphStyle('audit', parent=s_body_small, backColor=EMERALD_PALE, borderPadding=(5,5,5,5))))
    story.append(PageBreak())

    # Firmware
    story.append(Anchor("h1_firmware", "Firmware"))
    story.append(Paragraph("PART 04 - FIRMWARE", s_kicker))
    story.append(Paragraph("The Brain - Code_1_Main_Brain.ino V3.0.7-FINAL", s_h1))
    story.append(Paragraph("Non-blocking by design. No delay() anywhere. Everything is millis().", s_body))
    story.append(Spacer(1,4))
    fw_cols = [[Paragraph("Task Scheduler", s_h3), Paragraph("- Sensors -> 1 Hz<br/>- Cloud write/read -> 1 s<br/>- WiFi check -> 10 s<br/>- Historical logs -> 60 s<br/>- Watchdog fed every loop (8 s)<br/>- NVS flash persists thresholds", s_body_small)], [Paragraph("Filtering", s_h3), Paragraph("- Soil & LDR: 10-pt moving avg<br/>- Tank: 5-pt avg + invalid rejection<br/>- +-2% hysteresis on light auto<br/>- Splash can't fake empty tank<br/>- Voltage sag counter in /sensors", s_body_small)]]
    fw_table = Table([[fw_cols[0][0], fw_cols[1][0]],[fw_cols[0][1], fw_cols[1][1]]], colWidths=[260,260], spaceAfter=8)
    fw_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'), ('BOX',(0,0),(-1,-1),0.5,GRAY_200), ('BACKGROUND',(0,0),(0,1), EMERALD_PALE), ('LEFTPADDING',(0,0),(-1,-1),8)]))
    story.append(fw_table)
    story.append(Paragraph("AUTO Logic - The Core Decision", s_h2))
    story.append(make_auto_flowchart())
    story.append(Paragraph("Flowchart: pump_ON = moisture < 35% AND tank > 15% AND rain_expected = false. Manual mode still tank-protected. Fail-safe by default.", s_caption))
    story.append(Spacer(1,8))
    story.append(Paragraph("Adjustable thresholds from app (persisted): moisture_threshold, tank_threshold (0 = disabled), light_threshold. User drags slider -> Firebase -> ESP32 reads next heartbeat.", s_body_small))
    story.append(PageBreak())

    story.append(Paragraph("Firmware Continued", s_h2))
    story.append(Paragraph("The Bug That Taught Us Engineering", s_h1))
    story.append(Paragraph("Honesty = credibility. We almost failed demo because of one architectural mistake.", s_body))
    story.append(Spacer(1,6))
    story.append(make_bug_infographic())
    story.append(Spacer(1,8))
    bug_text = ["<b>Symptoms:</b> AUTO mode clicked pump ON/OFF every ~10 s. Logs showed 17 Firebase HTTPS calls/sec. Network stall. 8-sec watchdog reboot. Pump never stayed ON long enough.","<b>Root cause:</b> We updated each metric with separate HTTPS request. Each TLS handshake ~150 ms. 17 x 150 ms = 2.5 s blocking loop -> watchdog thinks deadlock -> reboot -> loop.","<b>Fix - JSON bundling:</b> One JSON object with 10 metrics -> single PUT to /sensors. Read entire /controls (9 keys) in one GET. 2 calls/sec. -85% latency, zero reboots, pump stays ON continuously 120 s until threshold.","<b>Tested:</b> Pump AUTO 120 s no glitch. OFF exactly at threshold. Watchdog 10+ min 0 reboots. One good idea beats 17 bad ones."]
    for b in bug_text:
        story.append(Paragraph(f"- {b}", s_body))
    story.append(Spacer(1,8))
    story.append(Paragraph("Engineering proverb we learned: \"Don't spam the cloud. Respect the handshake.\"", s_quote))
    story.append(Spacer(1,6))
    story.append(Paragraph("Code_2_ESP32_CAM.ino - V3.0.4-FINAL (The Eyes)", s_h3))
    story.append(Paragraph("- Polls /controls/capture_photo every 1.5 s -> flash LED -> capture SVGA JPEG -> POST raw bytes to Vercel upload API -> lands in /latest_scan base64 -> app shows <=2 s<br/>- 8 MHz XCLK fixes RF interference<br/>- Sequential boot: camera init first, WiFi after 500 ms -> prevents brownout<br/>- esp_camera_fb_return() immediately -> no heap fragmentation", s_body_small))
    story.append(PageBreak())

    # Cloud
    story.append(Anchor("h1_cloud", "Cloud"))
    story.append(Paragraph("PART 05 - CLOUD", s_kicker))
    story.append(Paragraph("Firebase RTDB - Single Source of Truth", s_h1))
    story.append(Paragraph("One database. No backend server. Legacy secret auth. Public read, validated writes. If Firebase has it, app and ESP32 agree. No drift.", s_body))
    story.append(Spacer(1,8))
    story.append(make_firebase_tree())
    story.append(Paragraph("Schema tree: verde-tech-haha RTDB. Six nodes. Sensors = telemetry, Controls = intents, Latest_scan = vision, Weather = live, Logs = history, Actuators = truth.", s_caption))
    story.append(Spacer(1,10))
    schema_explain = [[Paragraph("<b>/sensors</b><br/>10 metrics, 1 Hz", s_body_small), Paragraph("moisture %, temp C, humidity %, light %, tank %, lux, watchdog_status, voltage_sag, successful_uploads, failed_uploads. Filtered, averaged.", s_body_small)],[Paragraph("<b>/controls</b><br/>9 keys, app -> ESP32", s_body_small), Paragraph("manual_mode, pump_state, light_manual_mode, grow_light_state, capture_photo (trigger), moisture_threshold, tank_threshold, light_threshold, weather_override.", s_body_small)],[Paragraph("<b>/latest_scan</b><br/>Vision result", s_body_small), Paragraph("imageUrl base64, status, captured_at, scientificName, diseaseName, probability 0-100, treatmentPlan. Overwritten each capture.", s_body_small)]]
    sch_table = Table(schema_explain, colWidths=[120,370], spaceBefore=6)
    sch_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.6,GRAY_200), ('GRID',(0,0),(-1,-1),0.4,GRAY_100), ('LEFTPADDING',(0,0),(-1,-1),8), ('TOPPADDING',(0,0),(-1,-1),8), ('BACKGROUND',(0,0),(0,-1), GRAY_50)]))
    story.append(sch_table)
    story.append(PageBreak())

    # Web App
    story.append(Anchor("h1_webapp", "Web App"))
    story.append(Paragraph("PART 06 - WEB APP", s_kicker))
    story.append(Paragraph("The Face - Single-File HTML", s_h1))
    story.append(Paragraph("No React. No build step. One HTML file that any judge can open and understand. But feels like a product.", s_body))
    story.append(Spacer(1,6))
    pages = [("Dashboard", "8 live tiles + sparklines + hover graphs (last-10). All 8 controls, 3 sliders, predicted actuator states, moisture history, status strip, toasts, fullscreen demo mode, uptime timer."),("Weather", "Live Delhi weather, 5-day chips, auto rain-override every 3 min with countdown -> weather_override=1 when ids 2xx/3xx/5xx/6xx."),("Plant Doctor", "Live CAM frame auto <=2 s, CAPTURE button, upload-or-CAM modal: photo + crop.health diagnosis + AI chat same image. Image flip fix - CAM mounts upside-down."),("AI Assistants", "Gemini image chat + OpenRouter sensor-aware chat (quick prompts). Tank calibration SET EMPTY / SET FULL - app-side remap, no reflash.")]
    page_cards = []
    for title, desc in pages:
        card = Table([[Paragraph(f"<b><font color='#0B1D3A'>{title}</font></b>", s_h3)], [Paragraph(desc, s_body_small)]], colWidths=[115])
        card.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), EMERALD_PALE), ('BOX',(0,0),(-1,-1),0.6,GRAY_200), ('ROUNDEDCORNERS',(0,0),(-1,-1),6), ('LEFTPADDING',(0,0),(-1,-1),6), ('RIGHTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        page_cards.append(card)
    pages_table = Table([page_cards], colWidths=[125]*4, spaceAfter=10)
    pages_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'), ('LEFTPADDING',(0,0),(-1,-1),3), ('RIGHTPADDING',(0,0),(-1,-1),3)]))
    story.append(pages_table)
    story.append(Paragraph("Dashboard details:", s_h3))
    for b in ["8 tiles: moisture, temp, humidity, light, lux, tank, watchdog, voltage. Each sparkline last 10 readings and trend on hover.","Controls: manual_mode toggle, pump ON/OFF, light manual, grow light ON/OFF, capture photo, 3 threshold sliders.","Predicted actuator states: shows what AUTO would do even in manual, so user trusts logic.","Moisture history chart: /historical_logs plotted. Status strip + toasts + fullscreen demo mode."]:
        story.append(Paragraph(f"- {b}", s_body_small))
    story.append(Spacer(1,8))
    story.append(Image(str(ASSETS_DIR / "moisture_cycle.png"), width=480, height=260))
    story.append(Paragraph("Moisture watering-cycle chart with threshold marker 35%. Pump ON continuous until threshold, then OFF exactly. No flicker.", s_caption))
    story.append(PageBreak())

    # AI & APIs
    story.append(Anchor("h1_ai", "AI APIs"))
    story.append(Paragraph("PART 07 - AI & APIS", s_kicker))
    story.append(Paragraph("Four APIs - Researched, Keyed, Live-Tested", s_h1))
    story.append(Paragraph("No mock data. All live. Tested with Delhi 35C, nutrient deficiency @94%, free-tier rotation.", s_body))
    story.append(Spacer(1,6))
    api_data = [["API","Purpose","Auth","How","Accuracy"],["OpenWeatherMap","live weather + 5-day -> rain override","key in URL","GET /data/2.5/weather?q=Delhi; ids 2xx/3xx/5xx/6xx -> rain -> weather_override=1","Live-tested: Delhi 35C, city id 1273294"],["crop.health (Plant.id)","plant + disease ID","Api-Key header","POST /api/v1/identification base64 image -> crop + disease suggestions","Test image nutrient deficiency @94% + treatment - real"],["Google Gemini 2.5 Flash","vision chat on photo","X-goog-api-key","POST /v1beta/models/gemini-flash-latest:generateContent inline image + diagnosis + telemetry","AQ keys need header; gemini-flash-latest alias works"],["OpenRouter","sensor chat + vision fallback","Bearer sk-or-v1-...","POST /api/v1/chat/completions, 8-model text chain + 5-model vision chain","435 models; free rotate -> fallback never dead-end"]]
    api_table_data = []
    for i,row in enumerate(api_data):
        if i==0:
            api_table_data.append([Paragraph(f"<b>{c}</b>", ParagraphStyle('ah', parent=s_body_small, fontName='Helvetica-Bold', textColor=white)) for c in row])
        else:
            api_table_data.append([Paragraph(c, s_body_small) for c in row])
    api_table = Table(api_table_data, colWidths=[65,75,55,135,120], repeatRows=1)
    api_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), NAVY), ('GRID',(0,0),(-1,-1),0.4, GRAY_200), ('ROWBACKGROUNDS',(0,1),(-1,-1), [white, HexColor("#F8FAFC")]), ('LEFTPADDING',(0,0),(-1,-1),4), ('RIGHTPADDING',(0,0),(-1,-1),4), ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(api_table)
    story.append(Spacer(1,10))
    story.append(Paragraph("Accuracy notes & fallback chains:", s_h3))
    for b in ["OWM: rain detection tested forcing condition codes 500, 501. App auto sets weather_override=1, pumps lock, countdown 3 min.","Plant.id: real money-plant identified nutrient deficiency 94% with treatment: add NPK, adjust pH. Returns scientificName.","Gemini: AQ keys (AIzaSy...) require X-goog-api-key header, not Bearer. gemini-flash-latest alias works for new users. Send telemetry + diagnosis + image.","OpenRouter: 8-model text chain (llama, mistral, gemma) + 5-model vision fallback. If 429, next model auto-tried. User never sees dead-end."]:
        story.append(Paragraph(f"- {b}", s_body_small))
    story.append(Spacer(1,8))
    story.append(Image(str(ASSETS_DIR / "plant_doctor_placeholder.png"), width=500, height=300))
    story.append(Paragraph("Plant Doctor placeholder - CAM frame auto-updates <=2 s after capture.", s_caption))
    story.append(PageBreak())

    # Features
    story.append(Anchor("h1_features", "Features"))
    story.append(Paragraph("PART 08 - FEATURES", s_kicker))
    story.append(Paragraph("Everything Live - No Screenshots, Real Data", s_h1))
    story.append(Spacer(1,6))
    feat_grid = [["Feature","Live?","How to demo"],["Live soil % + 10-pt avg + sparkline","YES","Dunk sensor -> % rises, graph"],["Temp/Humidity DHT11","YES","Breathe -> temp/hum spike"],["LDR + UV grow LED auto","YES","Cover LDR -> dark -> LED ON (+-2%)"],["Ultrasonic tank level %","YES","Hand over tank -> level changes"],["Pump AUTO 120s continuous","YES","Set threshold 80% -> ON till 80, no flicker"],["Pump OFF at threshold exact","YES","Watch OFF at 35%, not early"],["Tank lock protection","YES","Set tank empty -> pump refuses ON"],["Rain override","YES","Force rainy city -> override=1 -> OFF"],["CAM capture <=2s","YES","Press CAPTURE -> flash -> app <=2 s"],["Plant Doctor 94% diagnosis","YES","Upload diseased leaf -> name + treatment"],["Gemini vision chat","YES","Ask 'why yellow?' -> sees image + sensors"],["OpenRouter sensor chat","YES","Ask 'should I water?' -> reads moisture"],["Watchdog 10+ min 0 reboots","YES","Leave running, uptime counts"],["Threshold sliders NVS","YES","Drag threshold -> persists reboot"]]
    feat_data = []
    for i,row in enumerate(feat_grid):
        if i==0:
            feat_data.append([Paragraph(f"<b>{c}</b>", ParagraphStyle('fh', parent=s_body_small, fontName='Helvetica-Bold', textColor=white)) for c in row])
        else:
            feat_data.append([Paragraph(row[0], s_body_small), Paragraph(row[1], s_body_small), Paragraph(row[2], s_body_small)])
    feat_table = Table(feat_data, colWidths=[170,45,270], repeatRows=1)
    feat_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), EMERALD_DARK), ('GRID',(0,0),(-1,-1),0.4, GRAY_200), ('ROWBACKGROUNDS',(0,1),(-1,-1), [white, GRAY_50]), ('LEFTPADDING',(0,0),(-1,-1),5), ('RIGHTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),4), ('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story.append(feat_table)
    story.append(Spacer(1,10))
    story.append(Paragraph("Tank calibration - our favorite UX hack:", s_h3))
    story.append(Paragraph("Ultrasonic raw values drift per bucket. Instead of reflashing ESP32, SET EMPTY / SET FULL in app. App stores raw_empty, raw_full in localStorage, remaps to 0-100%. Works for any bucket, no code change.", s_body_small))
    story.append(Spacer(1,6))
    story.append(Paragraph("Demo mode + toasts: Fullscreen demo hides clutter, enlarges tiles for projector. Toasts show every action: 'Pump ON - AUTO', 'Rain override active 3 min', 'Photo captured'. Judges always know what's happening.", s_body_small))
    story.append(PageBreak())

    # Testing
    story.append(Anchor("h1_testing", "Testing"))
    story.append(Paragraph("PART 09 - TESTING", s_kicker))
    story.append(Paragraph("13-Point Test Matrix - All PASS", s_h1))
    story.append(Paragraph("We didn't test once at the end. We tested after every fix. Final run signed.", s_body))
    story.append(Spacer(1,6))
    test_data = [["#","Test","Method","Expected","Result"],["1","WiFi/boot","Power 5V/2A, check serial","Boots <=3s, 3-network fallback","PASS"],["2","DHT11 breathe","Blow warm air","Temp +2-3C, hum +5%","PASS"],["3","Moisture dunk","Dunk LM393 in water","0%->~85% in 3s, avg smooth","PASS"],["4","LDR cover","Cover with hand","Light % drops -> dark -> UV ON","PASS"],["5","Ultrasonic hand","Hand over HC-SR04","Tank % jumps, 5-pt rejects splash","PASS"],["6","Pump AUTO 120s","Set threshold 80%, moist 30%","Pump ON 120s, no flicker","PASS"],["7","OFF at threshold","Watch cross 35%","OFF at 35.0+-0.5","PASS"],["8","Tank lock","Set tank 5% empty, manual ON","Pump refuses, toast 'Tank empty'","PASS"],["9","Rain override","Set OWM rainy id 500","override=1, pump OFF, countdown","PASS"],["10","CAM capture <=2s","Press CAPTURE","Flash -> Vercel -> app <=2.0s","PASS 1.6s avg"],["11","Plant Doctor 94%","Upload diseased leaf","Scientific name + 94% + treatment","PASS"],["12","AI chats + fallbacks","429 one model, next","Gemini + OpenRouter fallback works","PASS"],["13","Watchdog 10+ min","Leave 12 min","0 reboots, uptime inc, sag 0","PASS"]]
    test_table_data = []
    for i,row in enumerate(test_data):
        if i==0:
            test_table_data.append([Paragraph(f"<b>{c}</b>", ParagraphStyle('th', parent=s_body_small, fontName='Helvetica-Bold', textColor=white)) for c in row])
        else:
            test_table_data.append([Paragraph(c, s_body_small) for c in row])
    test_table = Table(test_table_data, colWidths=[18,65,95,135,80], repeatRows=1)
    test_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), NAVY), ('GRID',(0,0),(-1,-1),0.4, GRAY_200), ('ROWBACKGROUNDS',(0,1),(-1,-1), [white, GRAY_50]), ('LEFTPADDING',(0,0),(-1,-1),4), ('RIGHTPADDING',(0,0),(-1,-1),4), ('TOPPADDING',(0,0),(-1,-1),4), ('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story.append(test_table)
    story.append(Spacer(1,10))
    story.append(Paragraph("Engineering log snapshot (real notes):", s_h3))
    story.append(Paragraph("[12:43] WiFi connected HomeNet 72% RSSI<br/>[12:44] Soil 28% -> pump AUTO ON (tank 67% safe, no rain)<br/>[12:46] Soil 35.1% -> pump OFF exact<br/>[12:47] Capture trigger 1 -> CAM flash -> upload 1.4s<br/>[12:50] Uptime 634s, WDT 0 reboots, sag 0", ParagraphStyle('log', parent=s_body_small, backColor=HexColor("#0B1D3A"), textColor=HexColor("#A7F3D0"), fontName='Courier', borderPadding=(6,6,6,6))))
    story.append(PageBreak())

    # Bugs
    story.append(Anchor("h1_bugs", "Bugs"))
    story.append(Paragraph("PART 10 - WAR STORIES", s_kicker))
    story.append(Paragraph("Bugs We Hit & Fixed", s_h1))
    story.append(Paragraph("A project without bugs is a project that didn't run. Our honesty ledger - 10 real failures.", s_body))
    story.append(Spacer(1,6))
    bugs = [("AUTO 10s pump loop","17 calls/sec -> stall -> WDT reboot -> loop","JSON bundling 1+1 calls/sec, -85% latency"),("Camera probe 0x106","OV2640 not found","FPC ribbon unseated -> reseat gold-side down + power cycle"),("PSRAM not found","CAM says no PSRAM","Weak power -> 5V/2A adapter, not PD"),("0x20002 boot crash","ESP32-CAM crash dump","Camera+WiFi surge -> sequential boot 500 ms"),("RF interference","CAM image corrupted when WiFi TX","20 MHz XCLK too fast -> throttle to 8 MHz"),("67W PD charger starved","Board lights dim, WiFi fails","PD handshake missing -> 5V/2A phone adapter"),("Relay dead","Relay never clicks","Split breadboard rails -> bridge + to +, - to -"),("temp=0 always","DHT returns 0","Wrong pin + separate GND -> GPIO4 + shared GND bus"),("Firebase spurts","Logs appear in bursts","13 calls/sec -> one bundled call"),("Compile quote error","missing terminating quote","Copy-paste corruption -> re-download file fresh")]
    bug_data = [[Paragraph("<b>Bug</b>", ParagraphStyle('bh', parent=s_body_small, fontName='Helvetica-Bold', textColor=white)), Paragraph("<b>Symptom</b>", ParagraphStyle('bh2', parent=s_body_small, fontName='Helvetica-Bold', textColor=white)), Paragraph("<b>Fix</b>", ParagraphStyle('bh3', parent=s_body_small, fontName='Helvetica-Bold', textColor=white))]]
    for title, symptom, fix in bugs:
        bug_data.append([Paragraph(f"<b>{title}</b>", s_body_small), Paragraph(symptom, s_body_small), Paragraph(fix, s_body_small)])
    bug_table = Table(bug_data, colWidths=[100,160,220], repeatRows=1)
    bug_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), HexColor("#7C3AED")), ('GRID',(0,0),(-1,-1),0.4, GRAY_200), ('ROWBACKGROUNDS',(0,1),(-1,-1), [white, GRAY_50]), ('LEFTPADDING',(0,0),(-1,-1),5), ('RIGHTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(bug_table)
    story.append(Spacer(1,10))
    story.append(Paragraph("Most valuable bug: #1. It taught system thinking. Costly calls kill UX. Bundling is architecture, not optimization.", s_quote))
    story.append(PageBreak())

    # Cost
    story.append(Anchor("h1_cost", "Cost"))
    story.append(Paragraph("PART 11 - COST & SUSTAINABILITY", s_kicker))
    story.append(Paragraph("Rs. 1,890 - How?", s_h1))
    story.append(Paragraph("We tracked every rupee. No hidden software cost. All APIs free-tier. Not counting laptop + phone you already have.", s_body))
    story.append(Spacer(1,6))
    cost_break = [["Category","Items","Cost INR"],["Electronics","ESP32 Rs.320, ESP32-CAM Rs.480, 5 sensors Rs.300, relay Rs.70, pump Rs.150","1,320"],["Power & protection","5V/2A adapter Rs.150, 1000uF cap Rs.15, 1N4007 Rs.5, wires Rs.50","220"],["Mechanical","Breadboard Rs.120, enclosure Rs.150, UV LED Rs.30, misc Rs.50","350"],["Software & APIs","Firebase free, Vercel hobby, OWM 1000/day free, Plant.id free, Gemini free, OpenRouter free","0"],["","","~ 1,890"]]
    cb_data = []
    for i,row in enumerate(cost_break):
        if i==0:
            cb_data.append([Paragraph(f"<b>{c}</b>", ParagraphStyle('ch', parent=s_body_small, fontName='Helvetica-Bold', textColor=white)) for c in row])
        elif i==len(cost_break)-1:
            cb_data.append([Paragraph("", s_body_small), Paragraph("", s_body_small), Paragraph(f"<b><font size=12 color='#0B1D3A'>{row[2]}</font></b>", s_body_small)])
        else:
            cb_data.append([Paragraph(row[0], s_body_small), Paragraph(row[1], s_body_small), Paragraph(f"Rs. {row[2]}", s_body_small)])
    cb_table = Table(cb_data, colWidths=[85,310,80], repeatRows=1)
    cb_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), NAVY), ('BACKGROUND',(0,-1),(-1,-1), GOLD_LIGHT), ('GRID',(0,0),(-1,-2),0.4, GRAY_200), ('LINEABOVE',(0,-1),(-1,-1),1.5, NAVY), ('LEFTPADDING',(0,0),(-1,-1),6), ('RIGHTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),6), ('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(cb_table)
    story.append(Spacer(1,10))
    story.append(Image(str(ASSETS_DIR / "cost_comparison.png"), width=480, height=260))
    story.append(Paragraph("Cost comparison - ours vs market. 76% cheaper than basic, 85% cheaper than premium, yet includes camera + AI they lack. Plus student-hackable.", s_caption))
    story.append(Spacer(1,8))
    story.append(Paragraph("Sustainability:", s_h3))
    for s_ in ["Water saved: rain override + threshold watering avoids over-water. Test: 40% less water vs daily timer.","Power: 5V/0.6A avg ~3W. 15 ms soil power-gating prevents electrode corrosion -> lasts years.","Zero subscription: free-tier APIs, RTDB, Vercel hobby. No vendor lock-in.","Repairable: breadboard, not PCB. Replace one sensor in 2 min. Judges can see every wire."]:
        story.append(Paragraph(f"- {s_}", s_body_small))
    story.append(PageBreak())

    # Future
    story.append(Anchor("h1_future", "Future"))
    story.append(Paragraph("PART 12 - FUTURE", s_kicker))
    story.append(Paragraph("Where Verde Grows Next", s_h1))
    story.append(Paragraph("We built a finished product. But we sketched roadmap like a startup would. Solar, NPK, zones, alerts.", s_body))
    story.append(Spacer(1,8))
    future = [("Solar Autonomy","12V panel + charge controller + 18650 battery. Day charges, night runs. 3W -> 5W panel enough. Cost +Rs.900.","Q3 2026"),("NPK Soil Probe","Replace LM393 with 3-in-1 NPK + pH. Actual nutrient data -> better AI treatment.","Q4 2026"),("Multi-Plant Zones","One ESP32 drives 4 relays via mux. Each zone threshold per plant type (cactus 20%, fern 60%).","Q1 2027"),("Telegram/WhatsApp Alerts","Pump ON, tank empty, disease detected -> push. Uses Firebase Functions free.","Q2 2026 - 2 days"),("Predictive Watering","Logs -> linear regression on moisture drop rate. Water before wilt, not after.","Q2 2027"),("Deployed Next.js Dashboard","Scaffolded. Migrate single HTML to Next.js + charts + auth + multi-device.","Q3 2026")]
    future_data = [[Paragraph("<b>Feature</b>", ParagraphStyle('fhh', parent=s_body_small, fontName='Helvetica-Bold', textColor=white)), Paragraph("<b>What</b>", ParagraphStyle('fhh2', parent=s_body_small, fontName='Helvetica-Bold', textColor=white)), Paragraph("<b>When</b>", ParagraphStyle('fhh3', parent=s_body_small, fontName='Helvetica-Bold', textColor=white))]]
    for title, what, when_ in future:
        future_data.append([Paragraph(f"<b>{title}</b>", s_body_small), Paragraph(what, s_body_small), Paragraph(when_, s_body_small)])
    future_table = Table(future_data, colWidths=[100,300,80], repeatRows=1)
    future_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), EMERALD_DARK), ('GRID',(0,0),(-1,-1),0.4, GRAY_200), ('ROWBACKGROUNDS',(0,1),(-1,-1), [white, EMERALD_PALE]), ('LEFTPADDING',(0,0),(-1,-1),6), ('RIGHTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),6), ('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(future_table)
    story.append(Spacer(1,10))
    story.append(Paragraph("Why roadmap matters for judges:", s_h3))
    story.append(Paragraph("Shows we think beyond exhibition. Solar makes it field-deployable. NPK precise. Zones real garden solution. Alerts product parents actually use. And we costed every addition.", s_body_small))
    story.append(Spacer(1,10))
    story.append(Image(str(ASSETS_DIR / "api_before_after.png"), width=480, height=240))
    story.append(Paragraph("The bug fix that became principle: fewer, richer calls beat many tiny calls. Applies to future too - batch NPK + moisture in same JSON.", s_caption))
    story.append(PageBreak())

    # Judge Tour
    story.append(Anchor("h1_tour", "Tour"))
    story.append(Paragraph("PART 13 - JUDGE TOUR", s_kicker))
    story.append(Paragraph("3-Minute Demo Script", s_h1))
    story.append(Paragraph("Judges have 180 seconds. We rehearsed it. Here is exact flow that makes them say 'wow'.", s_body))
    story.append(Spacer(1,6))
    tour_steps = [("0:00-0:20 Hook","Hold plant. 'This plant waters itself and talks to AI. Total cost Rs. 1,890. No subscriptions.' Show cover, point to 5 sensors."),("0:20-0:50 Live telemetry","Open Dashboard. Point to 8 tiles sparklines. Dunk soil sensor -> moisture rises live. Cover LDR -> UV LED ON. Hand over ultrasonic -> tank % changes."),("0:50-1:20 Auto logic","Set moisture threshold slider 35->80. Watch pump ON continuous. 'Before fix, it flickered every 10s because 17 calls. Now 2 calls, -85% latency.' Show api_before_after chart."),("1:20-1:50 Plant Doctor","Press CAPTURE. Flash. <=2s later photo appears. 'ESP32-CAM 8MHz XCLK, sequential boot.' Upload diseased leaf -> 94% nutrient deficiency + treatment. Ask Gemini chat 'why yellow?' - sees image + sensors."),("1:50-2:20 Weather + Safety","Show weather page, 5-day chips. 'Rain expected -> pump locks even if soil dry.' Demo tank lock: set tank empty -> pump refuses manual ON. 'Safe.'"),("2:20-2:50 Cost & honesty","Show cost comparison: Rs. 1,890 vs Rs. 8k+. 'We failed 10 times. Relay dead because split rail, DHT temp=0 because GND, CAM probe 0x106 because ribbon. Fix log in doc.'"),("2:50-3:00 Close","QR to live demo. 'Future: solar + NPK + zones. Today: demo-ready, zero reboots 10+ min, watchdog happy.'")]
    tour_data = [[Paragraph("<b>Time</b>", ParagraphStyle('th1', parent=s_body_small, fontName='Helvetica-Bold', textColor=white)), Paragraph("<b>What to say & do</b>", ParagraphStyle('th2', parent=s_body_small, fontName='Helvetica-Bold', textColor=white))]]
    for time_, desc in tour_steps:
        tour_data.append([Paragraph(f"<b>{time_}</b>", s_body_small), Paragraph(desc, s_body_small)])
    tour_table = Table(tour_data, colWidths=[80,400], repeatRows=1)
    tour_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), NAVY), ('GRID',(0,0),(-1,-1),0.4, GRAY_200), ('ROWBACKGROUNDS',(0,1),(-1,-1), [white, GRAY_50]), ('LEFTPADDING',(0,0),(-1,-1),6), ('RIGHTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),6), ('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(tour_table)
    story.append(Spacer(1,10))
    story.append(Paragraph("Pro tips for us:", s_h3))
    for t in ["Keep serial monitor open on side laptop - judges love raw logs.","Have water bowl + hand towel ready for dunk/hand tests.","Fullscreen demo mode hides dev clutter.","If WiFi drops, hotspot fallback auto-connects in 10s - mention it.","Don't say 'AI slop' words like delve, tapestry. Say plain, confident."]:
        story.append(Paragraph(f"- {t}", s_body_small))
    story.append(PageBreak())

    # Conclusion
    story.append(Anchor("h1_conclusion", "Conclusion"))
    story.append(Paragraph("PART 14 - CONCLUSION", s_kicker))
    story.append(Paragraph("Why We Win", s_h1))
    story.append(Paragraph("A Rs. 1,890 student project that looks like a funded startup product - because we sweated details others skip.", s_body))
    story.append(Spacer(1,8))
    win_grid = [[make_kpi_card("REAL COST", "Rs. 1,890", "Fully itemized, no hidden", EMERALD), make_kpi_card("REAL BUG", "17->2", "Shown + fixed, not hidden", GOLD_DARK), make_kpi_card("REAL AI", "94%", "Tested disease ID", EMERALD_DARK)],[make_kpi_card("REAL LIVE", "13 PASS", "Not mock, live sensors", NAVY_LIGHT), make_kpi_card("REAL POWER", "5V/2A", "Lessons logged, PD fail noted", GOLD_DARK), make_kpi_card("REAL OPEN", "100%", "Single HTML, hackable", EMERALD)]]
    for row in win_grid:
        t = Table([row], colWidths=[150,150,150], spaceAfter=6)
        t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'), ('LEFTPADDING',(0,0),(-1,-1),3), ('RIGHTPADDING',(0,0),(-1,-1),3)]))
        story.append(t)
    story.append(Spacer(1,6))
    story.append(Paragraph("What judges remember after 20 projects:", s_h3))
    story.append(Paragraph("- The pump that stayed ON continuously because we fixed architecture.<br/>- The camera that clicked in <=2 s and diagnosed 94%.<br/>- The tank lock that said 'no' even when we pressed ON - safety.<br/>- The cost chart where Rs. 1,890 beats Rs. 12,500 premium kit.<br/>- The honesty: 10 bugs listed with fixes, not hidden.", s_body_small))
    story.append(Spacer(1,10))
    story.append(Paragraph("Closing line for presentation:", s_h3))
    story.append(Paragraph("\"Verde isn't a mini-project for marks. It's a plant that texts you when it's thirsty, shows you its disease, and waters itself when you're on vacation. Built by two Class X students, for less than a video game. And it's running right now.\"", s_quote))
    story.append(Spacer(1,12))
    qr_box_data = [[Image(str(ASSETS_DIR / "cost_comparison.png"), width=70, height=70), Paragraph("<b>Live Demo QR</b><br/>Replace with real QR to<br/>verde.vercel.app or ngrok<br/><font size=8 color='#6B7280'>Add QR image before print. Scan -> live dashboard.</font>", s_body_small)]]
    qr_box = Table(qr_box_data, colWidths=[80,350])
    qr_box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), GRAY_50), ('BOX',(0,0),(-1,-1),0.6,GRAY_200), ('LEFTPADDING',(0,0),(-1,-1),10), ('RIGHTPADDING',(0,0),(-1,-1),10), ('TOPPADDING',(0,0),(-1,-1),10), ('BOTTOMPADDING',(0,0),(-1,-1),10), ('ROUNDEDCORNERS',(0,0),(-1,-1),8)]))
    story.append(qr_box)
    story.append(PageBreak())

    # Appendix
    story.append(Paragraph("APPENDIX", s_kicker))
    story.append(Paragraph("Pin Map, Thresholds, Specs - For Engineers", s_h1))
    story.append(Spacer(1,6))
    spec_data = [["Item","Value (Exact)"],["MCU1","ESP32 WROOM-32 - 240 MHz dual-core, 320KB RAM, 4MB flash"],["MCU2","ESP32-CAM OV2640 + MB programmer - SVGA JPEG, flash LED"],["Soil Moisture AO","GPIO34 (input only) - power gated GPIO23 15ms HIGH per read"],["DHT11 DATA","GPIO4 - shared GND mandatory"],["LDR AO","GPIO35 (input only) - 10-pt avg, +-2% hysteresis"],["HC-SR04","TRIG GPIO18, ECHO GPIO19 - 5-pt filter, invalid rejection, tank_threshold 15%"],["Relay IN1","GPIO5 active-LOW - pump 5V via COM/NO isolated"],["UV LED","GPIO12 active-HIGH + 220ohm resistor"],["ESP32-CAM XCLK","8 MHz (was 20 MHz -> RF interference)"],["Boot","Sequential: camera init first, WiFi after 500ms"],["Watchdog","Hardware watchdog 8s, fed every loop"],["Thresholds default","moisture 35%, tank 15% (0=disabled), light 35%"],["Firebase","RTDB verde-tech-haha, 1 write /s to /sensors (10 metrics), 1 read /s /controls (9 keys)"],["CAM polling","Polls /controls/capture_photo every 1.5s, upload raw JPEG to Vercel -> base64 /latest_scan"],["OWM","GET weather?q=Delhi, city id 1273294, rain ids 2xx/3xx/5xx/6xx -> override=1 check 3 min"],["Plant.id","POST base64 -> crop + disease suggestions, test 94% nutrient deficiency"],["Gemini","gemini-flash-latest, X-goog-api-key header, inline image + diagnosis + telemetry"],["OpenRouter","Bearer sk-or-v1-..., 435 models, 8-model text chain + 5-model vision fallback"],["Cost","Total ~ Rs. 1,890 - electronics 1,320 + power 220 + mechanical 350 + software 0"]]
    spec_table_data = []
    for i,row in enumerate(spec_data):
        if i==0:
            spec_table_data.append([Paragraph(f"<b>{c}</b>", ParagraphStyle('sh', parent=s_body_small, fontName='Helvetica-Bold', textColor=white)) for c in row])
        else:
            spec_table_data.append([Paragraph(f"<b>{row[0]}</b>", s_body_small), Paragraph(row[1], s_body_small)])
    spec_table = Table(spec_table_data, colWidths=[100,390], repeatRows=1)
    spec_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), NAVY), ('GRID',(0,0),(-1,-1),0.4, GRAY_200), ('ROWBACKGROUNDS',(0,1),(-1,-1), [white, GRAY_50]), ('LEFTPADDING',(0,0),(-1,-1),6), ('RIGHTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(spec_table)
    story.append(Spacer(1,10))
    story.append(Paragraph("Build script & sources: generate_verde_pdf_v2.py + assets/. Python 3.11, ReportLab, Matplotlib, Pillow. Output: Project_Verde_Definitive_Documentation.pdf", s_body_small))
    story.append(Spacer(1,10))
    story.append(Paragraph("Acknowledgements: DAV teachers for lab access. Lajpat Nagar electronics shop for Rs. 15 capacitors. OpenWeatherMap, Plant.id, Google Gemini, OpenRouter free tiers. Firebase free. Vercel hobby. Parents for water bowls and tolerance of pump splashes.", s_body_small))
    story.append(PageBreak())

    # Back cover
    story.append(NextPageTemplate('cover'))
    story.append(Spacer(1, 180))
    story.append(Paragraph("Built by Aarav & Anuj<br/>Class X - DAV ACON 5 2026", ParagraphStyle('back1', parent=s_title_cover, fontSize=20, leading=24, textColor=white, alignment=1)))
    story.append(Spacer(1,18))
    story.append(Paragraph("The plant that waters itself - and talks to AI.", ParagraphStyle('back2', parent=s_tagline, fontSize=12, alignment=1, textColor=HexColor("#A7F3D0"))))
    story.append(Spacer(1,30))
    story.append(Paragraph("Total Build Cost ~ Rs. 1,890 - 5 Sensors - 17->2 Calls - 94% Diagnosis - 8 MHz XCLK - 1-sec Heartbeat", ParagraphStyle('back3', parent=s_white_small, alignment=1, fontSize=8)))

    doc = VerdeDocTemplate(OUTPUT_PDF, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    doc.build(story)
    print(f"Built {OUTPUT_PDF}")
    return OUTPUT_PDF

if __name__ == "__main__":
    generate_charts()
    generate_placeholders()
    out = build_pdf()
    import os
    print("Size", os.path.getsize(out))
