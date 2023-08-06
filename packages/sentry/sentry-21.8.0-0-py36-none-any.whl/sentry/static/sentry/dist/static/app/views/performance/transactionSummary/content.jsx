Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var transactionsList_1 = tslib_1.__importDefault(require("app/components/discover/transactionsList"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/events/searchBar"));
var globalSdkUpdateAlert_1 = tslib_1.__importDefault(require("app/components/globalSdkUpdateAlert"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var fields_1 = require("app/utils/discover/fields");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var cellAction_1 = require("app/views/eventsV2/table/cellAction");
var tags_1 = tslib_1.__importDefault(require("app/views/eventsV2/tags"));
var constants_2 = require("app/views/performance/transactionSummary/transactionVitals/constants");
var utils_2 = require("../utils");
var charts_1 = tslib_1.__importDefault(require("./charts"));
var filter_1 = tslib_1.__importStar(require("./filter"));
var header_1 = tslib_1.__importStar(require("./header"));
var relatedIssues_1 = tslib_1.__importDefault(require("./relatedIssues"));
var sidebarCharts_1 = tslib_1.__importDefault(require("./sidebarCharts"));
var statusBreakdown_1 = tslib_1.__importDefault(require("./statusBreakdown"));
var tagExplorer_1 = require("./tagExplorer");
var userStats_1 = tslib_1.__importDefault(require("./userStats"));
var utils_3 = require("./utils");
var SummaryContent = /** @class */ (function (_super) {
    tslib_1.__extends(SummaryContent, _super);
    function SummaryContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
        };
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var queryParams = getParams_1.getParams(tslib_1.__assign(tslib_1.__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            var searchQueryParams = omit_1.default(queryParams, 'cursor');
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        _this.generateTagUrl = function (key, value) {
            var location = _this.props.location;
            var query = utils_1.generateQueryWithTag(location.query, { key: key, value: value });
            return tslib_1.__assign(tslib_1.__assign({}, location), { query: query });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, _errors) {
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        _this.handleCellAction = function (column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location;
                var searchConditions = tokenizeSearch_1.tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeFilter('event.type');
                // no need to include transaction as its already in the query params
                searchConditions.removeFilter('transaction');
                cellAction_1.updateQuery(searchConditions, action, column, value);
                react_router_1.browserHistory.push({
                    pathname: location.pathname,
                    query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: searchConditions.formatString() }),
                });
            };
        };
        _this.handleTransactionsListSortChange = function (value) {
            var location = _this.props.location;
            var target = {
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { showTransactions: value, transactionCursor: undefined }),
            };
            react_router_1.browserHistory.push(target);
        };
        _this.handleAllEventsViewClick = function () {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.summary.view_in_transaction_events',
                eventName: 'Performance Views: View in All Events from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.handleDiscoverViewClick = function () {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.summary.view_in_discover',
                eventName: 'Performance Views: View in Discover from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.handleViewDetailsClick = function (_e) {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.summary.view_details',
                eventName: 'Performance Views: View Details from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        return _this;
    }
    SummaryContent.prototype.generateEventView = function (transactionsListEventView, transactionsListTitles) {
        var _a;
        var _b = this.props, location = _b.location, totalValues = _b.totalValues, spanOperationBreakdownFilter = _b.spanOperationBreakdownFilter;
        var selected = getTransactionsListSort(location, {
            p95: (_a = totalValues === null || totalValues === void 0 ? void 0 : totalValues.p95) !== null && _a !== void 0 ? _a : 0,
            spanOperationBreakdownFilter: spanOperationBreakdownFilter,
        }).selected;
        var sortedEventView = transactionsListEventView.withSorts([selected.sort]);
        if (spanOperationBreakdownFilter === filter_1.SpanOperationBreakdownFilter.None) {
            var fields = tslib_1.__spreadArray([], tslib_1.__read(sortedEventView.fields.slice(0, transactionsListTitles.length)));
            // omit "Operation Duration" column
            sortedEventView.fields = fields.filter(function (_a) {
                var field = _a.field;
                return !fields_1.isRelativeSpanOperationBreakdownField(field);
            });
        }
        return sortedEventView;
    };
    SummaryContent.prototype.render = function () {
        var _this = this;
        var _a;
        var eventView = this.props.eventView;
        var _b = this.props, transactionName = _b.transactionName, location = _b.location, organization = _b.organization, projects = _b.projects, isLoading = _b.isLoading, error = _b.error, totalValues = _b.totalValues, onChangeFilter = _b.onChangeFilter, onChangeThreshold = _b.onChangeThreshold, spanOperationBreakdownFilter = _b.spanOperationBreakdownFilter;
        var hasPerformanceEventsPage = organization.features.includes('performance-events-page');
        var hasPerformanceChartInterpolation = organization.features.includes('performance-chart-interpolation');
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        var query = queryString_1.decodeScalar(location.query.query, '');
        var totalCount = totalValues === null ? null : totalValues.count;
        // NOTE: This is not a robust check for whether or not a transaction is a front end
        // transaction, however it will suffice for now.
        var hasWebVitals = utils_2.isSummaryViewFrontendPageLoad(eventView, projects) ||
            (totalValues !== null &&
                constants_2.VITAL_GROUPS.some(function (group) {
                    return group.vitals.some(function (vital) {
                        var alias = fields_1.getAggregateAlias("percentile(" + vital + ", " + constants_2.PERCENTILE + ")");
                        return Number.isFinite(totalValues[alias]);
                    });
                }));
        var isFrontendView = utils_2.isSummaryViewFrontend(eventView, projects);
        var transactionsListTitles = [
            locale_1.t('event id'),
            locale_1.t('user'),
            locale_1.t('total duration'),
            locale_1.t('trace id'),
            locale_1.t('timestamp'),
        ];
        var transactionsListEventView = eventView.clone();
        if (organization.features.includes('performance-ops-breakdown')) {
            // update search conditions
            var spanOperationBreakdownConditions = filter_1.filterToSearchConditions(spanOperationBreakdownFilter, location);
            if (spanOperationBreakdownConditions) {
                eventView = eventView.clone();
                eventView.query = (eventView.query + " " + spanOperationBreakdownConditions).trim();
                transactionsListEventView = eventView.clone();
            }
            // update header titles of transactions list
            var operationDurationTableTitle = spanOperationBreakdownFilter === filter_1.SpanOperationBreakdownFilter.None
                ? locale_1.t('operation duration')
                : spanOperationBreakdownFilter + " duration";
            // add ops breakdown duration column as the 3rd column
            transactionsListTitles.splice(2, 0, operationDurationTableTitle);
            // span_ops_breakdown.relative is a preserved name and a marker for the associated
            // field renderer to be used to generate the relative ops breakdown
            var durationField = fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD;
            if (spanOperationBreakdownFilter !== filter_1.SpanOperationBreakdownFilter.None) {
                durationField = filter_1.filterToField(spanOperationBreakdownFilter);
            }
            var fields = tslib_1.__spreadArray([], tslib_1.__read(transactionsListEventView.fields));
            // add ops breakdown duration column as the 3rd column
            fields.splice(2, 0, { field: durationField });
            if (spanOperationBreakdownFilter === filter_1.SpanOperationBreakdownFilter.None) {
                fields.push.apply(fields, tslib_1.__spreadArray([], tslib_1.__read(fields_1.SPAN_OP_BREAKDOWN_FIELDS.map(function (field) {
                    return { field: field };
                }))));
            }
            transactionsListEventView.fields = fields;
        }
        var openAllEventsProps = {
            generatePerformanceTransactionEventsView: function () {
                var performanceTransactionEventsView = _this.generateEventView(transactionsListEventView, transactionsListTitles);
                performanceTransactionEventsView.query = query;
                return performanceTransactionEventsView;
            },
            handleOpenAllEventsClick: this.handleAllEventsViewClick,
        };
        var openInDiscoverProps = {
            generateDiscoverEventView: function () {
                return _this.generateEventView(transactionsListEventView, transactionsListTitles);
            },
            handleOpenInDiscoverClick: this.handleDiscoverViewClick,
        };
        return (<React.Fragment>
        <header_1.default eventView={eventView} location={location} organization={organization} projects={projects} transactionName={transactionName} currentTab={header_1.Tab.TransactionSummary} hasWebVitals="maybe" handleIncompatibleQuery={this.handleIncompatibleQuery} onChangeThreshold={onChangeThreshold}/>
        <Layout.Body>
          <StyledSdkUpdatesAlert />
          {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
          <Layout.Main>
            <Search>
              <filter_1.default organization={organization} currentFilter={spanOperationBreakdownFilter} onChangeFilter={onChangeFilter}/>
              <StyledSearchBar searchSource="transaction_summary" organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={this.handleSearch} maxQueryLength={constants_1.MAX_QUERY_LENGTH}/>
            </Search>
            <charts_1.default organization={organization} location={location} eventView={eventView} totalValues={totalCount} currentFilter={spanOperationBreakdownFilter} withoutZerofill={hasPerformanceChartInterpolation}/>
            <transactionsList_1.default location={location} organization={organization} eventView={transactionsListEventView} {...(hasPerformanceEventsPage ? openAllEventsProps : openInDiscoverProps)} showTransactions={queryString_1.decodeScalar(location.query.showTransactions, utils_3.TransactionFilterOptions.SLOW)} breakdown={filter_1.decodeFilterFromLocation(location)} titles={transactionsListTitles} handleDropdownChange={this.handleTransactionsListSortChange} generateLink={{
                id: utils_3.generateTransactionLink(transactionName),
                trace: utils_3.generateTraceLink(eventView.normalizeDateSelection(location)),
            }} baseline={transactionName} handleBaselineClick={this.handleViewDetailsClick} handleCellAction={this.handleCellAction} {...getTransactionsListSort(location, {
            p95: (_a = totalValues === null || totalValues === void 0 ? void 0 : totalValues.p95) !== null && _a !== void 0 ? _a : 0,
            spanOperationBreakdownFilter: spanOperationBreakdownFilter,
        })} forceLoading={isLoading}/>
            <feature_1.default requireAll={false} features={['performance-tag-explorer', 'performance-tag-page']}>
              <tagExplorer_1.TagExplorer eventView={eventView} organization={organization} location={location} projects={projects} transactionName={transactionName} currentFilter={spanOperationBreakdownFilter}/>
            </feature_1.default>
            <relatedIssues_1.default organization={organization} location={location} transaction={transactionName} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>
          </Layout.Main>
          <Layout.Side>
            <userStats_1.default organization={organization} location={location} isLoading={isLoading} hasWebVitals={hasWebVitals} error={error} totals={totalValues} transactionName={transactionName} eventView={eventView}/>
            {!isFrontendView && (<statusBreakdown_1.default eventView={eventView} organization={organization} location={location}/>)}
            <utils_3.SidebarSpacer />
            <sidebarCharts_1.default organization={organization} isLoading={isLoading} error={error} totals={totalValues} eventView={eventView}/>
            <utils_3.SidebarSpacer />
            <tags_1.default generateUrl={this.generateTagUrl} totalValues={totalCount} eventView={eventView} organization={organization} location={location}/>
          </Layout.Side>
        </Layout.Body>
      </React.Fragment>);
    };
    return SummaryContent;
}(React.Component));
function getFilterOptions(_a) {
    var p95 = _a.p95, spanOperationBreakdownFilter = _a.spanOperationBreakdownFilter;
    if (spanOperationBreakdownFilter === filter_1.SpanOperationBreakdownFilter.None) {
        return [
            {
                sort: { kind: 'asc', field: 'transaction.duration' },
                value: utils_3.TransactionFilterOptions.FASTEST,
                label: locale_1.t('Fastest Transactions'),
            },
            {
                query: [['transaction.duration', "<=" + p95.toFixed(0)]],
                sort: { kind: 'desc', field: 'transaction.duration' },
                value: utils_3.TransactionFilterOptions.SLOW,
                label: locale_1.t('Slow Transactions (p95)'),
            },
            {
                sort: { kind: 'desc', field: 'transaction.duration' },
                value: utils_3.TransactionFilterOptions.OUTLIER,
                label: locale_1.t('Outlier Transactions (p100)'),
            },
            {
                sort: { kind: 'desc', field: 'timestamp' },
                value: utils_3.TransactionFilterOptions.RECENT,
                label: locale_1.t('Recent Transactions'),
            },
        ];
    }
    var field = filter_1.filterToField(spanOperationBreakdownFilter);
    var operationName = spanOperationBreakdownFilter;
    return [
        {
            sort: { kind: 'asc', field: field },
            value: utils_3.TransactionFilterOptions.FASTEST,
            label: locale_1.t('Fastest %s Operations', operationName),
        },
        {
            query: [['transaction.duration', "<=" + p95.toFixed(0)]],
            sort: { kind: 'desc', field: field },
            value: utils_3.TransactionFilterOptions.SLOW,
            label: locale_1.t('Slow %s Operations (p95)', operationName),
        },
        {
            sort: { kind: 'desc', field: field },
            value: utils_3.TransactionFilterOptions.OUTLIER,
            label: locale_1.t('Outlier %s Operations (p100)', operationName),
        },
        {
            sort: { kind: 'desc', field: 'timestamp' },
            value: utils_3.TransactionFilterOptions.RECENT,
            label: locale_1.t('Recent Transactions'),
        },
    ];
}
function getTransactionsListSort(location, options) {
    var sortOptions = getFilterOptions(options);
    var urlParam = queryString_1.decodeScalar(location.query.showTransactions, utils_3.TransactionFilterOptions.SLOW);
    var selectedSort = sortOptions.find(function (opt) { return opt.value === urlParam; }) || sortOptions[0];
    return { selected: selectedSort, options: sortOptions };
}
var Search = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"])), space_1.default(3));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledSdkUpdatesAlert = styled_1.default(globalSdkUpdateAlert_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: function (p) { return <Layout.Main fullWidth {...p}/>; },
};
exports.default = withProjects_1.default(SummaryContent);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=content.jsx.map