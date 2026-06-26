"use client";

import * as React from "react";
import { Menu, X } from "lucide-react";
import { cn } from "../lib/cn";
import { Button } from "./button";
import { Container } from "./container";
import { Logo } from "./logo";

export interface NavLink {
  label: string;
  href: string;
}

const defaultLinks: NavLink[] = [
  { label: "Product", href: "/product" },
  { label: "Resources", href: "/resources" },
  { label: "Customers", href: "/customers" },
  { label: "Pricing", href: "/pricing" },
  { label: "Now", href: "/now" },
  { label: "Contact", href: "/contact" },
];

export interface MarketingNavProps extends React.HTMLAttributes<HTMLElement> {
  brand?: React.ReactNode;
  links?: NavLink[];
  renderLink?: (link: NavLink) => React.ReactNode;
  loginHref?: string;
  loginLabel?: string;
  signupHref?: string;
  signupLabel?: string;
  actions?: React.ReactNode;
  sticky?: boolean;
}

const desktopLinkClass =
  "text-small text-muted-foreground transition-colors duration-150 hover:text-foreground";
const mobileLinkClass =
  "text-body text-muted-foreground transition-colors duration-150 hover:text-foreground";

export const MarketingNav = React.forwardRef<HTMLElement, MarketingNavProps>(
  (
    {
      className,
      brand,
      links = defaultLinks,
      renderLink,
      loginHref = "/login",
      loginLabel = "Log in",
      signupHref = "/signup",
      signupLabel = "Sign up",
      actions,
      sticky = true,
      ...props
    },
    ref
  ) => {
    const [open, setOpen] = React.useState(false);

    const link = (item: NavLink, linkClass: string) => (
      <span key={item.href} className={linkClass}>
        {renderLink ? renderLink(item) : <a href={item.href}>{item.label}</a>}
      </span>
    );

    const signupButton = (variantClassName: string) => (
      <Button size="sm" variant="primary" className={cn("rounded-full", variantClassName)} asChild>
        {renderLink ? (
          renderLink({ label: signupLabel, href: signupHref })
        ) : (
          <a href={signupHref}>{signupLabel}</a>
        )}
      </Button>
    );

    return (
      <header
        ref={ref}
        className={cn(
          "z-50 w-full border-b border-border bg-canvas",
          sticky &&
            "sticky top-0 supports-[backdrop-filter]:bg-canvas/70 supports-[backdrop-filter]:backdrop-blur-xl",
          className
        )}
        {...props}
      >
        <Container className="flex h-14 items-center justify-between gap-8">
          <div className="flex shrink-0 items-center">{brand ?? <Logo size="sm" />}</div>

          <nav className="hidden items-center gap-7 lg:flex">
            {links.map((item) => link(item, desktopLinkClass))}
          </nav>

          <div className="flex shrink-0 items-center gap-4">
            {actions}
            <span className={cn("hidden lg:inline-flex", desktopLinkClass)}>
              {renderLink ? (
                renderLink({ label: loginLabel, href: loginHref })
              ) : (
                <a href={loginHref}>{loginLabel}</a>
              )}
            </span>
            {signupButton("hidden lg:inline-flex")}
            <button
              type="button"
              aria-label={open ? "Close menu" : "Open menu"}
              aria-expanded={open}
              onClick={() => setOpen((prev) => !prev)}
              className="inline-flex size-8 items-center justify-center rounded-md text-muted-foreground transition-colors duration-150 hover:text-foreground lg:hidden [&_svg]:size-5"
            >
              {open ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
            </button>
          </div>
        </Container>

        {open ? (
          <div className="border-t border-border bg-canvas lg:hidden">
            <Container className="flex flex-col gap-1 py-4">
              {links.map((item) => (
                <span key={item.href} className="py-1.5">
                  {link(item, mobileLinkClass)}
                </span>
              ))}
              <div className="mt-3 flex flex-col gap-4 border-t border-border pt-4">
                <span className={mobileLinkClass}>
                  {renderLink ? (
                    renderLink({ label: loginLabel, href: loginHref })
                  ) : (
                    <a href={loginHref}>{loginLabel}</a>
                  )}
                </span>
                {signupButton("w-full")}
              </div>
            </Container>
          </div>
        ) : null}
      </header>
    );
  }
);
MarketingNav.displayName = "MarketingNav";

export interface AnnouncementBarProps extends React.HTMLAttributes<HTMLDivElement> {
  href?: string;
}

export const AnnouncementBar = React.forwardRef<HTMLDivElement, AnnouncementBarProps>(
  ({ className, href, children, ...props }, ref) => {
    const inner = (
      <div
        ref={ref}
        className={cn(
          "flex w-full items-center justify-center gap-2 bg-foreground px-4 py-2 text-center text-caption font-medium text-background",
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
    return href ? (
      <a href={href} className="block transition-opacity duration-150 hover:opacity-90">
        {inner}
      </a>
    ) : (
      inner
    );
  }
);
AnnouncementBar.displayName = "AnnouncementBar";
