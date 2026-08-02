"""Design system + low-level drawing helpers for the Project Verde document."""
import colorsys
from reportlab.lib.colors import Color, HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm, cm

# ---------------------------------------------------------------- palette
NAVY_900 = HexColor("#050D16")
NAVY_850 = HexColor("#071525")
NAVY_800 = HexColor("#0A1B2E")
NAVY_700 = HexColor("#0E2A47")
NAVY_600 = HexColor("#14395E")
NAVY_500 = HexColor("#1D4A77")
NAVY = NAVY_800
EMERALD  = HexColor("#17C96E")
EMERALD_2= HexColor("#2BD576")
EMERALD_D= HexColor("#0EA35A")
GOLD     = HexColor("#F5B14C")
GOLD_2   = HexColor("#E8A33D")
INK      = HexColor("#122A3B")
BODY     = HexColor("#24384A")
MUTED    = HexColor("#5B6B78")
SOFT     = HexColor("#EAF2EE")   # light mint tint
CARD_BG  = HexColor("#FFFFFF")
MIST     = HexColor("#F4F7F6")
LINE     = HexColor("#DCE6E1")
WARN     = HexColor("#E4572E")
GOOD     = EMERALD

PAGE_W, PAGE_H = A4
MARGIN = 52
CONTENT_W = PAGE_W - 2 * MARGIN   # 491
GOLDEN = 1.618

# ---------------------------------------------------------------- fonts
def register_fonts():
    pdfmetrics.registerFont(TTFont("Inter", "assets/fonts/Inter-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("Inter-Medium", "assets/fonts/Inter-Medium.ttf"))
    pdfmetrics.registerFont(TTFont("Inter-SemiBold", "assets/fonts/Inter-SemiBold.ttf"))
    pdfmetrics.registerFont(TTFont("Inter-Bold", "assets/fonts/Inter-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Inter-ExtraBold", "assets/fonts/Inter-ExtraBold.ttf"))
    pdfmetrics.registerFont(TTFont("SG", "assets/fonts/SpaceGrotesk-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("SG-Medium", "assets/fonts/SpaceGrotesk-Medium.ttf"))
    pdfmetrics.registerFont(TTFont("SG-SemiBold", "assets/fonts/SpaceGrotesk-SemiBold.ttf"))
    pdfmetrics.registerFont(TTFont("SG-Bold", "assets/fonts/SpaceGrotesk-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Mono", "assets/fonts/Mono-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("Mono-Bold", "assets/fonts/Mono-Bold.ttf"))

# ---------------------------------------------------------------- color utils
def blend(c1, c2, t):
    r = c1.red + (c2.red - c1.red) * t
    g = c1.green + (c2.green - c1.green) * t
    b = c1.blue + (c2.blue - c1.blue) * t
    a = c1.alpha + (c2.alpha - c1.alpha) * t
    return Color(r, g, b, a)

def with_alpha(hexcol, a):
    c = HexColor(hexcol) if isinstance(hexcol, str) else hexcol
    return Color(c.red, c.green, c.blue, alpha=a)

# ---------------------------------------------------------------- canvas helpers
def vgrad(canv, x, y, w, h, top, bottom, steps=64):
    """Vertical gradient from top color to bottom color."""
    canv.saveState()
    dh = h / steps
    for i in range(steps):
        t = i / (steps - 1)
        c = blend(top, bottom, t)
        canv.setFillColor(c)
        canv.rect(x, y + h - (i + 1) * dh, w, dh + 0.5, stroke=0, fill=1)
    canv.restoreState()

def hgrad(canv, x, y, w, h, left, right, steps=64):
    canv.saveState()
    dw = w / steps
    for i in range(steps):
        t = i / (steps - 1)
        c = blend(left, right, t)
        canv.setFillColor(c)
        canv.rect(x + i * dw, y, dw + 0.5, h, stroke=0, fill=1)
    canv.restoreState()

def rr(canv, x, y, w, h, r, fill=None, stroke=None, lw=1, dash=None, alpha=1):
    """Rounded rectangle path helper."""
    from reportlab.lib.colors import Color
    canv.saveState()
    canv.setLineJoin(1)
    if fill is not None:
        fc = fill if isinstance(fill, Color) else HexColor(fill)
        canv.setFillColor(Color(fc.red, fc.green, fc.blue, alpha=alpha))
    else:
        canv.setFillColor(white)
        canv.setFillAlpha(0)
    if stroke is not None:
        sc = stroke if isinstance(stroke, Color) else HexColor(stroke)
        canv.setStrokeColor(Color(sc.red, sc.green, sc.blue, alpha=alpha))
        canv.setLineWidth(lw)
        if dash:
            canv.setDash(dash[0], dash[1])
    else:
        canv.setStrokeColor(white)
        canv.setStrokeAlpha(0)
    d = min(w, h)
    r = min(r, d / 2)
    canv.roundRect(x, y, w, h, r, stroke=1, fill=1)
    canv.restoreState()

def glow(canv, x, y, r, col, a=0.25, rings=14):
    """Soft radial glow."""
    for i in range(rings, 0, -1):
        t = 1 - i / rings
        c = with_alpha(col, a * (1 - t))
        canv.setFillColor(c)
        canv.circle(x, y, r * (i / rings), stroke=0, fill=1)
