import {Size as $ee1bfa90a957fb8a$export$cb6da89c6af1a8ec} from "./Size.module.js";
import {Virtualizer as $38b9490c1cca8fc4$export$89be5a243e59c4b2} from "./Virtualizer.module.js";
import {useState as $3Fik3$useState, useMemo as $3Fik3$useMemo, useEffect as $3Fik3$useEffect, useCallback as $3Fik3$useCallback} from "react";
import {useLayoutEffect as $3Fik3$useLayoutEffect} from "@react-aria/utils";

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



function $fc0b13b484ac1194$export$1505db82fe357e65(opts) {
    let [visibleViews, setVisibleViews] = (0, $3Fik3$useState)([]);
    let [contentSize, setContentSize] = (0, $3Fik3$useState)(new (0, $ee1bfa90a957fb8a$export$cb6da89c6af1a8ec)());
    let [isAnimating, setAnimating] = (0, $3Fik3$useState)(false);
    let [isScrolling, setScrolling] = (0, $3Fik3$useState)(false);
    let virtualizer = (0, $3Fik3$useMemo)(()=>new (0, $38b9490c1cca8fc4$export$89be5a243e59c4b2)(), []);
    virtualizer.delegate = {
        setVisibleViews: setVisibleViews,
        setVisibleRect (rect) {
            virtualizer.visibleRect = rect;
            opts.onVisibleRectChange(rect);
        },
        setContentSize: setContentSize,
        renderView: opts.renderView,
        renderWrapper: opts.renderWrapper,
        beginAnimations: ()=>setAnimating(true),
        endAnimations: ()=>setAnimating(false),
        getScrollAnchor: opts.getScrollAnchor
    };
    virtualizer.layout = opts.layout;
    virtualizer.collection = opts.collection;
    virtualizer.transitionDuration = opts.transitionDuration;
    (0, $3Fik3$useLayoutEffect)(()=>{
        virtualizer.afterRender();
    });
    // eslint-disable-next-line arrow-body-style
    (0, $3Fik3$useEffect)(()=>{
        return ()=>virtualizer.willUnmount();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);
    let setVisibleRect = (0, $3Fik3$useCallback)((rect)=>{
        virtualizer.visibleRect = rect;
    }, [
        virtualizer
    ]);
    let startScrolling = (0, $3Fik3$useCallback)(()=>{
        virtualizer.startScrolling();
        setScrolling(true);
    }, [
        virtualizer
    ]);
    let endScrolling = (0, $3Fik3$useCallback)(()=>{
        virtualizer.endScrolling();
        setScrolling(false);
    }, [
        virtualizer
    ]);
    let state = (0, $3Fik3$useMemo)(()=>({
            virtualizer: virtualizer,
            visibleViews: visibleViews,
            setVisibleRect: setVisibleRect,
            contentSize: contentSize,
            isAnimating: isAnimating,
            isScrolling: isScrolling,
            startScrolling: startScrolling,
            endScrolling: endScrolling
        }), [
        virtualizer,
        visibleViews,
        setVisibleRect,
        contentSize,
        isAnimating,
        isScrolling,
        startScrolling,
        endScrolling
    ]);
    return state;
}


export {$fc0b13b484ac1194$export$1505db82fe357e65 as useVirtualizerState};
//# sourceMappingURL=useVirtualizerState.module.js.map
