var $2jyrz$reactariautils = require("@react-aria/utils");
var $2jyrz$reactariafocus = require("@react-aria/focus");
var $2jyrz$reactariainteractions = require("@react-aria/interactions");


function $parcel$export(e, n, v, s) {
  Object.defineProperty(e, n, {get: v, set: s, enumerable: true, configurable: true});
}

$parcel$export(module.exports, "useToggle", () => $ee1b638d33c90dcc$export$cbe85ee05b554577);
/*
 * Copyright 2020 Adobe. All rights reserved.
 * This file is licensed to you under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License. You may obtain a copy
 * of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under
 * the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
 * OF ANY KIND, either express or implied. See the License for the specific language
 * governing permissions and limitations under the License.
 */ 


function $ee1b638d33c90dcc$export$cbe85ee05b554577(props, state, ref) {
    let { isDisabled: isDisabled = false, isReadOnly: isReadOnly = false, value: value, name: name, children: children, 'aria-label': ariaLabel, 'aria-labelledby': ariaLabelledby, validationState: validationState = 'valid', isInvalid: isInvalid } = props;
    let onChange = (e)=>{
        // since we spread props on label, onChange will end up there as well as in here.
        // so we have to stop propagation at the lowest level that we care about
        e.stopPropagation();
        state.setSelected(e.target.checked);
    };
    let hasChildren = children != null;
    let hasAriaLabel = ariaLabel != null || ariaLabelledby != null;
    if (!hasChildren && !hasAriaLabel) console.warn('If you do not provide children, you must specify an aria-label for accessibility');
    // This handles focusing the input on pointer down, which Safari does not do by default.
    let { pressProps: pressProps, isPressed: isPressed } = (0, $2jyrz$reactariainteractions.usePress)({
        isDisabled: isDisabled
    });
    // iOS does not toggle checkboxes if you drag off and back onto the label, so handle it ourselves.
    let { pressProps: labelProps, isPressed: isLabelPressed } = (0, $2jyrz$reactariainteractions.usePress)({
        isDisabled: isDisabled || isReadOnly,
        onPress () {
            state.toggle();
        }
    });
    let { focusableProps: focusableProps } = (0, $2jyrz$reactariafocus.useFocusable)(props, ref);
    let interactions = (0, $2jyrz$reactariautils.mergeProps)(pressProps, focusableProps);
    let domProps = (0, $2jyrz$reactariautils.filterDOMProps)(props, {
        labelable: true
    });
    (0, $2jyrz$reactariautils.useFormReset)(ref, state.isSelected, state.setSelected);
    return {
        labelProps: (0, $2jyrz$reactariautils.mergeProps)(labelProps, {
            onClick: (e)=>e.preventDefault()
        }),
        inputProps: (0, $2jyrz$reactariautils.mergeProps)(domProps, {
            'aria-invalid': isInvalid || validationState === 'invalid' || undefined,
            'aria-errormessage': props['aria-errormessage'],
            'aria-controls': props['aria-controls'],
            'aria-readonly': isReadOnly || undefined,
            onChange: onChange,
            disabled: isDisabled,
            ...value == null ? {} : {
                value: value
            },
            name: name,
            type: 'checkbox',
            ...interactions
        }),
        isSelected: state.isSelected,
        isPressed: isPressed || isLabelPressed,
        isDisabled: isDisabled,
        isReadOnly: isReadOnly,
        isInvalid: isInvalid || validationState === 'invalid'
    };
}


//# sourceMappingURL=useToggle.main.js.map
