import type { Draft } from 'immer';
import type { EntityId, DraftableEntityState, PreventAny } from './models';
import type { PayloadAction } from '../createAction';
export declare const isDraftTyped: <T>(value: T | Draft<T>) => value is Draft<T>;
export declare function createSingleArgumentStateOperator<T, Id extends EntityId>(mutator: (state: DraftableEntityState<T, Id>) => void): <S extends DraftableEntityState<T, Id>>(state: PreventAny<S, T, Id>) => S;
export declare function createStateOperator<T, Id extends EntityId, R>(mutator: (arg: R, state: DraftableEntityState<T, Id>) => void): <S extends DraftableEntityState<T, Id>>(state: S, arg: R | PayloadAction<R>) => S;
