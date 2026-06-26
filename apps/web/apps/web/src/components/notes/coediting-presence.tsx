"use client";

import { useEffect, useState } from "react";
import { Users } from "lucide-react";
import type { WebsocketProvider } from "y-websocket";

interface Peer {
  clientId: number;
  name: string;
  color: string;
}

export function CoeditingPresence({ provider }: { provider: WebsocketProvider }) {
  const [peers, setPeers] = useState<Peer[]>([]);
  const [connected, setConnected] = useState(false);
  const [stalled, setStalled] = useState(false);

  useEffect(() => {
    const { awareness } = provider;
    const update = () => {
      const out: Peer[] = [];
      awareness.getStates().forEach((state, clientId) => {
        if (clientId === awareness.clientID) return;
        const user = (state as { user?: { name: string; color: string } }).user;
        if (user) out.push({ clientId, name: user.name, color: user.color });
      });
      setPeers(out);
    };
    let stallTimer: ReturnType<typeof setTimeout> | undefined;
    const armStall = () => {
      clearTimeout(stallTimer);
      stallTimer = setTimeout(() => setStalled(true), 8000);
    };
    const onStatus = (event: { status: string }) => {
      const isConnected = event.status === "connected";
      setConnected(isConnected);
      if (isConnected) {
        setStalled(false);
        clearTimeout(stallTimer);
      } else {
        armStall();
      }
    };
    awareness.on("change", update);
    provider.on("status", onStatus);
    update();
    armStall();
    return () => {
      awareness.off("change", update);
      provider.off("status", onStatus);
      clearTimeout(stallTimer);
    };
  }, [provider]);

  const label = connected ? "Live" : stalled ? "Offline" : "Connecting…";

  return (
    <div
      className="flex items-center gap-1.5 text-caption text-muted-foreground"
      title={stalled && !connected ? "Realtime unavailable — your changes still save" : "Live editing"}
    >
      <Users className="size-3.5" />
      <span className={connected ? "text-success" : stalled ? "text-muted-foreground/60" : ""}>
        {label}
      </span>
      {peers.length > 0 ? (
        <div className="flex -space-x-1.5">
          {peers.slice(0, 5).map((peer) => (
            <span
              key={peer.clientId}
              className="flex size-5 items-center justify-center rounded-full border border-surface text-[10px] font-semibold text-white"
              style={{ backgroundColor: peer.color }}
              title={peer.name}
            >
              {peer.name.charAt(0).toUpperCase()}
            </span>
          ))}
          {peers.length > 5 ? <span className="pl-2">+{peers.length - 5}</span> : null}
        </div>
      ) : null}
    </div>
  );
}
