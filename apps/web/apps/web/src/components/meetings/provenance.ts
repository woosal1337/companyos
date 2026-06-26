import type { TranscriptSegment } from "@/lib/types";

export type Provenance = "ai" | "human";

export interface SummaryLine {
  id: string;
  raw: string;
  kind: "heading" | "bullet" | "text";
  level: number;
}

export interface SourceMatch {
  segment: TranscriptSegment;
  score: number;
}

const STOP_WORDS = new Set([
  "the",
  "and",
  "for",
  "are",
  "was",
  "were",
  "with",
  "that",
  "this",
  "from",
  "have",
  "has",
  "had",
  "will",
  "would",
  "should",
  "could",
  "their",
  "they",
  "them",
  "then",
  "than",
  "into",
  "about",
  "what",
  "which",
  "when",
  "your",
  "you",
  "our",
  "his",
  "her",
  "its",
  "out",
  "not",
  "but",
  "all",
  "any",
  "can",
  "get",
  "got",
]);

const MARKUP_PATTERN = /[*`#>_~[\]()]|\(([^)]+)\)/g;

export function stripMarkup(line: string): string {
  return line
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(MARKUP_PATTERN, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function tokenize(value: string): string[] {
  return stripMarkup(value)
    .toLowerCase()
    .split(/[^a-z0-9]+/)
    .filter((token) => token.length > 2 && !STOP_WORDS.has(token));
}

export function parseSummaryLines(source: string): SummaryLine[] {
  const lines: SummaryLine[] = [];
  let inCode = false;
  source.split("\n").forEach((rawLine, index) => {
    const trimmed = rawLine.trim();
    if (trimmed.startsWith("```")) {
      inCode = !inCode;
      return;
    }
    if (inCode || trimmed.length === 0) return;

    const headingMatch = /^(#{1,3})\s+(.*)$/.exec(trimmed);
    if (headingMatch && headingMatch[2]) {
      lines.push({
        id: `sl-${index}`,
        raw: headingMatch[2],
        kind: "heading",
        level: headingMatch[1]?.length ?? 1,
      });
      return;
    }

    const bulletMatch = /^\s*[-*]\s+(.*)$/.exec(rawLine);
    if (bulletMatch && bulletMatch[1] !== undefined) {
      lines.push({ id: `sl-${index}`, raw: bulletMatch[1], kind: "bullet", level: 0 });
      return;
    }

    lines.push({ id: `sl-${index}`, raw: trimmed, kind: "text", level: 0 });
  });
  return lines;
}

const MIN_OVERLAP_RATIO = 0.34;
const MIN_OVERLAP_TOKENS = 2;

export function matchLineToSegment(
  line: string,
  segments: TranscriptSegment[]
): SourceMatch | null {
  const lineTokens = tokenize(line);
  if (lineTokens.length === 0) return null;
  const lineSet = new Set(lineTokens);

  let best: SourceMatch | null = null;
  for (const segment of segments) {
    const segTokens = tokenize(segment.text);
    if (segTokens.length === 0) continue;
    let overlap = 0;
    const seen = new Set<string>();
    for (const token of segTokens) {
      if (lineSet.has(token) && !seen.has(token)) {
        seen.add(token);
        overlap += 1;
      }
    }
    if (overlap < MIN_OVERLAP_TOKENS) continue;
    const score = overlap / lineSet.size;
    if (!best || score > best.score) {
      best = { segment, score };
    }
  }

  if (!best || best.score < MIN_OVERLAP_RATIO) return null;
  return best;
}

export function matchTextToSegments(
  text: string,
  segments: TranscriptSegment[],
  limit = 3
): SourceMatch[] {
  const textTokens = tokenize(text);
  if (textTokens.length === 0) return [];
  const textSet = new Set(textTokens);

  const scored: SourceMatch[] = [];
  for (const segment of segments) {
    const segTokens = tokenize(segment.text);
    if (segTokens.length === 0) continue;
    let overlap = 0;
    const seen = new Set<string>();
    for (const token of segTokens) {
      if (textSet.has(token) && !seen.has(token)) {
        seen.add(token);
        overlap += 1;
      }
    }
    if (overlap < MIN_OVERLAP_TOKENS) continue;
    const score = overlap / textSet.size;
    if (score < MIN_OVERLAP_RATIO) continue;
    scored.push({ segment, score });
  }

  return scored.sort((a, b) => b.score - a.score).slice(0, limit);
}

export type SummarySectionKind = "decisions" | "actions" | "questions" | "highlights";

export interface SummarySection {
  kind: SummarySectionKind;
  lines: SummaryLine[];
}

interface SectionMatcher {
  kind: SummarySectionKind;
  heading: RegExp;
  lead: RegExp;
}

const SECTION_MATCHERS: SectionMatcher[] = [
  {
    kind: "decisions",
    heading: /\b(decision|decided|resolution|conclusion|agreement|agreed)\b/i,
    lead: /^(decided|agreed|resolved|we will|we'll|the team will|going with|chose|approved)\b/i,
  },
  {
    kind: "actions",
    heading: /\b(action item|action|next step|to-?do|todo|follow[- ]?up|task|owner)\b/i,
    lead: /^(\[[ x]\]\s*)?(@?\w+\s+(will|to|should|needs? to|owns?)|action:|todo:|follow[- ]?up:|assign)/i,
  },
  {
    kind: "questions",
    heading: /\b(open question|question|unresolved|risk|blocker|concern|parking lot)\b/i,
    lead: /(\?$|^(open question|unresolved|risk|blocker|concern|tbd)\b)/i,
  },
  {
    kind: "highlights",
    heading: /\b(highlight|key point|summary|overview|takeaway|note|topic|discussion)\b/i,
    lead: /.^/,
  },
];

const SECTION_ORDER: SummarySectionKind[] = [
  "decisions",
  "actions",
  "questions",
  "highlights",
];

function classifyHeading(text: string): SummarySectionKind | null {
  for (const matcher of SECTION_MATCHERS) {
    if (matcher.heading.test(text)) return matcher.kind;
  }
  return null;
}

function classifyLine(text: string): SummarySectionKind {
  const stripped = stripMarkup(text);
  for (const matcher of SECTION_MATCHERS) {
    if (matcher.kind === "highlights") continue;
    if (matcher.lead.test(stripped)) return matcher.kind;
  }
  return "highlights";
}

export function parseSummarySections(source: string): SummarySection[] {
  const lines = parseSummaryLines(source);
  const buckets = new Map<SummarySectionKind, SummaryLine[]>();
  const push = (kind: SummarySectionKind, line: SummaryLine) => {
    const existing = buckets.get(kind);
    if (existing) existing.push(line);
    else buckets.set(kind, [line]);
  };

  let current: SummarySectionKind | null = null;
  for (const line of lines) {
    if (line.kind === "heading") {
      current = classifyHeading(line.raw);
      continue;
    }
    const kind = current ?? classifyLine(line.raw);
    push(kind, line);
  }

  return SECTION_ORDER.filter((kind) => (buckets.get(kind)?.length ?? 0) > 0).map((kind) => ({
    kind,
    lines: buckets.get(kind) ?? [],
  }));
}
