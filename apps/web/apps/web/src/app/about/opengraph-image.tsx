import { ogImage, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const alt = "CompanyOS — About";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogImage({
    eyebrow: "CompanyOS",
    title: "About CompanyOS",
    subtitle: "An agent-native work platform, open source and self-hostable.",
  });
}
