import { AriaButtonProps } from "@react-types/button";
import { AriaComboBoxProps } from "@react-types/combobox";
import { AriaListBoxOptions } from "@react-aria/listbox";
import { DOMAttributes, KeyboardDelegate, ValidationResult } from "@react-types/shared";
import { ComboBoxState } from "@react-stately/combobox";
import { InputHTMLAttributes, RefObject } from "react";
export interface AriaComboBoxOptions<T> extends Omit<AriaComboBoxProps<T>, 'children'> {
    /** The ref for the input element. */
    inputRef: RefObject<HTMLInputElement>;
    /** The ref for the list box popover. */
    popoverRef: RefObject<Element>;
    /** The ref for the list box. */
    listBoxRef: RefObject<HTMLElement>;
    /** The ref for the optional list box popup trigger button.  */
    buttonRef?: RefObject<Element>;
    /** An optional keyboard delegate implementation, to override the default. */
    keyboardDelegate?: KeyboardDelegate;
}
export interface ComboBoxAria<T> extends ValidationResult {
    /** Props for the label element. */
    labelProps: DOMAttributes;
    /** Props for the combo box input element. */
    inputProps: InputHTMLAttributes<HTMLInputElement>;
    /** Props for the list box, to be passed to [useListBox](useListBox.html). */
    listBoxProps: AriaListBoxOptions<T>;
    /** Props for the optional trigger button, to be passed to [useButton](useButton.html). */
    buttonProps: AriaButtonProps;
    /** Props for the combo box description element, if any. */
    descriptionProps: DOMAttributes;
    /** Props for the combo box error message element, if any. */
    errorMessageProps: DOMAttributes;
}
/**
 * Provides the behavior and accessibility implementation for a combo box component.
 * A combo box combines a text input with a listbox, allowing users to filter a list of options to items matching a query.
 * @param props - Props for the combo box.
 * @param state - State for the select, as returned by `useComboBoxState`.
 */
export function useComboBox<T>(props: AriaComboBoxOptions<T>, state: ComboBoxState<T>): ComboBoxAria<T>;
export type { AriaComboBoxProps } from '@react-types/combobox';

//# sourceMappingURL=types.d.ts.map
