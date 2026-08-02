#!/usr/bin/env python3
"""Project Verde — definitive documentation builder.
Usage:  python build_verde.py [--variant dark|print] [--out PATH]"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas as CanvasMod
from reportlab.lib.pagesizes import A4
import verde_style as vs
from verde_style import PAGE_W, PAGE_H, M_L, M_R, M_T, M_B, PAL, VARIANT, register_fonts
import pages_front as PF
import pages_mid as PM
import pages_back as PB

# ---------------------------------------------------------------- page plan
# (id, title, draw_fn) — one entry per page; page numbers computed sequentially.
PLAN = [
    ("cover",       "Cover",                      PF.cover),
    ("story",       "The Whole Story in 60 Seconds", PF.story_60s),
    ("toc",         "Contents",                   None),          # special
    ("why",         "Why — The Problem",          PF.why_page),
    ("arch",        "How It Works — Architecture",PF.architecture_page),
    ("hw_bom",      "Hardware — The Brain & Eyes",PF.hardware_bom),
    ("hw_circuit",  "Hardware — Wiring & Power",  PF.circuit_page),
    ("firmware",    "Firmware — The Brain",       PF.firmware_page),
    ("bug",         "The Big Bug",                PF.bug_page),
    ("cam",         "ESP32-CAM — The Eyes",       PF.cam_page),
    ("cloud",       "Cloud — Firebase",           PM.cloud_page),
    ("app_dash",    "Web App — Dashboard & Weather", PM.webapp_dash),
    ("app_doctor",  "Web App — Plant Doctor & AI",PM.webapp_doctor),
    ("ai",          "AI & APIs",                  PM.ai_page),
    ("features",    "Features — All Live",        PM.features_page),
    ("testing",     "Testing — 13/13",            PM.testing_page),
    ("trouble",     "Troubleshooting Journal",    PB.troubleshooting_page),
    ("cost",        "Cost & Sustainability",      PB.cost_page),
    ("future",      "Future Scope",               PB.future_page),
    ("tour",        "Judge Tour Script",          PB.tour_page),
    ("conclusion",  "Conclusion",                 PB.conclusion_page),
]

TOC_ENTRIES = [
    (1,  "The Whole Story in 60 Seconds",   2,  "bm_story"),
    (2,  "Why — The Problem",               4,  "bm_why"),
    (3,  "How It Works — Architecture",     5,  "bm_arch"),
    (4,  "Hardware — The Brain & Eyes",     6,  "bm_hw_bom"),
    (5,  "Hardware — Wiring & Power",       7,  "bm_hw_circuit"),
    (6,  "Firmware — The Brain",            8,  "bm_firmware"),
    (7,  "The Big Bug (17 → 2 calls)",      9,  "bm_bug"),
    (8,  "ESP32-CAM — The Eyes",           10,  "bm_cam"),
    (9,  "Cloud — Firebase Schema",        11,  "bm_cloud"),
    (10, "Web App — Dashboard & Weather",  12,  "bm_app_dash"),
    (11, "Web App — Plant Doctor & AI",    13,  "bm_app_doctor"),
    (12, "AI & APIs — Accuracy Notes",     14,  "bm_ai"),
    (13, "Features — All Live",            15,  "bm_features"),
    (14, "Testing — 13/13 Matrix",         16,  "bm_testing"),
    (15, "Troubleshooting Journal",        17,  "bm_trouble"),
    (16, "Cost & Sustainability",          18,  "bm_cost"),
    (17, "Future Scope",                   19,  "bm_future"),
    (18, "Judge Tour Script",              20,  "bm_tour"),
    (19, "Conclusion",                     21,  "bm_conclusion"),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="dark", choices=["dark", "print"])
    ap.add_argument("--out", default=os.path.join(vs.ROOT, "Project_Verde_Documentation.pdf"))
    args = ap.parse_args()

    global VARIANT
    if args.variant == "print":
        vs.VARIANT = "print"
        vs.PAL.clear(); vs.PAL.update(vs.LIGHT)
        # light-mode page accents
        vs.PAL["navy_text"] = vs.LIGHT["ivory"]
    else:
        vs.PAL.clear(); vs.PAL.update(vs.DARK)

    register_fonts()
    # recompute page numbers from plan order
    start = {}
    page_no = 1
    for pid, title, fn in PLAN:
        start[pid] = page_no
        page_no += 1
    total = page_no - 1

    # verify TOC numbers match computed
    for num, title, pnum, dest in TOC_ENTRIES:
        pid = dest.replace("bm_", "")
        assert start.get(pid) == pnum, f"TOC page mismatch for {pid}: {start.get(pid)} != {pnum}"

    out = args.out
    c = CanvasMod.Canvas(out, pagesize=A4)
    c.setTitle("Project Verde — Smart IoT Irrigation & Plant-Care System")
    c.setAuthor("Aarav Choudhary & Anuj")
    c.setSubject("DAV ACON 5 — Tech Exhibition 2026 · Documentation")
    meta = {"total": total, "variant": args.variant}

    drawn = {}
    for pid, title, fn in PLAN:
        pno = start[pid]
        drawn[pid] = pno
        if pid == "cover":
            fn(c, meta)
        elif pid == "toc":
            c.bookmarkPage("bm_toc")
            c.addOutlineEntry("Contents", "bm_toc", level=0)
            PF.contents(c, meta, pno, TOC_ENTRIES)
        elif pid == "story":
            c.bookmarkPage("bm_story")
            c.addOutlineEntry("01 · The Whole Story in 60 Seconds", "bm_story", level=0)
            fn(c, meta, pno)
        else:
            c.bookmarkPage(f"bm_{pid}")
            c.addOutlineEntry(f"{title}", f"bm_{pid}", level=0)
            fn(c, meta, pno)
        c.showPage()

    c.save()
    print(f"[build] {args.variant} variant -> {out} ({total} pages)")
    return out

if __name__ == "__main__":
    main()
