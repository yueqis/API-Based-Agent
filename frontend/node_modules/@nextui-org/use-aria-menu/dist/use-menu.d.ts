import { AriaMenuProps } from '@react-types/menu';
import { DOMAttributes, KeyboardEvents, KeyboardDelegate, Key } from '@react-types/shared';
import { RefObject } from 'react';
import { TreeState } from '@react-stately/tree';

interface MenuAria {
    /** Props for the menu element. */
    menuProps: DOMAttributes;
}
interface AriaMenuOptions<T> extends Omit<AriaMenuProps<T>, "children">, KeyboardEvents {
    /** Whether the menu uses virtual scrolling. */
    isVirtualized?: boolean;
    /**
     * An optional keyboard delegate implementation for type to select,
     * to override the default.
     */
    keyboardDelegate?: KeyboardDelegate;
}
interface MenuData {
    onClose?: () => void;
    onAction?: (key: Key) => void;
}
declare const menuData: WeakMap<TreeState<unknown>, MenuData>;
/**
 * Provides the behavior and accessibility implementation for a menu component.
 * A menu displays a list of actions or options that a user can choose.
 * @param props - Props for the menu.
 * @param state - State for the menu, as returned by `useListState`.
 */
declare function useMenu<T>(props: AriaMenuOptions<T>, state: TreeState<T>, ref: RefObject<HTMLElement>): MenuAria;

export { AriaMenuOptions, MenuAria, menuData, useMenu };
