import type { BaseQueryFn, EndpointDefinitions, Module, MutationDefinition, QueryArgFrom, QueryDefinition } from '@reduxjs/toolkit/query';
import type { MutationHooks, QueryHooks } from './buildHooks';
import type { HooksWithUniqueNames } from './namedHooks';
import { createSelector as _createSelector } from 'reselect';
import type { QueryKeys } from '../core/apiState';
import type { PrefetchOptions } from '../core/module';
export declare const reactHooksModuleName: unique symbol;
export type ReactHooksModule = typeof reactHooksModuleName;
declare module '@reduxjs/toolkit/query' {
    interface ApiModules<BaseQuery extends BaseQueryFn, Definitions extends EndpointDefinitions, ReducerPath extends string, TagTypes extends string> {
        [reactHooksModuleName]: {
            /**
             *  Endpoints based on the input endpoints provided to `createApi`, containing `select`, `hooks` and `action matchers`.
             */
            endpoints: {
                [K in keyof Definitions]: Definitions[K] extends QueryDefinition<any, any, any, any, any> ? QueryHooks<Definitions[K]> : Definitions[K] extends MutationDefinition<any, any, any, any, any> ? MutationHooks<Definitions[K]> : never;
            };
            /**
             * A hook that accepts a string endpoint name, and provides a callback that when called, pre-fetches the data for that endpoint.
             */
            usePrefetch<EndpointName extends QueryKeys<Definitions>>(endpointName: EndpointName, options?: PrefetchOptions): (arg: QueryArgFrom<Definitions[EndpointName]>, options?: PrefetchOptions) => void;
        } & HooksWithUniqueNames<Definitions>;
    }
}
type RR = typeof import('react-redux');
export interface ReactHooksModuleOptions {
    /**
     * The hooks from React Redux to be used
     */
    hooks?: {
        /**
         * The version of the `useDispatch` hook to be used
         */
        useDispatch: RR['useDispatch'];
        /**
         * The version of the `useSelector` hook to be used
         */
        useSelector: RR['useSelector'];
        /**
         * The version of the `useStore` hook to be used
         */
        useStore: RR['useStore'];
    };
    /**
     * The version of the `batchedUpdates` function to be used
     */
    batch?: RR['batch'];
    /**
     * Enables performing asynchronous tasks immediately within a render.
     *
     * @example
     *
     * ```ts
     * import {
     *   buildCreateApi,
     *   coreModule,
     *   reactHooksModule
     * } from '@reduxjs/toolkit/query/react'
     *
     * const createApi = buildCreateApi(
     *   coreModule(),
     *   reactHooksModule({ unstable__sideEffectsInRender: true })
     * )
     * ```
     */
    unstable__sideEffectsInRender?: boolean;
    /**
     * A selector creator (usually from `reselect`, or matching the same signature)
     */
    createSelector?: typeof _createSelector;
}
/**
 * Creates a module that generates react hooks from endpoints, for use with `buildCreateApi`.
 *
 *  @example
 * ```ts
 * const MyContext = React.createContext<ReactReduxContextValue | null>(null);
 * const customCreateApi = buildCreateApi(
 *   coreModule(),
 *   reactHooksModule({
 *     hooks: {
 *       useDispatch: createDispatchHook(MyContext),
 *       useSelector: createSelectorHook(MyContext),
 *       useStore: createStoreHook(MyContext)
 *     }
 *   })
 * );
 * ```
 *
 * @returns A module for use with `buildCreateApi`
 */
export declare const reactHooksModule: ({ batch, hooks, createSelector, unstable__sideEffectsInRender, ...rest }?: ReactHooksModuleOptions) => Module<ReactHooksModule>;
export {};
