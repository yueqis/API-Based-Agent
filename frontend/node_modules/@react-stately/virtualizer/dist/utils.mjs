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
 */ function $fc36f9a046a9ce79$export$37a26b283fd7740e(a, b) {
    let res = new Set();
    for (let key of a.keys())if (!b.has(key)) res.add(key);
    return res;
}
function $fc36f9a046a9ce79$export$acaf96a27438246b(a, b) {
    let toRemove = $fc36f9a046a9ce79$export$37a26b283fd7740e(a, b);
    let toAdd = $fc36f9a046a9ce79$export$37a26b283fd7740e(b, a);
    let toUpdate = new Set;
    for (let key of a.keys())if (b.has(key)) toUpdate.add(key);
    return {
        toRemove: toRemove,
        toAdd: toAdd,
        toUpdate: toUpdate
    };
}
function* $fc36f9a046a9ce79$export$cfc14088dfefce5f(...iterators) {
    for (let iterator of iterators)yield* iterator;
}
function $fc36f9a046a9ce79$export$6897c284b6f9f4dc(object) {
    let res = {};
    for(let key in object)res[object[key]] = key;
    return res;
}
function $fc36f9a046a9ce79$export$a8d0d0c8d1c5df64(a, b) {
    if (a === b) return true;
    if (a.size !== b.size) return false;
    for (let key of a){
        if (!b.has(key)) return false;
    }
    return true;
}


export {$fc36f9a046a9ce79$export$37a26b283fd7740e as keyDiff, $fc36f9a046a9ce79$export$acaf96a27438246b as difference, $fc36f9a046a9ce79$export$cfc14088dfefce5f as concatIterators, $fc36f9a046a9ce79$export$6897c284b6f9f4dc as invert, $fc36f9a046a9ce79$export$a8d0d0c8d1c5df64 as isSetEqual};
//# sourceMappingURL=utils.module.js.map
