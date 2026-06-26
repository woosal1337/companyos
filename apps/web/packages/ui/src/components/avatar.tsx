"use client";

import * as React from "react";
import { Avatar as AvatarPrimitive } from "radix-ui";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../lib/cn";

const avatarVariants = cva(
  "relative flex shrink-0 overflow-hidden rounded-full ring-1 ring-inset ring-border/70",
  {
    variants: {
      size: {
        xs: "size-5 text-[9px]",
        sm: "size-6 text-[10px]",
        md: "size-8 text-caption",
        lg: "size-10 text-small",
        xl: "size-12 text-body",
      },
    },
    defaultVariants: {
      size: "md",
    },
  }
);

export interface AvatarProps
  extends React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root>,
    VariantProps<typeof avatarVariants> {
  name: string;
  src?: string | null;
  tone?: "auto" | "neutral";
}

const fallbackTones = [
  "bg-accent-muted text-accent",
  "bg-success-muted text-success",
  "bg-warning-muted text-warning",
  "bg-danger-muted text-danger",
  "bg-lavender text-lavender-foreground",
] as const;

function initials(name: string): string {
  const parts = name.trim().split(/\s+/);
  const first = parts[0]?.charAt(0) ?? "?";
  const last = parts.length > 1 ? (parts[parts.length - 1]?.charAt(0) ?? "") : "";
  return (first + last).toUpperCase();
}

function toneIndex(name: string): number {
  let hash = 0;
  for (let i = 0; i < name.length; i += 1) {
    hash = (hash * 31 + name.charCodeAt(i)) % 2147483647;
  }
  return hash % fallbackTones.length;
}

export const Avatar = React.forwardRef<
  React.ComponentRef<typeof AvatarPrimitive.Root>,
  AvatarProps
>(({ className, size, name, src, tone = "auto", ...props }, ref) => (
  <AvatarPrimitive.Root
    ref={ref}
    className={cn(avatarVariants({ size }), className)}
    {...props}
  >
    {src ? <AvatarPrimitive.Image src={src} alt={name} className="aspect-square size-full object-cover" /> : null}
    <AvatarPrimitive.Fallback
      delayMs={src ? 300 : 0}
      className={cn(
        "flex size-full items-center justify-center font-semibold tracking-tight",
        tone === "auto" ? fallbackTones[toneIndex(name)] : "bg-subtle text-muted-foreground"
      )}
    >
      {initials(name)}
    </AvatarPrimitive.Fallback>
  </AvatarPrimitive.Root>
));
Avatar.displayName = "Avatar";
