Object.defineProperty(exports, "__esModule", { value: true });
exports.trackAdvancedAnalyticsEvent = exports.getAnalyticsSessionId = exports.clearAnalyticsSession = exports.startAnalyticsSession = void 0;
var tslib_1 = require("tslib");
var analytics_1 = require("app/utils/analytics");
var growthAnalyticsEvents_1 = require("app/utils/growthAnalyticsEvents");
var guid_1 = require("app/utils/guid");
var integrationEvents_1 = require("app/utils/integrationEvents");
var issueEvents_1 = require("app/utils/issueEvents");
var performanceEvents_1 = require("app/utils/performanceEvents");
var ANALYTICS_SESSION = 'ANALYTICS_SESSION';
var startAnalyticsSession = function () {
    var sessionId = guid_1.uniqueId();
    window.sessionStorage.setItem(ANALYTICS_SESSION, sessionId);
    return sessionId;
};
exports.startAnalyticsSession = startAnalyticsSession;
var clearAnalyticsSession = function () {
    window.sessionStorage.removeItem(ANALYTICS_SESSION);
};
exports.clearAnalyticsSession = clearAnalyticsSession;
var getAnalyticsSessionId = function () {
    return window.sessionStorage.getItem(ANALYTICS_SESSION);
};
exports.getAnalyticsSessionId = getAnalyticsSessionId;
var hasAnalyticsDebug = function () { return window.localStorage.getItem('DEBUG_ANALYTICS') === '1'; };
var allEventMap = tslib_1.__assign(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, integrationEvents_1.integrationEventMap), growthAnalyticsEvents_1.growthEventMap), issueEvents_1.issueEventMap), performanceEvents_1.performanceEventMap);
/**
 * Tracks an event for analytics.
 * Must be tied to an organization.
 * Uses the current session ID or generates a new one if startSession == true.
 * An analytics session corresponds to a single action funnel such as installation.
 * Tracking by session allows us to track individual funnel attempts for a single user.
 */
function trackAdvancedAnalyticsEvent(eventKey, analyticsParams, options) {
    var eventName = allEventMap[eventKey];
    // need to destructure the org here to make TS happy
    var organization = analyticsParams.organization, rest = tslib_1.__rest(analyticsParams, ["organization"]);
    var params = tslib_1.__assign({ eventKey: eventKey, eventName: eventName, organization: organization }, rest);
    // could put this into a debug method or for the main trackAnalyticsEvent event
    if (hasAnalyticsDebug()) {
        // eslint-disable-next-line no-console
        console.log('trackAdvancedAnalytics', params);
    }
    // only apply options if required to make mock assertions easier
    if (options) {
        analytics_1.trackAnalyticsEventV2(params, options);
    }
    else {
        analytics_1.trackAnalyticsEventV2(params);
    }
}
exports.trackAdvancedAnalyticsEvent = trackAdvancedAnalyticsEvent;
//# sourceMappingURL=advancedAnalytics.jsx.map