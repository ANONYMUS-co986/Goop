#!/usr/bin/env python3
"""VIKAAS FINALE POWER SUITE — pix.py (the eyes)
Usage:
  pix.py stats <img...>            -> mean/std/dark%/acid%/green% per image
  pix.py ascii <img> [cols rows]   -> ASCII luminance map (the sight rig)
  pix.py diff <a> <b>              -> pixel diff % + region map
  pix.py region <img> x y w h      -> mean/std of a region (crop QA)
"""
import sys, os
import numpy as np
import cv2

CHARS = " .:-=+*#%@"

def stats(paths):
    for f in paths:
        im = cv2.imread(f)
        if im is None:
            print(f, 'MISSING'); continue
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        acid = 100 * cv2.inRange(hsv, (40, 60, 120), (95, 255, 255)).mean()
        green = 100 * cv2.inRange(hsv, (75, 50, 50), (100, 255, 255)).mean()
        dark = 100 * (gray < 40).mean()
        v = 'BLANK?' if gray.std() < 8 else 'OK'
        print(f"{os.path.basename(f):28s} {im.shape[1]}x{im.shape[0]}  mean {gray.mean():5.1f}  std {gray.std():5.1f}  dark {dark:5.1f}%  acid {acid:6.2f}%  green {green:6.2f}%  {v}")

def ascii_map(f, cols=88, rows=24):
    im = cv2.imread(f)
    if im is None: print(f, 'MISSING'); return
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (cols, rows))
    for row in small:
        print(''.join(CHARS[min(9, int(v / 25.6))] for v in row))

def diff(a, b):
    ia = cv2.imread(a); ib = cv2.imread(b)
    if ia is None or ib is None: print('MISSING'); return
    if ia.shape != ib.shape:
        ib = cv2.resize(ib, (ia.shape[1], ia.shape[0]))
    d = np.abs(ia.astype(int) - ib.astype(int)).mean()
    changed = 100 * (np.abs(ia.astype(int) - ib.astype(int)).mean(axis=2) > 30).mean()
    print(f"mean abs diff: {d:.2f}/255  | pixels changed >30: {changed:.2f}%")
    # coarse region map of changes
    small = cv2.resize((np.abs(ia.astype(int) - ib.astype(int)).mean(axis=2) > 30).astype(np.uint8), (64, 24))
    for row in small:
        print(''.join('#' if v else '.' for v in row))

def region(f, x, y, w, h):
    im = cv2.imread(f)
    if im is None: print('MISSING'); return
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    r = gray[y:y + h, x:x + w]
    print(f"region ({x},{y},{w}x{h}): mean {r.mean():.1f} std {r.std():.1f}")

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    args = sys.argv[2:]
    if cmd == 'stats': stats(args)
    elif cmd == 'ascii': ascii_map(args[0], int(args[1]) if len(args) > 1 else 88, int(args[2]) if len(args) > 2 else 24)
    elif cmd == 'diff': diff(args[0], args[1])
    elif cmd == 'region': region(args[0], *map(int, args[1:5]))
    else: print('unknown cmd', cmd)
