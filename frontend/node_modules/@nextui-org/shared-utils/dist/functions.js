"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/functions.ts
var functions_exports = {};
__export(functions_exports, {
  callAll: () => callAll,
  callAllHandlers: () => callAllHandlers,
  capitalize: () => capitalize,
  extractProperty: () => extractProperty,
  getUniqueID: () => getUniqueID,
  objectToDeps: () => objectToDeps,
  removeEvents: () => removeEvents
});
module.exports = __toCommonJS(functions_exports);
var capitalize = (text) => {
  return text.charAt(0).toUpperCase() + text.slice(1);
};
function callAllHandlers(...fns) {
  return function func(event) {
    fns.some((fn) => {
      fn == null ? void 0 : fn(event);
      return event == null ? void 0 : event.defaultPrevented;
    });
  };
}
function callAll(...fns) {
  return function mergedFn(arg) {
    fns.forEach((fn) => {
      fn == null ? void 0 : fn(arg);
    });
  };
}
function extractProperty(key, defaultValue, ...objs) {
  let result = defaultValue;
  for (const obj of objs) {
    if (obj && key in obj && !!obj[key]) {
      result = obj[key];
    }
  }
  return result;
}
function getUniqueID(prefix) {
  return `${prefix}-${Math.floor(Math.random() * 1e6)}`;
}
function removeEvents(input) {
  for (const key in input) {
    if (key.startsWith("on")) {
      delete input[key];
    }
  }
  return input;
}
function objectToDeps(obj) {
  if (!obj || typeof obj !== "object") {
    return "";
  }
  try {
    return JSON.stringify(obj);
  } catch (e) {
    return "";
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  callAll,
  callAllHandlers,
  capitalize,
  extractProperty,
  getUniqueID,
  objectToDeps,
  removeEvents
});
