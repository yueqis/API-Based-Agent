import * as _react_types_shared from '@react-types/shared';
import * as _react_aria_menu from '@react-aria/menu';
import * as react from 'react';
import { Ref } from 'react';
import * as _nextui_org_system from '@nextui-org/system';
import { PropGetter, HTMLNextUIProps } from '@nextui-org/system';
import { PopoverProps } from '@nextui-org/popover';
import { MenuTriggerType } from '@react-types/menu';
import { ReactRef } from '@nextui-org/react-utils';
import { MenuProps } from '@nextui-org/menu';

interface Props extends HTMLNextUIProps<"div"> {
    /**
     * Type of overlay that is opened by the trigger.
     */
    type?: "menu" | "listbox";
    /**
     * Ref to the DOM node.
     */
    ref?: ReactRef<HTMLElement | null>;
    /**
     * How the menu is triggered.
     * @default 'press'
     */
    trigger?: MenuTriggerType;
    /**
     * Whether menu trigger is disabled.
     * @default false
     */
    isDisabled?: boolean;
    /**
     * Whether the Menu closes when a selection is made.
     * @default true
     */
    closeOnSelect?: boolean;
}
type UseDropdownProps = Props & Omit<PopoverProps, "children" | "color" | "variant">;
declare function useDropdown(props: UseDropdownProps): {
    Component: _nextui_org_system.As<any>;
    menuRef: react.RefObject<HTMLUListElement>;
    menuProps: _react_aria_menu.AriaMenuOptions<object>;
    classNames: string;
    closeOnSelect: boolean;
    onClose: () => void;
    autoFocus: _react_types_shared.FocusStrategy;
    disableAnimation: boolean;
    getPopoverProps: PropGetter<Record<string, unknown>, _nextui_org_system.DOMAttributes<_nextui_org_system.DOMElement>>;
    getMenuProps: <T extends object>(props?: Partial<MenuProps<T>> | undefined, _ref?: Ref<any> | null | undefined) => MenuProps<object>;
    getMenuTriggerProps: PropGetter<Record<string, unknown>, _nextui_org_system.DOMAttributes<_nextui_org_system.DOMElement>>;
};
type UseDropdownReturn = ReturnType<typeof useDropdown>;

export { UseDropdownProps, UseDropdownReturn, useDropdown };
