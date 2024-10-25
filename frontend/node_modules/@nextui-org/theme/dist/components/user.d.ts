import * as tailwind_variants from 'tailwind-variants';
import * as tailwind_variants_dist_config from 'tailwind-variants/dist/config';
import * as tailwind_merge from 'tailwind-merge';

/**
 * User wrapper **Tailwind Variants** component
 *
 * const {base, wrapper, name, description} = user({...})
 *
 * @example
 * <div className={base())}>
 *   // avatar element @see avatar
 *  <div className={wrapper())}>
 *    <span className={name())}>user name</span>
 *    <span className={description())}>user description</span>
 *  </div>
 * </div>
 */
declare const user: tailwind_variants.TVReturnType<{
    [key: string]: {
        [key: string]: tailwind_merge.ClassNameValue | {
            base?: tailwind_merge.ClassNameValue;
            description?: tailwind_merge.ClassNameValue;
            name?: tailwind_merge.ClassNameValue;
            wrapper?: tailwind_merge.ClassNameValue;
        };
    };
} | {
    [x: string]: {
        [x: string]: tailwind_merge.ClassNameValue | {
            base?: tailwind_merge.ClassNameValue;
            description?: tailwind_merge.ClassNameValue;
            name?: tailwind_merge.ClassNameValue;
            wrapper?: tailwind_merge.ClassNameValue;
        };
    };
} | {}, {
    base: string[];
    wrapper: string;
    name: string;
    description: string;
}, undefined, tailwind_variants_dist_config.TVConfig<unknown, {
    [key: string]: {
        [key: string]: tailwind_merge.ClassNameValue | {
            base?: tailwind_merge.ClassNameValue;
            description?: tailwind_merge.ClassNameValue;
            name?: tailwind_merge.ClassNameValue;
            wrapper?: tailwind_merge.ClassNameValue;
        };
    };
} | {}>, {
    [key: string]: {
        [key: string]: tailwind_merge.ClassNameValue | {
            base?: tailwind_merge.ClassNameValue;
            description?: tailwind_merge.ClassNameValue;
            name?: tailwind_merge.ClassNameValue;
            wrapper?: tailwind_merge.ClassNameValue;
        };
    };
} | {}, {
    base: string[];
    wrapper: string;
    name: string;
    description: string;
}, tailwind_variants.TVReturnType<unknown, {
    base: string[];
    wrapper: string;
    name: string;
    description: string;
}, undefined, tailwind_variants_dist_config.TVConfig<unknown, {
    [key: string]: {
        [key: string]: tailwind_merge.ClassNameValue | {
            base?: tailwind_merge.ClassNameValue;
            description?: tailwind_merge.ClassNameValue;
            name?: tailwind_merge.ClassNameValue;
            wrapper?: tailwind_merge.ClassNameValue;
        };
    };
} | {}>, unknown, unknown, undefined>>;
type UserSlots = keyof ReturnType<typeof user>;

export { UserSlots, user };
