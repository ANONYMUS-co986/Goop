#!/usr/bin/env bash
# Project Verde — one-command build for the documentation deliverable.
# Produces: Project_Verde_Documentation.pdf (screen/dark)
#           Project_Verde_Documentation_print.pdf (ink-friendly)
set -euo pipefail
cd "$(dirname "$0")"

echo "[1/6] venv + dependencies"
python3 -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q reportlab pillow qrcode pymupdf fonttools brotli

echo "[2/6] bake static fonts (from fonts/*-var.ttf)"
.venv/bin/python tools/bake_fonts.py

echo "[3/6] preprocess AI images + gradients + QR"
.venv/bin/python tools/prep_images.py

echo "[4/6] build dark (screen) variant"
.venv/bin/python tools/build_verde.py --variant dark --out Project_Verde_Documentation.pdf

echo "[5/6] build print variant"
.venv/bin/python tools/build_verde.py --variant print --out Project_Verde_Documentation_print.pdf

echo "[6/6] self-review pass"
.venv/bin/python tools/review.py Project_Verde_Documentation.pdf || true
.venv/bin/python tools/review.py Project_Verde_Documentation_print.pdf || true

echo "DONE — Project_Verde_Documentation.pdf + _print.pdf"
