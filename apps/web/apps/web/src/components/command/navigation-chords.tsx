"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { useShortcut } from "@/lib/keyboard";
import { EntityPicker, type EntityKind } from "./entity-picker";

interface PickerState {
  open: boolean;
  kind: EntityKind;
}

export function NavigationChords({ orgId }: { orgId: string }) {
  const router = useRouter();
  const [picker, setPicker] = useState<PickerState>({ open: false, kind: "project" });

  const openPicker = useCallback((kind: EntityKind) => {
    setPicker({ open: true, kind });
  }, []);

  const setPickerOpen = useCallback((open: boolean) => {
    setPicker((prev) => ({ ...prev, open }));
  }, []);

  useShortcut(
    { id: "chord-open-project", keys: "o p", label: "Open project…", scope: "navigation" },
    () => openPicker("project")
  );

  useShortcut(
    { id: "chord-open-team", keys: "o t", label: "Open team…", scope: "navigation" },
    () => openPicker("team")
  );

  useShortcut(
    { id: "chord-open-profile", keys: "o m", label: "Open my profile", scope: "navigation" },
    () => router.push(`/app/${orgId}/settings`)
  );

  return (
    <EntityPicker
      orgId={orgId}
      kind={picker.kind}
      open={picker.open}
      onOpenChange={setPickerOpen}
    />
  );
}
