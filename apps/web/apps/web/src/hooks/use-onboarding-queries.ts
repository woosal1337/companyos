"use client";

import { useQuery } from "@tanstack/react-query";
import { api, orgPath } from "@/lib/api";

export interface OnboardingStep {
  key: string;
  label: string;
  done: boolean;
}

export interface Onboarding {
  steps: OnboardingStep[];
  completed: number;
  total: number;
  complete: boolean;
}

export function useOnboarding(orgId: string) {
  return useQuery({
    queryKey: ["orgs", orgId, "onboarding"],
    queryFn: ({ signal }) => api.get<Onboarding>(orgPath(orgId, "/onboarding"), signal),
  });
}
