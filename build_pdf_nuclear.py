#!/usr/bin/env python3
"""
Project Verde — DEFINITIVE Documentation Builder (NUCLEAR EDITION)
Generates a world-class 35-page PDF with charts, diagrams, and full design system.
"""

import os
import math
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, Flowable, Frame, PageTemplate, BaseDocTemplate,
    NextPageTemplate, FrameBreak, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color

# ============================================================
# REGISTER UNICODE FONTS
# ============================================================
FONT_DIR = '/usr/share/fonts/truetype/dejavu'
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('DejaVu', os.path.join(FONT_DIR, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', os.path.join(FONT_DIR, 'DejaVuSans-Bold.ttf')))

# ============================================================
# DESIGN SYSTEM
# ============================================================
NAVY = HexColor('#0A1628')
NAVY_LIGHT = HexColor('#1A2744')
EMERALD = HexColor('#00A86B')
EMERALD_DARK = HexColor('#008F5A')
GOLD = HexColor('#D4AF37')
GOLD_LIGHT = HexColor('#F0D060')
WHITE = HexColor('#FFFFFF')
OFF_WHITE = HexColor('#F8FAFE')
LIGHT_GRAY = HexColor('#E8ECF2')
MID_GRAY = HexColor('#8899AA')
TEXT_DARK = HexColor('#1A1A2E')
TEXT_BODY = HexColor('#2D3748')
ALERT_RED = HexColor('#E53E3E')
ALERT_ORANGE = HexColor('#DD6B20')
SUCCESS_GREEN = HexColor('#38A169')
SIDEBAR_BG = HexColor('#F0F7F4')

PAGE_W, PAGE_H = A4
MARGIN = 22 * mm
CONTENT_W = PAGE_W - 2 * MARGIN
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

# ============================================================
# CUSTOM FLOWABLES
# ============================================================

class SectionHeader(Flowable):
    """Full-bleed colored section header."""
    def __init__(self, width, number, title, subtitle='', color=NAVY):
        Flowable.__init__(self)
        self.width = width
        self.height = 85 if subtitle else 65
        self.number = number
        self.title = title
        self.subtitle = subtitle
        self.color = color

    def draw(self):
        c = self.canv
        # Background
        c.setFillColor(self.color)
        c.rect(-22*mm, 0, self.width + 44*mm, self.height, fill=1, stroke=0)
        
        # Gold accent line at top
        c.setStrokeColor(GOLD)
        c.setLineWidth(3)
        c.line(-22*mm, self.height - 1, self.width + 22*mm, self.height - 1)
        
        # Number
        c.setFillColor(Color(1, 1, 1, 0.2))
        c.setFont('DejaVu-Bold', 72)
        c.drawString(-18*mm, 5, self.number)
        
        # Title
        c.setFillColor(WHITE)
        c.setFont('DejaVu-Bold', 22)
        y = self.height - 30
        c.drawString(5*mm, y, self.title)
        
        # Subtitle
        if self.subtitle:
            c.setFillColor(Color(1, 1, 1, 0.7))
            c.setFont('DejaVu', 11)
            c.drawString(5*mm, y - 18, self.subtitle)


class KPICard(Flowable):
    def __init__(self, width, number, label, color=EMERALD):
        Flowable.__init__(self)
        self.width = width
        self.height = 70
        self.number = number
        self.label = label
        self.color = color

    def draw(self):
        c = self.canv
        c.setFillColor(WHITE)
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=1)
        c.setFillColor(self.color)
        c.rect(0, self.height - 3, self.width, 3, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.setFont('DejaVu-Bold', 22)
        c.drawCentredString(self.width/2, self.height - 35, str(self.number))
        c.setFillColor(TEXT_BODY)
        c.setFont('DejaVu', 8)
        c.drawCentredString(self.width/2, 8, self.label)


class SectionDivider(Flowable):
    def __init__(self, width=CONTENT_W, color=EMERALD):
        Flowable.__init__(self)
        self.width = width
        self.height = 6
        self.color = color

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.color)
        c.setLineWidth(2)
        c.line(0, 3, self.width * 0.3, 3)
        c.setFillColor(GOLD)
        c.circle(self.width * 0.3 + 5, 3, 3, fill=1, stroke=0)


class CalloutBox(Flowable):
    def __init__(self, width, text, box_type='info'):
        Flowable.__init__(self)
        self.width = width
        self.text = text
        self.box_type = box_type
        self._calc_height()

    def _calc_height(self):
        chars_per_line = int(self.width / 5.2)
        lines = max(1, math.ceil(len(self.text) / chars_per_line))
        self.height = lines * 14 + 24

    def draw(self):
        c = self.canv
        colors_map = {
            'info': (NAVY_LIGHT, WHITE),
            'warning': (GOLD, TEXT_DARK),
            'success': (EMERALD, WHITE),
            'bug': (HexColor('#4A1C1C'), WHITE),
        }
        bg, fg = colors_map.get(self.box_type, (NAVY_LIGHT, WHITE))
        c.setFillColor(bg)
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        icons = {'info': 'i', 'warning': '!', 'success': 'v', 'bug': 'x'}
        c.setFillColor(fg)
        c.setFont('DejaVu-Bold', 12)
        c.drawString(12, self.height - 18, icons.get(self.box_type, '*'))
        c.setFont('DejaVu', 9)
        x = 32
        y = self.height - 18
        words = self.text.split()
        line = ''
        max_w = self.width - 44
        for word in words:
            test = line + ' ' + word if line else word
            if c.stringWidth(test, 'DejaVu', 9) < max_w:
                line = test
            else:
                c.drawString(x, y, line)
                y -= 14
                line = word
        if line:
            c.drawString(x, y, line)


class Sidebar(Flowable):
    """A sidebar with colored background."""
    def __init__(self, width, text, title=''):
        Flowable.__init__(self)
        self.width = width
        self.text = text
        self.title = title
        chars_per_line = int(self.width / 5.0)
        lines = max(1, math.ceil(len(self.text) / chars_per_line))
        self.height = lines * 13 + (30 if title else 16)

    def draw(self):
        c = self.canv
        c.setFillColor(SIDEBAR_BG)
        c.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=0)
        # Left accent
        c.setFillColor(EMERALD)
        c.rect(0, 4, 3, self.height - 8, fill=1, stroke=0)
        y = self.height - 12
        if self.title:
            c.setFillColor(EMERALD_DARK)
            c.setFont('DejaVu-Bold', 9)
            c.drawString(10, y, self.title)
            y -= 16
        c.setFillColor(TEXT_BODY)
        c.setFont('DejaVu', 8.5)
        x = 10
        words = self.text.split()
        line = ''
        max_w = self.width - 20
        for word in words:
            test = line + ' ' + word if line else word
            if c.stringWidth(test, 'DejaVu', 8.5) < max_w:
                line = test
            else:
                c.drawString(x, y, line)
                y -= 13
                line = word
        if line:
            c.drawString(x, y, line)


class HorizontalBar(Flowable):
    def __init__(self, width, value, max_val, label, color=EMERALD):
        Flowable.__init__(self)
        self.width = width
        self.height = 28
        self.value = value
        self.max_val = max_val
        self.label = label
        self.color = color

    def draw(self):
        c = self.canv
        bar_y = 2
        bar_h = 14
        bar_w = self.width - 100
        c.setFillColor(TEXT_BODY)
        c.setFont('DejaVu', 8)
        c.drawString(0, bar_y + 3, self.label)
        bar_x = 90
        c.setFillColor(LIGHT_GRAY)
        c.roundRect(bar_x, bar_y, bar_w, bar_h, 3, fill=1, stroke=0)
        fill_w = bar_w * min(self.value / self.max_val, 1.0)
        c.setFillColor(self.color)
        c.roundRect(bar_x, bar_y, fill_w, bar_h, 3, fill=1, stroke=0)
        c.setFillColor(WHITE if fill_w > 40 else TEXT_BODY)
        c.setFont('DejaVu-Bold', 8)
        c.drawString(bar_x + fill_w + 5, bar_y + 3, str(self.value))


# ============================================================
# PAGE TEMPLATES
# ============================================================

def draw_page_footer(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setStrokeColor(LIGHT_GRAY)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(MARGIN, 28*mm, PAGE_W - MARGIN, 28*mm)
    canvas_obj.setFillColor(MID_GRAY)
    canvas_obj.setFont('DejaVu', 8)
    canvas_obj.drawCentredString(PAGE_W/2, 20*mm, f'\u2014 {doc.page} \u2014')
    canvas_obj.setFont('DejaVu', 7)
    canvas_obj.drawString(MARGIN, 20*mm, 'PROJECT VERDE')
    canvas_obj.drawRightString(PAGE_W - MARGIN, 20*mm, 'DAV ACON 5 \u2014 2026')
    canvas_obj.setStrokeColor(EMERALD)
    canvas_obj.setLineWidth(1.5)
    canvas_obj.line(MARGIN, PAGE_H - 10*mm, MARGIN + 35*mm, PAGE_H - 10*mm)
    canvas_obj.setStrokeColor(GOLD)
    canvas_obj.line(MARGIN + 36*mm, PAGE_H - 10*mm, MARGIN + 44*mm, PAGE_H - 10*mm)
    canvas_obj.restoreState()


def draw_cover_page(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    
    # Gradient at bottom
    for i in range(80):
        ratio = i / 80
        y = PAGE_H * ratio * 0.35
        h = PAGE_H * 0.004 + 1
        alpha = ratio * 0.5
        canvas_obj.setFillColor(Color(0, 0.66 * alpha, 0.42 * alpha, alpha))
        canvas_obj.rect(0, y, PAGE_W, h, fill=1, stroke=0)
    
    cover_path = os.path.join(IMG_DIR, 'cover_art.jpg')
    if os.path.exists(cover_path):
        canvas_obj.drawImage(cover_path, 0, PAGE_H * 0.32,
                           width=PAGE_W, height=PAGE_H * 0.48,
                           preserveAspectRatio=True, anchor='c', mask='auto')
    
    canvas_obj.setFillColor(Color(0.04, 0.09, 0.16, 0.5))
    canvas_obj.rect(0, PAGE_H * 0.32, PAGE_W, PAGE_H * 0.48, fill=1, stroke=0)
    
    # Gold line
    canvas_obj.setStrokeColor(GOLD)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(MARGIN, PAGE_H - 28*mm, MARGIN + 55*mm, PAGE_H - 28*mm)
    canvas_obj.setFillColor(GOLD)
    canvas_obj.circle(MARGIN + 58*mm, PAGE_H - 28*mm, 3, fill=1, stroke=0)
    
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont('DejaVu-Bold', 44)
    canvas_obj.drawString(MARGIN, PAGE_H - 72*mm, 'PROJECT')
    canvas_obj.setFillColor(EMERALD)
    canvas_obj.setFont('DejaVu-Bold', 54)
    canvas_obj.drawString(MARGIN, PAGE_H - 94*mm, 'VERDE')
    
    canvas_obj.setFillColor(GOLD_LIGHT)
    canvas_obj.setFont('DejaVu', 13)
    canvas_obj.drawString(MARGIN, PAGE_H - 112*mm, '"The plant that waters itself')
    canvas_obj.drawString(MARGIN, PAGE_H - 126*mm, '  \u2014 and talks to AI."')
    
    canvas_obj.setFillColor(Color(1, 1, 1, 0.08))
    canvas_obj.roundRect(MARGIN, 22*mm, CONTENT_W, 50*mm, 6, fill=1, stroke=0)
    
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont('DejaVu-Bold', 11)
    canvas_obj.drawString(MARGIN + 12*mm, 58*mm, 'Smart IoT Irrigation & Plant-Care System')
    canvas_obj.setFont('DejaVu', 9)
    canvas_obj.setFillColor(Color(1, 1, 1, 0.8))
    canvas_obj.drawString(MARGIN + 12*mm, 46*mm, 'DAV ACON 5 \u2014 Tech Exhibition 2026')
    canvas_obj.drawString(MARGIN + 12*mm, 34*mm, 'Aarav Choudhary & Anuj  |  Class X')
    
    canvas_obj.setFillColor(EMERALD)
    canvas_obj.roundRect(PAGE_W - MARGIN - 52*mm, 38*mm, 48*mm, 28*mm, 4, fill=1, stroke=0)
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont('DejaVu-Bold', 9)
    canvas_obj.drawCentredString(PAGE_W - MARGIN - 28*mm, 56*mm, 'BUILD COST')
    canvas_obj.setFont('DejaVu-Bold', 16)
    canvas_obj.drawCentredString(PAGE_W - MARGIN - 28*mm, 42*mm, '\u20B91,890')
    
    canvas_obj.setFillColor(GOLD)
    canvas_obj.roundRect(MARGIN, 78*mm, 48*mm, 11*mm, 3, fill=1, stroke=0)
    canvas_obj.setFillColor(NAVY)
    canvas_obj.setFont('DejaVu-Bold', 7.5)
    canvas_obj.drawCentredString(MARGIN + 24*mm, 82*mm, 'COMPLETE & DEMO-READY')
    
    canvas_obj.restoreState()


def draw_back_cover(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    
    back_path = os.path.join(IMG_DIR, 'back_cover.jpg')
    if os.path.exists(back_path):
        canvas_obj.drawImage(back_path, 0, 0,
                           width=PAGE_W, height=PAGE_H,
                           preserveAspectRatio=True, anchor='c', mask='auto')
    
    canvas_obj.setFillColor(Color(0.04, 0.09, 0.16, 0.7))
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    
    # Content centered
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont('DejaVu-Bold', 36)
    canvas_obj.drawCentredString(PAGE_W/2, PAGE_H/2 + 40*mm, 'PROJECT VERDE')
    
    canvas_obj.setFillColor(EMERALD)
    canvas_obj.setFont('DejaVu-Bold', 16)
    canvas_obj.drawCentredString(PAGE_W/2, PAGE_H/2 + 15*mm,
        '"The plant that waters itself \u2014 and talks to AI."')
    
    canvas_obj.setFillColor(Color(1, 1, 1, 0.7))
    canvas_obj.setFont('DejaVu', 11)
    canvas_obj.drawCentredString(PAGE_W/2, PAGE_H/2 - 10*mm,
        'Aarav Choudhary & Anuj')
    canvas_obj.drawCentredString(PAGE_W/2, PAGE_H/2 - 25*mm,
        'Class X | DAV ACON 5 | 2026')
    
    # Gold lines
    canvas_obj.setStrokeColor(GOLD)
    canvas_obj.setLineWidth(1.5)
    canvas_obj.line(PAGE_W/2 - 40*mm, PAGE_H/2 - 38*mm, PAGE_W/2 + 40*mm, PAGE_H/2 - 38*mm)
    canvas_obj.line(PAGE_W/2 - 40*mm, PAGE_H/2 + 52*mm, PAGE_W/2 + 40*mm, PAGE_H/2 + 52*mm)
    
    canvas_obj.setFont('DejaVu', 8)
    canvas_obj.setFillColor(Color(1, 1, 1, 0.4))
    canvas_obj.drawCentredString(PAGE_W/2, 25*mm,
        '\u20B91,890  |  5 Sensors  |  4 AI APIs  |  100% Student-Built')
    
    canvas_obj.restoreState()


# ============================================================
# STYLES
# ============================================================

def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('SectionTitle', parent=styles['Title'],
        fontName='DejaVu-Bold', fontSize=22, leading=28, textColor=NAVY, spaceAfter=5*mm, spaceBefore=3*mm))
    styles.add(ParagraphStyle('SubTitle', parent=styles['Title'],
        fontName='DejaVu-Bold', fontSize=15, leading=19, textColor=NAVY_LIGHT, spaceAfter=4*mm, spaceBefore=5*mm))
    styles.add(ParagraphStyle('BodyText2', parent=styles['Normal'],
        fontName='DejaVu', fontSize=10, leading=15, textColor=TEXT_BODY, spaceAfter=3*mm, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle('BulletItem', parent=styles['Normal'],
        fontName='DejaVu', fontSize=9.5, leading=14, textColor=TEXT_BODY, leftIndent=15, spaceAfter=2*mm))
    styles.add(ParagraphStyle('Caption', parent=styles['Normal'],
        fontName='DejaVu', fontSize=8, leading=11, textColor=MID_GRAY, alignment=TA_CENTER, spaceAfter=4*mm))
    styles.add(ParagraphStyle('PullQuote', parent=styles['Normal'],
        fontName='DejaVu-Bold', fontSize=14, leading=20, textColor=EMERALD, alignment=TA_CENTER, spaceAfter=5*mm, spaceBefore=5*mm, leftIndent=20, rightIndent=20))
    styles.add(ParagraphStyle('TOCEntry', parent=styles['Normal'],
        fontName='DejaVu', fontSize=11, leading=20, textColor=TEXT_DARK, leftIndent=10))
    styles.add(ParagraphStyle('SmallBold', parent=styles['Normal'],
        fontName='DejaVu-Bold', fontSize=9, leading=12, textColor=NAVY, spaceAfter=1*mm))
    styles.add(ParagraphStyle('TableCell', parent=styles['Normal'],
        fontName='DejaVu', fontSize=8.5, leading=12, textColor=TEXT_BODY))
    return styles


# ============================================================
# SECTION BUILDERS
# ============================================================

def build_toc(styles):
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('Contents', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 6*mm))
    
    toc_items = [
        ('01', 'The Whole Story in 60 Seconds'),
        ('02', 'The Problem \u2014 Why Plants Die'),
        ('03', 'Our Solution \u2014 Three-Tier Architecture'),
        ('04', 'Hardware \u2014 Sensors, Actuators & Power'),
        ('05', 'Firmware \u2014 The Brain & The Big Bug'),
        ('06', 'Cloud \u2014 Firebase Schema & Design'),
        ('07', 'The Web App \u2014 Dashboard, Controls & AI'),
        ('08', 'AI & APIs \u2014 Four Intelligence Layers'),
        ('09', 'Features \u2014 Every Live Capability'),
        ('10', 'Testing Journal \u2014 13-Point Matrix'),
        ('11', 'Real Bugs We Hit & Fixed'),
        ('12', 'Cost & Sustainability'),
        ('13', 'Future Scope'),
        ('14', 'Judge Tour Script'),
        ('15', 'Conclusion'),
    ]
    for num, title in toc_items:
        elements.append(Paragraph(
            f'<font color="{EMERALD}" size="14">{num}</font>'
            f'&nbsp;&nbsp;&nbsp;<font size="11">{title}</font>', styles['TOCEntry']))
    
    elements.append(Spacer(1, 12*mm))
    elements.append(Paragraph('<i>Every section can be read independently. Start anywhere.</i>', styles['Caption']))
    return elements


def build_executive_summary(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '01', 'THE WHOLE STORY IN 60 SECONDS', 'A one-minute overview of everything'))
    elements.append(Spacer(1, 6*mm))
    
    elements.append(Paragraph(
        'Project Verde is a smart irrigation system that costs \u20B91,890, uses 5 sensors and 2 microcontrollers, '
        'talks to 4 AI APIs, and <b>never lets your plants die again.</b>', styles['BodyText2']))
    
    elements.append(Spacer(1, 4*mm))
    
    kpi_data = [
        ('\u20B91,890', 'Total Build Cost', EMERALD),
        ('5', 'Sensors', NAVY_LIGHT),
        ('4', 'AI APIs', GOLD),
        ('94%', 'Diagnosis Accuracy', EMERALD_DARK),
    ]
    card_w = (CONTENT_W - 12) / 4
    kpi_table = [[KPICard(card_w, num, label, color) for num, label, color in kpi_data]]
    t = Table(kpi_table, colWidths=[card_w + 3]*4)
    t.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    elements.append(t)
    elements.append(Spacer(1, 5*mm))
    
    arch_path = os.path.join(IMG_DIR, 'architecture.jpg')
    if os.path.exists(arch_path):
        elements.append(Image(arch_path, width=CONTENT_W * 0.85, height=100))
        elements.append(Paragraph('Three-tier architecture: Edge \u2192 Cloud \u2192 Experience', styles['Caption']))
    
    elements.append(Spacer(1, 4*mm))
    
    for b in [
        '<b>Edge:</b> ESP32 reads soil moisture, temperature, humidity, light, and tank level every second. A pump and UV grow light respond automatically.',
        '<b>Cloud:</b> Firebase Realtime Database is the single source of truth. One bundled JSON write + one read per second.',
        '<b>Experience:</b> A single-file web app with live dashboard, weather integration, AI plant doctor, and smart chat assistants.',
        '<b>The Big Win:</b> We reduced 17 Firebase calls/second to 2 \u2014 eliminating watchdog reboots and making the pump run smoothly.',
    ]:
        elements.append(Paragraph(f'\u25cf {b}', styles['BulletItem']))
    
    elements.append(Spacer(1, 5*mm))
    
    # Sensor readings chart
    sensor_chart = os.path.join(IMG_DIR, 'chart_sensor_readings.png')
    if os.path.exists(sensor_chart):
        elements.append(Image(sensor_chart, width=CONTENT_W * 0.95, height=240))
        elements.append(Paragraph('Live sensor telemetry dashboard \u2014 last 20 readings per sensor', styles['Caption']))
    
    return elements


def build_problem_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '02', 'THE PROBLEM', 'Why plants die in urban homes'))
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'Urban families forget to water plants, or over-water them. Plants don\'t die from neglect \u2014 '
        'they die from a <b>lack of information</b>.', styles['BodyText2']))
    elements.append(Paragraph(
        'Nobody knows in real time how dry the soil is, whether the water tank is empty, '
        'or whether rain is coming. The feedback loop is broken.', styles['BodyText2']))
    
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph('The Market Gap', styles['SubTitle']))
    
    comp_data = [
        ['Feature', 'Commercial Kits\n(\u20B98,000+)', 'Project Verde\n(\u20B91,890)'],
        ['Soil Moisture', '\u2713', '\u2713'],
        ['Temperature & Humidity', '\u2713', '\u2713'],
        ['Water Tank Monitoring', '\u2717', '\u2713'],
        ['Camera / Visual Monitor', '\u2717', '\u2713 (ESP32-CAM)'],
        ['AI Plant Diagnosis', '\u2717', '\u2713 (94% accuracy)'],
        ['Weather Integration', '\u2717', '\u2713 (Rain override)'],
        ['Open Source / Hackable', '\u2717', '\u2713'],
        ['AI Chat Assistants', '\u2717', '\u2713 (4 APIs)'],
        ['Student-Buildable', '\u2717', '\u2713'],
    ]
    comp_table = Table(comp_data, colWidths=[CONTENT_W*0.4, CONTENT_W*0.3, CONTENT_W*0.3])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('BACKGROUND', (2,1), (2,-1), HexColor('#E8F8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, OFF_WHITE]),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(comp_table)
    
    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph('Cost Comparison', styles['SubTitle']))
    
    cost_chart = os.path.join(IMG_DIR, 'chart_cost_comparison.png')
    if os.path.exists(cost_chart):
        elements.append(Image(cost_chart, width=CONTENT_W * 0.95, height=220))
    
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph(
        'Commercial smart-garden kits cost \u20B98,000+, lack cameras, lack AI, and often can\'t be '
        'opened or understood by students. We built something better for less than a quarter of the price.',
        styles['BodyText2']))
    
    return elements


def build_solution_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '03', 'OUR SOLUTION', 'Three-tier IoT architecture'))
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'A three-tier IoT system where the plant "tells" us what it needs and the system acts automatically:',
        styles['BodyText2']))
    elements.append(Spacer(1, 3*mm))
    
    # Tier boxes
    tier_data = [[
        Paragraph('<font color="#FFFFFF"><b>EDGE TIER</b></font>', styles['TableCell']), '',
        Paragraph('<font color="#FFFFFF"><b>CLOUD TIER</b></font>', styles['TableCell']), '',
        Paragraph('<font color="#FFFFFF"><b>EXPERIENCE TIER</b></font>', styles['TableCell']),
    ]]
    tier_table = Table(tier_data, colWidths=[CONTENT_W*0.33, 3*mm, CONTENT_W*0.33, 3*mm, CONTENT_W*0.33 - 9*mm])
    tier_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), EMERALD_DARK), ('BACKGROUND', (2,0), (2,0), NAVY),
        ('BACKGROUND', (4,0), (4,0), NAVY_LIGHT), ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10), ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(tier_table)
    elements.append(Spacer(1, 2*mm))
    
    tier_details = [[
        Paragraph('<b>ESP32 WROOM-32</b><br/>Brain + 5 sensors<br/>Pump & UV-LED control', styles['TableCell']),
        '\u2192',
        Paragraph('<b>Firebase RTDB</b><br/>Single source of truth<br/>1s heartbeat JSON', styles['TableCell']),
        '\u2192',
        Paragraph('<b>Web App (HTML)</b><br/>Dashboard & controls<br/>AI assistants', styles['TableCell']),
    ]]
    detail_table = Table(tier_details, colWidths=[CONTENT_W*0.33, 3*mm, CONTENT_W*0.33, 3*mm, CONTENT_W*0.33 - 9*mm])
    detail_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 8), ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TEXTCOLOR', (1,0), (1,0), GOLD), ('TEXTCOLOR', (3,0), (3,0), GOLD),
        ('FONTSIZE', (1,0), (1,0), 16), ('FONTSIZE', (3,0), (3,0), 16),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(detail_table)
    elements.append(Spacer(1, 3*mm))
    
    cam_box = [
        [Paragraph('<font color="#FFFFFF"><b>CAM: ESP32-CAM (OV2640) \u2014 The Eyes</b></font>', styles['TableCell'])],
        [Paragraph('<font size="8">Captures SVGA photos on demand \u2192 uploads to cloud \u2192 app displays in \u22642 seconds</font>', styles['TableCell'])],
    ]
    cam_table = Table(cam_box, colWidths=[CONTENT_W])
    cam_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor('#2D5A3A')),
        ('BACKGROUND', (0,1), (0,1), HexColor('#E8F8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(cam_table)
    
    elements.append(Spacer(1, 5*mm))
    
    # Heartbeat chart
    hb_chart = os.path.join(IMG_DIR, 'chart_heartbeat.png')
    if os.path.exists(hb_chart):
        elements.append(Paragraph('The 1-Second Heartbeat', styles['SubTitle']))
        elements.append(Paragraph(
            'Every second, the ESP32 bundles 10 sensor readings into one JSON write and reads 9 control values.',
            styles['BodyText2']))
        elements.append(Image(hb_chart, width=CONTENT_W * 0.95, height=130))
    
    elements.append(Spacer(1, 4*mm))
    
    arch_path = os.path.join(IMG_DIR, 'architecture.jpg')
    if os.path.exists(arch_path):
        elements.append(Image(arch_path, width=CONTENT_W * 0.55, height=70))
        elements.append(Paragraph('System Architecture \u2014 Edge, Cloud, and Experience layers', styles['Caption']))
    
    return elements


def build_hardware_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '04', 'HARDWARE', 'Sensors, actuators & power design'))
    elements.append(Spacer(1, 5*mm))
    
    hw_path = os.path.join(IMG_DIR, 'hardware_bench.jpg')
    if os.path.exists(hw_path):
        elements.append(Image(hw_path, width=CONTENT_W * 0.85, height=120))
        elements.append(Paragraph('The Verde hardware bench \u2014 2 MCUs, 5 sensors, 2 actuators', styles['Caption']))
    
    elements.append(Spacer(1, 3*mm))
    
    # Circuit diagram
    circuit_path = os.path.join(IMG_DIR, 'circuit_diagram.jpg')
    if os.path.exists(circuit_path):
        elements.append(Paragraph('Circuit Wiring Diagram', styles['SubTitle']))
        elements.append(Image(circuit_path, width=CONTENT_W * 0.9, height=160))
        elements.append(Paragraph('Complete wiring schematic with all GPIO assignments', styles['Caption']))
    
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph('Bill of Materials', styles['SubTitle']))
    
    bom_data = [
        ['Module', 'ESP32 Pin', 'Role'],
        ['Soil Moisture (LM393)', 'AO\u2192GPIO34, VCC\u2192GPIO23', '% soil wetness (power-gated 15ms reads)'],
        ['DHT11', 'DATA\u2192GPIO4', 'Temperature + Humidity'],
        ['LDR Module', 'AO\u2192GPIO35', 'Ambient light \u2192 dark detection'],
        ['HC-SR04 Ultrasonic', 'TRIG\u2192GPIO18\nECHO\u2192GPIO19', 'Water tank level (5-point filter)'],
        ['2-Channel Relay', 'IN1\u2192GPIO5 (active-LOW)', 'Switches 5V water pump'],
        ['UV Grow LED', 'GPIO12 (active-HIGH, 220\u03A9)', 'Photosynthetic light'],
        ['ESP32-CAM (OV2640)', 'Own board + MB programmer', 'SVGA photos \u2192 cloud'],
    ]
    bom_table = Table(bom_data, colWidths=[CONTENT_W*0.28, CONTENT_W*0.32, CONTENT_W*0.4])
    bom_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'), ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'), ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, OFF_WHITE]),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(bom_table)
    
    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph('Power Design \u2014 Hard-Won Lessons', styles['SubTitle']))
    
    for b in [
        '<b>Main supply: 5V / 2A phone adapter</b> \u2014 NOT a USB-PD laptop charger. PD requires a handshake chip the ESP32 lacks.',
        '<b>1000 \u00B5F electrolytic capacitor</b> across 5V/GND \u2014 absorbs pump + WiFi current spikes.',
        '<b>1N4007 flyback diode</b> across the pump \u2014 kills inductive spikes that would reset the ESP32.',
        '<b>Pump electrically isolated</b> via relay COM/NO on its own 5V source \u2014 prevents noise coupling.',
    ]:
        elements.append(Paragraph(f'\u25cf {b}', styles['BulletItem']))
    
    elements.append(Spacer(1, 3*mm))
    elements.append(CalloutBox(CONTENT_W,
        'THE USB-PD TRAP: A 67W USB-PD charger will NOT power the ESP32. PD requires a negotiation handshake chip '
        'the ESP32 lacks \u2014 the charger defaults to 0mA output. Use a simple 5V/2A phone adapter instead.',
        'warning'))
    
    return elements


def build_firmware_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '05', 'FIRMWARE', 'The brain & the big bug story'))
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph('<b>Code_1_Main_Brain.ino \u2014 V3.0.7-FINAL</b>', styles['SmallBold']))
    elements.append(Spacer(1, 2*mm))
    
    for f in [
        'Non-blocking <b>millis()</b> task scheduler: sensors 1Hz \u00B7 cloud 1s \u00B7 WiFi 10s \u00B7 logs 60s',
        'Hardware watchdog (8s) fed every loop \u2014 if the system hangs, it reboots itself',
        '<b>AUTO logic:</b> pump_ON = moisture &lt; threshold AND tank safe AND no rain',
        '<b>Manual logic:</b> user-driven from app, still tank-protected',
        'Adjustable thresholds from app: moisture (35%), tank (15%), light (35%) \u2014 persisted in NVS flash',
        '<b>10-point moving averages</b> for soil/LDR sensors',
        '<b>5-point moving average + invalid-read rejection</b> for the tank',
        '<b>\u00B12% hysteresis</b> on light auto-switch \u2014 no LED flicker',
        '3-network WiFi fallback: home \u2192 hotspot \u2192 school',
    ]:
        elements.append(Paragraph(f'\u25cf {f}', styles['BulletItem']))
    
    elements.append(Spacer(1, 4*mm))
    
    # BEFORE/AFTER infographic
    ba_path = os.path.join(IMG_DIR, 'before_after.jpg')
    if os.path.exists(ba_path):
        elements.append(Paragraph('The Big Bug Story', styles['SubTitle']))
        elements.append(Image(ba_path, width=CONTENT_W * 0.8, height=140))
        elements.append(Paragraph('The impact of JSON bundling: 17 individual calls reduced to 2 bundled calls per second', styles['Caption']))
    
    elements.append(Spacer(1, 4*mm))
    
    # Before/After table
    bug_data = [
        [Paragraph('<font color="#E53E3E"><b>BEFORE \u2014 The Problem</b></font>', styles['TableCell']),
         Paragraph('<font color="#00A86B"><b>AFTER \u2014 The Fix</b></font>', styles['TableCell'])],
        [Paragraph('17 Firebase HTTPS calls per second', styles['TableCell']),
         Paragraph('2 calls per second (1 write + 1 read)', styles['TableCell'])],
        [Paragraph('Network stall \u2192 8s watchdog reboot', styles['TableCell']),
         Paragraph('Zero reboots, stable connection', styles['TableCell'])],
        [Paragraph('Pump clicked ON/OFF every ~10s', styles['TableCell']),
         Paragraph('Pump stays ON continuously until threshold', styles['TableCell'])],
    ]
    bug_table = Table(bug_data, colWidths=[CONTENT_W*0.5, CONTENT_W*0.5])
    bug_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor('#FEE2E2')),
        ('BACKGROUND', (1,0), (1,0), HexColor('#D1FAE5')),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    elements.append(bug_table)
    
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph(
        '<font color="#00A86B" size="28"><b>17 calls/s</b></font>'
        '<font color="#D4AF37" size="18">  \u279C  </font>'
        '<font color="#00A86B" size="28"><b>2 calls/s</b></font>'
        '<font color="#8899AA" size="12">  (\u224885% reduction)</font>',
        ParagraphStyle('hero', parent=styles['BodyText2'], alignment=TA_CENTER, spaceBefore=2*mm, spaceAfter=2*mm)))
    
    elements.append(Spacer(1, 4*mm))
    
    # Moisture cycle chart
    mc_path = os.path.join(IMG_DIR, 'chart_moisture_cycle.png')
    if os.path.exists(mc_path):
        elements.append(Paragraph('Moisture Watering Cycle', styles['SubTitle']))
        elements.append(Paragraph(
            'The chart below shows how AUTO mode works: when moisture drops below 35%, the pump activates '
            'and runs until the threshold is reached, then stops. The 5-point tank filter ensures pump-splash '
            'garbage can\'t fake an empty tank reading.',
            styles['BodyText2']))
        elements.append(Image(mc_path, width=CONTENT_W * 0.95, height=200))
        elements.append(Paragraph('AUTO-mode watering cycle with threshold markers and pump-active regions', styles['Caption']))
    
    elements.append(Spacer(1, 4*mm))
    
    # Flowchart
    flow_path = os.path.join(IMG_DIR, 'flowchart.jpg')
    if os.path.exists(flow_path):
        elements.append(Paragraph('AUTO-Mode Decision Flowchart', styles['SubTitle']))
        elements.append(Image(flow_path, width=CONTENT_W * 0.7, height=160))
        elements.append(Paragraph('Decision logic: moisture check \u2192 tank check \u2192 rain check \u2192 pump action', styles['Caption']))
    
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph('ESP32-CAM Firmware \u2014 V3.0.4-FINAL', styles['SubTitle']))
    
    for f in [
        'Polls <b>/controls/capture_photo</b> every 1.5s \u2192 on trigger: flash LED \u2192 capture SVGA JPEG',
        'POSTs raw bytes to Vercel upload API \u2192 lands in /latest_scan (base64) \u2192 app shows it \u22642s',
        '<b>8 MHz XCLK</b> \u2014 fixes RF interference with WiFi antenna (was 20 MHz)',
        '<b>Sequential boot:</b> camera first, WiFi after 500ms \u2014 prevents brownout',
        '<b>esp_camera_fb_return()</b> called immediately \u2014 prevents heap fragmentation',
    ]:
        elements.append(Paragraph(f'\u25cf {f}', styles['BulletItem']))
    
    return elements


def build_cloud_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '06', 'CLOUD', 'Firebase schema & design'))
    elements.append(Spacer(1, 5*mm))
    
    fb_path = os.path.join(IMG_DIR, 'firebase_schema.jpg')
    if os.path.exists(fb_path):
        elements.append(Image(fb_path, width=CONTENT_W * 0.6, height=100))
        elements.append(Paragraph('Firebase Realtime Database \u2014 verde-tech-haha', styles['Caption']))
    
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph('Database Schema Tree', styles['SubTitle']))
    
    schema_data = [
        ['Path', 'Fields', 'Purpose'],
        ['/sensors/', 'moisture, temperature, humidity, light,\ntank_level, lux, watchdog_status,\nvoltage_sag, uploads (success/fail)', 'All telemetry\n(10 metrics)'],
        ['/controls/', 'manual_mode, pump_state, light_manual_mode,\ngrow_light_state, capture_photo,\nthresholds, weather_override', 'App\u2192ESP32\ncommands (9 keys)'],
        ['/latest_scan/', 'imageUrl (base64), status, captured_at,\nscientificName, diseaseName,\nprobability, treatmentPlan', 'Camera + AI\nanalysis data'],
        ['/weather/', 'city, temp, condition, description,\nhumidity, wind_speed, rain_expected', 'OpenWeatherMap\ncached data'],
        ['/historical_logs/', 'moisture_log [{time, moisture}]', 'Chart data\nfor dashboard'],
        ['/actuators/', 'pump_actual, grow_light_actual, mode', 'Actual state\nconfirmation'],
    ]
    schema_table = Table(schema_data, colWidths=[CONTENT_W*0.22, CONTENT_W*0.45, CONTENT_W*0.33])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'), ('FONTSIZE', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'), ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, OFF_WHITE]),
        ('FONTNAME', (0,1), (0,-1), 'Courier'), ('TEXTCOLOR', (0,1), (0,-1), EMERALD_DARK),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(schema_table)
    
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph(
        '<b>Security Rules:</b> Public read access. Validated writes (booleans and numbers 0\u2013100). '
        'ESP32 authenticates using a legacy database secret.', styles['BodyText2']))
    return elements


def build_app_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '07', 'THE WEB APP', 'Dashboard, controls & AI interfaces'))
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'A single-file HTML application that serves as the "face" of Project Verde. Four pages via burger menu:',
        styles['BodyText2']))
    elements.append(Spacer(1, 3*mm))
    
    pages = [
        ('1', 'DASHBOARD', EMERALD, [
            '8 live telemetry tiles with sparklines + hover graphs',
            'All 8 controls (pump, light, camera, modes)',
            '3 threshold sliders (moisture, tank, light)',
            'Predicted actuator states',
            'Moisture history chart + system status strip + uptime timer',
            'Fullscreen demo mode + toast notifications',
        ]),
        ('2', 'WEATHER', NAVY_LIGHT, [
            'Live Delhi weather from OpenWeatherMap',
            '5-day forecast chips',
            'Auto rain-override (checks every 3 min) with countdown',
            'If rain expected \u2192 weather_override = 1 \u2192 pump disabled',
        ]),
        ('3', 'PLANT DOCTOR', GOLD, [
            'Live CAM photo frame (auto-updates \u22642s)',
            'CAPTURE button triggers ESP32-CAM',
            'Upload-or-CAM modal for diagnosis',
            'crop.health analysis: species + disease + treatment',
            'AI chat that sees the same image',
        ]),
        ('4', 'AI ASSISTANTS', HexColor('#6B46C1'), [
            'Gemini 2.5 Flash image chat',
            'OpenRouter sensor-aware chat',
            'Quick prompt buttons for common questions',
            'Fallback chains (435 models, never dead-end)',
        ]),
    ]
    
    for num, title, color, features in pages:
        ph = [[Paragraph(f'<font color="#FFFFFF"><b>  {num}. {title}</b></font>', styles['TableCell'])]]
        ph_table = Table(ph, colWidths=[CONTENT_W])
        ph_table.setStyle(TableStyle([('BACKGROUND', (0,0), (0,0), color),
            ('TOPPADDING', (0,0), (0,0), 6), ('BOTTOMPADDING', (0,0), (0,0), 6)]))
        elements.append(ph_table)
        for f in features:
            elements.append(Paragraph(f'  \u25cf {f}', ParagraphStyle('sb', parent=styles['BulletItem'], fontSize=8.5, leftIndent=12)))
        elements.append(Spacer(1, 2*mm))
    
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph('Additional App Features', styles['SubTitle']))
    for e in [
        '<b>Tank Calibration Panel:</b> SET EMPTY / SET FULL \u2014 app-side remap, no reflashing',
        '<b>Image Flip Fix:</b> ESP32-CAM mounts upside-down \u2014 CSS transform corrects orientation',
        '<b>Last-10 Trend Indicators:</b> Each tile shows \u25B2/\u25BC with percentage change',
    ]:
        elements.append(Paragraph(f'\u25cf {e}', styles['BulletItem']))
    return elements


def build_ai_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '08', 'AI & APIs', 'Four intelligence layers'))
    elements.append(Spacer(1, 5*mm))
    
    ai_path = os.path.join(IMG_DIR, 'ai_chat.jpg')
    if os.path.exists(ai_path):
        elements.append(Image(ai_path, width=CONTENT_W * 0.7, height=100))
        elements.append(Paragraph('AI-powered plant analysis and intelligent chat assistants', styles['Caption']))
    
    elements.append(Spacer(1, 3*mm))
    
    api_data = [
        ['API', 'Purpose', 'Auth Method', 'Key Mechanic', 'Accuracy'],
        ['OpenWeatherMap', 'Live weather +\n5-day forecast\n\u2192 rain override', 'Key in URL',
         'GET /data/2.5/weather\nids 2xx/3xx/5xx/6xx\n\u2192 rain \u2192 override=1',
         'Live-tested:\nDelhi 35\u00B0C\ncorrect city ID'],
        ['crop.health\n(Plant.id)', 'Plant + disease\nidentification', 'Api-Key header',
         'POST /api/v1/identification\nwith base64 image\n\u2192 crop + disease suggestions',
         '94% accuracy\non test image:\nnutrient deficiency'],
        ['Google Gemini\n2.5 Flash', 'Vision chat on\nanalysed photo', 'X-goog-api-key\nheader (AQ keys)',
         'POST /v1beta/models/\ngemini-flash-latest:\ngenerateContent',
         'Vision + text\nwith diagnosis\n+ telemetry context'],
        ['OpenRouter', 'Sensor chat +\nvision fallback', 'Bearer\nsk-or-v1-\u2026',
         'POST /api/v1/chat/\ncompletions\n(OpenAI-compatible)',
         '435 models\n8-model text chain\n5-model vision chain'],
    ]
    api_table = Table(api_data, colWidths=[CONTENT_W*0.17, CONTENT_W*0.2, CONTENT_W*0.15, CONTENT_W*0.28, CONTENT_W*0.2])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'), ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'), ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, OFF_WHITE]),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(api_table)
    
    elements.append(Spacer(1, 4*mm))
    elements.append(CalloutBox(CONTENT_W,
        'Note: Gemini 2.5 Flash is no longer offered to new users. We use gemini-flash-latest instead. '
        'AQ keys require the X-goog-api-key header format \u2014 standard Bearer tokens do not work.', 'info'))
    
    elements.append(Spacer(1, 4*mm))
    
    # API performance chart
    api_chart = os.path.join(IMG_DIR, 'chart_api_performance.png')
    if os.path.exists(api_chart):
        elements.append(Paragraph('API Performance Comparison', styles['SubTitle']))
        elements.append(Image(api_chart, width=CONTENT_W * 0.9, height=180))
    
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph('OpenRouter Fallback Architecture', styles['SubTitle']))
    elements.append(Paragraph(
        'The system uses intelligent fallback chains to ensure AI responses never fail:',
        styles['BodyText2']))
    
    chain_data = [
        ['Text Chain (8 models)', 'Vision Chain (5 models)'],
        ['Primary \u2192 Secondary \u2192 Tertiary \u2192\nQuaternary \u2192 Quinary \u2192 Senary \u2192\nSeptenary \u2192 Fallback',
         'Primary Vision \u2192 Secondary Vision \u2192\nTertiary Vision \u2192 Quaternary Vision \u2192\nText Fallback (sends image description)'],
    ]
    chain_table = Table(chain_data, colWidths=[CONTENT_W*0.5, CONTENT_W*0.5])
    chain_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), EMERALD), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'), ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(chain_table)
    return elements


def build_features_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '09', 'FEATURES', 'Every live capability'))
    elements.append(Spacer(1, 5*mm))
    
    features = [
        ('Auto Irrigation', 'Pump activates when soil moisture drops below 35%, with tank-level and rain protection'),
        ('Tank Monitoring', 'Ultrasonic sensor measures water level with 5-point filtering. Calibratable from app'),
        ('Climate Sensing', 'DHT11 provides temperature and humidity. 10-point moving average for smooth readings'),
        ('Light Management', 'LDR detects ambient light. UV grow LED auto-activates in darkness with \u00B12% hysteresis'),
        ('Live Camera', 'ESP32-CAM captures photos on demand. Image appears in app within 2 seconds'),
        ('Plant Doctor', 'AI-powered diagnosis: species ID + disease detection + treatment plan. 94% accuracy'),
        ('Weather Intelligence', 'Real-time Delhi weather + 5-day forecast. Auto rain-override prevents over-watering'),
        ('AI Chat (Gemini)', 'Vision-enabled chat that sees the plant photo, knows the diagnosis, and answers questions'),
        ('AI Chat (OpenRouter)', 'Sensor-aware chat with full telemetry context. 435 models, never dead-ends'),
        ('Live Dashboard', '8 telemetry tiles with sparklines, trend indicators, and last-10 data points'),
        ('Full Control', 'Manual/Auto mode toggle, threshold sliders, pump/light controls \u2014 all from the app'),
        ('Watchdog Recovery', 'Hardware watchdog (8s) automatically reboots if firmware hangs'),
        ('WiFi Resilience', '3-network fallback: home \u2192 hotspot \u2192 school. Always connected'),
        ('Data Persistence', 'Thresholds stored in NVS flash. Survives power cycles without reconfiguration'),
    ]
    for title, desc in features:
        elements.append(Paragraph(f'<b>{title}</b> \u2014 {desc}', styles['BulletItem']))
    return elements


def build_testing_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '10', 'TESTING JOURNAL', '13-point verification matrix'))
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'Every subsystem was independently tested and verified. Here is the complete test matrix:',
        styles['BodyText2']))
    
    elements.append(Spacer(1, 3*mm))
    
    # Test results chart
    tr_chart = os.path.join(IMG_DIR, 'chart_test_results.png')
    if os.path.exists(tr_chart):
        elements.append(Image(tr_chart, width=CONTENT_W * 0.9, height=170))
        elements.append(Paragraph('Test pass rate and category breakdown', styles['Caption']))
    
    elements.append(Spacer(1, 4*mm))
    
    test_data = [
        ['#', 'Test', 'Method', 'Result'],
        ['1', 'WiFi / Boot', 'Power cycle \u2192 auto-connect within 3s', '\u2713 PASS'],
        ['2', 'DHT11 Breathe', 'Blow warm air \u2192 temp rises within 2s', '\u2713 PASS'],
        ['3', 'Moisture Water-Dunk', 'Probe in water \u2192 95%+; Probe dry \u2192 &lt;5%', '\u2713 PASS'],
        ['4', 'LDR Cover Test', 'Hand over sensor \u2192 "Dark" triggers LED', '\u2713 PASS'],
        ['5', 'Ultrasonic Hand', 'Hand at known distance \u2192 accurate \u00B11cm', '\u2713 PASS'],
        ['6', 'Pump AUTO 120s', 'Dry soil \u2192 pump runs continuously 120s', '\u2713 PASS'],
        ['7', 'Threshold OFF', 'Moisture reaches 35% \u2192 pump stops exactly', '\u2713 PASS'],
        ['8', 'Tank Lock', 'Empty tank \u2192 pump blocked even if soil is dry', '\u2713 PASS'],
        ['9', 'Rain Override', 'Weather API says rain \u2192 pump disabled', '\u2713 PASS'],
        ['10', 'CAM Capture \u22642s', 'Trigger \u2192 photo in app within 2 seconds', '\u2713 PASS'],
        ['11', 'Plant Doctor 94%', 'Test leaf image \u2192 nutrient deficiency @94%', '\u2713 PASS'],
        ['12', 'AI Chats + Fallbacks', 'All 4 APIs respond correctly', '\u2713 PASS'],
        ['13', 'Watchdog 10+ min', 'System runs 10+ minutes with 0 reboots', '\u2713 PASS'],
    ]
    test_table = Table(test_data, colWidths=[CONTENT_W*0.06, CONTENT_W*0.22, CONTENT_W*0.45, CONTENT_W*0.27])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'), ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (0,-1), 'CENTER'), ('ALIGN', (3,1), (3,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, OFF_WHITE]),
        ('TEXTCOLOR', (3,1), (3,-1), SUCCESS_GREEN), ('FONTNAME', (3,1), (3,-1), 'DejaVu-Bold'),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(test_table)
    
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph(
        '<font color="#00A86B" size="24"><b>13 / 13</b></font> <font size="12">tests passed \u2014 zero failures</font>',
        ParagraphStyle('hero_test', parent=styles['BodyText2'], alignment=TA_CENTER, spaceBefore=3*mm, spaceAfter=3*mm)))
    return elements


def build_bugs_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '11', 'REAL BUGS', 'Engineering challenges we hit & fixed'))
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'Honesty builds credibility. Here are the real engineering challenges we encountered and solved:',
        styles['BodyText2']))
    elements.append(Spacer(1, 3*mm))
    
    bugs = [
        ('1', 'AUTO 10s pump loop', '17 Firebase calls/s caused network stall \u2192 watchdog reboot loop',
         'JSON bundling: 1 write + 1 read per second (2 calls/s total)'),
        ('2', 'Camera probe 0x106', 'FPC ribbon cable unseated', 'Reseat gold-side down + power cycle'),
        ('3', 'PSRAM not found', 'Weak power supply', 'Switched to 5V/2A adapter'),
        ('4', '0x20002 boot crash', 'Camera + WiFi simultaneous power surge', 'Sequential boot: camera first, WiFi after 500ms'),
        ('5', 'RF interference', '20 MHz XCLK caused WiFi noise', 'Throttled XCLK to 8 MHz'),
        ('6', '67W charger starved board', 'USB-PD negotiation fails without handshake chip', 'Use simple 5V/2A phone adapter'),
        ('7', 'Relay dead', 'Split breadboard power rails', 'Bridge + to +, \u2212 to \u2212 across split'),
        ('8', 'Temperature = 0', 'DHT11 on wrong pin', 'Move to GPIO4 + shared GND'),
        ('9', 'Firebase "spurts"', '13 individual calls/s blocking the loop', 'One bundled call with all sensor data'),
        ('10', 'Compile error', 'Copy-paste corruption in source', 'Re-download file cleanly'),
    ]
    for num, title, cause, fix in bugs:
        bug_data = [
            [Paragraph(f'<font color="#D4AF37"><b>Bug #{num}</b></font>', styles['TableCell']),
             Paragraph(f'<b>{title}</b>', styles['TableCell'])],
            [Paragraph(f'<font color="#E53E3E">Cause: {cause}</font>', styles['TableCell']),
             Paragraph(f'<font color="#00A86B">Fix: {fix}</font>', styles['TableCell'])],
        ]
        bug_table = Table(bug_data, colWidths=[CONTENT_W*0.35, CONTENT_W*0.65])
        bug_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), HexColor('#F8FAFE')),
            ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('FONTSIZE', (0,0), (-1,-1), 8),
        ]))
        elements.append(bug_table)
        elements.append(Spacer(1, 1.5*mm))
    return elements


def build_cost_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '12', 'COST & SUSTAINABILITY', 'Every rupee accounted for'))
    elements.append(Spacer(1, 5*mm))
    
    # Cost breakdown pie chart
    cb_path = os.path.join(IMG_DIR, 'chart_cost_breakdown.png')
    if os.path.exists(cb_path):
        elements.append(Image(cb_path, width=CONTENT_W * 0.7, height=160))
    
    elements.append(Spacer(1, 4*mm))
    
    cost_data = [
        ['Category', 'Items', 'Cost (\u20B9)'],
        ['Electronics', 'ESP32, ESP32-CAM, 5 sensors,\nrelay, pump, UV LED', '1,320'],
        ['Power & Protection', '5V/2A adapter, 1000\u00B5F cap,\n1N4007 diode', '220'],
        ['Mechanical', 'Breadboard, jumper wires,\nenclosure', '350'],
        ['Software & APIs', 'All on free tiers\n(Firebase, OWM, Gemini, OpenRouter)', '0'],
        ['', '', ''],
        ['', 'TOTAL', '\u20B91,890'],
    ]
    cost_table = Table(cost_data, colWidths=[CONTENT_W*0.3, CONTENT_W*0.45, CONTENT_W*0.25])
    cost_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'), ('FONTNAME', (1,6), (-1,6), 'DejaVu-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9), ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('GRID', (0,0), (-1,4), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,4), [WHITE, OFF_WHITE]),
        ('LINEABOVE', (0,6), (-1,6), 1.5, EMERALD),
        ('BACKGROUND', (0,6), (-1,6), HexColor('#E8F8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(cost_table)
    
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph(
        '<font color="#00A86B" size="20"><b>\u20B91,890</b></font>'
        '<font size="10"> \u2248 $23 USD \u2014 all software and APIs on free tiers</font>',
        ParagraphStyle('cost_hero', parent=styles['BodyText2'], alignment=TA_CENTER, spaceBefore=3*mm, spaceAfter=3*mm)))
    
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph('Sustainability Notes', styles['SubTitle']))
    for b in [
        'Low power draw: 5V/2A = 10W max, typically 3\u20135W during operation',
        'All software on free tiers \u2014 zero recurring cost',
        'Components are standard, replaceable, non-proprietary',
        'Future: solar autonomy planned (12V panel + charge controller + battery)',
        'Water-efficient: only irrigates when needed, respects rain forecasts',
    ]:
        elements.append(Paragraph(f'\u25cf {b}', styles['BulletItem']))
    return elements


def build_future_section(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '13', 'FUTURE SCOPE', 'Where we go next'))
    elements.append(Spacer(1, 5*mm))
    
    future_items = [
        ('Solar Autonomy', '12V solar panel + charge controller + LiPo battery for completely off-grid operation'),
        ('NPK Soil Probe', 'Measure nitrogen, phosphorus, potassium levels for precision fertilization'),
        ('Multi-Plant Zones', 'Multiple soil probes + valve manifold for different plant types'),
        ('Telegram / WhatsApp Alerts', 'Push notifications for critical events: tank empty, disease detected, extreme weather'),
        ('Predictive Watering', 'Use historical moisture logs + weather forecast to predict optimal watering schedule'),
        ('Deployed Dashboard', 'Next.js scaffold already built \u2014 ready for production deployment'),
    ]
    for title, desc in future_items:
        elements.append(Paragraph(f'<b>{title}</b>', ParagraphStyle('ft', parent=styles['SmallBold'], fontSize=11, spaceBefore=3*mm)))
        elements.append(Paragraph(f'    {desc}', styles['BulletItem']))
    
    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph('Roadmap', styles['SmallBold']))
    
    roadmap_data = [
        ['NOW', 'NEXT', 'LATER'],
        ['Single plant\nFull automation\n4 AI APIs',
         'Multi-zone\nSolar power\nPush alerts',
         'NPK probe\nPredictive model\nProduction dashboard'],
    ]
    rm_table = Table(roadmap_data, colWidths=[CONTENT_W/3]*3)
    rm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), EMERALD), ('BACKGROUND', (1,0), (1,0), NAVY_LIGHT),
        ('BACKGROUND', (2,0), (2,0), GOLD), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'), ('FONTSIZE', (0,0), (-1,0), 11),
        ('FONTSIZE', (0,1), (-1,1), 8), ('TEXTCOLOR', (0,1), (-1,1), TEXT_BODY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
    ]))
    elements.append(rm_table)
    return elements


def build_judge_tour(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '14', 'JUDGE TOUR SCRIPT', '3-minute guided presentation'))
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph('<i>A 3-minute guided tour script for presenting to judges:</i>', styles['Caption']))
    
    tour_steps = [
        ('0:00\u20130:30', 'The Hook',
         '"This is Project Verde. It costs \u20B91,890, uses 5 sensors, talks to 4 AIs, and this plant has been watering itself for the last 10 minutes without any human intervention."'),
        ('0:30\u20131:00', 'The Architecture',
         '"Three tiers: the ESP32 is the brain reading soil, temperature, humidity, light, and tank level. Firebase is the cloud brain. This web app is the face. And the ESP32-CAM is the eyes."'),
        ('1:00\u20131:30', 'The Demo',
         '"Watch the dashboard \u2014 moisture is at 28%, below our 35% threshold. The tank has water. No rain is expected. The pump just turned on automatically. See the tile turning green."'),
        ('1:30\u20132:00', 'The Big Bug',
         '"We hit a critical bug: the pump was clicking on and off every 10 seconds. Root cause: 17 Firebase calls per second. Fix: JSON bundling \u2014 2 calls per second. The pump now runs smoothly until the soil is moist enough."'),
        ('2:00\u20132:30', 'The AI',
         '"Let me show you the Plant Doctor. I capture a photo of this leaf, and the AI identifies it as a nutrient deficiency with 94% confidence and suggests a treatment plan. Gemini can also look at the image and answer questions about it."'),
        ('2:30\u20133:00', 'The Close',
         '"\u20B91,890. All free APIs. Built by two Class X students. This is what happens when you give a plant a voice."'),
    ]
    for time, title, script in tour_steps:
        step_data = [[
            Paragraph(f'<font color="#D4AF37"><b>{time}</b></font>', styles['TableCell']),
            Paragraph(f'<b>{title}</b>', styles['TableCell']),
            Paragraph(f'<i>{script}</i>', styles['TableCell']),
        ]]
        step_table = Table(step_data, colWidths=[CONTENT_W*0.12, CONTENT_W*0.15, CONTENT_W*0.73])
        step_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), HexColor('#FFFBF0')),
            ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ]))
        elements.append(step_table)
        elements.append(Spacer(1, 2*mm))
    return elements


def build_conclusion(styles):
    elements = []
    elements.append(SectionHeader(CONTENT_W, '15', 'CONCLUSION', 'What we proved'))
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'Project Verde proves that smart, AI-powered technology doesn\'t have to be expensive '
        'or complicated. With \u20B91,890 worth of components, free APIs, and honest engineering, '
        'we built a system that:', styles['BodyText2']))
    
    for p in [
        'Waters plants automatically \u2014 no human intervention needed',
        'Monitors 5 environmental parameters in real time',
        'Takes photos and diagnoses plant diseases with 94% accuracy',
        'Checks the weather and adjusts behavior accordingly',
        'Provides 4 AI-powered assistance tools',
        'Runs reliably with hardware watchdog protection',
        'Is fully open, hackable, and student-buildable',
    ]:
        elements.append(Paragraph(f'\u25cf {p}', styles['BulletItem']))
    
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph(
        'We encountered 10 real bugs and fixed every one of them. We learned that USB-PD chargers '
        'don\'t work without a negotiation chip, that camera ribbons need to be reseated firmly, '
        'and that 17 Firebase calls per second will bring your system to its knees.',
        styles['BodyText2']))
    
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph(
        'Every number in this document is real. Every test was actually run. '
        'Every bug was actually hit. We didn\'t simplify for the presentation \u2014 '
        'this is exactly what we built.', styles['BodyText2']))
    
    elements.append(Spacer(1, 6*mm))
    elements.append(Paragraph(
        '"The plant that waters itself \u2014 and talks to AI."', styles['PullQuote']))
    
    elements.append(Spacer(1, 5*mm))
    
    credit_data = [
        [Paragraph('<b>PROJECT VERDE</b>', ParagraphStyle('ct', parent=styles['TableCell'], fontSize=13, textColor=NAVY, alignment=TA_CENTER))],
        [Paragraph('Aarav Choudhary & Anuj \u2014 Class X', ParagraphStyle('cn', parent=styles['TableCell'], alignment=TA_CENTER))],
        [Paragraph('DAV ACON 5 \u2014 Tech Exhibition 2026', ParagraphStyle('ce', parent=styles['TableCell'], alignment=TA_CENTER))],
        [Paragraph('Build cost: \u20B91,890 | All software free tiers | 100% student-built', ParagraphStyle('cd', parent=styles['TableCell'], alignment=TA_CENTER, fontSize=8, textColor=MID_GRAY))],
    ]
    credit_table = Table(credit_data, colWidths=[CONTENT_W * 0.7])
    credit_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LINEABOVE', (0,0), (0,0), 2, EMERALD),
        ('LINEBELOW', (0,-1), (0,-1), 2, EMERALD),
    ]))
    outer = Table([[credit_table]], colWidths=[CONTENT_W])
    outer.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER')]))
    elements.append(outer)
    return elements


# ============================================================
# DOCUMENT ASSEMBLY
# ============================================================

def build_document():
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'Project_Verde_Nuclear.pdf')
    styles = get_styles()
    
    doc = BaseDocTemplate(output_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN, topMargin=15*mm, bottomMargin=32*mm,
        title='Project Verde \u2014 Definitive Documentation',
        author='Aarav Choudhary & Anuj', subject='DAV ACON 5 Tech Exhibition 2026')
    
    content_frame = Frame(MARGIN, 32*mm, CONTENT_W, PAGE_H - 47*mm, id='content')
    
    cover_template = PageTemplate(id='cover',
        frames=[Frame(0, 0, PAGE_W, PAGE_H, id='cover_frame', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
        onPage=draw_cover_page)
    
    content_template = PageTemplate(id='content', frames=[content_frame], onPage=draw_page_footer)
    
    back_template = PageTemplate(id='back',
        frames=[Frame(0, 0, PAGE_W, PAGE_H, id='back_frame', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
        onPage=draw_back_cover)
    
    doc.addPageTemplates([cover_template, content_template, back_template])
    
    elements = []
    elements.append(NextPageTemplate('content'))
    elements.append(PageBreak())
    
    elements.extend(build_toc(styles))
    elements.append(PageBreak())
    
    elements.extend(build_executive_summary(styles))
    elements.append(Spacer(1, 8*mm))
    elements.extend(build_problem_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_solution_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_hardware_section(styles))
    elements.append(Spacer(1, 5*mm))
    elements.extend(build_firmware_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_cloud_section(styles))
    elements.append(Spacer(1, 5*mm))
    elements.extend(build_app_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_ai_section(styles))
    elements.append(Spacer(1, 5*mm))
    elements.extend(build_features_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_testing_section(styles))
    elements.append(Spacer(1, 5*mm))
    elements.extend(build_bugs_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_cost_section(styles))
    elements.append(Spacer(1, 5*mm))
    elements.extend(build_future_section(styles))
    elements.append(Spacer(1, 6*mm))
    elements.extend(build_judge_tour(styles))
    elements.append(PageBreak())
    
    elements.extend(build_conclusion(styles))
    elements.append(NextPageTemplate('back'))
    elements.append(PageBreak())
    
    doc.build(elements)
    print(f'\u2705 Nuclear PDF generated: {output_path}')
    return output_path


if __name__ == '__main__':
    build_document()
