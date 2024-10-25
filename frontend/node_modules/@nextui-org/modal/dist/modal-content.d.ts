import * as _nextui_org_system from '@nextui-org/system';
import { HTMLNextUIProps } from '@nextui-org/system';
import { AriaDialogProps } from '@react-aria/dialog';
import { ReactNode } from 'react';

type KeysToOmit = "children" | "role";
interface ModalContentProps extends AriaDialogProps, HTMLNextUIProps<"div", KeysToOmit> {
    children: ReactNode | ((onClose: () => void) => ReactNode);
}
declare const ModalContent: _nextui_org_system.InternalForwardRefRenderFunction<"div", ModalContentProps, KeysToOmit>;

export { ModalContentProps, ModalContent as default };
