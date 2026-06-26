import type { ActivityEvent } from "@/lib/types";
import { classifyActivity, isHighSignal, type ActivityKind } from "./activity-taxonomy";

export const COLLAPSE_THRESHOLD = 3;

export interface SingleEntry {
  type: "single";
  id: string;
  event: ActivityEvent;
  kind: ActivityKind;
  signal: "high" | "low";
}

export interface AggregateEntry {
  type: "aggregate";
  id: string;
  kind: ActivityKind;
  events: ActivityEvent[];
  latest: ActivityEvent;
}

export type FeedEntry = SingleEntry | AggregateEntry;

export interface DayGroup {
  key: string;
  label: string;
  date: Date;
  entries: FeedEntry[];
  count: number;
}

const weekdayFormatter = new Intl.DateTimeFormat("en-US", { weekday: "long" });
const dateFormatter = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
});

function dayKey(date: Date): string {
  return `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
}

function dayLabel(date: Date, now: Date): string {
  const today = dayKey(now);
  const yesterday = new Date(now);
  yesterday.setDate(now.getDate() - 1);
  const key = dayKey(date);
  if (key === today) return "Today";
  if (key === dayKey(yesterday)) return "Yesterday";
  const ageDays = (now.getTime() - date.getTime()) / 86_400_000;
  if (ageDays < 7) return weekdayFormatter.format(date);
  return dateFormatter.format(date);
}

function collapseEntries(events: ActivityEvent[]): FeedEntry[] {
  const entries: FeedEntry[] = [];
  let run: ActivityEvent[] = [];
  let runKind: ActivityKind | null = null;

  const flush = () => {
    if (run.length === 0) return;
    if (run.length >= COLLAPSE_THRESHOLD && runKind) {
      entries.push({
        type: "aggregate",
        id: `agg-${run[0]!.id}-${run.length}`,
        kind: runKind,
        events: run,
        latest: run[0]!,
      });
    } else {
      for (const event of run) {
        entries.push({
          type: "single",
          id: event.id,
          event,
          kind: classifyActivity(event),
          signal: "low",
        });
      }
    }
    run = [];
    runKind = null;
  };

  for (const event of events) {
    if (isHighSignal(event)) {
      flush();
      entries.push({
        type: "single",
        id: event.id,
        event,
        kind: classifyActivity(event),
        signal: "high",
      });
      continue;
    }
    const kind = classifyActivity(event);
    if (runKind !== null && kind !== runKind) {
      flush();
    }
    runKind = kind;
    run.push(event);
  }
  flush();
  return entries;
}

export function groupActivity(events: ActivityEvent[], now: Date = new Date()): DayGroup[] {
  const sorted = [...events].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );

  const buckets = new Map<string, { date: Date; events: ActivityEvent[] }>();
  for (const event of sorted) {
    const date = new Date(event.created_at);
    const key = dayKey(date);
    const bucket = buckets.get(key);
    if (bucket) {
      bucket.events.push(event);
    } else {
      buckets.set(key, { date, events: [event] });
    }
  }

  const groups: DayGroup[] = [];
  for (const [key, bucket] of buckets) {
    groups.push({
      key,
      label: dayLabel(bucket.date, now),
      date: bucket.date,
      entries: collapseEntries(bucket.events),
      count: bucket.events.length,
    });
  }
  return groups;
}

export function countNewSince(events: ActivityEvent[], lastSeen: number | null): number {
  if (lastSeen === null) return 0;
  let count = 0;
  for (const event of events) {
    if (new Date(event.created_at).getTime() > lastSeen) count += 1;
  }
  return count;
}
