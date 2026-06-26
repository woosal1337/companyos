"use client";

import * as React from "react";
import { CalendarDays, ChevronLeft, ChevronRight } from "lucide-react";
import { cn } from "../lib/cn";
import { Popover, PopoverContent, PopoverTrigger } from "./popover";

const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
const MONTHS_SHORT = MONTHS.map((m) => m.slice(0, 3));
const WEEKDAYS = ["M", "T", "W", "T", "F", "S", "S"];

function pad(value: number): string {
  return value < 10 ? `0${value}` : `${value}`;
}

function toISO(date: Date): string {
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

function parseISO(value: string): Date | null {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) return null;
  const [, y, m, d] = match;
  return new Date(Number(y), Number(m) - 1, Number(d));
}

function formatDisplay(date: Date): string {
  return `${MONTHS_SHORT[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
}

function sameDay(a: Date, b: Date): boolean {
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  );
}

export interface DatePickerProps {
  value?: string | null;
  onChange: (value: string | null) => void;
  placeholder?: string;
  disabled?: boolean;
  clearable?: boolean;
  id?: string;
  className?: string;
  align?: "start" | "center" | "end";
  "aria-label"?: string;
}

export function DatePicker({
  value,
  onChange,
  placeholder = "Select date",
  disabled = false,
  clearable = true,
  id,
  className,
  align = "start",
  "aria-label": ariaLabel,
}: DatePickerProps) {
  const selected = value ? parseISO(value) : null;
  const [open, setOpen] = React.useState(false);
  const [view, setView] = React.useState(() => {
    const base = selected ?? new Date();
    return { year: base.getFullYear(), month: base.getMonth() };
  });

  React.useEffect(() => {
    if (open && selected) {
      setView({ year: selected.getFullYear(), month: selected.getMonth() });
    }
  }, [open]); // eslint-disable-line react-hooks/exhaustive-deps

  const today = new Date();
  const firstOfMonth = new Date(view.year, view.month, 1);
  const startOffset = (firstOfMonth.getDay() + 6) % 7;
  const gridStart = new Date(view.year, view.month, 1 - startOffset);
  const days = Array.from({ length: 42 }, (_, i) =>
    new Date(gridStart.getFullYear(), gridStart.getMonth(), gridStart.getDate() + i)
  );

  const shiftMonth = (delta: number) => {
    setView((current) => {
      const next = new Date(current.year, current.month + delta, 1);
      return { year: next.getFullYear(), month: next.getMonth() };
    });
  };

  const pick = (date: Date) => {
    onChange(toISO(date));
    setOpen(false);
  };

  return (
    <Popover open={open} onOpenChange={disabled ? undefined : setOpen}>
      <PopoverTrigger
        id={id}
        type="button"
        disabled={disabled}
        aria-label={ariaLabel ?? placeholder}
        className={cn(
          "flex h-9 w-full items-center gap-2 rounded-md border border-input bg-surface px-3 text-small shadow-xs transition-[color,border-color,box-shadow] duration-150 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/25 disabled:cursor-not-allowed disabled:opacity-50",
          selected ? "text-foreground" : "text-muted-foreground",
          className
        )}
      >
        <CalendarDays className="size-4 shrink-0 text-muted-foreground" />
        <span className="flex-1 truncate text-left">
          {selected ? formatDisplay(selected) : placeholder}
        </span>
      </PopoverTrigger>
      <PopoverContent align={align} className="w-[17rem] p-3">
        <div className="mb-2 flex items-center justify-between">
          <span className="text-small font-semibold text-foreground">
            {MONTHS[view.month]} {view.year}
          </span>
          <div className="flex items-center gap-1">
            <button
              type="button"
              aria-label="Previous month"
              onClick={() => shiftMonth(-1)}
              className="inline-flex size-7 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/30"
            >
              <ChevronLeft className="size-4" />
            </button>
            <button
              type="button"
              aria-label="Next month"
              onClick={() => shiftMonth(1)}
              className="inline-flex size-7 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/30"
            >
              <ChevronRight className="size-4" />
            </button>
          </div>
        </div>

        <div className="grid grid-cols-7 gap-0.5">
          {WEEKDAYS.map((label, index) => (
            <div
              key={index}
              className="flex h-7 items-center justify-center text-caption font-medium text-muted-foreground"
            >
              {label}
            </div>
          ))}
          {days.map((day) => {
            const inMonth = day.getMonth() === view.month;
            const isSelected = selected ? sameDay(day, selected) : false;
            const isToday = sameDay(day, today);
            return (
              <button
                key={toISO(day)}
                type="button"
                onClick={() => pick(day)}
                className={cn(
                  "flex h-8 items-center justify-center rounded-md text-small tabular transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/30",
                  isSelected
                    ? "bg-accent font-semibold text-accent-foreground"
                    : inMonth
                      ? "text-foreground hover:bg-muted"
                      : "text-muted-foreground/40 hover:bg-muted",
                  !isSelected && isToday ? "ring-1 ring-inset ring-accent/50" : null
                )}
              >
                {day.getDate()}
              </button>
            );
          })}
        </div>

        <div className="mt-2 flex items-center justify-between border-t border-border pt-2">
          {clearable ? (
            <button
              type="button"
              onClick={() => {
                onChange(null);
                setOpen(false);
              }}
              className="text-caption font-medium text-muted-foreground transition-colors hover:text-foreground"
            >
              Clear
            </button>
          ) : (
            <span />
          )}
          <button
            type="button"
            onClick={() => pick(new Date())}
            className="text-caption font-medium text-accent transition-colors hover:underline"
          >
            Today
          </button>
        </div>
      </PopoverContent>
    </Popover>
  );
}
