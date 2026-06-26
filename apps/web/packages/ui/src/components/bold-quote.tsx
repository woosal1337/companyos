import * as React from "react";
import { cn } from "../lib/cn";

export interface BoldQuoteProps extends React.HTMLAttributes<HTMLDivElement> {
  quote: string;
  name: string;
  role: string;
  tone?: "acid" | "lavender";
}

export const BoldQuote = React.forwardRef<HTMLDivElement, BoldQuoteProps>(
  ({ className, quote, name, role, tone = "acid", ...props }, ref) => (
    <figure
      ref={ref}
      className={cn(
        "flex min-h-80 flex-col justify-between gap-12 rounded-2xl p-10 sm:p-14",
        tone === "acid" ? "bg-bold text-bold-foreground" : "bg-lavender text-lavender-foreground",
        className
      )}
      {...props}
    >
      <blockquote className="font-display text-h2 tracking-tight">{quote}</blockquote>
      <figcaption className="flex flex-col gap-0.5">
        <span className="text-body font-medium">{name}</span>
        <span className="text-small opacity-70">{role}</span>
      </figcaption>
    </figure>
  )
);
BoldQuote.displayName = "BoldQuote";
