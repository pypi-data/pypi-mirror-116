Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var mobx_1 = require("mobx");
var locale_1 = require("app/locale");
var utils_1 = require("./utils");
var SpanTreeModel = /** @class */ (function () {
    function SpanTreeModel(parentSpan, childSpans, api, isRoot) {
        var _this = this;
        if (isRoot === void 0) { isRoot = false; }
        var _a;
        this.children = [];
        // readable/writable state
        this.fetchEmbeddedChildrenState = 'idle';
        this.showEmbeddedChildren = false;
        this.embeddedChildren = [];
        this.showSpanGroup = false;
        this.isSpanFilteredOut = function (props) {
            var operationNameFilters = props.operationNameFilters, filterSpans = props.filterSpans;
            if (operationNameFilters.type === 'active_filter') {
                var operationName = utils_1.getSpanOperation(_this.span);
                if (typeof operationName === 'string' &&
                    !operationNameFilters.operationNames.has(operationName)) {
                    return true;
                }
            }
            if (!filterSpans) {
                return false;
            }
            return !filterSpans.spanIDs.has(utils_1.getSpanID(_this.span));
        };
        this.getSpansList = function (props) {
            var e_1, _a;
            var operationNameFilters = props.operationNameFilters, generateBounds = props.generateBounds, isLastSibling = props.isLastSibling, hiddenSpanGroups = props.hiddenSpanGroups, 
            // The set of ancestor span IDs whose sub-tree that the span belongs to
            spanGroups = props.spanGroups, filterSpans = props.filterSpans, previousSiblingEndTimestamp = props.previousSiblingEndTimestamp, event = props.event, isOnlySibling = props.isOnlySibling, spanGrouping = props.spanGrouping, toggleSpanGroup = props.toggleSpanGroup, showSpanGroup = props.showSpanGroup;
            var treeDepth = props.treeDepth, continuingTreeDepths = props.continuingTreeDepths;
            var parentSpanID = utils_1.getSpanID(_this.span);
            var childSpanGroup = new Set(spanGroups);
            childSpanGroup.add(parentSpanID);
            var descendantsSource = _this.showEmbeddedChildren
                ? tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(_this.embeddedChildren)), tslib_1.__read(_this.children)) : _this.children;
            var lastIndex = descendantsSource.length - 1;
            var isNotLastSpanOfGroup = isOnlySibling && !_this.isRoot && descendantsSource.length === 1;
            var shouldGroup = isNotLastSpanOfGroup;
            var hideSpanTree = hiddenSpanGroups.has(parentSpanID);
            var isLastSpanOfGroup = isOnlySibling && !_this.isRoot && (descendantsSource.length !== 1 || hideSpanTree);
            var isFirstSpanOfGroup = shouldGroup &&
                (spanGrouping === undefined ||
                    (Array.isArray(spanGrouping) && spanGrouping.length === 0));
            if (isLastSpanOfGroup &&
                Array.isArray(spanGrouping) &&
                spanGrouping.length >= 1 &&
                !showSpanGroup) {
                // We always want to indent the last span of the span group chain
                treeDepth = treeDepth + 1;
                // For a collapsed span group chain to be useful, we prefer span groupings
                // that are two or more spans.
                // Since there is no concept of "backtracking" when constructing the span tree,
                // we will need to reconstruct the tree depth information. This is only neccessary
                // when the span group chain is hidden/collapsed.
                if (spanGrouping.length === 1) {
                    var treeDepthEntryFoo = utils_1.isOrphanSpan(spanGrouping[0].span)
                        ? { type: 'orphan', depth: spanGrouping[0].treeDepth }
                        : spanGrouping[0].treeDepth;
                    if (!spanGrouping[0].isLastSibling) {
                        continuingTreeDepths = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(continuingTreeDepths)), [treeDepthEntryFoo]);
                    }
                }
            }
            // Criteria for propagating information about the span group to the last span of the span group chain
            var spanGroupingCriteria = isLastSpanOfGroup && Array.isArray(spanGrouping) && spanGrouping.length > 1;
            var wrappedSpan = {
                type: _this.isRoot ? 'root_span' : 'span',
                span: _this.span,
                numOfSpanChildren: descendantsSource.length,
                treeDepth: treeDepth,
                isLastSibling: isLastSibling,
                continuingTreeDepths: continuingTreeDepths,
                fetchEmbeddedChildrenState: _this.fetchEmbeddedChildrenState,
                showEmbeddedChildren: _this.showEmbeddedChildren,
                toggleEmbeddedChildren: _this.toggleEmbeddedChildren,
                toggleSpanGroup: spanGroupingCriteria && toggleSpanGroup && !showSpanGroup
                    ? toggleSpanGroup
                    : isFirstSpanOfGroup && _this.showSpanGroup && !hideSpanTree
                        ? _this.toggleSpanGroup
                        : undefined,
            };
            var treeDepthEntry = utils_1.isOrphanSpan(_this.span)
                ? { type: 'orphan', depth: treeDepth }
                : treeDepth;
            var shouldHideSpanOfGroup = shouldGroup &&
                !isLastSpanOfGroup &&
                ((toggleSpanGroup === undefined && !_this.showSpanGroup) ||
                    (toggleSpanGroup !== undefined && !showSpanGroup));
            var descendantContinuingTreeDepths = isLastSibling || shouldHideSpanOfGroup
                ? continuingTreeDepths
                : tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(continuingTreeDepths)), [treeDepthEntry]);
            try {
                for (var hiddenSpanGroups_1 = tslib_1.__values(hiddenSpanGroups), hiddenSpanGroups_1_1 = hiddenSpanGroups_1.next(); !hiddenSpanGroups_1_1.done; hiddenSpanGroups_1_1 = hiddenSpanGroups_1.next()) {
                    var hiddenSpanGroup = hiddenSpanGroups_1_1.value;
                    if (spanGroups.has(hiddenSpanGroup)) {
                        // If this span is hidden, then all the descendants are hidden as well
                        return [];
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (hiddenSpanGroups_1_1 && !hiddenSpanGroups_1_1.done && (_a = hiddenSpanGroups_1.return)) _a.call(hiddenSpanGroups_1);
                }
                finally { if (e_1) throw e_1.error; }
            }
            var descendants = (hideSpanTree ? [] : descendantsSource).reduce(function (acc, span, index) {
                var _a;
                (_a = acc.descendants).push.apply(_a, tslib_1.__spreadArray([], tslib_1.__read(span.getSpansList({
                    operationNameFilters: operationNameFilters,
                    generateBounds: generateBounds,
                    treeDepth: shouldHideSpanOfGroup ? treeDepth : treeDepth + 1,
                    isLastSibling: index === lastIndex,
                    continuingTreeDepths: descendantContinuingTreeDepths,
                    hiddenSpanGroups: hiddenSpanGroups,
                    spanGroups: new Set(childSpanGroup),
                    filterSpans: filterSpans,
                    previousSiblingEndTimestamp: acc.previousSiblingEndTimestamp,
                    event: event,
                    isOnlySibling: descendantsSource.length === 1,
                    spanGrouping: shouldGroup
                        ? tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read((spanGrouping !== null && spanGrouping !== void 0 ? spanGrouping : []))), [wrappedSpan]) : undefined,
                    toggleSpanGroup: isNotLastSpanOfGroup
                        ? toggleSpanGroup === undefined
                            ? _this.toggleSpanGroup
                            : toggleSpanGroup
                        : undefined,
                    showSpanGroup: isNotLastSpanOfGroup
                        ? toggleSpanGroup === undefined
                            ? _this.showSpanGroup
                            : showSpanGroup
                        : false,
                }))));
                acc.previousSiblingEndTimestamp = span.span.timestamp;
                return acc;
            }, {
                descendants: [],
                previousSiblingEndTimestamp: undefined,
            }).descendants;
            if (_this.isSpanFilteredOut(props)) {
                return tslib_1.__spreadArray([
                    {
                        type: 'filtered_out',
                        span: _this.span,
                    }
                ], tslib_1.__read(descendants));
            }
            var bounds = generateBounds({
                startTimestamp: _this.span.start_timestamp,
                endTimestamp: _this.span.timestamp,
            });
            var isCurrentSpanOutOfView = !bounds.isSpanVisibleInView;
            if (isCurrentSpanOutOfView) {
                return tslib_1.__spreadArray([
                    {
                        type: 'out_of_view',
                        span: _this.span,
                    }
                ], tslib_1.__read(descendants));
            }
            if (shouldHideSpanOfGroup) {
                return tslib_1.__spreadArray([], tslib_1.__read(descendants));
            }
            if (isLastSpanOfGroup &&
                Array.isArray(spanGrouping) &&
                spanGrouping.length > 1 &&
                !showSpanGroup &&
                wrappedSpan.type === 'span') {
                var spanGroupChain = {
                    type: 'span_group_chain',
                    span: _this.span,
                    treeDepth: treeDepth - 1,
                    continuingTreeDepths: continuingTreeDepths,
                    spanGrouping: spanGrouping,
                    showSpanGroup: showSpanGroup,
                    toggleSpanGroup: wrappedSpan.toggleSpanGroup,
                };
                return tslib_1.__spreadArray([
                    spanGroupChain,
                    tslib_1.__assign(tslib_1.__assign({}, wrappedSpan), { toggleSpanGroup: undefined })
                ], tslib_1.__read(descendants));
            }
            if (isFirstSpanOfGroup &&
                _this.showSpanGroup &&
                !hideSpanTree &&
                descendants.length <= 1 &&
                wrappedSpan.type === 'span') {
                // If we know the descendants will be one span or less, we remove the "regroup" feature (therefore hide it)
                // by setting toggleSpanGroup to be undefined for the first span of the group chain.
                wrappedSpan.toggleSpanGroup = undefined;
            }
            if (isLastSpanOfGroup && Array.isArray(spanGrouping) && spanGrouping.length === 1) {
                if (toggleSpanGroup !== undefined && !showSpanGroup) {
                    toggleSpanGroup();
                }
                if (!showSpanGroup) {
                    return tslib_1.__spreadArray([spanGrouping[0], wrappedSpan], tslib_1.__read(descendants));
                }
                return tslib_1.__spreadArray([wrappedSpan], tslib_1.__read(descendants));
            }
            var gapSpan = _this.generateSpanGap(event, previousSiblingEndTimestamp, treeDepth, continuingTreeDepths);
            if (gapSpan) {
                return tslib_1.__spreadArray([gapSpan, wrappedSpan], tslib_1.__read(descendants));
            }
            return tslib_1.__spreadArray([wrappedSpan], tslib_1.__read(descendants));
        };
        this.toggleEmbeddedChildren = function (props) {
            _this.showEmbeddedChildren = !_this.showEmbeddedChildren;
            _this.fetchEmbeddedChildrenState = 'idle';
            if (_this.showEmbeddedChildren && _this.embeddedChildren.length === 0) {
                return _this.fetchEmbeddedTransactions(props);
            }
            return Promise.resolve(undefined);
        };
        this.toggleSpanGroup = function () {
            _this.showSpanGroup = !_this.showSpanGroup;
        };
        this.api = api;
        this.span = parentSpan;
        this.isRoot = isRoot;
        var spanID = utils_1.getSpanID(parentSpan);
        var spanChildren = (_a = childSpans === null || childSpans === void 0 ? void 0 : childSpans[spanID]) !== null && _a !== void 0 ? _a : [];
        // Mark descendents as being rendered. This is to address potential recursion issues due to malformed data.
        // For example if a span has a span_id that's identical to its parent_span_id.
        childSpans = tslib_1.__assign({}, childSpans);
        delete childSpans[spanID];
        this.children = spanChildren.map(function (span) {
            return new SpanTreeModel(span, childSpans, api);
        });
        mobx_1.makeObservable(this, {
            operationNameCounts: mobx_1.computed.struct,
            showEmbeddedChildren: mobx_1.observable,
            embeddedChildren: mobx_1.observable,
            fetchEmbeddedChildrenState: mobx_1.observable,
            toggleEmbeddedChildren: mobx_1.action,
            fetchEmbeddedTransactions: mobx_1.action,
            showSpanGroup: mobx_1.observable,
            toggleSpanGroup: mobx_1.action,
        });
    }
    Object.defineProperty(SpanTreeModel.prototype, "operationNameCounts", {
        get: function () {
            var e_2, _a, e_3, _b;
            var _c;
            var result = new Map();
            var operationName = this.span.op;
            if (typeof operationName === 'string' && operationName.length > 0) {
                result.set(operationName, 1);
            }
            try {
                for (var _d = tslib_1.__values(this.children), _e = _d.next(); !_e.done; _e = _d.next()) {
                    var directChild = _e.value;
                    var operationNameCounts = directChild.operationNameCounts;
                    try {
                        for (var operationNameCounts_1 = (e_3 = void 0, tslib_1.__values(operationNameCounts)), operationNameCounts_1_1 = operationNameCounts_1.next(); !operationNameCounts_1_1.done; operationNameCounts_1_1 = operationNameCounts_1.next()) {
                            var _f = tslib_1.__read(operationNameCounts_1_1.value, 2), key = _f[0], count = _f[1];
                            result.set(key, ((_c = result.get(key)) !== null && _c !== void 0 ? _c : 0) + count);
                        }
                    }
                    catch (e_3_1) { e_3 = { error: e_3_1 }; }
                    finally {
                        try {
                            if (operationNameCounts_1_1 && !operationNameCounts_1_1.done && (_b = operationNameCounts_1.return)) _b.call(operationNameCounts_1);
                        }
                        finally { if (e_3) throw e_3.error; }
                    }
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
                }
                finally { if (e_2) throw e_2.error; }
            }
            // sort alphabetically using case insensitive comparison
            return new Map(tslib_1.__spreadArray([], tslib_1.__read(result)).sort(function (a, b) {
                return String(a[0]).localeCompare(b[0], undefined, { sensitivity: 'base' });
            }));
        },
        enumerable: false,
        configurable: true
    });
    SpanTreeModel.prototype.generateSpanGap = function (event, previousSiblingEndTimestamp, treeDepth, continuingTreeDepths) {
        // hide gap spans (i.e. "missing instrumentation" spans) for browser js transactions,
        // since they're not useful to indicate
        var shouldIncludeGap = !utils_1.isEventFromBrowserJavaScriptSDK(event);
        var isValidGap = shouldIncludeGap &&
            typeof previousSiblingEndTimestamp === 'number' &&
            previousSiblingEndTimestamp < this.span.start_timestamp &&
            // gap is at least 100 ms
            this.span.start_timestamp - previousSiblingEndTimestamp >= 0.1;
        if (!isValidGap) {
            return undefined;
        }
        var gapSpan = {
            type: 'gap',
            span: {
                type: 'gap',
                start_timestamp: previousSiblingEndTimestamp || this.span.start_timestamp,
                timestamp: this.span.start_timestamp,
                description: locale_1.t('Missing instrumentation'),
                isOrphan: utils_1.isOrphanSpan(this.span),
            },
            numOfSpanChildren: 0,
            treeDepth: treeDepth,
            isLastSibling: false,
            continuingTreeDepths: continuingTreeDepths,
            fetchEmbeddedChildrenState: 'idle',
            showEmbeddedChildren: false,
            toggleEmbeddedChildren: undefined,
        };
        return gapSpan;
    };
    SpanTreeModel.prototype.fetchEmbeddedTransactions = function (_a) {
        var _this = this;
        var orgSlug = _a.orgSlug, eventSlug = _a.eventSlug;
        var url = "/organizations/" + orgSlug + "/events/" + eventSlug + "/";
        this.fetchEmbeddedChildrenState = 'loading_embedded_transactions';
        return this.api
            .requestPromise(url, {
            method: 'GET',
            query: {},
        })
            .then(mobx_1.action('fetchEmbeddedTransactionsSuccess', function (event) {
            if (!event) {
                return;
            }
            var parsedTrace = utils_1.parseTrace(event);
            var rootSpan = utils_1.generateRootSpan(parsedTrace);
            var parsedRootSpan = new SpanTreeModel(rootSpan, parsedTrace.childSpans, _this.api, false);
            _this.embeddedChildren = [parsedRootSpan];
            _this.fetchEmbeddedChildrenState = 'idle';
        }))
            .catch(mobx_1.action('fetchEmbeddedTransactionsError', function () {
            _this.embeddedChildren = [];
            _this.fetchEmbeddedChildrenState = 'error_fetching_embedded_transactions';
        }));
    };
    return SpanTreeModel;
}());
exports.default = SpanTreeModel;
//# sourceMappingURL=spanTreeModel.jsx.map