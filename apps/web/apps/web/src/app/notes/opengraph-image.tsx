import { ogImage, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const alt = "CompanyOS — Notes & wiki";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogImage({
    eyebrow: "CompanyOS",
    title: "Notes & wiki",
    subtitle: "Live, conflict-free co-editing on Yjs.",
  });
}
