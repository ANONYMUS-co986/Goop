export type VerdeRoute = {
  href: string;
  label: string;
  batch: string;
  live: boolean;
  blurb: string;
  ghost: string;
};

export const ROUTES: VerdeRoute[] = [
  { href: "/", label: "Home", batch: "B1", live: true, blurb: "The hook, the hologram, the heartbeat.", ghost: "00" },
  { href: "/build", label: "The Build", batch: "B2", live: true, blurb: "Exploded ESP32 — every wire on camera.", ghost: "01" },
  { href: "/brain", label: "The Brain", batch: "B3", live: true, blurb: "The bug that nearly killed us: 17 calls → 2.", ghost: "02" },
  { href: "/doctor", label: "AI Doctor", batch: "B4", live: true, blurb: "Point, click — the leaf gets a diagnosis.", ghost: "03" },
  { href: "/proof", label: "Proof Wall", batch: "B5", live: false, blurb: "13/13 tests. 10 bugs. Zero reboots.", ghost: "04" },
  { href: "/team", label: "Team Verde", batch: "B6", live: false, blurb: "Two builders, one greenhouse OS.", ghost: "05" },
];
