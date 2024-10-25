export declare function getTimeMeasureUtils(maxDelay: number, fnName: string): {
    measureTime<T>(fn: () => T): T;
    warnIfExceeded(): void;
};
export declare function delay(ms: number): Promise<unknown>;
export declare function find<T>(iterable: Iterable<T>, comparator: (item: T) => boolean): T | undefined;
export declare class Tuple<Items extends ReadonlyArray<unknown> = []> extends Array<Items[number]> {
    constructor(length: number);
    constructor(...items: Items);
    static get [Symbol.species](): any;
    concat<AdditionalItems extends ReadonlyArray<unknown>>(items: Tuple<AdditionalItems>): Tuple<[...Items, ...AdditionalItems]>;
    concat<AdditionalItems extends ReadonlyArray<unknown>>(items: AdditionalItems): Tuple<[...Items, ...AdditionalItems]>;
    concat<AdditionalItems extends ReadonlyArray<unknown>>(...items: AdditionalItems): Tuple<[...Items, ...AdditionalItems]>;
    prepend<AdditionalItems extends ReadonlyArray<unknown>>(items: Tuple<AdditionalItems>): Tuple<[...AdditionalItems, ...Items]>;
    prepend<AdditionalItems extends ReadonlyArray<unknown>>(items: AdditionalItems): Tuple<[...AdditionalItems, ...Items]>;
    prepend<AdditionalItems extends ReadonlyArray<unknown>>(...items: AdditionalItems): Tuple<[...AdditionalItems, ...Items]>;
}
export declare function freezeDraftable<T>(val: T): T;
interface WeakMapEmplaceHandler<K extends object, V> {
    /**
     * Will be called to get value, if no value is currently in map.
     */
    insert?(key: K, map: WeakMap<K, V>): V;
    /**
     * Will be called to update a value, if one exists already.
     */
    update?(previous: V, key: K, map: WeakMap<K, V>): V;
}
interface MapEmplaceHandler<K, V> {
    /**
     * Will be called to get value, if no value is currently in map.
     */
    insert?(key: K, map: Map<K, V>): V;
    /**
     * Will be called to update a value, if one exists already.
     */
    update?(previous: V, key: K, map: Map<K, V>): V;
}
export declare function emplace<K, V>(map: Map<K, V>, key: K, handler: MapEmplaceHandler<K, V>): V;
export declare function emplace<K extends object, V>(map: WeakMap<K, V>, key: K, handler: WeakMapEmplaceHandler<K, V>): V;
export {};
