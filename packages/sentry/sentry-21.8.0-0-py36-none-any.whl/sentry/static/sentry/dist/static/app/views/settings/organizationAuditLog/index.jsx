Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var locale_1 = require("app/locale");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var auditLogList_1 = tslib_1.__importDefault(require("./auditLogList"));
// Please keep this list sorted
var EVENT_TYPES = [
    'member.invite',
    'member.add',
    'member.accept-invite',
    'member.remove',
    'member.edit',
    'member.join-team',
    'member.leave-team',
    'member.pending',
    'team.create',
    'team.edit',
    'team.remove',
    'project.create',
    'project.edit',
    'project.remove',
    'project.set-public',
    'project.set-private',
    'project.request-transfer',
    'project.accept-transfer',
    'org.create',
    'org.edit',
    'org.remove',
    'org.restore',
    'tagkey.remove',
    'projectkey.create',
    'projectkey.edit',
    'projectkey.remove',
    'projectkey.enable',
    'projectkey.disable',
    'sso.enable',
    'sso.disable',
    'sso.edit',
    'sso-identity.link',
    'api-key.create',
    'api-key.edit',
    'api-key.remove',
    'rule.create',
    'rule.edit',
    'rule.remove',
    'servicehook.create',
    'servicehook.edit',
    'servicehook.remove',
    'servicehook.enable',
    'servicehook.disable',
    'integration.add',
    'integration.edit',
    'integration.remove',
    'ondemand.edit',
    'trial.started',
    'plan.changed',
    'plan.cancelled',
];
var OrganizationAuditLog = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationAuditLog, _super);
    function OrganizationAuditLog() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleEventSelect = function (value) {
            // Dont update if event has not changed
            if (_this.props.location.query.event === value) {
                return;
            }
            react_router_1.browserHistory.push({
                pathname: _this.props.location.pathname,
                search: "?event=" + value,
            });
        };
        return _this;
    }
    OrganizationAuditLog.prototype.getEndpoints = function () {
        return [
            [
                'entryList',
                "/organizations/" + this.props.params.orgId + "/audit-logs/",
                {
                    query: this.props.location.query,
                },
            ],
        ];
    };
    OrganizationAuditLog.prototype.getTitle = function () {
        return routeTitle_1.default(locale_1.t('Audit Log'), this.props.organization.slug, false);
    };
    OrganizationAuditLog.prototype.renderBody = function () {
        var currentEventType = this.props.location.query.event;
        return (<auditLogList_1.default entries={this.state.entryList} pageLinks={this.state.entryListPageLinks} eventType={currentEventType} eventTypes={EVENT_TYPES} onEventSelect={this.handleEventSelect} {...this.props}/>);
    };
    return OrganizationAuditLog;
}(asyncView_1.default));
exports.default = withOrganization_1.default(OrganizationAuditLog);
//# sourceMappingURL=index.jsx.map