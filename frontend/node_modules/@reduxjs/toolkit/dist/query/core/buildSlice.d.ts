import type { UnknownAction } from '@reduxjs/toolkit';
import type { QuerySubstateIdentifier, MutationSubstateIdentifier, MutationState, QueryState, InvalidationState, Subscribers, QueryCacheKey, SubscriptionState, ConfigState } from './apiState';
import type { MutationThunk, QueryThunk } from './buildThunks';
import type { AssertTagTypes, EndpointDefinitions, FullTagDescription } from '../endpointDefinitions';
import type { Patch } from 'immer';
import type { ApiContext } from '../apiTypes';
export declare function getMutationCacheKey(id: MutationSubstateIdentifier | {
    requestId: string;
    arg: {
        fixedCacheKey?: string | undefined;
    };
}): string;
export declare function getMutationCacheKey(id: {
    fixedCacheKey?: string;
    requestId?: string;
}): string | undefined;
export declare function buildSlice({ reducerPath, queryThunk, mutationThunk, context: { endpointDefinitions: definitions, apiUid, extractRehydrationInfo, hasRehydrationInfo, }, assertTagType, config, }: {
    reducerPath: string;
    queryThunk: QueryThunk;
    mutationThunk: MutationThunk;
    context: ApiContext<EndpointDefinitions>;
    assertTagType: AssertTagTypes;
    config: Omit<ConfigState<string>, 'online' | 'focused' | 'middlewareRegistered'>;
}): {
    reducer: import("redux").Reducer<{
        queries: QueryState<any>;
        mutations: MutationState<any>;
        provided: InvalidationState<string>;
        subscriptions: SubscriptionState;
        config: ConfigState<string>;
    }, UnknownAction, Partial<{
        queries: QueryState<any> | undefined;
        mutations: MutationState<any> | undefined;
        provided: InvalidationState<string> | undefined;
        subscriptions: SubscriptionState | undefined;
        config: ConfigState<string> | undefined;
    }>>;
    actions: {
        resetApiState: import("@reduxjs/toolkit").ActionCreatorWithoutPayload<`${string}/resetApiState`>;
        updateProvidedBy: import("@reduxjs/toolkit").ActionCreatorWithPreparedPayload<[payload: {
            queryCacheKey: QueryCacheKey;
            providedTags: readonly FullTagDescription<string>[];
        }], {
            queryCacheKey: QueryCacheKey;
            providedTags: readonly FullTagDescription<string>[];
        }, `${string}/invalidation/updateProvidedBy`, never, unknown>;
        removeMutationResult: import("@reduxjs/toolkit").ActionCreatorWithPreparedPayload<[payload: MutationSubstateIdentifier], MutationSubstateIdentifier, `${string}/mutations/removeMutationResult`, never, unknown>;
        subscriptionsUpdated: import("@reduxjs/toolkit").ActionCreatorWithPreparedPayload<[payload: Patch[]], Patch[], `${string}/internalSubscriptions/subscriptionsUpdated`, never, unknown>;
        updateSubscriptionOptions: import("@reduxjs/toolkit").ActionCreatorWithPayload<{
            endpointName: string;
            requestId: string;
            options: Subscribers[number];
        } & QuerySubstateIdentifier, `${string}/subscriptions/updateSubscriptionOptions`>;
        unsubscribeQueryResult: import("@reduxjs/toolkit").ActionCreatorWithPayload<{
            requestId: string;
        } & QuerySubstateIdentifier, `${string}/subscriptions/unsubscribeQueryResult`>;
        internal_getRTKQSubscriptions: import("@reduxjs/toolkit").ActionCreatorWithoutPayload<`${string}/subscriptions/internal_getRTKQSubscriptions`>;
        removeQueryResult: import("@reduxjs/toolkit").ActionCreatorWithPreparedPayload<[payload: QuerySubstateIdentifier], QuerySubstateIdentifier, `${string}/queries/removeQueryResult`, never, unknown>;
        queryResultPatched: import("@reduxjs/toolkit").ActionCreatorWithPreparedPayload<[payload: QuerySubstateIdentifier & {
            patches: readonly Patch[];
        }], QuerySubstateIdentifier & {
            patches: readonly Patch[];
        }, `${string}/queries/queryResultPatched`, never, unknown>;
        middlewareRegistered: import("@reduxjs/toolkit").ActionCreatorWithPayload<string, `${string}/config/middlewareRegistered`>;
    };
};
export type SliceActions = ReturnType<typeof buildSlice>['actions'];
