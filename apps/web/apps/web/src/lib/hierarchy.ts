export type HierarchyLevel = "label" | "meta" | "headline" | "supporting";

export const hierarchy: Record<HierarchyLevel, string> = {
  label: "text-caption font-medium uppercase tracking-wide text-muted-foreground",
  meta: "tabular font-mono text-caption text-muted-foreground",
  headline: "text-small font-semibold text-foreground",
  supporting: "line-clamp-1 text-caption font-normal text-muted-foreground",
};

export function hierarchyClass(level: HierarchyLevel): string {
  return hierarchy[level];
}
