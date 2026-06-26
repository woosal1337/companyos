import { describe, expect, it } from "bun:test";
import { readFileSync } from "node:fs";
import { join } from "node:path";

const css = readFileSync(join(import.meta.dir, "styles.css"), "utf8");

function block(selector: string): string {
  const start = css.indexOf(selector + " {");
  if (start === -1) throw new Error(`missing block ${selector}`);
  const open = css.indexOf("{", start);
  const end = css.indexOf("\n}", open);
  return css.slice(open + 1, end);
}

describe("DS-01 three-input theme", () => {
  for (const selector of [":root", ".light"]) {
    describe(selector, () => {
      const body = block(selector);

      it("declares exactly the three source inputs", () => {
        expect(body).toContain("--theme-base:");
        expect(body).toContain("--theme-accent:");
        expect(body).toContain("--theme-contrast:");
      });

      it("derives the accent family from --theme-accent in one place", () => {
        for (const token of ["--accent:", "--accent-foreground:", "--accent-muted:", "--accent-subtle:", "--ring:"]) {
          const line = body.split("\n").find((l) => l.trim().startsWith(token));
          expect(line).toBeDefined();
          expect(line).toContain("var(--theme-accent)");
        }
      });

      it("scales structure tokens by --theme-contrast", () => {
        for (const token of ["--muted-foreground:", "--border:", "--border-strong:", "--input:"]) {
          const line = body.split("\n").find((l) => l.trim().startsWith(token));
          expect(line).toBeDefined();
          expect(line).toContain("var(--theme-contrast)");
        }
      });

      it("computes neutral surfaces from --theme-base rather than hand-tuned literals", () => {
        for (const token of ["--background:", "--muted:", "--foreground:"]) {
          const line = body.split("\n").find((l) => l.trim().startsWith(token));
          expect(line).toBeDefined();
          expect(line).toContain("var(--theme-base)");
        }
      });
    });
  }
});
