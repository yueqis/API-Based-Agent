'use strict';

var vitest = require('vitest');
var matchers = require('./matchers-342a062d.js');
require('redent');
require('@adobe/css-tools');
require('dom-accessibility-api');
require('aria-query');
require('chalk');
require('lodash/isEqualWith.js');
require('css.escape');

/* istanbul ignore file */


vitest.expect.extend(matchers.extensions);
