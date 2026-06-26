export interface ParsedSegment {
  speaker: string;
  start_seconds: number;
  end_seconds: number;
  text: string;
}

export interface FolioImportPayload {
  title: string;
  started_at: string;
  duration_seconds?: number;
  attendees: string[];
  segments: ParsedSegment[];
  markdown?: string;
}

const UNKNOWN_SPEAKER = "Unknown";
const SPEAKER_LINE = /^\s*([A-Za-z0-9 ._'-]{1,80}?)\s*:\s+(.*\S.*)$/;

export function parseTranscript(title: string, raw: string): FolioImportPayload {
  const lines = raw.split(/\r?\n/);
  const segments: ParsedSegment[] = [];
  const attendees = new Set<string>();

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.length === 0) {
      continue;
    }
    const match = trimmed.match(SPEAKER_LINE);
    const speaker = match?.[1]?.trim();
    if (match && speaker) {
      attendees.add(speaker);
      segments.push({
        speaker,
        start_seconds: 0,
        end_seconds: 0,
        text: match[2]?.trim() ?? trimmed,
      });
      continue;
    }
    segments.push({
      speaker: UNKNOWN_SPEAKER,
      start_seconds: 0,
      end_seconds: 0,
      text: trimmed,
    });
  }

  return {
    title: title.trim(),
    started_at: new Date().toISOString(),
    attendees: Array.from(attendees),
    segments,
    markdown: raw.trim().length > 0 ? raw.trim() : undefined,
  };
}
