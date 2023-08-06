Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var react_2 = require("@emotion/react");
var api_1 = require("app/api");
var eventsChart_1 = tslib_1.__importDefault(require("app/components/charts/eventsChart"));
var eventsRequest_1 = tslib_1.__importDefault(require("app/components/charts/eventsRequest"));
var styles_1 = require("app/components/charts/styles");
var utils_1 = require("app/components/charts/utils");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var locale_1 = require("app/locale");
var types_1 = require("app/types");
var charts_1 = require("app/utils/discover/charts");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var data_1 = require("app/views/performance/data");
var utils_2 = require("../../utils");
function ReleaseEventsChart(_a) {
    var release = _a.release, project = _a.project, chartType = _a.chartType, value = _a.value, diff = _a.diff, theme = _a.theme, organization = _a.organization, api = _a.api, router = _a.router, period = _a.period, start = _a.start, end = _a.end, utc = _a.utc, location = _a.location;
    function getColors() {
        var colors = theme.charts.getColorPalette(14);
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.ERROR_COUNT:
                return [colors[12]];
            case types_1.ReleaseComparisonChartType.TRANSACTION_COUNT:
                return [theme.gray300];
            case types_1.ReleaseComparisonChartType.FAILURE_RATE:
                return [colors[9]];
            default:
                return undefined;
        }
    }
    function getQuery() {
        var releaseFilter = "release:" + release.version;
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.ERROR_COUNT:
                return new tokenizeSearch_1.QueryResults([
                    '!event.type:transaction',
                    releaseFilter,
                ]).formatString();
            case types_1.ReleaseComparisonChartType.TRANSACTION_COUNT:
                return new tokenizeSearch_1.QueryResults(['event.type:transaction', releaseFilter]).formatString();
            case types_1.ReleaseComparisonChartType.FAILURE_RATE:
                return new tokenizeSearch_1.QueryResults(['event.type:transaction', releaseFilter]).formatString();
            default:
                return '';
        }
    }
    function getField() {
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.ERROR_COUNT:
                return ['count()'];
            case types_1.ReleaseComparisonChartType.TRANSACTION_COUNT:
                return ['count()'];
            case types_1.ReleaseComparisonChartType.FAILURE_RATE:
                return ['failure_rate()'];
            default:
                return undefined;
        }
    }
    function getYAxis() {
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.ERROR_COUNT:
                return 'count()';
            case types_1.ReleaseComparisonChartType.TRANSACTION_COUNT:
                return 'count()';
            case types_1.ReleaseComparisonChartType.FAILURE_RATE:
                return 'failure_rate()';
            default:
                return '';
        }
    }
    function getHelp() {
        switch (chartType) {
            case types_1.ReleaseComparisonChartType.FAILURE_RATE:
                return data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE);
            default:
                return null;
        }
    }
    var projects = location.query.project;
    var environments = location.query.environment;
    var markLines = utils_2.generateReleaseMarkLines(release, project, theme, location);
    return (
    /**
     * EventsRequest is used to fetch the second series of Failure Rate chart.
     * First one is "This Release" - fetched as usual inside EventsChart
     * component and this one is "All Releases" that's shoehorned in place
     * of Previous Period via previousSeriesTransformer
     */
    <eventsRequest_1.default organization={organization} api={new api_1.Client()} period={period} project={projects} environment={environments} start={start} end={end} interval={utils_1.getInterval({ start: start, end: end, period: period, utc: utc }, 'high')} query="event.type:transaction" includePrevious={false} currentSeriesName={locale_1.t('All Releases')} yAxis={getYAxis()} field={getField()} confirmedQuery={chartType === types_1.ReleaseComparisonChartType.FAILURE_RATE} partial>
      {function (_a) {
            var timeseriesData = _a.timeseriesData, loading = _a.loading, reloading = _a.reloading;
            return (<eventsChart_1.default query={getQuery()} yAxis={getYAxis()} field={getField()} colors={getColors()} api={api} router={router} organization={organization} disableReleases disablePrevious showLegend projects={projects} environments={environments} start={start} end={end} period={period !== null && period !== void 0 ? period : undefined} utc={utc} currentSeriesName={locale_1.t('This Release') + (loading || reloading ? ' ' : '')} // HACK: trigger echarts rerender without remounting
             previousSeriesName={locale_1.t('All Releases')} disableableSeries={[locale_1.t('This Release'), locale_1.t('All Releases')]} chartHeader={<react_1.Fragment>
              <styles_1.HeaderTitleLegend>
                {utils_2.releaseComparisonChartTitles[chartType]}
                {getHelp() && (<questionTooltip_1.default size="sm" position="top" title={getHelp()}/>)}
              </styles_1.HeaderTitleLegend>

              <styles_1.HeaderValue>
                {value} {diff}
              </styles_1.HeaderValue>
            </react_1.Fragment>} legendOptions={{ right: 10, top: 0 }} chartOptions={{
                    grid: { left: '10px', right: '10px', top: '70px', bottom: '0px' },
                    tooltip: {
                        trigger: 'axis',
                        truncate: 80,
                        valueFormatter: function (val, label) {
                            if (label && Object.values(utils_2.releaseMarkLinesLabels).includes(label)) {
                                return '';
                            }
                            return charts_1.tooltipFormatter(val, getYAxis());
                        },
                    },
                }} usePageZoom height={240} seriesTransformer={function (series) { return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(series)), tslib_1.__read(markLines)); }} previousSeriesTransformer={function (series) {
                    if (chartType === types_1.ReleaseComparisonChartType.FAILURE_RATE) {
                        return timeseriesData === null || timeseriesData === void 0 ? void 0 : timeseriesData[0];
                    }
                    return series;
                }}/>);
        }}
    </eventsRequest_1.default>);
}
exports.default = withOrganization_1.default(react_2.withTheme(react_router_1.withRouter(withApi_1.default(ReleaseEventsChart))));
//# sourceMappingURL=releaseEventsChart.jsx.map