"""Custom ReportLab flowables for the Verde document."""
from reportlab.lib import colors
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Flowable, Table, TableStyle, Paragraph
from reportlab.platypus.flowables import Image
import theme as T

def _hex(c):
    return c if isinstance(c, Color) else HexColor(c)

def _blend(c1, c2, t):
    a = _hex(c1); b = _hex(c2)
    return Color(a.red + (b.red - a.red) * t,
                 a.green + (b.green - a.green) * t,
                 a.blue + (b.blue - a.blue) * t,
                 a.alpha + (b.alpha - a.alpha) * t)

class RoundedImage(Flowable):
    """An image with rounded corners + optional frame / caption baked under."""
    def __init__(self, path, width, height=None, radius=10, border=None,
                 caption=None, pad=0):
        super().__init__()
        self.path = path
        self.w = width
        self.img = ImageReader(path)
        iw, ih = self.img.getSize()
        self.h = height if height else width * ih / iw
        self.radius = radius
        self.border = border
        self.caption = caption
        self.pad = pad
        if caption:
            self._cap = caption

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        w, h = self.w, self.h
        r = self.radius
        # draw image clipped to rounded rect by drawing with alpha mask via rect path
        path = c.beginPath()
        d = min(w, h); r = min(r, d / 2)
        path.roundRect(0, 0, w, h, r)
        c.saveState()
        c.clipPath(path, stroke=0, fill=0)
        c.drawImage(self.path, 0, 0, width=w, height=h, preserveAspectRatio=True, anchor="c")
        c.restoreState()
        if self.border:
            c.setStrokeColor(_hex(self.border)); c.setLineWidth(1.5)
            path2 = c.beginPath(); path2.roundRect(0.5, 0.5, w - 1, h - 1, r)
            c.drawPath(path2, stroke=1, fill=0)

class ImgFigure(Flowable):
    """Rounded image + caption strip below."""
    def __init__(self, path, width, radius=10, caption=None, sub=None,
                 caption_color=T.NAVY, bg=T.CARD_BG, border=None, height=None):
        super().__init__()
        self.path = path
        self.w = width
        self.img = ImageReader(path)
        iw, ih = self.img.getSize()
        self.img_h = height if height else width * ih / iw
        self.radius = radius
        self.caption = caption
        self.sub = sub
        self.caption_color = caption_color
        self.bg = bg
        self.border = border
        self._cap_h = 0
        if caption or sub:
            self._cap_h = 22 if caption else 0
            if sub: self._cap_h += 16
            self._cap_h += 10

    def wrap(self, aw, ah):
        return self.w, self.img_h + self._cap_h

    def draw(self):
        c = self.canv
        w, h = self.w, self.img_h
        r = self.radius
        d = min(w, h); r = min(r, d / 2)
        path = c.beginPath(); path.roundRect(0, 0, w, h, r)
        c.saveState()
        c.clipPath(path, stroke=0, fill=0)
        c.drawImage(self.path, 0, 0, width=w, height=h, preserveAspectRatio=True, anchor="c")
        c.restoreState()
        if self.border:
            c.setStrokeColor(_hex(self.border)); c.setLineWidth(1.2)
            p2 = c.beginPath(); p2.roundRect(0.5, 0.5, w - 1, h - 1, r)
            c.drawPath(p2, stroke=1, fill=0)
        y = h + 8
        if self.caption:
            c.setFillColor(_hex(self.caption_color))
            c.setFont("SG-SemiBold", 11)
            c.drawString(2, y + 8, self.caption)
            y -= 13
        if self.sub:
            c.setFillColor(T.MUTED); c.setFont("Inter", 8.5)
            c.drawString(2, y + 4, self.sub)

class KpiCard(Flowable):
    """A hero-number KPI card: big number + label + optional caption."""
    def __init__(self, number, label, sub="", w=110, h=118,
                 accent=T.EMERALD, bg=None, number_color=None):
        super().__init__()
        self.number = number; self.label = label; self.sub = sub
        self.w = w; self.h = h; self.accent = accent
        self.bg = bg or T.CARD_BG
        self.number_color = number_color or T.NAVY

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        w, h = self.w, self.h
        r = 14
        path = c.beginPath(); path.roundRect(0, 0, w, h, r)
        c.saveState()
        if self.bg:
            c.setFillColor(_hex(self.bg)); c.drawPath(path, stroke=1, fill=1)
        # accent top strip
        c.setFillColor(_hex(self.accent))
        p2 = c.beginPath(); p2.roundRect(0, h - 5, w, 5, 2.5)
        c.drawPath(p2, stroke=0, fill=1)
        c.restoreState()
        c.setFillColor(_hex(self.number_color))
        c.setFont("SG-Bold", 30)
        c.drawString(14, h - 44, self.number)
        c.setFillColor(T.NAVY); c.setFont("Inter-SemiBold", 9.5)
        c.drawString(14, h - 58, self.label)
        if self.sub:
            c.setFillColor(T.MUTED); c.setFont("Inter", 7.5)
            c.drawString(14, h - 72, self.sub)

class MiniStat(Flowable):
    """Small inline stat used in tables/rows: bold number + tiny label stacked."""
    def __init__(self, number, label, w=90, accent=T.EMERALD, align="center"):
        super().__init__()
        self.number = number; self.label = label; self.w = w; self.h = 52
        self.accent = accent; self.align = align

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        cx = self.w / 2 if self.align == "center" else 8
        anchor = "middle" if self.align == "center" else "start"
        c.setFillColor(_hex(self.accent)); c.setFont("SG-Bold", 20)
        c.drawCentredString(cx, 26, self.number)
        c.setFillColor(T.NAVY); c.setFont("Inter", 7.5)
        if self.align == "center":
            c.drawCentredString(cx, 12, self.label)
        else:
            c.drawString(8, 12, self.label)

class Callout(Flowable):
    """A tinted callout box with an icon dot, title and body lines."""
    def __init__(self, title, body, icon="!", w=T.CONTENT_W,
                 bg=T.SOFT, accent=T.EMERALD, icon_color=None, h=64):
        super().__init__()
        self.title = title; self.body = body
        self.w = w; self.bg = bg; self.accent = accent
        self.icon = icon; self.icon_color = icon_color or accent
        self.text_w = w - 64
        # word wrap body
        self.body_lines = self._wrap(body, "Inter", 9.5)
        n = len(self.body_lines)
        self.h = max(h or 0, 30 + n * 13 + 12)

    def _wrap(self, text, font, size):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        lines = []
        for para in text.split("\n"):
            words = para.split(" ")
            cur = ""
            for wd in words:
                test = (cur + " " + wd).strip()
                if stringWidth(test, font, size) <= self.text_w:
                    cur = test
                else:
                    if cur: lines.append(cur)
                    cur = wd
            if cur: lines.append(cur)
        return lines

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        w, h = self.w, self.h
        r = 12
        path = c.beginPath(); path.roundRect(0, 0, w, h, r)
        c.setFillColor(_hex(self.bg)); c.drawPath(path, stroke=1, fill=1)
        # icon circle
        cx, cy = 26, h / 2
        c.setFillColor(_hex(self.accent))
        c.circle(cx, cy, 13, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("SG-Bold", 15)
        c.drawCentredString(cx, cy - 5, self.icon)
        c.setFillColor(T.NAVY); c.setFont("Inter-SemiBold", 11)
        c.drawString(48, h - 20, self.title)
        c.setFillColor(T.BODY); c.setFont("Inter", 9.5)
        ty = h - 34
        for ln in self.body_lines:
            c.drawString(48, ty, ln)
            ty -= 13

class PullQuote(Flowable):
    def __init__(self, text, w=T.CONTENT_W, accent=T.GOLD, fontsize=15):
        super().__init__()
        self.text = text; self.w = w; self.accent = accent; self.fontsize = fontsize
        import math
        nlines = 0
        # rough estimate
        self.h = 60

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        c.setFillColor(_hex(self.accent)); c.rect(0, 4, 4, self.h - 8, stroke=0, fill=1)
        c.setFillColor(T.NAVY); c.setFont("SG-Medium", self.fontsize)
        # word wrap manually
        words = self.text.split(" ")
        lines = []; cur = ""
        from reportlab.pdfbase.pdfmetrics import stringWidth
        for wd in words:
            test = (cur + " " + wd).strip()
            if stringWidth(test, "SG-Medium", self.fontsize) <= self.w - 26:
                cur = test
            else:
                if cur: lines.append(cur)
                cur = wd
        if cur: lines.append(cur)
        self._lines = lines
        c.saveState()
        ty = self.h - 8
        for ln in lines[:3]:
            c.drawString(18, ty, ln)
            ty -= self.fontsize + 3
        c.restoreState()
