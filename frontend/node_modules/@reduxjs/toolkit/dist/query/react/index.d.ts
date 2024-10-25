import { reactHooksModule, reactHooksModuleName } from './module';
export * from '@reduxjs/toolkit/query';
export { ApiProvider } from './ApiProvider';
declare const createApi: import("@reduxjs/toolkit/query").CreateApi<typeof import("@reduxjs/toolkit/query").coreModuleName | typeof reactHooksModuleName>;
export type { TypedUseMutationResult, TypedUseQueryHookResult, TypedUseQueryStateResult, TypedUseQuerySubscriptionResult, TypedLazyQueryTrigger, TypedUseLazyQuery, TypedUseMutation, TypedMutationTrigger, TypedUseQueryState, TypedUseQuery, TypedUseQuerySubscription, TypedUseLazyQuerySubscription, } from './buildHooks';
export { createApi, reactHooksModule, reactHooksModuleName };
