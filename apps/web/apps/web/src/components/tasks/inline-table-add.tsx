"use client";

import { useRef, useState } from "react";
import { Plus } from "lucide-react";
import { useCreateTask } from "@/hooks/use-task-queries";

export function InlineTableAdd({
  orgId,
  projectId,
  colSpan,
}: {
  orgId: string;
  projectId: string;
  colSpan: number;
}) {
  const createTask = useCreateTask(orgId, projectId);
  const [active, setActive] = useState(false);
  const [title, setTitle] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const submit = () => {
    const trimmed = title.trim();
    if (!trimmed || createTask.isPending) return;
    createTask.mutate(
      { title: trimmed, status: "backlog", priority: "none" },
      {
        onSuccess: () => {
          setTitle("");
          inputRef.current?.focus();
        },
      }
    );
  };

  return (
    <tr className="border-t border-border">
      <td colSpan={colSpan} className="px-4 py-1.5">
        {active ? (
          <input
            ref={inputRef}
            autoFocus
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                event.preventDefault();
                submit();
              } else if (event.key === "Escape") {
                setTitle("");
                setActive(false);
              }
            }}
            onBlur={() => {
              if (!title.trim() && !createTask.isPending) setActive(false);
            }}
            placeholder="New task title — Enter to add another, Esc to close"
            aria-label="New task title"
            disabled={createTask.isPending}
            className="w-full bg-transparent text-small text-foreground outline-none placeholder:text-muted-foreground"
          />
        ) : (
          <button
            type="button"
            onClick={() => setActive(true)}
            className="flex items-center gap-2 text-caption text-muted-foreground transition-colors hover:text-foreground"
          >
            <Plus className="size-3.5" aria-hidden="true" />
            Add task
          </button>
        )}
      </td>
    </tr>
  );
}
