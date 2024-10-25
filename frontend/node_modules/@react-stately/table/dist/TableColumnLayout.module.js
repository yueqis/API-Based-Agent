import {calculateColumnSizes as $6818b1c4fc67028d$export$55d50dc687385491, getMaxWidth as $6818b1c4fc67028d$export$59185c62a7544aa0, getMinWidth as $6818b1c4fc67028d$export$f556054ce4358701, isStatic as $6818b1c4fc67028d$export$1994a077b98ee0d5, parseFractionalUnit as $6818b1c4fc67028d$export$9078bad4c3934604} from "./TableUtils.module.js";

/*
 * Copyright 2022 Adobe. All rights reserved.
 * This file is licensed to you under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License. You may obtain a copy
 * of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under
 * the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
 * OF ANY KIND, either express or implied. See the License for the specific language
 * governing permissions and limitations under the License.
 */ 
class $a9e7ae544a4e41dd$export$7ff77a162970b30e {
    /** Takes an array of columns and splits it into 2 maps of columns with controlled and columns with uncontrolled widths. */ splitColumnsIntoControlledAndUncontrolled(columns) {
        return columns.reduce((acc, col)=>{
            if (col.props.width != null) acc[0].set(col.key, col);
            else acc[1].set(col.key, col);
            return acc;
        }, [
            new Map(),
            new Map()
        ]);
    }
    /** Takes uncontrolled and controlled widths and joins them into a single Map. */ recombineColumns(columns, uncontrolledWidths, uncontrolledColumns, controlledColumns) {
        return new Map(columns.map((col)=>{
            if (uncontrolledColumns.has(col.key)) return [
                col.key,
                uncontrolledWidths.get(col.key)
            ];
            else return [
                col.key,
                controlledColumns.get(col.key).props.width
            ];
        }));
    }
    /** Used to make an initial Map of the uncontrolled widths based on default widths. */ getInitialUncontrolledWidths(uncontrolledColumns) {
        return new Map(Array.from(uncontrolledColumns).map(([key, col])=>{
            var _this_getDefaultWidth, _this;
            var _col_props_defaultWidth, _ref;
            return [
                key,
                (_ref = (_col_props_defaultWidth = col.props.defaultWidth) !== null && _col_props_defaultWidth !== void 0 ? _col_props_defaultWidth : (_this_getDefaultWidth = (_this = this).getDefaultWidth) === null || _this_getDefaultWidth === void 0 ? void 0 : _this_getDefaultWidth.call(_this, col)) !== null && _ref !== void 0 ? _ref : '1fr'
            ];
        }));
    }
    getColumnWidth(key) {
        var _this_columnWidths_get;
        return (_this_columnWidths_get = this.columnWidths.get(key)) !== null && _this_columnWidths_get !== void 0 ? _this_columnWidths_get : 0;
    }
    getColumnMinWidth(key) {
        var _this_columnMinWidths_get;
        return (_this_columnMinWidths_get = this.columnMinWidths.get(key)) !== null && _this_columnMinWidths_get !== void 0 ? _this_columnMinWidths_get : 0;
    }
    getColumnMaxWidth(key) {
        var _this_columnMaxWidths_get;
        return (_this_columnMaxWidths_get = this.columnMaxWidths.get(key)) !== null && _this_columnMaxWidths_get !== void 0 ? _this_columnMaxWidths_get : 0;
    }
    resizeColumnWidth(tableWidth, collection, controlledWidths, uncontrolledWidths, col = null, width) {
        let prevColumnWidths = this.columnWidths;
        // resizing a column
        let resizeIndex = Infinity;
        let resizingChanged = new Map([
            ...controlledWidths,
            ...uncontrolledWidths
        ]);
        let percentKeys = new Map();
        let frKeysToTheRight = new Map();
        let minWidths = new Map();
        // freeze columns to the left to their previous pixel value
        collection.columns.forEach((column, i)=>{
            var _column_props_width_endsWith, _column_props_width;
            let frKey;
            let frValue;
            minWidths.set(column.key, this.getDefaultMinWidth(collection.columns[i]));
            if (col !== column.key && !column.props.width && !(0, $6818b1c4fc67028d$export$1994a077b98ee0d5)(uncontrolledWidths.get(column.key))) {
                // uncontrolled don't have props.width for us, so instead get from our state
                frKey = column.key;
                frValue = (0, $6818b1c4fc67028d$export$9078bad4c3934604)(uncontrolledWidths.get(column.key));
            } else if (col !== column.key && !(0, $6818b1c4fc67028d$export$1994a077b98ee0d5)(column.props.width) && !uncontrolledWidths.get(column.key)) {
                // controlledWidths will be the same in the collection
                frKey = column.key;
                frValue = (0, $6818b1c4fc67028d$export$9078bad4c3934604)(column.props.width);
            } else if (col !== column.key && ((_column_props_width = column.props.width) === null || _column_props_width === void 0 ? void 0 : (_column_props_width_endsWith = _column_props_width.endsWith) === null || _column_props_width_endsWith === void 0 ? void 0 : _column_props_width_endsWith.call(_column_props_width, '%'))) percentKeys.set(column.key, column.props.width);
            // don't freeze columns to the right of the resizing one
            if (resizeIndex < i) {
                if (frKey) frKeysToTheRight.set(frKey, frValue);
                return;
            }
            // we already know the new size of the resizing column
            if (column.key === col) {
                resizeIndex = i;
                resizingChanged.set(column.key, Math.floor(width));
                return;
            }
            // freeze column to previous value
            resizingChanged.set(column.key, prevColumnWidths.get(column.key));
        });
        // predict pixels sizes for all columns based on resize
        let columnWidths = (0, $6818b1c4fc67028d$export$55d50dc687385491)(tableWidth, collection.columns.map((col)=>({
                ...col.props,
                key: col.key
            })), resizingChanged, (i)=>this.getDefaultWidth(collection.columns[i]), (i)=>this.getDefaultMinWidth(collection.columns[i]));
        // set all new column widths for onResize event
        // columns going in will be the same order as the columns coming out
        let newWidths = new Map();
        // set all column widths based on calculateColumnSize
        columnWidths.forEach((width, index)=>{
            let key = collection.columns[index].key;
            newWidths.set(key, width);
        });
        // add FR's back as they were to columns to the right
        Array.from(frKeysToTheRight).forEach(([key])=>{
            newWidths.set(key, `${frKeysToTheRight.get(key)}fr`);
        });
        // put back in percents
        Array.from(percentKeys).forEach(([key, width])=>{
            // resizing locks a column to a px width
            if (key === col) return;
            newWidths.set(key, width);
        });
        return newWidths;
    }
    buildColumnWidths(tableWidth, collection, widths) {
        this.columnWidths = new Map();
        this.columnMinWidths = new Map();
        this.columnMaxWidths = new Map();
        // initial layout or table/window resizing
        let columnWidths = (0, $6818b1c4fc67028d$export$55d50dc687385491)(tableWidth, collection.columns.map((col)=>({
                ...col.props,
                key: col.key
            })), widths, (i)=>this.getDefaultWidth(collection.columns[i]), (i)=>this.getDefaultMinWidth(collection.columns[i]));
        // columns going in will be the same order as the columns coming out
        columnWidths.forEach((width, index)=>{
            let key = collection.columns[index].key;
            let column = collection.columns[index];
            this.columnWidths.set(key, width);
            var _column_props_minWidth;
            this.columnMinWidths.set(key, (0, $6818b1c4fc67028d$export$f556054ce4358701)((_column_props_minWidth = column.props.minWidth) !== null && _column_props_minWidth !== void 0 ? _column_props_minWidth : this.getDefaultMinWidth(column), tableWidth));
            this.columnMaxWidths.set(key, (0, $6818b1c4fc67028d$export$59185c62a7544aa0)(column.props.maxWidth, tableWidth));
        });
        return this.columnWidths;
    }
    constructor(options){
        this.columnWidths = new Map();
        this.columnMinWidths = new Map();
        this.columnMaxWidths = new Map();
        var _options_getDefaultWidth;
        this.getDefaultWidth = (_options_getDefaultWidth = options === null || options === void 0 ? void 0 : options.getDefaultWidth) !== null && _options_getDefaultWidth !== void 0 ? _options_getDefaultWidth : ()=>'1fr';
        var _options_getDefaultMinWidth;
        this.getDefaultMinWidth = (_options_getDefaultMinWidth = options === null || options === void 0 ? void 0 : options.getDefaultMinWidth) !== null && _options_getDefaultMinWidth !== void 0 ? _options_getDefaultMinWidth : ()=>75;
    }
}


export {$a9e7ae544a4e41dd$export$7ff77a162970b30e as TableColumnLayout};
//# sourceMappingURL=TableColumnLayout.module.js.map
