import {
  Activity,
  ArrowRightLeft,
  CheckCircle2,
  CircleAlert,
  CirclePlus,
  Download,
  FileText,
  Flag,
  Info,
  ListTodo,
  MessageSquare,
  Pencil,
  Sparkles,
  Trash2,
  UserPlus,
  type LucideIcon,
} from "lucide-react";
import type { ActivityEvent } from "@/lib/types";

export type ActivityTone =
  | "neutral"
  | "accent"
  | "success"
  | "warning"
  | "danger"
  | "info"
  | "teal"
  | "lavender";

export interface ActivityTypeMeta {
  label: string;
  tone: ActivityTone;
  icon: LucideIcon;
  signal: "high" | "low";
}

export type ActivityKind =
  | "created"
  | "updated"
  | "status-changed"
  | "assigned"
  | "commented"
  | "note"
  | "decision"
  | "action-item"
  | "blocker"
  | "approval"
  | "fyi"
  | "standup"
  | "imported"
  | "member-added"
  | "deleted"
  | "system";

export const TONE_CHIP_CLASSES: Record<ActivityTone, string> = {
  neutral: "bg-subtle text-muted-foreground",
  accent: "bg-accent-muted text-accent",
  success: "bg-success-muted text-success",
  warning: "bg-warning-muted text-warning",
  danger: "bg-danger-muted text-danger",
  info: "bg-info-muted text-info",
  teal: "bg-teal-muted text-teal",
  lavender: "bg-lavender/15 text-lavender",
};

export const TONE_ICON_CLASSES: Record<ActivityTone, string> = {
  neutral: "bg-subtle text-muted-foreground",
  accent: "bg-accent-muted text-accent",
  success: "bg-success-muted text-success",
  warning: "bg-warning-muted text-warning",
  danger: "bg-danger-muted text-danger",
  info: "bg-info-muted text-info",
  teal: "bg-teal-muted text-teal",
  lavender: "bg-lavender/15 text-lavender",
};

export const ACTIVITY_TAXONOMY: Record<ActivityKind, ActivityTypeMeta> = {
  created: { label: "Created", tone: "success", icon: CirclePlus, signal: "low" },
  updated: { label: "Updated", tone: "neutral", icon: Pencil, signal: "low" },
  "status-changed": {
    label: "Status",
    tone: "warning",
    icon: ArrowRightLeft,
    signal: "low",
  },
  assigned: { label: "Assigned", tone: "accent", icon: UserPlus, signal: "low" },
  commented: { label: "Comment", tone: "info", icon: MessageSquare, signal: "high" },
  note: { label: "Note", tone: "info", icon: FileText, signal: "high" },
  decision: { label: "Decision", tone: "accent", icon: Flag, signal: "high" },
  "action-item": { label: "Action item", tone: "teal", icon: ListTodo, signal: "high" },
  blocker: { label: "Blocker", tone: "danger", icon: CircleAlert, signal: "high" },
  approval: { label: "Approval", tone: "success", icon: CheckCircle2, signal: "high" },
  fyi: { label: "FYI", tone: "neutral", icon: Info, signal: "low" },
  standup: { label: "Standup", tone: "lavender", icon: Sparkles, signal: "high" },
  imported: { label: "Imported", tone: "teal", icon: Download, signal: "low" },
  "member-added": { label: "Member", tone: "accent", icon: UserPlus, signal: "high" },
  deleted: { label: "Deleted", tone: "danger", icon: Trash2, signal: "low" },
  system: { label: "Activity", tone: "neutral", icon: Activity, signal: "low" },
};

const EVENT_PATTERNS: ReadonlyArray<readonly [RegExp, ActivityKind]> = [
  [/decision/, "decision"],
  [/action[._-]?item/, "action-item"],
  [/block/, "blocker"],
  [/approv/, "approval"],
  [/standup/, "standup"],
  [/\bfyi\b/, "fyi"],
  [/import/, "imported"],
  [/member[._-]?(added|invited|joined)|joined/, "member-added"],
  [/comment|reply|message/, "commented"],
  [/note|summary|summariz/, "note"],
  [/status[._-]?changed|status|moved|transition/, "status-changed"],
  [/assign/, "assigned"],
  [/delete|remove|archive/, "deleted"],
  [/create|add|post|new\b/, "created"],
  [/update|edit|rename|change/, "updated"],
];

export function classifyActivity(event: ActivityEvent): ActivityKind {
  const haystack = `${event.entity_type} ${event.event_type}`.toLowerCase();
  for (const [pattern, kind] of EVENT_PATTERNS) {
    if (pattern.test(haystack)) {
      return kind;
    }
  }
  return "system";
}

export function activityMeta(event: ActivityEvent): ActivityTypeMeta {
  return ACTIVITY_TAXONOMY[classifyActivity(event)];
}

export function isHighSignal(event: ActivityEvent): boolean {
  return activityMeta(event).signal === "high";
}
