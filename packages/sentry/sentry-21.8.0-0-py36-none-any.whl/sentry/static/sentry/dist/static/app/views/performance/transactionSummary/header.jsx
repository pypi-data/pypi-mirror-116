Object.defineProperty(exports, "__esModule", { value: true });
exports.Tab = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var guideAnchor_1 = require("app/components/assistant/guideAnchor");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var createAlertButton_1 = require("app/components/createAlertButton");
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var listLink_1 = tslib_1.__importDefault(require("app/components/links/listLink"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var hasMeasurementsQuery_1 = tslib_1.__importDefault(require("app/utils/performance/vitals/hasMeasurementsQuery"));
var queryString_1 = require("app/utils/queryString");
var breadcrumb_1 = tslib_1.__importDefault(require("app/views/performance/breadcrumb"));
var utils_1 = require("../landing/utils");
var utils_2 = require("./transactionEvents/utils");
var utils_3 = require("./transactionTags/utils");
var utils_4 = require("./transactionVitals/utils");
var teamKeyTransactionButton_1 = tslib_1.__importDefault(require("./teamKeyTransactionButton"));
var transactionThresholdButton_1 = tslib_1.__importDefault(require("./transactionThresholdButton"));
var utils_5 = require("./utils");
var Tab;
(function (Tab) {
    Tab[Tab["TransactionSummary"] = 0] = "TransactionSummary";
    Tab[Tab["RealUserMonitoring"] = 1] = "RealUserMonitoring";
    Tab[Tab["Tags"] = 2] = "Tags";
    Tab[Tab["Events"] = 3] = "Events";
})(Tab = exports.Tab || (exports.Tab = {}));
var TransactionHeader = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionHeader, _super);
    function TransactionHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.trackVitalsTabClick = function () {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.vitals.vitals_tab_clicked',
                eventName: 'Performance Views: Vitals tab clicked',
                organization_id: organization.id,
            });
        };
        _this.trackTagsTabClick = function () {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.tags.tags_tab_clicked',
                eventName: 'Performance Views: Tags tab clicked',
                organization_id: organization.id,
            });
        };
        _this.trackEventsTabClick = function () {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.events.events_tab_clicked',
                eventName: 'Performance Views: Events tab clicked',
                organization_id: organization.id,
            });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, errors) {
            var _a, _b;
            _this.trackAlertClick(errors);
            (_b = (_a = _this.props).handleIncompatibleQuery) === null || _b === void 0 ? void 0 : _b.call(_a, incompatibleAlertNoticeFn, errors);
        };
        _this.handleCreateAlertSuccess = function () {
            _this.trackAlertClick();
        };
        return _this;
    }
    TransactionHeader.prototype.trackAlertClick = function (errors) {
        var organization = this.props.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.summary.create_alert_clicked',
            eventName: 'Performance Views: Create alert clicked',
            organization_id: organization.id,
            status: errors ? 'error' : 'success',
            errors: errors,
            url: window.location.href,
        });
    };
    TransactionHeader.prototype.renderCreateAlertButton = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects;
        return (<createAlertButton_1.CreateAlertFromViewButton eventView={eventView} organization={organization} projects={projects} onIncompatibleQuery={this.handleIncompatibleQuery} onSuccess={this.handleCreateAlertSuccess} referrer="performance"/>);
    };
    TransactionHeader.prototype.renderKeyTransactionButton = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, transactionName = _a.transactionName;
        return (<teamKeyTransactionButton_1.default transactionName={transactionName} eventView={eventView} organization={organization}/>);
    };
    TransactionHeader.prototype.renderSettingsButton = function () {
        var _a = this.props, organization = _a.organization, transactionName = _a.transactionName, eventView = _a.eventView, onChangeThreshold = _a.onChangeThreshold;
        return (<feature_1.default organization={organization} features={['project-transaction-threshold-override']}>
        {function (_a) {
                var hasFeature = _a.hasFeature;
                return hasFeature ? (<guideAnchor_1.GuideAnchor target="project_transaction_threshold_override" position="bottom">
              <transactionThresholdButton_1.default organization={organization} transactionName={transactionName} eventView={eventView} onChangeThreshold={onChangeThreshold}/>
            </guideAnchor_1.GuideAnchor>) : (<button_1.default href={"/settings/" + organization.slug + "/performance/"} icon={<icons_1.IconSettings />} aria-label={locale_1.t('Settings')}/>);
            }}
      </feature_1.default>);
    };
    TransactionHeader.prototype.renderWebVitalsTab = function () {
        var _a = this.props, organization = _a.organization, eventView = _a.eventView, location = _a.location, projects = _a.projects, transactionName = _a.transactionName, currentTab = _a.currentTab, hasWebVitals = _a.hasWebVitals;
        var vitalsTarget = utils_4.vitalsRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: queryString_1.decodeScalar(location.query.project),
            query: location.query,
        });
        var tab = (<listLink_1.default data-test-id="web-vitals-tab" to={vitalsTarget} isActive={function () { return currentTab === Tab.RealUserMonitoring; }} onClick={this.trackVitalsTabClick}>
        {locale_1.t('Web Vitals')}
      </listLink_1.default>);
        switch (hasWebVitals) {
            case 'maybe':
                // need to check if the web vitals tab should be shown
                // frontend projects should always show the web vitals tab
                if (utils_1.getCurrentLandingDisplay(location, projects, eventView).field ===
                    utils_1.LandingDisplayField.FRONTEND_PAGELOAD) {
                    return tab;
                }
                // if it is not a frontend project, then we check to see if there
                // are any web vitals associated with the transaction recently
                return (<hasMeasurementsQuery_1.default location={location} orgSlug={organization.slug} eventView={eventView} transaction={transactionName} type="web">
            {function (_a) {
                    var hasMeasurements = _a.hasMeasurements;
                    return (hasMeasurements ? tab : null);
                }}
          </hasMeasurementsQuery_1.default>);
            case 'yes':
                // always show the web vitals tab
                return tab;
            case 'no':
            default:
                // never show the web vitals tab
                return null;
        }
    };
    TransactionHeader.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, transactionName = _a.transactionName, currentTab = _a.currentTab;
        var summaryTarget = utils_5.transactionSummaryRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: queryString_1.decodeScalar(location.query.project),
            query: location.query,
        });
        var tagsTarget = utils_3.tagsRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: queryString_1.decodeScalar(location.query.project),
            query: location.query,
        });
        var eventsTarget = utils_2.eventsRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: queryString_1.decodeScalar(location.query.project),
            query: location.query,
        });
        return (<Layout.Header>
        <Layout.HeaderContent>
          <breadcrumb_1.default organization={organization} location={location} transactionName={transactionName} realUserMonitoring={currentTab === Tab.RealUserMonitoring}/>
          <Layout.Title>{transactionName}</Layout.Title>
        </Layout.HeaderContent>
        <Layout.HeaderActions>
          <buttonBar_1.default gap={1}>
            <feature_1.default organization={organization} features={['incidents']}>
              {function (_a) {
            var hasFeature = _a.hasFeature;
            return hasFeature && _this.renderCreateAlertButton();
        }}
            </feature_1.default>
            {this.renderKeyTransactionButton()}
            {this.renderSettingsButton()}
          </buttonBar_1.default>
        </Layout.HeaderActions>
        <React.Fragment>
          <StyledNavTabs>
            <listLink_1.default to={summaryTarget} isActive={function () { return currentTab === Tab.TransactionSummary; }}>
              {locale_1.t('Overview')}
            </listLink_1.default>
            {this.renderWebVitalsTab()}
            <feature_1.default features={['organizations:performance-tag-page']}>
              <listLink_1.default to={tagsTarget} isActive={function () { return currentTab === Tab.Tags; }} onClick={this.trackTagsTabClick}>
                {locale_1.t('Tags')}
                <featureBadge_1.default type="beta" noTooltip/>
              </listLink_1.default>
            </feature_1.default>
            <feature_1.default features={['organizations:performance-events-page']}>
              <listLink_1.default to={eventsTarget} isActive={function () { return currentTab === Tab.Events; }} onClick={this.trackEventsTabClick}>
                {locale_1.t('All Events')}
                <featureBadge_1.default type="new" noTooltip/>
              </listLink_1.default>
            </feature_1.default>
          </StyledNavTabs>
        </React.Fragment>
      </Layout.Header>);
    };
    return TransactionHeader;
}(React.Component));
var StyledNavTabs = styled_1.default(navTabs_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"], ["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"])));
exports.default = TransactionHeader;
var templateObject_1;
//# sourceMappingURL=header.jsx.map