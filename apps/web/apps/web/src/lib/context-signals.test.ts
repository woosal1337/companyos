import { describe, expect, it } from "bun:test";
import { groupSignals, signalHref } from "./context-signals";
import type { ContextSignal } from "./types";

const signals: ContextSignal[] = [
  { kind: "related_note", id: "n1", title: "Spec" },
  { kind: "related_task", id: "t1", title: "Fix login" },
  { kind: "related_meeting", id: "m1", title: "Kickoff" },
  { kind: "related_task", id: "t2", title: "Add SSO" },
];

describe("signalHref", () => {
  it("links meetings and notes, but not tasks", () => {
    expect(signalHref("org", { kind: "related_meeting", id: "m1", title: "" })).toBe(
      "/app/org/meetings/m1"
    );
    expect(signalHref("org", { kind: "related_note", id: "n1", title: "" })).toBe(
      "/app/org/notes/n1"
    );
    expect(signalHref("org", { kind: "related_task", id: "t1", title: "" })).toBeNull();
  });
});

describe("groupSignals", () => {
  it("groups by kind in a stable order and drops empty groups", () => {
    const grouped = groupSignals(signals);
    expect(grouped.map((g) => g.kind)).toEqual(["related_task", "related_meeting", "related_note"]);
    expect(grouped[0].items).toHaveLength(2);
  });

  it("returns nothing for an empty signal set", () => {
    expect(groupSignals([])).toEqual([]);
  });
});
