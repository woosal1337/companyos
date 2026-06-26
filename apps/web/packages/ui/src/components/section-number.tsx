import * as React from "react";
import { ArrowRight } from "lucide-react";
import { cn } from "../lib/cn";

export interface SectionNumberProps {
  index: string;
  label: string;
  href?: string;
  className?: string;
}

export function SectionNumber({ index, label, href, className }: SectionNumberProps) {
  const content = (
    <span
      className={cn(
        "inline-flex items-center gap-2 font-mono text-mono-label uppercase text-muted-foreground",
        className
      )}
    >
      <span className="text-foreground/70">{index}</span>
      <span>{label}</span>
      {href ? <ArrowRight className="size-3" aria-hidden="true" /> : null}
    </span>
  );

  if (href) {
    return (
      <a href={href} className="group inline-flex transition-colors hover:text-foreground">
        {content}
      </a>
    );
  }
  return content;
}
