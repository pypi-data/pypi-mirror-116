Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var members_1 = require("app/actionCreators/members");
var organizations_1 = require("app/actionCreators/organizations");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var defaultSearchBar_1 = require("app/views/settings/components/defaultSearchBar");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var membersFilter_1 = tslib_1.__importDefault(require("./components/membersFilter"));
var inviteRequestRow_1 = tslib_1.__importDefault(require("./inviteRequestRow"));
var organizationMemberRow_1 = tslib_1.__importDefault(require("./organizationMemberRow"));
var MemberListHeader = hookOrDefault_1.default({
    hookName: 'component:member-list-header',
    defaultComponent: function () { return <panels_1.PanelHeader>{locale_1.t('Active Members')}</panels_1.PanelHeader>; },
});
var OrganizationMembersList = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationMembersList, _super);
    function OrganizationMembersList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.removeMember = function (id) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var orgId;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        orgId = this.props.params.orgId;
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + orgId + "/members/" + id + "/", {
                                method: 'DELETE',
                                data: {},
                            })];
                    case 1:
                        _a.sent();
                        this.setState(function (state) { return ({
                            members: state.members.filter(function (_a) {
                                var existingId = _a.id;
                                return existingId !== id;
                            }),
                        }); });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleRemove = function (_a) {
            var id = _a.id, name = _a.name;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var organization, orgName, _b;
                return tslib_1.__generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            organization = this.props.organization;
                            orgName = organization.slug;
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, this.removeMember(id)];
                        case 2:
                            _c.sent();
                            return [3 /*break*/, 4];
                        case 3:
                            _b = _c.sent();
                            indicator_1.addErrorMessage(locale_1.tct('Error removing [name] from [orgName]', { name: name, orgName: orgName }));
                            return [2 /*return*/];
                        case 4:
                            indicator_1.addSuccessMessage(locale_1.tct('Removed [name] from [orgName]', { name: name, orgName: orgName }));
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.handleLeave = function (_a) {
            var id = _a.id;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var organization, orgName, _b;
                return tslib_1.__generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            organization = this.props.organization;
                            orgName = organization.slug;
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, this.removeMember(id)];
                        case 2:
                            _c.sent();
                            return [3 /*break*/, 4];
                        case 3:
                            _b = _c.sent();
                            indicator_1.addErrorMessage(locale_1.tct('Error leaving [orgName]', { orgName: orgName }));
                            return [2 /*return*/];
                        case 4:
                            organizations_1.redirectToRemainingOrganization({ orgId: orgName, removeOrg: true });
                            indicator_1.addSuccessMessage(locale_1.tct('You left [orgName]', { orgName: orgName }));
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.handleSendInvite = function (_a) {
            var id = _a.id, expired = _a.expired;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _b;
                return tslib_1.__generator(this, function (_c) {
                    switch (_c.label) {
                        case 0:
                            this.setState(function (state) {
                                var _a;
                                return ({
                                    invited: tslib_1.__assign(tslib_1.__assign({}, state.invited), (_a = {}, _a[id] = 'loading', _a)),
                                });
                            });
                            _c.label = 1;
                        case 1:
                            _c.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, members_1.resendMemberInvite(this.api, {
                                    orgId: this.props.params.orgId,
                                    memberId: id,
                                    regenerate: expired,
                                })];
                        case 2:
                            _c.sent();
                            return [3 /*break*/, 4];
                        case 3:
                            _b = _c.sent();
                            this.setState(function (state) {
                                var _a;
                                return ({ invited: tslib_1.__assign(tslib_1.__assign({}, state.invited), (_a = {}, _a[id] = null, _a)) });
                            });
                            indicator_1.addErrorMessage(locale_1.t('Error sending invite'));
                            return [2 /*return*/];
                        case 4:
                            this.setState(function (state) {
                                var _a;
                                return ({ invited: tslib_1.__assign(tslib_1.__assign({}, state.invited), (_a = {}, _a[id] = 'success', _a)) });
                            });
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.updateInviteRequest = function (id, data) {
            return _this.setState(function (state) {
                var inviteRequests = tslib_1.__spreadArray([], tslib_1.__read(state.inviteRequests));
                var inviteIndex = inviteRequests.findIndex(function (request) { return request.id === id; });
                inviteRequests[inviteIndex] = tslib_1.__assign(tslib_1.__assign({}, inviteRequests[inviteIndex]), data);
                return { inviteRequests: inviteRequests };
            });
        };
        _this.removeInviteRequest = function (id) {
            return _this.setState(function (state) { return ({
                inviteRequests: state.inviteRequests.filter(function (request) { return request.id !== id; }),
            }); });
        };
        _this.handleInviteRequestAction = function (_a) {
            var inviteRequest = _a.inviteRequest, method = _a.method, data = _a.data, successMessage = _a.successMessage, errorMessage = _a.errorMessage, eventKey = _a.eventKey;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _b, params, organization, _c;
                return tslib_1.__generator(this, function (_d) {
                    switch (_d.label) {
                        case 0:
                            _b = this.props, params = _b.params, organization = _b.organization;
                            this.setState(function (state) {
                                var _a;
                                return ({
                                    inviteRequestBusy: tslib_1.__assign(tslib_1.__assign({}, state.inviteRequestBusy), (_a = {}, _a[inviteRequest.id] = true, _a)),
                                });
                            });
                            _d.label = 1;
                        case 1:
                            _d.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, this.api.requestPromise("/organizations/" + params.orgId + "/invite-requests/" + inviteRequest.id + "/", {
                                    method: method,
                                    data: data,
                                })];
                        case 2:
                            _d.sent();
                            this.removeInviteRequest(inviteRequest.id);
                            indicator_1.addSuccessMessage(successMessage);
                            advancedAnalytics_1.trackAdvancedAnalyticsEvent(eventKey, {
                                member_id: parseInt(inviteRequest.id, 10),
                                invite_status: inviteRequest.inviteStatus,
                                organization: organization,
                            });
                            return [3 /*break*/, 4];
                        case 3:
                            _c = _d.sent();
                            indicator_1.addErrorMessage(errorMessage);
                            return [3 /*break*/, 4];
                        case 4:
                            this.setState(function (state) {
                                var _a;
                                return ({
                                    inviteRequestBusy: tslib_1.__assign(tslib_1.__assign({}, state.inviteRequestBusy), (_a = {}, _a[inviteRequest.id] = false, _a)),
                                });
                            });
                            return [2 /*return*/];
                    }
                });
            });
        };
        _this.handleInviteRequestApprove = function (inviteRequest) {
            _this.handleInviteRequestAction({
                inviteRequest: inviteRequest,
                method: 'PUT',
                data: {
                    role: inviteRequest.role,
                    teams: inviteRequest.teams,
                    approve: 1,
                },
                successMessage: locale_1.tct('[email] has been invited', { email: inviteRequest.email }),
                errorMessage: locale_1.tct('Error inviting [email]', { email: inviteRequest.email }),
                eventKey: 'invite_request.approved',
            });
        };
        _this.handleInviteRequestDeny = function (inviteRequest) {
            _this.handleInviteRequestAction({
                inviteRequest: inviteRequest,
                method: 'DELETE',
                data: {},
                successMessage: locale_1.tct('Invite request for [email] denied', {
                    email: inviteRequest.email,
                }),
                errorMessage: locale_1.tct('Error denying invite request for [email]', {
                    email: inviteRequest.email,
                }),
                eventKey: 'invite_request.denied',
            });
        };
        return _this;
    }
    OrganizationMembersList.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { members: [], invited: {} });
    };
    OrganizationMembersList.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [
            ['members', "/organizations/" + orgId + "/members/", {}, { paginate: true }],
            [
                'member',
                "/organizations/" + orgId + "/members/me/",
                {},
                { allowError: function (error) { return error.status === 404; } },
            ],
            [
                'authProvider',
                "/organizations/" + orgId + "/auth-provider/",
                {},
                { allowError: function (error) { return error.status === 403; } },
            ],
            ['inviteRequests', "/organizations/" + orgId + "/invite-requests/"],
        ];
    };
    OrganizationMembersList.prototype.getTitle = function () {
        var orgId = this.props.organization.slug;
        return routeTitle_1.default(locale_1.t('Members'), orgId, false);
    };
    OrganizationMembersList.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, params = _a.params, organization = _a.organization, routes = _a.routes, teams = _a.teams;
        var _b = this.state, membersPageLinks = _b.membersPageLinks, members = _b.members, currentMember = _b.member, inviteRequests = _b.inviteRequests;
        var orgName = organization.name, access = organization.access;
        var canAddMembers = access.includes('member:write');
        var canRemove = access.includes('member:admin');
        var currentUser = configStore_1.default.get('user');
        // Find out if current user is the only owner
        var isOnlyOwner = !members.find(function (_a) {
            var role = _a.role, email = _a.email, pending = _a.pending;
            return role === 'owner' && email !== currentUser.email && !pending;
        });
        // Only admins/owners can remove members
        var requireLink = !!this.state.authProvider && this.state.authProvider.require_link;
        // eslint-disable-next-line react/prop-types
        var renderSearch = function (_a) {
            var defaultSearchBar = _a.defaultSearchBar, value = _a.value, handleChange = _a.handleChange;
            return (<SearchWrapperWithFilter>
        <dropdownMenu_1.default closeOnEscape>
          {function (_a) {
                    var _b;
                    var getActorProps = _a.getActorProps, isOpen = _a.isOpen;
                    return (<FilterWrapper>
              <button_1.default icon={<icons_1.IconSliders size="xs"/>} {...getActorProps({})}>
                {locale_1.t('Filter')}
              </button_1.default>
              {isOpen && (<StyledMembersFilter roles={(_b = currentMember === null || currentMember === void 0 ? void 0 : currentMember.roles) !== null && _b !== void 0 ? _b : constants_1.MEMBER_ROLES} query={value} onChange={function (query) { return handleChange(query); }}/>)}
            </FilterWrapper>);
                }}
        </dropdownMenu_1.default>
        {defaultSearchBar}
      </SearchWrapperWithFilter>);
        };
        return (<React.Fragment>
        <react_1.ClassNames>
          {function (_a) {
                var css = _a.css;
                return _this.renderSearchInput({
                    updateRoute: true,
                    placeholder: locale_1.t('Search Members'),
                    children: renderSearch,
                    className: css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                font-size: ", ";\n              "], ["\n                font-size: ", ";\n              "])), theme_1.default.fontSizeMedium),
                });
            }}
        </react_1.ClassNames>
        {inviteRequests && inviteRequests.length > 0 && (<panels_1.Panel>
            <panels_1.PanelHeader>
              <StyledPanelItem>
                <div>{locale_1.t('Pending Members')}</div>
                <div>{locale_1.t('Role')}</div>
                <div>{locale_1.t('Teams')}</div>
              </StyledPanelItem>
            </panels_1.PanelHeader>
            <panels_1.PanelBody>
              {inviteRequests.map(function (inviteRequest) {
                    var _a;
                    return (<inviteRequestRow_1.default key={inviteRequest.id} organization={organization} inviteRequest={inviteRequest} inviteRequestBusy={{}} allTeams={teams} allRoles={(_a = currentMember === null || currentMember === void 0 ? void 0 : currentMember.roles) !== null && _a !== void 0 ? _a : constants_1.MEMBER_ROLES} onApprove={_this.handleInviteRequestApprove} onDeny={_this.handleInviteRequestDeny} onUpdate={function (data) { return _this.updateInviteRequest(inviteRequest.id, data); }}/>);
                })}
            </panels_1.PanelBody>
          </panels_1.Panel>)}
        <panels_1.Panel data-test-id="org-member-list">
          <MemberListHeader members={members} organization={organization}/>
          <panels_1.PanelBody>
            {members.map(function (member) { return (<organizationMemberRow_1.default routes={routes} params={params} key={member.id} member={member} status={_this.state.invited[member.id]} orgName={orgName} memberCanLeave={!isOnlyOwner} currentUser={currentUser} canRemoveMembers={canRemove} canAddMembers={canAddMembers} requireLink={requireLink} onSendInvite={_this.handleSendInvite} onRemove={_this.handleRemove} onLeave={_this.handleLeave}/>); })}
            {members.length === 0 && (<emptyMessage_1.default>{locale_1.t('No members found.')}</emptyMessage_1.default>)}
          </panels_1.PanelBody>
        </panels_1.Panel>

        <pagination_1.default pageLinks={membersPageLinks}/>
      </React.Fragment>);
    };
    return OrganizationMembersList;
}(asyncView_1.default));
var SearchWrapperWithFilter = styled_1.default(defaultSearchBar_1.SearchWrapper)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  margin-top: 0;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  margin-top: 0;\n"])));
var FilterWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledMembersFilter = styled_1.default(membersFilter_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  right: 0;\n  top: 42px;\n  z-index: ", ";\n\n  &:before,\n  &:after {\n    position: absolute;\n    top: -16px;\n    right: 32px;\n    content: '';\n    height: 16px;\n    width: 16px;\n    border: 8px solid transparent;\n    border-bottom-color: ", ";\n  }\n\n  &:before {\n    margin-top: -1px;\n    border-bottom-color: ", ";\n  }\n"], ["\n  position: absolute;\n  right: 0;\n  top: 42px;\n  z-index: ", ";\n\n  &:before,\n  &:after {\n    position: absolute;\n    top: -16px;\n    right: 32px;\n    content: '';\n    height: 16px;\n    width: 16px;\n    border: 8px solid transparent;\n    border-bottom-color: ", ";\n  }\n\n  &:before {\n    margin-top: -1px;\n    border-bottom-color: ", ";\n  }\n"])), function (p) { return p.theme.zIndex.dropdown; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; });
var StyledPanelItem = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(150px, auto) minmax(100px, 140px) 420px;\n  grid-gap: ", ";\n  align-items: center;\n  width: 100%;\n"], ["\n  display: grid;\n  grid-template-columns: minmax(150px, auto) minmax(100px, 140px) 420px;\n  grid-gap: ", ";\n  align-items: center;\n  width: 100%;\n"])), space_1.default(2));
exports.default = withTeams_1.default(withOrganization_1.default(OrganizationMembersList));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=organizationMembersList.jsx.map