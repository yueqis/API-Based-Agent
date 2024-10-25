"use client";
import {
  listbox_section_default
} from "./chunk-DTVN5FMW.mjs";
import {
  listbox_item_default
} from "./chunk-JLLHEVKP.mjs";
import {
  useListbox
} from "./chunk-CKVQTQL5.mjs";

// src/listbox.tsx
import { forwardRef } from "@nextui-org/system";
import { mergeProps } from "@react-aria/utils";
import { jsx, jsxs } from "react/jsx-runtime";
function Listbox(props, ref) {
  const {
    Component,
    state,
    color,
    variant,
    itemClasses,
    getBaseProps,
    topContent,
    bottomContent,
    hideEmptyContent,
    hideSelectedIcon,
    shouldHighlightOnFocus,
    disableAnimation,
    getEmptyContentProps,
    getListProps
  } = useListbox({ ...props, ref });
  const content = /* @__PURE__ */ jsxs(Component, { ...getListProps(), children: [
    !state.collection.size && !hideEmptyContent && /* @__PURE__ */ jsx("li", { children: /* @__PURE__ */ jsx("div", { ...getEmptyContentProps() }) }),
    [...state.collection].map((item) => {
      var _a;
      const itemProps = {
        color,
        item,
        state,
        variant,
        disableAnimation,
        hideSelectedIcon,
        ...item.props
      };
      if (item.type === "section") {
        return /* @__PURE__ */ jsx(listbox_section_default, { ...itemProps, itemClasses }, item.key);
      }
      let listboxItem = /* @__PURE__ */ jsx(
        listbox_item_default,
        {
          ...itemProps,
          classNames: mergeProps(itemClasses, (_a = item.props) == null ? void 0 : _a.classNames),
          shouldHighlightOnFocus
        },
        item.key
      );
      if (item.wrapper) {
        listboxItem = item.wrapper(listboxItem);
      }
      return listboxItem;
    })
  ] });
  return /* @__PURE__ */ jsxs("div", { ...getBaseProps(), children: [
    topContent,
    content,
    bottomContent
  ] });
}
Listbox.displayName = "NextUI.Listbox";
var listbox_default = forwardRef(Listbox);

export {
  listbox_default
};
