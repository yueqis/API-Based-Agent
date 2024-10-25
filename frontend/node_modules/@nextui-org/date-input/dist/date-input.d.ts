import { DateValue } from '@internationalized/date';
import { Ref, ReactElement } from 'react';
import { UseDateInputProps } from './use-date-input.js';
import '@nextui-org/system';
import 'tailwind-variants';
import '@react-stately/datepicker';
import '@nextui-org/theme';
import '@react-types/datepicker';
import '@nextui-org/react-utils';
import '@react-types/shared';
import './date-input-group.js';

interface Props<T extends DateValue> extends UseDateInputProps<T> {
}
type DateInputProps<T extends DateValue = DateValue> = Props<T> & {
    ref?: Ref<HTMLElement>;
};
declare const _default: <T extends DateValue>(props: DateInputProps<T>) => ReactElement;

export { DateInputProps, Props, _default as default };
