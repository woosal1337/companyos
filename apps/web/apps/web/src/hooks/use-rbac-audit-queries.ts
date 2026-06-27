"use client";

import { useQuery } from "@tanstack/react-query";
import type { Page, RbacAuditEntry } from "@/lib/types";
import { api, orgPath } from "@/lib/api";

export interface RbacAuditFilters {
  subject_user_id?: string;
  resource_scope?: string;
  action?: string;
  start_date?: string;
  end_date?: string;
}

function buildQuery(filters: RbacAuditFilters, extra: Record<string, string> = {}): string {
  const params = new URLSearchParams(extra);
  for (const [key, value] of Object.entries(filters)) {
    if (value) params.set(key, value);
  }
  const query = params.toString();
  return query ? `?${query}` : "";
}

export function useRbacAuditLog(orgId: string, filters: RbacAuditFilters) {
  return useQuery({
    queryKey: ["orgs", orgId, "rbac-audit", filters] as const,
    queryFn: ({ signal }) =>
      api.get<Page<RbacAuditEntry>>(
        orgPath(orgId, `/rbac-audit${buildQuery(filters, { limit: "100" })}`),
        signal
      ),
  });
}

export async function downloadRbacAuditCsv(
  orgId: string,
  filters: RbacAuditFilters
): Promise<void> {
  const response = await fetch(orgPath(orgId, `/rbac-audit/export.csv${buildQuery(filters)}`), {
    credentials: "include",
  });
  if (!response.ok) throw new Error("Export failed");
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "rbac-audit.csv";
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}
