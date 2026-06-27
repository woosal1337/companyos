"use client";

import { useMutation } from "@tanstack/react-query";
import { api, orgPath } from "@/lib/api";

export interface PqlTask {
  id: string;
  identifier: string | null;
  title: string;
  status: string;
  priority: string;
  assignee_id: string | null;
  due_date: string | null;
  project_id: string;
}

export interface PqlResult {
  query: string;
  count: number;
  results: PqlTask[];
}

export interface PqlValidation {
  valid: boolean;
  error: string | null;
}

export function useExecutePql(orgId: string) {
  return useMutation({
    mutationFn: (query: string) =>
      api.post<PqlResult>(orgPath(orgId, "/pql/execute"), { query }),
  });
}

export function useValidatePql(orgId: string) {
  return useMutation({
    mutationFn: (query: string) =>
      api.post<PqlValidation>(orgPath(orgId, "/pql/validate"), { query }),
  });
}

export interface PqlFromText {
  prompt: string;
  query: string;
  count: number;
  results: PqlTask[];
}

export function useTextToPql(orgId: string) {
  return useMutation({
    mutationFn: (prompt: string) =>
      api.post<PqlFromText>(orgPath(orgId, "/pql/from-text"), { prompt }),
  });
}
