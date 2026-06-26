export const WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] as const;

const monthFormatter = new Intl.DateTimeFormat("en-US", { month: "long", year: "numeric" });
const dayTimeFormatter = new Intl.DateTimeFormat("en-US", { hour: "numeric", minute: "2-digit" });
const fullDateFormatter = new Intl.DateTimeFormat("en-US", {
  weekday: "long",
  month: "long",
  day: "numeric",
});

export interface CalendarDay {
  date: Date;
  inMonth: boolean;
  isToday: boolean;
  isWeekend: boolean;
}

export function startOfDay(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

export function isSameDay(a: Date, b: Date): boolean {
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  );
}

export function addMonths(date: Date, delta: number): Date {
  return new Date(date.getFullYear(), date.getMonth() + delta, 1);
}

function mondayIndex(date: Date): number {
  return (date.getDay() + 6) % 7;
}

export function monthLabel(month: Date): string {
  return monthFormatter.format(month);
}

export function formatEventTime(iso: string): string {
  return dayTimeFormatter.format(new Date(iso));
}

export function formatEventTimeRange(
  startsISO: string,
  endsISO: string,
  allDay: boolean
): string {
  if (allDay) return "All day";
  return `${formatEventTime(startsISO)} – ${formatEventTime(endsISO)}`;
}

export function formatDayHeading(date: Date): string {
  return fullDateFormatter.format(date);
}

export function buildMonthGrid(month: Date, today: Date): CalendarDay[] {
  const firstOfMonth = new Date(month.getFullYear(), month.getMonth(), 1);
  const gridStart = new Date(firstOfMonth);
  gridStart.setDate(firstOfMonth.getDate() - mondayIndex(firstOfMonth));

  const days: CalendarDay[] = [];
  for (let i = 0; i < 42; i += 1) {
    const date = new Date(gridStart.getFullYear(), gridStart.getMonth(), gridStart.getDate() + i);
    days.push({
      date,
      inMonth: date.getMonth() === month.getMonth(),
      isToday: isSameDay(date, today),
      isWeekend: date.getDay() === 0 || date.getDay() === 6,
    });
  }
  return days;
}

export function monthRange(month: Date): { fromISO: string; toISO: string } {
  const firstOfMonth = new Date(month.getFullYear(), month.getMonth(), 1);
  const from = new Date(firstOfMonth);
  from.setDate(firstOfMonth.getDate() - mondayIndex(firstOfMonth));
  const to = new Date(from.getFullYear(), from.getMonth(), from.getDate() + 42);
  return { fromISO: from.toISOString(), toISO: to.toISOString() };
}

export function toDateInputValue(date: Date): string {
  const year = String(date.getFullYear()).padStart(4, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function toTimeInputValue(date: Date): string {
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  return `${hours}:${minutes}`;
}

export function combineDateTime(dateValue: string, timeValue: string): Date {
  const [year = 1970, month = 1, day = 1] = dateValue.split("-").map(Number);
  const [hours = 0, minutes = 0] = timeValue.split(":").map(Number);
  return new Date(year, month - 1, day, hours, minutes, 0, 0);
}

export function eventsForDay<T extends { starts_at: string }>(events: T[], day: Date): T[] {
  return events
    .filter((event) => isSameDay(new Date(event.starts_at), day))
    .sort((a, b) => new Date(a.starts_at).getTime() - new Date(b.starts_at).getTime());
}
