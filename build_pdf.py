#!/usr/bin/env python3
"""
Project Verde — Definitive Documentation Builder
Generates a world-class PDF document using ReportLab.
"""

import os
import math
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, Flowable, Frame, PageTemplate, BaseDocTemplate,
    NextPageTemplate, FrameBreak
)
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.colors import HexColor, Color, CMYKColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ============================================================
# REGISTER UNICODE FONTS (DejaVu for ₹ support)
# ============================================================
FONT_DIR = '/usr/share/fonts/truetype/dejavu'
pdfmetrics.registerFont(TTFont('DejaVu', os.path.join(FONT_DIR, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', os.path.join(FONT_DIR, 'DejaVuSans-Bold.ttf')))

# ============================================================
# DESIGN SYSTEM
# ============================================================
NAVY = HexColor('#0A1628')
NAVY_LIGHT = HexColor('#1A2744')
NAVY_MED = HexColor('#132040')
EMERALD = HexColor('#00A86B')
EMERALD_LIGHT = HexColor('#00C97B')
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

PAGE_W, PAGE_H = A4  # 595.27 x 841.89 points
MARGIN = 25 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

# ============================================================
# CUSTOM FLOWABLES
# ============================================================

class ColorBlock(Flowable):
    """A colored rectangle with optional text."""
    def __init__(self, width, height, color, text='', text_color=WHITE, font_size=11):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
    
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=0)
        if self.text:
            self.canv.setFillColor(self.text_color)
            self.canv.setFont('Helvetica-Bold', self.font_size)
            self.canv.drawCentredString(self.width/2, self.height/2 - self.font_size/3, self.text)


class GradientRect(Flowable):
    """A rectangle with gradient fill (simulated with lines)."""
    def __init__(self, width, height, color1, color2):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color1 = color1
        self.color2 = color2
    
    def draw(self):
        steps = 50
        for i in range(steps):
            ratio = i / steps
            r = self.color1.red + (self.color2.red - self.color1.red) * ratio
            g = self.color1.green + (self.color2.green - self.color1.green) * ratio
            b = self.color1.blue + (self.color2.blue - self.color1.blue) * ratio
            self.canv.setFillColor(Color(r, g, b))
            y = self.height * (1 - (i + 1) / steps)
            h = self.height / steps + 1
            self.canv.rect(0, y, self.width, h, fill=1, stroke=0)


class KPICard(Flowable):
    """A KPI card with icon, number, and label."""
    def __init__(self, width, number, label, color=EMERALD, icon='●'):
        Flowable.__init__(self)
        self.width = width
        self.height = 70
        self.number = number
        self.label = label
        self.color = color
        self.icon = icon
    
    def draw(self):
        c = self.canv
        # Card background
        c.setFillColor(WHITE)
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=1)
        
        # Top accent line
        c.setFillColor(self.color)
        c.rect(0, self.height - 3, self.width, 3, fill=1, stroke=0)
        
        # Number
        c.setFillColor(self.color)
        c.setFont('DejaVu-Bold', 22)
        c.drawCentredString(self.width/2, self.height - 35, str(self.number))
        
        # Label
        c.setFillColor(TEXT_BODY)
        c.setFont('DejaVu', 8)
        c.drawCentredString(self.width/2, 8, self.label)


class SectionDivider(Flowable):
    """A decorative section divider line."""
    def __init__(self, width=CONTENT_W, color=EMERALD):
        Flowable.__init__(self)
        self.width = width
        self.height = 6
        self.color = color
    
    def draw(self):
        c = self.canv
        # Main line
        c.setStrokeColor(self.color)
        c.setLineWidth(2)
        c.line(0, 3, self.width * 0.3, 3)
        # Dot
        c.setFillColor(GOLD)
        c.circle(self.width * 0.3 + 5, 3, 3, fill=1, stroke=0)


class CalloutBox(Flowable):
    """A styled callout box with text."""
    def __init__(self, width, text, box_type='info'):
        Flowable.__init__(self)
        self.width = width
        self.text = text
        self.box_type = box_type  # info, warning, success, bug
        self._calc_height()
    
    def _calc_height(self):
        # Approximate height based on text length
        chars_per_line = int(self.width / 5.5)
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
        
        # Background
        c.setFillColor(bg)
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        
        # Icon
        icons = {'info': 'I', 'warning': '!', 'success': chr(10003), 'bug': 'B'}
        c.setFillColor(fg)
        c.setFont('DejaVu-Bold', 10)
        c.drawString(12, self.height - 18, icons.get(self.box_type, chr(8226)))
        
        # Text
        c.setFont('DejaVu', 9)
        x = 30
        y = self.height - 18
        words = self.text.split()
        line = ''
        max_w = self.width - 40
        for word in words:
            test = line + ' ' + word if line else word
            if c.stringWidth(test, 'Helvetica', 9) < max_w:
                line = test
            else:
                c.drawString(x, y, line)
                y -= 14
                line = word
        if line:
            c.drawString(x, y, line)


class FlowchartBox(Flowable):
    """Draw a simple flowchart node."""
    def __init__(self, width, height, text, node_type='process'):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.text = text
        self.node_type = node_type
    
    def draw(self):
        c = self.canv
        if self.node_type == 'start':
            c.setFillColor(EMERALD)
            c.roundRect(0, 0, self.width, self.height, self.height/2, fill=1, stroke=0)
        elif self.node_type == 'decision':
            c.setFillColor(GOLD)
            c.saveState()
            cx, cy = self.width/2, self.height/2
            path = c.beginPath()
            path.moveTo(cx, cy + self.height/2)
            path.lineTo(cx + self.width/2, cy)
            path.lineTo(cx, cy - self.height/2)
            path.lineTo(cx - self.width/2, cy)
            path.close()
            c.drawPath(path, fill=1, stroke=0)
            c.restoreState()
        elif self.node_type == 'end':
            c.setFillColor(ALERT_RED)
            c.roundRect(0, 0, self.width, self.height, self.height/2, fill=1, stroke=0)
        else:
            c.setFillColor(NAVY_LIGHT)
            c.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=0)
        
        c.setFillColor(WHITE)
        c.setFont('DejaVu-Bold', 8)
        # Word wrap
        words = self.text.split()
        line = ''
        y = self.height/2 + 4
        for word in words:
            test = line + ' ' + word if line else word
            if c.stringWidth(test, 'Helvetica-Bold', 8) < self.width - 16:
                line = test
            else:
                c.drawCentredString(self.width/2, y, line)
                y -= 11
                line = word
        if line:
            c.drawCentredString(self.width/2, y, line)


class HorizontalBar(Flowable):
    """A horizontal progress/metric bar."""
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
        
        # Label
        c.setFillColor(TEXT_BODY)
        c.setFont('DejaVu', 8)
        c.drawString(0, bar_y + 3, self.label)
        
        # Background bar
        bar_x = 90
        c.setFillColor(LIGHT_GRAY)
        c.roundRect(bar_x, bar_y, bar_w, bar_h, 3, fill=1, stroke=0)
        
        # Value bar
        fill_w = bar_w * min(self.value / self.max_val, 1.0)
        c.setFillColor(self.color)
        c.roundRect(bar_x, bar_y, fill_w, bar_h, 3, fill=1, stroke=0)
        
        # Value text
        c.setFillColor(WHITE if fill_w > 40 else TEXT_BODY)
        c.setFont('DejaVu-Bold', 8)
        c.drawString(bar_x + fill_w + 5, bar_y + 3, str(self.value))


# ============================================================
# PAGE TEMPLATES WITH DECORATIONS
# ============================================================

def draw_page_footer(canvas_obj, doc):
    """Draw consistent footer on content pages."""
    canvas_obj.saveState()
    # Footer line
    canvas_obj.setStrokeColor(LIGHT_GRAY)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(MARGIN, 30*mm, PAGE_W - MARGIN, 30*mm)
    
    # Page number
    canvas_obj.setFillColor(MID_GRAY)
    canvas_obj.setFont('DejaVu', 8)
    canvas_obj.drawCentredString(PAGE_W/2, 22*mm, f'— {doc.page} —')
    
    # Footer text
    canvas_obj.setFont('DejaVu', 7)
    canvas_obj.setFillColor(MID_GRAY)
    canvas_obj.drawString(MARGIN, 22*mm, 'PROJECT VERDE')
    canvas_obj.drawRightString(PAGE_W - MARGIN, 22*mm, 'DAV ACON 5 — 2026')
    
    # Subtle top accent
    canvas_obj.setStrokeColor(EMERALD)
    canvas_obj.setLineWidth(1.5)
    canvas_obj.line(MARGIN, PAGE_H - 12*mm, MARGIN + 40*mm, PAGE_H - 12*mm)
    canvas_obj.setStrokeColor(GOLD)
    canvas_obj.setLineWidth(1.5)
    canvas_obj.line(MARGIN + 41*mm, PAGE_H - 12*mm, MARGIN + 50*mm, PAGE_H - 12*mm)
    
    canvas_obj.restoreState()


def draw_cover_page(canvas_obj, doc):
    """Draw the full-bleed cover page."""
    canvas_obj.saveState()
    
    # Full navy background
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    
    # Gradient overlay at bottom
    for i in range(100):
        ratio = i / 100
        y = PAGE_H * ratio * 0.4
        h = PAGE_H * 0.004 + 1
        alpha = ratio * 0.6
        c = Color(0, 0.66 * alpha, 0.42 * alpha, alpha)
        canvas_obj.setFillColor(c)
        canvas_obj.rect(0, y, PAGE_W, h, fill=1, stroke=0)
    
    # Cover image
    cover_path = os.path.join(IMG_DIR, 'cover_art.jpg')
    if os.path.exists(cover_path):
        canvas_obj.drawImage(cover_path, 0, PAGE_H * 0.35, 
                           width=PAGE_W, height=PAGE_H * 0.45,
                           preserveAspectRatio=True, anchor='c', mask='auto')
    
    # Semi-transparent overlay on image
    canvas_obj.setFillColor(Color(0.04, 0.09, 0.16, 0.5))
    canvas_obj.rect(0, PAGE_H * 0.35, PAGE_W, PAGE_H * 0.45, fill=1, stroke=0)
    
    # Top decorative elements
    canvas_obj.setStrokeColor(GOLD)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(MARGIN, PAGE_H - 30*mm, MARGIN + 60*mm, PAGE_H - 30*mm)
    canvas_obj.setFillColor(GOLD)
    canvas_obj.circle(MARGIN + 63*mm, PAGE_H - 30*mm, 3, fill=1, stroke=0)
    
    # Leaf icon (simple)
    canvas_obj.setFillColor(EMERALD)
    canvas_obj.setFont('DejaVu', 28)
    canvas_obj.drawString(MARGIN, PAGE_H - 55*mm, chr(127807))  # 🌿
    
    # Project name
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont('DejaVu-Bold', 42)
    canvas_obj.drawString(MARGIN, PAGE_H - 80*mm, 'PROJECT')
    canvas_obj.setFillColor(EMERALD)
    canvas_obj.setFont('DejaVu-Bold', 52)
    canvas_obj.drawString(MARGIN, PAGE_H - 100*mm, 'VERDE')
    
    # Tagline
    canvas_obj.setFillColor(GOLD_LIGHT)
    canvas_obj.setFont('DejaVu', 13)
    canvas_obj.drawString(MARGIN, PAGE_H - 118*mm, '"The plant that waters itself')
    canvas_obj.drawString(MARGIN, PAGE_H - 132*mm, '  \u2014 and talks to AI."')
    
    # Bottom info block
    canvas_obj.setFillColor(Color(1, 1, 1, 0.1))
    canvas_obj.roundRect(MARGIN, 25*mm, CONTENT_W, 55*mm, 6, fill=1, stroke=0)
    
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont('DejaVu-Bold', 11)
    canvas_obj.drawString(MARGIN + 15*mm, 65*mm, 'Smart IoT Irrigation & Plant-Care System')
    
    canvas_obj.setFont('DejaVu', 9)
    canvas_obj.setFillColor(Color(1, 1, 1, 0.8))
    canvas_obj.drawString(MARGIN + 15*mm, 52*mm, 'DAV ACON 5 \u2014 Tech Exhibition 2026')
    canvas_obj.drawString(MARGIN + 15*mm, 40*mm, 'Created by: Aarav Choudhary & Anuj  |  Class X')
    
    # Cost badge
    canvas_obj.setFillColor(EMERALD)
    canvas_obj.roundRect(PAGE_W - MARGIN - 55*mm, 42*mm, 50*mm, 30*mm, 4, fill=1, stroke=0)
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont('DejaVu-Bold', 10)
    canvas_obj.drawCentredString(PAGE_W - MARGIN - 30*mm, 62*mm, 'BUILD COST')
    canvas_obj.setFont('DejaVu-Bold', 16)
    canvas_obj.drawCentredString(PAGE_W - MARGIN - 30*mm, 47*mm, '\u20B91,890')
    
    # Status badge
    canvas_obj.setFillColor(GOLD)
    canvas_obj.roundRect(MARGIN, 85*mm, 50*mm, 12*mm, 3, fill=1, stroke=0)
    canvas_obj.setFillColor(NAVY)
    canvas_obj.setFont('DejaVu-Bold', 8)
    canvas_obj.drawCentredString(MARGIN + 25*mm, 89*mm, 'COMPLETE & DEMO-READY')
    
    canvas_obj.restoreState()


# ============================================================
# STYLES
# ============================================================

def get_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        'SectionTitle', parent=styles['Title'],
        fontName='DejaVu-Bold', fontSize=24, leading=30,
        textColor=NAVY, spaceAfter=6*mm, spaceBefore=4*mm,
    ))
    
    styles.add(ParagraphStyle(
        'SubTitle', parent=styles['Title'],
        fontName='DejaVu-Bold', fontSize=16, leading=20,
        textColor=NAVY_LIGHT, spaceAfter=4*mm, spaceBefore=6*mm,
    ))
    
    styles.add(ParagraphStyle(
        'BodyText2', parent=styles['Normal'],
        fontName='DejaVu', fontSize=10, leading=15,
        textColor=TEXT_BODY, spaceAfter=3*mm, alignment=TA_JUSTIFY,
    ))
    
    styles.add(ParagraphStyle(
        'BulletItem', parent=styles['Normal'],
        fontName='DejaVu', fontSize=9.5, leading=14,
        textColor=TEXT_BODY, leftIndent=15, spaceAfter=2*mm,
        bulletIndent=0, bulletFontSize=9,
    ))
    
    styles.add(ParagraphStyle(
        'Caption', parent=styles['Normal'],
        fontName='DejaVu', fontSize=8, leading=11,
        textColor=MID_GRAY, alignment=TA_CENTER, spaceAfter=4*mm,
    ))
    
    styles.add(ParagraphStyle(
        'PullQuote', parent=styles['Normal'],
        fontName='DejaVu-Bold', fontSize=13, leading=18,
        textColor=EMERALD, alignment=TA_CENTER, spaceAfter=5*mm, spaceBefore=5*mm,
        leftIndent=20, rightIndent=20,
    ))
    
    styles.add(ParagraphStyle(
        'TOCEntry', parent=styles['Normal'],
        fontName='DejaVu', fontSize=11, leading=20,
        textColor=TEXT_DARK, leftIndent=10,
    ))
    
    styles.add(ParagraphStyle(
        'TOCSection', parent=styles['Normal'],
        fontName='DejaVu-Bold', fontSize=12, leading=22,
        textColor=NAVY, spaceBefore=3*mm,
    ))
    
    styles.add(ParagraphStyle(
        'HeroNumber', parent=styles['Normal'],
        fontName='DejaVu-Bold', fontSize=36, leading=42,
        textColor=EMERALD, alignment=TA_CENTER,
    ))
    
    styles.add(ParagraphStyle(
        'SmallBold', parent=styles['Normal'],
        fontName='DejaVu-Bold', fontSize=9, leading=12,
        textColor=NAVY, spaceAfter=1*mm,
    ))
    
    styles.add(ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='DejaVu', fontSize=8.5, leading=12,
        textColor=TEXT_BODY,
    ))
    
    styles.add(ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontName='DejaVu-Bold', fontSize=9, leading=12,
        textColor=WHITE,
    ))
    
    styles.add(ParagraphStyle(
        'CodeBlock', parent=styles['Normal'],
        fontName='Courier', fontSize=8, leading=11,
        textColor=NAVY_LIGHT, leftIndent=10, rightIndent=10,
        backColor=HexColor('#F0F4F8'), spaceAfter=3*mm, spaceBefore=2*mm,
    ))
    
    return styles


# ============================================================
# SECTION BUILDERS
# ============================================================

def build_toc(styles):
    """Build table of contents."""
    elements = []
    elements.append(Spacer(1, 10*mm))
    elements.append(Paragraph('Contents', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 8*mm))
    
    toc_items = [
        ('01', 'The Whole Story in 60 Seconds'),
        ('02', 'The Problem — Why Plants Die'),
        ('03', 'Our Solution — Three-Tier Architecture'),
        ('04', 'Hardware — Sensors, Actuators & Power'),
        ('05', 'Firmware — The Brain & The Big Bug'),
        ('06', 'Cloud — Firebase Schema & Design'),
        ('07', 'The Web App — Dashboard, Controls & AI'),
        ('08', 'AI & APIs — Four Intelligence Layers'),
        ('09', 'Features — Every Live Capability'),
        ('10', 'Testing Journal — 13-Point Matrix'),
        ('11', 'Real Bugs We Hit & Fixed'),
        ('12', 'Cost & Sustainability'),
        ('13', 'Future Scope'),
        ('14', 'Judge Tour Script'),
        ('15', 'Conclusion'),
    ]
    
    for num, title in toc_items:
        elements.append(Paragraph(
            f'<font color="{EMERALD.hexval()}" size="14">{num}</font>'
            f'&nbsp;&nbsp;&nbsp;<font size="11">{title}</font>',
            styles['TOCEntry']
        ))
    
    elements.append(Spacer(1, 15*mm))
    elements.append(Paragraph(
        '<i>Every section can be read independently. Start anywhere.</i>',
        styles['Caption']
    ))
    
    return elements


def build_executive_summary(styles):
    """Section 1: 60-second overview."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('01', ParagraphStyle('num', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('The Whole Story in 60 Seconds', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'Project Verde is a smart irrigation system that costs ₹1,890, uses 5 sensors and 2 microcontrollers, '
        'talks to 4 AI APIs, and <b>never lets your plants die again.</b>',
        styles['BodyText2']
    ))
    
    elements.append(Spacer(1, 4*mm))
    
    # KPI Cards row
    kpi_data = [
        ('₹1,890', 'Total Build Cost', EMERALD),
        ('5', 'Sensors', NAVY_LIGHT),
        ('4', 'AI APIs', GOLD),
        ('94%', 'Diagnosis Accuracy', EMERALD_DARK),
    ]
    
    card_w = (CONTENT_W - 15) / 4
    kpi_table = []
    row = []
    for num, label, color in kpi_data:
        row.append(KPICard(card_w, num, label, color))
    kpi_table.append(row)
    
    t = Table(kpi_table, colWidths=[card_w + 4]*4)
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 6*mm))
    
    # Architecture image
    arch_path = os.path.join(IMG_DIR, 'architecture.jpg')
    if os.path.exists(arch_path):
        elements.append(Image(arch_path, width=CONTENT_W * 0.85, height=100))
        elements.append(Paragraph('Three-tier architecture: Edge → Cloud → Experience', styles['Caption']))
    
    elements.append(Spacer(1, 4*mm))
    
    # Quick summary bullets
    summary_bullets = [
        '<b>Edge:</b> ESP32 reads soil moisture, temperature, humidity, light, and tank level every second. A pump and UV grow light respond automatically.',
        '<b>Cloud:</b> Firebase Realtime Database is the single source of truth. One bundled JSON write + one read per second.',
        '<b>Experience:</b> A single-file web app with live dashboard, weather integration, AI plant doctor, and smart chat assistants.',
        '<b>The Big Win:</b> We reduced 17 Firebase calls/second to 2 — eliminating watchdog reboots and making the pump run smoothly.',
    ]
    for b in summary_bullets:
        elements.append(Paragraph(f'● {b}', styles['BulletItem']))
    
    return elements


def build_problem_section(styles):
    """Section 2: The Problem."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('02', ParagraphStyle('num2', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('The Problem — Why Plants Die', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'Urban families forget to water plants, or over-water them. Plants don\'t die from neglect — '
        'they die from a <b>lack of information</b>.',
        styles['BodyText2']
    ))
    
    elements.append(Spacer(1, 3*mm))
    
    elements.append(Paragraph(
        'Nobody knows in real time how dry the soil is, whether the water tank is empty, '
        'or whether rain is coming. The feedback loop is broken.',
        styles['BodyText2']
    ))
    
    elements.append(Spacer(1, 4*mm))
    
    # Comparison table
    elements.append(Paragraph('The Market Gap', styles['SubTitle']))
    
    comp_data = [
        ['Feature', 'Commercial Kits\n(₹8,000+)', 'Project Verde\n(₹1,890)'],
        ['Soil Moisture', '✓', '✓'],
        ['Temperature & Humidity', '✓', '✓'],
        ['Water Tank Monitoring', '✗', '✓'],
        ['Camera / Visual Monitor', '✗', '✓ (ESP32-CAM)'],
        ['AI Plant Diagnosis', '✗', '✓ (94% accuracy)'],
        ['Weather Integration', '✗', '✓ (Rain override)'],
        ['Open Source / Hackable', '✗', '✓'],
        ['AI Chat Assistants', '✗', '✓ (4 APIs)'],
        ['Student-Buildable', '✗', '✓'],
    ]
    
    comp_table = Table(comp_data, colWidths=[CONTENT_W*0.4, CONTENT_W*0.3, CONTENT_W*0.3])
    comp_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('BACKGROUND', (2,1), (2,-1), HexColor('#E8F8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, OFF_WHITE]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ])
    comp_table.setStyle(comp_style)
    elements.append(comp_table)
    
    elements.append(Spacer(1, 6*mm))
    
    elements.append(Paragraph(
        'Commercial smart-garden kits cost ₹8,000+, lack cameras, lack AI, and often can\'t be '
        'opened or understood by students. We built something better for less than a quarter of the price.',
        styles['BodyText2']
    ))
    
    # Cost comparison bar chart
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph('Cost Comparison', styles['SmallBold']))
    
    bar_data = [
        ('Commercial Kit A', 8000, ALERT_RED),
        ('Commercial Kit B', 12000, ALERT_RED),
        ('Average Market', 10000, ALERT_ORANGE),
        ('Project Verde', 1890, EMERALD),
    ]
    
    for label, val, color in bar_data:
        elements.append(HorizontalBar(CONTENT_W, val, 12000, label, color))
    
    return elements


def build_solution_section(styles):
    """Section 3: Solution & Architecture."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('03', ParagraphStyle('num3', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('Our Solution — Three-Tier Architecture', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'A three-tier IoT system where the plant "tells" us what it needs and the system acts automatically:',
        styles['BodyText2']
    ))
    
    elements.append(Spacer(1, 4*mm))
    
    # Tier boxes
    tier_data = [
        [Paragraph('<font color="#FFFFFF"><b>EDGE TIER</b></font>', styles['TableCell']),
         '',
         Paragraph('<font color="#FFFFFF"><b>CLOUD TIER</b></font>', styles['TableCell']),
         '',
         Paragraph('<font color="#FFFFFF"><b>EXPERIENCE TIER</b></font>', styles['TableCell'])],
    ]
    
    tier_table = Table(tier_data, colWidths=[CONTENT_W*0.33, 3*mm, CONTENT_W*0.33, 3*mm, CONTENT_W*0.33 - 9*mm])
    tier_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), EMERALD_DARK),
        ('BACKGROUND', (2,0), (2,0), NAVY),
        ('BACKGROUND', (4,0), (4,0), NAVY_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    elements.append(tier_table)
    
    elements.append(Spacer(1, 3*mm))
    
    # Tier details
    tier_details = [
        [Paragraph('<b>ESP32 WROOM-32</b><br/>Brain + 5 sensors<br/>Pump & UV-LED control', styles['TableCell']),
         '→',
         Paragraph('<b>Firebase RTDB</b><br/>Single source of truth<br/>1s heartbeat JSON', styles['TableCell']),
         '→',
         Paragraph('<b>Web App (HTML)</b><br/>Dashboard & controls<br/>AI assistants', styles['TableCell'])],
    ]
    
    detail_table = Table(tier_details, colWidths=[CONTENT_W*0.33, 3*mm, CONTENT_W*0.33, 3*mm, CONTENT_W*0.33 - 9*mm])
    detail_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (1,0), (1,0), GOLD),
        ('TEXTCOLOR', (3,0), (3,0), GOLD),
        ('FONTNAME', (1,0), (1,0), 'Helvetica-Bold'),
        ('FONTNAME', (3,0), (3,0), 'Helvetica-Bold'),
        ('FONTSIZE', (1,0), (1,0), 16),
        ('FONTSIZE', (3,0), (3,0), 16),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(detail_table)
    
    elements.append(Spacer(1, 4*mm))
    
    # Additional tier - ESP32-CAM
    cam_box_data = [
        [Paragraph('<font color="#FFFFFF"><b>CAM: ESP32-CAM (OV2640) — The Eyes</b></font>', styles['TableCell'])],
        [Paragraph('<font size="8">Captures SVGA photos on demand → uploads to cloud → app displays in ≤2 seconds</font>', styles['TableCell'])],
    ]
    cam_table = Table(cam_box_data, colWidths=[CONTENT_W])
    cam_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor('#2D5A3A')),
        ('BACKGROUND', (0,1), (0,1), HexColor('#E8F8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(cam_table)
    
    # 1-second heartbeat timeline (before image)
    elements.append(Spacer(1, 6*mm))
    elements.append(Paragraph('The 1-Second Heartbeat', styles['SubTitle']))
    elements.append(Paragraph(
        'Every second, the ESP32 bundles 10 sensor readings into one JSON write and reads 9 control values. '
        'This is the rhythm that keeps the system alive.',
        styles['BodyText2']
    ))
    timeline_items = ['0s', '1s', '2s', '3s', '4s', '5s']
    timeline_data = [[Paragraph(f'<font size="8" color="#00A86B"><b>● READ</b></font><br/>'
                                f'<font size="7">sensors→JSON</font>', styles['TableCell']) 
                      for _ in range(6)]]
    timeline_data.append([Paragraph(f'<font size="8" color="#D4AF37"><b>● WRITE</b></font><br/>'
                                    f'<font size="7">/sensors</font>', styles['TableCell']) 
                          for _ in range(6)])
    timeline_data.append([Paragraph(f'<font size="8" color="#1A2744"><b>● READ</b></font><br/>'
                                    f'<font size="7">/controls</font>', styles['TableCell']) 
                          for _ in range(6)])
    
    tl_table = Table(timeline_data, colWidths=[CONTENT_W/6]*6)
    tl_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#F0FAF5')),
        ('BACKGROUND', (0,1), (-1,1), HexColor('#FFFBF0')),
        ('BACKGROUND', (0,2), (-1,2), HexColor('#F0F4F8')),
    ]))
    elements.append(tl_table)
    
    # Architecture diagram image (also shown in executive summary)
    elements.append(Spacer(1, 6*mm))
    arch_path = os.path.join(IMG_DIR, 'architecture.jpg')
    if os.path.exists(arch_path):
        elements.append(Image(arch_path, width=CONTENT_W * 0.55, height=70))
        elements.append(Paragraph('System Architecture — Edge, Cloud, and Experience layers', styles['Caption']))
    
    return elements


def build_hardware_section(styles):
    """Section 4: Hardware."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('04', ParagraphStyle('num4', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('Hardware — Sensors, Actuators & Power', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    # Hardware image
    hw_path = os.path.join(IMG_DIR, 'hardware_bench.jpg')
    if os.path.exists(hw_path):
        elements.append(Image(hw_path, width=CONTENT_W * 0.8, height=120))
        elements.append(Paragraph('The Verde hardware bench — 2 MCUs, 5 sensors, 2 actuators', styles['Caption']))
    
    elements.append(Spacer(1, 4*mm))
    
    # BOM Table
    elements.append(Paragraph('Bill of Materials', styles['SubTitle']))
    
    bom_data = [
        ['Module', 'ESP32 Pin', 'Role'],
        ['Soil Moisture (LM393)', 'AO→GPIO34, VCC→GPIO23', '% soil wetness\n(power-gated 15ms reads)'],
        ['DHT11', 'DATA→GPIO4', 'Temperature + Humidity'],
        ['LDR Module', 'AO→GPIO35', 'Ambient light → dark detection'],
        ['HC-SR04 Ultrasonic', 'TRIG→GPIO18\nECHO→GPIO19', 'Water tank level\n(5-point filter)'],
        ['2-Channel Relay', 'IN1→GPIO5\n(active-LOW)', 'Switches 5V water pump'],
        ['UV Grow LED', 'GPIO12\n(active-HIGH, 220Ω)', 'Photosynthetic light'],
        ['ESP32-CAM (OV2640)', 'Own board + MB\nprogrammer', 'SVGA photos → cloud'],
    ]
    
    bom_table = Table(bom_data, colWidths=[CONTENT_W*0.28, CONTENT_W*0.32, CONTENT_W*0.4])
    bom_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, OFF_WHITE]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ])
    bom_table.setStyle(bom_style)
    elements.append(bom_table)
    
    elements.append(Spacer(1, 6*mm))
    
    # Power design section
    elements.append(Paragraph('Power Design — Hard-Won Lessons', styles['SubTitle']))
    
    power_bullets = [
        '<b>Main supply: 5V / 2A phone adapter</b> — NOT a USB-PD laptop charger. PD requires a handshake chip the ESP32 lacks, so it outputs ~0 mA and starves the board.',
        '<b>1000 µF electrolytic capacitor</b> across 5V/GND — absorbs pump + WiFi current spikes.',
        '<b>1N4007 flyback diode</b> across the pump — kills inductive spikes that would reset the ESP32.',
        '<b>Pump electrically isolated</b> via relay COM/NO on its own 5V source — prevents noise coupling.',
    ]
    for b in power_bullets:
        elements.append(Paragraph(f'● {b}', styles['BulletItem']))
    
    # Power warning callout
    elements.append(Spacer(1, 3*mm))
    elements.append(CalloutBox(CONTENT_W, 
        'THE USB-PD TRAP: A 67W USB-PD charger will NOT power the ESP32. '
        'PD requires a negotiation handshake chip the ESP32 lacks — the charger defaults to 0mA output. '
        'Use a simple 5V/2A phone adapter instead. We learned this the hard way.',
        'warning'))
    
    return elements


def build_firmware_section(styles):
    """Section 5: Firmware & The Big Bug."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('05', ParagraphStyle('num5', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('Firmware — The Brain & The Big Bug', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        '<b>Code_1_Main_Brain.ino — V3.0.7-FINAL</b>',
        styles['SmallBold']
    ))
    elements.append(Spacer(1, 2*mm))
    
    fw_features = [
        'Non-blocking <b>millis()</b> task scheduler: sensors 1Hz · cloud 1s · WiFi 10s · logs 60s',
        'Hardware watchdog (8s) fed every loop — if the system hangs, it reboots itself',
        '<b>AUTO logic:</b> pump_ON = moisture &lt; threshold AND tank safe AND no rain',
        '<b>Manual logic:</b> user-driven from app, still tank-protected',
        'Adjustable thresholds from app: moisture (35%), tank (15%), light (35%) — persisted in NVS flash',
        '<b>10-point moving averages</b> for soil/LDR sensors',
        '<b>5-point moving average + invalid-read rejection</b> for the tank (pump-splash garbage can\'t fake an empty tank)',
        '<b>±2% hysteresis</b> on light auto-switch — no LED flicker',
        '3-network WiFi fallback: home → hotspot → school',
    ]
    for f in fw_features:
        elements.append(Paragraph(f'● {f}', styles['BulletItem']))
    
    elements.append(Spacer(1, 6*mm))
    
    # THE BIG BUG - dramatic callout
    elements.append(Paragraph('The Big Bug Story', styles['SubTitle']))
    
    # BEFORE/AFTER comparison
    bug_data = [
        [Paragraph('<font color="#E53E3E"><b>BEFORE — The Problem</b></font>', styles['TableCell']),
         Paragraph('<font color="#00A86B"><b>AFTER — The Fix</b></font>', styles['TableCell'])],
        [Paragraph('17 Firebase HTTPS calls per second', styles['TableCell']),
         Paragraph('2 calls per second (1 write + 1 read)', styles['TableCell'])],
        [Paragraph('Network stall → 8s watchdog reboot', styles['TableCell']),
         Paragraph('Zero reboots, stable connection', styles['TableCell'])],
        [Paragraph('Pump clicked ON/OFF every ~10s', styles['TableCell']),
         Paragraph('Pump stays ON continuously until threshold', styles['TableCell'])],
        [Paragraph('Root cause: individual sensor writes', styles['TableCell']),
         Paragraph('JSON bundling: all sensors in one object', styles['TableCell'])],
    ]
    
    bug_table = Table(bug_data, colWidths=[CONTENT_W*0.5, CONTENT_W*0.5])
    bug_style = TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor('#FEE2E2')),
        ('BACKGROUND', (1,0), (1,0), HexColor('#D1FAE5')),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ])
    bug_table.setStyle(bug_style)
    elements.append(bug_table)
    
    elements.append(Spacer(1, 4*mm))
    
    # Visual: 17 → 2 calls
    elements.append(Paragraph(
        '<font color="#00A86B" size="28"><b>17 calls/s</b></font>'
        '<font color="#D4AF37" size="18">  ➜  </font>'
        '<font color="#00A86B" size="28"><b>2 calls/s</b></font>'
        '<font color="#8899AA" size="12">  (≈85% reduction)</font>',
        ParagraphStyle('hero', parent=styles['BodyText2'], alignment=TA_CENTER, spaceBefore=4*mm, spaceAfter=4*mm)
    ))
    
    elements.append(Paragraph(
        '<i>The fix was elegant: instead of writing each sensor individually (10 writes) and reading each '
        'control individually (7 reads), we bundled all sensor data into one /sensors JSON object and '
        'read all controls from one /controls object. Two network round-trips instead of seventeen.</i>',
        styles['BodyText2']
    ))
    
    # ESP32-CAM Section
    elements.append(Spacer(1, 6*mm))
    elements.append(Paragraph('ESP32-CAM Firmware — V3.0.4-FINAL', styles['SubTitle']))
    
    cam_features = [
        'Polls <b>/controls/capture_photo</b> every 1.5s → on trigger: flash LED → capture SVGA JPEG',
        'POSTs raw bytes to Vercel upload API → lands in /latest_scan (base64) → app shows it ≤2s',
        '<b>8 MHz XCLK</b> — fixes RF interference with WiFi antenna (was 20 MHz)',
        '<b>Sequential boot:</b> camera first, WiFi after 500ms — prevents brownout',
        '<b>esp_camera_fb_return()</b> called immediately — prevents heap fragmentation',
    ]
    for f in cam_features:
        elements.append(Paragraph(f'● {f}', styles['BulletItem']))
    
    return elements


def build_cloud_section(styles):
    """Section 6: Cloud & Firebase."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('06', ParagraphStyle('num6', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('Cloud — Firebase Schema & Design', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    # Firebase schema image
    fb_path = os.path.join(IMG_DIR, 'firebase_schema.jpg')
    if os.path.exists(fb_path):
        elements.append(Image(fb_path, width=CONTENT_W * 0.6, height=100))
        elements.append(Paragraph('Firebase Realtime Database — verde-tech-haha', styles['Caption']))
    
    elements.append(Spacer(1, 4*mm))
    
    # Schema tree
    elements.append(Paragraph('Database Schema Tree', styles['SubTitle']))
    
    schema_data = [
        ['Path', 'Fields', 'Purpose'],
        ['/sensors/', 'moisture, temperature, humidity, light,\ntank_level, lux, watchdog_status,\nvoltage_sag, uploads (success/fail)', 'All telemetry\n(10 metrics)'],
        ['/controls/', 'manual_mode, pump_state, light_manual_mode,\ngrow_light_state, capture_photo,\nthresholds (moisture/tank/light),\nweather_override', 'App→ESP32\ncommands (9 keys)'],
        ['/latest_scan/', 'imageUrl (base64), status, captured_at,\nscientificName, diseaseName,\nprobability, treatmentPlan', 'Camera + AI\nanalysis data'],
        ['/weather/', 'city, temp, condition, description,\nhumidity, wind_speed, rain_expected,\nsynced_at', 'OpenWeatherMap\ncached data'],
        ['/historical_logs/', 'moisture_log [{time, moisture}]', 'Chart data\nfor dashboard'],
        ['/actuators/', 'pump_actual, grow_light_actual, mode', 'Actual state\nconfirmation'],
    ]
    
    schema_table = Table(schema_data, colWidths=[CONTENT_W*0.22, CONTENT_W*0.45, CONTENT_W*0.33])
    schema_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, OFF_WHITE]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('FONTNAME', (0,1), (0,-1), 'Courier'),
        ('TEXTCOLOR', (0,1), (0,-1), EMERALD_DARK),
    ])
    schema_table.setStyle(schema_style)
    elements.append(schema_table)
    
    elements.append(Spacer(1, 4*mm))
    
    elements.append(Paragraph(
        '<b>Security Rules:</b> Public read access. Validated writes (booleans and numbers 0–100). '
        'ESP32 authenticates using a legacy database secret.',
        styles['BodyText2']
    ))
    
    return elements


def build_app_section(styles):
    """Section 7: Web App."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('07', ParagraphStyle('num7', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('The Web App — Dashboard, Controls & AI', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'A single-file HTML application that serves as the "face" of Project Verde. '
        'Four pages accessible via a burger menu:',
        styles['BodyText2']
    ))
    
    elements.append(Spacer(1, 4*mm))
    
    # Four pages
    pages = [
        ('1', 'Dashboard', EMERALD, [
            '8 live telemetry tiles with sparklines + hover graphs',
            'All 8 controls (pump, light, camera, modes)',
            '3 threshold sliders (moisture, tank, light)',
            'Predicted actuator states',
            'Moisture history chart',
            'System status strip + uptime timer',
            'Fullscreen demo mode + toast notifications',
        ]),
        ('2', 'Weather', NAVY_LIGHT, [
            'Live Delhi weather from OpenWeatherMap',
            '5-day forecast chips',
            'Auto rain-override (checks every 3 min) with countdown',
            'If rain expected → weather_override = 1 → pump disabled',
        ]),
        ('3', 'Plant Doctor', GOLD, [
            'Live CAM photo frame (auto-updates ≤2s)',
            'CAPTURE button triggers ESP32-CAM',
            'Upload-or-CAM modal for diagnosis',
            'crop.health analysis: species + disease + treatment',
            'AI chat that sees the same image',
        ]),
        ('4', 'AI Assistants', HexColor('#6B46C1'), [
            'Gemini 2.5 Flash image chat',
            'OpenRouter sensor-aware chat',
            'Quick prompt buttons for common questions',
            'Fallback chains (435 models, never dead-end)',
        ]),
    ]
    
    for num, title, color, features in pages:
        # Page header
        page_header = [[Paragraph(f'<font color="#FFFFFF"><b>  {num}. {title.upper()}</b></font>', styles['TableCell'])]]
        ph_table = Table(page_header, colWidths=[CONTENT_W])
        ph_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), color),
            ('TOPPADDING', (0,0), (0,0), 6),
            ('BOTTOMPADDING', (0,0), (0,0), 6),
        ]))
        elements.append(ph_table)
        
        for f in features:
            elements.append(Paragraph(f'  ● {f}', ParagraphStyle('sub_bullet', parent=styles['BulletItem'], fontSize=8.5, leftIndent=12)))
        elements.append(Spacer(1, 3*mm))
    
    # Extra features
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph('Additional App Features', styles['SubTitle']))
    extras = [
        '<b>Tank Calibration Panel:</b> SET EMPTY / SET FULL — app-side remap, no reflashing needed',
        '<b>Image Flip Fix:</b> ESP32-CAM mounts upside-down — CSS transform corrects orientation',
        '<b>Last-10 Trend Indicators:</b> Each tile shows ▲/▼ with percentage change',
    ]
    for e in extras:
        elements.append(Paragraph(f'● {e}', styles['BulletItem']))
    
    return elements


def build_ai_section(styles):
    """Section 8: AI & APIs."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('08', ParagraphStyle('num8', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('AI & APIs — Four Intelligence Layers', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    # AI image
    ai_path = os.path.join(IMG_DIR, 'ai_chat.jpg')
    if os.path.exists(ai_path):
        elements.append(Image(ai_path, width=CONTENT_W * 0.7, height=100))
        elements.append(Paragraph('AI-powered plant analysis and intelligent chat assistants', styles['Caption']))
    
    elements.append(Spacer(1, 4*mm))
    
    # API Table
    api_data = [
        ['API', 'Purpose', 'Auth Method', 'Key Mechanic', 'Accuracy'],
        ['OpenWeatherMap', 'Live weather +\n5-day forecast\n→ rain override', 'Key in URL', 'GET /data/2.5/weather\nids 2xx/3xx/5xx/6xx\n→ rain → override=1', 'Live-tested:\nDelhi 35°C\ncorrect city ID'],
        ['crop.health\n(Plant.id)', 'Plant + disease\nidentification', 'Api-Key\nheader', 'POST /api/v1/identification\nwith base64 image\n→ crop + disease suggestions', '94% accuracy\non test image:\nnutrient deficiency'],
        ['Google Gemini\n2.5 Flash', 'Vision chat on\nanalysed photo', 'X-goog-api-key\nheader (AQ keys)', 'POST /v1beta/models/\ngemini-flash-latest:\ngenerateContent', 'Vision + text\nwith diagnosis\n+ telemetry context'],
        ['OpenRouter', 'Sensor chat +\nvision fallback', 'Bearer\nsk-or-v1-…', 'POST /api/v1/chat/\ncompletions\n(OpenAI-compatible)', '435 models\n8-model text chain\n5-model vision chain'],
    ]
    
    api_table = Table(api_data, colWidths=[CONTENT_W*0.17, CONTENT_W*0.2, CONTENT_W*0.15, CONTENT_W*0.28, CONTENT_W*0.2])
    api_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, OFF_WHITE]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ])
    api_table.setStyle(api_style)
    elements.append(api_table)
    
    elements.append(Spacer(1, 5*mm))
    
    # Gemini note
    elements.append(CalloutBox(CONTENT_W,
        'Note: Gemini 2.5 Flash is no longer offered to new users. We use gemini-flash-latest instead. '
        'AQ keys require the X-goog-api-key header format — standard Bearer tokens do not work.',
        'info'))
    
    elements.append(Spacer(1, 4*mm))
    
    # OpenRouter fallback chains
    elements.append(Paragraph('OpenRouter Fallback Architecture', styles['SubTitle']))
    elements.append(Paragraph(
        'The system uses intelligent fallback chains to ensure AI responses never fail:',
        styles['BodyText2']
    ))
    
    chain_data = [
        ['Text Chain (8 models)', 'Vision Chain (5 models)'],
        ['Primary → Secondary → Tertiary →\nQuaternary → Quinary → Senary →\nSeptenary → Fallback',
         'Primary Vision → Secondary Vision →\nTertiary Vision → Quaternary Vision →\nText Fallback (sends image description)'],
    ]
    
    chain_table = Table(chain_data, colWidths=[CONTENT_W*0.5, CONTENT_W*0.5])
    chain_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), EMERALD),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ])
    chain_table.setStyle(chain_style)
    elements.append(chain_table)
    
    return elements


def build_features_section(styles):
    """Section 9: Features."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('09', ParagraphStyle('num9', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('Features — Every Live Capability', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    features = [
        ('Auto Irrigation', 'Pump activates when soil moisture drops below threshold (35%), with tank-level and rain protection'),
        ('Tank Monitoring', 'Ultrasonic sensor measures water level with 5-point filtering. Calibratable from app (SET EMPTY/FULL)'),
        ('Climate Sensing', 'DHT11 provides temperature and humidity. 10-point moving average for smooth readings'),
        ('Light Management', 'LDR detects ambient light. UV grow LED auto-activates in darkness with ±2% hysteresis'),
        ('Live Camera', 'ESP32-CAM captures photos on demand. Image appears in app within 2 seconds'),
        ('Plant Doctor', 'AI-powered diagnosis: species ID + disease detection + treatment plan. 94% accuracy'),
        ('Weather Intelligence', 'Real-time Delhi weather + 5-day forecast. Auto rain-override prevents over-watering'),
        ('AI Chat (Gemini)', 'Vision-enabled chat that sees the plant photo, knows the diagnosis, and answers questions'),
        ('AI Chat (OpenRouter)', 'Sensor-aware chat with full telemetry context. 435 models, never dead-ends'),
        ('Live Dashboard', '8 telemetry tiles with sparklines, trend indicators, and last-10 data points'),
        ('Full Control', 'Manual/Auto mode toggle, threshold sliders, pump/light controls — all from the app'),
        ('Watchdog Recovery', 'Hardware watchdog (8s) automatically reboots if firmware hangs'),
        ('WiFi Resilience', '3-network fallback: home → hotspot → school. Always connected'),
        ('Data Persistence', 'Thresholds stored in NVS flash. Survives power cycles without reconfiguration'),
    ]
    
    for title, desc in features:
        elements.append(Paragraph(
            f'<b>{title}</b> — {desc}',
            styles['BulletItem']
        ))
    
    return elements


def build_testing_section(styles):
    """Section 10: Testing."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('10', ParagraphStyle('num10', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('Testing Journal — 13-Point Matrix', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'Every subsystem was independently tested and verified. Here is the complete test matrix:',
        styles['BodyText2']
    ))
    
    test_data = [
        ['#', 'Test', 'Method', 'Result'],
        ['1', 'WiFi / Boot', 'Power cycle → auto-connect\nwithin 3s', '✓ PASS'],
        ['2', 'DHT11 Breathe', 'Blow warm air → temp rises\nwithin 2s', '✓ PASS'],
        ['3', 'Moisture Water-Dunk', 'Probe in water → 95%+\nProbe dry → <5%', '✓ PASS'],
        ['4', 'LDR Cover Test', 'Hand over sensor →\n"Dark" triggers LED', '✓ PASS'],
        ['5', 'Ultrasonic Hand', 'Hand at known distance\n→ accurate within ±1cm', '✓ PASS'],
        ['6', 'Pump AUTO 120s', 'Dry soil → pump runs\ncontinuously 120s', '✓ PASS'],
        ['7', 'Threshold OFF', 'Moisture reaches 35% →\npump stops exactly', '✓ PASS'],
        ['8', 'Tank Lock', 'Empty tank → pump blocked\neven if soil is dry', '✓ PASS'],
        ['9', 'Rain Override', 'Weather API says rain →\npump disabled', '✓ PASS'],
        ['10', 'CAM Capture ≤2s', 'Trigger → photo in app\nwithin 2 seconds', '✓ PASS'],
        ['11', 'Plant Doctor 94%', 'Test leaf image →\nnutrient deficiency @94%', '✓ PASS'],
        ['12', 'AI Chats + Fallbacks', 'All 4 APIs respond\ncorrectly', '✓ PASS'],
        ['13', 'Watchdog 10+ min', 'System runs 10+ minutes\nwith 0 reboots', '✓ PASS'],
    ]
    
    test_table = Table(test_data, colWidths=[CONTENT_W*0.06, CONTENT_W*0.22, CONTENT_W*0.45, CONTENT_W*0.27])
    test_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (3,1), (3,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, OFF_WHITE]),
        ('TEXTCOLOR', (3,1), (3,-1), SUCCESS_GREEN),
        ('FONTNAME', (3,1), (3,-1), 'Helvetica-Bold'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
    ])
    test_table.setStyle(test_style)
    elements.append(test_table)
    
    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph(
        '<font color="#00A86B" size="24"><b>13 / 13</b></font> <font size="12">tests passed</font>',
        ParagraphStyle('hero_test', parent=styles['BodyText2'], alignment=TA_CENTER, spaceBefore=4*mm, spaceAfter=4*mm)
    ))
    
    return elements


def build_bugs_section(styles):
    """Section 11: Real Bugs."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('11', ParagraphStyle('num11', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('Real Bugs We Hit & Fixed', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'Honesty builds credibility. Here are the real engineering challenges we encountered and solved:',
        styles['BodyText2']
    ))
    
    elements.append(Spacer(1, 3*mm))
    
    bugs = [
        ('1', 'AUTO 10s pump loop', '17 Firebase calls/s caused network stall → watchdog reboot loop', 
         'JSON bundling: 1 write + 1 read per second (2 calls/s total)'),
        ('2', 'Camera probe 0x106', 'FPC ribbon cable unseated', 
         'Reseat gold-side down + power cycle'),
        ('3', 'PSRAM not found', 'Weak power supply', 
         'Switched to 5V/2A adapter'),
        ('4', '0x20002 boot crash', 'Camera + WiFi simultaneous power surge', 
         'Sequential boot: camera first, WiFi after 500ms'),
        ('5', 'RF interference', '20 MHz XCLK caused WiFi noise', 
         'Throttled XCLK to 8 MHz'),
        ('6', '67W charger starved board', 'USB-PD negotiation fails without handshake chip', 
         'Use simple 5V/2A phone adapter'),
        ('7', 'Relay dead', 'Split breadboard power rails', 
         'Bridge + to +, − to − across split'),
        ('8', 'Temperature = 0', 'DHT11 on wrong pin', 
         'Move to GPIO4 + shared GND'),
        ('9', 'Firebase "spurts"', '13 individual calls/s blocking the loop', 
         'One bundled call with all sensor data'),
        ('10', 'Compile error', 'Copy-paste corruption in source', 
         'Re-download file cleanly'),
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
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('FONTSIZE', (0,0), (-1,-1), 8),
        ]))
        elements.append(bug_table)
        elements.append(Spacer(1, 1.5*mm))
    
    return elements


def build_cost_section(styles):
    """Section 12: Cost."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('12', ParagraphStyle('num12', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('Cost & Sustainability', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    # Cost table
    cost_data = [
        ['Category', 'Items', 'Cost (₹)'],
        ['Electronics', 'ESP32, ESP32-CAM, 5 sensors,\nrelay, pump, UV LED', '1,320'],
        ['Power & Protection', '5V/2A adapter, 1000µF cap,\n1N4007 diode', '220'],
        ['Mechanical', 'Breadboard, jumper wires,\nenclosure', '350'],
        ['Software & APIs', 'All on free tiers\n(Firebase, OWM, Gemini, OpenRouter)', '0'],
        ['', '', ''],
        ['', 'TOTAL', '₹1,890'],
    ]
    
    cost_table = Table(cost_data, colWidths=[CONTENT_W*0.3, CONTENT_W*0.45, CONTENT_W*0.25])
    cost_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (1,6), (-1,6), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,4), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,4), [WHITE, OFF_WHITE]),
        ('LINEABOVE', (0,6), (-1,6), 1.5, EMERALD),
        ('BACKGROUND', (0,6), (-1,6), HexColor('#E8F8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (2,0), (2,-1), 12),
    ])
    cost_table.setStyle(cost_style)
    elements.append(cost_table)
    
    elements.append(Spacer(1, 5*mm))
    
    # Value proposition
    elements.append(Paragraph(
        '<font color="#00A86B" size="20"><b>₹1,890</b></font>'
        '<font size="10"> ≈ $23 USD — all software and APIs on free tiers</font>',
        ParagraphStyle('cost_hero', parent=styles['BodyText2'], alignment=TA_CENTER, spaceBefore=4*mm, spaceAfter=4*mm)
    ))
    
    elements.append(Paragraph(
        'Every component is commercially available, every API is on a free tier, '
        'and every line of code is open to inspection. A student with basic electronics '
        'knowledge can replicate this build.',
        styles['BodyText2']
    ))
    
    # Sustainability
    elements.append(Spacer(1, 4*mm))
    elements.append(Paragraph('Sustainability Notes', styles['SubTitle']))
    sustain_bullets = [
        'Low power draw: 5V/2A = 10W max, typically 3-5W during operation',
        'All software on free tiers — zero recurring cost',
        'Components are standard, replaceable, non-proprietary',
        'Future: solar autonomy planned (12V panel + charge controller + battery)',
        'Water-efficient: only irrigates when needed, respects rain forecasts',
    ]
    for b in sustain_bullets:
        elements.append(Paragraph(f'● {b}', styles['BulletItem']))
    
    return elements


def build_future_section(styles):
    """Section 13: Future Scope."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('13', ParagraphStyle('num13', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('Future Scope', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    future_items = [
        ('Solar Autonomy', '12V solar panel + charge controller + LiPo battery for completely off-grid operation'),
        ('NPK Soil Probe', 'Measure nitrogen, phosphorus, potassium levels for precision fertilization'),
        ('Multi-Plant Zones', 'Multiple soil probes + valve manifold for different plant types'),
        ('Telegram / WhatsApp Alerts', 'Push notifications for critical events: tank empty, disease detected, extreme weather'),
        ('Predictive Watering', 'Use historical moisture logs + weather forecast to predict optimal watering schedule'),
        ('Deployed Dashboard', 'Next.js scaffold already built — ready for production deployment'),
    ]
    
    for title, desc in future_items:
        elements.append(Paragraph(
            f'<b>{title}</b>',
            ParagraphStyle('future_title', parent=styles['SmallBold'], fontSize=11, spaceBefore=3*mm)
        ))
        elements.append(Paragraph(f'    {desc}', styles['BulletItem']))
    
    # Roadmap visualization
    elements.append(Spacer(1, 6*mm))
    elements.append(Paragraph('Roadmap', styles['SmallBold']))
    
    roadmap_data = [
        ['NOW', 'NEXT', 'LATER'],
        ['Single plant\nFull automation\n4 AI APIs',
         'Multi-zone\nSolar power\nPush alerts',
         'NPK probe\nPredictive model\nProduction dashboard'],
    ]
    
    rm_table = Table(roadmap_data, colWidths=[CONTENT_W/3]*3)
    rm_style = TableStyle([
        ('BACKGROUND', (0,0), (0,0), EMERALD),
        ('BACKGROUND', (1,0), (1,0), NAVY_LIGHT),
        ('BACKGROUND', (2,0), (2,0), GOLD),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('FONTSIZE', (0,1), (-1,1), 8),
        ('TEXTCOLOR', (0,1), (-1,1), TEXT_BODY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
    ])
    rm_table.setStyle(rm_style)
    elements.append(rm_table)
    
    return elements


def build_judge_tour(styles):
    """Section 14: Judge Tour Script."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('14', ParagraphStyle('num14', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('Judge Tour Script', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        '<i>A 3-minute guided tour script for presenting to judges:</i>',
        styles['Caption']
    ))
    
    tour_steps = [
        ('0:00–0:30', 'The Hook', 
         '"This is Project Verde. It costs ₹1,890, uses 5 sensors, talks to 4 AIs, and this plant has been watering itself for the last 10 minutes without any human intervention."'),
        ('0:30–1:00', 'The Architecture',
         '"Three tiers: the ESP32 is the brain reading soil, temperature, humidity, light, and tank level. Firebase is the cloud brain. This web app is the face. And the ESP32-CAM is the eyes."'),
        ('1:00–1:30', 'The Demo',
         '"Watch the dashboard — moisture is at 28%, below our 35% threshold. The tank has water. No rain is expected. The pump just turned on automatically. See the tile turning green."'),
        ('1:30–2:00', 'The Big Bug',
         '"We hit a critical bug: the pump was clicking on and off every 10 seconds. Root cause: 17 Firebase calls per second. Fix: JSON bundling — 2 calls per second. The pump now runs smoothly until the soil is moist enough."'),
        ('2:00–2:30', 'The AI',
         '"Let me show you the Plant Doctor. I capture a photo of this leaf, and the AI identifies it as a nutrient deficiency with 94% confidence and suggests a treatment plan. Gemini can also look at the image and answer questions about it."'),
        ('2:30–3:00', 'The Close',
         '"₹1,890. All free APIs. Built by two Class X students. This is what happens when you give a plant a voice."'),
    ]
    
    for time, title, script in tour_steps:
        step_data = [
            [Paragraph(f'<font color="#D4AF37"><b>{time}</b></font>', styles['TableCell']),
             Paragraph(f'<b>{title}</b>', styles['TableCell']),
             Paragraph(f'<i>{script}</i>', styles['TableCell'])],
        ]
        step_table = Table(step_data, colWidths=[CONTENT_W*0.12, CONTENT_W*0.15, CONTENT_W*0.73])
        step_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), HexColor('#FFFBF0')),
            ('GRID', (0,0), (-1,-1), 0.5, LIGHT_GRAY),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ]))
        elements.append(step_table)
        elements.append(Spacer(1, 2*mm))
    
    return elements


def build_conclusion(styles):
    """Section 15: Conclusion."""
    elements = []
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph('15', ParagraphStyle('num15', parent=styles['SectionTitle'], fontSize=48, textColor=EMERALD, spaceAfter=0)))
    elements.append(Paragraph('Conclusion', styles['SectionTitle']))
    elements.append(SectionDivider())
    elements.append(Spacer(1, 5*mm))
    
    elements.append(Paragraph(
        'Project Verde proves that smart, AI-powered technology doesn\'t have to be expensive '
        'or complicated. With ₹1,890 worth of components, free APIs, and honest engineering, '
        'we built a system that:',
        styles['BodyText2']
    ))
    
    conclusion_points = [
        'Waters plants automatically — no human intervention needed',
        'Monitors 5 environmental parameters in real time',
        'Takes photos and diagnoses plant diseases with 94% accuracy',
        'Checks the weather and adjusts behavior accordingly',
        'Provides 4 AI-powered assistance tools',
        'Runs reliably with hardware watchdog protection',
        'Is fully open, hackable, and student-buildable',
    ]
    for p in conclusion_points:
        elements.append(Paragraph(f'● {p}', styles['BulletItem']))
    
    elements.append(Spacer(1, 6*mm))
    
    elements.append(Paragraph(
        'We encountered 10 real bugs and fixed every one of them. We learned that USB-PD chargers '
        'don\'t work without a negotiation chip, that camera ribbons need to be reseated firmly, '
        'and that 17 Firebase calls per second will bring your system to its knees.',
        styles['BodyText2']
    ))
    
    elements.append(Spacer(1, 4*mm))
    
    elements.append(Paragraph(
        'Every number in this document is real. Every test was actually run. '
        'Every bug was actually hit. We didn\'t simplify for the presentation — '
        'this is exactly what we built.',
        styles['BodyText2']
    ))
    
    elements.append(Spacer(1, 8*mm))
    
    # Final pull quote
    elements.append(Paragraph(
        '"The plant that waters itself — and talks to AI."',
        styles['PullQuote']
    ))
    
    elements.append(Spacer(1, 6*mm))
    
    # Credits
    credit_data = [
        [Paragraph('<b>PROJECT VERDE</b>', ParagraphStyle('credit_title', parent=styles['TableCell'], fontSize=12, textColor=NAVY, alignment=TA_CENTER))],
        [Paragraph('Aarav Choudhary & Anuj — Class X', ParagraphStyle('credit_names', parent=styles['TableCell'], alignment=TA_CENTER))],
        [Paragraph('DAV ACON 5 — Tech Exhibition 2026', ParagraphStyle('credit_event', parent=styles['TableCell'], alignment=TA_CENTER))],
        [Paragraph('Build cost: ₹1,890 | All software free tiers | 100% student-built', ParagraphStyle('credit_details', parent=styles['TableCell'], alignment=TA_CENTER, fontSize=8, textColor=MID_GRAY))],
    ]
    credit_table = Table(credit_data, colWidths=[CONTENT_W * 0.7])
    credit_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LINEABOVE', (0,0), (0,0), 2, EMERALD),
        ('LINEBELOW', (0,-1), (0,-1), 2, EMERALD),
    ]))
    # Center the table
    outer = Table([[credit_table]], colWidths=[CONTENT_W])
    outer.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER')]))
    elements.append(outer)
    
    return elements


# ============================================================
# DOCUMENT ASSEMBLY
# ============================================================

def build_document():
    """Build the complete PDF."""
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'Project_Verde_Documentation.pdf')
    
    styles = get_styles()
    
    # Create document
    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=18*mm,
        bottomMargin=35*mm,
        title='Project Verde — Smart IoT Irrigation & Plant-Care System',
        author='Aarav Choudhary & Anuj',
        subject='DAV ACON 5 Tech Exhibition 2026',
    )
    
    # Page templates
    content_frame = Frame(
        MARGIN, 35*mm, CONTENT_W, PAGE_H - 53*mm,
        id='content'
    )
    
    cover_template = PageTemplate(
        id='cover',
        frames=[Frame(0, 0, PAGE_W, PAGE_H, id='cover_frame', 
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
        onPage=draw_cover_page,
    )
    
    content_template = PageTemplate(
        id='content',
        frames=[content_frame],
        onPage=draw_page_footer,
    )
    
    doc.addPageTemplates([cover_template, content_template])
    
    # Build elements
    elements = []
    
    # Cover page (template handles the drawing)
    elements.append(NextPageTemplate('content'))
    elements.append(PageBreak())
    
    # Table of Contents
    elements.extend(build_toc(styles))
    elements.append(PageBreak())
    
    # All sections — grouped to minimize orphan pages and let content flow naturally
    elements.extend(build_executive_summary(styles))
    elements.append(Spacer(1, 10*mm))
    elements.extend(build_problem_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_solution_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_hardware_section(styles))
    elements.append(Spacer(1, 6*mm))
    elements.extend(build_firmware_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_cloud_section(styles))
    elements.append(Spacer(1, 6*mm))
    elements.extend(build_app_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_ai_section(styles))
    elements.append(Spacer(1, 6*mm))
    elements.extend(build_features_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_testing_section(styles))
    elements.append(Spacer(1, 6*mm))
    elements.extend(build_bugs_section(styles))
    elements.append(PageBreak())
    
    elements.extend(build_cost_section(styles))
    elements.append(Spacer(1, 6*mm))
    elements.extend(build_future_section(styles))
    elements.append(Spacer(1, 8*mm))
    elements.extend(build_judge_tour(styles))
    elements.append(PageBreak())
    
    elements.extend(build_conclusion(styles))
    
    # Build PDF
    doc.build(elements)
    print(f'✅ PDF generated: {output_path}')
    return output_path


if __name__ == '__main__':
    build_document()
