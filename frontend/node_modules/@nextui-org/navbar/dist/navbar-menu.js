"use client";
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

// src/navbar-menu.tsx
var navbar_menu_exports = {};
__export(navbar_menu_exports, {
  default: () => navbar_menu_default
});
module.exports = __toCommonJS(navbar_menu_exports);
var import_system = require("@nextui-org/system");
var import_react_utils2 = require("@nextui-org/react-utils");
var import_shared_utils = require("@nextui-org/shared-utils");
var import_framer_motion = require("framer-motion");
var import_utils = require("@react-aria/utils");
var import_react = require("react");
var import_react_remove_scroll = require("react-remove-scroll");
var import_overlays = require("@react-aria/overlays");

// src/navbar-menu-transitions.ts
var menuVariants = {
  enter: {
    height: "calc(100vh - var(--navbar-height))",
    transition: {
      duration: 0.3,
      easings: "easeOut"
    }
  },
  exit: {
    height: 0,
    transition: {
      duration: 0.25,
      easings: "easeIn"
    }
  }
};

// src/navbar-context.ts
var import_react_utils = require("@nextui-org/react-utils");
var [NavbarProvider, useNavbarContext] = (0, import_react_utils.createContext)({
  name: "NavbarContext",
  strict: true,
  errorMessage: "useNavbarContext: `context` is undefined. Seems you forgot to wrap component within <Navbar />"
});

// src/navbar-menu.tsx
var import_jsx_runtime = require("react/jsx-runtime");
var NavbarMenu = (0, import_system.forwardRef)((props, ref) => {
  var _a, _b;
  const { className, children, portalContainer, motionProps, style, ...otherProps } = props;
  const domRef = (0, import_react_utils2.useDOMRef)(ref);
  const { slots, isMenuOpen, height, disableAnimation, classNames } = useNavbarContext();
  const styles = (0, import_shared_utils.clsx)(classNames == null ? void 0 : classNames.menu, className);
  const MenuWrapper = (0, import_react.useCallback)(
    ({ children: children2 }) => {
      return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_react_remove_scroll.RemoveScroll, { forwardProps: true, enabled: isMenuOpen, removeScrollBar: false, children: children2 });
    },
    [isMenuOpen]
  );
  const contents = disableAnimation ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(MenuWrapper, { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(
    "ul",
    {
      ref: domRef,
      className: (_a = slots.menu) == null ? void 0 : _a.call(slots, { class: styles }),
      "data-open": (0, import_shared_utils.dataAttr)(isMenuOpen),
      style: {
        "--navbar-height": height
      },
      ...otherProps,
      children
    }
  ) }) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_framer_motion.AnimatePresence, { mode: "wait", children: isMenuOpen ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_framer_motion.LazyMotion, { features: import_framer_motion.domAnimation, children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(MenuWrapper, { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(
    import_framer_motion.m.ul,
    {
      ref: domRef,
      layoutScroll: true,
      animate: "enter",
      className: (_b = slots.menu) == null ? void 0 : _b.call(slots, { class: styles }),
      "data-open": (0, import_shared_utils.dataAttr)(isMenuOpen),
      exit: "exit",
      initial: "exit",
      style: {
        "--navbar-height": height,
        ...style
      },
      variants: menuVariants,
      ...(0, import_utils.mergeProps)(motionProps, otherProps),
      children
    }
  ) }) }) : null });
  return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(import_overlays.Overlay, { portalContainer, children: contents });
});
NavbarMenu.displayName = "NextUI.NavbarMenu";
var navbar_menu_default = NavbarMenu;
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {});
