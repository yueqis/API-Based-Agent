"use client";
import {
  useDropdownContext
} from "./chunk-WRRPXIUB.mjs";

// src/dropdown-trigger.tsx
import { forwardRef } from "@nextui-org/system";
import { PopoverTrigger } from "@nextui-org/popover";
import { jsx } from "react/jsx-runtime";
var DropdownTrigger = forwardRef((props, _) => {
  const { getMenuTriggerProps } = useDropdownContext();
  const { children, ...otherProps } = props;
  return /* @__PURE__ */ jsx(PopoverTrigger, { ...getMenuTriggerProps(otherProps), children });
});
DropdownTrigger.displayName = "NextUI.DropdownTrigger";
var dropdown_trigger_default = DropdownTrigger;

export {
  dropdown_trigger_default
};
