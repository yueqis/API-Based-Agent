import type { UnknownAction } from 'redux';
import type { ThunkMiddleware } from 'redux-thunk';
import type { ActionCreatorInvariantMiddlewareOptions } from './actionCreatorInvariantMiddleware';
import type { ImmutableStateInvariantMiddlewareOptions } from './immutableStateInvariantMiddleware';
import type { SerializableStateInvariantMiddlewareOptions } from './serializableStateInvariantMiddleware';
import type { ExcludeFromTuple } from './tsHelpers';
import { Tuple } from './utils';
interface ThunkOptions<E = any> {
    extraArgument: E;
}
interface GetDefaultMiddlewareOptions {
    thunk?: boolean | ThunkOptions;
    immutableCheck?: boolean | ImmutableStateInvariantMiddlewareOptions;
    serializableCheck?: boolean | SerializableStateInvariantMiddlewareOptions;
    actionCreatorCheck?: boolean | ActionCreatorInvariantMiddlewareOptions;
}
export type ThunkMiddlewareFor<S, O extends GetDefaultMiddlewareOptions = {}> = O extends {
    thunk: false;
} ? never : O extends {
    thunk: {
        extraArgument: infer E;
    };
} ? ThunkMiddleware<S, UnknownAction, E> : ThunkMiddleware<S, UnknownAction>;
export type GetDefaultMiddleware<S = any> = <O extends GetDefaultMiddlewareOptions = {
    thunk: true;
    immutableCheck: true;
    serializableCheck: true;
    actionCreatorCheck: true;
}>(options?: O) => Tuple<ExcludeFromTuple<[ThunkMiddlewareFor<S, O>], never>>;
export declare const buildGetDefaultMiddleware: <S = any>() => GetDefaultMiddleware<S>;
export {};
