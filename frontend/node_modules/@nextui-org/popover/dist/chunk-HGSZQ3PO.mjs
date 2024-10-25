"use client";
import {
  usePopoverContext
} from "./chunk-SQ3I4X62.mjs";

// src/popover-trigger.tsx
import { Children, cloneElement, useMemo } from "react";
import { forwardRef } from "@nextui-org/system";
import { pickChildren } from "@nextui-org/react-utils";
import { useAriaButton } from "@nextui-org/use-aria-button";
import { Button } from "@nextui-org/button";
import { mergeProps } from "@react-aria/utils";
import { jsx } from "react/jsx-runtime";
var PopoverTrigger = forwardRef((props, _) => {
  const { triggerRef, getTriggerProps } = usePopoverContext();
  const { children, ...otherProps } = props;
  const child = useMemo(() => {
    if (typeof children === "string")
      return /* @__PURE__ */ jsx("p", { children });
    return Children.only(children);
  }, [children]);
  const { onPress, isDisabled, ...restProps } = useMemo(() => {
    return getTriggerProps(mergeProps(otherProps, child.props), child.ref);
  }, [getTriggerProps, child.props, otherProps, child.ref]);
  const [, triggerChildren] = pickChildren(children, Button);
  const { buttonProps } = useAriaButton({ onPress, isDisabled }, triggerRef);
  const hasNextUIButton = useMemo(() => {
    return (triggerChildren == null ? void 0 : triggerChildren[0]) !== void 0;
  }, [triggerChildren]);
  return cloneElement(
    child,
    mergeProps(restProps, hasNextUIButton ? { onPress, isDisabled } : buttonProps)
  );
});
PopoverTrigger.displayName = "NextUI.PopoverTrigger";
var popover_trigger_default = PopoverTrigger;

export {
  popover_trigger_default
};
