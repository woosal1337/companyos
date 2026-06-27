import type { MeetingBriefBullet } from "./types";

export function isFutureEvent(startsAt: string, now: number = Date.now()): boolean {
  const start = new Date(startsAt).getTime();
  return Number.isFinite(start) && start > now;
}

export function briefSourceHref(orgId: string, bullet: MeetingBriefBullet): string | null {
  switch (bullet.source_kind) {
    case "meeting":
      return `/app/${orgId}/meetings/${bullet.source_id}`;
    case "note":
      return `/app/${orgId}/notes/${bullet.source_id}`;
    case "project":
      return `/app/${orgId}/projects/${bullet.source_id}`;
    default:
      return null;
  }
}
