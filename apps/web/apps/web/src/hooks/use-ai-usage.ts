"use client";

import { useQuery } from "@tanstack/react-query";
import { api, orgPath } from "@/lib/api";

export interface AIUsage {
  used: number;
  limit: number;
  remaining: number;
  billable_seats: number;
  credits_per_seat: number;
  period_start: string;
  percent_used: number;
}

export function useAIUsage(orgId: string) {
  return useQuery({
    queryKey: ["orgs", orgId, "ai", "usage"],
    queryFn: ({ signal }) => api.get<AIUsage>(orgPath(orgId, "/ai/usage"), signal),
  });
}
