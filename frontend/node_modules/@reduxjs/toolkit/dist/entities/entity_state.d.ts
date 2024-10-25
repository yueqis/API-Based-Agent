import type { EntityId, EntityState, EntityStateAdapter, EntityStateFactory } from './models';
export declare function getInitialEntityState<T, Id extends EntityId>(): EntityState<T, Id>;
export declare function createInitialStateFactory<T, Id extends EntityId>(stateAdapter: EntityStateAdapter<T, Id>): EntityStateFactory<T, Id>;
