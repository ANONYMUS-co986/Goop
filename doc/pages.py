"""Page templates: full-page (cover/divider) flowable + content-page background/footer."""
from reportlab.lib.colors import white
from reportlab.platypus import Flowable
import theme as T

class FullPage(Flowable):
    """A flowable that draws over the entire page (used for cover & chapter dividers)."""
    def __init__(self, draw_fn, *args, gap=6):
        super().__init__()
        self.draw_fn = draw_fn
        self.args = args
        self.gap = gap  # leave a sliver so a following NextPageTemplate fits on the same page

    def wrap(self, aw, ah):
        return T.PAGE_W, T.PAGE_H - self.gap

    def draw(self):
        self.draw_fn(self.canv, *self.args)

def content_bg(canv, doc):
    """Draw the header + footer for standard content pages."""
    w, h = T.PAGE_W, T.PAGE_H
    # faint side accents
    canv.saveState()
    # top brand strip
    canv.setFillColor(T.NAVY_900)
    canv.rect(0, h - 54, w, 54, stroke=0, fill=1)
    # brand
    canv.setFillColor(T.EMERALD_2)
    canv.setFont("SG-Bold", 16)
    canv.drawString(T.MARGIN, h - 34, "PROJECT")
    canv.setFillColor(white)
    canv.drawString(T.MARGIN + 72, h - 34, "VERDE")
    # small leaf glyph
    canv.setFillColor(T.GOLD)
    canv.circle(T.MARGIN + 142, h - 31, 4, stroke=0, fill=1)
    # section label right
    sec = getattr(doc, "section", "")
    canv.setFillColor(T.EMERALD_2)
    canv.setFont("Inter-SemiBold", 8.5)
    canv.drawRightString(w - T.MARGIN, h - 34, sec.upper())
    # hairline under strip
    canv.setStrokeColor(T.GOLD); canv.setLineWidth(2)
    canv.line(0, h - 54, w, h - 54)
    # footer
    fy = 30
    canv.setFillColor(T.MUTED)
    canv.setFont("Inter", 8)
    canv.drawString(T.MARGIN, fy, "PROJECT VERDE  ·  DAV ACON 5 Tech Exhibition 2026")
    canv.drawRightString(w - T.MARGIN, fy, "green · digital · autonomous")
    # page number
    canv.setFillColor(T.NAVY)
    canv.setFont("SG-SemiBold", 10)
    canv.drawCentredString(w / 2, fy, str(doc.page))
    # small emerald dot footer accent
    canv.setFillColor(T.EMERALD)
    canv.rect(0, 0, w, 4, stroke=0, fill=1)
    canv.restoreState()
