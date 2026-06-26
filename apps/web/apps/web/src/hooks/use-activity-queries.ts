"use client";

import { useQuery } from "@tanstack/react-query";
import { api, orgPath } from "@/lib/api";
import type { ActivityEvent, Page } from "@/lib/types";

export const activityKeys = {
  all: (orgId: string) => ["orgs", orgId, "activity"] as const,
  list: (orgId: string) => [...activityKeys.all(orgId), "org"] as const,
};

export function useActivity(orgId: string) {
  return useQuery({
    queryKey: activityKeys.list(orgId),
    queryFn: async ({ signal }) => {
      const page = await api.get<Page<ActivityEvent>>(orgPath(orgId, "/activity"), signal);
      return page.items;
    },
  });
}
