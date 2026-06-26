import * as React from "react";
import { cn } from "../lib/cn";

export interface BlueprintProps extends React.HTMLAttributes<HTMLDivElement> {
  label?: string;
  figureClassName?: string;
}

export const Blueprint = React.forwardRef<HTMLDivElement, BlueprintProps>(
  ({ className, label, figureClassName, children, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "relative aspect-video overflow-hidden rounded-xl border border-border bg-background",
        className
      )}
      {...props}
    >
      <div className="pointer-events-none absolute inset-0 bg-grid-sm opacity-50" />
      <div className="pointer-events-none absolute inset-2 rounded-lg border border-border" />
      <div className="pointer-events-none absolute inset-0">
        <span className="absolute left-4 top-4 size-2 border-l border-t border-border-strong" />
        <span className="absolute right-4 top-4 size-2 border-r border-t border-border-strong" />
        <span className="absolute bottom-4 left-4 size-2 border-b border-l border-border-strong" />
        <span className="absolute bottom-4 right-4 size-2 border-b border-r border-border-strong" />
      </div>
      {label ? (
        <span className="pointer-events-none absolute left-5 top-5 font-mono text-mono-label uppercase text-muted-foreground">
          {label}
        </span>
      ) : null}
      <div className="absolute inset-0 flex items-center justify-center p-10">
        <div className={cn("size-full max-h-[78%] max-w-[78%]", figureClassName)}>{children}</div>
      </div>
      <div className="pointer-events-none absolute inset-0 bg-vignette" />
    </div>
  )
);
Blueprint.displayName = "Blueprint";
