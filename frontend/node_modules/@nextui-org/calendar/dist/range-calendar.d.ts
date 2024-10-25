import { DateValue } from '@internationalized/date';
import { Ref, ReactElement } from 'react';
import { UseRangeCalendarProps } from './use-range-calendar.js';
import '@nextui-org/theme';
import 'tailwind-variants';
import '@nextui-org/system';
import '@react-types/calendar';
import '@react-stately/calendar';
import './use-calendar-base.js';
import '@react-types/shared';
import '@react-aria/calendar';
import '@react-types/button';
import '@nextui-org/button';
import '@nextui-org/react-utils';
import './calendar-base.js';
import 'react/jsx-runtime';

interface Props<T extends DateValue> extends Omit<UseRangeCalendarProps<T>, "isHeaderExpanded" | "onHeaderExpandedChange" | "isHeaderWrapperExpanded" | "showMonthAndYearPickers"> {
}
type RangeCalendarProps<T extends DateValue = DateValue> = Props<T> & {
    ref?: Ref<HTMLElement>;
};
declare const _default: <T extends DateValue>(props: RangeCalendarProps<T>) => ReactElement;

export { RangeCalendarProps, _default as default };
