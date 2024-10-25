import type { Middleware, ThunkDispatch, UnknownAction } from '@reduxjs/toolkit';
import type { EndpointDefinitions, FullTagDescription } from '../../endpointDefinitions';
import type { RootState } from '../apiState';
import type { BuildMiddlewareInput } from './types';
export declare function buildMiddleware<Definitions extends EndpointDefinitions, ReducerPath extends string, TagTypes extends string>(input: BuildMiddlewareInput<Definitions, ReducerPath, TagTypes>): {
    middleware: Middleware<{}, RootState<Definitions, string, ReducerPath>, ThunkDispatch<any, any, UnknownAction>>;
    actions: {
        invalidateTags: import("@reduxjs/toolkit").ActionCreatorWithPayload<(TagTypes | FullTagDescription<TagTypes>)[], string>;
    };
};
