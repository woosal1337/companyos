import globals from "globals";
import pluginReact from "eslint-plugin-react";
import pluginReactHooks from "eslint-plugin-react-hooks";
import tseslint from "typescript-eslint";
import { baseConfig } from "./base.js";

export const reactInternalConfig = tseslint.config(
  baseConfig,
  pluginReact.configs.flat.recommended,
  {
    languageOptions: {
      globals: { ...globals.browser },
    },
    plugins: {
      "react-hooks": pluginReactHooks,
    },
    settings: {
      react: { version: "detect" },
    },
    rules: {
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "error",
      "react/react-in-jsx-scope": "off",
      "react/prop-types": "off",
    },
  }
);
