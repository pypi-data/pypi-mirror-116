Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var modal_1 = require("app/actionCreators/modal");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var OrganizationMembersWrapper = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationMembersWrapper, _super);
    function OrganizationMembersWrapper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.removeAccessRequest = function (id) {
            return _this.setState(function (state) { return ({
                requestList: state.requestList.filter(function (request) { return request.id !== id; }),
            }); });
        };
        _this.removeInviteRequest = function (id) {
            return _this.setState(function (state) { return ({
                inviteRequests: state.inviteRequests.filter(function (request) { return request.id !== id; }),
            }); });
        };
        _this.updateInviteRequest = function (id, data) {
            return _this.setState(function (state) {
                var inviteRequests = tslib_1.__spreadArray([], tslib_1.__read(state.inviteRequests));
                var inviteIndex = inviteRequests.findIndex(function (request) { return request.id === id; });
                inviteRequests[inviteIndex] = tslib_1.__assign(tslib_1.__assign({}, inviteRequests[inviteIndex]), data);
                return { inviteRequests: inviteRequests };
            });
        };
        return _this;
    }
    OrganizationMembersWrapper.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [
            ['inviteRequests', "/organizations/" + orgId + "/invite-requests/"],
            ['requestList', "/organizations/" + orgId + "/access-requests/"],
        ];
    };
    OrganizationMembersWrapper.prototype.getTitle = function () {
        var orgId = this.props.params.orgId;
        return routeTitle_1.default(locale_1.t('Members'), orgId, false);
    };
    Object.defineProperty(OrganizationMembersWrapper.prototype, "onRequestsTab", {
        get: function () {
            return location.pathname.includes('/requests/');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationMembersWrapper.prototype, "hasWriteAccess", {
        get: function () {
            var organization = this.props.organization;
            if (!organization || !organization.access) {
                return false;
            }
            return organization.access.includes('member:write');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationMembersWrapper.prototype, "showInviteRequests", {
        get: function () {
            return this.hasWriteAccess;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationMembersWrapper.prototype, "showNavTabs", {
        get: function () {
            var requestList = this.state.requestList;
            // show the requests tab if there are pending team requests,
            // or if the user has access to approve or deny invite requests
            return (requestList && requestList.length > 0) || this.showInviteRequests;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationMembersWrapper.prototype, "requestCount", {
        get: function () {
            var _a = this.state, requestList = _a.requestList, inviteRequests = _a.inviteRequests;
            var count = requestList.length;
            // if the user can't see the invite requests panel,
            // exclude those requests from the total count
            if (this.showInviteRequests) {
                count += inviteRequests.length;
            }
            return count ? count.toString() : null;
        },
        enumerable: false,
        configurable: true
    });
    OrganizationMembersWrapper.prototype.renderBody = function () {
        var _this = this;
        var children = this.props.children;
        var _a = this.state, requestList = _a.requestList, inviteRequests = _a.inviteRequests;
        var action = (<button_1.default priority="primary" size="small" onClick={function () {
                return modal_1.openInviteMembersModal({
                    onClose: function () {
                        _this.fetchData();
                    },
                    source: 'members_settings',
                });
            }} data-test-id="email-invite" icon={<icons_1.IconMail />}>
        {locale_1.t('Invite Members')}
      </button_1.default>);
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title="Members" action={action}/>
        {children &&
                react_1.cloneElement(children, {
                    requestList: requestList,
                    inviteRequests: inviteRequests,
                    onRemoveInviteRequest: this.removeInviteRequest,
                    onUpdateInviteRequest: this.updateInviteRequest,
                    onRemoveAccessRequest: this.removeAccessRequest,
                    showInviteRequests: this.showInviteRequests,
                })}
      </react_1.Fragment>);
    };
    return OrganizationMembersWrapper;
}(asyncView_1.default));
exports.default = withOrganization_1.default(OrganizationMembersWrapper);
//# sourceMappingURL=organizationMembersWrapper.jsx.map