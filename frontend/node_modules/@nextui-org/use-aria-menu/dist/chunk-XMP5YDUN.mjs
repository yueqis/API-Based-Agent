import {
  menuData
} from "./chunk-PH3KUROQ.mjs";

// src/use-menu-item.ts
import {
  chain,
  filterDOMProps,
  mergeProps,
  useLinkProps,
  useRouter,
  useSlotId
} from "@react-aria/utils";
import { getItemCount } from "@react-stately/collections";
import { isFocusVisible, useFocus, useHover, useKeyboard, usePress } from "@react-aria/interactions";
import { useSelectableItem } from "@react-aria/selection";
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
  let router = useRouter();
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
  let labelId = useSlotId();
  let descriptionId = useSlotId();
  let keyboardId = useSlotId();
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
    ariaProps["aria-setsize"] = getItemCount(state.collection);
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
  let { itemProps, isFocused } = useSelectableItem({
    selectionManager: state.selectionManager,
    key,
    ref,
    shouldSelectOnPressUp: true,
    allowsDifferentPressOrigin: true,
    linkBehavior: "none"
  });
  let { pressProps, isPressed } = usePress({
    onPressStart,
    onPress,
    onPressUp,
    onPressChange,
    onPressEnd,
    isDisabled
  });
  let { isHovered, hoverProps } = useHover({
    isDisabled,
    onHoverStart(e) {
      if (!isFocusVisible()) {
        state.selectionManager.setFocused(true);
        state.selectionManager.setFocusedKey(key);
      }
      hoverStartProp == null ? void 0 : hoverStartProp(e);
    },
    onHoverChange,
    onHoverEnd
  });
  let { keyboardProps } = useKeyboard({
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
  let { focusProps } = useFocus({ onBlur, onFocus, onFocusChange });
  let domProps = filterDOMProps(item.props);
  delete domProps.id;
  let linkProps = useLinkProps(item.props);
  return {
    menuItemProps: {
      ...ariaProps,
      ...mergeProps(
        domProps,
        linkProps,
        isTrigger ? { onFocus: itemProps.onFocus } : itemProps,
        pressProps,
        hoverProps,
        keyboardProps,
        focusProps,
        {
          onClick: chain(onClick, pressProps.onClick)
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

export {
  useMenuItem
};
