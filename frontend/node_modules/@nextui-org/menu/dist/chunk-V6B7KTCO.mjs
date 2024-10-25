"use client";
import {
  menu_section_default
} from "./chunk-SMP2PQ35.mjs";
import {
  menu_item_default
} from "./chunk-CQ43W3AP.mjs";
import {
  useMenu
} from "./chunk-BA3PRXRG.mjs";

// src/menu.tsx
import { forwardRef } from "@nextui-org/system";
import { jsx, jsxs } from "react/jsx-runtime";
function Menu(props, ref) {
  const {
    Component,
    state,
    closeOnSelect,
    color,
    disableAnimation,
    hideSelectedIcon,
    hideEmptyContent,
    variant,
    onClose,
    onAction,
    topContent,
    bottomContent,
    itemClasses,
    getBaseProps,
    getListProps,
    getEmptyContentProps
  } = useMenu({ ...props, ref });
  const content = /* @__PURE__ */ jsxs(Component, { ...getListProps(), children: [
    !state.collection.size && !hideEmptyContent && /* @__PURE__ */ jsx("li", { children: /* @__PURE__ */ jsx("div", { ...getEmptyContentProps() }) }),
    [...state.collection].map((item) => {
      const itemProps = {
        closeOnSelect,
        color,
        disableAnimation,
        item,
        state,
        variant,
        onClose,
        onAction,
        hideSelectedIcon,
        ...item.props
      };
      if (item.type === "section") {
        return /* @__PURE__ */ jsx(menu_section_default, { ...itemProps, itemClasses }, item.key);
      }
      let menuItem = /* @__PURE__ */ jsx(menu_item_default, { ...itemProps, classNames: itemClasses }, item.key);
      if (item.wrapper) {
        menuItem = item.wrapper(menuItem);
      }
      return menuItem;
    })
  ] });
  return /* @__PURE__ */ jsxs("div", { ...getBaseProps(), children: [
    topContent,
    content,
    bottomContent
  ] });
}
var menu_default = forwardRef(Menu);
Menu.displayName = "NextUI.Menu";

export {
  menu_default
};
