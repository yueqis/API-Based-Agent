import { DateValue } from '@internationalized/date';
import { Ref, ReactElement } from 'react';
import { UseDatePickerProps } from './use-date-picker.js';
import '@nextui-org/date-input';
import '@react-stately/datepicker';
import '@nextui-org/button';
import '@nextui-org/calendar';
import '@nextui-org/popover';
import './use-date-picker-base.js';
import '@react-types/datepicker';
import '@nextui-org/system';
import '@react-types/shared';
import '@nextui-org/theme';
import '@react-aria/datepicker';

interface Props<T extends DateValue> extends UseDatePickerProps<T> {
}
type DatePickerProps<T extends DateValue = DateValue> = Props<T> & {
    ref?: Ref<HTMLElement>;
};
declare const _default: <T extends DateValue>(props: DatePickerProps<T>) => ReactElement;

export { DatePickerProps, Props, _default as default };
