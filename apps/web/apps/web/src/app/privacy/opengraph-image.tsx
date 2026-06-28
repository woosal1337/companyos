import { ogImage, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const alt = "CompanyOS — Privacy Policy";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogImage({
    eyebrow: "CompanyOS",
    title: "Privacy Policy",
    subtitle: "Your data stays on your own infrastructure.",
  });
}
