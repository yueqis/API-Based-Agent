import '@nextui-org/system-rsc';
import './types.js';
import { ModalProviderProps } from '@react-aria/overlays';
import { ProviderContextProps } from './provider-context.js';
import { I18nProviderProps } from '@react-aria/i18n';
import 'react';
import '@internationalized/date';

interface NextUIProviderProps extends Omit<ModalProviderProps, "children">, ProviderContextProps {
    children: React.ReactNode;
    /**
     * Controls whether `framer-motion` animations are skipped within the application.
     * This property is automatically enabled (`true`) when the `disableAnimation` prop is set to `true`,
     * effectively skipping all `framer-motion` animations. To retain `framer-motion` animations while
     * using the `disableAnimation` prop for other purposes, set this to `false`. However, note that
     * animations in NextUI Components are still omitted if the `disableAnimation` prop is `true`.
     */
    skipFramerMotionAnimations?: boolean;
    /**
     * The locale to apply to the children.
     * @default "en-US"
     */
    locale?: I18nProviderProps["locale"];
    /**
     * Provides a client side router to all nested components such as
     * Link, Menu, Tabs, Table, etc.
     */
    navigate?: (path: string) => void;
}
declare const NextUIProvider: React.FC<NextUIProviderProps>;

export { NextUIProvider, NextUIProviderProps };
