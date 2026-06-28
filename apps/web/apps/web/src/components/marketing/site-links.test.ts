import { test, expect } from "bun:test";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

// Static guard against dead footer / nav links. Walks the real source, so a new
// "#placeholder" or a link to a route with no page.tsx fails the build. No DOM, no network.

const SRC = join(import.meta.dir, "..", ".."); // src/components/marketing -> src
const APP = join(SRC, "app");
const MARKETING = join(SRC, "components", "marketing");

// Anchor ids the landing page actually renders via <Section id="...">.
function landingSectionIds(): Set<string> {
  const ids = new Set<string>();
  for (const file of readdirSync(MARKETING)) {
    if (!file.endsWith(".tsx")) continue;
    const txt = readFileSync(join(MARKETING, file), "utf8");
    for (const m of txt.matchAll(/<Section[^>]*\sid="([a-z0-9-]+)"/g)) ids.add(m[1]);
  }
  return ids;
}

// Internal routes that resolve: a directory with a page.tsx. Route groups "(x)" are
// transparent, dynamic "[x]" and private "_x" segments are skipped.
function internalRoutes(): Set<string> {
  const routes = new Set<string>(["/"]);
  function walk(dir: string, prefix: string) {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const name = entry.name;
      if (name.startsWith("_") || name.startsWith("[")) continue;
      const isGroup = name.startsWith("(") && name.endsWith(")");
      const routePath = isGroup ? prefix : `${prefix}/${name}`;
      const full = join(dir, name);
      if (existsSync(join(full, "page.tsx"))) routes.add(routePath || "/");
      walk(full, routePath);
    }
  }
  walk(APP, "");
  return routes;
}

function hrefsIn(file: string): string[] {
  const txt = readFileSync(join(MARKETING, file), "utf8");
  return [...txt.matchAll(/href:\s*"([^"]+)"/g)].map((m) => m[1]);
}

const SECTION_IDS = landingSectionIds();
const ROUTES = internalRoutes();

function check(href: string) {
  if (/^https?:\/\//.test(href) || href.startsWith("mailto:")) return; // external, fine
  const hash = href.match(/^\/?#(.+)$/);
  if (hash) {
    expect(SECTION_IDS.has(hash[1]), `dead anchor "${href}" (no <Section id="${hash[1]}">)`).toBe(
      true,
    );
    return;
  }
  const path = href.split("#")[0].replace(/\/$/, "") || "/";
  expect(ROUTES.has(path), `link "${href}" points at route "${path}" with no page.tsx`).toBe(true);
}

test("every footer link resolves", () => {
  const hrefs = hrefsIn("site-footer.tsx");
  expect(hrefs.length).toBeGreaterThan(0);
  for (const href of hrefs) check(href);
});

test("every nav link resolves", () => {
  const hrefs = hrefsIn("site-nav.tsx");
  expect(hrefs.length).toBeGreaterThan(0);
  for (const href of hrefs) check(href);
});

test("no bare # placeholder links remain", () => {
  for (const file of ["site-footer.tsx", "site-nav.tsx"]) {
    for (const href of hrefsIn(file)) {
      expect(href, `bare "#" placeholder in ${file}`).not.toBe("#");
    }
  }
});
