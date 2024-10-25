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
  menuData: () => menuData,
  useAriaMenu: () => useMenu,
  useAriaMenuItem: () => useMenuItem
});
module.exports = __toCommonJS(src_exports);

// src/use-menu.ts
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

// src/use-menu-item.ts
var import_utils2 = require("@react-aria/utils");
var import_collections = require("@react-stately/collections");
var import_interactions = require("@react-aria/interactions");
var import_selection2 = require("@react-aria/selection");
function useMenuItem(props, state, ref) {
  var _a, _b;
  let {
    key,
    closeOnSelect,
    isVirtualized,
    "aria-haspopup": hasPopup,
    onPressStart: pressStartProp,
    onPressUp: pressUpProp,
    onPress,
    onPressChange,
    onPressEnd,
    onHoverStart: hoverStartProp,
    onHoverChange,
    onHoverEnd,
    onKeyDown,
    onKeyUp,
    onFocus,
    onFocusChange,
    onBlur,
    onClick
  } = props;
  let isTrigger = !!hasPopup;
  let isDisabled = (_a = props.isDisabled) != null ? _a : state.selectionManager.isDisabled(key);
  let isSelected = (_b = props.isSelected) != null ? _b : state.selectionManager.isSelected(key);
  let data = menuData.get(state);
  let item = state.collection.getItem(key);
  let onClose = props.onClose || data.onClose;
  let router = (0, import_utils2.useRouter)();
  let performAction = (e) => {
    var _a2;
    if (isTrigger) {
      return;
    }
    if ((_a2 = item == null ? void 0 : item.props) == null ? void 0 : _a2.onAction) {
      item.props.onAction();
    }
    if (props.onAction) {
      props.onAction(key);
    } else if (data.onAction) {
      data.onAction(key);
    }
    if (e.target instanceof HTMLAnchorElement) {
      router.open(e.target, e, item.props.href, item.props.routerOptions);
    }
  };
  let role = "menuitem";
  if (!isTrigger) {
    if (state.selectionManager.selectionMode === "single") {
      role = "menuitemradio";
    } else if (state.selectionManager.selectionMode === "multiple") {
      role = "menuitemcheckbox";
    }
  }
  let labelId = (0, import_utils2.useSlotId)();
  let descriptionId = (0, import_utils2.useSlotId)();
  let keyboardId = (0, import_utils2.useSlotId)();
  let ariaProps = {
    "aria-disabled": isDisabled || void 0,
    role,
    "aria-label": props["aria-label"],
    "aria-labelledby": labelId,
    "aria-describedby": [descriptionId, keyboardId].filter(Boolean).join(" ") || void 0,
    "aria-controls": props["aria-controls"],
    "aria-haspopup": hasPopup,
    "aria-expanded": props["aria-expanded"]
  };
  if (state.selectionManager.selectionMode !== "none" && !isTrigger) {
    ariaProps["aria-checked"] = isSelected;
  }
  if (isVirtualized) {
    ariaProps["aria-posinset"] = item == null ? void 0 : item.index;
    ariaProps["aria-setsize"] = (0, import_collections.getItemCount)(state.collection);
  }
  let onPressStart = (e) => {
    if (e.pointerType === "keyboard") {
      performAction(e);
    }
    pressStartProp == null ? void 0 : pressStartProp(e);
  };
  let onPressUp = (e) => {
    if (e.pointerType !== "keyboard") {
      setTimeout(() => {
        performAction(e);
      });
      if (!isTrigger && onClose && (closeOnSelect != null ? closeOnSelect : state.selectionManager.selectionMode !== "multiple" || state.selectionManager.isLink(key))) {
        setTimeout(() => {
          onClose == null ? void 0 : onClose();
        });
      }
    }
    pressUpProp == null ? void 0 : pressUpProp(e);
  };
  let { itemProps, isFocused } = (0, import_selection2.useSelectableItem)({
    selectionManager: state.selectionManager,
    key,
    ref,
    shouldSelectOnPressUp: true,
    allowsDifferentPressOrigin: true,
    linkBehavior: "none"
  });
  let { pressProps, isPressed } = (0, import_interactions.usePress)({
    onPressStart,
    onPress,
    onPressUp,
    onPressChange,
    onPressEnd,
    isDisabled
  });
  let { isHovered, hoverProps } = (0, import_interactions.useHover)({
    isDisabled,
    onHoverStart(e) {
      if (!(0, import_interactions.isFocusVisible)()) {
        state.selectionManager.setFocused(true);
        state.selectionManager.setFocusedKey(key);
      }
      hoverStartProp == null ? void 0 : hoverStartProp(e);
    },
    onHoverChange,
    onHoverEnd
  });
  let { keyboardProps } = (0, import_interactions.useKeyboard)({
    onKeyDown: (e) => {
      if (e.repeat) {
        e.continuePropagation();
        return;
      }
      switch (e.key) {
        case " ":
          if (!isDisabled && state.selectionManager.selectionMode === "none" && !isTrigger && closeOnSelect !== false && onClose) {
            onClose();
          }
          break;
        case "Enter":
          if (!isDisabled && closeOnSelect !== false && !isTrigger && onClose) {
            onClose();
          }
          break;
        default:
          if (!isTrigger) {
            e.continuePropagation();
          }
          onKeyDown == null ? void 0 : onKeyDown(e);
          break;
      }
    },
    onKeyUp
  });
  let { focusProps } = (0, import_interactions.useFocus)({ onBlur, onFocus, onFocusChange });
  let domProps = (0, import_utils2.filterDOMProps)(item.props);
  delete domProps.id;
  let linkProps = (0, import_utils2.useLinkProps)(item.props);
  return {
    menuItemProps: {
      ...ariaProps,
      ...(0, import_utils2.mergeProps)(
        domProps,
        linkProps,
        isTrigger ? { onFocus: itemProps.onFocus } : itemProps,
        pressProps,
        hoverProps,
        keyboardProps,
        focusProps,
        {
          onClick: (0, import_utils2.chain)(onClick, pressProps.onClick)
        }
      ),
      tabIndex: itemProps.tabIndex != null ? -1 : void 0
    },
    labelProps: {
      id: labelId
    },
    descriptionProps: {
      id: descriptionId
    },
    keyboardShortcutProps: {
      id: keyboardId
    },
    isHovered,
    isFocused,
    isSelected,
    isPressed,
    isDisabled
  };
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  menuData,
  useAriaMenu,
  useAriaMenuItem
});
