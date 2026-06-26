"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { shareApiPath } from "@/lib/share";
import type { PublicMeetingChatResult, PublicMeetingShare } from "@/lib/types";

export function usePublicMeetingShare(token: string) {
  return useQuery({
    queryKey: ["share", "meetings", token] as const,
    queryFn: ({ signal }) => api.get<PublicMeetingShare>(shareApiPath(token), signal),
    enabled: token.length > 0,
    retry: false,
  });
}

export function usePublicMeetingChat(token: string) {
  return useMutation({
    mutationFn: (messages: { role: "user" | "assistant"; content: string }[]) =>
      api.post<PublicMeetingChatResult>(shareApiPath(token, "/chat"), { messages }),
  });
}
