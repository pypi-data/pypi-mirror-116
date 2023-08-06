Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var range_1 = tslib_1.__importDefault(require("lodash/range"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var qs = tslib_1.__importStar(require("query-string"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var input_1 = tslib_1.__importDefault(require("app/components/forms/input"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var locale_1 = require("app/locale");
var dates_1 = require("app/utils/dates");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var timePeriods = range_1.default(-1, -24 * 7, -1);
var defaultValue = '0.1';
function SessionPercent(_a) {
    var _this = this;
    var params = _a.params, api = _a.api, selection = _a.selection, organization = _a.organization;
    var _b = tslib_1.__read(react_1.useState(defaultValue), 2), threshold = _b[0], setThreshold = _b[1];
    var _c = tslib_1.__read(react_1.useState([]), 2), statsArr = _c[0], setStats = _c[1];
    var requestParams = {
        expand: 'sessions',
        display: 'sessions',
        project: selection.projects,
        query: 'is:unresolved',
        sort: 'freq',
    };
    var fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
        var _loop_1, idx;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _loop_1 = function (idx) {
                        var period, start, end, issuesQuery, results, _b, groupIds, query, groupStats, newData_1, _c;
                        return tslib_1.__generator(this, function (_d) {
                            switch (_d.label) {
                                case 0:
                                    period = timePeriods[idx];
                                    start = dates_1.getUtcDateString(moment_1.default().subtract(Math.abs(period), 'hours').toDate());
                                    end = dates_1.getUtcDateString(moment_1.default()
                                        .subtract(Math.abs(period) - 1, 'hours')
                                        .toDate());
                                    issuesQuery = tslib_1.__assign(tslib_1.__assign({}, requestParams), { limit: 5, start: start, end: end });
                                    _d.label = 1;
                                case 1:
                                    _d.trys.push([1, 3, , 4]);
                                    return [4 /*yield*/, api.requestPromise("/organizations/" + params.orgId + "/issues/", {
                                            method: 'GET',
                                            data: qs.stringify(issuesQuery),
                                        })];
                                case 2:
                                    results = _d.sent();
                                    return [3 /*break*/, 4];
                                case 3:
                                    _b = _d.sent();
                                    results = [];
                                    return [3 /*break*/, 4];
                                case 4:
                                    groupIds = results.map(function (group) { return group.id; });
                                    if (groupIds.length === 0) {
                                        setStats(function (prevState) {
                                            return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(prevState)), [[]]);
                                        });
                                        return [2 /*return*/, "continue"];
                                    }
                                    query = tslib_1.__assign(tslib_1.__assign({}, requestParams), { start: start, end: end, groups: groupIds });
                                    _d.label = 5;
                                case 5:
                                    _d.trys.push([5, 7, , 8]);
                                    return [4 /*yield*/, api.requestPromise("/organizations/" + params.orgId + "/issues-stats/", {
                                            method: 'GET',
                                            data: qs.stringify(query),
                                        })];
                                case 6:
                                    groupStats = _d.sent();
                                    newData_1 = groupStats.map(function (stats) {
                                        return {
                                            group: results.find(function (grp) { return grp.id === stats.id; }),
                                            percent: stats.sessionCount
                                                ? (Number(stats.count) / Number(stats.sessionCount)) * 100
                                                : 100,
                                        };
                                    });
                                    setStats(function (prevState) {
                                        return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(prevState)), [newData_1]);
                                    });
                                    return [3 /*break*/, 8];
                                case 7:
                                    _c = _d.sent();
                                    setStats(function (prevState) {
                                        return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(prevState)), [[]]);
                                    });
                                    return [3 /*break*/, 8];
                                case 8: return [2 /*return*/];
                            }
                        });
                    };
                    idx = 0;
                    _a.label = 1;
                case 1:
                    if (!(idx < timePeriods.length)) return [3 /*break*/, 4];
                    return [5 /*yield**/, _loop_1(idx)];
                case 2:
                    _a.sent();
                    _a.label = 3;
                case 3:
                    idx++;
                    return [3 /*break*/, 1];
                case 4: return [2 /*return*/];
            }
        });
    }); };
    react_1.useEffect(function () {
        fetchData();
    }, []);
    function getDiscoverUrl(_a, period) {
        var title = _a.title, id = _a.id, type = _a.type;
        var start = dates_1.getUtcDateString(moment_1.default()
            .subtract(Math.abs(period - 2), 'hours')
            .toDate());
        var end = dates_1.getUtcDateString(moment_1.default()
            .subtract(Math.abs(period) - 3, 'hours')
            .toDate());
        var discoverQuery = {
            id: undefined,
            name: title || type,
            fields: ['title', 'release', 'environment', 'user.display', 'timestamp'],
            orderby: '-timestamp',
            query: "issue.id:" + id,
            projects: selection.projects,
            version: 2,
            start: start,
            end: end,
        };
        var discoverView = eventView_1.default.fromSavedQuery(discoverQuery);
        return discoverView.getResultsViewUrlTarget(organization.slug);
    }
    return (<react_1.Fragment>
      <Layout.Header>
        <Layout.HeaderContent>
          <Layout.Title>{locale_1.t('Session Threshold Percent')}</Layout.Title>
          <StyledInput type="text" value={threshold} onChange={function (event) {
            setThreshold(event.target.value);
        }}/>
        </Layout.HeaderContent>
      </Layout.Header>
      <Layout.Body>
        <Layout.Main fullWidth>
          {timePeriods.map(function (period, idx) {
            var stats = statsArr[idx];
            var isLoading = stats === undefined;
            return (<react_1.Fragment key={idx}>
                <h4>{locale_1.tn('%s hour', '%s hours', period)}</h4>
                <ul>
                  {isLoading && locale_1.t('Loading\u2026')}
                  {!isLoading &&
                    stats
                        .filter(function (_a) {
                        var percent = _a.percent;
                        return percent > parseFloat(threshold);
                    })
                        .map(function (_a) {
                        var group = _a.group, percent = _a.percent;
                        return (<li key={group.id}>
                          {percent.toLocaleString()}% -{' '}
                          <link_1.default to={getDiscoverUrl(group, period)}>{group.title}</link_1.default>
                        </li>);
                    })}
                </ul>
              </react_1.Fragment>);
        })}
        </Layout.Main>
      </Layout.Body>
    </react_1.Fragment>);
}
function SessionPercentWrapper(props) {
    return (<feature_1.default features={['issue-percent-filters']} renderDisabled={function (p) { return <featureDisabled_1.default features={p.features} hideHelpToggle/>; }}>
      <SessionPercent {...props}/>
    </feature_1.default>);
}
exports.default = withApi_1.default(withGlobalSelection_1.default(withOrganization_1.default(SessionPercentWrapper)));
var StyledInput = styled_1.default(input_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 100px;\n"], ["\n  width: 100px;\n"])));
var templateObject_1;
//# sourceMappingURL=testSessionPercent.jsx.map