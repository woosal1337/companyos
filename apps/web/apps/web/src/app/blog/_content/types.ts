import type { DocBlock } from "@/app/docs/_content/types";

export interface BlogPost {
  /** URL slug, e.g. "introducing-companyos" -> /blog/introducing-companyos */
  slug: string;
  title: string;
  description: string;
  /** ISO date, yyyy-mm-dd */
  date: string;
  author: string;
  authorUrl?: string;
  tags?: string[];
  /** Article body, rendered with the shared docs Blocks renderer. */
  blocks: DocBlock[];
}
