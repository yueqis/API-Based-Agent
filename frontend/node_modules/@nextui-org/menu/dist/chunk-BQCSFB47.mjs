"use client";

// src/use-menu-item.ts
import { useMemo, useRef, useCallback } from "react";
import { menuItem } from "@nextui-org/theme";
import {
  mapPropsVariants,
  useProviderContext
} from "@nextui-org/system";
import { useFocusRing } from "@react-aria/focus";
import { clsx, dataAttr, objectToDeps, removeEvents } from "@nextui-org/shared-utils";
import { useAriaMenuItem } from "@nextui-org/use-aria-menu";
import { mergeProps } from "@react-aria/utils";
import { useIsMobile } from "@nextui-org/use-is-mobile";
import { filterDOMProps } from "@nextui-org/react-utils";
function useMenuItem(originalProps) {
  var _a, _b;
  const globalContext = useProviderContext();
  const [props, variantProps] = mapPropsVariants(originalProps, menuItem.variantKeys);
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
  const domRef = useRef(null);
  const Component = as || ((otherProps == null ? void 0 : otherProps.href) ? "a" : "li");
  const shouldFilterDOMProps = typeof Component === "string";
  const { rendered, key } = item;
  const isDisabled = state.disabledKeys.has(key) || originalProps.isDisabled;
  const isSelectable = state.selectionManager.selectionMode !== "none";
  const isMobile = useIsMobile();
  const { isFocusVisible, focusProps } = useFocusRing({
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
  } = useAriaMenuItem(
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
  const slots = useMemo(
    () => menuItem({
      ...variantProps,
      isDisabled,
      disableAnimation
    }),
    [objectToDeps(variantProps), isDisabled, disableAnimation]
  );
  const baseStyles = clsx(classNames == null ? void 0 : classNames.base, className);
  if (isReadOnly) {
    itemProps = removeEvents(itemProps);
  }
  const getItemProps = (props2 = {}) => ({
    ref: domRef,
    ...mergeProps(
      isReadOnly ? {} : focusProps,
      filterDOMProps(otherProps, {
        enabled: shouldFilterDOMProps
      }),
      itemProps,
      props2
    ),
    "data-focus": dataAttr(isFocused),
    "data-selectable": dataAttr(isSelectable),
    "data-hover": dataAttr(isMobile ? isHovered || isPressed : isHovered),
    "data-disabled": dataAttr(isDisabled),
    "data-selected": dataAttr(isSelected),
    "data-pressed": dataAttr(isPressed),
    "data-focus-visible": dataAttr(isFocusVisible),
    className: slots.base({ class: clsx(baseStyles, props2.className) })
  });
  const getLabelProps = (props2 = {}) => ({
    ...mergeProps(labelProps, props2),
    className: slots.title({ class: classNames == null ? void 0 : classNames.title })
  });
  const getDescriptionProps = (props2 = {}) => ({
    ...mergeProps(descriptionProps, props2),
    className: slots.description({ class: classNames == null ? void 0 : classNames.description })
  });
  const getKeyboardShortcutProps = (props2 = {}) => ({
    ...mergeProps(keyboardShortcutProps, props2),
    className: slots.shortcut({ class: classNames == null ? void 0 : classNames.shortcut })
  });
  const getSelectedIconProps = useCallback(
    (props2 = {}) => {
      return {
        "aria-hidden": dataAttr(true),
        "data-disabled": dataAttr(isDisabled),
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

export {
  useMenuItem
};
