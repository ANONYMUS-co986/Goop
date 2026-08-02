#!/usr/bin/env python3
"""Shared page-level components for the Project Verde document."""
from verde_style import (PAL, VARIANT, FB, PAGE_W, PAGE_H, M_L, M_R, M_T, M_B,
                         parse_runs, draw_par, measure_par, sw, rrect, shadow_rrect,
                         hrule, grad_image, dotgrid, chip, icon, icon_circle, section_header, footer)

def bg(c, deep=False):
    if VARIANT == "dark":
        c.setFillColor(PAL["bg"])
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        grad_image(c, "navy_up", 0, 0, PAGE_W, PAGE_H, alpha=0.5 if deep else 0.28)
    else:
        c.setFillColor(PAL["bg"])
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

def kpi_card(c, x, y, w, h, value, label, sub="", accent=None, value_size=19):
    accent = accent or PAL["emerald"]
    shadow_rrect(c, x, y, w, h, 8, PAL["card"])
    hrule(c, x + 10, y + h - 2, 26, accent, 2.4)
    c.setFont(FB["body_bl"], value_size); c.setFillColor(accent)
    c.drawString(x + 12, y + h - 22 - value_size, value)
    c.setFont(FB["body_b"], 7.4); c.setFillColor(PAL["ivory"])
    c.drawString(x + 12, y + h - 38 - value_size, label.upper())
    if sub:
        c.setFont(FB["body"], 6.2); c.setFillColor(PAL["slate_d"])
        c.drawString(x + 12, y + h - 50 - value_size, sub)

def callout(c, x, y, w, h, icon_kind, title, text, accent=None, tsize=8.6, bsize=7):
    accent = accent or PAL["gold"]
    shadow_rrect(c, x, y, w, h, 8, PAL["card2"])
    c.saveState()
    c.setFillColor(accent)
    c.rect(x, y, 3, h, stroke=0, fill=1)
    c.restoreState()
    icon_circle(c, x + 20, y + h - 20, icon_kind, 22, accent)
    c.setFont(FB["body_b"], tsize); c.setFillColor(PAL["ivory"])
    c.drawString(x + 38, y + h - 25, title)
    c.setFont(FB["body"], bsize); c.setFillColor(PAL["slate"])
    yy = y + h - 37
    draw_par(c, x + 38, yy + bsize + 1, text, w - 50, size=bsize, leading=bsize + 3.6)

def pull_quote(c, x, y, w, text, author=None, size=15.5, leading=None):
    leading = leading or size + 6.5
    c.setFont(FB["disp_bl"], 54); c.setFillColor(PAL["gold"])
    c.drawString(x, y + 16, "“")
    lines = []
    runs = parse_runs(text, base_color=PAL["ivory"])
    from verde_style import wrap_runs, runs_width
    for ln in wrap_runs(runs, w - 30, size):
        lines.append(ln)
    yy = y + 2
    for ln in lines:
        x0 = x + 26
        for t, f, col in ln:
            c.setFont(f, size); c.setFillColor(col)
            c.drawString(x0, yy, t)
            x0 += sw(t, f, size)
        yy -= leading
    yy += leading - 6
    if author:
        c.setFont(FB["mono_b"], 7); c.setFillColor(PAL["emerald"])
        c.drawString(x + 26, yy - 8, author)
    return y + 2 - (len(lines) * leading) - 4

def feature_card(c, x, y, w, h, icon_kind, title, text, accent=None, tsize=8.4):
    accent = accent or PAL["emerald"]
    shadow_rrect(c, x, y, w, h, 8, PAL["card"])
    icon_circle(c, x + 20, y + h - 22, icon_kind, 24, accent)
    c.setFont(FB["body_b"], tsize); c.setFillColor(PAL["ivory"])
    c.drawString(x + 40, y + h - 27, title)
    draw_par(c, x + 12, y + h - 42, text, w - 24, size=6.8, leading=9.2, color=PAL["slate"])

def table_grid(c, x, y, w, header, rows, col_w, row_h=17, header_h=20, r=6,
               font_size=7.2, header_color=None, align_cols=None):
    """Draw a styled table. header: list[str]; rows: list[list[str]] (supports **bold** and `mono`)."""
    align_cols = align_cols or ["l"] * len(header)
    total_h = header_h + len(rows) * row_h
    shadow_rrect(c, x, y, w, total_h, r, PAL["card"])
    # header
    rrect(c, x, y + total_h - header_h, w, header_h, r, fill=PAL["green_bg"], stroke=None)
    c.saveState()
    c.setFillColor(PAL["line"])
    c.rect(x, y + total_h - header_h, w, 0.8, stroke=0, fill=1)
    c.restoreState()
    hx = x
    for i, htxt in enumerate(header):
        col = header_color if header_color else PAL["emerald"]
        c.setFont(FB["mono_b"], 6.8); c.setFillColor(col)
        if align_cols[i] == "r":
            c.drawRightString(hx + col_w[i] - 8, y + total_h - header_h + 7, htxt.upper())
        else:
            c.drawString(hx + 8, y + total_h - header_h + 7, htxt.upper())
        hx += col_w[i]
    # rows
    for ri, row in enumerate(rows):
        ry = y + total_h - header_h - (ri + 1) * row_h
        if ri % 2 == 1:
            c.saveState()
            c.setFillColor(PAL["card2"]); c.setFillAlpha(0.55)
            c.rect(x, ry, w, row_h, stroke=0, fill=1)
            c.restoreState()
        rx = x
        for ci, cell in enumerate(row):
            if align_cols[ci] == "r":
                draw_par(c, rx, ry + row_h - 4, cell, col_w[ci] - 10,
                         size=font_size, leading=font_size + 3, align="right", color=PAL["slate"])
            else:
                draw_par(c, rx + 8, ry + row_h - 4, cell, col_w[ci] - 14,
                         size=font_size, leading=font_size + 3, color=PAL["slate"])
            rx += col_w[ci]
        c.saveState()
        c.setStrokeColor(PAL["line"]); c.setLineWidth(0.4)
        c.line(x + 4, ry, x + w - 4, ry)
        c.restoreState()
    return total_h

def photo_band(c, path, x, y, w, h, caption=None, radius=8, credit=None):
    c.saveState()
    rrect(c, x, y, w, h, radius, fill=None, stroke=None)
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(path, x, y, width=w, height=h, mask="auto", preserveAspectRatio=False)
    c.restoreState()
    # frame
    rrect(c, x, y, w, h, radius, fill=None, stroke=PAL["line"], sw_=0.8)
    if caption:
        c.setFont(FB["body"], 6.6); c.setFillColor(PAL["slate"])
        c.drawString(x + 2, y - 11, caption)

def bullet_list(c, x, ytop, width, items, size=8.6, leading=13, color=None, gap=1,
                marker="▸", marker_color=None):
    color = color if color is not None else PAL["slate"]
    marker_color = marker_color or PAL["emerald"]
    y = ytop
    for it in items:
        c.setFont(FB["mono_b"], size - 0.5)
        c.setFillColor(marker_color)
        c.drawString(x, y - size + 1, marker)
        y = draw_par(c, x + 14, y, it, width - 14, size=size, leading=leading, color=color)
        y -= gap
    return y

def stat_strip(c, x, y, w, items, h=56):
    """items: (value, label) shown as a horizontal KPI strip."""
    n = len(items)
    bw = (w - (n - 1) * 10) / n
    for i, (v, l) in enumerate(items):
        sx = x + i * (bw + 10)
        shadow_rrect(c, sx, y, bw, h, 8, PAL["card"])
        c.setFont(FB["mono_eb"], 16); c.setFillColor(PAL["gold"] if i % 2 else PAL["emerald"])
        c.drawCentredString(sx + bw / 2, y + 30, v)
        c.setFont(FB["body_b"], 6.4); c.setFillColor(PAL["slate"])
        c.drawCentredString(sx + bw / 2, y + 12, l.upper())
