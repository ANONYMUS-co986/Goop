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
REPO_ROOT="/home/user/Goop/vikaas-hq/v2-app/src"
ROUTES=("/" "/drawer" "/proof" "/kabadi" "/boot?fast=1" "/type" "/app" "/app/book" "/app/centres" "/app/map" "/app/receipts" "/app/assistant" "/app/dashboard" "/app/login" "/app/admin")
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
for mod in /src/App.jsx /src/main.jsx /src/shell/Shell.jsx /src/pages/Gate.jsx /src/pages/Drawer.jsx /src/pages/Boot.jsx /src/pages/Type.jsx /src/pages/AppHome.jsx /src/pages/Book.jsx /src/pages/Centres.jsx /src/pages/MapPage.jsx /src/pages/Receipts.jsx /src/pages/Assistant.jsx /src/pages/Dashboard.jsx /src/pages/Login.jsx /src/pages/Admin.jsx /src/pages/Proof.jsx /src/pages/Kabadi.jsx /src/pages/ComingSoon.jsx; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE$mod")
  verdict "module $mod" "$([ "$code" = "200" ] && echo 0 || echo 1)" "HTTP $code"
done
for css in /src/assets/css/shell.css /src/assets/css/gate.css /src/assets/css/drawer.css /src/assets/css/boot.css /src/pages/type.css /src/pages/apphome.css /src/pages/book.css /src/pages/centres.css /src/pages/map.css /src/pages/receipts.css /src/pages/assistant.css /src/pages/op.css /src/pages/proof.css /src/pages/kabadi.css /src/pages/comingsoon.css; do
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

# ---- 5b. JSX BALANCE gate (every page file: open==close section tags) ----
echo "── 5b. JSX BALANCE ──"
BAL_OK=1
for jsx in "$REPO_ROOT"/*.jsx "$REPO_ROOT"/**/*.jsx; do
  [ -f "$jsx" ] || continue
  o=$(grep -o '<section' "$jsx" | wc -l); c=$(grep -o '</section>' "$jsx" | wc -l)
  if [ "$o" != "$c" ]; then echo "  ❌ $jsx: $o open / $c close"; BAL_OK=0; fi
done
# also main-level balance via node check is overkill; section check catches the class
verdict "jsx-balance" "$([ "$BAL_OK" = "1" ] && echo 0 || echo 1)" "section tags balanced"

# ---- 6. CLICK GATE ----
echo "── 6. CLICKS ──"
if node "$ENGINE/probe_clicks_gate.js" "$BASE" 2>/dev/null; then
  verdict "clicks" 0 "menu + all links clickable"
else
  verdict "clicks" 1 "menu/links not clickable"
fi

echo ""
# ---- 7. REBEE CHAT GATE (real-AI fallback path) ----
echo "── 7. REBEE CHAT ──"
if node "$ENGINE/probe_rebee.js" "$BASE" 2>/dev/null; then
  verdict "rebee-chat" 0 "chips + fallback replies + free text"
else
  verdict "rebee-chat" 1 "chat probe failed"
fi

echo "═══ VERDICT: $pass ✅ / $fail ❌ ═══"
[ "$fail" = "0" ] && echo "GATE: PASS — ship it." || { echo "GATE: FAIL — fix before shipping."; exit 1; }
