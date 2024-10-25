import * as _nextui_org_system from '@nextui-org/system';
import { UseMenuItemProps } from './use-menu-item.js';
import './base/menu-item-base.js';
import '@nextui-org/theme';
import '@react-aria/menu';
import '@react-types/shared';
import '@nextui-org/aria-utils';
import 'react';
import 'tailwind-variants';
import '@react-stately/tree';

interface MenuItemProps<T extends object = object> extends UseMenuItemProps<T> {
}
/**
 * @internal
 */
declare const MenuItem: _nextui_org_system.InternalForwardRefRenderFunction<"li", MenuItemProps<object>, never>;

export { MenuItemProps, MenuItem as default };
