import React, { ForwardedRef, MutableRefObject, ReactNode, HTMLAttributes, EffectCallback, RefObject, Dispatch } from "react";
import { AriaLabelingProps, DOMProps, LinkDOMProps, FocusableElement, Href, RouterOptions, Orientation } from "@react-types/shared";
export const useLayoutEffect: typeof React.useLayoutEffect;
/**
 * If a default is not provided, generate an id.
 * @param defaultId - Default component id.
 */
export function useId(defaultId?: string): string;
/**
 * Merges two ids.
 * Different ids will trigger a side-effect and re-render components hooked up with `useId`.
 */
export function mergeIds(idA: string, idB: string): string;
/**
 * Used to generate an id, and after render, check if that id is rendered so we know
 * if we can use it in places such as labelledby.
 * @param depArray - When to recalculate if the id is in the DOM.
 */
export function useSlotId(depArray?: ReadonlyArray<any>): string;
/**
 * Calls all functions in the order they were chained with the same arguments.
 */
export function chain(...callbacks: any[]): (...args: any[]) => void;
export const getOwnerDocument: (el: Element | null | undefined) => Document;
export const getOwnerWindow: (el: (Window & typeof global) | Element | null | undefined) => Window & typeof global;
interface Props {
    [key: string]: any;
}
type PropsArg = Props | null | undefined;
type TupleTypes<T> = {
    [P in keyof T]: T[P];
} extends {
    [key: number]: infer V;
} ? NullToObject<V> : never;
type NullToObject<T> = T extends (null | undefined) ? {} : T;
type UnionToIntersection<U> = (U extends any ? (k: U) => void : never) extends ((k: infer I) => void) ? I : never;
/**
 * Merges multiple props objects together. Event handlers are chained,
 * classNames are combined, and ids are deduplicated - different ids
 * will trigger a side-effect and re-render components hooked up with `useId`.
 * For all other props, the last prop object overrides all previous ones.
 * @param args - Multiple sets of props to merge together.
 */
export function mergeProps<T extends PropsArg[]>(...args: T): UnionToIntersection<TupleTypes<T>>;
/**
 * Merges multiple refs into one. Works with either callback or object refs.
 */
export function mergeRefs<T>(...refs: Array<ForwardedRef<T> | MutableRefObject<T>>): ForwardedRef<T>;
interface Options {
    /**
     * If labelling associated aria properties should be included in the filter.
     */
    labelable?: boolean;
    /** Whether the element is a link and should include DOM props for <a> elements. */
    isLink?: boolean;
    /**
     * A Set of other property names that should be included in the filter.
     */
    propNames?: Set<string>;
}
/**
 * Filters out all props that aren't valid DOM props or defined via override prop obj.
 * @param props - The component props to be filtered.
 * @param opts - Props to override.
 */
export function filterDOMProps(props: DOMProps & AriaLabelingProps & LinkDOMProps, opts?: Options): DOMProps & AriaLabelingProps;
export function focusWithoutScrolling(element: FocusableElement): void;
export function getOffset(element: any, reverse: any, orientation?: string): any;
export function isMac(): boolean;
export function isIPhone(): boolean;
export function isIPad(): boolean;
export function isIOS(): boolean;
export function isAppleDevice(): boolean;
export function isWebKit(): boolean;
export function isChrome(): any;
export function isAndroid(): any;
export function isFirefox(): any;
interface Router {
    isNative: boolean;
    open: (target: Element, modifiers: Modifiers, href: Href, routerOptions: RouterOptions | undefined) => void;
    useHref: (href: Href) => string;
}
interface RouterProviderProps {
    navigate: (path: Href, routerOptions: RouterOptions | undefined) => void;
    useHref?: (href: Href) => string;
    children: ReactNode;
}
/**
 * A RouterProvider accepts a `navigate` function from a framework or client side router,
 * and provides it to all nested React Aria links to enable client side navigation.
 */
export function RouterProvider(props: RouterProviderProps): React.JSX.Element;
export function useRouter(): Router;
interface Modifiers {
    metaKey?: boolean;
    ctrlKey?: boolean;
    altKey?: boolean;
    shiftKey?: boolean;
}
export function shouldClientNavigate(link: HTMLAnchorElement, modifiers: Modifiers): boolean;
export function openLink(target: HTMLAnchorElement, modifiers: Modifiers, setOpening?: boolean): void;
export function getSyntheticLinkProps(props: LinkDOMProps): {
    'data-href': string;
    'data-target': React.HTMLAttributeAnchorTarget;
    'data-rel': string;
    'data-download': string | boolean;
    'data-ping': string;
    'data-referrer-policy': React.HTMLAttributeReferrerPolicy;
};
export function useLinkProps(props: LinkDOMProps): {
    href: string;
    target: React.HTMLAttributeAnchorTarget;
    rel: string;
    download: string | boolean;
    ping: string;
    referrerPolicy: React.HTMLAttributeReferrerPolicy;
};
export function runAfterTransition(fn: () => void): void;
interface UseDrag1DProps {
    containerRef: MutableRefObject<HTMLElement>;
    reverse?: boolean;
    orientation?: Orientation;
    onHover?: (hovered: boolean) => void;
    onDrag?: (dragging: boolean) => void;
    onPositionChange?: (position: number) => void;
    onIncrement?: () => void;
    onDecrement?: () => void;
    onIncrementToMax?: () => void;
    onDecrementToMin?: () => void;
    onCollapseToggle?: () => void;
}
export function useDrag1D(props: UseDrag1DProps): HTMLAttributes<HTMLElement>;
interface GlobalListeners {
    addGlobalListener<K extends keyof DocumentEventMap>(el: EventTarget, type: K, listener: (this: Document, ev: DocumentEventMap[K]) => any, options?: boolean | AddEventListenerOptions): void;
    addGlobalListener(el: EventTarget, type: string, listener: EventListenerOrEventListenerObject, options?: boolean | AddEventListenerOptions): void;
    removeGlobalListener<K extends keyof DocumentEventMap>(el: EventTarget, type: K, listener: (this: Document, ev: DocumentEventMap[K]) => any, options?: boolean | EventListenerOptions): void;
    removeGlobalListener(el: EventTarget, type: string, listener: EventListenerOrEventListenerObject, options?: boolean | EventListenerOptions): void;
    removeAllGlobalListeners(): void;
}
export function useGlobalListeners(): GlobalListeners;
/**
 * Merges aria-label and aria-labelledby into aria-labelledby when both exist.
 * @param props - Aria label props.
 * @param defaultLabel - Default value for aria-label when not present.
 */
export function useLabels(props: DOMProps & AriaLabelingProps, defaultLabel?: string): DOMProps & AriaLabelingProps;
/**
 * Offers an object ref for a given callback ref or an object ref. Especially
 * helfpul when passing forwarded refs (created using `React.forwardRef`) to
 * React Aria hooks.
 *
 * @param forwardedRef The original ref intended to be used.
 * @returns An object ref that updates the given ref.
 * @see https://reactjs.org/docs/forwarding-refs.html
 */
export function useObjectRef<T>(forwardedRef?: ((instance: T | null) => void) | MutableRefObject<T | null> | null): MutableRefObject<T | null>;
export function useUpdateEffect(effect: EffectCallback, dependencies: any[]): void;
type useResizeObserverOptionsType<T> = {
    ref: RefObject<T | undefined> | undefined;
    onResize: () => void;
};
export function useResizeObserver<T extends Element>(options: useResizeObserverOptionsType<T>): void;
interface ContextValue<T> {
    ref?: MutableRefObject<T | null>;
}
export function useSyncRef<T>(context?: ContextValue<T> | null, ref?: RefObject<T>): void;
export function isScrollable(node: Element, checkForOverflow?: boolean): boolean;
export function getScrollParent(node: Element, checkForOverflow?: boolean): Element;
export function getScrollParents(node: Element, checkForOverflow?: boolean): Element[];
interface ViewportSize {
    width: number;
    height: number;
}
export function useViewportSize(): ViewportSize;
export function useDescription(description?: string): AriaLabelingProps;
export function useEffectEvent<T extends Function>(fn?: T): T;
export function useEvent<K extends keyof GlobalEventHandlersEventMap>(ref: RefObject<EventTarget>, event: K, handler?: (this: Document, ev: GlobalEventHandlersEventMap[K]) => any, options?: boolean | AddEventListenerOptions): void;
type SetValueAction<S> = (prev: S) => Generator<any, void, unknown>;
export function useValueEffect<S>(defaultValue: S | (() => S)): [S, Dispatch<SetValueAction<S>>];
interface ScrollIntoViewportOpts {
    /** The optional containing element of the target to be centered in the viewport. */
    containingElement?: Element;
}
/**
 * Scrolls `scrollView` so that `element` is visible.
 * Similar to `element.scrollIntoView({block: 'nearest'})` (not supported in Edge),
 * but doesn't affect parents above `scrollView`.
 */
export function scrollIntoView(scrollView: HTMLElement, element: HTMLElement): void;
/**
 * Scrolls the `targetElement` so it is visible in the viewport. Accepts an optional `opts.containingElement`
 * that will be centered in the viewport prior to scrolling the targetElement into view. If scrolling is prevented on
 * the body (e.g. targetElement is in a popover), this will only scroll the scroll parents of the targetElement up to but not including the body itself.
 */
export function scrollIntoViewport(targetElement: Element, opts?: ScrollIntoViewportOpts): void;
export function isVirtualClick(event: MouseEvent | PointerEvent): boolean;
export function isVirtualPointerEvent(event: PointerEvent): boolean;
export function useDeepMemo<T>(value: T, isEqual: (a: T, b: T) => boolean): T;
export function useFormReset<T>(ref: RefObject<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>, initialValue: T, onReset: (value: T) => void): void;
export { clamp, snapValueToStep } from '@react-stately/utils';

//# sourceMappingURL=types.d.ts.map
