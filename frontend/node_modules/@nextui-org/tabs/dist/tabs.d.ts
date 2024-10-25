import { Ref, ReactElement } from 'react';
import { UseTabsProps } from './use-tabs.js';
import '@nextui-org/system';
import '@nextui-org/theme';
import '@nextui-org/react-utils';
import '@react-stately/tabs';
import '@react-aria/tabs';
import '@nextui-org/aria-utils';
import 'framer-motion';

interface Props<T> extends UseTabsProps<T> {
}
type TabsProps<T extends object = object> = Props<T> & {
    ref?: Ref<HTMLElement>;
};
declare const _default: <T extends object>(props: TabsProps<T>) => ReactElement;

export { TabsProps, _default as default };
