import { readFileSync } from "node:fs";
import { join } from "node:path";
import { ImageResponse } from "next/og";

export const OG_SIZE = { width: 1200, height: 630 };
export const OG_CONTENT_TYPE = "image/png";

// Read the brand mark once and inline it as a data URI — Satori cannot resolve a runtime URL.
const LOGO_DATA_URI = `data:image/png;base64,${readFileSync(
  join(process.cwd(), "public", "logo.png"),
).toString("base64")}`;

interface OgInput {
  eyebrow: string;
  title: string;
  subtitle?: string;
}

// Shared brand layout for every generated social-preview image. Only the text changes per page.
export function ogImage({ eyebrow, title, subtitle }: OgInput) {
  return new ImageResponse(
    (
      <div
        style={{
          height: "100%",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          background: "#0A0A0B",
          padding: "80px",
          fontFamily: "sans-serif",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "20px" }}>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={LOGO_DATA_URI} width={60} height={60} alt="" />
          <div style={{ fontSize: "34px", color: "#9CA3AF", fontWeight: 600 }}>{eyebrow}</div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: "22px" }}>
          <div
            style={{ display: "flex", fontSize: "76px", color: "#FFFFFF", fontWeight: 700, lineHeight: 1.08 }}
          >
            {title}
          </div>
          {subtitle ? (
            <div style={{ display: "flex", fontSize: "32px", color: "#9CA3AF", lineHeight: 1.3 }}>
              {subtitle}
            </div>
          ) : null}
        </div>
      </div>
    ),
    { ...OG_SIZE },
  );
}
