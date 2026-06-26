import * as React from "react";
import { cn } from "../lib/cn";

export interface IllustrationProps {
  className?: string;
}

export function IsoStack({ className }: IllustrationProps) {
  const layers = [0, 1, 2, 3, 4];
  return (
    <svg
      viewBox="0 0 200 200"
      fill="none"
      aria-hidden="true"
      className={cn("text-muted-foreground", className)}
    >
      <g stroke="currentColor" strokeWidth={1} strokeLinejoin="round">
        {layers.map((i) => {
          const y = 138 - i * 22;
          return (
            <g key={i} className={i === layers.length - 1 ? "text-border-strong" : undefined}>
              <path
                d={`M100 ${y - 26} L158 ${y} L100 ${y + 26} L42 ${y} Z`}
                stroke="currentColor"
                fill="currentColor"
                fillOpacity={0.03}
              />
              {i < layers.length - 1 ? (
                <>
                  <path d={`M42 ${y} L42 ${y + 8}`} stroke="currentColor" />
                  <path d={`M100 ${y + 26} L100 ${y + 34}`} stroke="currentColor" />
                  <path d={`M158 ${y} L158 ${y + 8}`} stroke="currentColor" />
                </>
              ) : null}
            </g>
          );
        })}
      </g>
    </svg>
  );
}

export function IsoCubes({ className }: IllustrationProps) {
  const cube = (ox: number, oy: number, s: number, bright: boolean) => {
    const w = s;
    const h = s * 0.55;
    const d = s * 0.7;
    const top = `M${ox} ${oy} L${ox + w} ${oy - h} L${ox + w * 2} ${oy} L${ox + w} ${oy + h} Z`;
    const left = `M${ox} ${oy} L${ox} ${oy + d} L${ox + w} ${oy + h + d} L${ox + w} ${oy + h} Z`;
    const right = `M${ox + w * 2} ${oy} L${ox + w * 2} ${oy + d} L${ox + w} ${oy + h + d} L${ox + w} ${oy + h} Z`;
    return (
      <g className={bright ? "text-border-strong" : undefined} stroke="currentColor" strokeWidth={1} strokeLinejoin="round">
        <path d={top} fill="currentColor" fillOpacity={bright ? 0.06 : 0.02} />
        <path d={left} fill="currentColor" fillOpacity={0.04} />
        <path d={right} fill="currentColor" fillOpacity={0.01} />
      </g>
    );
  };
  return (
    <svg
      viewBox="0 0 200 200"
      fill="none"
      aria-hidden="true"
      className={cn("text-muted-foreground", className)}
    >
      {cube(30, 96, 26, false)}
      {cube(96, 70, 30, true)}
      {cube(118, 128, 22, false)}
      {cube(58, 150, 20, false)}
    </svg>
  );
}

export function IsoFan({ className }: IllustrationProps) {
  const bars = [0, 1, 2, 3, 4, 5, 6];
  return (
    <svg
      viewBox="0 0 200 200"
      fill="none"
      aria-hidden="true"
      className={cn("text-muted-foreground", className)}
    >
      <g stroke="currentColor" strokeWidth={1} strokeLinejoin="round">
        {bars.map((i) => {
          const x = 30 + i * 22;
          const skew = (i - 3) * 6;
          const h = 96 - Math.abs(i - 3) * 9;
          const top = 150 - h;
          return (
            <g key={i} className={i === 3 ? "text-border-strong" : undefined}>
              <path
                d={`M${x} ${top} L${x + 16} ${top + skew * 0.4} L${x + 16} ${top + skew * 0.4 + h} L${x} ${150} Z`}
                stroke="currentColor"
                fill="currentColor"
                fillOpacity={i === 3 ? 0.06 : 0.025}
              />
            </g>
          );
        })}
      </g>
    </svg>
  );
}

export function WireMesh({ className }: IllustrationProps) {
  const nodes = [
    { x: 44, y: 56, bright: true },
    { x: 108, y: 38, bright: false },
    { x: 160, y: 74, bright: true },
    { x: 70, y: 110, bright: false },
    { x: 124, y: 116, bright: false },
    { x: 38, y: 156, bright: false },
    { x: 150, y: 152, bright: true },
  ];
  const edges: ReadonlyArray<readonly [number, number]> = [
    [0, 1],
    [1, 2],
    [0, 3],
    [1, 4],
    [3, 4],
    [3, 5],
    [4, 6],
    [2, 4],
    [5, 6],
  ];
  return (
    <svg
      viewBox="0 0 200 200"
      fill="none"
      aria-hidden="true"
      className={cn("text-muted-foreground", className)}
    >
      <g stroke="currentColor" strokeWidth={1}>
        {edges.map(([a, b], i) => (
          <line key={i} x1={nodes[a]!.x} y1={nodes[a]!.y} x2={nodes[b]!.x} y2={nodes[b]!.y} strokeOpacity={0.5} />
        ))}
      </g>
      {nodes.map((n, i) => (
        <g key={i} className={n.bright ? "text-border-strong" : undefined}>
          <circle
            cx={n.x}
            cy={n.y}
            r={n.bright ? 4.5 : 3}
            stroke="currentColor"
            strokeWidth={1}
            fill="currentColor"
            fillOpacity={n.bright ? 0.12 : 0.04}
          />
        </g>
      ))}
    </svg>
  );
}
