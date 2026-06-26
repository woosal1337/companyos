"use client";

import { useQuery } from "@tanstack/react-query";
import type { AuditEntry, Page } from "@/lib/types";
import { api, orgPath } from "@/lib/api";

export interface AuditFilters {
  entity_type?: string;
  event_type?: string;
  start_date?: string;
  end_date?: string;
}

function buildQuery(filters: AuditFilters, extra: Record<string, string> = {}): string {
  const params = new URLSearchParams(extra);
  for (const [key, value] of Object.entries(filters)) {
    if (value) params.set(key, value);
  }
  const query = params.toString();
  return query ? `?${query}` : "";
}

export function useAuditLog(orgId: string, filters: AuditFilters) {
  return useQuery({
    queryKey: ["orgs", orgId, "audit", filters] as const,
    queryFn: ({ signal }) =>
      api.get<Page<AuditEntry>>(
        orgPath(orgId, `/audit${buildQuery(filters, { limit: "100" })}`),
        signal
      ),
  });
}

export async function downloadAuditCsv(orgId: string, filters: AuditFilters): Promise<void> {
  const response = await fetch(orgPath(orgId, `/audit/export.csv${buildQuery(filters)}`), {
    credentials: "include",
  });
  if (!response.ok) throw new Error("Export failed");
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "audit-log.csv";
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}
