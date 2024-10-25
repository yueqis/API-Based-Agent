"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/index.ts
var src_exports = {};
__export(src_exports, {
  useAriaToggleButton: () => useAriaToggleButton
});
module.exports = __toCommonJS(src_exports);
var import_utils = require("@react-aria/utils");
var import_utils2 = require("@react-aria/utils");
var import_use_aria_button = require("@nextui-org/use-aria-button");
function useAriaToggleButton(props, state, ref) {
  const { isSelected } = state;
  const { isPressed, buttonProps } = (0, import_use_aria_button.useAriaButton)(
    {
      ...props,
      onPress: (0, import_utils.chain)(state.toggle, props.onPress)
    },
    ref
  );
  return {
    isPressed,
    buttonProps: (0, import_utils2.mergeProps)(buttonProps, {
      "aria-pressed": isSelected
    })
  };
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  useAriaToggleButton
});
