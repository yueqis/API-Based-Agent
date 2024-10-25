import { Ref, ReactElement } from 'react';
import { UseAutocompleteProps } from './use-autocomplete.js';
import 'tailwind-variants';
import '@react-stately/combobox';
import '@nextui-org/system';
import '@nextui-org/theme';
import '@nextui-org/react-utils';
import '@react-types/combobox';
import '@nextui-org/popover';
import '@nextui-org/listbox';
import '@nextui-org/input';
import '@nextui-org/scroll-shadow';
import '@nextui-org/button';
import '@react-types/shared';

interface Props<T> extends UseAutocompleteProps<T> {
}
type AutocompleteProps<T extends object = object> = Props<T> & {
    ref?: Ref<HTMLElement>;
};
declare const _default: <T extends object>(props: AutocompleteProps<T>) => ReactElement;

export { AutocompleteProps, _default as default };
