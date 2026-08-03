#!/usr/bin/env python3
"""Assemble the Project Verde document from parts.

- Injects concatenated CSS into the {{CSS}} token.
- Inlines every <use href="#i-…"> icon ref so the document has zero external
  symbol dependencies (required for WeasyPrint, harmless for Chromium).
- Emits index.html (chromium path) — index-weasy.html is derived at render time.
"""
import pathlib, re, sys

SRC = pathlib.Path(__file__).parent / "src"
OUT = pathlib.Path(__file__).parent / "index.html"

css_files = [SRC / "styles.css", SRC / "styles-components.css", SRC / "styles-dividers.css"]
css = "\n\n".join(p.read_text() for p in css_files)

parts = sorted((SRC / "parts").glob("*.html"))
html = []
for p in parts:
    html.append(p.read_text())

doc = "\n".join(html)
assert doc.count("{{CSS}}") == 1, "missing {{CSS}} token in head"
doc = doc.replace("{{CSS}}", css)
doc += "\n</body>\n</html>\n"

# ---- inline icon symbols -------------------------------------------------
def load_symbols(text):
    syms = {}
    for m in re.finditer(r'<symbol id="(i-[a-z0-9-]+)"[^>]*viewBox="([^"]+)"[^>]*>(.*?)</symbol>', text, re.S):
        syms[m.group(1)] = (m.group(2), m.group(3).strip())
    return syms

symbols = load_symbols(doc)
n_inlined = 0

def inline_use(m):
    global n_inlined
    open_tag, inner = m.group(1), m.group(2)
    ids = re.findall(r'href="#(i-[a-z0-9-]+)"', inner)
    if len(ids) != 1 or ids[0] not in symbols:
        return m.group(0)
    viewbox, content = symbols[ids[0]]
    if "viewBox" not in open_tag:
        open_tag = open_tag[:-1] + f' viewBox="{viewbox}">'
    n_inlined += 1
    return f"{open_tag}{content}</svg>"

doc = re.sub(r'(<svg[^>]*>)\s*(<use href="#i-[a-z0-9-]+"/>)\s*</svg>', lambda m: inline_use(m), doc)

# ---- renumber folios + TOC page numbers from document order --------------
# every <section class="page" id="..."> gets a folio = its 1-based position
page_ids = re.findall(r'<section class="page[^"]*" id="([^"]+)"', doc)
folio_of = {pid: i + 1 for i, pid in enumerate(page_ids)}

# stamp footers per-section: folio = position of the owning page in doc order
chunk_pat = re.compile(r'(<section class="page[^"]*" id="(p\d+|d-[a-z]+)">)')
chunks = chunk_pat.split(doc)
out = [chunks[0]]
for i in range(1, len(chunks), 3):
    marker, pid = chunks[i], chunks[i + 1]
    body = chunks[i + 2] if i + 2 < len(chunks) else ""
    n = folio_of[pid]
    body = re.sub(r'(<span class="folio">PAGE <b>)\d+(</b>)', rf'\g<1>{n:02d}\g<2>', body, count=1)
    out.extend([marker, pid, body])
doc = "".join(out)

# retarget TOC anchors so chapters open on their divider pages where present
TOC_TARGETS = {
    "p4": "d-why", "p11": "d-fw", "p15": "d-cloud",
    "p18": "d-ai", "p21": "d-proof", "p24": "d-next",
}
def fix_toc(m):
    target = m.group(1)
    new = TOC_TARGETS.get(target, target)
    pg = folio_of[new]
    return f'href="#{new}" {m.group(2)}<span class="pg">{pg:02d}</span>'
doc = re.sub(r'href="#(p\d+|d-[a-z]+)" (class="toc-item[^"]*">.*?<span class="pg">)\d+</span>',
             lambda m: f'href="#{TOC_TARGETS.get(m.group(1), m.group(1))}" {m.group(2)}'
                       f'{folio_of[TOC_TARGETS.get(m.group(1), m.group(1))]:02d}</span>', doc, flags=re.S)

OUT.write_text(doc)
print(f"assembled {len(parts)} parts -> {OUT}  ({len(doc)//1024} KB, {n_inlined} icons inlined, {len(page_ids)} pages)")
