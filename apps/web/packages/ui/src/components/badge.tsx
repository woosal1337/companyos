import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../lib/cn";

export const badgeVariants = cva(
  "inline-flex items-center gap-1.5 whitespace-nowrap rounded-full text-caption font-medium leading-none transition-colors [&_svg]:size-3",
  {
    variants: {
      variant: {
        neutral: "bg-subtle text-muted-foreground",
        accent: "bg-accent-muted text-accent",
        success: "bg-success-muted text-success",
        warning: "bg-warning-muted text-warning",
        danger: "bg-danger-muted text-danger",
        outline: "border border-border bg-transparent text-muted-foreground",
      },
      size: {
        sm: "h-5 px-2",
        md: "h-[1.375rem] px-2.5",
      },
    },
    defaultVariants: {
      variant: "neutral",
      size: "sm",
    },
  }
);

const dotColor = {
  neutral: "bg-muted-foreground",
  accent: "bg-accent",
  success: "bg-success",
  warning: "bg-warning",
  danger: "bg-danger",
  outline: "bg-muted-foreground",
} as const;

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {
  dot?: boolean;
}

export const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant, size, dot = false, children, ...props }, ref) => (
    <span ref={ref} className={cn(badgeVariants({ variant, size }), className)} {...props}>
      {dot ? (
        <span
          aria-hidden="true"
          className={cn("size-1.5 shrink-0 rounded-full", dotColor[variant ?? "neutral"])}
        />
      ) : null}
      {children}
    </span>
  )
);
Badge.displayName = "Badge";
