"use client";

import { Toaster as SonnerToaster, type ToasterProps } from "sonner";

export { toast } from "sonner";

export function Toaster(props: ToasterProps) {
  return (
    <SonnerToaster
      position="bottom-right"
      gap={8}
      toastOptions={{
        classNames: {
          toast:
            "!rounded-md !border !border-border !bg-surface !text-surface-foreground !shadow-lg !text-small",
          title: "!font-medium",
          description: "!text-muted-foreground",
          actionButton: "!bg-accent !text-accent-foreground",
          cancelButton: "!bg-subtle !text-muted-foreground",
        },
      }}
      {...props}
    />
  );
}
