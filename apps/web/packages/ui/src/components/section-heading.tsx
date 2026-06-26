import * as React from "react";
import { cn } from "../lib/cn";
import { Eyebrow } from "./pill";

export interface SectionHeadingProps extends Omit<React.HTMLAttributes<HTMLDivElement>, "title"> {
  eyebrow?: React.ReactNode;
  title: React.ReactNode;
  description?: React.ReactNode;
  align?: "left" | "center";
  large?: boolean;
}

export const SectionHeading = React.forwardRef<HTMLDivElement, SectionHeadingProps>(
  ({ className, eyebrow, title, description, align = "center", large = false, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "flex flex-col gap-3",
        align === "center" ? "mx-auto max-w-2xl items-center text-center" : "items-start text-left",
        className
      )}
      {...props}
    >
      {eyebrow ? <Eyebrow>{eyebrow}</Eyebrow> : null}
      <h2
        className={cn(
          "font-display text-balance text-foreground",
          large ? "text-h1" : "text-h2"
        )}
      >
        {title}
      </h2>
      {description ? (
        <p className="text-pretty text-body text-muted-foreground">{description}</p>
      ) : null}
    </div>
  )
);
SectionHeading.displayName = "SectionHeading";
