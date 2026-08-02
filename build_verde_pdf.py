#!/usr/bin/env python3
"""
Project Verde - World-class documentation builder
Uses ReportLab with premium design system: deep navy #0A1931, emerald #10B981, gold #FBBF24
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

W, H = A4  # 595.28 x 841.89

# Colors
NAVY = HexColor("#0A1931")
NAVY_LIGHT = HexColor("#162447")
NAVY_SOFT = HexColor("#1E3A5F")
EMERALD = HexColor("#10B981")
EMERALD_DARK = HexColor("#065F46")
EMERALD_LIGHT = HexColor("#D1FAE5")
EMERALD_MID = HexColor("#34D399")
GOLD = HexColor("#FBBF24")
GOLD_DARK = HexColor("#D97706")
GOLD_LIGHT = HexColor("#FEF3C7")
BG = HexColor("#F8FAFC")
BG_CARD = HexColor("#FFFFFF")
TEXT = HexColor("#0F172A")
TEXT_MUTED = HexColor("#64748B")
BORDER = HexColor("#E2E8F0")

ASSETS = "/home/user/Goop/assets"
CHARTS = os.path.join(ASSETS, "charts")

# Paragraph styles
styles = {}
styles['h1'] = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=28, leading=32, textColor=NAVY, spaceAfter=8)
styles['h2'] = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=NAVY, spaceAfter=6, spaceBefore=12)
styles['h3'] = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=NAVY_LIGHT, spaceAfter=4, spaceBefore=8)
styles['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=14, textColor=TEXT, spaceAfter=6, alignment=TA_LEFT)
styles['body_muted'] = ParagraphStyle('body_muted', fontName='Helvetica', fontSize=9, leading=13, textColor=TEXT_MUTED, spaceAfter=4)
styles['bullet'] = ParagraphStyle('bullet', fontName='Helvetica', fontSize=9.5, leading=14, textColor=TEXT, leftIndent=14, bulletIndent=0, spaceAfter=4)
styles['caption'] = ParagraphStyle('caption', fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=TEXT_MUTED, alignment=TA_CENTER)
styles['kpi_num'] = ParagraphStyle('kpi_num', fontName='Helvetica-Bold', fontSize=20, leading=22, textColor=NAVY, alignment=TA_CENTER)
styles['kpi_label'] = ParagraphStyle('kpi_label', fontName='Helvetica', fontSize=8, leading=10, textColor=TEXT_MUTED, alignment=TA_CENTER)
styles['pullquote'] = ParagraphStyle('pullquote', fontName='Helvetica-BoldOblique', fontSize=12, leading=16, textColor=EMERALD_DARK, leftIndent=12, borderPadding=(0,0,0,12), spaceBefore=8, spaceAfter=8)

def draw_rounded_rect(c, x, y, w, h, r, fill_color, stroke_color=None, stroke_width=0.5):
    c.saveState()
    c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
    else:
        c.setStrokeColor(fill_color)
    # ReportLab roundRect
    c.roundRect(x, y, w, h, r, fill=1, stroke=1 if stroke_color else 0)
    c.restoreState()

def draw_image_safe(c, path, x, y, w, h, preserve=True):
    if os.path.exists(path):
        try:
            c.drawImage(path, x, y, width=w, height=h, preserveAspectRatio=preserve, mask='auto')
            return True
        except Exception as e:
            print(f"Image fail {path}: {e}")
    # placeholder
    draw_rounded_rect(c, x, y, w, h, 6, BG, BORDER)
    c.setFont("Helvetica", 7)
    c.setFillColor(TEXT_MUTED)
    c.drawCentredString(x+w/2, y+h/2, "IMAGE: "+os.path.basename(path))
    return False

def draw_top_bar(c, title, page_num, total_pages):
    # Navy top bar 38mm
    draw_rounded_rect(c, 0, H-38, W, 38, 0, NAVY, NAVY)
    # Gold accent line bottom of bar
    c.setFillColor(GOLD)
    c.rect(0, H-41, W, 3, fill=1, stroke=0)
    # Title
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(white)
    c.drawString(18*mm, H-22, title.upper())
    # Page number
    c.setFont("Helvetica", 8)
    c.setFillColor(GOLD_LIGHT)
    c.drawRightString(W-18*mm, H-22, f"{page_num:02d} / {total_pages:02d}")
    # small tagline
    c.setFont("Helvetica", 7)
    c.setFillColor(HexColor("#94A3B8"))
    c.drawString(18*mm, H-32, "Project Verde — DAV ACON 5 • 2026 • Aarav & Anuj")

def draw_footer(c):
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.3)
    c.line(18*mm, 14*mm, W-18*mm, 14*mm)
    c.setFont("Helvetica", 6.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(18*mm, 9*mm, "The plant that waters itself — and talks to AI. • verde-tech • Rs.1,890 build • 5 sensors • 17->2 calls fix")
    c.drawRightString(W-18*mm, 9*mm, "Confidential — Competition Copy")

def add_bullet_points(c, x, y, points, width, style_key='bullet'):
    # returns y after drawing
    for pt in points:
        p = Paragraph(f"• {pt}", styles[style_key])
        w, h = p.wrap(width, 1000)
        if y - h < 20*mm:
            break
        p.drawOn(c, x, y-h)
        y -= h + 2
    return y

class VerdeDoc:
    def __init__(self, output_path):
        from reportlab.pdfgen import canvas
        self.output = output_path
        self.canvas = canvas.Canvas(output_path, pagesize=A4)
        self.canvas.setTitle("Project Verde — Definitive Documentation")
        self.canvas.setAuthor("Aarav Choudhary & Anuj")
        self.canvas.setSubject("Smart IoT Irrigation & Plant-Care System — DAV ACON 5")
        self.page_num = 1  # first canvas page is page 1 already
        self.total_pages = 22  # will update after
        self.toc = []

    def new_page(self):
        if self.page_num>=1:
            self.canvas.showPage()
        self.page_num += 1
        # add bookmark
        try:
            self.canvas.bookmarkPage(f"page{self.page_num}")
            self.canvas.addOutlineEntry(f"Page {self.page_num}", f"page{self.page_num}", level=0, closed=False)
        except:
            pass

    def save(self):
        self.canvas.save()
        print(f"Saved PDF to {self.output}")

    # ---- PAGE BUILDERS ----

    def page_cover(self):
        c = self.canvas
        # Full bleed cover image
        draw_image_safe(c, os.path.join(ASSETS, "cover_art.png"), 0, 0, W, H, preserve=False)
        # Overlay gradient simulation - dark navy translucent bottom 55%
        # Use semi-transparent rects stacked
        for i in range(40):
            alpha = 0.02 + i*0.018
            y = i* (H*0.58/40)
            c.saveState()
            c.setFillColor(HexColor("#0A1931"))
            # Can't set alpha easily? Use setFillAlpha if available
            try:
                c.setFillAlpha(alpha)
            except:
                pass
            c.rect(0, y, W, H*0.6/40 +1, fill=1, stroke=0)
            c.restoreState()

        # Content box
        draw_rounded_rect(c, 18*mm, 22*mm, W-36*mm, 150*mm, 12, HexColor("#0A1931"), stroke_color=GOLD, stroke_width=1.2)
        # Gold top line inside
        c.setFillColor(GOLD)
        c.roundRect(18*mm, 22*mm+148*mm, W-36*mm, 3*mm, 0, fill=1, stroke=0)

        # Text inside
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(GOLD)
        c.drawString(24*mm, 22*mm+135*mm, "DAV ACON 5 — TECH EXHIBITION 2026  •  COMPLETE & DEMO-READY")

        c.setFont("Helvetica-Bold", 46)
        c.setFillColor(white)
        c.drawString(24*mm, 22*mm+115*mm, "PROJECT")
        c.setFillColor(EMERALD)
        c.drawString(24*mm, 22*mm+92*mm, "VERDE")

        c.setFont("Helvetica", 13)
        c.setFillColor(HexColor("#CBD5E1"))
        c.drawString(24*mm, 22*mm+80*mm, "The plant that waters itself — and talks to AI.")

        # Divider
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.line(24*mm, 22*mm+72*mm, 90*mm, 22*mm+72*mm)

        # Details
        c.setFont("Helvetica", 9)
        c.setFillColor(white)
        lines = [
            "Creators: Aarav Choudhary (X) & Anuj (X)",
            "Category: Smart IoT Irrigation & Plant-Care",
            "Total Build Cost: Rs. 1,890 (≈ $23 USD) — all software on free tiers",
            "Stack: ESP32 + ESP32-CAM + Firebase + Single-file Web App + 4 AI APIs",
        ]
        y = 22*mm+62*mm
        for line in lines:
            c.drawString(24*mm, y, line)
            y -= 6*mm

        # KPI strip at bottom inside card
        kpis = [("Rs.1,890", "TOTAL COST"), ("5+2", "SENSORS & ACTUATORS"), ("94%", "AI DIAGNOSIS"), ("17->2", "CALLS FIX")]
        x0 = 24*mm
        for num, label in kpis:
            draw_rounded_rect(c, x0, 22*mm+10*mm, 34*mm, 18*mm, 4, BG_CARD, BORDER, 0.5)
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(NAVY)
            c.drawCentredString(x0+17*mm, 22*mm+22*mm, num)
            c.setFont("Helvetica-Bold", 6.5)
            c.setFillColor(TEXT_MUTED)
            c.drawCentredString(x0+17*mm, 22*mm+13*mm, label)
            x0 += 38*mm

        # QR placeholder subtle
        c.setFont("Helvetica", 6)
        c.setFillColor(HexColor("#64748B"))
        c.drawRightString(W-24*mm, 22*mm+8*mm, "Live demo QR inside ->")

        self.toc.append(("Cover", self.page_num))

    def page_60sec(self):
        c = self.canvas
        self.new_page()
        draw_top_bar(c, "The Whole Story in 60 Seconds", self.page_num, self.total_pages)

        y = H-58
        p = Paragraph("The whole project in one glance. If you read only this page, you still get it.", styles['body_muted'])
        w,h = p.wrap(W-36*mm, 100)
        p.drawOn(c, 18*mm, y-h)
        y -= h+8*mm

        # KPI cards row large - compact
        cards = [
            ("Rs. 1,890", "Total cost\nvs Rs.8k commercial", EMERALD),
            ("5 Sensors\n2 Actuators", "Moist/DHT/LDR/Ultra/Relay\nPump + UV LED", NAVY_LIGHT),
            ("17->2 calls/s", "85% less latency\nZero watchdog reboots", GOLD),
            ("94% AI", "Plant disease diag\n+ treatment plan", HexColor("#7C3AED")),
        ]
        x = 18*mm
        card_w = (W-36*mm-12*mm)/4
        card_h = 30*mm
        for num, desc, accent in cards:
            draw_rounded_rect(c, x, y-card_h, card_w, card_h, 8, white, BORDER)
            c.setFillColor(accent)
            c.roundRect(x, y-2, card_w, 3, 1, fill=1, stroke=0)
            # number
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(NAVY)
            first = num.split("\n")[0]
            c.drawCentredString(x+card_w/2, y-10, first)
            if "\n" in num:
                c.setFont("Helvetica", 6.5)
                c.drawCentredString(x+card_w/2, y-16, num.split("\n")[1])
            c.setFont("Helvetica", 6.5)
            c.setFillColor(TEXT_MUTED)
            lines = desc.split("\n")
            yy = y-22
            for line in lines:
                c.drawCentredString(x+card_w/2, yy, line)
                yy -= 3.2*mm
            x += card_w+4*mm
        y -= card_h + 8*mm

        left_x = 18*mm
        col_w = (W-36*mm-8*mm)/2
        col_h = 78*mm

        # Left: Problem -> Solution
        draw_rounded_rect(c, left_x, y-col_h, col_w, col_h, 8, BG, BORDER)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(left_x+5*mm, y-7, "PROBLEM")
        bullets = [
            "Urban families forget or over-water. Plants die from lack of information.",
            "Commercial kits: Rs.8,000+, no camera, no AI, not student-hackable.",
            "We wanted real data, real autonomy, real AI — at Rs.1,890.",
        ]
        yy = y-16
        for b in bullets:
            pp = Paragraph(f"• {b}", ParagraphStyle('pb', parent=styles['bullet'], fontSize=7.5, leading=10))
            w,h = pp.wrap(col_w-10*mm, 200)
            if yy-h < y-col_h+22*mm:
                break
            pp.drawOn(c, left_x+5*mm, yy-h)
            yy -= h+2.5

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(left_x+5*mm, yy-6, "SOLUTION — 3 TIERS")
        pp = Paragraph("• <b>[EDGE]</b> ESP32 brain + 5 sensors + pump/LED + ESP32-CAM eyes<br/>• <b>[CLOUD]</b> Firebase RTDB — single source of truth<br/>• <b>[EXPERIENCE]</b> Single-file web app + 4 AI APIs<br/>• <b>AUTO logic:</b> moisture &lt; 35% AND tank safe AND no rain -> pump ON", ParagraphStyle('pb2', parent=styles['bullet'], fontSize=7, leading=10))
        w,h = pp.wrap(col_w-10*mm, 300)
        pp.drawOn(c, left_x+5*mm, yy-12-h)

        # Right: Visual architecture mini
        draw_rounded_rect(c, left_x+col_w+8*mm, y-col_h, col_w, col_h, 8, white, BORDER)
        draw_image_safe(c, os.path.join(CHARTS, "architecture_diagram.png"), left_x+col_w+10*mm, y-col_h+6*mm, col_w-8*mm, 64*mm, True)

        y -= col_h + 8*mm

        # How it feels - single box bottom
        box_h = 36*mm
        draw_rounded_rect(c, 18*mm, y-box_h, W-36*mm, box_h, 8, HexColor("#FFFBEB"), GOLD_LIGHT, 0.8)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(GOLD_DARK)
        c.drawString(22*mm, y-8, "Why judges love it — honest, working, cheap, explainable.")
        lines = [
            "• We show every bug we hit and how we fixed it (credibility > perfection).",
            "• Demo-ready: pump AUTO runs 120s nonstop, CAM capture <=2s, watchdog 10+ min zero reboots.",
            "• 13-point test matrix — all PASS. Thresholds adjustable from app, persisted in NVS flash.",
            "• Plant Doctor: ESP32-CAM photo -> crop.health 94% diagnosis -> Gemini chat that sees same image.",
            "• Power: 5V/2A adapter, 1000uF cap, 1N4007 diode, 8MHz XCLK, sequential boot.",
        ]
        yy = y-16
        c.setFont("Helvetica", 7.2)
        c.setFillColor(TEXT)
        for line in lines:
            c.drawString(22*mm, yy, line)
            yy -= 4*mm

        draw_footer(c)
        self.toc.append(("60-Second Story", self.page_num))

    def page_contents(self):
        c = self.canvas
        self.new_page()
        draw_top_bar(c, "Contents", self.page_num, self.total_pages)
        y = H-58
        c.setFont("Helvetica-Bold", 22)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Contents")
        c.setFont("Helvetica", 9)
        c.setFillColor(TEXT_MUTED)
        c.drawString(18*mm, y-8*mm, "Hyperlinked for demo — flip in 3 minutes, understand everything.")
        y -= 18*mm

        items = [
            ("01", "Why — The Problem Urban Gardeners Face", "05"),
            ("02", "How It Works — Architecture & Heartbeat", "06"),
            ("03", "Hardware — 5 Sensors, 2 Actuators, Power Safeties", "07-08"),
            ("04", "Firmware V3.0.7 — Scheduler, Watchdog, AUTO Logic", "09"),
            ("05", "The Big Bug — 17 calls -> 2 calls (85% drop)", "10"),
            ("06", "ESP32-CAM V3.0.4 — Eyes, 8MHz XCLK, <=2s Capture", "11"),
            ("07", "Cloud — Firebase Schema (Single Source of Truth)", "12"),
            ("08", "Web App — Dashboard, Weather, Plant Doctor, AI", "13-14"),
            ("09", "AI & 4 APIs — Accuracy Notes & Fallback Chains", "15"),
            ("10", "Features Live — All Controls, Charts, Calibration", "16"),
            ("11", "Testing — 13-Point Matrix (All PASS)", "17"),
            ("12", "Troubleshooting Journal — 10 Bugs We Fixed", "18"),
            ("13", "Visual Data — Moisture Cycle + Heartbeat", "19"),
            ("14", "Cost & Sustainability — Rs.1,890 vs Rs.8,000", "20"),
            ("15", "Future Scope — Solar, NPK, Multi-Zone, Alerts", "21"),
            ("16", "Judge Tour Script — 5-Minute Walkthrough", "22-23"),
            ("17", "Conclusion — What We Learned", "24"),
        ]
        for num, title, pg in items:
            draw_rounded_rect(c, 18*mm, y-10, W-36*mm, 10*mm, 5, white, BORDER, 0.4)
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(EMERALD)
            c.drawString(22*mm, y-3, num)
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(NAVY)
            c.drawString(30*mm, y-3, title)
            c.setFont("Helvetica", 8)
            c.setFillColor(TEXT_MUTED)
            c.drawRightString(W-22*mm, y-3, f"p.{pg}")
            y -= 12*mm

        # Side box image
        draw_image_safe(c, os.path.join(ASSETS, "icons_grid.png"), 18*mm, y-55, W-36*mm, 50, True)

        draw_footer(c)
        self.toc.append(("Contents", self.page_num))

    def page_why(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Why — The Problem", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Plants die from a lack of information.")
        c.setFont("Helvetica", 9.5)
        c.setFillColor(TEXT_MUTED)
        c.drawString(18*mm, y-6*mm, "Urban families love plants. They just don't have real-time data. So they guess. Plants pay the price.")
        y-=20*mm

        left_w = (W-36*mm-8*mm)/2
        left_h = 68*mm

        # Left text - fixed mm
        draw_rounded_rect(c, 18*mm, y-left_h, left_w, left_h, 8, white, BORDER)
        txt = [
            "<b>The real problem:</b> Nobody knows — right now — how dry soil is, if tank is empty, or if rain is coming.",
            "<b>What families do:</b> Water on schedule, not on need. Result: root rot or drought stress.",
            "<b>Commercial kits:</b> Rs.8k+, closed source, no camera, no AI, over-engineered for Indian homes.",
            "<b>Student gap:</b> Kits you can't open, code you can't read, no bug stories — so no learning.",
            "<b>Our lens:</b> A plant should tell us what it needs. And act by itself when we're away.",
        ]
        yy=y-8*mm
        for t in txt:
            pp=Paragraph(f"• {t}", ParagraphStyle('whyb', parent=styles['bullet'], fontSize=8.2, leading=11))
            w,h=pp.wrap(left_w-10*mm, 500)
            if yy-h < y-left_h+4*mm:
                break
            pp.drawOn(c, 18*mm+5*mm, yy-h)
            yy-=h+3*mm

        # Right image
        draw_rounded_rect(c, 18*mm+left_w+8*mm, y-left_h, left_w, left_h, 8, BG, BORDER)
        draw_image_safe(c, os.path.join(ASSETS, "hardware_bench.png"), 18*mm+left_w+10*mm, y-left_h+18*mm, left_w-14*mm, 42*mm, True)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(NAVY)
        c.drawString(18*mm+left_w+12*mm, y-left_h+8*mm, "Bench prototype — organized, 5V/2A powered, 1000uF cap")

        y -= left_h + 8*mm

        # Pull quote
        pq_h = 12*mm
        draw_rounded_rect(c, 18*mm, y-pq_h, W-36*mm, pq_h, 8, EMERALD_LIGHT, EMERALD, 0.8)
        c.setFont("Helvetica-BoldOblique", 10)
        c.setFillColor(EMERALD_DARK)
        c.drawString(22*mm, y-7*mm, "\"Zero walls of text. Every page skimmable in <10 seconds.\" — Design brief we followed")
        y -= 18*mm

        # Bottom three cards - fixed mm and centered text
        cards = [
            ("Over-watering", "Root rot, fungus", "Wasted water", "#FECACA"),
            ("Under-watering", "Drought stress", "Leaves curl & die", "#FEF3C7"),
            ("No data", "Blind guessing", "No tank/rain check", "#BFDBFE"),
        ]
        x=18*mm
        cw=(W-36*mm-8*mm)/3
        card_h = 18*mm
        for title, line1, line2, bg in cards:
            draw_rounded_rect(c, x, y-card_h, cw, card_h, 6, HexColor(bg), BORDER, 0.4)
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(NAVY)
            c.drawString(x+4*mm, y-5*mm, title)
            c.setFont("Helvetica", 7.5)
            c.setFillColor(TEXT)
            c.drawString(x+4*mm, y-9*mm, line1)
            c.drawString(x+4*mm, y-13*mm, line2)
            x+=cw+4*mm

        draw_footer(c)
        self.toc.append(("Why", self.page_num))

    def page_architecture(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "How It Works — Architecture", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Three tiers. One heartbeat. Zero blind spots.")
        y-=16*mm

        # Image full width - larger, fixed mm
        arch_h = 72*mm
        draw_rounded_rect(c, 18*mm, y-arch_h, W-36*mm, arch_h, 8, white, BORDER)
        draw_image_safe(c, os.path.join(CHARTS, "architecture_diagram.png"), 18*mm+6*mm, y-arch_h+6*mm, W-48*mm, arch_h-12*mm, preserve=True)
        y-= arch_h + 8*mm

        # Timeline chart
        heart_h = 34*mm
        draw_rounded_rect(c, 18*mm, y-heart_h, W-36*mm, heart_h, 8, white, BORDER)
        draw_image_safe(c, os.path.join(CHARTS, "heartbeat.png"), 18*mm+6*mm, y-heart_h+6*mm, W-48*mm, heart_h-12*mm, preserve=True)
        y-= heart_h + 10*mm

        # Three pillars - fixed mm boxes, manual lines
        cols = [
            ("EDGE — Thinks fast", ["ESP32 WROOM-32 brain","5 sensors polled 1Hz","10-pt avg soil/LDR","5-pt avg tank + reject","Watchdog 8s fed every loop","Non-blocking millis()","AUTO: moisture < thresh","AND tank safe AND no rain"]),
            ("CLOUD — Single truth", ["Firebase RTDB verde-tech-haha","/sensors: 10 bundled","/controls: 9 bundled","1-sec heartbeat","Public read, validated","Legacy DB secret","Historical moisture_log"]),
            ("EXPERIENCE — Feels human", ["Single-file HTML","8 live tiles + sparklines","Moisture history chart","Weather auto-override","Plant Doctor CAM <=2s","Gemini + OpenRouter AI","Tank calibration SET","Fullscreen + uptime"]),
        ]
        x=18*mm
        cw=(W-36*mm-8*mm)/3
        box_h=48*mm
        for title, lines in cols:
            draw_rounded_rect(c, x, y-box_h, cw, box_h, 8, BG, BORDER, 0.5)
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(NAVY)
            c.drawString(x+4*mm, y-6*mm, title)
            yy = y-12*mm
            c.setFont("Helvetica", 6.8)
            c.setFillColor(TEXT_MUTED)
            for line in lines:
                if yy < y-box_h+3*mm:
                    break
                c.drawString(x+4*mm, yy, line)
                yy -= 3.6*mm
            x+=cw+4*mm

        draw_footer(c)
        self.toc.append(("Architecture", self.page_num))

    def page_hardware(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Hardware — 5 Sensors, 2 Actuators, 2 MCUs", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Rs.1,890 of honest engineering — not shopping list, but power lessons.")
        y-=12*mm

        left_w = (W-36*mm-8*mm)*0.55
        right_w = (W-36*mm-8*mm)*0.45
        table_h = 82*mm

        # Left: Pin mapping table
        draw_rounded_rect(c, 18*mm, y-table_h, left_w, table_h, 8, white, BORDER)
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-6*mm, "Module -> ESP32 Pin -> Role (exact as built)")
        data = [
            ["Soil LM393", "AO->GPIO34, VCC->GPIO23 (gated 15ms)", "% wetness, power-gated"],
            ["DHT11", "DATA->GPIO4", "Temp + humidity"],
            ["LDR module", "AO->GPIO35", "Ambient light -> dark"],
            ["HC-SR04", "TRIG->GPIO18, ECHO->GPIO19", "Tank level, 5-pt filter"],
            ["2-ch Relay", "IN1->GPIO5 (active-LOW)", "Switches 5V pump"],
            ["UV Grow LED", "GPIO12 (HIGH, 220ohm)", "Photosynthetic light"],
            ["ESP32-CAM", "Own board + MB", "SVGA JPEG, <=2s upload"],
        ]
        yy=y-14*mm
        for row in data:
            if data.index(row)%2==0:
                c.setFillColor(BG)
                c.rect(20*mm, yy-2*mm, left_w-4*mm, 7*mm, fill=1, stroke=0)
            c.setFillColor(NAVY)
            c.setFont("Helvetica-Bold", 6.8)
            c.drawString(20*mm, yy, row[0])
            c.setFont("Helvetica", 6.5)
            c.setFillColor(TEXT)
            c.drawString(42*mm, yy, row[1])
            yy-=3*mm
            c.setFont("Helvetica", 6)
            c.setFillColor(TEXT_MUTED)
            c.drawString(42*mm, yy, row[2])
            yy-=5*mm

        # Right: Power lessons
        draw_rounded_rect(c, 18*mm+left_w+8*mm, y-table_h, right_w, table_h, 8, HexColor("#FFFBEB"), GOLD_LIGHT, 0.8)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(GOLD_DARK)
        c.drawString(18*mm+left_w+10*mm, y-6*mm, "Power Design (hard-won lessons)")
        lessons = [
            "<b>Main:</b> 5V/2A phone adapter — NOT USB-PD laptop charger (PD needs handshake chip).",
            "<b>1000uF cap</b> across 5V/GND — absorbs pump+WiFi spikes.",
            "<b>1N4007 diode</b> across pump — kills inductive spikes.",
            "<b>Pump isolated</b> via relay COM/NO on its own 5V source.",
            "<b>Sequential boot:</b> camera first, WiFi after 500ms — prevents 0x20002 crash.",
            "<b>8MHz XCLK</b> (not 20MHz) — fixes RF interference.",
            "<b>Common GND</b> for DHT, else temp=0 ghost.",
        ]
        yy=y-14*mm
        for les in lessons:
            pp=Paragraph(f"• {les}", ParagraphStyle('b', parent=styles['bullet'], fontSize=6.8, leading=10))
            w,h=pp.wrap(right_w-10*mm, 200)
            if yy-h < y-table_h+2*mm:
                break
            pp.drawOn(c, 18*mm+left_w+10*mm, yy-h)
            yy-=h+1.5*mm

        y-= table_h + 10*mm

        diag_h = 56*mm
        draw_rounded_rect(c, 18*mm, y-diag_h, W-36*mm, diag_h, 8, white, BORDER)
        draw_image_safe(c, os.path.join(CHARTS, "circuit_diagram.png"), 18*mm+12*mm, y-diag_h+6*mm, W-60*mm, diag_h-12*mm, preserve=True)

        draw_footer(c)
        self.toc.append(("Hardware", self.page_num))

    def page_hardware2(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Hardware — Bench & Enclosure", self.page_num, self.total_pages)
        y=H-58

        left_w = (W-36*mm-8*mm)/2
        img_h = 52*mm
        # Left bench
        draw_rounded_rect(c, 18*mm, y-img_h, left_w, img_h, 8, white, BORDER)
        draw_image_safe(c, os.path.join(ASSETS, "hardware_bench.png"), 18*mm+6*mm, y-img_h+14*mm, left_w-12*mm, 30*mm, True)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-img_h+6*mm, "Breadboard — organized, green+gold coding, no split-rail bug")

        # Right abstract
        draw_rounded_rect(c, 18*mm+left_w+8*mm, y-img_h, left_w, img_h, 8, white, BORDER)
        draw_image_safe(c, os.path.join(ASSETS, "architecture_abstract.png"), 18*mm+left_w+14*mm, y-img_h+14*mm, left_w-12*mm, 30*mm, True)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(NAVY)
        c.drawString(18*mm+left_w+12*mm, y-img_h+6*mm, "Enclosure idea — future solar top, tidy wiring, child-safe")

        y-= img_h + 12*mm

        bom_h = 58*mm
        draw_rounded_rect(c, 18*mm, y-bom_h, W-36*mm, bom_h, 8, white, BORDER)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-7*mm, "BOM — Every rupee counted (Rs.1,890 total)")
        table = [
            ["Category", "Items", "Cost INR"],
            ["Electronics", "ESP32, ESP32-CAM, 5 sensors, relay, pump, LED", "1,320"],
            ["Power & protection", "5V/2A adapter, 1000uF cap, 1N4007 diode", "220"],
            ["Mechanical", "Breadboard, wires, enclosure", "350"],
            ["Software & APIs", "All free tiers (Firebase, OpenWeather, Plant.id, Gemini, OpenRouter)", "0"],
            ["TOTAL", "", "~ 1,890"],
        ]
        yy=y-16*mm
        for idx, row in enumerate(table):
            if idx==0:
                c.setFillColor(NAVY)
                c.rect(20*mm, yy-2*mm, W-40*mm, 7*mm, fill=1, stroke=0)
                c.setFillColor(white)
                c.setFont("Helvetica-Bold", 7)
            elif idx==len(table)-1:
                c.setFillColor(EMERALD_LIGHT)
                c.rect(20*mm, yy-2*mm, W-40*mm, 7*mm, fill=1, stroke=0)
                c.setFillColor(NAVY)
                c.setFont("Helvetica-Bold", 8)
            else:
                if idx%2==0:
                    c.setFillColor(BG)
                    c.rect(20*mm, yy-2*mm, W-40*mm, 7*mm, fill=1, stroke=0)
                c.setFillColor(TEXT)
                c.setFont("Helvetica", 6.8)
            c.drawString(22*mm, yy, row[0])
            c.drawString(52*mm, yy, row[1][:60])
            c.drawRightString(W-22*mm, yy, row[2])
            yy-=8*mm

        y-= bom_h + 10*mm

        warn_h = 14*mm
        draw_rounded_rect(c, 18*mm, y-warn_h, W-36*mm, warn_h, 6, HexColor("#FEF2F2"), HexColor("#FCA5A5"), 0.8)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(HexColor("#991B1B"))
        c.drawString(20*mm, y-6*mm, "Why we burned a 67W USB-PD charger: PD needs handshake chip ESP32 lacks -> outputs ~0mA -> board starved. Phone 5V/2A always wins.")

        draw_footer(c)

    def page_firmware(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Firmware — Code_1_Main_Brain V3.0.7-FINAL", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Non-blocking. Watchdog-fed. Hysteresis-protected.")
        y-=12*mm

        left_w=(W-36*mm-8*mm)*0.58
        right_w=(W-36*mm-8*mm)*0.42

        # Left
        draw_rounded_rect(c, 18*mm, y-86, left_w, 86, 8, white, BORDER)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-6, "Task scheduler (millis(), not delay())")
        tasks = [
            "sensors 1 Hz — 10-pt avg soil/LDR, 5-pt avg tank + invalid-reject",
            "cloud 1 s — 1 write /sensors (10 metrics) + 1 read /controls (9 keys)",
            "WiFi 10 s — 3-network fallback (home / hotspot / school)",
            "logs 60 s — moisture_log append for history chart",
            "watchdog 8 s — fed every loop, 0 reboots in 10+ min test",
            "Thresholds from app -> NVS flash (moist 35, tank 15, light 35)",
        ]
        yy=y-14
        for t in tasks:
            pp=Paragraph(f"• {t}", styles['bullet'])
            w,h=pp.wrap(left_w-10*mm, 200)
            pp.drawOn(c, 20*mm, yy-h)
            yy-=h+2

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(20*mm, yy-4, "AUTO logic (the brain)")
        pp=Paragraph("pump_ON = <b>moisture &lt; threshold (35%) AND tank safe AND no rain</b><br/>Manual: user-driven but still tank-protected<br/>Light: ±2% hysteresis — no LED flicker", ParagraphStyle('b2', parent=styles['bullet'], fontSize=8, leading=11))
        w,h=pp.wrap(left_w-10*mm, 200)
        pp.drawOn(c, 20*mm, yy-10-h)

        # Right - code snippet stylized
        draw_rounded_rect(c, 18*mm+left_w+8*mm, y-86, right_w, 86, 8, NAVY, NAVY)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(GOLD)
        c.drawString(18*mm+left_w+12*mm, y-8, "Pseudocode — auto()")
        code = [
            "float soil = avg10(moist_raw);",
            "float tank = avg5_filter(ultra);",
            "bool rain = (weather==2xx/3xx/5xx/6xx);",
            "",
            "if (mode==AUTO) {",
            "  if (soil < moist_thresh",
            "   && tank > tank_thresh",
            "   && !rain) pump=ON;",
            "  else pump=OFF;",
            "} else { // MANUAL",
            "  pump = user_pump && tank_ok;",
            "}",
            "feedWatchdog();",
            "// 1 JSON bundle per sec",
            "firebase.set(sensors:{10 keys});",
            "controls = firebase.get(/controls);",
        ]
        c.setFont("Courier", 6.5)
        c.setFillColor(EMERALD_MID)
        yy=y-16
        for line in code:
            c.drawString(18*mm+left_w+12*mm, yy, line)
            yy-=3.5*mm

        y-=94*mm

        # Light auto + thresholds
        draw_rounded_rect(c, 18*mm, y-40, W-36*mm, 40, 8, BG, BORDER)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-8, "Telemetry & thresholds — what makes it stable")
        items = [
            "Soil: LM393 VCC gated via GPIO23 — 15ms read window, prevents corrosion (electrolysis is real).",
            "Tank: 5-point moving avg + invalid-reject — pump splash can't fake empty.",
            "Light: ±2% hysteresis — LDR 10-pt avg, no flicker at dusk.",
            "Lux approx from LDR, watchdog_status, voltage_sag, successful/failed_uploads counted.",
            "Adjustable thresholds from app: moisture 0-100 (default 35), tank 0-100 (0=disabled, default 15), light 0-100 (default 35).",
        ]
        yy=y-16
        for it in items:
            pp=Paragraph(f"• {it}", ParagraphStyle('b3', parent=styles['bullet'], fontSize=7.5, leading=10))
            w,h=pp.wrap(W-40*mm, 200)
            pp.drawOn(c, 20*mm, yy-h)
            yy-=h+1.5

        draw_footer(c)

    def page_bug(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "The Big Bug — BEFORE vs AFTER", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 22)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "The bug that taught us bundling.")
        c.setFont("Helvetica", 9)
        c.setFillColor(TEXT_MUTED)
        c.drawString(18*mm, y-8*mm, "AUTO clicked pump ON/OFF every ~10s. Root cause hunt -> 17 blocking Firebase HTTPS calls per sec -> network stall -> 8s watchdog reboot -> loop.")
        y-=20*mm

        bug_h = 62*mm
        draw_rounded_rect(c, 18*mm, y-bug_h, W-36*mm, bug_h, 8, white, BORDER)
        draw_image_safe(c, os.path.join(CHARTS, "bug_fix.png"), 18*mm+12*mm, y-bug_h+8*mm, W-60*mm, bug_h-16*mm, preserve=True)
        y-=bug_h + 12*mm

        # Explanation two cols
        left_w=(W-36*mm-8*mm)/2
        col_h = 48*mm
        # BEFORE
        draw_rounded_rect(c, 18*mm, y-col_h, left_w, col_h, 8, HexColor("#FEF2F2"), HexColor("#FCA5A5"), 0.6)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(HexColor("#991B1B"))
        c.drawString(20*mm, y-7*mm, "BEFORE — 17 calls/s")
        txt=["Each metric separate HTTPS","Blocking -> loop stalls","WiFi + pump spikes -> brownout","Watchdog 8s fires -> reboot","Pump ON then immediate OFF (loop)","Saw: spurts, reboots, 0 stability"]
        yy=y-14*mm
        for t in txt:
            pp=Paragraph(f"• {t}", ParagraphStyle('bre', parent=styles['bullet'], fontSize=7.5, leading=10, textColor=HexColor("#7F1D1D")))
            w,h=pp.wrap(left_w-10*mm, 200)
            if yy-h < y-col_h+3*mm:
                break
            pp.drawOn(c, 20*mm, yy-h)
            yy-=h+2*mm

        # AFTER
        draw_rounded_rect(c, 18*mm+left_w+8*mm, y-col_h, left_w, col_h, 8, EMERALD_LIGHT, EMERALD, 0.6)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(EMERALD_DARK)
        c.drawString(18*mm+left_w+12*mm, y-7*mm, "AFTER — 2 calls/s (our fix)")
        txt2=["1 WRITE to /sensors: 10 metrics as JSON bundle","1 READ from /controls: 9 keys in one shot","85% less latency, non-blocking","Zero watchdog reboots in 10+ min","Pump stays ON till threshold","Lesson: bundle, don't spam"]
        yy=y-14*mm
        for t in txt2:
            pp=Paragraph(f"• {t}", ParagraphStyle('afe', parent=styles['bullet'], fontSize=7.5, leading=10))
            w,h=pp.wrap(left_w-10*mm, 200)
            if yy-h < y-col_h+3*mm:
                break
            pp.drawOn(c, 18*mm+left_w+12*mm, yy-h)
            yy-=h+2*mm

        y-=col_h + 12*mm
        # Pull quote
        pq_h = 12*mm
        draw_rounded_rect(c, 18*mm, y-pq_h, W-36*mm, pq_h, 6, HexColor("#FFFBEB"), GOLD_LIGHT, 0.8)
        c.setFont("Helvetica-BoldOblique", 9)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-7*mm, "\"This one fix made us judges' favorite — honest debugging > perfect claims.\" — Aarav")

        draw_footer(c)

    def page_cam(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "ESP32-CAM — The Eyes V3.0.4-FINAL", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "SVGA photos in ≤2 seconds. No heap fragmentation.")
        y-=10*mm

        left_w=(W-36*mm-8*mm)*0.55
        right_w=(W-36*mm-8*mm)*0.45

        draw_rounded_rect(c, 18*mm, y-76, left_w, 76, 8, white, BORDER)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-6, "How it works")
        points=[
            "Polls /controls/capture_photo every 1.5s.",
            "On trigger: flash LED -> capture SVGA JPEG -> POST raw bytes to Vercel upload API -> lands in /latest_scan (base64) -> app shows ≤2s.",
            "Engineering (hard-won):",
            "• 8 MHz XCLK (fixes RF interference with WiFi antenna — 20MHz noisy)",
            "• Sequential boot: camera first, WiFi after 500ms — prevents brownout crash 0x20002",
            "• esp_camera_fb_return() immediately — no heap fragmentation",
            "• Image flip fix: CAM mounts upside-down -> app-side CSS flip",
            "• FPC ribbon gold-side down, reseat + power cycle if probe 0x106",
            "• PSRAM not found? Weak power — need 5V/2A adapter.",
        ]
        yy=y-14
        for ptxt in points:
            if "Engineering" in ptxt:
                c.setFont("Helvetica-Bold", 8)
                c.setFillColor(EMERALD_DARK)
                c.drawString(20*mm, yy, ptxt)
                yy-=5*mm
                continue
            pp=Paragraph(f"{ptxt}" if ptxt.startswith("•") else f"• {ptxt}", ParagraphStyle('cam', parent=styles['bullet'], fontSize=7.5, leading=10))
            w,h=pp.wrap(left_w-10*mm, 500)
            if yy-h< y-76+2:
                break
            pp.drawOn(c, 20*mm, yy-h)
            yy-=h+1.5

        # Right image
        draw_rounded_rect(c, 18*mm+left_w+8*mm, y-76, right_w, 76, 8, BG, BORDER)
        draw_image_safe(c, os.path.join(ASSETS, "plant_doctor.png"), 18*mm+left_w+10*mm, y-62, right_w-4*mm, 48, True)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(NAVY)
        c.drawString(18*mm+left_w+12*mm, y-68, "Live CAM -> Plant Doctor -> 94% diagnosis")
        # small stats
        draw_rounded_rect(c, 18*mm+left_w+10*mm, y-76+4*mm, right_w-6*mm, 12*mm, 4, white, BORDER, 0.4)
        c.setFont("Helvetica", 6.5)
        c.setFillColor(TEXT)
        c.drawString(18*mm+left_w+12*mm, y-76+10*mm, "Trigger poll: 1.5s  • Capture: SVGA JPEG • Upload: raw bytes -> Vercel • Display: ≤2s")
        c.drawString(18*mm+left_w+12*mm, y-76+5*mm, "Fixes: 8MHz XCLK, sequential boot, fb_return(), flip CSS, FPC reseat")

        y-=84*mm

        # Bottom flowchart placeholder? Use auto flowchart
        draw_rounded_rect(c, 18*mm, y-58, W-36*mm, 58, 8, white, BORDER)
        draw_image_safe(c, os.path.join(CHARTS, "auto_flowchart.png"), 18*mm+2*mm, y-56, (W-36*mm)/2-4*mm, 54, True)
        # Right side text about flow
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(NAVY)
        c.drawString(18*mm+(W-36*mm)/2+4*mm, y-10, "AUTO-MODE Decision Flow")
        pp=Paragraph("Moisture below 35% <b>AND</b> tank safe (above 15% or disabled) <b>AND</b> no rain expected -> pump ON. All thresholds adjustable from app, persisted in NVS flash.<br/><br/>• <b>Tank protection:</b> pump never runs if unsafe — saves hardware.<br/>• <b>Rain override:</b> OpenWeatherMap IDs 2xx/3xx/5xx/6xx -> weather_override=1 -> skip watering, save water.<br/>• <b>Light:</b> LDR 10-pt avg + ±2% hysteresis -> UV LED auto on at dusk, off at dawn, no flicker.", styles['body'])
        w,h=pp.wrap((W-36*mm)/2-8*mm, 200)
        pp.drawOn(c, 18*mm+(W-36*mm)/2+4*mm, y-18-h)

        draw_footer(c)

    def page_cloud(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Cloud — Firebase RTDB Schema", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Single source of truth. One JSON bundle at a time.")
        y-=12*mm

        left_w=(W-36*mm-8*mm)*0.55
        right_w=(W-36*mm-8*mm)*0.45

        draw_rounded_rect(c, 18*mm, y-84, left_w, 84, 8, white, BORDER)
        draw_image_safe(c, os.path.join(CHARTS, "firebase_schema.png"), 18*mm+2*mm, y-82, left_w-4*mm, 80, True)

        draw_rounded_rect(c, 18*mm+left_w+8*mm, y-84, right_w, 84, 8, BG, BORDER)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(18*mm+left_w+12*mm, y-8, "DB: verde-tech-haha")
        schema = [
            ("Rules", "Public read, validated writes (bool & 0-100). ESP32 uses legacy DB secret — simple for student build, no OAuth dance."),
            ("sensors/", "moisture, temp, humidity, light, tank_level, lux, watchdog_status, voltage_sag, successful_uploads, failed_uploads — bundled in 1 write/sec."),
            ("controls/", "manual_mode, pump_state, light_manual_mode, grow_light_state, capture_photo, moisture_threshold, tank_threshold, light_threshold, weather_override — bundled in 1 read/sec."),
            ("latest_scan/", "imageUrl base64, status, captured_at, scientificName, diseaseName, probability, treatmentPlan — from crop.health API."),
            ("weather/", "city, temp, condition, description, humidity, wind_speed, rain_expected, synced_at — from OpenWeatherMap."),
            ("historical_logs/", "moisture_log [{time, moisture}] — for chart, 60s interval."),
            ("actuators/", "pump_actual, grow_light_actual, mode — predicted states for UI."),
        ]
        yy=y-16
        for k,v in schema:
            pp=Paragraph(f"<b>{k}</b> — {v}", ParagraphStyle('schema', parent=styles['bullet'], fontSize=7.2, leading=10))
            w,h=pp.wrap(right_w-8*mm, 500)
            pp.drawOn(c, 18*mm+left_w+12*mm, yy-h)
            yy-=h+3

        y-=92*mm

        draw_rounded_rect(c, 18*mm, y-36, W-36*mm, 36, 8, NAVY, NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(GOLD)
        c.drawString(22*mm, y-10, "Why RTDB not Firestore? -> RTDB = 1 JSON bundle, ultra low latency, free tier generous, ESP32 HTTP simple. Firestore needs heavier SDK.")
        c.setFont("Helvetica", 8)
        c.setFillColor(white)
        c.drawString(22*mm, y-18, "• Bundled writes: 10 metrics in one object -> ~85% less latency, solves watchdog reboot story.")
        c.drawString(22*mm, y-25, "• Tank calibration: SET EMPTY / SET FULL -> app-side remap, no reflash needed — demo judges love this UX.")
        c.drawString(22*mm, y-32, "• 3-network WiFi fallback: home / hotspot / school — demo never fails because of WiFi.")

        draw_footer(c)

    def page_webapp(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Web App — The Face (Single-file HTML)", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Dashboard so clear parents get it. So deep judges respect it.")
        y-=14*mm

        # Four pages grid
        cards = [
            ("Dashboard", "8 live tiles w/ sparklines + hover graphs (last-10 trend ▲/▼), 8 controls, 3 threshold sliders, predicted actuator states, moisture history chart, system status strip, toasts, fullscreen demo mode, uptime timer.", EMERALD),
            ("Weather", "Live Delhi weather, 5-day forecast chips, auto rain-override (checks every 3 min) with countdown. IDs 2xx/3xx/5xx/6xx -> rain -> weather_override=1.", "#60A5FA"),
            ("Plant Doctor", "Live CAM photo frame auto-updates ≤2s, CAPTURE button, upload-or-CAM modal: photo + crop.health diagnosis + AI chat that sees same image. Flip fix for upside-down mount.", GOLD),
            ("AI Assistants", "Gemini image chat + OpenRouter sensor-aware chat (quick prompts). 8-model text fallback + 5-model vision chain -> never dead-end.", HexColor("#8B5CF6")),
        ]
        x=18*mm
        cw=(W-36*mm-8*mm)/2
        rh=44
        for i, (title, desc, col) in enumerate(cards):
            cx = x + (i%2)*(cw+8*mm)
            cy = y - (i//2)*(rh+6*mm) - rh
            draw_rounded_rect(c, cx, cy, cw, rh, 8, white, BORDER)
            # accent top
            c.setFillColor(col)
            c.roundRect(cx, cy+rh-3, cw, 3, 1, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(NAVY)
            c.drawString(cx+5*mm, cy+rh-10, title)
            pp=Paragraph(desc, ParagraphStyle('web', parent=styles['body'], fontSize=7.5, leading=10))
            w,h=pp.wrap(cw-10*mm, 100)
            pp.drawOn(c, cx+5*mm, cy+rh-16-h)
        y-= (rh+6*mm)*2 + 8*mm

        # Feature screenshot placeholder + calibration
        draw_rounded_rect(c, 18*mm, y-58, W-36*mm, 58, 8, BG, BORDER)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-8, "Live telemetry UX — hover graphs, sparklines, tank calibration panel")
        # three mini boxes
        for i, txt in enumerate(["8 tiles: moisture, temp, humidity, light, tank, lux, watchdog, uploads", "3 sliders: moisture 35, tank 15, light 35 — NVS persisted", "Calibrate: SET EMPTY / SET FULL -> app remap, no reflash"]):
            xx = 20*mm + i*((W-40*mm)/3)
            draw_rounded_rect(c, xx, y-48, (W-48*mm)/3, 34, 5, white, BORDER, 0.5)
            c.setFont("Helvetica", 7)
            c.setFillColor(TEXT)
            pp=Paragraph(txt, styles['body_muted'])
            w,h=pp.wrap((W-48*mm)/3-6*mm, 100)
            pp.drawOn(c, xx+3*mm, y-18-h)

        draw_footer(c)

    def page_webapp2(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Web App — Plant Doctor & AI", self.page_num, self.total_pages)
        y=H-58

        left_w=(W-36*mm-8*mm)*0.5
        # Images
        draw_rounded_rect(c, 18*mm, y-70, left_w, 70, 8, white, BORDER)
        draw_image_safe(c, os.path.join(ASSETS, "plant_doctor.png"), 18*mm+2*mm, y-68, left_w-4*mm, 50, True)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-62, "Plant Doctor flow — ≤2s update")

        # Steps list
        steps=[
            "1. User taps CAPTURE -> controls/capture_photo=1",
            "2. ESP32-CAM polls 1.5s, sees trigger -> flash LED",
            "3. Capture SVGA JPEG -> POST raw bytes to Vercel /api/upload",
            "4. Vercel returns base64 -> write to /latest_scan/imageUrl",
            "5. App auto-updates photo ≤2s (polling)",
            "6. crop.health API POST base64 -> disease + prob + treatment",
            "7. Gemini sees same image + diagnosis + telemetry -> chat",
        ]
        yy=y-70-6
        for s in steps:
            c.setFont("Helvetica", 7)
            c.setFillColor(TEXT)
            c.drawString(20*mm, yy, s)
            yy-=4*mm

        draw_rounded_rect(c, 18*mm+left_w+8*mm, y-70, left_w, 70, 8, NAVY, NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(GOLD)
        c.drawString(18*mm+left_w+12*mm, y-10, "AI Chat UX (image-aware)")
        chat = [
            "User: \"Why yellow leaves?\"",
            "Gemini sees: latest_scan image + diseaseName + moisture 32%",
            "-> \"Nutrient deficiency @94%, soil dry 32% < 35% threshold, tank safe, no rain — watering now + add NPK.\"",
            "OpenRouter fallback chain:",
            "• 8 text models -> if free tier dies -> next",
            "• 5 vision models -> if one down -> next",
            "• Never dead-end, demo resilient.",
            "Quick prompts: \"Explain moisture\", \"Is tank empty?\", \"What to do?\"",
        ]
        yy=y-16
        c.setFont("Helvetica", 7)
        c.setFillColor(white)
        for line in chat:
            if "User:" in line:
                c.setFont("Helvetica-Bold", 7)
                c.setFillColor(GOLD_LIGHT)
            else:
                c.setFont("Helvetica", 7)
                c.setFillColor(HexColor("#CBD5E1"))
            c.drawString(18*mm+left_w+12*mm, yy, line[:86])
            yy-=4*mm

        y-=78*mm

        # Icons grid
        draw_rounded_rect(c, 18*mm, y-44, W-36*mm, 44, 8, white, BORDER)
        draw_image_safe(c, os.path.join(ASSETS, "icons_grid.png"), 18*mm+2*mm, y-42, 60*mm, 40, True)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(84*mm, y-10, "Feature icons — consistent  emerald + navy + gold")
        features=[
            "• Live telemetry (moisture, temp, humidity, light, tank, lux)",
            "• AUTO manual lights, pump, thresholds 35/15/35",
            "• Fullscreen demo mode + uptime timer + toasts",
            "• Weather 5-day forecast + rain override countdown",
            "• Plant Doctor CAPTURE + upload modal + treatment plan",
            "• Tank calibration SET EMPTY / FULL (no reflash)",
            "• Image flip fix (CAM upside-down mount)",
        ]
        yy=y-16
        for f in features:
            c.setFont("Helvetica", 7.5)
            c.setFillColor(TEXT)
            c.drawString(84*mm, yy, f)
            yy-=5*mm

        draw_footer(c)

    def page_apis(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "AI & 4 APIs — Accuracy Notes", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "4 APIs researched, keyed, tested — with fallback chains.")
        y-=12*mm

        # API table big
        headers=["API","Purpose","Auth","Mechanics","Accuracy / Live Test"]
        data=[
            ["OpenWeatherMap","Live weather + 5-day forecast -> rain override","key in URL","GET /data/2.5/weather?q=Delhi; ids 2xx/3xx/5xx/6xx -> rain -> weather_override=1","Live-tested: Delhi 35°C, correct city id 1273294, rain detection works"],
            ["crop.health (Plant.id)","Plant + disease ID","Api-Key header","POST /api/v1/identification base64 image -> result.crop.suggestions[] + result.disease.suggestions[] (name, prob, treatment)","Test image: nutrient deficiency @94% with treatment plan, annotated correctly"],
            ["Google Gemini 2.5 Flash","Vision chat on analysed photo","X-goog-api-key header (AQ keys)","POST /v1beta/models/gemini-flash-latest:generateContent with inline image + diagnosis + telemetry","AQ keys need header; gemini-2.5-flash no longer offered to new -> use gemini-flash-latest — we adapted"],
            ["OpenRouter","Sensor chat + vision fallback","Bearer sk-or-v1-…","POST /api/v1/chat/completions OpenAI-compat, 8-model text chain + 5-model vision chain","435 models accessible; free models rotate -> fallback chains never dead-end, demo resilient"],
        ]

        # Draw table header
        col_widths=[26*mm, 28*mm, 18*mm, 36*mm, 46*mm]
        x=18*mm
        # header row
        draw_rounded_rect(c, x, y-8, sum(col_widths), 8*mm, 4, NAVY, NAVY)
        cx=x+2*mm
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(white)
        for i, h in enumerate(headers):
            c.drawString(cx, y-3, h)
            cx+=col_widths[i]
        y-=10*mm

        # rows
        for row in data:
            rh=18*mm
            draw_rounded_rect(c, x, y-rh+2*mm, sum(col_widths), rh-2*mm, 4, white, BORDER, 0.4)
            cx=x+2*mm
            for i, cell in enumerate(row):
                pp=Paragraph(cell, ParagraphStyle(f'api_{i}', parent=styles['body'], fontSize=6.5, leading=9, textColor=TEXT))
                w,h=pp.wrap(col_widths[i]-4*mm, 100)
                pp.drawOn(c, cx, y - h -1*mm)
                cx+=col_widths[i]
            y-=rh
            if y<30*mm:
                break

        y-=6*mm
        draw_rounded_rect(c, 18*mm, y-28, W-36*mm, 28, 8, EMERALD_LIGHT, EMERALD, 0.6)
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(EMERALD_DARK)
        c.drawString(20*mm, y-8, "Key insight: Fallback chains = judge-proof demo. Free models rotate, but our chain never dead-ends. Vision + text both covered.")
        c.setFont("Helvetica", 7.5)
        c.setFillColor(TEXT)
        c.drawString(20*mm, y-16, "• Gemini AQ keys need X-goog-api-key header (not Authorization). • OpenWeather city id 1273294 Delhi verified • crop.health treatmentPlan field saves parent panic.")

        draw_footer(c)

    def page_features(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Features — All Live", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Everything works — not renders, not mocks.")
        y-=14*mm

        feats=[
            ("Dashboard", ["8 telemetry tiles + sparklines + hover last-10 trend ▲/▼", "Moisture history chart (historical_logs)", "System status strip (watchdog, voltage_sag)", "Predicted actuator states (actuators/)", "Fullscreen demo mode + uptime timer + toasts"]),
            ("Controls", ["Manual/auto pump, grow light manual/auto", "3 threshold sliders (moisture 35 default, tank 15, light 35) -> NVS", "Tank calibration SET EMPTY / SET FULL (app remap, no reflash)", "Weather override countdown"]),
            ("Plant Doctor", ["Live CAM frame auto ≤2s", "CAPTURE button + upload modal", "crop.health diagnosis 94% + treatment", "Gemini image chat (sees same image)", "Image flip fix"]),
            ("AI Assistants", ["Gemini vision chat + OpenRouter sensor chat", "8-model text + 5-model vision fallback chains", "Quick prompts: Explain moisture, Tank status, What to do?", "Telemetry injected into prompts"]),
            ("Reliability", ["1-sec heartbeat, non-blocking millis()", "Watchdog 8s, 0 reboots 10+min", "3-network WiFi fallback", "Power safeties: 1000µF, 1N4007, isolated pump", "Tank lock, rain skip, hysteresis ±2%"]),
        ]

        x=18*mm
        cw=(W-36*mm-8*mm)/2
        # We'll place 2 cols
        yy=y
        for idx, (cat, items) in enumerate(feats):
            col = idx%2
            row = idx//2
            cx = x + col*(cw+8*mm)
            cy = yy - row*52*mm -52*mm
            if cy<18*mm:
                # new page if overflow? For now stop
                pass
            draw_rounded_rect(c, cx, cy, cw, 48*mm, 8, white, BORDER)
            c.setFillColor(EMERALD)
            c.roundRect(cx, cy+45*mm, cw, 3*mm, 1, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(NAVY)
            c.drawString(cx+4*mm, cy+40*mm, cat.upper())
            # bullets
            by=cy+36*mm
            for it in items:
                pp=Paragraph(f"• {it}", ParagraphStyle('feat', parent=styles['bullet'], fontSize=7, leading=9.5))
                w,h=pp.wrap(cw-8*mm, 200)
                if by-h < cy+2*mm:
                    break
                pp.drawOn(c, cx+4*mm, by-h)
                by-=h+1.5

        # override y to below
        y = y - 3*52*mm - 8*mm
        draw_rounded_rect(c, 18*mm, 18*mm, W-36*mm, 18*mm, 8, NAVY, NAVY)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(GOLD)
        c.drawString(20*mm, 30*mm, "Judge note: Hover graphs + sparklines = 'wow' moment. Threshold sliders = 'understand' moment. Tank calibration = 'thoughtful UX' moment.")

        draw_footer(c)

    def page_testing(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Testing — 13-Point Matrix (All PASS)", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "13 tests. All PASS. Demo-ready proof.")
        y-=12*mm

        tests=[
            ["WiFi/boot", "ESP32 + CAM sequential boot, 3-network fallback", "Boots every time, connects in 3-5s", "PASS"],
            ["DHT11 breathe", "Breathe on sensor, watch temp/hum rise", "Temp 24->28, hum 45->70 in 10s", "PASS"],
            ["Moisture dunk", "Dry vs water dunk of probe", "0% dry, 85%+ wet, 15ms gated reads", "PASS"],
            ["LDR cover", "Cover LDR, check dark detection", "Lux drops, dark flag ON, LED auto", "PASS"],
            ["Ultrasonic hand", "Move hand over HC-SR04", "Tank level 5-pt avg tracks hand", "PASS"],
            ["Pump AUTO 120s", "AUTO mode continuous run", "Stays ON 120s no glitch, no watchdog", "PASS"],
            ["OFF at threshold", "Reach moisture threshold", "Pump OFF exactly at 35% (hysteresis)", "PASS"],
            ["Tank lock", "Empty tank simulation", "Pump locked, protects hardware", "PASS"],
            ["Rain override", "Fake rain via weather_override", "Skips watering, countdown shows", "PASS"],
            ["CAM capture ≤2s", "Trigger capture, time to app", "Photo in app ≤2s, flash works", "PASS"],
            ["Plant Doctor 94%", "Diseased leaf test image", "Nutrient deficiency 94% + treatment", "PASS"],
            ["AI chats + fallback", "Gemini + OpenRouter chat", "Both respond, fallback works", "PASS"],
            ["Watchdog 10+ min", "Run 10 min, count reboots", "0 reboots, uptime keeps rising", "PASS"],
        ]

        # Table header
        colws=[24*mm, 46*mm, 48*mm, 14*mm]
        x=18*mm
        draw_rounded_rect(c, x, y-8, sum(colws), 8*mm, 4, NAVY, NAVY)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(white)
        cx=x+2*mm
        for i, h in enumerate(["Test","Procedure","Observation","Result"]):
            c.drawString(cx, y-3, h)
            cx+=colws[i]
        y-=10*mm

        for row in tests:
            rh=9*mm
            bg = EMERALD_LIGHT if "PASS" in row[3] else BG
            draw_rounded_rect(c, x, y-rh+2*mm, sum(colws), rh-2*mm, 3, bg, BORDER, 0.3)
            cx=x+2*mm
            for i, cell in enumerate(row):
                if i==3:
                    c.setFont("Helvetica-Bold", 7)
                    c.setFillColor(EMERALD_DARK)
                    c.drawString(cx, y-4, cell)
                else:
                    pp=Paragraph(cell, ParagraphStyle(f'test{i}', parent=styles['body'], fontSize=6.5, leading=8))
                    w,h=pp.wrap(colws[i]-4*mm, 100)
                    pp.drawOn(c, cx, y-3-h)
                cx+=colws[i]
            y-=rh

        y-=6*mm
        draw_rounded_rect(c, 18*mm, y-18, W-36*mm, 18, 6, HexColor("#FFFBEB"), GOLD_LIGHT, 0.6)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-6, "KPI: Pump AUTO 120s nonstop (before fix: 10s ON/OFF loop). After JSON bundling fix -> stable.")

        draw_footer(c)

    def page_troubleshoot(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Troubleshooting Journal — 10 Bugs Honest", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Honesty = credibility. We hit 10 bugs. We fixed all 10.")
        y-=14*mm

        bugs=[
            ["AUTO 10s pump loop", "Pump ON/OFF every ~10s", "17 Firebase calls/s -> stall -> watchdog reboot", "JSON bundling: 1 write +1 read per sec -> 2 calls/s, 85% less latency"],
            ["Camera probe 0x106", "Camera not detected", "FPC ribbon unseated, gold-side wrong", "Reseat gold-side down + power cycle, check connector lock"],
            ["PSRAM not found", "CAM init fail", "Weak power, 67W PD charger 0mA", "5V/2A phone adapter only, not laptop PD"],
            ["0x20002 boot crash", "Brownout on boot", "Camera+WiFi surge together", "Sequential boot: CAM first, WiFi 500ms after"],
            ["RF interference", "Garbled image + WiFi drop", "20MHz XCLK too high, antenna coupling", "Throttle XCLK to 8MHz, stable"],
            ["67W PD starved", "Board dead", "PD requires handshake chip ESP32 lacks", "Phone adapter 5V/2A, 1000µF cap absorbs spikes"],
            ["Relay dead", "Pump not switching", "Split breadboard rails — + not connected", "Bridge + to +, - to -, continuity check"],
            ["temp=0", "DHT reads zero", "Wrong pin + floating GND", "GPIO4 + shared GND, pull-up internal"],
            ["Firebase spurts", "Data jumps like heartbeat missing", "13 calls/s overlapping", "One bundled call per second, non-blocking"],
            ["Missing quote compile", "\"missing terminating \" error", "Copy-paste corruption in secrets", "Re-download file, check quotes"],
        ]

        colws=[26*mm, 26*mm, 38*mm, 42*mm]
        x=18*mm
        # header
        draw_rounded_rect(c, x, y-8, sum(colws), 8*mm, 4, NAVY, NAVY)
        c.setFont("Helvetica-Bold", 6.5)
        c.setFillColor(white)
        cx=x+2*mm
        for i, h in enumerate(["Bug","Symptom","Root Cause","Fix"]):
            c.drawString(cx, y-3, h)
            cx+=colws[i]
        y-=10*mm

        for row in bugs:
            rh=10.5*mm
            draw_rounded_rect(c, x, y-rh+2*mm, sum(colws), rh-2*mm, 3, white, BORDER, 0.3)
            cx=x+2*mm
            for i, cell in enumerate(row):
                pp=Paragraph(cell, ParagraphStyle(f'bug{i}', parent=styles['body'], fontSize=6.2, leading=8))
                w,h=pp.wrap(colws[i]-4*mm, 200)
                pp.drawOn(c, cx, y-2-h)
                cx+=colws[i]
            y-=rh

        draw_footer(c)

    def page_visuals(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Visual Data — Moisture Cycle + Heartbeat", self.page_num, self.total_pages)
        y=H-58

        draw_rounded_rect(c, 18*mm, y-56, W-36*mm, 56, 8, white, BORDER)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-8, "Moisture Watering-Cycle with Threshold Marker (35%)")
        draw_image_safe(c, os.path.join(CHARTS, "moisture_cycle.png"), 18*mm+2*mm, y-54, W-40*mm, 46, True)
        y-=64*mm

        draw_rounded_rect(c, 18*mm, y-64, W-36*mm, 64, 8, white, BORDER)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-8, "One-Second Heartbeat Timeline — Non-blocking millis() Scheduler")
        draw_image_safe(c, os.path.join(CHARTS, "heartbeat.png"), 18*mm+2*mm, y-62, W-40*mm, 30, True)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(TEXT_MUTED)
        txt="Sensors 1Hz (10-pt avg soil/LDR, 5-pt tank filter) -> Bundle JSON 10 metrics -> 1 Write /sensors -> 1 Read /controls -> Actuate pump/LED -> Feed 8s watchdog. Total <300ms, leaves 700ms slack. Tank invalid-reject prevents splash fake-empty. ±2% hysteresis stops LED flicker."
        pp=Paragraph(txt, styles['body_muted'])
        w,h=pp.wrap(W-42*mm, 100)
        pp.drawOn(c, 20*mm, y-50-h)

        y-=72*mm
        # Circuit again small
        draw_rounded_rect(c, 18*mm, y-38, W-36*mm, 38, 8, BG, BORDER)
        draw_image_safe(c, os.path.join(CHARTS, "circuit_diagram.png"), 18*mm+2*mm, y-36, W-40*mm, 34, True)

        draw_footer(c)

    def page_cost(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Cost & Sustainability", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Rs.1,890 vs Rs.8,000+ — 76% cheaper with more features.")
        y-=14*mm

        left_w=(W-36*mm-8*mm)*0.55
        draw_rounded_rect(c, 18*mm, y-56, left_w, 56, 8, white, BORDER)
        draw_image_safe(c, os.path.join(CHARTS, "cost_comparison.png"), 18*mm+2*mm, y-54, left_w-4*mm, 52, True)

        draw_rounded_rect(c, 18*mm+left_w+8*mm, y-56, W-36*mm-left_w-8*mm, 56, 8, BG, BORDER)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(18*mm+left_w+12*mm, y-8, "Why ours wins")
        bullets=[
            "• Camera + AI plant doctor (commercial: none or $20/mo)",
            "• Open source + student understandable (commercial: closed)",
            "• Tank + rain checks (commercial: often moisture only)",
            "• 5 sensors vs 1-2, adjustable thresholds",
            "• Free tier APIs — $0 software",
            "• Power engineering documented",
            "• Honest bug journal = learnable",
        ]
        yy=y-16
        for b in bullets:
            c.setFont("Helvetica", 7.5)
            c.setFillColor(TEXT)
            c.drawString(18*mm+left_w+12*mm, yy, b)
            yy-=5*mm

        y-=64*mm

        # Sustainability
        draw_rounded_rect(c, 18*mm, y-50, W-36*mm, 50, 8, EMERALD_LIGHT, EMERALD, 0.6)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(EMERALD_DARK)
        c.drawString(20*mm, y-10, "Sustainability — low power, water saving, future solar")
        sust=[
            "• Water: AUTO only when needed + rain skip -> saves ~30% vs schedule watering.",
            "• Power: ESP32 deep-sleep ready, 5V/2A adapter (8W max), pump only ON when <35%.",
            "• Materials: breadboard reusable, enclosure from recycled plastic options.",
            "• Software free tiers -> no subscription e-waste.",
            "• Future: 12V solar panel + charge controller + battery -> full autonomy.",
        ]
        yy=y-20
        for s in sust:
            pp=Paragraph(s, ParagraphStyle('sus', parent=styles['body'], fontSize=8, leading=11, textColor=NAVY))
            w,h=pp.wrap(W-42*mm, 200)
            pp.drawOn(c, 20*mm, yy-h)
            yy-=h+2

        draw_footer(c)

    def page_future(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Future Scope", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Today Rs.1,890. Tomorrow autonomous farm.")
        y-=12*mm

        draw_rounded_rect(c, 18*mm, y-60, W-36*mm, 60, 8, white, BORDER)
        draw_image_safe(c, os.path.join(ASSETS, "future_vision.png"), 18*mm+2*mm, y-58, W-40*mm, 56, True)
        y-=68*mm

        futures=[
            ("Solar autonomy", "12V panel + MPPT + 18650 battery -> 24/7 off-grid, NVS thresholds survive reboots.", EMERALD),
            ("NPK probe", "Soil nitrogen/phosphorus/potassium -> precise nutrient deficiency AI, not just visual.", GOLD),
            ("Multi-zone", "One ESP32 + 4 relays + soil sensors each -> balcony with 4 plant types different needs.", NAVY_LIGHT),
            ("Alerts", "Telegram/WhatsApp bot -> 'Tank empty', 'Watered at 3pm', 'Rain tomorrow skip'.", HexColor("#8B5CF6")),
            ("Predictive", "Use historical_logs to predict drying rate -> water before threshold, ML.", HexColor("#0EA5E9")),
            ("Deployed dashboard", "Next.js + Tailwind scaffold ready -> beyond single-file, auth, multi-user, charts.", EMERALD_DARK),
        ]
        # grid 3 cols x2 rows
        cw=(W-36*mm-8*mm)/3
        rh=28*mm
        x0=18*mm
        yy=y
        for i, (title, desc, col) in enumerate(futures):
            col_idx=i%3
            row_idx=i//3
            cx=x0+col_idx*(cw+4*mm)
            cy=yy - row_idx*(rh+4*mm) - rh
            draw_rounded_rect(c, cx, cy, cw, rh, 8, white, BORDER, 0.5)
            c.setFillColor(col)
            c.roundRect(cx, cy+rh-3, cw, 3, 1, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 8.5)
            c.setFillColor(NAVY)
            c.drawString(cx+4*mm, cy+rh-9, title)
            pp=Paragraph(desc, ParagraphStyle('fut', parent=styles['body'], fontSize=7, leading=9.5))
            w,h=pp.wrap(cw-8*mm, 200)
            pp.drawOn(c, cx+4*mm, cy+rh-14-h)

        draw_footer(c)

    def page_tour(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Judge Tour Script — 5-Minute Walkthrough", self.page_num, self.total_pages)
        y=H-58
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(NAVY)
        c.drawString(18*mm, y, "Flip -> tell story -> demo -> answer. 5 minutes.")
        y-=14*mm

        script=[
            ("0:00-0:30 — Hook (Cover + 60s)", "Show cover KPI strip Rs.1,890, 17->2 bug fix, Plant Doctor. Say: 'Plant that waters itself and talks to AI, built for Rs.1,890. Visual + AI + cheap.'"),
            ("0:30-1:15 — Why + Architecture", "Problem: plants die lack info. Our 3 tiers: EDGE (ESP32+5 sensors+ CAM eyes), CLOUD (Firebase single truth), EXPERIENCE (web app+4 AI). 1-sec heartbeat timeline."),
            ("1:15-2:00 — Hardware + Power Lessons", "Point hardware bench image. 5 sensors pins: soil GPIO34/23 gated 15ms, DHT GPIO4, LDR GPIO35, ultra TRIG18 ECHO19, relay GPIO5 LOW, LED GPIO12 HIGH 220Ω. Power: 5V/2A phone, NOT PD, 1000µF cap, 1N4007 diode, isolated pump, 8MHz XCLK, sequential boot."),
            ("2:00-2:45 — Firmware + Big Bug Story (STAR)", "V3.0.7 FINAL non-blocking millis() scheduler, watchdog 8s, 10-pt avg soil/LDR, 5-pt tank filter, ±2% hysteresis, thresholds 35/15/35 NVS. BIG BUG: AUTO pump 10s loop -> 17 calls/s stall -> watchdog reboot -> fix bundling -> 2 calls/s 85% less latency, zero reboots, pump stays ON till threshold. Judges love honesty."),
            ("2:45-3:30 — Live Demo (Dashboard)", "Open web app: 8 tiles + sparklines hover, moisture chart, SET EMPTY/FULL calibration no reflash, threshold sliders, fullscreen mode. Trigger tank lock, rain override, manual pump (still tank-protected). Uptime timer ticks."),
            ("3:30-4:15 — Plant Doctor + AI", "Tap CAPTURE -> ESP32-CAM 1.5s poll, flash, SVGA JPEG -> Vercel -> /latest_scan base64 -> app ≤2s. crop.health 94% nutrient deficiency + treatment. Gemini sees same image + telemetry. OpenRouter fallback chain 8 text +5 vision -> demo never dies."),
            ("4:15-4:50 — Testing + Cost", "13-point matrix all PASS, show watchdog 10+ min 0 reboots, pump AUTO 120s stable. Cost Rs.1,890 vs commercial Rs.8k+ 76% cheaper + camera+AI. Sustainability + future solar."),
            ("4:50-5:00 — Closing", "Tagline + QR to live demo. 'Built by Aarav & Anuj, Class X, not funded startup — but looks like one.'"),
        ]

        yy=y
        for title, desc in script:
            if yy<30*mm:
                break
            draw_rounded_rect(c, 18*mm, yy-22, W-36*mm, 22, 6, white, BORDER, 0.4)
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(EMERALD_DARK)
            c.drawString(20*mm, yy-6, title)
            pp=Paragraph(desc, ParagraphStyle('tour', parent=styles['body'], fontSize=7.5, leading=10))
            w,h=pp.wrap(W-44*mm, 200)
            pp.drawOn(c, 20*mm, yy-10-h)
            yy-=24*mm

        draw_footer(c)

    def page_tour2(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Judge Tour — Anticipated Questions", self.page_num, self.total_pages)
        y=H-58
        qs=[
            ("Why Firebase RTDB not Firestore / Supabase?", "RTDB = 1 JSON bundle, low overhead, free tier, ESP32 HTTP simple, latency <150ms. Firestore SDK heavier, needs more RAM, student-unfriendly. RTDB validated writes enough."),
            ("Why phone adapter not PD?", "USB-PD negotiates voltage via CC handshake chip. ESP32 lacks it, PD charger shuts down 0mA. Phone 5V/2A is dumb 5V — always on, reliable + cheap."),
            ("How 17->2 fix works? Isn't Firebase unlimited?", "17 blocking HTTPS calls/sec each ~200-400ms -> 17× blocking ≈ 3-6 sec stall per second -> millis() scheduler starved -> watchdog not fed -> reboot. Bundling = 1 write+s tail."),
            ("What if WiFi dies at demo?", "3-network fallback list, plus hotspotted phone backup. Also sequential boot prevents brownout, cap prevents spikes. We demo with hotspot ready."),
            ("Accuracy of tank ultrasonic?", "HC-SR04 5-point median filter + invalid-reject (pump splash creates 0-2cm fake empty). Plus app calibration SET EMPTY/FULL remaps raw to %."),
            ("Why ESP32-CAM 8MHz not 20MHz?", "20MHz XCLK radiates RF near WiFi antenna -> interference -> packet loss + garbled JPEG. 8MHz lowers EMI, same SVGA quality, stable."),
            ("Is 94% diagnosis reliable?", "crop.health (Plant.id) on test diseased leaf gave nutrient deficiency 94% + treatment. Not 100% — we show probability, treatmentPlan, plus Gemini second opinion."),
            ("Can it scale to many plants?", "Future: one ESP32 drives 4 relays + moist sensors per zone, threshold per plant, Next.js dashboard scaffold exists."),
        ]
        yy=y
        for q,a in qs:
            draw_rounded_rect(c, 18*mm, yy-24, W-36*mm, 24, 6, BG, BORDER, 0.4)
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(NAVY)
            c.drawString(20*mm, yy-6, "Q: "+q)
            pp=Paragraph("A: "+a, ParagraphStyle('qa', parent=styles['body'], fontSize=7.5, leading=10))
            w,h=pp.wrap(W-44*mm, 200)
            pp.drawOn(c, 20*mm, yy-12-h)
            yy-=26*mm

        draw_footer(c)

    def page_conclusion(self):
        c=self.canvas
        self.new_page()
        draw_top_bar(c, "Conclusion — What We Learned", self.page_num, self.total_pages)
        y=H-58

        # Left text
        left_w=(W-36*mm-8*mm)*0.62
        right_w=(W-36*mm-8*mm)*0.38

        draw_rounded_rect(c, 18*mm, y-84, left_w, 84, 8, white, BORDER)
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(NAVY)
        c.drawString(20*mm, y-8, "We built a product, not just a project.")
        points=[
            "From idea to demo-ready: hardware, firmware V3.0.7, CAM V3.0.4, cloud, web app, 4 AI APIs — all working together, one-second heartbeat.",
            "Engineering lessons > shopping: power caps, flyback diodes, sequential boot, 8MHz XCLK, gated moisture reads to prevent corrosion — these small things make big reliability.",
            "The big lesson: bundling JSON (17->2) saved us. Not more code, less calls. 85% latency drop, zero watchdog reboots, pump stays ON. That's real engineering.",
            "AI with honesty: crop.health 94% diagnosis is helpful but not gospel — we show probability + treatment + Gemini second opinion, and OpenRouter fallback chain keeps demo alive.",
            "Cost matters: Rs.1,890 is one-tenth of commercial kits plus we added camera + AI. Students can build it, teachers can understand it, parents can read any page.",
            "Design matters too: short paragraphs ≤90 words, bullets, hero numbers, pull quotes, white space — nobody reads walls of text. This doc itself is our design statement.",
        ]
        yy=y-18
        for ptxt in points:
            pp=Paragraph(f"• {ptxt}", styles['bullet'])
            w,h=pp.wrap(left_w-10*mm, 500)
            if yy-h< y-84+2:
                break
            pp.drawOn(c, 20*mm, yy-h)
            yy-=h+3

        # Right QR + stats
        draw_rounded_rect(c, 18*mm+left_w+8*mm, y-84, right_w, 84, 8, NAVY, NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(GOLD)
        c.drawString(18*mm+left_w+12*mm, y-10, "Live Demo")
        draw_image_safe(c, os.path.join(ASSETS, "qr_demo.png"), 18*mm+left_w+14*mm, y-54, 28*mm, 28*mm, True)
        c.setFont("Helvetica", 7)
        c.setFillColor(white)
        c.drawString(18*mm+left_w+12*mm, y-60, "QR -> verde-tech-demo.vercel.app")
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(EMERALD_MID)
        c.drawString(18*mm+left_w+12*mm, y-68, "Creators: Aarav & Anuj — Class X")
        c.setFont("Helvetica", 6.5)
        c.setFillColor(HexColor("#94A3B8"))
        stats=[
            "• 5 sensors: soil, DHT11, LDR, HC-SR04, relay",
            "• 2 actuators: pump, UV LED",
            "• 2 MCUs: ESP32 WROOM-32 + ESP32-CAM",
            "• 1 sec heartbeat, 8s watchdog",
            "• Thresholds 35/15/35 NVS",
            "• 10-pt soil avg, 5-pt tank filter",
            "• ±2% hysteresis, 1000µF cap",
            "• 1N4007 flyback, 8MHz XCLK",
        ]
        yy=y-74
        for s in stats:
            c.drawString(18*mm+left_w+12*mm, yy, s)
            yy-=3.5*mm

        y-=92*mm

        # Final tagline full width
        draw_rounded_rect(c, 18*mm, y-22, W-36*mm, 22, 8, EMERALD, EMERALD)
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(white)
        c.drawCentredString(W/2, y-8, "Project Verde — The plant that waters itself — and talks to AI. 🌿")
        c.setFont("Helvetica", 8)
        c.drawCentredString(W/2, y-16, "Built with honesty, tested with rigor, priced for every home.")

        draw_footer(c)

    def build(self):
        # cover
        self.page_cover()
        # 60sec
        self.page_60sec()
        # contents
        self.page_contents()
        # why
        self.page_why()
        # architecture
        self.page_architecture()
        # hardware
        self.page_hardware()
        self.page_hardware2()
        # firmware
        self.page_firmware()
        # bug
        self.page_bug()
        # cam
        self.page_cam()
        # cloud
        self.page_cloud()
        # webapp 1
        self.page_webapp()
        # webapp2
        self.page_webapp2()
        # apis
        self.page_apis()
        # features
        self.page_features()
        # testing
        self.page_testing()
        # troubleshoot
        self.page_troubleshoot()
        # visuals
        self.page_visuals()
        # cost
        self.page_cost()
        # future
        self.page_future()
        # tour
        self.page_tour()
        self.page_tour2()
        # conclusion
        self.page_conclusion()

        # update total pages for footer? We tracked page_num
        print(f"Built {self.page_num} pages")
        self.save()

if __name__=="__main__":
    out = "/home/user/Goop/Project_Verde_Documentation.pdf"
    doc = VerdeDoc(out)
    doc.build()
