import { describe, expect, it } from "bun:test";
import { citationHtml, entityHref, parseEntityRef, serializeEntityRef } from "./dnd";

describe("entityHref", () => {
  it("links meetings and notes, but not tasks or decisions", () => {
    expect(entityHref("org", "meeting", "m1")).toBe("/app/org/meetings/m1");
    expect(entityHref("org", "note", "n1")).toBe("/app/org/notes/n1");
    expect(entityHref("org", "task", "t1")).toBeNull();
    expect(entityHref("org", "decision", "d1")).toBeNull();
  });
});

describe("serialize/parse round-trip", () => {
  it("preserves the ref", () => {
    const ref = { kind: "meeting" as const, id: "m1", title: "Kickoff", href: "/app/o/meetings/m1" };
    expect(parseEntityRef(serializeEntityRef(ref))).toEqual(ref);
  });

  it("rejects malformed payloads", () => {
    expect(parseEntityRef("not json")).toBeNull();
    expect(parseEntityRef(JSON.stringify({ id: "x" }))).toBeNull();
    expect(parseEntityRef(null)).toBeNull();
  });
});

describe("citationHtml", () => {
  it("renders a link with entity data attributes and escapes html", () => {
    const html = citationHtml({ kind: "meeting", id: "m1", title: "<b>Hi</b>", href: "/x" });
    expect(html).toContain('data-entity-kind="meeting"');
    expect(html).toContain("&lt;b&gt;Hi&lt;/b&gt;");
  });

  it("renders plain text when there is no href", () => {
    const html = citationHtml({ kind: "task", id: "t1", title: "Fix", href: null });
    expect(html).not.toContain("<a");
    expect(html).toContain("Fix");
  });
});
