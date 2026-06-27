"use client";

import { useQuery } from "@tanstack/react-query";
import { api, orgPath } from "@/lib/api";

export interface MarketplaceItem {
  id: string;
  category: string;
  name: string;
  description: string;
  install_kind: string;
}

export interface InstalledSummary {
  connectors: number;
  agents: number;
  categories: Record<string, number>;
}

export function useMarketplaceCatalog(orgId: string) {
  return useQuery({
    queryKey: ["orgs", orgId, "marketplace", "catalog"],
    queryFn: ({ signal }) =>
      api.get<MarketplaceItem[]>(orgPath(orgId, "/marketplace/catalog"), signal),
    staleTime: 300_000,
  });
}

export function useMarketplaceInstalled(orgId: string) {
  return useQuery({
    queryKey: ["orgs", orgId, "marketplace", "installed"],
    queryFn: ({ signal }) =>
      api.get<InstalledSummary>(orgPath(orgId, "/marketplace/installed"), signal),
  });
}
