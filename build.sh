#!/usr/bin/env bash
# Project Verde — build the documentation PDF from source.
set -euo pipefail
cd "$(dirname "$0")"

# 1) Python environment (WeasyPrint-compatible deps + PDF tooling)
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install --quiet reportlab matplotlib pillow fonttools brotli svglib pymupdf

# 2) (Optional) fonts live in assets/fonts. If missing, fetch Inter/Space
#    Grotesk/JetBrains Mono static instances from the google/fonts repo.
if [ ! -f "assets/fonts/Inter-Bold.ttf" ]; then
  echo "Downloading fonts…"
  rm -rf /tmp/gfonts && mkdir -p /tmp/gfonts && cd /tmp/gfonts
  git clone --depth 1 --filter=blob:none --sparse https://github.com/google/fonts.git
  cd fonts
  git sparse-checkout set ofl/inter ofl/spacegrotesk ofl/jetbrainsmono
  git checkout
  mkdir -p "$OLDPWD/assets/fonts"
  cp "ofl/inter/Inter[opsz,wght].ttf"      "$OLDPWD/assets/fonts/Inter.ttf"
  cp "ofl/spacegrotesk/SpaceGrotesk[wght].ttf" "$OLDPWD/assets/fonts/SpaceGrotesk.ttf"
  cp "ofl/jetbrainsmono/JetBrainsMono[wght].ttf" "$OLDPWD/assets/fonts/JetBrainsMono.ttf"
  cd "$OLDPWD"
  python -c "
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.ttLib import TTFont
for src,name,w in [
 ('assets/fonts/Inter.ttf','Inter',400),('assets/fonts/Inter.ttf','Inter-Medium',500),
 ('assets/fonts/Inter.ttf','Inter-SemiBold',600),('assets/fonts/Inter.ttf','Inter-Bold',700),
 ('assets/fonts/Inter.ttf','Inter-ExtraBold',800),
 ('assets/fonts/SpaceGrotesk.ttf','SG',400),('assets/fonts/SpaceGrotesk.ttf','SG-Medium',500),
 ('assets/fonts/SpaceGrotesk.ttf','SG-SemiBold',600),('assets/fonts/SpaceGrotesk.ttf','SG-Bold',700),
 ('assets/fonts/JetBrainsMono.ttf','Mono-Regular',400),('assets/fonts/JetBrainsMono.ttf','Mono-Bold',700),
]:
  f=TTFont(src); instantiateVariableFont(f,{'wght':w},inplace=True); f.save(f'assets/fonts/{name}.ttf')
print('fonts instanced')
"
fi

# 3) Build the document
python doc/build.py
echo "Done → build/Project_Verde_Documentation.pdf"
