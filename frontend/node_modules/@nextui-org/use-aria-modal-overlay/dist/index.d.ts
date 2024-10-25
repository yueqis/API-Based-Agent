import { AriaModalOverlayProps, ModalOverlayAria } from '@react-aria/overlays';
import { OverlayTriggerState } from '@react-stately/overlays';
import { RefObject } from 'react';

interface UseAriaModalOverlayProps extends AriaModalOverlayProps {
}
declare function useAriaModalOverlay(props: (UseAriaModalOverlayProps & {
    shouldBlockScroll?: boolean | undefined;
}) | undefined, state: OverlayTriggerState, ref: RefObject<HTMLElement>): ModalOverlayAria;
type UseAriaModalOverlayReturn = ReturnType<typeof useAriaModalOverlay>;

export { UseAriaModalOverlayProps, UseAriaModalOverlayReturn, useAriaModalOverlay };
