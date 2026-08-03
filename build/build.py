#!/usr/bin/env python3
"""Assemble the Project Verde document from parts."""
import pathlib, re, sys

SRC = pathlib.Path(__file__).parent / "src"
OUT = pathlib.Path(__file__).parent / "index.html"

css_files = [SRC / "styles.css", SRC / "styles-components.css"]
css = "\n\n".join(p.read_text() for p in css_files)

parts = sorted((SRC / "parts").glob("*.html"))
html = []
for p in parts:
    html.append(p.read_text())

doc = "\n".join(html)
assert doc.count("{{CSS}}") == 1, "missing {{CSS}} token in head"
doc = doc.replace("{{CSS}}", css)
doc += "\n</body>\n</html>\n"

OUT.write_text(doc)
print(f"assembled {len(parts)} parts -> {OUT}  ({len(doc)//1024} KB, images not inlined)")
