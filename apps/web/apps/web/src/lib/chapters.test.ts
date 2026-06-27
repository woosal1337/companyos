import { describe, expect, it } from "bun:test";
import { activeChapterIndex, shouldShowChapters } from "./chapters";
import type { TranscriptChapter } from "./types";

const chapters: TranscriptChapter[] = [
  { label: "Agenda", start_seconds: 0, segment_id: "s0" },
  { label: "Decisions", start_seconds: 300, segment_id: "s10" },
  { label: "Q&A", start_seconds: 900, segment_id: "s30" },
];

describe("shouldShowChapters", () => {
  it("requires at least two chapters and enough segments", () => {
    expect(shouldShowChapters(chapters, 40)).toBe(true);
    expect(shouldShowChapters([chapters[0]], 40)).toBe(false);
    expect(shouldShowChapters(chapters, 5)).toBe(false);
  });
});

describe("activeChapterIndex", () => {
  it("returns the last chapter whose start is at or before the position", () => {
    expect(activeChapterIndex(chapters, 0)).toBe(0);
    expect(activeChapterIndex(chapters, 299)).toBe(0);
    expect(activeChapterIndex(chapters, 300)).toBe(1);
    expect(activeChapterIndex(chapters, 1200)).toBe(2);
  });

  it("returns -1 for no chapters", () => {
    expect(activeChapterIndex([], 100)).toBe(-1);
  });
});
