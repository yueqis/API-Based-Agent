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

// src/use-menu.ts
var use_menu_exports = {};
__export(use_menu_exports, {
  menuData: () => menuData,
  useMenu: () => useMenu
});
module.exports = __toCommonJS(use_menu_exports);
var import_utils = require("@react-aria/utils");
var import_selection = require("@react-aria/selection");
var menuData = /* @__PURE__ */ new WeakMap();
function useMenu(props, state, ref) {
  let { shouldFocusWrap = true, onKeyDown, onKeyUp, ...otherProps } = props;
  if (!props["aria-label"] && !props["aria-labelledby"]) {
    console.warn("An aria-label or aria-labelledby prop is required for accessibility.");
  }
  let domProps = (0, import_utils.filterDOMProps)(props, { labelable: true });
  let { listProps } = (0, import_selection.useSelectableList)({
    ...otherProps,
    ref,
    selectionManager: state.selectionManager,
    collection: state.collection,
    disabledKeys: state.disabledKeys,
    shouldFocusWrap,
    linkBehavior: "override"
  });
  menuData.set(state, {
    onClose: props.onClose,
    onAction: props.onAction
  });
  return {
    menuProps: (0, import_utils.mergeProps)(
      domProps,
      { onKeyDown, onKeyUp },
      {
        role: "menu",
        ...listProps,
        onKeyDown: (event) => {
          if (event.key !== "Escape") {
            if (listProps.onKeyDown) {
              listProps.onKeyDown(event);
            }
          }
        }
      }
    )
  };
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  menuData,
  useMenu
});
