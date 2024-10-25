// src/index.ts
import { chain } from "@react-aria/utils";
import { mergeProps } from "@react-aria/utils";
import { useAriaButton } from "@nextui-org/use-aria-button";
function useAriaToggleButton(props, state, ref) {
  const { isSelected } = state;
  const { isPressed, buttonProps } = useAriaButton(
    {
      ...props,
      onPress: chain(state.toggle, props.onPress)
    },
    ref
  );
  return {
    isPressed,
    buttonProps: mergeProps(buttonProps, {
      "aria-pressed": isSelected
    })
  };
}
export {
  useAriaToggleButton
};
