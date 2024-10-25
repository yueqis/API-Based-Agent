import { ItemProps } from '@nextui-org/aria-utils';
import { ReactNode } from 'react';

interface Props<T extends object = {}> extends Omit<ItemProps<"button", T>, "children" | "title"> {
    /**
     * The content of the component.
     */
    children?: ReactNode | null;
    /**
     * The title of the component.
     */
    title?: ReactNode | null;
    /**
     *  A string representation of the item's contents. Use this when the title is not readable.
     *  This will be used as native `title` attribute.
     * */
    titleValue?: string;
    /** Whether the tab should be disabled. */
    isDisabled?: boolean;
    /** Whether the tab selection should occur on press up instead of press down. */
    shouldSelectOnPressUp?: boolean;
}
type TabItemProps<T extends object = {}> = Props<T>;
declare const TabItemBase: <T extends object>(props: TabItemProps<T>) => JSX.Element;

export { TabItemProps, TabItemBase as default };
