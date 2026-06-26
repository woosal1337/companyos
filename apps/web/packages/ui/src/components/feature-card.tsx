import * as React from "react";
import { cn } from "../lib/cn";

export interface FeatureCardProps extends Omit<React.HTMLAttributes<HTMLDivElement>, "title"> {
  icon?: React.ReactNode;
  title: React.ReactNode;
  description?: React.ReactNode;
  accent?: boolean;
}

export const FeatureCard = React.forwardRef<HTMLDivElement, FeatureCardProps>(
  ({ className, icon, title, description, accent = false, children, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "group flex flex-col gap-4 rounded-lg border border-border bg-surface p-6 shadow-xs transition-shadow duration-150 hover:shadow-sm",
        className
      )}
      {...props}
    >
      {icon ? (
        <div
          className={cn(
            "flex size-10 items-center justify-center rounded-lg border shadow-xs [&_svg]:size-5",
            accent
              ? "border-accent-subtle bg-accent-muted text-accent"
              : "border-border bg-muted text-foreground"
          )}
        >
          {icon}
        </div>
      ) : null}
      <div className="flex flex-col gap-1.5">
        <h3 className="text-h4 text-foreground">{title}</h3>
        {description ? (
          <p className="text-small leading-relaxed text-muted-foreground">{description}</p>
        ) : null}
        {children}
      </div>
    </div>
  )
);
FeatureCard.displayName = "FeatureCard";
