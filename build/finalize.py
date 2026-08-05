#!/usr/bin/env python3
"""Finalize + audit the PDF: metadata, links, bookmarks, fonts, fact check."""
import fitz, pathlib, sys

PDF = pathlib.Path(__file__).parent.parent / "Project_Verde_Documentation.pdf"
doc = fitz.open(PDF)

# 1) metadata
doc.set_metadata({
    "title": "Project Verde — Smart IoT Irrigation & Plant-Care System · Build Documentation",
    "author": "Aarav Choudhary & Anuj (Class X) — DAV ACON 5, 2026",
    "subject": "Competition documentation for Project Verde: ESP32 irrigation, Firebase cloud, web app, AI plant doctor",
    "keywords": "Project Verde, IoT, ESP32, Firebase, irrigation, plant care, DAV ACON 5",
    "creator": "Project Verde build pipeline",
})
doc.save(PDF, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
doc.close()

doc = fitz.open(PDF)
print(f"pages: {len(doc)}  size: {PDF.stat().st_size//1024} KB")

# 2) bookmarks / outline
toc = doc.get_toc()
print(f"bookmarks: {len(toc)}")
for t in toc[:12]:
    print("   ", t[0]*"  ", t[1][:60], "-> p", t[2])

# 3) internal links
links = 0
for p in doc:
    links += len(p.get_links())
print(f"link annotations: {links}")

# 4) fonts embedded
fonts = set()
for p in doc:
    for f in p.get_fonts():
        fonts.add(f[3])
print("fonts:", sorted(fonts))

# 5) fact audit — every must-have figure from the brief
text = "\n".join(p.get_text() for p in doc)
facts = [
    "1,890", "$23", "5 sensors", "2 actuators", "17", "2 calls", "94%",
    "8 MHz", "GPIO 34", "GPIO 23", "GPIO 4", "GPIO 35", "TRIG", "ECHO", "GPIO 5", "GPIO 12",
    "220 Ω", "35%", "15%", "±2%", "8 s", "120", "10+ min", "1273294", "35 °C",
    "1000 µF", "1N4007", "5 V / 2 A", "SVGA", "NVS", "millis", "watchdog",
    "manual_mode", "weather_override", "moisture_threshold", "tank_threshold",
    "gemini-flash-latest", "OpenRouter", "crop.health", "OpenWeatherMap", "435 models",
    "Aarav Choudhary", "Anuj", "DAV ACON 5", "V3.0.7-FINAL", "V3.0.4-FINAL",
    "₹8,000", "0x106", "0x20002", "verde-tech-haha",
]
missing = [f for f in facts if f not in text]
print(f"fact audit: {len(facts)-len(missing)}/{len(facts)} present")
if missing:
    print("MISSING:", missing)
doc.close()
