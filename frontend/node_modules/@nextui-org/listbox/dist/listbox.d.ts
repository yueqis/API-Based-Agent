import { Ref, ReactElement } from 'react';
import { UseListboxProps } from './use-listbox.js';
import 'tailwind-variants';
import '@nextui-org/system';
import '@react-types/shared';
import '@react-aria/listbox';
import '@nextui-org/theme';
import '@react-stately/list';
import '@nextui-org/react-utils';
import './listbox-item.js';
import './use-listbox-item.js';
import './base/listbox-item-base.js';
import '@nextui-org/aria-utils';

interface Props<T> extends UseListboxProps<T> {
}
type ListboxProps<T extends object = object> = Props<T> & {
    ref?: Ref<HTMLElement>;
};
declare const _default: <T extends object>(props: ListboxProps<T>) => ReactElement;

export { ListboxProps, _default as default };
