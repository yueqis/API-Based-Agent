// src/react/index.ts
export * from "@reduxjs/toolkit";

// src/dynamicMiddleware/react/index.ts
import { createDynamicMiddleware as cDM } from "@reduxjs/toolkit";
import { ReactReduxContext, useDispatch as useDefaultDispatch, createDispatchHook } from "react-redux";
var createDynamicMiddleware = () => {
  const instance = cDM();
  const createDispatchWithMiddlewareHookFactory = (context = ReactReduxContext) => {
    const useDispatch = context === ReactReduxContext ? useDefaultDispatch : createDispatchHook(context);
    function createDispatchWithMiddlewareHook2(...middlewares) {
      instance.addMiddleware(...middlewares);
      return useDispatch;
    }
    createDispatchWithMiddlewareHook2.withTypes = () => createDispatchWithMiddlewareHook2;
    return createDispatchWithMiddlewareHook2;
  };
  const createDispatchWithMiddlewareHook = createDispatchWithMiddlewareHookFactory();
  return {
    ...instance,
    createDispatchWithMiddlewareHookFactory,
    createDispatchWithMiddlewareHook
  };
};
export {
  createDynamicMiddleware
};
//# sourceMappingURL=redux-toolkit-react.modern.mjs.map