import { DOC_PAGES } from "./pages";
import type { DocPage } from "./types";

export interface DocsNavItem {
  slug: string;
  label: string;
}

export interface DocsNavGroup {
  heading: string;
  items: DocsNavItem[];
}

export const DOCS_NAV: DocsNavGroup[] = [
  {
    heading: "Getting started",
    items: [{ slug: "overview-getting-started", label: "Overview" }],
  },
  {
    heading: "Guides",
    items: [
      { slug: "organizations-teams-members", label: "Organizations & Members" },
      { slug: "projects-and-tasks", label: "Projects & Tasks" },
      { slug: "notes-activity-calendar-inbox", label: "Notes, Activity & Calendar" },
      { slug: "meetings", label: "Meetings" },
      { slug: "ai-brain-automations", label: "AI, Brain & Automations" },
    ],
  },
  {
    heading: "Reference",
    items: [
      { slug: "company-brain-mcp", label: "Company-Brain MCP" },
      { slug: "references-and-mentions", label: "References & Mentions" },
      { slug: "agent-project-setup", label: "Set up your agent" },
    ],
  },
];

const PAGE_BY_SLUG = new Map<string, DocPage>(DOC_PAGES.map((page) => [page.slug, page]));

export const ORDERED_SLUGS: string[] = DOCS_NAV.flatMap((group) =>
  group.items.map((item) => item.slug),
);

export const FIRST_SLUG: string = ORDERED_SLUGS[0] ?? "overview-getting-started";

export function getPage(slug?: string): DocPage | undefined {
  return PAGE_BY_SLUG.get(slug ?? FIRST_SLUG);
}

export function labelForSlug(slug: string): string {
  for (const group of DOCS_NAV) {
    const found = group.items.find((item) => item.slug === slug);
    if (found) return found.label;
  }
  return PAGE_BY_SLUG.get(slug)?.title ?? slug;
}

export function hrefForSlug(slug: string): string {
  return slug === FIRST_SLUG ? "/docs" : `/docs/${slug}`;
}

export function adjacentSlugs(slug: string): { prev?: string; next?: string } {
  const index = ORDERED_SLUGS.indexOf(slug);
  if (index === -1) return {};
  return {
    prev: index > 0 ? ORDERED_SLUGS[index - 1] : undefined,
    next: index < ORDERED_SLUGS.length - 1 ? ORDERED_SLUGS[index + 1] : undefined,
  };
}
