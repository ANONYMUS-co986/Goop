import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SplitText } from "gsap/SplitText";

// single registration point — every scroll-driven component imports from here
// so plugins are registered exactly once (safe under Fast Refresh too)
if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger, SplitText);
  // QA/dev bridge — lets the headless harness dial timeScale for mid-flight
  // animation receipts. Harmless in prod (a single reference, no side-effects).
  (window as unknown as { __gsap?: typeof gsap }).__gsap = gsap;
}

export { gsap, ScrollTrigger, SplitText };
