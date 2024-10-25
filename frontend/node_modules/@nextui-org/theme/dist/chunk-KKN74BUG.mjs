import {
  tv
} from "./chunk-N2KXC5ZE.mjs";

// src/components/autocomplete.ts
var autocomplete = tv({
  slots: {
    base: "group inline-flex flex-column w-full",
    listboxWrapper: "scroll-py-6 max-h-64 w-full",
    listbox: "",
    popoverContent: "w-full p-1 overflow-hidden",
    endContentWrapper: "relative flex h-full items-center -mr-2",
    clearButton: [
      "text-medium",
      "translate-x-1",
      "cursor-text",
      "opacity-0",
      "text-default-500",
      "group-data-[invalid=true]:text-danger",
      "data-[visible=true]:opacity-100",
      "data-[visible=true]:cursor-pointer",
      "sm:data-[visible=true]:opacity-0",
      "sm:group-data-[hover=true]:data-[visible=true]:opacity-100"
    ],
    selectorButton: "text-medium"
  },
  variants: {
    isClearable: {
      true: {},
      false: {
        clearButton: "hidden"
      }
    },
    disableAnimation: {
      true: {
        selectorButton: "transition-none"
      },
      false: {
        selectorButton: "transition-transform duration-150 ease motion-reduce:transition-none"
      }
    },
    disableSelectorIconRotation: {
      true: {},
      false: {
        selectorButton: "data-[open=true]:rotate-180"
      }
    }
  },
  defaultVariants: {
    isClearable: true,
    disableSelectorIconRotation: false
  }
});

export {
  autocomplete
};
