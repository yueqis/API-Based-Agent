import type { UnknownAction, Reducer, StateFromReducersMapObject } from 'redux';
import type { Id, NonUndefined, Tail, UnionToIntersection, WithOptionalProp } from './tsHelpers';
type SliceLike<ReducerPath extends string, State> = {
    reducerPath: ReducerPath;
    reducer: Reducer<State>;
};
type AnySliceLike = SliceLike<string, any>;
type SliceLikeReducerPath<A extends AnySliceLike> = A extends SliceLike<infer ReducerPath, any> ? ReducerPath : never;
type SliceLikeState<A extends AnySliceLike> = A extends SliceLike<any, infer State> ? State : never;
export type WithSlice<A extends AnySliceLike> = {
    [Path in SliceLikeReducerPath<A>]: SliceLikeState<A>;
};
type ReducerMap = Record<string, Reducer>;
type ExistingSliceLike<DeclaredState> = {
    [ReducerPath in keyof DeclaredState]: SliceLike<ReducerPath & string, NonUndefined<DeclaredState[ReducerPath]>>;
}[keyof DeclaredState];
export type InjectConfig = {
    /**
     * Allow replacing reducer with a different reference. Normally, an error will be thrown if a different reducer instance to the one already injected is used.
     */
    overrideExisting?: boolean;
};
/**
 * A reducer that allows for slices/reducers to be injected after initialisation.
 */
export interface CombinedSliceReducer<InitialState, DeclaredState = InitialState> extends Reducer<DeclaredState, UnknownAction, Partial<DeclaredState>> {
    /**
     * Provide a type for slices that will be injected lazily.
     *
     * One way to do this would be with interface merging:
     * ```ts
     *
     * export interface LazyLoadedSlices {}
     *
     * export const rootReducer = combineSlices(stringSlice).withLazyLoadedSlices<LazyLoadedSlices>();
     *
     * // elsewhere
     *
     * declare module './reducer' {
     *   export interface LazyLoadedSlices extends WithSlice<typeof booleanSlice> {}
     * }
     *
     * const withBoolean = rootReducer.inject(booleanSlice);
     *
     * // elsewhere again
     *
     * declare module './reducer' {
     *   export interface LazyLoadedSlices {
     *     customName: CustomState
     *   }
     * }
     *
     * const withCustom = rootReducer.inject({ reducerPath: "customName", reducer: customSlice.reducer })
     * ```
     */
    withLazyLoadedSlices<Lazy = {}>(): CombinedSliceReducer<InitialState, Id<DeclaredState & Partial<Lazy>>>;
    /**
     * Inject a slice.
     *
     * Accepts an individual slice, RTKQ API instance, or a "slice-like" { reducerPath, reducer } object.
     *
     * ```ts
     * rootReducer.inject(booleanSlice)
     * rootReducer.inject(baseApi)
     * rootReducer.inject({ reducerPath: 'boolean' as const, reducer: newReducer }, { overrideExisting: true })
     * ```
     *
     */
    inject<Sl extends Id<ExistingSliceLike<DeclaredState>>>(slice: Sl, config?: InjectConfig): CombinedSliceReducer<InitialState, Id<DeclaredState & WithSlice<Sl>>>;
    /**
     * Inject a slice.
     *
     * Accepts an individual slice, RTKQ API instance, or a "slice-like" { reducerPath, reducer } object.
     *
     * ```ts
     * rootReducer.inject(booleanSlice)
     * rootReducer.inject(baseApi)
     * rootReducer.inject({ reducerPath: 'boolean' as const, reducer: newReducer }, { overrideExisting: true })
     * ```
     *
     */
    inject<ReducerPath extends string, State>(slice: SliceLike<ReducerPath, State & (ReducerPath extends keyof DeclaredState ? never : State)>, config?: InjectConfig): CombinedSliceReducer<InitialState, Id<DeclaredState & WithSlice<SliceLike<ReducerPath, State>>>>;
    /**
     * Create a selector that guarantees that the slices injected will have a defined value when selector is run.
     *
     * ```ts
     * const selectBooleanWithoutInjection = (state: RootState) => state.boolean;
     * //                                                                ^? boolean | undefined
     *
     * const selectBoolean = rootReducer.inject(booleanSlice).selector((state) => {
     *   // if action hasn't been dispatched since slice was injected, this would usually be undefined
     *   // however selector() uses a Proxy around the first parameter to ensure that it evaluates to the initial state instead, if undefined
     *   return state.boolean;
     *   //           ^? boolean
     * })
     * ```
     *
     * If the reducer is nested inside the root state, a selectState callback can be passed to retrieve the reducer's state.
     *
     * ```ts
     *
     * export interface LazyLoadedSlices {};
     *
     * export const innerReducer = combineSlices(stringSlice).withLazyLoadedSlices<LazyLoadedSlices>();
     *
     * export const rootReducer = combineSlices({ inner: innerReducer });
     *
     * export type RootState = ReturnType<typeof rootReducer>;
     *
     * // elsewhere
     *
     * declare module "./reducer.ts" {
     *  export interface LazyLoadedSlices extends WithSlice<typeof booleanSlice> {}
     * }
     *
     * const withBool = innerReducer.inject(booleanSlice);
     *
     * const selectBoolean = withBool.selector(
     *   (state) => state.boolean,
     *   (rootState: RootState) => state.inner
     * );
     * //    now expects to be passed RootState instead of innerReducer state
     *
     * ```
     *
     * Value passed to selectorFn will be a Proxy - use selector.original(proxy) to get original state value (useful for debugging)
     *
     * ```ts
     * const injectedReducer = rootReducer.inject(booleanSlice);
     * const selectBoolean = injectedReducer.selector((state) => {
     *   console.log(injectedReducer.selector.original(state).boolean) // possibly undefined
     *   return state.boolean
     * })
     * ```
     */
    selector: {
        /**
         * Create a selector that guarantees that the slices injected will have a defined value when selector is run.
         *
         * ```ts
         * const selectBooleanWithoutInjection = (state: RootState) => state.boolean;
         * //                                                                ^? boolean | undefined
         *
         * const selectBoolean = rootReducer.inject(booleanSlice).selector((state) => {
         *   // if action hasn't been dispatched since slice was injected, this would usually be undefined
         *   // however selector() uses a Proxy around the first parameter to ensure that it evaluates to the initial state instead, if undefined
         *   return state.boolean;
         *   //           ^? boolean
         * })
         * ```
         *
         * Value passed to selectorFn will be a Proxy - use selector.original(proxy) to get original state value (useful for debugging)
         *
         * ```ts
         * const injectedReducer = rootReducer.inject(booleanSlice);
         * const selectBoolean = injectedReducer.selector((state) => {
         *   console.log(injectedReducer.selector.original(state).boolean) // undefined
         *   return state.boolean
         * })
         * ```
         */
        <Selector extends (state: DeclaredState, ...args: any[]) => unknown>(selectorFn: Selector): (state: WithOptionalProp<Parameters<Selector>[0], Exclude<keyof DeclaredState, keyof InitialState>>, ...args: Tail<Parameters<Selector>>) => ReturnType<Selector>;
        /**
         * Create a selector that guarantees that the slices injected will have a defined value when selector is run.
         *
         * ```ts
         * const selectBooleanWithoutInjection = (state: RootState) => state.boolean;
         * //                                                                ^? boolean | undefined
         *
         * const selectBoolean = rootReducer.inject(booleanSlice).selector((state) => {
         *   // if action hasn't been dispatched since slice was injected, this would usually be undefined
         *   // however selector() uses a Proxy around the first parameter to ensure that it evaluates to the initial state instead, if undefined
         *   return state.boolean;
         *   //           ^? boolean
         * })
         * ```
         *
         * If the reducer is nested inside the root state, a selectState callback can be passed to retrieve the reducer's state.
         *
         * ```ts
         *
         * interface LazyLoadedSlices {};
         *
         * const innerReducer = combineSlices(stringSlice).withLazyLoadedSlices<LazyLoadedSlices>();
         *
         * const rootReducer = combineSlices({ inner: innerReducer });
         *
         * type RootState = ReturnType<typeof rootReducer>;
         *
         * // elsewhere
         *
         * declare module "./reducer.ts" {
         *  interface LazyLoadedSlices extends WithSlice<typeof booleanSlice> {}
         * }
         *
         * const withBool = innerReducer.inject(booleanSlice);
         *
         * const selectBoolean = withBool.selector(
         *   (state) => state.boolean,
         *   (rootState: RootState) => state.inner
         * );
         * //    now expects to be passed RootState instead of innerReducer state
         *
         * ```
         *
         * Value passed to selectorFn will be a Proxy - use selector.original(proxy) to get original state value (useful for debugging)
         *
         * ```ts
         * const injectedReducer = rootReducer.inject(booleanSlice);
         * const selectBoolean = injectedReducer.selector((state) => {
         *   console.log(injectedReducer.selector.original(state).boolean) // possibly undefined
         *   return state.boolean
         * })
         * ```
         */
        <Selector extends (state: DeclaredState, ...args: any[]) => unknown, RootState>(selectorFn: Selector, selectState: (rootState: RootState, ...args: Tail<Parameters<Selector>>) => WithOptionalProp<Parameters<Selector>[0], Exclude<keyof DeclaredState, keyof InitialState>>): (state: RootState, ...args: Tail<Parameters<Selector>>) => ReturnType<Selector>;
        /**
         * Returns the unproxied state. Useful for debugging.
         * @param state state Proxy, that ensures injected reducers have value
         * @returns original, unproxied state
         * @throws if value passed is not a state Proxy
         */
        original: (state: DeclaredState) => InitialState & Partial<DeclaredState>;
    };
}
type InitialState<Slices extends Array<AnySliceLike | ReducerMap>> = UnionToIntersection<Slices[number] extends infer Slice ? Slice extends AnySliceLike ? WithSlice<Slice> : StateFromReducersMapObject<Slice> : never>;
export declare function combineSlices<Slices extends Array<AnySliceLike | ReducerMap>>(...slices: Slices): CombinedSliceReducer<Id<InitialState<Slices>>>;
export {};
