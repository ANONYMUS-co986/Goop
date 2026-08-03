#!/usr/bin/env python3
"""Render the Verde docs with WeasyPrint (engine built from source in ~/stack).

Usage: python3 weasy_render.py [input.html] [output.pdf]
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("LD_LIBRARY_PATH", "/home/user/stack/lib")
os.environ.setdefault("FONTCONFIG_PATH", "/home/user/stack/etc/fonts")

# pango's dlopen calls happen at import time; the process must see the libs
# (ctypes/cffi honor LD_LIBRARY_PATH on linux)
import ctypes
for lib in ("libpango-1.0.so.0", "libpangoft2-1.0.so.0", "libfontconfig.so.1",
            "libharfbuzz.so.0", "libgobject-2.0.so.0", "libglib-2.0.so.0"):
    ctypes.CDLL(f"/home/user/stack/lib/{lib}", mode=ctypes.RTLD_GLOBAL)

import weasyprint  # noqa: E402

root = Path(__file__).resolve().parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "index-weasy.html"
out = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "render" / "verde-weasyprint.pdf"
out.parent.mkdir(parents=True, exist_ok=True)

doc = weasyprint.HTML(filename=str(src), base_url=str(src.parent) + "/").render()
doc.write_pdf(str(out))
print(f"weasyprint -> {out} ({len(doc.pages)} pages)")
