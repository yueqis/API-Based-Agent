import type { Action as ReduxAction, UnknownAction, Dispatch as ReduxDispatch, Middleware } from 'redux';
import type { TSHelpersExtractDispatchExtensions } from '@reduxjs/toolkit';
import type { ReactReduxContextValue } from 'react-redux';
import type { Context } from 'react';
import type { DynamicMiddlewareInstance, GetDispatch, GetState, MiddlewareApiConfig } from '@reduxjs/toolkit';
export type UseDispatchWithMiddlewareHook<Middlewares extends Middleware<any, State, Dispatch>[] = [], State = any, Dispatch extends ReduxDispatch<UnknownAction> = ReduxDispatch<UnknownAction>> = () => TSHelpersExtractDispatchExtensions<Middlewares> & Dispatch;
export type CreateDispatchWithMiddlewareHook<State = any, Dispatch extends ReduxDispatch<UnknownAction> = ReduxDispatch<UnknownAction>> = {
    <Middlewares extends [
        Middleware<any, State, Dispatch>,
        ...Middleware<any, State, Dispatch>[]
    ]>(...middlewares: Middlewares): UseDispatchWithMiddlewareHook<Middlewares, State, Dispatch>;
    withTypes<MiddlewareConfig extends MiddlewareApiConfig>(): CreateDispatchWithMiddlewareHook<GetState<MiddlewareConfig>, GetDispatch<MiddlewareConfig>>;
};
type ActionFromDispatch<Dispatch extends ReduxDispatch<ReduxAction>> = Dispatch extends ReduxDispatch<infer Action> ? Action : never;
interface ReactDynamicMiddlewareInstance<State = any, Dispatch extends ReduxDispatch<UnknownAction> = ReduxDispatch<UnknownAction>> extends DynamicMiddlewareInstance<State, Dispatch> {
    createDispatchWithMiddlewareHookFactory: (context?: Context<ReactReduxContextValue<State, ActionFromDispatch<Dispatch>> | null>) => CreateDispatchWithMiddlewareHook<State, Dispatch>;
    createDispatchWithMiddlewareHook: CreateDispatchWithMiddlewareHook<State, Dispatch>;
}
export declare const createDynamicMiddleware: <State = any, Dispatch extends ReduxDispatch<UnknownAction> = ReduxDispatch<UnknownAction>>() => ReactDynamicMiddlewareInstance<State, Dispatch>;
export {};
