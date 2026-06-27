"use client";

import { useMemo } from "react";
import {
  ArchiveX,
  CheckSquare,
  Circle,
  LayoutGrid,
  ListChecks,
  SignalHigh,
  UserCheck,
  UserPlus,
} from "lucide-react";
import { useRegisterCommands, type RegisteredCommand } from "./command-registry";
import { useUpdateTask } from "@/hooks/use-task-queries";
import { useMe } from "@/hooks/use-auth-queries";
import { useOrgMembers } from "@/hooks/use-org-queries";
import {
  PRIORITY_LABELS,
  PRIORITY_SORT,
  STATUS_LABELS,
  STATUS_ORDER,
} from "@/lib/task-meta";
import type { Task } from "@/lib/types";

export function useTaskDetailCommands(orgId: string, projectId: string, task: Task): void {
  const updateTask = useUpdateTask(orgId, projectId);
  const me = useMe();
  const members = useOrgMembers(orgId);
  const mutate = updateTask.mutate;
  const myUserId = me.data?.id ?? null;
  const isMine = myUserId !== null && task.assignee_id === myUserId;
  const memberList = members.data;

  const commands = useMemo<RegisteredCommand[]>(() => {
    const list: RegisteredCommand[] = [];

    for (const status of STATUS_ORDER) {
      if (status === task.status) continue;
      list.push({
        id: `task-${task.id}-status-${status}`,
        label: `Change status to ${STATUS_LABELS[status]}`,
        keywords: ["status", "state", STATUS_LABELS[status]],
        icon: Circle,
        perform: () => mutate({ taskId: task.id, status }),
      });
    }

    for (const priority of PRIORITY_SORT) {
      if (priority === task.priority) continue;
      list.push({
        id: `task-${task.id}-priority-${priority}`,
        label: `Change priority to ${PRIORITY_LABELS[priority]}`,
        keywords: ["priority", PRIORITY_LABELS[priority]],
        icon: SignalHigh,
        perform: () => mutate({ taskId: task.id, priority }),
      });
    }

    if (myUserId !== null && !isMine) {
      list.push({
        id: `task-${task.id}-assign-me`,
        label: "Assign to me",
        keywords: ["assign", "assignee", "me", "owner"],
        icon: UserCheck,
        perform: () => mutate({ taskId: task.id, assignee_id: myUserId }),
      });
    }

    for (const member of memberList ?? []) {
      if (member.user_id === task.assignee_id || member.user_id === myUserId) continue;
      list.push({
        id: `task-${task.id}-assign-${member.user_id}`,
        label: `Assign to ${member.full_name}`,
        keywords: ["assign", "assignee", "owner", member.email],
        icon: UserPlus,
        perform: () => mutate({ taskId: task.id, assignee_id: member.user_id }),
      });
    }

    if (task.assignee_id !== null) {
      list.push({
        id: `task-${task.id}-unassign`,
        label: "Unassign",
        keywords: ["assign", "assignee", "clear", "remove"],
        icon: UserCheck,
        perform: () => mutate({ taskId: task.id, assignee_id: null }),
      });
    }

    if (task.status !== "cancelled") {
      list.push({
        id: `task-${task.id}-archive`,
        label: "Archive task",
        keywords: ["archive", "cancel", "close", "snooze"],
        icon: ArchiveX,
        perform: () => mutate({ taskId: task.id, status: "cancelled" }),
      });
    }

    return list;
  }, [task.id, task.status, task.priority, task.assignee_id, myUserId, isMine, memberList, mutate]);

  useRegisterCommands(
    { heading: `Actions on ${task.identifier}`, active: true },
    commands
  );
}

export function useProjectPageCommands(
  orgId: string,
  projectId: string,
  projectName: string,
  go: (segment: string) => void
): void {
  const commands = useMemo<RegisteredCommand[]>(
    () => [
      {
        id: `project-${projectId}-new-task`,
        label: "New task here",
        keywords: ["create", "add", "task", "issue", projectName],
        icon: CheckSquare,
        perform: () => go(`/projects/${projectId}`),
      },
      {
        id: `project-${projectId}-open-board`,
        label: "Open board",
        keywords: ["board", "kanban", projectName],
        icon: LayoutGrid,
        perform: () => go(`/projects/${projectId}`),
      },
      {
        id: `project-${projectId}-open-tasks`,
        label: "Open tasks",
        keywords: ["tasks", "table", "list", projectName],
        icon: ListChecks,
        perform: () => go(`/projects/${projectId}`),
      },
    ],
    [projectId, projectName, go]
  );

  useRegisterCommands(
    { heading: `Actions on ${projectName || "this project"}`, active: true },
    commands
  );
}
