import type { InternalHandlerBuilder, SubscriptionSelectors } from './types';
export declare const buildBatchedActionsHandler: InternalHandlerBuilder<[
    actionShouldContinue: boolean,
    returnValue: SubscriptionSelectors | boolean
]>;
