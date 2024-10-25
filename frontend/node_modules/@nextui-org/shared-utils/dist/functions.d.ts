type Args<T extends Function> = T extends (...args: infer R) => any ? R : never;
type AnyFunction<T = any> = (...args: T[]) => any;
type Extractable = {
    [key: string]: any;
} | undefined;
/**
 * Capitalizes the first letter of a string
 * @param {string} text
 * @returns {string}
 */
declare const capitalize: (text: string) => string;
declare function callAllHandlers<T extends (event: any) => void>(...fns: (T | undefined)[]): (event: Args<T>[0]) => void;
declare function callAll<T extends AnyFunction>(...fns: (T | undefined)[]): (arg: Args<T>[0]) => void;
declare function extractProperty<K extends keyof Extractable, D extends keyof Extractable>(key: K | string, defaultValue: D | string | boolean, ...objs: Extractable[]): string | boolean | D | Extractable[K];
declare function getUniqueID(prefix: string): string;
/**
 * This function removes all event handlers from an object.
 */
declare function removeEvents(input: {
    [key: string]: any;
}): {
    [key: string]: any;
};
declare function objectToDeps(obj: Extractable): string;

export { callAll, callAllHandlers, capitalize, extractProperty, getUniqueID, objectToDeps, removeEvents };
