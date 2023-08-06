Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var dashboards_1 = require("app/actionCreators/dashboards");
var indicator_1 = require("app/actionCreators/indicator");
var breadcrumbs_1 = tslib_1.__importDefault(require("app/components/breadcrumbs"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var controls_1 = tslib_1.__importDefault(require("./controls"));
var dashboard_1 = tslib_1.__importDefault(require("./dashboard"));
var data_1 = require("./data");
var title_1 = tslib_1.__importDefault(require("./title"));
var types_1 = require("./types");
var utils_1 = require("./utils");
var UNSAVED_MESSAGE = locale_1.t('You have unsaved changes, are you sure you want to leave?');
var HookHeader = hookOrDefault_1.default({ hookName: 'component:dashboards-header' });
var DashboardDetail = /** @class */ (function (_super) {
    tslib_1.__extends(DashboardDetail, _super);
    function DashboardDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dashboardState: _this.props.initialState,
            modifiedDashboard: _this.updateModifiedDashboard(_this.props.initialState),
        };
        _this.onEdit = function () {
            var dashboard = _this.props.dashboard;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'dashboards2.edit.start',
                eventName: 'Dashboards2: Edit start',
                organization_id: parseInt(_this.props.organization.id, 10),
            });
            _this.setState({
                dashboardState: types_1.DashboardState.EDIT,
                modifiedDashboard: utils_1.cloneDashboard(dashboard),
            });
        };
        _this.onRouteLeave = function () {
            if (![types_1.DashboardState.VIEW, types_1.DashboardState.PENDING_DELETE].includes(_this.state.dashboardState)) {
                return UNSAVED_MESSAGE;
            }
            return undefined;
        };
        _this.onUnload = function (event) {
            if ([types_1.DashboardState.VIEW, types_1.DashboardState.PENDING_DELETE].includes(_this.state.dashboardState)) {
                return;
            }
            event.preventDefault();
            event.returnValue = UNSAVED_MESSAGE;
        };
        _this.onDelete = function (dashboard) { return function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, location = _a.location;
            if (!(dashboard === null || dashboard === void 0 ? void 0 : dashboard.id)) {
                return;
            }
            var previousDashboardState = _this.state.dashboardState;
            _this.setState({ dashboardState: types_1.DashboardState.PENDING_DELETE }, function () {
                dashboards_1.deleteDashboard(api, organization.slug, dashboard.id)
                    .then(function () {
                    indicator_1.addSuccessMessage(locale_1.t('Dashboard deleted'));
                    analytics_1.trackAnalyticsEvent({
                        eventKey: 'dashboards2.delete',
                        eventName: 'Dashboards2: Delete',
                        organization_id: parseInt(_this.props.organization.id, 10),
                    });
                    react_router_1.browserHistory.replace({
                        pathname: "/organizations/" + organization.slug + "/dashboards/",
                        query: location.query,
                    });
                })
                    .catch(function () {
                    _this.setState({
                        dashboardState: previousDashboardState,
                    });
                });
            });
        }; };
        _this.onCancel = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location, params = _a.params;
            if (params.dashboardId) {
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'dashboards2.edit.cancel',
                    eventName: 'Dashboards2: Edit cancel',
                    organization_id: parseInt(_this.props.organization.id, 10),
                });
                _this.setState({
                    dashboardState: types_1.DashboardState.VIEW,
                    modifiedDashboard: null,
                });
                return;
            }
            analytics_1.trackAnalyticsEvent({
                eventKey: 'dashboards2.create.cancel',
                eventName: 'Dashboards2: Create cancel',
                organization_id: parseInt(_this.props.organization.id, 10),
            });
            react_router_1.browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/dashboards/",
                query: location.query,
            });
        };
        _this.onCommit = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, location = _a.location, dashboard = _a.dashboard, reloadData = _a.reloadData;
            var _b = _this.state, modifiedDashboard = _b.modifiedDashboard, dashboardState = _b.dashboardState;
            switch (dashboardState) {
                case types_1.DashboardState.CREATE: {
                    if (modifiedDashboard) {
                        dashboards_1.createDashboard(api, organization.slug, modifiedDashboard).then(function (newDashboard) {
                            indicator_1.addSuccessMessage(locale_1.t('Dashboard created'));
                            analytics_1.trackAnalyticsEvent({
                                eventKey: 'dashboards2.create.complete',
                                eventName: 'Dashboards2: Create complete',
                                organization_id: parseInt(organization.id, 10),
                            });
                            _this.setState({
                                dashboardState: types_1.DashboardState.VIEW,
                                modifiedDashboard: null,
                            });
                            // redirect to new dashboard
                            react_router_1.browserHistory.replace({
                                pathname: "/organizations/" + organization.slug + "/dashboard/" + newDashboard.id + "/",
                                query: tslib_1.__assign({}, location.query),
                            });
                        });
                    }
                    break;
                }
                case types_1.DashboardState.EDIT: {
                    // only update the dashboard if there are changes
                    if (modifiedDashboard) {
                        if (isEqual_1.default(dashboard, modifiedDashboard)) {
                            _this.setState({
                                dashboardState: types_1.DashboardState.VIEW,
                                modifiedDashboard: null,
                            });
                            return;
                        }
                        dashboards_1.updateDashboard(api, organization.slug, modifiedDashboard).then(function (newDashboard) {
                            indicator_1.addSuccessMessage(locale_1.t('Dashboard updated'));
                            analytics_1.trackAnalyticsEvent({
                                eventKey: 'dashboards2.edit.complete',
                                eventName: 'Dashboards2: Edit complete',
                                organization_id: parseInt(organization.id, 10),
                            });
                            _this.setState({
                                dashboardState: types_1.DashboardState.VIEW,
                                modifiedDashboard: null,
                            });
                            if (dashboard && newDashboard.id !== dashboard.id) {
                                react_router_1.browserHistory.replace({
                                    pathname: "/organizations/" + organization.slug + "/dashboard/" + newDashboard.id + "/",
                                    query: tslib_1.__assign({}, location.query),
                                });
                                return;
                            }
                            if (reloadData) {
                                reloadData();
                            }
                        });
                        return;
                    }
                    _this.setState({
                        dashboardState: types_1.DashboardState.VIEW,
                        modifiedDashboard: null,
                    });
                    break;
                }
                case types_1.DashboardState.VIEW:
                default: {
                    _this.setState({
                        dashboardState: types_1.DashboardState.VIEW,
                        modifiedDashboard: null,
                    });
                    break;
                }
            }
        };
        _this.setModifiedDashboard = function (dashboard) {
            _this.setState({
                modifiedDashboard: dashboard,
            });
        };
        _this.onSetWidgetToBeUpdated = function (widget) {
            _this.setState({ widgetToBeUpdated: widget });
        };
        _this.onUpdateWidget = function (widgets) {
            var modifiedDashboard = _this.state.modifiedDashboard;
            if (modifiedDashboard === null) {
                return;
            }
            _this.setState(function (state) { return (tslib_1.__assign(tslib_1.__assign({}, state), { widgetToBeUpdated: undefined, modifiedDashboard: tslib_1.__assign(tslib_1.__assign({}, state.modifiedDashboard), { widgets: widgets }) })); }, _this.updateRouteAfterSavingWidget);
        };
        return _this;
    }
    DashboardDetail.prototype.componentDidMount = function () {
        var _a = this.props, route = _a.route, router = _a.router;
        this.checkStateRoute();
        router.setRouteLeaveHook(route, this.onRouteLeave);
        window.addEventListener('beforeunload', this.onUnload);
    };
    DashboardDetail.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.location.pathname !== this.props.location.pathname) {
            this.checkStateRoute();
        }
    };
    DashboardDetail.prototype.componentWillUnmount = function () {
        window.removeEventListener('beforeunload', this.onUnload);
    };
    DashboardDetail.prototype.checkStateRoute = function () {
        var _a = this.props, router = _a.router, organization = _a.organization, params = _a.params;
        var dashboardId = params.dashboardId;
        var dashboardDetailsRoute = "/organizations/" + organization.slug + "/dashboard/" + dashboardId + "/";
        if (this.isWidgetBuilderRouter && !this.isEditing) {
            router.replace(dashboardDetailsRoute);
        }
        if (location.pathname === dashboardDetailsRoute && !!this.state.widgetToBeUpdated) {
            this.onSetWidgetToBeUpdated(undefined);
        }
    };
    DashboardDetail.prototype.updateRouteAfterSavingWidget = function () {
        if (this.isWidgetBuilderRouter) {
            var _a = this.props, router = _a.router, organization = _a.organization, params = _a.params;
            var dashboardId = params.dashboardId;
            if (dashboardId) {
                router.replace("/organizations/" + organization.slug + "/dashboard/" + dashboardId + "/");
                return;
            }
            router.replace("/organizations/" + organization.slug + "/dashboards/new/");
        }
    };
    DashboardDetail.prototype.updateModifiedDashboard = function (dashboardState) {
        var dashboard = this.props.dashboard;
        switch (dashboardState) {
            case types_1.DashboardState.CREATE:
                return utils_1.cloneDashboard(data_1.EMPTY_DASHBOARD);
            case types_1.DashboardState.EDIT:
                return utils_1.cloneDashboard(dashboard);
            default: {
                return null;
            }
        }
    };
    Object.defineProperty(DashboardDetail.prototype, "isEditing", {
        get: function () {
            var dashboardState = this.state.dashboardState;
            return [
                types_1.DashboardState.EDIT,
                types_1.DashboardState.CREATE,
                types_1.DashboardState.PENDING_DELETE,
            ].includes(dashboardState);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DashboardDetail.prototype, "isWidgetBuilderRouter", {
        get: function () {
            var _a = this.props, location = _a.location, params = _a.params, organization = _a.organization;
            var dashboardId = params.dashboardId;
            var newWidgetRoutes = [
                "/organizations/" + organization.slug + "/dashboards/new/widget/new/",
                "/organizations/" + organization.slug + "/dashboard/" + dashboardId + "/widget/new/",
            ];
            return newWidgetRoutes.includes(location.pathname) || this.isWidgetBuilderEditRouter;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DashboardDetail.prototype, "isWidgetBuilderEditRouter", {
        get: function () {
            var _a = this.props, location = _a.location, params = _a.params, organization = _a.organization;
            var dashboardId = params.dashboardId, widgetId = params.widgetId;
            var widgetEditRoutes = [
                "/organizations/" + organization.slug + "/dashboards/new/widget/" + widgetId + "/edit/",
                "/organizations/" + organization.slug + "/dashboard/" + dashboardId + "/widget/" + widgetId + "/edit/",
            ];
            return widgetEditRoutes.includes(location.pathname);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DashboardDetail.prototype, "dashboardTitle", {
        get: function () {
            var dashboard = this.props.dashboard;
            var modifiedDashboard = this.state.modifiedDashboard;
            return modifiedDashboard ? modifiedDashboard.title : dashboard.title;
        },
        enumerable: false,
        configurable: true
    });
    DashboardDetail.prototype.renderWidgetBuilder = function (dashboard) {
        var children = this.props.children;
        var _a = this.state, modifiedDashboard = _a.modifiedDashboard, widgetToBeUpdated = _a.widgetToBeUpdated;
        return react_1.isValidElement(children)
            ? react_1.cloneElement(children, {
                dashboard: modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard,
                onSave: this.onUpdateWidget,
                widget: widgetToBeUpdated,
            })
            : children;
    };
    DashboardDetail.prototype.renderDefaultDashboardDetail = function () {
        var _a = this.props, organization = _a.organization, dashboard = _a.dashboard, dashboards = _a.dashboards, params = _a.params, router = _a.router, location = _a.location;
        var _b = this.state, modifiedDashboard = _b.modifiedDashboard, dashboardState = _b.dashboardState;
        var dashboardId = params.dashboardId;
        return (<globalSelectionHeader_1.default skipLoadLastUsed={organization.features.includes('global-views')} defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: data_1.DEFAULT_STATS_PERIOD,
                },
            }}>
        <organization_1.PageContent>
          <lightWeightNoProjectMessage_1.default organization={organization}>
            <StyledPageHeader>
              <title_1.default dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} onUpdate={this.setModifiedDashboard} isEditing={this.isEditing}/>
              <controls_1.default organization={organization} dashboards={dashboards} onEdit={this.onEdit} onCancel={this.onCancel} onCommit={this.onCommit} onDelete={this.onDelete(dashboard)} dashboardState={dashboardState}/>
            </StyledPageHeader>
            <HookHeader organization={organization}/>
            <dashboard_1.default paramDashboardId={dashboardId} dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} organization={organization} isEditing={this.isEditing} onUpdate={this.onUpdateWidget} onSetWidgetToBeUpdated={this.onSetWidgetToBeUpdated} router={router} location={location}/>
          </lightWeightNoProjectMessage_1.default>
        </organization_1.PageContent>
      </globalSelectionHeader_1.default>);
    };
    DashboardDetail.prototype.renderDashboardDetail = function () {
        var _a = this.props, organization = _a.organization, dashboard = _a.dashboard, dashboards = _a.dashboards, params = _a.params, router = _a.router, location = _a.location;
        var _b = this.state, modifiedDashboard = _b.modifiedDashboard, dashboardState = _b.dashboardState;
        var dashboardId = params.dashboardId;
        return (<globalSelectionHeader_1.default skipLoadLastUsed={organization.features.includes('global-views')} defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: data_1.DEFAULT_STATS_PERIOD,
                },
            }}>
        <lightWeightNoProjectMessage_1.default organization={organization}>
          <Layout.Header>
            <Layout.HeaderContent>
              <breadcrumbs_1.default crumbs={[
                {
                    label: locale_1.t('Dashboards'),
                    to: "/organizations/" + organization.slug + "/dashboards/",
                },
                {
                    label: dashboardState === types_1.DashboardState.CREATE
                        ? locale_1.t('Create Dashboard')
                        : organization.features.includes('dashboards-edit') &&
                            dashboard.id === 'default-overview'
                            ? 'Default Dashboard'
                            : this.dashboardTitle,
                },
            ]}/>
              <Layout.Title>
                <title_1.default dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} onUpdate={this.setModifiedDashboard} isEditing={this.isEditing}/>
              </Layout.Title>
            </Layout.HeaderContent>
            <Layout.HeaderActions>
              <controls_1.default organization={organization} dashboards={dashboards} onEdit={this.onEdit} onCancel={this.onCancel} onCommit={this.onCommit} onDelete={this.onDelete(dashboard)} dashboardState={dashboardState}/>
            </Layout.HeaderActions>
          </Layout.Header>
          <Layout.Body>
            <Layout.Main fullWidth>
              <dashboard_1.default paramDashboardId={dashboardId} dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} organization={organization} isEditing={this.isEditing} onUpdate={this.onUpdateWidget} onSetWidgetToBeUpdated={this.onSetWidgetToBeUpdated} router={router} location={location}/>
            </Layout.Main>
          </Layout.Body>
        </lightWeightNoProjectMessage_1.default>
      </globalSelectionHeader_1.default>);
    };
    DashboardDetail.prototype.render = function () {
        var _a = this.props, organization = _a.organization, dashboard = _a.dashboard;
        if (this.isEditing && this.isWidgetBuilderRouter) {
            return this.renderWidgetBuilder(dashboard);
        }
        if (organization.features.includes('dashboards-edit')) {
            return this.renderDashboardDetail();
        }
        return this.renderDefaultDashboardDetail();
    };
    return DashboardDetail;
}(react_1.Component));
var StyledPageHeader = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n  grid-row-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(0, 1fr) max-content;\n    grid-column-gap: ", ";\n    height: 40px;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n  grid-row-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(0, 1fr) max-content;\n    grid-column-gap: ", ";\n    height: 40px;\n  }\n"])), space_1.default(2), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space_1.default(2), function (p) { return p.theme.breakpoints[1]; }, space_1.default(2));
exports.default = withApi_1.default(withOrganization_1.default(DashboardDetail));
var templateObject_1;
//# sourceMappingURL=detail.jsx.map