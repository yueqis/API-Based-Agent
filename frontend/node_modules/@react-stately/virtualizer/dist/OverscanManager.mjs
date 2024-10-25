import {Point as $3041db3296945e6e$export$baf26146a414f24a} from "./Point.mjs";
import {Rect as $60423f92c7f9ad87$export$c79fc6492f3af13d} from "./Rect.mjs";

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

class $364191b3decf3697$var$RollingAverage {
    addSample(sample) {
        this.count++;
        this.value += (sample - this.value) / this.count;
    }
    constructor(){
        this.count = 0;
        this.value = 0;
    }
}
class $364191b3decf3697$export$4455ee6afb38dcbb {
    setVisibleRect(rect) {
        let time = performance.now() - this.startTime;
        if (time < 500) {
            this.averageTime.addSample(time);
            if (rect.x !== this.visibleRect.x && time > 0) this.velocity.x = (rect.x - this.visibleRect.x) / time;
            if (rect.y !== this.visibleRect.y && time > 0) this.velocity.y = (rect.y - this.visibleRect.y) / time;
        }
        this.startTime = performance.now();
        this.visibleRect = rect;
    }
    collectMetrics() {
        let time = performance.now() - this.startTime;
        if (time < 500) this.averagePerf.addSample(time);
        if (this.visibleRect.height > 0) {
            let o = Math.abs(this.velocity.y * (this.averageTime.value + this.averagePerf.value));
            this.overscanY.addSample(o);
        }
        if (this.visibleRect.width > 0) {
            let o = Math.abs(this.velocity.x * (this.averageTime.value + this.averagePerf.value));
            this.overscanX.addSample(o);
        }
    }
    getOverscannedRect() {
        let overscanned = this.visibleRect.copy();
        let overscanY = Math.round(Math.min(this.visibleRect.height * 2, this.overscanY.value) / 100) * 100;
        if (this.velocity.y > 0) {
            overscanned.y -= overscanY * 0.2;
            overscanned.height += overscanY + overscanY * 0.2;
        } else {
            overscanned.y -= overscanY;
            overscanned.height += overscanY + overscanY * 0.2;
        }
        let overscanX = Math.round(Math.min(this.visibleRect.width * 2, this.overscanX.value) / 100) * 100;
        if (this.velocity.x > 0) {
            overscanned.x -= overscanX * 0.2;
            overscanned.width += overscanX + overscanX * 0.2;
        } else {
            overscanned.x -= overscanX;
            overscanned.width += overscanX + overscanX * 0.2;
        }
        return overscanned;
    }
    constructor(){
        this.startTime = 0;
        this.averagePerf = new $364191b3decf3697$var$RollingAverage();
        this.averageTime = new $364191b3decf3697$var$RollingAverage();
        this.velocity = new (0, $3041db3296945e6e$export$baf26146a414f24a)(5, 5);
        this.overscanX = new $364191b3decf3697$var$RollingAverage();
        this.overscanY = new $364191b3decf3697$var$RollingAverage();
        this.visibleRect = new (0, $60423f92c7f9ad87$export$c79fc6492f3af13d)();
    }
}


export {$364191b3decf3697$export$4455ee6afb38dcbb as OverscanManager};
//# sourceMappingURL=OverscanManager.module.js.map
