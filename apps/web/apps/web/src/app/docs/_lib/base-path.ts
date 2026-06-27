import { headers } from "next/headers";

export async function getDocsBasePath(): Promise<string> {
  const host = (await headers()).get("host") ?? "";
  const hostname = host.split(":")[0] ?? "";
  return hostname.startsWith("docs.") ? "" : "/docs";
}
