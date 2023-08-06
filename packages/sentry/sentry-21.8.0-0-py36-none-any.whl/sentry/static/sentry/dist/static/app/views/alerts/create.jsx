Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var guid_1 = require("app/utils/guid");
var builderBreadCrumbs_1 = tslib_1.__importDefault(require("app/views/alerts/builder/builderBreadCrumbs"));
var create_1 = tslib_1.__importDefault(require("app/views/alerts/incidentRules/create"));
var issueRuleEditor_1 = tslib_1.__importDefault(require("app/views/alerts/issueRuleEditor"));
var options_1 = require("app/views/alerts/wizard/options");
var utils_1 = require("app/views/alerts/wizard/utils");
var Create = /** @class */ (function (_super) {
    tslib_1.__extends(Create, _super);
    function Create() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        /** Used to track analytics within one visit to the creation page */
        _this.sessionId = guid_1.uniqueId();
        return _this;
    }
    Create.prototype.getInitialState = function () {
        var _a;
        var _b = this.props, organization = _b.organization, location = _b.location, project = _b.project;
        var _c = (_a = location === null || location === void 0 ? void 0 : location.query) !== null && _a !== void 0 ? _a : {}, createFromDiscover = _c.createFromDiscover, createFromWizard = _c.createFromWizard, aggregate = _c.aggregate, dataset = _c.dataset, eventTypes = _c.eventTypes;
        var alertType = 'issue';
        // Alerts can only be created via create from discover or alert wizard
        if (createFromDiscover) {
            alertType = 'metric';
        }
        else if (createFromWizard) {
            if (aggregate && dataset && eventTypes) {
                alertType = 'metric';
            }
            else {
                // Just to be explicit
                alertType = 'issue';
            }
        }
        else {
            react_router_1.browserHistory.replace("/organizations/" + organization.slug + "/alerts/" + project.slug + "/wizard");
        }
        return { alertType: alertType };
    };
    Create.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'new_alert_rule.viewed',
            eventName: 'New Alert Rule: Viewed',
            organization_id: organization.id,
            project_id: project.id,
            session_id: this.sessionId,
            alert_type: this.state.alertType,
        });
    };
    Create.prototype.render = function () {
        var _a;
        var _b = this.props, hasMetricAlerts = _b.hasMetricAlerts, organization = _b.organization, project = _b.project, projectId = _b.params.projectId, location = _b.location, routes = _b.routes;
        var alertType = this.state.alertType;
        var _c = (_a = location === null || location === void 0 ? void 0 : location.query) !== null && _a !== void 0 ? _a : {}, aggregate = _c.aggregate, dataset = _c.dataset, eventTypes = _c.eventTypes, createFromWizard = _c.createFromWizard, createFromDiscover = _c.createFromDiscover;
        var wizardTemplate = { aggregate: aggregate, dataset: dataset, eventTypes: eventTypes };
        var eventView = createFromDiscover ? eventView_1.default.fromLocation(location) : undefined;
        var wizardAlertType;
        if (createFromWizard && alertType === 'metric') {
            wizardAlertType = wizardTemplate
                ? utils_1.getAlertTypeFromAggregateDataset(wizardTemplate)
                : 'issues';
        }
        var title = locale_1.t('New Alert Rule');
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={title} projectSlug={projectId}/>

        <Layout.Header>
          <StyledHeaderContent>
            <builderBreadCrumbs_1.default hasMetricAlerts={hasMetricAlerts} orgSlug={organization.slug} alertName={locale_1.t('Set Conditions')} title={wizardAlertType ? locale_1.t('Select Alert') : title} projectSlug={projectId} routes={routes} location={location} canChangeProject/>
            <Layout.Title>
              {wizardAlertType
                ? locale_1.t('Set Conditions for') + " " + options_1.AlertWizardAlertNames[wizardAlertType]
                : title}
            </Layout.Title>
          </StyledHeaderContent>
        </Layout.Header>
        <AlertConditionsBody>
          <StyledLayoutMain fullWidth>
            {(!hasMetricAlerts || alertType === 'issue') && (<issueRuleEditor_1.default {...this.props} project={project}/>)}

            {hasMetricAlerts && alertType === 'metric' && (<create_1.default {...this.props} eventView={eventView} wizardTemplate={wizardTemplate} sessionId={this.sessionId} project={project} isCustomMetric={wizardAlertType === 'custom'}/>)}
          </StyledLayoutMain>
        </AlertConditionsBody>
      </react_1.Fragment>);
    };
    return Create;
}(react_1.Component));
var AlertConditionsBody = styled_1.default(Layout.Body)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: -", ";\n"], ["\n  margin-bottom: -", ";\n"])), space_1.default(3));
var StyledLayoutMain = styled_1.default(Layout.Main)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  max-width: 1000px;\n"], ["\n  max-width: 1000px;\n"])));
var StyledHeaderContent = styled_1.default(Layout.HeaderContent)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  overflow: visible;\n"], ["\n  overflow: visible;\n"])));
exports.default = Create;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=create.jsx.map