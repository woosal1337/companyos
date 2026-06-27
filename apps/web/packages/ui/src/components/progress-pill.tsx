import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../lib/cn";

const progressPillVariants = cva(
  "inline-flex items-center gap-2 whitespace-nowrap rounded-full border leading-none transition-colors",
  {
    variants: {
      variant: {
        neutral: "border-border bg-surface text-muted-foreground",
        accent: "border-accent-subtle bg-accent-muted text-accent",
        success: "border-transparent bg-success-muted text-success",
      },
      size: {
        sm: "h-5 px-2 text-caption",
        md: "h-6 px-2.5 text-num-sm",
      },
    },
    defaultVariants: {
      variant: "neutral",
      size: "md",
    },
  }
);

const barColor = {
  neutral: "bg-muted-foreground",
  accent: "bg-accent",
  success: "bg-success",
} as const;

export interface ProgressPillProps
  extends Omit<React.HTMLAttributes<HTMLSpanElement>, "children">,
    VariantProps<typeof progressPillVariants> {
  value: number;
  total: number;
  showBar?: boolean;
  format?: "fraction" | "percent";
  label?: string;
}

export const ProgressPill = React.forwardRef<HTMLSpanElement, ProgressPillProps>(
  (
    {
      className,
      variant,
      size,
      value,
      total,
      showBar = true,
      format = "fraction",
      label = "Progress",
      ...props
    },
    ref
  ) => {
    const safeTotal = Math.max(0, total);
    const safeValue = Math.min(Math.max(0, value), safeTotal || value);
    const ratio = safeTotal > 0 ? safeValue / safeTotal : 0;
    const percent = Math.round(ratio * 100);
    const text = format === "percent" ? `${percent}%` : `${safeValue} / ${safeTotal}`;
    const resolvedVariant = variant ?? (safeTotal > 0 && safeValue >= safeTotal ? "success" : "neutral");

    return (
      <span
        ref={ref}
        role="progressbar"
        aria-valuenow={safeValue}
        aria-valuemin={0}
        aria-valuemax={safeTotal}
        aria-label={label}
        aria-valuetext={text}
        className={cn(progressPillVariants({ variant: resolvedVariant, size }), className)}
        {...props}
      >
        {showBar ? (
          <span
            aria-hidden="true"
            className="relative h-1 w-8 shrink-0 overflow-hidden rounded-full bg-border-strong"
          >
            <span
              className={cn(
                "absolute inset-y-0 left-0 rounded-full transition-[width]",
                barColor[resolvedVariant]
              )}
              style={{ width: `${Math.round(ratio * 100)}%` }}
            />
          </span>
        ) : null}
        <span className="tabular font-medium">{text}</span>
      </span>
    );
  }
);
ProgressPill.displayName = "ProgressPill";
