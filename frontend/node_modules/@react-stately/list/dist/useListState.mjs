import {ListCollection as $a02d57049d202695$export$d085fb9e920b5ca7} from "./ListCollection.mjs";
import {useMultipleSelectionState as $d5vlZ$useMultipleSelectionState, SelectionManager as $d5vlZ$SelectionManager} from "@react-stately/selection";
import {useMemo as $d5vlZ$useMemo, useCallback as $d5vlZ$useCallback, useRef as $d5vlZ$useRef, useEffect as $d5vlZ$useEffect} from "react";
import {useCollection as $d5vlZ$useCollection} from "@react-stately/collections";

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



function $e72dd72e1c76a225$export$2f645645f7bca764(props) {
    let { filter: filter } = props;
    let selectionState = (0, $d5vlZ$useMultipleSelectionState)(props);
    let disabledKeys = (0, $d5vlZ$useMemo)(()=>props.disabledKeys ? new Set(props.disabledKeys) : new Set(), [
        props.disabledKeys
    ]);
    let factory = (0, $d5vlZ$useCallback)((nodes)=>filter ? new (0, $a02d57049d202695$export$d085fb9e920b5ca7)(filter(nodes)) : new (0, $a02d57049d202695$export$d085fb9e920b5ca7)(nodes), [
        filter
    ]);
    let context = (0, $d5vlZ$useMemo)(()=>({
            suppressTextValueWarning: props.suppressTextValueWarning
        }), [
        props.suppressTextValueWarning
    ]);
    let collection = (0, $d5vlZ$useCollection)(props, factory, context);
    let selectionManager = (0, $d5vlZ$useMemo)(()=>new (0, $d5vlZ$SelectionManager)(collection, selectionState), [
        collection,
        selectionState
    ]);
    // Reset focused key if that item is deleted from the collection.
    const cachedCollection = (0, $d5vlZ$useRef)(null);
    (0, $d5vlZ$useEffect)(()=>{
        if (selectionState.focusedKey != null && !collection.getItem(selectionState.focusedKey)) {
            const startItem = cachedCollection.current.getItem(selectionState.focusedKey);
            const cachedItemNodes = [
                ...cachedCollection.current.getKeys()
            ].map((key)=>{
                const itemNode = cachedCollection.current.getItem(key);
                return itemNode.type === 'item' ? itemNode : null;
            }).filter((node)=>node !== null);
            const itemNodes = [
                ...collection.getKeys()
            ].map((key)=>{
                const itemNode = collection.getItem(key);
                return itemNode.type === 'item' ? itemNode : null;
            }).filter((node)=>node !== null);
            const diff = cachedItemNodes.length - itemNodes.length;
            let index = Math.min(diff > 1 ? Math.max(startItem.index - diff + 1, 0) : startItem.index, itemNodes.length - 1);
            let newNode;
            while(index >= 0){
                if (!selectionManager.isDisabled(itemNodes[index].key)) {
                    newNode = itemNodes[index];
                    break;
                }
                // Find next, not disabled item.
                if (index < itemNodes.length - 1) index++;
                else {
                    if (index > startItem.index) index = startItem.index;
                    index--;
                }
            }
            selectionState.setFocusedKey(newNode ? newNode.key : null);
        }
        cachedCollection.current = collection;
    }, [
        collection,
        selectionManager,
        selectionState,
        selectionState.focusedKey
    ]);
    return {
        collection: collection,
        disabledKeys: disabledKeys,
        selectionManager: selectionManager
    };
}


export {$e72dd72e1c76a225$export$2f645645f7bca764 as useListState};
//# sourceMappingURL=useListState.module.js.map
