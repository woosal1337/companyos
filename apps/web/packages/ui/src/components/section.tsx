"use client";

import * as React from "react";
import { cn } from "../lib/cn";
import { useReveal } from "../lib/use-reveal";

export interface SectionProps extends React.HTMLAttributes<HTMLElement> {
  spacing?: "none" | "sm" | "md" | "lg" | "xl";
  reveal?: boolean;
  as?: "section" | "div";
}

const spacingClasses = {
  none: "",
  sm: "py-12",
  md: "py-16 sm:py-20",
  lg: "py-24 sm:py-28",
  xl: "py-28 sm:py-32",
} as const;

export const Section = React.forwardRef<HTMLElement, SectionProps>(
  ({ className, spacing = "lg", reveal = false, as = "section", children, ...props }, ref) => {
    const { ref: revealRef, revealed } = useReveal<HTMLElement>();
    const Comp = as;
    const setRefs = React.useCallback(
      (node: HTMLElement | null) => {
        if (reveal) revealRef.current = node;
        if (typeof ref === "function") ref(node);
        else if (ref) (ref as React.MutableRefObject<HTMLElement | null>).current = node;
      },
      [reveal, ref, revealRef]
    );

    return (
      <Comp
        ref={setRefs}
        className={cn(spacingClasses[spacing], reveal && "reveal", className)}
        data-revealed={reveal ? revealed : undefined}
        {...props}
      >
        {children}
      </Comp>
    );
  }
);
Section.displayName = "Section";
