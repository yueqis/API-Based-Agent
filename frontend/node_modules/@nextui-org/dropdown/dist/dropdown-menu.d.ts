import { MenuProps } from '@nextui-org/menu';
import { Ref, ReactElement } from 'react';

interface Props<T extends object = object> extends Omit<MenuProps<T>, "menuProps"> {
}
type DropdownMenuProps<T extends object = object> = Props<T> & {
    ref?: Ref<HTMLElement>;
};
declare const _default: <T extends object>(props: DropdownMenuProps<T>) => ReactElement;

export { DropdownMenuProps, _default as default };
