Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var traceFullQuery_1 = require("app/utils/performance/quickTrace/traceFullQuery");
var traceLiteQuery_1 = tslib_1.__importDefault(require("app/utils/performance/quickTrace/traceLiteQuery"));
var utils_1 = require("app/utils/performance/quickTrace/utils");
function QuickTraceQuery(_a) {
    var _b, _c;
    var children = _a.children, event = _a.event, props = tslib_1.__rest(_a, ["children", "event"]);
    var traceId = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id;
    if (!traceId) {
        return (<React.Fragment>
        {children({
                isLoading: false,
                error: null,
                trace: [],
                type: 'empty',
                currentEvent: null,
            })}
      </React.Fragment>);
    }
    var _d = utils_1.getTraceTimeRangeFromEvent(event), start = _d.start, end = _d.end;
    return (<traceLiteQuery_1.default eventId={event.id} traceId={traceId} start={start} end={end} {...props}>
      {function (traceLiteResults) { return (<traceFullQuery_1.TraceFullQuery eventId={event.id} traceId={traceId} start={start} end={end} {...props}>
          {function (traceFullResults) {
                var e_1, _a;
                var _b, _c, _d;
                if (!traceFullResults.isLoading &&
                    traceFullResults.error === null &&
                    traceFullResults.traces !== null) {
                    try {
                        for (var _e = tslib_1.__values(traceFullResults.traces), _f = _e.next(); !_f.done; _f = _e.next()) {
                            var subtrace = _f.value;
                            try {
                                var trace = utils_1.flattenRelevantPaths(event, subtrace);
                                return children(tslib_1.__assign(tslib_1.__assign({}, traceFullResults), { trace: trace, currentEvent: (_b = trace.find(function (e) { return utils_1.isCurrentEvent(e, event); })) !== null && _b !== void 0 ? _b : null }));
                            }
                            catch (_g) {
                                // let this fall through and check the next subtrace
                                // or use the trace lite results
                            }
                        }
                    }
                    catch (e_1_1) { e_1 = { error: e_1_1 }; }
                    finally {
                        try {
                            if (_f && !_f.done && (_a = _e.return)) _a.call(_e);
                        }
                        finally { if (e_1) throw e_1.error; }
                    }
                }
                if (!traceLiteResults.isLoading &&
                    traceLiteResults.error === null &&
                    traceLiteResults.trace !== null) {
                    var trace = traceLiteResults.trace;
                    return children(tslib_1.__assign(tslib_1.__assign({}, traceLiteResults), { currentEvent: (_c = trace.find(function (e) { return utils_1.isCurrentEvent(e, event); })) !== null && _c !== void 0 ? _c : null }));
                }
                return children({
                    // only use the light results loading state if it didn't error
                    // if it did, we should rely on the full results
                    isLoading: traceLiteResults.error
                        ? traceFullResults.isLoading
                        : traceLiteResults.isLoading || traceFullResults.isLoading,
                    // swallow any errors from the light results because we
                    // should rely on the full results in this situations
                    error: traceFullResults.error,
                    trace: [],
                    // if we reach this point but there were some traces in the full results,
                    // that means there were other transactions in the trace, but the current
                    // event could not be found
                    type: ((_d = traceFullResults.traces) === null || _d === void 0 ? void 0 : _d.length) ? 'missing' : 'empty',
                    currentEvent: null,
                });
            }}
        </traceFullQuery_1.TraceFullQuery>); }}
    </traceLiteQuery_1.default>);
}
exports.default = QuickTraceQuery;
//# sourceMappingURL=quickTraceQuery.jsx.map