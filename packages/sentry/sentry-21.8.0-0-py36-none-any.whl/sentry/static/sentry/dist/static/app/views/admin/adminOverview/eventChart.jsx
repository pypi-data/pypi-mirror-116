Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var miniBarChart_1 = tslib_1.__importDefault(require("app/components/charts/miniBarChart"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var initialState = {
    error: false,
    loading: true,
    rawData: {
        'events.total': [],
        'events.dropped': [],
    },
    stats: { received: [], rejected: [] },
};
var EventChart = /** @class */ (function (_super) {
    tslib_1.__extends(EventChart, _super);
    function EventChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = initialState;
        _this.fetchData = function () {
            var statNameList = ['events.total', 'events.dropped'];
            statNameList.forEach(function (statName) {
                // query the organization stats via a separate call as its possible the project stats
                // are too heavy
                _this.props.api.request('/internal/stats/', {
                    method: 'GET',
                    data: {
                        since: _this.props.since,
                        resolution: _this.props.resolution,
                        key: statName,
                    },
                    success: function (data) {
                        _this.setState(function (prevState) {
                            var rawData = prevState.rawData;
                            rawData[statName] = data;
                            return {
                                rawData: rawData,
                            };
                        }, _this.requestFinished);
                    },
                    error: function () {
                        _this.setState({
                            error: true,
                        });
                    },
                });
            });
        };
        return _this;
    }
    EventChart.prototype.componentWillMount = function () {
        this.fetchData();
    };
    EventChart.prototype.componentWillReceiveProps = function (nextProps) {
        if (this.props.since !== nextProps.since) {
            this.setState(initialState, this.fetchData);
        }
    };
    EventChart.prototype.requestFinished = function () {
        var rawData = this.state.rawData;
        if (rawData['events.total'] && rawData['events.dropped']) {
            this.processOrgData();
        }
    };
    EventChart.prototype.processOrgData = function () {
        var rawData = this.state.rawData;
        var sReceived = {};
        var sRejected = {};
        var aReceived = [0, 0]; // received, points
        rawData['events.total'].forEach(function (point, idx) {
            var _a;
            var dReceived = point[1];
            var dRejected = (_a = rawData['events.dropped'][idx]) === null || _a === void 0 ? void 0 : _a[1];
            var ts = point[0];
            if (sReceived[ts] === undefined) {
                sReceived[ts] = dReceived;
                sRejected[ts] = dRejected;
            }
            else {
                sReceived[ts] += dReceived;
                sRejected[ts] += dRejected;
            }
            if (dReceived > 0) {
                aReceived[0] += dReceived;
                aReceived[1] += 1;
            }
        });
        this.setState({
            stats: {
                rejected: Object.keys(sRejected).map(function (ts) { return ({
                    name: parseInt(ts, 10) * 1000,
                    value: sRejected[ts] || 0,
                }); }),
                accepted: Object.keys(sReceived).map(function (ts) {
                    // total number of events accepted (received - rejected)
                    return ({ name: parseInt(ts, 10) * 1000, value: sReceived[ts] - sRejected[ts] });
                }),
            },
            loading: false,
        });
    };
    EventChart.prototype.getChartSeries = function () {
        var stats = this.state.stats;
        return [
            {
                seriesName: locale_1.t('Accepted'),
                data: stats.accepted,
                color: theme_1.default.blue300,
            },
            {
                seriesName: locale_1.t('Dropped'),
                data: stats.rejected,
                color: theme_1.default.red200,
            },
        ];
    };
    EventChart.prototype.render = function () {
        var _a = this.state, loading = _a.loading, error = _a.error;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        else if (error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        var series = this.getChartSeries();
        var colors = series.map(function (_a) {
            var color = _a.color;
            return color;
        });
        return (<miniBarChart_1.default series={series} colors={colors} height={110} stacked isGroupedByDate showTimeInTooltip labelYAxisExtents/>);
    };
    return EventChart;
}(react_1.Component));
exports.default = withApi_1.default(EventChart);
//# sourceMappingURL=eventChart.jsx.map