import { confidenceBand, isActionable, type ConfidenceBand } from "./confidence";
import type { RouteSuggestion } from "./types";

export type RoutingMode = "suggest" | "pick";

export interface ResolvedRouting {
  mode: RoutingMode;
  projectId: string | null;
  band: ConfidenceBand;
}

export function resolveRouting(
  suggestion: RouteSuggestion | null | undefined
): ResolvedRouting {
  if (!suggestion || !suggestion.project_id) {
    return { mode: "pick", projectId: null, band: "low" };
  }
  const band = confidenceBand(suggestion.confidence);
  return {
    mode: isActionable(band) ? "suggest" : "pick",
    projectId: suggestion.project_id,
    band,
  };
}
