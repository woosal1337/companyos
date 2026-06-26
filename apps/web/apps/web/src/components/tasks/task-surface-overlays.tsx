"use client";

import type { OrgMember } from "@/lib/types";
import { clearAll } from "./use-task-selection";
import { BulkActionBar } from "./bulk-action-bar";
import { TaskPeek } from "./task-peek";
import { AssigneePicker, PriorityPicker, StatusPicker } from "./task-property-picker";
import type { TaskSurface } from "./use-task-surface";

export function TaskSurfaceOverlays({
  orgId,
  projectId,
  members,
  surface,
}: {
  orgId: string;
  projectId: string;
  members: OrgMember[];
  surface: TaskSurface;
}) {
  const { selection, picker, peekTaskId, pickerTask } = surface;
  const pickerCount = picker?.taskIds.length ?? 0;

  return (
    <>
      <BulkActionBar
        orgId={orgId}
        projectId={projectId}
        selectedIds={selection.selectedIds}
        members={members}
        onClear={() => clearAll()}
      />

      <TaskPeek orgId={orgId} taskId={peekTaskId} onClose={() => surface.setPeekTaskId(null)} />

      <StatusPicker
        kind="status"
        open={picker?.kind === "status"}
        count={pickerCount}
        current={pickerTask?.status ?? null}
        onSelect={surface.applyStatus}
        onClose={surface.closePicker}
      />
      <PriorityPicker
        kind="priority"
        open={picker?.kind === "priority"}
        count={pickerCount}
        current={pickerTask?.priority ?? null}
        onSelect={surface.applyPriority}
        onClose={surface.closePicker}
      />
      <AssigneePicker
        kind="assignee"
        open={picker?.kind === "assignee"}
        count={pickerCount}
        current={pickerTask?.assignee_id ?? null}
        members={members}
        onSelect={surface.applyAssignee}
        onClose={surface.closePicker}
      />
    </>
  );
}
