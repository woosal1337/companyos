"use client";

import { createContext, useCallback, useContext, useMemo, useState } from "react";

interface AnchorContextValue {
  activeSegmentId: string | null;
  requestSegment: (segmentId: string) => void;
  acknowledge: () => void;
}

const AnchorContext = createContext<AnchorContextValue | null>(null);

export function AnchorProvider({
  children,
  onRequest,
}: {
  children: React.ReactNode;
  onRequest?: (segmentId: string) => void;
}) {
  const [activeSegmentId, setActiveSegmentId] = useState<string | null>(null);

  const requestSegment = useCallback(
    (segmentId: string) => {
      setActiveSegmentId(segmentId);
      onRequest?.(segmentId);
    },
    [onRequest]
  );

  const acknowledge = useCallback(() => setActiveSegmentId(null), []);

  const value = useMemo<AnchorContextValue>(
    () => ({ activeSegmentId, requestSegment, acknowledge }),
    [activeSegmentId, requestSegment, acknowledge]
  );

  return <AnchorContext.Provider value={value}>{children}</AnchorContext.Provider>;
}

export function useAnchor(): AnchorContextValue {
  const context = useContext(AnchorContext);
  if (!context) {
    return { activeSegmentId: null, requestSegment: () => {}, acknowledge: () => {} };
  }
  return context;
}
