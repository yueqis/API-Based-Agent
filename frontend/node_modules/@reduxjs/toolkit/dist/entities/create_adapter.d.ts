import type { EntityAdapter, EntityId, EntityAdapterOptions } from './models';
import type { WithRequiredProp } from '../tsHelpers';
export declare function createEntityAdapter<T, Id extends EntityId>(options: WithRequiredProp<EntityAdapterOptions<T, Id>, 'selectId'>): EntityAdapter<T, Id>;
export declare function createEntityAdapter<T extends {
    id: EntityId;
}>(options?: Omit<EntityAdapterOptions<T, T['id']>, 'selectId'>): EntityAdapter<T, T['id']>;
