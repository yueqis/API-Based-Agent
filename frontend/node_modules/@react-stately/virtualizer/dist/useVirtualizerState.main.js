var $064492b79924894c$exports = require("./Size.main.js");
var $e1bc15d49d21df0e$exports = require("./Virtualizer.main.js");
var $amfZP$react = require("react");
var $amfZP$reactariautils = require("@react-aria/utils");


function $parcel$export(e, n, v, s) {
  Object.defineProperty(e, n, {get: v, set: s, enumerable: true, configurable: true});
}

$parcel$export(module.exports, "useVirtualizerState", () => $f02ef43b5e8eee9b$export$1505db82fe357e65);
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



function $f02ef43b5e8eee9b$export$1505db82fe357e65(opts) {
    let [visibleViews, setVisibleViews] = (0, $amfZP$react.useState)([]);
    let [contentSize, setContentSize] = (0, $amfZP$react.useState)(new (0, $064492b79924894c$exports.Size)());
    let [isAnimating, setAnimating] = (0, $amfZP$react.useState)(false);
    let [isScrolling, setScrolling] = (0, $amfZP$react.useState)(false);
    let virtualizer = (0, $amfZP$react.useMemo)(()=>new (0, $e1bc15d49d21df0e$exports.Virtualizer)(), []);
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
    (0, $amfZP$reactariautils.useLayoutEffect)(()=>{
        virtualizer.afterRender();
    });
    // eslint-disable-next-line arrow-body-style
    (0, $amfZP$react.useEffect)(()=>{
        return ()=>virtualizer.willUnmount();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);
    let setVisibleRect = (0, $amfZP$react.useCallback)((rect)=>{
        virtualizer.visibleRect = rect;
    }, [
        virtualizer
    ]);
    let startScrolling = (0, $amfZP$react.useCallback)(()=>{
        virtualizer.startScrolling();
        setScrolling(true);
    }, [
        virtualizer
    ]);
    let endScrolling = (0, $amfZP$react.useCallback)(()=>{
        virtualizer.endScrolling();
        setScrolling(false);
    }, [
        virtualizer
    ]);
    let state = (0, $amfZP$react.useMemo)(()=>({
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


//# sourceMappingURL=useVirtualizerState.main.js.map
