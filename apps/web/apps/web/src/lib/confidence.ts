export type ConfidenceBand = "high" | "medium" | "low";

export const CONFIDENCE_THRESHOLDS = {
  high: 0.75,
  medium: 0.45,
} as const;

export function confidenceBand(score: number): ConfidenceBand {
  if (!Number.isFinite(score)) return "low";
  const clamped = Math.min(1, Math.max(0, score));
  if (clamped >= CONFIDENCE_THRESHOLDS.high) return "high";
  if (clamped >= CONFIDENCE_THRESHOLDS.medium) return "medium";
  return "low";
}

export const CONFIDENCE_LABELS: Record<ConfidenceBand, string> = {
  high: "High confidence",
  medium: "Some evidence",
  low: "Low confidence",
};

export function isActionable(band: ConfidenceBand): boolean {
  return band !== "low";
}

export interface Coverage {
  consulted: number;
  total: number;
}

export function coverageRatio({ consulted, total }: Coverage): number {
  if (total <= 0) return 0;
  return Math.min(1, Math.max(0, consulted / total));
}

export function coverageLabel(coverage: Coverage): string {
  const { consulted, total } = coverage;
  if (total <= 0) return "No sources consulted";
  return `Based on ${consulted} of ${total} source${total === 1 ? "" : "s"}`;
}

export function coverageBand(coverage: Coverage): ConfidenceBand {
  return confidenceBand(coverageRatio(coverage));
}
