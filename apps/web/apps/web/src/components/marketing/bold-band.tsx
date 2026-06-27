import { Container, Section, SectionNumber } from "@companyos/ui";

const METRICS = [
  { value: "1", label: "system of record for projects, meetings, and tasks" },
  { value: "BYOK", label: "every AI call runs on your own model key" },
  { value: "0", label: "data leaves your org beyond that key" },
];

export function BoldBand() {
  return (
    <Section id="customers" spacing="xl" className="bg-canvas" reveal>
      <Container>
        <div className="flex flex-col gap-10">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <SectionNumber index="2.0" label="In practice" />
            <p className="max-w-xs text-small text-muted-foreground">
              Teams and their agents run the week inside CompanyOS.
            </p>
          </div>
          <dl className="grid gap-px overflow-hidden rounded-xl border border-border bg-border sm:grid-cols-3">
            {METRICS.map((metric) => (
              <div key={metric.value} className="flex flex-col gap-2 bg-canvas p-6">
                <dt className="font-display text-display text-foreground tabular">{metric.value}</dt>
                <dd className="text-small text-muted-foreground">{metric.label}</dd>
              </div>
            ))}
          </dl>
          <div className="grid gap-6 lg:grid-cols-2">
            <div className="flex min-h-80 flex-col justify-between gap-12 rounded-2xl bg-lavender p-10 text-lavender-foreground sm:p-14">
              <p className="font-display text-h2 tracking-tight">
                Agents are members, not a chatbot. They run the same board, tasks, and meetings your team does, over a built-in MCP server. Bidirectional, and scoped to your org.
              </p>
              <p className="font-mono text-mono-label uppercase tracking-wide opacity-70">
                Agent-native MCP
              </p>
            </div>
            <div className="flex min-h-80 flex-col justify-between gap-12 rounded-2xl bg-bold p-10 text-bold-foreground sm:p-14">
              <p className="font-display text-h2 tracking-tight">
                Bring your own model key. Every AI call runs on it and lands in an audit log, and your data stays on your own infrastructure. Open source, and self-hosted.
              </p>
              <p className="font-mono text-mono-label uppercase tracking-wide opacity-70">
                Your keys, your data
              </p>
            </div>
          </div>
        </div>
      </Container>
    </Section>
  );
}
