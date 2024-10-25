import type { IdSelector, Update, EntityId, DraftableEntityState } from './models';
export declare function selectIdValue<T, Id extends EntityId>(entity: T, selectId: IdSelector<T, Id>): Id;
export declare function ensureEntitiesArray<T, Id extends EntityId>(entities: readonly T[] | Record<Id, T>): readonly T[];
export declare function getCurrent<T>(value: T): T;
export declare function splitAddedUpdatedEntities<T, Id extends EntityId>(newEntities: readonly T[] | Record<Id, T>, selectId: IdSelector<T, Id>, state: DraftableEntityState<T, Id>): [T[], Update<T, Id>[], Id[]];
