import * as _nextui_org_menu from '@nextui-org/menu';
import * as _react_types_shared from '@react-types/shared';
import * as _react_aria_menu from '@react-aria/menu';
import * as react from 'react';
import * as _nextui_org_system from '@nextui-org/system';

declare const DropdownProvider: react.Provider<{
    Component: _nextui_org_system.As<any>;
    menuRef: react.RefObject<HTMLUListElement>;
    menuProps: _react_aria_menu.AriaMenuOptions<object>;
    classNames: string;
    closeOnSelect: boolean;
    onClose: () => void;
    autoFocus: _react_types_shared.FocusStrategy;
    disableAnimation: boolean;
    getPopoverProps: _nextui_org_system.PropGetter<Record<string, unknown>, _nextui_org_system.DOMAttributes<_nextui_org_system.DOMElement>>;
    getMenuProps: <T extends object>(props?: Partial<_nextui_org_menu.MenuProps<T>> | undefined, _ref?: react.Ref<any> | undefined) => _nextui_org_menu.MenuProps<object>;
    getMenuTriggerProps: _nextui_org_system.PropGetter<Record<string, unknown>, _nextui_org_system.DOMAttributes<_nextui_org_system.DOMElement>>;
}>;
declare const useDropdownContext: () => {
    Component: _nextui_org_system.As<any>;
    menuRef: react.RefObject<HTMLUListElement>;
    menuProps: _react_aria_menu.AriaMenuOptions<object>;
    classNames: string;
    closeOnSelect: boolean;
    onClose: () => void;
    autoFocus: _react_types_shared.FocusStrategy;
    disableAnimation: boolean;
    getPopoverProps: _nextui_org_system.PropGetter<Record<string, unknown>, _nextui_org_system.DOMAttributes<_nextui_org_system.DOMElement>>;
    getMenuProps: <T extends object>(props?: Partial<_nextui_org_menu.MenuProps<T>> | undefined, _ref?: react.Ref<any> | undefined) => _nextui_org_menu.MenuProps<object>;
    getMenuTriggerProps: _nextui_org_system.PropGetter<Record<string, unknown>, _nextui_org_system.DOMAttributes<_nextui_org_system.DOMElement>>;
};

export { DropdownProvider, useDropdownContext };
