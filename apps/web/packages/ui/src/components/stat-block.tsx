import * as React from "react";
import { cn } from "../lib/cn";

export interface StatBlockProps extends React.HTMLAttributes<HTMLDivElement> {
  value: React.ReactNode;
  label: React.ReactNode;
  hint?: React.ReactNode;
  align?: "left" | "center";
}

export const StatBlock = React.forwardRef<HTMLDivElement, StatBlockProps>(
  ({ className, value, label, hint, align = "left", ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "flex flex-col gap-1",
        align === "center" ? "items-center text-center" : "items-start text-left",
        className
      )}
      {...props}
    >
      <span className="text-h1 font-semibold tracking-[-0.03em] tabular-nums text-foreground">
        {value}
      </span>
      <span className="text-small font-medium text-foreground">{label}</span>
      {hint ? <span className="text-caption text-muted-foreground">{hint}</span> : null}
    </div>
  )
);
StatBlock.displayName = "StatBlock";
