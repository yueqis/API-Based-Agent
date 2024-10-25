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

// src/use-menu-item.ts
var use_menu_item_exports = {};
__export(use_menu_item_exports, {
  useMenuItem: () => useMenuItem
});
module.exports = __toCommonJS(use_menu_item_exports);
var import_react = require("react");
var import_theme = require("@nextui-org/theme");
var import_system = require("@nextui-org/system");
var import_focus = require("@react-aria/focus");
var import_shared_utils = require("@nextui-org/shared-utils");
var import_use_aria_menu = require("@nextui-org/use-aria-menu");
var import_utils = require("@react-aria/utils");
var import_use_is_mobile = require("@nextui-org/use-is-mobile");
var import_react_utils = require("@nextui-org/react-utils");
function useMenuItem(originalProps) {
  var _a, _b;
  const globalContext = (0, import_system.useProviderContext)();
  const [props, variantProps] = (0, import_system.mapPropsVariants)(originalProps, import_theme.menuItem.variantKeys);
  const {
    as,
    item,
    state,
    shortcut,
    description,
    startContent,
    endContent,
    isVirtualized,
    selectedIcon,
    className,
    classNames,
    onAction,
    autoFocus,
    onClick,
    onPress,
    onPressStart,
    onPressUp,
    onPressEnd,
    onPressChange,
    hideSelectedIcon = false,
    isReadOnly = false,
    closeOnSelect,
    onClose,
    ...otherProps
  } = props;
  const disableAnimation = (_b = (_a = originalProps.disableAnimation) != null ? _a : globalContext == null ? void 0 : globalContext.disableAnimation) != null ? _b : false;
  const domRef = (0, import_react.useRef)(null);
  const Component = as || ((otherProps == null ? void 0 : otherProps.href) ? "a" : "li");
  const shouldFilterDOMProps = typeof Component === "string";
  const { rendered, key } = item;
  const isDisabled = state.disabledKeys.has(key) || originalProps.isDisabled;
  const isSelectable = state.selectionManager.selectionMode !== "none";
  const isMobile = (0, import_use_is_mobile.useIsMobile)();
  const { isFocusVisible, focusProps } = (0, import_focus.useFocusRing)({
    autoFocus
  });
  const {
    isHovered,
    isPressed,
    isFocused,
    isSelected,
    menuItemProps,
    labelProps,
    descriptionProps,
    keyboardShortcutProps
  } = (0, import_use_aria_menu.useAriaMenuItem)(
    {
      key,
      onClose,
      isDisabled,
      onPress,
      onClick,
      onPressStart,
      onPressUp,
      onPressEnd,
      onPressChange,
      "aria-label": props["aria-label"],
      closeOnSelect,
      isVirtualized,
      onAction
    },
    state,
    domRef
  );
  let itemProps = menuItemProps;
  const slots = (0, import_react.useMemo)(
    () => (0, import_theme.menuItem)({
      ...variantProps,
      isDisabled,
      disableAnimation
    }),
    [(0, import_shared_utils.objectToDeps)(variantProps), isDisabled, disableAnimation]
  );
  const baseStyles = (0, import_shared_utils.clsx)(classNames == null ? void 0 : classNames.base, className);
  if (isReadOnly) {
    itemProps = (0, import_shared_utils.removeEvents)(itemProps);
  }
  const getItemProps = (props2 = {}) => ({
    ref: domRef,
    ...(0, import_utils.mergeProps)(
      isReadOnly ? {} : focusProps,
      (0, import_react_utils.filterDOMProps)(otherProps, {
        enabled: shouldFilterDOMProps
      }),
      itemProps,
      props2
    ),
    "data-focus": (0, import_shared_utils.dataAttr)(isFocused),
    "data-selectable": (0, import_shared_utils.dataAttr)(isSelectable),
    "data-hover": (0, import_shared_utils.dataAttr)(isMobile ? isHovered || isPressed : isHovered),
    "data-disabled": (0, import_shared_utils.dataAttr)(isDisabled),
    "data-selected": (0, import_shared_utils.dataAttr)(isSelected),
    "data-pressed": (0, import_shared_utils.dataAttr)(isPressed),
    "data-focus-visible": (0, import_shared_utils.dataAttr)(isFocusVisible),
    className: slots.base({ class: (0, import_shared_utils.clsx)(baseStyles, props2.className) })
  });
  const getLabelProps = (props2 = {}) => ({
    ...(0, import_utils.mergeProps)(labelProps, props2),
    className: slots.title({ class: classNames == null ? void 0 : classNames.title })
  });
  const getDescriptionProps = (props2 = {}) => ({
    ...(0, import_utils.mergeProps)(descriptionProps, props2),
    className: slots.description({ class: classNames == null ? void 0 : classNames.description })
  });
  const getKeyboardShortcutProps = (props2 = {}) => ({
    ...(0, import_utils.mergeProps)(keyboardShortcutProps, props2),
    className: slots.shortcut({ class: classNames == null ? void 0 : classNames.shortcut })
  });
  const getSelectedIconProps = (0, import_react.useCallback)(
    (props2 = {}) => {
      return {
        "aria-hidden": (0, import_shared_utils.dataAttr)(true),
        "data-disabled": (0, import_shared_utils.dataAttr)(isDisabled),
        className: slots.selectedIcon({ class: classNames == null ? void 0 : classNames.selectedIcon }),
        ...props2
      };
    },
    [isDisabled, slots, classNames]
  );
  return {
    Component,
    domRef,
    slots,
    classNames,
    isSelectable,
    isSelected,
    isDisabled,
    rendered,
    shortcut,
    description,
    startContent,
    endContent,
    selectedIcon,
    disableAnimation,
    getItemProps,
    getLabelProps,
    hideSelectedIcon,
    getDescriptionProps,
    getKeyboardShortcutProps,
    getSelectedIconProps
  };
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  useMenuItem
});
