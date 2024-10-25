import { AnchorHTMLAttributes, ButtonHTMLAttributes, ElementType, HTMLAttributes, InputHTMLAttributes, RefObject } from "react";
import { AriaButtonProps, AriaToggleButtonProps } from "@react-types/button";
import { DOMAttributes } from "@react-types/shared";
import { ToggleState } from "@react-stately/toggle";
export interface AriaButtonOptions<E extends ElementType> extends Omit<AriaButtonProps<E>, 'children'> {
}
export interface ButtonAria<T> {
    /** Props for the button element. */
    buttonProps: T;
    /** Whether the button is currently pressed. */
    isPressed: boolean;
}
export function useButton(props: AriaButtonOptions<'button'>, ref: RefObject<HTMLButtonElement>): ButtonAria<ButtonHTMLAttributes<HTMLButtonElement>>;
export function useButton(props: AriaButtonOptions<'a'>, ref: RefObject<HTMLAnchorElement>): ButtonAria<AnchorHTMLAttributes<HTMLAnchorElement>>;
export function useButton(props: AriaButtonOptions<'div'>, ref: RefObject<HTMLDivElement>): ButtonAria<HTMLAttributes<HTMLDivElement>>;
export function useButton(props: AriaButtonOptions<'input'>, ref: RefObject<HTMLInputElement>): ButtonAria<InputHTMLAttributes<HTMLInputElement>>;
export function useButton(props: AriaButtonOptions<'span'>, ref: RefObject<HTMLSpanElement>): ButtonAria<HTMLAttributes<HTMLSpanElement>>;
export function useButton(props: AriaButtonOptions<ElementType>, ref: RefObject<Element>): ButtonAria<DOMAttributes>;
interface AriaToggleButtonOptions<E extends ElementType> extends Omit<AriaToggleButtonProps<E>, 'children'> {
}
export function useToggleButton(props: AriaToggleButtonOptions<'button'>, state: ToggleState, ref: RefObject<HTMLButtonElement>): ButtonAria<ButtonHTMLAttributes<HTMLButtonElement>>;
export function useToggleButton(props: AriaToggleButtonOptions<'a'>, state: ToggleState, ref: RefObject<HTMLAnchorElement>): ButtonAria<AnchorHTMLAttributes<HTMLAnchorElement>>;
export function useToggleButton(props: AriaToggleButtonOptions<'div'>, state: ToggleState, ref: RefObject<HTMLDivElement>): ButtonAria<HTMLAttributes<HTMLDivElement>>;
export function useToggleButton(props: AriaToggleButtonOptions<'input'>, state: ToggleState, ref: RefObject<HTMLInputElement>): ButtonAria<InputHTMLAttributes<HTMLInputElement>>;
export function useToggleButton(props: AriaToggleButtonOptions<'span'>, state: ToggleState, ref: RefObject<HTMLSpanElement>): ButtonAria<HTMLAttributes<HTMLSpanElement>>;
export function useToggleButton(props: AriaToggleButtonOptions<ElementType>, state: ToggleState, ref: RefObject<Element>): ButtonAria<DOMAttributes>;
export type { AriaButtonProps, AriaToggleButtonProps } from '@react-types/button';

//# sourceMappingURL=types.d.ts.map
