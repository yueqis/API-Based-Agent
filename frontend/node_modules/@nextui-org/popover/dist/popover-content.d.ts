import * as _nextui_org_system from '@nextui-org/system';
import { HTMLNextUIProps } from '@nextui-org/system';
import { AriaDialogProps } from '@react-aria/dialog';
import { ReactNode, DOMAttributes } from 'react';

interface PopoverContentProps extends AriaDialogProps, Omit<HTMLNextUIProps, "children" | "role"> {
    children: ReactNode | ((titleProps: DOMAttributes<HTMLElement>) => ReactNode);
}
declare const PopoverContent: _nextui_org_system.InternalForwardRefRenderFunction<"div", PopoverContentProps, never>;

export { PopoverContentProps, PopoverContent as default };
