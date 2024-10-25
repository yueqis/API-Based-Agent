import { OverlayTriggerProps } from '@react-types/overlays';
import { CollectionBase, AsyncLoadable, InputBase, DOMProps, HelpTextProps, Validation, LabelableProps, TextInputBase, MultipleSelection, FocusableProps } from '@react-types/shared';
import { MenuTriggerState } from '@react-stately/menu';
import { FormValidationState } from '@react-stately/form';
import { MultiSelectListState } from './use-multiselect-list-state.js';
import '@react-stately/list';
import 'react';

interface MultiSelectProps<T> extends CollectionBase<T>, AsyncLoadable, Omit<InputBase, "isReadOnly">, DOMProps, HelpTextProps, Omit<Validation<T>, "validationBehavior" | "validate">, LabelableProps, TextInputBase, Omit<MultipleSelection, "none">, FocusableProps, OverlayTriggerProps {
    /**
     * Whether the menu should automatically flip direction when space is limited.
     * @default true
     */
    shouldFlip?: boolean;
}
interface MultiSelectState<T> extends MultiSelectListState<T>, MenuTriggerState, FormValidationState {
    /** Whether the select is currently focused. */
    isFocused: boolean;
    /** Sets whether the select is focused. */
    setFocused(isFocused: boolean): void;
}
declare function useMultiSelectState<T extends {}>(props: MultiSelectProps<T>): MultiSelectState<T>;

export { MultiSelectProps, MultiSelectState, useMultiSelectState };
