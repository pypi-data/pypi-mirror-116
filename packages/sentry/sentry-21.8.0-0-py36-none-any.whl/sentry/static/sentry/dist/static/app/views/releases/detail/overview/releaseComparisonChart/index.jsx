Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var styles_1 = require("app/components/charts/styles");
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var notAvailable_1 = tslib_1.__importDefault(require("app/components/notAvailable"));
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var radio_1 = tslib_1.__importDefault(require("app/components/radio"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var utils_1 = require("app/utils");
var formatters_1 = require("app/utils/formatters");
var queryString_1 = require("app/utils/queryString");
var sessions_1 = require("app/utils/sessions");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_2 = require("app/views/releases/utils");
var utils_3 = require("../../utils");
var releaseEventsChart_1 = tslib_1.__importDefault(require("./releaseEventsChart"));
var releaseSessionsChart_1 = tslib_1.__importDefault(require("./releaseSessionsChart"));
function ReleaseComparisonChart(_a) {
    var release = _a.release, project = _a.project, releaseSessions = _a.releaseSessions, allSessions = _a.allSessions, platform = _a.platform, location = _a.location, loading = _a.loading, reloading = _a.reloading, errored = _a.errored, api = _a.api, organization = _a.organization, hasHealthData = _a.hasHealthData;
    var _b = tslib_1.__read(react_1.useState(null), 2), issuesTotals = _b[0], setIssuesTotals = _b[1];
    var _c = tslib_1.__read(react_1.useState(null), 2), eventsTotals = _c[0], setEventsTotals = _c[1];
    var _d = tslib_1.__read(react_1.useState(false), 2), eventsLoading = _d[0], setEventsLoading = _d[1];
    var charts = [];
    var hasDiscover = organization.features.includes('discover-basic') ||
        organization.features.includes('performance-view');
    var hasPerformance = organization.features.includes('performance-view');
    var _e = react_1.useMemo(function () {
        // Memoizing this so that it does not calculate different `end` for releases without events+sessions each rerender
        return utils_2.getReleaseParams({
            location: location,
            releaseBounds: utils_2.getReleaseBounds(release),
            defaultStatsPeriod: constants_1.DEFAULT_STATS_PERIOD,
            allowEmptyPeriod: true,
        });
    }, [release, location]), period = _e.statsPeriod, start = _e.start, end = _e.end, utc = _e.utc;
    react_1.useEffect(function () {
        if (hasDiscover || hasPerformance) {
            fetchEventsTotals();
            fetchIssuesTotals();
        }
    }, [period, start, end, organization.slug, location]);
    function fetchEventsTotals() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var url, commonQuery, _a, releaseTransactionTotals, allTransactionTotals, releaseErrorTotals, allErrorTotals, err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        url = "/organizations/" + organization.slug + "/eventsv2/";
                        commonQuery = tslib_1.__assign({ environment: queryString_1.decodeList(location.query.environment), project: queryString_1.decodeList(location.query.project), start: start, end: end }, (period ? { statsPeriod: period } : {}));
                        if (eventsTotals === null) {
                            setEventsLoading(true);
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(url, {
                                    query: tslib_1.__assign({ field: ['failure_rate()', 'count()'], query: new tokenizeSearch_1.QueryResults([
                                            'event.type:transaction',
                                            "release:" + release.version,
                                        ]).formatString() }, commonQuery),
                                }),
                                api.requestPromise(url, {
                                    query: tslib_1.__assign({ field: ['failure_rate()', 'count()'], query: new tokenizeSearch_1.QueryResults(['event.type:transaction']).formatString() }, commonQuery),
                                }),
                                api.requestPromise(url, {
                                    query: tslib_1.__assign({ field: ['count()'], query: new tokenizeSearch_1.QueryResults([
                                            'event.type:error',
                                            "release:" + release.version,
                                        ]).formatString() }, commonQuery),
                                }),
                                api.requestPromise(url, {
                                    query: tslib_1.__assign({ field: ['count()'], query: new tokenizeSearch_1.QueryResults(['event.type:error']).formatString() }, commonQuery),
                                }),
                            ])];
                    case 2:
                        _a = tslib_1.__read.apply(void 0, [_b.sent(), 4]), releaseTransactionTotals = _a[0], allTransactionTotals = _a[1], releaseErrorTotals = _a[2], allErrorTotals = _a[3];
                        setEventsTotals({
                            allErrorCount: allErrorTotals.data[0].count,
                            releaseErrorCount: releaseErrorTotals.data[0].count,
                            allTransactionCount: allTransactionTotals.data[0].count,
                            releaseTransactionCount: releaseTransactionTotals.data[0].count,
                            releaseFailureRate: releaseTransactionTotals.data[0].failure_rate,
                            allFailureRate: allTransactionTotals.data[0].failure_rate,
                        });
                        setEventsLoading(false);
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        setEventsTotals(null);
                        setEventsLoading(false);
                        Sentry.captureException(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function fetchIssuesTotals() {
        var _a, _b;
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var UNHANDLED_QUERY, HANDLED_QUERY, response, err_2;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        UNHANDLED_QUERY = "release:\"" + release.version + "\" error.handled:0";
                        HANDLED_QUERY = "release:\"" + release.version + "\" error.handled:1";
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/organizations/" + organization.slug + "/issues-count/", {
                                query: tslib_1.__assign(tslib_1.__assign({ project: project.id, environment: queryString_1.decodeList(location.query.environment), start: start, end: end }, (period ? { statsPeriod: period } : {})), { query: [UNHANDLED_QUERY, HANDLED_QUERY] }),
                            })];
                    case 2:
                        response = _c.sent();
                        setIssuesTotals({
                            handled: (_a = response[HANDLED_QUERY]) !== null && _a !== void 0 ? _a : 0,
                            unhandled: (_b = response[UNHANDLED_QUERY]) !== null && _b !== void 0 ? _b : 0,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _c.sent();
                        setIssuesTotals(null);
                        Sentry.captureException(err_2);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    var releaseCrashFreeSessions = sessions_1.getCrashFreeRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS);
    var allCrashFreeSessions = sessions_1.getCrashFreeRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS);
    var diffCrashFreeSessions = utils_1.defined(releaseCrashFreeSessions) && utils_1.defined(allCrashFreeSessions)
        ? releaseCrashFreeSessions - allCrashFreeSessions
        : null;
    var releaseHealthySessions = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY);
    var allHealthySessions = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY);
    var diffHealthySessions = utils_1.defined(releaseHealthySessions) && utils_1.defined(allHealthySessions)
        ? releaseHealthySessions - allHealthySessions
        : null;
    var releaseAbnormalSessions = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL);
    var allAbnormalSessions = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL);
    var diffAbnormalSessions = utils_1.defined(releaseAbnormalSessions) && utils_1.defined(allAbnormalSessions)
        ? releaseAbnormalSessions - allAbnormalSessions
        : null;
    var releaseErroredSessions = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED);
    var allErroredSessions = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED);
    var diffErroredSessions = utils_1.defined(releaseErroredSessions) && utils_1.defined(allErroredSessions)
        ? releaseErroredSessions - allErroredSessions
        : null;
    var releaseCrashedSessions = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED);
    var allCrashedSessions = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED);
    var diffCrashedSessions = utils_1.defined(releaseCrashedSessions) && utils_1.defined(allCrashedSessions)
        ? releaseCrashedSessions - allCrashedSessions
        : null;
    var releaseCrashFreeUsers = sessions_1.getCrashFreeRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS);
    var allCrashFreeUsers = sessions_1.getCrashFreeRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS);
    var diffCrashFreeUsers = utils_1.defined(releaseCrashFreeUsers) && utils_1.defined(allCrashFreeUsers)
        ? releaseCrashFreeUsers - allCrashFreeUsers
        : null;
    var releaseHealthyUsers = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY);
    var allHealthyUsers = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY);
    var diffHealthyUsers = utils_1.defined(releaseHealthyUsers) && utils_1.defined(allHealthyUsers)
        ? releaseHealthyUsers - allHealthyUsers
        : null;
    var releaseAbnormalUsers = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL);
    var allAbnormalUsers = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL);
    var diffAbnormalUsers = utils_1.defined(releaseAbnormalUsers) && utils_1.defined(allAbnormalUsers)
        ? releaseAbnormalUsers - allAbnormalUsers
        : null;
    var releaseErroredUsers = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED);
    var allErroredUsers = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED);
    var diffErroredUsers = utils_1.defined(releaseErroredUsers) && utils_1.defined(allErroredUsers)
        ? releaseErroredUsers - allErroredUsers
        : null;
    var releaseCrashedUsers = sessions_1.getSessionStatusRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED);
    var allCrashedUsers = sessions_1.getSessionStatusRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED);
    var diffCrashedUsers = utils_1.defined(releaseCrashedUsers) && utils_1.defined(allCrashedUsers)
        ? releaseCrashedUsers - allCrashedUsers
        : null;
    var releaseSessionsCount = sessions_1.getCount(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.SESSIONS);
    var allSessionsCount = sessions_1.getCount(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.SESSIONS);
    var releaseUsersCount = sessions_1.getCount(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS);
    var allUsersCount = sessions_1.getCount(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, types_1.SessionField.USERS);
    var diffFailure = (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseFailureRate) && (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allFailureRate)
        ? eventsTotals.releaseFailureRate - eventsTotals.allFailureRate
        : null;
    if (hasHealthData) {
        charts.push({
            type: types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS,
            role: 'parent',
            drilldown: null,
            thisRelease: utils_1.defined(releaseCrashFreeSessions)
                ? utils_2.displaySessionStatusPercent(releaseCrashFreeSessions)
                : null,
            allReleases: utils_1.defined(allCrashFreeSessions)
                ? utils_2.displaySessionStatusPercent(allCrashFreeSessions)
                : null,
            diff: utils_1.defined(diffCrashFreeSessions)
                ? utils_2.displaySessionStatusPercent(diffCrashFreeSessions)
                : null,
            diffDirection: diffCrashFreeSessions
                ? diffCrashFreeSessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffCrashFreeSessions
                ? diffCrashFreeSessions > 0
                    ? 'green300'
                    : 'red300'
                : null,
        }, {
            type: types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS,
            role: 'children',
            drilldown: null,
            thisRelease: utils_1.defined(releaseHealthySessions)
                ? utils_2.displaySessionStatusPercent(releaseHealthySessions)
                : null,
            allReleases: utils_1.defined(allHealthySessions)
                ? utils_2.displaySessionStatusPercent(allHealthySessions)
                : null,
            diff: utils_1.defined(diffHealthySessions)
                ? utils_2.displaySessionStatusPercent(diffHealthySessions)
                : null,
            diffDirection: diffHealthySessions
                ? diffHealthySessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffHealthySessions
                ? diffHealthySessions > 0
                    ? 'green300'
                    : 'red300'
                : null,
        }, {
            type: types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS,
            role: 'children',
            drilldown: null,
            thisRelease: utils_1.defined(releaseAbnormalSessions)
                ? utils_2.displaySessionStatusPercent(releaseAbnormalSessions)
                : null,
            allReleases: utils_1.defined(allAbnormalSessions)
                ? utils_2.displaySessionStatusPercent(allAbnormalSessions)
                : null,
            diff: utils_1.defined(diffAbnormalSessions)
                ? utils_2.displaySessionStatusPercent(diffAbnormalSessions)
                : null,
            diffDirection: diffAbnormalSessions
                ? diffAbnormalSessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffAbnormalSessions
                ? diffAbnormalSessions > 0
                    ? 'red300'
                    : 'green300'
                : null,
        }, {
            type: types_1.ReleaseComparisonChartType.ERRORED_SESSIONS,
            role: 'children',
            drilldown: utils_1.defined(issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.handled) ? (<tooltip_1.default title={locale_1.t('Open in Issues')}>
            <globalSelectionLink_1.default to={utils_2.getReleaseHandledIssuesUrl(organization.slug, project.id, release.version, { start: start, end: end, period: period !== null && period !== void 0 ? period : undefined })}>
              {locale_1.tct('([count] handled [issues])', {
                    count: (issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.handled)
                        ? issuesTotals.handled >= 100
                            ? '99+'
                            : issuesTotals.handled
                        : 0,
                    issues: locale_1.tn('issue', 'issues', issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.handled),
                })}
            </globalSelectionLink_1.default>
          </tooltip_1.default>) : null,
            thisRelease: utils_1.defined(releaseErroredSessions)
                ? utils_2.displaySessionStatusPercent(releaseErroredSessions)
                : null,
            allReleases: utils_1.defined(allErroredSessions)
                ? utils_2.displaySessionStatusPercent(allErroredSessions)
                : null,
            diff: utils_1.defined(diffErroredSessions)
                ? utils_2.displaySessionStatusPercent(diffErroredSessions)
                : null,
            diffDirection: diffErroredSessions
                ? diffErroredSessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffErroredSessions
                ? diffErroredSessions > 0
                    ? 'red300'
                    : 'green300'
                : null,
        }, {
            type: types_1.ReleaseComparisonChartType.CRASHED_SESSIONS,
            role: 'default',
            drilldown: utils_1.defined(issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.unhandled) ? (<tooltip_1.default title={locale_1.t('Open in Issues')}>
            <globalSelectionLink_1.default to={utils_2.getReleaseUnhandledIssuesUrl(organization.slug, project.id, release.version, { start: start, end: end, period: period !== null && period !== void 0 ? period : undefined })}>
              {locale_1.tct('([count] unhandled [issues])', {
                    count: (issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.unhandled)
                        ? issuesTotals.unhandled >= 100
                            ? '99+'
                            : issuesTotals.unhandled
                        : 0,
                    issues: locale_1.tn('issue', 'issues', issuesTotals === null || issuesTotals === void 0 ? void 0 : issuesTotals.unhandled),
                })}
            </globalSelectionLink_1.default>
          </tooltip_1.default>) : null,
            thisRelease: utils_1.defined(releaseCrashedSessions)
                ? utils_2.displaySessionStatusPercent(releaseCrashedSessions)
                : null,
            allReleases: utils_1.defined(allCrashedSessions)
                ? utils_2.displaySessionStatusPercent(allCrashedSessions)
                : null,
            diff: utils_1.defined(diffCrashedSessions)
                ? utils_2.displaySessionStatusPercent(diffCrashedSessions)
                : null,
            diffDirection: diffCrashedSessions
                ? diffCrashedSessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffCrashedSessions
                ? diffCrashedSessions > 0
                    ? 'red300'
                    : 'green300'
                : null,
        });
    }
    var hasUsers = !!sessions_1.getCount(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, types_1.SessionField.USERS);
    if (hasHealthData && (hasUsers || loading)) {
        charts.push({
            type: types_1.ReleaseComparisonChartType.CRASH_FREE_USERS,
            role: 'parent',
            drilldown: null,
            thisRelease: utils_1.defined(releaseCrashFreeUsers)
                ? utils_2.displaySessionStatusPercent(releaseCrashFreeUsers)
                : null,
            allReleases: utils_1.defined(allCrashFreeUsers)
                ? utils_2.displaySessionStatusPercent(allCrashFreeUsers)
                : null,
            diff: utils_1.defined(diffCrashFreeUsers)
                ? utils_2.displaySessionStatusPercent(diffCrashFreeUsers)
                : null,
            diffDirection: diffCrashFreeUsers
                ? diffCrashFreeUsers > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffCrashFreeUsers
                ? diffCrashFreeUsers > 0
                    ? 'green300'
                    : 'red300'
                : null,
        }, {
            type: types_1.ReleaseComparisonChartType.HEALTHY_USERS,
            role: 'children',
            drilldown: null,
            thisRelease: utils_1.defined(releaseHealthyUsers)
                ? utils_2.displaySessionStatusPercent(releaseHealthyUsers)
                : null,
            allReleases: utils_1.defined(allHealthyUsers)
                ? utils_2.displaySessionStatusPercent(allHealthyUsers)
                : null,
            diff: utils_1.defined(diffHealthyUsers)
                ? utils_2.displaySessionStatusPercent(diffHealthyUsers)
                : null,
            diffDirection: diffHealthyUsers ? (diffHealthyUsers > 0 ? 'up' : 'down') : null,
            diffColor: diffHealthyUsers
                ? diffHealthyUsers > 0
                    ? 'green300'
                    : 'red300'
                : null,
        }, {
            type: types_1.ReleaseComparisonChartType.ABNORMAL_USERS,
            role: 'children',
            drilldown: null,
            thisRelease: utils_1.defined(releaseAbnormalUsers)
                ? utils_2.displaySessionStatusPercent(releaseAbnormalUsers)
                : null,
            allReleases: utils_1.defined(allAbnormalUsers)
                ? utils_2.displaySessionStatusPercent(allAbnormalUsers)
                : null,
            diff: utils_1.defined(diffAbnormalUsers)
                ? utils_2.displaySessionStatusPercent(diffAbnormalUsers)
                : null,
            diffDirection: diffAbnormalUsers ? (diffAbnormalUsers > 0 ? 'up' : 'down') : null,
            diffColor: diffAbnormalUsers
                ? diffAbnormalUsers > 0
                    ? 'red300'
                    : 'green300'
                : null,
        }, {
            type: types_1.ReleaseComparisonChartType.ERRORED_USERS,
            role: 'children',
            drilldown: null,
            thisRelease: utils_1.defined(releaseErroredUsers)
                ? utils_2.displaySessionStatusPercent(releaseErroredUsers)
                : null,
            allReleases: utils_1.defined(allErroredUsers)
                ? utils_2.displaySessionStatusPercent(allErroredUsers)
                : null,
            diff: utils_1.defined(diffErroredUsers)
                ? utils_2.displaySessionStatusPercent(diffErroredUsers)
                : null,
            diffDirection: diffErroredUsers ? (diffErroredUsers > 0 ? 'up' : 'down') : null,
            diffColor: diffErroredUsers
                ? diffErroredUsers > 0
                    ? 'red300'
                    : 'green300'
                : null,
        }, {
            type: types_1.ReleaseComparisonChartType.CRASHED_USERS,
            role: 'default',
            drilldown: null,
            thisRelease: utils_1.defined(releaseCrashedUsers)
                ? utils_2.displaySessionStatusPercent(releaseCrashedUsers)
                : null,
            allReleases: utils_1.defined(allCrashedUsers)
                ? utils_2.displaySessionStatusPercent(allCrashedUsers)
                : null,
            diff: utils_1.defined(diffCrashedUsers)
                ? utils_2.displaySessionStatusPercent(diffCrashedUsers)
                : null,
            diffDirection: diffCrashedUsers ? (diffCrashedUsers > 0 ? 'up' : 'down') : null,
            diffColor: diffCrashedUsers
                ? diffCrashedUsers > 0
                    ? 'red300'
                    : 'green300'
                : null,
        });
    }
    if (hasPerformance) {
        charts.push({
            type: types_1.ReleaseComparisonChartType.FAILURE_RATE,
            role: 'default',
            drilldown: null,
            thisRelease: (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseFailureRate)
                ? formatters_1.formatPercentage(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseFailureRate)
                : null,
            allReleases: (eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allFailureRate)
                ? formatters_1.formatPercentage(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allFailureRate)
                : null,
            diff: diffFailure ? formatters_1.formatPercentage(Math.abs(diffFailure)) : null,
            diffDirection: diffFailure ? (diffFailure > 0 ? 'up' : 'down') : null,
            diffColor: diffFailure ? (diffFailure > 0 ? 'red300' : 'green300') : null,
        });
    }
    if (hasHealthData) {
        charts.push({
            type: types_1.ReleaseComparisonChartType.SESSION_COUNT,
            role: 'default',
            drilldown: null,
            thisRelease: utils_1.defined(releaseSessionsCount) ? (<count_1.default value={releaseSessionsCount}/>) : null,
            allReleases: utils_1.defined(allSessionsCount) ? (<count_1.default value={allSessionsCount}/>) : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        }, {
            type: types_1.ReleaseComparisonChartType.USER_COUNT,
            role: 'default',
            drilldown: null,
            thisRelease: utils_1.defined(releaseUsersCount) ? (<count_1.default value={releaseUsersCount}/>) : null,
            allReleases: utils_1.defined(allUsersCount) ? <count_1.default value={allUsersCount}/> : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        });
    }
    if (hasDiscover) {
        charts.push({
            type: types_1.ReleaseComparisonChartType.ERROR_COUNT,
            role: 'default',
            drilldown: null,
            thisRelease: utils_1.defined(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseErrorCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseErrorCount}/>) : null,
            allReleases: utils_1.defined(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allErrorCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allErrorCount}/>) : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        });
    }
    if (hasPerformance) {
        charts.push({
            type: types_1.ReleaseComparisonChartType.TRANSACTION_COUNT,
            role: 'default',
            drilldown: null,
            thisRelease: utils_1.defined(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseTransactionCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.releaseTransactionCount}/>) : null,
            allReleases: utils_1.defined(eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allTransactionCount) ? (<count_1.default value={eventsTotals === null || eventsTotals === void 0 ? void 0 : eventsTotals.allTransactionCount}/>) : null,
            diff: null,
            diffDirection: null,
            diffColor: null,
        });
    }
    function handleChartChange(chartType) {
        react_router_1.browserHistory.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { chart: chartType }) }));
    }
    function getChartDiff(diff, diffColor, diffDirection) {
        return diff ? (<Change color={utils_1.defined(diffColor) ? diffColor : undefined}>
        {diff}{' '}
        {utils_1.defined(diffDirection) ? (<icons_1.IconArrow direction={diffDirection} size="xs"/>) : (<StyledNotAvailable />)}
      </Change>) : null;
    }
    var activeChart = queryString_1.decodeScalar(location.query.chart, hasHealthData
        ? types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS
        : hasPerformance
            ? types_1.ReleaseComparisonChartType.FAILURE_RATE
            : types_1.ReleaseComparisonChartType.ERROR_COUNT);
    var chart = charts.find(function (ch) { return ch.type === activeChart; });
    if (!chart) {
        chart = charts[0];
        activeChart = charts[0].type;
    }
    var showPlaceholders = loading || eventsLoading;
    if (errored || !chart) {
        return (<panels_1.Panel>
        <errorPanel_1.default>
          <icons_1.IconWarning color="gray300" size="lg"/>
        </errorPanel_1.default>
      </panels_1.Panel>);
    }
    var titleChartDiff = chart.diff !== '0%' && chart.thisRelease !== '0%'
        ? getChartDiff(chart.diff, chart.diffColor, chart.diffDirection)
        : null;
    return (<react_1.Fragment>
      <ChartPanel>
        <styles_1.ChartContainer>
          {[
            types_1.ReleaseComparisonChartType.ERROR_COUNT,
            types_1.ReleaseComparisonChartType.TRANSACTION_COUNT,
            types_1.ReleaseComparisonChartType.FAILURE_RATE,
        ].includes(activeChart) ? (<releaseEventsChart_1.default release={release} project={project} chartType={activeChart} period={period !== null && period !== void 0 ? period : undefined} start={start} end={end} utc={utc === 'true'} value={chart.thisRelease} diff={titleChartDiff}/>) : (<releaseSessionsChart_1.default releaseSessions={releaseSessions} allSessions={allSessions} release={release} project={project} chartType={activeChart} platform={platform} period={period !== null && period !== void 0 ? period : undefined} start={start} end={end} utc={utc === 'true'} value={chart.thisRelease} diff={titleChartDiff} loading={loading} reloading={reloading}/>)}
        </styles_1.ChartContainer>
      </ChartPanel>
      <ChartTable headers={[
            <DescriptionCell key="description">{locale_1.t('Description')}</DescriptionCell>,
            <Cell key="releases">{locale_1.t('All Releases')}</Cell>,
            <Cell key="release">{locale_1.t('This Release')}</Cell>,
            <Cell key="change">{locale_1.t('Change')}</Cell>,
        ]} data-test-id="release-comparison-table">
        {charts.map(function (_a) {
            var type = _a.type, role = _a.role, drilldown = _a.drilldown, thisRelease = _a.thisRelease, allReleases = _a.allReleases, diff = _a.diff, diffDirection = _a.diffDirection, diffColor = _a.diffColor;
            return (<ChartTableRow key={type} htmlFor={type} isActive={type === activeChart} isLoading={showPlaceholders} role={role}>
                <DescriptionCell>
                  <TitleWrapper>
                    <radio_1.default id={type} disabled={false} checked={type === activeChart} onChange={function () { return handleChartChange(type); }}/>
                    {utils_3.releaseComparisonChartLabels[type]}&nbsp;{drilldown}
                  </TitleWrapper>
                </DescriptionCell>
                <Cell>
                  {showPlaceholders ? (<placeholder_1.default height="20px"/>) : utils_1.defined(allReleases) ? (allReleases) : (<notAvailable_1.default />)}
                </Cell>
                <Cell>
                  {showPlaceholders ? (<placeholder_1.default height="20px"/>) : utils_1.defined(thisRelease) ? (thisRelease) : (<notAvailable_1.default />)}
                </Cell>
                <Cell>
                  {showPlaceholders ? (<placeholder_1.default height="20px"/>) : utils_1.defined(diff) ? (getChartDiff(diff, diffColor, diffDirection)) : (<notAvailable_1.default />)}
                </Cell>
              </ChartTableRow>);
        })}
      </ChartTable>
    </react_1.Fragment>);
}
var ChartPanel = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom: none;\n  border-bottom-right-radius: 0;\n"], ["\n  margin-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom: none;\n  border-bottom-right-radius: 0;\n"])));
var Cell = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n  ", "\n"], ["\n  text-align: right;\n  ", "\n"])), overflowEllipsis_1.default);
var DescriptionCell = styled_1.default(Cell)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n  overflow: visible;\n"], ["\n  text-align: left;\n  overflow: visible;\n"])));
var TitleWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  position: relative;\n  z-index: 1;\n  background: ", ";\n\n  input {\n    width: ", ";\n    height: ", ";\n    flex-shrink: 0;\n    background-color: ", ";\n    margin-right: ", " !important;\n\n    &:checked:after {\n      width: ", ";\n      height: ", ";\n    }\n\n    &:hover {\n      cursor: pointer;\n    }\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  position: relative;\n  z-index: 1;\n  background: ", ";\n\n  input {\n    width: ", ";\n    height: ", ";\n    flex-shrink: 0;\n    background-color: ", ";\n    margin-right: ", " !important;\n\n    &:checked:after {\n      width: ", ";\n      height: ", ";\n    }\n\n    &:hover {\n      cursor: pointer;\n    }\n  }\n"])), function (p) { return p.theme.background; }, space_1.default(2), space_1.default(2), function (p) { return p.theme.background; }, space_1.default(1), space_1.default(1), space_1.default(1));
var Change = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  ", "\n"], ["\n  font-size: ", ";\n  ", "\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.color && "color: " + p.theme[p.color]; });
var ChartTableRow = styled_1.default('label')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  display: contents;\n  font-weight: 400;\n  margin-bottom: 0;\n\n  > * {\n    padding: ", " ", ";\n  }\n\n  ", "\n\n  &:hover {\n    cursor: pointer;\n    ", ", ", ", ", " {\n      ", "\n    }\n  }\n\n  ", "\n\n  ", "\n\n  ", "\n\n    ", "\n"], ["\n  display: contents;\n  font-weight: 400;\n  margin-bottom: 0;\n\n  > * {\n    padding: ", " ", ";\n  }\n\n  ", "\n\n  &:hover {\n    cursor: pointer;\n    " /* sc-selector */, ", " /* sc-selector */, ", "
    /* sc-selector */ , " {\n      ", "\n    }\n  }\n\n  ", "\n\n  ", "\n\n  ", "\n\n    ", "\n"])), space_1.default(1), space_1.default(2), function (p) {
    return p.isActive &&
        !p.isLoading && react_2.css(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n      ", ", ", ", ", " {\n        background-color: ", ";\n      }\n    "], ["\n      ", ", ", ", ", " {\n        background-color: ", ";\n      }\n    "])), Cell, DescriptionCell, TitleWrapper, p.theme.bodyBackground);
}, /* sc-selector */ Cell, /* sc-selector */ DescriptionCell, 
/* sc-selector */ TitleWrapper, function (p) { return !p.isLoading && "background-color: " + p.theme.bodyBackground; }, function (p) {
    return p.role === 'default' && react_2.css(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n      &:not(:last-child) {\n        ", ", ", " {\n          border-bottom: 1px solid ", ";\n        }\n      }\n    "], ["\n      &:not(:last-child) {\n        ", ", ", " {\n          border-bottom: 1px solid ", ";\n        }\n      }\n    "])), Cell, DescriptionCell, p.theme.border);
}, function (p) {
    return p.role === 'parent' && react_2.css(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n      ", ", ", " {\n        margin-top: ", ";\n      }\n    "], ["\n      ", ", ", " {\n        margin-top: ", ";\n      }\n    "])), Cell, DescriptionCell, space_1.default(0.75));
}, function (p) {
    return p.role === 'children' && react_2.css(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n      ", " {\n        padding-left: 44px;\n        position: relative;\n        &:before {\n          content: '';\n          width: 15px;\n          height: 36px;\n          position: absolute;\n          top: -17px;\n          left: 24px;\n          border-bottom: 1px solid ", ";\n          border-left: 1px solid ", ";\n        }\n      }\n    "], ["\n      ", " {\n        padding-left: 44px;\n        position: relative;\n        &:before {\n          content: '';\n          width: 15px;\n          height: 36px;\n          position: absolute;\n          top: -17px;\n          left: 24px;\n          border-bottom: 1px solid ", ";\n          border-left: 1px solid ", ";\n        }\n      }\n    "])), DescriptionCell, p.theme.border, p.theme.border);
}, function (p) {
    return (p.role === 'parent' || p.role === 'children') && react_2.css(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n      ", ", ", " {\n        padding-bottom: ", ";\n        padding-top: ", ";\n        border-bottom: 0;\n      }\n    "], ["\n      ", ", ", " {\n        padding-bottom: ", ";\n        padding-top: ", ";\n        border-bottom: 0;\n      }\n    "])), Cell, DescriptionCell, space_1.default(0.75), space_1.default(0.75));
});
var ChartTable = styled_1.default(panels_1.PanelTable)(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  border-top-left-radius: 0;\n  border-top-right-radius: 0;\n  grid-template-columns: minmax(424px, auto) repeat(3, minmax(min-content, 1fr));\n\n  > * {\n    border-bottom: 1px solid ", ";\n  }\n\n  @media (max-width: ", ") {\n    grid-template-columns: repeat(4, minmax(min-content, 1fr));\n  }\n"], ["\n  border-top-left-radius: 0;\n  border-top-right-radius: 0;\n  grid-template-columns: minmax(424px, auto) repeat(3, minmax(min-content, 1fr));\n\n  > * {\n    border-bottom: 1px solid ", ";\n  }\n\n  @media (max-width: ", ") {\n    grid-template-columns: repeat(4, minmax(min-content, 1fr));\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.breakpoints[2]; });
var StyledNotAvailable = styled_1.default(notAvailable_1.default)(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n"], ["\n  display: inline-block;\n"])));
exports.default = ReleaseComparisonChart;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=index.jsx.map