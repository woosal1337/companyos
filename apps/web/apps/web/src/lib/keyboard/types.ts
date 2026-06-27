export type ShortcutScope = "global" | "navigation" | "action";

export interface ShortcutBinding {
  id: string;
  keys: string;
  label: string;
  scope: ShortcutScope;
  run: () => void;
  enabled?: boolean;
}

export interface ParsedKeys {
  kind: "single" | "chord" | "combo";
  prefix?: string;
  key: string;
  mod: boolean;
  shift: boolean;
  alt: boolean;
}

export interface KeyboardContextValue {
  register: (binding: ShortcutBinding) => () => void;
  list: () => ShortcutBinding[];
  setSuppressed: (suppressed: boolean) => void;
}
