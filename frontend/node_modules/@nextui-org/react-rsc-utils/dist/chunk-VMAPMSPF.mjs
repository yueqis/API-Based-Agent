import {
  require_react
} from "./chunk-2GZPFWUB.mjs";
import {
  __toESM
} from "./chunk-UYSIEMEK.mjs";

// src/children.ts
var import_react = __toESM(require_react());
function getValidChildren(children) {
  return import_react.Children.toArray(children).filter(
    (child) => (0, import_react.isValidElement)(child)
  );
}
var pickChildren = (children, targetChild) => {
  var _a;
  let target = [];
  const withoutTargetChildren = (_a = import_react.Children.map(children, (item) => {
    if (!(0, import_react.isValidElement)(item))
      return item;
    if (item.type === targetChild) {
      target.push(item);
      return null;
    }
    return item;
  })) == null ? void 0 : _a.filter(Boolean);
  const targetChildren = target.length >= 0 ? target : void 0;
  return [withoutTargetChildren, targetChildren];
};

export {
  getValidChildren,
  pickChildren
};
