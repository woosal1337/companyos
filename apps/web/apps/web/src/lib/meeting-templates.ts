import type { MeetingRecipe, MeetingTemplate } from "./types";

export const FREEFORM_TEMPLATE_ID = "freeform";

export const BUILTIN_TEMPLATES: MeetingTemplate[] = [
  { id: FREEFORM_TEMPLATE_ID, name: "Freeform", sections: [], prompt_scaffold: null, built_in: true },
  {
    id: "one-on-one",
    name: "One-on-One",
    sections: ["Wins", "Blockers", "Feedback", "Action items"],
    prompt_scaffold: null,
    built_in: true,
  },
  {
    id: "standup",
    name: "Stand-up",
    sections: ["Yesterday", "Today", "Blockers"],
    prompt_scaffold: null,
    built_in: true,
  },
  {
    id: "customer-call",
    name: "Customer Call",
    sections: ["Context", "Pain points", "Requests", "Next steps"],
    prompt_scaffold: null,
    built_in: true,
  },
  {
    id: "decision",
    name: "Decision Meeting",
    sections: ["Options considered", "Decision", "Rationale", "Owners"],
    prompt_scaffold: null,
    built_in: true,
  },
  {
    id: "retro",
    name: "Retrospective",
    sections: ["What went well", "What didn't", "Action items"],
    prompt_scaffold: null,
    built_in: true,
  },
];

export const BUILTIN_RECIPES: MeetingRecipe[] = [
  {
    id: "create-tasks",
    name: "Create tasks from action items",
    prompt: "Extract every action item from this meeting as a discrete task with an owner.",
    built_in: true,
  },
  {
    id: "slack-summary",
    name: "Draft Slack summary",
    prompt: "Write a concise Slack-ready summary of this meeting with the key decisions.",
    built_in: true,
  },
  {
    id: "follow-up-email",
    name: "Write follow-up email to attendees",
    prompt: "Draft a follow-up email to the attendees recapping outcomes and next steps.",
    built_in: true,
  },
  {
    id: "extract-decisions",
    name: "Extract decisions for the project log",
    prompt: "List the decisions made in this meeting, one per line, for the project log.",
    built_in: true,
  },
];

export function mergeTemplates(
  builtIns: MeetingTemplate[],
  custom: MeetingTemplate[]
): MeetingTemplate[] {
  const seen = new Set(builtIns.map((template) => template.id));
  return [...builtIns, ...custom.filter((template) => !seen.has(template.id))];
}

export function matchRecipes(query: string, recipes: MeetingRecipe[]): MeetingRecipe[] {
  const trimmed = query.trim().toLowerCase();
  if (trimmed.length === 0) return recipes;
  return recipes.filter((recipe) => recipe.name.toLowerCase().includes(trimmed));
}

export function parseRecipeTrigger(input: string): string | null {
  if (!input.startsWith("/")) return null;
  return input.slice(1);
}
