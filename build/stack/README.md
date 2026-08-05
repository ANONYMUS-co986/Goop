# build/stack — from-source native toolchain for WeasyPrint

This folder preserves the two non-obvious artifacts of the from-source
Pango/WeasyPrint build (the full recipe is documented in `../../REVIEW_NOTES.md`):

- `gperf.py` — a Python gperf-compatible generator. fontconfig's Meson build needs
  GNU gperf to turn `src/fcobjshash.gperf.h` into `fcobjshash.h`; gperf isn't on
  PyPI and its git home is unreachable in the sandbox. This script consumes the same
  preprocessed spec and emits a linear-scan hash that is semantically identical
  (perfect-hash performance is irrelevant at ~60 objects). Install as
  `/home/user/stack/bin/gperf` (chmod +x).
- `fonts.conf` — the minimal fontconfig config used for WeasyPrint renders: registers
  the document's TTF fonts plus DejaVu as glyph fallback (₹). Install as
  `/home/user/stack/etc/fonts/fonts.conf`.

Everything else under `/home/user/stack` (compiled glib/freetype/fribidi/fontconfig/
harfbuzz/pango + zlib/expat/pcre2) is rebuildable in ~25 min from the GitHub codeload
tarballs listed in REVIEW_NOTES.md.
