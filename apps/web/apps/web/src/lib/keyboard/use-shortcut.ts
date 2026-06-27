"use client";

import { useEffect, useRef } from "react";
import { useKeyboard } from "./keyboard-provider";
import type { ShortcutScope } from "./types";

export interface UseShortcutOptions {
  id: string;
  keys: string;
  label: string;
  scope: ShortcutScope;
  enabled?: boolean;
}

export function useShortcut(options: UseShortcutOptions, run: () => void): void {
  const { register } = useKeyboard();
  const runRef = useRef(run);
  runRef.current = run;

  const { id, keys, label, scope, enabled = true } = options;

  useEffect(() => {
    return register({
      id,
      keys,
      label,
      scope,
      enabled,
      run: () => runRef.current(),
    });
  }, [register, id, keys, label, scope, enabled]);
}
