"use client";

import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";

const ENTITY_KEY: Record<string, string> = {
  task: "tasks",
  meeting: "meetings",
  note: "notes",
  event: "events",
  project: "projects",
  comment: "tasks",
  ai_user: "ai",
};

interface ActivityPayload {
  entity_type?: string;
}

export function useActivityStream(orgId: string): void {
  const queryClient = useQueryClient();

  useEffect(() => {
    if (!orgId) return;

    const source = new EventSource(`/api/v1/orgs/${orgId}/stream`);

    source.addEventListener("activity", (event) => {
      let payload: ActivityPayload;
      try {
        payload = JSON.parse((event as MessageEvent).data) as ActivityPayload;
      } catch {
        return;
      }
      void queryClient.invalidateQueries({ queryKey: ["orgs", orgId, "activity"] });
      const segment = payload.entity_type ? ENTITY_KEY[payload.entity_type] : undefined;
      if (segment) {
        void queryClient.invalidateQueries({ queryKey: ["orgs", orgId, segment] });
      }
    });

    return () => source.close();
  }, [orgId, queryClient]);
}
