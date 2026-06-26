import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../lib/cn";
import { Container } from "./container";

const ctaBandVariants = cva("overflow-hidden rounded-2xl border px-8 py-14 text-center sm:px-14", {
  variants: {
    tone: {
      dark: "border-transparent bg-foreground text-background",
      light: "border-border bg-surface text-foreground shadow-sm",
    },
  },
  defaultVariants: {
    tone: "dark",
  },
});

export interface CTABandProps
  extends Omit<React.HTMLAttributes<HTMLDivElement>, "title">,
    VariantProps<typeof ctaBandVariants> {
  title: React.ReactNode;
  description?: React.ReactNode;
  actions?: React.ReactNode;
  contained?: boolean;
}

export const CTABand = React.forwardRef<HTMLDivElement, CTABandProps>(
  ({ className, tone, title, description, actions, contained = true, ...props }, ref) => {
    const band = (
      <div ref={ref} className={cn(ctaBandVariants({ tone }), className)} {...props}>
        <div className="mx-auto flex max-w-2xl flex-col items-center gap-4">
          <h2 className="text-balance text-h1">{title}</h2>
          {description ? (
            <p
              className={cn(
                "text-pretty text-body",
                tone === "light" ? "text-muted-foreground" : "text-background/70"
              )}
            >
              {description}
            </p>
          ) : null}
          {actions ? <div className="mt-2 flex flex-wrap items-center justify-center gap-3">{actions}</div> : null}
        </div>
      </div>
    );
    return contained ? <Container>{band}</Container> : band;
  }
);
CTABand.displayName = "CTABand";
