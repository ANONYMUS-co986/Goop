// ocr.js — REAL OCR via tesseract.js (WASM from npm) + tessdata cloned from GitHub.
// Usage: node engine/ocr.js <image>
// Preprocess in python first (dark-mode invert + upscale), then OCR.
const { createWorker } = require('tesseract.js');
const path = require('path');
const { execSync } = require('child_process');

(async () => {
  const img = process.argv[2];
  if (!img) { console.error('usage: node ocr.js <image>'); process.exit(1); }
  const prep = '/tmp/ocr_prep.png';
  // preprocess: grayscale → invert if dark → upscale 2x (better OCR)
  execSync(`/tmp/pw_venv/bin/python -c "
import cv2
im = cv2.imread('${img}')
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
if g.mean() < 120: g = 255 - g
g = cv2.resize(g, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
g = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
cv2.imwrite('${prep}', g)
"`);
  const worker = await createWorker('eng', 1, {
    langPath: '/tmp/tessdata',
    cachePath: '/tmp/ocr_cache',
    logger: () => {},
  });
  const { data } = await worker.recognize(prep);
  console.log(data.text);
  await worker.terminate();
})().catch((e) => { console.error('OCR FAIL:', e.message.slice(0, 300)); process.exit(1); });
