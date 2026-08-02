#!/usr/bin/env python3
"""Project Verde — self-review loop v2.
Renders every page, checks for overflow / blank pages / density,
footer presence and margin violations; audits facts."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fitz  # PyMuPDF

PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Project_Verde_Documentation.pdf")
OUT = os.path.join(os.path.dirname(PDF), "review")
os.makedirs(OUT, exist_ok=True)
VARIANT = "print" if "print" in PDF else "dark"
BG = (8, 27, 41) if VARIANT == "dark" else (255, 255, 255)

FACTS = ["1,890", "1,320", "220", "350", "5 sensors", "2 MCUs", "17", "94%", "8 MHz",
         "GPIO34", "GPIO23", "GPIO4", "GPIO35", "GPIO18", "GPIO19", "GPIO5", "GPIO12",
         "35%", "15%", "2 calls", "watchdog", "1000", "1N4007", "1273294", "5 V / 2 A",
         "13", "10-pt", "5-pt", "±2%", "1.5 s", "500 ms", "SVGA", "gemini-flash-latest",
         "crop.health", "OpenRouter", "OpenWeatherMap", "Firebase", "esp_camera_fb_return",
         "V3.0.7", "V3.0.4", "₹", "8,000"]

doc = fitz.open(PDF)
print(f"pages: {doc.page_count}  variant: {VARIANT}")
report = []
all_text = ""
problems = 0
for i, page in enumerate(doc):
    pw, ph = page.rect.width, page.rect.height
    d = page.get_text("dict")
    words = page.get_text("words")
    n_words = len(words)
    overflow = []
    margin_violations = []
    for block in d.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                bbox = fitz.Rect(span["bbox"])
                if bbox.x1 > pw + 1 or bbox.y1 > ph + 1 or bbox.x0 < -1 or bbox.y0 < -1:
                    overflow.append((round(bbox.x0), round(bbox.y0), round(bbox.x1), round(bbox.y1),
                                     span["text"][:40]))
                elif bbox.x1 > pw - 8 and bbox.y1 < ph - 26:
                    margin_violations.append((round(bbox.x1), round(bbox.y0), span["text"][:40]))
    # bg-relative ink coverage
    pix = page.get_pixmap(dpi=72)
    img = pix.samples
    content = 0
    sampled = 0
    for y in range(0, pix.height, 2):
        row = y * pix.n * pix.width
        for x in range(0, pix.width, 2):
            idx = row + x * pix.n
            r, g, b = img[idx], img[idx + 1], img[idx + 2]
            if abs(r - BG[0]) + abs(g - BG[1]) + abs(b - BG[2]) > 60:
                content += 1
            sampled += 1
    ink = content / sampled
    # span collision + footer zone
    spans = []
    for block in d.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                spans.append(fitz.Rect(span["bbox"]))
    collisions = []
    for a in range(len(spans)):
        for b in range(a + 1, len(spans)):
            r = spans[a] & spans[b]
            if not r.is_empty:
                area = r.get_area()
                small = min(spans[a].get_area(), spans[b].get_area())
                if small > 0 and area / small > 0.5:
                    collisions.append((round(area / small, 2), spans[a], spans[b]))
                    break
    footer_intr = [s for s in spans if s.y0 < 27 and s.y1 > 0]
    txt = page.get_text()
    all_text += txt
    has_footer = f"{i+1:02d} / {doc.page_count:02d}" in txt
    issues = []
    if overflow:
        issues.append(f"{len(overflow)} spans OFF-PAGE")
    if margin_violations:
        issues.append(f"{len(margin_violations)} touches right margin")
    if n_words < 20 and i not in (0, doc.page_count - 1):
        issues.append(f"sparse text ({n_words}w)")
    if ink < (0.015 if VARIANT == "dark" else 0.01):
        issues.append(f"nearly blank ({ink:.1%})")
    if i == 0 and ink < 0.10:
        issues.append("cover too empty?")
    if not has_footer and i not in (0, doc.page_count - 1):
        issues.append("footer missing")
    if collisions:
        issues.append(f"{len(collisions)} text collision(s)")
    if footer_intr:
        issues.append("text in footer zone")
    status = "OK" if not issues else "; ".join(issues)
    if issues:
        problems += 1
    report.append({"page": i + 1, "words": n_words, "ink": round(ink, 4),
                   "status": status, "overflow": overflow[:3], "margin": margin_violations[:3],
                   "collisions": [[round(x, 1) for x in r] for c in collisions[:3] for r in c[1:]]})
    pix.save(os.path.join(OUT, f"page_{i+1:02d}.png"))
    print(f"p{i+1:02d} words={n_words:4d} content={ink:5.1%} footer={'y' if has_footer else 'n'} | {status}")

missing = [f for f in FACTS if f.lower() not in all_text.lower()]
print("\n--- fact audit ---")
print("missing:", missing if missing else "NONE — all key facts present")
print(f"\nPROBLEMS: {problems} page(s) flagged")
with open(os.path.join(OUT, "review_report.json"), "w") as f:
    json.dump({"pages": doc.page_count, "report": report, "missing_facts": missing}, f, indent=1)
print("saved ->", os.path.join(OUT, "review_report.json"))
