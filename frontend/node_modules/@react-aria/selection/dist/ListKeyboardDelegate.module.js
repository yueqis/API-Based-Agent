import {isScrollable as $eak97$isScrollable} from "@react-aria/utils";

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
class $2a25aae57d74318e$export$a05409b8bb224a5a {
    isDisabled(item) {
        var _item_props;
        return this.disabledBehavior === 'all' && (((_item_props = item.props) === null || _item_props === void 0 ? void 0 : _item_props.isDisabled) || this.disabledKeys.has(item.key));
    }
    getNextKey(key) {
        key = this.collection.getKeyAfter(key);
        while(key != null){
            let item = this.collection.getItem(key);
            if (item.type === 'item' && !this.isDisabled(item)) return key;
            key = this.collection.getKeyAfter(key);
        }
        return null;
    }
    getPreviousKey(key) {
        key = this.collection.getKeyBefore(key);
        while(key != null){
            let item = this.collection.getItem(key);
            if (item.type === 'item' && !this.isDisabled(item)) return key;
            key = this.collection.getKeyBefore(key);
        }
        return null;
    }
    findKey(key, nextKey, shouldSkip) {
        let item = this.getItem(key);
        if (!item) return null;
        // Find the item above or below in the same column.
        let prevRect = item.getBoundingClientRect();
        do {
            key = nextKey(key);
            item = this.getItem(key);
        }while (item && shouldSkip(prevRect, item.getBoundingClientRect()));
        return key;
    }
    isSameRow(prevRect, itemRect) {
        return prevRect.top === itemRect.top || prevRect.left !== itemRect.left;
    }
    isSameColumn(prevRect, itemRect) {
        return prevRect.left === itemRect.left || prevRect.top !== itemRect.top;
    }
    getKeyBelow(key) {
        if (this.layout === 'grid' && this.orientation === 'vertical') return this.findKey(key, (key)=>this.getNextKey(key), this.isSameRow);
        else return this.getNextKey(key);
    }
    getKeyAbove(key) {
        if (this.layout === 'grid' && this.orientation === 'vertical') return this.findKey(key, (key)=>this.getPreviousKey(key), this.isSameRow);
        else return this.getPreviousKey(key);
    }
    getNextColumn(key, right) {
        return right ? this.getPreviousKey(key) : this.getNextKey(key);
    }
    getKeyRightOf(key) {
        if (this.layout === 'grid') {
            if (this.orientation === 'vertical') return this.getNextColumn(key, this.direction === 'rtl');
            else return this.findKey(key, (key)=>this.getNextColumn(key, this.direction === 'rtl'), this.isSameColumn);
        } else if (this.orientation === 'horizontal') return this.getNextColumn(key, this.direction === 'rtl');
        return null;
    }
    getKeyLeftOf(key) {
        if (this.layout === 'grid') {
            if (this.orientation === 'vertical') return this.getNextColumn(key, this.direction === 'ltr');
            else return this.findKey(key, (key)=>this.getNextColumn(key, this.direction === 'ltr'), this.isSameColumn);
        } else if (this.orientation === 'horizontal') return this.getNextColumn(key, this.direction === 'ltr');
        return null;
    }
    getFirstKey() {
        let key = this.collection.getFirstKey();
        while(key != null){
            let item = this.collection.getItem(key);
            if ((item === null || item === void 0 ? void 0 : item.type) === 'item' && !this.isDisabled(item)) return key;
            key = this.collection.getKeyAfter(key);
        }
        return null;
    }
    getLastKey() {
        let key = this.collection.getLastKey();
        while(key != null){
            let item = this.collection.getItem(key);
            if (item.type === 'item' && !this.isDisabled(item)) return key;
            key = this.collection.getKeyBefore(key);
        }
        return null;
    }
    getItem(key) {
        return key !== null ? this.ref.current.querySelector(`[data-key="${CSS.escape(key.toString())}"]`) : null;
    }
    getKeyPageAbove(key) {
        let menu = this.ref.current;
        let item = this.getItem(key);
        if (!item) return null;
        if (!(0, $eak97$isScrollable)(menu)) return this.getFirstKey();
        let containerRect = menu.getBoundingClientRect();
        let itemRect = item.getBoundingClientRect();
        if (this.orientation === 'horizontal') {
            let containerX = containerRect.x - menu.scrollLeft;
            let pageX = Math.max(0, itemRect.x - containerX + itemRect.width - containerRect.width);
            while(item && itemRect.x - containerX > pageX){
                key = this.getKeyAbove(key);
                item = key == null ? null : this.getItem(key);
                itemRect = item === null || item === void 0 ? void 0 : item.getBoundingClientRect();
            }
        } else {
            let containerY = containerRect.y - menu.scrollTop;
            let pageY = Math.max(0, itemRect.y - containerY + itemRect.height - containerRect.height);
            while(item && itemRect.y - containerY > pageY){
                key = this.getKeyAbove(key);
                item = key == null ? null : this.getItem(key);
                itemRect = item === null || item === void 0 ? void 0 : item.getBoundingClientRect();
            }
        }
        return key !== null && key !== void 0 ? key : this.getFirstKey();
    }
    getKeyPageBelow(key) {
        let menu = this.ref.current;
        let item = this.getItem(key);
        if (!item) return null;
        if (!(0, $eak97$isScrollable)(menu)) return this.getLastKey();
        let containerRect = menu.getBoundingClientRect();
        let itemRect = item.getBoundingClientRect();
        if (this.orientation === 'horizontal') {
            let containerX = containerRect.x - menu.scrollLeft;
            let pageX = Math.min(menu.scrollWidth, itemRect.x - containerX - itemRect.width + containerRect.width);
            while(item && itemRect.x - containerX < pageX){
                key = this.getKeyBelow(key);
                item = key == null ? null : this.getItem(key);
                itemRect = item === null || item === void 0 ? void 0 : item.getBoundingClientRect();
            }
        } else {
            let containerY = containerRect.y - menu.scrollTop;
            let pageY = Math.min(menu.scrollHeight, itemRect.y - containerY - itemRect.height + containerRect.height);
            while(item && itemRect.y - containerY < pageY){
                key = this.getKeyBelow(key);
                item = key == null ? null : this.getItem(key);
                itemRect = item === null || item === void 0 ? void 0 : item.getBoundingClientRect();
            }
        }
        return key !== null && key !== void 0 ? key : this.getLastKey();
    }
    getKeyForSearch(search, fromKey) {
        if (!this.collator) return null;
        let collection = this.collection;
        let key = fromKey || this.getFirstKey();
        while(key != null){
            let item = collection.getItem(key);
            let substring = item.textValue.slice(0, search.length);
            if (item.textValue && this.collator.compare(substring, search) === 0) return key;
            key = this.getKeyBelow(key);
        }
        return null;
    }
    constructor(...args){
        if (args.length === 1) {
            let opts = args[0];
            this.collection = opts.collection;
            this.ref = opts.ref;
            this.collator = opts.collator;
            this.disabledKeys = opts.disabledKeys || new Set();
            this.disabledBehavior = opts.disabledBehavior || 'all';
            this.orientation = opts.orientation;
            this.direction = opts.direction;
            this.layout = opts.layout || 'stack';
        } else {
            this.collection = args[0];
            this.disabledKeys = args[1];
            this.ref = args[2];
            this.collator = args[3];
            this.layout = 'stack';
            this.orientation = 'vertical';
            this.disabledBehavior = 'all';
        }
        // If this is a vertical stack, remove the left/right methods completely
        // so they aren't called by useDroppableCollection.
        if (this.layout === 'stack' && this.orientation === 'vertical') {
            this.getKeyLeftOf = undefined;
            this.getKeyRightOf = undefined;
        }
    }
}


export {$2a25aae57d74318e$export$a05409b8bb224a5a as ListKeyboardDelegate};
//# sourceMappingURL=ListKeyboardDelegate.module.js.map
