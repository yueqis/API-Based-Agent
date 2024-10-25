import { DateInputReturnType, SlotsToClasses, DateInputSlots } from '@nextui-org/theme';
import { DateValue, AriaDatePickerProps } from '@react-types/datepicker';
import { HTMLNextUIProps } from '@nextui-org/system';
import { DateInputProps } from '@nextui-org/date-input';
import { Ref, ReactElement } from 'react';

type NextUIBaseProps<T extends DateValue> = Omit<HTMLNextUIProps<"div">, keyof AriaDatePickerProps<T> | "onChange">;
interface Props<T extends DateValue> extends NextUIBaseProps<T>, AriaDatePickerProps<T>, Pick<DateInputProps, "createCalendar"> {
    /** DateInput classes slots. */
    slots: DateInputReturnType;
    /** DateInput classes. */
    classNames?: SlotsToClasses<DateInputSlots>;
}
type DateRangePickerFieldProps<T extends DateValue = DateValue> = Props<T> & {
    ref?: Ref<HTMLElement>;
};
declare const _default: <T extends DateValue>(props: DateRangePickerFieldProps<T>) => ReactElement;

export { DateRangePickerFieldProps, Props, _default as default };
