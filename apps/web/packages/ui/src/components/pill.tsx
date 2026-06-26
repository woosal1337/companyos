import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../lib/cn";

const pillVariants = cva(
  "inline-flex items-center gap-1.5 whitespace-nowrap rounded-full border text-caption font-medium leading-none transition-colors [&_svg]:size-3.5",
  {
    variants: {
      variant: {
        neutral: "border-border bg-surface text-muted-foreground shadow-xs",
        accent: "border-accent-subtle bg-accent-muted text-accent",
        solid: "border-transparent bg-foreground text-background",
      },
      size: {
        sm: "h-6 px-2.5",
        md: "h-7 px-3",
      },
    },
    defaultVariants: {
      variant: "neutral",
      size: "md",
    },
  }
);

export interface PillProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof pillVariants> {
  dot?: boolean;
  icon?: React.ReactNode;
}

export const Pill = React.forwardRef<HTMLSpanElement, PillProps>(
  ({ className, variant, size, dot = false, icon, children, ...props }, ref) => (
    <span ref={ref} className={cn(pillVariants({ variant, size }), className)} {...props}>
      {dot ? (
        <span
          aria-hidden="true"
          className={cn(
            "size-1.5 shrink-0 rounded-full",
            variant === "accent" ? "bg-accent" : variant === "solid" ? "bg-background" : "bg-accent"
          )}
        />
      ) : null}
      {icon ? <span className="flex shrink-0 items-center">{icon}</span> : null}
      {children}
    </span>
  )
);
Pill.displayName = "Pill";

export interface EyebrowProps extends React.HTMLAttributes<HTMLParagraphElement> {
  accent?: boolean;
}

export const Eyebrow = React.forwardRef<HTMLParagraphElement, EyebrowProps>(
  ({ className, accent = true, ...props }, ref) => (
    <p
      ref={ref}
      className={cn(
        "text-eyebrow font-semibold uppercase",
        accent ? "text-accent" : "text-muted-foreground",
        className
      )}
      {...props}
    />
  )
);
Eyebrow.displayName = "Eyebrow";
