#!/usr/bin/env bash
# resurrect.sh — VIKAAS wipe-proof environment restore (7th doctrine: run after any sandbox wipe)
set -euo pipefail
REPO="${1:-/home/user/Goop}"
cd "$REPO"

echo "[1/6] Fetching session branch (explicit refspec — remote.origin.fetch only maps main)"
git fetch origin 'refs/heads/arena/019ff044-goop:refs/remotes/origin/arena/019ff044-goop'
git reset --hard origin/arena/019ff044-goop

echo "[2/6] Recreating venv (OUTSIDE repo — exclusion-proof)"
[ -x /tmp/pw_venv/bin/python ] || python3 -m venv /tmp/pw_venv
/tmp/pw_venv/bin/pip install -q pillow numpy opencv-python-headless==4.10.0.84 pyelftools imageio-ffmpeg soundfile scipy 2>&1 | tail -1

echo "[3/6] Installing app deps"
cd "$REPO/vikaas-hq/v2-app"
[ -x node_modules/.bin/vite ] || npm install 2>&1 | tail -1

echo "[4/6] Inflating chromium binary"
cd "$REPO/vikaas-hq/studio"
CHROME=$(node -e "require('@sparticuz/chromium').executablePath().then(p=>console.log(p))")

echo "[5/6] Building NSS stubs + installing libs"
if [ ! -f /usr/lib/x86_64-linux-gnu/libnspr4.so ]; then
  /tmp/pw_venv/bin/python engine/make_nss_stub.py "$CHROME" /tmp/chromelibs
  sudo cp /tmp/chromelibs/*.so /usr/lib/x86_64-linux-gnu/
  sudo ldconfig
fi

echo "[6/6] Browser smoke test"
node engine/browser_demo.js 2>&1 | tail -1
echo "RESURRECTED — ready."
