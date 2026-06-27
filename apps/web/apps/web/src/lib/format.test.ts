import { describe, expect, it } from "bun:test";
import { formatCount, formatDuration, formatPercent, formatTimestamp, relativeTime } from "./format";

describe("formatDuration", () => {
  it("renders seconds under a minute", () => {
    expect(formatDuration(45)).toBe("45s");
  });

  it("renders hours and minutes", () => {
    expect(formatDuration(5040)).toBe("1h 24m");
  });

  it("clamps negatives to 0s", () => {
    expect(formatDuration(-10)).toBe("0s");
  });
});

describe("formatCount", () => {
  it("compacts large numbers", () => {
    expect(formatCount(1200)).toBe("1.2K");
    expect(formatCount(3_400_000)).toBe("3.4M");
  });

  it("guards non-finite input", () => {
    expect(formatCount(Number.NaN)).toBe("0");
  });
});

describe("formatPercent", () => {
  it("formats a fraction", () => {
    expect(formatPercent(0.5)).toBe("50%");
  });
});

describe("formatTimestamp", () => {
  it("formats mm:ss", () => {
    expect(formatTimestamp(125)).toBe("2:05");
  });

  it("formats h:mm:ss", () => {
    expect(formatTimestamp(3725)).toBe("1:02:05");
  });
});

describe("relativeTime", () => {
  it("returns a relative string and an exact title", () => {
    const result = relativeTime(new Date().toISOString());
    expect(result.relative).toBe("just now");
    expect(result.title.length).toBeGreaterThan(0);
  });
});
