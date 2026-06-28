import { ogImage, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const alt = "CompanyOS — Changelog";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogImage({
    eyebrow: "CompanyOS",
    title: "Changelog",
    subtitle: "Notable changes to CompanyOS, newest first.",
  });
}
