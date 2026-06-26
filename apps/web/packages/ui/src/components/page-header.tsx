import * as React from "react";
import { cn } from "../lib/cn";

export interface PageHeaderProps extends Omit<React.HTMLAttributes<HTMLDivElement>, "title"> {
  title: React.ReactNode;
  description?: React.ReactNode;
  eyebrow?: React.ReactNode;
  actions?: React.ReactNode;
}

export const PageHeader = React.forwardRef<HTMLDivElement, PageHeaderProps>(
  ({ className, title, description, eyebrow, actions, children, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col gap-4", className)} {...props}>
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="flex flex-col gap-1">
          {eyebrow ? (
            <span className="text-eyebrow font-semibold uppercase text-muted-foreground">
              {eyebrow}
            </span>
          ) : null}
          <h1 className="font-display text-h3 font-semibold tracking-[-0.02em] text-foreground">
            {title}
          </h1>
          {description ? (
            <p className="text-small text-muted-foreground">{description}</p>
          ) : null}
        </div>
        {actions ? <div className="flex shrink-0 items-center gap-2">{actions}</div> : null}
      </div>
      {children}
    </div>
  )
);
PageHeader.displayName = "PageHeader";
