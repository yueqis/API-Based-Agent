"use client";
import {
  useNavbarContext
} from "./chunk-CLWTNWD4.mjs";
import {
  menuVariants
} from "./chunk-UJDFI5KD.mjs";

// src/navbar-menu.tsx
import { forwardRef } from "@nextui-org/system";
import { useDOMRef } from "@nextui-org/react-utils";
import { clsx, dataAttr } from "@nextui-org/shared-utils";
import { AnimatePresence, domAnimation, LazyMotion, m } from "framer-motion";
import { mergeProps } from "@react-aria/utils";
import { useCallback } from "react";
import { RemoveScroll } from "react-remove-scroll";
import { Overlay } from "@react-aria/overlays";
import { jsx } from "react/jsx-runtime";
var NavbarMenu = forwardRef((props, ref) => {
  var _a, _b;
  const { className, children, portalContainer, motionProps, style, ...otherProps } = props;
  const domRef = useDOMRef(ref);
  const { slots, isMenuOpen, height, disableAnimation, classNames } = useNavbarContext();
  const styles = clsx(classNames == null ? void 0 : classNames.menu, className);
  const MenuWrapper = useCallback(
    ({ children: children2 }) => {
      return /* @__PURE__ */ jsx(RemoveScroll, { forwardProps: true, enabled: isMenuOpen, removeScrollBar: false, children: children2 });
    },
    [isMenuOpen]
  );
  const contents = disableAnimation ? /* @__PURE__ */ jsx(MenuWrapper, { children: /* @__PURE__ */ jsx(
    "ul",
    {
      ref: domRef,
      className: (_a = slots.menu) == null ? void 0 : _a.call(slots, { class: styles }),
      "data-open": dataAttr(isMenuOpen),
      style: {
        "--navbar-height": height
      },
      ...otherProps,
      children
    }
  ) }) : /* @__PURE__ */ jsx(AnimatePresence, { mode: "wait", children: isMenuOpen ? /* @__PURE__ */ jsx(LazyMotion, { features: domAnimation, children: /* @__PURE__ */ jsx(MenuWrapper, { children: /* @__PURE__ */ jsx(
    m.ul,
    {
      ref: domRef,
      layoutScroll: true,
      animate: "enter",
      className: (_b = slots.menu) == null ? void 0 : _b.call(slots, { class: styles }),
      "data-open": dataAttr(isMenuOpen),
      exit: "exit",
      initial: "exit",
      style: {
        "--navbar-height": height,
        ...style
      },
      variants: menuVariants,
      ...mergeProps(motionProps, otherProps),
      children
    }
  ) }) }) : null });
  return /* @__PURE__ */ jsx(Overlay, { portalContainer, children: contents });
});
NavbarMenu.displayName = "NextUI.NavbarMenu";
var navbar_menu_default = NavbarMenu;

export {
  navbar_menu_default
};
