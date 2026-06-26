import { describe, expect, it } from "bun:test";
import { shareApiPath, shareMeetingPath, shareMeetingUrl } from "./share";

describe("share helpers", () => {
  it("builds the public route path", () => {
    expect(shareMeetingPath("tok123")).toBe("/share/meetings/tok123");
  });

  it("builds an absolute url and strips a trailing slash from origin", () => {
    expect(shareMeetingUrl("https://app.example.com/", "tok123")).toBe(
      "https://app.example.com/share/meetings/tok123"
    );
  });

  it("builds the public api path with an optional suffix", () => {
    expect(shareApiPath("tok123")).toBe("/api/v1/share/meetings/tok123");
    expect(shareApiPath("tok123", "/chat")).toBe("/api/v1/share/meetings/tok123/chat");
  });
});
