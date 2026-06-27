import { describe, expect, it } from "bun:test";
import { describeAction, describeRule, type TriageRule } from "./automation";

describe("describeAction", () => {
  it("renders a human-readable action", () => {
    expect(describeAction({ type: "label", value: "bug" })).toBe("Add label bug");
    expect(describeAction({ type: "set_priority", value: "urgent" })).toBe("Set priority urgent");
  });
});

describe("describeRule", () => {
  const base: TriageRule = {
    id: "r1",
    name: "Bug intake",
    trigger: "on_triage_entry",
    actions: [
      { type: "label", value: "bug" },
      { type: "route", value: "Platform" },
    ],
    is_skill: false,
    enabled: true,
    created_at: "2026-06-12T00:00:00Z",
  };

  it("chains the trigger and ordered actions", () => {
    expect(describeRule(base)).toBe(
      "When a task enters triage → Add label bug, then Route to project Platform"
    );
  });

  it("handles rules with no actions", () => {
    expect(describeRule({ ...base, actions: [] })).toBe("When a task enters triage → do nothing");
  });
});
