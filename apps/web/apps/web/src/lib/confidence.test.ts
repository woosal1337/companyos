import { describe, expect, it } from "bun:test";
import {
  confidenceBand,
  coverageBand,
  coverageLabel,
  coverageRatio,
  isActionable,
} from "./confidence";

describe("confidenceBand", () => {
  it("classifies high/medium/low by threshold", () => {
    expect(confidenceBand(0.9)).toBe("high");
    expect(confidenceBand(0.75)).toBe("high");
    expect(confidenceBand(0.5)).toBe("medium");
    expect(confidenceBand(0.44)).toBe("low");
    expect(confidenceBand(0)).toBe("low");
  });

  it("treats non-finite and out-of-range scores as low/clamped", () => {
    expect(confidenceBand(Number.NaN)).toBe("low");
    expect(confidenceBand(-1)).toBe("low");
    expect(confidenceBand(5)).toBe("high");
  });
});

describe("isActionable", () => {
  it("blocks auto-suggest on low confidence only", () => {
    expect(isActionable("high")).toBe(true);
    expect(isActionable("medium")).toBe(true);
    expect(isActionable("low")).toBe(false);
  });
});

describe("coverage", () => {
  it("computes ratio and guards zero total", () => {
    expect(coverageRatio({ consulted: 2, total: 8 })).toBe(0.25);
    expect(coverageRatio({ consulted: 1, total: 0 })).toBe(0);
  });

  it("labels coverage and pluralizes", () => {
    expect(coverageLabel({ consulted: 2, total: 8 })).toBe("Based on 2 of 8 sources");
    expect(coverageLabel({ consulted: 1, total: 1 })).toBe("Based on 1 of 1 source");
    expect(coverageLabel({ consulted: 0, total: 0 })).toBe("No sources consulted");
  });

  it("bands coverage by ratio", () => {
    expect(coverageBand({ consulted: 8, total: 8 })).toBe("high");
    expect(coverageBand({ consulted: 2, total: 8 })).toBe("low");
  });
});
