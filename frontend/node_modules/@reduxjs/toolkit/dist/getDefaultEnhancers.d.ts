import type { StoreEnhancer } from 'redux';
import type { AutoBatchOptions } from './autoBatchEnhancer';
import { Tuple } from './utils';
import type { Middlewares } from './configureStore';
import type { ExtractDispatchExtensions } from './tsHelpers';
type GetDefaultEnhancersOptions = {
    autoBatch?: boolean | AutoBatchOptions;
};
export type GetDefaultEnhancers<M extends Middlewares<any>> = (options?: GetDefaultEnhancersOptions) => Tuple<[StoreEnhancer<{
    dispatch: ExtractDispatchExtensions<M>;
}>]>;
export declare const buildGetDefaultEnhancers: <M extends Middlewares<any>>(middlewareEnhancer: StoreEnhancer<{
    dispatch: ExtractDispatchExtensions<M>;
}>) => GetDefaultEnhancers<M>;
export {};
