import { RefObject, ButtonHTMLAttributes, AnchorHTMLAttributes, HTMLAttributes, InputHTMLAttributes, ElementType } from 'react';
import { AriaToggleButtonProps } from '@react-types/button';
export { AriaToggleButtonProps } from '@react-types/button';
import { DOMAttributes } from '@react-types/shared';
import { ToggleState } from '@react-stately/toggle';
import { ButtonAria } from '@nextui-org/use-aria-button';

declare function useAriaToggleButton(props: AriaToggleButtonProps<"button">, state: ToggleState, ref: RefObject<HTMLButtonElement>): ButtonAria<ButtonHTMLAttributes<HTMLButtonElement>>;
declare function useAriaToggleButton(props: AriaToggleButtonProps<"a">, state: ToggleState, ref: RefObject<HTMLAnchorElement>): ButtonAria<AnchorHTMLAttributes<HTMLAnchorElement>>;
declare function useAriaToggleButton(props: AriaToggleButtonProps<"div">, state: ToggleState, ref: RefObject<HTMLDivElement>): ButtonAria<HTMLAttributes<HTMLDivElement>>;
declare function useAriaToggleButton(props: AriaToggleButtonProps<"input">, state: ToggleState, ref: RefObject<HTMLInputElement>): ButtonAria<InputHTMLAttributes<HTMLInputElement>>;
declare function useAriaToggleButton(props: AriaToggleButtonProps<"span">, state: ToggleState, ref: RefObject<HTMLSpanElement>): ButtonAria<HTMLAttributes<HTMLSpanElement>>;
declare function useAriaToggleButton(props: AriaToggleButtonProps<ElementType>, state: ToggleState, ref: RefObject<Element>): ButtonAria<DOMAttributes>;

export { useAriaToggleButton };
