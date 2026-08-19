# 🎯 TASK 2 (M2) + FLASH 3 — THE REAL BRIEFS (READ VIA OCR — 19 Aug 2026)

> **BREAKTHROUGH:** I built real OCR in the sandbox (tesseract.js WASM from npm +
> tessdata cloned from GitHub — both open channels) + a contour-vision pipeline
> (OpenCV). **I read all 7 of your screenshots.** These are the exact briefs.

---

## FLASH CHALLENGE #3 — DEADLINE 23 AUG (4 DAYS)

**The task:** Audit the dead devices piling up around you, find them a better
end, and document what you diverted.

**Step 0 — WATCH THE VIDEO (2 min):** `youtu.be/9P6xal4dWKLo` (Divaa — 17, Forbes
30 under 30, started with 1M1B at 13). This is on YOUR phone — the sandbox can't
reach YouTube.

**Submit (Response Text — the form has one box):**
1. **How do you get on the Forbes 30 under 30 list?** (draft below)
2. **What you thought about Divaa's line on "intentional YOLO"** (draft below —
   adjust after you watch the video)
3. **A question for Divaa/Manav** (draft below — make it the most interesting
   one in the country; top 5 = ₹1000 vouchers + Zoom call)

**DRAFT ANSWERS (paste-ready, refine after you watch):**

Q1 — *"How do you get on the Forbes 30 under 30 list?"*
> You don't chase the list. You chase a problem nobody else is willing to
> measure. Forbes 30 under 30 is a list of people who turned a stubborn local
> problem into measurable change — the scale comes from the receipts, not the
> press. In our case: one drawer in Gurugram weighed 1.4 kg of dead electronics.
> Ten homes asked — ten drawers found. Fifteen government-authorised recyclers
> exist on the HSPCB list — zero doorsteps served them. So we became the
> doorstep. We measured the problem (1.4 kg, 10/10 homes), we acted (weighed,
> logged, delivered), and we'll measure again until the number moves. The list
> isn't a goal; it's a byproduct of proving change with numbers.

Q2 — *"What you thought about Divaa's line on 'intentional YOLO'":*
> "You only live once" is usually an excuse to do the easy thing now. Divaa's
> "intentional YOLO" flips it: you only live once, so be deliberate about what
> you spend that one life on. The drawer taught me the same lesson — I'd walked
> past mine for four years, and the only difference between the drawer and a
> changemaker was a decision. Intentional YOLO is choosing the problem that
> outlives you, then acting like today is the only day you get.

Q3 — *The question (the voucher-winner):*
> "Divaa — when you started at 13, what did you measure first? The problem, or
> yourself? And what would you tell a 15-year-old whose first number is tiny —
> like 1.4 kilograms — about why a small number is still a real number?"

**AARAV'S 4-DAY PLAN (the physical part — ~2 hours total):**
1. Watch the video (tonight, 2 min) → confirm Divaa's exact line.
2. Do the audit action: take a NEW photo of the drawer + count the devices
   (weigh if possible) — this is the "audit the dead devices" proof.
3. Paste the 3 answers (drafts above) → submit on cwcsubmission.in (F3 tab).
4. The "document what you diverted" = the drawer photo + our real receipts.

---

## MISSION 2 — DEADLINE 31 AUG (12 DAYS) — "THE ACTION"

**The brief (exact):** Measure. Act. Measure Again. Three steps:
- **STEP 1 — THE AUDIT:** Go back to your Mission 1 problem (the drawer). Visit
  it, count/measure it as it actually happens, photograph it, note the
  alternative already available (the recyclers).
- **STEP 2 — THE CONVERSATION:** Sit with whoever's closest to the problem
  (family/neighbours). LISTEN — why does the drawer exist? Cost? Habit? Never
  raised? What would make change easier? Don't propose yet.
- **STEP 3 — THE CHANGE:** ONE specific switch — the smallest that counts.
  Ours: **a weigh-and-drop day** — the drawer's contents weighed, handed to the
  kabadi network / an authorised recycler, receipted.

**SUBMISSION STRUCTURE (exactly what they grade):**
1. **BEFORE photo** — the drawer (WE HAVE IT — `drawer_real.jpg`).
2. **BEFORE number** — 1.4 kg / 10 homes / 15 recyclers / 0 doorsteps.
3. **TAKE ACTION** — photos/videos/numbers of the drive + calls + weigh-day.
4. **AFTER photo** — the same drawer, emptied (new photo — YOUR JOB).
5. **AFTER number** — kg diverted · ₹ paid · drawer now empty (measured again).
6. **AGREEMENT** — photo/proof that a kabadiwala / recycler / society will
   continue (a signed line, a WhatsApp commitment screenshot).

**THE GOLDEN RULE:** What changed? How much? Can you prove it?
**NON-NEGOTIABLE:** No number = incomplete. No proof = incomplete.
**Format:** PPT or PDF + pictures. **Password:** hidden in the 2 brief videos
(Watch on your phone: `-OgSjIMHUTE` + `OiqD4psEYQU` — find it, it's needed at
submit time!)

**AARAV'S PHYSICAL TO-DO (this week, ~3 hours):**
1. [ ] Watch BOTH brief videos → find the Mission Password → send it to me.
2. [ ] NEW "AFTER" photo: the drawer, emptied/cleared (vs the BEFORE photo).
3. [ ] Weigh-day on camera: the drawer's contents on the kitchen scale (30–60s
      video + photo of the reading) — the "measure again" proof.
4. [ ] Survey 2+ more households (we have 10; brief wants conversation —
      actually TALK to a neighbour: why does your drawer exist? 2–3 questions,
      note answers, photo the drawer if they let you).
5. [ ] One recycler call on speaker (log: who answered, minimum kg, doorstep?)
      — screenshot or note = the "conversation" evidence.
6. [ ] Society drive OR a mini handover: give the drawer's items to the kabadi
      / a compliant route (Croma/Namo/Karo Sambhav/MCG) — photo + ₹ receipt.
7. [ ] Agreement proof: ask the kabadiwala/recycler to write "will accept small
      doorstep lots from this household" + sign/thumbprint + photo. (That's the
      AGREEMENT item — our door-step gap, closing.)
8. [ ] Push all photos/videos to repo `main` → I build the M2 submission
      (PPT/PDF) + the Flash-3 response.

**WHAT I BUILD WHEN YOU SEND THE PROOF:**
- The M2 submission deck (BEFORE/AFTER numbers + photos + story) as PPT/PDF.
- The Flash-3 response text (refined with Divaa's actual line).
- Any supporting poster/reel for the campaign.

---

## THE OCR POWER (how I read your screenshots — banked)
- `engine/ocr.js` — tesseract.js WASM (npm) + `eng.traineddata` (cloned from
  `tesseract-ocr/tessdata_fast` on GitHub, gzipped locally). Works on dark-mode
  screenshots (invert + upscale + Otsu preprocessing).
- `engine/vision_desc.py` — OpenCV contour/MSER pipeline: palette, text blocks,
  panels, buttons → structured JSON layout descriptions.
- **This means I can now READ any screenshot you commit to the repo — task
  briefs, dashboards, error screens, the website's own screenshots.** Eyes: 2.0.
EOF
