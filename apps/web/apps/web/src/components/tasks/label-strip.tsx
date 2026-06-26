"use client";

import { useLayoutEffect, useRef, useState } from "react";
import type { Label } from "@/lib/types";

const ROW_HEIGHT = 22;
const ROW_GAP = 4;

function Chip({ children, label }: { children: React.ReactNode; label?: Label }) {
  return (
    <span className="inline-flex h-5 max-w-full items-center gap-1 rounded-full border border-border bg-surface px-1.5 text-caption text-foreground">
      {label ? (
        <span
          aria-hidden
          className="size-1.5 shrink-0 rounded-full"
          style={{ backgroundColor: label.color }}
        />
      ) : null}
      <span className="min-w-0 truncate">{children}</span>
    </span>
  );
}

export function LabelStrip({ labels, maxRows = 2 }: { labels: Label[]; maxRows?: number }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const lastWidthRef = useRef(-1);
  const [visibleCount, setVisibleCount] = useState<number | null>(null);

  useLayoutEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    let raf = 0;

    const commit = () => {
      const chips = Array.from(container.querySelectorAll<HTMLElement>("[data-label-chip]"));
      if (chips.length === 0) {
        setVisibleCount(0);
        return;
      }
      const rowTops: number[] = [];
      for (const chip of chips) {
        const top = chip.offsetTop;
        if (!rowTops.includes(top)) rowTops.push(top);
      }
      if (rowTops.length <= maxRows) {
        setVisibleCount(labels.length);
        return;
      }
      const lastAllowedTop = rowTops[maxRows - 1] ?? rowTops[0] ?? 0;
      let firstOverflow = chips.length;
      for (let i = 0; i < chips.length; i += 1) {
        const chip = chips[i];
        if (chip && chip.offsetTop > lastAllowedTop) {
          firstOverflow = i;
          break;
        }
      }
      setVisibleCount(Math.max(0, firstOverflow));
    };

    const remeasure = () => {
      cancelAnimationFrame(raf);
      setVisibleCount(null);
      raf = requestAnimationFrame(commit);
    };

    lastWidthRef.current = container.clientWidth;
    remeasure();

    const observer = new ResizeObserver((entries) => {
      const width = entries[0]?.contentRect.width ?? container.clientWidth;
      if (Math.abs(width - lastWidthRef.current) < 1) return;
      lastWidthRef.current = width;
      remeasure();
    });
    observer.observe(container);

    return () => {
      cancelAnimationFrame(raf);
      observer.disconnect();
    };
  }, [labels, maxRows]);

  if (labels.length === 0) return null;

  const measuring = visibleCount === null;
  const shown = measuring ? labels : labels.slice(0, visibleCount);
  const hidden = labels.length - shown.length;

  return (
    <div
      ref={containerRef}
      className="mt-2 flex flex-wrap content-start gap-1 overflow-hidden"
      style={{ maxHeight: maxRows * ROW_HEIGHT + (maxRows - 1) * ROW_GAP }}
    >
      {shown.map((label) => (
        <span key={label.id} data-label-chip className="max-w-full">
          <Chip label={label}>{label.name}</Chip>
        </span>
      ))}
      {measuring || hidden > 0 ? (
        <span
          data-label-chip
          aria-hidden={measuring ? true : undefined}
          className={measuring ? "invisible shrink-0" : "shrink-0"}
        >
          <Chip>+{measuring ? 0 : hidden}</Chip>
        </span>
      ) : null}
    </div>
  );
}
