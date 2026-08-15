#!/usr/bin/env python3
"""pix_std.py — print the std-dev of an image's luminance (blank-screen detector).
Usage: python3 pix_std.py <image.png>"""
import sys
import cv2

im = cv2.imread(sys.argv[1])
if im is None:
    print(-1)
    sys.exit(0)
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
print(round(float(gray.std()), 1))
