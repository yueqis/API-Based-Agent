"use client";
import {
  useCheckboxGroup
} from "./chunk-EVFZI3P4.mjs";
import {
  CheckboxGroupProvider
} from "./chunk-ACAJT7GC.mjs";

// src/checkbox-group.tsx
import { forwardRef } from "@nextui-org/system";
import { useMemo } from "react";
import { jsx, jsxs } from "react/jsx-runtime";
var CheckboxGroup = forwardRef((props, ref) => {
  const {
    children,
    context,
    label,
    description,
    isInvalid,
    errorMessage,
    getGroupProps,
    getLabelProps,
    getWrapperProps,
    getDescriptionProps,
    getErrorMessageProps
  } = useCheckboxGroup({ ...props, ref });
  const errorMessageContent = useMemo(() => errorMessage, [isInvalid]);
  return /* @__PURE__ */ jsxs("div", { ...getGroupProps(), children: [
    label && /* @__PURE__ */ jsx("span", { ...getLabelProps(), children: label }),
    /* @__PURE__ */ jsx("div", { ...getWrapperProps(), children: /* @__PURE__ */ jsx(CheckboxGroupProvider, { value: context, children }) }),
    isInvalid && errorMessageContent ? /* @__PURE__ */ jsx("div", { ...getErrorMessageProps(), children: errorMessageContent }) : description ? /* @__PURE__ */ jsx("div", { ...getDescriptionProps(), children: description }) : null
  ] });
});
CheckboxGroup.displayName = "NextUI.CheckboxGroup";
var checkbox_group_default = CheckboxGroup;

export {
  checkbox_group_default
};
