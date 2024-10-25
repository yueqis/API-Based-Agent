import {
  colorVariants
} from "./chunk-2PIR7DFM.mjs";
import {
  tv
} from "./chunk-N2KXC5ZE.mjs";

// src/components/code.ts
var code = tv({
  base: ["px-2", "py-1", "h-fit", "font-mono", "font-normal", "inline-block", "whitespace-nowrap"],
  variants: {
    color: {
      default: colorVariants.flat.default,
      primary: colorVariants.flat.primary,
      secondary: colorVariants.flat.secondary,
      success: colorVariants.flat.success,
      warning: colorVariants.flat.warning,
      danger: colorVariants.flat.danger
    },
    size: {
      sm: "text-small",
      md: "text-medium",
      lg: "text-large"
    },
    radius: {
      none: "rounded-none",
      sm: "rounded-small",
      md: "rounded-medium",
      lg: "rounded-large",
      full: "rounded-full"
    }
  },
  defaultVariants: {
    color: "default",
    size: "sm",
    radius: "sm"
  }
});

export {
  code
};
