import { AriaTooltipProps, TooltipTriggerProps } from "@react-types/tooltip";
import { DOMAttributes, FocusableElement } from "@react-types/shared";
import { TooltipTriggerState } from "@react-stately/tooltip";
import { RefObject } from "react";
export interface TooltipAria {
    /**
     * Props for the tooltip element.
     */
    tooltipProps: DOMAttributes;
}
/**
 * Provides the accessibility implementation for a Tooltip component.
 */
export function useTooltip(props: AriaTooltipProps, state?: TooltipTriggerState): TooltipAria;
export interface TooltipTriggerAria {
    /**
     * Props for the trigger element.
     */
    triggerProps: DOMAttributes;
    /**
     * Props for the overlay container element.
     */
    tooltipProps: DOMAttributes;
}
/**
 * Provides the behavior and accessibility implementation for a tooltip trigger, e.g. a button
 * that shows a description when focused or hovered.
 */
export function useTooltipTrigger(props: TooltipTriggerProps, state: TooltipTriggerState, ref: RefObject<FocusableElement>): TooltipTriggerAria;
export type { AriaTooltipProps, TooltipTriggerProps } from '@react-types/tooltip';

//# sourceMappingURL=types.d.ts.map
