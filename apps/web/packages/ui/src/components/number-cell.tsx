import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../lib/cn";

const numberCellVariants = cva("tabular inline-flex items-baseline justify-end gap-1 text-right", {
  variants: {
    size: {
      sm: "text-num-sm",
      md: "text-num",
    },
    tone: {
      default: "text-foreground",
      muted: "text-muted-foreground",
    },
    weight: {
      regular: "font-normal",
      medium: "font-medium",
      semibold: "font-semibold",
    },
  },
  defaultVariants: {
    size: "md",
    tone: "default",
    weight: "medium",
  },
});

const trendColor = {
  up: "text-success",
  down: "text-danger",
  flat: "text-muted-foreground",
} as const;

const trendGlyph = {
  up: "↑",
  down: "↓",
  flat: "→",
} as const;

export interface NumberCellProps
  extends Omit<React.HTMLAttributes<HTMLSpanElement>, "children">,
    VariantProps<typeof numberCellVariants> {
  value: React.ReactNode;
  unit?: React.ReactNode;
  secondary?: React.ReactNode;
  trend?: "up" | "down" | "flat";
}

export const NumberCell = React.forwardRef<HTMLSpanElement, NumberCellProps>(
  ({ className, size, tone, weight, value, unit, secondary, trend, ...props }, ref) => (
    <span
      ref={ref}
      className={cn(numberCellVariants({ size, tone, weight }), className)}
      {...props}
    >
      <span className="inline-flex items-baseline gap-0.5">
        {value}
        {unit ? (
          <span className="text-caption font-normal text-muted-foreground">{unit}</span>
        ) : null}
      </span>
      {trend ? (
        <span aria-hidden="true" className={cn("text-caption", trendColor[trend])}>
          {trendGlyph[trend]}
        </span>
      ) : null}
      {secondary != null ? (
        <span className="text-caption font-normal text-muted-foreground">{secondary}</span>
      ) : null}
    </span>
  )
);
NumberCell.displayName = "NumberCell";
