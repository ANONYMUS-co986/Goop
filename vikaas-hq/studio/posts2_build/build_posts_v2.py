#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SERIES 02 — THE REMIXES: old 7 concepts, new-formula bodies. 1440x1800 each."""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT   = "/home/user/Goop"
FIN    = f"{ROOT}/vikaas-hq/studio/drops/FINALE"
OUT    = f"{FIN}/posts2"
SRC    = f"{ROOT}/vikaas-hq/studio/drops/v5/remix_src"
STASH  = f"{ROOT}/image-search"
FONTS  = f"{ROOT}/vikaas-hq/studio/seed/fonts"
os.makedirs(OUT, exist_ok=True)

INK   = (7, 11, 8); PAPER = (239, 233, 220); ACID  = (185, 255, 63)
GREEN = (46, 222, 130); DEW = (234, 255, 244); RED  = (255, 77, 94)
GOLD  = (255, 211, 77); MUTE = (125, 134, 127); VIOLET = (167, 139, 250)
CREAM = (244, 236, 214); BROWN = (52, 34, 18); BLUE = (11, 43, 84)

def f_anton(sz): return ImageFont.truetype(f"{FONTS}/Anton.ttf", sz)
def f_arch(sz):  return ImageFont.truetype(f"{FONTS}/Archivo.ttf", sz)
def f_mono(sz):  return ImageFont.truetype(f"{FONTS}/SpaceGrotesk.ttf", sz)
def f_dev(sz):   return ImageFont.truetype(f"{FONTS}/NotoSansDevanagari.ttf", sz)

def grain(img, amt=0.05, seed=11):
    rng = np.random.default_rng(seed)
    n = rng.normal(128, 42, (img.height, img.width)).clip(0, 255).astype(np.uint8)
    return Image.blend(img, Image.fromarray(n, "L").convert("RGB"), amt)

def fit(img, w, h, mode="contain"):
    return ImageOps.fit(img, (w, h), Image.LANCZOS) if mode == "cover" else (lambda im: (im.thumbnail((w, h), Image.LANCZOS), im)[1])(img.copy())

def autosize(d, text, fn, max_w, start, min_sz=24):
    sz = start
    while sz > min_sz:
        f = fn(sz)
        lines = text.split("\n")
        if max(d.textlength(l, font=f) for l in lines) <= max_w: return f, sz
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

def has_dev(t):
    return any('\u0900' <= c <= '\u097f' for c in t)

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

def rot_paste(base, layer, cx, cy, angle):
    l2 = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    base.paste(l2, (int(cx - l2.width/2), int(cy - l2.height/2)), l2 if l2.mode == "RGBA" else None)
    return l2

def shadow_card(size, radius=0, shadow=18, blur=12):
    """card + its soft shadow layer"""
    card = Image.new("RGBA", (size[0]+shadow*2, size[1]+shadow*2), (0,0,0,0))
    sd = ImageDraw.Draw(card)
    sd.rounded_rectangle([shadow, shadow+6, shadow+size[0], shadow+size[1]+6], radius=radius, fill=(0,0,0,150))
    card = card.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(blur))
    face = Image.new("RGBA", card.size, (0,0,0,0))
    fd = ImageDraw.Draw(face)
    fd.rounded_rectangle([shadow-2, shadow-2, shadow-2+size[0], shadow-2+size[1]], radius=radius, fill=CREAM)
    return Image.alpha_composite(card, face), shadow

def bubble(img, cx, cy, w, h, text, tail="left", font_fn=None, start=44, fg=(12,12,12)):
    """white speech bubble with tail; text centered; returns bbox"""
    d = ImageDraw.Draw(img)
    layer = Image.new("RGBA", (int(w+140), int(h+140)), (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    bx, by = layer.width/2, layer.height/2
    ld.rounded_rectangle([bx-w/2, by-h/2, bx+w/2, by+h/2], radius=34, fill=(255,255,255,255), outline=(10,10,10,255), width=7)
    if tail == "left":
        ld.polygon([(bx-w/2+30, by+h/2-24), (bx-w/2-42, by+h/2+30), (bx-w/2+88, by+h/2+6)], fill=(255,255,255,255), outline=(10,10,10,255))
    else:
        ld.polygon([(bx+w/2-30, by+h/2-24), (bx+w/2+42, by+h/2+30), (bx+w/2-88, by+h/2+6)], fill=(255,255,255,255), outline=(10,10,10,255))
    fn = font_fn or f_arch
    f, sz = autosize(ld, text, fn, w-70, start, min_sz=24)
    ld.multiline_text((bx, by), text, font=f, fill=fg+(255,), anchor="mm", align="center", spacing=int(f.size*0.16))
    img.paste(layer, (int(cx-layer.width/2), int(cy-layer.height/2)), layer)

def narr(img, x, y, text, angle=-2, sz=30):
    d = ImageDraw.Draw(img)
    f = f_mono(sz)
    w = d.textlength(text, font=f) + 46; h = int(sz*1.9)
    lay = Image.new("RGBA", (int(w)+24, h+16), (0,0,0,0))
    ld = ImageDraw.Draw(lay)
    ld.rectangle([8, 8, w+8, h+8], fill=(255, 228, 94, 255))
    ld.rectangle([8, 8, w+8, h+8], outline=(20,20,20,255), width=4)
    ld.text((8 + w/2, 8 + h/2 - 2), text, font=f, fill=(15,15,15,255), anchor="mm")
    rot_paste(img, lay, x + w/2, y + h/2, angle)

posts = {}

# ============ R1 — THE MUSEUM #001 (old P1 anthem) ============
def r1():
    img = Image.new("RGB", (1440, 1800), INK); d = ImageDraw.Draw(img)
    art = fit(Image.open(f"{SRC}/R1_museum_blank.png").convert("RGB"), 1440, 1800, "cover")
    img.paste(art, (0,0)); d = ImageDraw.Draw(img)
    d.text((70, 58), "THE REMIXES · R1/7 — MUSEUM #001 (P1, RESTORED)", font=f_mono(27), fill=(176,186,178))
    f, sz = autosize(d, "KABHI KAAM\nAAYEGA.", f_anton, 1240, 168)
    d.multiline_text((720, 108), "KABHI KAAM\nAAYEGA.", font=f, fill=DEW, anchor="ma", align="center", spacing=int(f.size*0.04))
    uy = 108 + len("KABHI KAAM\nAAYEGA.".split("\n"))*f.size*1.02 + 30
    d.rectangle([590, uy, 850, uy+10], fill=ACID)
    d.text((720, uy+34), "कभी काम आएगा।” — said every dead charger, 2014–forever", font=f_dev(46), fill=ACID, anchor="ma")
    # plaque
    card, sh = shadow_card((960, 250))
    pd_ = ImageDraw.Draw(card)
    pd_.text((sh+30, sh+20), "EXHIBIT 001 — “CHARGER” (2014–PRESENT)", font=f_mono(32), fill=BROWN)
    pd_.text((sh+30, sh+74), "mixed media on drawer · donated by EVERY INDIAN HOUSEHOLD", font=f_mono(28), fill=(110,86,60))
    pd_.line([sh+26, sh+122, sh+934, sh+122], fill=(180,150,110), width=2)
    pd_.text((sh+30, sh+140), "verdict: it never did. recycle it instead.", font=f_anton(52), fill=(120,20,20))
    rot_paste(img, card, 720, 1466, -1.5)
    footer(d, "the national drawer anthem. LIE no. 001 — documented, framed, hung.", "LIE no.001 · TRUE")
    posts["R1_museum"] = grain(img)

# ============ R2 — LOST: 15 RECYCLERS (old P2 ledger) ============
def r2():
    img = Image.new("RGB", (1440, 1800), INK); d = ImageDraw.Draw(img)
    eyebrow(d, "THE REMIXES · R2/7 — LOST HANDBILL (P2, RESTORED)")
    pole = Image.open(f"{STASH}/street-utility-pole-covered-in-flyers-pa-1.jpg").convert("RGB")
    pole = fit(pole, 1150, 1400, "cover")
    img.paste(pole, (145, 210))
    d.rectangle([139, 204, 145+pole.width+5, 210+pole.height+5], outline=ACID, width=4)
    # the flyer
    FW, FH = 840, 1030
    card, sh = shadow_card((FW, FH))
    pd_ = ImageDraw.Draw(card)
    cx = sh + FW/2
    pd_.text((cx, sh+30), "L O S T", font=f_anton(150), fill=BROWN, anchor="ma")
    pd_.text((cx, sh+196), "15 AUTHORISED\nRECYCLERS", font=f_anton(78), fill=(15,60,30), anchor="ma", align="center", spacing=8)
    pd_.text((cx, sh+368), "last seen: inside the haryana govt list (HSPCB).\nabandoned by all 0 of gurgaon’s doorsteps.\nfor a 1–2 kg household lot they said “500 kg lao”. okay.", font=f_mono(30), fill=(60,45,30), anchor="ma", align="center", spacing=10)
    pd_.line([sh+50, sh+612, sh+FW-50, sh+612], fill=BROWN, width=3)
    pd_.text((cx, sh+636), "REWARD: ₹40-ISH CASH* + A CLEAN DRAWER", font=f_anton(46), fill=(120,20,20), anchor="ma")
    pd_.text((cx, sh+700), "*actual weighed rate: ₹40 for 1.4 kg. receipts in bio.", font=f_mono(26), fill=(110,86,60), anchor="ma")
    # tear-off tabs
    ty = sh + FH - 296
    for i in range(6):
        x0 = sh + 34 + i * ((FW-68)/6)
        pd_.line([x0, ty, x0, ty+178], fill=(160,130,100), width=2)
    pd_.line([sh+34, ty, sh+FW-34, ty], fill=(160,130,100), width=3)
    for i in range(6):
        x0 = sh + 34 + (i+0.5) * ((FW-68)/6)
        tab = Image.new("RGBA", (200, 40), (0,0,0,0))
        td = ImageDraw.Draw(tab)
        td.text((100, 20), "TAKE ONE · TAULO KARO", font=f_mono(26), fill=BROWN+(255,), anchor="mm")
        rot = tab.rotate(90, expand=True)
        card.paste(rot, (int(x0-20), ty+14), rot)
    # tape strips
    for (tx, tyy, ang) in [(sh+FW/2-180, sh-16, -3), (sh+FW/2+170, sh-12, 4)]:
        tape = Image.new("RGBA", (150, 44), (185,255,63,170))
        card.alpha_composite(tape, (int(tx-75), int(tyy-22)))
    rot_paste(img, card, 720, 905, -2.0)
    # red diagonal double-stamp
    st = Image.new("RGBA", (620, 210), (0,0,0,0))
    sd = ImageDraw.Draw(st)
    sd.rectangle([8, 8, 612, 202], outline=(200,30,40,255), width=8)
    sd.text((310, 70), "DOORSTEP COUNT:", font=f_mono(38), fill=(200,30,40,255), anchor="mm")
    sd.text((310, 148), "0 (ZERO)", font=f_anton(94), fill=(200,30,40,255), anchor="mm")
    st = st.resize((int(st.width*0.88), int(st.height*0.88)), Image.LANCZOS)
    rot_paste(img, st, 1050, 330, -11)
    footer(d, "the infrastructure exists. the doorstep doesn’t. the list is public — we just never look.", "SOURCED · HSPCB")
    posts["R2_lost"] = grain(img)

# ============ R3 — E-WASTE SAGA #01 RESTORED (old P3 comic) ============
def r3():
    img = Image.new("RGB", (1440, 1800), INK); d = ImageDraw.Draw(img)
    eyebrow(d, "THE REMIXES · R3/7 — SAGA #01 RESTORED (P3)")
    rows = [
        ("R3_p1_blank.png", False, "aaj recycle karke hi\nrahunga.", "PANEL 1 · THE MISSION"),
        ("R3_p2_blank.png", True,  "“500 KG minimum,\nbeta.” — the authorised gate", "PANEL 2 · THE GATE"),
        ("R3_p3_blank.png", False, "PPEEEEP! → “₹40. horn\nsuna tha na?”", "PANEL 3 · THE HORN"),
    ]
    y = 178
    for fname, flip, txt, chip in rows:
        pan = fit(Image.open(f"{SRC}/{fname}").convert("RGB"), 470, 470)
        px = 110 if not flip else 860
        img.paste(pan, (px, y))
        d.rectangle([px-6, y-6, px+476, y+476], outline=ACID, width=4)
        bx = 880 if not flip else 380
        bubble(img, bx, y+170, 480, 200, txt, tail="left" if not flip else "right", start=40)
        narr(img, bx-230, y+396, chip, angle=2 if flip else -2, sz=30)
        y += 470 + 24
    footer(d, "hero → gate → horn. a true story in three panels. moral: doorstep missing, comedy available.", "TRUE STORY · ₹40")
    posts["R3_saga"] = grain(img)

# ============ R4 — THE MINE BLUEPRINT (old P4, code-drawn cyanotype) ============
def r4():
    img = Image.new("RGB", (1440, 1800), BLUE); d = ImageDraw.Draw(img)
    GRID = (21, 64, 110); GRID2 = (30, 84, 140)
    for x in range(0, 1441, 44): d.line([x, 0, x, 1800], fill=GRID, width=1)
    for y in range(0, 1801, 44): d.line([0, y, 1440, y], fill=GRID, width=1)
    for x in range(0, 1441, 220): d.line([x, 0, x, 1800], fill=GRID2, width=2)
    for y in range(0, 1801, 220): d.line([0, y, 1440, y], fill=GRID2, width=2)
    W_ = (220, 235, 255); DIM = (150, 190, 230)
    d.text((70, 56), "THE REMIXES · R4/7 — DWG 004 (P4, REDRAWN)", font=f_mono(28), fill=DIM)
    d.text((70, 110), "IT ISN’T RUBBISH.", font=f_anton(104), fill=(245,250,255))
    d.text((70, 226), "IT’S A MINE.", font=f_anton(104), fill=ACID)
    # exploded phone — left column
    cx = 380
    slabs = [("top", 470, 420, 170), ("mid", 720, 420, 150), ("bot", 950, 460, 190)]
    d.line([cx, 400, cx, 1230], fill=DIM, width=2)
    for yy in range(400, 1235, 24): d.line([cx-10, yy, cx+10, yy], fill=DIM, width=2)
    # body slab
    d.rounded_rectangle([cx-210, 950, cx+210, 1140], radius=26, outline=W_, width=4)
    d.rounded_rectangle([cx-186, 978, cx+186, 1112], radius=18, outline=DIM, width=2)
    d.ellipse([cx-16, 1148, cx+16, 1180], outline=W_, width=3)
    # board slab
    d.rounded_rectangle([cx-210, 720, cx+210, 870], radius=10, outline=W_, width=4)
    for (ox, oy, s) in [(-150,-44,72),(-30,-30,54),(66,-50,84),(-120,16,54),(30,14,64)]:
        d.rectangle([cx+ox, 720+75+oy-s/2, cx+ox+s, 720+75+oy+s/2], outline=W_, width=3)
    for i in range(7):
        y0 = 750 + i*16
        d.line([cx-200, y0, cx-60, y0], fill=DIM, width=2)
        d.line([cx+60, y0+8, cx+200, y0+8], fill=DIM, width=2)
    d.ellipse([cx-10, 788, cx+10, 808], fill=GOLD)  # the gold speck
    # battery slab
    d.rounded_rectangle([cx-175, 470, cx+175, 640], radius=14, outline=W_, width=4)
    d.polygon([(cx+8, 500), (cx-38, 570), (cx-4, 570), (cx-16, 612), (cx+34, 536), (cx-2, 536)], outline=W_, fill=None)
    d.polygon([(cx+8, 500), (cx-38, 570), (cx-4, 570), (cx-16, 612), (cx+34, 536), (cx-2, 536)], outline=W_)
    d.rectangle([cx-40, 456, cx+40, 470], outline=W_, width=3)
    # camera + speaker floats
    d.ellipse([cx-40, 330, cx+40, 410], outline=W_, width=4); d.ellipse([cx-14, 356, cx+14, 384], outline=DIM, width=3)
    d.rounded_rectangle([cx-90, 262, cx+90, 292], radius=15, outline=W_, width=3)
    for i in range(5): d.ellipse([cx-60+i*28, 272, cx-52+i*28, 280], fill=DIM)
    # callouts → right labels
    callouts = [
        (cx+92, 798, 640, 700, "BOARD — GOLD TRACES, ~0.03 G / PHONE", "[ESTIMATE · SOURCES.md]"),
        (cx+176, 560, 640, 470, "BATTERY — LITHIUM: RESPECT THE CHEMISTRY", "[SOURCED · 3.2 MT/YR, CWC]"),
        (cx+92, 1164, 640, 1150, "PORTS — COPPER: CHECK TODAY’S RATE", "[DAILY OBSERVATION]"),
        (cx-212, 1040, 640, 950, "BODY — ALU + GLASS: CASH-BACK PART", "[WEIGHED · ₹40 LOT]"),
    ]
    for x0, y0, tx, ty, l1, l2 in callouts:
        d.line([x0, y0, tx, ty], fill=DIM, width=2)
        d.line([tx, ty, tx+236, ty], fill=DIM, width=2)
        d.ellipse([x0-6, y0-6, x0+6, y0+6], fill=ACID)
        xf = tx if tx > 700 else 640
        d.text((640, ty-66), l1, font=f_mono(30), fill=(235,244,252))
        d.text((640, ty-28), l2, font=f_mono(26), fill=ACID)
        d.line([640, ty+8, 876, ty+8], fill=DIM, width=1)
    # big stat
    d.text((70, 1300), "~0.03 g", font=f_anton(120), fill=ACID)
    d.text((70, 1432), "gold in every phone. one drawer ≈ a micro mine.\nthe ore is free — you already paid for it.", font=f_mono(34), fill=(215,230,245), spacing=8)
    # title block
    d.rectangle([70, 1524, 1370, 1632], outline=W_, width=3)
    for i, (k, v) in enumerate([("DWG", "004 — THE MINE"), ("USER LOT", "3 PHONES · 7 CHARGERS · 1 BANK"), ("SCALE", "1 : 1.4 KG"), ("ASSAYER", "MY KITCHEN SCALE")]):
        x = 94 + i * 322
        d.text((x, 1546), k, font=f_mono(24), fill=DIM)
        d.text((x, 1582), v, font=f_mono(26), fill=(240,248,255))
        if i: d.line([x-22, 1540, x-22, 1616], fill=DIM, width=1)
    footer_y = 1656
    d.rectangle([0, footer_y, 1440, 1800], fill=(8, 31, 62))
    d.text((720, footer_y+34), "recycle = india’s cheapest mine. #EWasteOff · #ChangemakersWorldCup · @1m1bfoundation", font=f_mono(30), fill=DIM, anchor="ma")
    # stamp
    sf = f_anton(46); st = "ESTIMATE · NOT JUNK"
    w_ = d.textlength(st, font=sf) + 56
    d.rounded_rectangle([1440-70-w_, footer_y+76, 1440-70, footer_y+76+84], radius=20, fill=ACID)
    d.text((1440-70-w_/2, footer_y+76+42), st, font=sf, fill=INK, anchor="mm")
    d.text((70, footer_y+96), "the stamp is the point.", font=f_mono(26), fill=DIM)
    posts["R4_mine"] = grain(img, amt=0.035)

# ============ R5 — TIER LIST (old P5 board) ============
def r5():
    img = Image.new("RGB", (1440, 1800), INK); d = ImageDraw.Draw(img)
    eyebrow(d, "THE REMIXES · R5/7 — TIER SCIENCE DEPT. (P5, RESTORED)")
    d.text((70, 148), "कबाड़ी UNIVERSE", font=f_dev(84), fill=DEW)
    d.text((76, 250), "TIER LIST", font=f_anton(96), fill=ACID)
    d.text((1010, 168), "tier science dept.\ndispute in comments.", font=f_mono(28), fill=MUTE, anchor="ma", align="center", spacing=8)
    rows = [
        ("S", GOLD,   f"{STASH}/kabadiwala-india-street-scrap-collector--2.png", "कबाड़ीवाला", "doorstep king. zero questions. horn supremacy."),
        ("A", GREEN,  f"{STASH}/phone-repair-shop-hands-screwdriver-tool-1.jpg", "गली का repair भैया", "one screwdriver. full confidence. no billing app."),
        ("B", (154, 230, 110), f"{STASH}/recycling-factory-gate-entrance-industri-2.jpg", "authorised recycler", "right place, wrong vibe — “500 kg minimum” energy."),
        ("C", VIOLET, f"{STASH}/drawer-full-of-old-phones-chargers-cable-1.jpg", "drawer में ताड़ी मारना", "the national conservation strategy. “kabhi kaam aayega.”"),
        ("F", RED,    f"{STASH}/e-waste-pile-old-mobile-phones-circuit-b-2.jpg", "कूड़ेदान में फेंकना", "battery-fire speedrun. WHAT are we even doing."),
    ]
    y = 400
    for letter, col, th, name, sub in rows:
        h = 238
        d.rounded_rectangle([70, y, 1370, y+h-18], radius=20, fill=(13, 19, 15), outline=(40, 48, 42), width=2)
        d.rounded_rectangle([70, y, 240, y+h-18], radius=20, fill=col)
        d.rectangle([200, y, 240, y+h-18], fill=col)
        d.text((155, y+(h-18)/2), letter, font=f_anton(130), fill=INK, anchor="mm")
        try:
            thi = fit(Image.open(th).convert("RGB"), 190, 190, "cover")
            mask = Image.new("L", (190, 190), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, 190, 190], radius=14, fill=255)
            img.paste(thi, (262, y+14), mask)
            d.rounded_rectangle([262, y+14, 452, y+204], radius=14, outline=(70, 80, 72), width=3)
        except Exception as e:
            print("thumb fail", th, e)
        d.text((486, y+46), name, font=f_dev(58), fill=DEW)
        d.text((490, y+124), sub, font=f_mono(31), fill=MUTE)
        y += h
    d.text((70, y+6), "S-tier non-negotiable. the rest of the alphabet is also correct.", font=f_mono(30), fill=MUTE)
    footer(d, "कबाड़ी universe tier list — राय रखने से पहले अपना drawer तौल लेना.", "THE LAW · SCIENCE")
    posts["R5_tierlist"] = grain(img)

# ============ R6 — WANTED: THE 2014 CHARGER (old P6 etiquette) ============
def r6():
    img = Image.new("RGB", (1440, 1800), INK); d = ImageDraw.Draw(img)
    art = Image.open(f"{SRC}/R6_wanted_blank.png").convert("RGB")
    art = fit(art, 1440, 1690, "cover")
    img.paste(art, (0, 40)); d = ImageDraw.Draw(img)
    INKB = (58, 36, 16)
    f, sz = autosize(d, "WANTED", f_anton, 1200, 218)
    d.text((720, 108), "WANTED", font=f, fill=INKB, anchor="ma")
    d.rectangle([270, 118+ f.size*1.02, 1170, 118+f.size*1.02+8], fill=INKB)
    d.text((720, 364), "THE 2014 CHARGER", font=f_anton(104), fill=INKB, anchor="ma")
    d.text((720, 1296), "aliases: “kabhi kaam aayega” · “backup cable” · “woh wala grey one”", font=f_mono(33), fill=INKB, anchor="ma")
    d.text((720, 1344), "crimes: fleeing every dustbin since 2014 · occupying premium drawer real estate", font=f_mono(33), fill=INKB, anchor="ma")
    d.line([300, 1400, 1140, 1400], fill=INKB, width=3)
    f2, _ = autosize(d, "REWARD: ₹40 CASH + PEACE OF DRAWER", f_anton, 1180, 72)
    d.text((720, 1428), "REWARD: ₹40 CASH + PEACE OF DRAWER", font=f2, fill=(120, 24, 20), anchor="ma")
    d.text((720, 1518), "[ WEIGHED — our scale. 1.4 kg lot. ]", font=f_mono(28), fill=(110, 80, 50), anchor="ma")
    d.text((720, 1630), "TAG THE ACCOMPLICE KEEPING HIM.", font=f_anton(74), fill=INKB, anchor="ma")
    shadow = Image.new("RGBA", img.size, (0,0,0,0))
    footer_h = 0
    # stamp + footer strip over parchment
    d.rectangle([0, 1800-118, 1440, 1800], fill=(7,11,8))
    d.line([0, 1800-118, 1440, 1800-118], fill=ACID, width=4)
    d.text((70, 1800-84), "drawer etiquette 101 — don’t bin it, cash it. #EWasteOff · #ChangemakersWorldCup · @1m1bfoundation", font=f_mono(29), fill=MUTE)
    sf = f_anton(40); stt = "WEIGHED · ₹40"
    w_ = d.textlength(stt, font=sf) + 46
    d.rounded_rectangle([1440-58-w_, 1800-200, 1440-58, 1800-200+74], radius=18, fill=ACID)
    d.text((1440-58-w_/2, 1800-200+37), stt, font=sf, fill=INK, anchor="mm")
    posts["R6_wanted"] = grain(img, amt=0.045)

# ============ R7 — THE RECEIPT (old P7 protocol) ============
def r7():
    img = Image.new("RGB", (1440, 1800), INK); d = ImageDraw.Draw(img)
    eyebrow(d, "THE REMIXES · R7/7 — HOW I PROVE THINGS (P7, RESTORED)")
    d.text((1010, 66), "MISSION 02 PREP", font=f_mono(29), fill=ACID)
    RW, RH = 940, 1420
    # shadow
    base = Image.new("RGBA", (RW+80, RH+80), (0,0,0,0))
    bd = ImageDraw.Draw(base)
    zig = 14
    pts_top = [(40 + i*(RW/ (RW//zig)), 40 + (0 if i % 2 == 0 else 10)) for i in range(RW//zig + 1)]
    pts_bot = [(40 + i*(RW/ (RW//zig)), 40+RH - (0 if i % 2 == 0 else 10)) for i in range(RW//zig, -1, -1)]
    poly = pts_top + pts_bot
    bd.polygon([(x, y+10) for (x, y) in poly], fill=(0,0,0,120))
    bd.polygon(poly, fill=(246, 240, 224, 255))
    rd = ImageDraw.Draw(base)
    cx = 40 + RW/2; x0 = 40+64; x1 = 40+RW-64
    def dashline(y):
        for x in range(x0, x1, 22): rd.line([x, y, x+11, y], fill=(120,110,90,255), width=3)
    rd.text((cx, 96), "VIRECEIPTS PROVING CO.", font=f_mono(48), fill=(30,25,18,255), anchor="ma")
    rd.text((cx, 158), "plot no. 1, THE DRAWER, gurugram · est. today", font=f_mono(28), fill=(90,80,65,255), anchor="ma")
    rd.text((cx, 200), "bill no. 0014 · MISSION 02 PREP · dine-in", font=f_mono(28), fill=(90,80,65,255), anchor="ma")
    dashline(246)
    rd.text((cx, 268), "** THE RECEIPTS PROTOCOL **", font=f_mono(36), fill=(30,25,18,255), anchor="ma")
    items = [
        ("01 DRAWER KHOLO", "DONE"), ("( everything out. no mercy. )", ""),
        ("02 SCALE PAR RAKHO", "1.4 KG"), ("( kitchen scale. zero drama. )", ""),
        ("03 HSPCB LIST KHOLO", "15 GATES"), ("04 PHOTO + DROP", "POSTED"),
    ]
    y = 340
    for name, val in items:
        if val:
            nm_w = rd.textlength(name, font=f_mono(36))
            vl_w = rd.textlength(val, font=f_mono(36))
            dots = max(3, int((x1 - x0 - nm_w - vl_w - 34) / 18))
            rd.text((x0, y), name + " " + "." * dots, font=f_mono(36), fill=(30,25,18,255))
            rd.text((x1, y), val, font=f_mono(36), fill=(30,25,18,255), anchor="ra")
        else:
            rd.text((cx, y), name, font=f_mono(28), fill=(120,110,90,255), anchor="ma")
        y += 62 if val else 50
    dashline(y + 6); y += 40
    for name, val in [("TOTAL EVIDENCE", "1.4 KG"), ("CASH RECEIVED", "₹40"), ("WORDS USED", "0"), ("RESPECT EARNED", "100%")]:
        nm_w = rd.textlength(name, font=f_mono(40))
        vl_w = rd.textlength(val, font=f_mono(40))
        dots = max(3, int((x1 - x0 - nm_w - vl_w - 34) / 20))
        rd.text((x0, y), name + " " + "." * dots, font=f_mono(40), fill=(20,16,12,255))
        rd.text((x1, y), val, font=f_mono(40), fill=(20,16,12,255), anchor="ra")
        y += 66
    dashline(y + 2)
    stamp_l = Image.new("RGBA", (720, 200), (0,0,0,0))
    sd = ImageDraw.Draw(stamp_l)
    sd.rectangle([10, 10, 710, 190], outline=(160,30,30,255), width=8)
    sd.text((360, 100), "WEIGHED. NOT GUESSED.", font=f_anton(72), fill=(160,30,30,255), anchor="mm")
    rot_p = stamp_l.rotate(-7, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(rot_p, (196, y+62))
    y += 290
    # barcode
    import random
    rng = random.Random(40)
    bx = x0 + 40
    for _ in range(46):
        w = rng.choice([3, 3, 5, 8])
        rd.rectangle([bx, y, bx+w, y+92], fill=(25,22,16,255)); bx += w + rng.choice([4, 6, 9])
    rd.text((cx, y+104), "0014 · 4002 · 2026", font=f_mono(30), fill=(90,80,65,255), anchor="ma")
    rd.text((cx, y+170), "thank you for proving things. NO RETURNS ON EVIDENCE.", font=f_mono(28), fill=(120,110,90,255), anchor="ma")
    rot_paste(img, base, 720, 1000, -3)
    footer(d, "receipts protocol: kholo → taulo → list kholo → photo + drop. that’s the whole religion.", "WEIGHED · 1.4 KG")
    posts["R7_receipt"] = grain(img, amt=0.045)

r1(); r2(); r3(); r4(); r5(); r6(); r7()
for k, im in posts.items():
    im.save(f"{OUT}/{k}.jpg", quality=92)
    print("saved", k)

# contact sheets
keys = list(posts.keys())
imgs = [Image.open(f"{OUT}/{k}.jpg") for k in keys]
for i in imgs: i.thumbnail((500, 625))
s = Image.new("RGB", (4*530+20, 2*655+20), (16,20,16))
for i, im in enumerate(imgs):
    s.paste(im, (20 + (i%4)*530, 20 + (i//4)*655))
s.save("/tmp/remix_sheet.jpg", quality=88)
print("sheet ok")