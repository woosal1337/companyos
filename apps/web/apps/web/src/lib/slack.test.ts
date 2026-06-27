import { describe, expect, it } from "bun:test";
import { buildSlackMessage } from "./slack";

describe("buildSlackMessage", () => {
  it("includes the title, action items, and an Ask link", () => {
    const message = buildSlackMessage(
      "Weekly sync",
      ["Ship the API", "Email the customer"],
      "https://app.example.com/share/meetings/tok"
    );
    expect(message).toContain("*Weekly sync* — meeting summary");
    expect(message).toContain("• Ship the API");
    expect(message).toContain("Ask the AI about this meeting: https://app.example.com/share/meetings/tok");
  });

  it("caps action items at eight", () => {
    const items = Array.from({ length: 12 }, (_, i) => `Item ${i}`);
    const message = buildSlackMessage("M", items, null);
    expect(message.match(/•/g)).toHaveLength(8);
  });

  it("omits the action items block and link when absent", () => {
    expect(buildSlackMessage("M", [], null)).toBe("*M* — meeting summary");
  });
});
