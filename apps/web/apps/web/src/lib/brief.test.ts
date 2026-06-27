import { describe, expect, it } from "bun:test";
import { briefSourceHref, isFutureEvent } from "./brief";

describe("isFutureEvent", () => {
  const now = Date.parse("2026-06-12T10:00:00Z");

  it("is true for events after now", () => {
    expect(isFutureEvent("2026-06-12T11:00:00Z", now)).toBe(true);
  });

  it("is false for past events", () => {
    expect(isFutureEvent("2026-06-12T09:00:00Z", now)).toBe(false);
  });

  it("guards invalid dates", () => {
    expect(isFutureEvent("not-a-date", now)).toBe(false);
  });
});

describe("briefSourceHref", () => {
  it("links meeting, note, and project sources", () => {
    expect(
      briefSourceHref("org", { text: "", source_kind: "meeting", source_id: "m1", source_label: "" })
    ).toBe("/app/org/meetings/m1");
    expect(
      briefSourceHref("org", { text: "", source_kind: "project", source_id: "p1", source_label: "" })
    ).toBe("/app/org/projects/p1");
  });

  it("returns null for task sources (no deep link)", () => {
    expect(
      briefSourceHref("org", { text: "", source_kind: "task", source_id: "t1", source_label: "" })
    ).toBeNull();
  });
});
