import { DateValue } from '@internationalized/date';
import { Ref, ReactElement } from 'react';
import { UseDateRangePickerProps } from './use-date-range-picker.js';
import '@react-types/datepicker';
import 'tailwind-variants';
import '@nextui-org/date-input';
import '@nextui-org/button';
import '@nextui-org/calendar';
import '@nextui-org/popover';
import '@react-types/shared';
import '@react-stately/datepicker';
import './use-date-picker-base.js';
import '@nextui-org/system';
import '@nextui-org/theme';
import './date-range-picker-field.js';

interface Props<T extends DateValue> extends UseDateRangePickerProps<T> {
}
type DateRangePickerProps<T extends DateValue = DateValue> = Props<T> & {
    ref?: Ref<HTMLElement>;
};
declare const _default: <T extends DateValue>(props: DateRangePickerProps<T>) => ReactElement;

export { DateRangePickerProps, Props, _default as default };
