"use client";

import Link from "next/link";
import { ChevronRight } from "lucide-react";

export interface Crumb {
  label: string;
  href?: string;
}

export function Breadcrumbs({ items }: { items: Crumb[] }) {
  return (
    <nav
      aria-label="Breadcrumb"
      className="flex min-w-0 items-center gap-1 text-caption text-muted-foreground"
    >
      {items.map((item, index) => {
        const isLast = index === items.length - 1;
        return (
          <span key={`${item.label}-${index}`} className="flex min-w-0 items-center gap-1">
            {index > 0 ? (
              <ChevronRight aria-hidden="true" className="size-3.5 shrink-0 text-muted-foreground/50" />
            ) : null}
            {item.href && !isLast ? (
              <Link
                href={item.href}
                className="max-w-[16rem] truncate transition-colors duration-150 hover:text-foreground"
              >
                {item.label}
              </Link>
            ) : (
              <span
                className="max-w-[16rem] truncate text-foreground"
                aria-current={isLast ? "page" : undefined}
              >
                {item.label}
              </span>
            )}
          </span>
        );
      })}
    </nav>
  );
}
