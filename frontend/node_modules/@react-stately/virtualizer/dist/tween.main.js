var $f89f15d7f52bce29$exports = require("./Point.main.js");


function $parcel$export(e, n, v, s) {
  Object.defineProperty(e, n, {get: v, set: s, enumerable: true, configurable: true});
}

$parcel$export(module.exports, "tween", () => $57c5d36217e1f286$export$dc0b63720788090c);
$parcel$export(module.exports, "easeOut", () => $57c5d36217e1f286$export$57636bb43b1ccbb0);
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
// use high res timer if available
let $57c5d36217e1f286$var$perf = typeof window !== 'undefined' ? window.performance : null;
// @ts-ignore
let $57c5d36217e1f286$var$perfNow = $57c5d36217e1f286$var$perf && ($57c5d36217e1f286$var$perf.now || $57c5d36217e1f286$var$perf.webkitNow || $57c5d36217e1f286$var$perf.msNow || $57c5d36217e1f286$var$perf.mozNow);
let $57c5d36217e1f286$var$getTime = $57c5d36217e1f286$var$perfNow ? $57c5d36217e1f286$var$perfNow.bind($57c5d36217e1f286$var$perf) : function() {
    return Date.now ? Date.now() : new Date().getTime();
};
let $57c5d36217e1f286$var$fixTs;
function $57c5d36217e1f286$export$dc0b63720788090c(begin, end, duration, ease, fn) {
    let canceled = false;
    let raf_id;
    let promise = new Promise((resolve)=>{
        let start = $57c5d36217e1f286$var$getTime();
        let diffX = end.x - begin.x;
        let diffY = end.y - begin.y;
        raf_id = requestAnimationFrame(function run(t) {
            // if we're using a high res timer, make sure timestamp is not the old epoch-based value.
            // http://updates.html5rocks.com/2012/05/requestAnimationFrame-API-now-with-sub-millisecond-precision
            if ($57c5d36217e1f286$var$fixTs == null) $57c5d36217e1f286$var$fixTs = t > 1e12 !== $57c5d36217e1f286$var$getTime() > 1e12;
            if ($57c5d36217e1f286$var$fixTs) t = $57c5d36217e1f286$var$getTime();
            // check if we're done
            let delta = t - start;
            if (delta > duration) {
                fn(end);
                resolve();
            } else {
                // call frame callback after computing eased time and get the next frame
                let proceed = fn(new (0, $f89f15d7f52bce29$exports.Point)(begin.x + diffX * ease(delta / duration), begin.y + diffY * ease(delta / duration)));
                if (proceed !== false && !canceled) raf_id = requestAnimationFrame(run);
            }
        });
    });
    promise.cancel = function() {
        canceled = true;
        cancelAnimationFrame(raf_id);
    };
    return promise;
}
function $57c5d36217e1f286$export$77860c106b4a6a2e(t) {
    return t;
}
function $57c5d36217e1f286$export$57636bb43b1ccbb0(t) {
    return Math.sin(t * Math.PI / 2);
}


//# sourceMappingURL=tween.main.js.map
