import type { Config } from "tailwindcss";

/**
 * NIGHT LAB — the Project Verde showcase design system.
 * A botanical laboratory at 2 AM: near-black teal base, chlorophyll energy,
 * UV-violet AI accents, hydro-cyan water/cloud accents.
 */
const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#050D0B",
          2: "#081410",
          3: "#0B1B15",
          4: "#10251D",
        },
        lime: {
          DEFAULT: "#A6FF3F",
          soft: "#C7FF7A",
          dim: "#6FCB2E",
          ghost: "rgba(166,255,63,0.12)",
        },
        uv: {
          DEFAULT: "#A78BFA",
          soft: "#C4B5FD",
          ghost: "rgba(167,139,250,0.12)",
        },
        hydro: {
          DEFAULT: "#67E8F9",
          dim: "#22D3EE",
          ghost: "rgba(103,232,249,0.12)",
        },
        dew: {
          DEFAULT: "#E9FFF2",
          dim: "#B8D8C6",
          mute: "#63806F",
        },
        amber: {
          DEFAULT: "#FFC24B",
        },
        danger: "#FF5C6C",
      },
      fontFamily: {
        display: ["var(--font-display)", "system-ui", "sans-serif"],
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"],
      },
      letterSpacing: {
        ultra: "0.32em",
      },
      keyframes: {
        marquee: {
          "0%": { transform: "translateX(0%)" },
          "100%": { transform: "translateX(-50%)" },
        },
        grain: {
          "0%, 100%": { transform: "translate(0, 0)" },
          "12.5%": { transform: "translate(-2%, 3%)" },
          "25%": { transform: "translate(3%, -2%)" },
          "37.5%": { transform: "translate(-3%, -3%)" },
          "50%": { transform: "translate(2%, 2%)" },
          "62.5%": { transform: "translate(-1%, 2%)" },
          "75%": { transform: "translate(2%, -3%)" },
          "87.5%": { transform: "translate(-2%, 1%)" },
        },
        floaty: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-14px)" },
        },
        scanline: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100vh)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 50%" },
          "100%": { backgroundPosition: "200% 50%" },
        },
        pingring: {
          "0%": { transform: "scale(1)", opacity: "0.7" },
          "100%": { transform: "scale(2.6)", opacity: "0" },
        },
        bootup: {
          "0%": { width: "0%" },
          "100%": { width: "100%" },
        },
        blinker: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.15" },
        },
      },
      animation: {
        marquee: "marquee 30s linear infinite",
        grain: "grain 0.9s steps(8) infinite",
        floaty: "floaty 7s ease-in-out infinite",
        scanline: "scanline 9s linear infinite",
        shimmer: "shimmer 2.4s linear infinite",
        pingring: "pingring 1.8s cubic-bezier(0,0,0.2,1) infinite",
        bootup: "bootup 1.4s cubic-bezier(0.65,0,0.35,1) forwards",
        blinker: "blinker 1.1s steps(2) infinite",
      },
      boxShadow: {
        "glow-lime": "0 0 24px rgba(166,255,63,0.28), 0 0 64px rgba(166,255,63,0.10)",
        "glow-uv": "0 0 24px rgba(167,139,250,0.28)",
        "glow-hydro": "0 0 24px rgba(103,232,249,0.22)",
      },
      backgroundImage: {
        "grid-thin":
          "linear-gradient(rgba(233,255,242,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(233,255,242,0.05) 1px, transparent 1px)",
      },
      backgroundSize: {
        "grid-44": "44px 44px",
      },
    },
  },
  plugins: [],
};

export default config;
