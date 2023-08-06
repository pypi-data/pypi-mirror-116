Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var react_1 = require("@emotion/react");
var round_1 = tslib_1.__importDefault(require("lodash/round"));
var areaChart_1 = tslib_1.__importDefault(require("app/components/charts/areaChart"));
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var stackedAreaChart_1 = tslib_1.__importDefault(require("app/components/charts/stackedAreaChart"));
var styles_1 = require("app/components/charts/styles");
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var locale_1 = require("app/locale");
var types_1 = require("app/types");
var utils_1 = require("app/utils");
var sessions_1 = require("app/utils/sessions");
var utils_2 = require("app/views/releases/utils");
var utils_3 = require("../../utils");
var utils_4 = require("../chart/utils");
var ReleaseSessionsChart = /** @class */ (function (_super) {
    tslib_1.__extends(ReleaseSessionsChart, _super);
    function ReleaseSessionsChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.formatTooltipValue = function (value, label) {
            if (label && Object.values(utils_3.releaseMarkLinesLabels).includes(label)) {
                return '';
            }
            var chartType = _this.props.chartType;
            if (value === null) {
                return '\u2015';
            }
            switch (chartType) {
                case types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
                case types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS:
                case types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS:
                case types_1.ReleaseComparisonChartType.ERRORED_SESSIONS:
                case types_1.ReleaseComparisonChartType.CRASHED_SESSIONS:
                case types_1.ReleaseComparisonChartType.CRASH_FREE_USERS:
                case types_1.ReleaseComparisonChartType.HEALTHY_USERS:
                case types_1.ReleaseComparisonChartType.ABNORMAL_USERS:
                case types_1.ReleaseComparisonChartType.ERRORED_USERS:
                case types_1.ReleaseComparisonChartType.CRASHED_USERS:
                    return utils_1.defined(value) ? value + "%" : '\u2015';
                case types_1.ReleaseComparisonChartType.SESSION_COUNT:
                case types_1.ReleaseComparisonChartType.USER_COUNT:
                default:
                    return typeof value === 'number' ? value.toLocaleString() : value;
            }
        };
        return _this;
    }
    ReleaseSessionsChart.prototype.getYAxis = function () {
        var _a = this.props, theme = _a.theme, chartType = _a.chartType;
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
            case types_1.ReleaseComparisonChartType.CRASH_FREE_USERS:
                return {
                    max: 100,
                    scale: true,
                    axisLabel: {
                        formatter: function (value) { return utils_2.displayCrashFreePercent(value); },
                        color: theme.chartLabel,
                    },
                };
            case types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS:
            case types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS:
            case types_1.ReleaseComparisonChartType.ERRORED_SESSIONS:
            case types_1.ReleaseComparisonChartType.CRASHED_SESSIONS:
            case types_1.ReleaseComparisonChartType.HEALTHY_USERS:
            case types_1.ReleaseComparisonChartType.ABNORMAL_USERS:
            case types_1.ReleaseComparisonChartType.ERRORED_USERS:
            case types_1.ReleaseComparisonChartType.CRASHED_USERS:
                return {
                    scale: true,
                    axisLabel: {
                        formatter: function (value) { return round_1.default(value, 2) + "%"; },
                        color: theme.chartLabel,
                    },
                };
            case types_1.ReleaseComparisonChartType.SESSION_COUNT:
            case types_1.ReleaseComparisonChartType.USER_COUNT:
            default:
                return undefined;
        }
    };
    ReleaseSessionsChart.prototype.getChart = function () {
        var chartType = this.props.chartType;
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
            case types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS:
            case types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS:
            case types_1.ReleaseComparisonChartType.ERRORED_SESSIONS:
            case types_1.ReleaseComparisonChartType.CRASHED_SESSIONS:
            case types_1.ReleaseComparisonChartType.CRASH_FREE_USERS:
            case types_1.ReleaseComparisonChartType.HEALTHY_USERS:
            case types_1.ReleaseComparisonChartType.ABNORMAL_USERS:
            case types_1.ReleaseComparisonChartType.ERRORED_USERS:
            case types_1.ReleaseComparisonChartType.CRASHED_USERS:
            default:
                return areaChart_1.default;
            case types_1.ReleaseComparisonChartType.SESSION_COUNT:
            case types_1.ReleaseComparisonChartType.USER_COUNT:
                return stackedAreaChart_1.default;
        }
    };
    ReleaseSessionsChart.prototype.getColors = function () {
        var _a = this.props, theme = _a.theme, chartType = _a.chartType;
        var colors = theme.charts.getColorPalette(14);
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
                return [colors[0]];
            case types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS:
                return [theme.green300];
            case types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS:
                return [colors[15]];
            case types_1.ReleaseComparisonChartType.ERRORED_SESSIONS:
                return [colors[12]];
            case types_1.ReleaseComparisonChartType.CRASHED_SESSIONS:
                return [theme.red300];
            case types_1.ReleaseComparisonChartType.CRASH_FREE_USERS:
                return [colors[6]];
            case types_1.ReleaseComparisonChartType.HEALTHY_USERS:
                return [theme.green300];
            case types_1.ReleaseComparisonChartType.ABNORMAL_USERS:
                return [colors[15]];
            case types_1.ReleaseComparisonChartType.ERRORED_USERS:
                return [colors[12]];
            case types_1.ReleaseComparisonChartType.CRASHED_USERS:
                return [theme.red300];
            case types_1.ReleaseComparisonChartType.SESSION_COUNT:
            case types_1.ReleaseComparisonChartType.USER_COUNT:
            default:
                return undefined;
        }
    };
    ReleaseSessionsChart.prototype.getSeries = function (chartType) {
        var _a = this.props, releaseSessions = _a.releaseSessions, allSessions = _a.allSessions, release = _a.release, location = _a.location, project = _a.project, theme = _a.theme;
        if (!releaseSessions) {
            return {};
        }
        var markLines = utils_3.generateReleaseMarkLines(release, project, theme, location);
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getCrashFreeRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getCrashFreeRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.HEALTHY_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.ABNORMAL_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.ERRORED_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.CRASHED_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.SESSIONS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.CRASH_FREE_USERS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getCrashFreeRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getCrashFreeRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.HEALTHY_USERS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.HEALTHY),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.ABNORMAL_USERS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ABNORMAL),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.ERRORED_USERS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.ERRORED),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.CRASHED_USERS:
                return {
                    series: [
                        {
                            seriesName: locale_1.t('This Release'),
                            connectNulls: true,
                            data: sessions_1.getSessionStatusRateSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: locale_1.t('All Releases'),
                            data: sessions_1.getSessionStatusRateSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, types_1.SessionField.USERS, types_1.SessionStatus.CRASHED),
                        },
                    ],
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.SESSION_COUNT:
                return {
                    series: Object.values(utils_4.fillChartDataFromSessionsResponse({
                        response: releaseSessions,
                        field: types_1.SessionField.SESSIONS,
                        groupBy: 'session.status',
                        chartData: utils_4.initSessionsBreakdownChartData(theme),
                    })),
                    markLines: markLines,
                };
            case types_1.ReleaseComparisonChartType.USER_COUNT:
                return {
                    series: Object.values(utils_4.fillChartDataFromSessionsResponse({
                        response: releaseSessions,
                        field: types_1.SessionField.USERS,
                        groupBy: 'session.status',
                        chartData: utils_4.initSessionsBreakdownChartData(theme),
                    })),
                    markLines: markLines,
                };
            default:
                return {};
        }
    };
    ReleaseSessionsChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, chartType = _a.chartType, router = _a.router, period = _a.period, start = _a.start, end = _a.end, utc = _a.utc, value = _a.value, diff = _a.diff, loading = _a.loading, reloading = _a.reloading;
        var Chart = this.getChart();
        var _b = this.getSeries(chartType), series = _b.series, previousSeries = _b.previousSeries, markLines = _b.markLines;
        var legend = {
            right: 10,
            top: 0,
            data: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read((series !== null && series !== void 0 ? series : []))), tslib_1.__read((previousSeries !== null && previousSeries !== void 0 ? previousSeries : []))).map(function (s) { return s.seriesName; }),
        };
        return (<transitionChart_1.default loading={loading} reloading={reloading} height="240px">
        <transparentLoadingMask_1.default visible={reloading}/>
        <styles_1.HeaderTitleLegend aria-label={locale_1.t('Chart Title')}>
          {utils_3.releaseComparisonChartTitles[chartType]}
          {utils_3.releaseComparisonChartHelp[chartType] && (<questionTooltip_1.default size="sm" position="top" title={utils_3.releaseComparisonChartHelp[chartType]}/>)}
        </styles_1.HeaderTitleLegend>

        <styles_1.HeaderValue aria-label={locale_1.t('Chart Value')}>
          {value} {diff}
        </styles_1.HeaderValue>

        <chartZoom_1.default router={router} period={period} utc={utc} start={start} end={end} usePageDate>
          {function (zoomRenderProps) { return (<Chart legend={legend} series={tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read((series !== null && series !== void 0 ? series : []))), tslib_1.__read((markLines !== null && markLines !== void 0 ? markLines : [])))} previousPeriod={previousSeries !== null && previousSeries !== void 0 ? previousSeries : []} {...zoomRenderProps} grid={{
                    left: '10px',
                    right: '10px',
                    top: '70px',
                    bottom: '0px',
                }} yAxis={_this.getYAxis()} tooltip={{ valueFormatter: _this.formatTooltipValue }} colors={_this.getColors()} transformSinglePointToBar height={240}/>); }}
        </chartZoom_1.default>
      </transitionChart_1.default>);
    };
    return ReleaseSessionsChart;
}(React.Component));
exports.default = react_1.withTheme(react_router_1.withRouter(ReleaseSessionsChart));
//# sourceMappingURL=releaseSessionsChart.jsx.map