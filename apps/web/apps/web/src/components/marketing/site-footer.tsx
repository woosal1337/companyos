import Link from "next/link";
import { cn, Container, Logo } from "@companyos/ui";

interface FooterLink {
  label: string;
  href: string;
}

interface FooterColumn {
  index: string;
  heading: string;
  links: FooterLink[];
}

const COLUMNS: FooterColumn[] = [
  {
    index: "01",
    heading: "Product",
    links: [
      { label: "Projects", href: "#projects" },
      { label: "Meetings", href: "#meetings" },
      { label: "Notes", href: "#notes" },
      { label: "Activity", href: "#activity" },
    ],
  },
  {
    index: "02",
    heading: "Features",
    links: [
      { label: "BYOK", href: "#byok" },
      { label: "Board", href: "#board" },
      { label: "Transcripts", href: "#transcripts" },
      { label: "Activity log", href: "#activity-log" },
    ],
  },
  {
    index: "03",
    heading: "Company",
    links: [
      { label: "About", href: "#about" },
      { label: "Careers", href: "#careers" },
      { label: "Blog", href: "#blog" },
      { label: "Contact", href: "#contact" },
    ],
  },
  {
    index: "04",
    heading: "Resources",
    links: [
      { label: "Docs", href: "#docs" },
      { label: "Changelog", href: "#changelog" },
      { label: "Status", href: "#status" },
    ],
  },
  {
    index: "05",
    heading: "Connect",
    links: [
      { label: "X (Twitter)", href: "https://x.com" },
      { label: "GitHub", href: "https://github.com" },
    ],
  },
];

const LEGAL: FooterLink[] = [
  { label: "Privacy", href: "#privacy" },
  { label: "Terms", href: "#terms" },
];

const linkClass =
  "inline-flex items-center gap-2 text-small text-muted-foreground transition-colors duration-150 hover:text-foreground";

const legalClass =
  "text-caption text-muted-foreground transition-colors duration-150 hover:text-foreground";

export function SiteFooter() {
  return (
    <footer className="border-t border-border bg-canvas">
      <Container className="py-20">
        <div className="flex flex-col gap-16 lg:flex-row lg:justify-between">
          <div className="flex max-w-xs flex-col gap-4">
            <Logo />
            <p className="text-small text-muted-foreground">
              The coordination layer for your whole company. Projects, meetings, and AI on your own
              key.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-x-12 gap-y-12 sm:grid-cols-3 lg:grid-cols-5 lg:gap-x-16">
            {COLUMNS.map((column) => (
              <div key={column.heading} className="flex flex-col gap-4">
                <p className="flex items-center gap-2 font-mono text-mono-label uppercase text-muted-foreground">
                  <span className="text-foreground/50">{column.index}</span>
                  <span>{column.heading}</span>
                </p>
                <ul className="flex flex-col gap-3">
                  {column.links.map((link) => (
                    <li key={link.href}>
                      <Link href={link.href} className={linkClass}>
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
        <div className="mt-20 flex flex-col items-start justify-between gap-4 border-t border-border pt-8 sm:flex-row sm:items-center">
          <div className="flex items-center gap-6">
            {LEGAL.map((link) => (
              <Link key={link.href} href={link.href} className={cn(legalClass)}>
                {link.label}
              </Link>
            ))}
          </div>
          <p className="text-caption text-muted-foreground">© 2026 CompanyOS</p>
        </div>
      </Container>
    </footer>
  );
}
