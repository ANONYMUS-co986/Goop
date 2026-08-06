#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FINALE POST COMPOSER — 8 template memes + 6 AI-art posters -> 1440x1800 feed masters.
House style: ink canvas, mono eyebrow, VIReceipts stamps, grain. English lead, Hinglish flavor.
"""
import os, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

ROOT   = "/home/user/Goop"
FIN    = f"{ROOT}/vikaas-hq/studio/drops/FINALE"
OUT    = f"{FIN}/posts"
SRC    = f"{ROOT}/image-search"
ART    = f"{ROOT}/vikaas-hq/studio/drops/ai_art_test"
FONTS  = f"{ROOT}/vikaas-hq/studio/seed/fonts"
os.makedirs(OUT, exist_ok=True)

INK    = (7, 11, 8)
PAPER  = (239, 233, 220)
ACID   = (185, 255, 63)
GREEN  = (46, 222, 130)
DEW    = (234, 255, 244)
RED    = (255, 77, 94)
GOLD   = (255, 211, 77)
MUTE   = (125, 134, 127)

CANVAS = (1440, 1800)

def f_anton(sz):    return ImageFont.truetype(f"{FONTS}/Anton.ttf", sz)
def f_arch(sz, b=False): return ImageFont.truetype(f"{FONTS}/Archivo.ttf", sz)
def f_mono(sz):     return ImageFont.truetype(f"{FONTS}/SpaceGrotesk.ttf", sz)
def f_dev(sz):      return ImageFont.truetype(f"{FONTS}/NotoSansDevanagari.ttf", sz)

def grain(img, amt=0.055, seed=7):
    rng = np.random.default_rng(seed)
    n = rng.normal(128, 42, (img.height, img.width)).clip(0, 255).astype(np.uint8)
    noise = Image.fromarray(n, "L").convert("RGB")
    return Image.blend(img, noise, amt)

def fit(img, w, h, mode="contain"):
    if mode == "cover":
        return ImageOps.fit(img, (w, h), Image.LANCZOS)
    img2 = img.copy(); img2.thumbnail((w, h), Image.LANCZOS); return img2

def autosize(draw, text, font_fn, max_w, start, min_sz=30, spacing_ratio=0.16):
    sz = start
    while sz > min_sz:
        f = font_fn(sz)
        lines = text.split("\n")
        worst = max(draw.textlength(l, font=f) for l in lines)
        if worst <= max_w: return f, sz
        sz -= 4
    return font_fn(min_sz), min_sz

def stroke_text(base, xy, text, font, fill=(255,255,255), stroke=(0,0,0), sw=None, anchor="mm", spacing=None):
    d = ImageDraw.Draw(base)
    sw = sw if sw is not None else max(4, font.size // 13)
    spacing = spacing if spacing is not None else int(font.size * 0.12)
    d.multiline_text(xy, text, font=font, fill=fill, anchor=anchor, align="center",
                     spacing=spacing, stroke_width=sw, stroke_fill=stroke)

def chip(draw, x, y, text, bg=ACID, fg=INK, sz=34, pad=18, mono=False):
    f = f_mono(sz) if mono else f_anton(sz)
    w = draw.textlength(text, font=f) + pad*2
    h = int(sz * 1.5) + pad
    draw.rounded_rectangle([x, y, x+w, y+h], radius=int(h*0.24), fill=bg)
    draw.text(((x + x+w)/2, (y + y+h)/2 - sz*0.04), text, font=f, fill=fg, anchor="mm", align="center")
    return w, h

def eyebrow(draw, left, right=""):
    draw.text((70, 66), left, font=f_mono(30), fill=MUTE)
    if right:
        w = draw.textlength(right, font=f_mono(30)); draw.text((1440-70-w, 66), right, font=f_mono(30), fill=MUTE)
    # dotted rule
    y = 118
    for x in range(70, 1370, 26):
        draw.ellipse([x, y, x+4, y+4], fill=(63, 71, 64))

def footer(draw, caption, stamp, stamp_bg=ACID):
    h = 238
    draw.rectangle([0, 1800-h, 1440, 1800], fill=INK)
    draw.line([0, 1800-h, 1440, 1800-h], fill=(63, 71, 64), width=3)
    cap_f = f_mono(40); sub_f = f_mono(30)
    lines = wrap_text(draw, caption, cap_f, 1010)
    y = 1800 - h + 48
    for ln in lines:
        draw.text((70, y), ln, font=cap_f, fill=DEW); y += 52
    draw.text((70, y+6), "#EWasteOff · #ChangemakersWorldCup · @1m1bfoundation", font=f_mono(28), fill=MUTE)
    # stamp chip right
    sf = f_anton(44); w_ = ImageDraw.Draw(Image.new("RGB",(10,10))).textlength(stamp, font=sf) + 52
    chip(draw, 1440-70-w_, 1800-h+52, stamp, bg=stamp_bg, fg=INK, sz=44, pad=26)
    draw.text((1440-70-w_, 1800-h+150), "the stamp is the point.", font=f_mono(26), fill=MUTE)

def wrap_text(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def base_canvas():
    img = Image.new("RGB", CANVAS, INK)
    return img, ImageDraw.Draw(img)

def hogaya(s): return s  # marker

# ---------- TEMPLATE MEME BUILDER ----------
def paste_rotated_text(img, cx, cy, w, h, text, text_fn, max_sz, angle, fg=(15,15,15), cover=(255,255,255), pad_ratio=0.06):
    """White rotated cover + horizontal dark text inside (for signs/boards)."""
    d = ImageDraw.Draw(img)
    import math
    half_diag = int(((w**2 + h**2) ** 0.5) / 2) + 8
    # cover polygon
    pts = []
    for sx, sy in [(-w/2 - w*pad_ratio, -h/2 - h*pad_ratio), (w/2 + w*pad_ratio, -h/2 - h*pad_ratio),
                   (w/2 + w*pad_ratio, h/2 + h*pad_ratio), (-w/2 - w*pad_ratio, h/2 + h*pad_ratio)]:
        a = math.radians(angle)
        pts.append((cx + sx*math.cos(a) - sy*math.sin(a), cy + sx*math.sin(a) + sy*math.cos(a)))
    d.polygon(pts, fill=cover)
    # text layer
    size = half_diag*2
    layer = Image.new("RGBA", (size, size), (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    f, sz = autosize(ld, text, text_fn, w, max_sz, min_sz=18)
    n = len(text.split("\n"))
    lh = f.size*1.12
    ty = size/2 - n*lh/2 + lh/2
    for i, ln in enumerate(text.split("\n")):
        ld.text((size/2, ty + i*lh), ln, font=f, fill=fg+(255,), anchor="mm")
    layer = layer.rotate(angle, resample=Image.BICUBIC, center=(size/2, size/2))
    img.paste(layer, (int(cx-size/2), int(cy-size/2)), layer)

def build_meme(fname, tpl_path, zones, caption, stamp, stamp_bg=ACID, tpl_mode="contain", tpl_box=(60,150,1320,1290), border=True, crop=None):
    img, d = base_canvas()
    eyebrow(d, fname)
    tpl = Image.open(tpl_path).convert("RGB")
    if crop:
        tpl = tpl.crop((int(crop[0]*tpl.width), int(crop[1]*tpl.height),
                        int(crop[2]*tpl.width), int(crop[3]*tpl.height)))
    x, y, w, h = tpl_box
    tpl2 = fit(tpl, w, h, tpl_mode)
    ox = x + (w - tpl2.width)//2; oy = y + (h - tpl2.height)//2
    img.paste(tpl2, (ox, oy))
    if border:
        d = ImageDraw.Draw(img)
        d.rectangle([ox-6, oy-6, ox+tpl2.width+5, oy+tpl2.height+5], outline=ACID, width=4)
    # zones (rel coords on pasted template)
    for z in zones:
        kind = z.get("kind","impact")
        zx = ox + z["x"]*tpl2.width; zy = oy + z["y"]*tpl2.height
        zw = z.get("w", 0.9)*tpl2.width
        if kind == "impact":
            f, sz = autosize(d, z["t"], f_anton, zw, z.get("sz", 76))
            stroke_text(img, (zx, zy), z["t"], f, fill=z.get("fg",(255,255,255)),
                        stroke=z.get("bg",(0,0,0)))
        elif kind == "board":  # dark text on white board (gru)
            f, sz = autosize(d, z["t"], f_anton, zw, z.get("sz", 60), min_sz=22)
            dd = ImageDraw.Draw(img)
            dd.multiline_text((zx, zy), z["t"], font=f, fill=z.get("fg",(20,20,20)), anchor="mm",
                              align="center", spacing=int(f.size*0.1))
        elif kind == "mono":
            f, sz = autosize(d, z["t"], f_mono, zw, z.get("sz", 40))
            stroke_text(img, (zx, zy), z["t"], f, fill=z.get("fg", PAPER), stroke=(0,0,0), sw=max(3, f.size//14))
        elif kind == "rotcover":
            zw2 = z.get("w", 0.5)*tpl2.width; zh2 = z.get("h", 0.3)*tpl2.height
            paste_rotated_text(img, zx, zy, zw2, zh2, z["t"], f_anton, z.get("sz", 56),
                               z.get("angle", -6), fg=z.get("fg",(15,15,15)))
    d = ImageDraw.Draw(img)
    footer(d, caption, stamp, stamp_bg)
    img = grain(img)
    return img

# ---------- POSTER BUILDER ----------
def build_poster(fname, art_path, headline, sub, sub_dev, stamp, stamp_bg=ACID, accent=None):
    img, d = base_canvas()
    art = Image.open(art_path).convert("RGB")
    art = fit(art, 1440, 1800, "cover")
    img.paste(art, (0, 0))
    d = ImageDraw.Draw(img)
    f, sz = autosize(d, headline, f_anton, 1240, 148, min_sz=60)
    nlines = len(headline.split("\n"))
    lh = f.size * 1.06
    # block vertically centered in top empty zone (art empty zone ~0..500 on canvas)
    block_h = nlines * lh
    hy = max(120, 250 - block_h/2 + (60 if nlines == 3 else 0))
    d.multiline_text((720, hy), headline, font=f, fill=DEW, anchor="ma", align="center", spacing=int(f.size*0.06))
    # acid underline bar under block
    uw = min(300, d.textlength(headline.split("\n")[-1], font=f) * 0.5)
    uy = hy + block_h + 26
    d.rectangle([720-uw/2, uy, 720+uw/2, uy+10], fill=ACID)
    d.text((70, 52), fname, font=f_mono(28), fill=(170, 182, 172))
    # bottom band: sub + tags
    d.rectangle([0, 1800-150, 1440, 1800], fill=(7, 11, 8))
    d.line([0, 1800-150, 1440, 1800-150], fill=ACID, width=4)
    if sub_dev:
        d.text((70, 1800-122), sub_dev, font=f_dev(38), fill=ACID)
    else:
        d.text((70, 1800-122), sub, font=f_mono(34), fill=DEW)
    d.text((70, 1800-56), "VIReceipts · #EWasteOff · Changemakers World Cup 2026 · @1m1bfoundation", font=f_mono(28), fill=MUTE)
    # stamp chip above band
    sf = f_anton(40); w_ = d.textlength(stamp, font=sf) + 46
    chip(d, 1440-58-w_, 1800-238, stamp, bg=stamp_bg, fg=INK, sz=40, pad=23)
    img = grain(img, amt=0.05)
    return img

# ============================================================
# THE 14
# ============================================================
posts = {}

# M1 DRAKE
posts["M1_drake"] = build_meme(
    "PR POST 01/14 · MEME — DRAKE'S CHOICE",
    f"{SRC}/drake-meme-template-blank-hd-disgust-app-1.jpg",
    [
        {"x":0.75, "y":0.24, "w":0.42, "t":"DUSTBIN\nMEIN FEKNA", "sz":66},
        {"x":0.75, "y":0.76, "w":0.42, "t":"KABADI WALE\nKO DENA\n→ ₹40 BACK", "sz":60},
    ],
    "same phone. same effort. one option pays you ₹40 and doesn't poison a river. choose like a chad.",
    "WEIGHED · ₹40 RECEIPT")

# M2 TWO BUTTONS (huge vertical restoration png)
posts["M2_buttons"] = build_meme(
    "PR POST 02/14 · MEME — THE DAILY STRUGGLE",
    f"{SRC}/two-buttons-meme-template-blank-sweating-3.png",
    [
        {"x":0.31, "y":0.145, "w":0.30, "t":"DRAWER MEIN\nWAPAS RAKHO", "sz":58},
        {"x":0.71, "y":0.145, "w":0.30, "t":"FINALLY\nTAULO!", "sz":58},
    ],
    "5 saal se same decision, same paseena. the scale has been waiting patiently. it is very humble.",
    "TOO REAL · WEIGH IN")


# M3 CHANGE MY MIND (rotated cover over the sign)
posts["M3_cmm"] = build_meme(
    "PR POST 03/14 · MEME — CHANGE MY MIND",
    f"{SRC}/change-my-mind-meme-template-blank-hd-2.jpg",
    [
        {"kind":"rotcover", "x":0.705, "y":0.64, "w":0.44, "h":0.38, "angle":-5,
         "t":"THE KABADI WALA HAS BETTER\nPRICE DATA THAN YOUR APP.\nCHANGE MY MIND.", "sz":52},
    ],
    "ask him today's copper rate. then ask your favourite fintech. we dare you. — call one yourself & see.",
    "DAILY REALITY")

# M4 MONKEY PUPPET
posts["M4_puppet"] = build_meme(
    "PR POST 04/14 · MEME — SIDE-EYE",
    f"{SRC}/awkward-monkey-puppet-looking-away-meme--1.jpg",
    [
        {"x":0.5, "y":0.30, "w":0.86, "t":"MUM STORING THE DEAD PHONE\nNEXT TO THE ONIONS", "sz":66, "kind":"board", "fg":(12,12,12)},
        {"x":0.5, "y":0.93, "w":0.9, "t":"“KYUNKI KAAM KA CHEEZ HAI”", "sz":60},
    ],
    "indian homes don't hoard. they curate very private museums with onion-based security.",
    "DRAMATISED · ALSO TRUE")

# M5 KALM PANIK KALM (text in LEFT cells, faces on the right)
posts["M5_panik"] = build_meme(
    "PR POST 05/14 · MEME — KALM PANIK KALM",
    f"{SRC}/panik-kalm-panik-meme-template-blank-hd-2.png",
    [
        {"x":0.26, "y":0.16, "w":0.42, "t":"FOUND 3 DEAD PHONES\nIN THE DRAWER", "sz":44, "kind":"board", "fg":(15,15,15)},
        {"x":0.26, "y":0.50, "w":0.42, "t":"LANDFILL MEIN =\nLITHIUM LEAK", "sz":44, "kind":"board", "fg":(15,15,15)},
        {"x":0.26, "y":0.84, "w":0.42, "t":"KABADIWALA NE CASH DIYA.\nCHILL.", "sz":42, "kind":"board", "fg":(15,15,15)},
    ],
    "india bins 3.2 million tonnes a year — official CWC submission data. the drawer was option B, yaar.",
    "SOURCED · CWC 3.2 MT/YR")

# M6 DISTRACTED BOYFRIEND (crop to the classic first panel)
posts["M6_dbf"] = build_meme(
    "PR POST 06/14 · MEME — THE AFFAIR",
    f"{SRC}/distracted-boyfriend-meme-template-blank-2.png",
    [
        {"x":0.17, "y":0.66, "w":0.30, "t":"BIG BILLION\nDAY SALE", "sz":48},
        {"x":0.55, "y":0.70, "w":0.28, "t":"EVERY\nINDIAN HOME", "sz":44},
        {"x":0.83, "y":0.90, "w":0.32, "t":"THE DRAWER\n(ALREADY FULL)", "sz":38},
    ],
    "the drawer sees everything. the drawer remembers. the drawer is tired. open the drawer.",
    "OBSERVED · DAILY", crop=(0.0, 0.0, 1.0, 0.335))

# M7 WOMAN YELLING AT CAT (HD wide, dark text on the white label band)
posts["M7_cat"] = build_meme(
    "PR POST 07/14 · MEME — DINNER DEBATE",
    f"{SRC}/woman-yelling-at-cat-meme-template-blank-1.jpg",
    [
        {"x":0.25, "y":0.155, "w":0.40, "t":"“BAS FEK DE!\nWHY SO MUCH DRAMA?”", "sz":58, "kind":"board", "fg":(12,12,12)},
        {"x":0.75, "y":0.155, "w":0.44, "t":"15 GOVT-AUTHORISED\nRECYCLERS. NEAR YOU.", "sz":50, "kind":"board", "fg":(12,12,12)},
    ],
    "the cat has read the haryana pollution board list. the cat is correct. SOURCES.md for the names.",
    "SOURCED · HSPCB LIST")

# M8 GRU 5 PANEL (short boards + big 5th board payoff)
posts["M8_gru"] = build_meme(
    "PR POST 08/14 · MEME — THE PLAN",
    f"{SRC}/gru-plan-4-panel-presentation-meme-templ-1.png",
    [
        {"x":0.36, "y":0.145, "w":0.22, "t":"TAULO.", "sz":40, "kind":"board"},
        {"x":0.845, "y":0.13, "w":0.20, "t":"RECEIPTS.", "sz":32, "kind":"board"},
        {"x":0.345, "y":0.52, "w":0.22, "t":"POST IT.", "sz":38, "kind":"board"},
        {"x":0.85, "y":0.455, "w":0.20, "t":"1 CRORE\nDRAWERS.", "sz":30, "kind":"board", "fg":(180,30,40)},
        {"x":0.72, "y":0.775, "w":0.30, "t":"TOP 3 →\nGENEVA.", "sz":48, "kind":"board"},
    ],
    "taulo. receipts. post. repeat. the world cup's top 3 fly to the UN in geneva — that's the plan, publicly.",
    "THE PLAN · CWC TOP 3")

# --- AI POSTERS ---
posts["P1_hero"]  = build_poster("PR POST 09/14 · POSTER — THE SERIES 01",
    f"{ART}/poster_hero_blank.png",
    "IT TAKES\nONE DRAWER.", "start yours today. the mountain can wait no longer.",
    "", "WEIGHED · 1.4 KG OURS")

posts["P2_handshake"] = build_poster("PR POST 10/14 · POSTER — THE SERIES 02",
    f"{ART}/poster_handshake_blank.png",
    "THE ₹40\nHANDSHAKE.", "kabadi wale cash dete hain. they PAY you. remember that.", "",
    "WEIGHED · LOT NO. 1.4")

posts["P3_gold"] = build_poster("PR POST 11/14 · POSTER — THE SERIES 03",
    f"{ART}/poster_gold_blank.png",
    "0.03 g\nOF GOLD.", "per phone, roughly. a billion phones nap in drawers.",
    "", "ESTIMATE · SOURCES.md", stamp_bg=GOLD)

posts["P4_2047"] = build_poster("PR POST 12/14 · POSTER — THE SERIES 04",
    f"{ART}/poster_2047_blank.png",
    "TWO FUTURES.\nONE DRAWER.", "same city. same stuff. different habits. we get to pick.",
    "", "AMBITION · 2047", stamp_bg=GREEN)

posts["P5_kabadi"] = build_poster("PR POST 13/14 · POSTER — THE SERIES 05",
    f"{ART}/poster_kabadi_blank.png",
    "THE ORIGINAL\nSUPPLY CHAIN.", "you have an app. he has a bicycle. he still wins.",
    "", "RESPECT · DAILY")

posts["P6_mummy"] = build_poster("PR POST 14/14 · POSTER — THE SERIES 06",
    f"{ART}/poster_mummy_blank.png",
    "MUMMY'S\nMUSEUM.\nEST. FOREVER.", "",
    "हर भारतीय घर की सबसे पुरानी गैलरी", "DRAMATISED · TRUE")

# save
for k, im in posts.items():
    im.save(f"{OUT}/{k}.jpg", quality=92)
    print("saved", k, im.size)

# contact sheets
def sheet(keys, path, cols=2, tw=680):
    imgs = [Image.open(f"{OUT}/{k}.jpg") for k in keys]
    for i in imgs: i.thumbnail((tw, tw*1800//1440))
    th = imgs[0].size
    rows = (len(imgs)+cols-1)//cols
    s = Image.new("RGB", (cols*(th[0]+20)+20, rows*(th[1]+20)+20), (20,24,20))
    for i, im in enumerate(imgs):
        s.paste(im, (20 + (i%cols)*(th[0]+20), 20 + (i//cols)*(th[1]+20)))
    s.save(path, quality=88)
    print("sheet:", path, s.size)

meme_keys   = [k for k in posts if k.startswith("M")]
poster_keys = [k for k in posts if k.startswith("P")]
sheet(meme_keys[:4],  "/tmp/sheet_memes_a.jpg")
sheet(meme_keys[4:],  "/tmp/sheet_memes_b.jpg")
sheet(poster_keys,    "/tmp/sheet_posters.jpg", cols=3)
print("DONE14")
