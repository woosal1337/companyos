"use client";

import { useMemo } from "react";
import { useRouter } from "next/navigation";
import { Settings2 } from "lucide-react";
import { useRegisterCommands, type RegisteredCommand } from "./command-registry";
import { SETTINGS_SECTIONS, settingsSectionPath } from "@/lib/settings-sections";

export function SettingsCommands({ orgId }: { orgId: string }) {
  const router = useRouter();

  const commands = useMemo<RegisteredCommand[]>(
    () =>
      SETTINGS_SECTIONS.map((section) => ({
        id: `settings-${section.value}`,
        label: `Settings: ${section.label}`,
        keywords: ["settings", section.label, ...section.keywords],
        icon: Settings2,
        perform: () => router.push(settingsSectionPath(orgId, section.value)),
      })),
    [orgId, router]
  );

  useRegisterCommands({ heading: "Settings" }, commands);
  return null;
}
