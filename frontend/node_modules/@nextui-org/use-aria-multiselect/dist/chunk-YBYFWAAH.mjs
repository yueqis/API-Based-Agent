import {
  useMultiSelectListState
} from "./chunk-RVB7J7GX.mjs";

// src/use-multiselect-state.ts
import { useMenuTriggerState } from "@react-stately/menu";
import { useFormValidationState } from "@react-stately/form";
import { useState } from "react";
function useMultiSelectState(props) {
  const [isFocused, setFocused] = useState(false);
  const [focusStrategy, setFocusStrategy] = useState(null);
  const triggerState = useMenuTriggerState(props);
  const listState = useMultiSelectListState({
    ...props,
    onSelectionChange: (keys) => {
      if (props.onSelectionChange != null) {
        if (keys === "all") {
          props.onSelectionChange(new Set(listState.collection.getKeys()));
        } else {
          props.onSelectionChange(keys);
        }
      }
      if (props.selectionMode === "single") {
        triggerState.close();
      }
    }
  });
  const validationState = useFormValidationState({
    ...props,
    validationBehavior: "native",
    value: listState.selectedKeys
  });
  return {
    ...validationState,
    ...listState,
    ...triggerState,
    focusStrategy,
    close() {
      triggerState.close();
    },
    open(focusStrategy2 = null) {
      if (listState.collection.size !== 0) {
        setFocusStrategy(focusStrategy2);
        triggerState.open();
      }
    },
    toggle(focusStrategy2 = null) {
      if (listState.collection.size !== 0) {
        setFocusStrategy(focusStrategy2);
        triggerState.toggle();
        validationState.commitValidation();
      }
    },
    isFocused,
    setFocused
  };
}

export {
  useMultiSelectState
};
