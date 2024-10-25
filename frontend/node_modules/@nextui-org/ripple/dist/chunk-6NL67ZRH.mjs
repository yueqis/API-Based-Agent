"use client";

// src/use-ripple.ts
import { getUniqueID } from "@nextui-org/shared-utils";
import { useCallback, useState } from "react";
function useRipple(props = {}) {
  const [ripples, setRipples] = useState([]);
  const onClick = useCallback((event) => {
    const trigger = event.currentTarget;
    const size = Math.max(trigger.clientWidth, trigger.clientHeight);
    const rect = trigger.getBoundingClientRect();
    setRipples((prevRipples) => [
      ...prevRipples,
      {
        key: getUniqueID(prevRipples.length.toString()),
        size,
        x: event.clientX - rect.left - size / 2,
        y: event.clientY - rect.top - size / 2
      }
    ]);
  }, []);
  const onClear = useCallback((key) => {
    setRipples((prevState) => prevState.filter((ripple) => ripple.key !== key));
  }, []);
  return { ripples, onClick, onClear, ...props };
}

export {
  useRipple
};
