#!/usr/bin/env python3
"""Render PDF pages to PNGs (+ contact sheets) for visual review."""
import fitz, pathlib, sys, math

PDF = pathlib.Path(__file__).parent.parent / "Project_Verde_Documentation.pdf"
OUT = pathlib.Path(__file__).parent / "render"
OUT.mkdir(exist_ok=True)
for f in OUT.glob("*.png"): f.unlink()

doc = fitz.open(PDF)
dpi = int(sys.argv[1]) if len(sys.argv) > 1 else 100
paths = []
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=dpi)
    p = OUT / f"page-{i+1:02d}.png"
    pix.save(str(p))
    paths.append(p)
print(f"rendered {len(paths)} pages at {dpi} dpi")

# contact sheets (grids of 9) for fast scanning
from PIL import Image
THUMB_W = 360
cols, rows = 3, 3
for sheet_i in range(math.ceil(len(paths) / (cols * rows))):
    batch = paths[sheet_i*cols*rows:(sheet_i+1)*cols*rows]
    ims = []
    for p in batch:
        im = Image.open(p)
        r = THUMB_W / im.width
        ims.append(im.resize((THUMB_W, int(im.height * r)), Image.LANCZOS))
    W, H = ims[0].size
    gap = 10
    sheet = Image.new("RGB", (cols*W + (cols+1)*gap, rows*H + (rows+1)*gap), (24, 27, 38))
    for j, im in enumerate(ims):
        x = gap + (j % cols) * (W + gap)
        y = gap + (j // cols) * (H + gap)
        sheet.paste(im, (x, y))
    sp = OUT / f"sheet-{sheet_i+1}.png"
    sheet.save(sp)
    print("sheet:", sp)
