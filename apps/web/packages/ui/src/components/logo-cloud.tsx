import * as React from "react";
import { cn } from "../lib/cn";

export interface LogoCloudProps extends React.HTMLAttributes<HTMLDivElement> {
  label?: React.ReactNode;
  items?: React.ReactNode[];
}

export const LogoCloud = React.forwardRef<HTMLDivElement, LogoCloudProps>(
  ({ className, label, items = [], children, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col items-center gap-6", className)} {...props}>
      {label ? (
        <p className="text-caption font-medium uppercase tracking-[0.04em] text-muted-foreground">
          {label}
        </p>
      ) : null}
      <div className="flex flex-wrap items-center justify-center gap-x-10 gap-y-6 text-muted-foreground">
        {items.map((item, i) => (
          <span
            key={i}
            className="text-body font-semibold tracking-[-0.01em] opacity-70 transition-opacity duration-150 hover:opacity-100"
          >
            {item}
          </span>
        ))}
        {children}
      </div>
    </div>
  )
);
LogoCloud.displayName = "LogoCloud";
