import type { IdSelector, Comparer, EntityStateAdapter, EntityId } from './models';
export declare function findInsertIndex<T>(sortedItems: T[], item: T, comparisonFunction: Comparer<T>): number;
export declare function insert<T>(sortedItems: T[], item: T, comparisonFunction: Comparer<T>): T[];
export declare function createSortedStateAdapter<T, Id extends EntityId>(selectId: IdSelector<T, Id>, comparer: Comparer<T>): EntityStateAdapter<T, Id>;
