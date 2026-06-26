import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../lib/cn";

const containerVariants = cva("mx-auto w-full px-6", {
  variants: {
    size: {
      sm: "max-w-3xl",
      md: "max-w-5xl",
      lg: "max-w-[1200px]",
      full: "max-w-none",
    },
  },
  defaultVariants: {
    size: "lg",
  },
});

export interface ContainerProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof containerVariants> {
  as?: React.ElementType;
}

export const Container = React.forwardRef<HTMLDivElement, ContainerProps>(
  ({ className, size, as, ...props }, ref) => {
    const Comp = (as ?? "div") as React.ElementType;
    return <Comp ref={ref} className={cn(containerVariants({ size }), className)} {...props} />;
  }
);
Container.displayName = "Container";
