"use client";

import { useParams } from "next/navigation";
import { PageHeader } from "@/components/page-header";
import { MyTasks } from "@/components/tasks/my-tasks";

export default function MyTasksPage() {
  const { orgId } = useParams<{ orgId: string }>();

  return (
    <div className="mx-auto flex max-w-4xl flex-col gap-8 px-6 py-8">
      <PageHeader
        eyebrow="Personal"
        title="Your Work"
        description="Tasks assigned to and created by you across your projects, with a workload summary."
      />
      <MyTasks orgId={orgId} />
    </div>
  );
}
