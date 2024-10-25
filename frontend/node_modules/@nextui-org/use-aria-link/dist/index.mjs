// src/index.ts
import {
  filterDOMProps,
  mergeProps,
  useRouter,
  shouldClientNavigate,
  useLinkProps
} from "@react-aria/utils";
import { useFocusable } from "@react-aria/focus";
import { usePress } from "@react-aria/interactions";
function useAriaLink(props, ref) {
  let {
    elementType = "a",
    onPress,
    onPressStart,
    onPressEnd,
    onClick: deprecatedOnClick,
    isDisabled,
    ...otherProps
  } = props;
  let linkProps = {};
  if (elementType !== "a") {
    linkProps = {
      role: "link",
      tabIndex: !isDisabled ? 0 : void 0
    };
  }
  let { focusableProps } = useFocusable(props, ref);
  let { pressProps, isPressed } = usePress({ onPress, onPressStart, onPressEnd, isDisabled, ref });
  let domProps = filterDOMProps(otherProps, { labelable: true, isLink: elementType === "a" });
  let interactionHandlers = mergeProps(focusableProps, pressProps);
  let router = useRouter();
  let routerLinkProps = useLinkProps(props);
  return {
    isPressed,
    linkProps: mergeProps(domProps, routerLinkProps, {
      ...interactionHandlers,
      ...linkProps,
      "aria-disabled": isDisabled || void 0,
      "aria-current": props["aria-current"],
      onClick: (e) => {
        var _a;
        (_a = pressProps.onClick) == null ? void 0 : _a.call(pressProps, e);
        if (deprecatedOnClick) {
          deprecatedOnClick(e);
        }
        if (!router.isNative && e.currentTarget instanceof HTMLAnchorElement && e.currentTarget.href && !e.isDefaultPrevented() && shouldClientNavigate(e.currentTarget, e) && props.href) {
          e.preventDefault();
          router.open(e.currentTarget, e, props.href, props.routerOptions);
        }
      }
    })
  };
}
export {
  useAriaLink
};
