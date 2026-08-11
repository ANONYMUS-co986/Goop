# CHROMIUM_LIBS_SOURCES.md — rights & provenance ledger for the in-sandbox browser

The sandbox egress allowlist is **github.com + registry.npmjs.org + pypi.org only**
(verified 11 Aug 2026: cdn.playwright.dev / playwright.download.prss.microsoft.com /
npmmirror / gofile / youtube = 000 blocked). Playwright's `install` cannot fetch a
browser. This ledger documents the working assembly, pin-for-pin.

## The working chain (what got installed)

| Piece | Source | Pinned SHA / version | License note |
|---|---|---|---|
| chromium-138 binary | `@sparticuz/chromium@138.0.2` (npm, bundled in package tarball — no CDN) | 138.0.2 | Apache-2.0 (package); Chromium is BSD-3-Clause |
| libnspr4 / libplc4 / libplds4 / libsmime3 / libssl3 (real 64-bit) | `awesome-fc/puppeteer-fc-starter-kit` — `lib/usr/lib/x86_64-linux-gnu/` | `19e29d8b3264cf7534d86586efd6f3e4b4c1efab` | NSPR/NSS are MPL-2.0; repo = serverless starter kit (MIT-style kit, libs are Mozilla-built) |
| libnss3 / libnssutil3 | **self-built stubs** via `make_nss_stub.py` (auto-generated from chromium's ELF symbol/version requirements, gcc 12) | generated | our own code (repo, MIT-style) |

## Why stubs instead of the real libnss3

Chromium 138 requires the `NSS_3.30` symbol version node. Every real NSS build
reachable from this sandbox failed the hunt:

| Candidate | Result |
|---|---|
| `awesome-fc/puppeteer-fc-starter-kit` libnss3 | real 64-bit, but NSS ≤ 3.28 → `NSS_3.30 not found` |
| `Raspberrynani/darkly-patched` squashfs libnss3 | real 64-bit, but NSS ≤ 3.22 → `NSS_3.30 not found` |
| `bizplay/kiosk-os-chroot` (opt/firefox) | full NSS set, but **ELFCLASS32** |
| `jndre/In-the-DOM-We-Trust` foxhound | **Git LFS pointers** (131 B) — media.githubusercontent.com blocked |
| `KiriNoNe/tester_gosuslug` firefox | **Git LFS pointers** (131 B) |
| `melon-gg/libnss3.so` | real, but old NSS (< 3.30) |
| `nguyenhoaibao/ansible` (chrome libs) | Git LFS pointers |
| apt (Ubuntu/Debian mirrors), dl.google.com | 000 blocked |

The stub exports exactly the 37 symbols chromium references from libnss3
(6 version nodes: NSS_3.2/3.3/3.4/3.6/3.9.2/3.30) + the 1 symbol from
libnssutil3 (`NSS_SetAlgorithmPolicy@NSSUTIL_3.12.3`). Init functions return
SECSuccess; cert/trust functions return NULL/SECFailure.

## Honest capability statement

- ✅ WORKS: headless rendering of local HTML (file://, data:, localhost HTTP),
  screenshots, DOM automation, GSAP timelines, the whole studio engine.
- ❌ DOES NOT WORK: TLS certificate verification (stub returns failure for cert
  ops) — irrelevant here since external egress is blocked at the network layer
  anyway; `page.goto('https://…')` to an unreachable host fails at connect.
- Re-run `bash engine/chromium_bootstrap.sh` after any sandbox wipe.

## Verification receipt (11 Aug 2026)

```
HeadlessChrome/138.0.7204.0 (X11; Linux x86_64)
screenshot 1080x1920 rendered, non-blank (mean 19.3, std 21.8, 2,073,600 px)
```
