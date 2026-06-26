"use client";

import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { KeyboardProvider } from "@/lib/keyboard";
import { CommandPalette } from "./command-palette";
import { CommandRegistryProvider } from "./command-registry";
import { NavigationChords } from "./navigation-chords";
import { ShortcutHelp } from "./shortcut-help";

interface CommandMenuContextValue {
  open: () => void;
  close: () => void;
  toggle: () => void;
  isOpen: boolean;
}

const CommandMenuContext = createContext<CommandMenuContextValue | null>(null);

export function CommandMenuProvider({
  orgId,
  children,
}: {
  orgId: string;
  children: ReactNode;
}) {
  const [isOpen, setIsOpen] = useState(false);

  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);
  const toggle = useCallback(() => setIsOpen((value) => !value), []);

  const value = useMemo<CommandMenuContextValue>(
    () => ({ open, close, toggle, isOpen }),
    [open, close, toggle, isOpen]
  );

  return (
    <KeyboardProvider>
      <CommandRegistryProvider>
        <CommandMenuContext.Provider value={value}>
          {children}
          <NavigationChords orgId={orgId} />
          <ShortcutHelp />
          <CommandPalette orgId={orgId} open={isOpen} onOpenChange={setIsOpen} />
        </CommandMenuContext.Provider>
      </CommandRegistryProvider>
    </KeyboardProvider>
  );
}

export function useCommandMenu(): CommandMenuContextValue {
  const context = useContext(CommandMenuContext);
  if (!context) {
    throw new Error("useCommandMenu must be used within a CommandMenuProvider");
  }
  return context;
}
