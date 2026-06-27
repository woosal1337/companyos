"use client";

import Link from "next/link";
import { Logo, MarketingNav, type NavLink as NavLinkType } from "@companyos/ui";

const NAV_LINKS: NavLinkType[] = [
  { label: "Product", href: "#how-it-works" },
  { label: "Resources", href: "#resources" },
  { label: "Customers", href: "#customers" },
  { label: "Pricing", href: "#pricing" },
  { label: "Now", href: "#now" },
  { label: "Contact", href: "#contact" },
];

export function SiteNav() {
  return (
    <MarketingNav
      brand={
        <Link href="/" aria-label="CompanyOS home" className="flex items-center">
          <Logo />
        </Link>
      }
      links={NAV_LINKS}
      renderLink={(link) => <Link href={link.href}>{link.label}</Link>}
      loginHref="/login"
      signupHref="/signup"
    />
  );
}
