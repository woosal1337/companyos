"use client";

import { useQuery } from "@tanstack/react-query";
import { api, orgPath } from "@/lib/api";

interface TriageCount {
  total: number;
  by_project: Record<string, number>;
}

export function useTriageCount(orgId: string) {
  return useQuery({
    queryKey: ["orgs", orgId, "triage-count"] as const,
    queryFn: ({ signal }) => api.get<TriageCount>(orgPath(orgId, "/triage/count"), signal),
    refetchInterval: 60_000,
  });
}
