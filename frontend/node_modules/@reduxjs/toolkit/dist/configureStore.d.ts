import type { Reducer, ReducersMapObject, Middleware, Action, StoreEnhancer, Store, UnknownAction } from 'redux';
import type { DevToolsEnhancerOptions as DevToolsOptions } from './devtoolsExtension';
import type { ThunkMiddlewareFor, GetDefaultMiddleware } from './getDefaultMiddleware';
import type { ExtractDispatchExtensions, ExtractStoreExtensions, ExtractStateExtensions, UnknownIfNonSpecific } from './tsHelpers';
import type { Tuple } from './utils';
import type { GetDefaultEnhancers } from './getDefaultEnhancers';
/**
 * Options for `configureStore()`.
 *
 * @public
 */
export interface ConfigureStoreOptions<S = any, A extends Action = UnknownAction, M extends Tuple<Middlewares<S>> = Tuple<Middlewares<S>>, E extends Tuple<Enhancers> = Tuple<Enhancers>, P = S> {
    /**
     * A single reducer function that will be used as the root reducer, or an
     * object of slice reducers that will be passed to `combineReducers()`.
     */
    reducer: Reducer<S, A, P> | ReducersMapObject<S, A, P>;
    /**
     * An array of Redux middleware to install, or a callback receiving `getDefaultMiddleware` and returning a Tuple of middleware.
     * If not supplied, defaults to the set of middleware returned by `getDefaultMiddleware()`.
     *
     * @example `middleware: (gDM) => gDM().concat(logger, apiMiddleware, yourCustomMiddleware)`
     * @see https://redux-toolkit.js.org/api/getDefaultMiddleware#intended-usage
     */
    middleware?: (getDefaultMiddleware: GetDefaultMiddleware<S>) => M;
    /**
     * Whether to enable Redux DevTools integration. Defaults to `true`.
     *
     * Additional configuration can be done by passing Redux DevTools options
     */
    devTools?: boolean | DevToolsOptions;
    /**
     * The initial state, same as Redux's createStore.
     * You may optionally specify it to hydrate the state
     * from the server in universal apps, or to restore a previously serialized
     * user session. If you use `combineReducers()` to produce the root reducer
     * function (either directly or indirectly by passing an object as `reducer`),
     * this must be an object with the same shape as the reducer map keys.
     */
    preloadedState?: P;
    /**
     * The store enhancers to apply. See Redux's `createStore()`.
     * All enhancers will be included before the DevTools Extension enhancer.
     * If you need to customize the order of enhancers, supply a callback
     * function that will receive a `getDefaultEnhancers` function that returns a Tuple,
     * and should return a Tuple of enhancers (such as `getDefaultEnhancers().concat(offline)`).
     * If you only need to add middleware, you can use the `middleware` parameter instead.
     */
    enhancers?: (getDefaultEnhancers: GetDefaultEnhancers<M>) => E;
}
export type Middlewares<S> = ReadonlyArray<Middleware<{}, S>>;
type Enhancers = ReadonlyArray<StoreEnhancer>;
/**
 * A Redux store returned by `configureStore()`. Supports dispatching
 * side-effectful _thunks_ in addition to plain actions.
 *
 * @public
 */
export type EnhancedStore<S = any, A extends Action = UnknownAction, E extends Enhancers = Enhancers> = ExtractStoreExtensions<E> & Store<S, A, UnknownIfNonSpecific<ExtractStateExtensions<E>>>;
/**
 * A friendly abstraction over the standard Redux `createStore()` function.
 *
 * @param options The store configuration.
 * @returns A configured Redux store.
 *
 * @public
 */
export declare function configureStore<S = any, A extends Action = UnknownAction, M extends Tuple<Middlewares<S>> = Tuple<[ThunkMiddlewareFor<S>]>, E extends Tuple<Enhancers> = Tuple<[
    StoreEnhancer<{
        dispatch: ExtractDispatchExtensions<M>;
    }>,
    StoreEnhancer
]>, P = S>(options: ConfigureStoreOptions<S, A, M, E, P>): EnhancedStore<S, A, E>;
export {};
