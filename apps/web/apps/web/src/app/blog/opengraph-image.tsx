import { ogImage, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const alt = "The CompanyOS blog";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogImage({
    eyebrow: "CompanyOS Blog",
    title: "The CompanyOS blog",
    subtitle: "Product updates and notes on building an agent-native company.",
  });
}
