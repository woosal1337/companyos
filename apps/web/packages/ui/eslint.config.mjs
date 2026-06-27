import { reactInternalConfig } from "@companyos/eslint-config/react-internal";

export default [...reactInternalConfig, { ignores: ["**/*.test.ts", "**/*.test.tsx"] }];
