import {
  twMergeConfig
} from "./chunk-BYWORP66.mjs";

// src/utils/cn.ts
import clsx from "clsx";
import { extendTailwindMerge } from "tailwind-merge";
var twMerge = extendTailwindMerge(twMergeConfig);
function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export {
  cn
};
