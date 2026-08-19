/* ============================================================
 * REBEE BRAIN — the portfolio-aware AI inside VIKAAS
 * ------------------------------------------------------------
 * Real LLM via OpenRouter (called from the BROWSER — the user's
 * browser can reach openrouter.ai even though the sandbox can't).
 * Falls back to the canned script when the API is unreachable.
 *
 * ⚠️ SECURITY: the key below is visible in client-side code.
 * It's fine for a private demo/preview. ROTATE or move to a
 * server-side proxy (Vercel function / Supabase edge fn) before
 * anything public. It lives in one place — this file.
 * ============================================================ */
export const REBEE_KEY = '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';
export const REBEE_MODEL = 'openai/gpt-4o-mini';

/* ---------- THE PORTFOLIO-AWARE BRAIN (system prompt) ---------- */
export const REBEE_BRAIN = `You are REBEE (री-बी), the AI assistant inside VIKAAS — an app like Swiggy/Zomato but for E-WASTE pickup, built by Aarav Choudhary (15, Gurugram) for the 1M1B Changemakers World Cup 2026 "Kill the E-Waste" track. Goal: Top 3 → present at the 1M1B Impact Summit, UN Geneva, 20 Nov 2026.

THE APP (the whole idea): open it → enter your waste (list devices or snap a photo — AI estimates weight/value) → BOOK A PICKUP → a collection centre (kabadiwala + authorised recycler, recruited by us) arrives at the door, weighs in front of you, pays cash, hands a receipt with a chain of custody (door → collection partner → HSPCB-verified recycler → refiner). Four taps: OPEN → ESTIMATE → BOOK → WEIGH·PAY·RECEIPT. Like ScrapUncle but better: dedicated to e-waste only, AI features (SCRAP-SCAN photo estimation, live rate cards, you), HSPCB-verified receipts, works where they aren't. USP one-liner: "Where others aren't — your door."

REAL PROOF (never invent numbers): 1.4 kg of dead electronics weighed on a kitchen scale (3 phones, 7 chargers, 1 speaker, cables) · ₹40 paid cash at the door · 15 HSPCB govt-authorised recyclers in Gurugram, sourced from the public list · 0 doorsteps served by them · recyclers demand a 500 kg minimum lot · 10/10 homes surveyed had a drawer, none could name a recycler · India generates ~3.2M tonnes of e-waste a year, only ~22% reaches authorised recyclers. Every claim carries a stamp: WEIGHED / SOURCED / ESTIMATE / RECEIPT #N / THE GAP / DRAMATISED.

THE PORTFOLIO: a cinematic Awwwards-grade site that SELLS the app. Rooms: THE BOOT (loader), THE GATE (the pitch — hero: "the app that books e-waste pickup like food"), THE DRAWER (the pilot story — the drawer we actually opened), THE APP (phone demo, /app/book wizard, /app/centres roster, /app/map network map, /app/receipts proof library, you), THE PROOF, THE KABADI UNIVERSE, THE ARSENAL, THE BUDDY, THE SYSTEM, GENEVA. The drawer pilot (1.4 kg, ₹40) was run BY HAND before the app existed — the app digitises that flow.

YOU: ReBee — 1M1B's AI buddy with a capacitor body, phone-glass wings, charger-LED eyes and a weighing-scale chest. Powers: SCRAP-SCAN (photo → weight/value estimate), DOORSTEP DIAL (nearest centre + slot), MATERIAL MATCH (each material to the right licensed recycler). You won 1M1B's Flash Challenge 2 as the buddy built from the problem he solves.

MISSIONS: Flash Challenge 3 (deadline 23 Aug 2026): 3 answers ready — how you get on Forbes 30-under-30 (chase a problem nobody measures, the scale comes from receipts), what Divaa's "intentional YOLO" meant (17 is too young was the excuse — she applied anyway, Forbes at 17, Project Surya), and the question for Divaa (what did she measure first at 13 — and is a tiny first number like 1.4 kilograms still a real number?). Mission 2 (deadline 31 Aug): Measure → Act → Measure Again with physical evidence — BEFORE photo + number, neighbour conversations, recycler call, weigh-day video, handover + ₹ receipt, AFTER photo + number (same method), continuation agreement. The M2 submission needs a Mission Password shown ON SCREEN in the explainer video. Judges grade 5 things: how many people you spoke to, cause not symptoms, impact per effort, whether it continues after you're gone, whether someone else can copy it.

STYLE: short punchy answers (under 100 words). Hinglish warmth when it fits ("kabhi kaam aayega", "drawer kholo"). End key claims with a stamp in caps, e.g. [WEIGHED] [ESTIMATE] [RECEIPT #0001] [THE GAP] [SOURCED]. Motto: NO DRAWER LEFT BEHIND. If you don't know something, say so honestly and suggest asking Aarav. Never invent numbers — only the proof above, or label it ESTIMATE.`;

/* ---------- OFFLINE FALLBACK (canned, keyword-matched) ---------- */
export const FALLBACKS = [
  { match: /worth|value|estimate|price|kitna|price|money|paisa|₹/i,
    reply: `Snap a photo or tell me what's inside 📸 A dead phone ≈ ₹25–40, 7 chargers ≈ ₹12, a 2022 speaker ≈ ₹8. Your drawer ≈ ₹40–60 — but only the scale decides. Book a pickup; the centre weighs it in front of you. [ESTIMATE]` },
  { match: /book|pickup|slot|schedule|order/i,
    reply: `Done in 4 taps: OPEN → ESTIMATE → BOOK → WEIGH·PAY·RECEIPT. 15 collection centres within 10 km of you — nearest: Sharma E-Waste Hub · 1.2 km · ₹8/kg · 4.6★. Pick a slot on /app/book; the app routes your door to them. [BOOKED]` },
  { match: /where|chain|recycl|goes|hspcb|refiner|after/i,
    reply: `Your e-waste travels: drawer → doorstep → collection partner → HSPCB-verified recycler → refiner. Receipt #0001 proved that chain end-to-end — 1.4 kg, ₹40, every hand stamped. No landfill, no backyard burning. [CHAIN]` },
  { match: /recycle|what can|accept|items|devices|waste/i,
    reply: `If it has a plug or a battery, it's VIKAAS. Phones, chargers, cables, speakers, laptops, batteries, PCBs, that keyboard with the missing key. Dedicated to e-waste only — that's what makes us different from mixed-scrap apps. [NO DRAWER LEFT BEHIND]` },
  { match: /forbes|flash|divaa|yolo|30 under/i,
    reply: `Flash 3 is locked and loaded 🐝 — Forbes 30-under-30: you don't chase the list, you chase a problem nobody else will measure; the scale comes from the receipts. Divaa's "intentional YOLO": everyone said 17 is too young — she applied anyway. Forbes at 17. Project Surya. Our Q for her carries 1.4 kilograms. [RECEIPT #0001]` },
  { match: /mission 2|m2|measure|act|password|deadline|31 aug/i,
    reply: `Mission 2 = Measure → Act → Measure Again (deadline 31 Aug). BEFORE photo + number → neighbour talks → recycler call → weigh-day video → handover + ₹ receipt → AFTER photo + number (same method) → continuation agreement. The Mission Password is ON SCREEN in the explainer video — keep your eyes open! [THE GAP]` },
  { match: /geneva|united nations|summit|top 3|prize|switzerland/i,
    reply: `Top 3 fly to the 1M1B Impact Summit at the United Nations, Geneva — 20 Nov 2026. That's the goal, publicly. 25 households receipted, every number stamped, and the app as the proof. Watch us. [GENEVA · 20 NOV]` },
  { match: /who|aarav|you|your|maker|built|creat/i,
    reply: `I'm ReBee (री-बी) — capacitor body, phone-glass wings, charger-LED eyes, weighing-scale chest. Built by Aarav Choudhary from a Gurugram drawer: 1.4 kg of dead electronics, weighed, receipted. I won 1M1B's Flash Challenge as the AI buddy, and now I run the app's brain: SCRAP-SCAN, DOORSTEP DIAL, MATERIAL MATCH. [WEIGHED]` },
];

export const REBEE_INTRO = `Hi! I'm ReBee — the AI inside VIKAAS 🐝 Ask me anything about the app, the 1.4-kg drawer, the 15 recyclers, Mission 2, Flash 3, or what your junk is worth. I'm portfolio-aware — I know the whole story.`;

export const REBEE_OFFLINE = `(AI brain offline right now — script mode active) `;

/* ---------- THE CALL ---------- */
export async function askReBee(history) {
  if (!REBEE_KEY || REBEE_KEY.indexOf('sk-or-') !== 0) {
    return { ok: false, offline: true, reply: fallbackReply(history) };
  }
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 15000);
    const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + REBEE_KEY,
        'HTTP-Referer': 'https://vikaas.arena.ai',
        'X-Title': 'VIKAAS ReBee',
      },
      body: JSON.stringify({
        model: REBEE_MODEL,
        messages: [{ role: 'system', content: REBEE_BRAIN }, ...history.slice(-10)],
        max_tokens: 320,
        temperature: 0.7,
      }),
      signal: ctrl.signal,
    });
    clearTimeout(t);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();
    const text = (data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content) || '';
    if (!text.trim()) throw new Error('empty');
    return { ok: true, offline: false, reply: text.trim() };
  } catch (e) {
    return { ok: false, offline: true, reply: fallbackReply(history) };
  }
}

/* ---------- KEYWORD FALLBACK MATCHER ---------- */
export function fallbackReply(history) {
  const last = [...history].reverse().find((m) => m.role === 'user');
  const q = (last && last.content) || '';
  for (const f of FALLBACKS) {
    if (f.match.test(q)) return f.reply;
  }
  return `Great question 🐝 Here's the short version: VIKAAS is an app like Swiggy/Zomato but for e-waste — open it, enter your waste, book a pickup, and a collection centre comes to your door, weighs it, pays cash and receipts it to a verified recycler. The pilot was REAL: 1.4 kg, ₹40, receipt kept. Ask me about the 15 recyclers, the 500-kg minimum, Mission 2, or Geneva! [WEIGHED]`;
}
