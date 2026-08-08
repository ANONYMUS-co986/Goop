#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R8 — GENERATION GAP: buff doge PAPA (1998) vs crying cheems ME (2026).
One-off house-style build (1440x1800). Template: imgflip 247758660 community blank (no watermark).
ZERO-TOLERANCE: all text bbox-measured; no emoji (font-tofu risk); cheems-speak carries the baby-voice."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT   = "/home/user/Goop"
FIN    = f"{ROOT}/vikaas-hq/studio/drops/FINALE"
OUT    = f"{FIN}/posts2"
STASH  = f"{ROOT}/vikaas-hq/studio/posts2_build/src_assets"
FONTS  = f"{ROOT}/vikaas-hq/studio/seed/fonts"
os.makedirs(OUT, exist_ok=True)

INK   = (7, 11, 8); PAPER = (239, 233, 220); ACID  = (185, 255, 63)
GREEN = (46, 222, 130); DEW = (234, 255, 244); RED  = (255, 77, 94)
GOLD  = (255, 211, 77); MUTE = (125, 134, 127)

def f_anton(sz): return ImageFont.truetype(f"{FONTS}/Anton.ttf", sz)
def f_mono(sz):  return ImageFont.truetype(f"{FONTS}/SpaceGrotesk.ttf", sz)
def f_dev(sz):   return ImageFont.truetype(f"{FONTS}/NotoSansDevanagari.ttf", sz)

def grain(img, amt=0.045, seed=11):
    rng = np.random.default_rng(seed)
    n = rng.normal(128, 42, (img.height, img.width)).clip(0, 255).astype(np.uint8)
    return Image.blend(img, Image.fromarray(n, "L").convert("RGB"), amt)

def autosize(d, text, fn, max_w, start, min_sz=24):
    sz = start
    while sz > min_sz:
        f = fn(sz)
        if max(d.textlength(l, font=f) for l in text.split("\n")) <= max_w: return f, sz
        sz -= 4
    return fn(min_sz), min_sz

def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def eyebrow(d, left):
    d.text((70, 64), left, font=f_mono(29), fill=MUTE)
    y = 116
    for x in range(70, 1370, 26): d.ellipse([x, y, x+4, y+4], fill=(63, 71, 64))

def has_dev(t): return any('ऀ' <= c <= 'ॿ' for c in t)

def footer(d, caption, stamp, stamp_bg=ACID):
    h = 216
    d.rectangle([0, 1800-h, 1440, 1800], fill=INK)
    d.line([0, 1800-h, 1440, 1800-h], fill=(63, 71, 64), width=3)
    sf0 = f_anton(42); w0 = d.textlength(stamp, font=sf0) + 50
    cap_w = (1440 - 70 - w0) - 110
    cap_font = f_dev(44) if has_dev(caption) else f_mono(40)
    lines = wrap(d, caption, cap_font, cap_w)
    y = 1800 - h + 44
    for ln in lines:
        lf = f_dev(44) if has_dev(ln) else f_mono(40)
        d.text((70, y), ln, font=lf, fill=DEW); y += 54
    d.text((70, y+4), "#EWasteOff · #ChangemakersWorldCup · @1m1bfoundation", font=f_mono(28), fill=MUTE)
    sf = f_anton(42); w_ = d.textlength(stamp, font=sf) + 50
    x0 = 1440-70-w_
    d.rounded_rectangle([x0, 1800-h+46, x0+w_, 1800-h+46+int(42*1.5)+24], radius=20, fill=stamp_bg)
    d.text((x0+w_/2, 1800-h+46+(int(42*1.5)+24)/2-2), stamp, font=sf, fill=INK, anchor="mm")
    d.text((x0, 1800-h+140), "the stamp is the point.", font=f_mono(26), fill=MUTE)

img = Image.new("RGB", (1440, 1800), INK)
d = ImageDraw.Draw(img)

eyebrow(d, "THE REMIXES · R8 — GENERATION GAP DIVISION")

# ── headline (autosized to <=1300, Anton) ──────────────────────────────
f1, sz1 = autosize(d, "EK PHONE, 22 SAAL.", f_anton, 1300, 108)
d.text((70, 150), "EK PHONE, 22 SAAL.", font=f1, fill=DEW)
h1 = d.textbbox((70, 150), "EK PHONE, 22 SAAL.", font=f1)[3]
f2, sz2 = autosize(d, "EK PHONE, 2 SAAL — 'OUTDATED'.", f_anton, 1300, 108)
d.text((70, h1 + 18), "EK PHONE, 2 SAAL — 'OUTDATED'.", font=f2, fill=ACID)
h2 = d.textbbox((70, h1 + 18), "EK PHONE, 2 SAAL — 'OUTDATED'.", font=f2)[3]

# ── template card (PAPER, rounded; VS pill on divider) ────────────────
CARD_T, CARD_B = max(h2 + 56, 430), 1062
CARD_L, CARD_R = 70, 1370
d.rounded_rectangle([CARD_L, CARD_T, CARD_R, CARD_B], radius=26, fill=PAPER)
tpl = Image.open(f"{STASH}/doge_cheems_247758660.png").convert("RGB")
tpl.thumbnail((CARD_R-CARD_L-56, CARD_B-CARD_T-56), Image.LANCZOS)
tx = CARD_L + (CARD_R-CARD_L - tpl.width)//2
ty = CARD_T + (CARD_B-CARD_T - tpl.height)//2
img.paste(tpl, (tx, ty))
cx = (CARD_L + CARD_R)//2
yy = CARD_T + 28
while yy < CARD_B - 28:                      # dashed centre divider
    d.line([cx, yy, cx, yy+14], fill=(198, 192, 176), width=4); yy += 26
pw = d.textlength("VS", font=f_anton(40)) + 44
d.rounded_rectangle([cx-pw/2, CARD_T-26, cx+pw/2, CARD_T+26], radius=22, fill=INK)
d.text((cx, CARD_T+1), "VS", font=f_anton(40), fill=ACID, anchor="mm")

# ── two-column captions under the card ────────────────────────────────
COL_W = 620
LX, RX = 70, 750
y_lab = CARD_B + 34
d.text((LX, y_lab), "PAPA · 1998", font=f_anton(52), fill=GOLD)
d.text((RX, y_lab), "ME · 2026",  font=f_anton(52), fill=RED)
y_lab_b = d.textbbox((LX, y_lab), "PAPA · 1998", font=f_anton(52))[3] + 18

fbody = f_mono(36)
for x, body, kick in (
    (LX, "ek phone. 22 saal. toota? repair karwa liya. aaj bhi utna hi bajta hai.",
     "(good morning forwards bhi daily. machine nahi, family member hai.)"),
    (RX, "guizzz mera phom 2 saal purana ho gaya. slowm chal raha. naya lemga ab.",
     "(drawer mein 5 laashein padi hain. koi poochta bhi nahi.)"),
):
    yy = y_lab_b
    for ln in wrap(d, body, fbody, COL_W):
        d.text((x, yy), ln, font=fbody, fill=DEW); yy += 50
    yy += 12
    for ln in wrap(d, kick, f_mono(30), COL_W):
        d.text((x, yy), ln, font=f_mono(30), fill=MUTE); yy += 42

# footer caption kept in latin Hinglish: fresh-venv Pillow lacks raqm → Devanagari
# shaping (pre-base i-matra / stacked anusvara) breaks. Mono SpaceGrotesk = always safe.
footer(d, "5 laashein drawer mein padi hain aur phone naya chahiye? pahle tolo, phir recycler ko do.", "TRUE STORY")

img = grain(img, amt=0.045)
img.save(f"{OUT}/R8_upgrade.jpg", quality=92)
print("saved R8_upgrade.jpg")

# quick zoom crops for QC
img.crop((0, 40, 1440, 430)).save("/tmp/r8_qc_headline.png")
img.crop((0, 420, 1440, 1120)).save("/tmp/r8_qc_card.png")
img.crop((0, 1080, 1440, 1500)).save("/tmp/r8_qc_captions.png")
img.crop((0, 1560, 1440, 1800)).save("/tmp/r8_qc_footer.png")
img.crop((700, 1560, 1440, 1800)).save("/tmp/r8_qc_stamp.png")
print("qc crops ok")
