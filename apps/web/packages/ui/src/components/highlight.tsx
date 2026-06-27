import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../lib/cn";

const highlightVariants = cva("relative inline-block whitespace-nowrap", {
  variants: {
    variant: {
      marker: "box-decoration-clone rounded-[0.2em] bg-accent-muted px-[0.12em] text-accent",
      underline:
        "underline decoration-accent decoration-[0.12em] underline-offset-[0.18em]",
      text: "text-accent",
    },
  },
  defaultVariants: {
    variant: "marker",
  },
});

export interface HighlightProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof highlightVariants> {}

export const Highlight = React.forwardRef<HTMLSpanElement, HighlightProps>(
  ({ className, variant, ...props }, ref) => (
    <span ref={ref} className={cn(highlightVariants({ variant }), className)} {...props} />
  )
);
Highlight.displayName = "Highlight";
