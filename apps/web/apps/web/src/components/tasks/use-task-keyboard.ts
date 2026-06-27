"use client";

import { useEffect } from "react";
import { useShortcut } from "@/lib/keyboard";
import {
  clearAll,
  extendSelection,
  moveFocus,
  selectAll,
  setOrder,
  toggleFocused,
  useTaskSelection,
} from "./use-task-selection";

export type FocusedAction = "status" | "priority" | "assignee" | "assign-me" | "rename" | "create";

export interface TaskKeyboardHandlers {
  onOpen: (taskId: string) => void;
  onPeek: (taskId: string) => void;
  onAction: (action: FocusedAction, focusedId: string | null, selectedIds: string[]) => void;
  peekOpen: boolean;
}

export function useTaskKeyboard(
  order: string[],
  enabled: boolean,
  handlers: TaskKeyboardHandlers
) {
  const selection = useTaskSelection();

  useEffect(() => {
    if (!enabled) return;
    setOrder(order);
  }, [order, enabled]);

  useEffect(() => {
    return () => clearAll();
  }, []);

  const focusedId = selection.focusedId;

  useEffect(() => {
    if (!focusedId) return;
    const element = document.querySelector<HTMLElement>(`[data-task-item="${focusedId}"]`);
    element?.scrollIntoView({ block: "nearest", inline: "nearest" });
  }, [focusedId]);

  const { onOpen, onPeek, onAction, peekOpen } = handlers;

  useShortcut(
    { id: "tasks-focus-next", keys: "arrowdown", label: "Focus next task", scope: "navigation", enabled },
    () => moveFocus(1)
  );
  useShortcut(
    { id: "tasks-focus-prev", keys: "arrowup", label: "Focus previous task", scope: "navigation", enabled },
    () => moveFocus(-1)
  );
  useShortcut(
    { id: "tasks-focus-left", keys: "arrowleft", label: "Focus previous task", scope: "navigation", enabled },
    () => moveFocus(-1)
  );
  useShortcut(
    { id: "tasks-focus-right", keys: "arrowright", label: "Focus next task", scope: "navigation", enabled },
    () => moveFocus(1)
  );

  useShortcut(
    {
      id: "tasks-extend-down",
      keys: "shift+arrowdown",
      label: "Extend selection down",
      scope: "navigation",
      enabled,
    },
    () => extendSelection(1)
  );
  useShortcut(
    {
      id: "tasks-extend-up",
      keys: "shift+arrowup",
      label: "Extend selection up",
      scope: "navigation",
      enabled,
    },
    () => extendSelection(-1)
  );

  useShortcut(
    { id: "tasks-select-all", keys: "mod+a", label: "Select all tasks", scope: "action", enabled },
    () => selectAll()
  );

  useShortcut(
    {
      id: "tasks-toggle-select",
      keys: "x",
      label: "Toggle task selection",
      scope: "action",
      enabled: enabled && focusedId !== null,
    },
    () => toggleFocused()
  );

  useShortcut(
    {
      id: "tasks-clear",
      keys: "escape",
      label: "Clear selection",
      scope: "action",
      enabled: enabled && (focusedId !== null || selection.selected.size > 0 || peekOpen),
    },
    () => clearAll()
  );

  useShortcut(
    {
      id: "tasks-open",
      keys: "enter",
      label: "Open focused task",
      scope: "action",
      enabled: enabled && focusedId !== null,
    },
    () => {
      if (focusedId) onOpen(focusedId);
    }
  );

  useShortcut(
    {
      id: "tasks-peek",
      keys: "space",
      label: "Peek focused task",
      scope: "action",
      enabled: enabled && focusedId !== null,
    },
    () => {
      if (focusedId) onPeek(focusedId);
    }
  );

  useShortcut(
    {
      id: "tasks-action-status",
      keys: "s",
      label: "Set status",
      scope: "action",
      enabled: enabled && (focusedId !== null || selection.selected.size > 0),
    },
    () => onAction("status", focusedId, selection.selectedIds)
  );
  useShortcut(
    {
      id: "tasks-action-priority",
      keys: "p",
      label: "Set priority",
      scope: "action",
      enabled: enabled && (focusedId !== null || selection.selected.size > 0),
    },
    () => onAction("priority", focusedId, selection.selectedIds)
  );
  useShortcut(
    {
      id: "tasks-action-assignee",
      keys: "a",
      label: "Assign",
      scope: "action",
      enabled: enabled && (focusedId !== null || selection.selected.size > 0),
    },
    () => onAction("assignee", focusedId, selection.selectedIds)
  );
  useShortcut(
    {
      id: "tasks-action-assign-me",
      keys: "i",
      label: "Assign to me",
      scope: "action",
      enabled: enabled && (focusedId !== null || selection.selected.size > 0),
    },
    () => onAction("assign-me", focusedId, selection.selectedIds)
  );
  useShortcut(
    {
      id: "tasks-action-rename",
      keys: "r",
      label: "Rename task",
      scope: "action",
      enabled: enabled && focusedId !== null,
    },
    () => onAction("rename", focusedId, selection.selectedIds)
  );

  return selection;
}
