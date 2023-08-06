Object.defineProperty(exports, "__esModule", { value: true });
exports.metric = exports.analytics = exports.trackDeprecated = exports.logExperiment = exports.trackAdhocEvent = exports.trackAnalyticsEvent = exports.trackAnalyticsEventV2 = void 0;
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var hookStore_1 = tslib_1.__importDefault(require("app/stores/hookStore"));
/**
 * Analytics and metric tracking functionality.
 *
 * These are primarily driven through hooks provided through the hookstore. For
 * sentry.io these are currently mapped to our in-house analytics backend
 * 'Reload' and the Amplitude service.
 *
 * NOTE: sentry.io contributors, you will need to ensure that the eventKey
 *       passed exists as an event key in the Reload events.py configuration:
 *
 *       https://github.com/getsentry/reload/blob/master/reload_app/events.py
 *
 * NOTE: sentry.io contributors, if you are using `gauge` or `increment` the
 *       name must be added to the Reload metrics module:
 *
 *       https://github.com/getsentry/reload/blob/master/reload_app/metrics/__init__.py
 */
/**
 * This should be with all analytics events regardless of the analytics destination
 * which includes Reload, Amplitude, and Google Analytics.
 * All events go to Reload. If eventName is defined, events also go to Amplitude.
 * For more details, refer to the API defined in hooks.
 */
var trackAnalyticsEventV2 = function (data, options) {
    return hookStore_1.default.get('analytics:track-event-v2').forEach(function (cb) { return cb(data, options); });
};
exports.trackAnalyticsEventV2 = trackAnalyticsEventV2;
/**
 * @deprecated Prefer `trackAnalyticsEventV2`
 */
var trackAnalyticsEvent = function (options) {
    return hookStore_1.default.get('analytics:track-event').forEach(function (cb) { return cb(options); });
};
exports.trackAnalyticsEvent = trackAnalyticsEvent;
/**
 * @deprecated Prefer `trackAnalyticsEventV2`
 */
var trackAdhocEvent = function (options) {
    return hookStore_1.default.get('analytics:track-adhoc-event').forEach(function (cb) { return cb(options); });
};
exports.trackAdhocEvent = trackAdhocEvent;
/**
 * This should be used to log when a `organization.experiments` experiment
 * variant is checked in the application.
 *
 * Refer for the backend implementation provided through HookStore for more
 * details.
 */
var logExperiment = function (options) {
    return hookStore_1.default.get('analytics:log-experiment').forEach(function (cb) { return cb(options); });
};
exports.logExperiment = logExperiment;
/**
 * Helper function for `trackAnalyticsEvent` to generically track usage of deprecated features
 *
 * @param feature A name to identify the feature you are tracking
 * @param orgId The organization id
 * @param url [optional] The URL
 */
var trackDeprecated = function (feature, orgId, url) {
    if (url === void 0) { url = ''; }
    return exports.trackAdhocEvent({
        eventKey: 'deprecated.feature',
        feature: feature,
        url: url,
        org_id: orgId && Number(orgId),
    });
};
exports.trackDeprecated = trackDeprecated;
/**
 * Legacy analytics tracking.
 *
 * @deprecated Prefer `trackAnalyticsEvent` and `trackAdhocEvent`.
 */
var analytics = function (name, data) {
    return hookStore_1.default.get('analytics:event').forEach(function (cb) { return cb(name, data); });
};
exports.analytics = analytics;
/**
 * Used to pass data between metric.mark() and metric.measure()
 */
var metricDataStore = new Map();
/**
 * Record metrics.
 */
var metric = function (name, value, tags) {
    return hookStore_1.default.get('metrics:event').forEach(function (cb) { return cb(name, value, tags); });
};
exports.metric = metric;
// JSDOM implements window.performance but not window.performance.mark
var CAN_MARK = window.performance &&
    typeof window.performance.mark === 'function' &&
    typeof window.performance.measure === 'function' &&
    typeof window.performance.getEntriesByName === 'function' &&
    typeof window.performance.clearMeasures === 'function';
exports.metric.mark = function metricMark(_a) {
    var name = _a.name, _b = _a.data, data = _b === void 0 ? {} : _b;
    // Just ignore if browser is old enough that it doesn't support this
    if (!CAN_MARK) {
        return;
    }
    if (!name) {
        throw new Error('Invalid argument provided to `metric.mark`');
    }
    window.performance.mark(name);
    metricDataStore.set(name, data);
};
/**
 * Performs a measurement between `start` and `end` (or now if `end` is not
 * specified) Calls `metric` with `name` and the measured time difference.
 */
exports.metric.measure = function metricMeasure(_a) {
    var _b = _a === void 0 ? {} : _a, name = _b.name, start = _b.start, end = _b.end, _c = _b.data, data = _c === void 0 ? {} : _c, noCleanup = _b.noCleanup;
    // Just ignore if browser is old enough that it doesn't support this
    if (!CAN_MARK) {
        return;
    }
    if (!name || !start) {
        throw new Error('Invalid arguments provided to `metric.measure`');
    }
    var endMarkName = end;
    // Can't destructure from performance
    var performance = window.performance;
    // NOTE: Edge REQUIRES an end mark if it is given a start mark
    // If we don't have an end mark, create one now.
    if (!end) {
        endMarkName = start + "-end";
        performance.mark(endMarkName);
    }
    // Check if starting mark exists
    if (!performance.getEntriesByName(start, 'mark').length) {
        return;
    }
    performance.measure(name, start, endMarkName);
    var startData = metricDataStore.get(start) || {};
    // Retrieve measurement entries
    performance
        .getEntriesByName(name, 'measure')
        .forEach(function (measurement) {
        return exports.metric(measurement.name, measurement.duration, tslib_1.__assign(tslib_1.__assign({}, startData), data));
    });
    // By default, clean up measurements
    if (!noCleanup) {
        performance.clearMeasures(name);
        performance.clearMarks(start);
        performance.clearMarks(endMarkName);
        metricDataStore.delete(start);
    }
};
/**
 * Used to pass data between startTransaction and endTransaction
 */
var transactionDataStore = new Map();
var getCurrentTransaction = function () {
    var _a;
    return (_a = Sentry.getCurrentHub().getScope()) === null || _a === void 0 ? void 0 : _a.getTransaction();
};
exports.metric.startTransaction = function (_a) {
    var _b;
    var name = _a.name, traceId = _a.traceId, op = _a.op;
    if (!traceId) {
        traceId = (_b = getCurrentTransaction()) === null || _b === void 0 ? void 0 : _b.traceId;
    }
    var transaction = Sentry.startTransaction({ name: name, op: op, traceId: traceId });
    transactionDataStore[name] = transaction;
    return transaction;
};
exports.metric.endTransaction = function (_a) {
    var name = _a.name;
    var transaction = transactionDataStore[name];
    if (transaction) {
        transaction.finish();
    }
};
//# sourceMappingURL=analytics.jsx.map