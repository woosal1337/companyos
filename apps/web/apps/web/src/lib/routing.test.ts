import { describe, expect, it } from "bun:test";
import { resolveRouting } from "./routing";

describe("resolveRouting", () => {
  it("suggests when confidence is actionable and a project is present", () => {
    const result = resolveRouting({ project_id: "p1", route: "Engineering", confidence: 0.8 });
    expect(result.mode).toBe("suggest");
    expect(result.projectId).toBe("p1");
    expect(result.band).toBe("high");
  });

  it("falls back to the picker on low confidence rather than a confident wrong guess", () => {
    const result = resolveRouting({ project_id: "p1", route: "Engineering", confidence: 0.2 });
    expect(result.mode).toBe("pick");
    expect(result.band).toBe("low");
  });

  it("falls back to the picker when there is no suggestion or project", () => {
    expect(resolveRouting(null).mode).toBe("pick");
    expect(resolveRouting({ project_id: null, route: null, confidence: 0.9 }).mode).toBe("pick");
  });
});
