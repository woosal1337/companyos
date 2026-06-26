"use client";

import { useQuery } from "@tanstack/react-query";
import { api, orgPath } from "@/lib/api";

export interface DuplicateCandidate {
  task_id: string;
  title: string;
  status: string;
  score: number;
  shared_tokens: number;
}

export function useDuplicateCheck(orgId: string, projectId: string, title: string) {
  const trimmed = title.trim();
  return useQuery({
    queryKey: ["orgs", orgId, "projects", projectId, "dup-check", trimmed] as const,
    enabled: trimmed.length >= 6,
    staleTime: 30_000,
    queryFn: ({ signal }) =>
      api.get<DuplicateCandidate[]>(
        orgPath(orgId, `/projects/${projectId}/tasks/duplicate-check?title=${encodeURIComponent(trimmed)}`),
        signal
      ),
  });
}
