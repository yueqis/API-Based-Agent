import React from 'react';

type RippleType = {
    key: React.Key;
    x: number;
    y: number;
    size: number;
};
interface UseRippleProps {
}
declare function useRipple(props?: UseRippleProps): {
    ripples: RippleType[];
    onClick: (event: React.MouseEvent<HTMLElement, MouseEvent>) => void;
    onClear: (key: React.Key) => void;
};
type UseRippleReturn = ReturnType<typeof useRipple>;

export { RippleType, UseRippleProps, UseRippleReturn, useRipple };
