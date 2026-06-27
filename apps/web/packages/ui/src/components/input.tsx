"use client";

import * as React from "react";
import { cn } from "../lib/cn";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  iconLeft?: React.ReactNode;
  iconRight?: React.ReactNode;
}

const fieldClasses =
  "flex h-9 w-full rounded-md border border-input bg-surface text-small text-foreground shadow-xs transition-[color,border-color,box-shadow] duration-150 placeholder:text-muted-foreground focus-visible:border-ring focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/25 disabled:cursor-not-allowed disabled:opacity-50 aria-invalid:border-danger aria-invalid:focus-visible:border-danger aria-invalid:focus-visible:ring-danger/25";

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = "text", iconLeft, iconRight, "aria-invalid": ariaInvalid, ...props }, ref) => {
    if (iconLeft || iconRight) {
      return (
        <div
          data-invalid={ariaInvalid ? "" : undefined}
          className={cn(
            "flex h-9 w-full items-center gap-2 rounded-md border border-input bg-surface px-3 text-small text-foreground shadow-xs transition-[color,border-color,box-shadow] duration-150 focus-within:border-ring focus-within:ring-2 focus-within:ring-ring/25 data-invalid:border-danger data-invalid:focus-within:ring-danger/25",
            className
          )}
        >
          {iconLeft ? (
            <span className="flex shrink-0 items-center text-muted-foreground [&_svg]:size-4">
              {iconLeft}
            </span>
          ) : null}
          <input
            ref={ref}
            type={type}
            aria-invalid={ariaInvalid}
            className="h-full w-full bg-transparent text-foreground outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50"
            {...props}
          />
          {iconRight ? (
            <span className="flex shrink-0 items-center text-muted-foreground [&_svg]:size-4">
              {iconRight}
            </span>
          ) : null}
        </div>
      );
    }

    return (
      <input
        ref={ref}
        type={type}
        aria-invalid={ariaInvalid}
        className={cn(fieldClasses, "px-3", className)}
        {...props}
      />
    );
  }
);
Input.displayName = "Input";
