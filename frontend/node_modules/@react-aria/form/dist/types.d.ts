import { FormValidationState } from "@react-stately/form";
import { RefObject } from "react";
import { Validation } from "@react-types/shared";
type ValidatableElement = HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement;
interface FormValidationProps<T> extends Validation<T> {
    focus?: () => void;
}
export function useFormValidation<T>(props: FormValidationProps<T>, state: FormValidationState, ref: RefObject<ValidatableElement> | undefined): void;

//# sourceMappingURL=types.d.ts.map
