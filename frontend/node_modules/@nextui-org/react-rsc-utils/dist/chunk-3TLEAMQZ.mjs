import {
  require_react
} from "./chunk-2GZPFWUB.mjs";
import {
  __toESM
} from "./chunk-UYSIEMEK.mjs";

// src/functions.ts
var React = __toESM(require_react());
function renderFn({ Component, props, renderCustom }) {
  if (renderCustom && typeof renderCustom === "function") {
    return renderCustom(props);
  } else {
    return React.createElement(Component, props);
  }
}

export {
  renderFn
};
