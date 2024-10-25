import type { Action, Dispatch, UnknownAction } from 'redux';
import type { ThunkDispatch } from 'redux-thunk';
import type { CreateListenerMiddlewareOptions, ListenerMiddlewareInstance, TypedAddListener, TypedCreateListenerEntry, TypedRemoveListener } from './types';
export { TaskAbortError } from './exceptions';
export type { AsyncTaskExecutor, CreateListenerMiddlewareOptions, ForkedTask, ForkedTaskAPI, ForkedTaskExecutor, ListenerEffect, ListenerEffectAPI, ListenerErrorHandler, ListenerMiddleware, ListenerMiddlewareInstance, SyncTaskExecutor, TaskCancelled, TaskRejected, TaskResolved, TaskResult, TypedAddListener, TypedRemoveListener, TypedStartListening, TypedStopListening, UnsubscribeListener, UnsubscribeListenerOptions, } from './types';
/** Accepts the possible options for creating a listener, and returns a formatted listener entry */
export declare const createListenerEntry: TypedCreateListenerEntry<unknown>;
/**
 * @public
 */
export declare const addListener: TypedAddListener<unknown>;
/**
 * @public
 */
export declare const clearAllListeners: import("../createAction").ActionCreatorWithoutPayload<"listenerMiddleware/removeAll">;
/**
 * @public
 */
export declare const removeListener: TypedRemoveListener<unknown>;
/**
 * @public
 */
export declare const createListenerMiddleware: <StateType = unknown, DispatchType extends Dispatch<Action> = ThunkDispatch<StateType, unknown, UnknownAction>, ExtraArgument = unknown>(middlewareOptions?: CreateListenerMiddlewareOptions<ExtraArgument>) => ListenerMiddlewareInstance<StateType, DispatchType, ExtraArgument>;
