export type DocBlockType =
  | "h2"
  | "h3"
  | "p"
  | "ul"
  | "ol"
  | "steps"
  | "code"
  | "callout"
  | "table";

export interface DocStep {
  title: string;
  text: string;
}

export interface DocBlock {
  type: DocBlockType;
  text?: string;
  items?: string[];
  steps?: DocStep[];
  code?: string;
  lang?: string;
  variant?: "info" | "tip" | "warning";
  title?: string;
  headers?: string[];
  rows?: string[][];
}

export interface DocPage {
  title: string;
  slug: string;
  description: string;
  blocks: DocBlock[];
}
