import { DOMAttributes, DOMProps, PressEvents, HoverEvents, KeyboardEvents, FocusEvents, Key, FocusableElement } from '@react-types/shared';
import { RefObject } from 'react';
import { TreeState } from '@react-stately/tree';

interface MenuItemAria {
    /** Props for the menu item element. */
    menuItemProps: DOMAttributes;
    /** Props for the main text element inside the menu item. */
    labelProps: DOMAttributes;
    /** Props for the description text element inside the menu item, if any. */
    descriptionProps: DOMAttributes;
    /** Props for the keyboard shortcut text element inside the item, if any. */
    keyboardShortcutProps: DOMAttributes;
    /** Whether the item is currently hovered. */
    isHovered: boolean;
    /** Whether the item is currently focused. */
    isFocused: boolean;
    /** Whether the item is currently selected. */
    isSelected: boolean;
    /** Whether the item is currently in a pressed state. */
    isPressed: boolean;
    /** Whether the item is disabled. */
    isDisabled: boolean;
}
interface AriaMenuItemProps extends DOMProps, PressEvents, HoverEvents, KeyboardEvents, FocusEvents {
    /**
     * Whether the menu item is disabled.
     * @deprecated - pass disabledKeys to useTreeState instead.
     */
    isDisabled?: boolean;
    /**
     * Whether the menu item is selected.
     * @deprecated - pass selectedKeys to useTreeState instead.
     */
    isSelected?: boolean;
    /** A screen reader only label for the menu item. */
    "aria-label"?: string;
    /** The unique key for the menu item. */
    key?: Key;
    /**
     * Handler that is called when the menu should close after selecting an item.
     * @deprecated - pass to the menu instead.
     */
    onClose?: () => void;
    /**
     * Whether the menu should close when the menu item is selected.
     * @default true
     */
    closeOnSelect?: boolean;
    /** Whether the menu item is contained in a virtual scrolling menu. */
    isVirtualized?: boolean;
    /**
     * Handler that is called when the user activates the item.
     * @deprecated - pass to the menu instead.
     */
    onAction?: (key: Key) => void;
    /**
     * The native button click event handler
     * @deprecated - use `onAction` instead.
     */
    onClick?: DOMAttributes["onClick"];
    /** What kind of popup the item opens. */
    "aria-haspopup"?: "menu" | "dialog";
    /** Indicates whether the menu item's popup element is expanded or collapsed. */
    "aria-expanded"?: boolean | "true" | "false";
    /** Identifies the menu item's popup element whose contents or presence is controlled by the menu item. */
    "aria-controls"?: string;
}
/**
 * Provides the behavior and accessibility implementation for an item in a menu.
 * See `useMenu` for more details about menus.
 * @param props - Props for the item.
 * @param state - State for the menu, as returned by `useTreeState`.
 */
declare function useMenuItem<T>(props: AriaMenuItemProps, state: TreeState<T>, ref: RefObject<FocusableElement>): MenuItemAria;

export { AriaMenuItemProps, MenuItemAria, useMenuItem };
