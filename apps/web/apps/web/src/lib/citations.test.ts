import { describe, expect, it } from "bun:test";
import { citationHref, citationLabel } from "./citations";

describe("citationHref", () => {
  it("appends a timestamp anchor when present", () => {
    expect(
      citationHref("org", { meeting_id: "m1", quote: "", start_seconds: 125 })
    ).toBe("/app/org/meetings/m1?t=125");
  });

  it("links the meeting without anchor when no timestamp", () => {
    expect(citationHref("org", { meeting_id: "m1", quote: "" })).toBe("/app/org/meetings/m1");
  });
});

describe("citationLabel", () => {
  it("combines title and timestamp", () => {
    expect(
      citationLabel({ meeting_id: "m1", meeting_title: "Kickoff", quote: "", start_seconds: 65 })
    ).toBe("Kickoff · 1:05");
  });

  it("falls back to Meeting when title is missing", () => {
    expect(citationLabel({ meeting_id: "m1", quote: "" })).toBe("Meeting");
  });
});
