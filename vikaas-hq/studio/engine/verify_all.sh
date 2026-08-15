#!/usr/bin/env bash
# ============================================================
# VIKAAS QA GATE — verify_all.sh  (the definition of done)
# Usage: bash engine/verify_all.sh [baseUrl]
# Checks, in order:
#   1. COMPILE gate   — every route module returns 200 (no 500s)
#   2. RENDER gate    — main exists, fonts >= 4, scrollHeight > vh
#   3. BLANK gate     — viewport screenshot std >= 8 (no black pages)
#   4. INTERACTION    — suite.js overlap probes + CTA click, desktop+mobile
#   5. CONSOLE gate   — 0 pageerrors / 0 console errors / 0 failed requests
# Prints a verdict table. Any FAIL => phase does not ship.
# ============================================================
set -uo pipefail
BASE="${1:-http://localhost:5173}"
ROUTES=("/" "/drawer" "/boot?fast=1")
ENGINE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT=/tmp/qa_gate
mkdir -p "$OUT"

pass=0; fail=0
verdict() { # $1 name $2 ok(0)/not(1) $3 detail
  if [ "$2" = "0" ]; then echo "  ✅ $1 — $3"; pass=$((pass+1));
  else echo "  ❌ $1 — $3"; fail=$((fail+1)); fi
}

echo "═══ VIKAAS QA GATE ═══  base: $BASE"

# ---- 1. COMPILE gate (curl every route module) ----
echo "── 1. COMPILE ──"
for mod in /src/App.jsx /src/main.jsx /src/components/Shell.jsx /src/pages/Gate.jsx /src/pages/Drawer.jsx /src/pages/Boot.jsx; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE$mod")
  verdict "module $mod" "$([ "$code" = "200" ] && echo 0 || echo 1)" "HTTP $code"
done
for css in /src/assets/css/shell.css /src/assets/css/gate.css /src/assets/css/drawer.css /src/assets/css/boot.css; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE$css")
  verdict "css $css" "$([ "$code" = "200" ] && echo 0 || echo 1)" "HTTP $code"
done
for f in /fonts/Anton.ttf /fonts/SpaceGrotesk.ttf /fonts/NotoSansDevanagari.ttf /audio/boot.wav /audio/enter.wav; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE$f")
  verdict "asset $f" "$([ "$code" = "200" ] && echo 0 || echo 1)" "HTTP $code"
done

# ---- 2-5. per-route deep check via node ----
echo "── 2-5. RENDER + BLANK + INTERACTION + CONSOLE ──"
for route in "${ROUTES[@]}"; do
  if node "$ENGINE/probe_route.js" "$BASE$route" "$OUT/$(echo "$route" | tr '/?=' '___')" 2>/dev/null; then
    verdict "route $route" 0 "all checks"
  else
    verdict "route $route" 1 "probe failed"
  fi
done

# ---- 6. CLICK GATE ----
echo "── 6. CLICKS ──"
if node "$ENGINE/probe_clicks_gate.js" "$BASE" 2>/dev/null; then
  verdict "clicks" 0 "menu + all links clickable"
else
  verdict "clicks" 1 "menu/links not clickable"
fi

echo ""
echo "═══ VERDICT: $pass ✅ / $fail ❌ ═══"
[ "$fail" = "0" ] && echo "GATE: PASS — ship it." || { echo "GATE: FAIL — fix before shipping."; exit 1; }
