import * as _nextui_org_system from '@nextui-org/system';
import { UseListboxItemProps } from './use-listbox-item.js';
import './base/listbox-item-base.js';
import '@nextui-org/theme';
import '@react-aria/listbox';
import '@react-types/shared';
import '@nextui-org/aria-utils';
import 'react';
import 'tailwind-variants';
import '@react-stately/list';

interface ListboxItemProps<T extends object = object> extends UseListboxItemProps<T> {
}
/**
 * @internal
 */
declare const ListboxItem: _nextui_org_system.InternalForwardRefRenderFunction<"li", ListboxItemProps<object>, never>;

export { ListboxItemProps, ListboxItem as default };
