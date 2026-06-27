import { describe, expect, it } from "bun:test";
import {
  BUILTIN_RECIPES,
  BUILTIN_TEMPLATES,
  FREEFORM_TEMPLATE_ID,
  matchRecipes,
  mergeTemplates,
  parseRecipeTrigger,
} from "./meeting-templates";
import type { MeetingTemplate } from "./types";

describe("BUILTIN_TEMPLATES", () => {
  it("ships the five named templates plus a freeform default", () => {
    expect(BUILTIN_TEMPLATES).toHaveLength(6);
    expect(BUILTIN_TEMPLATES[0]!.id).toBe(FREEFORM_TEMPLATE_ID);
    expect(BUILTIN_TEMPLATES.map((t) => t.name)).toContain("Retrospective");
  });
});

describe("mergeTemplates", () => {
  it("appends custom templates and drops id collisions with built-ins", () => {
    const custom: MeetingTemplate[] = [
      { id: "custom-1", name: "Weekly", sections: ["A"], prompt_scaffold: null, built_in: false },
      { id: FREEFORM_TEMPLATE_ID, name: "Dupe", sections: [], prompt_scaffold: null, built_in: false },
    ];
    const merged = mergeTemplates(BUILTIN_TEMPLATES, custom);
    expect(merged).toHaveLength(BUILTIN_TEMPLATES.length + 1);
    expect(merged.some((t) => t.id === "custom-1")).toBe(true);
  });
});

describe("matchRecipes", () => {
  it("returns all recipes for the empty query", () => {
    expect(matchRecipes("", BUILTIN_RECIPES)).toHaveLength(BUILTIN_RECIPES.length);
  });

  it("filters by name fragment", () => {
    const matches = matchRecipes("task", BUILTIN_RECIPES);
    expect(matches).toHaveLength(1);
    expect(matches[0]!.id).toBe("create-tasks");
  });
});

describe("parseRecipeTrigger", () => {
  it("extracts the query after a leading slash", () => {
    expect(parseRecipeTrigger("/task")).toBe("task");
    expect(parseRecipeTrigger("/")).toBe("");
  });

  it("returns null when not a recipe trigger", () => {
    expect(parseRecipeTrigger("hello")).toBeNull();
  });
});
