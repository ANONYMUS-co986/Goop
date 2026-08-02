"""Post-process the built PDF: add metadata + an interactive table of contents (outline)."""
import os, re
import fitz  # PyMuPDF


def add_outline(path):
    doc = fitz.open(path)
    doc.set_metadata({
        "title": "Project Verde — Smart IoT Irrigation & Plant-Care System",
        "author": "Aarav Choudhary & Anuj, Class X · DAV ACON 5 2026",
        "subject": "Definitive documentation for DAV ACON 5 Tech Exhibition 2026",
        "keywords": "IoT, ESP32, plant care, Firebase, AI, DAV ACON 5, Project Verde",
        "creator": "Project Verde build system",
    })

    # chapters to find: (chapter number string as rendered, outline title)
    chapters = [
        ("00", "The Whole Story in 60 Seconds"),
        ("01", "Why — the problem"),
        ("02", "How it works — architecture"),
        ("03", "Hardware — BOM, circuit & power"),
        ("04", "Firmware — logic, watchdog & the big bug"),
        ("05", "Cloud & web app"),
        ("06", "AI & the four APIs"),
        ("07", "Features — everything live"),
        ("08", "Testing & troubleshooting"),
        ("09", "Cost & sustainability"),
        ("10", "Judge tour & conclusion"),
    ]

    def find_page(frag):
        for pno in range(doc.page_count):
            if frag in doc[pno].get_text():
                return pno + 1
        return None

    toc = [[1, "Project Verde — Smart IoT Irrigation", 1]]
    for num, title in chapters:
        pg = find_page(f"C H A P T E R  {num}")
        if pg is None:
            pg = find_page(f"CHAPTER {num}")
        if pg is None:
            pg = 1
        toc.append([2, f"{num} — {title}", pg])

    doc.set_toc(toc)
    doc.save(path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()
    print("outline + metadata added")


if __name__ == "__main__":
    import sys
    add_outline(sys.argv[1])
