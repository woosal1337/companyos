import { describe, expect, it } from "bun:test";
import { hierarchy, hierarchyClass } from "./hierarchy";

describe("hierarchy", () => {
  it("defines exactly the four levels", () => {
    expect(Object.keys(hierarchy).sort()).toEqual(["headline", "label", "meta", "supporting"]);
  });

  it("renders identifiers and timestamps as mono + muted + tabular", () => {
    expect(hierarchy.meta).toContain("font-mono");
    expect(hierarchy.meta).toContain("text-muted-foreground");
    expect(hierarchy.meta).toContain("tabular");
  });

  it("gives only the headline full foreground weight", () => {
    expect(hierarchy.headline).toContain("font-semibold");
    expect(hierarchy.headline).toContain("text-foreground");
    expect(hierarchy.label).toContain("text-muted-foreground");
    expect(hierarchy.supporting).toContain("text-muted-foreground");
  });

  it("clamps supporting copy to one line", () => {
    expect(hierarchy.supporting).toContain("line-clamp-1");
  });

  it("resolves a level via hierarchyClass", () => {
    expect(hierarchyClass("headline")).toBe(hierarchy.headline);
  });
});
