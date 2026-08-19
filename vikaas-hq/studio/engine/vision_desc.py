#!/usr/bin/env python3
"""vision_desc.py — turn an image into structured TEXT a non-visual LLM can read.
Outputs JSON: size/mode, dominant palette, text-region blocks (MSER), layout
panels/cards (contours), buttons (filled rects), edge-density map.
Usage: python3 vision_desc.py <img> [--ascii]
"""
import cv2, numpy as np, sys, json

img = cv2.imread(sys.argv[1])
if img is None:
    print(json.dumps({"error": "unreadable"})); sys.exit(0)
h, w = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mean = float(gray.mean()); std = float(gray.std())
mode = "dark" if mean < 90 else ("light" if mean > 160 else "mid")

out = {"size": [w, h], "mean": round(mean, 1), "std": round(std, 1), "mode": mode, "palette": [], "text_blocks": [], "panels": [], "buttons": []}

# ---- 1. dominant palette (kmeans on small sample) ----
small = cv2.resize(img, (64, 64)).reshape(-1, 3).astype(np.float32)
K = 6
crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 15, 1.0)
_, labels, centers = cv2.kmeans(small, K, None, crit, 3, cv2.KMEANS_PP_CENTERS)
counts = np.bincount(labels.flatten())
for i in np.argsort(counts)[::-1][:K]:
    c = centers[i].astype(int)
    out["palette"].append({"rgb": [int(c[0]), int(c[1]), int(c[2])], "pct": round(100 * counts[i] / counts.sum(), 1)})

# ---- 2. text regions (MSER) → merged blocks ----
try:
    mser = cv2.MSER_create()
    mser.setMinArea(120); mser.setMaxArea(60000)
    regions, _ = mser.detectRegions(gray)
    boxes = [cv2.boundingRect(r) for r in regions if r.shape[0] > 4]
    # merge boxes into lines/blocks: sort by y, cluster
    boxes.sort(key=lambda b: b[1])
    blocks = []
    for b in boxes:
        bx, by, bw, bh = b
        placed = False
        for bl in blocks:
            if abs(by + bh / 2 - (bl["y"] + bl["h"] / 2)) < max(14, bl["h"] * 0.8) and not (bx > bl["x"] + bl["w"] + 20 or bx + bw < bl["x"] - 20):
                bl["x"] = min(bl["x"], bx); bl["y"] = min(bl["y"], by)
                bl["w"] = max(bl["x"] + bl["w"], bx + bw) - bl["x"]
                bl["h"] = max(bl["y"] + bl["h"], by + bh) - bl["y"]
                bl["n"] += 1
                placed = True
                break
        if not placed:
            blocks.append({"x": bx, "y": by, "w": bw, "h": bh, "n": 1})
    blocks = [b for b in blocks if b["n"] >= 2 and b["w"] > 30]  # multi-char = real text
    blocks.sort(key=lambda b: (b["y"], b["x"]))
    out["text_blocks"] = blocks[:60]
except Exception as e:
    out["text_mser_error"] = str(e)[:100]

# ---- 3. panels/cards: large 4-vertex contours ----
edges = cv2.Canny(gray, 60, 160)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
panels = []
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    x, y, bw, bh = cv2.boundingRect(approx)
    area = bw * bh
    if area > (w * h) * 0.02 and bw > 80 and bh > 40 and len(approx) in (3, 4, 5):
        panels.append({"x": x, "y": y, "w": bw, "h": bh, "verts": len(approx)})
panels.sort(key=lambda p: p["area"] if "area" in p else p["w"] * p["h"], reverse=True)
for p in panels[:14]:
    p["area_pct"] = round(100 * p["w"] * p["h"] / (w * h), 1)
out["panels"] = panels[:14]

# ---- 4. buttons: filled rounded rects (high-contrast small regions) ----
# detect via threshold + connected components, keep small filled rects
_, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
n, labels, stats, cents = cv2.connectedComponentsWithStats(th, 8)
buttons = []
for i in range(1, n):
    x, y, bw, bh, area = stats[i]
    if 30 < bw < 400 and 20 < bh < 120 and area > bw * bh * 0.55 and bw > bh * 0.4:
        buttons.append({"x": int(x), "y": int(y), "w": int(bw), "h": int(bh)})
out["buttons"] = buttons[:12]

print(json.dumps(out, indent=1))
