import type { Metadata, Viewport } from "next";
import "@fontsource/syne/600.css";
import "@fontsource/syne/700.css";
import "@fontsource/syne/800.css";
import "@fontsource/sora/300.css";
import "@fontsource/sora/400.css";
import "@fontsource/sora/500.css";
import "@fontsource/jetbrains-mono/500.css";
import "./globals.css";
import Grain from "@/components/fx/Grain";
import Cursor from "@/components/fx/Cursor";
import SmoothScroll from "@/components/fx/SmoothScroll";
import Preloader from "@/components/fx/Preloader";
import Burger from "@/components/nav/Burger";

export const metadata: Metadata = {
  title: "VERDE — The Plant That Waters Itself",
  description:
    "Project Verde · Round 2 showcase. A ₹1,890 smart irrigation & plant-care system with a living digital twin — designed and built by Aarav Choudhary & Anuj (Class X) for DAV ACON 5.",
};

export const viewport: Viewport = {
  themeColor: "#050D0B",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="lab-cursor-active min-h-screen">
        <Preloader />
        <SmoothScroll />
        <Cursor />
        <Grain />
        <Burger />
        {children}
      </body>
    </html>
  );
}
