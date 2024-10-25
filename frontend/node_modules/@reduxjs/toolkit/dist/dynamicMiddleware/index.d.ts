import type { Dispatch as ReduxDispatch, UnknownAction } from 'redux';
import type { DynamicMiddlewareInstance } from './types';
export declare const createDynamicMiddleware: <State = any, Dispatch extends ReduxDispatch<UnknownAction> = ReduxDispatch<UnknownAction>>() => DynamicMiddlewareInstance<State, Dispatch>;
