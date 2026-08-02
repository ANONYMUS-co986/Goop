#!/usr/bin/env python3
"""Bake static TTF weights from variable fonts (Inter, Fraunces, JetBrains Mono)."""
import os, sys
from fontTools import ttLib
from fontTools.varLib.instancer import instantiateVariableFont

FONTS = {
    "Inter-var.ttf": {
        "Inter-Regular":  {"wght": 400},
        "Inter-Medium":   {"wght": 500},
        "Inter-SemiBold": {"wght": 600},
        "Inter-Bold":     {"wght": 700},
        "Inter-ExtraBold":{"wght": 800},
        "Inter-Black":    {"wght": 900},
    },
    "Fraunces-var.ttf": {
        "Fraunces-Regular":   {"wght": 400},
        "Fraunces-SemiBold":  {"wght": 600},
        "Fraunces-Bold":      {"wght": 700},
        "Fraunces-Black":     {"wght": 900},
    },
    "JBMono-var.ttf": {
        "JBMono-Regular":    {"wght": 400},
        "JBMono-Bold":       {"wght": 700},
        "JBMono-ExtraBold":  {"wght": 800},
    },
}

SRC = os.path.join(os.path.dirname(__file__), "..", "fonts")
DST = os.path.join(os.path.dirname(__file__), "..", "fonts", "static")
os.makedirs(DST, exist_ok=True)

for src, weights in FONTS.items():
    path = os.path.join(SRC, src)
    for name, axis in weights.items():
        out = os.path.join(DST, name + ".ttf")
        if os.path.exists(out):
            print("skip", name)
            continue
        f = ttLib.TTFont(path)
        instantiateVariableFont(f, axis, inplace=True)
        # drop variable tables so ReportLab treats it as static
        for tag in ("fvar", "gvar", "HVAR", "VVAR", "MVAR", "STAT", "avar", "cvar"):
            if tag in f:
                del f[tag]
        f.save(out)
        print("baked", name)

print("done ->", DST)
