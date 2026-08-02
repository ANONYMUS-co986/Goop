#!/usr/bin/env python3
"""Preprocess AI images for the PDF: crop-to-ratio, grade, FX overlays.
Also bakes reusable gradient strips and the demo QR code."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import qrcode

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "src")
PREP = os.path.join(ROOT, "assets", "prep")
os.makedirs(PREP, exist_ok=True)

def crop_to_ratio(im, ratio_w, ratio_h):
    """Crop image (centered-ish) to w/h = ratio_w/ratio_h."""
    w, h = im.size
    target = ratio_w / ratio_h
    cur = w / h
    if cur > target:  # too wide -> crop width
        nw = int(h * target)
        x0 = (w - nw) // 2
        return im.crop((x0, 0, x0 + nw, h))
    else:             # too tall -> crop height
        nh = int(w / target)
        y0 = (h - nh) // 3
        return im.crop((0, y0, w, y0 + nh))

def grade(im, bright=1.0, sat=1.12, contrast=1.06):
    im = ImageEnhance.Brightness(im).enhance(bright)
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    return im

def vignette(im, strength=0.45):
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-w * 0.25, -h * 0.25, w * 1.25, h * 1.25), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(w * 0.18))
    dark = Image.new("RGB", (w, h), (4, 14, 24))
    return Image.composite(im, dark, mask.point(lambda p: int(p * (1 - strength))))

def bottom_shade(im, height_frac=0.5, color=(6, 16, 26), max_alpha=215):
    """Dark gradient overlay from bottom up for text legibility."""
    w, h = im.size
    grad = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(grad)
    top = int(h * (1 - height_frac))
    for i in range(top, h):
        a = int(max_alpha * ((i - top) / max(1, h - top)) ** 1.3)
        d.line([(0, i), (w, i)], fill=a)
    overlay = Image.new("RGB", (w, h), color)
    return Image.composite(overlay, im, grad)

def top_shade(im, height_frac=0.35, color=(6, 16, 26), max_alpha=140):
    w, h = im.size
    grad = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(grad)
    bot = int(h * height_frac)
    for i in range(bot):
        a = int(max_alpha * (1 - i / max(1, bot)) ** 1.2)
        d.line([(0, i), (w, i)], fill=a)
    overlay = Image.new("RGB", (w, h), color)
    return Image.composite(overlay, im, grad)

def save(im, name, q=90):
    p = os.path.join(PREP, name)
    im.convert("RGB").save(p, quality=q)
    print("prep ->", p, im.size)

def make_gradients():
    def g(name, stops, vertical=True):
        W_, H_ = 24, 256
        im = Image.new("RGB", (W_, H_))
        d = ImageDraw.Draw(im)
        for y in range(H_):
            t = y / (H_ - 1)
            i = min(len(stops) - 2, int(t * (len(stops) - 2)))
            f = t * (len(stops) - 1) - i
            c1, c2 = stops[i], stops[i + 1]
            col = tuple(int(c1[k] + (c2[k] - c1[k]) * f) for k in range(3))
            d.line([(0, y), (W_, y)], fill=col)
        if not vertical:
            im = im.transpose(Image.ROTATE_90)
        im.save(os.path.join(PREP, name))
        print("grad ->", name)
    g("grad_navy_up.png",   [(8, 27, 41), (14, 45, 64), (10, 33, 47), (8, 27, 41)])
    g("grad_navy_v.png",    [(12, 38, 55), (8, 27, 41), (7, 20, 31)])
    g("grad_emerald.png",   [(16, 185, 129), (8, 120, 84), (8, 27, 41)])
    g("grad_gold.png",      [(242, 181, 61), (201, 138, 27), (8, 27, 41)])
    g("grad_ink.png",       [(16, 47, 66), (8, 27, 41)])
    # diagonal foil (gold -> deep) 512x256
    W_, H_ = 512, 256
    im = Image.new("RGB", (W_, H_))
    d = ImageDraw.Draw(im)
    for y in range(H_):
        for x in range(W_):
            t = (x / W_ + y / H_) / 2
            c = tuple(int(242 + (8 - 242) * t ** 1.4 + (k and 0 or 0)) for k in range(3))
            d.point((x, y), fill=(
                int(242 - 234 * t ** 1.5),
                int(181 - 154 * t ** 1.5),
                int(61 - 20 * t ** 1.2),
            ))
    im = im.filter(ImageFilter.GaussianBlur(1))
    im.save(os.path.join(PREP, "grad_foil.png"))
    print("grad -> grad_foil.png")

def make_qr():
    url = "https://verde-tech-haha-default-rtdb.firebaseio.com"
    qr = qrcode.QRCode(border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=(244, 241, 230), back_color=(8, 27, 41)).convert("RGB")
    img.save(os.path.join(PREP, "qr.png"))
    print("qr ->", img.size)

def main():
    # cover: A4 portrait ratio, bottom-heavy shading
    im = crop_to_ratio(Image.open(os.path.join(SRC, "cover.png")), 595, 842)
    im = grade(im, bright=0.96, sat=1.15, contrast=1.05)
    im = vignette(im, 0.35)
    im = top_shade(im, 0.42, max_alpha=150)
    im = bottom_shade(im, 0.62, max_alpha=235)
    im = im.resize((1190, 1682), Image.LANCZOS)
    save(im, "cover_prep.jpg")

    # bench: wide band, slight emerald grade
    im = crop_to_ratio(Image.open(os.path.join(SRC, "bench.png")), 16, 9)
    im = grade(im, bright=0.97, sat=1.18, contrast=1.08)
    im = vignette(im, 0.3)
    save(im, "bench_prep.jpg")

    # doctor: wide band
    im = crop_to_ratio(Image.open(os.path.join(SRC, "doctor.png")), 16, 9)
    im = grade(im, bright=0.99, sat=1.12, contrast=1.05)
    im = vignette(im, 0.25)
    save(im, "doctor_prep.jpg")

    # future: wide band
    im = crop_to_ratio(Image.open(os.path.join(SRC, "future.png")), 16, 9)
    im = grade(im, bright=0.98, sat=1.15, contrast=1.06)
    im = vignette(im, 0.3)
    save(im, "future_prep.jpg")

    make_gradients()
    make_qr()

if __name__ == "__main__":
    main()
