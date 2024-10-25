import type { CreateSelectorFunction } from 'reselect';
import type { EntityState, EntitySelectors, EntityId } from './models';
type AnyFunction = (...args: any) => any;
type AnyCreateSelectorFunction = CreateSelectorFunction<(<F extends AnyFunction>(f: F) => F), <F extends AnyFunction>(f: F) => F>;
export interface GetSelectorsOptions {
    createSelector?: AnyCreateSelectorFunction;
}
export declare function createSelectorsFactory<T, Id extends EntityId>(): {
    getSelectors: {
        (selectState?: undefined, options?: GetSelectorsOptions): EntitySelectors<T, EntityState<T, Id>, Id>;
        <V>(selectState: (state: V) => EntityState<T, Id>, options?: GetSelectorsOptions): EntitySelectors<T, V, Id>;
    };
};
export {};
