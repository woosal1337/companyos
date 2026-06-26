"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useId,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import type { LucideIcon } from "lucide-react";

export interface RegisteredCommand {
  id: string;
  label: string;
  keywords?: string[];
  icon: LucideIcon;
  hint?: string;
  perform: () => void;
}

export interface CommandScope {
  id: string;
  heading: string;
  commands: RegisteredCommand[];
}

interface RegistryContextValue {
  scopes: CommandScope[];
  register: (entry: CommandScope) => void;
  unregister: (sourceId: string) => void;
}

const CommandRegistryContext = createContext<RegistryContextValue | null>(null);

export function CommandRegistryProvider({ children }: { children: ReactNode }) {
  const [entries, setEntries] = useState<Map<string, CommandScope>>(() => new Map());

  const register = useCallback((entry: CommandScope) => {
    setEntries((prev) => {
      const next = new Map(prev);
      next.set(entry.id, entry);
      return next;
    });
  }, []);

  const unregister = useCallback((sourceId: string) => {
    setEntries((prev) => {
      if (!prev.has(sourceId)) return prev;
      const next = new Map(prev);
      next.delete(sourceId);
      return next;
    });
  }, []);

  const scopes = useMemo(() => Array.from(entries.values()), [entries]);

  const value = useMemo<RegistryContextValue>(
    () => ({ scopes, register, unregister }),
    [scopes, register, unregister]
  );

  return (
    <CommandRegistryContext.Provider value={value}>{children}</CommandRegistryContext.Provider>
  );
}

export function useCommandScopes(): CommandScope[] {
  const context = useContext(CommandRegistryContext);
  return context?.scopes ?? [];
}

export function useRegisterCommands(
  scope: { heading: string; active?: boolean },
  commands: RegisteredCommand[]
): void {
  const context = useContext(CommandRegistryContext);
  const sourceId = useId();
  const active = scope.active ?? true;
  const heading = scope.heading;

  const commandsRef = useRef(commands);
  commandsRef.current = commands;

  if (!context) {
    throw new Error("useRegisterCommands must be used within a CommandMenuProvider");
  }
  const { register, unregister } = context;

  useEffect(() => {
    if (!active) {
      unregister(sourceId);
      return;
    }
    register({ id: sourceId, heading, commands: commandsRef.current });
    return () => unregister(sourceId);
  }, [active, heading, register, unregister, sourceId, commands]);
}
