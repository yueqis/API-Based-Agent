import type { EntityStateAdapter, IdSelector, EntityId } from './models';
export declare function createUnsortedStateAdapter<T, Id extends EntityId>(selectId: IdSelector<T, Id>): EntityStateAdapter<T, Id>;
