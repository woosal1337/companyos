"use client";

import { useMemo, useState } from "react";
import { ListTree } from "lucide-react";

interface Heading {
  level: number;
  text: string;
  key: string;
}

function parseHeadings(markdown: string): Heading[] {
  const headings: Heading[] = [];
  let inFence = false;
  markdown.split("\n").forEach((line, index) => {
    if (/^\s*```/.test(line)) inFence = !inFence;
    if (inFence) return;
    const match = /^(#{1,6})\s+(.+?)\s*#*$/.exec(line);
    if (match) {
      headings.push({
        level: match[1]!.length,
        text: match[2]!.replace(/[*_`]/g, "").trim(),
        key: `${index}-${match[2]!.slice(0, 16)}`,
      });
    }
  });
  return headings;
}

function jumpTo(text: string): void {
  const target = text.trim().toLowerCase();
  const headings = Array.from(document.querySelectorAll("h1,h2,h3,h4,h5,h6"));
  const el = headings.find((h) => (h.textContent ?? "").trim().toLowerCase() === target);
  el?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export function NoteOutline({ content }: { content: string }) {
  const [open, setOpen] = useState(true);
  const headings = useMemo(() => parseHeadings(content), [content]);

  const stats = useMemo(() => {
    const text = content.replace(/[#>*_`~-]/g, " ");
    const words = text.split(/\s+/).filter(Boolean).length;
    return {
      words,
      chars: content.length,
      readMin: Math.max(1, Math.round(words / 200)),
    };
  }, [content]);

  return (
    <aside className="flex w-56 shrink-0 flex-col gap-3">
      <div className="flex items-center justify-between">
        <button
          type="button"
          onClick={() => setOpen((value) => !value)}
          className="flex items-center gap-1.5 text-caption font-medium text-muted-foreground hover:text-foreground"
        >
          <ListTree className="size-3.5" />
          Outline
        </button>
      </div>
      {open ? (
        headings.length === 0 ? (
          <p className="text-caption text-muted-foreground/70">No headings yet.</p>
        ) : (
          <ul className="flex flex-col gap-0.5 border-l border-border">
            {headings.map((heading) => (
              <li key={heading.key}>
                <button
                  type="button"
                  onClick={() => jumpTo(heading.text)}
                  className="block w-full truncate py-0.5 text-left text-caption text-muted-foreground transition-colors hover:text-foreground"
                  style={{ paddingLeft: `${(heading.level - 1) * 0.75 + 0.75}rem` }}
                  title={heading.text}
                >
                  {heading.text}
                </button>
              </li>
            ))}
          </ul>
        )
      ) : null}
      <div className="flex flex-col gap-0.5 border-t border-border pt-3 text-caption text-muted-foreground">
        <span>{stats.words} words</span>
        <span>{stats.chars} characters</span>
        <span>{stats.readMin} min read</span>
      </div>
    </aside>
  );
}
