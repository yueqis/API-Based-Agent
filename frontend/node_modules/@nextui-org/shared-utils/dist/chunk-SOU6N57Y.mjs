// src/functions.ts
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

export {
  capitalize,
  callAllHandlers,
  callAll,
  extractProperty,
  getUniqueID,
  removeEvents,
  objectToDeps
};
