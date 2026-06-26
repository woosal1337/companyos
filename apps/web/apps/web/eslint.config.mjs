import { nextJsConfig } from "@companyos/eslint-config/next-js";

export default [...nextJsConfig, { ignores: ["**/*.test.ts", "**/*.test.tsx"] }];
