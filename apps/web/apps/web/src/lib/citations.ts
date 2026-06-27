import { formatTimestamp } from "./format";
import type { MeetingChatCitation } from "./types";

export function citationHref(orgId: string, citation: MeetingChatCitation): string {
  const base = `/app/${orgId}/meetings/${citation.meeting_id}`;
  if (citation.start_seconds != null && citation.start_seconds >= 0) {
    return `${base}?t=${Math.floor(citation.start_seconds)}`;
  }
  return base;
}

export function citationLabel(citation: MeetingChatCitation): string {
  const title = citation.meeting_title?.trim() || "Meeting";
  if (citation.start_seconds != null && citation.start_seconds >= 0) {
    return `${title} · ${formatTimestamp(citation.start_seconds)}`;
  }
  return title;
}
