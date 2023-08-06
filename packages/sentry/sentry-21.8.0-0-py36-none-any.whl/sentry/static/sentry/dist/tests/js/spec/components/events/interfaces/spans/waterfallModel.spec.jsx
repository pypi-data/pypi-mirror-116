var _this = this;
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var filter_1 = require("app/components/events/interfaces/spans/filter");
var waterfallModel_1 = tslib_1.__importDefault(require("app/components/events/interfaces/spans/waterfallModel"));
var event_1 = require("app/types/event");
var utils_1 = require("app/types/utils");
describe('WaterfallModel', function () {
    var event = {
        id: '2b658a829a21496b87fd1f14a61abf65',
        eventID: '2b658a829a21496b87fd1f14a61abf65',
        title: '/organizations/:orgId/discover/results/',
        type: 'transaction',
        startTimestamp: 1622079935.86141,
        endTimestamp: 1622079940.032905,
        contexts: {
            trace: {
                trace_id: '8cbbc19c0f54447ab702f00263262726',
                span_id: 'a934857184bdf5a6',
                op: 'pageload',
                status: 'unknown',
                type: 'trace',
            },
        },
        entries: [
            {
                data: [
                    {
                        timestamp: 1622079937.227645,
                        start_timestamp: 1622079936.90689,
                        description: 'GET /api/0/organizations/?member=1',
                        op: 'http',
                        span_id: 'b23703998ae619e7',
                        parent_span_id: 'a934857184bdf5a6',
                        trace_id: '8cbbc19c0f54447ab702f00263262726',
                        status: 'ok',
                        tags: {
                            'http.status_code': '200',
                        },
                        data: {
                            method: 'GET',
                            type: 'fetch',
                            url: '/api/0/organizations/?member=1',
                        },
                    },
                    {
                        timestamp: 1622079938.20331,
                        start_timestamp: 1622079937.907515,
                        description: 'GET /api/0/internal/health/',
                        op: 'http',
                        span_id: 'a453cc713e5baf9c',
                        parent_span_id: 'a934857184bdf5a6',
                        trace_id: '8cbbc19c0f54447ab702f00263262726',
                        status: 'ok',
                        tags: {
                            'http.status_code': '200',
                        },
                        data: {
                            method: 'GET',
                            type: 'fetch',
                            url: '/api/0/internal/health/',
                        },
                    },
                    {
                        timestamp: 1622079936.05839,
                        start_timestamp: 1622079936.048125,
                        description: '/_static/dist/sentry/sentry.541f5b.css',
                        op: 'resource.link',
                        span_id: 'a23f26b939d1a735',
                        parent_span_id: 'a453cc713e5baf9c',
                        trace_id: '8cbbc19c0f54447ab702f00263262726',
                        data: {
                            'Decoded Body Size': 159248,
                            'Encoded Body Size': 159248,
                            'Transfer Size': 275,
                        },
                    },
                    {
                        timestamp: 1622079938.32451,
                        start_timestamp: 1622079938.31431,
                        description: '/_static/dist/sentry/sentry.541f5b.min.css',
                        op: 'css',
                        span_id: 'b5795cf4ba68bbb4',
                        parent_span_id: 'a934857184bdf5a6',
                        trace_id: '8cbbc19c0f54447ab702f00263262726',
                        data: {
                            'Decoded Body Size': 159248,
                            'Encoded Body Size': 159248,
                            'Transfer Size': 275,
                        },
                    },
                ],
                type: event_1.EntryType.SPANS,
            },
        ],
    };
    var fullWaterfall = [
        {
            type: 'root_span',
            span: {
                trace_id: '8cbbc19c0f54447ab702f00263262726',
                span_id: 'a934857184bdf5a6',
                start_timestamp: 1622079935.86141,
                timestamp: 1622079940.032905,
                description: undefined,
                parent_span_id: undefined,
                op: 'pageload',
                data: {},
                status: 'unknown',
            },
            numOfSpanChildren: 3,
            treeDepth: 0,
            isLastSibling: true,
            continuingTreeDepths: [],
            showEmbeddedChildren: false,
            toggleEmbeddedChildren: expect.any(Function),
            fetchEmbeddedChildrenState: 'idle',
        },
        {
            type: 'span',
            span: {
                timestamp: 1622079937.227645,
                start_timestamp: 1622079936.90689,
                description: 'GET /api/0/organizations/?member=1',
                op: 'http',
                span_id: 'b23703998ae619e7',
                parent_span_id: 'a934857184bdf5a6',
                trace_id: '8cbbc19c0f54447ab702f00263262726',
                status: 'ok',
                tags: { 'http.status_code': '200' },
                data: { method: 'GET', type: 'fetch', url: '/api/0/organizations/?member=1' },
            },
            numOfSpanChildren: 0,
            treeDepth: 1,
            isLastSibling: false,
            continuingTreeDepths: [],
            showEmbeddedChildren: false,
            toggleEmbeddedChildren: expect.any(Function),
            fetchEmbeddedChildrenState: 'idle',
            toggleSpanGroup: undefined,
        },
        {
            type: 'gap',
            span: {
                type: 'gap',
                start_timestamp: 1622079937.227645,
                timestamp: 1622079937.907515,
                description: 'Missing instrumentation',
                isOrphan: false,
            },
            numOfSpanChildren: 0,
            treeDepth: 1,
            isLastSibling: false,
            continuingTreeDepths: [],
            showEmbeddedChildren: false,
            toggleEmbeddedChildren: undefined,
            fetchEmbeddedChildrenState: 'idle',
        },
        {
            type: 'span',
            span: {
                timestamp: 1622079938.20331,
                start_timestamp: 1622079937.907515,
                description: 'GET /api/0/internal/health/',
                op: 'http',
                span_id: 'a453cc713e5baf9c',
                parent_span_id: 'a934857184bdf5a6',
                trace_id: '8cbbc19c0f54447ab702f00263262726',
                status: 'ok',
                tags: { 'http.status_code': '200' },
                data: { method: 'GET', type: 'fetch', url: '/api/0/internal/health/' },
            },
            numOfSpanChildren: 1,
            treeDepth: 1,
            isLastSibling: false,
            continuingTreeDepths: [],
            showEmbeddedChildren: false,
            toggleEmbeddedChildren: expect.any(Function),
            fetchEmbeddedChildrenState: 'idle',
            toggleSpanGroup: undefined,
        },
        {
            type: 'span',
            span: {
                timestamp: 1622079936.05839,
                start_timestamp: 1622079936.048125,
                description: '/_static/dist/sentry/sentry.541f5b.css',
                op: 'resource.link',
                span_id: 'a23f26b939d1a735',
                parent_span_id: 'a453cc713e5baf9c',
                trace_id: '8cbbc19c0f54447ab702f00263262726',
                data: {
                    'Decoded Body Size': 159248,
                    'Encoded Body Size': 159248,
                    'Transfer Size': 275,
                },
            },
            numOfSpanChildren: 0,
            treeDepth: 2,
            isLastSibling: true,
            continuingTreeDepths: [1],
            showEmbeddedChildren: false,
            toggleEmbeddedChildren: expect.any(Function),
            fetchEmbeddedChildrenState: 'idle',
            toggleSpanGroup: undefined,
        },
        {
            type: 'gap',
            span: {
                type: 'gap',
                start_timestamp: 1622079938.20331,
                timestamp: 1622079938.31431,
                description: 'Missing instrumentation',
                isOrphan: false,
            },
            numOfSpanChildren: 0,
            treeDepth: 1,
            isLastSibling: false,
            continuingTreeDepths: [],
            showEmbeddedChildren: false,
            toggleEmbeddedChildren: undefined,
            fetchEmbeddedChildrenState: 'idle',
        },
        {
            type: 'span',
            span: {
                timestamp: 1622079938.32451,
                start_timestamp: 1622079938.31431,
                description: '/_static/dist/sentry/sentry.541f5b.min.css',
                op: 'css',
                span_id: 'b5795cf4ba68bbb4',
                parent_span_id: 'a934857184bdf5a6',
                trace_id: '8cbbc19c0f54447ab702f00263262726',
                data: {
                    'Decoded Body Size': 159248,
                    'Encoded Body Size': 159248,
                    'Transfer Size': 275,
                },
            },
            numOfSpanChildren: 0,
            treeDepth: 1,
            isLastSibling: true,
            continuingTreeDepths: [],
            showEmbeddedChildren: false,
            toggleEmbeddedChildren: expect.any(Function),
            fetchEmbeddedChildrenState: 'idle',
            toggleSpanGroup: undefined,
        },
    ];
    it('isEvent', function () {
        var waterfallModel = new waterfallModel_1.default(event);
        expect(waterfallModel.event).toMatchObject(event);
        expect(waterfallModel.isEvent(event)).toBe(true);
        expect(waterfallModel.isEvent(tslib_1.__assign(tslib_1.__assign({}, event), { id: 'somethingelse' }))).toBe(false);
    });
    it('get operationNameCounts', function () {
        var waterfallModel = new waterfallModel_1.default(event);
        expect(Object.fromEntries(waterfallModel.operationNameCounts)).toMatchObject({
            http: 2,
            pageload: 1,
            'resource.link': 1,
        });
    });
    it('toggleOperationNameFilter', function () {
        var waterfallModel = new waterfallModel_1.default(event);
        expect(waterfallModel.operationNameFilters).toEqual(filter_1.noFilter);
        // toggle http filter
        waterfallModel.toggleOperationNameFilter('http');
        var operationNameFilters = waterfallModel.operationNameFilters;
        expect(operationNameFilters.type).toBe('active_filter');
        expect(Array.from(operationNameFilters.operationNames)).toEqual(['http']);
        // un-toggle http filter
        waterfallModel.toggleOperationNameFilter('http');
        expect(waterfallModel.operationNameFilters).toEqual(filter_1.noFilter);
    });
    it('toggleAllOperationNameFilters', function () {
        var waterfallModel = new waterfallModel_1.default(event);
        expect(waterfallModel.operationNameFilters).toEqual(filter_1.noFilter);
        // toggle all operation names
        waterfallModel.toggleAllOperationNameFilters();
        var operationNameFilters = waterfallModel.operationNameFilters;
        expect(operationNameFilters.type).toBe('active_filter');
        expect(Array.from(operationNameFilters.operationNames)).toEqual([
            'css',
            'http',
            'pageload',
            'resource.link',
        ]);
        // toggle http filter
        waterfallModel.toggleOperationNameFilter('http');
        operationNameFilters = waterfallModel.operationNameFilters;
        expect(operationNameFilters.type).toBe('active_filter');
        expect(Array.from(operationNameFilters.operationNames)).toEqual([
            'css',
            'pageload',
            'resource.link',
        ]);
        // toggle all operation names; expect un-toggled operation names to be toggled on
        waterfallModel.toggleAllOperationNameFilters();
        operationNameFilters = waterfallModel.operationNameFilters;
        expect(operationNameFilters.type).toBe('active_filter');
        expect(Array.from(operationNameFilters.operationNames)).toEqual([
            'css',
            'http',
            'pageload',
            'resource.link',
        ]);
        // un-toggle all operation names
        waterfallModel.toggleAllOperationNameFilters();
        expect(waterfallModel.operationNameFilters).toEqual(filter_1.noFilter);
    });
    it('querySpanSearch', function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
        var waterfallModel;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    waterfallModel = new waterfallModel_1.default(event);
                    expect(waterfallModel.fuse).toBe(undefined);
                    // Fuzzy search needs to be loaded asynchronously
                    // @ts-expect-error
                    return [4 /*yield*/, tick()];
                case 1:
                    // Fuzzy search needs to be loaded asynchronously
                    // @ts-expect-error
                    _a.sent();
                    // expect fuse index to be created
                    expect(waterfallModel.fuse).not.toBe(undefined);
                    expect(waterfallModel.filterSpans).toBe(undefined);
                    expect(waterfallModel.searchQuery).toBe(undefined);
                    waterfallModel.querySpanSearch('GET /api/0/organizations/?member=1');
                    expect(Array.from(waterfallModel.filterSpans.spanIDs).sort()).toEqual(['a453cc713e5baf9c', 'b23703998ae619e7'].sort());
                    expect(waterfallModel.searchQuery).toBe('GET /api/0/organizations/?member=1');
                    return [2 /*return*/];
            }
        });
    }); });
    it('getWaterfall()', function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
        var waterfallModel, spans, expected;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    waterfallModel = new waterfallModel_1.default(event);
                    // Fuzzy search needs to be loaded asynchronously
                    // @ts-expect-error
                    return [4 /*yield*/, tick()];
                case 1:
                    // Fuzzy search needs to be loaded asynchronously
                    // @ts-expect-error
                    _a.sent();
                    spans = waterfallModel.getWaterfall({
                        viewStart: 0,
                        viewEnd: 1,
                    });
                    expect(spans).toEqual(fullWaterfall);
                    // perform a window selection
                    spans = waterfallModel.getWaterfall({
                        viewStart: 0.4,
                        viewEnd: 0.65,
                    });
                    expected = tslib_1.__spreadArray([], tslib_1.__read(fullWaterfall));
                    expected[1] = {
                        type: 'out_of_view',
                        span: fullWaterfall[1].span,
                    };
                    expected[4] = {
                        type: 'out_of_view',
                        span: fullWaterfall[4].span,
                    };
                    expect(spans).toEqual(expected);
                    // toggle http filter with a window selection
                    waterfallModel.toggleOperationNameFilter('http');
                    spans = waterfallModel.getWaterfall({
                        viewStart: 0.4,
                        viewEnd: 0.65,
                    });
                    expect(spans).toEqual([
                        {
                            type: 'filtered_out',
                            span: fullWaterfall[0].span,
                        },
                        {
                            type: 'out_of_view',
                            span: fullWaterfall[1].span,
                        },
                        fullWaterfall[2],
                        fullWaterfall[3],
                        {
                            type: 'filtered_out',
                            span: fullWaterfall[4].span,
                        },
                        {
                            type: 'filtered_out',
                            span: fullWaterfall[6].span,
                        },
                    ]);
                    // toggle ops filters with a window selection and search query
                    // NOTE: http was toggled on in the previous case
                    waterfallModel.toggleOperationNameFilter('pageload');
                    waterfallModel.querySpanSearch('a453cc713e5baf9c');
                    expect(waterfallModel.searchQuery).toBe('a453cc713e5baf9c');
                    spans = waterfallModel.getWaterfall({
                        viewStart: 0.2,
                        viewEnd: 0.65,
                    });
                    expect(spans).toEqual([
                        {
                            type: 'filtered_out',
                            span: fullWaterfall[0].span,
                        },
                        {
                            type: 'filtered_out',
                            span: fullWaterfall[1].span,
                        },
                        fullWaterfall[2],
                        fullWaterfall[3],
                        {
                            type: 'filtered_out',
                            span: fullWaterfall[4].span,
                        },
                        {
                            type: 'filtered_out',
                            span: fullWaterfall[6].span,
                        },
                    ]);
                    return [2 /*return*/];
            }
        });
    }); });
    it('toggleSpanGroup()', function () {
        var waterfallModel = new waterfallModel_1.default(event);
        var spans = waterfallModel.getWaterfall({
            viewStart: 0,
            viewEnd: 1,
        });
        expect(spans).toEqual(fullWaterfall);
        // toggle a span group to hide their sub-tree
        waterfallModel.toggleSpanGroup('a453cc713e5baf9c');
        spans = waterfallModel.getWaterfall({
            viewStart: 0,
            viewEnd: 1,
        });
        expect(spans).toEqual(fullWaterfall.filter(function (_span, index) {
            // 5th span should be hidden
            return index !== 4;
        }));
        // toggle a span group to reveal their sub-tree
        waterfallModel.toggleSpanGroup('a453cc713e5baf9c');
        spans = waterfallModel.getWaterfall({
            viewStart: 0,
            viewEnd: 1,
        });
        expect(spans).toEqual(fullWaterfall);
    });
    it('span grouping - only child parent-child chain - root is not grouped', function () {
        var event2 = tslib_1.__assign(tslib_1.__assign({}, event), { entries: [] });
        var waterfallModel = new waterfallModel_1.default(event2);
        var spans = waterfallModel.getWaterfall({
            viewStart: 0,
            viewEnd: 1,
        });
        expect(spans).toEqual([
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[0]), { numOfSpanChildren: 0, toggleSpanGroup: undefined }),
        ]);
    });
    it('span grouping - only child parent-child chain - root span and a span (2 spans) are not grouped', function () {
        var event2 = tslib_1.__assign(tslib_1.__assign({}, event), { entries: [
                {
                    data: [event.entries[0].data[0]],
                    type: event_1.EntryType.SPANS,
                },
            ] });
        var waterfallModel = new waterfallModel_1.default(event2);
        var spans = waterfallModel.getWaterfall({
            viewStart: 0,
            viewEnd: 1,
        });
        expect(spans).toEqual([
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[0]), { numOfSpanChildren: 1, toggleSpanGroup: undefined }),
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1]), { isLastSibling: true, numOfSpanChildren: 0, toggleSpanGroup: undefined }),
        ]);
    });
    it('span grouping - only child parent-child chain - root span and 2 spans (3 spans) are not grouped', function () {
        var event2 = tslib_1.__assign(tslib_1.__assign({}, event), { entries: [
                {
                    data: [
                        event.entries[0].data[0],
                        tslib_1.__assign(tslib_1.__assign({}, event.entries[0].data[0]), { parent_span_id: event.entries[0].data[0].span_id, span_id: 'foo' }),
                    ],
                    type: event_1.EntryType.SPANS,
                },
            ] });
        var waterfallModel = new waterfallModel_1.default(event2);
        var spans = waterfallModel.getWaterfall({
            viewStart: 0,
            viewEnd: 1,
        });
        expect(spans).toEqual([
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[0]), { treeDepth: 0, numOfSpanChildren: 1, toggleSpanGroup: undefined }),
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1]), { treeDepth: 1, isLastSibling: true, numOfSpanChildren: 1, toggleSpanGroup: undefined }),
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1]), { span: tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1].span), { parent_span_id: event.entries[0].data[0].span_id, span_id: 'foo' }), treeDepth: 2, isLastSibling: true, numOfSpanChildren: 0, toggleSpanGroup: undefined }),
        ]);
    });
    it('span grouping - only child parent-child chain - root span and 3+ spans (4 spans) are not grouped', function () {
        var event2 = tslib_1.__assign(tslib_1.__assign({}, event), { entries: [
                {
                    data: [
                        event.entries[0].data[0],
                        tslib_1.__assign(tslib_1.__assign({}, event.entries[0].data[0]), { parent_span_id: event.entries[0].data[0].span_id, span_id: 'foo' }),
                        tslib_1.__assign(tslib_1.__assign({}, event.entries[0].data[0]), { parent_span_id: 'foo', span_id: 'bar' }),
                    ],
                    type: event_1.EntryType.SPANS,
                },
            ] });
        var waterfallModel = new waterfallModel_1.default(event2);
        var spans = waterfallModel.getWaterfall({
            viewStart: 0,
            viewEnd: 1,
        });
        // expect 1 or more spans are grouped
        expect(spans).toHaveLength(3);
        utils_1.assert(fullWaterfall[1].type === 'span');
        var collapsedWaterfallExpected = [
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[0]), { numOfSpanChildren: 1, toggleSpanGroup: undefined }),
            {
                type: 'span_group_chain',
                treeDepth: 1,
                continuingTreeDepths: fullWaterfall[1].continuingTreeDepths,
                span: tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1].span), { parent_span_id: 'foo', span_id: 'bar' }),
                spanGrouping: [
                    tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1]), { isLastSibling: true, numOfSpanChildren: 1, toggleSpanGroup: undefined }),
                    tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1]), { span: tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1].span), { parent_span_id: event.entries[0].data[0].span_id, span_id: 'foo' }), isLastSibling: true, numOfSpanChildren: 1, toggleSpanGroup: undefined }),
                ],
                showSpanGroup: false,
                toggleSpanGroup: expect.any(Function),
            },
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1]), { span: tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1].span), { parent_span_id: 'foo', span_id: 'bar' }), isLastSibling: true, numOfSpanChildren: 0, treeDepth: 2, toggleSpanGroup: undefined }),
        ];
        expect(spans).toEqual(collapsedWaterfallExpected);
        // Expand span group
        utils_1.assert(spans[1].type === 'span' && spans[1].toggleSpanGroup);
        spans[1].toggleSpanGroup();
        spans = waterfallModel.getWaterfall({
            viewStart: 0,
            viewEnd: 1,
        });
        // expect span group to be expanded
        expect(spans).toHaveLength(4);
        expect(spans).toEqual([
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[0]), { numOfSpanChildren: 1, treeDepth: 0, toggleSpanGroup: undefined }),
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1]), { isLastSibling: true, numOfSpanChildren: 1, treeDepth: 1, toggleSpanGroup: expect.any(Function) }),
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1]), { span: tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1].span), { parent_span_id: event.entries[0].data[0].span_id, span_id: 'foo' }), isLastSibling: true, numOfSpanChildren: 1, treeDepth: 2, toggleSpanGroup: undefined }),
            tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1]), { span: tslib_1.__assign(tslib_1.__assign({}, fullWaterfall[1].span), { parent_span_id: 'foo', span_id: 'bar' }), isLastSibling: true, numOfSpanChildren: 0, treeDepth: 3, toggleSpanGroup: undefined }),
        ]);
        // Collapse span group
        utils_1.assert(spans[1].type === 'span' && spans[1].toggleSpanGroup);
        spans[1].toggleSpanGroup();
        spans = waterfallModel.getWaterfall({
            viewStart: 0,
            viewEnd: 1,
        });
        expect(spans).toHaveLength(3);
        expect(spans).toEqual(collapsedWaterfallExpected);
    });
});
//# sourceMappingURL=waterfallModel.spec.jsx.map