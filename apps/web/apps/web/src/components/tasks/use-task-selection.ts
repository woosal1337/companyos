"use client";

import { useCallback, useMemo, useSyncExternalStore } from "react";

interface SelectionState {
  order: string[];
  focusIndex: number;
  anchorIndex: number;
  selected: ReadonlySet<string>;
}

const EMPTY_SELECTION: ReadonlySet<string> = new Set();

let state: SelectionState = {
  order: [],
  focusIndex: -1,
  anchorIndex: -1,
  selected: EMPTY_SELECTION,
};

const listeners = new Set<() => void>();

function emit() {
  for (const listener of listeners) listener();
}

function setState(next: SelectionState) {
  state = next;
  emit();
}

function clampIndex(index: number, length: number): number {
  if (length === 0) return -1;
  if (index < 0) return 0;
  if (index > length - 1) return length - 1;
  return index;
}

function subscribe(listener: () => void): () => void {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

function getSnapshot(): SelectionState {
  return state;
}

export function setOrder(order: string[]): void {
  const sameOrder =
    order.length === state.order.length && order.every((id, i) => id === state.order[i]);
  const idSet = new Set(order);
  const nextSelected = new Set<string>();
  for (const id of state.selected) {
    if (idSet.has(id)) nextSelected.add(id);
  }
  const focusedId = state.focusIndex >= 0 ? state.order[state.focusIndex] : undefined;
  const nextFocusIndex = focusedId ? order.indexOf(focusedId) : -1;
  const selectionUnchanged = nextSelected.size === state.selected.size;

  if (sameOrder && selectionUnchanged && nextFocusIndex === state.focusIndex) return;

  setState({
    order,
    focusIndex: nextFocusIndex,
    anchorIndex: nextFocusIndex,
    selected: nextSelected.size === 0 ? EMPTY_SELECTION : nextSelected,
  });
}

export function clearAll(): void {
  if (state.focusIndex === -1 && state.selected.size === 0) return;
  setState({ ...state, focusIndex: -1, anchorIndex: -1, selected: EMPTY_SELECTION });
}

export function moveFocus(delta: number): void {
  if (state.order.length === 0) return;
  const base = state.focusIndex === -1 ? (delta > 0 ? -1 : state.order.length) : state.focusIndex;
  const nextIndex = clampIndex(base + delta, state.order.length);
  if (nextIndex === state.focusIndex) return;
  setState({ ...state, focusIndex: nextIndex, anchorIndex: nextIndex });
}

export function focusId(id: string): void {
  const index = state.order.indexOf(id);
  if (index === -1 || index === state.focusIndex) return;
  setState({ ...state, focusIndex: index, anchorIndex: index });
}

function buildRange(order: string[], from: number, to: number): Set<string> {
  const lo = Math.min(from, to);
  const hi = Math.max(from, to);
  const range = new Set<string>();
  for (let i = lo; i <= hi; i += 1) {
    const id = order[i];
    if (id !== undefined) range.add(id);
  }
  return range;
}

export function selectId(id: string): void {
  const index = state.order.indexOf(id);
  if (index === -1) return;
  setState({
    ...state,
    focusIndex: index,
    anchorIndex: index,
    selected: new Set([id]),
  });
}

export function toggleId(id: string): void {
  const index = state.order.indexOf(id);
  if (index === -1) return;
  const next = new Set(state.selected);
  if (next.has(id)) next.delete(id);
  else next.add(id);
  setState({
    ...state,
    focusIndex: index,
    anchorIndex: index,
    selected: next.size === 0 ? EMPTY_SELECTION : next,
  });
}

export function rangeToId(id: string): void {
  const index = state.order.indexOf(id);
  if (index === -1) return;
  const anchor = state.anchorIndex === -1 ? index : state.anchorIndex;
  setState({
    ...state,
    focusIndex: index,
    selected: buildRange(state.order, anchor, index),
  });
}

export function toggleFocused(): void {
  const id = state.focusIndex === -1 ? undefined : state.order[state.focusIndex];
  if (id !== undefined) toggleId(id);
}

export function extendSelection(delta: number): void {
  if (state.order.length === 0) return;
  const anchor = state.anchorIndex === -1 ? state.focusIndex : state.anchorIndex;
  const base = state.focusIndex === -1 ? anchor : state.focusIndex;
  const nextIndex = clampIndex((base === -1 ? 0 : base) + delta, state.order.length);
  const safeAnchor = anchor === -1 ? nextIndex : anchor;
  setState({
    ...state,
    focusIndex: nextIndex,
    anchorIndex: safeAnchor,
    selected: buildRange(state.order, safeAnchor, nextIndex),
  });
}

export function selectAll(): void {
  if (state.order.length === 0) return;
  setState({
    ...state,
    selected: new Set(state.order),
    anchorIndex: state.focusIndex === -1 ? 0 : state.focusIndex,
  });
}

export interface TaskSelection {
  order: string[];
  focusIndex: number;
  focusedId: string | null;
  selected: ReadonlySet<string>;
  selectedIds: string[];
  isSelected: (id: string) => boolean;
  isFocused: (id: string) => boolean;
}

export function useTaskSelection(): TaskSelection {
  const snapshot = useSyncExternalStore(subscribe, getSnapshot, getSnapshot);

  const focusedId = useMemo(
    () => (snapshot.focusIndex >= 0 ? snapshot.order[snapshot.focusIndex] ?? null : null),
    [snapshot.focusIndex, snapshot.order]
  );

  const selectedIds = useMemo(() => Array.from(snapshot.selected), [snapshot.selected]);

  const isSelected = useCallback((id: string) => snapshot.selected.has(id), [snapshot.selected]);

  const isFocused = useCallback((id: string) => focusedId === id, [focusedId]);

  return {
    order: snapshot.order,
    focusIndex: snapshot.focusIndex,
    focusedId,
    selected: snapshot.selected,
    selectedIds,
    isSelected,
    isFocused,
  };
}
