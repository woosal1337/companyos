import type { ParsedKeys } from "./types";

const MODIFIERS = new Set(["mod", "shift", "alt", "ctrl", "cmd", "meta"]);

export function parseKeys(keys: string): ParsedKeys {
  const trimmed = keys.trim().toLowerCase();

  if (trimmed.includes("+")) {
    const parts = trimmed.split("+").map((part) => part.trim());
    const key = parts.filter((part) => !MODIFIERS.has(part)).at(-1) ?? "";
    return {
      kind: "combo",
      key,
      mod: parts.includes("mod") || parts.includes("cmd") || parts.includes("meta") || parts.includes("ctrl"),
      shift: parts.includes("shift"),
      alt: parts.includes("alt"),
    };
  }

  const parts = trimmed.split(/\s+/).filter(Boolean);
  const [first, second] = parts;
  if (first !== undefined && second !== undefined) {
    return {
      kind: "chord",
      prefix: first,
      key: second,
      mod: false,
      shift: false,
      alt: false,
    };
  }

  return {
    kind: "single",
    key: first ?? "",
    mod: false,
    shift: false,
    alt: false,
  };
}

export function eventKey(event: KeyboardEvent): string {
  const key = event.key;
  if (key === " ") return "space";
  if (key === "Escape") return "escape";
  if (key === "Enter") return "enter";
  return key.toLowerCase();
}

export function matchesCombo(parsed: ParsedKeys, event: KeyboardEvent): boolean {
  if (parsed.kind !== "combo") return false;
  const mod = event.metaKey || event.ctrlKey;
  if (parsed.mod !== mod) return false;
  if (parsed.shift !== event.shiftKey) return false;
  if (parsed.alt !== event.altKey) return false;
  return eventKey(event) === parsed.key;
}

export function isPlainKey(event: KeyboardEvent): boolean {
  return !event.metaKey && !event.ctrlKey && !event.altKey;
}

export function formatKeysForDisplay(keys: string): string[] {
  const parsed = parseKeys(keys);
  if (parsed.kind === "combo") {
    const tokens: string[] = [];
    if (parsed.mod) tokens.push("⌘");
    if (parsed.shift) tokens.push("⇧");
    if (parsed.alt) tokens.push("⌥");
    tokens.push(parsed.key.toUpperCase());
    return tokens;
  }
  if (parsed.kind === "chord") {
    return [parsed.prefix?.toUpperCase() ?? "", parsed.key.toUpperCase()];
  }
  return [parsed.key.toUpperCase()];
}
