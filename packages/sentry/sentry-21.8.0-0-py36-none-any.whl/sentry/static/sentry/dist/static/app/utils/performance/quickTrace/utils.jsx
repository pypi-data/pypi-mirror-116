Object.defineProperty(exports, "__esModule", { value: true });
exports.isTraceFullDetailed = exports.isTraceFull = exports.filterTrace = exports.reduceTrace = exports.getTraceTimeRangeFromEvent = exports.makeEventView = exports.getTraceRequestPayload = exports.beforeFetch = exports.parseQuickTrace = exports.flattenRelevantPaths = exports.isCurrentEvent = exports.isTransaction = void 0;
var tslib_1 = require("tslib");
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var moment_timezone_1 = tslib_1.__importDefault(require("moment-timezone"));
var utils_1 = require("app/components/events/interfaces/spans/utils");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var analytics_1 = require("app/utils/analytics");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
function isTransaction(event) {
    return event.type === 'transaction';
}
exports.isTransaction = isTransaction;
/**
 * An event can be an error or a transaction. We need to check whether the current
 * event id is in the list of errors as well
 */
function isCurrentEvent(event, currentEvent) {
    if (isTransaction(currentEvent)) {
        return event.event_id === currentEvent.id;
    }
    else {
        return (event.errors !== undefined && event.errors.some(function (e) { return e.event_id === currentEvent.id; }));
    }
}
exports.isCurrentEvent = isCurrentEvent;
/**
 * The `events-full` endpoint returns the full trace containing the specified event.
 * This means any sibling paths in the trace will also be returned.
 *
 * This method strips away these sibling paths leaving only the path from the root to
 * the specified event and all of its children/descendants.
 *
 * This method additionally flattens the trace into an array of the transactions in
 * the trace.
 */
function flattenRelevantPaths(currentEvent, traceFull) {
    var e_1, _a, e_2, _b, e_3, _c;
    var relevantPath = [];
    var events = [];
    /**
     * First find a path from the root transaction to the current transaction via
     * a breadth first search. This adds all transactions from the root to the
     * current transaction (excluding the current transaction itself), to the
     * relevant path.
     */
    var paths = [{ event: traceFull, path: [] }];
    while (paths.length) {
        var current = paths.shift();
        if (isCurrentEvent(current.event, currentEvent)) {
            try {
                for (var _d = (e_1 = void 0, tslib_1.__values(current.path)), _e = _d.next(); !_e.done; _e = _d.next()) {
                    var node = _e.value;
                    relevantPath.push(node);
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
                }
                finally { if (e_1) throw e_1.error; }
            }
            events.push(current.event);
        }
        else {
            var path = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(current.path)), [simplifyEvent(current.event)]);
            try {
                for (var _f = (e_2 = void 0, tslib_1.__values(current.event.children)), _g = _f.next(); !_g.done; _g = _f.next()) {
                    var child = _g.value;
                    paths.push({ event: child, path: path });
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
                }
                finally { if (e_2) throw e_2.error; }
            }
        }
    }
    if (!events.length) {
        throw new Error('No relevant path exists!');
    }
    /**
     * Traverse all transactions from current transaction onwards and add
     * them all to the relevant path.
     */
    while (events.length) {
        var current = events.shift();
        try {
            for (var _h = (e_3 = void 0, tslib_1.__values(current.children)), _j = _h.next(); !_j.done; _j = _h.next()) {
                var child = _j.value;
                events.push(child);
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (_j && !_j.done && (_c = _h.return)) _c.call(_h);
            }
            finally { if (e_3) throw e_3.error; }
        }
        relevantPath.push(simplifyEvent(current));
    }
    return relevantPath;
}
exports.flattenRelevantPaths = flattenRelevantPaths;
function simplifyEvent(event) {
    return omit_1.default(event, ['children']);
}
function parseQuickTrace(quickTrace, event, organization) {
    var _a, _b, _c;
    var type = quickTrace.type, trace = quickTrace.trace;
    if (type === 'empty' || trace === null) {
        throw new Error('Current event not in trace navigator!');
    }
    var isFullTrace = type === 'full';
    var current = (_a = trace.find(function (e) { return isCurrentEvent(e, event); })) !== null && _a !== void 0 ? _a : null;
    if (current === null) {
        throw new Error('Current event not in trace navigator!');
    }
    /**
     * The parent event is the direct ancestor of the current event.
     * This takes priority over the root, meaning if the parent is
     * the root of the trace, this favours showing it as the parent.
     */
    var parent = current.parent_event_id
        ? (_b = trace.find(function (e) { return e.event_id === current.parent_event_id; })) !== null && _b !== void 0 ? _b : null
        : null;
    /**
     * The root event is the first event in the trace. This has lower priority
     * than the parent event, meaning if the root event is the parent event of
     * the current event, this favours showing it as the parent event.
     */
    var root = (_c = trace.find(function (e) {
        // a root can't be the current event
        return e.event_id !== current.event_id &&
            // a root can't be the direct parent
            e.event_id !== (parent === null || parent === void 0 ? void 0 : parent.event_id) &&
            // a root has to to be the first generation
            e.generation === 0;
    })) !== null && _c !== void 0 ? _c : null;
    var isChildren = function (e) { return e.parent_event_id === current.event_id; };
    var isDescendant = function (e) {
        // the current generation needs to be known to determine a descendant
        return current.generation !== null &&
            // the event's generation needs to be known to determine a descendant
            e.generation !== null &&
            // a descendant is the generation after the direct children
            current.generation + 1 < e.generation;
    };
    var isAncestor = function (e) {
        // the current generation needs to be known to determine an ancestor
        return current.generation !== null &&
            // the event's generation needs to be known to determine an ancestor
            e.generation !== null &&
            // an ancestor can't be the root
            e.generation > 0 &&
            // an ancestor is the generation before the direct parent
            current.generation - 1 > e.generation;
    };
    var ancestors = isFullTrace ? [] : null;
    var children = [];
    var descendants = isFullTrace ? [] : null;
    var projects = new Set();
    trace.forEach(function (e) {
        projects.add(e.project_id);
        if (isChildren(e)) {
            children.push(e);
        }
        else if (isFullTrace) {
            if (isAncestor(e)) {
                ancestors === null || ancestors === void 0 ? void 0 : ancestors.push(e);
            }
            else if (isDescendant(e)) {
                descendants === null || descendants === void 0 ? void 0 : descendants.push(e);
            }
        }
    });
    if (isFullTrace && projects.size > 1) {
        handleProjectMeta(organization, projects.size);
    }
    return {
        root: root,
        ancestors: ancestors === null ? null : sortTraceLite(ancestors),
        parent: parent,
        current: current,
        children: sortTraceLite(children),
        descendants: descendants === null ? null : sortTraceLite(descendants),
    };
}
exports.parseQuickTrace = parseQuickTrace;
function sortTraceLite(trace) {
    return trace.sort(function (a, b) { return b['transaction.duration'] - a['transaction.duration']; });
}
function beforeFetch(api) {
    api.clear();
}
exports.beforeFetch = beforeFetch;
function getTraceRequestPayload(_a) {
    var eventView = _a.eventView, location = _a.location;
    return omit_1.default(eventView.getEventsAPIPayload(location), ['field', 'sort', 'per_page']);
}
exports.getTraceRequestPayload = getTraceRequestPayload;
function makeEventView(_a) {
    var start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod;
    return eventView_1.default.fromSavedQuery({
        id: undefined,
        version: 2,
        name: '',
        // This field doesn't actually do anything,
        // just here to satisfy a constraint in EventView.
        fields: ['transaction.duration'],
        projects: [globalSelectionHeader_1.ALL_ACCESS_PROJECTS],
        query: '',
        environment: [],
        start: start,
        end: end,
        range: statsPeriod,
    });
}
exports.makeEventView = makeEventView;
function getTraceTimeRangeFromEvent(event) {
    var start = isTransaction(event)
        ? event.startTimestamp
        : moment_timezone_1.default(event.dateReceived ? event.dateReceived : event.dateCreated).valueOf() /
            1000;
    var end = isTransaction(event) ? event.endTimestamp : start;
    return utils_1.getTraceDateTimeRange({ start: start, end: end });
}
exports.getTraceTimeRangeFromEvent = getTraceTimeRangeFromEvent;
function reduceTrace(trace, visitor, initialValue) {
    var e_4, _a;
    var result = initialValue;
    var events = [trace];
    while (events.length) {
        var current = events.pop();
        try {
            for (var _b = (e_4 = void 0, tslib_1.__values(current.children)), _c = _b.next(); !_c.done; _c = _b.next()) {
                var child = _c.value;
                events.push(child);
            }
        }
        catch (e_4_1) { e_4 = { error: e_4_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_4) throw e_4.error; }
        }
        result = visitor(result, current);
    }
    return result;
}
exports.reduceTrace = reduceTrace;
function filterTrace(trace, predicate) {
    return reduceTrace(trace, function (transactions, transaction) {
        if (predicate(transaction)) {
            transactions.push(transaction);
        }
        return transactions;
    }, []);
}
exports.filterTrace = filterTrace;
function isTraceFull(transaction) {
    return Boolean(transaction.event_id);
}
exports.isTraceFull = isTraceFull;
function isTraceFullDetailed(transaction) {
    return Boolean(transaction.event_id);
}
exports.isTraceFullDetailed = isTraceFullDetailed;
function handleProjectMeta(organization, projects) {
    analytics_1.trackAnalyticsEvent({
        eventKey: 'quick_trace.connected_services',
        eventName: 'Quick Trace: Connected Services',
        organization_id: parseInt(organization.id, 10),
        projects: projects,
    });
}
//# sourceMappingURL=utils.jsx.map