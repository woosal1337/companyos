import type { TranscriptChapter } from "./types";

export const MIN_CHAPTERS = 2;
export const MIN_SEGMENTS_FOR_CHAPTERS = 12;

export function shouldShowChapters(
  chapters: TranscriptChapter[],
  segmentCount: number
): boolean {
  return chapters.length >= MIN_CHAPTERS && segmentCount >= MIN_SEGMENTS_FOR_CHAPTERS;
}

export function activeChapterIndex(
  chapters: TranscriptChapter[],
  currentSeconds: number
): number {
  if (chapters.length === 0) return -1;
  let index = 0;
  for (let i = 0; i < chapters.length; i += 1) {
    const chapter = chapters[i];
    if (chapter && chapter.start_seconds <= currentSeconds) {
      index = i;
    } else {
      break;
    }
  }
  return index;
}
