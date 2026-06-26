export type AutomationTrigger = "on_triage_entry" | "on_status_change";

export type AutomationActionType = "label" | "route" | "assign" | "set_priority";

export interface AutomationAction {
  type: AutomationActionType;
  value: string;
}

export interface TriageRule {
  id: string;
  name: string;
  trigger: AutomationTrigger;
  actions: AutomationAction[];
  is_skill: boolean;
  enabled: boolean;
  created_at: string;
}

export const TRIGGER_LABELS: Record<AutomationTrigger, string> = {
  on_triage_entry: "When a task enters triage",
  on_status_change: "When a task's status changes",
};

export const ACTION_LABELS: Record<AutomationActionType, string> = {
  label: "Add label",
  route: "Route to project",
  assign: "Assign to",
  set_priority: "Set priority",
};

export function describeAction(action: AutomationAction): string {
  return `${ACTION_LABELS[action.type]} ${action.value}`.trim();
}

export function describeRule(rule: TriageRule): string {
  const actions =
    rule.actions.length === 0
      ? "do nothing"
      : rule.actions.map(describeAction).join(", then ");
  return `${TRIGGER_LABELS[rule.trigger]} → ${actions}`;
}
