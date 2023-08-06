Object.defineProperty(exports, "__esModule", { value: true });
exports.OwnershipRules = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var sidebarSection_1 = tslib_1.__importDefault(require("../sidebarSection"));
var OwnershipRules = function (_a) {
    var project = _a.project, organization = _a.organization, issueId = _a.issueId, codeowners = _a.codeowners, isDismissed = _a.isDismissed, handleCTAClose = _a.handleCTAClose;
    var handleOpenCreateOwnershipRule = function () {
        modal_1.openCreateOwnershipRule({ project: project, organization: organization, issueId: issueId });
    };
    var showCTA = organization.features.includes('integrations-codeowners') &&
        !codeowners.length &&
        !isDismissed;
    var createRuleButton = (<access_1.default access={['project:write']}>
      <guideAnchor_1.default target="owners" position="bottom" offset={space_1.default(3)}>
        <button_1.default onClick={handleOpenCreateOwnershipRule} size="small">
          {locale_1.t('Create Ownership Rule')}
        </button_1.default>
      </guideAnchor_1.default>
    </access_1.default>);
    var codeOwnersCTA = (<Container dashedBorder>
      <HeaderContainer>
        <Header>{locale_1.t('Codeowners sync')}</Header> <featureBadge_1.default type="beta" noTooltip/>
        <DismissButton icon={<icons_1.IconClose size="xs"/>} priority="link" onClick={function () { return handleCTAClose(); }}/>
      </HeaderContainer>
      <Content>
        {locale_1.t('Import GitHub or GitLab CODEOWNERS files to automatically assign issues to the right people.')}
      </Content>
      <buttonBar_1.default gap={1}>
        <SetupButton size="small" priority="primary" href={"/settings/" + organization.slug + "/projects/" + project.slug + "/ownership/"} onClick={function () {
            return integrationUtil_1.trackIntegrationEvent('integrations.code_owners_cta_setup_clicked', {
                view: 'stacktrace_issue_details',
                project_id: project.id,
                organization: organization,
            });
        }}>
          {locale_1.t('Set It Up')}
        </SetupButton>
        <button_1.default size="small" external href="https://docs.sentry.io/product/issues/issue-owners/#code-owners" onClick={function () {
            return integrationUtil_1.trackIntegrationEvent('integrations.code_owners_cta_docs_clicked', {
                view: 'stacktrace_issue_details',
                project_id: project.id,
                organization: organization,
            });
        }}>
          {locale_1.t('Read Docs')}
        </button_1.default>
      </buttonBar_1.default>
    </Container>);
    return (<sidebarSection_1.default title={<react_1.Fragment>
          {locale_1.t('Ownership Rules')}
          <react_2.ClassNames>
            {function (_a) {
                var css = _a.css;
                return (<hovercard_1.default body={<HelpfulBody>
                    <p>
                      {locale_1.t('Ownership rules allow you to associate file paths and URLs to specific teams or users, so alerts can be routed to the right people.')}
                    </p>
                    <button_1.default href="https://docs.sentry.io/workflow/issue-owners/" priority="primary">
                      {locale_1.t('Learn more')}
                    </button_1.default>
                  </HelpfulBody>} containerClassName={css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                  display: flex;\n                  align-items: center;\n                "], ["\n                  display: flex;\n                  align-items: center;\n                "])))}>
                <StyledIconQuestion size="xs"/>
              </hovercard_1.default>);
            }}
          </react_2.ClassNames>
        </react_1.Fragment>}>
      {showCTA ? codeOwnersCTA : createRuleButton}
    </sidebarSection_1.default>);
};
exports.OwnershipRules = OwnershipRules;
var StyledIconQuestion = styled_1.default(icons_1.IconQuestion)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(0.5));
var HelpfulBody = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  text-align: center;\n"], ["\n  padding: ", ";\n  text-align: center;\n"])), space_1.default(1));
var Container = styled_1.default(panels_1.Panel)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  background: none;\n  display: flex;\n  flex-direction: column;\n  padding: ", ";\n"], ["\n  background: none;\n  display: flex;\n  flex-direction: column;\n  padding: ", ";\n"])), space_1.default(2));
var HeaderContainer = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content max-content 1fr;\n  align-items: flex-start;\n"], ["\n  display: grid;\n  grid-template-columns: max-content max-content 1fr;\n  align-items: flex-start;\n"])));
var Header = styled_1.default('h4')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  text-transform: uppercase;\n  font-weight: bold;\n  color: ", ";\n  font-size: ", ";\n"], ["\n  margin-bottom: ", ";\n  text-transform: uppercase;\n  font-weight: bold;\n  color: ", ";\n  font-size: ", ";\n"])), space_1.default(1), function (p) { return p.theme.gray400; }, function (p) { return p.theme.fontSizeMedium; });
var Content = styled_1.default('span')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.subText; }, space_1.default(2));
var SetupButton = styled_1.default(button_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  &:focus {\n    color: ", ";\n  }\n"], ["\n  &:focus {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.white; });
var DismissButton = styled_1.default(button_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  justify-self: flex-end;\n  color: ", ";\n"], ["\n  justify-self: flex-end;\n  color: ", ";\n"])), function (p) { return p.theme.gray400; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=ownershipRules.jsx.map