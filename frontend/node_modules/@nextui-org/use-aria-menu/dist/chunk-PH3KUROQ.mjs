// src/use-menu.ts
import { filterDOMProps, mergeProps } from "@react-aria/utils";
import { useSelectableList } from "@react-aria/selection";
var menuData = /* @__PURE__ */ new WeakMap();
function useMenu(props, state, ref) {
  let { shouldFocusWrap = true, onKeyDown, onKeyUp, ...otherProps } = props;
  if (!props["aria-label"] && !props["aria-labelledby"]) {
    console.warn("An aria-label or aria-labelledby prop is required for accessibility.");
  }
  let domProps = filterDOMProps(props, { labelable: true });
  let { listProps } = useSelectableList({
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
    menuProps: mergeProps(
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

export {
  menuData,
  useMenu
};
