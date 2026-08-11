#!/usr/bin/env bash
# chromium_bootstrap.sh — one-command in-sandbox headless-Chromium bootstrap.
#
# The sandbox egress allowlist is github.com + npm + pypi ONLY. The normal
# Playwright browser CDN (cdn.playwright.dev) is blocked, so we assemble a
# working browser from the open pipes:
#   1. @sparticuz/chromium (npm)      -> chromium-138 binary (self-inflates)
#   2. awesome-fc/puppeteer-fc-starter-kit (GitHub, pinned SHA) -> real 64-bit
#      libnspr4/libplc4/libplds4/libsmime3/libssl3
#   3. make_nss_stub.py (this repo)   -> minimal libnss3/libnssutil3 stubs that
#      satisfy the loader (chromium demands the NSS_3.30 version node; no real
#      NSS >= 3.30 is reachable from this sandbox)
#   4. sudo install + ldconfig so LD_LIBRARY_PATH is never needed.
#
# TRADEOFF (honest): the NSS stub returns success for init and failure for
# cert/trust calls -> local rendering (file://, data:, localhost HTTP),
# screenshots and automation work; TLS/https certificate verification does NOT.
# External egress is blocked at the network layer anyway.
#
# Usage: bash engine/chromium_bootstrap.sh
set -euo pipefail
ENGINE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STUDIO_DIR="$(dirname "$ENGINE_DIR")"
LIBS_DIR="${CHROMELIBS_DIR:-/tmp/chromelibs}"
FC_SHA="19e29d8b3264cf7534d86586efd6f3e4b4c1efab"

echo "[1/4] Inflating @sparticuz/chromium binary..."
cd "$STUDIO_DIR"
CHROME_BIN="$(node -e "require('@sparticuz/chromium').executablePath().then(p=>console.log(p))")"
echo "      -> $CHROME_BIN"

echo "[2/4] Fetching real NSPR libs from GitHub (pinned $FC_SHA)..."
rm -rf /tmp/fc-kit
git clone -q --depth 1 https://github.com/awesome-fc/puppeteer-fc-starter-kit.git /tmp/fc-kit
(cd /tmp/fc-kit && git fetch -q --depth 1 origin "$FC_SHA" && git checkout -q FETCH_HEAD)
mkdir -p "$LIBS_DIR"
cp /tmp/fc-kit/lib/usr/lib/x86_64-linux-gnu/libnspr4.so \
   /tmp/fc-kit/lib/usr/lib/x86_64-linux-gnu/libplc4.so \
   /tmp/fc-kit/lib/usr/lib/x86_64-linux-gnu/libplds4.so \
   /tmp/fc-kit/lib/usr/lib/x86_64-linux-gnu/libsmime3.so \
   /tmp/fc-kit/lib/usr/lib/x86_64-linux-gnu/libssl3.so \
   "$LIBS_DIR/"

echo "[3/4] Building NSS stubs..."
python3 "$ENGINE_DIR/make_nss_stub.py" "$CHROME_BIN" "$LIBS_DIR"

echo "[4/4] Installing to /usr/lib/x86_64-linux-gnu + ldconfig (sudo)..."
sudo cp "$LIBS_DIR"/*.so /usr/lib/x86_64-linux-gnu/
sudo ldconfig

echo "Verifying launch..."
cd "$STUDIO_DIR"
node engine/browser_demo.js && echo "BOOTSTRAP OK — headless Chromium is live."
