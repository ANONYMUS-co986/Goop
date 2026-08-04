"use client";

import { useEffect, useRef } from "react";

export type StormMode = "storm" | "fixed";

type Packet = {
  born: number;      // ms timestamp of spawn
  dur: number;       // ms flight time
  off: number;       // bezier control offset (px)
  lane: number;      // base y lane offset
  hue: "amber" | "danger" | "lime" | "hydro";
  jitter: boolean;
};

const CYCLE = 2600;

/**
 * THE STORM — the 17→2 telemetry bug, drawn live on a 2D canvas.
 * storm: 17 choked packets per cycle + a hard 10s AUTO stutter freeze.
 * fixed: 2 smooth bundle packets. Pure Canvas2D — no WebGL tax —
 * and it pauses offscreen / honors reduced-motion.
 */
export default function StormCanvas({ mode, onCycle }: { mode: StormMode; onCycle?: (calls: number) => void }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const modeRef = useRef(mode);
  const onCycleRef = useRef(onCycle);
  modeRef.current = mode;
  onCycleRef.current = onCycle;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let W = 0, H = 0, dpr = 1;
    let raf = 0;
    let running = true;
    let visible = true;

    const packets: Packet[] = [];
    let slot = 0;               // ordinal spawn slots mapped onto cycle time
    let slotTime = 0;
    let lastReport = -1;

    const resize = () => {
      const r = canvas.getBoundingClientRect();
      dpr = Math.min(2, window.devicePixelRatio || 1);
      W = Math.max(1, Math.round(r.width));
      H = Math.max(1, Math.round(r.height));
      canvas.width = W * dpr;
      canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(canvas);

    const io = new IntersectionObserver(([e]) => { visible = e.isIntersecting; }, { threshold: 0.05 });
    io.observe(canvas);
    const onVis = () => { running = document.visibilityState === "visible"; };
    document.addEventListener("visibilitychange", onVis);

    const easeInOut = (t: number) => t * t * (3 - 2 * t);

    // node anchors recomputed per frame from W/H (responsive)
    const anchors = () => ({
      ax: W * 0.14, ay: H * 0.52,        // ESP32 (left)
      bx: W * 0.86, by: H * 0.42,        // Firebase (right)
    });

    const spawnColor = (i: number, m: StormMode): Packet["hue"] => {
      if (m === "fixed") return i % 2 === 0 ? "lime" : "hydro";
      return i % 5 === 0 ? "danger" : i % 3 === 0 ? "amber" : "amber";
    };
    const COLORS: Record<Packet["hue"], [string, string]> = {
      amber: ["#FFC24B", "rgba(255,194,75,0)"],
      danger: ["#FF5C6C", "rgba(255,92,108,0)"],
      lime: ["#A6FF3F", "rgba(166,255,63,0)"],
      hydro: ["#67E8F9", "rgba(103,232,249,0)"],
    };

    const drawNode = (x: number, y: number, w: number, h: number, label: string, sub: string, accent: string, pulse: number) => {
      ctx.save();
      ctx.strokeStyle = accent;
      ctx.globalAlpha = 0.9;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect(x - w / 2, y - h / 2, w, h, 10);
      ctx.stroke();
      ctx.globalAlpha = 0.06 + pulse * 0.1;
      ctx.fillStyle = accent;
      ctx.fill();
      ctx.globalAlpha = 1;
      ctx.fillStyle = "#E9FFF2";
      ctx.font = "600 11px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText(label, x, y - 2);
      ctx.fillStyle = "rgba(154,184,168,0.9)";
      ctx.font = "500 8.5px 'JetBrains Mono', monospace";
      ctx.fillText(sub, x, y + 12);
      ctx.restore();
    };

    const drawFrame = (now: number, frozen: boolean) => {
      const m = modeRef.current;
      const { ax, ay, bx, by } = anchors();
      const shake = frozen ? (Math.random() - 0.5) * 5 : 0;

      ctx.clearRect(0, 0, W, H);
      ctx.save();
      ctx.translate(shake, shake * 0.6);

      // faint board-grid backdrop
      ctx.strokeStyle = "rgba(16,37,29,0.55)";
      ctx.lineWidth = 1;
      const gs = 44;
      ctx.beginPath();
      for (let gx = (W / 2) % gs; gx < W; gx += gs) { ctx.moveTo(gx, 0); ctx.lineTo(gx, H); }
      for (let gy = (H / 2) % gs; gy < H; gy += gs) { ctx.moveTo(0, gy); ctx.lineTo(W, gy); }
      ctx.stroke();

      // base link line
      ctx.strokeStyle = frozen ? "rgba(255,92,108,0.5)" : "rgba(103,232,249,0.18)";
      ctx.setLineDash([3, 7]);
      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(bx, by);
      ctx.stroke();
      ctx.setLineDash([]);

      const pulse = (Math.sin(now / 420) + 1) / 2;
      drawNode(ax, ay, 108, 46, "ESP32", m === "storm" ? "AUTO refresh 10s" : "bundle writer", "#A6FF3F", pulse);
      drawNode(bx, by, 118, 46, "FIREBASE", m === "storm" ? "REST ×17 / cycle" : "/sensors bundle · /actuators", "#67E8F9", pulse);

      // -------- packet traffic --------
      for (let i = packets.length - 1; i >= 0; i--) {
        const p = packets[i];
        const t = (now - p.born) / p.dur;
        if (t >= 1) { packets.splice(i, 1); continue; }
        const k = easeInOut(Math.max(0, t));
        const mx = (ax + bx) / 2;
        const my = (ay + by) / 2 + p.off;
        // quadratic bezier
        const u = 1 - k;
        let x = u * u * ax + 2 * u * k * mx + k * k * bx;
        let y = u * u * ay + 2 * u * k * my + k * k * by + p.lane;
        if (p.jitter && frozen) y += (Math.random() - 0.5) * 3;
        const [c0, c1] = COLORS[p.hue];
        // trail
        const tk = Math.max(0, k - 0.05);
        const tu = 1 - tk;
        const tx = tu * tu * ax + 2 * tu * tk * mx + tk * tk * bx;
        const ty = tu * tu * ay + 2 * tu * tk * my + tk * tk * by + p.lane;
        const grad = ctx.createLinearGradient(tx, ty, x, y);
        grad.addColorStop(0, c1);
        grad.addColorStop(1, c0);
        ctx.strokeStyle = grad;
        ctx.lineWidth = m === "fixed" ? 2 : 1.2;
        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(x, y);
        ctx.stroke();
        // head
        ctx.fillStyle = c0;
        if (p.hue === "danger") ctx.shadowColor = c0, ctx.shadowBlur = 6;
        ctx.beginPath();
        ctx.arc(x, y, m === "fixed" ? 3 : 2.2, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // -------- stutter overlay --------
      if (frozen) {
        ctx.fillStyle = "rgba(255,92,108,0.05)";
        ctx.fillRect(-8, -8, W + 16, H + 16);
        ctx.fillStyle = "#FF5C6C";
        ctx.font = "700 15px 'JetBrains Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText("!! 10s AUTO STUTTER — UI BLOCKED !!", W / 2, H * 0.16);
        ctx.font = "500 9px 'JetBrains Mono', monospace";
        ctx.fillStyle = "rgba(255,194,75,0.95)";
        ctx.fillText("17 queued REST calls fight for the main thread", W / 2, H * 0.16 + 18);
      }

      ctx.restore();
    };

    if (reduced) {
      // single static frame for reduced-motion users
      packets.push({ born: 0, dur: Infinity, off: 0, lane: 0, hue: "lime", jitter: false });
      drawFrame(performance.now(), false);
      return () => { ro.disconnect(); io.disconnect(); document.removeEventListener("visibilitychange", onVis); };
    }

    const t0 = performance.now();
    const loop = () => {
      raf = requestAnimationFrame(loop);
      if (!running || !visible) return;
      const now = performance.now();
      const m = modeRef.current;

      // cycle bookkeeping
      const cycle = Math.floor((now - t0) / CYCLE);
      const inCycle = (now - t0) % CYCLE;

      // the 10s AUTO stutter: every 4th cycle in storm mode freezes 500ms
      const freezeWindow = m === "storm" && cycle % 4 === 1 && inCycle < 500;
      const frozenNow = freezeWindow;

      // slot-deterministic spawning: exactly N packets per cycle, always
      const N = m === "storm" ? 17 : 2;
      if (!frozenNow && now >= slotTime) {
        const i = slot % N;
        if (m === "storm") {
          packets.push({
            born: now,
            dur: 900 + (i % 7) * 130 + Math.random() * 300,
            off: ((i % 5) - 2) * 34 + (Math.random() - 0.5) * 22,
            lane: ((i % 9) - 4) * 9,
            hue: spawnColor(i, m),
            jitter: true,
          });
        } else {
          packets.push({
            born: now,
            dur: 1450,
            off: i === 0 ? -26 : 22,
            lane: i === 0 ? -6 : 6,
            hue: spawnColor(i, m),
            jitter: false,
          });
        }
        slot++;
        slotTime = Math.max(now + 40, t0 + slot * (CYCLE / N));
      }
      if (inCycle < 120 && cycle !== lastReport) {
        lastReport = cycle;
        onCycleRef.current?.(N);
      }

      drawFrame(now, frozenNow);
    };

    raf = requestAnimationFrame(loop);
    return () => {
      cancelAnimationFrame(raf);
      ro.disconnect();
      io.disconnect();
      document.removeEventListener("visibilitychange", onVis);
    };
  }, []);

  return <canvas ref={canvasRef} className="h-full w-full" aria-hidden />;
}
