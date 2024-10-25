import type { InternalSerializeQueryArgs } from '../defaultSerializeQueryArgs';
import type { Api, ApiContext } from '../apiTypes';
import type { BaseQueryFn, BaseQueryError } from '../baseQueryTypes';
import type { RootState, QueryKeys, QuerySubstateIdentifier } from './apiState';
import type { StartQueryActionCreatorOptions, QueryActionCreatorResult } from './buildInitiate';
import type { AssertTagTypes, EndpointDefinition, EndpointDefinitions, MutationDefinition, QueryArgFrom, QueryDefinition, ResultTypeFrom, FullTagDescription } from '../endpointDefinitions';
import type { Draft, UnknownAction } from '@reduxjs/toolkit';
import { SHOULD_AUTOBATCH } from './rtkImports';
import type { Patch } from 'immer';
import type { ThunkAction, ThunkDispatch, AsyncThunk } from '@reduxjs/toolkit';
import type { PrefetchOptions } from './module';
import type { UnwrapPromise } from '../tsHelpers';
declare module './module' {
    interface ApiEndpointQuery<Definition extends QueryDefinition<any, any, any, any, any>, Definitions extends EndpointDefinitions> extends Matchers<QueryThunk, Definition> {
    }
    interface ApiEndpointMutation<Definition extends MutationDefinition<any, any, any, any, any>, Definitions extends EndpointDefinitions> extends Matchers<MutationThunk, Definition> {
    }
}
type EndpointThunk<Thunk extends QueryThunk | MutationThunk, Definition extends EndpointDefinition<any, any, any, any>> = Definition extends EndpointDefinition<infer QueryArg, infer BaseQueryFn, any, infer ResultType> ? Thunk extends AsyncThunk<unknown, infer ATArg, infer ATConfig> ? AsyncThunk<ResultType, ATArg & {
    originalArgs: QueryArg;
}, ATConfig & {
    rejectValue: BaseQueryError<BaseQueryFn>;
}> : never : never;
export type PendingAction<Thunk extends QueryThunk | MutationThunk, Definition extends EndpointDefinition<any, any, any, any>> = ReturnType<EndpointThunk<Thunk, Definition>['pending']>;
export type FulfilledAction<Thunk extends QueryThunk | MutationThunk, Definition extends EndpointDefinition<any, any, any, any>> = ReturnType<EndpointThunk<Thunk, Definition>['fulfilled']>;
export type RejectedAction<Thunk extends QueryThunk | MutationThunk, Definition extends EndpointDefinition<any, any, any, any>> = ReturnType<EndpointThunk<Thunk, Definition>['rejected']>;
export type Matcher<M> = (value: any) => value is M;
export interface Matchers<Thunk extends QueryThunk | MutationThunk, Definition extends EndpointDefinition<any, any, any, any>> {
    matchPending: Matcher<PendingAction<Thunk, Definition>>;
    matchFulfilled: Matcher<FulfilledAction<Thunk, Definition>>;
    matchRejected: Matcher<RejectedAction<Thunk, Definition>>;
}
export interface QueryThunkArg extends QuerySubstateIdentifier, StartQueryActionCreatorOptions {
    type: 'query';
    originalArgs: unknown;
    endpointName: string;
}
export interface MutationThunkArg {
    type: 'mutation';
    originalArgs: unknown;
    endpointName: string;
    track?: boolean;
    fixedCacheKey?: string;
}
export type ThunkResult = unknown;
export type ThunkApiMetaConfig = {
    pendingMeta: {
        startedTimeStamp: number;
        [SHOULD_AUTOBATCH]: true;
    };
    fulfilledMeta: {
        fulfilledTimeStamp: number;
        baseQueryMeta: unknown;
        [SHOULD_AUTOBATCH]: true;
    };
    rejectedMeta: {
        baseQueryMeta: unknown;
        [SHOULD_AUTOBATCH]: true;
    };
};
export type QueryThunk = AsyncThunk<ThunkResult, QueryThunkArg, ThunkApiMetaConfig>;
export type MutationThunk = AsyncThunk<ThunkResult, MutationThunkArg, ThunkApiMetaConfig>;
export type MaybeDrafted<T> = T | Draft<T>;
export type Recipe<T> = (data: MaybeDrafted<T>) => void | MaybeDrafted<T>;
export type UpsertRecipe<T> = (data: MaybeDrafted<T> | undefined) => void | MaybeDrafted<T>;
export type PatchQueryDataThunk<Definitions extends EndpointDefinitions, PartialState> = <EndpointName extends QueryKeys<Definitions>>(endpointName: EndpointName, args: QueryArgFrom<Definitions[EndpointName]>, patches: readonly Patch[], updateProvided?: boolean) => ThunkAction<void, PartialState, any, UnknownAction>;
export type UpdateQueryDataThunk<Definitions extends EndpointDefinitions, PartialState> = <EndpointName extends QueryKeys<Definitions>>(endpointName: EndpointName, args: QueryArgFrom<Definitions[EndpointName]>, updateRecipe: Recipe<ResultTypeFrom<Definitions[EndpointName]>>, updateProvided?: boolean) => ThunkAction<PatchCollection, PartialState, any, UnknownAction>;
export type UpsertQueryDataThunk<Definitions extends EndpointDefinitions, PartialState> = <EndpointName extends QueryKeys<Definitions>>(endpointName: EndpointName, args: QueryArgFrom<Definitions[EndpointName]>, value: ResultTypeFrom<Definitions[EndpointName]>) => ThunkAction<QueryActionCreatorResult<Definitions[EndpointName] extends QueryDefinition<any, any, any, any> ? Definitions[EndpointName] : never>, PartialState, any, UnknownAction>;
/**
 * An object returned from dispatching a `api.util.updateQueryData` call.
 */
export type PatchCollection = {
    /**
     * An `immer` Patch describing the cache update.
     */
    patches: Patch[];
    /**
     * An `immer` Patch to revert the cache update.
     */
    inversePatches: Patch[];
    /**
     * A function that will undo the cache update.
     */
    undo: () => void;
};
export declare function buildThunks<BaseQuery extends BaseQueryFn, ReducerPath extends string, Definitions extends EndpointDefinitions>({ reducerPath, baseQuery, context: { endpointDefinitions }, serializeQueryArgs, api, assertTagType, }: {
    baseQuery: BaseQuery;
    reducerPath: ReducerPath;
    context: ApiContext<Definitions>;
    serializeQueryArgs: InternalSerializeQueryArgs;
    api: Api<BaseQuery, Definitions, ReducerPath, any>;
    assertTagType: AssertTagTypes;
}): {
    queryThunk: AsyncThunk<unknown, QueryThunkArg, {
        pendingMeta: {
            startedTimeStamp: number;
            RTK_autoBatch: true;
        };
        fulfilledMeta: {
            fulfilledTimeStamp: number;
            baseQueryMeta: unknown;
            RTK_autoBatch: true;
        };
        rejectedMeta: {
            baseQueryMeta: unknown;
            RTK_autoBatch: true;
        };
        state: RootState<any, string, ReducerPath>;
        extra?: unknown;
        dispatch?: ThunkDispatch<unknown, unknown, UnknownAction> | undefined;
        rejectValue?: unknown;
        serializedErrorType?: unknown;
    }>;
    mutationThunk: AsyncThunk<unknown, MutationThunkArg, {
        pendingMeta: {
            startedTimeStamp: number;
            RTK_autoBatch: true;
        };
        fulfilledMeta: {
            fulfilledTimeStamp: number;
            baseQueryMeta: unknown;
            RTK_autoBatch: true;
        };
        rejectedMeta: {
            baseQueryMeta: unknown;
            RTK_autoBatch: true;
        };
        state: RootState<any, string, ReducerPath>;
        extra?: unknown;
        dispatch?: ThunkDispatch<unknown, unknown, UnknownAction> | undefined;
        rejectValue?: unknown;
        serializedErrorType?: unknown;
    }>;
    prefetch: <EndpointName extends QueryKeys<Definitions>>(endpointName: EndpointName, arg: any, options: PrefetchOptions) => ThunkAction<void, any, any, UnknownAction>;
    updateQueryData: UpdateQueryDataThunk<EndpointDefinitions, RootState<any, string, ReducerPath>>;
    upsertQueryData: UpsertQueryDataThunk<Definitions, RootState<any, string, ReducerPath>>;
    patchQueryData: PatchQueryDataThunk<EndpointDefinitions, RootState<any, string, ReducerPath>>;
    buildMatchThunkActions: <Thunk extends AsyncThunk<any, QueryThunkArg, ThunkApiMetaConfig> | AsyncThunk<any, MutationThunkArg, ThunkApiMetaConfig>>(thunk: Thunk, endpointName: string) => Matchers<Thunk, any>;
};
export declare function calculateProvidedByThunk(action: UnwrapPromise<ReturnType<ReturnType<QueryThunk>> | ReturnType<ReturnType<MutationThunk>>>, type: 'providesTags' | 'invalidatesTags', endpointDefinitions: EndpointDefinitions, assertTagType: AssertTagTypes): readonly FullTagDescription<string>[];
export {};
