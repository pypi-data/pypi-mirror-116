Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var textField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textField"));
var NOTIFICATION_PROVIDERS = ['slack'];
var TeamNotificationSettings = /** @class */ (function (_super) {
    tslib_1.__extends(TeamNotificationSettings, _super);
    function TeamNotificationSettings() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TeamNotificationSettings.prototype.getTitle = function () {
        return 'Team Notification Settings';
    };
    TeamNotificationSettings.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, team = _a.team;
        return [
            [
                'teamDetails',
                "/teams/" + organization.slug + "/" + team.slug + "/",
                { query: { expand: ['externalTeams'] } },
            ],
            [
                'integrations',
                "/organizations/" + organization.slug + "/integrations/",
                { query: { includeConfig: 0 } },
            ],
        ];
    };
    TeamNotificationSettings.prototype.renderBody = function () {
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Notifications')}</panels_1.PanelHeader>
        <panels_1.PanelBody>{this.renderPanelBody()}</panels_1.PanelBody>
      </panels_1.Panel>);
    };
    TeamNotificationSettings.prototype.renderPanelBody = function () {
        var _a = this.state, teamDetails = _a.teamDetails, integrations = _a.integrations;
        var notificationIntegrations = integrations.filter(function (integration) {
            return NOTIFICATION_PROVIDERS.includes(integration.provider.key);
        });
        if (!notificationIntegrations.length) {
            return (<emptyMessage_1.default>
          {locale_1.t('No Notification Integrations have been installed yet.')}
        </emptyMessage_1.default>);
        }
        var externalTeams = (teamDetails.externalTeams || []).filter(function (externalTeam) {
            return NOTIFICATION_PROVIDERS.includes(externalTeam.provider);
        });
        if (!externalTeams.length) {
            return (<emptyMessage_1.default>
          <div>{locale_1.t('No teams have been linked yet.')}</div>
          <NotDisabledSubText>
            {locale_1.tct('Head over to Slack and type [code] to get started. [link].', {
                    code: <code>/sentry link team</code>,
                    link: <a>{locale_1.t('Learn more')}</a>,
                })}
          </NotDisabledSubText>
        </emptyMessage_1.default>);
        }
        var integrationsById = Object.fromEntries(notificationIntegrations.map(function (integration) { return [integration.id, integration]; }));
        return externalTeams.map(function (externalTeam) { return (<textField_1.default disabled key={externalTeam.id} label={<div>
            <NotDisabledText>
              {utils_1.toTitleCase(externalTeam.provider)}:
              {integrationsById[externalTeam.integrationId].name}
            </NotDisabledText>
            <NotDisabledSubText>
              {locale_1.tct('Unlink this channel in Slack with [code]. [link].', {
                    code: <code>/sentry unlink team</code>,
                    link: <a>{locale_1.t('Learn more')}</a>,
                })}
            </NotDisabledSubText>
          </div>} name="externalName" value={externalTeam.externalName}/>); });
    };
    return TeamNotificationSettings;
}(asyncView_1.default));
exports.default = withOrganization_1.default(TeamNotificationSettings);
var NotDisabledText = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  line-height: ", ";\n"], ["\n  color: ", ";\n  line-height: ", ";\n"])), function (p) { return p.theme.textColor; }, space_1.default(2));
var NotDisabledSubText = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.4;\n  margin-top: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.4;\n  margin-top: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeRelativeSmall; }, space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=teamNotifications.jsx.map