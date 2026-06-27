import type { Task } from "@/lib/types";
import { PRIORITY_SORT, statusCategory, type StatusCategory } from "@/lib/task-meta";
import { taskCardContext } from "./task-context";

export type FocusGroupId =
  | "urgent"
  | "blocking"
  | "started"
  | "unstarted"
  | "backlog"
  | "done";

export interface FocusGroup {
  id: FocusGroupId;
  label: string;
  category: StatusCategory | null;
  tasks: Task[];
}

export const FOCUS_GROUP_ORDER: readonly FocusGroupId[] = [
  "urgent",
  "blocking",
  "started",
  "unstarted",
  "backlog",
  "done",
];

const FOCUS_GROUP_LABELS: Record<FocusGroupId, string> = {
  urgent: "Urgent",
  blocking: "Blocking",
  started: "In progress",
  unstarted: "Up next",
  backlog: "Backlog",
  done: "Done",
};

interface TaskBlocking {
  is_blocking?: boolean | null;
  blocking_count?: number | null;
}

function isBlocking(task: Task): boolean {
  const data = task as Task & TaskBlocking;
  if (data.is_blocking === true) return true;
  return typeof data.blocking_count === "number" && data.blocking_count > 0;
}

const PRIORITY_RANK = new Map<string, number>(
  PRIORITY_SORT.map((priority, index) => [priority, index])
);

function focusGroupOf(task: Task): FocusGroupId {
  const category = statusCategory(task.status);
  if (category === "completed" || category === "cancelled") return "done";
  if (task.priority === "urgent") return "urgent";
  if (isBlocking(task)) return "blocking";
  if (category === "started") return "started";
  if (category === "unstarted") return "unstarted";
  return "backlog";
}

function startedFirst(task: Task): number {
  return statusCategory(task.status) === "started" ? 0 : 1;
}

function compareWithinGroup(a: Task, b: Task): number {
  const startDelta = startedFirst(a) - startedFirst(b);
  if (startDelta !== 0) return startDelta;
  const priorityDelta =
    (PRIORITY_RANK.get(a.priority) ?? PRIORITY_SORT.length) -
    (PRIORITY_RANK.get(b.priority) ?? PRIORITY_SORT.length);
  if (priorityDelta !== 0) return priorityDelta;
  return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime();
}

export function groupTasksByFocus(tasks: readonly Task[]): FocusGroup[] {
  const buckets = new Map<FocusGroupId, Task[]>(
    FOCUS_GROUP_ORDER.map((id) => [id, [] as Task[]])
  );
  for (const task of tasks) {
    buckets.get(focusGroupOf(task))?.push(task);
  }
  const groups: FocusGroup[] = [];
  for (const id of FOCUS_GROUP_ORDER) {
    const bucket = buckets.get(id) ?? [];
    if (bucket.length === 0) continue;
    bucket.sort(compareWithinGroup);
    groups.push({
      id,
      label: FOCUS_GROUP_LABELS[id],
      category: null,
      tasks: bucket,
    });
  }
  return groups;
}

export function taskContextLine(task: Task, assigneeName: string | null): string | null {
  return taskCardContext(task, assigneeName);
}
