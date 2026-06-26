import path from "node:path";
import { fileURLToPath } from "node:url";
import type { NextConfig } from "next";

const dirname = path.dirname(fileURLToPath(import.meta.url));
const backendOrigin = process.env.BACKEND_ORIGIN ?? "http://localhost:8000";

const realtimeUrl =
  process.env.NEXT_PUBLIC_REALTIME_URL ?? backendOrigin.replace(/^http/, "ws");

const nextConfig: NextConfig = {
  output: "standalone",
  outputFileTracingRoot: path.join(dirname, "../.."),
  transpilePackages: ["@companyos/ui"],
  env: {
    NEXT_PUBLIC_REALTIME_URL: realtimeUrl,
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${backendOrigin}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
