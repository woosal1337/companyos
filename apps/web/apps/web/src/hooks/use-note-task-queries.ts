"use client";

import { useQuery } from "@tanstack/react-query";
import type { Task } from "@/lib/types";
import { api, orgPath } from "@/lib/api";

export function useNoteTasks(orgId: string, noteId: string, enabled = true) {
  return useQuery({
    queryKey: ["orgs", orgId, "notes", noteId, "tasks"] as const,
    enabled,
    queryFn: ({ signal }) => api.get<Task[]>(orgPath(orgId, `/notes/${noteId}/tasks`), signal),
  });
}
