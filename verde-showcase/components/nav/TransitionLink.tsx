"use client";

import Link from "next/link";
import type { ComponentProps } from "react";

/**
 * A Link that plays the Switch curtain before navigating — the loader
 * between rooms. Modifier clicks / new-tab intents fall through to the
 * browser untouched.
 */
export default function TransitionLink({
  href,
  label,
  onNavigate,
  children,
  ...rest
}: ComponentProps<typeof Link> & { label?: string; onNavigate?: () => void }) {
  return (
    <Link
      href={href}
      {...rest}
      onClick={(e) => {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || rest.target === "_blank") return;
        e.preventDefault();
        onNavigate?.();
        const text = label ?? (typeof children === "string" ? children : String(href));
        window.dispatchEvent(
          new CustomEvent("verde:cover", { detail: { href: String(href), label: text } })
        );
      }}
    >
      {children}
    </Link>
  );
}
