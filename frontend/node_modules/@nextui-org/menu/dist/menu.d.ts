import { Ref, ReactElement } from 'react';
import { UseMenuProps } from './use-menu.js';
import '@react-types/shared';
import '@nextui-org/system';
import '@react-types/menu';
import '@react-aria/menu';
import '@nextui-org/theme';
import '@react-stately/tree';
import '@nextui-org/react-utils';
import './menu-item.js';
import './use-menu-item.js';
import './base/menu-item-base.js';
import '@nextui-org/aria-utils';
import 'tailwind-variants';

interface Props<T> extends UseMenuProps<T> {
}
type MenuProps<T extends object = object> = Props<T> & {
    ref?: Ref<HTMLElement>;
};
declare const _default: <T extends object>(props: MenuProps<T>) => ReactElement;

export { MenuProps, _default as default };
