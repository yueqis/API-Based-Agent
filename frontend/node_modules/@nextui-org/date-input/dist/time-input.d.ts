import { TimeValue } from '@react-types/datepicker';
import { Ref, ReactElement } from 'react';
import { UseTimeInputProps } from './use-time-input.js';
import '@nextui-org/system';
import 'tailwind-variants';
import '@react-stately/datepicker';
import '@nextui-org/theme';
import '@nextui-org/react-utils';
import '@react-types/shared';
import './date-input-group.js';

interface Props<T extends TimeValue> extends UseTimeInputProps<T> {
}
type TimeInputProps<T extends TimeValue = TimeValue> = Props<T> & {
    ref?: Ref<HTMLElement>;
};
declare const _default: <T extends TimeValue>(props: TimeInputProps<T>) => ReactElement;

export { Props, TimeInputProps, _default as default };
