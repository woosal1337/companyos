"use client";

import { useQuery } from "@tanstack/react-query";
import { api, orgPath } from "@/lib/api";

export interface TimelineTask {
  id: string;
  identifier: string | null;
  title: string;
  status: string;
  start_date: string | null;
  due_date: string | null;
  on_critical_path: boolean;
  is_violated: boolean;
  is_done: boolean;
}

export interface TimelineLink {
  predecessor_id: string;
  successor_id: string;
  dependency_type: string;
  violated: boolean;
}

export interface Timeline {
  tasks: TimelineTask[];
  links: TimelineLink[];
  critical_path: string[];
  violation_count: number;
}

export function useProjectTimeline(orgId: string, projectId: string) {
  return useQuery({
    queryKey: ["orgs", orgId, "projects", projectId, "timeline"],
    queryFn: ({ signal }) =>
      api.get<Timeline>(orgPath(orgId, `/projects/${projectId}/timeline`), signal),
  });
}
