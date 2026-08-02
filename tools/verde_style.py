#!/usr/bin/env python3
"""Project Verde — design system: palette, fonts, text engine, UI primitives."""
import os, re, math
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as _canvas_mod
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, HexColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "fonts", "static")
ASSET_DIR = os.path.join(ROOT, "assets")
PREP_DIR = os.path.join(ASSET_DIR, "prep")
QR_PATH = os.path.join(PREP_DIR, "qr.png")
GRAD_PATHS = {
    "navy_up":  os.path.join(PREP_DIR, "grad_navy_up.png"),
    "navy_v":   os.path.join(PREP_DIR, "grad_navy_v.png"),
    "emerald":  os.path.join(PREP_DIR, "grad_emerald.png"),
    "gold":     os.path.join(PREP_DIR, "grad_gold.png"),
    "foil":     os.path.join(PREP_DIR, "grad_foil.png"),
    "ink":      os.path.join(PREP_DIR, "grad_ink.png"),
}

PAGE_W, PAGE_H = A4  # 595.27 x 841.89
M_L, M_R, M_T, M_B = 54, 54, 62, 52

# ---------------- palette (dark default; "print" variant flips) ----------------
DARK = dict(
    bg=HexColor("#081B29"), bg2=HexColor("#0C2637"), card=HexColor("#102F42"),
    card2=HexColor("#0D2A3B"), line=HexColor("#1D4557"),
    emerald=HexColor("#10B981"), emerald_d=HexColor("#0A8A63"), mint=HexColor("#6EE7B7"),
    gold=HexColor("#F2B53D"), gold_l=HexColor("#FFD77A"), gold_d=HexColor("#C98A1B"),
    ivory=HexColor("#F4F1E6"), slate=HexColor("#A9C0CB"), slate_d=HexColor("#6E8A96"),
    red=HexColor("#F9706B"), red_d=HexColor("#C0504A"), red_bg=HexColor("#3A1E22"),
    green_bg=HexColor("#12352B"), gold_bg=HexColor("#3A2E14"),
    white=HexColor("#FFFFFF"),
)
LIGHT = dict(
    bg=HexColor("#FFFFFF"), bg2=HexColor("#F2F6F4"), card=HexColor("#FFFFFF"),
    card2=HexColor("#EDF4F1"), line=HexColor("#C9DAD4"),
    emerald=HexColor("#0B8A5F"), emerald_d=HexColor("#086B49"), mint=HexColor("#0E9F6E"),
    gold=HexColor("#B47B12"), gold_l=HexColor("#D99E1F"), gold_d=HexColor("#8F5E0A"),
    ivory=HexColor("#14293B"), slate=HexColor("#4A6370"), slate_d=HexColor("#7C929E"),
    red=HexColor("#C0392B"), red_d=HexColor("#A22B1F"), red_bg=HexColor("#FBE9E7"),
    green_bg=HexColor("#E4F4EC"), gold_bg=HexColor("#FBF3DF"),
    white=HexColor("#FFFFFF"),
)

PAL = dict(DARK)          # current palette — swapped by variant
VARIANT = "dark"

# ---------------- fonts ----------------
F = {}
_FONT_FILES = {
    "Inter-Regular": "Inter-Regular.ttf", "Inter-Medium": "Inter-Medium.ttf",
    "Inter-SemiBold": "Inter-SemiBold.ttf", "Inter-Bold": "Inter-Bold.ttf",
    "Inter-ExtraBold": "Inter-ExtraBold.ttf", "Inter-Black": "Inter-Black.ttf",
    "Fraunces-Regular": "Fraunces-Regular.ttf", "Fraunces-SemiBold": "Fraunces-SemiBold.ttf",
    "Fraunces-Bold": "Fraunces-Bold.ttf", "Fraunces-Black": "Fraunces-Black.ttf",
    "JBMono-Regular": "JBMono-Regular.ttf", "JBMono-Bold": "JBMono-Bold.ttf",
    "JBMono-ExtraBold": "JBMono-ExtraBold.ttf",
}
FB = {}  # semantic font shortcuts

def register_fonts():
    for name, fn in _FONT_FILES.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fn)))
    FB["body"] = "Inter-Regular"; FB["body_m"] = "Inter-Medium"; FB["body_sb"] = "Inter-SemiBold"
    FB["body_b"] = "Inter-Bold"; FB["body_eb"] = "Inter-ExtraBold"; FB["body_bl"] = "Inter-Black"
    FB["disp"] = "Fraunces-Regular"; FB["disp_sb"] = "Fraunces-SemiBold"
    FB["disp_b"] = "Fraunces-Bold"; FB["disp_bl"] = "Fraunces-Black"
    FB["mono"] = "JBMono-Regular"; FB["mono_b"] = "JBMono-Bold"; FB["mono_eb"] = "JBMono-ExtraBold"

def sw(t, f, s):
    return pdfmetrics.stringWidth(t, f, s)

# ---------------- mini-markup -> runs ----------------
_COLOR_KEYS = {"g": "gold", "gl": "gold_l", "e": "emerald", "m": "mint", "r": "red",
               "s": "slate", "sd": "slate_d", "i": "ivory", "n": "navy_text", "w": "white"}

def _color_of(key):
    k = key.lower()
    if k == "navy_text":
        return PAL["ivory"] if VARIANT == "dark" else PAL["navy_text"]
    return PAL.get(_COLOR_KEYS.get(k, "ivory"), PAL["ivory"])

def parse_runs(text, base_color=None, base_bold=False, base_mono=False):
    """Parse **bold**, `mono`, {g:...} colored spans -> list of (txt, font, color)."""
    if base_color is None:
        base_color = PAL["ivory"]
    runs = []
    # pass 1: color spans
    parts = re.split(r"(\{[a-zA-Z]+:.*?\})", text)
    for part in parts:
        if not part:
            continue
        cm = re.match(r"\{([a-zA-Z]+):(.*)\}$", part)
        if cm:
            col = _color_of(cm.group(1))
            inner = cm.group(2)
        else:
            col = base_color
            inner = part
        # pass 2: bold / mono
        for tok in re.split(r"(\*\*.+?\*\*|`[^`]+`)", inner):
            if not tok:
                continue
            if tok.startswith("**") and tok.endswith("**"):
                runs.append((tok[2:-2], FB["body_b"], col))
            elif tok.startswith("`") and tok.endswith("`"):
                runs.append((tok[1:-1], FB["mono"], col))
            else:
                if base_mono:
                    runs.append((tok, FB["mono"], col))
                elif base_bold:
                    runs.append((tok, FB["body_b"], col))
                else:
                    runs.append((tok, FB["body"], col))
    return runs

def runs_width(runs, size):
    return sum(sw(t, f, size) for t, f, _ in runs)

def wrap_runs(runs, width, size):
    """Word-wrap runs to width -> list of lines; each line is a list of runs.
    Hard line breaks (`\\n` inside a run) force a new line."""
    lines, cur, cur_w = [], [], 0.0
    for t, f, col in runs:
        segs = t.split("\n")
        for si, seg in enumerate(segs):
            if si > 0:
                lines.append(cur); cur, cur_w = [], 0.0
            if seg == "":
                continue
            words = re.split(r"(\s+)", seg)
            for w in words:
                if w == "":
                    continue
                ww = sw(w, f, size)
                if cur and cur_w + ww > width and w.strip() != "":
                    lines.append(cur); cur, cur_w = [], 0.0
                cur.append((w, f, col)); cur_w += ww
    if cur:
        lines.append(cur)
    return lines

def draw_par(c, x, ytop, text, width, size=9.5, leading=14, color=None, align="left",
             bold=False, mono=False, max_lines=None):
    """Draw paragraph at top-based y. Returns next ytop."""
    if color is None:
        color = PAL["ivory"]
    if isinstance(text, str):
        runs = parse_runs(text, base_color=color, base_bold=bold, base_mono=mono)
    else:
        runs = text
    lines = wrap_runs(runs, width, size)
    if max_lines:
        lines = lines[:max_lines]
    y = ytop - size
    for line in lines:
        w = runs_width(line, size)
        if align == "right":
            x0 = x + width - w
        elif align == "center":
            x0 = x + (width - w) / 2.0
        else:
            x0 = x
        for t, f, col in line:
            c.setFont(f, size); c.setFillColor(col)
            c.drawString(x0, y, t)
            x0 += sw(t, f, size)
        y -= leading
    return ytop - len(lines) * leading

def measure_par(text, width, size=9.5, leading=14, color=None):
    if isinstance(text, str):
        runs = parse_runs(text, base_color=color or PAL["ivory"])
    else:
        runs = text
    return len(wrap_runs(runs, width, size)) * leading

# ---------------- canvas helpers ----------------
def rrect(c, x, y, w, h, r, fill=None, stroke=None, sw_=1, dash=None):
    c.saveState()
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke); c.setLineWidth(sw_)
        if dash:
            c.setDash(dash[0], dash[1])
    else:
        c.setStrokeColor(PAL["bg"]); c.setLineWidth(0)
    c.roundRect(x, y, w, h, r, stroke=(stroke is not None), fill=(fill is not None))
    c.restoreState()

def shadow_rrect(c, x, y, w, h, r, fill, shadow=None, dy=3, blur=0):
    if shadow is None:
        shadow = Color(0, 0, 0, 0.28)
    c.saveState()
    c.setFillColor(shadow)
    c.roundRect(x + 0, y - dy, w, h + dy, r, stroke=0, fill=1)
    c.restoreState()
    rrect(c, x, y, w, h, r, fill=fill)

def hrule(c, x, y, w, color, width=1):
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(width)
    c.line(x, y, x + w, y); c.restoreState()

def grad_image(c, key, x, y, w, h, alpha=1.0):
    if VARIANT == "print":          # keep print variant clean & ink-friendly
        return
    p = GRAD_PATHS.get(key)
    if not p or not os.path.exists(p):
        return
    c.saveState(); c.setFillAlpha(alpha)
    c.drawImage(p, x, y, width=w, height=h, mask="auto", preserveAspectRatio=False)
    c.restoreState()

def dotgrid(c, x, y, w, h, spacing=16, color=None, alpha=0.25, r=0.55):
    if color is None:
        color = PAL["slate"]
    c.saveState()
    c.setFillColor(color); c.setFillAlpha(alpha)
    yy = y + spacing / 2
    while yy < y + h:
        xx = x + spacing / 2
        while xx < x + w:
            c.circle(xx, yy, r, stroke=0, fill=1)
            xx += spacing
        yy += spacing
    c.restoreState()

def chip(c, x, ytop, text, font=None, size=7.5, color=None, bg=None, padx=9, pady=4,
         border=None, radius=10):
    """Small uppercase label chip. Returns (x_end, ytop)."""
    font = font or FB["mono_b"]
    color = color or PAL["emerald"]
    w = sw(text, font, size) + padx * 2
    h = size + pady * 2
    if bg is not None or border is not None:
        rrect(c, x, ytop - h, w, h, radius, fill=bg, stroke=border, sw_=0.8)
    c.setFont(font, size); c.setFillColor(color)
    c.drawString(x + padx, ytop - h / 2 - size / 2.8, text)
    return x + w, ytop

def footer(c, page_no, total, section=""):
    y = 30
    hrule(c, M_L, y + 8, PAGE_W - M_L - M_R, PAL["line"], 0.7)
    c.setFont(FB["mono"], 6.3); c.setFillColor(PAL["slate_d"])
    c.drawString(M_L, y, "PROJECT VERDE  ·  DAV ACON 5 — TECH EXHIBITION 2026")
    c.drawString(PAGE_W / 2, y, section.upper())
    c.setFillColor(PAL["gold"] if VARIANT == "dark" else PAL["gold_d"])
    c.drawRightString(PAGE_W - M_R, y, f"{page_no:02d} / {total:02d}")

def page_header(c, section_label, ytop=46):
    c.setFont(FB["mono"], 6.8); c.setFillColor(PAL["slate_d"])
    c.drawRightString(PAGE_W - M_R, PAGE_H - ytop + 8, section_label.upper())
    hrule(c, M_L, PAGE_H - ytop, PAGE_W - M_L - M_R, PAL["line"], 0.6)

def section_header(c, kicker, title, subtitle, ytop, x=None, w=None, num=None,
                   title_size=27, rule=True):
    x = x if x is not None else M_L
    w = w if w is not None else PAGE_W - M_L - M_R
    if num is not None:
        c.setFont(FB["disp_bl"], 40); c.setFillColor(PAL["line"])
        c.drawString(x, ytop - 30, f"{num:02d}")
        tx = x + 44
    else:
        tx = x
    if kicker:
        chip(c, tx, ytop, kicker, size=7.6, bg=PAL["green_bg"], color=PAL["emerald"])
        ytop -= 20
    c.setFont(FB["disp_b"], title_size); c.setFillColor(PAL["ivory"])
    c.drawString(tx, ytop - title_size - 6, title)
    if subtitle:
        c.setFont(FB["body"], 9.5); c.setFillColor(PAL["slate"])
        c.drawString(tx, ytop - title_size - 26, subtitle)
    if rule:
        yy = ytop - title_size - 40
        hrule(c, tx, yy, 52, PAL["gold"], 2.2)
        c.setFillColor(PAL["emerald"]); c.circle(tx + 56, yy + 0.6, 1.6, stroke=0, fill=1)
    return ytop - title_size - 58

# ---------------- icons (simple line glyphs) ----------------
def icon(c, cx, cy, kind, size=12, color=None, sw_=1.6):
    """Draw a simple stroke icon centered at (cx,cy) in a size box."""
    color = color or PAL["emerald"]
    c.saveState()
    c.setStrokeColor(color); c.setLineWidth(sw_); c.setLineCap(1); c.setLineJoin(1)
    c.setFillColor(color)
    s = size
    def P(pt):
        return (cx + (pt[0] - 0.5) * s, cy + (pt[1] - 0.5) * s)
    def F(pts):
        out = []
        for pt in pts:
            out.extend(P(pt))
        return out
    if kind == "drop":
        p = c.beginPath()
        p.moveTo(*P((0.5, 0.86)))
        p.curveTo(*F([(0.18, 0.62), (0.2, 0.3), (0.5, 0.08)]))
        p.curveTo(*F([(0.8, 0.3), (0.82, 0.62), (0.5, 0.86)]))
        p.close(); c.drawPath(p, stroke=1, fill=0)
    elif kind == "sun":
        c.circle(cx, cy, s * 0.2, stroke=1, fill=0)
        for a in range(0, 360, 45):
            x1, y1 = cx + s * 0.34 * math.cos(math.radians(a)), cy + s * 0.34 * math.sin(math.radians(a))
            x2, y2 = cx + s * 0.46 * math.cos(math.radians(a)), cy + s * 0.46 * math.sin(math.radians(a))
            c.line(x1, y1, x2, y2)
    elif kind == "chip":
        rrect(c, cx - s * 0.34, cy - s * 0.34, s * 0.68, s * 0.68, 2, fill=None, stroke=color, sw_=sw_)
        for dx, dy in [(-0.34, 0), (0.34, 0), (0, -0.34), (0, 0.34)]:
            c.line(cx + dx * s - s * 0.07, cy + dy * s, cx + dx * s + s * 0.07, cy + dy * s)
    elif kind == "cloud":
        p = c.beginPath()
        p.moveTo(*P((0.14, 0.38)))
        p.curveTo(*F([(0.0, 0.38), (0.04, 0.16), (0.26, 0.18)]))
        p.curveTo(*F([(0.28, 0.0), (0.52, -0.02), (0.64, 0.12)]))
        p.curveTo(*F([(0.92, 0.04), (1.0, 0.34), (0.86, 0.4)]))
        p.curveTo(*F([(1.0, 0.52), (0.92, 0.7), (0.72, 0.68)]))
        p.lineTo(*P((0.28, 0.68)))
        p.curveTo(*F([(0.06, 0.72), (-0.02, 0.52), (0.14, 0.38)]))
        p.close(); c.drawPath(p, stroke=1, fill=0)
    elif kind == "leaf":
        p = c.beginPath()
        p.moveTo(*P((0.08, 0.92)))
        p.curveTo(*F([(0.84, 0.68), (0.84, 0.16), (0.08, 0.08)]))
        p.curveTo(*F([(0.3, 0.52), (0.38, 0.8), (0.08, 0.92)]))
        p.close(); c.drawPath(p, stroke=1, fill=0)
        c.line(*P((0.16, 0.62)), *P((0.8, 0.14)))
    elif kind == "camera":
        rrect(c, cx - s * 0.42, cy - s * 0.3, s * 0.84, s * 0.6, 3, fill=None, stroke=color, sw_=sw_)
        rrect(c, cx - s * 0.16, cy + s * 0.06, s * 0.32, s * 0.12, 1, fill=None, stroke=color, sw_=sw_)
        c.circle(cx, cy - s * 0.04, s * 0.17, stroke=1, fill=0)
    elif kind == "wifi":
        for r_ in (0.42, 0.28, 0.14):
            p = c.beginPath()
            p.moveTo(cx - r_ * s * math.cos(math.radians(20)), cy - s * 0.3 + r_ * s * math.sin(math.radians(20)))
            for a in range(20, 161, 4):
                p.lineTo(cx + r_ * s * math.cos(math.radians(a)), cy - s * 0.3 + r_ * s * math.sin(math.radians(a)))
            c.drawPath(p, stroke=1, fill=0)
        c.circle(cx, cy - s * 0.34, s * 0.05, stroke=0, fill=1)
    elif kind == "cpu":
        rrect(c, cx - s * 0.3, cy - s * 0.3, s * 0.6, s * 0.6, 1.5, fill=None, stroke=color, sw_=sw_)
        for dx, dy in [(-0.3, -0.15), (-0.3, 0.15), (0.3, -0.15), (0.3, 0.15), (-0.15, -0.3), (0.15, -0.3), (-0.15, 0.3), (0.15, 0.3)]:
            c.line(cx + dx * s, cy + dy * s, cx + dx * s + (0.08 if dx > 0 else -0.08) * s, cy + dy * s)
    elif kind == "bolt":
        p = c.beginPath()
        p.moveTo(*P((0.56, 0.96)))
        p.lineTo(*P((0.2, 0.46)))
        p.lineTo(*P((0.48, 0.46)))
        p.lineTo(*P((0.44, 0.04)))
        p.lineTo(*P((0.8, 0.54)))
        p.lineTo(*P((0.52, 0.54)))
        p.close(); c.drawPath(p, stroke=1, fill=0)
    elif kind == "check":
        p = c.beginPath()
        p.moveTo(*P((0.16, 0.5)))
        p.lineTo(*P((0.42, 0.76)))
        p.lineTo(*P((0.86, 0.2)))
        c.drawPath(p, stroke=1, fill=0)
    elif kind == "alert":
        p = c.beginPath()
        p.moveTo(*P((0.5, 0.9)))
        p.lineTo(*P((0.18, 0.3)))
        p.lineTo(*P((0.82, 0.3)))
        p.close(); c.drawPath(p, stroke=1, fill=0)
        c.line(*P((0.5, 0.56)), *P((0.5, 0.34)))
        c.circle(*P((0.5, 0.2)), s * 0.05, stroke=0, fill=1)
    elif kind == "clock":
        c.circle(cx, cy, s * 0.4, stroke=1, fill=0)
        c.line(cx, cy, cx, cy + s * 0.24)
        c.line(cx, cy, cx + s * 0.16, cy - s * 0.02)
    elif kind == "shield":
        p = c.beginPath()
        p.moveTo(*P((0.5, 0.94)))
        p.lineTo(*P((0.16, 0.8)))
        p.lineTo(*P((0.16, 0.4)))
        p.curveTo(*F([(0.16, 0.16), (0.4, 0.08), (0.5, 0.04)]))
        p.curveTo(*F([(0.6, 0.08), (0.84, 0.16), (0.84, 0.4)]))
        p.lineTo(*P((0.84, 0.8)))
        p.close(); c.drawPath(p, stroke=1, fill=0)
        c.setStrokeColor(color); c.line(*P((0.36, 0.46)), *P((0.48, 0.6)))
        c.line(*P((0.48, 0.6)), *P((0.66, 0.36)))
    elif kind == "flask":
        p = c.beginPath()
        p.moveTo(*P((0.36, 0.84)))
        p.lineTo(*P((0.64, 0.84)))
        p.lineTo(*P((0.6, 0.54)))
        p.lineTo(*P((0.86, 0.16)))
        p.lineTo(*P((0.14, 0.16)))
        p.lineTo(*P((0.4, 0.54)))
        p.close(); c.drawPath(p, stroke=1, fill=0)
        c.line(*P((0.32, 0.34)), *P((0.68, 0.34)))
    elif kind == "gear":
        c.circle(cx, cy, s * 0.16, stroke=1, fill=0)
        for a in range(0, 360, 45):
            x1, y1 = cx + s * 0.24 * math.cos(math.radians(a)), cy + s * 0.24 * math.sin(math.radians(a))
            x2, y2 = cx + s * 0.38 * math.cos(math.radians(a)), cy + s * 0.38 * math.sin(math.radians(a))
            c.line(x1, y1, x2, y2)
    elif kind == "heart":
        p = c.beginPath()
        p.moveTo(*P((0.5, 0.2)))
        p.curveTo(*F([(0.02, 0.58), (0.3, 0.96), (0.5, 0.62)]))
        p.curveTo(*F([(0.7, 0.96), (0.98, 0.58), (0.5, 0.2)]))
        p.close(); c.drawPath(p, stroke=1, fill=0)
    elif kind == "signal":
        for i, h in enumerate([0.12, 0.24, 0.36]):
            rrect(c, cx - s * 0.3 + i * s * 0.22, cy - s * 0.42, s * 0.14, h * s, 1, fill=color, stroke=None)
    elif kind == "book":
        p = c.beginPath()
        p.moveTo(*P((0.1, 0.9)))
        p.lineTo(*P((0.1, 0.16)))
        p.curveTo(*F([(0.32, 0.06), (0.62, 0.06), (0.9, 0.2)]))
        p.lineTo(*P((0.9, 0.9)))
        p.curveTo(*F([(0.62, 0.76), (0.32, 0.76), (0.1, 0.9)]))
        c.drawPath(p, stroke=1, fill=0)
    elif kind == "money":
        rrect(c, cx - s * 0.42, cy - s * 0.3, s * 0.84, s * 0.6, 3, fill=None, stroke=color, sw_=sw_)
        c.circle(cx, cy, s * 0.16, stroke=1, fill=0)
    elif kind == "eye":
        p = c.beginPath()
        p.moveTo(*P((0.08, 0.5)))
        p.curveTo(*F([(0.24, 0.78), (0.76, 0.78), (0.92, 0.5)]))
        p.curveTo(*F([(0.76, 0.22), (0.24, 0.22), (0.08, 0.5)]))
        p.close(); c.drawPath(p, stroke=1, fill=0)
        c.circle(cx, cy, s * 0.14, stroke=1, fill=0)
    elif kind == "plant":
        c.line(*P((0.5, 0.7)), *P((0.5, 0.08)))
        p = c.beginPath()
        p.moveTo(*P((0.5, 0.66)))
        p.curveTo(*F([(0.16, 0.78), (0.2, 0.96), (0.5, 0.9)]))
        p.curveTo(*F([(0.8, 0.96), (0.84, 0.78), (0.5, 0.66)]))
        c.drawPath(p, stroke=1, fill=0)
        p = c.beginPath()
        p.moveTo(*P((0.5, 0.52)))
        p.curveTo(*F([(0.2, 0.62), (0.24, 0.8), (0.5, 0.74)]))
        c.drawPath(p, stroke=1, fill=0)
        p = c.beginPath()
        p.moveTo(*P((0.5, 0.4)))
        p.curveTo(*F([(0.8, 0.5), (0.76, 0.68), (0.5, 0.62)]))
        c.drawPath(p, stroke=1, fill=0)
    elif kind == "phone":
        rrect(c, cx - s * 0.22, cy - s * 0.44, s * 0.44, s * 0.88, 3, fill=None, stroke=color, sw_=sw_)
        c.line(*P((0.42, 0.84)), *P((0.58, 0.84)))
    elif kind == "db":
        for i in range(3):
            p = c.beginPath()
            yc = 0.66 - i * 0.16
            p.moveTo(*P((0.14, yc)))
            p.curveTo(*F([(0.14, yc + 0.14), (0.86, yc + 0.14), (0.86, yc)]))
            p.curveTo(*F([(0.86, yc - 0.14), (0.14, yc - 0.14), (0.14, yc)]))
            p.close()
            c.drawPath(p, stroke=1, fill=0)
    elif kind == "target":
        c.circle(cx, cy, s * 0.4, stroke=1, fill=0)
        c.circle(cx, cy, s * 0.24, stroke=1, fill=0)
        c.circle(cx, cy, s * 0.09, stroke=1, fill=0)
    elif kind == "upload":
        c.line(*P((0.5, 0.86)), *P((0.5, 0.14)))
        p = c.beginPath()
        p.moveTo(*P((0.3, 0.62)))
        p.lineTo(*P((0.5, 0.36)))
        p.lineTo(*P((0.7, 0.62)))
        c.drawPath(p, stroke=1, fill=0)
        c.line(*P((0.22, 0.14)), *P((0.78, 0.14)))
    c.restoreState()


def icon_circle(c, cx, cy, kind, d=30, color=None, bg=None, sw_=1.7):
    if bg is None:
        bg = PAL["card"]
    color = color or PAL["emerald"]
    c.saveState()
    c.setFillColor(bg)
    c.circle(cx, cy, d / 2, stroke=0, fill=1)
    c.setStrokeColor(PAL["line"]); c.setLineWidth(0.8)
    c.circle(cx, cy, d / 2, stroke=1, fill=0)
    c.restoreState()
    icon(c, cx, cy, kind, size=d * 0.52, color=color, sw_=sw_)
