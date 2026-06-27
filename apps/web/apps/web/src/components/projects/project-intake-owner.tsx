"use client";

import type { Project } from "@/lib/types";
import { useOrgMembers } from "@/hooks/use-org-queries";
import { useProjectMembers, useUpdateProject } from "@/hooks/use-project-queries";
import { AssigneeSelect } from "@/components/tasks/task-bits";

export function ProjectIntakeOwner({
  orgId,
  project,
  canManage,
}: {
  orgId: string;
  project: Project;
  canManage: boolean;
}) {
  const updateProject = useUpdateProject(orgId, project.id);
  const orgMembers = useOrgMembers(orgId);
  const projectMembers = useProjectMembers(orgId, project.id);

  const memberIds = new Set((projectMembers.data ?? []).map((member) => member.user_id));
  const members = (orgMembers.data ?? []).filter((member) => memberIds.has(member.user_id));

  if (!canManage) return null;

  return (
    <section className="flex flex-col gap-3 rounded-lg border border-border bg-surface p-4">
      <div className="flex flex-col gap-1">
        <h2 className="text-small font-semibold text-foreground">Intake owner</h2>
        <p className="text-caption text-muted-foreground">
          Incoming triage items are auto-assigned to this person, who is notified on each new
          intake.
        </p>
      </div>
      <AssigneeSelect
        value={project.intake_owner_id}
        members={members}
        onChange={(userId) =>
          updateProject.mutate(
            userId ? { intake_owner_id: userId } : { clear_intake_owner: true }
          )
        }
      />
    </section>
  );
}
