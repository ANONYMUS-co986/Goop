"""Project Verde — definitive documentation PDF builder."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme as T
from theme import PAGE_W, PAGE_H, MARGIN, CONTENT_W, NAVY, NAVY_900, NAVY_700, NAVY_600, NAVY_500
from theme import EMERALD, EMERALD_2, EMERALD_D, GOLD, GOLD_2, INK, BODY, MUTED, SOFT, CARD_BG, MIST, LINE, WARN, GOOD
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, NextPageTemplate, KeepTogether,
                                Preformatted, HRFlowable, Image, Flowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm, cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from PIL import Image as PILImage
import diagrams as D
import flowables as F
from pages import FullPage, content_bg

T.register_fonts()

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build", "Project_Verde_Documentation.pdf")

# ---------------------------------------------------------------- styles
def _ps(name, **kw):
    base = dict(fontName="Inter", fontSize=9.7, leading=14.6, textColor=BODY,
                alignment=TA_JUSTIFY, spaceAfter=0, spaceBefore=0)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
 "body": _ps("body"),
 "body-l": _ps("body-l", fontSize=10.6, leading=16.4),
 "body-sm": _ps("body-sm", fontSize=8.8, leading=12.6),
 "muted": _ps("muted", textColor=MUTED, fontSize=9, leading=13.5, alignment=TA_LEFT),
 "h1": _ps("h1", fontName="SG-Bold", fontSize=25, leading=29, textColor=NAVY, alignment=TA_LEFT),
 "h2": _ps("h2", fontName="SG-SemiBold", fontSize=15, leading=19, textColor=NAVY, alignment=TA_LEFT),
 "h3": _ps("h3", fontName="Inter-SemiBold", fontSize=11, leading=14, textColor=NAVY, alignment=TA_LEFT),
 "kicker": _ps("kicker", fontName="SG-SemiBold", fontSize=9, leading=11, textColor=EMERALD_D, alignment=TA_LEFT),
 "bullet": _ps("bullet", fontSize=9.6, leading=14.2, leftIndent=14, bulletIndent=2, alignment=TA_LEFT),
 "cap": _ps("cap", fontName="Inter", fontSize=8, leading=11, textColor=MUTED, alignment=TA_LEFT),
 "quote": _ps("quote", fontName="SG-Medium", fontSize=13, leading=18, textColor=NAVY, alignment=TA_LEFT),
 "table": _ps("table", fontSize=8.6, leading=12, textColor=BODY, alignment=TA_LEFT),
 "table-h": _ps("table-h", fontName="Inter-SemiBold", fontSize=8.6, leading=12, textColor=white, alignment=TA_LEFT),
 "big": _ps("big", fontName="SG-SemiBold", fontSize=18, leading=22, textColor=NAVY, alignment=TA_LEFT),
 "center": _ps("center", alignment=TA_CENTER),
}

def P(txt, style="body"):
    return Paragraph(txt, S[style])

def cell(txt, style="table", bold=False):
    if bold:
        return Paragraph(f"<b>{txt}</b>", S[style])
    return Paragraph(txt, S[style])

def B(txt):
    return Paragraph(txt, S["bullet"])

# ---------------------------------------------------------------- doc
class VerdeDoc(BaseDocTemplate):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.section = ""

story = []

class SectionFlow(Flowable):
    """Zero-size marker that records the running section during layout."""
    def wrap(self, aw, ah):
        _doc.section = self.name
        return (0, 0)

    def draw(self):
        pass

def sec(name):
    f = SectionFlow()
    f.name = name
    story.append(f)

# ---------------------------------------------------------------- helpers
def section_title(number, kicker, title, lead=None):
    """Chapter opener block placed at top of a content section."""
    rows = [[Paragraph(f'<font color="#17C96E">C H A P T E R&nbsp;&nbsp;{number}</font>&nbsp;&nbsp;·&nbsp;&nbsp;{kicker}', S["kicker"])],
            [Paragraph(title, S["h1"])]]
    t = Table(rows, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,0), 0),
        ("BOTTOMPADDING", (0,0), (-1,0), 3),
        ("BOTTOMPADDING", (0,1), (-1,1), 6),
        ("TOPPADDING", (0,1), (-1,1), 2),
    ]))
    story.append(t)
    # gold rule
    story.append(HRFlowable(width=64, thickness=3, color=GOLD, spaceBefore=2, spaceAfter=14))
    if lead:
        story.append(Paragraph(lead, S["body-l"]))
        story.append(Spacer(1, 14))
    story.append(Spacer(1, 2))

def subhead(text):
    story.append(Spacer(1, 6))
    story.append(Paragraph(text, S["h2"]))
    story.append(Spacer(1, 5))

def bullets(items, style="bullet"):
    for it in items:
        story.append(Paragraph(f'<bullet>&bull;</bullet>{it}', S[style]))
    story.append(Spacer(1, 6))

def kpi_row(cards):
    widths = [CONTENT_W / len(cards)] * len(cards)
    t = Table([cards], colWidths=widths)
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

def fig(img, w, caption=None, sub=None, border=None, height=None):
    story.append(F.ImgFigure(img, w, caption=caption, sub=sub, border=border, height=height))
    story.append(Spacer(1, 12))

def svg(drawing, w, h=None):
    orig_w = drawing.width
    orig_h = drawing.height
    sc = w / orig_w
    target_h = orig_h * sc
    drawing.width = w
    drawing.height = target_h
    drawing.scale(sc, sc)
    story.append(drawing)
    story.append(Spacer(1, 12))

def callout(title, body, icon="!", bg=SOFT, accent=EMERALD, h=None):
    story.append(F.Callout(title, body, icon=icon, bg=bg, accent=accent, h=h))
    story.append(Spacer(1, 12))

def quote(text, accent=GOLD):
    q = F.PullQuote(text, accent=accent)
    story.append(q)
    story.append(Spacer(1, 14))

def spacer(h=10):
    story.append(Spacer(1, h))

def new_content():
    story.append(NextPageTemplate("content"))
    story.append(PageBreak())

def cover_page():
    story.append(FullPage(cover))
    story.append(NextPageTemplate("content"))
    story.append(PageBreak())

def divider_page(draw_fn):
    story.append(NextPageTemplate("fullpage"))
    story.append(PageBreak())
    story.append(FullPage(draw_fn))
    story.append(NextPageTemplate("content"))
    story.append(PageBreak())

# ================================================================ COVER
def cover(canv):
    W, H = PAGE_W, PAGE_H
    canv.saveState()
    # background image cover (scale to fill)
    img = ImageReader("assets/img/cover_art.png")
    iw, ih = img.getSize()
    scale = max(W / iw, H / ih)
    dw, dh = iw * scale, ih * scale
    canv.drawImage(img, W/2 - dw/2, H/2 - dh/2, width=dw, height=dh, preserveAspectRatio=True, anchor="c", mask="auto")
    # dark overlay for text legibility (gradient bottom)
    T.vgrad(canv, 0, 0, W, 330, T.with_alpha(NAVY_900, 0.95), T.with_alpha(NAVY_900, 0.0))
    T.vgrad(canv, 0, H-240, W, 240, T.with_alpha(NAVY_900, 0.0), T.with_alpha(NAVY_900, 0.98))
    # top brand
    canv.setFillColor(T.EMERALD_2); canv.setFont("SG-Bold", 17)
    canv.drawString(58, H - 84, "PROJECT")
    canv.setFillColor(white); canv.drawString(58 + 88, H - 84, "VERDE")
    canv.setFillColor(GOLD); canv.circle(58 + 176, H - 79, 4, stroke=0, fill=1)
    canv.setFillColor(T.with_alpha(white, 0.75)); canv.setFont("Inter", 10)
    canv.drawRightString(W - 58, H - 82, "DAV ACON 5  ·  TECH EXHIBITION 2026")
    # center tagline
    canv.setFillColor(T.EMERALD_2); canv.setFont("SG-Medium", 13)
    canv.drawCentredString(W/2, H - 310, "THE PLANT THAT WATERS ITSELF — AND TALKS TO AI")
    # bottom block
    canv.setFillColor(white); canv.setFont("SG-Bold", 40)
    canv.drawString(58, 150, "Smart IoT Irrigation")
    canv.drawString(58, 106, "& Plant-Care System")
    canv.setFillColor(T.EMERALD_2); canv.rect(58, 88, 150, 5, stroke=0, fill=1)
    canv.setFillColor(T.with_alpha(white, 0.9)); canv.setFont("Inter-Medium", 12)
    canv.drawString(58, 66, "Aarav Choudhary  &  Anuj  ·  Class X")
    canv.setFillColor(T.with_alpha(white, 0.7)); canv.setFont("Inter", 11)
    canv.drawString(58, 46, "ESP32 + 5 sensors + pump/UV · Firebase · single-file web app · 4 AI APIs")
    # cost pill top-right
    canv.setFillColor(T.with_alpha(GOLD, 0.95)); canv.setFont("SG-SemiBold", 11)
    canv.drawString(W - 260, H - 124, "BUILT FOR ₹1,890  ·  ALL SOFTWARE FREE TIERS")
    canv.restoreState()

# ================================================================ DIVIDER
def divider(canv, number, title, subtitle, icon, accent=EMERALD, blurb=None):
    W, H = PAGE_W, PAGE_H
    canv.saveState()
    T.vgrad(canv, 0, 0, W, H, NAVY_900, NAVY_700)
    # large ghost number
    canv.setFillColor(T.with_alpha(GOLD, 0.10)); canv.setFont("SG-Bold", 260)
    canv.drawRightString(W - 40, H - 300, str(number))
    # accent orb glow
    F = T
    cx, cy = W - 130, H - 300
    canv.setFillColor(T.with_alpha(EMERALD, 0.18)); canv.circle(cx, cy, 120, stroke=0, fill=1)
    canv.setFillColor(T.with_alpha(EMERALD, 0.12)); canv.circle(cx, cy, 170, stroke=0, fill=1)
    # left content
    canv.setFillColor(accent); canv.setFont("SG-SemiBold", 12)
    canv.drawString(MARGIN, H - 150, f"CHAPTER {number}")
    canv.setFillColor(white); canv.setFont("SG-Bold", 44)
    # word-wrap the title across lines
    maxw = W - 2 * MARGIN
    avail = MARGIN
    ty = H - 205
    words = title.split(" ")
    cur = ""
    for wd in words:
        test = (cur + " " + wd).strip()
        if stringWidth(test, "SG-Bold", 44) <= maxw:
            cur = test
        else:
            if cur:
                canv.drawString(MARGIN, ty, cur)
                ty -= 52
            cur = wd
    if cur:
        canv.drawString(MARGIN, ty, cur)
    canv.setFillColor(GOLD); canv.rect(MARGIN, ty - 26, 64, 5, stroke=0, fill=1)
    canv.setFillColor(T.with_alpha(white, 0.85)); canv.setFont("Inter-Medium", 13)
    y = H - 265
    for ln in subtitle.split("\n"):
        canv.drawString(MARGIN, y, ln); y -= 20
    if blurb:
        canv.setFillColor(T.with_alpha(white, 0.6)); canv.setFont("Inter", 10.5)
        by = 90
        for ln in blurb.split("\n"):
            canv.drawString(MARGIN, by, ln); by += 15
    # bottom tagline
    canv.setFillColor(T.with_alpha(white, 0.4)); canv.setFont("Inter", 9)
    canv.drawString(MARGIN, 46, "PROJECT VERDE  ·  the plant that waters itself — and talks to AI")
    canv.restoreState()

# ================================================================ SECTION BUILDERS
def build_cover():
    cover_page()

def build_60_seconds():
    sec("Overview")
    section_title("00", "THE WHOLE STORY IN 60 SECONDS", "Meet Verde — the plant\nthat takes care of itself",
                  lead='Two tenth-graders built a smart-garden system that reads its own soil, decides when to water, '
                       'snaps a photo when worried, and asks an AI what is wrong. It costs ₹1,890, runs on free tiers, '
                       'and every part is open enough that anyone can understand it.')
    kpi_row([F.KpiCard("5", "sensors", "soil · temp · light · tank · camera", accent=EMERALD),
             F.KpiCard("2", "calls/sec", "down from 17 — the bug we fixed", accent=GOLD),
             F.KpiCard("94%", "diagnosis", "crop.health accuracy on a test photo", accent=EMERALD),
             F.KpiCard("₹1,890", "total cost", "vs ₹8,000+ for commercial kits", accent=GOLD)])
    quote("We built the plant a brain, a pair of eyes, a cloud, and four AI doctors — so the plant can finally speak up.",
          accent=EMERALD)
    subhead("Read this document in three minutes")
    bullets([
        "<b>The problem</b> — nobody knows in real time if soil is dry, the tank is empty, or rain is coming. Plants die from a <i>lack of information</i>.",
        "<b>Our answer</b> — a three-tier IoT system: an ESP32 edge reads 5 sensors, a Firebase cloud keeps one source of truth, and a single-file web app makes it all visible and controllable.",
        "<b>Five hardware sensors</b> power it: soil moisture, temperature/humidity, light, tank level — plus an ESP32-CAM that acts as the plant's eyes.",
        "<b>Two actuators</b> act on its behalf: a relay-driven water pump and a UV grow light.",
        "<b>Four AI APIs</b> give it a brain in the cloud: live weather, plant/disease ID, and two chat models that both see the same photo.",
        "<b>It just works</b> — 13 test points all pass, including one dramatic bug we fixed by cutting 17 network calls per second down to 2.",
    ])
    story.append(Spacer(1, 6))
    callout("Want the fastest tour?",
            "Flip to the Judge Tour Script at the end — a scripted walkthrough a judge can follow in three minutes.",
            icon="⚑", accent=GOLD)

def build_contents():
    new_content()
    sec("Contents")
    W = CONTENT_W
    # contents on a styled page
    story.append(Spacer(1, 8))
    story.append(Paragraph("CONTENTS", S["kicker"]))
    story.append(Paragraph("What's inside", S["h1"]))
    story.append(HRFlowable(width=64, thickness=3, color=GOLD, spaceBefore=4, spaceAfter=16))
    items = [
        ("00", "The Whole Story in 60 Seconds", "hero numbers, the one-liner, how to read this"),
        ("01", "Why — the problem", "forgotten plants, dry tanks, no real-time info"),
        ("02", "How it works — architecture", "edge · cloud · experience, the heartbeat"),
        ("03", "Hardware — BOM, circuit & power lessons", "5 sensors, pump, UV, the 5 V/2 A rule"),
        ("04", "Firmware — logic, watchdog & the big bug", "AUTO mode, JSON bundling 17→2"),
        ("05", "Cloud & web app", "Firebase schema, the single-file dashboard"),
        ("06", "AI & the four APIs", "weather, Plant Doctor, Gemini, OpenRouter"),
        ("07", "Features — everything live", "the dashboard, weather, plant doctor, AI chat"),
        ("08", "Testing & troubleshooting journal", "13-point pass matrix, 10 real bugs"),
        ("09", "Cost & sustainability", "₹1,890 budget breakdown, future scope"),
        ("10", "Judge tour script & conclusion", "a three-minute walkthrough"),
    ]
    rows = []
    for num, title, sub in items:
        rows.append([Paragraph(f'<font color="#17C96E" size="9">{num}</font>', S["table"]),
                     Paragraph(f"<b>{title}</b>", S["table"]),
                     Paragraph(sub, S["muted"])])
    t = Table(rows, colWidths=[46, 205, 240])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CARD_BG),
        ("GRID", (0,0), (-1,-1), 0.6, LINE),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [white, MIST]),
    ]))
    story.append(t)
    story.append(Spacer(1, 18))
    callout("A note on numbers",
            "Every figure in this document matches the project exactly — ₹1,890, 5 sensors, 2 MCUs, 17→2 calls, 94% diagnosis, "
            "8 MHz camera clock, GPIO pins, and thresholds of 35% / 15% / 35%.",
            icon="i", accent=GOLD)

def build_why():
    new_content()
    sec("Chapter 01 — Why")
    section_title("01", "THE PROBLEM", "Plants die from a lack of\ninformation — not a lack of love",
                  lead="Families want houseplants. They forget to water them, or drown them. The plant itself knows exactly "
                       "what it needs, but nobody is listening — because until now, a plant had no way to talk.")
    subhead("The everyday failure")
    bullets([
        "Urban families <b>forget to water</b>, or <b>over-water</b> — both kill plants slowly and silently.",
        "Nobody knows in real time: <b>how dry is the soil?</b> <b>Is the water tank empty?</b> <b>Is rain coming tonight?</b>",
        "By the time the leaves droop, it is often already too late — and the cause is a mystery.",
    ])
    spacer(4)
    subhead("What the market offers (and why it falls short)")
    rows = [
        [cell("Commercial smart-garden kits", bold=True), cell("₹8,000+"),
         cell("No camera, no AI, sealed black boxes students can't open")],
        [cell("Basic soil moisture probes", bold=True), cell("₹300"),
         cell("A raw number with no brain, no cloud, no automation")],
        [cell("DIY timers", bold=True), cell("₹500"),
         cell("Water on a clock, not on the plant's actual need")],
    ]
    t = Table(rows, colWidths=[180, 90, 221], rowHeights=None)
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.7, LINE),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [white, MIST]),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    quote("A plant shouldn't have to look thirsty before someone thinks to check on it. Ours simply tells us.",
          accent=EMERALD)
    subhead("The opportunity we saw")
    story.append(P("An open, affordable, understandable system that <b>watches the real world with sensors</b>, "
                   "<b>decides with logic</b>, <b>acts with a pump and light</b>, <b>shows everything in a web app</b>, and — "
                   "the part the big brands skip — <b>lets you ask an AI why your plant looks unhappy</b>. "
                   "Built by two Class X students, on free tiers, for less than the price of a video game."))

def build_architecture():
    divider_page(lambda c: divider(c, 2, "How it works",
        "Three tiers, one source of truth,\nand a heartbeat that never sleeps",
        icon="2", accent=EMERALD))
    sec("Chapter 02 — How it works")
    section_title("02", "ARCHITECTURE", "Edge · Cloud · Experience",
                  lead="Verde is a three-tier IoT system. The plant's world is sensed at the edge, stored in one place "
                       "in the cloud, and brought to life in a web app — with AI layered on top.")
    svg(D.architecture(), CONTENT_W * 0.92)
    spacer(4)
    subhead("The one-second heartbeat")
    story.append(P("Every second, the ESP32 reads its sensors, bundles the results into a single JSON payload, "
                   "writes them to Firebase, reads the latest control keys, and repeats. The whole network moves on "
                   "<b>two HTTPS calls per second</b>."))
    spacer(4)
    fig(D.heartbeat_timeline(), CONTENT_W * 0.9, caption="One heartbeat, ~450 ms round trip",
        sub="read → bundle → 1 write /sensors → 1 read /controls")
    callout("Why it matters",
            "Sensors are re-read every second, yet the network only needs 2 calls/sec. That decoupling is what lets "
            "the pump stay ON continuously without ever tripping the watchdog.",
            icon="♥", accent=EMERALD)

def build_hardware():
    divider_page(lambda c: divider(c, 3, "Hardware",
        "Five sensors, two actuators, two brains,\nand a power rule we learned the hard way",
        icon="3", accent=EMERALD))
    sec("Chapter 03 — Hardware")
    section_title("03", "THE BOM", "What's on the bench",
                  lead="Two microcontroller boards and a handful of cheap modules make up the entire physical system. "
                       "Nothing exotic — everything a student can buy, wire, and actually understand.")
    kpi_row([F.KpiCard("5", "sensors", "soil · temp · light · tank", accent=EMERALD),
             F.KpiCard("2", "actuators", "pump · UV grow LED", accent=GOLD),
             F.KpiCard("2", "MCUs", "ESP32 + ESP32-CAM", accent=EMERALD),
             F.KpiCard("₹1,320", "electronics", "the whole bill of materials", accent=GOLD)])
    # BOM table
    rows = [
        ["Module", "ESP32 pin", "Role"],
        ["Soil moisture (LM393)", "AO→GPIO34 · VCC gated→GPIO23", "% soil wetness; 15 ms power-gated reads stop corrosion"],
        ["DHT11", "DATA→GPIO4", "temperature + humidity"],
        ["LDR module", "AO→GPIO35", "ambient light → “dark” detection"],
        ["HC-SR04 ultrasonic", "TRIG→GPIO18 · ECHO→GPIO19", "tank level; 5-point filter rejects splash garbage"],
        ["2-ch relay", "IN1→GPIO5 (active-LOW)", "switches the isolated 5 V water pump"],
        ["UV grow LED", "GPIO12 (active-HIGH, 220Ω)", "photosynthetic light"],
        ["ESP32-CAM (OV2640)", "own board + MB programmer", "SVGA photos, uploaded to the cloud"],
    ]
    rows = [[cell(c, style="table-h") if ri == 0 else cell(c) for c in r] for ri, r in enumerate(rows)]
    t = Table(rows, colWidths=[150, 170, 171])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY_700), ("TEXTCOLOR", (0,0), (-1,0), white),
        ("GRID", (0,0), (-1,-1), 0.6, LINE),
        ("FONTSIZE", (0,0), (-1,-1), 8.3), ("LEADING", (0,0), (-1,-1), 11),
        ("LEFTPADDING", (0,0), (-1,-1), 9), ("RIGHTPADDING", (0,0), (-1,-1), 9),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, MIST]),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    svg(D.circuit(), CONTENT_W * 0.95)
    story.append(Paragraph('<font color="#122A3B"><b>Wiring map — every sensor on its pin</b></font>', S["cap"]))
    story.append(Paragraph("ESP32 WROOM-32 brain with the 5 sensors, relay, and UV LED", S["cap"]))
    story.append(Spacer(1, 12))
    new_content()
    sec("Chapter 03 — Hardware")
    subhead("Power lessons we learned the hard way")
    svg(D.power_lessons(), CONTENT_W * 0.95)
    spacer(2)
    story.append(P("The biggest “device bug” wasn't code at all — it was electricity. A <b>USB-PD laptop charger</b> refused to "
                   "power the board because PD requires a handshake chip the ESP32 lacks, so it output ~0 mA and starved the "
                   "whole project. The fix was a humble <b>5 V / 2 A phone adapter</b>, a <b>1000 µF capacitor</b> to soak up "
                   "pump-and-WiFi spikes, a <b>1N4007 flyback diode</b> to kill the pump's inductive kick, and a <b>relay-isolated "
                   "pump supply</b> so the brain never browns out."))
    spacer(6)
    fig("assets/img/esp32_hardware.png", CONTENT_W * 0.5, caption="The bench", sub="ESP32, ESP32-CAM, and the sensor set")
    fig("assets/img/bench_setup.png", CONTENT_W * 0.42, caption="Wired and running", sub="A working student build")

def build_firmware():
    divider_page(lambda c: divider(c, 4, "Firmware",
        "Logic, a watchdog, and the big bug\nthat taught us how to talk to the cloud",
        icon="4", accent=EMERALD))
    sec("Chapter 04 — Firmware")
    section_title("04", "CODE_1_MAIN_BRAIN.INO · V3.0.7-FINAL", "The brain's decisions",
                  lead="The ESP32 never blocks. A non-blocking millis() task scheduler keeps sensors at 1 Hz, the cloud "
                       "at 1 s, WiFi at 10 s, and logs at 60 s — while an 8-second hardware watchdog makes sure nothing "
                       "ever hangs silently.")
    subhead("The AUTO watering rule")
    story.append(P("<b>pump_ON = soil is dry AND the tank is safe AND no rain is coming.</b> "
                   "Every condition is sensed and checked in real time — nothing is guessed."))
    spacer(4)
    svg(D.auto_flow(), CONTENT_W * 0.9)
    spacer(4)
    fig(D.moisture_chart(), CONTENT_W * 0.92,
        caption="The watering cycle — falls to the threshold, waters, rises again",
        sub="gold dots mark each watering event · red dashed line = the 35% threshold")
    spacer(2)
    subhead("Engineering detail we're proud of")
    bullets([
        "<b>10-point moving averages</b> for soil and LDR — sensor noise disappears.",
        "<b>5-point moving average + invalid-read rejection</b> for the tank — pump splash can never fake an empty tank.",
        "<b>±2% hysteresis</b> on the light auto-switch — no LED flicker at the boundary.",
        "<b>3-network WiFi fallback</b> — home, hotspot, and school, so it works at the demo.",
        "<b>Adjustable thresholds</b> from the app (moisture / tank / light), persisted in NVS flash — no reflash needed.",
    ])
    new_content()
    sec("Chapter 04 — Firmware")
    section_title("04", "THE BIG BUG", "17 calls a second — and how we\ncut it to 2",
                  lead="AUTO mode kept clicking the pump ON and OFF every ~10 seconds. The culprit wasn't the watering "
                       "logic. It was the way the board talked to the internet.")
    story.append(P("<b>What we saw:</b> the pump would switch on, then off, then on again in a loop. A watchdog reboot "
                   "happened roughly every 8 seconds. From the outside it looked random; from the logs it was a pattern."))
    spacer(6)
    svg(D.before_after(), CONTENT_W * 0.96)
    spacer(2)
    subhead("Root cause")
    story.append(P("The firmware was making <b>17 blocking Firebase HTTPS calls every second</b> — writing sensor by "
                   "sensor, reading control by control. Each call stalled the network, the stalled network starved the "
                   "main loop, and the starved loop tripped the <b>8-second watchdog</b>, which rebooted the board and "
                   "reset the pump."))
    subhead("The fix: JSON bundling")
    bullets([
        "Group all <b>10 sensor metrics</b> into <b>one write</b> to <b>/sensors</b>.",
        "Read all <b>9 control keys</b> in <b>one read</b> of <b>/controls</b>.",
        "Result: <b>2 calls per second</b>, ~<b>85% less latency</b>, <b>zero watchdog reboots</b>, and the pump stays ON "
        "continuously until the moisture threshold is reached.",
    ])
    callout("The lesson",
            "The plant's real problem was chatty code, not dry soil. Talking to the cloud efficiently made the whole "
            "system calm, fast, and reliable.",
            icon="★", accent=GOLD)
    # CAM
    subhead("The eyes — Code_2_ESP32_CAM.ino · V3.0.4-FINAL")
    story.append(P("The ESP32-CAM polls <b>/controls/capture_photo</b> every 1.5 s. On a trigger it flashes an LED, "
                   "captures an SVGA JPEG, posts the raw bytes to a Vercel upload API, and the result lands in "
                   "<b>/latest_scan</b> — the web app shows it within about two seconds."))
    bullets([
        "<b>8 MHz XCLK</b> — throttled down to stop RF interference with the WiFi antenna.",
        "<b>Sequential boot</b> — camera first, WiFi after 500 ms, to prevent the power brownout that crashed earlier builds.",
        "<b>esp_camera_fb_return()</b> immediately — no heap fragmentation on long runs.",
    ])

def build_cloud():
    divider_page(lambda c: divider(c, 5, "Cloud & App",
        "One source of truth in Firebase,\nand a single-file web app as the face",
        icon="5", accent=EMERALD))
    sec("Chapter 05 — Cloud & App")
    section_title("05", "FIREBASE REALTIME DATABASE", "One place where everything lives",
                  lead="Every sensor value, control flag, photo, weather reading, and log flows through a single Firebase "
                       "Realtime Database. Public reads, validated writes — and the ESP32 authenticates with the legacy "
                       "database secret.")
    svg(D.firebase_schema(), CONTENT_W * 0.96)
    spacer(2)
    subhead("Rules that keep it safe")
    bullets([
        "<b>Public read</b> — the web app and the demo need instant access.",
        "<b>Validated writes</b> — only booleans and numbers in range (0–100) are accepted.",
        "<b>ESP32 uses the legacy database secret</b> for authenticated control writes.",
    ])
    new_content()
    sec("Chapter 05 — Cloud & App")
    section_title("05", "THE SINGLE-FILE WEB APP", "Four pages, one HTML file, no install",
                  lead="The entire interface ships as one self-contained HTML file served anywhere. A burger menu opens "
                       "four pages: Dashboard, Weather, Plant Doctor, and AI Assistants.")
    kpi_row([F.KpiCard("4", "pages", "dashboard · weather · doctor · AI", accent=EMERALD),
             F.KpiCard("8", "live tiles", "with sparklines + hover graphs", accent=GOLD),
             F.KpiCard("3", "sliders", "moisture / tank / light thresholds", accent=EMERALD),
             F.KpiCard("2 s", "photo refresh", "camera → cloud → screen", accent=GOLD)])
    subhead("Dashboard")
    bullets([
        "<b>8 live telemetry tiles</b> with sparklines and hover graphs, each showing a last-10 trend with ▲/▼ arrows.",
        "<b>All 8 controls</b> — manual mode, pump, light, and more.",
        "<b>3 threshold sliders</b> plus predicted actuator states and a moisture history chart.",
        "<b>System status strip, toasts, uptime timer, and a fullscreen demo mode</b> for exhibitions.",
    ])
    subhead("Weather")
    bullets([
        "Live Delhi weather plus a <b>5-day forecast</b>.",
        "An <b>auto rain-override</b> checks the forecast every 3 minutes and pauses watering when rain is coming.",
    ])
    subhead("Plant Doctor")
    bullets([
        "A live CAM photo frame that auto-updates within ~2 seconds, with a CAPTURE button.",
        "An upload-or-CAM modal for your own photo, crop.health diagnosis, and an AI chat that sees the same image.",
    ])
    subhead("AI Assistants")
    bullets([
        "<b>Gemini image chat</b> and an <b>OpenRouter sensor-aware chat</b> with quick prompts.",
    ])
    spacer(4)
    fig(D.demo_dashboard() if False else "assets/img/demo_dashboard.png", CONTENT_W * 0.86,
        caption="The dashboard, as it feels live", sub="telemetry tiles, moisture history, and the AI plant doctor")

def build_ai():
    divider_page(lambda c: divider(c, 6, "AI & APIs",
        "Weather, Plant Doctor, Gemini, OpenRouter —\nfour brains, each with honest accuracy notes",
        icon="6", accent=EMERALD))
    sec("Chapter 06 — AI & APIs")
    section_title("06", "THE FOUR APIS", "Four brains, each with honest accuracy notes",
                  lead="No fake AI. Every model is real, keyed, and tested. Here is what each one does, how it talks to us, "
                       "and exactly how accurate it turned out to be.")
    rows = [
        ["API", "Job", "Auth", "How it calls us", "Accuracy (tested)"],
        ["OpenWeatherMap", "live weather + 5-day rain forecast", "key in URL", "GET /data/2.5/weather?q=Delhi; ids 2xx/3xx/5xx/6xx → rain → override=1",
         "Delhi 35 °C; city id 1273294 verified"],
        ["crop.health (Plant.id)", "plant + disease identification", "Api-Key header", "POST /api/v1/identification with base64 image → crop.suggestions[] + disease.suggestions[]",
         "94% on a test photo — nutrient deficiency + treatment plan"],
        ["Google Gemini 2.5 Flash", "vision chat on the analysed photo", "X-goog-api-key header (AQ keys)", "POST /v1beta/models/gemini-flash-latest:generateContent with inline image + diagnosis + telemetry",
         "gemini-flash-latest used (gemini-2.5-flash retired for new users)"],
        ["OpenRouter", "sensor chat + vision fallback", "Authorization: Bearer sk-or-v1-…", "POST /api/v1/chat/completions (OpenAI-compatible)",
         "8-model text chain + 5-model vision chain over 435 models"],
    ]
    t = Table([[Paragraph(c, S["table-h"]) for c in rows[0]]] +
              [[Paragraph(c, S["table"]) for c in r] for r in rows[1:]],
              colWidths=[100, 108, 76, 138, 69])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY_700),
        ("GRID", (0,0), (-1,-1), 0.6, LINE),
        ("FONTSIZE", (0,0), (-1,-1), 7.9), ("LEADING", (0,0), (-1,-1), 10.5),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, MIST]),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    subhead("Why so many models?")
    story.append(P("Free AI models rotate, retire, and throttle. Rather than trust one, Verde builds <b>fallback chains</b>: "
                   "if the first model is busy or gone, the next takes over. The text chat has an 8-model chain, the vision "
                   "chat a 5-model chain — so the assistant never dead-ends on a queue."))
    spacer(6)
    fig("assets/img/plant_doctor.png", CONTENT_W * 0.5, caption="The Plant Doctor in action",
        sub="crop.health reads the photo; Gemini explains it")
    quote("The camera captures it. crop.health names it. Gemini explains it. OpenRouter keeps the conversation going when "
          "any single model gets busy.", accent=EMERALD)

def build_features():
    divider_page(lambda c: divider(c, 7, "Features",
        "Everything that works today —\nnothing here is a mock-up",
        icon="7", accent=EMERALD))
    sec("Chapter 07 — Features")
    section_title("07", "ALL LIVE", "Twelve features, zero placeholders",
                  lead="Every feature below was built, tested, and demoed on real hardware. There is no 'coming soon' and "
                       "no static mock-up.")
    feats = [
        ("Live telemetry", "8 sensor tiles, sparklines, trend arrows"),
        ("Auto watering", "moisture + tank + rain, all three checks"),
        ("Manual control", "user-driven, still tank-protected"),
        ("UV grow light", "light-threshold auto-switch, no flicker"),
        ("Tank calibration", "SET EMPTY / SET FULL, no reflash"),
        ("Camera capture", "ESP32-CAM photo on demand, ≤2 s"),
        ("Plant Doctor", "crop.health diagnosis + treatment plan"),
        ("AI vision chat", "Gemini sees the same analysed photo"),
        ("AI sensor chat", "OpenRouter, 8-model fallback chain"),
        ("Live weather", "Delhi forecast + 3-min rain override"),
        ("Moisture history", "chart with threshold marker"),
        ("Fullscreen demo mode", "judge-friendly exhibition display"),
    ]
    rows = []
    for i in range(0, len(feats), 3):
        row = []
        for name, desc in feats[i:i+3]:
            card = (F'<font color="#0EA35A" size="12">●</font>&nbsp;&nbsp;<b>{name}</b><br/>'
                    f'<font color="#5B6B78" size="8.2">{desc}</font>')
            row.append(Paragraph(card, S["table"]))
        while len(row) < 3:
            row.append(Paragraph("", S["table"]))
        rows.append(row)
    t = Table(rows, colWidths=[CONTENT_W/3]*3)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CARD_BG),
        ("GRID", (0,0), (-1,-1), 0.7, LINE),
        ("LEFTPADDING", (0,0), (-1,-1), 12), ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 12), ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [white, MIST]),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    callout("The fullscreen demo mode",
            "One tap and the dashboard fills the screen with big live tiles — built specifically so a judge at an "
            "exhibition can read everything from a few feet away.",
            icon="▣", accent=GOLD)

def build_testing():
    divider_page(lambda c: divider(c, 8, "Testing & Troubleshooting",
        "Thirteen checkpoints passed, ten real bugs\nfixed, and the journal to prove it",
        icon="8", accent=EMERALD))
    sec("Chapter 08 — Testing")
    section_title("08", "TEST MATRIX", "Thirteen points, all PASS",
                  lead="This is not a list of things that 'should' work. Each line is a test we ran, on the bench, and "
                       "watched pass in front of us.")
    tests = [
        "WiFi / boot", "DHT11 breathe test", "moisture water-dunk",
        "LDR cover test", "ultrasonic hand test", "pump AUTO 120 s (no glitch)",
        "pump OFF exactly at threshold", "tank lock", "rain override",
        "CAM capture ≤ 2 s", "Plant Doctor 94% diagnosis",
        "AI chats + fallback chains", "watchdog 10+ min (0 reboots)",
    ]
    rows = [[Paragraph(f'<font color="#0EA35A" size="10">✔</font>', S["table"]),
             Paragraph(t, S["table"])] for t in tests]
    t = Table(rows, colWidths=[40, CONTENT_W - 40])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CARD_BG),
        ("GRID", (0,0), (-1,-1), 0.6, LINE),
        ("LEFTPADDING", (0,0), (-1,-1), 12), ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [white, MIST]),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    subhead("Troubleshooting journal — ten bugs we actually hit")
    bugs = [
        ("AUTO 10 s pump loop", "17 blocking calls/sec → JSON bundling (2 calls/sec)"),
        ("Camera probe 0x106", "FPC ribbon unseated → reseat gold-side down + power cycle"),
        ("PSRAM not found", "weak power → 5 V / 2 A adapter"),
        ("0x20002 boot crash", "camera+WiFi power surge → sequential boot"),
        ("RF interference", "20 MHz XCLK → throttle to 8 MHz"),
        ("67 W USB-PD charger starved the board", "→ 5 V / 2 A adapter"),
        ("Relay dead", "split breadboard rails → bridge + to +, − to −"),
        ("temp = 0", "DHT on wrong pin → GPIO 4 + shared GND"),
        ("Firebase 'spurts'", "13 calls/sec → one bundled call"),
        ("Compile 'missing terminating quote'", "copy-paste corruption → re-download file"),
    ]
    for num, (bug, fix) in enumerate(bugs, 1):
        row = Table([[Paragraph(f'<font color="#E4572E" size="9">BUG {num:02d}</font>', S["table"]),
                      Paragraph(f"<b>{bug}</b>", S["table"]),
                      Paragraph(f'<font color="#5B6B78">{fix}</font>', S["muted"])]],
                    colWidths=[60, 190, 241])
        row.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.5, LINE),
            ("BACKGROUND", (0,0), (-1,-1), white),
            ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10),
            ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))
        story.append(row)
        story.append(Spacer(1, 5))

def build_cost():
    divider_page(lambda c: divider(c, 9, "Cost & Sustainability",
        "₹1,890 for the build, free tiers forever,\nand a roadmap to solar",
        icon="9", accent=EMERALD))
    sec("Chapter 09 — Cost")
    section_title("09", "THE NUMBERS", "A ₹1,890 system that\nlooks like a startup's",
                  lead="Openness and honesty about money is part of the credibility. Here is exactly where every rupee "
                       "went — and how it stacks up against the commercial competition.")
    rows = [
        ["Electronics (ESP32, ESP32-CAM, 5 sensors, relay, pump, LED)", "₹1,320"],
        ["Power & protection (adapter, capacitors, diode)", "₹220"],
        ["Mechanical (breadboard, wires, enclosure)", "₹350"],
        ["Software & APIs (all free tiers)", "₹0"],
        ["Total", "≈ ₹1,890"],
    ]
    rows = [[cell(c, style="table-h") if ri == 4 else cell(c) for c in r] for ri, r in enumerate(rows)]
    t = Table(rows, colWidths=[CONTENT_W - 120, 120])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CARD_BG),
        ("GRID", (0,0), (-1,-1), 0.6, LINE),
        ("FONTSIZE", (0,0), (-1,-1), 9), ("LEADING", (0,0), (-1,-1), 12),
        ("LEFTPADDING", (0,0), (-1,-1), 12), ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("BACKGROUND", (0,-1), (-1,-1), NAVY_700),
        ("TEXTCOLOR", (0,-1), (-1,-1), white),
        ("ROWBACKGROUNDS", (0,0), (-1,-2), [white, MIST]),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    fig(D.cost_chart(), CONTENT_W * 0.82, caption="Ours vs the commercial kits",
        sub="we built it for ~22% of the price")
    spacer(4)
    subhead("Future scope")
    bullets([
        "<b>Solar autonomy</b> — 12 V panel + charge controller + battery for off-grid operation.",
        "<b>NPK soil probe</b> — go beyond moisture to actual nutrient levels.",
        "<b>Multi-plant zones</b> — one brain, many plants, per-zone decisions.",
        "<b>Telegram / WhatsApp alerts</b> — the plant pings you directly.",
        "<b>Predictive watering</b> — learn from the moisture log and water before it's dry.",
        "<b>Deployed Next.js dashboard</b> — already scaffolded, ready to go public.",
    ])

def build_tour():
    divider_page(lambda c: divider(c, 10, "Judge Tour & Conclusion",
        "A scripted three-minute walkthrough,\nso the demo tells its own story",
        icon="10", accent=EMERALD))
    sec("Chapter 10 — Judge Tour")
    section_title("10", "THE THREE-MINUTE TOUR", "What to say, and when",
                  lead="Hand a judge this script and the live demo, and let the project speak for itself.")
    steps = [
        ("0:00", "Hook", "\"This is Verde — a plant that waters itself and talks to AI. Built for ₹1,890, on free tiers.\""),
        ("0:20", "The problem", "\"Plants die from a lack of information — not a lack of love.\" Point at the dry soil and the empty-tank risk."),
        ("0:40", "Live telemetry", "Show the 8 dashboard tiles updating every second. \"Five sensors are reading the real world right now.\""),
        ("1:05", "Auto watering", "Wave a finger near the soil or talk through the rule: dry soil + safe tank + no rain → pump ON."),
        ("1:30", "The eyes", "Press CAPTURE. In ~2 s a fresh photo appears. \"The ESP32-CAM just photographed itself.\""),
        ("1:50", "Plant Doctor", "Point at the diagnosis. \"crop.health identified this at 94% and gave a treatment plan.\""),
        ("2:15", "AI chat", "Ask a question in the AI assistant. \"Gemini sees the same photo and answers in plain language.\""),
        ("2:40", "The bug story", "Mention the 17→2 fix. Judges love honesty: \"We crashed every 10 seconds and fixed it with JSON bundling.\""),
        ("3:00", "Cost & close", "\"₹1,890, all software free, every part understandable. The future is solar.\""),
    ]
    rows = []
    for t0, who, say in steps:
        rows.append([Paragraph(f'<font color="#0EA35A" size="9"><b>{t0}</b></font>', S["table"]),
                     Paragraph(f"<b>{who}</b>", S["table"]),
                     Paragraph(say, S["muted"])])
    t = Table(rows, colWidths=[54, 92, 345])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CARD_BG),
        ("GRID", (0,0), (-1,-1), 0.6, LINE),
        ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [white, MIST]),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    new_content()
    sec("Conclusion")
    section_title("CLOSING", "CONCLUSION", "A ₹1,890 plant with\na startup's confidence",
                  lead="Project Verde is proof that a serious, working IoT system doesn't need a big budget — it needs a "
                       "clear question, cheap parts, free tools, and the willingness to break things and fix them.")
    story.append(P("Two Class X students asked why a houseplant can't just tell us what it needs. The answer they built "
                   "reads five sensors, waters itself, takes photos, asks four AI services for help, and shows it all in "
                   "a web app — for less than ₹1,890. It is complete, demo-ready, and every part of it is understandable "
                   "by the person who built it."))
    spacer(6)
    quote("No black boxes. No ₹8,000 price tag. No 'AI' we can't explain. Just a plant that finally has a voice.",
          accent=EMERALD)
    spacer(10)
    kpi_row([F.KpiCard("100%", "tested & passing", "13-point matrix", accent=EMERALD),
             F.KpiCard("0", "watchdog reboots", "after the 17→2 fix", accent=GOLD),
             F.KpiCard("₹1,890", "total build cost", "all software free tiers", accent=EMERALD),
             F.KpiCard("4", "AI APIs", "all real, keyed, tested", accent=GOLD)])
    story.append(Spacer(1, 10))
    callout("Thank you for reading",
            "Project Verde · DAV ACON 5 Tech Exhibition 2026 · Aarav Choudhary & Anuj, Class X. "
            "The plant waters itself — and talks to AI.",
            icon="✓", accent=GOLD)

# ================================================================ ASSEMBLE
def main():
    global _doc
    # ensure charts exist
    D.moisture_chart(); D.cost_chart(); D.heartbeat_timeline()
    doc = VerdeDoc(OUT, pagesize=(PAGE_W, PAGE_H))
    fw = Frame(0, 0, PAGE_W, PAGE_H, id="full",
               leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    cw_frame = Frame(MARGIN, 46, CONTENT_W, PAGE_H - 46 - 70, id="content",
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="fullpage", frames=[fw], onPage=lambda c, d: None),
        PageTemplate(id="content", frames=[cw_frame], onPageEnd=content_bg),
    ])
    _doc = doc
    # seed story onto first (fullpage default)
    build_cover()
    build_60_seconds()
    build_contents()
    build_why()
    build_architecture()
    build_hardware()
    build_firmware()
    build_cloud()
    build_ai()
    build_features()
    build_testing()
    build_cost()
    build_tour()
    doc.build(story)
    try:
        import outline
        outline.add_outline(OUT)
    except Exception as e:
        print("outline skipped:", e)
    print("BUILT", OUT)
    return OUT

if __name__ == "__main__":
    main()
