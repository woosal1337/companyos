import type { ContextSignal } from "./types";

export const SIGNAL_LABEL: Record<ContextSignal["kind"], string> = {
  related_task: "Related task",
  related_meeting: "Related meeting",
  related_note: "Related note",
};

export function signalHref(orgId: string, signal: ContextSignal): string | null {
  switch (signal.kind) {
    case "related_meeting":
      return `/app/${orgId}/meetings/${signal.id}`;
    case "related_note":
      return `/app/${orgId}/notes/${signal.id}`;
    default:
      return null;
  }
}

export function groupSignals(
  signals: ContextSignal[]
): { kind: ContextSignal["kind"]; items: ContextSignal[] }[] {
  const order: ContextSignal["kind"][] = ["related_task", "related_meeting", "related_note"];
  return order
    .map((kind) => ({ kind, items: signals.filter((signal) => signal.kind === kind) }))
    .filter((group) => group.items.length > 0);
}
