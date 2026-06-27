import {
  CATEGORY_LABELS,
  CATEGORY_ORDER,
  STATUS_ORDER,
  STATUS_LABELS,
  STATUS_TO_CATEGORY,
  type StatusCategory,
} from "./task-meta";

export interface WorkflowStatus {
  id: string;
  name: string;
  category: StatusCategory;
  color: string;
  position: number;
  is_default: boolean;
  allow_new_items: boolean;
  team_id: string | null;
}

export interface WorkflowCategoryGroup {
  category: StatusCategory;
  label: string;
  statuses: WorkflowStatus[];
}

export const STATUS_COLORS: readonly string[] = [
  "muted-foreground",
  "accent",
  "warning",
  "success",
  "danger",
  "info",
  "teal",
];

export function defaultWorkflow(): WorkflowStatus[] {
  return STATUS_ORDER.map((status, index) => ({
    id: status,
    name: STATUS_LABELS[status],
    category: STATUS_TO_CATEGORY[status],
    color: status === "in_review" ? "accent" : "muted-foreground",
    position: index,
    is_default: status === "backlog",
    allow_new_items: true,
    team_id: null,
  }));
}

export function groupByCategory(statuses: WorkflowStatus[]): WorkflowCategoryGroup[] {
  return CATEGORY_ORDER.map((category) => ({
    category,
    label: CATEGORY_LABELS[category],
    statuses: statuses
      .filter((status) => status.category === category)
      .sort((a, b) => a.position - b.position),
  }));
}

export function moveWithinCategory(
  statuses: WorkflowStatus[],
  id: string,
  direction: "up" | "down"
): WorkflowStatus[] {
  const target = statuses.find((status) => status.id === id);
  if (!target) return statuses;
  const siblings = statuses
    .filter((status) => status.category === target.category)
    .sort((a, b) => a.position - b.position);
  const index = siblings.findIndex((status) => status.id === id);
  const swapIndex = direction === "up" ? index - 1 : index + 1;
  if (swapIndex < 0 || swapIndex >= siblings.length) return statuses;
  const neighbor = siblings[swapIndex]!;
  return statuses.map((status) => {
    if (status.id === target.id) return { ...status, position: neighbor.position };
    if (status.id === neighbor.id) return { ...status, position: target.position };
    return status;
  });
}
