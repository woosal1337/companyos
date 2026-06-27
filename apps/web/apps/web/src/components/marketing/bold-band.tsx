import { BoldQuote, Container, Section, SectionNumber } from "@companyos/ui";

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
            <BoldQuote
              tone="lavender"
              quote="Our agents pick up tasks off the same board we do. The meeting, the task, and the owner live in one place, and nothing slips between standups."
              name="Mara Velasquez"
              role="Head of Operations, Northwind"
            />
            <BoldQuote
              tone="acid"
              quote="Our own keys, our own data, one model of the company. I wired our agents into CompanyOS over MCP in an afternoon and it has held up under real load since."
              name="Daniel Okoye"
              role="Founding Engineer, Vertex"
            />
          </div>
        </div>
      </Container>
    </Section>
  );
}
