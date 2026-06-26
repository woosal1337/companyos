import * as React from "react";
import { cn } from "../lib/cn";
import { Container } from "./container";
import { Logo } from "./logo";
import type { NavLink } from "./marketing-nav";

export interface FooterColumn {
  heading: string;
  links: NavLink[];
}

export interface MarketingFooterProps extends React.HTMLAttributes<HTMLElement> {
  brand?: React.ReactNode;
  tagline?: React.ReactNode;
  columns?: FooterColumn[];
  renderLink?: (link: NavLink) => React.ReactNode;
  bottom?: React.ReactNode;
}

export const MarketingFooter = React.forwardRef<HTMLElement, MarketingFooterProps>(
  ({ className, brand, tagline, columns = [], renderLink, bottom, ...props }, ref) => (
    <footer ref={ref} className={cn("border-t border-border bg-background", className)} {...props}>
      <Container className="py-16">
        <div className="flex flex-col justify-between gap-12 lg:flex-row">
          <div className="flex max-w-xs flex-col gap-3">
            {brand ?? <Logo />}
            {tagline ? <p className="text-small text-muted-foreground">{tagline}</p> : null}
          </div>
          {columns.length > 0 ? (
            <div className="grid grid-cols-2 gap-10 sm:grid-cols-3 lg:gap-16">
              {columns.map((col) => (
                <div key={col.heading} className="flex flex-col gap-3">
                  <p className="text-eyebrow font-semibold uppercase text-muted-foreground">
                    {col.heading}
                  </p>
                  <ul className="flex flex-col gap-2.5">
                    {col.links.map((link) => (
                      <li key={link.href}>
                        {renderLink ? (
                          renderLink(link)
                        ) : (
                          <a
                            href={link.href}
                            className="text-small text-muted-foreground transition-colors duration-150 hover:text-foreground"
                          >
                            {link.label}
                          </a>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          ) : null}
        </div>
        {bottom ? (
          <div className="mt-12 flex flex-col items-start justify-between gap-3 border-t border-border pt-6 text-caption text-muted-foreground sm:flex-row sm:items-center">
            {bottom}
          </div>
        ) : null}
      </Container>
    </footer>
  )
);
MarketingFooter.displayName = "MarketingFooter";
